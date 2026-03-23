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
from scripts.data.common.pool_utils import assign_pool_decisions, build_review_manifest, build_training_exclusion_list, summarize_cluster_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill malicious sample fingerprints and emit review artifacts.")
    parser.add_argument("--input_roots", nargs="+", default=[str(REPO_ROOT / "data" / "raw" / "phish")])
    parser.add_argument("--output_dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "malicious_backfill"))
    parser.add_argument("--family_share_cap", type=float, default=0.10)
    parser.add_argument("--emit_clusters", action="store_true")
    parser.add_argument("--emit_review_manifest", action="store_true")
    parser.add_argument("--emit_exclusion_list", action="store_true")
    args = parser.parse_args()

    roots = [Path(item) for item in args.input_roots]
    output_dir = ensure_dir(Path(args.output_dir))
    records = [build_sample_fingerprint_record(sample_dir) for sample_dir in discover_sample_dirs(roots)]

    write_jsonl(output_dir / "sample_fingerprints.jsonl", records)
    write_json(output_dir / "fingerprint_summary.json", summarize_cluster_records(records))

    should_emit_clusters = args.emit_clusters or args.emit_review_manifest or args.emit_exclusion_list
    if should_emit_clusters:
        write_jsonl(output_dir / "cluster_assignments.jsonl", records)

    decisions = []
    if args.emit_review_manifest or args.emit_exclusion_list:
        decisions, summary = assign_pool_decisions(records, family_share_cap=args.family_share_cap)
        write_json(output_dir / "backfill_pool_summary.json", summary)
        if args.emit_review_manifest:
            write_jsonl(output_dir / "dedup_review_manifest.jsonl", build_review_manifest(records, decisions))
        if args.emit_exclusion_list:
            write_jsonl(output_dir / "training_exclusion_list.jsonl", build_training_exclusion_list(decisions))


if __name__ == "__main__":
    main()
