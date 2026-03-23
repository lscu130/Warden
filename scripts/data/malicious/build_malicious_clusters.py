#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.fingerprint_utils import build_sample_fingerprint_record
from scripts.data.common.io_utils import discover_sample_dirs, ensure_dir, write_json, write_jsonl
from scripts.data.common.pool_utils import summarize_cluster_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Build malicious fingerprint / cluster / subcluster assignments.")
    parser.add_argument("--input_roots", nargs="+", default=[str(REPO_ROOT / "data" / "raw" / "phish")])
    parser.add_argument("--output_dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "malicious_clusters"))
    args = parser.parse_args()

    roots = [Path(item) for item in args.input_roots]
    output_dir = ensure_dir(Path(args.output_dir))

    records = [build_sample_fingerprint_record(sample_dir) for sample_dir in discover_sample_dirs(roots)]
    write_jsonl(output_dir / "malicious_cluster_records.jsonl", records)
    write_json(output_dir / "malicious_cluster_summary.json", summarize_cluster_records(records))


if __name__ == "__main__":
    main()
