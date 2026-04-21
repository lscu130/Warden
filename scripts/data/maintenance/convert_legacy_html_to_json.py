#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.html_payload_utils import convert_legacy_html_file
from scripts.data.common.io_utils import discover_sample_dirs, log, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert legacy sample HTML artifacts to JSON wrappers with optional original-file deletion."
    )
    parser.add_argument("--input_roots", nargs="+", required=True, help="sample roots to scan")
    parser.add_argument("--summary_path", type=str, default="", help="optional JSON summary output path")
    parser.add_argument("--dry_run", action="store_true", help="report what would be converted without writing files")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing JSON wrappers when present")
    parser.add_argument(
        "--delete_original_html",
        action="store_true",
        help="delete legacy .html files after successful JSON conversion",
    )
    parser.add_argument("--limit", type=int, default=0, help="optional max number of legacy HTML files to process")
    return parser.parse_args()


def plan_status(html_path: Path, overwrite: bool) -> str:
    json_path = html_path.with_suffix(".json")
    if json_path.exists() and not overwrite:
        return "skip_existing_json"
    if json_path.exists() and overwrite:
        return "would_overwrite"
    return "would_convert"


def build_summary(
    *,
    input_roots: List[Path],
    sample_dir_count: int,
    html_file_count: int,
    result_counter: Counter,
    records: List[Dict[str, str]],
    dry_run: bool,
    overwrite: bool,
    delete_original_html: bool,
) -> Dict[str, object]:
    return {
        "input_roots": [str(path.resolve()) for path in input_roots],
        "sample_dir_count": sample_dir_count,
        "html_file_count": html_file_count,
        "dry_run": dry_run,
        "overwrite": overwrite,
        "delete_original_html": delete_original_html,
        "result_counts": dict(sorted(result_counter.items(), key=lambda kv: kv[0])),
        "records": records,
    }


def main() -> None:
    args = parse_args()
    if args.limit < 0:
        raise SystemExit("--limit must be >= 0")

    input_roots = [Path(item).resolve() for item in args.input_roots]
    sample_dirs = list(discover_sample_dirs(input_roots))
    result_counter: Counter = Counter()
    records: List[Dict[str, str]] = []
    processed_html_files = 0
    html_file_count = 0

    for sample_dir in sample_dirs:
        html_paths = sorted(path for path in sample_dir.rglob("*.html") if path.is_file())
        html_file_count += len(html_paths)
        for html_path in html_paths:
            if args.limit and processed_html_files >= args.limit:
                break

            relative_path = ""
            try:
                relative_path = str(html_path.resolve().relative_to(sample_dir.resolve()))
            except Exception:
                relative_path = str(html_path.resolve())

            if args.dry_run:
                status = plan_status(html_path, overwrite=bool(args.overwrite))
            else:
                status = convert_legacy_html_file(
                    html_path,
                    overwrite=bool(args.overwrite),
                    delete_original=bool(args.delete_original_html),
                )

            processed_html_files += 1
            result_counter[status] += 1
            records.append(
                {
                    "sample_dir": str(sample_dir.resolve()),
                    "html_path": str(html_path.resolve()),
                    "relative_path": relative_path,
                    "json_path": str(html_path.with_suffix(".json").resolve()),
                    "status": status,
                }
            )

        if args.limit and processed_html_files >= args.limit:
            break

    summary = build_summary(
        input_roots=input_roots,
        sample_dir_count=len(sample_dirs),
        html_file_count=html_file_count,
        result_counter=result_counter,
        records=records,
        dry_run=bool(args.dry_run),
        overwrite=bool(args.overwrite),
        delete_original_html=bool(args.delete_original_html),
    )

    if args.summary_path.strip():
        summary_path = Path(args.summary_path).resolve()
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(summary_path, summary)
        log(f"[done] summary_path={summary_path}")

    if args.dry_run:
        log("[DRY_RUN] no files were written. Re-run without --dry_run to create JSON wrappers.")
    elif args.delete_original_html:
        log("[done] JSON wrappers were written and legacy .html files were deleted where conversion succeeded.")
    else:
        log("[done] JSON wrappers were written. Legacy .html files were retained because --delete_original_html was not set.")

    log(f"[done] sample_dirs={len(sample_dirs)} html_files_found={html_file_count} processed={processed_html_files}")
    log(f"[done] result_counts={json.dumps(summary['result_counts'], ensure_ascii=False)}")


if __name__ == "__main__":
    main()
