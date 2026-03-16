#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backfill EVT v1.1 auto labels for existing sample directories.

Usage examples:
  python evt_dataset_backfill_labels.py --roots "C:/EVT/phish1" "C:/EVT/benign"
  python evt_dataset_backfill_labels.py --roots ./phish1 --only-missing --workers 4 --emit-rule-labels

Default behavior:
- Always writes auto_labels.json
- Optionally writes rule_labels.json when --emit-rule-labels is enabled
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, List, Tuple

from evt_auto_label_utils import derive_auto_labels_from_sample_dir, derive_rule_labels, iter_sample_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="+", required=True, help="dataset roots to scan")
    parser.add_argument("--auto-output-name", default="auto_labels.json", help="auto-label filename inside each sample dir")
    parser.add_argument("--rule-output-name", default="rule_labels.json", help="rule-label filename inside each sample dir")
    parser.add_argument("--only-missing", action="store_true", help="skip sample dirs that already have target output file(s)")
    parser.add_argument("--emit-rule-labels", action="store_true", help="also emit rule_labels.json from auto_labels")
    parser.add_argument("--workers", type=int, default=4, help="I/O worker count; keep modest to avoid disk thrash")
    parser.add_argument("--limit", type=int, default=0, help="optional max number of samples to process")
    parser.add_argument("--fail-fast", action="store_true")
    return parser.parse_args()


def collect_sample_dirs(roots: Iterable[Path], auto_output_name: str, rule_output_name: str, only_missing: bool, emit_rule_labels: bool, limit: int) -> List[Path]:
    sample_dirs: List[Path] = []
    seen = set()
    for sample_dir in iter_sample_dirs(roots):
        if sample_dir in seen:
            continue
        seen.add(sample_dir)
        if only_missing:
            auto_exists = (sample_dir / auto_output_name).exists()
            rule_exists = (sample_dir / rule_output_name).exists()
            if auto_exists and (not emit_rule_labels or rule_exists):
                continue
        sample_dirs.append(sample_dir)
        if limit > 0 and len(sample_dirs) >= limit:
            break
    return sample_dirs


def process_one(sample_dir: Path, auto_output_name: str, rule_output_name: str, emit_rule_labels: bool) -> Tuple[Path, bool, str]:
    try:
        auto_labels = derive_auto_labels_from_sample_dir(sample_dir, source="backfill_v1_1")
        (sample_dir / auto_output_name).write_text(json.dumps(auto_labels, ensure_ascii=False, indent=2), encoding="utf-8")
        if emit_rule_labels:
            rule_labels = derive_rule_labels(auto_labels)
            (sample_dir / rule_output_name).write_text(json.dumps(rule_labels, ensure_ascii=False, indent=2), encoding="utf-8")
        return sample_dir, True, ""
    except Exception as e:
        return sample_dir, False, repr(e)


def main() -> None:
    args = parse_args()
    roots = [Path(r) for r in args.roots]
    sample_dirs = collect_sample_dirs(
        roots,
        args.auto_output_name,
        args.rule_output_name,
        args.only_missing,
        args.emit_rule_labels,
        args.limit,
    )
    total = len(sample_dirs)
    if total == 0:
        print("[INFO] no sample directories matched")
        return

    ok = 0
    fail = 0
    print(
        f"[INFO] matched_samples={total} workers={max(1, args.workers)} "
        f"auto={args.auto_output_name} emit_rule_labels={args.emit_rule_labels}"
    )

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {
            ex.submit(process_one, sample_dir, args.auto_output_name, args.rule_output_name, args.emit_rule_labels): sample_dir
            for sample_dir in sample_dirs
        }
        for idx, fut in enumerate(as_completed(futs), 1):
            sample_dir = futs[fut]
            try:
                _, success, msg = fut.result()
            except Exception as e:
                success = False
                msg = repr(e)
            if success:
                ok += 1
                print(f"[{idx}/{total}] OK {sample_dir}")
            else:
                fail += 1
                print(f"[{idx}/{total}] FAIL {sample_dir} :: {msg}")
                if args.fail_fast:
                    print("[FATAL] fail-fast triggered", file=sys.stderr)
                    sys.exit(1)

    print(f"[DONE] success={ok} failed={fail} total={total}")


if __name__ == "__main__":
    main()
