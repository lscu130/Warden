#!/usr/bin/env python3
"""Read-only inspection helper for Warden distillation skeleton outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_FILES = [
    "distillation_records.jsonl",
    "review_queue.jsonl",
    "attempts.jsonl",
    "validation_summaries.jsonl",
    "run_audit.json",
    "run_report.md",
    "adapter_readiness_report.md",
    "errors.jsonl",
    "prompt_snapshots",
    "raw_outputs",
    "repaired_outputs",
]

REQUIRED_RECORD_FIELDS = [
    "schema_version",
    "record_id",
    "sample_key",
    "sample_id",
    "sample_path",
    "source_manifest",
    "source_split",
    "source_url",
    "canonical_url",
    "capture_id",
    "evidence_pack_id",
    "split",
    "diagnostic_only",
    "do_not_train_as_gold",
    "teacher_provider",
    "teacher_model",
    "teacher_role",
    "teacher_profile",
    "teacher_run_id",
    "prompt_template_id",
    "prompt_template_version",
    "prompt_snapshot_path",
    "input_modalities",
    "fallback_reason",
    "image_input_expected",
    "image_input_passed_to_teacher",
    "modality_guard_status",
    "raw_output_path",
    "repaired_output_path",
    "validation_status",
    "validation_errors",
    "attempt_id",
    "attempt_index",
    "attempt_status",
    "repair_attempted",
    "repair_reason",
    "token_usage_placeholder",
    "cost_placeholder",
    "latency_ms_placeholder",
    "provider_request_id_placeholder",
    "failure_category",
    "retry_allowed",
    "rollback_required",
    "evidence_pack_summary",
    "rule_router_observation",
    "formula_semantics",
    "formula_concepts",
    "observed_evidence_summary",
    "manipulative_context",
    "risk_bearing_engagement",
    "context_engagement_relation",
    "evidence_sufficiency",
    "formula_result",
    "url_claim_analysis",
    "visible_impersonation_analysis",
    "funnel_affordance_analysis",
    "risk_outcome_axes",
    "claimed_identity_candidates",
    "text_semantic_concepts",
    "vision_evidence",
    "decision_head_auxiliary_targets",
    "quality_flags",
    "review_reasons",
    "validation",
    "error_status",
    "record_hash",
    "evidence_pack_hash",
    "prompt_input_hash",
    "created_at",
]

FUTURE_READINESS_FIELDS = [
    "sample_key",
    "source_manifest",
    "source_split",
    "evidence_pack_id",
    "teacher_provider",
    "teacher_profile",
    "teacher_run_id",
    "prompt_template_id",
    "prompt_template_version",
    "prompt_snapshot_path",
    "image_input_expected",
    "image_input_passed_to_teacher",
    "modality_guard_status",
    "raw_output_path",
    "repaired_output_path",
    "validation_status",
    "validation_errors",
    "attempt_status",
    "repair_attempted",
    "repair_reason",
    "token_usage_placeholder",
    "cost_placeholder",
    "latency_ms_placeholder",
    "provider_request_id_placeholder",
    "failure_category",
    "retry_allowed",
    "rollback_required",
    "validation",
    "error_status",
    "attempt_id",
    "attempt_index",
    "created_at_utc",
    "image_input_policy",
    "visual_evidence_source",
    "record_hash",
    "evidence_pack_hash",
    "prompt_input_hash",
]

REQUIRED_CONCEPT_FIELD_PATHS = [
    ("formula_semantics",),
    ("formula_concepts",),
    ("formula_concepts", "manipulative_context"),
    ("formula_concepts", "action_surface"),
    ("formula_concepts", "risk_bearing_engagement"),
    ("formula_concepts", "risk_bearing_engagement", "direct_high_risk_action"),
    ("formula_concepts", "risk_bearing_engagement", "routed_high_risk_action"),
    ("formula_concepts", "risk_bearing_engagement", "action_preparation"),
    ("formula_concepts", "risk_bearing_engagement", "deceptive_funnel_priming"),
    ("formula_concepts", "context_engagement_relation"),
    ("formula_concepts", "evidence_sufficiency"),
    ("formula_concepts", "formula_result"),
    ("formula_concepts", "url_claim_analysis"),
    ("formula_concepts", "visible_impersonation_analysis"),
    ("formula_concepts", "funnel_affordance_analysis"),
    ("formula_concepts", "risk_outcome_axes"),
    ("claimed_identity_candidates",),
    ("text_semantic_concepts", "claimed_identity_candidates"),
    ("text_semantic_concepts", "identity_claim"),
    ("text_semantic_concepts", "action_surface"),
    ("text_semantic_concepts", "behavior_context"),
    ("text_semantic_concepts", "relation_judgments"),
    ("text_semantic_concepts", "evidence_state"),
    ("text_semantic_concepts", "threat_action_candidate"),
    ("text_semantic_concepts", "concept_level_evaluation_readiness"),
    ("decision_head_auxiliary_targets",),
]

FORBIDDEN_FIELDS = {
    "final_gold_label",
    "final_training_label",
    "gold_malicious_label",
    "chain_of_thought",
    "hidden_reasoning",
    "teacher_cot",
}


def _load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    issues: list[str] = []
    if not path.exists():
        return records, [f"missing file: {path.name}"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"{path.name}:{line_number}: JSON parse error: {exc}")
            continue
        if not isinstance(payload, dict):
            issues.append(f"{path.name}:{line_number}: row is not an object")
            continue
        records.append(payload)
    return records, issues


def _walk_forbidden(payload: Any, path: str = "") -> list[str]:
    issues: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            current = f"{path}.{key}" if path else key
            if key in FORBIDDEN_FIELDS:
                issues.append(current)
            issues.extend(_walk_forbidden(value, current))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            issues.extend(_walk_forbidden(value, f"{path}[{index}]"))
    return issues


def _report_count(report_text: str, key: str) -> int | None:
    match = re.search(rf"`{re.escape(key)}`:\s*(\d+)", report_text)
    if not match:
        return None
    return int(match.group(1))


def _missing_path_count(records: list[dict[str, Any]], path: tuple[str, ...]) -> int:
    count = 0
    for record in records:
        current: Any = record
        for part in path:
            if not isinstance(current, dict) or part not in current:
                count += 1
                break
            current = current[part]
    return count


def inspect_output_dir(output_dir: Path) -> dict[str, Any]:
    files = {name: output_dir / name for name in EXPECTED_FILES}
    missing_files = [name for name, path in files.items() if not path.exists()]
    file_sizes = {name: (path.stat().st_size if path.exists() else None) for name, path in files.items()}

    records, record_issues = _load_jsonl(files["distillation_records.jsonl"])
    review_records, review_issues = _load_jsonl(files["review_queue.jsonl"])
    attempt_records, attempt_issues = _load_jsonl(files["attempts.jsonl"])
    validation_records, validation_issues = _load_jsonl(files["validation_summaries.jsonl"])
    error_records, error_issues = _load_jsonl(files["errors.jsonl"])

    audit: dict[str, Any] = {}
    audit_issues: list[str] = []
    if files["run_audit.json"].exists():
        try:
            audit_payload = json.loads(files["run_audit.json"].read_text(encoding="utf-8-sig"))
            if isinstance(audit_payload, dict):
                audit = audit_payload
            else:
                audit_issues.append("run_audit.json is not an object")
        except json.JSONDecodeError as exc:
            audit_issues.append(f"run_audit.json JSON parse error: {exc}")

    report_text = files["run_report.md"].read_text(encoding="utf-8-sig") if files["run_report.md"].exists() else ""
    report_count_mismatches: list[str] = []
    for key in (
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
    ):
        reported = _report_count(report_text, key)
        audited = audit.get(key)
        if reported is None:
            report_count_mismatches.append(f"{key}: missing from run_report.md")
        elif audited != reported:
            report_count_mismatches.append(f"{key}: audit={audited!r} report={reported!r}")

    record_id_counts = Counter(str(record.get("record_id", "")) for record in records)
    sample_id_counts = Counter(str(record.get("sample_id", "")) for record in records)
    sample_key_counts = Counter(str(record.get("sample_key", "")) for record in records)
    duplicate_record_ids = sorted(key for key, count in record_id_counts.items() if key and count > 1)
    duplicate_sample_ids = sorted(key for key, count in sample_id_counts.items() if key and count > 1)
    duplicate_sample_keys = sorted(key for key, count in sample_key_counts.items() if key and count > 1)

    missing_required_fields: dict[str, int] = {}
    for field in REQUIRED_RECORD_FIELDS:
        count = sum(1 for record in records if field not in record)
        if count:
            missing_required_fields[field] = count

    missing_future_fields: dict[str, int] = {}
    for field in FUTURE_READINESS_FIELDS:
        count = sum(1 for record in records if field not in record)
        if count:
            missing_future_fields[field] = count

    missing_concept_fields: dict[str, int] = {}
    for path in REQUIRED_CONCEPT_FIELD_PATHS:
        count = _missing_path_count(records, path)
        if count:
            missing_concept_fields[".".join(path)] = count

    forbidden_hits: list[str] = []
    for index, record in enumerate(records, start=1):
        for hit in _walk_forbidden(record):
            forbidden_hits.append(f"record[{index}].{hit}")

    non_gold_failures = sum(1 for record in records if record.get("do_not_train_as_gold") is not True)
    diagnostic_failures = sum(1 for record in records if record.get("diagnostic_only") is not True)
    schema_version_counts = Counter(str(record.get("schema_version")) for record in records)
    teacher_model_counts = Counter(str(record.get("teacher_model")) for record in records)
    split_counts = Counter(str(record.get("split")) for record in records)

    linked_record_ids = {str(record.get("record_id")) for record in records}
    unlinked_review_rows = [
        index
        for index, review in enumerate(review_records, start=1)
        if str(review.get("record_id")) not in linked_record_ids
    ]
    review_reason_counts = Counter(
        reason
        for review in review_records
        for reason in review.get("review_reasons", [])
        if isinstance(review.get("review_reasons"), list)
    )
    review_rows_without_reasons = sum(
        1 for review in review_records if not isinstance(review.get("review_reasons"), list) or not review["review_reasons"]
    )
    review_rows_without_action = sum(1 for review in review_records if not review.get("suggested_action"))

    call_counter_values = {
        key: audit.get(key)
        for key in (
            "teacher_calls",
            "real_teacher_calls",
            "mock_teacher_calls",
            "external_api_calls",
            "ocr_calls",
            "yolo_calls",
            "clip_calls",
        )
    }

    machine_ok = not (
        missing_files
        or record_issues
        or review_issues
        or attempt_issues
        or validation_issues
        or error_issues
        or audit_issues
        or report_count_mismatches
        or audit.get("adapter_readiness_status") != "ready_for_no_network_dry_run"
        or audit.get("live_teacher_readiness") != "not_ready_for_live_teacher"
        or missing_future_fields
        or missing_concept_fields
        or forbidden_hits
        or non_gold_failures
        or diagnostic_failures
        or duplicate_record_ids
        or duplicate_sample_keys
    )

    return {
        "output_dir": str(output_dir),
        "expected_files": EXPECTED_FILES,
        "missing_files": missing_files,
        "file_sizes": file_sizes,
        "record_count": len(records),
        "review_queue_count": len(review_records),
        "attempt_count": len(attempt_records),
        "validation_summary_count": len(validation_records),
        "error_count": len(error_records),
        "record_parse_issues": record_issues,
        "review_parse_issues": review_issues,
        "attempt_parse_issues": attempt_issues,
        "validation_parse_issues": validation_issues,
        "error_parse_issues": error_issues,
        "audit_issues": audit_issues,
        "report_count_mismatches": report_count_mismatches,
        "audit_counts": {
            key: audit.get(key)
            for key in (
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
            )
        },
        "adapter_readiness_status": audit.get("adapter_readiness_status"),
        "live_teacher_readiness": audit.get("live_teacher_readiness"),
        "output_path_inventory": audit.get("output_path_inventory"),
        "cost_token_placeholders": audit.get("cost_token_placeholders"),
        "call_counters": call_counter_values,
        "schema_version_counts": dict(schema_version_counts),
        "teacher_model_counts": dict(teacher_model_counts),
        "split_counts": dict(split_counts),
        "missing_required_fields": missing_required_fields,
        "missing_future_readiness_fields": missing_future_fields,
        "missing_required_concept_fields": missing_concept_fields,
        "duplicate_record_ids": duplicate_record_ids,
        "duplicate_sample_ids": duplicate_sample_ids,
        "duplicate_sample_keys": duplicate_sample_keys,
        "forbidden_field_hits": forbidden_hits,
        "non_gold_failures": non_gold_failures,
        "diagnostic_failures": diagnostic_failures,
        "unlinked_review_rows": unlinked_review_rows,
        "review_reason_counts": dict(review_reason_counts),
        "review_rows_without_reasons": review_rows_without_reasons,
        "review_rows_without_action": review_rows_without_action,
        "machine_readiness_ok": machine_ok,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect Warden distillation skeleton output files.")
    parser.add_argument("--output-dir", required=True, help="Distillation skeleton output directory.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    result = inspect_output_dir(Path(args.output_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
