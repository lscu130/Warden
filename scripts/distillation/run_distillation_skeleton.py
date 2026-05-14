#!/usr/bin/env python3
"""CLI for the Warden distillation dry-run/mock skeleton."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from warden.distillation.runner import DistillationRunConfig, run_distillation


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Warden distillation skeleton in dry-run or mock mode.")
    parser.add_argument("--manifest", required=True, help="Input manifest CSV.")
    parser.add_argument("--output-dir", required=True, help="Output directory for skeleton artifacts.")
    parser.add_argument("--split", required=True, choices=["train", "val", "test", "unknown"], help="Requested split.")
    parser.add_argument("--mode", choices=["dry-run", "mock"], default="dry-run", help="Skeleton execution mode.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum rows to process; 0 means no limit.")
    parser.add_argument("--seed", type=int, default=0, help="Deterministic mock seed.")
    parser.add_argument("--resume", action="store_true", help="Skip already processed record ids.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing skeleton output files.")
    parser.add_argument("--diagnostic-only", action="store_true", help="Required for val/test skeleton runs.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    config = DistillationRunConfig(
        manifest=Path(args.manifest),
        output_dir=Path(args.output_dir),
        split=args.split,
        mode=args.mode,
        limit=args.limit,
        seed=args.seed,
        resume=args.resume,
        overwrite=args.overwrite,
        diagnostic_only=args.diagnostic_only,
    )
    result = run_distillation(config)
    print(
        "distillation skeleton complete: "
        f"processed={result.processed_count} "
        f"skipped_existing={result.skipped_existing_count} "
        f"errors={result.error_count} "
        f"review_queue={result.review_queue_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
