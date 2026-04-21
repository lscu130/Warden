#!/usr/bin/env python3

"""
check_schema_compat.py

Baseline schema compatibility checks for Warden Harness P0.

This script intentionally checks only a minimal subset of selected
file-presence and top-level-key contracts. The human-readable registry
for this phase lives in docs/frozen/SCHEMA_REGISTRY.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DOC_REL = Path("docs/frozen/SCHEMA_REGISTRY.md")
REGISTRY_DOC = REPO_ROOT / REGISTRY_DOC_REL

SAMPLE_DIR_REQUIRED_FILES = [
    "meta.json",
    "url.json",
    "env.json",
    "redirect_chain.json",
    "screenshot_viewport.png",
    "net_summary.json",
    "auto_labels.json",
]

META_JSON_REQUIRED_KEYS = [
    "sample_id",
    "label",
    "crawl_time_utc",
    "http_status",
    "page_title",
    "etld1_mode",
    "ingest_metadata",
]

URL_JSON_REQUIRED_KEYS = [
    "input_url",
    "final_url",
    "redirect_chain",
]

AUTO_LABELS_REQUIRED_KEYS = [
    "schema_version",
    "generated_at_utc",
    "source",
    "label_hint",
    "page_stage_candidate",
    "language_candidate",
    "url_features",
    "form_features",
    "html_features",
    "brand_signals",
    "intent_signals",
    "evasion_signals",
    "network_features",
    "risk_outputs",
]

MANIFEST_REQUIRED_FIELDS = [
    "sample_id",
    "sample_dir",
    "label_hint",
    "crawl_time_utc",
    "http_status",
    "input_url",
    "final_url",
    "has_visible_text",
    "has_forms",
    "has_html_rendered",
    "has_html_raw",
    "has_screenshot_full",
    "has_rule_labels",
    "has_manual_labels",
    "usable_for_text",
    "usable_for_vision",
    "usable_for_multimodal",
]

MANIFEST_BOOLEAN_FIELDS = [
    "has_visible_text",
    "has_forms",
    "has_html_rendered",
    "has_html_raw",
    "has_screenshot_full",
    "has_rule_labels",
    "has_manual_labels",
    "usable_for_text",
    "usable_for_vision",
    "usable_for_multimodal",
]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run baseline Warden schema compatibility checks for selected artifact kinds."
    )
    parser.add_argument(
        "--kind",
        required=True,
        choices=["sample_dir", "meta_json", "url_json", "auto_labels_json", "manifest_record"],
        help="Artifact kind to validate.",
    )
    parser.add_argument("--path", required=True, help="Path to the artifact to validate.")
    return parser.parse_args(argv)


def resolve_user_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def print_coverage_note() -> None:
    print("[schema-compat] Warden Harness P0 baseline guard")
    print(f"[schema-compat] Registry reference: {REGISTRY_DOC_REL.as_posix()}")
    print(
        "[schema-compat] Coverage: selected required file names and top-level keys only."
    )
    print(
        "[schema-compat] Not covered: enum semantics, nested schema shape, cross-field logic, "
        "inference routing, or capture generation correctness."
    )


def read_json_object(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", errors="ignore") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected a JSON object at {path}")
    return data


def missing_keys(data: Dict[str, Any], required_keys: Sequence[str]) -> List[str]:
    return [key for key in required_keys if key not in data]


def check_sample_dir(path: Path) -> List[str]:
    issues: List[str] = []
    if not path.exists():
        return [f"missing path: {path}"]
    if not path.is_dir():
        return [f"not a directory: {path}"]

    for filename in SAMPLE_DIR_REQUIRED_FILES:
        if not (path / filename).exists():
            issues.append(f"missing required file: {filename}")
    return issues


def check_json_keys(path: Path, required_keys: Sequence[str]) -> List[str]:
    if not path.exists():
        return [f"missing path: {path}"]
    if not path.is_file():
        return [f"not a file: {path}"]

    try:
        data = read_json_object(path)
    except Exception as exc:
        return [f"json read failure: {exc}"]

    return [f"missing required key: {key}" for key in missing_keys(data, required_keys)]


def check_manifest_record(path: Path) -> List[str]:
    issues = check_json_keys(path, MANIFEST_REQUIRED_FIELDS)
    if issues:
        return issues

    try:
        data = read_json_object(path)
    except Exception as exc:
        return [f"json read failure: {exc}"]

    for field in MANIFEST_BOOLEAN_FIELDS:
        if not isinstance(data.get(field), bool):
            issues.append(f"field must be boolean: {field}")
    return issues


def run_check(kind: str, path: Path) -> List[str]:
    if kind == "sample_dir":
        return check_sample_dir(path)
    if kind == "meta_json":
        return check_json_keys(path, META_JSON_REQUIRED_KEYS)
    if kind == "url_json":
        return check_json_keys(path, URL_JSON_REQUIRED_KEYS)
    if kind == "auto_labels_json":
        return check_json_keys(path, AUTO_LABELS_REQUIRED_KEYS)
    if kind == "manifest_record":
        return check_manifest_record(path)
    return [f"unsupported kind: {kind}"]


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    path = resolve_user_path(args.path)

    print_coverage_note()
    issues = run_check(args.kind, path)

    if issues:
        print(f"[schema-compat] FAIL kind={args.kind} path={path}")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print(f"[schema-compat] OK   kind={args.kind} path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
