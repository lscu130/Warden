import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from scripts.l1.run_l1_draft_mixed_runtime_benchmark import (
    build_summary,
    detect_final_like_label_leakage,
    load_candidate_rows,
    main,
    sample_rows,
)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_sample(sample_dir: Path, *, visible_text: str = "Welcome to a normal website.") -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    _write_json(sample_dir / "meta.json", {"sample_id": sample_dir.name})
    _write_json(
        sample_dir / "url.json",
        {"input_url": "https://example.test/", "final_url": "https://example.test/"},
    )
    (sample_dir / "visible_text.txt").write_text(visible_text, encoding="utf-8")
    _write_json(sample_dir / "forms.json", {"forms": []})
    _write_json(sample_dir / "net_summary.json", {"requests": []})
    return sample_dir


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["sample_id", "triage_label", "current_path"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_manifest_loader_maps_t00_t01_buckets(tmp_path):
    t00 = _make_sample(tmp_path / "t00")
    t01 = _make_sample(tmp_path / "t01")
    manifest = tmp_path / "manifest.csv"
    _write_manifest(
        manifest,
        [
            {"sample_id": "t00", "triage_label": "T00_clear_benign", "current_path": str(t00)},
            {"sample_id": "t01", "triage_label": "T01_benign_hard_negative", "current_path": str(t01)},
        ],
    )

    rows = load_candidate_rows(
        type(
            "Args",
            (),
            {
                "benign_train": None,
                "benign_val": str(manifest),
                "benign_test": None,
                "input_manifest": [],
                "malicious_manifest": [],
            },
        )()
    )

    assert {row["_bucket"] for row in rows} == {"B00_benign_clear", "B01_benign_hard_negative"}


def test_sampling_respects_limit_per_bucket(tmp_path):
    rows = []
    for index in range(5):
        rows.append({"current_path": str(tmp_path / f"t00_{index}"), "_bucket": "B00_benign_clear"})
        rows.append({"current_path": str(tmp_path / f"t01_{index}"), "_bucket": "B01_benign_hard_negative"})

    selected = sample_rows(rows, limit_per_bucket=2, seed=42)

    counts = {}
    for row in selected:
        counts[row["_bucket"]] = counts.get(row["_bucket"], 0) + 1
    assert counts == {"B00_benign_clear": 2, "B01_benign_hard_negative": 2}


def test_benchmark_cli_writes_required_outputs(tmp_path):
    t00 = _make_sample(tmp_path / "t00", visible_text="Welcome to a normal homepage.")
    t01 = _make_sample(tmp_path / "t01", visible_text="Sign in to manage your account.")
    manifest = tmp_path / "manifest.csv"
    output_dir = tmp_path / "out"
    _write_manifest(
        manifest,
        [
            {"sample_id": "t00", "triage_label": "T00_clear_benign", "current_path": str(t00)},
            {"sample_id": "t01", "triage_label": "T01_benign_hard_negative", "current_path": str(t01)},
        ],
    )

    rc = main(
        [
            "--benign-val",
            str(manifest),
            "--output-dir",
            str(output_dir),
            "--limit-per-bucket",
            "1",
            "--seed",
            "42",
        ]
    )

    assert rc == 0
    results = output_dir / "l1_draft_mixed_runtime_results_v1.jsonl"
    summary = output_dir / "l1_draft_mixed_runtime_summary_v1.csv"
    report = output_dir / "l1_draft_mixed_runtime_report_v1.md"
    errors = output_dir / "l1_draft_mixed_runtime_errors_v1.csv"
    assert results.exists()
    assert summary.exists()
    assert report.exists()
    assert errors.exists()
    rows = [json.loads(line) for line in results.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2
    assert all(row["runtime_status"] == "ok" for row in rows)
    assert all(row["has_l1_draft_sidecar"] is True for row in rows)
    assert all(row["official_fields_match_flag_off"] is True for row in rows)
    assert all(row["l1_rule_assessment"] for row in rows)
    assert all(row["final_like_label_leakage"] is False for row in rows)
    report_text = report.read_text(encoding="utf-8")
    assert "rule_assessment distribution" in report_text
    assert "label distribution" not in report_text
    assert all(row["flag_off_has_debug_sidecars"] is False for row in rows)


def test_summary_counts_runtime_errors():
    summary = build_summary(
        [
            {
                "bucket": "B00_benign_clear",
                "runtime_status": "ok",
                "l1_draft_status": "ok",
                "has_l1_draft_sidecar": True,
                "l1_draft_duration_ms": 1.0,
                "total_runtime_duration_ms": 2.0,
                "l1_draft_need_ocr": False,
                "l1_draft_need_yolo": False,
                "l1_draft_need_review": False,
                "l1_rule_assessment": "low_risk_candidate",
                "l1_risk_hint_high_risk_candidate": False,
                "l1_risk_hint_low_risk_candidate": True,
                "final_like_label_leakage": False,
                "official_fields_match_flag_off": True,
                "flag_off_has_debug_sidecars": False,
            },
            {
                "bucket": "B01_benign_hard_negative",
                "runtime_status": "error",
                "l1_draft_status": "",
                "has_l1_draft_sidecar": False,
                "l1_draft_duration_ms": "",
                "total_runtime_duration_ms": "",
                "l1_draft_need_ocr": "",
                "l1_draft_need_yolo": "",
                "l1_draft_need_review": "",
                "l1_rule_assessment": "",
                "l1_risk_hint_high_risk_candidate": "",
                "l1_risk_hint_low_risk_candidate": "",
                "final_like_label_leakage": False,
                "official_fields_match_flag_off": False,
                "flag_off_has_debug_sidecars": False,
            },
        ]
    )

    assert summary["runtime_success_count"] == 1
    assert summary["runtime_error_count"] == 1
    assert summary["missing_sidecar_count"] == 1
    assert summary["rule_assessment_distribution"] == {"low_risk_candidate": 1, "": 1}
    assert summary["final_like_label_leakage_warning_count"] == 0


def test_detects_final_like_label_leakage():
    assert detect_final_like_label_leakage({"label": "malicious"}) is True
    assert detect_final_like_label_leakage({"rule_router": {"label": "benign"}}) is True
    assert detect_final_like_label_leakage({"rule_router": {"rule_assessment": "high_risk_candidate"}}) is False
