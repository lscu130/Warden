"""Dry-run/mock Warden distillation runner skeleton."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit_log import write_adapter_readiness_report, write_audit, write_report
from .evidence_pack import build_evidence_pack
from .jsonl_writer import append_jsonl, write_jsonl
from .manifest_reader import DistillationSampleRecord, read_manifest_records
from .mock_teacher import build_mock_record
from .resume import load_processed_record_ids
from .review_queue import build_review_queue_record
from .schema import ALLOWED_MODES, ALLOWED_SPLITS, REQUIRED_OUTPUT_FILES
from .schema_validator import validate_distillation_record


@dataclass(frozen=True)
class DistillationRunConfig:
    manifest: Path
    output_dir: Path
    split: str
    mode: str = "dry-run"
    limit: int | None = None
    seed: int = 0
    resume: bool = False
    overwrite: bool = False
    diagnostic_only: bool = False


@dataclass(frozen=True)
class DistillationRunResult:
    run_id: str
    total_rows_seen: int
    processed_count: int
    skipped_existing_count: int
    error_count: int
    review_queue_count: int
    schema_valid_count: int
    schema_invalid_count: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _run_id(config: DistillationRunConfig) -> str:
    digest = hashlib.sha256(
        f"{config.manifest}|{config.output_dir}|{config.split}|{config.mode}|{config.seed}".encode("utf-8")
    ).hexdigest()
    return f"distill_skeleton_{digest[:16]}"


def _output_paths(output_dir: Path) -> dict[str, Path]:
    return {
        "records": output_dir / "distillation_records.jsonl",
        "review": output_dir / "review_queue.jsonl",
        "attempts": output_dir / "attempts.jsonl",
        "validation_summaries": output_dir / "validation_summaries.jsonl",
        "audit": output_dir / "run_audit.json",
        "report": output_dir / "run_report.md",
        "adapter_readiness_report": output_dir / "adapter_readiness_report.md",
        "errors": output_dir / "errors.jsonl",
        "prompt_snapshots": output_dir / "prompt_snapshots",
        "raw_outputs": output_dir / "raw_outputs",
        "repaired_outputs": output_dir / "repaired_outputs",
    }


def _validate_config(config: DistillationRunConfig) -> None:
    if config.split not in ALLOWED_SPLITS:
        raise ValueError(f"split must be one of {sorted(ALLOWED_SPLITS)}")
    if config.mode not in ALLOWED_MODES:
        raise ValueError(f"mode must be one of {sorted(ALLOWED_MODES)}")
    if config.split in {"val", "test"} and not config.diagnostic_only:
        raise ValueError("val/test skeleton runs require --diagnostic-only")
    if config.resume and config.overwrite:
        raise ValueError("--resume and --overwrite cannot be used together")


def _prepare_output_dir(config: DistillationRunConfig, paths: dict[str, Path]) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    existing = [
        path
        for name, path in paths.items()
        if name in {"records", "review", "attempts", "validation_summaries", "errors"} and path.exists()
    ]
    if existing and not config.resume and not config.overwrite:
        raise FileExistsError("output files already exist; use --resume or --overwrite")
    if config.overwrite:
        for name in REQUIRED_OUTPUT_FILES:
            path = config.output_dir / name
            if path.exists():
                path.unlink()
    for name in ("prompt_snapshots", "raw_outputs", "repaired_outputs"):
        paths[name].mkdir(parents=True, exist_ok=True)
    for name in ("records", "review", "attempts", "validation_summaries", "errors"):
        paths[name].parent.mkdir(parents=True, exist_ok=True)
        paths[name].touch(exist_ok=True)


def _check_row_split(record: DistillationSampleRecord, requested_split: str) -> None:
    row_split = (record.row.get("split") or "").strip()
    if row_split and row_split != requested_split:
        raise ValueError(f"manifest row split {row_split!r} does not match requested split {requested_split!r}")


def _write_error(paths: dict[str, Path], record: DistillationSampleRecord, error: Exception) -> None:
    payload = {
        "sample_id": record.sample_id,
        "sample_path": str(record.sample_path),
        "split": record.split,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "retryable": True,
        "do_not_train_as_gold": True,
        "needs_human_review": True,
    }
    append_jsonl(paths["errors"], payload)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _count_missing_readiness_fields(records: list[dict[str, Any]]) -> dict[str, int]:
    fields = (
        "sample_key",
        "source_manifest",
        "source_split",
        "teacher_profile",
        "teacher_run_id",
        "prompt_template_version",
        "prompt_template_id",
        "prompt_snapshot_path",
        "teacher_provider",
        "evidence_pack_id",
        "image_input_passed_to_teacher",
        "image_input_expected",
        "modality_guard_status",
        "validation",
        "validation_status",
        "validation_errors",
        "error_status",
        "attempt_id",
        "attempt_index",
        "attempt_status",
        "repair_attempted",
        "repair_reason",
        "raw_output_path",
        "repaired_output_path",
        "token_usage_placeholder",
        "cost_placeholder",
        "latency_ms_placeholder",
        "provider_request_id_placeholder",
        "failure_category",
        "retry_allowed",
        "rollback_required",
        "created_at_utc",
        "record_hash",
        "evidence_pack_hash",
        "prompt_input_hash",
    )
    missing: dict[str, int] = {}
    for field in fields:
        count = sum(1 for record in records if field not in record)
        if count:
            missing[field] = count
    return missing


def _count_missing_concept_fields(records: list[dict[str, Any]]) -> dict[str, int]:
    concept_paths = (
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
    )
    missing: dict[str, int] = {}
    for path in concept_paths:
        count = 0
        for record in records:
            current: Any = record
            for part in path:
                if not isinstance(current, dict) or part not in current:
                    count += 1
                    break
                current = current[part]
        if count:
            missing[".".join(path)] = count
    return missing


def _build_attempt_record(record: dict[str, Any], validation: Any) -> dict[str, Any]:
    return {
        "attempt_id": record["attempt_id"],
        "attempt_index": record["attempt_index"],
        "attempt_status": record["attempt_status"],
        "mock_only": True,
        "record_id": record["record_id"],
        "sample_key": record["sample_key"],
        "sample_id": record["sample_id"],
        "source_manifest": record["source_manifest"],
        "source_split": record["source_split"],
        "evidence_pack_id": record["evidence_pack_id"],
        "teacher_provider": record["teacher_provider"],
        "teacher_run_id": record["teacher_run_id"],
        "teacher_profile": record["teacher_profile"],
        "teacher_model": record["teacher_model"],
        "teacher_role": record["teacher_role"],
        "prompt_template_id": record["prompt_template_id"],
        "prompt_template_version": record["prompt_template_version"],
        "prompt_snapshot_path": record["prompt_snapshot_path"],
        "schema_version": record["schema_version"],
        "input_modalities": record["input_modalities"],
        "fallback_reason": record["fallback_reason"],
        "image_input_expected": record["image_input_expected"],
        "image_input_passed_to_teacher": record["image_input_passed_to_teacher"],
        "modality_guard_status": record["modality_guard_status"],
        "real_teacher_call": False,
        "external_api_call": False,
        "raw_output_path": record["raw_output_path"],
        "raw_teacher_output_path": record["raw_output_path"],
        "prompt_path": record["prompt_snapshot_path"],
        "repair_path": record["repaired_output_path"],
        "repaired_output_path": record["repaired_output_path"],
        "repair_attempted": record["repair_attempted"],
        "repair_reason": record["repair_reason"],
        "validation_status": record["validation_status"],
        "schema_valid": validation.valid,
        "validation_errors": list(validation.issues),
        "token_usage_placeholder": record["token_usage_placeholder"],
        "cost_placeholder": record["cost_placeholder"],
        "latency_ms_placeholder": record["latency_ms_placeholder"],
        "provider_request_id_placeholder": record["provider_request_id_placeholder"],
        "failure_category": record["failure_category"],
        "retry_allowed": record["retry_allowed"],
        "rollback_required": record["rollback_required"],
        "created_at_utc": record["created_at_utc"],
    }


def _build_validation_summary(record: dict[str, Any], validation: Any) -> dict[str, Any]:
    return {
        "mock_only": True,
        "record_id": record["record_id"],
        "sample_key": record["sample_key"],
        "sample_id": record["sample_id"],
        "attempt_id": record["attempt_id"],
        "schema_version": record["schema_version"],
        "validator_version": record["validation"]["validator_version"],
        "validation_status": record["validation_status"],
        "schema_valid": validation.valid,
        "validation_errors": list(validation.issues),
        "required_fields_present": record["validation"]["required_fields_present"],
        "do_not_train_as_gold": record["do_not_train_as_gold"],
        "diagnostic_only": record["diagnostic_only"],
        "created_at_utc": record["created_at_utc"],
    }


def _write_adapter_placeholders(output_dir: Path, record: dict[str, Any]) -> None:
    prompt_snapshot_path = output_dir / record["prompt_snapshot_path"]
    raw_output_path = output_dir / record["raw_output_path"]
    prompt_snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    raw_output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_snapshot = {
        "mock_only": True,
        "prompt_template_id": record["prompt_template_id"],
        "prompt_template_version": record["prompt_template_version"],
        "sample_key": record["sample_key"],
        "evidence_pack_id": record["evidence_pack_id"],
        "teacher_provider": record["teacher_provider"],
        "teacher_model": record["teacher_model"],
        "image_input_expected": record["image_input_expected"],
        "image_input_passed_to_teacher": record["image_input_passed_to_teacher"],
        "modality_guard_status": record["modality_guard_status"],
        "note": "placeholder prompt snapshot for no-network adapter readiness; no provider call performed",
    }
    raw_output = {
        "mock_only": True,
        "attempt_id": record["attempt_id"],
        "record_id": record["record_id"],
        "teacher_provider": record["teacher_provider"],
        "teacher_model": record["teacher_model"],
        "raw_provider_response": None,
        "external_api_call": False,
        "note": "placeholder raw output for no-network adapter readiness; no provider response exists",
    }
    prompt_snapshot_path.write_text(json.dumps(prompt_snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    raw_output_path.write_text(json.dumps(raw_output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_distillation(config: DistillationRunConfig) -> DistillationRunResult:
    config = DistillationRunConfig(
        manifest=Path(config.manifest),
        output_dir=Path(config.output_dir),
        split=config.split,
        mode=config.mode,
        limit=config.limit,
        seed=config.seed,
        resume=config.resume,
        overwrite=config.overwrite,
        diagnostic_only=config.diagnostic_only,
    )
    _validate_config(config)
    paths = _output_paths(config.output_dir)
    _prepare_output_dir(config, paths)

    started_at = _utc_now()
    run_id = _run_id(config)
    teacher_run_id = run_id
    processed_ids = load_processed_record_ids(paths["records"]) if config.resume else set()

    total_rows_seen = 0
    processed_count = 0
    skipped_existing_count = 0
    error_count = 0
    review_queue_count = 0
    schema_valid_count = 0
    schema_invalid_count = 0

    records = read_manifest_records(config.manifest, requested_split=config.split, limit=config.limit)
    for sample_record in records:
        total_rows_seen += 1
        try:
            _check_row_split(sample_record, config.split)
            pack = build_evidence_pack(sample_record)
            record = build_mock_record(
                pack,
                split=config.split,
                seed=config.seed,
                diagnostic_only=True,
                source_manifest=str(config.manifest),
                source_split=sample_record.split,
                teacher_run_id=teacher_run_id,
                attempt_index=1,
            )
            if record["record_id"] in processed_ids:
                skipped_existing_count += 1
                continue
            validation = validate_distillation_record(record)
            record["quality_flags"]["schema_valid"] = validation.valid
            record["validation"]["schema_valid"] = validation.valid
            record["validation"]["errors"] = list(validation.issues)
            record["validation_errors"] = list(validation.issues)
            record["validation_status"] = "passed" if validation.valid else "failed"
            record["attempt_status"] = "mock_completed" if validation.valid else "schema_validation_failed"
            record["validation"]["required_fields_present"] = not any(
                issue.startswith("missing required key:") for issue in validation.issues
            )
            if validation.valid:
                record["error_status"] = {
                    "status": "ok",
                    "error_type": None,
                    "error_message": None,
                    "retryable": False,
                }
            else:
                record["error_status"] = {
                    "status": "error",
                    "error_type": "schema_validation_failed",
                    "error_message": "; ".join(validation.issues),
                    "retryable": True,
                }
            if validation.valid:
                schema_valid_count += 1
            else:
                schema_invalid_count += 1
                record["quality_flags"]["needs_human_review"] = True
                if "schema_validation_failure" not in record["review_reasons"]:
                    record["review_reasons"].append("schema_validation_failure")
                for issue in validation.issues:
                    if issue not in record["review_reasons"]:
                        record["review_reasons"].append(issue)
            _write_adapter_placeholders(config.output_dir, record)
            append_jsonl(paths["records"], record)
            append_jsonl(paths["attempts"], _build_attempt_record(record, validation))
            append_jsonl(paths["validation_summaries"], _build_validation_summary(record, validation))
            processed_count += 1
            review_record = build_review_queue_record(record)
            if review_record is not None:
                append_jsonl(paths["review"], review_record)
                review_queue_count += 1
        except Exception as exc:  # noqa: BLE001 - keep processing recoverable per-sample errors.
            _write_error(paths, sample_record, exc)
            error_count += 1

    finished_at = _utc_now()
    written_records = _read_jsonl(paths["records"])
    written_review = _read_jsonl(paths["review"])
    written_attempts = _read_jsonl(paths["attempts"])
    written_validation_summaries = _read_jsonl(paths["validation_summaries"])
    record_ids = [str(record.get("record_id")) for record in written_records if record.get("record_id")]
    sample_keys = [str(record.get("sample_key")) for record in written_records if record.get("sample_key")]
    record_id_counts = Counter(record_ids)
    sample_key_counts = Counter(sample_keys)
    duplicate_record_ids = sorted(key for key, count in record_id_counts.items() if count > 1)
    duplicate_sample_keys = sorted(key for key, count in sample_key_counts.items() if count > 1)
    review_reason_counts = Counter(
        reason
        for review in written_review
        for reason in review.get("review_reasons", [])
        if isinstance(review.get("review_reasons"), list)
    )
    schema_error_counts = Counter(
        issue
        for record in written_records
        for issue in record.get("validation", {}).get("errors", [])
        if isinstance(record.get("validation"), dict)
    )
    non_gold_failures = sum(1 for record in written_records if record.get("do_not_train_as_gold") is not True)
    diagnostic_failures = sum(1 for record in written_records if record.get("diagnostic_only") is not True)
    repair_count = sum(1 for attempt in written_attempts if attempt.get("repair_attempted") is True)
    validation_pass_count = sum(1 for row in written_validation_summaries if row.get("validation_status") == "passed")
    validation_fail_count = sum(1 for row in written_validation_summaries if row.get("validation_status") == "failed")
    output_path_inventory = {
        "distillation_records": str(paths["records"]),
        "review_queue": str(paths["review"]),
        "attempts": str(paths["attempts"]),
        "validation_summaries": str(paths["validation_summaries"]),
        "run_audit": str(paths["audit"]),
        "run_report": str(paths["report"]),
        "adapter_readiness_report": str(paths["adapter_readiness_report"]),
        "errors": str(paths["errors"]),
        "prompt_snapshots": str(paths["prompt_snapshots"]),
        "raw_outputs": str(paths["raw_outputs"]),
        "repaired_outputs": str(paths["repaired_outputs"]),
    }

    audit: dict[str, Any] = {
        "run_id": run_id,
        "teacher_run_id": teacher_run_id,
        "started_at": started_at,
        "started_at_utc": started_at,
        "finished_at": finished_at,
        "finished_at_utc": finished_at,
        "manifest": str(config.manifest),
        "source_manifest": str(config.manifest),
        "output_dir": str(config.output_dir),
        "split": config.split,
        "source_split": config.split,
        "schema_version": "warden_distill_v0.3_mock",
        "prompt_template_version": "warden_distill_v0.3",
        "prompt_template_versions": dict(Counter(str(record.get("prompt_template_version")) for record in written_records)),
        "teacher_profiles": dict(Counter(str(record.get("teacher_profile")) for record in written_records)),
        "mode": config.mode,
        "limit": config.limit,
        "seed": config.seed,
        "total_rows_seen": total_rows_seen,
        "processed_count": processed_count,
        "skipped_existing_count": skipped_existing_count,
        "error_count": error_count,
        "review_queue_count": review_queue_count,
        "schema_valid_count": schema_valid_count,
        "schema_invalid_count": schema_invalid_count,
        "records_written": processed_count,
        "records_valid": schema_valid_count,
        "records_invalid": schema_invalid_count,
        "attempt_count": len(written_attempts),
        "repair_count": repair_count,
        "validation_summary_count": len(written_validation_summaries),
        "validation_pass_count": validation_pass_count,
        "validation_fail_count": validation_fail_count,
        "mock_teacher_calls": processed_count,
        "real_teacher_calls": 0,
        "external_api_calls": 0,
        "teacher_calls": 0,
        "ocr_calls": 0,
        "yolo_calls": 0,
        "clip_calls": 0,
        "do_not_train_as_gold_failures": non_gold_failures,
        "diagnostic_only_failures": diagnostic_failures,
        "missing_required_readiness_fields": _count_missing_readiness_fields(written_records),
        "missing_required_concept_fields": _count_missing_concept_fields(written_records),
        "concept_level_readiness": {
            "records_with_formula_concepts": sum(1 for record in written_records if "formula_concepts" in record),
            "records_with_context_engagement_relation": sum(
                1
                for record in written_records
                if isinstance(record.get("formula_concepts"), dict)
                and "context_engagement_relation" in record["formula_concepts"]
            ),
            "records_with_evidence_sufficiency": sum(
                1
                for record in written_records
                if isinstance(record.get("formula_concepts"), dict)
                and "evidence_sufficiency" in record["formula_concepts"]
            ),
            "records_with_formula_result": sum(
                1
                for record in written_records
                if isinstance(record.get("formula_concepts"), dict)
                and "formula_result" in record["formula_concepts"]
            ),
            "records_with_claimed_identity_candidates": sum(
                1 for record in written_records if "claimed_identity_candidates" in record
            ),
            "records_with_relation_judgments": sum(
                1
                for record in written_records
                if isinstance(record.get("text_semantic_concepts"), dict)
                and "relation_judgments" in record["text_semantic_concepts"]
            ),
            "records_with_evidence_state": sum(
                1
                for record in written_records
                if isinstance(record.get("text_semantic_concepts"), dict)
                and "evidence_state" in record["text_semantic_concepts"]
            ),
            "records_with_threat_action_candidate": sum(
                1
                for record in written_records
                if isinstance(record.get("text_semantic_concepts"), dict)
                and "threat_action_candidate" in record["text_semantic_concepts"]
            ),
        },
        "schema_validation_errors_by_type": dict(schema_error_counts),
        "review_reason_counts": dict(review_reason_counts),
        "duplicate_record_ids": duplicate_record_ids,
        "duplicate_sample_keys": duplicate_sample_keys,
        "duplicate_sample_key_summary": {
            "duplicate_count": len(duplicate_sample_keys),
            "duplicate_sample_keys": duplicate_sample_keys,
        },
        "output_files": {name: str(path) for name, path in paths.items()},
        "output_path_inventory": output_path_inventory,
        "cost_token_placeholders": {
            "mock_only": True,
            "token_usage_available": False,
            "cost_available": False,
        },
        "adapter_readiness_status": "ready_for_no_network_dry_run",
        "live_teacher_readiness": "not_ready_for_live_teacher",
    }
    write_audit(paths["audit"], audit)
    write_report(paths["report"], audit)
    write_adapter_readiness_report(paths["adapter_readiness_report"], audit)

    return DistillationRunResult(
        run_id=run_id,
        total_rows_seen=total_rows_seen,
        processed_count=processed_count,
        skipped_existing_count=skipped_existing_count,
        error_count=error_count,
        review_queue_count=review_queue_count,
        schema_valid_count=schema_valid_count,
        schema_invalid_count=schema_invalid_count,
    )
