#!/usr/bin/env python3

"""
run_harness_checks.py

Thin local entrypoint for the Warden harness checks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Dict, Sequence

import check_handoff_doc
import check_schema_compat
import check_task_doc


REPO_ROOT = Path(__file__).resolve().parents[2]

FIXTURE_SUITES = {
    "positive": {
        "task_doc": Path("tests/fixtures/harness/task_doc/positive_minimal.md"),
        "handoff_doc": Path("tests/fixtures/harness/handoff_doc/positive_minimal.md"),
        "schema": Path("tests/fixtures/harness/schema/positive_manifest_record.json"),
    },
    "negative": {
        "task_doc": Path("tests/fixtures/harness/task_doc/negative_missing_requested_by.md"),
        "handoff_doc": Path("tests/fixtures/harness/handoff_doc/negative_missing_not_run.md"),
        "schema": Path("tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json"),
    },
}


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local Warden harness fixture checks."
    )
    parser.add_argument(
        "--suite",
        choices=["positive", "negative"],
        default="positive",
        help="Fixture suite to run. Default: positive.",
    )
    parser.add_argument(
        "--only",
        choices=["task_doc", "handoff_doc", "schema"],
        help="Optionally run only one checker.",
    )
    return parser.parse_args(argv)


def run_task_doc(path: Path) -> bool:
    return not check_task_doc.lint_task_doc(path)


def run_handoff_doc(path: Path) -> bool:
    return not check_handoff_doc.lint_handoff_doc(path)


def run_schema(path: Path) -> bool:
    return not check_schema_compat.run_check("manifest_record", path)


RUNNERS: Dict[str, Callable[[Path], bool]] = {
    "task_doc": run_task_doc,
    "handoff_doc": run_handoff_doc,
    "schema": run_schema,
}


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    fixture_map = FIXTURE_SUITES[args.suite]
    names = [args.only] if args.only else ["task_doc", "handoff_doc", "schema"]
    failed = False

    for name in names:
        fixture_rel = fixture_map[name]
        fixture_path = REPO_ROOT / fixture_rel
        ok = RUNNERS[name](fixture_path)
        print(
            f"[harness-runner] {'PASS' if ok else 'FAIL'} "
            f"{name} suite={args.suite} fixture={fixture_rel.as_posix()}"
        )
        if not ok:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
