#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Apply manual R01 review-queue removals to benign_clean_v1 manifests.

This script removes only rows whose sample_id appears in
manual_review_decisions_v1.csv with manual_status
`removed_from_review_queue_by_manual_action`.

It also deletes the corresponding review-queue copies under the R01 `removed`
management folder and the matching original sample directories under the
approved triage root.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


TARGET_FILES = [
    "tranco_benign_clean_pool_v1.csv",
    "benign_train_manifest_v1.csv",
    "benign_val_manifest_v1.csv",
    "benign_test_manifest_v1.csv",
]

REMOVAL_FIELDS = [
    "sample_id",
    "source_decision_status",
    "clean_pool_removed",
    "train_removed",
    "val_removed",
    "test_removed",
    "review_queue_removed_dir",
    "review_queue_dir_removed",
    "original_source_path",
    "original_source_dir_removed",
    "notes",
]


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(f"missing CSV header: {path}")
        return list(reader), list(reader.fieldnames)


def write_csv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def load_removed_decisions(review_root: Path) -> List[Dict[str, str]]:
    path = review_root / "manual_review_decisions_v1.csv"
    rows, _ = read_csv(path)
    removed = [
        row
        for row in rows
        if row.get("review_bucket") == "R01_missing_visible_text"
        and row.get("manual_status") == "removed_from_review_queue_by_manual_action"
    ]
    if not removed:
        raise SystemExit("no removed R01 decisions found")
    return removed


def remove_from_manifest(path: Path, sample_ids: set[str]) -> tuple[int, int]:
    rows, fields = read_csv(path)
    before = len(rows)
    kept = [row for row in rows if row.get("sample_id") not in sample_ids]
    removed = before - len(kept)
    if removed:
        write_csv(path, kept, fields)
    return before, removed


def find_removed_review_dir(review_root: Path, review_id: str, sample_id: str) -> Path | None:
    removed_root = review_root / "R01_missing_visible_text" / "removed"
    if not removed_root.exists():
        return None
    prefix = review_id or ""
    for child in removed_root.iterdir():
        if not child.is_dir():
            continue
        if prefix and child.name.startswith(prefix):
            return child
        if sample_id and sample_id in child.name:
            return child
    return None


def safe_delete_dir(path: Path, allowed_root: Path) -> bool:
    if not path.exists():
        return False
    if not path.is_dir():
        raise SystemExit(f"refusing to delete non-directory path: {path}")
    resolved_path = path.resolve()
    resolved_root = allowed_root.resolve()
    if resolved_path == resolved_root or resolved_root not in resolved_path.parents:
        raise SystemExit(f"refusing to delete path outside allowed root: {resolved_path}")
    shutil.rmtree(resolved_path)
    return True


def write_report(path: Path, manifest_dir: Path, review_root: Path, result_rows: Sequence[Dict[str, str]], file_counts: Dict[str, tuple[int, int]]) -> None:
    removed_counts = Counter()
    for row in result_rows:
        for key in (
            "clean_pool_removed",
            "train_removed",
            "val_removed",
            "test_removed",
            "review_queue_dir_removed",
            "original_source_dir_removed",
        ):
            if row.get(key) == "true":
                removed_counts[key] += 1
    lines = [
        "# Benign Clean Manual Removal Apply Report V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告记录按人工 review queue 决策应用的 targeted removals。",
        "- 只从 benign_clean_v1 的 clean pool / split manifest 移除命中样本行，并删除 review_queue 中对应 R01 removed 副本目录。",
        "- 按用户要求，已删除 tranco_benign_triage_v1 下对应原始样本目录；人工标签文件本身未重写，未重切 split。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Run timestamp UTC: `{now_utc_iso()}`",
        f"- Manifest directory: `{manifest_dir}`",
        f"- Review root: `{review_root}`",
        f"- Removed decision rows processed: `{len(result_rows)}`",
        f"- Clean pool rows removed: `{removed_counts['clean_pool_removed']}`",
        f"- Train rows removed: `{removed_counts['train_removed']}`",
        f"- Validation rows removed: `{removed_counts['val_removed']}`",
        f"- Test rows removed: `{removed_counts['test_removed']}`",
        f"- Review queue removed directories deleted: `{removed_counts['review_queue_dir_removed']}`",
        f"- Original source sample directories deleted: `{removed_counts['original_source_dir_removed']}`",
        "- Existing labels were not rewritten.",
        "- Split manifests were not regenerated; this is a targeted row removal.",
        "",
        "## 2. File Row Changes",
        "",
        "| File | Rows before | Rows removed | Rows after |",
        "|---|---:|---:|---:|",
    ]
    for filename, (before, removed) in file_counts.items():
        lines.append(f"| `{filename}` | {before} | {removed} | {before - removed} |")
    lines.extend(
        [
            "",
            "## 3. Removed Sample Decisions",
            "",
        "| Sample ID | Clean pool | Train | Val | Test | Review queue dir deleted | Original dir deleted |",
        "|---|---|---|---|---|---|---|",
        ]
    )
    for row in result_rows:
        lines.append(
            f"| `{row['sample_id']}` | `{row['clean_pool_removed']}` | `{row['train_removed']}` | `{row['val_removed']}` | `{row['test_removed']}` | `{row['review_queue_dir_removed']}` | `{row['original_source_dir_removed']}` |"
        )
    lines.extend(
        [
            "",
            "## 4. Caveats",
            "",
            "- Derived audit/review reports generated before this removal may now be stale for row counts.",
            "- Original sample directories listed in this report were deleted intentionally per user instruction.",
            "- Any downstream training manifest consumer should use the updated manifest files.",
            "- If exact split ratios are required again, run a separate approved re-split task.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply manual removed R01 samples to benign_clean_v1 manifests.")
    parser.add_argument("--manifest-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--review-root", default=r"E:\WardenData\manifests\benign_clean_v1_review_queue")
    parser.add_argument("--triage-root", default=r"E:\WardenData\manifests\tranco_benign_triage_v1")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest_dir = Path(args.manifest_dir).resolve()
    review_root = Path(args.review_root).resolve()
    triage_root = Path(args.triage_root).resolve()
    removed_decisions = load_removed_decisions(review_root)
    removed_ids = {row["sample_id"] for row in removed_decisions if row.get("sample_id")}

    file_counts: Dict[str, tuple[int, int]] = {}
    per_file_removed: Dict[str, set[str]] = {}
    for filename in TARGET_FILES:
        path = manifest_dir / filename
        rows, _ = read_csv(path)
        matched = {row.get("sample_id", "") for row in rows if row.get("sample_id", "") in removed_ids}
        before, removed = remove_from_manifest(path, removed_ids)
        file_counts[filename] = (before, removed)
        per_file_removed[filename] = matched

    result_rows: List[Dict[str, str]] = []
    for row in removed_decisions:
        sample_id = row.get("sample_id", "")
        review_dir = find_removed_review_dir(review_root, row.get("review_id", ""), sample_id)
        deleted = False
        review_dir_str = str(review_dir) if review_dir else ""
        if review_dir and review_dir.exists():
            deleted = safe_delete_dir(review_dir, review_root)
        source_path = Path(row.get("source_path", ""))
        source_deleted = False
        if str(source_path):
            source_deleted = safe_delete_dir(source_path, triage_root)
        result_rows.append(
            {
                "sample_id": sample_id,
                "source_decision_status": row.get("manual_status", ""),
                "clean_pool_removed": str(sample_id in per_file_removed["tranco_benign_clean_pool_v1.csv"]).lower(),
                "train_removed": str(sample_id in per_file_removed["benign_train_manifest_v1.csv"]).lower(),
                "val_removed": str(sample_id in per_file_removed["benign_val_manifest_v1.csv"]).lower(),
                "test_removed": str(sample_id in per_file_removed["benign_test_manifest_v1.csv"]).lower(),
                "review_queue_removed_dir": review_dir_str,
                "review_queue_dir_removed": str(deleted).lower(),
                "original_source_path": row.get("source_path", ""),
                "original_source_dir_removed": str(source_deleted).lower(),
                "notes": "source sample directory deleted per user instruction",
            }
        )

    removal_csv = review_root / "manual_removed_samples_apply_v1.csv"
    report = review_root / "manual_removed_samples_apply_report_v1.md"
    write_csv(removal_csv, result_rows, REMOVAL_FIELDS)
    write_report(report, manifest_dir, review_root, result_rows, file_counts)

    print(f"MANIFEST_DIR={manifest_dir}")
    print(f"REVIEW_ROOT={review_root}")
    print(f"REMOVED_DECISIONS={len(result_rows)}")
    for filename, (before, removed) in file_counts.items():
        print(f"{filename}: before={before} removed={removed} after={before - removed}")
    print(f"REVIEW_QUEUE_DIRS_REMOVED={sum(1 for row in result_rows if row['review_queue_dir_removed'] == 'true')}")
    print(f"ORIGINAL_SOURCE_DIRS_REMOVED={sum(1 for row in result_rows if row['original_source_dir_removed'] == 'true')}")
    print(f"OUTPUT_CSV={removal_csv}")
    print(f"OUTPUT_REPORT={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
