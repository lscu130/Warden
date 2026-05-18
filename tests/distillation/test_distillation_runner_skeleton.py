import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from warden.distillation.evidence_pack import build_evidence_pack
from warden.distillation.manifest_reader import read_manifest_records
from warden.distillation.mock_teacher import build_mock_record
from warden.distillation.runner import DistillationRunConfig, run_distillation
from warden.distillation.schema_validator import validate_distillation_record


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_sample(sample_dir: Path, visible_text: str = "Welcome to Example University search portal.") -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        sample_dir / "url.json",
        {
            "input_url": "https://example.edu/",
            "final_url": "https://example.edu/home",
            "final_host": "example.edu",
        },
    )
    (sample_dir / "visible_text.txt").write_text(visible_text, encoding="utf-8")
    _write_json(
        sample_dir / "forms.json",
        {"forms": [{"action": "https://example.edu/search", "inputs": [{"type": "text", "name": "q"}]}]},
    )
    _write_json(sample_dir / "net_summary.json", {"requests": [{"url": "https://example.edu/home"}]})
    (sample_dir / "html_rendered.html").write_text(
        "<html><body><form><input name='q'><button>Search</button></form></body></html>",
        encoding="utf-8",
    )
    return sample_dir


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> Path:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_manifest_reader_reads_small_csv(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )

    records = list(read_manifest_records(manifest, requested_split="train"))

    assert len(records) == 1
    assert records[0].sample_id == "s1"
    assert records[0].sample_path == sample
    assert records[0].split == "train"


def test_evidence_pack_excludes_label_and_split_metadata_from_evidence_text(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    row = {
        "sample_id": "s1",
        "current_path": str(sample),
        "split": "train",
        "triage_label": "T99_should_not_be_prompt_text",
    }

    pack = build_evidence_pack(row)
    serialized = json.dumps(pack.teacher_visible_evidence, ensure_ascii=False)

    assert "T99_should_not_be_prompt_text" not in serialized
    assert "triage_label" not in serialized
    assert "split" not in serialized


def test_mock_teacher_output_validates_against_schema(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    pack = build_evidence_pack({"sample_id": "s1", "current_path": str(sample), "split": "train"})

    record = build_mock_record(pack, split="train", seed=42, diagnostic_only=True)
    result = validate_distillation_record(record)

    assert result.valid is True
    assert record["schema_version"] == "warden_distill_v0.3_mock"
    assert record["teacher_model"] == "mock_teacher_v0"
    assert record["teacher_profile"] == "mock_v0_3_formula"
    assert record["prompt_template_version"] == "warden_distill_v0.3"
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
    assert set(record["formula_concepts"]["risk_bearing_engagement"]) >= {
        "direct_high_risk_action",
        "routed_high_risk_action",
        "action_preparation",
        "deceptive_funnel_priming",
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
    assert set(record["text_semantic_concepts"]) >= {
        "claimed_identity_candidates",
        "identity_claim",
        "action_surface",
        "behavior_context",
        "relation_judgments",
        "evidence_state",
        "threat_action_candidate",
        "concept_level_evaluation_readiness",
    }
    assert record["text_semantic_concepts"]["action_surface"][
        "action_surface_is_not_automatically_threat_action"
    ] is True
    assert record["text_semantic_concepts"]["relation_judgments"]["unknown_is_not_malicious"] is True
    assert record["text_semantic_concepts"]["evidence_state"][
        "payload_not_observed_is_not_automatic_benign"
    ] is True
    assert record["decision_head_auxiliary_targets"]["do_not_train_as_gold"] is True
    assert record["decision_head_auxiliary_targets"]["final_label_advisory"] == "unknown_diagnostic_only"


def test_mock_records_are_always_non_gold_and_diagnostic(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    pack = build_evidence_pack({"sample_id": "s1", "current_path": str(sample), "split": "train"})

    record = build_mock_record(pack, split="train", seed=7, diagnostic_only=True)

    assert record["do_not_train_as_gold"] is True
    assert record["diagnostic_only"] is True


def test_val_or_test_without_diagnostic_only_fails_closed(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "val"}],
    )

    config = DistillationRunConfig(
        manifest=manifest,
        output_dir=tmp_path / "out",
        split="val",
        mode="mock",
        diagnostic_only=False,
    )

    with pytest.raises(ValueError, match="diagnostic-only"):
        run_distillation(config)


def test_resume_skips_already_processed_samples(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"

    first = run_distillation(
        DistillationRunConfig(manifest=manifest, output_dir=output_dir, split="train", mode="mock", overwrite=True)
    )
    second = run_distillation(
        DistillationRunConfig(manifest=manifest, output_dir=output_dir, split="train", mode="mock", resume=True)
    )

    records = _read_jsonl(output_dir / "distillation_records.jsonl")
    assert first.processed_count == 1
    assert second.skipped_existing_count == 1
    assert second.processed_count == 0
    assert len(records) == 1


def test_existing_output_without_resume_or_overwrite_fails_closed(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"
    run_distillation(
        DistillationRunConfig(manifest=manifest, output_dir=output_dir, split="train", mode="mock", overwrite=True)
    )

    with pytest.raises(FileExistsError):
        run_distillation(DistillationRunConfig(manifest=manifest, output_dir=output_dir, split="train", mode="mock"))


def test_review_queue_receives_sparse_or_missing_evidence_samples(tmp_path):
    sample = _make_sample(tmp_path / "sample", visible_text="")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"

    run_distillation(
        DistillationRunConfig(manifest=manifest, output_dir=output_dir, split="train", mode="mock", overwrite=True)
    )

    review_rows = _read_jsonl(output_dir / "review_queue.jsonl")
    assert review_rows
    assert any("evidence_sufficiency_low" in row["review_reasons"] for row in review_rows)


def test_schema_validator_rejects_forbidden_fields():
    record = {
        "schema_version": "warden_distill_v0.3_mock",
        "record_id": "r1",
        "sample_id": "s1",
        "sample_path": "sample",
        "split": "train",
        "diagnostic_only": True,
        "do_not_train_as_gold": True,
        "teacher_model": "mock_teacher_v0",
        "teacher_role": "mock_skeleton",
        "input_modalities": [],
        "fallback_reason": None,
        "evidence_pack_summary": {},
        "rule_router_observation": {},
        "formula_semantics": {},
        "formula_concepts": {},
        "claimed_identity_candidates": [],
        "text_semantic_concepts": {},
        "vision_evidence": {},
        "decision_head_auxiliary_targets": {},
        "quality_flags": {"needs_human_review": False, "schema_valid": True},
        "review_reasons": [],
        "created_at": "2026-05-12T00:00:00Z",
        "final_gold_label": "malicious",
    }

    result = validate_distillation_record(record)

    assert result.valid is False
    assert any("forbidden field" in issue for issue in result.issues)


def test_schema_validator_rejects_missing_required_concept_fields(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    pack = build_evidence_pack({"sample_id": "s1", "current_path": str(sample), "split": "train"})
    record = build_mock_record(pack, split="train", seed=42, diagnostic_only=True)
    record["text_semantic_concepts"].pop("relation_judgments")

    result = validate_distillation_record(record)

    assert result.valid is False
    assert (
        "missing required concept key: text_semantic_concepts.relation_judgments"
        in result.issues
    )


def test_schema_validator_rejects_missing_formula_concepts(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    pack = build_evidence_pack({"sample_id": "s1", "current_path": str(sample), "split": "train"})
    record = build_mock_record(pack, split="train", seed=42, diagnostic_only=True)
    record["formula_concepts"].pop("context_engagement_relation")

    result = validate_distillation_record(record)

    assert result.valid is False
    assert "missing required formula concept key: formula_concepts.context_engagement_relation" in result.issues


def test_cli_smoke_writes_required_output_files(tmp_path):
    sample = _make_sample(tmp_path / "sample")
    manifest = _write_manifest(
        tmp_path / "manifest.csv",
        [{"sample_id": "s1", "current_path": str(sample), "split": "train"}],
    )
    output_dir = tmp_path / "out"

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "distillation" / "run_distillation_skeleton.py"),
            "--manifest",
            str(manifest),
            "--output-dir",
            str(output_dir),
            "--split",
            "train",
            "--mode",
            "mock",
            "--limit",
            "1",
            "--seed",
            "42",
            "--overwrite",
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    for name in ["distillation_records.jsonl", "review_queue.jsonl", "run_audit.json", "run_report.md", "errors.jsonl"]:
        assert (output_dir / name).exists()

    audit = json.loads((output_dir / "run_audit.json").read_text(encoding="utf-8"))
    assert audit["schema_version"] == "warden_distill_v0.3_mock"
    assert audit["prompt_template_version"] == "warden_distill_v0.3"
    assert audit["external_api_calls"] == 0
    assert audit["teacher_calls"] == 0
    assert audit["ocr_calls"] == 0
    assert audit["yolo_calls"] == 0
    assert audit["clip_calls"] == 0
    assert audit["missing_required_concept_fields"] == {}
    assert audit["concept_level_readiness"]["records_with_formula_concepts"] == 1
    assert audit["concept_level_readiness"]["records_with_formula_result"] == 1

    records = _read_jsonl(output_dir / "distillation_records.jsonl")
    assert records
    assert all(record["do_not_train_as_gold"] is True for record in records)
    assert all(record["diagnostic_only"] is True for record in records)
    assert all("formula_concepts" in record for record in records)
