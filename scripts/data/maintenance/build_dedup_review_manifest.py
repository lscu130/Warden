#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, read_jsonl, write_jsonl
from scripts.data.common.pool_utils import build_review_manifest, filter_advanced_family_scope, parse_advanced_family_scope


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a dedup review manifest from cluster records and pool decisions.")
    parser.add_argument("--clusters_path", type=str, required=True)
    parser.add_argument("--pool_decisions_path", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "malicious_review"))
    parser.add_argument(
        "--advanced_family_brands",
        type=str,
        default="roblox",
        help="Comma-separated brand/family tokens included in the current advanced review-manifest path. Use 'all' to review every family.",
    )
    args = parser.parse_args()

    advanced_family_scope = parse_advanced_family_scope(args.advanced_family_brands)
    records = filter_advanced_family_scope(read_jsonl(Path(args.clusters_path)), advanced_family_scope)
    decisions = filter_advanced_family_scope(read_jsonl(Path(args.pool_decisions_path)), advanced_family_scope)
    output_dir = ensure_dir(Path(args.output_dir))
    write_jsonl(output_dir / "dedup_review_manifest.jsonl", build_review_manifest(records, decisions))


if __name__ == "__main__":
    main()
