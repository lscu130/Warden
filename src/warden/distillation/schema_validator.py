"""Minimal standard-library validation for mock distillation records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schema import (
    ALLOWED_SPLITS,
    FORBIDDEN_FIELDS,
    PROMPT_TEMPLATE_VERSION,
    REQUIRED_RECORD_KEYS,
    SCHEMA_VERSION,
    TEACHER_MODEL,
    TEACHER_PROFILE,
    VALIDATOR_VERSION,
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
    if record.get("teacher_profile") != TEACHER_PROFILE:
        issues.append(f"teacher_profile must be {TEACHER_PROFILE}")
    if record.get("prompt_template_version") != PROMPT_TEMPLATE_VERSION:
        issues.append(f"prompt_template_version must be {PROMPT_TEMPLATE_VERSION}")
    if record.get("do_not_train_as_gold") is not True:
        issues.append("do_not_train_as_gold must be true")
    if record.get("diagnostic_only") is not True:
        issues.append("diagnostic_only must be true")
    if record.get("image_input_passed_to_teacher") is not False:
        issues.append("image_input_passed_to_teacher must be false in mock mode")
    if record.get("image_input_policy") != "not_supported_in_mock":
        issues.append("image_input_policy must be not_supported_in_mock in mock mode")
    if record.get("visual_evidence_source") != "none":
        issues.append("visual_evidence_source must be none in mock mode")
    if record.get("split") not in ALLOWED_SPLITS:
        issues.append("split has invalid value")
    if not isinstance(record.get("review_reasons"), list):
        issues.append("review_reasons must be a list")
    quality_flags = record.get("quality_flags")
    if not isinstance(quality_flags, dict) or "needs_human_review" not in quality_flags:
        issues.append("quality_flags.needs_human_review is required")
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
