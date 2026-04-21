#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

HTML_PAYLOAD_SCHEMA_VERSION = "warden_html_payload_v1"
HTML_PAYLOAD_TEXT_KEYS = ("text", "html", "content")


def _normalize_names(name: str) -> Tuple[str, str]:
    stem = Path(name).stem or Path(name).name
    return f"{stem}.json", f"{stem}.html"


def get_html_payload_paths(parent: Path, name: str) -> Tuple[Path, Path]:
    json_name, legacy_name = _normalize_names(name)
    return parent / json_name, parent / legacy_name


def get_html_payload_json_name(name: str) -> str:
    json_name, _ = _normalize_names(name)
    return json_name


def get_html_payload_legacy_name(name: str) -> str:
    _, legacy_name = _normalize_names(name)
    return legacy_name


def html_payload_exists(parent: Path, name: str) -> bool:
    json_path, legacy_path = get_html_payload_paths(parent, name)
    return json_path.exists() or legacy_path.exists()


def build_html_payload(text: str) -> Dict[str, str]:
    return {
        "schema_version": HTML_PAYLOAD_SCHEMA_VERSION,
        "content_type": "text/html",
        "encoding": "utf-8",
        "text": text or "",
    }


def write_html_payload(parent: Path, name: str, text: str) -> Path:
    json_path, _ = get_html_payload_paths(parent, name)
    payload = build_html_payload(text)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return json_path


def parse_html_payload(data: Any) -> str:
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in HTML_PAYLOAD_TEXT_KEYS:
            value = data.get(key)
            if isinstance(value, str):
                return value
    return ""


def read_html_payload_text(parent: Path, name: str, max_chars: Optional[int] = None) -> str:
    json_path, legacy_path = get_html_payload_paths(parent, name)
    text = ""

    if json_path.exists():
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8-sig", errors="ignore"))
            text = parse_html_payload(payload)
        except Exception:
            text = ""

    if not text and legacy_path.exists():
        try:
            if max_chars is None:
                text = legacy_path.read_text(encoding="utf-8", errors="ignore")
            else:
                with legacy_path.open("r", encoding="utf-8", errors="ignore") as handle:
                    text = handle.read(max_chars)
        except Exception:
            text = ""

    if max_chars is not None:
        return text[:max_chars]
    return text


def convert_legacy_html_file(
    html_path: Path,
    *,
    overwrite: bool = False,
    delete_original: bool = False,
) -> str:
    if html_path.suffix.lower() != ".html":
        return "skip_non_html"
    if not html_path.exists() or not html_path.is_file():
        return "skip_missing"

    json_path = html_path.with_suffix(".json")
    if json_path.exists() and not overwrite:
        return "skip_existing_json"

    text = html_path.read_text(encoding="utf-8", errors="ignore")
    json_path.write_text(json.dumps(build_html_payload(text), ensure_ascii=False, indent=2), encoding="utf-8")

    if delete_original:
        os.remove(html_path)
        return "converted_and_deleted_html"
    return "converted"
