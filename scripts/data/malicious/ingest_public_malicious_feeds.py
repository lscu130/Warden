#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, now_utc_iso, write_json, write_jsonl, write_lines
from scripts.data.common.runtime_data_root import data_path
from scripts.data.common.url_utils import canonicalize_url, stable_hash

OPENPHISH_COMMUNITY_URL = "https://openphish.com/feed.txt"
PHISHTANK_FEED_URL = "https://data.phishtank.com/data/online-valid.csv"


def _read_bytes(source_url: str = "", source_path: str = "") -> bytes:
    if source_path:
        return Path(source_path).read_bytes()
    with urllib.request.urlopen(source_url, timeout=30) as response:
        return response.read()


def _parse_text_feed(payload: bytes, source: str) -> List[Dict[str, str]]:
    text = payload.decode("utf-8", errors="ignore")
    rows: List[Dict[str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        url = line.strip()
        if not url:
            continue
        rows.append({"source": source, "original_url": url, "source_row": str(lineno)})
    return rows


def _parse_csv_feed(payload: bytes, source: str) -> List[Dict[str, str]]:
    text = payload.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    rows: List[Dict[str, str]] = []
    for lineno, row in enumerate(reader, 2):
        url = (row.get("url") or row.get("URL") or "").strip()
        if not url:
            continue
        rows.append({"source": source, "original_url": url, "source_row": str(lineno)})
    return rows


def _normalize_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    normalized: Dict[str, Dict[str, str]] = {}
    ingest_timestamp = now_utc_iso()
    for row in rows:
        normalized_url = canonicalize_url(row["original_url"])
        if not normalized_url:
            continue
        key = f"{row['source']}|{normalized_url}"
        normalized[key] = {
            "source": row["source"],
            "ingest_timestamp_utc": ingest_timestamp,
            "original_url": row["original_url"],
            "normalized_url": normalized_url,
            "source_row": row.get("source_row", ""),
            "record_id": stable_hash(f"{row['source']}|{normalized_url}", prefix="feed_", length=16),
        }
    return sorted(normalized.values(), key=lambda item: (item["source"], item["normalized_url"]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest OpenPhish Community and PhishTank feed candidates.")
    parser.add_argument("--output_dir", type=str, default=str(data_path("ingest", "malicious")))
    parser.add_argument("--openphish_url", type=str, default=OPENPHISH_COMMUNITY_URL)
    parser.add_argument("--phishtank_url", type=str, default=PHISHTANK_FEED_URL)
    parser.add_argument("--openphish_input_path", type=str, default="")
    parser.add_argument("--phishtank_input_path", type=str, default="")
    args = parser.parse_args()

    output_dir = ensure_dir(Path(args.output_dir))

    openphish_rows = _parse_text_feed(_read_bytes(args.openphish_url, args.openphish_input_path), "openphish_community")
    phishtank_rows = _parse_csv_feed(_read_bytes(args.phishtank_url, args.phishtank_input_path), "phishtank")
    rows = _normalize_rows([*openphish_rows, *phishtank_rows])

    write_jsonl(output_dir / "malicious_feed_candidates.jsonl", rows)
    write_lines(output_dir / "malicious_feed_candidates.txt", (row["original_url"] for row in rows))
    write_json(
        output_dir / "malicious_feed_summary.json",
        {
            "openphish_count": len(openphish_rows),
            "phishtank_count": len(phishtank_rows),
            "combined_deduped_count": len(rows),
        },
    )


if __name__ == "__main__":
    main()
