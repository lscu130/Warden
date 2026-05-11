#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deduplicate Tranco benign triage bucket sample directories by URL key.

The script scans direct child sample directories in selected T-bucket roots.
It parses directory names as <url_key>_<YYYYMMDDTHHMMSSZ>, keeps the oldest
timestamped sample for each URL key, and writes keep/delete manifests.

No sample-internal files are edited. In --delete mode, same-bucket duplicate
sample directories inside the explicitly selected roots are removed. Cross-
bucket duplicates are reported but not deleted unless --delete-cross-bucket is
explicitly passed, because cross-bucket duplicates may indicate triage conflict.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional


DIRNAME_PATTERN = re.compile(r"^(?P<url_key>.+)_(?P<timestamp>\d{8}T\d{6}Z)$")
DEFAULT_BUCKETS = (
    "T00_clear_benign",
    "T01_benign_hard_negative",
    "T02_gamble",
    "T03_adult",
    "T04_gate",
    "T05_evasion",
)


@dataclass(frozen=True)
class ParsedSampleDir:
    bucket: str
    sample_dir: Path
    dirname: str
    url_key: str
    timestamp_utc: str


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_sample_dir(path: Path) -> bool:
    return path.is_dir() and (path / "meta.json").exists() and (path / "url.json").exists()


def parse_sample_dir(bucket: str, sample_dir: Path) -> Optional[ParsedSampleDir]:
    match = DIRNAME_PATTERN.match(sample_dir.name)
    if not match:
        return None
    return ParsedSampleDir(
        bucket=bucket,
        sample_dir=sample_dir.resolve(),
        dirname=sample_dir.name,
        url_key=match.group("url_key"),
        timestamp_utc=match.group("timestamp"),
    )


def iter_bucket_child_dirs(bucket_roots: Dict[str, Path]) -> Iterator[tuple[str, Path]]:
    for bucket, root in bucket_roots.items():
        if not root.exists() or not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if child.is_dir():
                yield bucket, child


def is_better_keeper(candidate: ParsedSampleDir, current: ParsedSampleDir) -> bool:
    if candidate.timestamp_utc != current.timestamp_utc:
        return candidate.timestamp_utc < current.timestamp_utc
    if candidate.bucket != current.bucket:
        return candidate.bucket < current.bucket
    return candidate.dirname < current.dirname


def is_within_any_root(target: Path, roots: Iterable[Path]) -> bool:
    resolved = target.resolve()
    for root in roots:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def collect_samples(bucket_roots: Dict[str, Path]) -> tuple[List[ParsedSampleDir], List[dict]]:
    parsed_samples: List[ParsedSampleDir] = []
    skipped: List[dict] = []
    for bucket, child in iter_bucket_child_dirs(bucket_roots):
        if not is_sample_dir(child):
            skipped.append({"bucket": bucket, "dirname": child.name, "path": str(child.resolve()), "reason": "not_sample_dir"})
            continue
        parsed = parse_sample_dir(bucket, child)
        if parsed is None:
            skipped.append({"bucket": bucket, "dirname": child.name, "path": str(child.resolve()), "reason": "nonmatching_dirname"})
            continue
        parsed_samples.append(parsed)
    return parsed_samples, skipped


def write_keep_manifest(path: Path, keepers: Dict[str, ParsedSampleDir]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for url_key in sorted(keepers):
            parsed = keepers[url_key]
            row = {
                "url_key": parsed.url_key,
                "kept_bucket": parsed.bucket,
                "kept_dirname": parsed.dirname,
                "kept_dir": str(parsed.sample_dir),
                "kept_timestamp_utc": parsed.timestamp_utc,
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def run(args: argparse.Namespace) -> int:
    triage_root = Path(args.triage_root).resolve()
    bucket_roots = {bucket: (triage_root / bucket).resolve() for bucket in args.buckets}
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    missing_buckets = [bucket for bucket, root in bucket_roots.items() if not root.exists()]
    if missing_buckets:
        raise SystemExit(f"missing bucket roots: {missing_buckets}")

    samples, skipped = collect_samples(bucket_roots)
    keepers: Dict[str, ParsedSampleDir] = {}
    all_by_key: Dict[str, List[ParsedSampleDir]] = {}
    for parsed in samples:
        all_by_key.setdefault(parsed.url_key, []).append(parsed)
        current = keepers.get(parsed.url_key)
        if current is None or is_better_keeper(parsed, current):
            keepers[parsed.url_key] = parsed

    suffix = "delete" if args.delete else "dry_run"
    keep_manifest_path = output_dir / f"t00_t05_keep_manifest_{suffix}.jsonl"
    delete_manifest_path = output_dir / f"t00_t05_delete_manifest_{suffix}.jsonl"
    summary_path = output_dir / f"t00_t05_dedup_summary_{suffix}.json"

    num_kept = write_keep_manifest(keep_manifest_path, keepers)
    num_duplicate_dirs = 0
    num_deleted_dirs = 0
    num_delete_failures = 0
    cross_bucket_duplicate_keys = 0
    same_bucket_duplicate_keys = 0
    status_counts: Dict[str, int] = {}

    with delete_manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for url_key in sorted(all_by_key):
            entries = sorted(all_by_key[url_key], key=lambda p: (p.timestamp_utc, p.bucket, p.dirname))
            if len(entries) <= 1:
                continue
            buckets = sorted({entry.bucket for entry in entries})
            if len(buckets) > 1:
                cross_bucket_duplicate_keys += 1
            else:
                same_bucket_duplicate_keys += 1
            keeper = keepers[url_key]
            for parsed in entries:
                if parsed.sample_dir == keeper.sample_dir:
                    continue
                num_duplicate_dirs += 1
                row = {
                    "url_key": parsed.url_key,
                    "duplicate_bucket": parsed.bucket,
                    "duplicate_dirname": parsed.dirname,
                    "duplicate_dir": str(parsed.sample_dir),
                    "duplicate_timestamp_utc": parsed.timestamp_utc,
                    "kept_bucket": keeper.bucket,
                    "kept_dirname": keeper.dirname,
                    "kept_dir": str(keeper.sample_dir),
                    "kept_timestamp_utc": keeper.timestamp_utc,
                    "all_buckets_for_url_key": buckets,
                    "cross_bucket_duplicate": len(buckets) > 1,
                    "mode": "delete" if args.delete else "dry_run",
                }

                is_cross_bucket = len(buckets) > 1
                if args.delete and is_cross_bucket and not args.delete_cross_bucket:
                    row["action"] = "skipped_cross_bucket_duplicate"
                elif args.delete:
                    if not is_within_any_root(parsed.sample_dir, bucket_roots.values()):
                        row["action"] = "delete_blocked_outside_roots"
                        num_delete_failures += 1
                    else:
                        try:
                            shutil.rmtree(parsed.sample_dir)
                            row["action"] = "deleted"
                            num_deleted_dirs += 1
                        except Exception as exc:  # pragma: no cover - depends on filesystem
                            row["action"] = "delete_failed"
                            row["error"] = repr(exc)
                            num_delete_failures += 1
                else:
                    row["action"] = "would_delete_cross_bucket" if is_cross_bucket else "would_delete_same_bucket"

                status_counts[row["action"]] = status_counts.get(row["action"], 0) + 1
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    bucket_counts: Dict[str, int] = {bucket: 0 for bucket in bucket_roots}
    for parsed in samples:
        bucket_counts[parsed.bucket] = bucket_counts.get(parsed.bucket, 0) + 1

    summary = {
        "generated_at_utc": now_utc_iso(),
        "mode": "delete" if args.delete else "dry_run",
        "triage_root": str(triage_root),
        "buckets": list(args.buckets),
        "output_dir": str(output_dir),
        "num_sample_dirs_scanned": len(samples),
        "num_unique_url_keys": len(keepers),
        "num_kept_dirs": num_kept,
        "num_duplicate_dirs": num_duplicate_dirs,
        "num_deleted_dirs": num_deleted_dirs,
        "num_delete_failures": num_delete_failures,
        "num_skipped_dirs": len(skipped),
        "skipped_examples": skipped[:20],
        "bucket_sample_counts": bucket_counts,
        "same_bucket_duplicate_keys": same_bucket_duplicate_keys,
        "cross_bucket_duplicate_keys": cross_bucket_duplicate_keys,
        "status_counts": status_counts,
        "artifacts": {
            "keep_manifest": str(keep_manifest_path),
            "delete_manifest": str(delete_manifest_path),
            "summary": str(summary_path),
        },
    }
    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if num_delete_failures else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-root", required=True, help="Root containing T00-T05 bucket directories.")
    parser.add_argument("--output-dir", required=True, help="Output directory for keep/delete manifests and summary.")
    parser.add_argument("--buckets", nargs="+", default=list(DEFAULT_BUCKETS), help="Bucket directory names to scan.")
    parser.add_argument("--delete", action="store_true", help="Actually delete duplicate directories. Default is dry-run.")
    parser.add_argument(
        "--delete-cross-bucket",
        action="store_true",
        help="Also delete cross-bucket duplicates. Default delete mode skips them to preserve triage-conflict evidence.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
