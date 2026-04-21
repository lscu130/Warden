#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from scripts.data.common.html_payload_utils import read_html_payload_text
from scripts.data.common.io_utils import read_json
from scripts.data.common.url_utils import canonicalize_url, registrable_domain, stable_hash

RE_WS = re.compile(r"\s+")


def _normalize_text(text: str, max_chars: int = 4000) -> str:
    text = RE_WS.sub(" ", (text or "").strip())
    return text[:max_chars]


def _read_text_if_exists(path: Path, max_chars: int = 4000) -> str:
    if not path.exists():
        return ""
    return _normalize_text(path.read_text(encoding="utf-8", errors="ignore"), max_chars=max_chars)


def _read_json_if_exists(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return read_json(path)
    except Exception:
        return default


def _sha1_bytes(path: Path) -> str:
    if not path.exists():
        return ""
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()[:16]


def _forms_summary(forms_payload: Dict[str, Any]) -> Dict[str, Any]:
    forms = forms_payload.get("forms") or []
    summary: Dict[str, Any] = {
        "form_count": len(forms),
        "has_password": False,
        "has_otp": False,
        "has_card": False,
        "input_types": {},
        "action_domains": [],
    }
    action_domains: set[str] = set()
    input_types: Dict[str, int] = {}
    for form in forms:
        if not isinstance(form, dict):
            continue
        summary["has_password"] = summary["has_password"] or bool(form.get("has_password"))
        summary["has_otp"] = summary["has_otp"] or bool(form.get("has_otp"))
        summary["has_card"] = summary["has_card"] or bool(form.get("has_card"))
        action = canonicalize_url(form.get("action_abs") or form.get("action") or "")
        if action:
            action_domains.add(registrable_domain(action))
        for input_item in form.get("inputs") or []:
            if not isinstance(input_item, dict):
                continue
            input_type = str(input_item.get("type") or "unknown").lower()
            input_types[input_type] = input_types.get(input_type, 0) + 1
    summary["input_types"] = dict(sorted(input_types.items()))
    summary["action_domains"] = sorted(domain for domain in action_domains if domain)
    return summary


def build_sample_fingerprint_record(sample_dir: Path) -> Dict[str, Any]:
    meta = _read_json_if_exists(sample_dir / "meta.json", {})
    url_info = _read_json_if_exists(sample_dir / "url.json", {})
    auto_labels = _read_json_if_exists(sample_dir / "auto_labels.json", {})
    forms_payload = _read_json_if_exists(sample_dir / "forms.json", {"forms": []})

    sample_id = str(meta.get("sample_id") or sample_dir.name)
    input_url = str(url_info.get("input_url") or "")
    final_url = str(url_info.get("final_url") or "")
    normalized_input_url = canonicalize_url(input_url)
    normalized_final_url = canonicalize_url(final_url)
    final_or_input = normalized_final_url or normalized_input_url

    visible_text = _read_text_if_exists(sample_dir / "visible_text.txt")
    html_rendered = read_html_payload_text(sample_dir, "html_rendered.json", max_chars=4000)
    text_fp = stable_hash(visible_text, prefix="txt_", length=16) if visible_text else ""
    html_fp = stable_hash(html_rendered, prefix="dom_", length=16) if html_rendered else ""
    forms_summary = _forms_summary(forms_payload)
    forms_fp = stable_hash(json.dumps(forms_summary, ensure_ascii=False, sort_keys=True), prefix="frm_", length=16)
    screenshot_fp = _sha1_bytes(sample_dir / "screenshot_viewport.png")

    page_stage = str(auto_labels.get("page_stage_candidate") or "unknown")
    language = str(auto_labels.get("language_candidate") or "unknown")
    brand_signals = auto_labels.get("brand_signals") or {}
    claimed_brands = [str(item).strip().lower() for item in (brand_signals.get("claimed_brands") or []) if str(item).strip()]
    family_key = "|".join(sorted(claimed_brands)) or registrable_domain(final_or_input)
    if not family_key:
        family_key = "unknown_family"

    has_viewport = (sample_dir / "screenshot_viewport.png").exists()
    has_text = bool(visible_text)
    has_html = bool(html_rendered)
    has_forms = bool((forms_payload.get("forms") or []))
    page_validity_status = "valid" if has_viewport and (has_text or has_html or has_forms) else "invalid"

    cluster_seed = "|".join(
        part for part in [family_key, page_stage, forms_fp, html_fp or text_fp or screenshot_fp or normalized_final_url] if part
    )
    subcluster_seed = "|".join(
        part for part in [family_key, page_stage, language, text_fp or html_fp, normalized_final_url or normalized_input_url] if part
    )

    return {
        "sample_id": sample_id,
        "sample_dir": str(sample_dir.resolve()),
        "label_hint": str(meta.get("label") or ""),
        "capture_time_utc": str(meta.get("crawl_time_utc") or ""),
        "input_url": input_url,
        "final_url": final_url,
        "normalized_input_url": normalized_input_url,
        "normalized_final_url": normalized_final_url,
        "registrable_domain": registrable_domain(final_or_input),
        "family_key": family_key,
        "claimed_brands": sorted(claimed_brands),
        "page_stage_candidate": page_stage,
        "language_candidate": language,
        "has_viewport_screenshot": has_viewport,
        "has_visible_text": has_text,
        "has_html_rendered": has_html,
        "has_forms": has_forms,
        "text_fingerprint": text_fp,
        "html_fingerprint": html_fp,
        "forms_fingerprint": forms_fp,
        "screenshot_fingerprint": screenshot_fp,
        "exact_url_key": stable_hash(input_url, prefix="url_", length=16) if input_url else "",
        "normalized_url_key": stable_hash(normalized_input_url, prefix="nurl_", length=16) if normalized_input_url else "",
        "final_url_key": stable_hash(normalized_final_url, prefix="furl_", length=16) if normalized_final_url else "",
        "cluster_id": stable_hash(cluster_seed or sample_id, prefix="cl_", length=16),
        "subcluster_id": stable_hash(subcluster_seed or sample_id, prefix="sub_", length=16),
        "page_validity_status": page_validity_status,
        "forms_summary": forms_summary,
    }
