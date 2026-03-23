#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import hashlib
from typing import Iterable, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "mkt_tok",
    "ref",
    "ref_src",
    "source",
    "spm",
    "trk",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
}


def normalize_input_url(url: str) -> str:
    url = (url or "").replace("\ufeff", "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme:
        return url
    return f"https://{url}"


def _filtered_query_pairs(query: str) -> Iterable[Tuple[str, str]]:
    for key, value in parse_qsl(query, keep_blank_values=True):
        key_l = key.lower()
        if key_l in TRACKING_QUERY_KEYS or key_l.startswith("utm_"):
            continue
        yield key, value


def canonicalize_url(url: str) -> str:
    url = normalize_input_url(url)
    if not url:
        return ""
    parsed = urlparse(url)
    scheme = (parsed.scheme or "https").lower()
    host = (parsed.hostname or "").lower()
    if not host:
        return ""
    port = ""
    if parsed.port and not ((scheme == "http" and parsed.port == 80) or (scheme == "https" and parsed.port == 443)):
        port = f":{parsed.port}"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/") or "/"
    query = urlencode(sorted(_filtered_query_pairs(parsed.query)))
    return urlunparse((scheme, f"{host}{port}", path, "", query, ""))


def host_from_url(url: str) -> str:
    return (urlparse(normalize_input_url(url)).hostname or "").lower()


def registrable_domain(url: str) -> str:
    host = host_from_url(url).strip(".")
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def stable_hash(text: str, prefix: str = "", length: int = 16) -> str:
    digest = hashlib.sha1((text or "").encode("utf-8", errors="ignore")).hexdigest()
    digest = digest[:length]
    return f"{prefix}{digest}" if prefix else digest
