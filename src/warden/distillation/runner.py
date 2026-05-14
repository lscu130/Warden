"""Dry-run/mock Warden distillation runner skeleton."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit_log import write_audit, write_report
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
        "audit": output_dir / "run_audit.json",
        "report": output_dir / "run_report.md",
        "errors": output_dir / "errors.jsonl",
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
        path for name, path in paths.items() if name in {"records", "review", "attempts", "errors"} and path.exists()
    ]
    if existing and not config.resume and not config.overwrite:
        raise FileExistsError("output files already exist; use --resume or --overwrite")
    if config.overwrite:
        for name in REQUIRED_OUTPUT_FILES:
            path = config.output_dir / name
            if path.exists():
                path.unlink()
    for name in ("records", "review", "attempts", "errors"):
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
        "image_input_passed_to_teacher",
        "validation",
        "error_status",
        "attempt_id",
        "attempt_index",
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


def _build_attempt_record(record: dict[str, Any], validation: Any) -> dict[str, Any]:
    return {
        "attempt_id": record["attempt_id"],
        "attempt_index": record["attempt_index"],
        "record_id": record["record_id"],
        "sample_key": record["sample_key"],
        "sample_id": record["sample_id"],
        "source_manifest": record["source_manifest"],
        "source_split": record["source_split"],
        "teacher_run_id": record["teacher_run_id"],
        "teacher_profile": record["teacher_profile"],
        "teacher_model": record["teacher_model"],
        "teacher_role": record["teacher_role"],
        "prompt_template_version": record["prompt_template_version"],
        "schema_version": record["schema_version"],
        "input_modalities": record["input_modalities"],
        "fallback_reason": record["fallback_reason"],
        "image_input_passed_to_teacher": record["image_input_passed_to_teacher"],
        "real_teacher_call": False,
        "external_api_call": False,
        "raw_teacher_output_path": None,
        "prompt_path": None,
        "repair_path": None,
        "schema_valid": validation.valid,
        "validation_errors": list(validation.issues),
        "created_at_utc": record["created_at_utc"],
    }


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
                for issue in validation.issues:
                    if issue not in record["review_reasons"]:
                        record["review_reasons"].append(issue)
            append_jsonl(paths["records"], record)
            append_jsonl(paths["attempts"], _build_attempt_record(record, validation))
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
        "schema_validation_errors_by_type": dict(schema_error_counts),
        "review_reason_counts": dict(review_reason_counts),
        "duplicate_record_ids": duplicate_record_ids,
        "duplicate_sample_keys": duplicate_sample_keys,
        "output_files": {name: str(path) for name, path in paths.items()},
    }
    write_audit(paths["audit"], audit)
    write_report(paths["report"], audit)

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
