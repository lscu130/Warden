import json
import sys
from types import SimpleNamespace
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
import warden.runtime.pipeline as runtime_pipeline
from warden.runtime.pipeline import build_cheap_evidence_snapshot, build_sample_context, process_sample


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


def _fake_l0_module(routing_hints: dict, specialized_surface_signals: dict | None = None) -> SimpleNamespace:
    def prepare_l0_inputs(**kwargs):
        return {
            "input_url": kwargs.get("input_url", ""),
            "final_url": kwargs.get("final_url", ""),
            "raw_visible_text": kwargs.get("visible_text", ""),
            "visible_text": kwargs.get("visible_text", ""),
            "url_features": {},
            "forms_summary": {},
            "net_features": {},
            "html_features": {},
        }

    def derive_l0_outputs(**_kwargs):
        return {
            "page_stage_candidate": "other",
            "language_candidate": "unknown",
            "risk_outputs": {},
            "intent_signals": {},
            "evasion_signals": {},
            "specialized_surface_signals": specialized_surface_signals or {},
            "l0_routing_hints": routing_hints,
        }

    return SimpleNamespace(prepare_l0_inputs=prepare_l0_inputs, derive_l0_outputs=derive_l0_outputs)


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
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module({}))

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
    assert draft["result"]["result_kind"] == "warden_l1_routing_diagnostic_draft_v1"
    assert draft["result"]["evidence_construction"]["cheap_snapshot_reused"] is True
    assert draft["result"]["evidence_construction"]["cheap_snapshot_schema_version"] == "cheap_evidence_snapshot_v1"
    assert draft["result"]["rule_router"]["rule_assessment"]
    assert draft["result"]["decision_head"]["status"] == "not_run"
    assert "label" not in draft["result"]
    assert draft["result"]["evidence_ledger"]
    assert draft["result"]["rule_router"]["reason_codes"]
    assert draft["result"]["explanation"]


def test_valid_non_terminal_l0_sample_routes_to_l1_by_default(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    monkeypatch.delenv(L1_DRAFT_ENV_VAR, raising=False)
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module({}))

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))

    assert result["stage_sequence"][:2] == ["L0", "L1"]
    assert result["stage_routing_outcomes"]["L0"]["next_stage"] == "L1"
    assert result["stage_routing_outcomes"]["L0"]["outcome_kind"] == "route_to_l1_default"
    assert "valid_non_terminal_sample_routes_to_l1" in result["stage_routing_outcomes"]["L0"]["reason_codes"]


def test_l0_terminal_auxiliary_bucket_does_not_enter_ordinary_l1(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    routing_hints = {
        "no_early_stop_candidate": True,
        "need_text_semantic_candidate": False,
        "need_vision_candidate": False,
        "need_l2_candidate": False,
        "routing_reason_codes": ["specialized_surface_forbid_early_stop", "adult_surface_requires_text_semantic"],
    }
    specialized = {
        "possible_adult_lure": True,
        "specialized_fast_resolution_candidate": True,
    }
    monkeypatch.delenv(L1_DRAFT_ENV_VAR, raising=False)
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module(routing_hints, specialized))

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))

    assert result["stage_sequence"] == ["L0"]
    assert result["final_stage"] == "L0"
    assert result["routing_outcome"]["next_stage"] == "STOP"
    assert result["routing_outcome"]["outcome_kind"] == "l0_terminal_auxiliary_bucket"


def test_l0_terminal_auxiliary_bucket_does_not_run_l1_draft_when_enabled(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    routing_hints = {
        "need_text_semantic_candidate": False,
        "need_vision_candidate": False,
        "need_l2_candidate": False,
        "routing_reason_codes": ["specialized_surface_forbid_early_stop"],
    }
    specialized = {
        "possible_adult_lure": True,
        "specialized_fast_resolution_candidate": True,
    }

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("L1 draft runner must not run for L0 terminal samples")

    monkeypatch.setenv(L1_DRAFT_ENV_VAR, "1")
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module(routing_hints, specialized))
    monkeypatch.setattr("warden.runtime.l1_draft_bridge.run_l1_baseline_for_sample", fail_if_called)

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))
    trace = json.loads(Path(record["trace_path"]).read_text(encoding="utf-8"))

    assert result["stage_sequence"] == ["L0"]
    assert "debug_sidecars" not in result
    assert "debug_sidecars" not in trace


def test_non_terminal_l1_input_bundle_reuses_cheap_snapshot(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    output_dir = tmp_path / "out"
    monkeypatch.setenv(L1_DRAFT_ENV_VAR, "1")
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module({}))

    record = process_sample(sample_dir, output_dir)
    result = json.loads(Path(record["result_path"]).read_text(encoding="utf-8"))
    trace = json.loads(Path(record["trace_path"]).read_text(encoding="utf-8"))
    l1_contract = result["stage_trace"][1]["input_contract"]
    draft_result = trace["debug_sidecars"]["l1_draft"]["result"]

    assert result["stage_sequence"][:2] == ["L0", "L1"]
    assert l1_contract["cheap_snapshot_reused"] is True
    assert l1_contract["cheap_snapshot_schema_version"] == "cheap_evidence_snapshot_v1"
    assert draft_result["evidence_construction"]["mode"] == "incremental_from_cheap_snapshot"
    assert draft_result["evidence_construction"]["cheap_snapshot_reused"] is True


def test_cheap_snapshot_is_cached_on_context(monkeypatch, tmp_path):
    sample_dir = _make_runtime_sample(tmp_path / "sample")
    context = build_sample_context(sample_dir)
    calls = {"count": 0}

    def load_l0_module_once():
        calls["count"] += 1
        return _fake_l0_module({})

    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", load_l0_module_once)

    first = build_cheap_evidence_snapshot(context)
    second = build_cheap_evidence_snapshot(context)

    assert first is second
    assert context.cheap_snapshot is first
    assert context.cheap_evidence["schema_version"] == "cheap_evidence_snapshot_v1"
    assert calls["count"] == 1


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
    monkeypatch.setattr(runtime_pipeline, "_load_l0_module", lambda: _fake_l0_module({}))
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
        "reason_codes": draft["result"]["rule_router"]["reason_codes"],
        "rule_router": draft["result"]["rule_router"],
    }
    serialized = json.dumps(evidence_only, ensure_ascii=False)

    assert "manual_benign_label" not in serialized
    assert "T00" not in serialized
    assert "train" not in serialized
    assert "folder_label" not in serialized
