#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# operator: Codex; task: content-warning-candidate-rebucket; date: 2026-04-24

"""Move content-warning candidates out of the primary benign pool.

This script intentionally handles only rows where `content_warning_candidate`
is not `none`. High-confidence URL/domain matches are moved to adult/gambling
content buckets. Everything ambiguous is moved to a manual-review folder.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, now_utc_iso, read_json, write_json, write_jsonl
from scripts.data.common.runtime_data_root import data_path, get_data_root

DEFAULT_MANIFEST = data_path("reviewed", "benign_second_pass", "2026-04-24_primary_benign_second_pass_review_manifest.jsonl")
DEFAULT_PLAN = data_path("reviewed", "benign_second_pass", "2026-04-24_content_warning_rebucket_plan.jsonl")
DEFAULT_SUMMARY = data_path("reviewed", "benign_second_pass", "2026-04-24_content_warning_rebucket_summary.json")
DEFAULT_APPLY_LOG = data_path("reviewed", "benign_second_pass", "2026-04-24_content_warning_rebucket_apply_log.jsonl")

ADULT_TARGET = data_path("raw", "benign", "hard benign", "adult")
GAMBLING_TARGET = data_path("raw", "benign", "hard benign", "gambling")
BOTH_TARGET = data_path("raw", "benign", "hard benign", "adult_and_gambling")
MANUAL_TARGET = data_path("raw", "benign", "hard benign", "content_warning_manual_review_20260424")

ADULT_URL_RE = re.compile(
    r"(porn|porno|\.porn\b|xxx|xnxx|xvideos|hentai|onlyfans|escort|camgirl|cams|brazzers|erotic|sexcam|sextube|adult[-_]?video|adult[-_]?dating)",
    re.IGNORECASE,
)
GAMBLING_URL_RE = re.compile(
    r"(casino|sportsbook|bookmaker|bet365|1xbet|1win|betway|betfair|betano|\bbet[-_]?|[-_]bet\b|betting|gambling|togel|toto|slots?|stake|spin4win)",
    re.IGNORECASE,
)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", errors="ignore") as handle:
        for lineno, line in enumerate(handle, 1):
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            if not isinstance(row, dict):
                raise ValueError(f"{path} line {lineno} is not an object")
            rows.append(row)
    return rows


def safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def classify(row: Mapping[str, Any], data_root: Path) -> Dict[str, Any]:
    sample_dir = data_root / safe_str(row.get("sample_dir"))
    url_blob = " ".join(
        [
            safe_str(row.get("sample_id")),
            safe_str(row.get("input_url")),
            safe_str(row.get("final_url")),
            safe_str(row.get("host")),
            safe_str(row.get("etld1")),
        ]
    )
    adult_hit = bool(ADULT_URL_RE.search(url_blob))
    gambling_hit = bool(GAMBLING_URL_RE.search(url_blob))

    if adult_hit and gambling_hit:
        bucket = "adult_and_gambling"
        target_root = BOTH_TARGET
        confidence = "high"
        reason = "strong_url_or_domain_hit:adult_and_gambling"
    elif adult_hit:
        bucket = "adult"
        target_root = ADULT_TARGET
        confidence = "high"
        reason = "strong_url_or_domain_hit:adult"
    elif gambling_hit:
        bucket = "gambling"
        target_root = GAMBLING_TARGET
        confidence = "high"
        reason = "strong_url_or_domain_hit:gambling"
    else:
        bucket = "manual_review"
        target_root = MANUAL_TARGET
        confidence = "low"
        reason = "ambiguous_content_warning_candidate"

    return {
        "sample_id": safe_str(row.get("sample_id")),
        "content_warning_candidate": safe_str(row.get("content_warning_candidate")),
        "decision_bucket": bucket,
        "decision_confidence": confidence,
        "decision_reason": reason,
        "src": str(sample_dir),
        "dst": str(target_root / sample_dir.name),
        "input_url": safe_str(row.get("input_url")),
        "final_url": safe_str(row.get("final_url")),
        "source_reason_codes": row.get("reason_codes", []),
        "weak_label_warning": "This move is operational rebucketing, not a manual gold label.",
    }


def build_plan(rows: List[Dict[str, Any]], data_root: Path) -> List[Dict[str, Any]]:
    plan: List[Dict[str, Any]] = []
    for row in rows:
        if safe_str(row.get("content_warning_candidate")) == "none":
            continue
        plan.append(classify(row, data_root))
    return plan


def summarize(plan: List[Dict[str, Any]], applied: bool, apply_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    decision_counter = Counter(item["decision_bucket"] for item in plan)
    candidate_counter = Counter(item["content_warning_candidate"] for item in plan)
    status_counter = Counter(item.get("status", "planned") for item in apply_log) if applied else Counter()
    return {
        "schema_version": "content_warning_rebucket_summary_v1",
        "generated_at_utc": now_utc_iso(),
        "applied": applied,
        "planned_count": len(plan),
        "candidate_distribution": dict(sorted(candidate_counter.items())),
        "decision_distribution": dict(sorted(decision_counter.items())),
        "apply_status_distribution": dict(sorted(status_counter.items())),
        "note": "High-confidence moves use strict URL/domain evidence. Manual-review moves are not final labels.",
    }


def apply_plan(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    log_rows: List[Dict[str, Any]] = []
    for item in plan:
        src = Path(item["src"])
        dst = Path(item["dst"])
        record = dict(item)
        if not src.exists():
            record["status"] = "missing_source"
        elif dst.exists():
            record["status"] = "destination_exists"
        else:
            ensure_dir(dst.parent)
            shutil.move(str(src), str(dst))
            record["status"] = "moved"
        log_rows.append(record)
    return log_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebucket content-warning candidates from primary benign.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="second-pass review manifest JSONL")
    parser.add_argument("--data-root", default=str(get_data_root()), help="active Warden data root")
    parser.add_argument("--plan-out", default=str(DEFAULT_PLAN), help="move plan JSONL")
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY), help="summary JSON")
    parser.add_argument("--apply-log-out", default=str(DEFAULT_APPLY_LOG), help="apply log JSONL")
    parser.add_argument("--apply", action="store_true", help="apply the move plan")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    rows = read_jsonl(Path(args.manifest))
    plan = build_plan(rows, data_root)

    plan_path = Path(args.plan_out)
    summary_path = Path(args.summary_out)
    ensure_dir(plan_path.parent)
    write_jsonl(plan_path, plan)

    apply_log: List[Dict[str, Any]] = []
    if args.apply:
        apply_log = apply_plan(plan)
        apply_log_path = Path(args.apply_log_out)
        ensure_dir(apply_log_path.parent)
        write_jsonl(apply_log_path, apply_log)

    write_json(summary_path, summarize(plan, args.apply, apply_log))
    print(f"[done] planned={len(plan)}")
    print(f"[done] plan={plan_path}")
    print(f"[done] summary={summary_path}")
    if args.apply:
        print(f"[done] apply_log={args.apply_log_out}")


if __name__ == "__main__":
    main()
