#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# operator: Codex; task: template-noise-plan-content-and-benign; date: 2026-04-24

"""Build a dry-run plan for repeated template-like benign/content pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, now_utc_iso, write_json, write_jsonl
from scripts.data.common.runtime_data_root import data_path

DEFAULT_CONTENT_ROOT = data_path("raw", "benign", "hard benign", "content_warning_manual_review_20260424")
DEFAULT_CONTENT_REMOVED_ROOT = data_path("raw", "benign", "hard benign", "content_warning_manual_review_20260424", "removed")
DEFAULT_BENIGN_ROOT = data_path("raw", "benign", "benign")
DEFAULT_OUT_DIR = data_path("reviewed", "benign_second_pass")
DEFAULT_PLAN_NAME = "2026-04-24_template_noise_content_and_benign_plan.jsonl"
DEFAULT_SUMMARY_NAME = "2026-04-24_template_noise_content_and_benign_summary.json"

TEMPLATE_PATTERNS = [
    "Your Ultimate Guide to",
    "Latest",
    "Latest Update",
    "Latest Updates",
    "All Posts",
    "Business",
    "Esports",
    "Fashion",
    "Featured",
    "Gaming",
    "Health",
    "Life & Fitness",
    "Lifestyle",
    "Contact Us",
    "Ryan Jones",
    "Megan Ward",
    "Bryan Wilson",
    "Today's Top Highlights",
    "Discover our latest stories",
    "Recent Articles",
]

TITLE_TEMPLATE_RE = re.compile(
    r"(your ultimate guide|expert tips|latest news|expert insights|tips and strategies|premium lifestyle blog|daily dose|"
    r"modern web design|gaming news|business growth|digital innovation|online casino|sports betting|casino bonuses)",
    re.IGNORECASE,
)


def safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def read_text(path: Path, max_chars: int) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="ignore")[:max_chars]
    except Exception:
        return ""


def read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception:
        return str(path)


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def title_family(first_line: str) -> str:
    text = first_line.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[:|].*$", "", text).strip()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text[:80] or "unknown"


def iter_sample_dirs(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def score_sample(sample_dir: Path, source_pool: str, data_root: Path, max_chars: int) -> Dict[str, Any] | None:
    visible_text_path = sample_dir / "visible_text.txt"
    if not visible_text_path.exists():
        return None
    text = read_text(visible_text_path, max_chars)
    if not text.strip():
        return None

    first_line = first_nonempty_line(text)
    normalized_text = normalize_text(text)
    matched = [pattern for pattern in TEMPLATE_PATTERNS if pattern.lower() in normalized_text.lower()]
    title_hit = bool(TITLE_TEMPLATE_RE.search(first_line))
    score = len(matched) + (2 if title_hit else 0)

    if score < 6:
        return None

    url_info = read_json(sample_dir / "url.json")
    return {
        "schema_version": "template_noise_plan_v1",
        "source_pool": source_pool,
        "sample_id": sample_dir.name,
        "sample_dir": rel(sample_dir, data_root),
        "input_url": safe_str(url_info.get("input_url")),
        "final_url": safe_str(url_info.get("final_url")),
        "template_score": score,
        "matched_patterns": matched,
        "title_template_hit": title_hit,
        "first_line": first_line,
        "title_family": title_family(first_line),
        "suggested_action": "pending",
        "suggested_future_target": "",
        "note": "Dry-run template-noise suggestion, not a manual label.",
    }


def assign_actions(rows: List[Dict[str, Any]], keep_per_pool: int, keep_per_family: int) -> None:
    kept_by_pool: Counter[str] = Counter()
    kept_by_pool_family: Counter[tuple[str, str]] = Counter()
    rows.sort(key=lambda row: (row["source_pool"], row["title_family"], -int(row["template_score"]), row["sample_id"]))

    for row in rows:
        pool = row["source_pool"]
        family = row["title_family"]
        if pool == "content_warning_manual_review_removed":
            row["suggested_action"] = "already_removed_reference"
            row["suggested_future_target"] = ""
            continue
        if kept_by_pool[pool] < keep_per_pool and kept_by_pool_family[(pool, family)] < keep_per_family:
            row["suggested_action"] = "keep_representative"
            row["suggested_future_target"] = ""
            kept_by_pool[pool] += 1
            kept_by_pool_family[(pool, family)] += 1
            continue

        row["suggested_action"] = "move_to_template_noise"
        if pool == "content_warning_manual_review":
            row["suggested_future_target"] = str(data_path("raw", "benign", "hard benign", "template_noise_content_warning_20260424"))
        else:
            row["suggested_future_target"] = str(data_path("raw", "benign", "hard benign", "template_noise_primary_benign_20260424"))


def build_summary(rows: List[Dict[str, Any]], args: argparse.Namespace) -> Dict[str, Any]:
    by_pool_action: Counter[str] = Counter()
    by_pool: Counter[str] = Counter()
    families: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for row in rows:
        pool = row["source_pool"]
        action = row["suggested_action"]
        by_pool[pool] += 1
        by_pool_action[f"{pool}:{action}"] += 1
        families[pool][row["title_family"]] += 1
        if len(examples[pool]) < 20:
            examples[pool].append(
                {
                    "sample_id": row["sample_id"],
                    "template_score": row["template_score"],
                    "suggested_action": row["suggested_action"],
                    "first_line": row["first_line"],
                }
            )

    return {
        "schema_version": "template_noise_plan_summary_v1",
        "generated_at_utc": now_utc_iso(),
        "content_root": str(Path(args.content_root)),
        "benign_root": str(Path(args.benign_root)),
        "dry_run": True,
        "template_candidate_count": len(rows),
        "keep_per_pool": args.keep_per_pool,
        "keep_per_family": args.keep_per_family,
        "by_pool": dict(sorted(by_pool.items())),
        "by_pool_action": dict(sorted(by_pool_action.items())),
        "top_families_by_pool": {
            pool: dict(counter.most_common(25))
            for pool, counter in sorted(families.items())
        },
        "examples_by_pool": dict(examples),
        "note": "No files were moved. This plan only identifies repeated template-like pages.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan repeated template-noise handling for content and benign pools.")
    parser.add_argument("--content-root", default=str(DEFAULT_CONTENT_ROOT))
    parser.add_argument("--content-removed-root", default=str(DEFAULT_CONTENT_REMOVED_ROOT))
    parser.add_argument("--benign-root", default=str(DEFAULT_BENIGN_ROOT))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--plan-name", default=DEFAULT_PLAN_NAME)
    parser.add_argument("--summary-name", default=DEFAULT_SUMMARY_NAME)
    parser.add_argument("--keep-per-pool", type=int, default=100)
    parser.add_argument("--keep-per-family", type=int, default=2)
    parser.add_argument("--text-max-chars", type=int, default=12000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = data_path()
    rows: List[Dict[str, Any]] = []

    for sample_dir in iter_sample_dirs(Path(args.content_root)):
        row = score_sample(sample_dir, "content_warning_manual_review", data_root, args.text_max_chars)
        if row is not None:
            rows.append(row)

    for sample_dir in iter_sample_dirs(Path(args.content_removed_root)):
        row = score_sample(sample_dir, "content_warning_manual_review_removed", data_root, args.text_max_chars)
        if row is not None:
            rows.append(row)

    for sample_dir in iter_sample_dirs(Path(args.benign_root)):
        row = score_sample(sample_dir, "primary_benign", data_root, args.text_max_chars)
        if row is not None:
            rows.append(row)

    assign_actions(rows, args.keep_per_pool, args.keep_per_family)

    out_dir = ensure_dir(Path(args.out_dir))
    plan_path = out_dir / args.plan_name
    summary_path = out_dir / args.summary_name
    write_jsonl(plan_path, rows)
    write_json(summary_path, build_summary(rows, args))

    print(f"[done] candidates={len(rows)}")
    print(f"[done] plan={plan_path}")
    print(f"[done] summary={summary_path}")


if __name__ == "__main__":
    main()
