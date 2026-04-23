"""Execution-ready runtime/dataflow skeleton for Warden V0.1."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

from scripts.data.common.io_utils import discover_sample_dirs, ensure_dir, now_utc_iso, write_json

from .core import ArtifactPackage, SampleContext, StageResult

MAX_TEXT_SCAN_CHARS = 120_000
MAX_HTML_SCAN_CHARS = 600_000


def _load_l0_module():
    auto_module = importlib.import_module("scripts.labeling.Warden_auto_label_utils_brandlex")
    sys.modules.setdefault("Warden_auto_label_utils_brandlex", auto_module)
    return importlib.import_module("warden.module.l0")


def build_sample_context(sample_dir: Path) -> SampleContext:
    artifacts = ArtifactPackage.from_sample_dir(sample_dir)
    meta = artifacts.read_json_optional("meta.json", {})
    url_info = artifacts.read_json_optional("url.json", {})
    sample_id = str(meta.get("sample_id") or artifacts.sample_dir.name)
    return SampleContext(
        artifacts=artifacts,
        sample_id=sample_id,
        input_url=str(url_info.get("input_url") or ""),
        final_url=str(url_info.get("final_url") or ""),
        page_title=str(meta.get("page_title") or ""),
        label_hint=str(meta.get("label") or ""),
    )


def _make_routing_outcome(*, stage: str, status: str, next_stage: str, reason_codes: List[str], outcome_kind: str) -> Dict[str, Any]:
    return {
        "routing_contract_version": "warden_routing_outcome_v0_1",
        "stage": stage,
        "stage_status": status,
        "next_stage": next_stage,
        "outcome_kind": outcome_kind,
        "reached_terminal_state": next_stage == "STOP",
        "reason_codes": list(reason_codes),
    }


def _present_artifacts(artifact_presence: Dict[str, bool], artifact_names: List[str]) -> List[str]:
    return [name for name in artifact_names if artifact_presence.get(name)]


def _missing_artifacts(artifact_presence: Dict[str, bool], artifact_names: List[str]) -> List[str]:
    return [name for name in artifact_names if not artifact_presence.get(name)]


def build_l1_input_bundle(context: SampleContext, previous: StageResult | None) -> Dict[str, Any]:
    evidence = prepare_shared_evidence(context)
    artifact_presence = evidence.get("artifact_presence") or {}
    prior_outputs = previous.outputs if previous else {}
    l0_routing_hints = prior_outputs.get("l0_routing_hints") or {}
    required_heavy_artifacts: List[str] = []
    if l0_routing_hints.get("need_text_semantic_candidate"):
        required_heavy_artifacts.append("html_rendered")
    if l0_routing_hints.get("need_vision_candidate"):
        required_heavy_artifacts.append("screenshot_viewport_png")

    required_cheap_families = [
        "sample_identity",
        "url_info",
        "url_features",
        "raw_visible_text",
        "visible_text",
        "forms_summary",
        "net_features",
        "html_features",
        "artifact_presence",
    ]
    if evidence.get("auto_labels"):
        required_cheap_families.append("auto_labels")
    if evidence.get("diff_summary") is not None:
        required_cheap_families.append("diff_summary")

    return {
        "contract_name": "l1_main_judgment_input_bundle_v0_1",
        "sample_identity": {
            "sample_id": context.sample_id,
            "input_url": context.input_url,
            "final_url": context.final_url,
        },
        "routing_context": {
            "incoming_stage": previous.stage if previous else "L0",
            "incoming_stage_status": previous.status if previous else "unknown",
            "incoming_routing_outcome": previous.routing_outcome if previous else {},
            "incoming_reason_codes": list(previous.reason_codes) if previous else [],
            "page_stage_candidate": prior_outputs.get("page_stage_candidate"),
            "risk_level_weak": (prior_outputs.get("risk_outputs") or {}).get("risk_level_weak"),
        },
        "required_cheap_families": required_cheap_families,
        "required_heavy_artifacts": required_heavy_artifacts,
        "present_required_heavy_artifacts": _present_artifacts(artifact_presence, required_heavy_artifacts),
        "missing_required_heavy_artifacts": _missing_artifacts(artifact_presence, required_heavy_artifacts),
        "observability_summary": {
            "visible_text_len": len(str(evidence.get("visible_text") or "")),
            "raw_visible_text_len": len(str(evidence.get("raw_visible_text") or "")),
            "has_auto_labels": bool(evidence.get("auto_labels")),
            "has_diff_summary": evidence.get("diff_summary") is not None,
            "has_net_summary": bool(evidence.get("net_summary")),
        },
        "judgment_focus": {
            "text_semantic_required": bool(l0_routing_hints.get("need_text_semantic_candidate")),
            "vision_followup_required": bool(l0_routing_hints.get("need_vision_candidate")),
            "high_cost_escalation_hint": bool(l0_routing_hints.get("need_l2_candidate")),
        },
    }


def build_l2_review_contract(context: SampleContext, previous: StageResult | None) -> Dict[str, Any]:
    evidence = prepare_shared_evidence(context)
    artifact_presence = evidence.get("artifact_presence") or {}
    prior_outputs = previous.outputs if previous else {}
    required_heavy_artifacts = ["html_raw", "screenshot_viewport_png"]
    review_targets: List[str] = ["preserve_escalation_context", "emit_high_cost_review_placeholder"]
    if (prior_outputs.get("evasion_signals") or {}).get("anti_bot_or_cloaking_candidate"):
        review_targets.append("inspect_evasion_or_cloaking_surface")
    if (prior_outputs.get("l0_routing_hints") or {}).get("need_l2_candidate"):
        review_targets.append("inspect_high_risk_delivery_or_specialized_surface")

    return {
        "contract_name": "l2_high_cost_review_contract_v0_1",
        "sample_identity": {
            "sample_id": context.sample_id,
            "input_url": context.input_url,
            "final_url": context.final_url,
        },
        "escalation_context": {
            "incoming_stage": previous.stage if previous else "L1",
            "incoming_stage_status": previous.status if previous else "unknown",
            "incoming_routing_outcome": previous.routing_outcome if previous else {},
            "incoming_reason_codes": list(previous.reason_codes) if previous else [],
        },
        "required_cheap_families": [
            "sample_identity",
            "artifact_presence",
            "url_features",
            "forms_summary",
            "net_features",
            "auto_labels",
            "l0_and_l1_trace_context",
        ],
        "required_heavy_artifacts": required_heavy_artifacts,
        "present_required_heavy_artifacts": _present_artifacts(artifact_presence, required_heavy_artifacts),
        "missing_required_heavy_artifacts": _missing_artifacts(artifact_presence, required_heavy_artifacts),
        "review_targets": review_targets,
        "output_contract": {
            "must_preserve_escalation_reason_codes": True,
            "must_emit_review_mode": True,
            "must_keep_routing_vs_final_judgment_distinct": True,
        },
    }


def load_html_rendered_text(context: SampleContext) -> str:
    cached = context.get_heavy("html_rendered_text")
    if cached is not None:
        return cached
    return context.cache_heavy(
        "html_rendered_text",
        context.artifacts.read_html_payload_optional("html_rendered.json", max_chars=MAX_HTML_SCAN_CHARS),
    )


def load_html_raw_text(context: SampleContext) -> str:
    cached = context.get_heavy("html_raw_text")
    if cached is not None:
        return cached
    return context.cache_heavy(
        "html_raw_text",
        context.artifacts.read_html_payload_optional("html_raw.json", max_chars=MAX_HTML_SCAN_CHARS),
    )


def load_viewport_screenshot_bytes(context: SampleContext) -> bytes:
    cached = context.get_heavy("viewport_screenshot_bytes")
    if cached is not None:
        return cached
    return context.cache_heavy(
        "viewport_screenshot_bytes",
        context.artifacts.read_bytes_optional("screenshot_viewport.png"),
    )


def prepare_shared_evidence(context: SampleContext) -> Dict[str, Any]:
    if context.cheap_evidence:
        return context.cheap_evidence

    l0_module = _load_l0_module()
    meta = context.artifacts.read_json_optional("meta.json", {})
    url_info = context.artifacts.read_json_optional("url.json", {})
    forms = context.artifacts.read_json_optional("forms.json", {"forms": []})
    net_summary = context.artifacts.read_json_optional("net_summary.json", {})
    diff_summary = context.artifacts.read_json_optional("diff_summary.json", None)
    auto_labels = context.artifacts.read_json_optional("auto_labels.json", {})
    visible_text = context.artifacts.read_text_optional("visible_text.txt", max_chars=MAX_TEXT_SCAN_CHARS)

    l0_prepared = l0_module.prepare_l0_inputs(
        input_url=str(url_info.get("input_url") or ""),
        final_url=str(url_info.get("final_url") or ""),
        visible_text=visible_text,
        forms_json=forms,
        net_summary=net_summary,
        html_rendered="",
        html_raw="",
        page_title=str(meta.get("page_title") or ""),
    )

    context.input_url = str(l0_prepared["input_url"] or context.input_url)
    context.final_url = str(l0_prepared["final_url"] or context.final_url)
    context.page_title = str(meta.get("page_title") or context.page_title)
    context.label_hint = str(meta.get("label") or context.label_hint)

    context.cheap_evidence = {
        "prepared_at_utc": now_utc_iso(),
        "artifact_presence": context.artifacts.artifact_presence(),
        "meta": meta,
        "url_info": url_info,
        "forms_payload": forms,
        "net_summary": net_summary,
        "diff_summary": diff_summary,
        "auto_labels": auto_labels,
        "raw_visible_text": l0_prepared["raw_visible_text"],
        "visible_text": l0_prepared["visible_text"],
        "url_features": l0_prepared["url_features"],
        "forms_summary": l0_prepared["forms_summary"],
        "net_features": l0_prepared["net_features"],
        "html_features": l0_prepared["html_features"],
    }
    return context.cheap_evidence


def run_l0_stage(context: SampleContext) -> StageResult:
    evidence = prepare_shared_evidence(context)
    l0_module = _load_l0_module()
    auto_labels = evidence.get("auto_labels") or {}
    brand_signals = auto_labels.get("brand_signals") or {
        "brand_claim_present_candidate": False,
        "claimed_brands": [],
        "brand_claim_source": "none",
        "text_brand_candidates": [],
        "url_brand_candidates": [],
        "domain_brand_consistency_candidate": "no_brand_claim",
        "brand_token_in_url": [],
    }

    l0_outputs = l0_module.derive_l0_outputs(
        final_url=context.final_url,
        visible_text=str(evidence.get("visible_text") or ""),
        raw_visible_text=str(evidence.get("raw_visible_text") or ""),
        page_title=context.page_title,
        forms_summary=evidence.get("forms_summary") or {},
        net_features=evidence.get("net_features") or {},
        html_features=evidence.get("html_features") or {},
        diff_summary=evidence.get("diff_summary"),
        brand_signals=brand_signals,
        url_features=evidence.get("url_features") or {},
    )

    routing = l0_outputs.get("l0_routing_hints") or {}
    reason_codes = list(routing.get("routing_reason_codes") or [])
    if routing.get("need_l2_candidate"):
        next_stage = "L2"
        status = "escalate"
        outcome_kind = "escalate_to_l2"
    elif routing.get("need_text_semantic_candidate") or routing.get("need_vision_candidate") or routing.get("no_early_stop_candidate"):
        next_stage = "L1"
        status = "escalate"
        outcome_kind = "escalate_to_l1"
    else:
        next_stage = "STOP"
        status = "stop"
        outcome_kind = "l0_stop"

    routing_outcome = _make_routing_outcome(
        stage="L0",
        status=status,
        next_stage=next_stage,
        reason_codes=reason_codes,
        outcome_kind=outcome_kind,
    )

    result = StageResult(
        stage="L0",
        status=status,
        next_stage=next_stage,
        reason_codes=reason_codes,
        routing_outcome=routing_outcome,
        input_contract={
            "contract_name": "l0_runtime_observation_input_bundle_v0_1",
            "required_cheap_families": [
                "sample_identity",
                "url_info",
                "visible_text",
                "forms_payload",
                "net_summary",
                "artifact_presence",
            ],
            "required_heavy_artifacts": [],
        },
        requested_heavy_artifacts=[],
        outputs={
            "page_stage_candidate": l0_outputs.get("page_stage_candidate"),
            "language_candidate": l0_outputs.get("language_candidate"),
            "risk_outputs": l0_outputs.get("risk_outputs") or {},
            "intent_signals": l0_outputs.get("intent_signals") or {},
            "evasion_signals": l0_outputs.get("evasion_signals") or {},
            "specialized_surface_signals": l0_outputs.get("specialized_surface_signals") or {},
            "l0_routing_hints": routing,
        },
    )
    return context.append_stage(result)


def run_l1_stage(context: SampleContext) -> StageResult:
    evidence = prepare_shared_evidence(context)
    previous = context.stage_trace[-1] if context.stage_trace else None
    previous_outputs = previous.outputs if previous else {}
    input_bundle = build_l1_input_bundle(context, previous)
    requested_heavy_artifacts = list(input_bundle.get("required_heavy_artifacts") or [])
    html_rendered_text = ""
    html_loaded = False
    screenshot_loaded = False

    if previous_outputs.get("l0_routing_hints", {}).get("need_text_semantic_candidate"):
        html_rendered_text = load_html_rendered_text(context)
        html_loaded = bool(html_rendered_text)

    if previous_outputs.get("l0_routing_hints", {}).get("need_vision_candidate"):
        screenshot_loaded = bool(load_viewport_screenshot_bytes(context))

    evasion_signals = previous_outputs.get("evasion_signals") or {}
    need_l2 = bool(previous_outputs.get("l0_routing_hints", {}).get("need_l2_candidate")) or bool(
        evasion_signals.get("anti_bot_or_cloaking_candidate")
    )
    if need_l2:
        next_stage = "L2"
        status = "escalate"
        reason_codes = ["l1_escalation_required"]
        outcome_kind = "escalate_to_l2"
    else:
        next_stage = "STOP"
        status = "complete"
        reason_codes = ["l1_placeholder_complete"]
        outcome_kind = "l1_complete"

    routing_outcome = _make_routing_outcome(
        stage="L1",
        status=status,
        next_stage=next_stage,
        reason_codes=reason_codes,
        outcome_kind=outcome_kind,
    )

    result = StageResult(
        stage="L1",
        status=status,
        next_stage=next_stage,
        reason_codes=reason_codes,
        routing_outcome=routing_outcome,
        input_contract=input_bundle,
        requested_heavy_artifacts=requested_heavy_artifacts,
        outputs={
            "judgment_mode": "placeholder_main_judgment_shell",
            "visible_text_len": len(str(evidence.get("visible_text") or "")),
            "html_rendered_loaded": html_loaded,
            "html_rendered_len": len(html_rendered_text),
            "viewport_screenshot_loaded": screenshot_loaded,
            "brand_claims": (evidence.get("auto_labels") or {}).get("brand_signals", {}).get("claimed_brands", []),
            "input_bundle_contract_name": input_bundle.get("contract_name"),
            "loaded_heavy_artifacts": [
                name
                for name, loaded in [
                    ("html_rendered", html_loaded),
                    ("screenshot_viewport_png", screenshot_loaded),
                ]
                if loaded
            ],
        },
    )
    return context.append_stage(result)


def run_l2_stage(context: SampleContext) -> StageResult:
    previous = context.stage_trace[-1] if context.stage_trace else None
    review_contract = build_l2_review_contract(context, previous)
    requested_heavy_artifacts = list(review_contract.get("required_heavy_artifacts") or [])
    html_raw_text = load_html_raw_text(context)
    screenshot_loaded = bool(load_viewport_screenshot_bytes(context))
    routing_outcome = _make_routing_outcome(
        stage="L2",
        status="complete",
        next_stage="STOP",
        reason_codes=["l2_placeholder_review_complete"],
        outcome_kind="l2_complete",
    )
    result = StageResult(
        stage="L2",
        status="complete",
        next_stage="STOP",
        reason_codes=["l2_placeholder_review_complete"],
        routing_outcome=routing_outcome,
        input_contract=review_contract,
        requested_heavy_artifacts=requested_heavy_artifacts,
        outputs={
            "review_mode": "placeholder_high_cost_review_shell",
            "html_raw_loaded": bool(html_raw_text),
            "html_raw_len": len(html_raw_text),
            "viewport_screenshot_loaded": screenshot_loaded,
            "review_contract_name": review_contract.get("contract_name"),
            "loaded_heavy_artifacts": [
                name
                for name, loaded in [
                    ("html_raw", bool(html_raw_text)),
                    ("screenshot_viewport_png", screenshot_loaded),
                ]
                if loaded
            ],
        },
    )
    return context.append_stage(result)


def build_result_payload(context: SampleContext) -> Dict[str, Any]:
    final_entry = context.stage_trace[-1] if context.stage_trace else None
    final_stage = final_entry.stage if final_entry else "none"
    terminal_routing = final_entry.next_stage if final_entry else "STOP"
    final_routing_outcome = final_entry.routing_outcome if final_entry else {}
    return {
        "schema_version": "warden_runtime_result_v0_2",
        "generated_at_utc": now_utc_iso(),
        "sample_id": context.sample_id,
        "sample_dir": str(context.artifacts.sample_dir),
        "input_url": context.input_url,
        "final_url": context.final_url,
        "page_title": context.page_title,
        "label_hint": context.label_hint,
        "final_stage": final_stage,
        "terminal_routing": terminal_routing,
        "routing_outcome": final_routing_outcome,
        "stage_sequence": [item.stage for item in context.stage_trace],
        "stage_status_map": {item.stage: item.status for item in context.stage_trace},
        "stage_routing_outcomes": {item.stage: item.routing_outcome for item in context.stage_trace},
        "result_contract": {
            "contract_name": "warden_runtime_result_contract_v0_1",
            "keeps_routing_distinct_from_final_judgment": True,
            "includes_stage_trace": True,
            "includes_terminal_routing_outcome": True,
        },
        "artifact_presence": context.artifacts.artifact_presence(),
        "runtime_notes": list(context.runtime_notes),
        "stage_trace": [item.to_dict() for item in context.stage_trace],
    }


def process_sample(sample_dir: Path, output_dir: Path) -> Dict[str, Any]:
    context = build_sample_context(sample_dir)
    run_l0_stage(context)
    if context.stage_trace[-1].next_stage == "L1":
        run_l1_stage(context)
    elif context.stage_trace[-1].next_stage == "L2":
        run_l2_stage(context)

    if context.stage_trace and context.stage_trace[-1].next_stage == "L2":
        run_l2_stage(context)

    sample_output_dir = ensure_dir(output_dir / context.sample_id)
    result_payload = build_result_payload(context)
    trace_payload = {
        "schema_version": "warden_runtime_trace_v0_2",
        "generated_at_utc": now_utc_iso(),
        "sample_id": context.sample_id,
        "sample_dir": str(context.artifacts.sample_dir),
        "trace_contract": {
            "contract_name": "warden_runtime_trace_contract_v0_1",
            "includes_stage_input_contracts": True,
            "includes_requested_heavy_artifacts": True,
            "includes_routing_outcomes": True,
        },
        "routing_outcome_history": [item.routing_outcome for item in context.stage_trace],
        "stage_trace": [item.to_dict() for item in context.stage_trace],
        "heavy_cache_keys_before_release": sorted(context.heavy_cache.keys()),
    }

    write_json(sample_output_dir / "runtime_result.json", result_payload)
    write_json(sample_output_dir / "runtime_trace.json", trace_payload)

    released = context.release_heavy_cache()
    result_payload["released_heavy_cache_entries"] = released
    write_json(sample_output_dir / "runtime_result.json", result_payload)
    return {
        "sample_id": context.sample_id,
        "sample_dir": str(context.artifacts.sample_dir),
        "result_path": str((sample_output_dir / "runtime_result.json").resolve()),
        "trace_path": str((sample_output_dir / "runtime_trace.json").resolve()),
        "released_heavy_cache_entries": released,
        "final_stage": result_payload["final_stage"],
    }


def process_samples(roots: Iterable[Path], output_dir: Path, limit: int = 0) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for index, sample_dir in enumerate(discover_sample_dirs(roots), 1):
        records.append(process_sample(sample_dir=sample_dir, output_dir=output_dir))
        if limit > 0 and index >= limit:
            break
    return records
