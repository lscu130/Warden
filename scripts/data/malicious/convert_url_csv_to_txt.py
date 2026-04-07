#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, write_lines


def _required_columns_present(fieldnames: Iterable[str] | None) -> Tuple[bool, str]:
    names = {str(name).strip() for name in (fieldnames or []) if str(name).strip()}
    if "url" not in names:
        return False, "url"
    return True, ""


def _default_output_txt(input_csv: Path) -> Path:
    return input_csv.with_suffix(".txt")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a URL-only CSV with a 'url' column into a one-URL-per-line TXT file for capture."
    )
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_txt", type=str, default="")
    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    output_txt = Path(args.output_txt) if args.output_txt else _default_output_txt(input_csv)
    ensure_dir(output_txt.parent)

    urls = []
    total_rows = 0
    missing_url_rows = 0

    with input_csv.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        ok, missing_columns = _required_columns_present(reader.fieldnames)
        if not ok:
            raise SystemExit(f"Missing required CSV columns: {missing_columns}")

        for row in reader:
            total_rows += 1
            url = str((row or {}).get("url") or "").strip()
            if not url:
                missing_url_rows += 1
                continue
            urls.append(url)

    write_lines(output_txt, urls)

    log(f"[INFO] input_csv={input_csv}")
    log(f"[INFO] output_txt={output_txt}")
    log(f"[INFO] total_rows={total_rows}")
    log(f"[INFO] selected_urls={len(urls)}")
    log(f"[INFO] missing_url_rows={missing_url_rows}")


if __name__ == "__main__":
    main()
