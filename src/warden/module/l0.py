"""Canonical L0 runtime logic for the current Warden auto-label pipeline.

This module is intentionally imported by the legacy auto-label script as an
internal implementation module so the external auto-label entrypoints can stay
stable while the active L0 logic lives outside the monolithic script body.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

_auto = sys.modules.get("Warden_auto_label_utils_brandlex")
if _auto is None:
    import Warden_auto_label_utils_brandlex as _auto  # type: ignore

MAX_HTML_SCAN_CHARS = _auto.MAX_HTML_SCAN_CHARS
MAX_TEXT_SCAN_CHARS = _auto.MAX_TEXT_SCAN_CHARS

LOGIN_KEYWORDS = _auto.LOGIN_KEYWORDS
VERIFY_KEYWORDS = _auto.VERIFY_KEYWORDS
PAYMENT_KEYWORDS = _auto.PAYMENT_KEYWORDS
WALLET_KEYWORDS = _auto.WALLET_KEYWORDS
WEB3_WALLET_KEYWORDS = _auto.WEB3_WALLET_KEYWORDS
PII_KEYWORDS = _auto.PII_KEYWORDS
URGENCY_KEYWORDS = _auto.URGENCY_KEYWORDS
CAPTCHA_KEYWORDS = _auto.CAPTCHA_KEYWORDS
DOWNLOAD_KEYWORDS = _auto.DOWNLOAD_KEYWORDS
TRANSITION_KEYWORDS = _auto.TRANSITION_KEYWORDS
SOCIAL_ENGINEERING_HINTS = _auto.SOCIAL_ENGINEERING_HINTS

GAMBLING_KEYWORDS = _auto.GAMBLING_KEYWORDS
GAMBLING_HIGH_CONFIDENCE_KEYWORDS = _auto.GAMBLING_HIGH_CONFIDENCE_KEYWORDS
GAMBLING_STRONG_TEXT_KEYWORDS = getattr(
    _auto,
    "GAMBLING_STRONG_TEXT_KEYWORDS",
    ["sportsbook", "live dealer", "cashier", "bet365", "博彩", "赌博", "賭博", "赌场", "賭場", "体育投注", "體育投注"],
)
GAMBLING_ACTION_KEYWORDS = getattr(
    _auto,
    "GAMBLING_ACTION_KEYWORDS",
    ["login", "log in", "sign in", "sign up", "register", "registration", "join now", "play now", "download app", "app download", "official website", "official mirror", "登录", "登入", "注册", "下注", "投注"],
)
GAMBLING_EDITORIAL_KEYWORDS = getattr(
    _auto,
    "GAMBLING_EDITORIAL_KEYWORDS",
    ["guide", "guides", "review", "reviews", "latest update", "latest news", "news", "insights", "about us", "contact", "advertiser disclosure", "responsible gambling", "gambling statistics", "statistics", "faq", "blog", "blogs", "community", "article"],
)
GAMBLING_BONUS_KEYWORDS = _auto.GAMBLING_BONUS_KEYWORDS
GAMBLING_STRONG_BONUS_KEYWORDS = getattr(_auto, "GAMBLING_STRONG_BONUS_KEYWORDS", GAMBLING_BONUS_KEYWORDS)
GAMBLING_INDONESIAN_TITLE_TOKENS = getattr(_auto, "GAMBLING_INDONESIAN_TITLE_TOKENS", ["togel", "bandar", "situs", "terpercaya", "resmi"])
GAMBLING_SCORE_HIGH_CONFIDENCE = getattr(_auto, "GAMBLING_SCORE_HIGH_CONFIDENCE", 8)
GAMBLING_SCORE_BET_DIGIT_HOST = getattr(_auto, "GAMBLING_SCORE_BET_DIGIT_HOST", 5)
GAMBLING_SCORE_DOMAIN_HINT = getattr(_auto, "GAMBLING_SCORE_DOMAIN_HINT", 4)
GAMBLING_SCORE_URL_HIT = getattr(_auto, "GAMBLING_SCORE_URL_HIT", 2)
GAMBLING_SCORE_TEXT_GE2 = getattr(_auto, "GAMBLING_SCORE_TEXT_GE2", 2)
GAMBLING_SCORE_TEXT_GE3 = getattr(_auto, "GAMBLING_SCORE_TEXT_GE3", 1)
GAMBLING_SCORE_TRANSACTIONAL = getattr(_auto, "GAMBLING_SCORE_TRANSACTIONAL", 2)
GAMBLING_SCORE_EDITORIAL_SUPPRESSION = getattr(_auto, "GAMBLING_SCORE_EDITORIAL_SUPPRESSION", -4)
GAMBLING_SCORE_BONUS_WITHOUT_TEXT = getattr(_auto, "GAMBLING_SCORE_BONUS_WITHOUT_TEXT", -3)
GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD = getattr(_auto, "GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD", 8)

ADULT_KEYWORDS = _auto.ADULT_KEYWORDS
ADULT_HIGH_CONFIDENCE_KEYWORDS = _auto.ADULT_HIGH_CONFIDENCE_KEYWORDS
ADULT_AGE_GATE_KEYWORDS = _auto.ADULT_AGE_GATE_KEYWORDS
ADULT_WEAK_TEXT_KEYWORDS = getattr(_auto, "ADULT_WEAK_TEXT_KEYWORDS", ["av", "nsfw", "erotic", "nude", "nudity", "anal"])
ADULT_WEAK_URL_KEYWORDS = getattr(_auto, "ADULT_WEAK_URL_KEYWORDS", ["av"])
ADULT_WEAK_AGE_GATE_KEYWORDS = getattr(_auto, "ADULT_WEAK_AGE_GATE_KEYWORDS", ["nsfw", "age verification", "adult only", "not safe for work"])
ADULT_DOMAIN_HINT_TOKENS = getattr(
    _auto,
    "ADULT_DOMAIN_HINT_TOKENS",
    ["porn", "xxx", "jav", "hentai", "bdsm", "milf", "bokep", "escort", "adult", "hookup", "brazzers", "xnxx"],
)
ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKENS = getattr(_auto, "ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKENS", ["jav", "porno", "avxxx"])

GATE_SURFACE_KEYWORDS = _auto.GATE_SURFACE_KEYWORDS
GATE_STRONG_KEYWORDS = _auto.GATE_STRONG_KEYWORDS
GATE_URL_KEYWORDS = getattr(_auto, "GATE_URL_KEYWORDS", ["loading", "verify", "verification", "captcha", "auth", "secure", "humancheck"])
GATE_SHORT_FLOW_KEYWORDS = getattr(_auto, "GATE_SHORT_FLOW_KEYWORDS", ["verificando", "loading", "loading...", "click here to continue", "click to continue", "please confirm to continue", "secure portal", "点击继续", "點擊繼續"])
GATE_IDENTITY_FLOW_KEYWORDS = getattr(_auto, "GATE_IDENTITY_FLOW_KEYWORDS", ["verify to sign", "verify your identity", "verification code", "copy code"])
SUSPICIOUS_URL_KEYWORDS = _auto.SUSPICIOUS_URL_KEYWORDS
KNOWN_JS_LIBS = _auto.KNOWN_JS_LIBS

sanitize_text = _auto.sanitize_text
normalize_url = _auto.normalize_url
detect_language_candidate = _auto.detect_language_candidate
contains_any = _auto.contains_any
hit_keywords = _auto.hit_keywords
unique_keep_order = _auto.unique_keep_order
normalize_url_keyword_blob = _auto.normalize_url_keyword_blob
has_gambling_domain_hint = _auto.has_gambling_domain_hint
has_bet_digit_host_pattern = _auto.has_bet_digit_host_pattern
_host = _auto._host
_netloc = _auto._netloc
_path = _auto._path
_is_ip_host = _auto._is_ip_host
get_etld1 = _auto.get_etld1
RE_SCRIPT_SRC = _auto.RE_SCRIPT_SRC
RE_VERSION = _auto.RE_VERSION

SPECIALIZED_TEXT_SCAN_SPECS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("gambling_text", tuple(unique_keep_order(GAMBLING_KEYWORDS)), 12),
    ("gambling_bonus", tuple(unique_keep_order(GAMBLING_BONUS_KEYWORDS)), 12),
    ("gambling_action", tuple(unique_keep_order(GAMBLING_ACTION_KEYWORDS)), 12),
    ("gambling_editorial", tuple(unique_keep_order(GAMBLING_EDITORIAL_KEYWORDS)), 12),
    ("adult_text", tuple(unique_keep_order(ADULT_KEYWORDS)), 12),
    ("adult_age", tuple(unique_keep_order(ADULT_AGE_GATE_KEYWORDS)), 8),
    ("gate_text", tuple(unique_keep_order(GATE_SURFACE_KEYWORDS)), 12),
)
SPECIALIZED_URL_SCAN_SPECS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("gambling_url", tuple(unique_keep_order(GAMBLING_KEYWORDS + GAMBLING_BONUS_KEYWORDS)), 12),
    ("adult_url", tuple(unique_keep_order(ADULT_KEYWORDS + ADULT_AGE_GATE_KEYWORDS)), 12),
    ("gate_url", tuple(unique_keep_order(GATE_URL_KEYWORDS)), 8),
)
SPECIALIZED_TEXT_SCAN_UNION = tuple(
    unique_keep_order([kw for _, keywords, _ in SPECIALIZED_TEXT_SCAN_SPECS for kw in keywords])
)
SPECIALIZED_URL_SCAN_UNION = tuple(
    unique_keep_order([kw for _, keywords, _ in SPECIALIZED_URL_SCAN_SPECS for kw in keywords])
)
GAMBLING_HIGH_CONFIDENCE_KEYWORD_SET = set(GAMBLING_HIGH_CONFIDENCE_KEYWORDS)
GAMBLING_STRONG_TEXT_KEYWORD_SET = set(GAMBLING_STRONG_TEXT_KEYWORDS)
GAMBLING_STRONG_BONUS_KEYWORD_SET = set(GAMBLING_STRONG_BONUS_KEYWORDS)
ADULT_HIGH_CONFIDENCE_KEYWORD_SET = set(ADULT_HIGH_CONFIDENCE_KEYWORDS)
ADULT_WEAK_TEXT_KEYWORD_SET = set(ADULT_WEAK_TEXT_KEYWORDS)
ADULT_WEAK_URL_KEYWORD_SET = set(ADULT_WEAK_URL_KEYWORDS)
ADULT_WEAK_AGE_GATE_KEYWORD_SET = set(ADULT_WEAK_AGE_GATE_KEYWORDS)
ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKEN_SET = set(ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKENS)
GATE_STRONG_KEYWORD_SET = set(GATE_STRONG_KEYWORDS)


def collect_keyword_hits_by_bucket(
    text: str,
    scan_specs: Tuple[Tuple[str, Tuple[str, ...], int], ...],
    union_keywords: Tuple[str, ...],
) -> Dict[str, List[str]]:
    hit_set = set(hit_keywords(text, union_keywords, limit=len(union_keywords)))
    out: Dict[str, List[str]] = {}
    for bucket_name, keywords, limit in scan_specs:
        out[bucket_name] = [kw for kw in keywords if kw in hit_set][:limit]
    return out


def has_adult_domain_hint(final_url: str) -> bool:
    host = _host(final_url)
    tokens = [tok for tok in re.split(r"[^a-z0-9]+", (host or "").lower()) if tok]
    for token in tokens:
        if token in ADULT_DOMAIN_HINT_TOKENS:
            return True
        if any(core in token for core in ADULT_DOMAIN_HINT_TOKENS):
            return True
    return False


def default_html_features() -> dict:
    return {
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


def summarize_forms(forms_json: Optional[dict]) -> dict:
    forms = []
    if isinstance(forms_json, dict):
        forms = forms_json.get("forms") or []
    forms = forms if isinstance(forms, list) else []

    type_counter: Counter = Counter()
    attr_counter: Counter = Counter()
    action_domains: List[str] = []
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
            blob = " ".join(
                [
                    inp_type,
                    str(inp.get("name") or ""),
                    str(inp.get("id") or ""),
                    str(inp.get("autocomplete") or ""),
                    str(inp.get("placeholder") or ""),
                    str(inp.get("aria_label") or ""),
                ]
            ).lower()
            for flag, kws in {
                "email_like": ["mail", "email", "e-mail"],
                "phone_like": ["phone", "mobile", "tel"],
                "otp_like": ["otp", "one-time", "2fa", "mfa"],
                "user_like": ["user", "login", "account"],
                "name_like": ["name", "fullname"],
                "address_like": ["address"],
                "card_like": ["card", "cvv", "expiry", "exp"],
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


def summarize_html_features(html_text: str, final_url: str = "") -> dict:
    del final_url
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


def derive_safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def prepare_l0_inputs(
    *,
    input_url: str,
    final_url: str,
    visible_text: str,
    forms_json: Optional[dict],
    net_summary: Optional[dict],
    html_rendered: str = "",
    html_raw: str = "",
    page_title: str = "",
) -> dict:
    del html_rendered, html_raw
    final_url = normalize_url(final_url)
    input_url = normalize_url(input_url)
    raw_visible_text = sanitize_text(visible_text or "", MAX_TEXT_SCAN_CHARS)
    visible_text = sanitize_text((page_title or "") + "\n" + (visible_text or ""), MAX_TEXT_SCAN_CHARS)

    url_features = summarize_url(final_url, input_url)
    forms_summary = summarize_forms(forms_json)
    top_etld1 = url_features.get("etld1") or ""
    net_features = summarize_network(net_summary, top_etld1)
    html_features = default_html_features()
    forms_summary["off_domain_form_action"] = any(
        d and top_etld1 and d != top_etld1 for d in (forms_summary.get("action_domains") or [])
    )
    return {
        "input_url": input_url,
        "final_url": final_url,
        "raw_visible_text": raw_visible_text,
        "visible_text": visible_text,
        "url_features": url_features,
        "forms_summary": forms_summary,
        "net_features": net_features,
        "html_features": html_features,
    }


def derive_specialized_surface_signals(
    final_url: str,
    text: str,
    title_text: str,
    forms_summary: dict,
    html_features: dict,
    evasion_signals: dict,
) -> dict:
    del html_features
    text_low = (text or "").lower()
    title_low = (title_text or "").lower()
    url_blob = normalize_url_keyword_blob(final_url)
    text_compact = " ".join(text_low.split()).strip()

    text_scan_hits = collect_keyword_hits_by_bucket(text_low, SPECIALIZED_TEXT_SCAN_SPECS, SPECIALIZED_TEXT_SCAN_UNION)
    url_scan_hits = collect_keyword_hits_by_bucket(url_blob, SPECIALIZED_URL_SCAN_SPECS, SPECIALIZED_URL_SCAN_UNION)

    gambling_text_hits = text_scan_hits["gambling_text"]
    gambling_url_hits = url_scan_hits["gambling_url"]
    gambling_bonus_hits = text_scan_hits["gambling_bonus"]
    gambling_strong_bonus_hits = [kw for kw in gambling_bonus_hits if kw in GAMBLING_STRONG_BONUS_KEYWORD_SET]
    gambling_strong_text_hits = [kw for kw in gambling_text_hits if kw in GAMBLING_STRONG_TEXT_KEYWORD_SET]
    gambling_action_hits = text_scan_hits["gambling_action"]
    gambling_editorial_hits = text_scan_hits["gambling_editorial"]
    gambling_indonesian_title_hits = [kw for kw in GAMBLING_INDONESIAN_TITLE_TOKENS if kw in title_low]
    gambling_domain_hint = has_gambling_domain_hint(final_url)
    gambling_bet_digit_host = has_bet_digit_host_pattern(final_url)

    adult_text_hits = text_scan_hits["adult_text"]
    adult_url_hits = url_scan_hits["adult_url"]
    adult_age_hits = text_scan_hits["adult_age"]
    adult_strong_text_hits = [kw for kw in adult_text_hits if kw not in ADULT_WEAK_TEXT_KEYWORD_SET]
    adult_strong_url_hits = [kw for kw in adult_url_hits if kw not in ADULT_WEAK_URL_KEYWORD_SET]
    adult_strong_age_hits = [kw for kw in adult_age_hits if kw not in ADULT_WEAK_AGE_GATE_KEYWORD_SET]
    adult_domain_hint = has_adult_domain_hint(final_url)
    adult_domain_single_strong_recovery = bool(
        len(adult_strong_text_hits) == 1
        and adult_domain_hint
        and adult_strong_text_hits[0] in ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKEN_SET
    )

    gate_text_hits = text_scan_hits["gate_text"]
    gate_url_hits = url_scan_hits["gate_url"]
    gambling_high_confidence_hit = bool(set(gambling_text_hits + gambling_url_hits) & GAMBLING_HIGH_CONFIDENCE_KEYWORD_SET)
    adult_high_confidence_hit = bool(set(adult_text_hits + adult_url_hits) & ADULT_HIGH_CONFIDENCE_KEYWORD_SET)
    has_sensitive_form = bool(
        forms_summary.get("has_password")
        or forms_summary.get("has_otp")
        or forms_summary.get("has_card")
    )
    form_count = derive_safe_int(forms_summary.get("form_count"))

    gambling_weighted_score = 0
    gambling_weighted_score_reasons: List[str] = []

    def add_gambling(points: int, reason: str, cond: bool) -> None:
        nonlocal gambling_weighted_score
        if cond:
            gambling_weighted_score += points
            gambling_weighted_score_reasons.append(reason)

    add_gambling(GAMBLING_SCORE_HIGH_CONFIDENCE, "high_confidence_keyword", gambling_high_confidence_hit)
    add_gambling(GAMBLING_SCORE_BET_DIGIT_HOST, "bet_digit_host_pattern", gambling_bet_digit_host)
    add_gambling(GAMBLING_SCORE_DOMAIN_HINT, "gambling_domain_hint", gambling_domain_hint)
    add_gambling(GAMBLING_SCORE_URL_HIT * min(2, len(gambling_url_hits)), "gambling_url_hits", bool(gambling_url_hits))
    add_gambling(GAMBLING_SCORE_TEXT_GE2, "gambling_text_ge2", len(gambling_text_hits) >= 2)
    add_gambling(GAMBLING_SCORE_TEXT_GE3, "gambling_text_ge3", len(gambling_text_hits) >= 3)
    add_gambling(
        GAMBLING_SCORE_TRANSACTIONAL,
        "gambling_transactional_support",
        bool(gambling_action_hits) or has_sensitive_form or form_count > 0,
    )
    add_gambling(
        GAMBLING_SCORE_EDITORIAL_SUPPRESSION,
        "editorial_or_review_suppression",
        bool(gambling_editorial_hits) and not gambling_high_confidence_hit and not gambling_domain_hint,
    )
    add_gambling(
        GAMBLING_SCORE_BONUS_WITHOUT_TEXT,
        "bonus_without_gambling_text",
        bool(gambling_bonus_hits) and not gambling_text_hits and not gambling_domain_hint,
    )

    possible_gambling_lure = bool(
        gambling_high_confidence_hit
        or (len(gambling_strong_text_hits) >= 2 and (bool(gambling_action_hits) or has_sensitive_form or gambling_domain_hint))
        or (gambling_weighted_score >= GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD)
        or (
            gambling_domain_hint
            and gambling_bet_digit_host
            and (bool(gambling_bonus_hits) or bool(gambling_action_hits) or len(gambling_text_hits) >= 1)
        )
        or (
            bool(gambling_indonesian_title_hits)
            and gambling_domain_hint
            and (len(gambling_text_hits) >= 1 or bool(gambling_bonus_hits))
        )
    )
    possible_bonus_or_betting_induction = bool(
        gambling_bonus_hits
        and (
            possible_gambling_lure
            or gambling_domain_hint
            or bool(gambling_action_hits)
            or len(gambling_text_hits) >= 2
        )
    )

    possible_adult_lure = bool(
        adult_high_confidence_hit
        or (
            adult_domain_hint
            and (
                len(adult_strong_text_hits) >= 1
                or len(adult_strong_url_hits) >= 1
                or adult_domain_single_strong_recovery
            )
        )
        or (
            len(adult_strong_text_hits) >= 3
            and (adult_domain_hint or bool(adult_strong_url_hits) or bool(forms_summary.get("form_count")))
        )
        or (
            len(adult_strong_text_hits) >= 2
            and adult_domain_hint
            and (bool(adult_strong_url_hits) or len(adult_strong_age_hits) >= 1)
        )
    )
    possible_age_gate_surface = bool(
        len(adult_strong_age_hits) >= 1
        and (possible_adult_lure or adult_domain_hint or len(adult_strong_url_hits) >= 1)
    )

    gate_strong_hits = [kw for kw in gate_text_hits if kw in GATE_STRONG_KEYWORD_SET]
    gate_short_flow_hit = contains_any(text_compact, GATE_SHORT_FLOW_KEYWORDS)
    gate_identity_flow_hit = contains_any(text_compact, GATE_IDENTITY_FLOW_KEYWORDS)
    possible_challenge_surface = bool(
        gate_strong_hits
        or (evasion_signals.get("captcha_present_candidate") and (gate_text_hits or gate_url_hits))
        or (gate_short_flow_hit and (gate_url_hits or evasion_signals.get("anti_bot_or_cloaking_candidate")))
    )
    possible_gate_or_evasion = bool(
        possible_challenge_surface
        or (
            (len(gate_text_hits) >= 2 or bool(gate_url_hits))
            and (
                evasion_signals.get("anti_bot_or_cloaking_candidate")
                or evasion_signals.get("dynamic_redirect_candidate")
                or evasion_signals.get("needs_interaction_candidate")
                or gate_identity_flow_hit
            )
        )
    )

    specialized_fast_resolution_candidate = bool(
        (possible_gambling_lure and gambling_high_confidence_hit and not gambling_editorial_hits)
        or (possible_adult_lure and (adult_high_confidence_hit or adult_domain_single_strong_recovery))
        or (possible_gate_or_evasion and possible_challenge_surface and bool(gate_strong_hits))
    )

    return {
        "possible_gambling_lure": possible_gambling_lure,
        "possible_bonus_or_betting_induction": possible_bonus_or_betting_induction,
        "possible_adult_lure": possible_adult_lure,
        "possible_age_gate_surface": possible_age_gate_surface,
        "possible_gate_or_evasion": possible_gate_or_evasion,
        "possible_challenge_surface": possible_challenge_surface,
        "specialized_fast_resolution_candidate": specialized_fast_resolution_candidate,
        "gambling_weighted_score": gambling_weighted_score,
        "gambling_weighted_score_reasons": unique_keep_order(gambling_weighted_score_reasons),
        "matched_keywords": {
            "gambling_text": gambling_text_hits,
            "gambling_url": gambling_url_hits,
            "gambling_bonus": gambling_bonus_hits,
            "gambling_action": gambling_action_hits,
            "gambling_editorial": gambling_editorial_hits,
            "gambling_title": gambling_indonesian_title_hits,
            "adult_text": adult_text_hits,
            "adult_url": adult_url_hits,
            "adult_age": adult_age_hits,
            "gate_text": gate_text_hits,
            "gate_url": gate_url_hits,
        },
    }


def derive_text_observability_signals(
    raw_visible_text: str,
    page_title: str,
    html_features: dict,
    net_features: dict,
    evasion_signals: dict,
) -> dict:
    del html_features
    raw_visible_text = sanitize_text(raw_visible_text or "", MAX_TEXT_SCAN_CHARS)
    page_title = sanitize_text(page_title or "", 512)
    dynamic_page_candidate = bool(
        derive_safe_int(net_features.get("request_total")) >= 20
        or net_features.get("too_many_redirects")
        or net_features.get("many_third_party")
    )
    empty_visible_text_candidate = not raw_visible_text
    empty_visible_text_requires_l1 = bool(empty_visible_text_candidate)
    return {
        "raw_visible_text_len": len(raw_visible_text),
        "page_title_present": bool(page_title),
        "dynamic_page_candidate": dynamic_page_candidate,
        "empty_visible_text_candidate": empty_visible_text_candidate,
        "empty_visible_text_requires_l1": empty_visible_text_requires_l1,
        "empty_visible_text_support_signals": unique_keep_order(
            [
                "page_title_present" if page_title else "",
                "dynamic_page_candidate" if dynamic_page_candidate else "",
                "high_request_count" if derive_safe_int(net_features.get("request_total")) >= 20 else "",
                "needs_interaction_candidate" if evasion_signals.get("needs_interaction_candidate") else "",
                "anti_bot_or_cloaking_candidate" if evasion_signals.get("anti_bot_or_cloaking_candidate") else "",
                "too_many_redirects" if net_features.get("too_many_redirects") else "",
                "many_third_party" if net_features.get("many_third_party") else "",
            ]
        ),
    }


def derive_l0_routing_hints(
    specialized_signals: dict,
    intent_signals: dict,
    evasion_signals: dict,
    forms_summary: dict,
    net_features: dict,
    text_observability_signals: Optional[dict] = None,
) -> dict:
    text_observability_signals = text_observability_signals or {}
    empty_visible_text_requires_l1 = bool(text_observability_signals.get("empty_visible_text_requires_l1"))
    specialized_fast_resolution = bool(specialized_signals.get("specialized_fast_resolution_candidate"))
    no_early_stop_candidate = any(
        [
            specialized_signals.get("possible_gambling_lure"),
            specialized_signals.get("possible_adult_lure"),
            specialized_signals.get("possible_age_gate_surface"),
            specialized_signals.get("possible_gate_or_evasion"),
            empty_visible_text_requires_l1,
        ]
    )
    adult_url_only = bool(
        specialized_signals.get("possible_adult_lure")
        and (specialized_signals.get("matched_keywords") or {}).get("adult_url")
        and not (specialized_signals.get("matched_keywords") or {}).get("adult_text")
    )
    need_text_semantic_candidate = bool(
        not specialized_fast_resolution
        or empty_visible_text_requires_l1
    )
    need_vision_candidate = adult_url_only
    need_l2_candidate = bool(
        (
            specialized_signals.get("possible_gate_or_evasion")
            and (
                evasion_signals.get("anti_bot_or_cloaking_candidate")
                or evasion_signals.get("variant_failed_candidate")
                or evasion_signals.get("dynamic_redirect_candidate")
            )
        )
        or (
            specialized_signals.get("possible_gambling_lure")
            and (
                bool(forms_summary.get("has_card"))
                or bool(net_features.get("post_to_third_party"))
                or bool(forms_summary.get("off_domain_form_action"))
            )
        )
        or (
            specialized_signals.get("possible_adult_lure")
            and (
                intent_signals.get("download_intent_candidate")
                or net_features.get("too_many_redirects")
                or net_features.get("post_to_third_party")
            )
        )
    )

    routing_reason_codes: List[str] = []
    if no_early_stop_candidate:
        routing_reason_codes.append("specialized_surface_forbid_early_stop")
    if specialized_signals.get("possible_gambling_lure"):
        routing_reason_codes.append("gambling_surface_requires_text_semantic")
    if specialized_signals.get("possible_adult_lure"):
        routing_reason_codes.append("adult_surface_requires_text_semantic")
    if specialized_signals.get("possible_gate_or_evasion"):
        routing_reason_codes.append("gate_surface_requires_cautious_routing")
    if need_vision_candidate:
        routing_reason_codes.append("adult_url_only_signal_needs_vision")
    if need_l2_candidate:
        routing_reason_codes.append("specialized_surface_needs_l2")
    if empty_visible_text_requires_l1:
        routing_reason_codes.append("raw_visible_text_missing_requires_l1")
        if text_observability_signals.get("dynamic_page_candidate"):
            routing_reason_codes.append("dynamic_page_support_present")
        for support in text_observability_signals.get("empty_visible_text_support_signals") or []:
            routing_reason_codes.append(f"empty_visible_text_support:{support}")
    if need_text_semantic_candidate and not any(
        [
            specialized_signals.get("possible_gambling_lure"),
            specialized_signals.get("possible_adult_lure"),
            specialized_signals.get("possible_age_gate_surface"),
            specialized_signals.get("possible_gate_or_evasion"),
            empty_visible_text_requires_l1,
        ]
    ):
        routing_reason_codes.append("default_non_specialized_l1_path")

    return {
        "no_early_stop_candidate": no_early_stop_candidate,
        "need_text_semantic_candidate": need_text_semantic_candidate,
        "need_vision_candidate": need_vision_candidate,
        "need_l2_candidate": need_l2_candidate,
        "routing_reason_codes": unique_keep_order(routing_reason_codes),
    }


def derive_intent_signals(
    text: str,
    forms_summary: dict,
    html_features: dict,
    specialized_signals: Optional[dict] = None,
) -> dict:
    text_low = (text or "").lower()
    input_types = forms_summary.get("input_types") or {}
    attr_hints = forms_summary.get("input_attr_hints") or {}
    specialized_signals = specialized_signals or {}
    gambling_surface = bool(specialized_signals.get("possible_gambling_lure"))
    adult_surface = bool(specialized_signals.get("possible_adult_lure"))
    gate_surface = bool(specialized_signals.get("possible_gate_or_evasion"))
    has_sensitive_form = bool(forms_summary.get("has_password") or forms_summary.get("has_otp") or forms_summary.get("has_card"))
    credential_text_hit = contains_any(text_low, LOGIN_KEYWORDS)
    if (gambling_surface or adult_surface) and not has_sensitive_form and attr_hints.get("user_like", 0) <= 0:
        credential_text_hit = False
    credential = (
        bool(forms_summary.get("has_password"))
        or input_types.get("password", 0) > 0
        or credential_text_hit
        or attr_hints.get("user_like", 0) > 0
    )
    otp_text_hit = contains_any(text_low, VERIFY_KEYWORDS)
    if (gate_surface or gambling_surface or adult_surface) and not (forms_summary.get("has_otp") or attr_hints.get("otp_like", 0) > 0):
        otp_text_hit = False
    otp = bool(forms_summary.get("has_otp")) or attr_hints.get("otp_like", 0) > 0 or otp_text_hit
    payment_text_hit = contains_any(text_low, PAYMENT_KEYWORDS)
    if gambling_surface and not (forms_summary.get("has_card") or attr_hints.get("card_like", 0) > 0):
        payment_text_hit = False
    payment = bool(forms_summary.get("has_card")) or attr_hints.get("card_like", 0) > 0 or payment_text_hit
    wallet = contains_any(text_low, WEB3_WALLET_KEYWORDS)
    pii_text_hit = contains_any(text_low, PII_KEYWORDS)
    if (adult_surface or gambling_surface) and not (attr_hints.get("name_like", 0) > 0 or attr_hints.get("address_like", 0) > 0):
        pii_text_hit = False
    pii = attr_hints.get("name_like", 0) > 0 or attr_hints.get("address_like", 0) > 0 or pii_text_hit
    urgency = contains_any(text_low, URGENCY_KEYWORDS)
    social_hint = contains_any(text_low, SOCIAL_ENGINEERING_HINTS)
    download_text_hit = contains_any(text_low, DOWNLOAD_KEYWORDS)
    if gambling_surface and not html_features.get("download_evidence"):
        download_text_hit = False
    return {
        "credential_intent_candidate": credential,
        "otp_intent_candidate": otp,
        "payment_intent_candidate": payment,
        "wallet_connect_intent_candidate": wallet,
        "personal_info_intent_candidate": pii,
        "urgency_or_threat_language_candidate": urgency,
        "social_engineering_language_candidate": social_hint,
        "download_intent_candidate": bool(html_features.get("download_evidence")) or download_text_hit,
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


def derive_l0_outputs(
    *,
    final_url: str,
    visible_text: str,
    raw_visible_text: str,
    page_title: str,
    forms_summary: dict,
    net_features: dict,
    html_features: dict,
    diff_summary: Optional[dict],
    brand_signals: dict,
    url_features: dict,
) -> dict:
    evasion_signals = derive_evasion_signals(visible_text, html_features, diff_summary, net_features)
    text_observability_signals = derive_text_observability_signals(
        raw_visible_text=raw_visible_text,
        page_title=page_title,
        html_features=html_features,
        net_features=net_features,
        evasion_signals=evasion_signals,
    )
    specialized_surface_signals = derive_specialized_surface_signals(
        final_url=final_url,
        text=visible_text,
        title_text=page_title,
        forms_summary=forms_summary,
        html_features=html_features,
        evasion_signals=evasion_signals,
    )
    intent_signals = derive_intent_signals(visible_text, forms_summary, html_features, specialized_surface_signals)
    page_stage_candidate = derive_page_stage(intent_signals, forms_summary, visible_text)
    l0_routing_hints = derive_l0_routing_hints(
        specialized_signals=specialized_surface_signals,
        intent_signals=intent_signals,
        evasion_signals=evasion_signals,
        forms_summary=forms_summary,
        net_features=net_features,
        text_observability_signals=text_observability_signals,
    )
    score, reasons = compute_weak_risk(
        url_features=url_features,
        forms_summary=forms_summary,
        brand_signals=brand_signals,
        intent_signals=intent_signals,
        evasion_signals=evasion_signals,
        net_features=net_features,
        html_features=html_features,
    )
    return {
        "page_stage_candidate": page_stage_candidate,
        "language_candidate": detect_language_candidate(visible_text),
        "intent_signals": intent_signals,
        "evasion_signals": evasion_signals,
        "specialized_surface_signals": specialized_surface_signals,
        "l0_routing_hints": l0_routing_hints,
        "risk_outputs": {
            "risk_score_weak": score,
            "risk_level_weak": risk_level_from_score(score),
            "risk_reasons": reasons,
        },
    }


__all__ = [
    "default_html_features",
    "prepare_l0_inputs",
    "derive_specialized_surface_signals",
    "derive_text_observability_signals",
    "derive_l0_routing_hints",
    "derive_intent_signals",
    "derive_page_stage",
    "derive_evasion_signals",
    "derive_safe_int",
    "compute_weak_risk",
    "risk_level_from_score",
    "derive_l0_outputs",
]
