"""Minimal standard-library validation for mock distillation records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schema import (
    ALLOWED_ENGAGEMENT_RELATION_TYPES,
    ALLOWED_FINAL_LABEL_ADVISORY,
    ALLOWED_MALICIOUS_BASIS_ADVISORY,
    ALLOWED_RELATION_TYPES,
    ALLOWED_SPLITS,
    FORBIDDEN_FIELDS,
    PROMPT_TEMPLATE_ID,
    PROMPT_TEMPLATE_VERSION,
    REQUIRED_RECORD_KEYS,
    SCHEMA_VERSION,
    TEACHER_MODEL,
    TEACHER_PROVIDER,
    TEACHER_PROFILE,
    VALIDATOR_VERSION,
    V03_REVIEW_REASONS,
)


REQUIRED_CONCEPT_KEYS = (
    "identity_claim",
    "action_surface",
    "behavior_context",
    "relation_judgments",
    "evidence_state",
    "threat_action_candidate",
    "concept_level_evaluation_readiness",
)

REQUIRED_FORMULA_CONCEPT_KEYS = (
    "manipulative_context",
    "action_surface",
    "risk_bearing_engagement",
    "context_engagement_relation",
    "evidence_sufficiency",
    "formula_result",
    "url_claim_analysis",
    "visible_impersonation_analysis",
    "funnel_affordance_analysis",
    "risk_outcome_axes",
)


@dataclass(frozen=True)
class DistillationValidationResult:
    valid: bool
    issues: list[str]


def _walk_forbidden(payload: Any, path: str = "") -> list[str]:
    issues: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            current = f"{path}.{key}" if path else key
            if key in FORBIDDEN_FIELDS:
                issues.append(f"forbidden field present: {current}")
            issues.extend(_walk_forbidden(value, current))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            issues.extend(_walk_forbidden(value, f"{path}[{index}]"))
    return issues


def validate_distillation_record(record: dict[str, Any]) -> DistillationValidationResult:
    issues: list[str] = []
    for key in REQUIRED_RECORD_KEYS:
        if key not in record:
            issues.append(f"missing required key: {key}")
    if record.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"schema_version must be {SCHEMA_VERSION}")
    if record.get("teacher_model") != TEACHER_MODEL:
        issues.append(f"teacher_model must be {TEACHER_MODEL}")
    if record.get("teacher_provider") != TEACHER_PROVIDER:
        issues.append(f"teacher_provider must be {TEACHER_PROVIDER}")
    if record.get("teacher_profile") != TEACHER_PROFILE:
        issues.append(f"teacher_profile must be {TEACHER_PROFILE}")
    if record.get("prompt_template_id") != PROMPT_TEMPLATE_ID:
        issues.append(f"prompt_template_id must be {PROMPT_TEMPLATE_ID}")
    if record.get("prompt_template_version") != PROMPT_TEMPLATE_VERSION:
        issues.append(f"prompt_template_version must be {PROMPT_TEMPLATE_VERSION}")
    if record.get("do_not_train_as_gold") is not True:
        issues.append("do_not_train_as_gold must be true")
    if record.get("diagnostic_only") is not True:
        issues.append("diagnostic_only must be true")
    if record.get("image_input_passed_to_teacher") is not False:
        issues.append("image_input_passed_to_teacher must be false in mock mode")
    if record.get("image_input_expected") is not False:
        issues.append("image_input_expected must be false in mock mode")
    if record.get("image_input_policy") != "not_supported_in_mock":
        issues.append("image_input_policy must be not_supported_in_mock in mock mode")
    if record.get("modality_guard_status") != "mock_no_image_input":
        issues.append("modality_guard_status must be mock_no_image_input in mock mode")
    if record.get("visual_evidence_source") != "none":
        issues.append("visual_evidence_source must be none in mock mode")
    if record.get("attempt_status") not in {"mock_completed", "schema_validation_failed"}:
        issues.append("attempt_status has invalid value")
    if record.get("repair_attempted") is not False:
        issues.append("repair_attempted must be false in mock mode")
    if record.get("repair_reason") is not None:
        issues.append("repair_reason must be null in mock mode")
    if record.get("repaired_output_path") is not None:
        issues.append("repaired_output_path must be null when repair_attempted is false")
    if record.get("validation_status") not in {"pending", "passed", "failed"}:
        issues.append("validation_status has invalid value")
    if not isinstance(record.get("validation_errors"), list):
        issues.append("validation_errors must be a list")
    if not isinstance(record.get("token_usage_placeholder"), dict) or record["token_usage_placeholder"].get("mock_only") is not True:
        issues.append("token_usage_placeholder.mock_only must be true")
    if not isinstance(record.get("cost_placeholder"), dict) or record["cost_placeholder"].get("mock_only") is not True:
        issues.append("cost_placeholder.mock_only must be true")
    if record.get("latency_ms_placeholder") is not None:
        issues.append("latency_ms_placeholder must be null in mock mode")
    if record.get("provider_request_id_placeholder") is not None:
        issues.append("provider_request_id_placeholder must be null in mock mode")
    if record.get("failure_category") is not None:
        issues.append("failure_category must be null for valid mock records")
    if record.get("retry_allowed") is not False:
        issues.append("retry_allowed must be false in mock mode")
    if record.get("rollback_required") is not False:
        issues.append("rollback_required must be false in mock mode")
    for key in ("prompt_snapshot_path", "raw_output_path"):
        if not isinstance(record.get(key), str) or not record.get(key):
            issues.append(f"{key} must be a non-empty string")
    formula_semantics = record.get("formula_semantics")
    if not isinstance(formula_semantics, dict):
        issues.append("formula_semantics must be an object")
    else:
        if formula_semantics.get("web_se_formula") != "EvidenceSufficient(ManipulativeContext AND RiskBearingEngagement)":
            issues.append("formula_semantics.web_se_formula has invalid value")
        if formula_semantics.get("risk_bearing_engagement_formula") != (
            "DirectHighRiskAction OR RoutedHighRiskAction OR ActionPreparation OR DeceptiveFunnelPriming"
        ):
            issues.append("formula_semantics.risk_bearing_engagement_formula has invalid value")
    formula_concepts = record.get("formula_concepts")
    if not isinstance(formula_concepts, dict):
        issues.append("formula_concepts must be an object")
    else:
        for key in REQUIRED_FORMULA_CONCEPT_KEYS:
            if key not in formula_concepts:
                issues.append(f"missing required formula concept key: formula_concepts.{key}")
        action_surface_formula = formula_concepts.get("action_surface")
        if not isinstance(action_surface_formula, dict):
            issues.append("formula_concepts.action_surface must be an object")
        elif action_surface_formula.get("not_threat_by_itself") is not True:
            issues.append("formula_concepts.action_surface.not_threat_by_itself must be true")
        engagement = formula_concepts.get("risk_bearing_engagement")
        if not isinstance(engagement, dict):
            issues.append("formula_concepts.risk_bearing_engagement must be an object")
        else:
            if not isinstance(engagement.get("present"), bool):
                issues.append("formula_concepts.risk_bearing_engagement.present must be a bool")
            for key in (
                "direct_high_risk_action",
                "routed_high_risk_action",
                "action_preparation",
                "deceptive_funnel_priming",
            ):
                if key not in engagement:
                    issues.append(f"missing required engagement key: formula_concepts.risk_bearing_engagement.{key}")
            if engagement.get("action_surface_is_not_automatically_risk_bearing_engagement") is not True:
                issues.append("formula_concepts.risk_bearing_engagement must preserve action-surface boundary")
        relation = formula_concepts.get("context_engagement_relation")
        if not isinstance(relation, dict):
            issues.append("formula_concepts.context_engagement_relation must be an object")
        else:
            if relation.get("relation_type") not in ALLOWED_ENGAGEMENT_RELATION_TYPES and relation.get("relation_type") not in ALLOWED_RELATION_TYPES:
                issues.append("formula_concepts.context_engagement_relation.relation_type has invalid value")
            if relation.get("unknown_relation_is_not_malicious") is not True:
                issues.append("formula_concepts.context_engagement_relation must preserve unknown relation rule")
        sufficiency = formula_concepts.get("evidence_sufficiency")
        if not isinstance(sufficiency, dict):
            issues.append("formula_concepts.evidence_sufficiency must be an object")
        elif not isinstance(sufficiency.get("sufficient_for_web_se_threat"), bool):
            issues.append("formula_concepts.evidence_sufficiency.sufficient_for_web_se_threat must be a bool")
        formula_result = formula_concepts.get("formula_result")
        if not isinstance(formula_result, dict):
            issues.append("formula_concepts.formula_result must be an object")
        elif not isinstance(formula_result.get("web_se_threat_formula_satisfied"), bool):
            issues.append("formula_concepts.formula_result.web_se_threat_formula_satisfied must be a bool")
        for key in (
            "url_claim_analysis",
            "visible_impersonation_analysis",
            "funnel_affordance_analysis",
        ):
            if not isinstance(formula_concepts.get(key), dict):
                issues.append(f"formula_concepts.{key} must be an object")
        if not isinstance(formula_concepts.get("risk_outcome_axes"), list):
            issues.append("formula_concepts.risk_outcome_axes must be a list")
    for key in (
        "observed_evidence_summary",
        "manipulative_context",
        "risk_bearing_engagement",
        "context_engagement_relation",
        "evidence_sufficiency",
        "formula_result",
        "url_claim_analysis",
        "visible_impersonation_analysis",
        "funnel_affordance_analysis",
    ):
        if not isinstance(record.get(key), dict):
            issues.append(f"{key} must be an object")
    if not isinstance(record.get("risk_outcome_axes"), list):
        issues.append("risk_outcome_axes must be a list")
    if record.get("split") not in ALLOWED_SPLITS:
        issues.append("split has invalid value")
    if not isinstance(record.get("review_reasons"), list):
        issues.append("review_reasons must be a list")
    else:
        for reason in record.get("review_reasons", []):
            if reason not in V03_REVIEW_REASONS:
                issues.append(f"review_reasons contains non-V0.3 reason: {reason}")
    if not isinstance(record.get("claimed_identity_candidates"), list):
        issues.append("claimed_identity_candidates must be a list")
    concepts = record.get("text_semantic_concepts")
    if not isinstance(concepts, dict):
        issues.append("text_semantic_concepts must be an object")
    else:
        for key in REQUIRED_CONCEPT_KEYS:
            if key not in concepts:
                issues.append(f"missing required concept key: text_semantic_concepts.{key}")
        if concepts.get("claimed_identity_candidates") != record.get("claimed_identity_candidates"):
            issues.append("text_semantic_concepts.claimed_identity_candidates must mirror top-level claimed_identity_candidates")
        action_surface = concepts.get("action_surface")
        if not isinstance(action_surface, dict):
            issues.append("text_semantic_concepts.action_surface must be an object")
        elif action_surface.get("action_surface_is_not_automatically_threat_action") is not True:
            issues.append("text_semantic_concepts.action_surface must preserve action surface non-threat rule")
        relation_judgments = concepts.get("relation_judgments")
        if not isinstance(relation_judgments, dict):
            issues.append("text_semantic_concepts.relation_judgments must be an object")
        elif relation_judgments.get("unknown_is_not_malicious") is not True:
            issues.append("text_semantic_concepts.relation_judgments must preserve unknown relation rule")
        evidence_state = concepts.get("evidence_state")
        if not isinstance(evidence_state, dict):
            issues.append("text_semantic_concepts.evidence_state must be an object")
        elif evidence_state.get("payload_not_observed_is_not_automatic_benign") is not True:
            issues.append("text_semantic_concepts.evidence_state must preserve payload-not-observed rule")
        threat_action_candidate = concepts.get("threat_action_candidate")
        if not isinstance(threat_action_candidate, dict):
            issues.append("text_semantic_concepts.threat_action_candidate must be an object")
    decision_targets = record.get("decision_head_auxiliary_targets")
    if not isinstance(decision_targets, dict):
        issues.append("decision_head_auxiliary_targets must be an object")
    else:
        if decision_targets.get("do_not_train_as_gold") is not True:
            issues.append("decision_head_auxiliary_targets.do_not_train_as_gold must be true")
        if decision_targets.get("advisory_only") is not True:
            issues.append("decision_head_auxiliary_targets.advisory_only must be true")
        if decision_targets.get("final_label_advisory") not in ALLOWED_FINAL_LABEL_ADVISORY:
            issues.append("decision_head_auxiliary_targets.final_label_advisory has invalid value")
        if decision_targets.get("malicious_basis_advisory") not in ALLOWED_MALICIOUS_BASIS_ADVISORY:
            issues.append("decision_head_auxiliary_targets.malicious_basis_advisory has invalid value")
    quality_flags = record.get("quality_flags")
    if not isinstance(quality_flags, dict) or "needs_human_review" not in quality_flags:
        issues.append("quality_flags.needs_human_review is required")
    else:
        if quality_flags.get("diagnostic_only") is not True:
            issues.append("quality_flags.diagnostic_only must be true")
        for key in (
            "formula_relation_unclear",
            "action_surface_without_risk_bearing_engagement",
            "risk_bearing_engagement_unclear",
            "downstream_risk_unclear",
            "evidence_sufficiency_low",
            "out_of_v1_scope_candidate",
            "gate_or_evasion_excluded_v1",
            "redirect_only_excluded_v1",
            "regulated_content_only_excluded_v1",
            "schema_or_grounding_failure",
        ):
            if key not in quality_flags:
                issues.append(f"quality_flags.{key} is required")
    validation = record.get("validation")
    if not isinstance(validation, dict):
        issues.append("validation must be an object")
    else:
        if validation.get("validator_version") != VALIDATOR_VERSION:
            issues.append(f"validation.validator_version must be {VALIDATOR_VERSION}")
        if not isinstance(validation.get("errors"), list):
            issues.append("validation.errors must be a list")
        if not isinstance(validation.get("warnings"), list):
            issues.append("validation.warnings must be a list")
        if validation.get("required_fields_present") is not True:
            issues.append("validation.required_fields_present must be true")
    error_status = record.get("error_status")
    if not isinstance(error_status, dict):
        issues.append("error_status must be an object")
    else:
        if error_status.get("status") not in {"ok", "error", "skipped"}:
            issues.append("error_status.status has invalid value")
        if not isinstance(error_status.get("retryable"), bool):
            issues.append("error_status.retryable must be a bool")
    if not record.get("sample_key"):
        issues.append("sample_key must be non-empty")
    if not record.get("source_manifest"):
        issues.append("source_manifest must be non-empty")
    if not record.get("evidence_pack_id"):
        issues.append("evidence_pack_id must be non-empty")
    if record.get("source_split") not in ALLOWED_SPLITS:
        issues.append("source_split has invalid value")
    if not record.get("teacher_run_id"):
        issues.append("teacher_run_id must be non-empty")
    if not record.get("attempt_id"):
        issues.append("attempt_id must be non-empty")
    if not isinstance(record.get("attempt_index"), int) or record.get("attempt_index") < 1:
        issues.append("attempt_index must be a positive integer")
    for key in ("record_hash", "evidence_pack_hash", "prompt_input_hash"):
        value = record.get(key)
        if not isinstance(value, str) or len(value) != 64:
            issues.append(f"{key} must be a sha256 hex string")
    issues.extend(_walk_forbidden(record))
    return DistillationValidationResult(valid=not issues, issues=issues)
