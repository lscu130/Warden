"""Rule-based joint-signal derivation for Warden L1 V1."""

from __future__ import annotations

from typing import Any, Dict


def build_joint_signals(
    *,
    url_features: Dict[str, Any],
    text_features: Dict[str, Any],
    html_features: Dict[str, Any],
    form_features: Dict[str, Any],
    network_features: Dict[str, Any],
    artifact_presence: Dict[str, Any],
    issues: list[Dict[str, str]],
) -> Dict[str, bool]:
    keyword_hits = text_features.get("keyword_hits_by_bucket") or {}
    html_text = str(html_features.get("html_actionable_text_compact") or "").lower()
    button_link_text = " ".join(
        list(html_features.get("button_texts_sample") or []) + list(html_features.get("link_texts_sample") or [])
    ).lower()
    combined_action_text = f"{html_text} {button_link_text}"

    login_surface = bool(form_features.get("has_password")) or "login" in combined_action_text or "sign in" in combined_action_text
    payment_surface = bool(form_features.get("has_card_hint")) or bool(keyword_hits.get("payment_checkout_billing"))
    wallet_surface = bool(form_features.get("has_wallet_hint")) or bool(keyword_hits.get("crypto_web3_wallet"))
    download_surface = bool(keyword_hits.get("download_install_app_extension")) or "download" in combined_action_text
    support_surface = bool(keyword_hits.get("support_contact_chat")) or "support" in combined_action_text
    sensitive_surface = any([login_surface, payment_surface, wallet_surface, download_surface])
    reward_context = bool(keyword_hits.get("reward_prize_airdrop"))
    security_context = bool(keyword_hits.get("security_verify_urgent"))
    financial_context = bool(keyword_hits.get("finance_banking") or keyword_hits.get("payment_checkout_billing"))
    off_domain = form_features.get("off_domain_form_action") is True
    html_sparse = int(html_features.get("html_actionable_node_count") or 0) < 2
    text_sparse = bool(text_features.get("text_sparse"))
    evidence_conflict = off_domain or bool(issues)
    need_ocr = (text_sparse or not text_features.get("visible_text_present")) and bool(artifact_presence.get("any_screenshot"))
    need_yolo = html_sparse and bool(artifact_presence.get("any_screenshot")) and sensitive_surface

    return {
        "text_sparse": text_sparse,
        "html_action_sparse": html_sparse,
        "sensitive_action_surface_present": sensitive_surface,
        "login_surface_present": login_surface,
        "payment_surface_present": payment_surface,
        "wallet_surface_present": wallet_surface,
        "download_surface_present": download_surface,
        "support_surface_present": support_surface,
        "reward_or_prize_context_present": reward_context,
        "security_or_urgency_context_present": security_context,
        "financial_context_present": financial_context,
        "brand_claim_candidate_present": bool(url_features.get("brand_token_candidate")),
        "hosted_platform_brand_shell_candidate": bool(
            url_features.get("hosted_platform_domain") and url_features.get("brand_token_candidate")
        ),
        "off_domain_submission_candidate": off_domain,
        "suspicious_download_candidate": download_surface and (security_context or bool(url_features.get("query_present"))),
        "evidence_conflict_candidate": evidence_conflict,
        "need_ocr_candidate": need_ocr,
        "need_yolo_candidate": need_yolo,
        "need_review_candidate": evidence_conflict or (sensitive_surface and text_sparse),
    }
