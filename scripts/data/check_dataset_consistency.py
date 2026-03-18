#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
check_dataset_consistency.py

用途：
- 校验 build_manifest.py 生成的 Warden TRAINSET_V1 manifest.jsonl
- 只做一致性检查，不修改样本目录，也不重写 manifest

说明：
- 校验规则按当前仓库 docs/data/TRAINSET_V1.md 与实际样本结构对齐
- 重点检查：
  1) manifest 最小字段是否齐全
  2) sample_dir 与关键文件是否真实存在
  3) 各类 has_* 布尔字段是否与样本目录一致
  4) usable_for_text / vision / multimodal 是否与文件条件一致
  5) sample_id、URL、标签提示等关键字段是否空缺或异常
"""

from __future__ import annotations

# =========================
# 头部配置区：默认输入位置 / 输出位置
# 命令行参数可覆盖
# =========================
CONFIG_DATA_ROOT = "./data"
CONFIG_MANIFEST_PATH = "./data/processed/trainset_v1/manifest.jsonl"
CONFIG_OUTPUT_DIR = "./data/processed/trainset_v1/consistency_check"
CONFIG_REPORT_JSON_NAME = "consistency_report.json"
CONFIG_REPORT_MD_NAME = "consistency_report.md"
CONFIG_SUMMARY_NAME = "summary.json"

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
FILE_HTML_RENDERED = "html_rendered.html"

FILE_HTML_RAW = "html_raw.html"
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

REQUIRED_COLUMNS = [
    "sample_id",
    "sample_dir",
    "label_hint",
    "crawl_time_utc",
    "http_status",
    "input_url",
    "final_url",
    "has_visible_text",
    "has_forms",
    "has_html_rendered",
    "has_html_raw",
    "has_screenshot_full",
    "has_rule_labels",
    "has_manual_labels",
    "usable_for_text",
    "usable_for_vision",
    "usable_for_multimodal",
]

OPTIONAL_COLUMNS = [
    "page_stage_candidate",
    "risk_level_weak",
    "review_priority",
    "domain_etld1",
    "split",
]

ALLOWED_SPLITS = {"train", "val", "test"}

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urlparse


# =========================
# 通用工具函数
# =========================
def log(msg: str) -> None:
    """统一日志输出。"""
    print(msg, flush=True)


def safe_str(value: Any) -> str:
    """安全字符串化。"""
    if value is None:
        return ""
    return str(value)


def is_empty(value: Any) -> bool:
    """判断值是否为空。"""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """读取 JSONL。"""
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, 1):
            text = line.strip()
            if not text:
                continue
            try:
                rows.append(json.loads(text))
            except Exception as exc:
                raise ValueError(f"manifest 第 {lineno} 行不是合法 JSON: {exc}") from exc
    return rows


def is_bool_like(value: Any) -> bool:
    """当前 manifest 中布尔字段必须真的写 bool。"""
    return isinstance(value, bool)


def is_int_like(value: Any) -> bool:
    """http_status 的宽松整数判定。"""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, str) and value.strip().isdigit():
        return True
    return False


def get_etld1_from_url(url: str) -> str:
    """不引入第三方依赖的简化 eTLD+1 提取。"""
    host = (urlparse(url).hostname or "").strip(".").lower()
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


# =========================
# 报告结构
# =========================
class Report:
    """收集检查项结果。"""

    def __init__(self) -> None:
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.infos: List[Dict[str, Any]] = []

    def error(self, code: str, message: str, count: int = 1, examples: Optional[List[Dict[str, Any]]] = None) -> None:
        self.errors.append({"level": "error", "code": code, "message": message, "count": int(count), "examples": examples or []})

    def warn(self, code: str, message: str, count: int = 1, examples: Optional[List[Dict[str, Any]]] = None) -> None:
        self.warnings.append({"level": "warning", "code": code, "message": message, "count": int(count), "examples": examples or []})

    def info(self, code: str, message: str, count: int = 0, payload: Optional[Dict[str, Any]] = None) -> None:
        item: Dict[str, Any] = {"level": "info", "code": code, "message": message}
        if count:
            item["count"] = int(count)
        if payload is not None:
            item["payload"] = payload
        self.infos.append(item)

    def has_errors(self) -> bool:
        return bool(self.errors)


# =========================
# 校验逻辑
# =========================
def check_schema(rows: Sequence[Dict[str, Any]], report: Report, example_limit: int) -> None:
    """校验 manifest 的字段集合。"""
    if not rows:
        report.error("empty_manifest", "manifest 为空。", count=1)
        return

    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())

    missing_required = [c for c in REQUIRED_COLUMNS if c not in all_keys]
    missing_optional = [c for c in OPTIONAL_COLUMNS if c not in all_keys]

    if missing_required:
        report.error(
            "missing_required_columns",
            f"manifest 缺少必备字段: {', '.join(missing_required)}",
            count=len(missing_required),
            examples=[{"missing": missing_required[:example_limit]}],
        )

    if missing_optional:
        report.warn(
            "missing_optional_columns",
            f"manifest 缺少可选字段: {', '.join(missing_optional)}",
            count=len(missing_optional),
            examples=[{"missing": missing_optional[:example_limit]}],
        )


def check_basic_fields(rows: Sequence[Dict[str, Any]], report: Report, example_limit: int) -> None:
    """检查基础字段取值。"""
    empty_sample_id = []
    duplicate_ids = Counter()

    for row in rows:
        sample_id = safe_str(row.get("sample_id")).strip()
        if not sample_id:
            empty_sample_id.append(row)
        else:
            duplicate_ids[sample_id] += 1

    if empty_sample_id:
        report.error(
            "empty_sample_id",
            "存在空 sample_id。",
            count=len(empty_sample_id),
            examples=empty_sample_id[:example_limit],
        )

    dup_examples = [{"sample_id": sid, "count": cnt} for sid, cnt in duplicate_ids.items() if cnt > 1][:example_limit]
    if dup_examples:
        total_dup_rows = sum(item["count"] for item in dup_examples)
        report.error(
            "duplicate_sample_id",
            "存在重复 sample_id。",
            count=total_dup_rows,
            examples=dup_examples,
        )

    bad_rows: List[Dict[str, Any]] = []
    for row in rows:
        entry = {"sample_id": row.get("sample_id"), "sample_dir": row.get("sample_dir")}
        any_bad = False

        for key in ["sample_dir", "label_hint", "crawl_time_utc", "input_url", "final_url"]:
            if is_empty(row.get(key)):
                entry[key] = row.get(key)
                any_bad = True

        if not is_int_like(row.get("http_status")):
            entry["http_status"] = row.get("http_status")
            any_bad = True

        for key in [
            "has_visible_text",
            "has_forms",
            "has_html_rendered",
            "has_html_raw",
            "has_screenshot_full",
            "has_rule_labels",
            "has_manual_labels",
            "usable_for_text",
            "usable_for_vision",
            "usable_for_multimodal",
        ]:
            if key in row and not is_bool_like(row.get(key)):
                entry[key] = row.get(key)
                any_bad = True

        split = safe_str(row.get("split")).strip().lower()
        if split and split not in ALLOWED_SPLITS:
            entry["split"] = row.get("split")
            any_bad = True

        if any_bad:
            bad_rows.append(entry)

    if bad_rows:
        report.error(
            "invalid_core_fields",
            "存在空缺或类型不合法的核心字段。",
            count=len(bad_rows),
            examples=bad_rows[:example_limit],
        )


def check_sample_paths(rows: Sequence[Dict[str, Any]], data_root: Path, report: Report, example_limit: int) -> None:
    """检查 sample_dir 与文件存在性，以及 has_* / usable_* 逻辑一致性。"""
    missing_sample_dir: List[Dict[str, Any]] = []
    missing_required_files: List[Dict[str, Any]] = []
    inconsistent_flags: List[Dict[str, Any]] = []

    for row in rows:
        sample_dir_value = safe_str(row.get("sample_dir")).strip()
        if not sample_dir_value:
            continue

        sample_dir = Path(sample_dir_value)
        if not sample_dir.is_absolute():
            sample_dir = (data_root / sample_dir).resolve()

        if not sample_dir.exists() or not sample_dir.is_dir():
            missing_sample_dir.append({
                "sample_id": row.get("sample_id"),
                "sample_dir": sample_dir_value,
            })
            continue

        missing = [name for name in REQUIRED_FILES if not (sample_dir / name).exists()]
        if missing:
            missing_required_files.append({
                "sample_id": row.get("sample_id"),
                "sample_dir": sample_dir_value,
                "missing_required_files": missing,
            })

        actual_flags = {
            "has_visible_text": (sample_dir / FILE_VISIBLE_TEXT).exists(),
            "has_forms": (sample_dir / FILE_FORMS).exists(),
            "has_html_rendered": (sample_dir / FILE_HTML_RENDERED).exists(),
            "has_html_raw": (sample_dir / FILE_HTML_RAW).exists(),
            "has_screenshot_full": (sample_dir / FILE_SCREENSHOT_FULL).exists(),
            "has_rule_labels": (sample_dir / FILE_RULE_LABELS).exists(),
            "has_manual_labels": (sample_dir / FILE_MANUAL_LABELS).exists(),
        }

        # 先校验 has_* 标记是否与真实文件一致。
        for key, actual in actual_flags.items():
            expected = row.get(key)
            if isinstance(expected, bool) and expected != actual:
                inconsistent_flags.append({
                    "sample_id": row.get("sample_id"),
                    "sample_dir": sample_dir_value,
                    "field": key,
                    "manifest_value": expected,
                    "actual_value": actual,
                })

        # 再校验 usable_* 与文件条件是否一致。
        has_text_payload = False
        visible_text_path = sample_dir / FILE_VISIBLE_TEXT
        if visible_text_path.exists() and visible_text_path.is_file():
            try:
                has_text_payload = bool(visible_text_path.read_text(encoding="utf-8", errors="ignore").strip())
            except Exception:
                has_text_payload = False

        actual_vision = all((sample_dir / name).exists() for name in REQUIRED_FILES)
        actual_text = actual_vision and (sample_dir / FILE_VISIBLE_TEXT).exists() and has_text_payload
        actual_mm = actual_text and (sample_dir / FILE_FORMS).exists()

        expected_vision = row.get("usable_for_vision")
        if isinstance(expected_vision, bool) and expected_vision != actual_vision:
            inconsistent_flags.append({
                "sample_id": row.get("sample_id"),
                "sample_dir": sample_dir_value,
                "field": "usable_for_vision",
                "manifest_value": expected_vision,
                "actual_value": actual_vision,
            })

        expected_text = row.get("usable_for_text")
        if isinstance(expected_text, bool) and expected_text != actual_text:
            inconsistent_flags.append({
                "sample_id": row.get("sample_id"),
                "sample_dir": sample_dir_value,
                "field": "usable_for_text",
                "manifest_value": expected_text,
                "actual_value": actual_text,
            })

        expected_mm = row.get("usable_for_multimodal")
        if isinstance(expected_mm, bool) and expected_mm != actual_mm:
            inconsistent_flags.append({
                "sample_id": row.get("sample_id"),
                "sample_dir": sample_dir_value,
                "field": "usable_for_multimodal",
                "manifest_value": expected_mm,
                "actual_value": actual_mm,
            })

    if missing_sample_dir:
        report.error(
            "missing_sample_dir",
            "manifest 中存在不存在的 sample_dir。",
            count=len(missing_sample_dir),
            examples=missing_sample_dir[:example_limit],
        )

    if missing_required_files:
        report.error(
            "missing_required_files_in_sample_dir",
            "manifest 样本目录缺少 TRAINSET_V1 必需文件。",
            count=len(missing_required_files),
            examples=missing_required_files[:example_limit],
        )

    if inconsistent_flags:
        report.error(
            "inconsistent_presence_or_usable_flags",
            "manifest 中的 has_* / usable_* 与真实样本目录不一致。",
            count=len(inconsistent_flags),
            examples=inconsistent_flags[:example_limit],
        )


def check_semantics(rows: Sequence[Dict[str, Any]], report: Report, example_limit: int) -> None:
    """检查一些不涉及改字段的轻量语义问题。"""
    label_warnings: List[Dict[str, Any]] = []
    domain_warnings: List[Dict[str, Any]] = []

    for row in rows:
        label_hint = safe_str(row.get("label_hint")).strip().lower()
        if label_hint and label_hint not in {"phish", "benign", "unknown"}:
            label_warnings.append({
                "sample_id": row.get("sample_id"),
                "label_hint": row.get("label_hint"),
            })

        final_url = safe_str(row.get("final_url")).strip()
        domain_etld1 = safe_str(row.get("domain_etld1")).strip().lower()
        actual_etld1 = get_etld1_from_url(final_url)
        if domain_etld1 and actual_etld1 and domain_etld1 != actual_etld1:
            domain_warnings.append({
                "sample_id": row.get("sample_id"),
                "domain_etld1": domain_etld1,
                "actual_etld1_from_final_url": actual_etld1,
                "final_url": final_url,
            })

    if label_warnings:
        report.warn(
            "unexpected_label_hint_values",
            "label_hint 出现非 phish/benign/unknown 的取值。",
            count=len(label_warnings),
            examples=label_warnings[:example_limit],
        )

    if domain_warnings:
        report.warn(
            "domain_etld1_mismatch",
            "domain_etld1 与 final_url 推导出的域不一致。",
            count=len(domain_warnings),
            examples=domain_warnings[:example_limit],
        )


def build_summary(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """生成摘要统计。"""
    label_counter = Counter(safe_str(r.get("label_hint")).strip().lower() or "<empty>" for r in rows)
    stage_counter = Counter(safe_str(r.get("page_stage_candidate")).strip().lower() or "<empty>" for r in rows)
    risk_counter = Counter(safe_str(r.get("risk_level_weak")).strip().lower() or "<empty>" for r in rows)
    split_counter = Counter(safe_str(r.get("split")).strip().lower() or "<empty>" for r in rows)

    return {
        "num_rows": len(rows),
        "label_hint_distribution": dict(sorted(label_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "page_stage_distribution": dict(sorted(stage_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "risk_level_weak_distribution": dict(sorted(risk_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "split_distribution": dict(sorted(split_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "usable_counts": {
            "usable_for_text": sum(1 for r in rows if r.get("usable_for_text") is True),
            "usable_for_vision": sum(1 for r in rows if r.get("usable_for_vision") is True),
            "usable_for_multimodal": sum(1 for r in rows if r.get("usable_for_multimodal") is True),
        },
    }


def build_markdown_report(report: Report, summary: Dict[str, Any], manifest_path: Path, data_root: Path) -> str:
    """生成 Markdown 报告。"""
    lines: List[str] = []
    lines.append("# TRAINSET_V1 consistency report")
    lines.append("")
    lines.append(f"- manifest: `{manifest_path}`")
    lines.append(f"- data_root: `{data_root}`")
    lines.append(f"- rows: {summary.get('num_rows', 0)}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- errors: {len(report.errors)}")
    lines.append(f"- warnings: {len(report.warnings)}")
    lines.append("")

    for title, counter_name in [
        ("label_hint_distribution", "label_hint_distribution"),
        ("page_stage_distribution", "page_stage_distribution"),
        ("risk_level_weak_distribution", "risk_level_weak_distribution"),
        ("split_distribution", "split_distribution"),
    ]:
        lines.append(f"### {title}")
        data = summary.get(counter_name) or {}
        if not data:
            lines.append("- <empty>")
        else:
            for key, value in data.items():
                lines.append(f"- {key}: {value}")
        lines.append("")

    lines.append("### usable_counts")
    for key, value in (summary.get("usable_counts") or {}).items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    def dump_items(title: str, items: Sequence[Dict[str, Any]]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("- <none>")
            lines.append("")
            return
        for item in items:
            lines.append(f"- **{item.get('code')}**: {item.get('message')} (count={item.get('count', 0)})")
            for ex in item.get("examples", [])[:10]:
                lines.append(f"  - example: `{json.dumps(ex, ensure_ascii=False)}`")
        lines.append("")

    dump_items("Errors", report.errors)
    dump_items("Warnings", report.warnings)
    return "\n".join(lines) + "\n"


# =========================
# CLI
# =========================
def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="Check Warden TRAINSET_V1 manifest consistency.")
    parser.add_argument("--data-root", default=CONFIG_DATA_ROOT, help="dataset root directory")
    parser.add_argument("--manifest", default=CONFIG_MANIFEST_PATH, help="manifest.jsonl path")
    parser.add_argument("--out-dir", default=CONFIG_OUTPUT_DIR, help="output directory")
    parser.add_argument("--report-json-name", default=CONFIG_REPORT_JSON_NAME, help="json report filename")
    parser.add_argument("--report-md-name", default=CONFIG_REPORT_MD_NAME, help="markdown report filename")
    parser.add_argument("--summary-name", default=CONFIG_SUMMARY_NAME, help="summary filename")
    parser.add_argument("--example-limit", type=int, default=10, help="max examples to keep for each issue")
    parser.add_argument("--strict", action="store_true", help="exit with non-zero when report has errors")
    return parser.parse_args()


def main() -> None:
    """主流程：读取 manifest，执行校验，导出报告。"""
    args = parse_args()

    data_root = Path(args.data_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not manifest_path.exists():
        raise SystemExit(f"manifest 不存在: {manifest_path}")

    rows = read_jsonl(manifest_path)
    report = Report()
    report.info("manifest_loaded", "已加载 manifest。", count=len(rows), payload={"manifest": str(manifest_path)})

    check_schema(rows, report, example_limit=args.example_limit)
    check_basic_fields(rows, report, example_limit=args.example_limit)
    check_sample_paths(rows, data_root=data_root, report=report, example_limit=args.example_limit)
    check_semantics(rows, report=report, example_limit=args.example_limit)

    summary = build_summary(rows)

    payload = {
        "manifest": str(manifest_path),
        "data_root": str(data_root),
        "summary": summary,
        "errors": report.errors,
        "warnings": report.warnings,
        "infos": report.infos,
        "status": "fail" if report.has_errors() else "pass",
    }

    report_json_path = out_dir / args.report_json_name
    report_md_path = out_dir / args.report_md_name
    summary_path = out_dir / args.summary_name

    report_json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md_path.write_text(build_markdown_report(report, summary, manifest_path, data_root), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"[done] rows={len(rows)}")
    log(f"[done] errors={len(report.errors)} warnings={len(report.warnings)}")
    log(f"[done] report_json={report_json_path}")
    log(f"[done] report_md={report_md_path}")
    log(f"[done] summary={summary_path}")

    if args.strict and report.has_errors():
        raise SystemExit(2)


if __name__ == "__main__":
    main()
