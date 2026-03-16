#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lightweight EVT auto-label utilities aligned to EVT_Label_Schema_v1.1.

Design goals:
- Zero heavy parsing dependencies.
- Reuse existing A~G crawler artifacts and in-memory payloads.
- Emit v1.1-aligned weak labels without pretending to be human gold.
- Keep memory bounded: no OCR, no image decoding, no repeated page rendering.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

SCHEMA_VERSION = "evt_v1.1"
MAX_HTML_SCAN_CHARS = 600_000
MAX_TEXT_SCAN_CHARS = 120_000

RE_WS = re.compile(r"\s+")
RE_SCRIPT_SRC = re.compile(r"<script[^>]+src=[\"\']([^\"\']+)[\"\']", re.I)
RE_URL_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
RE_HTML_TAG = re.compile(r"<[^>]+>")
RE_VERSION = re.compile(r"(?<!\d)(\d{1,3}(?:\.\d{1,3}){1,3})(?!\d)")

LOGIN_KEYWORDS = [
    "login", "log in", "sign in", "signin", "password", "username", "account",
    "password reset", "unlock", "secure login", "登录", "登入", "密码", "账号",
    "賬號", "帳號", "账户", "用戶名", "用户名",
]
VERIFY_KEYWORDS = [
    "verify", "verification", "confirm", "authenticate", "security check", "2fa",
    "mfa", "one-time", "otp", "passcode", "验证", "驗證", "确认", "確認",
    "认证", "驗證碼", "验证码", "动态码", "安全检查",
]
PAYMENT_KEYWORDS = [
    "payment", "pay", "billing", "invoice", "checkout", "card", "cvv", "bank",
    "debit", "credit card", "wire", "iban", "swift", "支付", "付款", "账单",
    "帳單", "发票", "發票", "银行卡", "信用卡", "卡号",
]
WALLET_KEYWORDS = [
    "wallet", "metamask", "coinbase wallet", "trust wallet", "seed phrase",
    "mnemonic", "private key", "connect wallet", "signature request", "approve",
    "钱包", "錢包", "助记词", "助記詞", "私钥", "私鑰", "连接钱包",
    "連接錢包", "签名", "簽名",
]
PII_KEYWORDS = [
    "ssn", "social security", "passport", "driver license", "identity card", "tax id",
    "full name", "date of birth", "phone number", "address", "身份证", "身份證",
    "护照", "護照", "驾驶证", "駕駛證", "姓名", "出生日期", "住址", "地址",
    "手机号", "手機號",
]
URGENCY_KEYWORDS = [
    "urgent", "immediately", "suspended", "locked", "expired", "action required",
    "verify now", "limited time", "final notice", "failure notice", "risk alert",
    "unauthorized", "紧急", "立即", "马上", "停用", "冻结", "凍結", "过期",
    "過期", "尽快", "盡快", "需要操作", "异常", "異常",
]
CAPTCHA_KEYWORDS = [
    "captcha", "verify you are human", "i am human", "cloudflare", "turnstile",
    "hcaptcha", "recaptcha", "geetest", "slider captcha", "press and hold",
    "验证码", "驗證碼", "人机验证", "人機驗證", "滑块", "滑塊",
]
DOWNLOAD_KEYWORDS = [
    "download", "open document", "view file", "shared file", "open pdf",
    "下载", "下載", "查看文件", "打开文档", "打開文檔",
]
TRANSITION_KEYWORDS = [
    "continue", "next", "proceed", "open", "view", "access", "start", "继续",
    "繼續", "下一步", "打开", "打開", "查看", "进入", "進入",
]
NOTIFICATION_KEYWORDS = [
    "invoice", "shipment", "delivery", "notice", "notification", "security alert",
    "billing notice", "package", "邮件通知", "通知", "账单提醒", "帳單提醒",
    "物流", "快递", "快遞", "包裹",
]
SOCIAL_ENGINEERING_HINTS = [
    "dear customer", "dear user", "support team", "security team", "billing team",
    "尊敬的用户", "尊敬的用戶", "客服", "支持团队", "支持團隊",
]
SUSPICIOUS_URL_KEYWORDS = [
    "login", "signin", "verify", "update", "secure", "account", "wallet", "payment",
    "auth", "session", "recover", "unlock", "suspended", "invoice", "webscr", "confirm",
]
KNOWN_JS_LIBS = {
    "jquery": ["jquery"],
    "bootstrap": ["bootstrap"],
    "react": ["react", "react-dom"],
    "vue": ["vue"],
    "angular": ["angular"],
    "axios": ["axios"],
    "socket.io": ["socket.io"],
    "crypto-js": ["crypto-js"],
    "lodash": ["lodash"],
    "sweetalert": ["sweetalert", "swal"],
    "moment": ["moment"],
}

BUILTIN_BRAND_LEXICON: Dict[str, Dict[str, Sequence[str]]] = {
    "paypal": {"aliases": ["paypal"], "domains": ["paypal.com"]},
    "microsoft": {"aliases": ["microsoft", "office 365", "outlook", "onedrive", "sharepoint"], "domains": ["microsoft.com", "live.com", "office.com", "outlook.com", "sharepoint.com", "microsoftonline.com"]},
    "google": {"aliases": ["google", "gmail", "google drive", "docs", "sheets"], "domains": ["google.com", "gmail.com", "googleusercontent.com"]},
    "apple": {"aliases": ["apple", "icloud", "apple id", "itunes"], "domains": ["apple.com", "icloud.com"]},
    "amazon": {"aliases": ["amazon", "aws", "amazon pay"], "domains": ["amazon.com", "amazonaws.com"]},
    "meta": {"aliases": ["facebook", "instagram", "meta", "whatsapp"], "domains": ["facebook.com", "instagram.com", "whatsapp.com", "meta.com"]},
    "telegram": {"aliases": ["telegram"], "domains": ["telegram.org"]},
    "binance": {"aliases": ["binance"], "domains": ["binance.com"]},
    "coinbase": {"aliases": ["coinbase", "coinbase wallet"], "domains": ["coinbase.com"]},
    "stripe": {"aliases": ["stripe"], "domains": ["stripe.com"]},
    "dhl": {"aliases": ["dhl"], "domains": ["dhl.com"]},
    "fedex": {"aliases": ["fedex"], "domains": ["fedex.com"]},
    "ups": {"aliases": ["ups"], "domains": ["ups.com"]},
    "alipay": {"aliases": ["alipay", "支付宝", "支付寶"], "domains": ["alipay.com"]},
    "wechat": {"aliases": ["wechat", "weixin", "微信"], "domains": ["wechat.com", "weixin.qq.com", "qq.com"]},
}


# ---------- basic helpers ----------
def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not RE_URL_SCHEME.match(url):
        url = "https://" + url
    return url


def _host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def _path(url: str) -> str:
    try:
        return urlparse(url).path or "/"
    except Exception:
        return "/"


def _is_ip_host(host: str) -> bool:
    parts = host.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except Exception:
        return False


def get_etld1(url_or_host: str) -> str:
    host = url_or_host
    if "://" in url_or_host or "/" in url_or_host:
        host = _host(url_or_host)
    host = (host or "").strip(".").lower()
    if not host:
        return ""
    if _is_ip_host(host):
        return host
    parts = [p for p in host.split(".") if p]
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


def sanitize_text(text: str, max_chars: int = MAX_TEXT_SCAN_CHARS) -> str:
    text = RE_HTML_TAG.sub(" ", text or "")
    text = RE_WS.sub(" ", text).strip()
    return text[:max_chars]


def derive_safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def detect_language_candidate(text: str) -> str:
    if not text:
        return "unknown"
    sample = text[:4000]
    counts = {
        "zh": sum(1 for ch in sample if "\u4e00" <= ch <= "\u9fff"),
        "ja": sum(1 for ch in sample if "\u3040" <= ch <= "\u30ff"),
        "ko": sum(1 for ch in sample if "\uac00" <= ch <= "\ud7af"),
        "arabic": sum(1 for ch in sample if "\u0600" <= ch <= "\u06ff"),
        "cyrillic": sum(1 for ch in sample if "\u0400" <= ch <= "\u04ff"),
        "latin": sum(1 for ch in sample if ch.isascii() and ch.isalpha()),
    }
    top_lang, top_count = max(counts.items(), key=lambda kv: kv[1])
    return top_lang if top_count > 0 else "unknown"


def _kw_match(text_low: str, kw: str) -> bool:
    kw_low = kw.lower().strip()
    if not kw_low:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 ._-]*", kw_low):
        pattern = r"(?<![a-z0-9])" + re.escape(kw_low).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        return re.search(pattern, text_low) is not None
    return kw_low in text_low


def contains_any(text: str, keywords: Sequence[str]) -> bool:
    text_low = (text or "").lower()
    return any(_kw_match(text_low, kw) for kw in keywords)


def hit_keywords(text: str, keywords: Sequence[str], limit: int = 12) -> List[str]:
    text_low = (text or "").lower()
    out: List[str] = []
    for kw in keywords:
        if _kw_match(text_low, kw) and kw not in out:
            out.append(kw)
            if len(out) >= limit:
                break
    return out


# ---------- feature extraction ----------
def summarize_url(final_url: str, input_url: str = "", lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> dict:
    final_url = normalize_url(final_url)
    host = _host(final_url)
    etld1 = get_etld1(host)
    parts = [p for p in host.split(".") if p]
    subdomain_depth = 0 if _is_ip_host(host) else max(0, len(parts) - 2)
    brand_tokens = extract_brands_from_url(final_url, lexicon=lexicon)
    suspicious_tokens = hit_keywords(final_url.lower(), SUSPICIOUS_URL_KEYWORDS, limit=12)
    return {
        "host": host,
        "etld1": etld1,
        "subdomain_depth": subdomain_depth,
        "url_length": len(final_url),
        "has_ip_host": _is_ip_host(host),
        "has_punycode": "xn--" in host,
        "brand_tokens": brand_tokens,
        "suspicious_tokens": suspicious_tokens,
    }


def summarize_forms(forms_json: Optional[dict], top_etld1: str, post_to_third_party: bool) -> Tuple[dict, dict]:
    forms = []
    if isinstance(forms_json, dict):
        forms = forms_json.get("forms") or []
    forms = forms if isinstance(forms, list) else []

    password_field_count = 0
    otp_field_count = 0
    card_field_count = 0
    email_field_count = 0
    phone_field_count = 0
    action_domains: List[str] = []
    attr_counter: Counter = Counter()

    for form in forms:
        if not isinstance(form, dict):
            continue
        action = form.get("action_abs") or form.get("action") or ""
        if action:
            d = get_etld1(action)
            if d:
                action_domains.append(d)
        for inp in form.get("inputs") or []:
            if not isinstance(inp, dict):
                continue
            inp_type = (inp.get("type") or "text").strip().lower() or "text"
            blob = " ".join([
                inp_type,
                str(inp.get("name") or ""),
                str(inp.get("id") or ""),
                str(inp.get("autocomplete") or ""),
                str(inp.get("placeholder") or ""),
                str(inp.get("aria_label") or ""),
            ]).lower()
            if inp_type == "password" or any(k in blob for k in ["password", "密码"]):
                password_field_count += 1
            if any(k in blob for k in ["otp", "one-time", "2fa", "mfa", "验证码", "驗證碼", "passcode"]):
                otp_field_count += 1
            if any(k in blob for k in ["card", "cvv", "expiry", "iban", "swift", "银行卡", "信用卡", "卡号"]):
                card_field_count += 1
            if inp_type == "email" or any(k in blob for k in ["email", "e-mail", "mail", "邮箱", "郵箱"]):
                email_field_count += 1
            if inp_type == "tel" or any(k in blob for k in ["phone", "mobile", "tel", "手机号", "手機號", "电话", "電話"]):
                phone_field_count += 1
            for flag, kws in {
                "name_like": ["name", "fullname", "姓名"],
                "address_like": ["address", "地址", "住址"],
            }.items():
                if any(k in blob for k in kws):
                    attr_counter[flag] += 1

    off_domain_form_action = any(d and top_etld1 and d != top_etld1 for d in action_domains)
    form_features = {
        "form_count": len(forms),
        "password_field_count": password_field_count,
        "otp_field_count": otp_field_count,
        "card_field_count": card_field_count,
        "email_field_count": email_field_count,
        "phone_field_count": phone_field_count,
        "off_domain_form_action": off_domain_form_action,
        "post_to_third_party": bool(post_to_third_party),
    }
    support = {
        "action_domains": sorted(set(d for d in action_domains if d)),
        "name_like_count": int(attr_counter.get("name_like") or 0),
        "address_like_count": int(attr_counter.get("address_like") or 0),
    }
    return form_features, support


def summarize_network(net_summary: Optional[dict], response_header_flags: Optional[dict], top_etld1: str) -> Tuple[dict, dict]:
    if not isinstance(net_summary, dict):
        net_summary = {}
    request_counts = net_summary.get("request_counts") or {}
    status_counts = net_summary.get("status_counts") or {}
    post_targets = net_summary.get("post_targets") or []
    post_targets = post_targets if isinstance(post_targets, list) else []
    cross_site_post_count = 0
    for item in post_targets:
        if not isinstance(item, dict):
            continue
        d = item.get("domain_etld1") or ""
        c = derive_safe_int(item.get("count"), 0)
        if d and top_etld1 and d != top_etld1:
            cross_site_post_count += max(0, c)
    failed_request_count = derive_safe_int(status_counts.get("4xx"), 0) + derive_safe_int(status_counts.get("5xx"), 0)
    response_headers_present = _maybe_read_headers_presence(response_header_flags)
    network_features = {
        "request_count": derive_safe_int(request_counts.get("total"), 0),
        "failed_request_count": failed_request_count,
        "cross_site_post_count": cross_site_post_count,
        "suspicious_submit_candidate": cross_site_post_count > 0,
        "response_headers_present": response_headers_present,
    }
    support = {
        "post_to_third_party": cross_site_post_count > 0,
        "many_third_party": "many_third_party" in set(net_summary.get("anomalies") or []),
        "too_many_redirects": "too_many_redirects" in set(net_summary.get("anomalies") or []),
        "request_total": derive_safe_int(request_counts.get("total"), 0),
    }
    return network_features, support


def summarize_html_support(html_text: str) -> dict:
    html_text = (html_text or "")[:MAX_HTML_SCAN_CHARS]
    script_srcs = RE_SCRIPT_SRC.findall(html_text)
    lower_html = html_text.lower()
    versions: List[str] = []
    for src in script_srcs[:80]:
        m = RE_VERSION.search(src)
        if m:
            versions.append(m.group(1))
    known_libs: List[str] = []
    for lib, aliases in KNOWN_JS_LIBS.items():
        if any(alias.lower() in lower_html for alias in aliases):
            known_libs.append(lib)
    return {
        "external_script_count": len(script_srcs),
        "known_js_libraries": sorted(set(known_libs)),
        "library_version_candidates": versions[:20],
        "inline_obfuscation_like_count": lower_html.count("eval(") + lower_html.count("fromcharcode") + lower_html.count("atob("),
        "captcha_evidence": contains_any(lower_html, CAPTCHA_KEYWORDS),
        "download_evidence": contains_any(lower_html, DOWNLOAD_KEYWORDS),
    }


def build_html_features(page_title: str, visible_text: str, form_features: dict, html_support: dict) -> dict:
    text_low = (visible_text or "").lower()
    return {
        "title": (page_title or "")[:512],
        "text_len": len(visible_text or ""),
        "has_form": derive_safe_int(form_features.get("form_count"), 0) > 0,
        "password_evidence": derive_safe_int(form_features.get("password_field_count"), 0) > 0 or contains_any(text_low, LOGIN_KEYWORDS),
        "otp_evidence": derive_safe_int(form_features.get("otp_field_count"), 0) > 0 or contains_any(text_low, VERIFY_KEYWORDS),
        "card_evidence": derive_safe_int(form_features.get("card_field_count"), 0) > 0 or contains_any(text_low, PAYMENT_KEYWORDS),
        "wallet_evidence": contains_any(text_low, WALLET_KEYWORDS),
        "captcha_evidence": bool(html_support.get("captcha_evidence")) or contains_any(text_low, CAPTCHA_KEYWORDS),
        "download_evidence": bool(html_support.get("download_evidence")) or contains_any(text_low, DOWNLOAD_KEYWORDS),
        "urgency_evidence": contains_any(text_low, URGENCY_KEYWORDS),
    }


def extract_claimed_brands(text: str, lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None, limit: int = 6) -> List[str]:
    lex = lexicon or BUILTIN_BRAND_LEXICON
    text_low = (text or "").lower()
    scored: List[Tuple[str, int]] = []
    for brand, spec in lex.items():
        score = 0
        for alias in (spec.get("aliases") or []):
            if _kw_match(text_low, alias):
                score += max(1, len(alias))
        if score > 0:
            scored.append((brand, score))
    scored.sort(key=lambda kv: (-kv[1], kv[0]))
    return [b for b, _ in scored[:limit]]


def extract_brands_from_url(final_url: str, lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None, limit: int = 6) -> List[str]:
    lex = lexicon or BUILTIN_BRAND_LEXICON
    url_low = (final_url or "").lower()
    hits: List[str] = []
    for brand, spec in lex.items():
        for alias in (spec.get("aliases") or []):
            alias_low = alias.lower()
            if alias_low and alias_low in url_low:
                hits.append(brand)
                break
        if len(hits) >= limit:
            break
    return sorted(set(hits))[:limit]


def classify_domain_brand_consistency(claimed_brands: Sequence[str], final_url: str, lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> str:
    if not claimed_brands:
        return "unknown"
    lex = lexicon or BUILTIN_BRAND_LEXICON
    host = _host(final_url)
    etld1 = get_etld1(host)
    if not host:
        return "unknown"
    for brand in claimed_brands:
        spec = lex.get(brand) or {}
        for d in (spec.get("domains") or []):
            d_etld1 = get_etld1(d)
            if d_etld1 and (etld1 == d_etld1 or host.endswith("." + d_etld1)):
                return "consistent"
    return "mismatch"


def build_brand_signals(visible_text: str, final_url: str, url_brand_tokens: Sequence[str], lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> dict:
    claimed_from_text = extract_claimed_brands(visible_text, lexicon=lexicon)
    merged = list(dict.fromkeys(list(claimed_from_text) + list(url_brand_tokens)))[:6]
    has_text = bool(claimed_from_text)
    has_url = bool(url_brand_tokens)
    if has_text and has_url:
        source = "mixed"
    elif has_text:
        source = "text"
    elif has_url:
        source = "url"
    else:
        source = "none"
    return {
        "brand_claim_present_candidate": bool(merged),
        "claimed_brands": merged,
        "domain_brand_consistency_candidate": classify_domain_brand_consistency(merged, final_url, lexicon=lexicon),
        "brand_claim_source": source,
    }


def build_intent_signals(visible_text: str, form_features: dict, html_features: dict, form_support: dict) -> dict:
    text_low = (visible_text or "").lower()
    credential = (
        derive_safe_int(form_features.get("password_field_count"), 0) > 0
        or derive_safe_int(form_features.get("email_field_count"), 0) > 0
        or contains_any(text_low, LOGIN_KEYWORDS)
    )
    otp = derive_safe_int(form_features.get("otp_field_count"), 0) > 0 or contains_any(text_low, VERIFY_KEYWORDS)
    payment = derive_safe_int(form_features.get("card_field_count"), 0) > 0 or contains_any(text_low, PAYMENT_KEYWORDS)
    wallet = bool(html_features.get("wallet_evidence"))
    pii = (
        derive_safe_int(form_support.get("name_like_count"), 0) > 0
        or derive_safe_int(form_support.get("address_like_count"), 0) > 0
        or contains_any(text_low, PII_KEYWORDS)
    )
    download = bool(html_features.get("download_evidence"))
    return {
        "credential_intent_candidate": credential,
        "payment_intent_candidate": payment,
        "otp_intent_candidate": otp,
        "wallet_connect_intent_candidate": wallet,
        "personal_info_intent_candidate": pii,
        "download_intent_candidate": download,
    }


def derive_page_stage(intent_signals: dict, html_features: dict, visible_text: str) -> str:
    text_low = (visible_text or "").lower()
    if intent_signals.get("wallet_connect_intent_candidate"):
        return "wallet"
    if intent_signals.get("payment_intent_candidate"):
        return "payment"
    if intent_signals.get("otp_intent_candidate") and not intent_signals.get("credential_intent_candidate"):
        return "verification"
    if intent_signals.get("credential_intent_candidate"):
        return "login"
    if intent_signals.get("download_intent_candidate"):
        return "download"
    if contains_any(text_low, TRANSITION_KEYWORDS):
        return "transition"
    if contains_any(text_low, NOTIFICATION_KEYWORDS) or (html_features.get("urgency_evidence") and not html_features.get("has_form")):
        return "notification"
    return "landing"


def derive_evasion_signals(visible_text: str, html_features: dict, diff_summary: Optional[dict], network_support: dict) -> dict:
    text_low = (visible_text or "").lower()
    flags = set((diff_summary or {}).get("flags") or []) if isinstance(diff_summary, dict) else set()
    errors = (diff_summary or {}).get("errors") if isinstance(diff_summary, dict) else None
    captcha = bool(html_features.get("captcha_evidence")) or contains_any(text_low, CAPTCHA_KEYWORDS)
    anti_bot = captcha or contains_any(text_low, ["cloudflare", "attention required", "verify you are human"])
    cloak = bool({"possible_cloaking", "dynamic_redirect"} & flags)
    base_visible_len = derive_safe_int((((diff_summary or {}).get("base") or {}).get("visible_text_len")), 0)
    needs_interaction = captcha or (base_visible_len == 0 and network_support.get("request_total", 0) > 20)
    return {
        "needs_interaction_candidate": needs_interaction,
        "anti_bot_or_cloaking_candidate": anti_bot or cloak,
        "captcha_present_candidate": captcha,
        "variant_failed_candidate": bool(errors) or ("variant_failed" in flags),
        "visual_semantic_mismatch_candidate": None,
    }


def _high_value_asset_target(intent_signals: dict) -> str:
    buckets = []
    for name in ["credential", "otp", "payment", "wallet", "pii"]:
        key = {
            "credential": "credential_intent_candidate",
            "otp": "otp_intent_candidate",
            "payment": "payment_intent_candidate",
            "wallet": "wallet_connect_intent_candidate",
            "pii": "personal_info_intent_candidate",
        }[name]
        if intent_signals.get(key):
            buckets.append(name)
    if len(buckets) >= 2:
        return "multiple"
    return buckets[0] if buckets else "none"


def _multi_signal_risk_candidate(brand_signals: dict, intent_signals: dict, html_features: dict, network_features: dict, evasion_signals: dict) -> bool:
    groups = 0
    if brand_signals.get("domain_brand_consistency_candidate") == "mismatch":
        groups += 1
    if any(intent_signals.get(k) for k in [
        "credential_intent_candidate", "payment_intent_candidate", "otp_intent_candidate",
        "wallet_connect_intent_candidate", "personal_info_intent_candidate", "download_intent_candidate",
    ]):
        groups += 1
    if html_features.get("urgency_evidence"):
        groups += 1
    if network_features.get("suspicious_submit_candidate"):
        groups += 1
    if evasion_signals.get("anti_bot_or_cloaking_candidate") or evasion_signals.get("needs_interaction_candidate"):
        groups += 1
    return groups >= 2


def compute_weak_risk(url_features: dict, form_features: dict, brand_signals: dict, intent_signals: dict, evasion_signals: dict, network_features: dict, html_features: dict, html_support: dict) -> Tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []

    def add(points: int, reason: str, cond: bool) -> None:
        nonlocal score
        if cond:
            score += points
            reasons.append(reason)

    add(30, "brand_domain_mismatch", brand_signals.get("domain_brand_consistency_candidate") == "mismatch")
    add(22, "credential_collection", intent_signals.get("credential_intent_candidate"))
    add(16, "payment_collection", intent_signals.get("payment_intent_candidate"))
    add(12, "otp_collection", intent_signals.get("otp_intent_candidate"))
    add(12, "wallet_connect", intent_signals.get("wallet_connect_intent_candidate"))
    add(8, "personal_info_collection", intent_signals.get("personal_info_intent_candidate"))
    add(8, "download_lure", intent_signals.get("download_intent_candidate"))
    add(8, "urgency_language", html_features.get("urgency_evidence"))
    add(10, "off_domain_form_action", form_features.get("off_domain_form_action"))
    add(10, "off_domain_post", form_features.get("post_to_third_party") or network_features.get("cross_site_post_count", 0) > 0)
    add(6, "suspicious_submit", network_features.get("suspicious_submit_candidate"))
    add(8, "captcha_or_cloaking", evasion_signals.get("anti_bot_or_cloaking_candidate"))
    add(6, "needs_interaction", evasion_signals.get("needs_interaction_candidate"))
    add(6, "punycode_or_ip_host", url_features.get("has_punycode") or url_features.get("has_ip_host"))
    add(4, "suspicious_url_tokens", len(url_features.get("suspicious_tokens") or []) >= 2)
    add(4, "inline_obfuscation_like", derive_safe_int(html_support.get("inline_obfuscation_like_count"), 0) >= 2)
    score = min(100, score)
    return score, reasons


def risk_level_from_score(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 45:
        return "high"
    if score >= 20:
        return "medium"
    return "low"


def build_risk_outputs(score: int, reasons: List[str], brand_signals: dict, intent_signals: dict, html_features: dict, form_features: dict, network_features: dict, evasion_signals: dict) -> dict:
    level = risk_level_from_score(score)
    needs_l2 = (
        bool(evasion_signals.get("anti_bot_or_cloaking_candidate"))
        or bool(evasion_signals.get("needs_interaction_candidate"))
        or (brand_signals.get("domain_brand_consistency_candidate") == "mismatch" and intent_signals.get("credential_intent_candidate"))
        or (intent_signals.get("payment_intent_candidate") and form_features.get("post_to_third_party"))
        or level in {"high", "critical"}
    )
    return {
        "risk_score_weak": score,
        "risk_level_weak": level,
        "risk_reasons": reasons,
        "needs_l2_review_candidate": needs_l2,
        "high_value_asset_target": _high_value_asset_target(intent_signals),
        "multi_signal_risk_candidate": _multi_signal_risk_candidate(brand_signals, intent_signals, html_features, network_features, evasion_signals),
    }


def derive_auto_labels(*, input_url: str, final_url: str, visible_text: str, forms_json: Optional[dict], net_summary: Optional[dict], html_rendered: str = "", html_raw: str = "", diff_summary: Optional[dict] = None, page_title: str = "", label: Optional[str] = None, response_header_flags: Optional[dict] = None, source: str = "unknown", lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None) -> dict:
    final_url = normalize_url(final_url)
    visible_text = sanitize_text((page_title or "") + "\n" + (visible_text or ""), MAX_TEXT_SCAN_CHARS)
    html_for_scan = (html_rendered or html_raw or "")[:MAX_HTML_SCAN_CHARS]

    url_features = summarize_url(final_url, input_url, lexicon=lexicon)
    network_features, network_support = summarize_network(net_summary, response_header_flags, url_features.get("etld1") or "")
    form_features, form_support = summarize_forms(forms_json, url_features.get("etld1") or "", network_support.get("post_to_third_party", False))
    html_support = summarize_html_support(html_for_scan)
    html_features = build_html_features(page_title, visible_text, form_features, html_support)
    brand_signals = build_brand_signals(visible_text, final_url, url_features.get("brand_tokens") or [], lexicon=lexicon)
    intent_signals = build_intent_signals(visible_text, form_features, html_features, form_support)
    evasion_signals = derive_evasion_signals(visible_text, html_features, diff_summary, network_support)
    score, reasons = compute_weak_risk(url_features, form_features, brand_signals, intent_signals, evasion_signals, network_features, html_features, html_support)
    risk_outputs = build_risk_outputs(score, reasons, brand_signals, intent_signals, html_features, form_features, network_features, evasion_signals)

    label_hint = (label or "unknown").strip().lower() or "unknown"
    if label_hint not in {"phish", "benign", "unknown"}:
        label_hint = "unknown"

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_utc_iso(),
        "source": source,
        "label_hint": label_hint,
        "page_stage_candidate": derive_page_stage(intent_signals, html_features, visible_text),
        "language_candidate": detect_language_candidate(visible_text),
        "url_features": url_features,
        "html_features": html_features,
        "form_features": form_features,
        "brand_signals": brand_signals,
        "intent_signals": intent_signals,
        "network_features": network_features,
        "evasion_signals": evasion_signals,
        "risk_outputs": risk_outputs,
    }


def derive_rule_labels(auto_labels: Optional[dict]) -> dict:
    auto_labels = auto_labels if isinstance(auto_labels, dict) else {}
    brand = auto_labels.get("brand_signals") or {}
    intent = auto_labels.get("intent_signals") or {}
    formf = auto_labels.get("form_features") or {}
    evasion = auto_labels.get("evasion_signals") or {}
    risk = auto_labels.get("risk_outputs") or {}

    triggered_rules: List[str] = []
    rule_summary: List[str] = []
    boost = 0

    def hit(rule_id: str, summary: str, points: int, cond: bool) -> None:
        nonlocal boost
        if cond:
            triggered_rules.append(rule_id)
            rule_summary.append(summary)
            boost += points

    hit("EVT_R001", "brand mismatch with credential intent", 15,
        brand.get("domain_brand_consistency_candidate") == "mismatch" and intent.get("credential_intent_candidate"))
    hit("EVT_R002", "payment intent with third-party submit", 12,
        intent.get("payment_intent_candidate") and (formf.get("post_to_third_party") or formf.get("off_domain_form_action")))
    hit("EVT_R003", "anti-bot or cloaking suspected", 10,
        evasion.get("anti_bot_or_cloaking_candidate"))
    hit("EVT_R004", "interaction required before key content", 8,
        evasion.get("needs_interaction_candidate"))
    hit("EVT_R005", "weak risk already high", 8,
        risk.get("risk_level_weak") in {"high", "critical"})
    hit("EVT_R006", "multiple risk signal groups observed", 6,
        risk.get("multi_signal_risk_candidate"))

    return {
        "triggered_rules": triggered_rules,
        "rule_risk_boost": min(40, boost),
        "rule_summary": rule_summary,
    }


# ---------- file helpers ----------
def _maybe_read_headers_presence(resp_header_flags: Optional[dict]) -> dict:
    flags = resp_header_flags or {}
    if not isinstance(flags, dict):
        return {}
    out = {}
    for k in ("content_security_policy", "strict_transport_security", "x_frame_options", "x_content_type_options", "referrer_policy"):
        if k in flags:
            out[k] = bool(flags.get(k))
    return out


def load_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def read_text_limited(path: Path, max_chars: int) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_chars)
    except Exception:
        return ""


def derive_auto_labels_from_sample_dir(sample_dir: Path, source: str = "backfill") -> dict:
    meta = load_json(sample_dir / "meta.json") or {}
    urlj = load_json(sample_dir / "url.json") or {}
    forms = load_json(sample_dir / "forms.json") or {"forms": []}
    net = load_json(sample_dir / "net_summary.json") or {}
    diff = load_json(sample_dir / "diff_summary.json")
    visible_text = read_text_limited(sample_dir / "visible_text.txt", MAX_TEXT_SCAN_CHARS)
    html_rendered = read_text_limited(sample_dir / "html_rendered.html", MAX_HTML_SCAN_CHARS)
    html_raw = "" if html_rendered else read_text_limited(sample_dir / "html_raw.html", MAX_HTML_SCAN_CHARS)

    return derive_auto_labels(
        input_url=str(urlj.get("input_url") or ""),
        final_url=str(urlj.get("final_url") or ""),
        visible_text=visible_text,
        forms_json=forms,
        net_summary=net,
        html_rendered=html_rendered,
        html_raw=html_raw,
        diff_summary=diff,
        page_title=str(meta.get("page_title") or ""),
        label=str(meta.get("label") or "") or None,
        source=source,
    )


def is_sample_dir(path: Path) -> bool:
    return path.is_dir() and (path / "meta.json").exists() and (path / "url.json").exists()


def iter_sample_dirs(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("meta.json"):
            sample_dir = p.parent
            if (sample_dir / "url.json").exists():
                yield sample_dir
