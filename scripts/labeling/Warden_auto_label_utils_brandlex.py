#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lightweight Warden auto-label utilities.

Design goals:
- Zero heavy parsing dependencies.
- Work with existing A~G sample structure and in-memory crawler payloads.
- Prefer weak/auto labels only; never pretend to be human gold.
- Keep memory bounded: accept already-truncated text/html and avoid loading images.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
import os
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
    "login", "log in", "sign in", "signin", "password", "username",
    "account", "password reset", "unlock", "secure login",
    "登录", "登入", "密码", "账号", "賬號", "帳號", "账户", "用戶名", "用户名",
]
VERIFY_KEYWORDS = [
    "verify", "verification", "confirm", "authenticate", "security check",
    "2fa", "mfa", "one-time", "otp", "passcode",
    "验证", "驗證", "确认", "確認", "认证", "驗證碼", "验证码", "动态码", "安全检查",
]
PAYMENT_KEYWORDS = [
    "payment", "pay", "billing", "invoice", "checkout", "card", "cvv", "bank",
    "debit", "credit card", "wire", "iban", "swift",
    "支付", "付款", "账单", "帳單", "发票", "發票", "银行卡", "信用卡", "卡号",
]
WALLET_KEYWORDS = [
    "wallet", "metamask", "coinbase wallet", "trust wallet", "seed phrase", "mnemonic",
    "private key", "connect wallet", "signature request", "approve",
    "钱包", "錢包", "助记词", "助記詞", "私钥", "私鑰", "连接钱包", "連接錢包", "签名", "簽名",
]
PII_KEYWORDS = [
    "ssn", "social security", "passport", "driver license", "identity card", "tax id",
    "full name", "date of birth", "phone number", "address",
    "身份证", "身份證", "护照", "護照", "驾驶证", "駕駛證", "姓名", "出生日期", "住址", "地址", "手机号", "手機號",
]
URGENCY_KEYWORDS = [
    "urgent", "immediately", "suspended", "locked", "expired", "action required", "verify now",
    "limited time", "final notice", "failure notice", "risk alert", "unauthorized",
    "紧急", "立即", "马上", "停用", "冻结", "凍結", "过期", "過期", "尽快", "盡快", "需要操作", "异常", "異常",
]
CAPTCHA_KEYWORDS = [
    "captcha", "verify you are human", "i am human", "cloudflare", "turnstile", "hcaptcha",
    "recaptcha", "geetest", "slider captcha", "press and hold",
    "验证码", "驗證碼", "人机验证", "人機驗證", "滑块", "滑塊",
]
DOWNLOAD_KEYWORDS = [
    "download", "open document", "view file", "shared file", "open pdf",
    "下载", "下載", "查看文件", "打开文档", "打開文檔",
]
TRANSITION_KEYWORDS = [
    "continue", "next", "proceed", "open", "view", "access", "start",
    "继续", "繼續", "下一步", "打开", "打開", "查看", "进入", "進入",
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

# Small built-in lexicon. Keep it lightweight; allow external expansion in future if needed.
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



THIS_DIR = Path(__file__).resolve().parent
ASSET_BRAND_LEXICON_DIR = THIS_DIR.parent.parent / "assets" / "brand_lexicon"
DEFAULT_BRAND_LEXICON_CANDIDATES = [
    os.environ.get("WARDEN_BRAND_LEXICON", "").strip(),
    str(THIS_DIR / "warden_brand_lexicon_v1.json"),
    str(THIS_DIR / "warden_brand_lexicon.json"),
    str(Path.cwd() / "warden_brand_lexicon_v1.json"),
    str(Path.cwd() / "warden_brand_lexicon.json"),
    str(ASSET_BRAND_LEXICON_DIR / "warden_brand_lexicon_v1.json"),
    str(ASSET_BRAND_LEXICON_DIR / "warden_brand_lexicon.json"),
    os.environ.get("EVT_BRAND_LEXICON", "").strip(),
    str(THIS_DIR / "evt_brand_lexicon_v1.json"),
    str(THIS_DIR / "evt_brand_lexicon.json"),
    str(Path.cwd() / "evt_brand_lexicon_v1.json"),
    str(Path.cwd() / "evt_brand_lexicon.json"),
    str(ASSET_BRAND_LEXICON_DIR / "evt_brand_lexicon_v1.json"),
    str(ASSET_BRAND_LEXICON_DIR / "evt_brand_lexicon.json"),
    str(ASSET_BRAND_LEXICON_DIR / "evt_brand_lexicon_standard_v1_web3_expanded.json"),
]


def _normalize_brand_key(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def _normalize_brand_lexicon(raw: Any) -> Dict[str, Dict[str, List[str]]]:
    out: Dict[str, Dict[str, List[str]]] = {}
    if not isinstance(raw, dict):
        return out
    for brand, spec in raw.items():
        brand_key = _normalize_brand_key(str(brand))
        if not brand_key:
            continue
        spec = spec if isinstance(spec, dict) else {}
        aliases: List[str] = []
        domains: List[str] = []
        for alias in spec.get("aliases") or []:
            alias_s = _normalize_brand_key(str(alias))
            if alias_s and alias_s not in aliases:
                aliases.append(alias_s)
        for domain in spec.get("domains") or []:
            domain_s = get_etld1(str(domain).lower())
            if domain_s and domain_s not in domains:
                domains.append(domain_s)
        if brand_key not in aliases:
            aliases.insert(0, brand_key)
        out[brand_key] = {"aliases": aliases, "domains": domains}
    return out


@lru_cache(maxsize=8)
def load_brand_lexicon_from_file(path_str: str) -> Dict[str, Dict[str, List[str]]]:
    path = Path(path_str)
    raw = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    return _normalize_brand_lexicon(raw)


@lru_cache(maxsize=2)
def discover_brand_lexicon() -> Dict[str, Dict[str, List[str]]]:
    for cand in DEFAULT_BRAND_LEXICON_CANDIDATES:
        if not cand:
            continue
        try:
            p = Path(cand)
            if p.exists() and p.is_file():
                return load_brand_lexicon_from_file(str(p.resolve()))
        except Exception:
            continue
    return _normalize_brand_lexicon(BUILTIN_BRAND_LEXICON)


def resolve_brand_lexicon(
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
) -> Dict[str, Dict[str, List[str]]]:
    if lexicon is not None:
        return _normalize_brand_lexicon(lexicon)
    if lexicon_path:
        try:
            p = Path(lexicon_path)
            if p.exists() and p.is_file():
                return load_brand_lexicon_from_file(str(p.resolve()))
        except Exception:
            pass
    return discover_brand_lexicon()


def _edit_distance_leq_one(a: str, b: str) -> bool:
    a = (a or "").lower()
    b = (b or "").lower()
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la > lb:
        a, b = b, a
        la, lb = lb, la
    i = j = edits = 0
    while i < la and j < lb:
        if a[i] == b[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        if la == lb:
            i += 1
            j += 1
        else:
            j += 1
    if j < lb or i < la:
        edits += 1
    return edits <= 1


def extract_claimed_brands_from_url(
    final_url: str,
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
    limit: int = 6,
) -> List[str]:
    lex = resolve_brand_lexicon(lexicon=lexicon, lexicon_path=lexicon_path)
    host = _host(final_url)
    if not host:
        return []
    host_labels = [p for p in re.split(r"[.\-_]+", host) if p]
    etld1 = get_etld1(host)
    etld1_stem = etld1.split(".", 1)[0] if etld1 else ""
    tokens = list(dict.fromkeys(host_labels + ([etld1_stem] if etld1_stem else [])))
    hits: List[Tuple[str, int]] = []
    for brand, spec in lex.items():
        aliases = [re.sub(r"[^a-z0-9]+", "", a.lower()) for a in (spec.get("aliases") or [])]
        aliases = [a for a in aliases if a]
        domains = [get_etld1(d) for d in (spec.get("domains") or []) if d]
        score = 0
        for token in tokens:
            token_n = re.sub(r"[^a-z0-9]+", "", token.lower())
            if not token_n:
                continue
            for alias in aliases:
                if token_n == alias:
                    score = max(score, 100 + len(alias))
                elif len(token_n) >= 5 and len(alias) >= 5 and _edit_distance_leq_one(token_n, alias):
                    score = max(score, 60 + len(alias))
            for domain in domains:
                stem = re.sub(r"[^a-z0-9]+", "", domain.split(".", 1)[0].lower())
                if stem and token_n == stem:
                    score = max(score, 95 + len(stem))
                elif stem and len(token_n) >= 5 and len(stem) >= 5 and _edit_distance_leq_one(token_n, stem):
                    score = max(score, 55 + len(stem))
        if score > 0:
            hits.append((brand, score))
    hits.sort(key=lambda kv: (-kv[1], kv[0]))
    return [brand for brand, _ in hits[:limit]]


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def _netloc(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
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
    if top_count <= 0:
        return "unknown"
    return top_lang


def _kw_match(text_low: str, kw: str) -> bool:
    kw_low = kw.lower()
    if not kw_low:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 ._-]*", kw_low):
        pattern = r"(?<![a-z0-9])" + re.escape(kw_low).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        return re.search(pattern, text_low) is not None
    return kw_low in text_low


def contains_any(text: str, keywords: Sequence[str]) -> bool:
    text_low = (text or "").lower()
    return any(_kw_match(text_low, k) for k in keywords)


def hit_keywords(text: str, keywords: Sequence[str], limit: int = 10) -> List[str]:
    text_low = (text or "").lower()
    hits: List[str] = []
    for kw in keywords:
        if _kw_match(text_low, kw) and kw not in hits:
            hits.append(kw)
            if len(hits) >= limit:
                break
    return hits


def summarize_forms(forms_json: Optional[dict]) -> dict:
    forms = []
    if isinstance(forms_json, dict):
        forms = forms_json.get("forms") or []
    forms = forms if isinstance(forms, list) else []

    type_counter: Counter = Counter()
    attr_counter: Counter = Counter()
    action_domains: List[str] = []
    off_domain_form_action = False
    has_password = False
    has_otp = False
    has_card = False
    total_inputs = 0
    form_methods: Counter = Counter()

    for form in forms:
        if not isinstance(form, dict):
            continue
        method = (form.get("method") or "GET").upper()
        form_methods[method] += 1
        action = form.get("action_abs") or form.get("action") or ""
        if action:
            action_domains.append(get_etld1(action))
        has_password = has_password or bool(form.get("has_password"))
        has_otp = has_otp or bool(form.get("has_otp"))
        has_card = has_card or bool(form.get("has_card"))
        for inp in form.get("inputs") or []:
            if not isinstance(inp, dict):
                continue
            total_inputs += 1
            inp_type = (inp.get("type") or "text").strip().lower() or "text"
            type_counter[inp_type] += 1
            blob = " ".join([
                inp_type,
                str(inp.get("name") or ""),
                str(inp.get("id") or ""),
                str(inp.get("autocomplete") or ""),
                str(inp.get("placeholder") or ""),
                str(inp.get("aria_label") or ""),
            ]).lower()
            for flag, kws in {
                "email_like": ["mail", "email", "e-mail", "邮箱", "郵箱"],
                "phone_like": ["phone", "mobile", "tel", "手机号", "手機號", "电话", "電話"],
                "otp_like": ["otp", "one-time", "2fa", "mfa", "验证码", "驗證碼"],
                "user_like": ["user", "login", "account", "账号", "賬號", "账户", "帳戶"],
                "name_like": ["name", "fullname", "姓名"],
                "address_like": ["address", "地址", "住址"],
                "card_like": ["card", "cvv", "银行卡", "信用卡", "expiry", "exp"],
            }.items():
                if any(k in blob for k in kws):
                    attr_counter[flag] += 1

    return {
        "form_count": len(forms),
        "input_total": total_inputs,
        "input_types": dict(type_counter),
        "input_attr_hints": dict(attr_counter),
        "has_password": has_password,
        "has_otp": has_otp,
        "has_card": has_card,
        "form_methods": dict(form_methods),
        "action_domains": sorted(d for d in set(action_domains) if d),
    }


def summarize_url(final_url: str, input_url: str = "") -> dict:
    final_url = normalize_url(final_url)
    input_url = normalize_url(input_url)
    host = _host(final_url)
    etld1 = get_etld1(host)
    path = _path(final_url)
    path_lower = path.lower()
    netloc = _netloc(final_url)
    depth = max(0, host.count("."))
    suspicious_kw_hits = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in final_url.lower()]
    return {
        "input_url": input_url,
        "final_url": final_url,
        "host": host,
        "etld1": etld1,
        "subdomain_depth": depth,
        "is_ip_host": _is_ip_host(host),
        "has_punycode": "xn--" in host,
        "url_length": len(final_url),
        "path_length": len(path),
        "digit_count": sum(ch.isdigit() for ch in final_url),
        "special_char_count": sum(ch in "-_@=%" for ch in final_url),
        "suspicious_url_keywords": suspicious_kw_hits[:12],
        "path": path,
        "netloc": netloc,
        "path_loginish": contains_any(path_lower, LOGIN_KEYWORDS + VERIFY_KEYWORDS + PAYMENT_KEYWORDS + WALLET_KEYWORDS),
    }


def summarize_network(net_summary: Optional[dict], top_etld1: str) -> dict:
    if not isinstance(net_summary, dict):
        return {
            "third_party_domain_count": 0,
            "post_target_count": 0,
            "post_to_third_party": False,
            "many_third_party": False,
            "too_many_redirects": False,
            "request_total": 0,
        }
    third_party_domains = [d for d in (net_summary.get("third_party_domains") or []) if isinstance(d, str)]
    post_targets = [d for d in (net_summary.get("post_targets") or []) if isinstance(d, dict)]
    anomalies = set(net_summary.get("anomalies") or [])
    request_counts = net_summary.get("request_counts") or {}
    request_total = int(request_counts.get("total") or 0)
    post_to_third_party = any((pt.get("domain_etld1") or "") != top_etld1 for pt in post_targets if pt.get("domain_etld1"))
    return {
        "third_party_domain_count": len(third_party_domains),
        "third_party_domains": third_party_domains[:20],
        "post_target_count": len(post_targets),
        "post_to_third_party": post_to_third_party,
        "many_third_party": ("many_third_party" in anomalies) or len(third_party_domains) >= 10,
        "too_many_redirects": "too_many_redirects" in anomalies,
        "request_total": request_total,
        "resource_type_counts": (request_counts.get("by_resource_type") or {}) if isinstance(request_counts, dict) else {},
    }


def _maybe_read_headers_presence(resp_header_flags: Optional[dict]) -> dict:
    flags = resp_header_flags or {}
    if not isinstance(flags, dict):
        return {}
    out = {}
    for k in ("content_security_policy", "strict_transport_security", "x_frame_options", "x_content_type_options", "referrer_policy"):
        if k in flags:
            out[k] = bool(flags.get(k))
    return out


def summarize_html_features(html_text: str, final_url: str = "") -> dict:
    html_text = (html_text or "")[:MAX_HTML_SCAN_CHARS]
    script_srcs = RE_SCRIPT_SRC.findall(html_text)
    script_domains = sorted({get_etld1(src) for src in script_srcs if get_etld1(src)})
    lib_hits: Dict[str, List[str]] = {}
    lower_html = html_text.lower()
    for lib, aliases in KNOWN_JS_LIBS.items():
        matched = [a for a in aliases if a.lower() in lower_html]
        if matched:
            lib_hits[lib] = matched[:4]
    versions: List[str] = []
    for src in script_srcs[:80]:
        m = RE_VERSION.search(src)
        if m:
            versions.append(m.group(1))
    inline_obfuscation_like = lower_html.count("eval(") + lower_html.count("fromcharcode") + lower_html.count("atob(")
    return {
        "external_script_count": len(script_srcs),
        "external_script_domain_count": len(script_domains),
        "external_script_domains": script_domains[:20],
        "known_js_libraries": sorted(lib_hits.keys()),
        "known_js_library_hits": lib_hits,
        "library_version_candidates": versions[:20],
        "inline_obfuscation_like_count": inline_obfuscation_like,
        "captcha_evidence": contains_any(lower_html, CAPTCHA_KEYWORDS),
        "download_evidence": contains_any(lower_html, DOWNLOAD_KEYWORDS),
    }



def extract_claimed_brands(
    text: str,
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
    limit: int = 6,
) -> List[str]:
    lex = resolve_brand_lexicon(lexicon=lexicon, lexicon_path=lexicon_path)
    text_low = (text or "").lower()
    claimed: List[Tuple[str, int]] = []
    for brand, spec in lex.items():
        aliases = spec.get("aliases") or []
        score = 0
        for alias in aliases:
            if _kw_match(text_low, alias):
                score += max(1, len(alias))
        if score > 0:
            claimed.append((brand, score))
    claimed.sort(key=lambda kv: (-kv[1], kv[0]))
    return [b for b, _ in claimed[:limit]]


def classify_domain_brand_consistency(
    claimed_brands: Sequence[str],
    final_url: str,
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
) -> str:
    if not claimed_brands:
        return "no_brand_claim"
    lex = resolve_brand_lexicon(lexicon=lexicon, lexicon_path=lexicon_path)
    host = _host(final_url)
    etld1 = get_etld1(host)
    if not host:
        return "unknown"
    for brand in claimed_brands:
        spec = lex.get(brand) or {}
        domains = [d.lower() for d in (spec.get("domains") or [])]
        if not domains:
            continue
        for d in domains:
            d_etld1 = get_etld1(d)
            if etld1 == d_etld1 or host.endswith("." + d_etld1):
                return "consistent"
    return "mismatch"


def derive_intent_signals(text: str, forms_summary: dict, html_features: dict) -> dict:
    text_low = (text or "").lower()
    input_types = forms_summary.get("input_types") or {}
    attr_hints = forms_summary.get("input_attr_hints") or {}
    credential = (
        bool(forms_summary.get("has_password"))
        or input_types.get("password", 0) > 0
        or contains_any(text_low, LOGIN_KEYWORDS)
        or attr_hints.get("user_like", 0) > 0
    )
    otp = bool(forms_summary.get("has_otp")) or attr_hints.get("otp_like", 0) > 0 or contains_any(text_low, VERIFY_KEYWORDS)
    payment = bool(forms_summary.get("has_card")) or attr_hints.get("card_like", 0) > 0 or contains_any(text_low, PAYMENT_KEYWORDS)
    wallet = contains_any(text_low, WALLET_KEYWORDS)
    pii = attr_hints.get("name_like", 0) > 0 or attr_hints.get("address_like", 0) > 0 or contains_any(text_low, PII_KEYWORDS)
    urgency = contains_any(text_low, URGENCY_KEYWORDS)
    social_hint = contains_any(text_low, SOCIAL_ENGINEERING_HINTS)
    return {
        "credential_intent_candidate": credential,
        "otp_intent_candidate": otp,
        "payment_intent_candidate": payment,
        "wallet_connect_intent_candidate": wallet,
        "personal_info_intent_candidate": pii,
        "urgency_or_threat_language_candidate": urgency,
        "social_engineering_language_candidate": social_hint,
        "download_intent_candidate": bool(html_features.get("download_evidence")) or contains_any(text_low, DOWNLOAD_KEYWORDS),
    }


def derive_page_stage(intent_signals: dict, forms_summary: dict, text: str) -> str:
    text_low = (text or "").lower()
    if intent_signals.get("wallet_connect_intent_candidate"):
        return "wallet_connect"
    if intent_signals.get("payment_intent_candidate"):
        return "payment"
    if intent_signals.get("otp_intent_candidate") and not intent_signals.get("credential_intent_candidate"):
        return "verification"
    if intent_signals.get("credential_intent_candidate"):
        return "login"
    if intent_signals.get("personal_info_intent_candidate"):
        return "pii_collection"
    if intent_signals.get("download_intent_candidate"):
        return "download"
    if forms_summary.get("form_count", 0) > 0 and contains_any(text_low, TRANSITION_KEYWORDS + VERIFY_KEYWORDS):
        return "transition"
    if contains_any(text_low, TRANSITION_KEYWORDS):
        return "transition"
    return "other"


def derive_evasion_signals(text: str, html_features: dict, diff_summary: Optional[dict], net_features: dict) -> dict:
    text_low = (text or "").lower()
    flags = set((diff_summary or {}).get("flags") or []) if isinstance(diff_summary, dict) else set()
    errors = (diff_summary or {}).get("errors") if isinstance(diff_summary, dict) else None
    captcha = bool(html_features.get("captcha_evidence")) or contains_any(text_low, CAPTCHA_KEYWORDS)
    cloak = bool({"possible_cloaking", "dynamic_redirect"} & flags)
    anti_bot = captcha or contains_any(text_low, ["cloudflare", "attention required", "verify you are human"])
    return {
        "captcha_present_candidate": captcha,
        "dynamic_redirect_candidate": "dynamic_redirect" in flags,
        "cloak_suspected_candidate": cloak,
        "anti_bot_or_cloaking_candidate": anti_bot or cloak,
        "variant_failed_candidate": bool(errors) or ("variant_failed" in flags),
        "needs_interaction_candidate": captcha or (derive_safe_int((diff_summary or {}).get("base", {}).get("visible_text_len")) == 0 and net_features.get("request_total", 0) > 20),
    }


def derive_safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def compute_weak_risk(
    url_features: dict,
    forms_summary: dict,
    brand_signals: dict,
    intent_signals: dict,
    evasion_signals: dict,
    net_features: dict,
    html_features: dict,
) -> Tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []

    def add(points: int, reason: str, cond: bool) -> None:
        nonlocal score
        if cond:
            score += points
            reasons.append(reason)

    add(30, "brand_domain_mismatch", brand_signals.get("domain_brand_consistency_candidate") == "mismatch")
    add(22, "credential_intent", intent_signals.get("credential_intent_candidate"))
    add(16, "payment_intent", intent_signals.get("payment_intent_candidate"))
    add(12, "otp_intent", intent_signals.get("otp_intent_candidate"))
    add(12, "wallet_connect_intent", intent_signals.get("wallet_connect_intent_candidate"))
    add(8, "urgency_language", intent_signals.get("urgency_or_threat_language_candidate"))
    add(10, "off_domain_form_action", forms_summary.get("off_domain_form_action"))
    add(10, "post_to_third_party", net_features.get("post_to_third_party"))
    add(6, "many_third_party", net_features.get("many_third_party"))
    add(8, "captcha_or_cloak", evasion_signals.get("anti_bot_or_cloaking_candidate"))
    add(6, "dynamic_redirect", evasion_signals.get("dynamic_redirect_candidate"))
    add(6, "punycode_or_ip_host", url_features.get("has_punycode") or url_features.get("is_ip_host"))
    add(4, "suspicious_url_keywords", len(url_features.get("suspicious_url_keywords") or []) >= 2)
    add(4, "inline_obfuscation_like", derive_safe_int(html_features.get("inline_obfuscation_like_count")) >= 2)
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


def derive_auto_labels(
    *,
    input_url: str,
    final_url: str,
    visible_text: str,
    forms_json: Optional[dict],
    net_summary: Optional[dict],
    html_rendered: str = "",
    html_raw: str = "",
    diff_summary: Optional[dict] = None,
    page_title: str = "",
    label: Optional[str] = None,
    response_header_flags: Optional[dict] = None,
    source: str = "unknown",
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
) -> dict:
    final_url = normalize_url(final_url)
    input_url = normalize_url(input_url)
    visible_text = sanitize_text((page_title or "") + "\n" + (visible_text or ""), MAX_TEXT_SCAN_CHARS)
    html_for_scan = (html_rendered or html_raw or "")[:MAX_HTML_SCAN_CHARS]

    url_features = summarize_url(final_url, input_url)
    forms_summary = summarize_forms(forms_json)
    top_etld1 = url_features.get("etld1") or ""
    net_features = summarize_network(net_summary, top_etld1)
    html_features = summarize_html_features(html_for_scan, final_url) if html_for_scan else {
        "external_script_count": 0,
        "external_script_domain_count": 0,
        "external_script_domains": [],
        "known_js_libraries": [],
        "known_js_library_hits": {},
        "library_version_candidates": [],
        "inline_obfuscation_like_count": 0,
        "captcha_evidence": False,
        "download_evidence": False,
    }
    text_claimed_brands = extract_claimed_brands(visible_text, lexicon=lexicon, lexicon_path=lexicon_path)
    url_claimed_brands = extract_claimed_brands_from_url(final_url, lexicon=lexicon, lexicon_path=lexicon_path)
    claimed_brands = list(dict.fromkeys(list(text_claimed_brands) + list(url_claimed_brands)))
    if text_claimed_brands and url_claimed_brands:
        brand_claim_source = "mixed"
    elif text_claimed_brands:
        brand_claim_source = "text"
    elif url_claimed_brands:
        brand_claim_source = "url"
    else:
        brand_claim_source = "none"
    brand_signals = {
        "brand_claim_present_candidate": bool(claimed_brands),
        "claimed_brands": claimed_brands,
        "brand_claim_source": brand_claim_source,
        "text_brand_candidates": text_claimed_brands,
        "url_brand_candidates": url_claimed_brands,
        "domain_brand_consistency_candidate": classify_domain_brand_consistency(
            claimed_brands, final_url, lexicon=lexicon, lexicon_path=lexicon_path
        ),
        "brand_token_in_url": [b for b in claimed_brands if b in final_url.lower()],
    }

    forms_summary["off_domain_form_action"] = any(
        d and top_etld1 and d != top_etld1 for d in (forms_summary.get("action_domains") or [])
    )

    intent_signals = derive_intent_signals(visible_text, forms_summary, html_features)
    page_stage_candidate = derive_page_stage(intent_signals, forms_summary, visible_text)
    evasion_signals = derive_evasion_signals(visible_text, html_features, diff_summary, net_features)
    score, reasons = compute_weak_risk(
        url_features=url_features,
        forms_summary=forms_summary,
        brand_signals=brand_signals,
        intent_signals=intent_signals,
        evasion_signals=evasion_signals,
        net_features=net_features,
        html_features=html_features,
    )

    out = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_utc_iso(),
        "source": source,
        "label_hint": label,
        "page_stage_candidate": page_stage_candidate,
        "language_candidate": detect_language_candidate(visible_text),
        "url_features": url_features,
        "form_features": forms_summary,
        "html_features": html_features,
        "brand_signals": brand_signals,
        "intent_signals": intent_signals,
        "evasion_signals": evasion_signals,
        "network_features": {
            **net_features,
            "response_headers_present": _maybe_read_headers_presence(response_header_flags),
        },
        "risk_outputs": {
            "risk_score_weak": score,
            "risk_level_weak": risk_level_from_score(score),
            "risk_reasons": reasons,
        },
    }
    return out



def derive_rule_labels(auto_labels: dict) -> dict:
    brand = auto_labels.get("brand_signals") or {}
    intent = auto_labels.get("intent_signals") or {}
    evasion = auto_labels.get("evasion_signals") or {}
    forms = auto_labels.get("form_features") or {}
    risk = auto_labels.get("risk_outputs") or {}

    escalate_l2 = any([
        brand.get("domain_brand_consistency_candidate") == "mismatch" and intent.get("credential_intent_candidate"),
        intent.get("payment_intent_candidate"),
        intent.get("wallet_connect_intent_candidate"),
        evasion.get("anti_bot_or_cloaking_candidate"),
        evasion.get("needs_interaction_candidate"),
        forms.get("off_domain_form_action"),
        (risk.get("risk_level_weak") in {"high", "critical"}),
    ])
    return {
        "schema_version": "evt_v1.1",
        "generated_at_utc": now_utc_iso(),
        "rule_flags": {
            "escalate_to_l2_candidate": escalate_l2,
            "brand_mismatch_with_sensitive_intent": (
                brand.get("domain_brand_consistency_candidate") == "mismatch"
                and (
                    intent.get("credential_intent_candidate")
                    or intent.get("payment_intent_candidate")
                    or intent.get("otp_intent_candidate")
                    or intent.get("wallet_connect_intent_candidate")
                )
            ),
            "off_domain_sensitive_form": bool(forms.get("off_domain_form_action")) and (
                intent.get("credential_intent_candidate")
                or intent.get("payment_intent_candidate")
                or intent.get("otp_intent_candidate")
            ),
        },
        "review_priority": (
            "p0" if risk.get("risk_level_weak") == "critical"
            else "p1" if risk.get("risk_level_weak") == "high"
            else "p2" if risk.get("risk_level_weak") == "medium"
            else "p3"
        ),
    }


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


def derive_auto_labels_from_sample_dir(sample_dir: Path, source: str = "backfill", lexicon_path: Optional[str] = None) -> dict:
    meta = load_json(sample_dir / "meta.json") or {}
    urlj = load_json(sample_dir / "url.json") or {}
    forms = load_json(sample_dir / "forms.json") or {"forms": []}
    net = load_json(sample_dir / "net_summary.json") or {}
    diff = load_json(sample_dir / "diff_summary.json")
    visible_text = read_text_limited(sample_dir / "visible_text.txt", MAX_TEXT_SCAN_CHARS)
    html_rendered = read_text_limited(sample_dir / "html_rendered.html", MAX_HTML_SCAN_CHARS)
    html_raw = ""
    if not html_rendered:
        html_raw = read_text_limited(sample_dir / "html_raw.html", MAX_HTML_SCAN_CHARS)

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
        lexicon_path=lexicon_path,
    )


def is_sample_dir(path: Path) -> bool:
    return path.is_dir() and (path / "meta.json").exists() and (path / "url.json").exists()


def iter_sample_dirs(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        # two-level scan is not enough because user may have nested folders; use rglob lazily.
        for p in root.rglob("meta.json"):
            sample_dir = p.parent
            if (sample_dir / "url.json").exists():
                yield sample_dir
