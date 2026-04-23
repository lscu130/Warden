#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, write_lines
from scripts.data.common.runtime_data_root import data_path


def _prompt_start_date() -> date:
    while True:
        raw = input("Enter PT verification start date (YYYY/M/D, e.g. 2026/3/27): ").replace("\x00", "").strip()
        parts = raw.split("/")
        if len(parts) != 3:
            log("[WARN] invalid date format; expected YYYY/M/D such as 2026/3/27")
            continue
        try:
            year, month, day = (int(part) for part in parts)
            return date(year, month, day)
        except Exception:
            log("[WARN] invalid date value; expected YYYY/M/D such as 2026/3/27")


def _parse_verification_time(value: str) -> datetime:
    text = value.strip()
    if not text:
        raise ValueError("empty verification_time")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _default_output_csv(output_dir: Path, start_date: date) -> Path:
    return output_dir / f"phishtank_verified_since_{start_date.isoformat()}_urls.csv"


def _default_output_txt(output_csv: Path) -> Path:
    return output_csv.with_suffix(".txt")


def _required_columns_present(fieldnames: Iterable[str] | None) -> Tuple[bool, str]:
    names = {str(name).strip() for name in (fieldnames or []) if str(name).strip()}
    missing = [column for column in ("url", "verification_time") if column not in names]
    if missing:
        return False, ", ".join(missing)
    return True, ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export both a URL-only CSV and a one-URL-per-line TXT from a PhishTank verified_online CSV by filtering rows on or after a prompted UTC verification date."
    )
    parser.add_argument("--source_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, default="")
    parser.add_argument("--output_txt", type=str, default="")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=str(data_path("processed", "pt_csv_exports")),
        help="Used only when --output_csv is not provided. The default TXT path is derived from the CSV path.",
    )
    args = parser.parse_args()

    source_csv = Path(args.source_csv)
    output_dir = ensure_dir(Path(args.output_dir))
    start_date = _prompt_start_date()
    output_csv = Path(args.output_csv) if args.output_csv else _default_output_csv(output_dir, start_date)
    output_txt = Path(args.output_txt) if args.output_txt else _default_output_txt(output_csv)
    ensure_dir(output_csv.parent)
    ensure_dir(output_txt.parent)

    selected_urls = []
    total_rows = 0
    missing_url_rows = 0
    missing_verification_rows = 0
    invalid_verification_rows = 0
    latest_verification_time_utc = ""

    with source_csv.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        ok, missing_columns = _required_columns_present(reader.fieldnames)
        if not ok:
            raise SystemExit(f"Missing required CSV columns: {missing_columns}")

        for row in reader:
            total_rows += 1
            url = str((row or {}).get("url") or "").strip()
            verification_time_text = str((row or {}).get("verification_time") or "").strip()

            if not url:
                missing_url_rows += 1
                continue
            if not verification_time_text:
                missing_verification_rows += 1
                continue

            try:
                verification_time_utc = _parse_verification_time(verification_time_text)
            except Exception:
                invalid_verification_rows += 1
                continue

            verification_iso = verification_time_utc.isoformat().replace("+00:00", "Z")
            if not latest_verification_time_utc or verification_iso > latest_verification_time_utc:
                latest_verification_time_utc = verification_iso

            if verification_time_utc.date() >= start_date:
                selected_urls.append(url)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["url"])
        writer.writeheader()
        for url in selected_urls:
            writer.writerow({"url": url})
    write_lines(output_txt, selected_urls)

    log(f"[INFO] source_csv={source_csv}")
    log(f"[INFO] output_csv={output_csv}")
    log(f"[INFO] output_txt={output_txt}")
    log(f"[INFO] start_date_utc={start_date.isoformat()}")
    log(f"[INFO] latest_verification_time_utc={latest_verification_time_utc or 'none'}")
    log(f"[INFO] total_rows={total_rows}")
    log(f"[INFO] selected_urls={len(selected_urls)}")
    log(f"[INFO] missing_url_rows={missing_url_rows}")
    log(f"[INFO] missing_verification_rows={missing_verification_rows}")
    log(f"[INFO] invalid_verification_rows={invalid_verification_rows}")


if __name__ == "__main__":
    main()
