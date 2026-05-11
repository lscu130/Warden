"""Evidence ledger construction for deterministic L1 explanations."""

from __future__ import annotations

from typing import Any, Dict, List


def _entry(index: int, source: str, claim: str, value: Any, stance: str, reason_code: str, confidence: float | None = None) -> Dict[str, Any]:
    return {
        "evidence_id": f"l1ev_{index:04d}",
        "source": source,
        "claim": claim,
        "value": value,
        "confidence": confidence,
        "stance": stance,
        "reason_code": reason_code,
    }


def build_evidence_ledger(
    *,
    artifact_presence: Dict[str, Any],
    issues: list[Dict[str, str]],
    url_features: Dict[str, Any],
    text_features: Dict[str, Any],
    html_features: Dict[str, Any],
    form_features: Dict[str, Any],
    network_features: Dict[str, Any],
    joint_signals: Dict[str, Any],
    reason_codes: List[str],
) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []

    def add(source: str, claim: str, value: Any, stance: str, reason_code: str, confidence: float | None = None) -> None:
        entries.append(_entry(len(entries) + 1, source, claim, value, stance, reason_code, confidence))

    if text_features.get("visible_text_present"):
        add("visible_text", "visible text is available", text_features.get("effective_visible_text_chars"), "supports", "text_available", 0.8)
    else:
        add("artifact_presence", "visible text missing", True, "limits", "visible_text_missing", None)
    if text_features.get("text_sparse"):
        add("visible_text", "visible text is sparse", text_features.get("effective_visible_text_chars"), "limits", "text_sparse", 0.8)
    if html_features.get("html_actionable_node_count"):
        add("html_actionable", "actionable HTML nodes extracted", html_features.get("html_actionable_node_count"), "supports", "html_actionable_present", 0.8)
    elif joint_signals.get("html_action_sparse"):
        add("html_actionable", "actionable HTML is sparse", html_features.get("html_actionable_node_count"), "limits", "html_action_sparse", 0.7)
    if form_features.get("has_password"):
        add("forms", "password input surface observed", True, "supports", "login_surface_present", 0.9)
    if form_features.get("has_card_hint"):
        add("forms", "payment input hint observed", True, "supports", "payment_surface_present", 0.8)
    if form_features.get("has_wallet_hint"):
        add("forms", "wallet-related input hint observed", True, "supports", "wallet_surface_present", 0.8)
    if form_features.get("off_domain_form_action") is True:
        add("forms", "form action targets off-domain host", form_features.get("action_domains"), "conflicts", "off_domain_form_action", 0.8)
    if url_features.get("hosted_platform_domain") and url_features.get("brand_token_candidate"):
        add("url", "hosted platform URL contains brand-like token", url_features.get("brand_token_candidates"), "supports", "hosted_platform_brand_shell_candidate", 0.5)
    if network_features.get("post_targets"):
        add("network", "POST target observed in network summary", network_features.get("post_targets"), "supports", "payload_observed", 0.6)
    for issue in issues:
        add("artifact_presence", f"artifact issue: {issue.get('artifact')}", issue.get("issue"), "limits", "artifact_issue", None)
    for signal, value in joint_signals.items():
        if value and signal.startswith("need_"):
            add("joint_signal", signal, value, "limits", signal, 0.6)
    if "insufficient_evidence" in reason_codes:
        add("rule_baseline", "evidence is insufficient for confident decision", True, "limits", "insufficient_evidence", 0.7)
    return entries
