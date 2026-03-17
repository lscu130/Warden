#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backfill lightweight auto labels for existing EVT dataset samples.

Usage examples:
  python evt_dataset_backfill_labels.py --roots "C:/EVT/phish1" "C:/EVT/benign"
  python evt_dataset_backfill_labels.py --roots ./phish1 --only-missing --workers 4

Output:
  Writes auto_labels.json into each sample directory.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, List, Tuple

from evt_auto_label_utils_brandlex import derive_auto_labels_from_sample_dir, derive_rule_labels, iter_sample_dirs



# -----------------------------
# 头部配置区：优先在这里改默认输入/输出位置
# 命令行参数仍可覆盖这些默认值
# -----------------------------
CONFIG_DATASET_ROOTS = [
    "./data/raw/phish",
    "./data/raw/benign",
]
CONFIG_AUTO_LABEL_OUTPUT_NAME = "auto_labels.json"
CONFIG_RULE_LABEL_OUTPUT_NAME = "rule_labels.json"
CONFIG_BRAND_LEXICON_PATH = ""  # 没有外部品牌词典就保持空字符串

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="+", default=CONFIG_DATASET_ROOTS, help="dataset roots to scan")
    parser.add_argument("--output-name", default=CONFIG_AUTO_LABEL_OUTPUT_NAME, help="output filename inside each sample dir")
    parser.add_argument("--only-missing", action="store_true", help="skip sample dirs that already have output file")
    parser.add_argument("--workers", type=int, default=4, help="I/O worker count; keep modest to avoid disk thrash")
    parser.add_argument("--limit", type=int, default=0, help="optional max number of samples to process")
    parser.add_argument("--brand-lexicon", type=str, default=CONFIG_BRAND_LEXICON_PATH, help="optional path to external brand lexicon json")
    parser.add_argument("--emit-rule-labels", action="store_true", help="also emit rule_labels.json from auto_labels")
    parser.add_argument("--fail-fast", action="store_true")
    return parser.parse_args()


def collect_sample_dirs(roots: Iterable[Path], output_name: str, only_missing: bool, limit: int) -> List[Path]:
    sample_dirs: List[Path] = []
    seen = set()
    for sample_dir in iter_sample_dirs(roots):
        if sample_dir in seen:
            continue
        seen.add(sample_dir)
        if only_missing and (sample_dir / output_name).exists():
            continue
        sample_dirs.append(sample_dir)
        if limit > 0 and len(sample_dirs) >= limit:
            break
    return sample_dirs



def process_one(sample_dir: Path, output_name: str, brand_lexicon: str = "", emit_rule_labels: bool = False) -> Tuple[Path, bool, str]:
    try:
        labels = derive_auto_labels_from_sample_dir(sample_dir, source="backfill", lexicon_path=brand_lexicon or None)
        out_path = sample_dir / output_name
        out_path.write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")
        if emit_rule_labels:
            rule_labels = derive_rule_labels(labels)
            (sample_dir / CONFIG_RULE_LABEL_OUTPUT_NAME).write_text(json.dumps(rule_labels, ensure_ascii=False, indent=2), encoding="utf-8")
        return sample_dir, True, ""
    except Exception as e:
        return sample_dir, False, repr(e)


def main() -> None:
    args = parse_args()
    roots = [Path(r) for r in args.roots]
    sample_dirs = collect_sample_dirs(roots, args.output_name, args.only_missing, args.limit)
    total = len(sample_dirs)
    if total == 0:
        print("[INFO] no sample directories matched")
        return

    ok = 0
    fail = 0
    print(f"[INFO] matched_samples={total} workers={max(1, args.workers)} output={args.output_name}")

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {
            ex.submit(process_one, sample_dir, args.output_name, args.brand_lexicon, args.emit_rule_labels): sample_dir
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
