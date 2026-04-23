#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, log, now_utc_iso, read_jsonl, write_json
from scripts.data.common.runtime_data_root import data_path

CAPTURE_SCRIPT = REPO_ROOT / "scripts" / "capture" / "capture_url_v6_optimized_v6_2_plus_labels_brandlex.py"


def _build_capture_command(
    source: str,
    input_path: Path,
    output_root: Path,
    brand_lexicon: str,
    proxy_server: str,
    proxy_username: str,
    proxy_password: str,
    nav_timeout_ms: int,
    disable_route_intercept: bool,
    goto_wait_until: str,
    dry_run: bool,
) -> List[str]:
    metadata = {
        "pipeline": "malicious",
        "source": source,
        "run_timestamp_utc": now_utc_iso(),
    }
    command = [
        sys.executable,
        str(CAPTURE_SCRIPT),
        "--input_path",
        str(input_path),
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
    if proxy_server:
        command.extend(["--proxy_server", proxy_server])
    if proxy_username:
        command.extend(["--proxy_username", proxy_username])
    if proxy_password:
        command.extend(["--proxy_password", proxy_password])
    if nav_timeout_ms and nav_timeout_ms > 0:
        command.extend(["--nav_timeout_ms", str(nav_timeout_ms)])
    if disable_route_intercept:
        command.append("--disable_route_intercept")
    if goto_wait_until:
        command.extend(["--goto_wait_until", goto_wait_until])
    if dry_run:
        command.append("--dry_run")
    return command


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
    proxy_server: str,
    proxy_username: str,
    proxy_password: str,
    nav_timeout_ms: int,
    disable_route_intercept: bool,
    goto_wait_until: str,
    dry_run: bool,
) -> int:
    if not urls:
        return 0
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        handle.write("\n".join(urls) + "\n")
        temp_path = Path(handle.name)
    command = _build_capture_command(
        source,
        temp_path,
        output_root,
        brand_lexicon,
        proxy_server,
        proxy_username,
        proxy_password,
        nav_timeout_ms,
        disable_route_intercept,
        goto_wait_until,
        dry_run,
    )
    log(f"[INFO] malicious capture for source={source}: {' '.join(command)}")
    try:
        completed = subprocess.run(command, cwd=str(REPO_ROOT))
        return completed.returncode
    finally:
        try:
            temp_path.unlink()
        except Exception:
            pass


def _read_supervised_targets(feed_manifest: str, input_path: str, source: str) -> List[Tuple[str, str]]:
    targets: List[Tuple[str, str]] = []
    if feed_manifest:
        rows = read_jsonl(Path(feed_manifest))
        for row in rows:
            item_source = str((row or {}).get("source") or "manual_malicious").strip() or "manual_malicious"
            url = str((row or {}).get("original_url") or (row or {}).get("normalized_url") or "").strip()
            if url:
                targets.append((item_source, url))
        return targets

    if input_path:
        return [(source, line.strip()) for line in Path(input_path).read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]

    raise SystemExit("Either --feed_manifest or --input_path is required.")


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
        log(f"[WARN] failed to terminate current malicious URL worker for reason={reason}: {exc!r}")


def _list_sample_dirs(output_root: Path) -> Dict[str, Path]:
    if not output_root.exists():
        return {}
    return {
        child.name: child
        for child in output_root.iterdir()
        if child.is_dir() and not child.name.startswith("_")
    }


def _delete_sample_dirs(paths: List[Path]) -> List[str]:
    deleted: List[str] = []
    for path in paths:
        try:
            if path.exists() and path.is_dir():
                shutil.rmtree(path, ignore_errors=False)
                deleted.append(str(path))
        except Exception as exc:
            log(f"[WARN] failed to delete partial malicious sample dir {path}: {exc!r}")
    return deleted


def run_supervised_capture(args: argparse.Namespace, output_root: Path) -> int:
    targets = _read_supervised_targets(args.feed_manifest, args.input_path, args.source)
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
    deleted_partial_sample_dirs: List[str] = []

    for index, (source, url) in enumerate(targets, 1):
        while not skip_queue.empty():
            try:
                skip_queue.get_nowait()
            except queue.Empty:
                break

        before_dirs = _list_sample_dirs(output_root)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
            handle.write(url + "\n")
            temp_input_path = Path(handle.name)

        command = _build_capture_command(
            source,
            temp_input_path,
            output_root,
            args.brand_lexicon,
            args.proxy_server,
            args.proxy_username,
            args.proxy_password,
            args.nav_timeout_ms,
            args.disable_route_intercept,
            args.goto_wait_until,
            args.dry_run,
        )
        log(f"[INFO] supervised malicious capture [{index}/{len(targets)}] source={source} url={url}")
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

        after_dirs = _list_sample_dirs(output_root)
        new_dirs = [path for name, path in after_dirs.items() if name not in before_dirs]
        deleted_dirs: List[str] = []
        if status != "success" and new_dirs:
            deleted_dirs = _delete_sample_dirs(new_dirs)
            deleted_partial_sample_dirs.extend(deleted_dirs)

        child_returncodes.append(returncode)
        results.append(
            {
                "index": index,
                "source": source,
                "url": url,
                "status": status,
                "returncode": returncode,
                "elapsed_ms": elapsed_ms,
                "deleted_sample_dirs": deleted_dirs,
            }
        )
        if termination_reason:
            log(f"[INFO] current malicious URL ended with status={status} after {elapsed_ms} ms")
        elif status == "failed":
            log(f"[INFO] current malicious URL failed after {elapsed_ms} ms; deleted_partial_dirs={len(deleted_dirs)}")

    write_json(
        output_root / "malicious_capture_run.json",
        {
            "pipeline": "malicious",
            "feed_manifest": args.feed_manifest,
            "input_path": args.input_path,
            "source": args.source,
            "returncodes": child_returncodes,
            "all_success": all(item["status"] == "success" for item in results),
            "supervised_mode": True,
            "interactive_skip": bool(args.interactive_skip),
            "url_hard_timeout_ms": args.url_hard_timeout_ms,
            "skipped_urls": [item["url"] for item in results if item["status"] == "skipped_by_user"],
            "timed_out_urls": [item["url"] for item in results if item["status"] == "timed_out"],
            "deleted_partial_sample_dirs": deleted_partial_sample_dirs,
            "results": results,
        },
    )
    return 0 if all(item["status"] == "success" for item in results) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the malicious upper-layer capture pipeline.")
    parser.add_argument("--feed_manifest", type=str, default="")
    parser.add_argument("--input_path", type=str, default="")
    parser.add_argument("--source", type=str, default="manual_malicious")
    parser.add_argument("--output_root", type=str, default=str(data_path("raw", "phish")))
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

    returncodes: List[int] = []

    if args.feed_manifest:
        rows = read_jsonl(Path(args.feed_manifest))
        for source, urls in sorted(_group_rows_by_source(rows).items()):
            returncodes.append(
                _run_capture_for_source(
                    source,
                    urls,
                    output_root,
                    args.brand_lexicon,
                    args.proxy_server,
                    args.proxy_username,
                    args.proxy_password,
                    args.nav_timeout_ms,
                    args.disable_route_intercept,
                    args.goto_wait_until,
                    args.dry_run,
                )
            )
    elif args.input_path:
        urls = [line.strip() for line in Path(args.input_path).read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
        returncodes.append(
            _run_capture_for_source(
                args.source,
                urls,
                output_root,
                args.brand_lexicon,
                args.proxy_server,
                args.proxy_username,
                args.proxy_password,
                args.nav_timeout_ms,
                args.disable_route_intercept,
                args.goto_wait_until,
                args.dry_run,
            )
        )
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
