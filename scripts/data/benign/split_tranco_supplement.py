#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, write_json, write_lines  # noqa: E402


BUCKETS = [
    {"label": "top_1_10000", "rank_start": 1, "rank_end": 10000, "quota": 2000},
    {"label": "top_10001_100000", "rank_start": 10001, "rank_end": 100000, "quota": 7000},
    {"label": "top_100001_500000", "rank_start": 100001, "rank_end": 500000, "quota": 8000},
    {"label": "top_500001_1000000", "rank_start": 500001, "rank_end": 1000000, "quota": 3000},
]

BUCKET_MAP = {bucket["label"]: bucket for bucket in BUCKETS}

CSV_PATTERN = re.compile(r"^tranco_(.+)_batch_(\d{4})\.csv$")


def _read_source_rows(source_csv: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with source_csv.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row or len(row) < 2:
                continue
            rank_text = str(row[0]).strip()
            domain = str(row[1]).strip()
            if not rank_text or not domain:
                continue
            try:
                rank = int(rank_text)
            except ValueError:
                continue
            rows.append({"rank": rank, "domain": domain, "url": f"https://{domain}/"})
    return rows


def _load_existing_tranco_rows(output_dir: Path) -> Tuple[set[int], set[str], Dict[str, int]]:
    used_ranks: set[int] = set()
    used_domains: set[str] = set()
    max_batch_index: Dict[str, int] = defaultdict(int)

    for path in sorted(output_dir.glob("tranco_top_*_batch_*.csv")):
        match = CSV_PATTERN.match(path.name)
        if not match:
            continue
        bucket_label = match.group(1)
        batch_index = int(match.group(2))
        max_batch_index[bucket_label] = max(max_batch_index[bucket_label], batch_index)

        with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rank_text = str(row.get("rank") or "").strip()
                domain = str(row.get("domain") or "").strip().lower()
                if rank_text:
                    try:
                        used_ranks.add(int(rank_text))
                    except ValueError:
                        pass
                if domain:
                    used_domains.add(domain)

    return used_ranks, used_domains, dict(max_batch_index)


def _evenly_spaced_sample(rows: List[Dict[str, str]], quota: int) -> List[Dict[str, str]]:
    if quota <= 0 or not rows:
        return []
    if quota >= len(rows):
        return list(rows)
    indices: List[int] = []
    for i in range(quota):
        idx = math.floor(i * len(rows) / quota)
        if idx >= len(rows):
            idx = len(rows) - 1
        indices.append(idx)
    return [rows[idx] for idx in indices]


def _write_batch_csv(path: Path, rows: Iterable[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["rank", "domain", "url"])
        writer.writeheader()
        for row in rows:
            writer.writerow({"rank": row["rank"], "domain": row["domain"], "url": row["url"]})


def _resolve_requested_buckets(bucket_labels_arg: str | None) -> List[Dict[str, int | str]]:
    if not bucket_labels_arg:
        return list(BUCKETS)

    requested_labels = [label.strip() for label in str(bucket_labels_arg).split(",") if label.strip()]
    if not requested_labels:
        return list(BUCKETS)

    unknown = [label for label in requested_labels if label not in BUCKET_MAP]
    if unknown:
        raise ValueError(f"Unknown bucket label(s): {', '.join(sorted(unknown))}")

    return [BUCKET_MAP[label] for label in requested_labels]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a supplemental Tranco benign split while excluding domains/ranks already split under the output directory."
    )
    parser.add_argument("--source_csv", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default=str(REPO_ROOT / "tranco csv"))
    parser.add_argument("--batch_size", type=int, default=1000)
    parser.add_argument("--summary_name", type=str, default="supplement_split_summary_2026-03-26.json")
    parser.add_argument(
        "--bucket_labels",
        type=str,
        default=None,
        help="Comma-separated bucket labels to generate. Default: all frozen buckets.",
    )
    args = parser.parse_args()

    source_csv = Path(args.source_csv)
    output_dir = ensure_dir(Path(args.output_dir))
    batch_size = args.batch_size
    requested_buckets = _resolve_requested_buckets(args.bucket_labels)

    source_rows = _read_source_rows(source_csv)
    used_ranks, used_domains, max_batch_index = _load_existing_tranco_rows(output_dir)

    summary = {
        "source_csv": str(source_csv),
        "output_dir": str(output_dir),
        "selection_policy": "Warden_BENIGN_SAMPLING_STRATEGY_V1 rank-bucket quotas",
        "selection_method": "deterministic evenly spaced sampling within each rank bucket after excluding previously split ranks/domains",
        "requested_bucket_labels": [bucket["label"] for bucket in requested_buckets],
        "batch_size": batch_size,
        "source_total_rows": len(source_rows),
        "excluded_existing_rank_count": len(used_ranks),
        "excluded_existing_domain_count": len(used_domains),
        "selected_total_rows": 0,
        "total_batches": 0,
        "buckets": [],
        "batches": [],
    }

    global_batch_index = 1
    for bucket in requested_buckets:
        bucket_label = bucket["label"]
        rank_start = bucket["rank_start"]
        rank_end = bucket["rank_end"]
        quota = bucket["quota"]

        bucket_rows = [
            row
            for row in source_rows
            if rank_start <= row["rank"] <= rank_end
            and row["rank"] not in used_ranks
            and row["domain"].lower() not in used_domains
        ]
        bucket_rows.sort(key=lambda row: int(row["rank"]))
        selected_rows = _evenly_spaced_sample(bucket_rows, min(quota, len(bucket_rows)))

        for row in selected_rows:
            used_ranks.add(int(row["rank"]))
            used_domains.add(str(row["domain"]).lower())

        next_batch_index = max_batch_index.get(bucket_label, 0) + 1
        batch_count = math.ceil(len(selected_rows) / batch_size) if selected_rows else 0
        summary["buckets"].append(
            {
                "label": bucket_label,
                "rank_start": rank_start,
                "rank_end": rank_end,
                "quota": quota,
                "available_rows_after_exclusion": len(bucket_rows),
                "selected_rows": len(selected_rows),
                "batch_count": batch_count,
                "starting_batch_index": next_batch_index if batch_count else 0,
            }
        )

        for batch_offset, start in enumerate(range(0, len(selected_rows), batch_size), 0):
            batch_rows = selected_rows[start : start + batch_size]
            local_batch_index = next_batch_index + batch_offset
            batch_name = f"tranco_{bucket_label}_batch_{local_batch_index:04d}"
            csv_path = output_dir / f"{batch_name}.csv"
            txt_path = output_dir / f"{batch_name}_urls.txt"

            _write_batch_csv(csv_path, batch_rows)
            write_lines(txt_path, (row["url"] for row in batch_rows))

            summary["batches"].append(
                {
                    "global_batch_index": global_batch_index,
                    "bucket_label": bucket_label,
                    "bucket_rank_start": rank_start,
                    "bucket_rank_end": rank_end,
                    "local_batch_index": local_batch_index,
                    "row_count": len(batch_rows),
                    "csv_path": str(csv_path),
                    "txt_path": str(txt_path),
                    "selected_rank_min": min(int(row["rank"]) for row in batch_rows),
                    "selected_rank_max": max(int(row["rank"]) for row in batch_rows),
                }
            )
            global_batch_index += 1

        summary["selected_total_rows"] += len(selected_rows)
        summary["total_batches"] += batch_count

    write_json(output_dir / args.summary_name, summary)

    print(json.dumps({"selected_total_rows": summary["selected_total_rows"], "total_batches": summary["total_batches"]}))


if __name__ == "__main__":
    main()
