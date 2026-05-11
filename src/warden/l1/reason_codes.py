"""Reason-code generation for L1 draft results."""

from __future__ import annotations

from typing import Any, Dict, List


SIGNAL_TO_REASON = {
    "text_sparse": "text_sparse",
    "html_action_sparse": "html_action_sparse",
    "login_surface_present": "login_surface_present",
    "payment_surface_present": "payment_surface_present",
    "wallet_surface_present": "wallet_surface_present",
    "download_surface_present": "download_surface_present",
    "support_surface_present": "support_surface_present",
    "reward_or_prize_context_present": "reward_context_present",
    "financial_context_present": "financial_context_present",
    "security_or_urgency_context_present": "security_urgency_context_present",
    "off_domain_submission_candidate": "off_domain_form_action",
    "hosted_platform_brand_shell_candidate": "hosted_platform_brand_shell_candidate",
    "need_ocr_candidate": "need_ocr_for_text_recovery",
    "need_yolo_candidate": "need_yolo_for_ui_localization",
    "need_review_candidate": "need_review_for_conflict",
}


def generate_reason_codes(joint_signals: Dict[str, Any], text_features: Dict[str, Any], payload_observed: bool) -> List[str]:
    codes: List[str] = []
    if not text_features.get("visible_text_present"):
        codes.append("visible_text_missing")
    for signal, code in SIGNAL_TO_REASON.items():
        if joint_signals.get(signal):
            codes.append(code)
    if not payload_observed:
        codes.append("payload_not_observed")
    if text_features.get("text_very_sparse") and joint_signals.get("html_action_sparse"):
        codes.append("insufficient_evidence")
    if joint_signals.get("sensitive_action_surface_present") and not joint_signals.get("evidence_conflict_candidate"):
        codes.append("benign_hard_negative_candidate")
    return list(dict.fromkeys(codes))
