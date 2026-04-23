#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, now_utc_iso, write_json
from scripts.data.common.runtime_data_root import data_path

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


def build_capture_command(args: argparse.Namespace, input_path: Path, input_format: str = "", csv_url_column: str = "") -> List[str]:
    ingest_metadata = build_ingest_metadata(args)
    command = [
        sys.executable,
        str(CAPTURE_SCRIPT),
        "--input_path",
        str(input_path),
        "--input_format",
        input_format or args.input_format,
        "--csv_url_column",
        csv_url_column or args.csv_url_column,
        "--label",
        "benign",
        "--output_root",
        str(args.output_root),
        "--ingest_metadata_json",
        json.dumps(ingest_metadata, ensure_ascii=False),
    ]
    if args.brand_lexicon:
        command.extend(["--brand_lexicon", args.brand_lexicon])
    if args.proxy_server:
        command.extend(["--proxy_server", args.proxy_server])
    if args.proxy_username:
        command.extend(["--proxy_username", args.proxy_username])
    if args.proxy_password:
        command.extend(["--proxy_password", args.proxy_password])
    if args.nav_timeout_ms and args.nav_timeout_ms > 0:
        command.extend(["--nav_timeout_ms", str(args.nav_timeout_ms)])
    if args.disable_route_intercept:
        command.append("--disable_route_intercept")
    if args.goto_wait_until:
        command.extend(["--goto_wait_until", args.goto_wait_until])
    if args.dry_run:
        command.append("--dry_run")
    return command


def read_urls(input_path: Path, input_format: str, csv_url_column: str) -> List[str]:
    if input_format == "txt":
        return [
            line.strip()
            for line in input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]

    rows: List[str] = []
    with input_path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        if csv_url_column not in (reader.fieldnames or []):
            raise SystemExit(f"csv column not found: {csv_url_column}")
        for row in reader:
            value = str((row or {}).get(csv_url_column) or "").strip()
            if value:
                rows.append(value)
    return rows


def _stdin_skip_listener(skip_queue: "queue.Queue[str]") -> None:
    while True:
        try:
            text = input().strip().lower()
        except EOFError:
            return
        except Exception:
            return
        if text == "skip":
            skip_queue.put("skip")
        elif text:
            log(f"[INFO] unknown operator command: {text!r}; type 'skip' and press Enter to abort the current URL.")


def _kill_process_tree(proc: subprocess.Popen, reason: str) -> None:
    if proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            proc.kill()
    except Exception as exc:
        log(f"[WARN] failed to terminate current URL worker for reason={reason}: {exc!r}")


def run_supervised_capture(args: argparse.Namespace, output_root: Path) -> int:
    urls = read_urls(Path(args.input_path), args.input_format, args.csv_url_column)
    skip_queue: "queue.Queue[str]" = queue.Queue()
    listener_started = False
    if args.interactive_skip and sys.stdin and sys.stdin.isatty():
        thread = threading.Thread(target=_stdin_skip_listener, args=(skip_queue,), daemon=True)
        thread.start()
        listener_started = True
        log("[INFO] interactive skip enabled; type 'skip' and press Enter to abort only the current URL.")
    elif args.interactive_skip:
        log("[WARN] --interactive_skip requested, but stdin is not a TTY; skip commands will be unavailable.")

    results = []
    child_returncodes: List[int] = []
    for index, url in enumerate(urls, 1):
        while not skip_queue.empty():
            try:
                skip_queue.get_nowait()
            except queue.Empty:
                break

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
            handle.write(url + "\n")
            temp_input_path = Path(handle.name)

        command = build_capture_command(args, temp_input_path, input_format="txt", csv_url_column="url")
        log(f"[INFO] supervised benign capture [{index}/{len(urls)}] {url}")
        if listener_started:
            log("       operator control: type 'skip' and press Enter to stop only this URL.")

        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        started_at = time.time()
        proc = subprocess.Popen(
            command,
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
        )
        termination_reason = ""

        try:
            while True:
                returncode = proc.poll()
                if returncode is not None:
                    break

                if listener_started:
                    try:
                        skip_queue.get_nowait()
                        termination_reason = "skip"
                    except queue.Empty:
                        pass

                if not termination_reason and args.url_hard_timeout_ms > 0:
                    elapsed_ms = int((time.time() - started_at) * 1000)
                    if elapsed_ms >= args.url_hard_timeout_ms:
                        termination_reason = "hard_timeout"

                if termination_reason:
                    _kill_process_tree(proc, termination_reason)
                    break

                time.sleep(0.25)

            try:
                returncode = proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                _kill_process_tree(proc, termination_reason or "post_kill_wait_timeout")
                try:
                    returncode = proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    returncode = proc.poll() if proc.poll() is not None else -9
        finally:
            try:
                temp_input_path.unlink()
            except Exception:
                pass

        elapsed_ms = int((time.time() - started_at) * 1000)
        status = "success" if returncode == 0 and not termination_reason else "failed"
        if termination_reason == "skip":
            status = "skipped_by_user"
        elif termination_reason == "hard_timeout":
            status = "timed_out"

        child_returncodes.append(returncode)
        results.append(
            {
                "index": index,
                "url": url,
                "status": status,
                "returncode": returncode,
                "elapsed_ms": elapsed_ms,
            }
        )
        if termination_reason:
            log(f"[INFO] current URL ended with status={status} after {elapsed_ms} ms")

    ingest_metadata = build_ingest_metadata(args)
    write_json(
        output_root / "benign_capture_run.json",
        {
            "pipeline": "benign",
            "input_path": args.input_path,
            "input_format": args.input_format,
            "csv_url_column": args.csv_url_column,
            "ingest_metadata": ingest_metadata,
            "returncode": 0 if all(item["status"] == "success" for item in results) else 1,
            "supervised_mode": True,
            "interactive_skip": bool(args.interactive_skip),
            "url_hard_timeout_ms": args.url_hard_timeout_ms,
            "all_success": all(item["status"] == "success" for item in results),
            "child_returncodes": child_returncodes,
            "skipped_urls": [item["url"] for item in results if item["status"] == "skipped_by_user"],
            "timed_out_urls": [item["url"] for item in results if item["status"] == "timed_out"],
            "results": results,
        },
    )
    return 0 if all(item["status"] == "success" for item in results) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the benign upper-layer capture pipeline.")
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--input_format", type=str, default="txt", choices=["txt", "csv"])
    parser.add_argument("--csv_url_column", type=str, default="url")
    parser.add_argument("--output_root", type=str, default=str(data_path("raw", "benign")))
    parser.add_argument("--source", type=str, default="manual_benign")
    parser.add_argument("--rank_bucket", type=str, default="")
    parser.add_argument("--page_type", type=str, default="")
    parser.add_argument("--language", type=str, default="")
    parser.add_argument("--hard_benign", action="store_true")
    parser.add_argument("--brand_lexicon", type=str, default="")
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--proxy_server", type=str, default="")
    parser.add_argument("--proxy_username", type=str, default="")
    parser.add_argument("--proxy_password", type=str, default="")
    parser.add_argument("--nav_timeout_ms", type=int, default=0)
    parser.add_argument("--disable_route_intercept", action="store_true")
    parser.add_argument(
        "--goto_wait_until",
        type=str,
        default="commit",
        choices=["load", "domcontentloaded", "commit", "networkidle"],
    )
    parser.add_argument("--interactive_skip", action="store_true")
    parser.add_argument("--url_hard_timeout_ms", type=int, default=0)
    args = parser.parse_args()

    output_root = ensure_dir(Path(args.output_root))
    if args.interactive_skip or (args.url_hard_timeout_ms and args.url_hard_timeout_ms > 0):
        raise SystemExit(run_supervised_capture(args, output_root))

    ingest_metadata = build_ingest_metadata(args)
    command = build_capture_command(args, Path(args.input_path))
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
