"""Lightweight URL and domain features for the L1 rule baseline."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List
from urllib.parse import parse_qsl, urlparse


HOSTED_PLATFORM_SUFFIXES = (
    "github.io",
    "pages.dev",
    "web.app",
    "firebaseapp.com",
    "netlify.app",
    "vercel.app",
    "workers.dev",
    "sites.google.com",
    "wixsite.com",
    "weebly.com",
    "wordpress.com",
    "blogspot.com",
)

BRAND_TOKEN_CANDIDATES = {
    "adobe",
    "amazon",
    "apple",
    "binance",
    "coinbase",
    "facebook",
    "google",
    "icloud",
    "ledger",
    "metamask",
    "microsoft",
    "netflix",
    "office",
    "paypal",
    "trezor",
    "whatsapp",
}


def host_from_url(url: str) -> str:
    parsed = urlparse(url or "")
    return (parsed.hostname or "").lower().strip(".")


def approximate_registrable_domain(host: str) -> str:
    parts = [part for part in (host or "").lower().split(".") if part]
    if len(parts) <= 2:
        return ".".join(parts)
    if len(parts[-1]) == 2 and parts[-2] in {"co", "com", "net", "org", "gov", "ac"} and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def _tokenize_url_parts(values: Iterable[str]) -> List[str]:
    tokens: List[str] = []
    for value in values:
        for token in re.split(r"[^A-Za-z0-9]+", value or ""):
            token = token.lower()
            if len(token) >= 2:
                tokens.append(token)
    return tokens[:80]


def extract_url_features(url_info: Dict[str, Any] | None) -> Dict[str, Any]:
    url_info = url_info if isinstance(url_info, dict) else {}
    input_url = str(url_info.get("input_url") or url_info.get("url") or "")
    final_url = str(url_info.get("final_url") or url_info.get("resolved_url") or input_url)
    parsed = urlparse(final_url)
    final_host = host_from_url(final_url)
    redirect_chain = url_info.get("redirect_chain") or url_info.get("redirects") or []
    if isinstance(redirect_chain, list):
        redirect_count = max(0, len(redirect_chain) - 1)
    else:
        redirect_count = int(url_info.get("redirect_count") or 0)

    path_tokens = _tokenize_url_parts([parsed.path, parsed.params, parsed.query])
    host_tokens = _tokenize_url_parts([final_host])
    query_present = bool(parse_qsl(parsed.query, keep_blank_values=True))
    hosted_platform_domain = any(
        final_host == suffix or final_host.endswith(f".{suffix}") for suffix in HOSTED_PLATFORM_SUFFIXES
    )
    brand_tokens = sorted((set(path_tokens) | set(host_tokens)) & BRAND_TOKEN_CANDIDATES)

    score = 0
    if query_present:
        score += 5
    if redirect_count:
        score += min(15, redirect_count * 5)
    if hosted_platform_domain and brand_tokens:
        score += 20
    if any(token in {"login", "verify", "account", "secure", "wallet", "airdrop"} for token in path_tokens):
        score += 15
    if final_url.startswith("http://"):
        score += 10

    return {
        "input_url": input_url,
        "final_url": final_url,
        "final_host": final_host,
        "registrable_domain_approx": approximate_registrable_domain(final_host),
        "path_tokens": path_tokens,
        "query_present": query_present,
        "redirect_count": redirect_count,
        "hosted_platform_domain": hosted_platform_domain,
        "brand_token_candidate": bool(brand_tokens),
        "brand_token_candidates": brand_tokens,
        "url_suspicion_basic_score": min(score, 100),
    }
