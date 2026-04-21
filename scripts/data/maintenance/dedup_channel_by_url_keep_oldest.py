#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, now_utc_iso, write_json

CONFIG_INPUT_ROOT = str(REPO_ROOT / "channel")
CONFIG_OUTPUT_DIR = str(REPO_ROOT / "data" / "processed" / "channel_url_dedup")
KEEP_MANIFEST_NAME = "keep_manifest.jsonl"
DELETE_MANIFEST_NAME = "delete_manifest.jsonl"
SUMMARY_NAME = "summary.json"
DIRNAME_PATTERN = re.compile(r"^(?P<url_key>.+)_(?P<timestamp>\d{8}T\d{6}Z)$")


@dataclass(frozen=True)
class ParsedSampleDir:
    sample_dir: Path
    dirname: str
    url_key: str
    timestamp_utc: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deduplicate channel sample directories by directory-name URL key and keep the oldest timestamped sample."
    )
    parser.add_argument("--input-root", default=CONFIG_INPUT_ROOT, help="channel root whose direct child directories will be scanned")
    parser.add_argument("--output-dir", default=CONFIG_OUTPUT_DIR, help="directory used for keep/delete manifests and summary")
    parser.add_argument("--delete", action="store_true", help="actually delete newer duplicate directories; default is dry-run only")
    parser.add_argument(
        "--skip-nonmatching",
        action="store_true",
        help="silently skip child directories whose names do not match <url_key>_<YYYYMMDDTHHMMSSZ>; default reports them in the summary",
    )
    return parser.parse_args()


def iter_child_dirs(root: Path) -> Iterator[Path]:
    with os.scandir(root) as entries:
        for entry in entries:
            if entry.is_dir():
                yield Path(entry.path)


def parse_sample_dir(sample_dir: Path) -> Optional[ParsedSampleDir]:
    match = DIRNAME_PATTERN.match(sample_dir.name)
    if not match:
        return None
    return ParsedSampleDir(
        sample_dir=sample_dir.resolve(),
        dirname=sample_dir.name,
        url_key=match.group("url_key"),
        timestamp_utc=match.group("timestamp"),
    )


def is_better_keeper(candidate: ParsedSampleDir, current: ParsedSampleDir) -> bool:
    if candidate.timestamp_utc != current.timestamp_utc:
        return candidate.timestamp_utc < current.timestamp_utc
    return candidate.dirname < current.dirname


def is_within_root(target: Path, root: Path) -> bool:
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def write_keep_manifest(path: Path, keepers: Dict[str, ParsedSampleDir]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for parsed in keepers.values():
            row = {
                "url_key": parsed.url_key,
                "kept_dirname": parsed.dirname,
                "kept_dir": str(parsed.sample_dir),
                "kept_timestamp_utc": parsed.timestamp_utc,
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    args = parse_args()

    input_root = Path(args.input_root).resolve()
    output_dir = ensure_dir(Path(args.output_dir).resolve())
    keep_manifest_path = output_dir / KEEP_MANIFEST_NAME
    delete_manifest_path = output_dir / DELETE_MANIFEST_NAME
    summary_path = output_dir / SUMMARY_NAME

    if not input_root.exists():
        raise SystemExit(f"input root does not exist: {input_root}")
    if not input_root.is_dir():
        raise SystemExit(f"input root is not a directory: {input_root}")

    keepers: Dict[str, ParsedSampleDir] = {}
    num_child_dirs_scanned = 0
    num_matching_dirs = 0
    num_skipped_dirs = 0
    skipped_examples = []

    for child_dir in iter_child_dirs(input_root):
        num_child_dirs_scanned += 1
        parsed = parse_sample_dir(child_dir)
        if parsed is None:
            num_skipped_dirs += 1
            if not args.skip_nonmatching and len(skipped_examples) < 10:
                skipped_examples.append({"dirname": child_dir.name, "path": str(child_dir.resolve())})
            continue

        num_matching_dirs += 1
        current = keepers.get(parsed.url_key)
        if current is None or is_better_keeper(parsed, current):
            keepers[parsed.url_key] = parsed

    num_kept = write_keep_manifest(keep_manifest_path, keepers)

    num_duplicate_dirs = 0
    num_deleted_dirs = 0
    num_delete_failures = 0

    with delete_manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for child_dir in iter_child_dirs(input_root):
            parsed = parse_sample_dir(child_dir)
            if parsed is None:
                continue

            keeper = keepers.get(parsed.url_key)
            if keeper is None or parsed.sample_dir == keeper.sample_dir:
                continue

            num_duplicate_dirs += 1
            row = {
                "url_key": parsed.url_key,
                "kept_dirname": keeper.dirname,
                "kept_dir": str(keeper.sample_dir),
                "kept_timestamp_utc": keeper.timestamp_utc,
                "duplicate_dirname": parsed.dirname,
                "duplicate_dir": str(parsed.sample_dir),
                "duplicate_timestamp_utc": parsed.timestamp_utc,
                "mode": "delete" if args.delete else "dry_run",
            }

            if args.delete:
                if not is_within_root(parsed.sample_dir, input_root):
                    row["action"] = "delete_blocked_outside_root"
                    num_delete_failures += 1
                else:
                    try:
                        shutil.rmtree(parsed.sample_dir)
                        row["action"] = "deleted"
                        num_deleted_dirs += 1
                    except Exception as exc:
                        row["action"] = "delete_failed"
                        row["error"] = repr(exc)
                        num_delete_failures += 1
            else:
                row["action"] = "would_delete"

            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "generated_at_utc": now_utc_iso(),
        "input_root": str(input_root),
        "output_dir": str(output_dir),
        "mode": "delete" if args.delete else "dry_run",
        "num_child_dirs_scanned": num_child_dirs_scanned,
        "num_matching_dirs": num_matching_dirs,
        "num_unique_url_keys": len(keepers),
        "num_kept_dirs": num_kept,
        "num_duplicate_dirs": num_duplicate_dirs,
        "num_deleted_dirs": num_deleted_dirs,
        "num_delete_failures": num_delete_failures,
        "num_skipped_dirs": num_skipped_dirs,
        "skipped_examples": [] if args.skip_nonmatching else skipped_examples,
        "artifacts": {
            "keep_manifest": str(keep_manifest_path),
            "delete_manifest": str(delete_manifest_path),
            "summary": str(summary_path),
        },
    }
    write_json(summary_path, summary)

    log(
        "[done] "
        f"mode={summary['mode']} scanned={num_child_dirs_scanned} matching={num_matching_dirs} "
        f"unique={len(keepers)} duplicates={num_duplicate_dirs} deleted={num_deleted_dirs} skipped={num_skipped_dirs}"
    )
    log(f"[done] keep_manifest={keep_manifest_path}")
    log(f"[done] delete_manifest={delete_manifest_path}")
    log(f"[done] summary={summary_path}")


if __name__ == "__main__":
    main()
