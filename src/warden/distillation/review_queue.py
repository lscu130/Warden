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
    formula_concepts = record.get("formula_concepts", {}) if isinstance(record.get("formula_concepts"), dict) else {}
    formula_result = formula_concepts.get("formula_result", {}) if isinstance(formula_concepts.get("formula_result"), dict) else {}
    risk_bearing = (
        formula_concepts.get("risk_bearing_engagement", {})
        if isinstance(formula_concepts.get("risk_bearing_engagement"), dict)
        else {}
    )
    url_claim = formula_concepts.get("url_claim_analysis", {}) if isinstance(formula_concepts.get("url_claim_analysis"), dict) else {}
    visible_impersonation = (
        formula_concepts.get("visible_impersonation_analysis", {})
        if isinstance(formula_concepts.get("visible_impersonation_analysis"), dict)
        else {}
    )
    funnel_affordance = (
        formula_concepts.get("funnel_affordance_analysis", {})
        if isinstance(formula_concepts.get("funnel_affordance_analysis"), dict)
        else {}
    )
    quality_flags = record.get("quality_flags", {}) if isinstance(record.get("quality_flags"), dict) else {}

    return {
        "record_id": record["record_id"],
        "sample_key": record.get("sample_key"),
        "sample_id": record["sample_id"],
        "sample_path": record["sample_path"],
        "priority": _severity(review_reasons),
        "source_manifest": record.get("source_manifest"),
        "source_split": record.get("source_split"),
        "teacher_run_id": record.get("teacher_run_id"),
        "teacher_profile": record.get("teacher_profile"),
        "prompt_template_version": record.get("prompt_template_version"),
        "attempt_id": record.get("attempt_id"),
        "severity": _severity(review_reasons),
        "review_reason": sorted(set(review_reasons))[0] if review_reasons else "needs_human_review",
        "review_reasons": sorted(set(review_reasons)),
        "quality_flags": quality_flags,
        "short_evidence_context": {
            "source_url": record.get("source_url"),
            "canonical_url": record.get("canonical_url"),
            "summary": record.get("evidence_pack_summary", {}),
        },
        "formula_failure_mode": formula_result.get("formula_basis", "unknown"),
        "risk_bearing_engagement_uncertainty": quality_flags.get("risk_bearing_engagement_unclear", False),
        "url_claim_state": url_claim,
        "visible_impersonation_state": visible_impersonation,
        "funnel_affordance_state": funnel_affordance,
        "concept_level_review": {
            "claimed_identity_candidates_present": "claimed_identity_candidates" in record,
            "relation_judgments_present": isinstance(record.get("text_semantic_concepts"), dict)
            and "relation_judgments" in record["text_semantic_concepts"],
            "evidence_state_present": isinstance(record.get("text_semantic_concepts"), dict)
            and "evidence_state" in record["text_semantic_concepts"],
            "threat_action_candidate_present": isinstance(record.get("text_semantic_concepts"), dict)
            and "threat_action_candidate" in record["text_semantic_concepts"],
            "review_reasons": [
                reason
                for reason in review_reasons
                if "concept" in reason or "text_semantic_concepts" in reason
            ],
        },
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
        "suggested_next_action": suggested_action,
        "do_not_train_as_gold": record.get("do_not_train_as_gold") is True,
        "not_train_as_gold": record.get("do_not_train_as_gold") is True,
        "diagnostic_only": record.get("diagnostic_only") is True,
    }
