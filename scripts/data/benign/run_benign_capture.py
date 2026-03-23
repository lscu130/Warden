#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, now_utc_iso, write_json

CAPTURE_SCRIPT = REPO_ROOT / "scripts" / "capture" / "capture_url_v6_optimized_v6_2_plus_labels_brandlex.py"


def build_ingest_metadata(args: argparse.Namespace) -> dict:
    payload = {
        "pipeline": "benign",
        "source": args.source,
        "run_timestamp_utc": now_utc_iso(),
    }
    if args.rank_bucket:
        payload["rank_bucket"] = args.rank_bucket
    if args.page_type:
        payload["page_type"] = args.page_type
    if args.language:
        payload["language_hint"] = args.language
    if args.hard_benign:
        payload["hard_benign"] = True
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the benign upper-layer capture pipeline.")
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--input_format", type=str, default="txt", choices=["txt", "csv"])
    parser.add_argument("--csv_url_column", type=str, default="url")
    parser.add_argument("--output_root", type=str, default=str(REPO_ROOT / "data" / "raw" / "benign"))
    parser.add_argument("--source", type=str, default="manual_benign")
    parser.add_argument("--rank_bucket", type=str, default="")
    parser.add_argument("--page_type", type=str, default="")
    parser.add_argument("--language", type=str, default="")
    parser.add_argument("--hard_benign", action="store_true")
    parser.add_argument("--brand_lexicon", type=str, default="")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    output_root = ensure_dir(Path(args.output_root))
    ingest_metadata = build_ingest_metadata(args)

    command = [
        sys.executable,
        str(CAPTURE_SCRIPT),
        "--input_path",
        args.input_path,
        "--input_format",
        args.input_format,
        "--csv_url_column",
        args.csv_url_column,
        "--label",
        "benign",
        "--output_root",
        str(output_root),
        "--ingest_metadata_json",
        json.dumps(ingest_metadata, ensure_ascii=False),
    ]
    if args.brand_lexicon:
        command.extend(["--brand_lexicon", args.brand_lexicon])
    if args.dry_run:
        command.append("--dry_run")

    log(f"[INFO] benign pipeline invoking capture: {' '.join(command)}")
    completed = subprocess.run(command, cwd=str(REPO_ROOT))
    write_json(
        output_root / "benign_capture_run.json",
        {
            "pipeline": "benign",
            "input_path": args.input_path,
            "input_format": args.input_format,
            "csv_url_column": args.csv_url_column,
            "ingest_metadata": ingest_metadata,
            "returncode": completed.returncode,
        },
    )
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
