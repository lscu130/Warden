"""Conservative replaceable rule baseline for internal L1 draft output."""

from __future__ import annotations

from typing import Any, Dict, List


def _risk_axes(signals: Dict[str, Any]) -> List[str]:
    axes: List[str] = []
    if signals.get("security_or_urgency_context_present") or signals.get("reward_or_prize_context_present"):
        axes.append("deceptive_identity_risk")
    if signals.get("sensitive_action_surface_present"):
        axes.append("observed_action_risk")
    if signals.get("off_domain_submission_candidate"):
        axes.append("payload_deployment_risk")
    if signals.get("hosted_platform_brand_shell_candidate"):
        axes.append("brand_domain_conflict_risk")
    if signals.get("text_sparse") or signals.get("html_action_sparse"):
        axes.append("evidence_incompleteness_risk")
    return axes or ["low_observed_risk"]


def run_rule_baseline(
    *,
    url_features: Dict[str, Any],
    text_features: Dict[str, Any],
    html_features: Dict[str, Any],
    form_features: Dict[str, Any],
    network_features: Dict[str, Any],
    joint_signals: Dict[str, Any],
    reason_codes: List[str],
) -> Dict[str, Any]:
    risk_score = int(url_features.get("url_suspicion_basic_score") or 0)
    if joint_signals.get("login_surface_present"):
        risk_score += 15
    if joint_signals.get("payment_surface_present") or joint_signals.get("wallet_surface_present"):
        risk_score += 25
    if joint_signals.get("download_surface_present"):
        risk_score += 15
    if joint_signals.get("security_or_urgency_context_present") or joint_signals.get("reward_or_prize_context_present"):
        risk_score += 20
    if joint_signals.get("off_domain_submission_candidate"):
        risk_score += 25
    if joint_signals.get("hosted_platform_brand_shell_candidate"):
        risk_score += 15
    if "insufficient_evidence" in reason_codes:
        risk_score = max(risk_score, 20)
    risk_score = min(risk_score, 100)

    payload_observed = bool(
        form_features.get("has_password")
        or form_features.get("has_card_hint")
        or form_features.get("has_wallet_hint")
        or network_features.get("post_targets")
    )
    high_risk_context = bool(
        joint_signals.get("security_or_urgency_context_present")
        or joint_signals.get("reward_or_prize_context_present")
        or joint_signals.get("financial_context_present")
        or joint_signals.get("off_domain_submission_candidate")
    )
    if risk_score >= 70 and joint_signals.get("sensitive_action_surface_present") and high_risk_context:
        label = "malicious"
        confidence = 0.7
    elif risk_score >= 35 or joint_signals.get("need_review_candidate"):
        label = "suspicious"
        confidence = 0.55
    elif "insufficient_evidence" in reason_codes:
        label = "unknown"
        confidence = 0.35
    else:
        label = "benign"
        confidence = 0.5

    if label == "malicious" and payload_observed and high_risk_context:
        malicious_basis = "both_behavior_and_action_observed"
    elif label == "malicious" and high_risk_context:
        malicious_basis = "high_risk_behavior_observed"
    elif label in {"suspicious", "unknown"} and "insufficient_evidence" in reason_codes:
        malicious_basis = "insufficient_evidence"
    elif payload_observed:
        malicious_basis = "high_risk_action_surface_observed"
    else:
        malicious_basis = "no_malicious_evidence_observed"

    if joint_signals.get("wallet_surface_present"):
        page_role = "wallet_drain_or_web3_abuse_page"
    elif joint_signals.get("payment_surface_present"):
        page_role = "payment_collection_page"
    elif joint_signals.get("login_surface_present"):
        page_role = "credential_collection_page"
    elif joint_signals.get("download_surface_present"):
        page_role = "fake_download_lure_page"
    elif joint_signals.get("support_surface_present"):
        page_role = "fake_support_page"
    elif label == "benign":
        page_role = "benign_clear"
    else:
        page_role = "unknown"

    routing = {
        "need_ocr_candidate": bool(joint_signals.get("need_ocr_candidate")),
        "need_yolo_candidate": bool(joint_signals.get("need_yolo_candidate")),
        "need_review_candidate": bool(joint_signals.get("need_review_candidate")),
    }
    return {
        "label": label,
        "risk_score": risk_score,
        "confidence": confidence,
        "malicious_basis": malicious_basis,
        "payload_observed": payload_observed,
        "page_role": page_role,
        "risk_axes": _risk_axes(joint_signals),
        "routing": routing,
    }
