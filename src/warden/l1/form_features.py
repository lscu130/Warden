"""Forms feature extraction for the L1 rule baseline."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .url_features import approximate_registrable_domain, host_from_url


OTP_HINTS = ("otp", "code", "2fa", "mfa", "verification")
CARD_HINTS = ("card", "cc", "cvv", "cvc", "exp", "payment")
WALLET_HINTS = ("wallet", "seed", "phrase", "private", "metamask")


def _as_forms(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        forms = payload.get("forms")
        if isinstance(forms, list):
            return [form for form in forms if isinstance(form, dict)]
        if any(key in payload for key in ("inputs", "action")):
            return [payload]
    if isinstance(payload, list):
        return [form for form in payload if isinstance(form, dict)]
    return []


def _inputs_for_form(form: Dict[str, Any]) -> List[Dict[str, Any]]:
    inputs = form.get("inputs") or form.get("fields") or []
    if isinstance(inputs, list):
        return [item for item in inputs if isinstance(item, dict)]
    return []


def _joined_input_text(item: Dict[str, Any]) -> str:
    return " ".join(str(item.get(key) or "") for key in ("type", "name", "id", "placeholder", "label")).lower()


def extract_form_features(forms_payload: Any, *, final_host: str = "") -> Dict[str, Any]:
    forms = _as_forms(forms_payload)
    input_total = 0
    action_domains: List[str] = []
    has_password = False
    has_otp_hint = False
    has_card_hint = False
    has_wallet_hint = False

    final_reg = approximate_registrable_domain(final_host)
    off_domain = False
    for form in forms:
        action = str(form.get("action") or form.get("action_url") or "")
        action_host = host_from_url(action)
        if action_host:
            action_domains.append(action_host)
            if final_reg and approximate_registrable_domain(action_host) != final_reg:
                off_domain = True
        for input_item in _inputs_for_form(form):
            input_total += 1
            joined = _joined_input_text(input_item)
            if "password" in joined or joined.split(" ", 1)[0] == "password":
                has_password = True
            if any(hint in joined for hint in OTP_HINTS):
                has_otp_hint = True
            if any(hint in joined for hint in CARD_HINTS):
                has_card_hint = True
            if any(hint in joined for hint in WALLET_HINTS):
                has_wallet_hint = True

    return {
        "form_count": len(forms),
        "input_total": input_total,
        "has_password": has_password,
        "has_otp_hint": has_otp_hint,
        "has_card_hint": has_card_hint,
        "has_wallet_hint": has_wallet_hint,
        "action_domains": sorted(set(action_domains)),
        "off_domain_form_action": off_domain if forms else "unknown",
    }
