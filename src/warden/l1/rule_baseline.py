"""Rule router and evidence-sufficiency diagnostics for internal L1 draft output."""

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
    rule_signal_score = int(url_features.get("url_suspicion_basic_score") or 0)
    if joint_signals.get("login_surface_present"):
        rule_signal_score += 15
    if joint_signals.get("payment_surface_present") or joint_signals.get("wallet_surface_present"):
        rule_signal_score += 25
    if joint_signals.get("download_surface_present"):
        rule_signal_score += 15
    if joint_signals.get("security_or_urgency_context_present") or joint_signals.get("reward_or_prize_context_present"):
        rule_signal_score += 20
    if joint_signals.get("off_domain_submission_candidate"):
        rule_signal_score += 25
    if joint_signals.get("hosted_platform_brand_shell_candidate"):
        rule_signal_score += 15
    if "insufficient_evidence" in reason_codes:
        rule_signal_score = max(rule_signal_score, 20)
    rule_signal_score = min(rule_signal_score, 100)

    action_surface_present = bool(joint_signals.get("sensitive_action_surface_present"))
    behavior_context_hint_present = bool(
        joint_signals.get("security_or_urgency_context_present")
        or joint_signals.get("reward_or_prize_context_present")
        or joint_signals.get("financial_context_present")
        or joint_signals.get("hosted_platform_brand_shell_candidate")
    )
    relation_conflict_hint_present = bool(
        joint_signals.get("off_domain_submission_candidate") or joint_signals.get("evidence_conflict_candidate")
    )
    payload_surface_observed = bool(
        form_features.get("has_password")
        or form_features.get("has_card_hint")
        or form_features.get("has_wallet_hint")
        or network_features.get("post_targets")
    )

    visible_text_status = "sufficient"
    if not text_features.get("visible_text_present"):
        visible_text_status = "missing"
    elif text_features.get("text_sparse"):
        visible_text_status = "sparse"

    html_action_status = "sufficient"
    if int(html_features.get("html_actionable_node_count") or 0) == 0:
        html_action_status = "missing"
    elif joint_signals.get("html_action_sparse"):
        html_action_status = "sparse"

    needs_visual_recovery = bool(joint_signals.get("need_ocr_candidate") or joint_signals.get("need_yolo_candidate"))
    insufficient_observability = bool(visible_text_status == "missing" and html_action_status == "missing")
    strong_malicious_rule_hit = bool(
        action_surface_present
        and (relation_conflict_hint_present or behavior_context_hint_present)
        and rule_signal_score >= 70
    )
    high_risk_candidate = strong_malicious_rule_hit
    low_risk_candidate = bool(
        not action_surface_present
        and not behavior_context_hint_present
        and not relation_conflict_hint_present
        and visible_text_status == "sufficient"
        and html_action_status == "sufficient"
    )
    benign_hard_negative_candidate = bool(
        action_surface_present and not behavior_context_hint_present and not relation_conflict_hint_present
    )

    routing_hints = {
        "need_text_tower": bool(
            action_surface_present
            or behavior_context_hint_present
            or relation_conflict_hint_present
            or not low_risk_candidate
        ),
        "need_ocr": bool(joint_signals.get("need_ocr_candidate")),
        "need_yolo": bool(joint_signals.get("need_yolo_candidate")),
        "need_review": bool(joint_signals.get("need_review_candidate") or high_risk_candidate or insufficient_observability),
    }
    risk_hints = {
        "action_surface_present": action_surface_present,
        "payload_surface_observed": payload_surface_observed,
        "behavior_context_hint_present": behavior_context_hint_present,
        "relation_conflict_hint_present": relation_conflict_hint_present,
        "strong_malicious_rule_hit": strong_malicious_rule_hit,
        "high_risk_candidate": high_risk_candidate,
        "low_risk_candidate": low_risk_candidate,
        "benign_hard_negative_candidate": benign_hard_negative_candidate,
        "rule_signal_score": rule_signal_score,
    }
    evidence_sufficiency = {
        "visible_text_status": visible_text_status,
        "html_action_status": html_action_status,
        "needs_visual_recovery": needs_visual_recovery,
        "insufficient_observability": insufficient_observability,
    }

    if "insufficient_evidence" in reason_codes:
        rule_assessment = "insufficient_evidence"
    elif insufficient_observability:
        rule_assessment = "insufficient_observability"
    elif high_risk_candidate:
        rule_assessment = "high_risk_candidate"
    elif routing_hints["need_review"]:
        rule_assessment = "needs_review"
    elif needs_visual_recovery:
        rule_assessment = "needs_vision_evidence"
    elif benign_hard_negative_candidate:
        rule_assessment = "benign_hard_negative_candidate"
    elif visible_text_status == "sparse":
        rule_assessment = "text_sparse"
    elif html_action_status == "sparse":
        rule_assessment = "html_action_sparse"
    elif routing_hints["need_text_tower"]:
        rule_assessment = "needs_text_model_judgment"
    elif low_risk_candidate:
        rule_assessment = "low_risk_candidate"
    else:
        rule_assessment = "text_sufficient"

    if routing_hints["need_review"]:
        routing_assessment = "route_to_review"
    elif routing_hints["need_ocr"] or routing_hints["need_yolo"]:
        routing_assessment = "route_to_visual_evidence_recovery"
    elif routing_hints["need_text_tower"]:
        routing_assessment = "route_to_text_tower"
    else:
        routing_assessment = "no_additional_route"

    return {
        "rule_assessment": rule_assessment,
        "routing_assessment": routing_assessment,
        "routing_hints": routing_hints,
        "risk_hints": risk_hints,
        "evidence_sufficiency": evidence_sufficiency,
        "risk_axes": _risk_axes(joint_signals),
        "reason_codes": list(reason_codes),
    }
