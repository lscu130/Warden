"""Review queue helpers for mock distillation records."""

from __future__ import annotations

from typing import Any


def _severity(review_reasons: list[str]) -> str:
    if any("schema" in reason or "validation" in reason for reason in review_reasons):
        return "blocker"
    if any(reason in {"bad_json_artifact", "visible_text_missing", "url_json_missing"} for reason in review_reasons):
        return "high"
    if review_reasons:
        return "medium"
    return "low"


def build_review_queue_record(record: dict[str, Any]) -> dict[str, Any] | None:
    review_reasons = list(record.get("review_reasons") or [])
    if record.get("split") in {"val", "test"} and record.get("diagnostic_only") is True:
        review_reasons.append("val_test_diagnostic_only_record")
    if not review_reasons and not record.get("quality_flags", {}).get("needs_human_review"):
        return None

    suggested_action = "inspect"
    if "bad_json_artifact" in review_reasons:
        suggested_action = "repair_artifact"
    elif "url_json_missing" in review_reasons or "visible_text_missing" in review_reasons:
        suggested_action = "recrawl"
    elif "val_test_diagnostic_only_record" in review_reasons:
        suggested_action = "keep_diagnostic_only"

    return {
        "record_id": record["record_id"],
        "sample_key": record.get("sample_key"),
        "sample_id": record["sample_id"],
        "sample_path": record["sample_path"],
        "source_manifest": record.get("source_manifest"),
        "source_split": record.get("source_split"),
        "teacher_run_id": record.get("teacher_run_id"),
        "teacher_profile": record.get("teacher_profile"),
        "prompt_template_version": record.get("prompt_template_version"),
        "attempt_id": record.get("attempt_id"),
        "severity": _severity(review_reasons),
        "review_reason": sorted(set(review_reasons))[0] if review_reasons else "needs_human_review",
        "review_reasons": sorted(set(review_reasons)),
        "quality_flags": record.get("quality_flags", {}),
        "evidence_context": {
            "summary": record.get("evidence_pack_summary", {}),
            "input_modalities": record.get("input_modalities", []),
        },
        "artifact_references": {
            "sample_path": record.get("sample_path"),
            "raw_teacher_output_path": None,
            "prompt_path": None,
            "repair_path": None,
        },
        "suggested_action": suggested_action,
        "do_not_train_as_gold": record.get("do_not_train_as_gold") is True,
        "diagnostic_only": record.get("diagnostic_only") is True,
    }
