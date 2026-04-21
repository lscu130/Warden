#!/usr/bin/env python3

"""
check_task_doc.py

Read-only structural lint for Warden non-trivial task documents.
This checker validates the presence of required template sections only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence


REQUIRED_MARKERS = [
    "# Task Metadata",
    "- Task ID:",
    "- Task Title:",
    "- Owner Role:",
    "- Priority:",
    "- Status:",
    "- Related Module:",
    "- Related Issue / ADR / Doc:",
    "- Created At:",
    "- Requested By:",
    "## 中文版",
    "## English Version",
    "## 1. Background",
    "## 2. Goal",
    "## 3. Scope In",
    "## 4. Scope Out",
    "## 5. Inputs",
    "## 6. Required Outputs",
    "## 7. Hard Constraints",
    "## 8. Interface / Schema Constraints",
    "## 10. Acceptance Criteria",
    "## 11. Validation Checklist",
]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check required Warden task-doc sections and metadata markers."
    )
    parser.add_argument("paths", nargs="+", help="One or more task Markdown files to check.")
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def lint_task_doc(path: Path) -> List[str]:
    issues: List[str] = []
    if not path.exists():
        return [f"missing file: {path}"]
    if not path.is_file():
        return [f"not a file: {path}"]

    text = read_text(path)
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            issues.append(f"missing marker: {marker}")
    return issues


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    failed = False

    for raw_path in args.paths:
        path = Path(raw_path)
        issues = lint_task_doc(path)
        if issues:
            failed = True
            print(f"[task-doc] FAIL {path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[task-doc] OK   {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
