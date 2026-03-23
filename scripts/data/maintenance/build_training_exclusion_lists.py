#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, read_jsonl, write_jsonl
from scripts.data.common.pool_utils import build_training_exclusion_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Build malicious training exclusion lists from pool decisions.")
    parser.add_argument("--pool_decisions_path", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "malicious_exclusions"))
    args = parser.parse_args()

    decisions = read_jsonl(Path(args.pool_decisions_path))
    output_dir = ensure_dir(Path(args.output_dir))
    write_jsonl(output_dir / "training_exclusion_list.jsonl", build_training_exclusion_list(decisions))


if __name__ == "__main__":
    main()
