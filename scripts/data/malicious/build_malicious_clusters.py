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
from scripts.data.common.pool_utils import (
    filter_advanced_family_scope,
    parse_advanced_family_scope,
    summarize_cluster_records,
)
from scripts.data.common.runtime_data_root import data_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build malicious fingerprint / cluster / subcluster assignments.")
    parser.add_argument("--input_roots", nargs="+", default=[str(data_path("raw", "phish"))])
    parser.add_argument("--output_dir", type=str, default=str(data_path("processed", "malicious_clusters")))
    parser.add_argument(
        "--advanced_family_brands",
        type=str,
        default="roblox,netflix,trezor,ledger",
        help="Comma-separated brand/family tokens for the current advanced cluster scope. Use 'all' to keep the broader V1 capability active.",
    )
    args = parser.parse_args()

    roots = [Path(item) for item in args.input_roots]
    output_dir = ensure_dir(Path(args.output_dir))
    advanced_family_scope = parse_advanced_family_scope(args.advanced_family_brands)

    records = [build_sample_fingerprint_record(sample_dir) for sample_dir in discover_sample_dirs(roots)]
    advanced_records = filter_advanced_family_scope(records, advanced_family_scope)
    write_jsonl(output_dir / "malicious_cluster_records.jsonl", advanced_records)
    write_json(output_dir / "malicious_cluster_summary.json", summarize_cluster_records(advanced_records))


if __name__ == "__main__":
    main()
