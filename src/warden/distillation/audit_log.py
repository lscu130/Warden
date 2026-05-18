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
        "schema_version",
        "prompt_template_version",
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
        "repair_count",
        "validation_summary_count",
        "validation_pass_count",
        "validation_fail_count",
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
            f"- `missing_required_concept_fields`: {audit.get('missing_required_concept_fields')}",
            f"- `concept_level_readiness`: {audit.get('concept_level_readiness')}",
            f"- `schema_validation_errors_by_type`: {audit.get('schema_validation_errors_by_type')}",
            f"- `review_reason_counts`: {audit.get('review_reason_counts')}",
            f"- `duplicate_record_ids`: {audit.get('duplicate_record_ids')}",
            f"- `duplicate_sample_keys`: {audit.get('duplicate_sample_keys')}",
            f"- `output_path_inventory`: {audit.get('output_path_inventory')}",
            f"- `output_files`: {audit.get('output_files')}",
            f"- `cost_token_placeholders`: {audit.get('cost_token_placeholders')}",
            f"- `adapter_readiness_status`: {audit.get('adapter_readiness_status')}",
            f"- `live_teacher_readiness`: {audit.get('live_teacher_readiness')}",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_adapter_readiness_report(path: Path, audit: dict[str, Any]) -> None:
    lines = [
        "# Warden Distillation Adapter Readiness Report",
        "",
        "## 中文版",
        "",
        "本报告只说明 no-network adapter-readiness baseline。没有真实 provider/API/OCR/YOLO/CLIP 调用，也不代表 live teacher 已获批准。",
        "",
        "## English Version",
        "",
        "This report documents no-network adapter-readiness only. It is not live-teacher approval.",
        "",
        "## Status",
        "",
        f"- `adapter_readiness_status`: {audit.get('adapter_readiness_status')}",
        f"- `live_teacher_readiness`: {audit.get('live_teacher_readiness')}",
        f"- `schema_version`: {audit.get('schema_version')}",
        f"- `prompt_template_versions`: {audit.get('prompt_template_versions')}",
        f"- `teacher_profiles`: {audit.get('teacher_profiles')}",
        "",
        "## Counts",
        "",
        f"- `attempt_count`: {audit.get('attempt_count')}",
        f"- `repair_count`: {audit.get('repair_count')}",
        f"- `validation_pass_count`: {audit.get('validation_pass_count')}",
        f"- `validation_fail_count`: {audit.get('validation_fail_count')}",
        f"- `review_reason_counts`: {audit.get('review_reason_counts')}",
        "",
        "## Call Counters",
        "",
        f"- `teacher_calls`: {audit.get('teacher_calls')}",
        f"- `real_teacher_calls`: {audit.get('real_teacher_calls')}",
        f"- `external_api_calls`: {audit.get('external_api_calls')}",
        f"- `ocr_calls`: {audit.get('ocr_calls')}",
        f"- `yolo_calls`: {audit.get('yolo_calls')}",
        f"- `clip_calls`: {audit.get('clip_calls')}",
        "",
        "## Output Path Inventory",
        "",
        f"- `output_path_inventory`: {audit.get('output_path_inventory')}",
        "",
        "## Guardrails",
        "",
        "- `ready_for_live_teacher`: false",
        "- `ready_for_training_ingestion`: false",
        "- `provider_budget_approved`: false",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
