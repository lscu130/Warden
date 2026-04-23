#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, read_jsonl, write_json, write_jsonl
from scripts.data.common.pool_utils import assign_pool_decisions, filter_advanced_family_scope, parse_advanced_family_scope
from scripts.data.common.runtime_data_root import data_path


def _join(records, decisions, bucket: str):
    decision_map = {str(row.get("sample_id")): row for row in decisions}
    for record in records:
        decision = decision_map.get(str(record.get("sample_id")), {})
        if decision.get("pool_bucket") != bucket:
            continue
        merged = dict(record)
        merged.update(
            {
                "pool_bucket": decision.get("pool_bucket"),
                "reason_code": decision.get("reason_code"),
            }
        )
        yield merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Build malicious train/reserve manifests from cluster records.")
    parser.add_argument("--clusters_path", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default=str(data_path("processed", "malicious_train_pool")))
    parser.add_argument("--family_share_cap", type=float, default=0.25)
    parser.add_argument(
        "--advanced_family_brands",
        type=str,
        default="roblox,netflix,trezor,ledger",
        help="Comma-separated brand/family tokens allowed through the current advanced train/reserve path. Use 'all' to keep the broader V1 capability active.",
    )
    args = parser.parse_args()

    advanced_family_scope = parse_advanced_family_scope(args.advanced_family_brands)
    records = filter_advanced_family_scope(read_jsonl(Path(args.clusters_path)), advanced_family_scope)
    decisions, summary = assign_pool_decisions(records, family_share_cap=args.family_share_cap)

    output_dir = ensure_dir(Path(args.output_dir))
    write_jsonl(output_dir / "pool_decisions.jsonl", decisions)
    write_jsonl(output_dir / "train_pool_manifest.jsonl", _join(records, decisions, "train_candidate"))
    write_jsonl(output_dir / "reserve_pool_manifest.jsonl", _join(records, decisions, "reserve"))
    write_json(output_dir / "pool_summary.json", summary)


if __name__ == "__main__":
    main()
