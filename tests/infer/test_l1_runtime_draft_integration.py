import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from warden.runtime.l1_draft_bridge import (
    L1_DRAFT_ENV_VAR,
    l1_draft_enabled,
    maybe_attach_l1_draft_trace,
    run_l1_draft_bridge,
)
from warden.runtime.pipeline import build_sample_context, process_sample


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_runtime_sample(sample_dir: Path) -> Path:
    sample_dir.mkdir(parents=True, exist_ok=True)
    _write_json(sample_dir / "meta.json", {"sample_id": "runtime_l1_draft_sample", "label": "benign"})
    _write_json(
        sample_dir / "url.json",
        {
            "input_url": "https://example.test/",
            "final_url": "https://example.test/login",
            "redirect_chain": [],
        },
    )
    (sample_dir / "visible_text.txt").write_text("Sign in to verify your account.", encoding="utf-8")
    _write_json(
        sample_dir / "forms.json",
        {"forms": [{"action": "https://example.test/login", "inputs": [{"type": "password", "name": "password"}]}]},
    )
    _write_json(
        sample_dir / "net_summary.json",
        {"requests": [{"url": "https://example.test/login", "method": "POST"}]},
    )
    _write_json(
        sample_dir / "html_rendered.json",
        {"text": "<form><input type='password' name='password'><button>Login</button></form>"},
    )
    return sample_dir


def test_l1_draft_flag_defaults_to_disabled(monkeypatch):
    monkeypatch.delenv(L1_DRAFT_ENV_VAR, raising=False)

    assert l1_draft_enabled() is False


def test_disabled_flag_does_not_call_l1_draft(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    context = build_sample_context(sample_dir)
    called = False

    def runner(_sample_dir: Path) -> dict:
        nonlocal called
        called = True
        return {}

    monkeypatch.delenv(L1_DRAFT_ENV_VAR, raising=False)
    trace = maybe_attach_l1_draft_trace(context)

    assert trace is None
    assert called is False
    assert "l1_draft" not in context.terminal_outputs


def test_enabled_flag_records_l1_draft_trace_and_preserves_official_result(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    monkeypatch.setenv(L1_DRAFT_ENV_VAR, "1")

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))
    trace = json.loads(Path(record["trace_path"]).read_text(encoding="utf-8"))
    draft = trace["debug_sidecars"]["l1_draft"]

    assert result["sample_id"] == "runtime_l1_draft_sample"
    assert result["final_stage"] in {"L0", "L1", "L2"}
    assert result["routing_outcome"]["stage"] == result["final_stage"]
    assert result["debug_sidecars"]["l1_draft"]["draft"] is True
    assert draft["enabled"] is True
    assert draft["not_final_schema"] is True
    assert draft["status"] == "ok"
    assert draft["result"]["result_kind"] == "warden_l1_rule_baseline_draft_v1"
    assert draft["result"]["evidence_ledger"]
    assert draft["result"]["reason_codes"]
    assert draft["result"]["explanation"]


def test_disabled_runtime_output_has_no_l1_draft_sidecar(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    monkeypatch.delenv(L1_DRAFT_ENV_VAR, raising=False)

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))
    trace = json.loads(Path(record["trace_path"]).read_text(encoding="utf-8"))

    assert "debug_sidecars" not in result
    assert "debug_sidecars" not in trace


def test_l1_draft_exception_is_captured_without_failing_runtime(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"

    def boom(_sample_dir: Path) -> dict:
        raise RuntimeError("draft exploded")

    monkeypatch.setenv(L1_DRAFT_ENV_VAR, "1")
    monkeypatch.setattr("warden.runtime.l1_draft_bridge.run_l1_baseline_for_sample", boom)

    record = process_sample(sample_dir, output_dir)
    trace = json.loads(Path(record["trace_path"]).read_text(encoding="utf-8"))
    draft = trace["debug_sidecars"]["l1_draft"]

    assert Path(record["result_path"]).exists()
    assert draft["status"] == "error"
    assert draft["error"]["type"] == "RuntimeError"
    assert "draft exploded" in draft["error"]["message"]


def test_label_split_and_triage_metadata_do_not_enter_evidence_inputs(tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "T00_benign_folder_label")
    _write_json(
        sample_dir / "meta.json",
        {
            "sample_id": "runtime_l1_draft_sample",
            "label": "manual_benign_label",
            "triage_label": "T00",
            "split": "train",
        },
    )
    context = build_sample_context(sample_dir)

    draft = run_l1_draft_bridge(context)
    evidence_only = {
        "features": draft["result"]["features"],
        "evidence_ledger": draft["result"]["evidence_ledger"],
        "explanation": draft["result"]["explanation"],
        "reason_codes": draft["result"]["reason_codes"],
    }
    serialized = json.dumps(evidence_only, ensure_ascii=False)

    assert "manual_benign_label" not in serialized
    assert "T00" not in serialized
    assert "train" not in serialized
    assert "folder_label" not in serialized
