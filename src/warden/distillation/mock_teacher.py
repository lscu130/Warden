"""Deterministic mock teacher adapter for skeleton validation."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .evidence_pack import DistillationEvidencePack
from .schema import (
    ALLOWED_MALICIOUS_BASIS_ADVISORY,
    PROMPT_TEMPLATE_ID,
    PROMPT_TEMPLATE_VERSION,
    SCHEMA_VERSION,
    TEACHER_MODEL,
    TEACHER_PROVIDER,
    TEACHER_PROFILE,
    TEACHER_ROLE,
    VALIDATOR_VERSION,
)


CREATED_AT = "1970-01-01T00:00:00Z"


def _stable_json_hash(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sample_key(pack: DistillationEvidencePack) -> str:
    url_payload = pack.teacher_visible_evidence.get("url", {})
    final_url = url_payload.get("final_url") if isinstance(url_payload, dict) else ""
    digest = hashlib.sha256(f"{pack.sample_id}|{pack.sample_path}|{final_url or ''}".encode("utf-8")).hexdigest()
    return f"sample_{digest[:24]}"


def _record_id(pack: DistillationEvidencePack, split: str, seed: int) -> str:
    digest = hashlib.sha256(f"{pack.sample_id}|{pack.sample_path}|{split}|{seed}".encode("utf-8")).hexdigest()
    return f"mock_{digest[:24]}"


def _claimed_identity_candidates(evidence_pack: DistillationEvidencePack) -> list[dict[str, Any]]:
    url_payload = evidence_pack.teacher_visible_evidence.get("url", {})
    final_host = url_payload.get("final_host") if isinstance(url_payload, dict) else None
    if not final_host:
        return []
    normalized = str(final_host).lower().removeprefix("www.")
    return [
        {
            "candidate_id": "cid_001",
            "raw_name": normalized,
            "normalized_name": normalized,
            "candidate_type_hint": "unknown",
            "sources": ["final_host"],
            "source_count": 1,
            "surface_confidence": 0.25,
            "notes": "candidate only; not a confirmed brand match",
        }
    ]


def _text_semantic_concepts(
    evidence_pack: DistillationEvidencePack,
    action_surface_present: bool,
    needs_review: bool,
) -> dict[str, Any]:
    candidates = _claimed_identity_candidates(evidence_pack)
    return {
        "schema_version": "warden_l1_text_semantic_concepts_v1_draft",
        "claimed_identity_candidates": candidates,
        "identity_claim": {
            "claimed_identity_present": "yes" if candidates else "unknown",
            "claimed_identity_strength": "weak" if candidates else "unknown",
            "claimed_identity_type": "unknown",
            "self_claim_vs_reference": "unknown",
            "claim_sources": ["final_host"] if candidates else [],
        },
        "action_surface": {
            "present": action_surface_present,
            "types": ["login"] if action_surface_present else [],
            "sensitive_surface_strength": "weak" if action_surface_present else "none",
            "action_surface_is_not_automatically_threat_action": True,
        },
        "behavior_context": {
            "present": False,
            "types": [],
            "context_strength": "none",
        },
        "relation_judgments": {
            "identity_domain_relation": "unknown",
            "action_context_relation": "unknown",
            "business_legitimacy_hint": "unknown",
            "hosted_platform_context": "unknown",
            "unknown_is_not_malicious": True,
        },
        "evidence_state": {
            "payload_observed": "yes" if action_surface_present else "unknown",
            "payload_not_observed_is_not_automatic_benign": True,
            "evidence_sufficiency": "partial" if needs_review else "sufficient",
            "needs_vision_evidence": needs_review,
            "text_html_conflict": "unknown",
            "do_not_train_as_gold": True,
        },
        "threat_action_candidate": {
            "present": "no",
            "basis": "none",
            "candidate_types": [],
            "supporting_behavior_contexts": [],
            "supporting_relation_conflicts": [],
        },
        "concept_level_evaluation_readiness": {
            "identity_claim_head_ready": True,
            "action_surface_head_ready": True,
            "behavior_context_head_ready": True,
            "relation_judgment_head_ready": True,
            "evidence_state_head_ready": True,
            "threat_action_candidate_head_ready": True,
            "final_label_head_ready": False,
            "notes": "mock-only readiness metadata; no gold labels produced",
        },
    }


def _v03_review_reasons(raw_reasons: list[str], action_surface_present: bool, needs_review: bool) -> list[str]:
    mapped: set[str] = set()
    for reason in raw_reasons:
        if reason == "action_surface_present_with_mock_context":
            mapped.add("action_surface_without_risk_bearing_engagement")
            mapped.add("risk_bearing_engagement_unclear")
        elif reason in {"visible_text_missing", "visible_text_sparse", "url_json_missing"}:
            mapped.add("evidence_sufficiency_low")
        elif reason == "bad_json_artifact":
            mapped.add("schema_or_grounding_failure")
        else:
            mapped.add(reason)
    if action_surface_present:
        mapped.add("action_surface_without_risk_bearing_engagement")
        mapped.add("risk_bearing_engagement_unclear")
    if needs_review:
        mapped.add("formula_relation_unclear")
    return sorted(mapped)


def _formula_concepts(action_surface_present: bool, needs_review: bool, final_host: str | None) -> dict[str, Any]:
    relation_type = "relation_unclear" if action_surface_present else "no_relation_observed"
    url_claim_present = bool(final_host)
    funnel_affordance_present = action_surface_present
    risk_bearing_engagement = {
        "present": False,
        "engagement_types": [],
        "direct_high_risk_action": {"present": False, "evidence_quotes": []},
        "routed_high_risk_action": {"present": False, "evidence_quotes": []},
        "action_preparation": {"present": False, "evidence_quotes": []},
        "deceptive_funnel_priming": {"present": False, "evidence_quotes": []},
        "evidence_quotes": [],
        "downstream_risk": [],
        "confidence": 0.0,
        "action_surface_is_not_automatically_risk_bearing_engagement": True,
    }
    return {
        "manipulative_context": {
            "present": False,
            "context_types": [],
            "evidence_quotes": [],
            "confidence": 0.0,
        },
        "action_surface": {
            "present": action_surface_present,
            "surface_types": ["login"] if action_surface_present else [],
            "evidence_quotes": [],
            "not_threat_by_itself": True,
        },
        "risk_bearing_engagement": risk_bearing_engagement,
        "induced_high_risk_action": {
            "compatibility_only": True,
            "use_risk_bearing_engagement_instead": True,
        },
        "context_engagement_relation": {
            "relation_supported": False,
            "relation_type": relation_type,
            "evidence_quotes": [],
            "unknown_relation_is_not_malicious": True,
        },
        "evidence_sufficiency": {
            "sufficient_for_web_se_threat": False,
            "missing_evidence": ["manipulative_context", "context_engagement_relation"]
            if action_surface_present
            else ["manipulative_context", "risk_bearing_engagement"],
            "conflicts": [],
            "confidence": 0.1 if needs_review else 0.0,
        },
        "formula_result": {
            "web_se_threat_formula_satisfied": False,
            "formula_basis": "mock-only record: V0.3 formula not satisfied without manipulative context and risk-bearing engagement evidence",
        },
        "url_claim_analysis": {
            "claim_present": url_claim_present,
            "url_only_brand_claim": url_claim_present and not funnel_affordance_present,
            "not_v1_positive_by_itself": True,
        },
        "visible_impersonation_analysis": {
            "present": False,
            "without_funnel_affordance": False,
            "with_funnel_affordance": False,
        },
        "funnel_affordance_analysis": {
            "present": funnel_affordance_present,
            "affordance_types": ["form"] if funnel_affordance_present else [],
        },
        "risk_outcome_axes": [],
    }


def build_mock_record(
    evidence_pack: DistillationEvidencePack,
    split: str,
    seed: int = 0,
    diagnostic_only: bool = True,
    source_manifest: str = "unknown_manifest",
    source_split: str | None = None,
    teacher_run_id: str = "mock_teacher_run_unknown",
    attempt_index: int = 1,
) -> dict[str, Any]:
    raw_review_reasons = list(evidence_pack.review_reasons)
    forms_summary = evidence_pack.teacher_visible_evidence.get("forms", {})
    form_count = int(forms_summary.get("form_count") or 0)
    action_surface_present = form_count > 0
    review_reasons = _v03_review_reasons(raw_review_reasons, action_surface_present, bool(raw_review_reasons))
    needs_review = bool(review_reasons)
    text_semantic_concepts = _text_semantic_concepts(evidence_pack, action_surface_present, needs_review)
    claimed_identity_candidates = text_semantic_concepts["claimed_identity_candidates"]
    url_payload = evidence_pack.teacher_visible_evidence.get("url", {})
    final_host = url_payload.get("final_host") if isinstance(url_payload, dict) else None
    formula_concepts = _formula_concepts(action_surface_present, needs_review, str(final_host) if final_host else None)
    malicious_basis = "action_surface_only" if action_surface_present else "no_web_se_evidence_observed"
    if malicious_basis not in ALLOWED_MALICIOUS_BASIS_ADVISORY:
        malicious_basis = "insufficient_evidence"

    sample_key = _sample_key(evidence_pack)
    record_id = _record_id(evidence_pack, split, seed)
    attempt_id = f"attempt_{hashlib.sha256(f'{record_id}|{attempt_index}'.encode('utf-8')).hexdigest()[:24]}"
    url_payload = evidence_pack.teacher_visible_evidence.get("url", {})
    source_url = url_payload.get("input_url") if isinstance(url_payload, dict) else None
    canonical_url = url_payload.get("final_url") if isinstance(url_payload, dict) else None
    evidence_pack_hash = _stable_json_hash(
        {
            "summary": evidence_pack.summary(),
            "teacher_visible_evidence": evidence_pack.teacher_visible_evidence,
        }
    )
    evidence_pack_id = f"evidence_pack_{evidence_pack_hash[:24]}"
    prompt_input_hash = _stable_json_hash(
        {
            "sample_key": sample_key,
            "input_modalities": list(evidence_pack.input_modalities),
            "teacher_visible_evidence": evidence_pack.teacher_visible_evidence,
        }
    )

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "record_id": record_id,
        "sample_key": sample_key,
        "sample_id": evidence_pack.sample_id,
        "sample_path": str(evidence_pack.sample_path),
        "source_manifest": source_manifest,
        "source_split": source_split or split,
        "source_url": source_url,
        "canonical_url": canonical_url,
        "capture_id": None,
        "evidence_pack_id": evidence_pack_id,
        "split": split,
        "diagnostic_only": True if diagnostic_only else True,
        "do_not_train_as_gold": True,
        "teacher_provider": TEACHER_PROVIDER,
        "teacher_model": TEACHER_MODEL,
        "teacher_role": TEACHER_ROLE,
        "teacher_profile": TEACHER_PROFILE,
        "teacher_run_id": teacher_run_id,
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "prompt_snapshot_path": f"prompt_snapshots/{attempt_id}.json",
        "attempt_id": attempt_id,
        "attempt_index": attempt_index,
        "attempt_status": "mock_completed",
        "repair_attempted": False,
        "repair_reason": None,
        "created_at_utc": CREATED_AT,
        "input_modalities": list(evidence_pack.input_modalities),
        "fallback_reason": None,
        "image_input_expected": False,
        "image_input_passed_to_teacher": False,
        "image_input_policy": "not_supported_in_mock",
        "modality_guard_status": "mock_no_image_input",
        "visual_evidence_source": "none",
        "raw_output_path": f"raw_outputs/{attempt_id}.json",
        "repaired_output_path": None,
        "validation_status": "pending",
        "validation_errors": [],
        "token_usage_placeholder": {
            "mock_only": True,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
        },
        "cost_placeholder": {
            "mock_only": True,
            "currency": None,
            "estimated_cost": None,
        },
        "latency_ms_placeholder": None,
        "provider_request_id_placeholder": None,
        "failure_category": None,
        "retry_allowed": False,
        "rollback_required": False,
        "evidence_pack_summary": evidence_pack.summary(),
        "rule_router_observation": {
            "used_as_context_only": True,
            "not_teacher_label": True,
            "legacy_optional": True,
            "not_a_label_source": True,
            "not_a_teacher_label_source": True,
            "not_final_judgment": True,
        },
        "formula_semantics": {
            "web_se_formula": "EvidenceSufficient(ManipulativeContext AND RiskBearingEngagement)",
            "risk_bearing_engagement_formula": "DirectHighRiskAction OR RoutedHighRiskAction OR ActionPreparation OR DeceptiveFunnelPriming",
        },
        "formula_concepts": formula_concepts,
        "observed_evidence_summary": evidence_pack.summary(),
        "manipulative_context": formula_concepts["manipulative_context"],
        "risk_bearing_engagement": formula_concepts["risk_bearing_engagement"],
        "context_engagement_relation": formula_concepts["context_engagement_relation"],
        "evidence_sufficiency": formula_concepts["evidence_sufficiency"],
        "formula_result": formula_concepts["formula_result"],
        "url_claim_analysis": formula_concepts["url_claim_analysis"],
        "visible_impersonation_analysis": formula_concepts["visible_impersonation_analysis"],
        "funnel_affordance_analysis": formula_concepts["funnel_affordance_analysis"],
        "risk_outcome_axes": formula_concepts["risk_outcome_axes"],
        "claimed_identity_candidates": claimed_identity_candidates,
        "text_semantic_concepts": text_semantic_concepts,
        "vision_evidence": {
            "status": "not_run",
            "note": "mock skeleton does not run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference",
        },
        "decision_head_auxiliary_targets": {
            "advisory_only": True,
            "final_label_advisory": "unknown_diagnostic_only",
            "malicious_basis_advisory": malicious_basis,
            "payload_observed_advisory": "unknown",
            "risk_score_hint": 0.0,
            "confidence_hint": 0.0,
            "do_not_train_as_gold": True,
            "note": "payload not observed is not automatic benign",
        },
        "quality_flags": {
            "needs_human_review": needs_review,
            "schema_valid": True,
            "evidence_incomplete": bool(evidence_pack.missing_artifacts or evidence_pack.bad_json_issues),
            "fallback_modality_loss": False,
            "diagnostic_only": True,
            "formula_relation_unclear": needs_review or action_surface_present,
            "action_surface_without_risk_bearing_engagement": action_surface_present,
            "risk_bearing_engagement_unclear": action_surface_present,
            "downstream_risk_unclear": action_surface_present,
            "evidence_sufficiency_low": True,
            "out_of_v1_scope_candidate": False,
            "gate_or_evasion_excluded_v1": False,
            "redirect_only_excluded_v1": False,
            "regulated_content_only_excluded_v1": False,
            "schema_or_grounding_failure": bool(evidence_pack.bad_json_issues),
        },
        "review_reasons": review_reasons,
        "validation": {
            "schema_valid": True,
            "validator_version": VALIDATOR_VERSION,
            "errors": [],
            "warnings": [],
            "required_fields_present": True,
        },
        "error_status": {
            "status": "ok",
            "error_type": None,
            "error_message": None,
            "retryable": False,
        },
        "record_hash": "",
        "evidence_pack_hash": evidence_pack_hash,
        "prompt_input_hash": prompt_input_hash,
        "created_at": CREATED_AT,
    }
    hash_payload = dict(record)
    hash_payload["record_hash"] = None
    record["record_hash"] = _stable_json_hash(hash_payload)
    return record
