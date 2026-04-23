#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
build_manifest.py

用途：
- 扫描 Warden 当前冻结数据结构下的成功样本目录
- 基于 TRAINSET_V1 规则生成统一 manifest.jsonl
- 不修改样本目录本体，不重写上游文件，只做读取与清单导出

说明：
- 本脚本按当前仓库中的真实数据结构对齐：
  required: meta.json, url.json, env.json, redirect_chain.json,
            screenshot_viewport.png, net_summary.json, auto_labels.json
  recommended: visible_text.txt, forms.json, html_rendered.json
  optional: html_raw.json, screenshot_full.png, rule_labels.json, manual_labels.json
- label_hint 属于弱标签层，优先来自 auto_labels.json，其次回退到 meta.json 的 label。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.html_payload_utils import html_payload_exists
from scripts.data.common.runtime_data_root import data_path, get_data_root

# =========================
# 头部配置区：默认输入位置 / 输出位置
# 命令行参数可覆盖
# =========================
CONFIG_DATA_ROOT = str(get_data_root())
CONFIG_INPUT_ROOTS = [
    str(data_path("raw", "phish")),
    str(data_path("raw", "benign")),
]
CONFIG_OUTPUT_DIR = str(data_path("processed", "trainset_v1"))
CONFIG_MANIFEST_NAME = "manifest.jsonl"
CONFIG_REJECTED_NAME = "manifest_rejected.jsonl"
CONFIG_SUMMARY_NAME = "build_summary.json"

# =========================
# 冻结文件名配置：当前样本结构
# =========================
FILE_META = "meta.json"
FILE_URL = "url.json"
FILE_ENV = "env.json"
FILE_REDIRECT_CHAIN = "redirect_chain.json"
FILE_SCREENSHOT_VIEWPORT = "screenshot_viewport.png"
FILE_NET_SUMMARY = "net_summary.json"
FILE_AUTO_LABELS = "auto_labels.json"

FILE_VISIBLE_TEXT = "visible_text.txt"
FILE_FORMS = "forms.json"
FILE_HTML_RENDERED = "html_rendered.json"

FILE_HTML_RAW = "html_raw.json"
FILE_SCREENSHOT_FULL = "screenshot_full.png"
FILE_RULE_LABELS = "rule_labels.json"
FILE_MANUAL_LABELS = "manual_labels.json"

REQUIRED_FILES = [
    FILE_META,
    FILE_URL,
    FILE_ENV,
    FILE_REDIRECT_CHAIN,
    FILE_SCREENSHOT_VIEWPORT,
    FILE_NET_SUMMARY,
    FILE_AUTO_LABELS,
]

TEXT_REQUIRED_FILES = REQUIRED_FILES + [FILE_VISIBLE_TEXT]
MULTIMODAL_REQUIRED_FILES = REQUIRED_FILES + [FILE_VISIBLE_TEXT, FILE_FORMS]


# =========================
# 通用工具函数
# =========================
def log(msg: str) -> None:
    """统一日志输出。"""
    print(msg, flush=True)


def read_json(path: Path) -> Any:
    """读取 JSON 文件。"""
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def safe_str(value: Any) -> str:
    """把任意值安全转成字符串。"""
    if value is None:
        return ""
    return str(value)


def is_nonempty_text(path: Path) -> bool:
    """判断文本文件是否存在且读取后非空。"""
    if not path.exists() or not path.is_file():
        return False
    try:
        return bool(path.read_text(encoding="utf-8", errors="ignore").strip())
    except Exception:
        return False


def relpath_or_abs(path: Path, root: Path) -> str:
    """优先返回相对 data_root 的路径，失败则返回绝对路径。"""
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception:
        return str(path.resolve())


def get_etld1_from_url(url: str) -> str:
    """
    基于 host 的简化 eTLD+1 提取。
    这里不引入第三方依赖，只做保守近似。
    """
    host = (urlparse(url).hostname or "").strip(".").lower()
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def nested_get(obj: Any, path: Sequence[str], default: Any = None) -> Any:
    """安全读取嵌套字典字段。"""
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


# =========================
# 样本发现与判定
# =========================
def is_sample_dir(path: Path) -> bool:
    """
    判定一个目录是否像 Warden 成功样本目录。
    当前最稳的锚点是同时存在 meta.json 和 url.json。
    """
    return path.is_dir() and (path / FILE_META).exists() and (path / FILE_URL).exists()


def iter_sample_dirs(roots: Iterable[Path]) -> Iterable[Path]:
    """递归遍历样本目录。"""
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        if is_sample_dir(root):
            key = str(root.resolve())
            if key not in seen:
                seen.add(key)
                yield root
        for meta_path in root.rglob(FILE_META):
            sample_dir = meta_path.parent
            if not is_sample_dir(sample_dir):
                continue
            key = str(sample_dir.resolve())
            if key in seen:
                continue
            seen.add(key)
            yield sample_dir


def collect_presence(sample_dir: Path) -> Dict[str, bool]:
    """收集样本目录内关键文件存在性。"""
    return {
        "has_visible_text": (sample_dir / FILE_VISIBLE_TEXT).exists(),
        "has_forms": (sample_dir / FILE_FORMS).exists(),
        "has_html_rendered": html_payload_exists(sample_dir, FILE_HTML_RENDERED),
        "has_html_raw": html_payload_exists(sample_dir, FILE_HTML_RAW),
        "has_screenshot_full": (sample_dir / FILE_SCREENSHOT_FULL).exists(),
        "has_rule_labels": (sample_dir / FILE_RULE_LABELS).exists(),
        "has_manual_labels": (sample_dir / FILE_MANUAL_LABELS).exists(),
    }


def has_all(sample_dir: Path, filenames: Sequence[str]) -> bool:
    """判断样本是否具备一组文件。"""
    return all((sample_dir / name).exists() for name in filenames)


def derive_review_priority(risk_level_weak: str) -> Optional[str]:
    """根据弱风险等级推一个粗粒度 review priority。"""
    level = safe_str(risk_level_weak).strip().lower()
    if not level:
        return None
    mapping = {
        "critical": "p0",
        "high": "p1",
        "medium": "p2",
        "low": "p3",
        "info": "p4",
    }
    return mapping.get(level, None)


def build_record(sample_dir: Path, data_root: Path) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    为单个样本目录构造 manifest 记录。
    返回:
    - 成功时: (record, None)
    - 失败时: (None, rejected_info)
    """
    missing_required = [name for name in REQUIRED_FILES if not (sample_dir / name).exists()]
    if missing_required:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "missing_required_files",
            "missing_required_files": missing_required,
        }

    try:
        meta = read_json(sample_dir / FILE_META)
    except Exception as exc:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "invalid_meta_json",
            "error": repr(exc),
        }

    try:
        url_info = read_json(sample_dir / FILE_URL)
    except Exception as exc:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "invalid_url_json",
            "error": repr(exc),
        }

    try:
        auto_labels = read_json(sample_dir / FILE_AUTO_LABELS)
    except Exception as exc:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "invalid_auto_labels_json",
            "error": repr(exc),
        }

    try:
        _ = read_json(sample_dir / FILE_NET_SUMMARY)
    except Exception as exc:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "invalid_net_summary_json",
            "error": repr(exc),
        }

    # env.json / redirect_chain.json 按存在性和可解析性都做校验，避免 manifest 放进损坏样本。
    for filename, reason in [
        (FILE_ENV, "invalid_env_json"),
        (FILE_REDIRECT_CHAIN, "invalid_redirect_chain_json"),
    ]:
        try:
            _ = read_json(sample_dir / filename)
        except Exception as exc:
            return None, {
                "sample_dir": relpath_or_abs(sample_dir, data_root),
                "reason": reason,
                "error": repr(exc),
            }

    sample_id = safe_str(meta.get("sample_id")).strip() or sample_dir.name
    input_url = safe_str(url_info.get("input_url")).strip()
    final_url = safe_str(url_info.get("final_url")).strip()

    if not sample_id:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "empty_sample_id",
        }

    if sample_id != sample_dir.name:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "sample_id_dirname_mismatch",
            "sample_id": sample_id,
            "dirname": sample_dir.name,
        }

    if not input_url or not final_url:
        return None, {
            "sample_dir": relpath_or_abs(sample_dir, data_root),
            "reason": "missing_input_or_final_url",
            "input_url": input_url,
            "final_url": final_url,
        }

    presence = collect_presence(sample_dir)

    has_text_payload = is_nonempty_text(sample_dir / FILE_VISIBLE_TEXT)
    usable_for_text = has_all(sample_dir, TEXT_REQUIRED_FILES) and has_text_payload
    usable_for_vision = has_all(sample_dir, REQUIRED_FILES)
    usable_for_multimodal = has_all(sample_dir, MULTIMODAL_REQUIRED_FILES) and has_text_payload

    label_hint = (
        safe_str(auto_labels.get("label_hint")).strip()
        or safe_str(meta.get("label")).strip()
        or ""
    )

    record: Dict[str, Any] = {
        "sample_id": sample_id,
        "sample_dir": relpath_or_abs(sample_dir, data_root),
        "label_hint": label_hint,
        "crawl_time_utc": safe_str(meta.get("crawl_time_utc")).strip(),
        "http_status": meta.get("http_status"),
        "input_url": input_url,
        "final_url": final_url,
        "has_visible_text": bool(presence["has_visible_text"]),
        "has_forms": bool(presence["has_forms"]),
        "has_html_rendered": bool(presence["has_html_rendered"]),
        "has_html_raw": bool(presence["has_html_raw"]),
        "has_screenshot_full": bool(presence["has_screenshot_full"]),
        "has_rule_labels": bool(presence["has_rule_labels"]),
        "has_manual_labels": bool(presence["has_manual_labels"]),
        "usable_for_text": bool(usable_for_text),
        "usable_for_vision": bool(usable_for_vision),
        "usable_for_multimodal": bool(usable_for_multimodal),
        "page_stage_candidate": safe_str(auto_labels.get("page_stage_candidate")).strip() or None,
        "risk_level_weak": safe_str(nested_get(auto_labels, ["risk_outputs", "risk_level_weak"])).strip() or None,
        "review_priority": None,
        "domain_etld1": (
            safe_str(nested_get(auto_labels, ["url_features", "etld1"])).strip()
            or get_etld1_from_url(final_url)
            or get_etld1_from_url(input_url)
            or None
        ),
        "split": None,
    }

    record["review_priority"] = derive_review_priority(record["risk_level_weak"] or "")

    return record, None


# =========================
# 输出与统计
# =========================
def write_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """写出 JSONL 文件。"""
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_summary(records: Sequence[Dict[str, Any]], rejected: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """生成基础统计摘要。"""
    label_counter = Counter(safe_str(r.get("label_hint")).strip().lower() or "<empty>" for r in records)
    stage_counter = Counter(safe_str(r.get("page_stage_candidate")).strip().lower() or "<empty>" for r in records)
    risk_counter = Counter(safe_str(r.get("risk_level_weak")).strip().lower() or "<empty>" for r in records)
    domain_counter = Counter(safe_str(r.get("domain_etld1")).strip().lower() or "<empty>" for r in records)
    reject_counter = Counter(safe_str(r.get("reason")).strip().lower() or "<empty>" for r in rejected)

    return {
        "num_records": len(records),
        "num_rejected": len(rejected),
        "label_hint_distribution": dict(sorted(label_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "page_stage_distribution": dict(sorted(stage_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "risk_level_weak_distribution": dict(sorted(risk_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "domain_etld1_top20": dict(sorted(domain_counter.items(), key=lambda kv: (-kv[1], kv[0]))[:20]),
        "rejected_reason_distribution": dict(sorted(reject_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "usable_counts": {
            "usable_for_text": sum(1 for r in records if r.get("usable_for_text")),
            "usable_for_vision": sum(1 for r in records if r.get("usable_for_vision")),
            "usable_for_multimodal": sum(1 for r in records if r.get("usable_for_multimodal")),
        },
    }


# =========================
# CLI
# =========================
def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="Build Warden TRAINSET_V1 manifest.jsonl from frozen sample dirs.")
    parser.add_argument("--data-root", default=CONFIG_DATA_ROOT, help="dataset root directory")
    parser.add_argument("--input-roots", nargs="+", default=CONFIG_INPUT_ROOTS, help="sample roots to scan")
    parser.add_argument("--out-dir", default=CONFIG_OUTPUT_DIR, help="output directory")
    parser.add_argument("--manifest-name", default=CONFIG_MANIFEST_NAME, help="manifest output filename")
    parser.add_argument("--rejected-name", default=CONFIG_REJECTED_NAME, help="rejected samples output filename")
    parser.add_argument("--summary-name", default=CONFIG_SUMMARY_NAME, help="summary output filename")
    parser.add_argument("--limit", type=int, default=0, help="optional max number of matched sample dirs to process")
    return parser.parse_args()


def main() -> None:
    """主流程：扫描、构建、导出。"""
    args = parse_args()

    data_root = Path(args.data_root).resolve()
    input_roots = [Path(p).resolve() for p in args.input_roots]
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    matched_dirs: List[Path] = []
    for sample_dir in iter_sample_dirs(input_roots):
        matched_dirs.append(sample_dir)
        if args.limit > 0 and len(matched_dirs) >= args.limit:
            break

    if not matched_dirs:
        raise SystemExit("未发现可处理的样本目录。")

    records: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    for idx, sample_dir in enumerate(matched_dirs, 1):
        record, rejected_info = build_record(sample_dir, data_root=data_root)
        if record is not None:
            records.append(record)
            log(f"[{idx}/{len(matched_dirs)}] OK {sample_dir}")
        else:
            rejected.append(rejected_info or {"sample_dir": relpath_or_abs(sample_dir, data_root), "reason": "unknown"})
            log(f"[{idx}/{len(matched_dirs)}] SKIP {sample_dir} :: {rejected[-1]['reason']}")

    manifest_path = out_dir / args.manifest_name
    rejected_path = out_dir / args.rejected_name
    summary_path = out_dir / args.summary_name

    write_jsonl(manifest_path, records)
    write_jsonl(rejected_path, rejected)
    summary = build_summary(records, rejected)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"[done] matched={len(matched_dirs)} kept={len(records)} rejected={len(rejected)}")
    log(f"[done] manifest={manifest_path}")
    log(f"[done] rejected={rejected_path}")
    log(f"[done] summary={summary_path}")


if __name__ == "__main__":
    main()
