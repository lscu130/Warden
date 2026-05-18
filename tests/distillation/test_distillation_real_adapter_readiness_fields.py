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
    "evidence_pack_id",
    "teacher_profile",
    "teacher_provider",
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
    "validation",
    "error_status",
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
    validation_summaries = _read_jsonl(output_dir / "validation_summaries.jsonl")
    review_rows = _read_jsonl(output_dir / "review_queue.jsonl")
    audit = json.loads((output_dir / "run_audit.json").read_text(encoding="utf-8"))
    report = (output_dir / "run_report.md").read_text(encoding="utf-8")
    adapter_report = (output_dir / "adapter_readiness_report.md").read_text(encoding="utf-8")

    assert result.processed_count == 1
    assert len(records) == 1
    assert len(attempts) == 1
    assert len(validation_summaries) == 1
    assert (output_dir / "prompt_snapshots").is_dir()
    assert (output_dir / "raw_outputs").is_dir()
    assert (output_dir / "repaired_outputs").is_dir()

    record = records[0]
    assert READINESS_FIELDS.issubset(record)
    assert record["sample_key"]
    assert record["source_manifest"] == str(manifest)
    assert record["source_split"] == "train"
    assert record["teacher_profile"] == "mock_v0_3_formula"
    assert record["teacher_provider"] == "mock"
    assert record["teacher_run_id"] == audit["teacher_run_id"]
    assert record["prompt_template_id"] == "warden_distill_v0.3.primary_mock"
    assert record["prompt_template_version"] == "warden_distill_v0.3"
    assert record["prompt_snapshot_path"]
    assert record["raw_output_path"]
    assert record["repaired_output_path"] is None
    assert record["validation_status"] == "passed"
    assert record["validation_errors"] == []
    assert record["image_input_expected"] is False
    assert record["image_input_passed_to_teacher"] is False
    assert record["modality_guard_status"] == "mock_no_image_input"
    assert record["image_input_policy"] == "not_supported_in_mock"
    assert record["visual_evidence_source"] == "none"
    assert record["attempt_status"] == "mock_completed"
    assert record["repair_attempted"] is False
    assert record["repair_reason"] is None
    assert record["token_usage_placeholder"]["mock_only"] is True
    assert record["cost_placeholder"]["mock_only"] is True
    assert record["latency_ms_placeholder"] is None
    assert record["provider_request_id_placeholder"] is None
    assert record["failure_category"] is None
    assert record["retry_allowed"] is False
    assert record["rollback_required"] is False
    assert record["do_not_train_as_gold"] is True
    assert record["diagnostic_only"] is True
    assert record["validation"]["schema_valid"] is True
    assert record["validation"]["required_fields_present"] is True
    assert record["validation"]["errors"] == []
    assert record["error_status"]["status"] == "ok"
    assert record["schema_version"] == "warden_distill_v0.3_mock"
    assert record["formula_semantics"]["web_se_formula"] == (
        "EvidenceSufficient(ManipulativeContext AND RiskBearingEngagement)"
    )
    assert record["formula_semantics"]["risk_bearing_engagement_formula"] == (
        "DirectHighRiskAction OR RoutedHighRiskAction OR ActionPreparation OR DeceptiveFunnelPriming"
    )
    assert set(record["formula_concepts"]) >= {
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
    }
    assert record["formula_concepts"]["action_surface"]["not_threat_by_itself"] is True
    assert (
        record["formula_concepts"]["risk_bearing_engagement"][
            "action_surface_is_not_automatically_risk_bearing_engagement"
        ]
        is True
    )
    assert record["formula_concepts"]["formula_result"]["web_se_threat_formula_satisfied"] is False
    assert "claimed_identity_candidates" in record
    assert record["text_semantic_concepts"]["claimed_identity_candidates"] == record["claimed_identity_candidates"]
    assert "identity_claim" in record["text_semantic_concepts"]
    assert "action_surface" in record["text_semantic_concepts"]
    assert "behavior_context" in record["text_semantic_concepts"]
    assert "relation_judgments" in record["text_semantic_concepts"]
    assert "evidence_state" in record["text_semantic_concepts"]
    assert "threat_action_candidate" in record["text_semantic_concepts"]
    assert record["decision_head_auxiliary_targets"]["do_not_train_as_gold"] is True
    assert record["record_hash"]
    assert record["evidence_pack_hash"]
    assert record["prompt_input_hash"]
    assert validate_distillation_record(record).valid is True

    attempt = attempts[0]
    assert attempt["attempt_id"] == record["attempt_id"]
    assert attempt["record_id"] == record["record_id"]
    assert attempt["sample_key"] == record["sample_key"]
    assert attempt["teacher_run_id"] == record["teacher_run_id"]
    assert attempt["mock_only"] is True
    assert attempt["attempt_status"] == "mock_completed"
    assert attempt["real_teacher_call"] is False
    assert attempt["external_api_call"] is False
    assert attempt["raw_output_path"] == record["raw_output_path"]
    assert attempt["prompt_snapshot_path"] == record["prompt_snapshot_path"]
    assert attempt["repaired_output_path"] is None
    assert attempt["repair_attempted"] is False
    assert attempt["validation_status"] == "passed"
    assert attempt["schema_valid"] is True

    validation_summary = validation_summaries[0]
    assert validation_summary["mock_only"] is True
    assert validation_summary["record_id"] == record["record_id"]
    assert validation_summary["validation_status"] == "passed"
    assert validation_summary["validation_errors"] == []

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
        "priority",
        "do_not_train_as_gold",
        "not_train_as_gold",
        "diagnostic_only",
        "short_evidence_context",
        "formula_failure_mode",
        "risk_bearing_engagement_uncertainty",
        "url_claim_state",
        "visible_impersonation_state",
        "funnel_affordance_state",
        "suggested_next_action",
        "concept_level_review",
    ):
        assert key in review
    assert review["record_id"] == record["record_id"]
    assert review["sample_key"] == record["sample_key"]

    assert audit["teacher_run_id"] == record["teacher_run_id"]
    assert audit["schema_version"] == "warden_distill_v0.3_mock"
    assert audit["prompt_template_version"] == "warden_distill_v0.3"
    assert audit["source_manifest"] == str(manifest)
    assert audit["source_split"] == "train"
    assert audit["records_written"] == 1
    assert audit["records_valid"] == 1
    assert audit["records_invalid"] == 0
    assert audit["attempt_count"] == 1
    assert audit["repair_count"] == 0
    assert audit["validation_pass_count"] == 1
    assert audit["validation_fail_count"] == 0
    assert audit["mock_teacher_calls"] == 1
    assert audit["real_teacher_calls"] == 0
    assert audit["external_api_calls"] == 0
    assert audit["ocr_calls"] == 0
    assert audit["yolo_calls"] == 0
    assert audit["clip_calls"] == 0
    assert audit["do_not_train_as_gold_failures"] == 0
    assert audit["diagnostic_only_failures"] == 0
    assert audit["adapter_readiness_status"] == "ready_for_no_network_dry_run"
    assert audit["live_teacher_readiness"] == "not_ready_for_live_teacher"
    assert audit["cost_token_placeholders"]["mock_only"] is True
    assert "prompt_snapshots" in audit["output_path_inventory"]
    assert "adapter_readiness_report" in audit["output_path_inventory"]
    assert audit["missing_required_readiness_fields"] == {}
    assert audit["missing_required_concept_fields"] == {}
    assert audit["concept_level_readiness"]["records_with_formula_concepts"] == 1
    assert audit["concept_level_readiness"]["records_with_formula_result"] == 1
    assert audit["concept_level_readiness"]["records_with_relation_judgments"] == 1

    assert "teacher_run_id" in report
    assert "schema_version" in report
    assert "prompt_template_version" in report
    assert "mock_teacher_calls" in report
    assert "missing_required_readiness_fields" in report
    assert "missing_required_concept_fields" in report
    assert "adapter_readiness_status" in report
    assert "not_ready_for_live_teacher" in report
    assert "ready_for_no_network_dry_run" in adapter_report
    assert "not_ready_for_live_teacher" in adapter_report


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
