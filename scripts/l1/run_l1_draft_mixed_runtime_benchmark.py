#!/usr/bin/env python3
"""Run a bounded mixed runtime benchmark for the L1 draft sidecar."""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from scripts.data.common.io_utils import ensure_dir  # noqa: E402
from warden.runtime.pipeline import process_sample  # noqa: E402


RESULTS_JSONL = "l1_draft_mixed_runtime_results_v1.jsonl"
SUMMARY_CSV = "l1_draft_mixed_runtime_summary_v1.csv"
REPORT_MD = "l1_draft_mixed_runtime_report_v1.md"
ERRORS_CSV = "l1_draft_mixed_runtime_errors_v1.csv"
L1_FLAG = "WARDEN_ENABLE_L1_DRAFT"

PER_SAMPLE_FIELDS = [
    "sample_id",
    "bucket",
    "current_path",
    "runtime_status",
    "official_final_stage",
    "official_terminal_routing",
    "official_routing_outcome",
    "official_stage_sequence",
    "official_fields_match_flag_off",
    "flag_off_has_debug_sidecars",
    "has_l1_draft_sidecar",
    "l1_draft_status",
    "l1_draft_duration_ms",
    "total_runtime_duration_ms",
    "l1_rule_assessment",
    "l1_routing_assessment",
    "l1_draft_need_text_tower",
    "l1_draft_need_ocr",
    "l1_draft_need_yolo",
    "l1_draft_need_review",
    "l1_risk_hint_high_risk_candidate",
    "l1_risk_hint_low_risk_candidate",
    "l1_risk_hint_benign_hard_negative_candidate",
    "final_like_label_leakage",
    "reason_codes_count",
    "evidence_ledger_count",
    "has_explanation",
    "error_type",
    "error_message",
]

BUCKET_FROM_TRIAGE = {
    "T00_clear_benign": "B00_benign_clear",
    "T01_benign_hard_negative": "B01_benign_hard_negative",
    "T90_uncertain_or_suspicious": "B90_bad_capture_or_gate",
}

SUPPORTED_BUCKETS = {
    "B00_benign_clear",
    "B01_benign_hard_negative",
    "B90_bad_capture_or_gate",
    "M10_malicious_behavior_only",
    "M11_malicious_action_observed",
    "M12_malicious_behavior_and_action",
    "M90_malicious_or_suspicious_unknown",
}


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a bounded L1 draft mixed runtime benchmark.")
    parser.add_argument("--input-manifest", action="append", default=[], help="Generic CSV manifest with current_path.")
    parser.add_argument("--benign-train", help="Benign train manifest CSV.")
    parser.add_argument("--benign-val", help="Benign val manifest CSV.")
    parser.add_argument("--benign-test", help="Benign test manifest CSV.")
    parser.add_argument("--malicious-manifest", action="append", default=[], help="Optional malicious manifest CSV.")
    parser.add_argument("--output-dir", required=True, help="Output directory for benchmark artifacts.")
    parser.add_argument("--limit-per-bucket", type=int, default=25, help="Max samples per bucket; 0 means no limit.")
    parser.add_argument("--seed", type=int, default=42, help="Sampling seed.")
    return parser.parse_args(argv)


def _read_csv_rows(path: Path, *, source_manifest: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row = {str(k): "" if v is None else str(v) for k, v in row.items()}
            row["_source_manifest"] = source_manifest
            rows.append(row)
    return rows


def _bucket_for_row(row: Dict[str, str], *, default_malicious: bool = False) -> str:
    for key in ("bucket", "l1_benchmark_bucket", "benchmark_bucket"):
        value = row.get(key, "").strip()
        if value in SUPPORTED_BUCKETS:
            return value
    triage = row.get("triage_label", "").strip()
    if triage in BUCKET_FROM_TRIAGE:
        return BUCKET_FROM_TRIAGE[triage]
    if default_malicious:
        return "M90_malicious_or_suspicious_unknown"
    return ""


def load_candidate_rows(args: argparse.Namespace) -> List[Dict[str, str]]:
    candidates: List[Dict[str, str]] = []
    benign_manifests = [
        item
        for item in [
            ("benign_train", args.benign_train),
            ("benign_val", args.benign_val),
            ("benign_test", args.benign_test),
        ]
        if item[1]
    ]
    for name, raw_path in benign_manifests:
        for row in _read_csv_rows(Path(raw_path), source_manifest=str(raw_path)):
            bucket = _bucket_for_row(row)
            if bucket:
                row["_bucket"] = bucket
                row["_input_group"] = name
                candidates.append(row)
    for raw_path in args.input_manifest:
        for row in _read_csv_rows(Path(raw_path), source_manifest=str(raw_path)):
            bucket = _bucket_for_row(row)
            if bucket:
                row["_bucket"] = bucket
                row["_input_group"] = "input_manifest"
                candidates.append(row)
    for raw_path in args.malicious_manifest:
        for row in _read_csv_rows(Path(raw_path), source_manifest=str(raw_path)):
            bucket = _bucket_for_row(row, default_malicious=True)
            row["_bucket"] = bucket
            row["_input_group"] = "malicious_manifest"
            candidates.append(row)
    return candidates


def sample_rows(rows: Iterable[Dict[str, str]], *, limit_per_bucket: int, seed: int) -> List[Dict[str, str]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        current_path = row.get("current_path", "").strip()
        bucket = row.get("_bucket", "").strip()
        if not current_path or bucket not in SUPPORTED_BUCKETS:
            continue
        grouped[bucket].append(row)
    rng = random.Random(seed)
    selected: List[Dict[str, str]] = []
    for bucket in sorted(grouped):
        bucket_rows = list(grouped[bucket])
        rng.shuffle(bucket_rows)
        if limit_per_bucket > 0:
            bucket_rows = bucket_rows[:limit_per_bucket]
        selected.extend(bucket_rows)
    return selected


def _read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _run_one_runtime(sample_dir: Path, output_root: Path, *, flag_enabled: bool) -> tuple[Dict[str, Any], float]:
    old_flag = os.environ.get(L1_FLAG)
    os.environ[L1_FLAG] = "1" if flag_enabled else "0"
    started = time.perf_counter()
    try:
        record = process_sample(sample_dir=sample_dir, output_dir=output_root)
    finally:
        if old_flag is None:
            os.environ.pop(L1_FLAG, None)
        else:
            os.environ[L1_FLAG] = old_flag
    duration_ms = round((time.perf_counter() - started) * 1000.0, 3)
    return record, duration_ms


def _official_compare(off_result: Dict[str, Any], on_result: Dict[str, Any]) -> bool:
    keys = ["final_stage", "terminal_routing", "routing_outcome", "stage_sequence"]
    return all(off_result.get(key) == on_result.get(key) for key in keys)


def _routing_bool(draft_result: Dict[str, Any], key: str) -> bool:
    routing = ((draft_result.get("rule_router") or {}).get("routing_hints") or {})
    return bool(routing.get(key))


FINAL_LIKE_LABEL_VALUES = {"benign", "suspicious", "malicious"}


def detect_final_like_label_leakage(payload: Any) -> bool:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in {"label", "final_label"} and str(value).lower() in FINAL_LIKE_LABEL_VALUES:
                return True
            if detect_final_like_label_leakage(value):
                return True
    if isinstance(payload, list):
        return any(detect_final_like_label_leakage(item) for item in payload)
    return False


def benchmark_row(row: Dict[str, str], output_dir: Path) -> Dict[str, Any]:
    bucket = row["_bucket"]
    current_path = row.get("current_path", "").strip()
    sample_dir = Path(current_path)
    base = {
        "sample_id": row.get("sample_id", "") or sample_dir.name,
        "bucket": bucket,
        "current_path": current_path,
        "runtime_status": "ok",
        "official_final_stage": "",
        "official_terminal_routing": "",
        "official_routing_outcome": "",
        "official_stage_sequence": "",
        "official_fields_match_flag_off": False,
        "flag_off_has_debug_sidecars": False,
        "has_l1_draft_sidecar": False,
        "l1_draft_status": "",
        "l1_draft_duration_ms": "",
        "total_runtime_duration_ms": "",
        "l1_rule_assessment": "",
        "l1_routing_assessment": "",
        "l1_draft_need_text_tower": "",
        "l1_draft_need_ocr": "",
        "l1_draft_need_yolo": "",
        "l1_draft_need_review": "",
        "l1_risk_hint_high_risk_candidate": "",
        "l1_risk_hint_low_risk_candidate": "",
        "l1_risk_hint_benign_hard_negative_candidate": "",
        "final_like_label_leakage": False,
        "reason_codes_count": 0,
        "evidence_ledger_count": 0,
        "has_explanation": False,
        "error_type": "",
        "error_message": "",
    }
    try:
        off_record, _off_duration = _run_one_runtime(sample_dir, output_dir / "runtime_flag_off", flag_enabled=False)
        on_record, on_duration = _run_one_runtime(sample_dir, output_dir / "runtime_flag_on", flag_enabled=True)
        off_result = _read_json(off_record["result_path"])
        on_result = _read_json(on_record["result_path"])
        on_trace = _read_json(on_record["trace_path"])
        sidecar = (on_trace.get("debug_sidecars") or {}).get("l1_draft") or {}
        draft_result = sidecar.get("result") or {}
        rule_router = draft_result.get("rule_router") or {}
        routing_hints = rule_router.get("routing_hints") or {}
        risk_hints = rule_router.get("risk_hints") or {}
        reason_codes = rule_router.get("reason_codes") or []
        evidence_ledger = draft_result.get("evidence_ledger") or []
        base.update(
            {
                "sample_id": on_result.get("sample_id") or base["sample_id"],
                "official_final_stage": on_result.get("final_stage") or "",
                "official_terminal_routing": on_result.get("terminal_routing") or "",
                "official_routing_outcome": on_result.get("routing_outcome") or {},
                "official_stage_sequence": on_result.get("stage_sequence") or [],
                "official_fields_match_flag_off": _official_compare(off_result, on_result),
                "flag_off_has_debug_sidecars": "debug_sidecars" in off_result,
                "has_l1_draft_sidecar": bool(sidecar),
                "l1_draft_status": sidecar.get("status") or "",
                "l1_draft_duration_ms": sidecar.get("duration_ms") if sidecar else "",
                "total_runtime_duration_ms": on_duration,
                "l1_rule_assessment": rule_router.get("rule_assessment") or "",
                "l1_routing_assessment": rule_router.get("routing_assessment") or "",
                "l1_draft_need_text_tower": bool(routing_hints.get("need_text_tower")),
                "l1_draft_need_ocr": _routing_bool(draft_result, "need_ocr"),
                "l1_draft_need_yolo": _routing_bool(draft_result, "need_yolo"),
                "l1_draft_need_review": _routing_bool(draft_result, "need_review"),
                "l1_risk_hint_high_risk_candidate": bool(risk_hints.get("high_risk_candidate")),
                "l1_risk_hint_low_risk_candidate": bool(risk_hints.get("low_risk_candidate")),
                "l1_risk_hint_benign_hard_negative_candidate": bool(risk_hints.get("benign_hard_negative_candidate")),
                "final_like_label_leakage": detect_final_like_label_leakage(draft_result),
                "reason_codes_count": len(reason_codes),
                "evidence_ledger_count": len(evidence_ledger),
                "has_explanation": bool(draft_result.get("explanation")),
            }
        )
        if sidecar.get("error"):
            error = sidecar.get("error") or {}
            base["error_type"] = error.get("type") or ""
            base["error_message"] = error.get("message") or ""
    except Exception as exc:
        base["runtime_status"] = "error"
        base["error_type"] = type(exc).__name__
        base["error_message"] = str(exc)
    return base


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=_json_default) + "\n")


def write_errors_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    error_rows = [row for row in rows if row.get("runtime_status") == "error" or row.get("l1_draft_status") == "error"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample_id", "bucket", "current_path", "error_type", "error_message"])
        writer.writeheader()
        for row in error_rows:
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames or []})


def _percentile(values: Sequence[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return round(ordered[index], 3)


def build_summary(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    durations = [float(row["l1_draft_duration_ms"]) for row in rows if row.get("l1_draft_duration_ms") not in ("", None)]
    total_durations = [
        float(row["total_runtime_duration_ms"]) for row in rows if row.get("total_runtime_duration_ms") not in ("", None)
    ]
    bucket_counts = Counter(str(row.get("bucket") or "") for row in rows)
    assessments = Counter(str(row.get("l1_rule_assessment") or "") for row in rows)
    assessments_by_bucket: Dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        assessments_by_bucket[str(row.get("bucket") or "")][str(row.get("l1_rule_assessment") or "")] += 1
    return {
        "total_samples": len(rows),
        "samples_by_bucket": dict(bucket_counts),
        "runtime_success_count": sum(1 for row in rows if row.get("runtime_status") == "ok"),
        "runtime_error_count": sum(1 for row in rows if row.get("runtime_status") == "error"),
        "l1_draft_ok_count": sum(1 for row in rows if row.get("l1_draft_status") == "ok"),
        "l1_draft_error_count": sum(1 for row in rows if row.get("l1_draft_status") == "error"),
        "missing_sidecar_count": sum(1 for row in rows if not row.get("has_l1_draft_sidecar")),
        "avg_l1_draft_duration_ms": round(statistics.mean(durations), 3) if durations else 0.0,
        "p50_l1_draft_duration_ms": _percentile(durations, 50),
        "p95_l1_draft_duration_ms": _percentile(durations, 95),
        "p99_l1_draft_duration_ms": _percentile(durations, 99),
        "avg_total_runtime_duration_ms": round(statistics.mean(total_durations), 3) if total_durations else 0.0,
        "rule_assessment_distribution": dict(assessments),
        "routing_need_text_tower_count": sum(1 for row in rows if row.get("l1_draft_need_text_tower") is True),
        "routing_need_ocr_count": sum(1 for row in rows if row.get("l1_draft_need_ocr") is True),
        "routing_need_yolo_count": sum(1 for row in rows if row.get("l1_draft_need_yolo") is True),
        "routing_need_review_count": sum(1 for row in rows if row.get("l1_draft_need_review") is True),
        "high_risk_candidate_count": sum(1 for row in rows if row.get("l1_risk_hint_high_risk_candidate") is True),
        "low_risk_candidate_count": sum(1 for row in rows if row.get("l1_risk_hint_low_risk_candidate") is True),
        "benign_hard_negative_candidate_count": sum(
            1 for row in rows if row.get("l1_risk_hint_benign_hard_negative_candidate") is True
        ),
        "final_like_label_leakage_warning_count": sum(1 for row in rows if row.get("final_like_label_leakage") is True),
        "b01_rule_assessment_distribution": dict(assessments_by_bucket.get("B01_benign_hard_negative", Counter())),
        "b00_rule_assessment_distribution": dict(assessments_by_bucket.get("B00_benign_clear", Counter())),
        "b01_high_risk_candidate_count": sum(
            1 for row in rows if row.get("bucket") == "B01_benign_hard_negative" and row.get("l1_risk_hint_high_risk_candidate") is True
        ),
        "b01_need_review_count": sum(
            1 for row in rows if row.get("bucket") == "B01_benign_hard_negative" and row.get("l1_draft_need_review") is True
        ),
        "b01_need_ocr_count": sum(
            1 for row in rows if row.get("bucket") == "B01_benign_hard_negative" and row.get("l1_draft_need_ocr") is True
        ),
        "b00_high_risk_candidate_count": sum(
            1 for row in rows if row.get("bucket") == "B00_benign_clear" and row.get("l1_risk_hint_high_risk_candidate") is True
        ),
        "official_fields_mismatch_count": sum(1 for row in rows if row.get("official_fields_match_flag_off") is False),
        "flag_off_debug_sidecar_count": sum(1 for row in rows if row.get("flag_off_has_debug_sidecars") is True),
        "reason_code_top_counts": {},
    }


def add_reason_code_summary(rows: Sequence[Dict[str, Any]], output_dir: Path, summary: Dict[str, Any]) -> None:
    reason_counts: Counter[str] = Counter()
    reason_counts_by_bucket: Dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        sample_id = row.get("sample_id")
        if not sample_id:
            continue
        trace_path = output_dir / "runtime_flag_on" / str(sample_id) / "runtime_trace.json"
        if not trace_path.exists():
            continue
        try:
            trace = _read_json(trace_path)
        except Exception:
            continue
        result = ((trace.get("debug_sidecars") or {}).get("l1_draft") or {}).get("result") or {}
        codes = ((result.get("rule_router") or {}).get("reason_codes") or [])
        reason_counts.update(codes)
        reason_counts_by_bucket[str(row.get("bucket") or "")].update(codes)
    summary["reason_code_top_counts"] = dict(reason_counts.most_common(20))
    summary["b01_top_reason_codes"] = dict(reason_counts_by_bucket["B01_benign_hard_negative"].most_common(20))
    summary["b00_top_reason_codes"] = dict(reason_counts_by_bucket["B00_benign_clear"].most_common(20))


def write_summary_csv(path: Path, summary: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "bucket", "value"])
        writer.writeheader()
        for key, value in summary.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    writer.writerow({"metric": key, "bucket": subkey, "value": json.dumps(subvalue, ensure_ascii=False)})
            else:
                writer.writerow({"metric": key, "bucket": "", "value": value})


def write_report(path: Path, summary: Dict[str, Any], *, manifests: Sequence[str], output_dir: Path) -> None:
    reason_lines = "\n".join(
        f"- `{code}`: `{count}`" for code, count in (summary.get("reason_code_top_counts") or {}).items()
    ) or "- none"
    b01_reason_lines = "\n".join(
        f"- `{code}`: `{count}`" for code, count in (summary.get("b01_top_reason_codes") or {}).items()
    ) or "- none"
    b00_reason_lines = "\n".join(
        f"- `{code}`: `{count}`" for code, count in (summary.get("b00_top_reason_codes") or {}).items()
    ) or "- none"
    bucket_lines = "\n".join(
        f"- `{bucket}`: `{count}`" for bucket, count in (summary.get("samples_by_bucket") or {}).items()
    ) or "- none"
    text = f"""# L1 Draft Mixed Runtime Benchmark Report V1

## 中文版

> 本报告是 runtime 接线、draft sidecar 完整性、规则路由 sanity 和延迟 smoke，不是最终模型准确率评估。

### 输入

- manifests: `{'; '.join(manifests) if manifests else 'none'}`
- output_dir: `{output_dir}`

### 样本桶

{bucket_lines}

### 汇总

- total_samples: `{summary.get('total_samples')}`
- runtime_success_count: `{summary.get('runtime_success_count')}`
- runtime_error_count: `{summary.get('runtime_error_count')}`
- l1_draft_ok_count: `{summary.get('l1_draft_ok_count')}`
- l1_draft_error_count: `{summary.get('l1_draft_error_count')}`
- missing_sidecar_count: `{summary.get('missing_sidecar_count')}`
- official_fields_mismatch_count: `{summary.get('official_fields_mismatch_count')}`
- flag_off_debug_sidecar_count: `{summary.get('flag_off_debug_sidecar_count')}`

### 延迟

- avg_l1_draft_duration_ms: `{summary.get('avg_l1_draft_duration_ms')}`
- p50_l1_draft_duration_ms: `{summary.get('p50_l1_draft_duration_ms')}`
- p95_l1_draft_duration_ms: `{summary.get('p95_l1_draft_duration_ms')}`
- p99_l1_draft_duration_ms: `{summary.get('p99_l1_draft_duration_ms')}`
- avg_total_runtime_duration_ms: `{summary.get('avg_total_runtime_duration_ms')}`

### 路由计数

- routing_need_text_tower_count: `{summary.get('routing_need_text_tower_count')}`
- routing_need_ocr_count: `{summary.get('routing_need_ocr_count')}`
- routing_need_yolo_count: `{summary.get('routing_need_yolo_count')}`
- routing_need_review_count: `{summary.get('routing_need_review_count')}`

### Rule Router Metrics

- rule_assessment distribution: `{json.dumps(summary.get('rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- high_risk_candidate count: `{summary.get('high_risk_candidate_count')}`
- low_risk_candidate count: `{summary.get('low_risk_candidate_count')}`
- benign_hard_negative_candidate count: `{summary.get('benign_hard_negative_candidate_count')}`
- final-like label leakage warning count: `{summary.get('final_like_label_leakage_warning_count')}`

### B00 / B01 Rule Router Breakout

- B00 rule_assessment distribution: `{json.dumps(summary.get('b00_rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- B00 high_risk_candidate count: `{summary.get('b00_high_risk_candidate_count')}`
- B01 rule_assessment distribution: `{json.dumps(summary.get('b01_rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- B01 need_review count: `{summary.get('b01_need_review_count')}`
- B01 need_ocr count: `{summary.get('b01_need_ocr_count')}`
- B01 high_risk_candidate count: `{summary.get('b01_high_risk_candidate_count')}`

### B00 Top Reason Codes

{b00_reason_lines}

### B01 Top Reason Codes

{b01_reason_lines}

### Rule-Routing Sanity Note

- This benchmark reports rule router assessments and routing hints only.
- It does not evaluate final model accuracy, because the L1 Decision Head is not run.
- If B01 has many high-risk candidates in larger runs, treat this as routing calibration evidence, not final model accuracy.

### Top Reason Codes

{reason_lines}

### Caveats

- L1 draft output is not final accuracy, not a training label, not a benchmark metric, and not frozen schema.
- No training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference was run.
- Malicious coverage may be absent if no malicious manifest was supplied.

## English Version

> This report is a runtime wiring, draft sidecar completeness, rule-routing sanity, and latency smoke benchmark. It is not a final model accuracy evaluation.

### Inputs

- manifests: `{'; '.join(manifests) if manifests else 'none'}`
- output_dir: `{output_dir}`

### Buckets

{bucket_lines}

### Summary

- total_samples: `{summary.get('total_samples')}`
- runtime_success_count: `{summary.get('runtime_success_count')}`
- runtime_error_count: `{summary.get('runtime_error_count')}`
- l1_draft_ok_count: `{summary.get('l1_draft_ok_count')}`
- l1_draft_error_count: `{summary.get('l1_draft_error_count')}`
- missing_sidecar_count: `{summary.get('missing_sidecar_count')}`
- official_fields_mismatch_count: `{summary.get('official_fields_mismatch_count')}`
- flag_off_debug_sidecar_count: `{summary.get('flag_off_debug_sidecar_count')}`

### Duration

- avg_l1_draft_duration_ms: `{summary.get('avg_l1_draft_duration_ms')}`
- p50_l1_draft_duration_ms: `{summary.get('p50_l1_draft_duration_ms')}`
- p95_l1_draft_duration_ms: `{summary.get('p95_l1_draft_duration_ms')}`
- p99_l1_draft_duration_ms: `{summary.get('p99_l1_draft_duration_ms')}`
- avg_total_runtime_duration_ms: `{summary.get('avg_total_runtime_duration_ms')}`

### Routing Counts

- routing_need_text_tower_count: `{summary.get('routing_need_text_tower_count')}`
- routing_need_ocr_count: `{summary.get('routing_need_ocr_count')}`
- routing_need_yolo_count: `{summary.get('routing_need_yolo_count')}`
- routing_need_review_count: `{summary.get('routing_need_review_count')}`

### Rule Router Metrics

- rule_assessment distribution: `{json.dumps(summary.get('rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- high_risk_candidate count: `{summary.get('high_risk_candidate_count')}`
- low_risk_candidate count: `{summary.get('low_risk_candidate_count')}`
- benign_hard_negative_candidate count: `{summary.get('benign_hard_negative_candidate_count')}`
- final-like label leakage warning count: `{summary.get('final_like_label_leakage_warning_count')}`

### B00 / B01 Rule Router Breakout

- B00 rule_assessment distribution: `{json.dumps(summary.get('b00_rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- B00 high_risk_candidate count: `{summary.get('b00_high_risk_candidate_count')}`
- B01 rule_assessment distribution: `{json.dumps(summary.get('b01_rule_assessment_distribution') or {{}}, ensure_ascii=False)}`
- B01 need_review count: `{summary.get('b01_need_review_count')}`
- B01 need_ocr count: `{summary.get('b01_need_ocr_count')}`
- B01 high_risk_candidate count: `{summary.get('b01_high_risk_candidate_count')}`

### B00 Top Reason Codes

{b00_reason_lines}

### B01 Top Reason Codes

{b01_reason_lines}

### Rule-Routing Sanity Note

- This benchmark reports rule router assessments and routing hints only.
- It does not evaluate final model accuracy, because the L1 Decision Head is not run.
- If B01 has many high-risk candidates in larger runs, treat this as routing calibration evidence, not final model accuracy.

### Top Reason Codes

{reason_lines}

### Caveats

- L1 draft output is not final accuracy, not a training label, not a benchmark metric, and not frozen schema.
- No training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference was run.
- Malicious coverage may be absent if no malicious manifest was supplied.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    output_dir = ensure_dir(Path(args.output_dir))
    candidates = load_candidate_rows(args)
    selected = sample_rows(candidates, limit_per_bucket=max(0, args.limit_per_bucket), seed=args.seed)
    if not selected:
        raise ValueError("no benchmark samples selected")

    rows = [benchmark_row(row, output_dir) for row in selected]
    summary = build_summary(rows)
    add_reason_code_summary(rows, output_dir, summary)

    write_jsonl(output_dir / RESULTS_JSONL, rows)
    write_summary_csv(output_dir / SUMMARY_CSV, summary)
    write_errors_csv(output_dir / ERRORS_CSV, rows)
    manifests = [
        item
        for item in [
            args.benign_train,
            args.benign_val,
            args.benign_test,
            *args.input_manifest,
            *args.malicious_manifest,
        ]
        if item
    ]
    write_report(output_dir / REPORT_MD, summary, manifests=manifests, output_dir=output_dir)
    print(json.dumps({"output_dir": str(output_dir), **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
