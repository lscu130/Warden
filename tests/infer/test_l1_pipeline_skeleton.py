import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from warden.l1.evidence_pack import build_evidence_pack
from warden.l1.explanation_renderer import render_explanation
from warden.l1.form_features import extract_form_features
from warden.l1.html_action_extractor import extract_actionable_html_features
from warden.l1.l1_runner import run_l1_baseline_for_manifest_row, run_l1_baseline_for_sample


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_sample(sample_dir: Path) -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        sample_dir / "url.json",
        {
            "input_url": "https://example-login.test/start",
            "final_url": "https://example-login.test/login?next=dashboard",
            "redirect_chain": ["https://example-login.test/start", "https://example-login.test/login"],
        },
    )
    (sample_dir / "visible_text.txt").write_text("Sign in to verify your account now.", encoding="utf-8")
    _write_json(
        sample_dir / "forms.json",
        {
            "forms": [
                {
                    "action": "https://collector.example.net/post",
                    "inputs": [{"type": "password", "name": "password"}],
                }
            ]
        },
    )
    _write_json(
        sample_dir / "net_summary.json",
        {
            "requests": [
                {"url": "https://example-login.test/login", "method": "GET"},
                {"url": "https://collector.example.net/post", "method": "POST"},
            ]
        },
    )
    _write_json(
        sample_dir / "html_rendered.json",
        {
            "text": "<html><body><h1>Account verify</h1><form action='https://collector.example.net/post'><input type='password' name='password'><button>Login</button></form><a href='https://example.org/help'>Help</a></body></html>"
        },
    )
    return sample_dir


def test_evidence_pack_records_missing_files_and_bad_json_without_crashing(tmp_path):
    sample_dir = tmp_path / "sample"
    sample_dir.mkdir()
    (sample_dir / "url.json").write_text("{bad json", encoding="utf-8")

    pack = build_evidence_pack(sample_dir)

    assert pack["sample_dir"] == str(sample_dir)
    assert "visible_text.txt" in pack["missing_artifacts"]
    assert any(issue["artifact"] == "url.json" for issue in pack["issues"])


def test_evidence_pack_reuses_cheap_snapshot_for_cheap_artifacts(tmp_path):
    sample_dir = _make_sample(tmp_path / "sample")
    snapshot = {
        "schema_version": "cheap_evidence_snapshot_v1",
        "artifact_presence": {
            "url_json": True,
            "visible_text_txt": True,
            "forms_json": True,
            "net_summary_json": True,
        },
        "url_info": {"input_url": "https://snapshot.test/", "final_url": "https://snapshot.test/login"},
        "visible_text": "Snapshot visible text",
        "forms_payload": {"forms": [{"inputs": [{"type": "password"}]}]},
        "net_summary": {"requests": [{"url": "https://snapshot.test/login", "method": "POST"}]},
    }
    (sample_dir / "visible_text.txt").unlink()
    (sample_dir / "forms.json").unlink()
    (sample_dir / "net_summary.json").unlink()

    pack = build_evidence_pack(sample_dir, cheap_snapshot=snapshot)

    assert pack["evidence_construction_mode"] == "incremental_from_cheap_snapshot"
    assert pack["cheap_snapshot_reused"] is True
    assert pack["cheap_snapshot_schema_version"] == "cheap_evidence_snapshot_v1"
    assert pack["visible_text"] == "Snapshot visible text"
    assert pack["forms_payload"] == snapshot["forms_payload"]
    assert pack["net_summary"] == snapshot["net_summary"]
    assert "visible_text.txt" not in pack["missing_artifacts"]
    assert "forms.json" not in pack["missing_artifacts"]
    assert "net_summary.json" not in pack["missing_artifacts"]


def test_actionable_html_extraction_recognizes_core_tags():
    features = extract_actionable_html_features(
        "<html><head><title>Login</title></head><body><h1>Verify</h1>"
        "<form><input type='password' name='password'><button>Continue</button></form>"
        "<a href='https://external.example/path'>Help</a></body></html>",
        base_host="brand.example",
    )

    assert features["form_count"] == 1
    assert features["input_count"] == 1
    assert features["password_input_count"] == 1
    assert features["external_link_count"] == 1
    assert "Continue" in features["button_texts_sample"]


def test_form_features_detect_password_surface():
    features = extract_form_features(
        {"forms": [{"action": "https://collector.example/post", "inputs": [{"type": "password", "name": "pass"}]}]},
        final_host="brand.example",
    )

    assert features["form_count"] == 1
    assert features["input_total"] == 1
    assert features["has_password"] is True
    assert features["off_domain_form_action"] is True


def test_l1_baseline_generates_reason_codes_and_explanation(tmp_path):
    sample_dir = _make_sample(tmp_path / "sample")

    result = run_l1_baseline_for_sample(sample_dir)

    assert result["stage"] == "L1"
    assert result["draft"] is True
    assert result["not_final_schema"] is True
    assert "label" not in result
    assert result["rule_router"]["rule_assessment"] in {
        "low_risk_candidate",
        "benign_hard_negative_candidate",
        "text_sufficient",
        "text_sparse",
        "html_action_sparse",
        "needs_text_model_judgment",
        "needs_vision_evidence",
        "needs_review",
        "insufficient_observability",
        "high_risk_candidate",
        "insufficient_evidence",
    }
    assert "login_surface_present" in result["rule_router"]["reason_codes"]
    assert result["decision_head"]["status"] == "not_run"
    assert result["decision_head"]["final_label"] is None
    assert result["decision_head"]["risk_score"] is None
    assert result["decision_head"]["confidence"] is None
    assert result["evidence_ledger"]
    assert result["explanation"]["type"] == "routing_diagnostic"
    assert "final" not in result["explanation"]["summary"].lower()
    assert result["explanation"]["positive_evidence"]


def test_manifest_row_uses_current_path(tmp_path):
    sample_dir = _make_sample(tmp_path / "sample")

    result = run_l1_baseline_for_manifest_row({"current_path": str(sample_dir), "triage_label": "T00"})

    assert result["sample_dir"] == str(sample_dir)
    serialized = json.dumps(result, ensure_ascii=False)
    assert "T00" not in serialized


def test_explanation_renderer_only_uses_ledger_claims():
    explanation = render_explanation(
        rule_assessment="insufficient_evidence",
        routing_hints={"need_review": True},
        risk_hints={"action_surface_present": False},
        evidence_sufficiency={"visible_text_status": "missing"},
        reason_codes=["insufficient_evidence"],
        routing={"need_review_candidate": True},
        evidence_ledger=[
            {
                "evidence_id": "ev1",
                "source": "artifact_presence",
                "claim": "visible text missing",
                "value": True,
                "confidence": None,
                "stance": "limits",
                "reason_code": "visible_text_missing",
            }
        ],
    )

    joined = " ".join(explanation["positive_evidence"] + explanation["limiting_evidence"])
    assert "visible text missing" in joined
    assert "password" not in joined.lower()
    assert explanation["type"] == "routing_diagnostic"
    assert "malicious" not in explanation["summary"].lower()
    assert "benign" not in explanation["summary"].lower()


def test_cli_smoke_runs_on_tiny_manifest(tmp_path):
    sample_dir = _make_sample(tmp_path / "sample")
    manifest = tmp_path / "manifest.csv"
    output = tmp_path / "results.jsonl"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["current_path", "triage_label"])
        writer.writeheader()
        writer.writerow({"current_path": str(sample_dir), "triage_label": "T00"})

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "l1" / "run_l1_baseline_smoke.py"),
            "--manifest",
            str(manifest),
            "--limit",
            "1",
            "--output",
            str(output),
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["sample_dir"] == str(sample_dir)
    assert "label" not in rows[0]
    assert rows[0]["decision_head"]["status"] == "not_run"


def test_invalid_capture_like_sample_is_diagnostic_only_without_recrawl_or_final_label(tmp_path):
    sample_dir = tmp_path / "invalid_capture_like"
    sample_dir.mkdir()
    _write_json(sample_dir / "url.json", {"input_url": "https://example.test/", "final_url": "https://example.test/"})

    result = run_l1_baseline_for_sample(sample_dir)
    router = result["rule_router"]

    assert "label" not in result
    assert router["rule_assessment"] in {"insufficient_evidence", "insufficient_observability"}
    assert "need_recrawl" not in router["routing_hints"]
    assert router["routing_assessment"] != "route_to_recrawl"
    serialized = json.dumps(result, ensure_ascii=False)
    assert '"final_label": null' in serialized
