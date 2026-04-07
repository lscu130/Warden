#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, read_json, write_json, write_lines
from scripts.data.common.url_utils import canonicalize_url

BENIGN_RUNNER = REPO_ROOT / "scripts" / "data" / "benign" / "run_benign_capture.py"

REQUIRED_SAMPLE_FILES = [
    "meta.json",
    "url.json",
    "env.json",
    "forms.json",
    "net_summary.json",
    "screenshot_viewport.png",
    "auto_labels.json",
]
CONTENT_SAMPLE_FILES = [
    "html_rendered.html",
    "visible_text.txt",
]


def now_utc_compact() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_input_urls(input_path: Path) -> Tuple[List[Dict[str, Any]], int]:
    line_count = 0
    rows: List[Dict[str, Any]] = []
    seen: set[str] = set()
    with input_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for lineno, line in enumerate(handle, 1):
            original = line.strip()
            if not original or original.startswith("#"):
                continue
            line_count += 1
            canonical = canonicalize_url(original)
            if not canonical or canonical in seen:
                continue
            seen.add(canonical)
            rows.append(
                {
                    "line_no": lineno,
                    "original_url": original,
                    "canonical_url": canonical,
                }
            )
    return rows, line_count


def iter_batch_sample_dirs(output_root: Path) -> Iterable[Path]:
    if not output_root.exists():
        return []
    return sorted(
        [
            child
            for child in output_root.iterdir()
            if child.is_dir() and not child.name.startswith("_")
        ],
        key=lambda p: p.name.lower(),
    )


def inspect_sample_dir(sample_dir: Path, input_canonical_urls: set[str]) -> Dict[str, Any]:
    record: Dict[str, Any] = {
        "sample_dir": sample_dir.name,
        "sample_dir_path": str(sample_dir),
        "status": "partial",
        "input_url": "",
        "canonical_input_url": "",
        "missing_files": [],
        "has_content_file": False,
        "outside_input": False,
    }

    url_json_path = sample_dir / "url.json"
    if not url_json_path.exists():
        record["missing_files"] = ["url.json"]
        return record

    try:
        url_payload = read_json(url_json_path)
    except Exception as exc:
        record["missing_files"] = [f"url.json:parse_error:{type(exc).__name__}"]
        return record

    input_url = str(url_payload.get("input_url") or "").strip()
    canonical_input_url = canonicalize_url(input_url)
    record["input_url"] = input_url
    record["canonical_input_url"] = canonical_input_url
    record["outside_input"] = bool(canonical_input_url and canonical_input_url not in input_canonical_urls)

    missing_files = [name for name in REQUIRED_SAMPLE_FILES if not (sample_dir / name).exists()]
    has_content_file = any((sample_dir / name).exists() for name in CONTENT_SAMPLE_FILES)
    if not has_content_file:
        missing_files.append("html_rendered.html|visible_text.txt")

    record["missing_files"] = missing_files
    record["has_content_file"] = has_content_file
    record["status"] = "complete" if canonical_input_url and not missing_files else "partial"
    return record


def build_inventory_state(input_rows: List[Dict[str, Any]], input_line_count: int, output_root: Path) -> Dict[str, Any]:
    input_canonical_urls = {row["canonical_url"] for row in input_rows}
    input_original_by_canonical = {row["canonical_url"]: row["original_url"] for row in input_rows}

    sample_records: List[Dict[str, Any]] = []
    captured_map: Dict[str, List[str]] = {}
    outside_input_samples: List[Dict[str, Any]] = []

    for sample_dir in iter_batch_sample_dirs(output_root):
        record = inspect_sample_dir(sample_dir, input_canonical_urls)
        sample_records.append(record)
        canonical_input_url = record.get("canonical_input_url") or ""
        if record.get("outside_input"):
            outside_input_samples.append(record)
        if record.get("status") == "complete" and canonical_input_url:
            captured_map.setdefault(canonical_input_url, []).append(record["sample_dir"])

    duplicate_captured_urls = [
        {
            "canonical_url": canonical_url,
            "input_url": input_original_by_canonical.get(canonical_url, canonical_url),
            "sample_dirs": sample_dirs,
        }
        for canonical_url, sample_dirs in sorted(captured_map.items())
        if len(sample_dirs) > 1
    ]

    captured_canonical_urls = {canonical_url for canonical_url in captured_map}
    captured_urls = [
        row["original_url"]
        for row in input_rows
        if row["canonical_url"] in captured_canonical_urls
    ]
    missing_rows = [
        row
        for row in input_rows
        if row["canonical_url"] not in captured_canonical_urls
    ]
    missing_urls = [row["original_url"] for row in missing_rows]

    partial_samples = []
    retry_partial_count = 0
    for record in sample_records:
        if record.get("status") == "complete":
            continue
        canonical_input_url = record.get("canonical_input_url") or ""
        retry_required = bool(
            canonical_input_url
            and canonical_input_url in input_canonical_urls
            and canonical_input_url not in captured_canonical_urls
        )
        partial_record = dict(record)
        partial_record["retry_required"] = retry_required
        partial_samples.append(partial_record)
        if retry_required:
            retry_partial_count += 1

    inventory = {
        "generated_at_utc": now_utc_compact(),
        "input_count": input_line_count,
        "unique_input_count": len(input_rows),
        "sample_dir_count": len(sample_records),
        "captured_count": len(captured_urls),
        "missing_count": len(missing_urls),
        "partial_sample_count": len(partial_samples),
        "retry_partial_count": retry_partial_count,
        "duplicate_captured_count": len(duplicate_captured_urls),
        "outside_input_count": len(outside_input_samples),
        "duplicate_captured_urls": duplicate_captured_urls,
        "outside_input_samples": outside_input_samples,
    }
    return {
        "inventory": inventory,
        "captured_urls": captured_urls,
        "missing_urls": missing_urls,
        "captured_canonical_urls": sorted(captured_canonical_urls),
        "missing_canonical_urls": [row["canonical_url"] for row in missing_rows],
        "partial_samples": partial_samples,
    }


def build_partial_retry_artifacts(state: Dict[str, Any]) -> Tuple[List[str], List[str], List[Dict[str, Any]]]:
    partial_retry_records = [
        record
        for record in state["partial_samples"]
        if record.get("retry_required")
    ]
    partial_retry_urls = [
        record["input_url"]
        for record in partial_retry_records
        if record.get("input_url")
    ]
    partial_retry_sample_dirs = [
        record["sample_dir_path"]
        for record in partial_retry_records
        if record.get("sample_dir_path")
    ]
    return partial_retry_urls, partial_retry_sample_dirs, partial_retry_records


def write_inventory_artifacts(recovery_dir: Path, state: Dict[str, Any]) -> None:
    partial_retry_urls, partial_retry_sample_dirs, partial_retry_records = build_partial_retry_artifacts(state)
    write_json(recovery_dir / "inventory.json", state["inventory"])
    write_lines(recovery_dir / "captured_urls.txt", state["captured_urls"])
    write_lines(recovery_dir / "missing_urls.txt", state["missing_urls"])
    write_json(recovery_dir / "partial_samples.json", state["partial_samples"])
    write_lines(recovery_dir / "partial_retry_urls.txt", partial_retry_urls)
    write_lines(recovery_dir / "partial_retry_sample_dirs.txt", partial_retry_sample_dirs)
    write_json(recovery_dir / "partial_retry_samples.json", partial_retry_records)


def quarantine_partial_sample_dirs(recovery_dir: Path, partial_retry_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    quarantine_dir = ensure_dir(recovery_dir / "partial_quarantine")
    moved_records: List[Dict[str, Any]] = []
    for record in partial_retry_records:
        src = Path(str(record.get("sample_dir_path") or "")).resolve()
        if not src.exists():
            continue

        dst = quarantine_dir / src.name
        suffix = 1
        while dst.exists():
            dst = quarantine_dir / f"{src.name}__dup{suffix:02d}"
            suffix += 1
        shutil.move(str(src), str(dst))
        moved_records.append(
            {
                "input_url": record.get("input_url", ""),
                "sample_dir": src.name,
                "from_path": str(src),
                "to_path": str(dst),
                "missing_files": record.get("missing_files", []),
            }
        )
    write_json(recovery_dir / "quarantined_partial_samples.json", moved_records)
    write_lines(
        recovery_dir / "quarantined_partial_sample_dirs.txt",
        [item["to_path"] for item in moved_records],
    )
    return moved_records


def chunked(rows: List[str], chunk_size: int) -> Iterable[List[str]]:
    for idx in range(0, len(rows), chunk_size):
        yield rows[idx : idx + chunk_size]


def build_runner_command(args: argparse.Namespace, chunk_input_path: Path, output_root: Path) -> List[str]:
    command = [
        sys.executable,
        str(BENIGN_RUNNER),
        "--input_path",
        str(chunk_input_path),
        "--output_root",
        str(output_root),
        "--source",
        args.source,
        "--rank_bucket",
        args.rank_bucket,
        "--page_type",
        args.page_type,
        "--language",
        args.language,
        "--nav_timeout_ms",
        str(args.nav_timeout_ms),
        "--goto_wait_until",
        args.goto_wait_until,
    ]
    if args.brand_lexicon:
        command.extend(["--brand_lexicon", args.brand_lexicon])
    if args.proxy_server:
        command.extend(["--proxy_server", args.proxy_server])
    if args.proxy_username:
        command.extend(["--proxy_username", args.proxy_username])
    if args.proxy_password:
        command.extend(["--proxy_password", args.proxy_password])
    if args.disable_route_intercept:
        command.append("--disable_route_intercept")
    return command


def copy_chunk_summary(output_root: Path, recovery_dir: Path, chunk_index: int) -> str:
    summary_src = output_root / "benign_capture_run.json"
    if not summary_src.exists():
        return ""
    summary_dst = recovery_dir / f"chunk_{chunk_index:04d}_benign_capture_run.json"
    shutil.copy2(summary_src, summary_dst)
    return str(summary_dst)


def main() -> None:
    parser = argparse.ArgumentParser(description="Recover a partially completed benign batch and retry only the missing URLs.")
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_root", type=str, required=True)
    parser.add_argument("--source", type=str, default="manual_benign")
    parser.add_argument("--rank_bucket", type=str, default="")
    parser.add_argument("--page_type", type=str, default="")
    parser.add_argument("--language", type=str, default="")
    parser.add_argument("--brand_lexicon", type=str, default="")
    parser.add_argument("--proxy_server", type=str, default="")
    parser.add_argument("--proxy_username", type=str, default="")
    parser.add_argument("--proxy_password", type=str, default="")
    parser.add_argument("--nav_timeout_ms", type=int, default=60000)
    parser.add_argument("--disable_route_intercept", action="store_true")
    parser.add_argument(
        "--goto_wait_until",
        type=str,
        default="commit",
        choices=["load", "domcontentloaded", "commit", "networkidle"],
    )
    parser.add_argument("--chunk_size", type=int, default=50)
    parser.add_argument("--inventory_only", action="store_true")
    parser.add_argument("--quarantine_partial_dirs", action="store_true")
    parser.add_argument("--recovery_dir", type=str, default="")
    args = parser.parse_args()

    if args.chunk_size <= 0:
        raise SystemExit("--chunk_size must be > 0")
    if args.inventory_only and args.quarantine_partial_dirs:
        raise SystemExit("--quarantine_partial_dirs cannot be used together with --inventory_only")

    input_path = Path(args.input_path)
    output_root = ensure_dir(Path(args.output_root))
    recovery_dir = (
        ensure_dir(Path(args.recovery_dir))
        if args.recovery_dir.strip()
        else ensure_dir(output_root / "_recovery" / now_utc_compact())
    )

    input_rows, input_line_count = read_input_urls(input_path)
    initial_state = build_inventory_state(input_rows, input_line_count, output_root)
    write_inventory_artifacts(recovery_dir, initial_state)
    initial_partial_retry_urls, _, initial_partial_retry_records = build_partial_retry_artifacts(initial_state)

    if initial_state["inventory"]["duplicate_captured_count"]:
        log(f"[WARN] duplicate captured URLs detected: {initial_state['inventory']['duplicate_captured_count']}")
    if initial_state["inventory"]["outside_input_count"]:
        log(f"[WARN] sample dirs outside current input detected: {initial_state['inventory']['outside_input_count']}")

    chunk_results: List[Dict[str, Any]] = []
    final_state = initial_state
    quarantined_partial_samples: List[Dict[str, Any]] = []

    if not args.inventory_only:
        if args.quarantine_partial_dirs and initial_partial_retry_records:
            log(f"[INFO] quarantining partial sample dirs before retry: {len(initial_partial_retry_records)}")
            quarantined_partial_samples = quarantine_partial_sample_dirs(recovery_dir, initial_partial_retry_records)
            final_state = build_inventory_state(input_rows, input_line_count, output_root)
            write_inventory_artifacts(recovery_dir, final_state)
        for chunk_index, chunk_urls in enumerate(chunked(initial_state["missing_urls"], args.chunk_size), 1):
            chunk_input_path = recovery_dir / f"chunk_{chunk_index:04d}_urls.txt"
            write_lines(chunk_input_path, chunk_urls)
            command = build_runner_command(args, chunk_input_path, output_root)
            log(f"[INFO] recovery chunk {chunk_index}: {len(chunk_urls)} URLs")
            started_at = now_utc_compact()
            completed = subprocess.run(command, cwd=str(REPO_ROOT))
            finished_at = now_utc_compact()

            pre_captured = set(final_state["captured_canonical_urls"])
            post_state = build_inventory_state(input_rows, input_line_count, output_root)
            post_captured = set(post_state["captured_canonical_urls"])
            post_missing = set(post_state["missing_canonical_urls"])
            write_inventory_artifacts(recovery_dir, post_state)
            summary_copy_path = copy_chunk_summary(output_root, recovery_dir, chunk_index)

            newly_captured = sorted(post_captured - pre_captured)
            remaining_in_chunk = [
                url
                for url in chunk_urls
                if canonicalize_url(url) in post_missing
            ]
            chunk_results.append(
                {
                    "chunk_index": chunk_index,
                    "started_at_utc": started_at,
                    "finished_at_utc": finished_at,
                    "input_count": len(chunk_urls),
                    "chunk_input_path": str(chunk_input_path),
                    "returncode": completed.returncode,
                    "summary_copy_path": summary_copy_path,
                    "captured_before": len(pre_captured),
                    "captured_after": len(post_captured),
                    "remaining_after": len(post_missing),
                    "newly_captured_count": len(newly_captured),
                    "newly_captured_urls": newly_captured,
                    "remaining_urls_in_chunk": remaining_in_chunk,
                    "command": command,
                }
            )
            final_state = post_state

    recovery_summary = {
        "generated_at_utc": now_utc_compact(),
        "input_path": str(input_path),
        "output_root": str(output_root),
        "recovery_dir": str(recovery_dir),
        "inventory_only": bool(args.inventory_only),
        "chunk_size": args.chunk_size,
        "initial_inventory": initial_state["inventory"],
        "final_inventory": final_state["inventory"],
        "initial_partial_retry_count": len(initial_partial_retry_urls),
        "quarantine_partial_dirs": bool(args.quarantine_partial_dirs),
        "quarantined_partial_sample_count": len(quarantined_partial_samples),
        "quarantined_partial_samples": quarantined_partial_samples,
        "chunk_results": chunk_results,
        "all_chunks_success": all(item["returncode"] == 0 for item in chunk_results),
        "fully_recovered": final_state["inventory"]["missing_count"] == 0,
        "notes": [
            "This recovery summary is the authoritative batch-level record for interrupted benign recovery.",
            "Successful retry samples remain under the original output_root; recovery bookkeeping stays under _recovery.",
            "Partial retry URLs are derived from sample directories on disk rather than from a batch manifest.",
        ],
    }
    write_json(recovery_dir / "recovery_summary.json", recovery_summary)

    if args.inventory_only:
        raise SystemExit(0)

    success = recovery_summary["all_chunks_success"] and recovery_summary["fully_recovered"]
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
