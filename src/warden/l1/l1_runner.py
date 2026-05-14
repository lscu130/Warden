"""End-to-end L1 evidence pack plus rule baseline runner."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .evidence_ledger import build_evidence_ledger
from .evidence_pack import build_evidence_pack
from .explanation_renderer import render_explanation
from .form_features import extract_form_features
from .html_action_extractor import extract_actionable_html_features
from .joint_signals import build_joint_signals
from .network_features import extract_network_features
from .reason_codes import generate_reason_codes
from .rule_baseline import run_rule_baseline
from .text_features import extract_visible_text_features
from .url_features import extract_url_features


def run_l1_baseline_for_sample(source: Any, *, cheap_snapshot: Any = None) -> Dict[str, Any]:
    pack = build_evidence_pack(source, cheap_snapshot=cheap_snapshot)
    url_features = extract_url_features(pack.get("url_info"))
    final_host = str(url_features.get("final_host") or "")
    text_features = extract_visible_text_features(str(pack.get("visible_text") or ""))
    html_features = extract_actionable_html_features(
        str(pack.get("html_text") or ""),
        base_host=final_host,
        html_truncated=bool(pack.get("html_truncated")),
    )
    form_features = extract_form_features(pack.get("forms_payload"), final_host=final_host)
    network_features = extract_network_features(pack.get("net_summary"), final_host=final_host)
    joint_signals = build_joint_signals(
        url_features=url_features,
        text_features=text_features,
        html_features=html_features,
        form_features=form_features,
        network_features=network_features,
        artifact_presence=pack.get("artifact_presence") or {},
        issues=pack.get("issues") or [],
    )
    payload_observed = bool(
        form_features.get("has_password")
        or form_features.get("has_card_hint")
        or form_features.get("has_wallet_hint")
        or network_features.get("post_targets")
    )
    reason_codes = generate_reason_codes(joint_signals, text_features, payload_observed)
    baseline = run_rule_baseline(
        url_features=url_features,
        text_features=text_features,
        html_features=html_features,
        form_features=form_features,
        network_features=network_features,
        joint_signals=joint_signals,
        reason_codes=reason_codes,
    )
    ledger = build_evidence_ledger(
        artifact_presence=pack.get("artifact_presence") or {},
        issues=pack.get("issues") or [],
        url_features=url_features,
        text_features=text_features,
        html_features=html_features,
        form_features=form_features,
        network_features=network_features,
        joint_signals=joint_signals,
        reason_codes=reason_codes,
    )
    explanation = render_explanation(
        rule_assessment=baseline["rule_assessment"],
        routing_hints=baseline["routing_hints"],
        risk_hints=baseline["risk_hints"],
        evidence_sufficiency=baseline["evidence_sufficiency"],
        reason_codes=reason_codes,
        evidence_ledger=ledger,
        routing=baseline["routing_hints"],
    )
    return {
        "result_kind": "warden_l1_routing_diagnostic_draft_v1",
        "stage": "L1",
        "draft": True,
        "not_final_schema": True,
        "evidence_construction": {
            "mode": pack.get("evidence_construction_mode"),
            "cheap_snapshot_reused": bool(pack.get("cheap_snapshot_reused")),
            "cheap_snapshot_schema_version": pack.get("cheap_snapshot_schema_version"),
        },
        "sample_dir": pack["sample_dir"],
        "rule_router": {
            "rule_assessment": baseline["rule_assessment"],
            "routing_assessment": baseline["routing_assessment"],
            "routing_hints": baseline["routing_hints"],
            "risk_hints": baseline["risk_hints"],
            "evidence_sufficiency": baseline["evidence_sufficiency"],
            "risk_axes": baseline["risk_axes"],
            "reason_codes": reason_codes,
        },
        "text_semantic_concepts": {
            "status": "stub_not_run",
            "reason": "real_text_tower_not_available_yet",
            "concept_outputs": {},
        },
        "vision_evidence": {
            "status": "requested_but_stub_not_run"
            if baseline["routing_hints"].get("need_ocr") or baseline["routing_hints"].get("need_yolo")
            else "not_requested_or_stub",
            "need_ocr": bool(baseline["routing_hints"].get("need_ocr")),
            "need_yolo": bool(baseline["routing_hints"].get("need_yolo")),
            "ocr_ran": False,
            "yolo_ran": False,
        },
        "decision_head": {
            "status": "not_run",
            "reason": "real_text_tower_and_l1_decision_head_not_available_yet",
            "final_label": None,
            "risk_score": None,
            "confidence": None,
            "malicious_basis": None,
            "payload_observed": None,
        },
        "evidence_ledger": ledger,
        "explanation": explanation,
        "features": {
            "url": url_features,
            "visible_text": text_features,
            "html_actionable": html_features,
            "forms": form_features,
            "network": network_features,
            "joint_signals": joint_signals,
        },
        "artifact_presence": pack.get("artifact_presence") or {},
        "missing_artifacts": pack.get("missing_artifacts") or [],
        "issues": pack.get("issues") or [],
    }


def run_l1_baseline_for_manifest_row(row: Dict[str, Any]) -> Dict[str, Any]:
    current_path = row.get("current_path")
    if not current_path:
        raise ValueError("manifest row is missing current_path")
    return run_l1_baseline_for_sample(Path(str(current_path)))
