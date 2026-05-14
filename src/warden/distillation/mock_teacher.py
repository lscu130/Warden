"""Deterministic mock teacher adapter for skeleton validation."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .evidence_pack import DistillationEvidencePack
from .schema import (
    PROMPT_TEMPLATE_VERSION,
    SCHEMA_VERSION,
    TEACHER_MODEL,
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
    review_reasons = list(evidence_pack.review_reasons)
    needs_review = bool(review_reasons)
    forms_summary = evidence_pack.teacher_visible_evidence.get("forms", {})
    form_count = int(forms_summary.get("form_count") or 0)
    action_surface_present = form_count > 0

    sample_key = _sample_key(evidence_pack)
    record_id = _record_id(evidence_pack, split, seed)
    attempt_id = f"attempt_{hashlib.sha256(f'{record_id}|{attempt_index}'.encode('utf-8')).hexdigest()[:24]}"
    evidence_pack_hash = _stable_json_hash(
        {
            "summary": evidence_pack.summary(),
            "teacher_visible_evidence": evidence_pack.teacher_visible_evidence,
        }
    )
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
        "split": split,
        "diagnostic_only": True if diagnostic_only else True,
        "do_not_train_as_gold": True,
        "teacher_model": TEACHER_MODEL,
        "teacher_role": TEACHER_ROLE,
        "teacher_profile": TEACHER_PROFILE,
        "teacher_run_id": teacher_run_id,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "attempt_id": attempt_id,
        "attempt_index": attempt_index,
        "created_at_utc": CREATED_AT,
        "input_modalities": list(evidence_pack.input_modalities),
        "fallback_reason": None,
        "image_input_passed_to_teacher": False,
        "image_input_policy": "not_supported_in_mock",
        "visual_evidence_source": "none",
        "evidence_pack_summary": evidence_pack.summary(),
        "rule_router_observation": {
            "used_as_context_only": True,
            "not_teacher_label": True,
        },
        "text_semantic_concepts": {
            "action_surfaces": {
                "form_surface_present": {
                    "present": action_surface_present,
                    "is_threat_action": False,
                    "note": "action surface is not automatically threat action",
                }
            },
            "behavior_contexts": {},
            "relation_consistency": {},
            "risk_axes": {},
            "page_role_candidates": {},
            "routing_recommendations": {},
        },
        "vision_evidence": {
            "status": "not_run",
            "note": "mock skeleton does not run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference",
        },
        "decision_head_auxiliary_targets": {
            "advisory_only": True,
            "final_label_advisory": "unknown",
            "payload_observed_advisory": "unknown",
            "note": "payload not observed is not automatic benign",
        },
        "quality_flags": {
            "needs_human_review": needs_review,
            "schema_valid": True,
            "evidence_incomplete": bool(evidence_pack.missing_artifacts or evidence_pack.bad_json_issues),
            "fallback_modality_loss": False,
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
