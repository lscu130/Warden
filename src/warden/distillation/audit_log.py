"""Audit and report writers for the distillation skeleton."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_audit(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, audit: dict[str, Any]) -> None:
    lines = [
        "# Warden Distillation Skeleton Run Report",
        "",
        "## 中文版",
        "",
        "本报告来自 dry-run / mock distillation runner skeleton。没有真实 teacher call，输出不得作为 gold label 或训练标签。",
        "",
        "## English Version",
        "",
        "This report was produced by the dry-run / mock distillation runner skeleton.",
        "",
        "- No real teacher calls were made.",
        "- Outputs are mock/dry-run only.",
        "- All records must keep `do_not_train_as_gold=true`.",
        "- All records must keep `diagnostic_only=true`.",
        "",
        "## Counts",
        "",
    ]
    for key in [
        "run_id",
        "teacher_run_id",
        "source_manifest",
        "source_split",
        "total_rows_seen",
        "processed_count",
        "skipped_existing_count",
        "error_count",
        "review_queue_count",
        "schema_valid_count",
        "schema_invalid_count",
        "records_written",
        "records_valid",
        "records_invalid",
        "attempt_count",
        "mock_teacher_calls",
        "real_teacher_calls",
        "external_api_calls",
        "teacher_calls",
        "ocr_calls",
        "yolo_calls",
        "clip_calls",
        "do_not_train_as_gold_failures",
        "diagnostic_only_failures",
    ]:
        lines.append(f"- `{key}`: {audit.get(key)}")
    lines.extend(
        [
            "",
            "## Readiness Summary",
            "",
            f"- `missing_required_readiness_fields`: {audit.get('missing_required_readiness_fields')}",
            f"- `schema_validation_errors_by_type`: {audit.get('schema_validation_errors_by_type')}",
            f"- `review_reason_counts`: {audit.get('review_reason_counts')}",
            f"- `duplicate_record_ids`: {audit.get('duplicate_record_ids')}",
            f"- `duplicate_sample_keys`: {audit.get('duplicate_sample_keys')}",
            f"- `output_files`: {audit.get('output_files')}",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
