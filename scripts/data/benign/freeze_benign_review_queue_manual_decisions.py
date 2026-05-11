#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Freeze manual review decisions from the current benign review queue directory."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


BUCKETS = {
    "R01_missing_visible_text": "missing_visible_text",
    "R02_visible_text_exact": "visible_text_exact",
    "R03_dom_exact": "dom_exact",
    "R04_visible_text_simhash": "visible_text_simhash_candidate",
    "R05_dom_simhash": "dom_simhash_candidate",
    "R99_unresolved_or_manifest_only": "unresolved",
}

ADMIN_DIR_NAMES = {"removed", "remove", "_removed", "__removed", "discarded", "_discarded"}

DECISION_FIELDS = [
    "decision_id",
    "decision_source",
    "review_bucket",
    "candidate_type",
    "candidate_id",
    "review_id",
    "directory_name",
    "manual_status",
    "recommended_action",
    "sample_id_a",
    "sample_id_b",
    "sample_id",
    "source_path_a",
    "source_path_b",
    "source_path",
    "review_path",
    "details",
]


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def list_bucket_dirs(review_root: Path) -> Dict[str, Dict[str, Path]]:
    out: Dict[str, Dict[str, Path]] = {}
    for bucket in BUCKETS:
        path = review_root / bucket
        dirs: Dict[str, Path] = {}
        if path.exists():
            for child in path.iterdir():
                if child.is_dir():
                    if child.name.strip().lower() in ADMIN_DIR_NAMES:
                        continue
                    dirs[child.name] = child
        out[bucket] = dirs
    return out


def candidate_dir_name(candidate_id: str) -> str:
    match = re.search(r"(\d+)$", candidate_id or "")
    if not match:
        return ""
    return f"candidate_{int(match.group(1)):06d}"


def r01_dir_prefix(review_id: str) -> str:
    return review_id or ""


def infer_status(bucket: str, present: bool, is_directory_only: bool = False) -> Tuple[str, str, str]:
    if is_directory_only:
        return (
            "directory_only",
            "reconcile_directory_only_item_before_using_as_final_decision",
            "Directory exists but no matching source CSV row was found.",
        )
    if bucket == "R01_missing_visible_text":
        if present:
            return (
                "keep_sample_with_text_artifact_gap",
                "keep_sample_for_non_text_or_repair_later",
                "Manual review reports screenshot has visible text; likely client-rendered text was not captured into visible_text.txt.",
            )
        return (
            "removed_from_review_queue_by_manual_action",
            "do_not_apply_automatic_sample_removal",
            "Review directory is absent under the user-declared directory-authoritative rule.",
        )
    if bucket == "R02_visible_text_exact":
        if present:
            return (
                "keep_candidate_after_manual_review",
                "keep_candidate_no_split_or_label_change",
                "User stated R02 does not need removal.",
            )
        return (
            "removed_from_review_queue_by_manual_action",
            "do_not_apply_automatic_sample_removal",
            "Review directory is absent under the user-declared directory-authoritative rule.",
        )
    if bucket in {"R03_dom_exact", "R04_visible_text_simhash"}:
        if present:
            return (
                "keep_candidate_after_manual_review",
                "keep_candidate_no_split_or_label_change",
                "User stated candidates remaining in the directory can be kept.",
            )
        return (
            "removed_from_review_queue_by_manual_action",
            "exclude_candidate_from_manual_review_followup_only",
            "User removed this candidate directory; this is a review-queue decision, not a source-data mutation.",
        )
    if bucket == "R05_dom_simhash":
        if present:
            return (
                "keep_candidate_after_manual_review",
                "keep_candidate_no_split_or_label_change",
                "User stated all R05 can be kept because screenshots are not the same webpage.",
            )
        return (
            "removed_from_review_queue_by_manual_action",
            "do_not_apply_automatic_sample_removal",
            "Review directory is absent; verify because user stated R05 can be kept.",
        )
    return (
        "unresolved",
        "manual_reconciliation_required",
        "Unresolved bucket.",
    )


def build_r01_decisions(review_root: Path, review_manifest_rows: Sequence[Dict[str, str]], dirs: Dict[str, Dict[str, Path]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    bucket = "R01_missing_visible_text"
    source_rows = [row for row in review_manifest_rows if row.get("review_bucket") == bucket and row.get("candidate_type") == "missing_visible_text"]
    matched_dirs = set()
    for row in source_rows:
        review_id = row.get("review_id", "")
        present_name = ""
        present_path = None
        for dirname, dirpath in dirs[bucket].items():
            if dirname.startswith(review_id):
                present_name = dirname
                present_path = dirpath
                matched_dirs.add(dirname)
                break
        status, action, details = infer_status(bucket, bool(present_path))
        rows.append(
            {
                "decision_id": f"DEC_{len(rows) + 1:06d}",
                "decision_source": "directory_authority",
                "review_bucket": bucket,
                "candidate_type": "missing_visible_text",
                "candidate_id": "",
                "review_id": review_id,
                "directory_name": present_name,
                "manual_status": status,
                "recommended_action": action,
                "sample_id": row.get("sample_id", ""),
                "source_path": row.get("source_path", ""),
                "review_path": str(present_path or row.get("review_path", "")),
                "details": details,
            }
        )
    for dirname, dirpath in sorted(dirs[bucket].items()):
        if dirname in matched_dirs:
            continue
        status, action, details = infer_status(bucket, True, is_directory_only=True)
        rows.append(
            {
                "decision_id": f"DEC_{len(rows) + 1:06d}",
                "decision_source": "directory_authority",
                "review_bucket": bucket,
                "candidate_type": "missing_visible_text",
                "directory_name": dirname,
                "manual_status": status,
                "recommended_action": action,
                "review_path": str(dirpath),
                "details": details,
            }
        )
    return rows


def build_candidate_decisions(candidate_rows: Sequence[Dict[str, str]], dirs: Dict[str, Dict[str, Path]], start_index: int) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    by_bucket_seen = {bucket: set() for bucket in BUCKETS}
    for row in candidate_rows:
        candidate_type = row.get("candidate_type", "")
        bucket = next((name for name, ctype in BUCKETS.items() if ctype == candidate_type), "R99_unresolved_or_manifest_only")
        dirname = candidate_dir_name(row.get("candidate_id", ""))
        present_path = dirs.get(bucket, {}).get(dirname)
        if present_path:
            by_bucket_seen[bucket].add(dirname)
        status, action, details = infer_status(bucket, bool(present_path))
        rows.append(
            {
                "decision_id": f"DEC_{start_index + len(rows):06d}",
                "decision_source": "directory_authority",
                "review_bucket": bucket,
                "candidate_type": candidate_type,
                "candidate_id": row.get("candidate_id", ""),
                "review_id": "",
                "directory_name": dirname if present_path else "",
                "manual_status": status,
                "recommended_action": action,
                "sample_id_a": row.get("sample_id_a", ""),
                "sample_id_b": row.get("sample_id_b", ""),
                "source_path_a": row.get("source_path_a", ""),
                "source_path_b": row.get("source_path_b", ""),
                "review_path": str(present_path or ""),
                "details": details,
            }
        )

    source_dirnames = {candidate_dir_name(row.get("candidate_id", "")) for row in candidate_rows}
    for bucket, bucket_dirs in dirs.items():
        if bucket == "R01_missing_visible_text":
            continue
        for dirname, dirpath in sorted(bucket_dirs.items()):
            if dirname in source_dirnames:
                continue
            status, action, details = infer_status(bucket, True, is_directory_only=True)
            rows.append(
                {
                    "decision_id": f"DEC_{start_index + len(rows):06d}",
                    "decision_source": "directory_authority",
                    "review_bucket": bucket,
                    "candidate_type": BUCKETS[bucket],
                    "directory_name": dirname,
                    "manual_status": status,
                    "recommended_action": action,
                    "review_path": str(dirpath),
                    "details": details,
                }
            )
    return rows


def write_report(path: Path, review_root: Path, rows: Sequence[Dict[str, str]], directory_counts: Counter) -> None:
    status_counts = Counter(row.get("manual_status", "") for row in rows)
    bucket_status = Counter((row.get("review_bucket", ""), row.get("manual_status", "")) for row in rows)
    lines: List[str] = [
        "# Benign Review Queue Manual Decisions V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告按用户要求，以当前 review queue 目录内子文件夹为人工审查权威。",
        "- 目录仍存在的条目视为保留；原 CSV 有但目录不存在的条目视为人工从复核队列移除。",
        "- 这是 review queue 决策固化，不改原始样本、不改标签、不改 split manifest。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Run timestamp UTC: `{datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}`",
        f"- Review root: `{review_root}`",
        "- Authority rule: current review queue subdirectories are authoritative.",
        "- Existing directories mean keep; missing directories mean removed from review queue by manual action.",
        "- These decisions do not relabel samples and do not mutate original samples or split manifests.",
        "",
        "## 2. Directory Counts",
        "",
        "| Bucket | Current directories |",
        "|---|---:|",
    ]
    for bucket in BUCKETS:
        lines.append(f"| `{bucket}` | {directory_counts[bucket]} |")
    lines.extend(["", "## 3. Decision Status Counts", "", "| Status | Count |", "|---|---:|"])
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## 4. Bucket / Status Counts", "", "| Bucket | Status | Count |", "|---|---|---:|"])
    for (bucket, status), count in sorted(bucket_status.items()):
        lines.append(f"| `{bucket}` | `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## 5. Interpretation",
            "",
            "- R01 kept items: keep samples with a visible-text artifact gap; future repair/recrawl/text-tower exclusion remains a separate task.",
            "- R02 kept items: no removal required.",
            "- R03/R04 kept items: remaining candidate directories are kept; removed directories are excluded only from follow-up review queue.",
            "- R05 kept items: DOM hash similarity alone is not treated as same-page leakage because manual screenshot review found different webpages.",
        ]
    )
    if status_counts.get("directory_only", 0):
        lines.append("- Directory-only items require reconciliation before being used as final decisions.")
    else:
        lines.append("- No directory-only items remain after ignoring administrative folders such as `removed`.")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze benign review queue manual decisions from current directories.")
    parser.add_argument("--review-root", default=r"E:\WardenData\manifests\benign_clean_v1_review_queue")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    review_root = Path(args.review_root).resolve()
    queue_manifest = review_root / "review_queue_manifest_v1.csv"
    duplicate_manifest = review_root / "duplicate_template_review_v1.csv"
    if not queue_manifest.exists():
        raise SystemExit(f"missing review queue manifest: {queue_manifest}")
    if not duplicate_manifest.exists():
        raise SystemExit(f"missing duplicate review manifest: {duplicate_manifest}")

    dirs = list_bucket_dirs(review_root)
    directory_counts = Counter({bucket: len(items) for bucket, items in dirs.items()})
    review_rows = read_csv(queue_manifest)
    duplicate_rows = read_csv(duplicate_manifest)
    r01 = build_r01_decisions(review_root, review_rows, dirs)
    candidates = build_candidate_decisions(duplicate_rows, dirs, len(r01) + 1)
    decisions = r01 + candidates

    decision_csv = review_root / "manual_review_decisions_v1.csv"
    report = review_root / "manual_review_decision_report_v1.md"
    write_csv(decision_csv, decisions, DECISION_FIELDS)
    write_report(report, review_root, decisions, directory_counts)

    status_counts = Counter(row.get("manual_status", "") for row in decisions)
    print(f"REVIEW_ROOT={review_root}")
    for bucket in BUCKETS:
        print(f"DIRCOUNT_{bucket}={directory_counts[bucket]}")
    for status, count in sorted(status_counts.items()):
        print(f"STATUS_{status}={count}")
    print(f"OUTPUT_DECISIONS={decision_csv}")
    print(f"OUTPUT_REPORT={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
