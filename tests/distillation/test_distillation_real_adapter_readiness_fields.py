import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from warden.distillation.runner import DistillationRunConfig, run_distillation
from warden.distillation.schema_validator import validate_distillation_record


READINESS_FIELDS = {
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
    "image_input_policy",
    "visual_evidence_source",
    "record_hash",
    "evidence_pack_hash",
    "prompt_input_hash",
}


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_sample(sample_dir: Path) -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        sample_dir / "url.json",
        {
            "input_url": "https://example.edu/",
            "final_url": "https://example.edu/home",
            "final_host": "example.edu",
        },
    )
    (sample_dir / "visible_text.txt").write_text("Welcome to Example University login and search.", encoding="utf-8")
    _write_json(
        sample_dir / "forms.json",
        {"forms": [{"action": "https://example.edu/login", "inputs": [{"type": "password", "name": "pw"}]}]},
    )
    _write_json(sample_dir / "net_summary.json", {"requests": [{"url": "https://example.edu/home"}]})
    (sample_dir / "html_rendered.html").write_text(
        "<html><body><form><input type='password' name='pw'></form></body></html>",
        encoding="utf-8",
    )
    return sample_dir


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> Path:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_mock_run_writes_real_adapter_readiness_fields_and_attempts(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"

    result = run_distillation(
        DistillationRunConfig(
            manifest=manifest,
            output_dir=output_dir,
            split="train",
            mode="mock",
            seed=42,
            overwrite=True,
        )
    )

    records = _read_jsonl(output_dir / "distillation_records.jsonl")
    attempts = _read_jsonl(output_dir / "attempts.jsonl")
    review_rows = _read_jsonl(output_dir / "review_queue.jsonl")
    audit = json.loads((output_dir / "run_audit.json").read_text(encoding="utf-8"))
    report = (output_dir / "run_report.md").read_text(encoding="utf-8")

    assert result.processed_count == 1
    assert len(records) == 1
    assert len(attempts) == 1

    record = records[0]
    assert READINESS_FIELDS.issubset(record)
    assert record["sample_key"]
    assert record["source_manifest"] == str(manifest)
    assert record["source_split"] == "train"
    assert record["teacher_profile"] == "mock_teacher_v0"
    assert record["teacher_run_id"] == audit["teacher_run_id"]
    assert record["prompt_template_version"] == "mock_prompt_v0"
    assert record["image_input_passed_to_teacher"] is False
    assert record["image_input_policy"] == "not_supported_in_mock"
    assert record["visual_evidence_source"] == "none"
    assert record["do_not_train_as_gold"] is True
    assert record["diagnostic_only"] is True
    assert record["validation"]["schema_valid"] is True
    assert record["validation"]["required_fields_present"] is True
    assert record["validation"]["errors"] == []
    assert record["error_status"]["status"] == "ok"
    assert record["record_hash"]
    assert record["evidence_pack_hash"]
    assert record["prompt_input_hash"]
    assert validate_distillation_record(record).valid is True

    attempt = attempts[0]
    assert attempt["attempt_id"] == record["attempt_id"]
    assert attempt["record_id"] == record["record_id"]
    assert attempt["sample_key"] == record["sample_key"]
    assert attempt["teacher_run_id"] == record["teacher_run_id"]
    assert attempt["real_teacher_call"] is False
    assert attempt["external_api_call"] is False
    assert attempt["schema_valid"] is True

    assert review_rows
    review = review_rows[0]
    for key in (
        "record_id",
        "sample_key",
        "source_manifest",
        "source_split",
        "teacher_run_id",
        "teacher_profile",
        "prompt_template_version",
        "attempt_id",
        "severity",
        "do_not_train_as_gold",
        "diagnostic_only",
    ):
        assert key in review
    assert review["record_id"] == record["record_id"]
    assert review["sample_key"] == record["sample_key"]

    assert audit["teacher_run_id"] == record["teacher_run_id"]
    assert audit["source_manifest"] == str(manifest)
    assert audit["source_split"] == "train"
    assert audit["records_written"] == 1
    assert audit["records_valid"] == 1
    assert audit["records_invalid"] == 0
    assert audit["attempt_count"] == 1
    assert audit["mock_teacher_calls"] == 1
    assert audit["real_teacher_calls"] == 0
    assert audit["external_api_calls"] == 0
    assert audit["ocr_calls"] == 0
    assert audit["yolo_calls"] == 0
    assert audit["clip_calls"] == 0
    assert audit["do_not_train_as_gold_failures"] == 0
    assert audit["diagnostic_only_failures"] == 0
    assert audit["missing_required_readiness_fields"] == {}

    assert "teacher_run_id" in report
    assert "mock_teacher_calls" in report
    assert "missing_required_readiness_fields" in report


def test_validator_rejects_missing_readiness_fields(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"
    run_distillation(
        DistillationRunConfig(
            manifest=manifest,
            output_dir=output_dir,
            split="train",
            mode="mock",
            seed=42,
            overwrite=True,
        )
    )
    record = _read_jsonl(output_dir / "distillation_records.jsonl")[0]
    record.pop("sample_key")

    result = validate_distillation_record(record)

    assert result.valid is False
    assert "missing required key: sample_key" in result.issues
