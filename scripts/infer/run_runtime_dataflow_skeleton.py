#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin local CLI for the Warden runtime/dataflow skeleton."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from scripts.data.common.io_utils import ensure_dir
from warden.runtime import process_samples


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Warden runtime/dataflow skeleton on one or more sample directories.")
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="sample directory or root directory containing sample directories; may be passed multiple times",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "tmp" / "runtime_dataflow_skeleton_smoke"),
        help="directory where runtime_result.json and runtime_trace.json outputs are written",
    )
    parser.add_argument("--limit", type=int, default=0, help="optional max number of discovered sample directories to process")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = [Path(item).resolve() for item in args.input]
    output_dir = ensure_dir(Path(args.output_dir).resolve())
    records = process_samples(roots=roots, output_dir=output_dir, limit=max(0, int(args.limit or 0)))
    print(json.dumps({"processed": len(records), "records": records}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
