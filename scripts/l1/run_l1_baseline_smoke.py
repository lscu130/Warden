#!/usr/bin/env python3
"""Read-only smoke runner for the Warden L1 rule baseline."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from scripts.data.common.io_utils import ensure_dir
from warden.l1.l1_runner import run_l1_baseline_for_manifest_row


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Warden L1 baseline smoke over manifest current_path rows.")
    parser.add_argument("--manifest", required=True, help="CSV manifest containing current_path.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum rows to process; 0 means no limit.")
    parser.add_argument("--output", required=True, help="JSONL output path.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest = Path(args.manifest)
    output = Path(args.output)
    ensure_dir(output.parent)

    count = 0
    with manifest.open("r", encoding="utf-8-sig", errors="ignore", newline="") as src, output.open(
        "w", encoding="utf-8", newline="\n"
    ) as dst:
        reader = csv.DictReader(src)
        if not reader.fieldnames or "current_path" not in reader.fieldnames:
            raise ValueError(f"manifest is missing current_path column: {manifest}")
        for row in reader:
            if args.limit > 0 and count >= args.limit:
                break
            result = run_l1_baseline_for_manifest_row(row)
            dst.write(json.dumps(result, ensure_ascii=False) + "\n")
            count += 1

    print(f"wrote {count} L1 baseline rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
