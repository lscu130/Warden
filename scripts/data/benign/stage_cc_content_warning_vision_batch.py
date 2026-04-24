#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# operator: Codex; task: cc-content-warning-vision-review; date: 2026-04-24

"""Stage repo-local screenshot batches for Claude Code visual review."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, write_jsonl
from scripts.data.common.runtime_data_root import data_path

DEFAULT_SOURCE = data_path("raw", "benign", "hard benign", "content_warning_manual_review_20260424")
DEFAULT_OUT_ROOT = REPO_ROOT / "tmp" / "cc_content_warning_vision_review_20260424"

BASELINES = [
    {
        "sample_id": "baseline_adult_18porncomic.com_20260420T113554Z",
        "expected_label": "adult",
        "source_image": data_path("raw", "benign", "hard benign", "adult", "18porncomic.com_20260420T113554Z", "screenshot_viewport.png"),
    },
    {
        "sample_id": "baseline_gambling_1xbet-benv.top_20260330T085847Z",
        "expected_label": "gambling",
        "source_image": data_path("raw", "benign", "hard benign", "gambling", "1xbet-benv.top_20260330T085847Z", "screenshot_viewport.png"),
    },
    {
        "sample_id": "baseline_benign_101.ru_20260422T041006Z",
        "expected_label": "benign_or_false_positive",
        "source_image": data_path(
            "raw",
            "benign",
            "hard benign",
            "content_warning_manual_review_20260424",
            "101.ru_20260422T041006Z",
            "screenshot_viewport.png",
        ),
    },
]


def safe_name(text: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in text)


def sample_dirs(source: Path) -> List[Path]:
    return sorted(path for path in source.iterdir() if path.is_dir())


def copy_image(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage a CC screenshot vision-review batch.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="manual review sample root")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="repo-local staging root")
    parser.add_argument("--batch-id", default="batch_0001", help="batch directory name")
    parser.add_argument("--offset", type=int, default=0, help="start offset in sorted source dirs")
    parser.add_argument("--limit", type=int, default=50, help="number of candidate screenshots to stage")
    parser.add_argument("--include-baselines", action="store_true", help="include baseline screenshots in the batch")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = Path(args.source)
    batch_dir = ensure_dir(Path(args.out_root) / args.batch_id)
    image_dir = ensure_dir(batch_dir / "images")
    rows: List[Dict[str, Any]] = []

    if args.include_baselines:
        for baseline in BASELINES:
            src = Path(baseline["source_image"])
            dst = image_dir / f"{safe_name(baseline['sample_id'])}.png"
            copied = copy_image(src, dst)
            rows.append(
                {
                    "record_type": "baseline",
                    "sample_id": baseline["sample_id"],
                    "expected_label": baseline["expected_label"],
                    "source_image": str(src),
                    "staged_image": str(dst),
                    "copy_status": "copied" if copied else "missing_source_image",
                }
            )

    dirs = sample_dirs(source)
    selected = dirs[args.offset : args.offset + args.limit]
    for sample_dir in selected:
        src = sample_dir / "screenshot_viewport.png"
        dst = image_dir / f"{safe_name(sample_dir.name)}.png"
        copied = copy_image(src, dst)
        rows.append(
            {
                "record_type": "candidate",
                "sample_id": sample_dir.name,
                "source_dir": str(sample_dir),
                "source_image": str(src),
                "staged_image": str(dst),
                "copy_status": "copied" if copied else "missing_source_image",
            }
        )

    manifest_path = batch_dir / "batch_manifest.jsonl"
    write_jsonl(manifest_path, rows)
    print(f"[done] batch_dir={batch_dir}")
    print(f"[done] manifest={manifest_path}")
    print(f"[done] records={len(rows)}")
    print(f"[done] candidates={len(selected)}")


if __name__ == "__main__":
    main()
