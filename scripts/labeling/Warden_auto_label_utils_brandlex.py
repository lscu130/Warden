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
import re
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from scripts.data.common.html_payload_utils import read_html_payload_text

SCHEMA_VERSION = "evt_v1.2"
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
WEB3_WALLET_KEYWORDS = [
    "metamask", "coinbase wallet", "trust wallet", "wallet connect", "connect wallet",
    "walletconnect", "seed phrase", "mnemonic", "private key", "signature request",
    "approve transaction", "approve request", "connect your wallet",
    "助记词", "助記詞", "私钥", "私鑰", "连接钱包", "連接錢包", "錢包連接", "钱包连接", "签名请求", "簽名請求",
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
GAMBLING_KEYWORDS = [
    "casino", "sportsbook", "sports betting", "betting", "bet now", "place your bet",
    "bonus bet", "bonus bets", "jackpot", "slots", "slot machine", "blackjack", "roulette",
    "poker", "slot", "wager", "wagering", "odds", "bookmaker", "bookie", "live dealer", "cashier",
    "bet365", "博彩", "赌博", "賭博", "赌场", "賭場", "下注", "投注", "体育投注", "體育投注",
    "彩票", "真人", "棋牌", "捕鱼", "老虎机", "老虎機", "彩金", "线路中心",
]
GAMBLING_HIGH_CONFIDENCE_KEYWORDS = [
    "bet365",
]
GAMBLING_BONUS_KEYWORDS = [
    "welcome bonus", "bonus", "bonus offer", "bonus bet", "profit boost", "free spins",
    "free spin", "cashback", "promo code", "promotion", "promotions", "loyalty program",
    "deposit bonus", "payout", "withdrawal", "deposit", "play now", "sign up bonus",
    "注册送彩金", "首存优惠", "首存優惠", "返水", "返现", "返現", "彩金", "优惠码", "優惠碼",
]
ADULT_KEYWORDS = [
    "porn", "porno", "pornhub", "xxx", "sex video", "sex videos", "sex tube", "adult video",
    "adult videos", "adult content", "cam girl", "cams", "jav", "hentai", "cumshot", "bdsm",
    "anal", "nsfw", "nude", "nudity", "boobs", "milf", "erotic", "amateur porn",
    "theporndude", "91porn", "порно", "色情", "成人视频", "成人影片", "成人内容", "成人內容",
    "成人社区", "成人社區", "裸聊", "约炮", "約炮", "口交", "内射", "內射", "啪啪", "无码", "無碼", "av", "avxxx",
]
ADULT_HIGH_CONFIDENCE_KEYWORDS = [
    "theporndude", "91porn", "порно", "成人社区", "成人社區", "约炮", "約炮", "口交", "内射", "內射",
]
ADULT_AGE_GATE_KEYWORDS = [
    "18+", "18 years", "adults only", "adult only", "age verification", "verify your age",
    "you must be 18", "over 18", "not safe for work", "nsfw", "mature audience",
    "仅限成人", "僅限成人", "年龄验证", "年齡驗證", "未满18岁", "未滿18歲", "成人电影", "成人內容警告",
]
GATE_SURFACE_KEYWORDS = [
    "user verification", "verification in progress", "verify you are human", "i am human",
    "security check", "checking your browser", "attention required", "request unsuccessful",
    "press and hold", "enable javascript and cookies", "access denied", "challenge", "turnstile",
    "incapsula", "cloudflare", "ddos protection", "anti bot", "human verification", "captcha",
    "browser verification", "verify to continue", "click allow", "allow notifications",
    "enable notifications", "install extension", "download extension",
    "human check", "security verification", "confirm you are human", "not a robot",
    "i am not a robot", "i'm not a robot", "one moment please", "one moment, please",
    "please wait while your request is being verified", "your request is being verified",
    "verify your request", "verify if you're human", "verify if you are human", "verify you're not a bot",
    "verify you are not a bot", "checkbox to verify", "checking if the site connection is secure",
    "用户验证", "用戶驗證", "验证中", "驗證中", "安全检查", "安全檢查", "正在检查", "正在檢查", "人机验证", "人機驗證",
    "点击允许", "點擊允許", "允许通知", "允許通知", "安装扩展", "安裝擴展",
    "请稍候", "請稍候", "正在验证您的请求", "正在驗證您的請求",
]
GATE_STRONG_KEYWORDS = [
    "human check", "security verification", "confirm you are human",
    "i am not a robot", "i'm not a robot", "not a robot",
    "please wait while your request is being verified", "your request is being verified",
    "verify your request", "verify if you're human", "verify if you are human",
    "verify you're not a bot", "verify you are not a bot",
    "请稍候", "請稍候", "正在验证您的请求", "正在驗證您的請求",
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


def extract_claimed_brands(
    text: str,
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
    limit: int = 6,
) -> List[str]:
    lex = resolve_brand_lexicon(lexicon=lexicon, lexicon_path=lexicon_path)
    text_low = sanitize_text(text or "", max_chars=MAX_TEXT_SCAN_CHARS).lower()
    if not text_low:
        return []
    hits: List[Tuple[str, int]] = []
    for brand, spec in lex.items():
        aliases = unique_keep_order([brand] + list(spec.get("aliases") or []))
        matched_lengths: List[int] = []
        for alias in aliases:
            alias_s = str(alias or "").strip().lower()
            if alias_s and _kw_match(text_low, alias_s):
                matched_lengths.append(len(alias_s))
        if matched_lengths:
            hits.append((brand, max(matched_lengths)))
    hits.sort(key=lambda kv: (-kv[1], kv[0]))
    return [brand for brand, _ in hits[:limit]]


def classify_domain_brand_consistency(
    claimed_brands: Sequence[str],
    final_url: str,
    lexicon: Optional[Dict[str, Dict[str, Sequence[str]]]] = None,
    lexicon_path: Optional[str] = None,
) -> str:
    brands = [str(b).strip().lower() for b in (claimed_brands or []) if str(b).strip()]
    if not brands:
        return "no_brand_claim"
    host_etld1 = get_etld1(final_url)
    if not host_etld1:
        return "unknown"
    host_stem = re.sub(r"[^a-z0-9]+", "", host_etld1.split(".", 1)[0].lower())
    lex = resolve_brand_lexicon(lexicon=lexicon, lexicon_path=lexicon_path)
    saw_known_brand = False
    for brand in brands:
        spec = lex.get(brand)
        if not spec:
            continue
        saw_known_brand = True
        domains = [get_etld1(d) for d in (spec.get("domains") or []) if d]
        if host_etld1 in domains:
            return "consistent"
        aliases = [re.sub(r"[^a-z0-9]+", "", str(a).lower()) for a in (spec.get("aliases") or [])]
        aliases = [a for a in aliases if a]
        if host_stem and host_stem in aliases:
            return "consistent"
    if saw_known_brand:
        return "mismatch"
    return "unknown"


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
    text_low = (
        (text_low or "")
        .lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2026", "...")
        .replace("\u00a0", " ")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )
    kw_low = (
        (kw or "")
        .lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2026", "...")
        .replace("\u00a0", " ")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )
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


def unique_keep_order(items: Sequence[str], limit: Optional[int] = None) -> List[str]:
    out: List[str] = []
    for item in items:
        if not item or item in out:
            continue
        out.append(item)
        if limit is not None and len(out) >= limit:
            break
    return out


def normalize_url_keyword_blob(final_url: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (final_url or "").lower())


def has_gambling_domain_hint(final_url: str) -> bool:
    host = _host(final_url)
    tokens = [tok for tok in re.split(r"[^a-z0-9]+", (host or "").lower()) if tok]
    for token in tokens:
        if token in {"bet", "casino", "slot", "slots", "poker", "lotto", "sportsbook"}:
            return True
        if len(token) < 5:
            continue
        if "bet" in token or "casino" in token or "slot" in token or "poker" in token or "lotto" in token:
            return True
    return False


def has_bet_digit_host_pattern(final_url: str) -> bool:
    host = _host(final_url)
    if not host:
        return False
    return re.search(r"(?:^|[^a-z0-9])(bet\d{2,}|\d{2,}bet)(?:[^a-z0-9]|$)", host.lower()) is not None


def has_adult_domain_hint(final_url: str) -> bool:
    host = _host(final_url)
    tokens = [tok for tok in re.split(r"[^a-z0-9]+", (host or "").lower()) if tok]
    for token in tokens:
        if token in ADULT_DOMAIN_HINT_TOKENS:
            return True
        if any(core in token for core in ADULT_DOMAIN_HINT_TOKENS):
            return True
    return False


def _maybe_read_headers_presence(resp_header_flags: Optional[dict]) -> dict:
    flags = resp_header_flags or {}
    if not isinstance(flags, dict):
        return {}
    out = {}
    for k in ("content_security_policy", "strict_transport_security", "x_frame_options", "x_content_type_options", "referrer_policy"):
        if k in flags:
            out[k] = bool(flags.get(k))
    return out


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
    from warden.module import l0 as warden_l0

    l0_prepared = warden_l0.prepare_l0_inputs(
        input_url=input_url,
        final_url=final_url,
        visible_text=visible_text,
        forms_json=forms_json,
        net_summary=net_summary,
        html_rendered=html_rendered,
        html_raw=html_raw,
        page_title=page_title,
    )
    input_url = l0_prepared["input_url"]
    final_url = l0_prepared["final_url"]
    raw_visible_text = l0_prepared["raw_visible_text"]
    visible_text = l0_prepared["visible_text"]
    url_features = l0_prepared["url_features"]
    forms_summary = l0_prepared["forms_summary"]
    net_features = l0_prepared["net_features"]
    html_features = l0_prepared["html_features"]

    brand_signals = {
        "brand_claim_present_candidate": False,
        "claimed_brands": [],
        "brand_claim_source": "none",
        "text_brand_candidates": [],
        "url_brand_candidates": [],
        "domain_brand_consistency_candidate": "no_brand_claim",
        "brand_token_in_url": [],
    }

    l0_outputs = warden_l0.derive_l0_outputs(
        final_url=final_url,
        visible_text=visible_text,
        raw_visible_text=raw_visible_text,
        page_title=page_title,
        forms_summary=forms_summary,
        net_features=net_features,
        html_features=html_features,
        diff_summary=diff_summary,
        brand_signals=brand_signals,
        url_features=url_features,
    )

    out = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_utc_iso(),
        "source": source,
        "label_hint": label,
        "page_stage_candidate": l0_outputs["page_stage_candidate"],
        "language_candidate": l0_outputs["language_candidate"],
        "url_features": url_features,
        "form_features": forms_summary,
        "html_features": html_features,
        "brand_signals": brand_signals,
        "intent_signals": l0_outputs["intent_signals"],
        "evasion_signals": l0_outputs["evasion_signals"],
        "specialized_surface_signals": l0_outputs["specialized_surface_signals"],
        "l0_routing_hints": l0_outputs["l0_routing_hints"],
        "network_features": {
            **net_features,
            "response_headers_present": _maybe_read_headers_presence(response_header_flags),
        },
        "risk_outputs": l0_outputs["risk_outputs"],
    }
    return out



def derive_rule_labels(auto_labels: dict) -> dict:
    brand = auto_labels.get("brand_signals") or {}
    intent = auto_labels.get("intent_signals") or {}
    evasion = auto_labels.get("evasion_signals") or {}
    specialized = auto_labels.get("specialized_surface_signals") or {}
    routing = auto_labels.get("l0_routing_hints") or {}
    forms = auto_labels.get("form_features") or {}
    network = auto_labels.get("network_features") or {}
    risk = auto_labels.get("risk_outputs") or {}
    page_stage = str(auto_labels.get("page_stage_candidate") or "other")

    def add_vote(
        votes: Dict[str, int],
        reasons: Dict[str, List[str]],
        label: str,
        weight: int,
        reason: str,
        cond: bool = True,
    ) -> None:
        if not cond or not label or weight <= 0:
            return
        votes[label] = votes.get(label, 0) + weight
        reasons.setdefault(label, [])
        if reason not in reasons[label]:
            reasons[label].append(reason)

    def choose_candidate(
        votes: Dict[str, int],
        reasons: Dict[str, List[str]],
        fallback_label: str,
        fallback_reason: str,
        fallback_confidence: float,
    ) -> Tuple[str, float, List[str]]:
        if not votes:
            return fallback_label, round(max(0.0, min(1.0, fallback_confidence)), 2), [fallback_reason]

        ranked = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))
        best_label, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0
        confidence = 0.35 + min(best_score, 12) * 0.04 + min(best_score - second_score, 6) * 0.03
        confidence = round(max(0.0, min(0.98, confidence)), 2)
        return best_label, confidence, reasons.get(best_label, []) or [fallback_reason]

    claimed_brands = set(brand.get("claimed_brands") or [])
    mismatch = brand.get("domain_brand_consistency_candidate") == "mismatch"
    risk_level = str(risk.get("risk_level_weak") or "low")
    has_contact_brand = bool({"telegram", "meta"} & claimed_brands)
    gambling_surface = bool(specialized.get("possible_gambling_lure"))
    adult_surface = bool(specialized.get("possible_adult_lure"))
    gate_surface = bool(specialized.get("possible_gate_or_evasion"))
    has_sensitive_form = bool(forms.get("has_password") or forms.get("has_otp") or forms.get("has_card"))
    suspicious_delivery = bool(mismatch or forms.get("off_domain_form_action") or network.get("post_to_third_party"))

    primary_votes: Dict[str, int] = {}
    primary_reasons: Dict[str, List[str]] = {}
    add_vote(
        primary_votes,
        primary_reasons,
        "wallet_drain_or_web3_approval_fraud",
        10,
        "wallet_connect_intent_candidate",
        bool(intent.get("wallet_connect_intent_candidate")),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "payment_fraud",
        9,
        "payment_intent_candidate",
        bool(intent.get("payment_intent_candidate")) and not (gambling_surface and not has_sensitive_form and not suspicious_delivery),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "credential_theft",
        8,
        "credential_intent_candidate",
        bool(intent.get("credential_intent_candidate"))
        and not ((gambling_surface or gate_surface) and not has_sensitive_form and not suspicious_delivery),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "credential_theft",
        4,
        "otp_intent_candidate",
        bool(intent.get("otp_intent_candidate")) and not (gate_surface and not has_sensitive_form and not suspicious_delivery),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "pii_kyc_harvesting",
        8,
        "personal_info_intent_candidate",
        bool(intent.get("personal_info_intent_candidate")),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "malware_or_fake_download",
        8,
        "download_intent_candidate",
        bool(intent.get("download_intent_candidate"))
        and not (gambling_surface and not forms.get("off_domain_form_action") and not network.get("post_to_third_party")),
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "fake_support_or_contact_diversion",
        6,
        "social_engineering_language_with_contact_brand",
        bool(intent.get("social_engineering_language_candidate")) and has_contact_brand,
    )
    add_vote(
        primary_votes,
        primary_reasons,
        "credential_theft",
        3,
        "brand_mismatch_with_sensitive_intent",
        bool(
            mismatch
            and (
                intent.get("credential_intent_candidate")
                or intent.get("otp_intent_candidate")
                or intent.get("payment_intent_candidate")
                or intent.get("wallet_connect_intent_candidate")
            )
        ),
    )

    if primary_votes:
        primary_label, primary_confidence, primary_rules = choose_candidate(
            primary_votes,
            primary_reasons,
            fallback_label="uncertain",
            fallback_reason="insufficient_primary_signal",
            fallback_confidence=0.2,
        )
    else:
        low_risk_benign = (
            risk_level == "low"
            and not mismatch
            and not evasion.get("anti_bot_or_cloaking_candidate")
            and not forms.get("off_domain_form_action")
            and not routing.get("no_early_stop_candidate")
        )
        primary_label = "benign" if low_risk_benign else "uncertain"
        primary_confidence = 0.3 if low_risk_benign else 0.2
        primary_rules = ["low_risk_no_high_intent_signals"] if low_risk_benign else ["insufficient_primary_signal"]

    scenario_votes: Dict[str, int] = {}
    scenario_reasons: Dict[str, List[str]] = {}
    add_vote(scenario_votes, scenario_reasons, "logistics_delivery", 8, "brand_logistics_delivery", bool({"dhl", "fedex", "ups"} & claimed_brands))
    add_vote(scenario_votes, scenario_reasons, "payment_platform", 8, "brand_payment_platform", bool({"paypal", "stripe", "alipay"} & claimed_brands))
    add_vote(scenario_votes, scenario_reasons, "crypto_web3", 9, "wallet_connect_or_crypto_brand", bool(intent.get("wallet_connect_intent_candidate") or ({"binance", "coinbase"} & claimed_brands)))
    add_vote(scenario_votes, scenario_reasons, "enterprise_mail_cloud", 7, "brand_enterprise_mail_cloud", bool({"microsoft", "google"} & claimed_brands))
    add_vote(scenario_votes, scenario_reasons, "ecommerce_retail", 6, "brand_ecommerce_retail", bool({"amazon"} & claimed_brands))
    add_vote(scenario_votes, scenario_reasons, "social_media", 6, "brand_social_media", bool({"meta", "telegram"} & claimed_brands))
    add_vote(scenario_votes, scenario_reasons, "tech_support", 6, "contact_diversion_signal", primary_label == "fake_support_or_contact_diversion")
    add_vote(scenario_votes, scenario_reasons, "job_recruitment", 5, "pii_without_brand_and_page_stage_other", bool(intent.get("personal_info_intent_candidate") and not claimed_brands and page_stage == "other"))
    add_vote(scenario_votes, scenario_reasons, "payment_platform", 4, "payment_page_stage", page_stage == "payment")

    scenario_label, scenario_confidence, scenario_rules = choose_candidate(
        scenario_votes,
        scenario_reasons,
        fallback_label="other",
        fallback_reason="no_specific_vertical_signal",
        fallback_confidence=0.25,
    )

    narrative_tags: List[str] = []
    if mismatch and brand.get("brand_claim_present_candidate"):
        narrative_tags.append("brand_impersonation")
    if intent.get("social_engineering_language_candidate"):
        narrative_tags.append("customer_service_narrative")
    if intent.get("urgency_or_threat_language_candidate"):
        narrative_tags.append("urgency_or_loss_framing")
    if scenario_label == "crypto_web3" and intent.get("wallet_connect_intent_candidate"):
        narrative_tags.append("giveaway_airdrop_narrative")

    evidence_tags: List[str] = []
    if forms.get("has_password") or intent.get("credential_intent_candidate"):
        evidence_tags.append("credential_form_present")
    if forms.get("has_card") or intent.get("payment_intent_candidate"):
        evidence_tags.append("payment_form_present")
    if intent.get("wallet_connect_intent_candidate"):
        evidence_tags.append("wallet_connect_present")
    if intent.get("download_intent_candidate"):
        evidence_tags.append("download_prompt_present")
    if primary_label == "fake_support_or_contact_diversion" or has_contact_brand:
        evidence_tags.append("contact_redirect_present")
    if gambling_surface:
        evidence_tags.append("specialized_gambling_surface")
    if adult_surface:
        evidence_tags.append("specialized_adult_surface")
    if specialized.get("possible_age_gate_surface"):
        evidence_tags.append("adult_age_gate_surface")

    evasion_tags: List[str] = []
    if evasion.get("captcha_present_candidate") or page_stage == "verification":
        evasion_tags.append("gate_or_verification_present")
    if evasion.get("needs_interaction_candidate"):
        evasion_tags.append("requires_interaction_to_reveal")
    if evasion.get("variant_failed_candidate"):
        evasion_tags.append("blank_or_sparse_initial_page")
    if evasion.get("dynamic_redirect_candidate") or network.get("too_many_redirects"):
        evasion_tags.append("redirect_chain_present")
    if gate_surface:
        evasion_tags.append("specialized_gate_surface")

    ecosystem_tags: List[str] = []
    if scenario_label == "crypto_web3" and primary_label in {
        "wallet_drain_or_web3_approval_fraud",
        "fake_support_or_contact_diversion",
    }:
        ecosystem_tags.append("illicit_service_content")

    threat_taxonomy_v1 = {
        "primary_threat_label_candidate": primary_label,
        "primary_threat_label_confidence": primary_confidence,
        "primary_threat_label_rules": primary_rules,
        "scenario_label_candidate": scenario_label,
        "scenario_label_confidence": scenario_confidence,
        "scenario_label_rules": scenario_rules,
        "narrative_tags_candidate": sorted(set(narrative_tags)),
        "evidence_tags_candidate": sorted(set(evidence_tags)),
        "evasion_tags_candidate": sorted(set(evasion_tags)),
        "ecosystem_tags_candidate": sorted(set(ecosystem_tags)),
        "taxonomy_source": "rule_derived_from_auto_labels",
        "taxonomy_review_status": "weak_candidate_only",
    }

    escalate_l2 = any([
        brand.get("domain_brand_consistency_candidate") == "mismatch" and intent.get("credential_intent_candidate"),
        intent.get("payment_intent_candidate"),
        intent.get("wallet_connect_intent_candidate"),
        evasion.get("anti_bot_or_cloaking_candidate"),
        evasion.get("needs_interaction_candidate"),
        forms.get("off_domain_form_action"),
        (risk.get("risk_level_weak") in {"high", "critical"}),
        routing.get("need_l2_candidate"),
    ])
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_utc_iso(),
        "rule_flags": {
            "escalate_to_l2_candidate": escalate_l2,
            "no_early_stop_candidate": bool(routing.get("no_early_stop_candidate")),
            "need_text_semantic_candidate": bool(routing.get("need_text_semantic_candidate")),
            "need_vision_candidate": bool(routing.get("need_vision_candidate")),
            "need_l2_candidate": bool(routing.get("need_l2_candidate")),
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
            "specialized_surface_family_candidates": unique_keep_order(specialized.get("specialized_surface_family_candidates") or []),
            "specialized_routing_reason_codes": unique_keep_order(routing.get("routing_reason_codes") or []),
        },
        "review_priority": (
            "p0" if risk.get("risk_level_weak") == "critical"
            else "p1" if risk.get("risk_level_weak") == "high"
            else "p2" if risk.get("risk_level_weak") == "medium"
            else "p3"
        ),
        "threat_taxonomy_v1": threat_taxonomy_v1,
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
    html_rendered = read_html_payload_text(sample_dir, "html_rendered.json", max_chars=MAX_HTML_SCAN_CHARS)
    html_raw = ""
    if not html_rendered:
        html_raw = read_html_payload_text(sample_dir, "html_raw.json", max_chars=MAX_HTML_SCAN_CHARS)

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
        # Keep traversal deterministic for repeatable evaluation and auditing.
        for p in sorted(root.rglob("meta.json"), key=lambda x: str(x).lower()):
            sample_dir = p.parent
            if (sample_dir / "url.json").exists():
                yield sample_dir
