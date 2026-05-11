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

    assert result["label"] in {"malicious", "suspicious", "unknown", "benign"}
    assert "login_surface_present" in result["reason_codes"]
    assert result["payload_observed"] is True
    assert result["evidence_ledger"]
    assert result["explanation"]["summary"]
    assert result["explanation"]["positive_evidence"]


def test_manifest_row_uses_current_path(tmp_path):
    sample_dir = _make_sample(tmp_path / "sample")

    result = run_l1_baseline_for_manifest_row({"current_path": str(sample_dir), "triage_label": "T00"})

    assert result["sample_dir"] == str(sample_dir)
    serialized = json.dumps(result, ensure_ascii=False)
    assert "T00" not in serialized


def test_explanation_renderer_only_uses_ledger_claims():
    explanation = render_explanation(
        label="unknown",
        malicious_basis="insufficient_evidence",
        risk_axes=["evidence_incompleteness_risk"],
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
