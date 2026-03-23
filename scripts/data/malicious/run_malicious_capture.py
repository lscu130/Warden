#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, now_utc_iso, read_jsonl, write_json

CAPTURE_SCRIPT = REPO_ROOT / "scripts" / "capture" / "capture_url_v6_optimized_v6_2_plus_labels_brandlex.py"


def _group_rows_by_source(rows: Iterable[Dict[str, object]]) -> Dict[str, List[str]]:
    grouped: Dict[str, List[str]] = defaultdict(list)
    for row in rows:
        source = str(row.get("source") or "manual_malicious")
        url = str(row.get("original_url") or row.get("normalized_url") or "").strip()
        if url:
            grouped[source].append(url)
    return grouped


def _run_capture_for_source(
    source: str,
    urls: List[str],
    output_root: Path,
    brand_lexicon: str,
    dry_run: bool,
) -> int:
    if not urls:
        return 0
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        handle.write("\n".join(urls) + "\n")
        temp_path = Path(handle.name)
    metadata = {
        "pipeline": "malicious",
        "source": source,
        "run_timestamp_utc": now_utc_iso(),
    }
    command = [
        sys.executable,
        str(CAPTURE_SCRIPT),
        "--input_path",
        str(temp_path),
        "--input_format",
        "txt",
        "--label",
        "phish",
        "--output_root",
        str(output_root),
        "--ingest_metadata_json",
        json.dumps(metadata, ensure_ascii=False),
    ]
    if brand_lexicon:
        command.extend(["--brand_lexicon", brand_lexicon])
    if dry_run:
        command.append("--dry_run")
    log(f"[INFO] malicious capture for source={source}: {' '.join(command)}")
    try:
        completed = subprocess.run(command, cwd=str(REPO_ROOT))
        return completed.returncode
    finally:
        try:
            temp_path.unlink()
        except Exception:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the malicious upper-layer capture pipeline.")
    parser.add_argument("--feed_manifest", type=str, default="")
    parser.add_argument("--input_path", type=str, default="")
    parser.add_argument("--source", type=str, default="manual_malicious")
    parser.add_argument("--output_root", type=str, default=str(REPO_ROOT / "data" / "raw" / "phish"))
    parser.add_argument("--brand_lexicon", type=str, default="")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    output_root = ensure_dir(Path(args.output_root))
    returncodes: List[int] = []

    if args.feed_manifest:
        rows = read_jsonl(Path(args.feed_manifest))
        for source, urls in sorted(_group_rows_by_source(rows).items()):
            returncodes.append(_run_capture_for_source(source, urls, output_root, args.brand_lexicon, args.dry_run))
    elif args.input_path:
        urls = [line.strip() for line in Path(args.input_path).read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
        returncodes.append(_run_capture_for_source(args.source, urls, output_root, args.brand_lexicon, args.dry_run))
    else:
        raise SystemExit("Either --feed_manifest or --input_path is required.")

    write_json(
        output_root / "malicious_capture_run.json",
        {
            "pipeline": "malicious",
            "feed_manifest": args.feed_manifest,
            "input_path": args.input_path,
            "returncodes": returncodes,
            "all_success": all(code == 0 for code in returncodes),
        },
    )
    raise SystemExit(0 if all(code == 0 for code in returncodes) else 1)


if __name__ == "__main__":
    main()
