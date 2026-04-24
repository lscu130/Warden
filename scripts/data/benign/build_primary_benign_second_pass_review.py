#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# operator: Codex; task: primary-benign-second-pass-review-manifest; date: 2026-04-24

"""Build a second-pass review manifest for primary benign candidates.

This script is intentionally read-only for sample directories. It emits routing
and review suggestions, not manual gold labels or final dataset admission.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import discover_sample_dirs, ensure_dir, now_utc_iso, read_json, relpath_or_abs, write_json, write_jsonl
from scripts.data.common.runtime_data_root import data_path, get_data_root

FILE_URL = "url.json"
FILE_AUTO_LABELS = "auto_labels.json"
FILE_RULE_LABELS = "rule_labels.json"
FILE_FORMS = "forms.json"
FILE_NET_SUMMARY = "net_summary.json"
FILE_VISIBLE_TEXT = "visible_text.txt"
FILE_SCREENSHOT_VIEWPORT = "screenshot_viewport.png"
FILE_HTML_RENDERED = "html_rendered.json"
FILE_HTML_RAW = "html_raw.json"

DEFAULT_INPUT_ROOTS = [data_path("raw", "benign", "benign")]
DEFAULT_OUTPUT_DIR = data_path("reviewed", "benign_second_pass")
DEFAULT_MANIFEST_NAME = "primary_benign_second_pass_review_manifest.jsonl"
DEFAULT_SUMMARY_NAME = "primary_benign_second_pass_summary.json"

ADULT_RE = re.compile(
    r"\b("
    r"adult|porn|porno|pornhub|xvideos|xnxx|xxx|sex|sexy|nude|nudes|hentai|escort|camgirl|camgirls|onlyfans|brazzers|erotic"
    r")\b",
    re.IGNORECASE,
)
GAMBLING_RE = re.compile(
    r"\b("
    r"casino|betting|sportsbook|bookmaker|gambling|gamble|lottery|slots?|poker|blackjack|roulette|baccarat|toto|togel|jackpot|1xbet|1win|stake"
    r")\b",
    re.IGNORECASE,
)
GATE_RE = re.compile(
    r"\b("
    r"captcha|verify you are human|checking your browser|just a moment|attention required|cloudflare|challenge|anti[- ]?bot|enable javascript"
    r")\b",
    re.IGNORECASE,
)
DOWNLOAD_RE = re.compile(
    r"\b("
    r"download|installer|apk|extension|plugin|update required|browser update|software update|setup\.exe|\.apk|\.dmg|\.msi"
    r")\b",
    re.IGNORECASE,
)
LOGIN_RE = re.compile(
    r"\b("
    r"login|log in|sign in|signin|password|passcode|otp|two[- ]?factor|2fa|account verification|verify account|reset password"
    r")\b",
    re.IGNORECASE,
)
PAYMENT_RE = re.compile(
    r"\b("
    r"payment|pay now|checkout|billing|invoice|card number|credit card|cvv|bank account|wire transfer|fee|subscription"
    r")\b",
    re.IGNORECASE,
)
WEB3_RE = re.compile(
    r"\b("
    r"wallet|connect wallet|seed phrase|recovery phrase|private key|metamask|walletconnect|airdrop|claim token|mint nft|approve transaction"
    r")\b",
    re.IGNORECASE,
)
CLONE_RE = re.compile(r"\b(clone|template|replica|demo|phishing simulation|training page)\b", re.IGNORECASE)
SUPPORT_DIVERSION_RE = re.compile(
    r"\b("
    r"help desk|customer service|whatsapp|telegram|live chat|toll[- ]?free|refund support|account support|wallet support|recovery support"
    r")\b",
    re.IGNORECASE,
)
SUPPORT_DIVERSION_CONTEXT_RE = re.compile(
    r"\b("
    r"refund|locked|suspended|verify|verification|account|wallet|password|seed phrase|recovery phrase|private key|urgent|limited time|security alert"
    r")\b",
    re.IGNORECASE,
)


def safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return read_json(path)
    except Exception as exc:
        return {"_read_error": repr(exc)}


def read_text_if_exists(path: Path, max_chars: int) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8-sig", errors="ignore")[:max_chars]
    except Exception:
        return ""


def nested_get(obj: Any, path: Sequence[str], default: Any = None) -> Any:
    cur = obj
    for key in path:
        if not isinstance(cur, Mapping) or key not in cur:
            return default
        cur = cur[key]
    return cur


def recursive_key_values(obj: Any, key_fragments: Sequence[str]) -> List[Any]:
    hits: List[Any] = []
    fragments = tuple(fragment.lower() for fragment in key_fragments)

    def walk(value: Any) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                key_lower = str(key).lower()
                if any(fragment in key_lower for fragment in fragments):
                    hits.append(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return hits


def any_truthy(values: Iterable[Any]) -> bool:
    for value in values:
        if isinstance(value, bool) and value:
            return True
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0:
            return True
        if isinstance(value, str) and value.strip().lower() in {"true", "yes", "y", "1", "high", "medium"}:
            return True
    return False


def host_from_url(url: str) -> str:
    return (urlparse(url).hostname or "").strip(".").lower()


def etld1_from_host(host: str) -> str:
    parts = host.split(".") if host else []
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def classify_content_warning(text_blob: str) -> str:
    adult = bool(ADULT_RE.search(text_blob))
    gambling = bool(GAMBLING_RE.search(text_blob))
    if adult and gambling:
        return "adult_and_gambling"
    if adult:
        return "adult"
    if gambling:
        return "gambling"
    return "none"


def forms_signals(forms: Any) -> Dict[str, Any]:
    signals = {
        "form_count": 0,
        "has_password": False,
        "has_otp": False,
        "has_card": False,
        "has_email": False,
        "has_submit": False,
    }
    if not isinstance(forms, Mapping):
        return signals
    form_items = forms.get("forms")
    if not isinstance(form_items, list):
        return signals
    signals["form_count"] = len(form_items)
    text = json.dumps(form_items, ensure_ascii=False).lower()
    signals["has_password"] = "password" in text or '"type": "password"' in text
    signals["has_otp"] = bool(re.search(r"\botp\b|one[- ]?time|verification code|2fa", text))
    signals["has_card"] = bool(re.search(r"card|cvv|cvc|expiry|expiration", text))
    signals["has_email"] = "email" in text or '"type": "email"' in text
    signals["has_submit"] = "submit" in text or "button" in text
    return signals


def build_record(sample_dir: Path, data_root: Path, text_max_chars: int) -> Dict[str, Any]:
    url_info = read_json_if_exists(sample_dir / FILE_URL)
    auto_labels = read_json_if_exists(sample_dir / FILE_AUTO_LABELS)
    rule_labels = read_json_if_exists(sample_dir / FILE_RULE_LABELS)
    forms = read_json_if_exists(sample_dir / FILE_FORMS)
    net_summary = read_json_if_exists(sample_dir / FILE_NET_SUMMARY)
    visible_text = read_text_if_exists(sample_dir / FILE_VISIBLE_TEXT, text_max_chars)

    url_info_map = url_info if isinstance(url_info, Mapping) else {}
    auto_map = auto_labels if isinstance(auto_labels, Mapping) else {}
    rule_map = rule_labels if isinstance(rule_labels, Mapping) else {}
    net_map = net_summary if isinstance(net_summary, Mapping) else {}

    input_url = safe_str(url_info_map.get("input_url")).strip()
    final_url = safe_str(url_info_map.get("final_url")).strip() or input_url
    host = host_from_url(final_url or input_url)
    etld1 = etld1_from_host(host)

    evidence_blob = "\n".join(
        [
            sample_dir.name,
            input_url,
            final_url,
            host,
            safe_str(nested_get(auto_map, ["url_features", "path"])),
            visible_text,
            json.dumps(rule_map, ensure_ascii=False) if rule_map else "",
        ]
    )

    form_flags = forms_signals(forms)
    auto_credential = bool(nested_get(auto_map, ["intent_signals", "credential_intent_candidate"], False))
    auto_otp = bool(nested_get(auto_map, ["intent_signals", "otp_intent_candidate"], False))
    auto_payment = bool(nested_get(auto_map, ["intent_signals", "payment_intent_candidate"], False))
    auto_wallet = bool(nested_get(auto_map, ["intent_signals", "wallet_connect_intent_candidate"], False))
    auto_download = bool(nested_get(auto_map, ["intent_signals", "download_intent_candidate"], False)) or bool(
        nested_get(auto_map, ["html_features", "download_evidence"], False)
    )
    auto_gate = any_truthy(recursive_key_values(auto_map, ["captcha", "challenge", "evasion", "cloak", "interaction"]))
    rule_gate = any_truthy(recursive_key_values(rule_map, ["gate", "evasion", "cloak", "challenge"]))
    rule_review = any_truthy(recursive_key_values(rule_map, ["manual_review", "review"]))
    rule_hard_negative = any_truthy(recursive_key_values(rule_map, ["hard_negative", "hard_negative_candidate"]))
    rule_hard_positive = any_truthy(recursive_key_values(rule_map, ["hard_positive", "hard_positive_candidate"]))
    rule_page_role_values = [safe_str(value).lower() for value in recursive_key_values(rule_map, ["page_role", "role_hint"])]
    rule_page_role_threat = any(any(token in value for token in ["login", "payment", "wallet", "download", "support"]) for value in rule_page_role_values)

    content_warning = classify_content_warning(evidence_blob)
    text_len = len(visible_text.strip())
    missing_files = [
        name
        for name in [FILE_URL, FILE_AUTO_LABELS, FILE_FORMS, FILE_NET_SUMMARY, FILE_VISIBLE_TEXT, FILE_SCREENSHOT_VIEWPORT]
        if not (sample_dir / name).exists()
    ]

    text_gate = bool(GATE_RE.search(evidence_blob))
    text_download = bool(DOWNLOAD_RE.search(evidence_blob))
    text_login = bool(LOGIN_RE.search(evidence_blob))
    text_payment = bool(PAYMENT_RE.search(evidence_blob))
    text_web3 = bool(WEB3_RE.search(evidence_blob))
    text_clone = bool(CLONE_RE.search(evidence_blob))
    text_support_diversion = bool(SUPPORT_DIVERSION_RE.search(evidence_blob)) and bool(SUPPORT_DIVERSION_CONTEXT_RE.search(evidence_blob))
    brand_claim_present = bool(nested_get(auto_map, ["brand_signals", "brand_claim_present_candidate"], False))
    brand_behavior_conflict = brand_claim_present and any(
        [form_flags["has_password"], form_flags["has_card"], text_login, text_payment, text_web3, text_download, text_support_diversion]
    )
    forms_text_conflict = form_flags["form_count"] > 0 and not any([text_login, text_payment, text_web3, text_support_diversion]) and text_len < 400

    strong_threat_behavior = any(
        [
            auto_credential,
            auto_otp,
            auto_payment,
            auto_wallet,
            auto_download,
            form_flags["has_password"],
            form_flags["has_otp"],
            form_flags["has_card"],
            text_login and form_flags["form_count"] > 0,
            text_web3,
            text_support_diversion,
            rule_hard_negative,
            rule_page_role_threat,
        ]
    )
    mixed_surface = any([text_login, text_payment, text_download, text_web3, brand_behavior_conflict, forms_text_conflict])
    gate_or_evasion = auto_gate or rule_gate or text_gate or safe_str(auto_map.get("page_stage_candidate")).lower() in {"gate", "evasion", "challenge"}
    sparse_or_incomplete = bool(missing_files) or text_len < 80
    screenshot_dependent = sparse_or_incomplete or (text_clone or text_web3 or text_download or text_login or text_payment) or (
        gate_or_evasion and text_len < 240
    )

    reason_codes: List[str] = []
    if content_warning != "none":
        reason_codes.append(f"content_warning:{content_warning}")
    if gate_or_evasion:
        reason_codes.append("auxiliary_candidate:gate_or_evasion")
    if strong_threat_behavior:
        reason_codes.append("threat_behavior_surface")
    if text_web3:
        reason_codes.append("mixed_surface:web3")
    if text_download or auto_download:
        reason_codes.append("mixed_surface:download")
    if text_login or auto_credential or form_flags["has_password"]:
        reason_codes.append("mixed_surface:login_or_credential")
    if text_payment or auto_payment or form_flags["has_card"]:
        reason_codes.append("mixed_surface:payment")
    if text_clone:
        reason_codes.append("mixed_surface:clone_or_demo")
    if text_support_diversion:
        reason_codes.append("mixed_surface:fake_support_or_contact_diversion")
    if brand_behavior_conflict:
        reason_codes.append("conflict:brand_shell_with_behavior_signal")
    if forms_text_conflict:
        reason_codes.append("conflict:forms_present_but_text_sparse_or_mismatched")
    if rule_hard_negative:
        reason_codes.append("rule_layer:hard_negative_candidate")
    if rule_hard_positive:
        reason_codes.append("rule_layer:hard_positive_candidate")
    if rule_page_role_threat:
        reason_codes.append("rule_layer:threat_page_role_hint")
    if sparse_or_incomplete:
        reason_codes.append("quality:sparse_or_missing_artifacts")
    if rule_review:
        reason_codes.append("rule_layer:manual_review_candidate")
    if not reason_codes:
        reason_codes.append("benign_purity:no_high_risk_surface_detected")

    if strong_threat_behavior:
        routing = "exclude"
    elif content_warning != "none":
        routing = "exclude"
    elif gate_or_evasion:
        routing = "aux_only"
    elif sparse_or_incomplete:
        routing = "uncertain"
    elif mixed_surface:
        routing = "uncertain"
    elif text_clone or rule_hard_positive:
        routing = "eval_main"
    else:
        routing = "train_main"

    needs_manual_review = bool(
        strong_threat_behavior
        or rule_review
        or rule_hard_negative
        or rule_page_role_threat
        or brand_behavior_conflict
        or forms_text_conflict
        or screenshot_dependent
        or routing == "uncertain"
        or (content_warning != "none" and (text_login or text_payment or text_web3 or text_download))
    )

    confidence = "medium"
    if routing == "train_main" and text_len >= 400 and not missing_files:
        confidence = "high"
    elif routing in {"exclude", "aux_only"} and (strong_threat_behavior or gate_or_evasion or content_warning != "none"):
        confidence = "medium"
    if sparse_or_incomplete:
        confidence = "low"

    return {
        "schema_version": "primary_benign_second_pass_review_v1",
        "sample_id": sample_dir.name,
        "sample_dir": relpath_or_abs(sample_dir, data_root),
        "source_bucket": relpath_or_abs(sample_dir.parent, data_root),
        "input_url": input_url,
        "final_url": final_url,
        "host": host,
        "etld1": etld1,
        "dataset_routing_suggestion": routing,
        "suggestion_confidence": confidence,
        "needs_manual_review": needs_manual_review,
        "requires_screenshot_review": bool(screenshot_dependent),
        "content_warning_candidate": content_warning,
        "reason_codes": reason_codes,
        "key_evidence": {
            "auto_label_hint": safe_str(auto_map.get("label_hint")).strip() or None,
            "auto_page_stage_candidate": safe_str(auto_map.get("page_stage_candidate")).strip() or None,
            "auto_risk_level_weak": safe_str(nested_get(auto_map, ["risk_outputs", "risk_level_weak"])).strip() or None,
            "form_count": form_flags["form_count"],
            "forms_has_password": form_flags["has_password"],
            "forms_has_otp": form_flags["has_otp"],
            "forms_has_card": form_flags["has_card"],
            "brand_claim_present_candidate": brand_claim_present,
            "rule_hard_negative_candidate": rule_hard_negative,
            "rule_hard_positive_candidate": rule_hard_positive,
            "rule_page_role_threat_hint": rule_page_role_threat,
            "visible_text_chars_read": text_len,
            "net_request_total": nested_get(net_map, ["request_total"], None),
            "third_party_domain_count": nested_get(auto_map, ["network_features", "third_party_domain_count"], None),
            "rule_labels_present": bool(rule_map),
            "missing_priority_files": missing_files,
        },
        "weak_label_warning": "auto_labels and rule_labels are evidence only; this record is not a manual gold label.",
    }


def summarize(rows: Sequence[Dict[str, Any]], args: argparse.Namespace, data_root: Path) -> Dict[str, Any]:
    route_counter = Counter(row["dataset_routing_suggestion"] for row in rows)
    warning_counter = Counter(row["content_warning_candidate"] for row in rows)
    reason_counter: Counter[str] = Counter()
    for row in rows:
        reason_counter.update(row.get("reason_codes", []))
    return {
        "schema_version": "primary_benign_second_pass_summary_v1",
        "generated_at_utc": now_utc_iso(),
        "data_root": str(data_root),
        "input_roots": [str(Path(root)) for root in args.input_roots],
        "sample_count": len(rows),
        "limit": args.limit,
        "routing_distribution": dict(sorted(route_counter.items())),
        "content_warning_distribution": dict(sorted(warning_counter.items())),
        "manual_review_count": sum(1 for row in rows if row["needs_manual_review"]),
        "screenshot_review_count": sum(1 for row in rows if row["requires_screenshot_review"]),
        "top_reason_codes": dict(reason_counter.most_common(30)),
        "note": "Suggestions are second-pass routing evidence, not manual gold labels or final dataset admission.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a primary benign second-pass review manifest.")
    parser.add_argument("--data-root", default=str(get_data_root()), help="active Warden data root")
    parser.add_argument("--input-roots", nargs="+", default=[str(path) for path in DEFAULT_INPUT_ROOTS], help="sample roots to scan")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUTPUT_DIR), help="output directory")
    parser.add_argument("--manifest-name", default=DEFAULT_MANIFEST_NAME, help="JSONL manifest filename")
    parser.add_argument("--summary-name", default=DEFAULT_SUMMARY_NAME, help="summary JSON filename")
    parser.add_argument("--limit", type=int, default=0, help="optional maximum number of sample dirs to process")
    parser.add_argument("--text-max-chars", type=int, default=20000, help="maximum visible_text chars to read per sample")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    roots = [Path(root) for root in args.input_roots]
    out_dir = ensure_dir(Path(args.out_dir))

    rows: List[Dict[str, Any]] = []
    for sample_dir in discover_sample_dirs(roots):
        rows.append(build_record(sample_dir, data_root, args.text_max_chars))
        if args.limit and len(rows) >= args.limit:
            break

    manifest_path = out_dir / args.manifest_name
    summary_path = out_dir / args.summary_name
    write_jsonl(manifest_path, rows)
    write_json(summary_path, summarize(rows, args, data_root))

    print(f"[done] samples={len(rows)}")
    print(f"[done] manifest={manifest_path}")
    print(f"[done] summary={summary_path}")


if __name__ == "__main__":
    main()
