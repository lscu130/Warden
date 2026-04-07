#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块说明：
该脚本用于从 PhishStats 公共 API 抓取一个完整自然日内的 URL，
并按两个 score 档位分别导出为 TXT 文件：
1) score > 8
2) 5 < score < 8

设计原则：
- 仅使用 Python 标准库，避免新增第三方依赖。
- 优先使用官方文档明确给出的 API 能力：分页、排序、字段读取。
- 由于官方公开示例未明确展示 date 字段的服务端范围过滤，本脚本采用：
  “按 date 倒序分页 + 本地单日过滤”的保守实现。
- 输出为纯文本，一行一个 URL，便于后续人工审查或脚本消费。
"""

from __future__ import annotations

# =========================
# 模块导入
# 作用：提供命令行解析、日期处理、HTTP 请求、JSON 解析与路径操作能力。
# =========================
import argparse
import json
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# =========================
# 常量定义
# 作用：集中维护 API 地址、分页大小、速率控制和输出命名规则。
# =========================
API_BASE_URL = "https://api.phishstats.info/api/phishing"
PAGE_SIZE = 100
REQUEST_INTERVAL_SECONDS = 6.0  # 基于实际 429 情况，使用更保守的间隔
USER_AGENT = "Warden-PhishStats-Fetcher/1.0"


# =========================
# 参数解析模块
# 作用：解析命令行参数；默认抓昨天，也支持显式指定目标日期。
# =========================
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch PhishStats URLs for one complete target day and export two TXT files: "
            "score > 8, and 5 < score < 8."
        )
    )
    parser.add_argument(
        "--start-date",
        default=None,
        help="Deprecated alias for --target-date. The script fetches only that exact day.",
    )
    parser.add_argument(
        "--target-date",
        default=None,
        help="Target date in YYYY/MM/DD or YYYY-MM-DD format. If omitted, the script fetches yesterday.",
    )
    parser.add_argument(
        "--output-dir",
        default="./phishstats_output",
        help="Directory to store TXT outputs. Default: ./phishstats_output",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Optional safety cap for pagination. 0 means no explicit cap.",
    )
    return parser.parse_args()


# =========================
# 输入处理模块
# 作用：统一解析目标日期。默认抓昨天；显式输入时只抓那一天。
# =========================
def get_target_date(start_date_raw: Optional[str], target_date_raw: Optional[str]) -> date:
    if start_date_raw and target_date_raw:
        raise ValueError("请只传一个日期参数：--target-date 或兼容别名 --start-date，不能同时传。")

    raw_value = target_date_raw or start_date_raw
    today = date.today()
    if raw_value is None:
        return today - timedelta(days=1)

    parsed = parse_user_date(raw_value)
    if parsed is None:
        raise ValueError(
            "无效日期格式。仅支持 YYYY/MM/DD 或 YYYY-MM-DD，例如 2026/03/29。"
        )
    if parsed >= today:
        raise ValueError(f"目标日期必须是完整自然日，不能是今天或未来日期。今天是 {today.isoformat()}。")
    return parsed


# =========================
# 日期解析模块（用户输入）
# 作用：解析用户输入日期。
# =========================
def parse_user_date(raw_value: str) -> Optional[date]:
    cleaned = raw_value.strip()
    for fmt in ("%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None


# =========================
# 日期解析模块（API 字段）
# 作用：尽量容错地解析 API 返回的 date/date_update 字段。
# 说明：官方 FAQ 说明存在 date 字段，但公开示例未固定展示具体字符串格式。
# 因此这里做多格式兼容，避免因小范围格式变化导致全脚本失效。
# =========================
def parse_api_date(raw_value: Any) -> Optional[date]:
    if raw_value is None:
        return None

    if isinstance(raw_value, (int, float)):
        # 兼容时间戳秒值
        try:
            return datetime.utcfromtimestamp(raw_value).date()
        except (OverflowError, OSError, ValueError):
            return None

    text = str(raw_value).strip()
    if not text:
        return None

    # 常见 ISO 形式兼容：结尾 Z 改写为 +00:00 便于 fromisoformat 解析
    iso_candidate = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(iso_candidate).date()
    except ValueError:
        pass

    # 去掉部分 API 或第三方代理常见的小数秒 / 时区残留后再试
    normalized = text.replace("T", " ")
    if "+" in normalized:
        normalized = normalized.split("+", 1)[0].strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1].strip()

    candidate_formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
    )
    for fmt in candidate_formats:
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue

    return None


# =========================
# HTTP 请求模块
# 作用：向 PhishStats API 发起 GET 请求并返回 JSON 数组。
# =========================
def fetch_page(page_number: int) -> List[Dict[str, Any]]:
    params = {
        "_sort": "-date",
        "_p": page_number,
        "_size": PAGE_SIZE,
    }
    url = f"{API_BASE_URL}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})

    with urlopen(request, timeout=30) as response:
        payload = response.read().decode("utf-8")
        data = json.loads(payload)

    if not isinstance(data, list):
        raise ValueError("Unexpected API response: expected a JSON list.")

    return data


# =========================
# 记录分类模块
# 作用：按用户起始日期、今天日期、score 档位对单条记录进行判断。
# 返回：
# - bucket: 'gt8' / 'gt5lt8' / None
# - record_date: 解析后的日期，供分页终止逻辑使用
# =========================
def classify_record(
    record: Dict[str, Any],
    start_date: date,
    end_date: date,
) -> Tuple[Optional[str], Optional[date]]:
    record_date = parse_api_date(record.get("date"))
    if record_date is None:
        return None, None

    if record_date < start_date or record_date > end_date:
        return None, record_date

    score = record.get("score")
    try:
        score_value = float(score)
    except (TypeError, ValueError):
        return None, record_date

    if score_value > 8:
        return "gt8", record_date
    if 5 < score_value < 8:
        return "gt5lt8", record_date
    return None, record_date


# =========================
# 主抓取模块
# 作用：分页抓取、按时间范围与 score 档位收集 URL，并在可安全终止时停止翻页。
# 终止策略：
# - API 返回空页：终止
# - 当前页所有可解析日期都早于起始日期：终止
# - 如设置了 max_pages，则到达上限后终止
# =========================
def collect_urls(
    start_date: date,
    end_date: date,
    max_pages: int = 0,
) -> Tuple[List[str], List[str], Dict[str, int]]:
    gt8_urls: List[str] = []
    gt5lt8_urls: List[str] = []
    seen_gt8 = set()
    seen_gt5lt8 = set()

    stats = {
        "pages_fetched": 0,
        "records_seen": 0,
        "records_in_range": 0,
        "records_date_unparsed": 0,
        "gt8_count": 0,
        "gt5lt8_count": 0,
    }

    page_number = 1
    while True:
        if max_pages > 0 and page_number > max_pages:
            break

        page_records = fetch_page(page_number)
        stats["pages_fetched"] += 1

        if not page_records:
            break

        page_has_any_in_range = False
        parsed_dates_in_page: List[date] = []

        for record in page_records:
            stats["records_seen"] += 1
            bucket, record_date = classify_record(record, start_date, end_date)
            if record_date is None:
                stats["records_date_unparsed"] += 1
                continue

            parsed_dates_in_page.append(record_date)

            if start_date <= record_date <= end_date:
                page_has_any_in_range = True
                stats["records_in_range"] += 1

            url = record.get("url")
            if not url or bucket is None:
                continue

            url_text = str(url).strip()
            if not url_text:
                continue

            if bucket == "gt8":
                if url_text not in seen_gt8:
                    seen_gt8.add(url_text)
                    gt8_urls.append(url_text)
                    stats["gt8_count"] += 1
            elif bucket == "gt5lt8":
                if url_text not in seen_gt5lt8:
                    seen_gt5lt8.add(url_text)
                    gt5lt8_urls.append(url_text)
                    stats["gt5lt8_count"] += 1

        # 若当前页的所有可解析日期均已早于起始日期，则后续页只会更旧，可安全停止。
        if parsed_dates_in_page:
            newest = max(parsed_dates_in_page)
            oldest = min(parsed_dates_in_page)

            # 理论上按 -date 排序，newest >= oldest。这里不依赖严格单页排序，只用 oldest 判停。
            if oldest < start_date and not page_has_any_in_range:
                break

            # 若整页都已早于起始日期，也可终止。
            if newest < start_date:
                break

        page_number += 1
        time.sleep(REQUEST_INTERVAL_SECONDS)

    return gt8_urls, gt5lt8_urls, stats


# =========================
# 输出模块
# 作用：将 URL 列表写入 TXT 文件，一行一个 URL。
# =========================
def write_txt(file_path: Path, urls: Sequence[str]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8", newline="\n") as f:
        for url in urls:
            f.write(url)
            f.write("\n")


# =========================
# 文件命名模块
# 作用：生成稳定、可读的输出文件名，按运行当天日期命名。
# =========================
def build_output_paths(output_dir: Path, run_date: date) -> Tuple[Path, Path]:
    run_token = run_date.strftime("%Y%m%d")

    gt8_path = output_dir / f"phishstats_urls_score_gt_8_{run_token}.txt"
    gt5lt8_path = output_dir / f"phishstats_urls_score_gt_5_lt_8_{run_token}.txt"
    return gt8_path, gt5lt8_path


# =========================
# 结果展示模块
# 作用：向终端输出本次抓取的统计信息和产物路径。
# =========================
def print_summary(
    target_date: date,
    run_date: date,
    gt8_urls: Sequence[str],
    gt5lt8_urls: Sequence[str],
    stats: Dict[str, int],
    gt8_path: Path,
    gt5lt8_path: Path,
) -> None:
    print("=" * 72)
    print("PhishStats URL 抓取完成")
    print(f"目标完整日期: {target_date.isoformat()}")
    print(f"产物命名日期: {run_date.isoformat()}")
    print(f"抓取页数: {stats['pages_fetched']}")
    print(f"扫描记录数: {stats['records_seen']}")
    print(f"日期可解析且在范围内的记录数: {stats['records_in_range']}")
    print(f"日期无法解析的记录数: {stats['records_date_unparsed']}")
    print(f"score > 8 URL 数量: {len(gt8_urls)}")
    print(f"5 < score < 8 URL 数量: {len(gt5lt8_urls)}")
    print(f"输出文件 1: {gt8_path}")
    print(f"输出文件 2: {gt5lt8_path}")
    print("=" * 72)


# =========================
# 主流程模块
# 作用：串联参数解析、日期校验、抓取、导出与结果输出。
# =========================
def main() -> int:
    args = parse_args()

    try:
        target_date = get_target_date(args.start_date, args.target_date)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).resolve()
    run_date = date.today()

    try:
        gt8_urls, gt5lt8_urls, stats = collect_urls(
            start_date=target_date,
            end_date=target_date,
            max_pages=args.max_pages,
        )
    except HTTPError as exc:
        print(f"[ERROR] HTTP error while requesting PhishStats API: {exc}", file=sys.stderr)
        return 3
    except URLError as exc:
        print(f"[ERROR] Network error while requesting PhishStats API: {exc}", file=sys.stderr)
        return 4
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Failed to parse API JSON response: {exc}", file=sys.stderr)
        return 5
    except Exception as exc:  # 保留兜底，避免脚本直接抛栈退出
        print(f"[ERROR] Unexpected failure: {exc}", file=sys.stderr)
        return 6

    gt8_path, gt5lt8_path = build_output_paths(output_dir, run_date)
    write_txt(gt8_path, gt8_urls)
    write_txt(gt5lt8_path, gt5lt8_urls)

    print_summary(target_date, run_date, gt8_urls, gt5lt8_urls, stats, gt8_path, gt5lt8_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
