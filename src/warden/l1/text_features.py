"""Visible-text feature extraction for the L1 rule baseline."""

from __future__ import annotations

import re
from typing import Dict, List


KEYWORD_BUCKETS = {
    "login_auth": ["login", "log in", "sign in", "signin", "password", "account", "verify"],
    "payment_checkout_billing": ["payment", "checkout", "billing", "card", "invoice", "pay now"],
    "finance_banking": ["bank", "banking", "transfer", "loan", "investment", "financial"],
    "crypto_web3_wallet": ["wallet", "seed phrase", "private key", "metamask", "airdrop", "web3"],
    "support_contact_chat": ["support", "helpdesk", "contact us", "chat", "agent"],
    "download_install_app_extension": ["download", "install", "extension", "update", "apk", "app"],
    "reward_prize_airdrop": ["reward", "prize", "winner", "claim", "airdrop", "bonus"],
    "security_verify_urgent": ["security", "urgent", "suspended", "verify now", "locked", "protect"],
    "ai_api_token_dashboard": ["api key", "token", "dashboard", "openai", "chatgpt", "ai"],
    "donation_charity": ["donate", "donation", "charity", "fundraiser"],
    "hosting_domain_cloud_telecom": ["hosting", "domain", "cloud", "dns", "telecom"],
}


def _effective_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _rough_words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_]+", text or "")


def extract_visible_text_features(visible_text: str | None) -> Dict[str, object]:
    text = visible_text or ""
    effective = _effective_text(text)
    lowered = effective.lower()
    keyword_hits: Dict[str, List[str]] = {}
    for bucket, keywords in KEYWORD_BUCKETS.items():
        hits = [keyword for keyword in keywords if keyword in lowered]
        if hits:
            keyword_hits[bucket] = hits

    return {
        "visible_text_present": bool(effective),
        "visible_text_chars": len(text),
        "visible_text_words": len(_rough_words(effective)),
        "effective_visible_text_chars": len(effective),
        "text_sparse": len(effective) < 300,
        "text_very_sparse": len(effective) < 100,
        "keyword_hits_by_bucket": keyword_hits,
    }
