#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Split primary benign direct sample directories into manual review batches.

This utility only moves direct child sample directories. A sample directory is
defined conservatively as a directory containing both meta.json and url.json.
It does not inspect or modify labels and does not edit files inside samples.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_BATCH_COUNT = 10


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def is_direct_sample_dir(path: Path) -> bool:
    return path.is_dir() and (path / "meta.json").exists() and (path / "url.json").exists()


def collect_direct_samples(input_root: Path, batch_root: Path) -> tuple[List[Path], List[Path]]:
    samples: List[Path] = []
    skipped: List[Path] = []
    batch_root_resolved = batch_root.resolve()

    for child in sorted(input_root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        try:
            if child.resolve() == batch_root_resolved:
                skipped.append(child)
                continue
        except OSError:
            skipped.append(child)
            continue
        if is_direct_sample_dir(child):
            samples.append(child)
        else:
            skipped.append(child)
    return samples, skipped


def assign_batches(samples: List[Path], batch_count: int) -> List[Dict[str, Any]]:
    total = len(samples)
    base = total // batch_count
    remainder = total % batch_count

    rows: List[Dict[str, Any]] = []
    cursor = 0
    for batch_index in range(batch_count):
        size = base + (1 if batch_index < remainder else 0)
        batch_name = f"batch_{batch_index + 1:02d}"
        for sample in samples[cursor : cursor + size]:
            rows.append(
                {
                    "sample_id": sample.name,
                    "batch": batch_name,
                    "source": str(sample),
                    "destination": "",
                    "status": "planned",
                }
            )
        cursor += size
    return rows


def build_summary(
    *,
    mode: str,
    input_root: Path,
    batch_root: Path,
    out_dir: Path,
    rows: List[Dict[str, Any]],
    skipped: List[Path],
    moved: int,
    failures: int,
) -> Dict[str, Any]:
    batch_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}
    for row in rows:
        batch = str(row["batch"])
        batch_counts[batch] = batch_counts.get(batch, 0) + 1
        status = str(row["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "generated_at_utc": utc_now(),
        "mode": mode,
        "input_root": str(input_root),
        "batch_root": str(batch_root),
        "out_dir": str(out_dir),
        "num_planned_samples": len(rows),
        "num_moved": moved,
        "num_failures": failures,
        "num_skipped_directories": len(skipped),
        "skipped_examples": [str(p) for p in skipped[:20]],
        "batch_counts": batch_counts,
        "status_counts": status_counts,
    }


def run(args: argparse.Namespace) -> int:
    input_root = Path(args.input_root).resolve()
    batch_root = Path(args.batch_root).resolve()
    out_dir = Path(args.out_dir).resolve()

    if not input_root.exists() or not input_root.is_dir():
        raise SystemExit(f"input root does not exist or is not a directory: {input_root}")

    try:
        batch_root.relative_to(input_root)
    except ValueError as exc:
        raise SystemExit(f"batch root must be inside input root: {batch_root}") from exc

    samples, skipped = collect_direct_samples(input_root, batch_root)
    rows = assign_batches(samples, args.batch_count)

    moved = 0
    failures = 0
    mode = "apply" if args.apply else "dry_run"

    for row in rows:
        src = Path(str(row["source"]))
        dst = batch_root / str(row["batch"]) / src.name
        row["destination"] = str(dst)

        if not args.apply:
            row["status"] = "planned"
            continue

        if not src.exists():
            row["status"] = "missing_source"
            failures += 1
            continue
        if dst.exists():
            row["status"] = "destination_exists"
            failures += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        row["status"] = "moved"
        moved += 1

    suffix = "apply" if args.apply else "dry_run"
    plan_path = out_dir / f"primary_benign_manual_10_batches_{suffix}.jsonl"
    summary_path = out_dir / f"primary_benign_manual_10_batches_{suffix}_summary.json"
    append_jsonl(plan_path, rows)
    summary = build_summary(
        mode=mode,
        input_root=input_root,
        batch_root=batch_root,
        out_dir=out_dir,
        rows=rows,
        skipped=skipped,
        moved=moved,
        failures=failures,
    )
    summary["artifacts"] = {
        "plan": str(plan_path),
        "summary": str(summary_path),
    }
    write_json(summary_path, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if failures else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", required=True, help="Primary benign input root.")
    parser.add_argument("--batch-root", required=True, help="Destination batch root inside input root.")
    parser.add_argument("--out-dir", required=True, help="Output directory for plan and summary files.")
    parser.add_argument("--batch-count", type=int, default=DEFAULT_BATCH_COUNT, help="Number of batches to create.")
    parser.add_argument("--apply", action="store_true", help="Move directories. Without this flag, only writes a dry-run plan.")
    args = parser.parse_args()
    if args.batch_count < 1:
        raise SystemExit("--batch-count must be >= 1")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
