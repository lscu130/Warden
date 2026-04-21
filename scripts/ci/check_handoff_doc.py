#!/usr/bin/env python3

"""
check_handoff_doc.py

Read-only structural lint for Warden non-trivial handoff documents.
This checker validates the presence of required template sections only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence


REQUIRED_MARKERS = [
    "# Handoff Metadata",
    "- Handoff ID:",
    "- Related Task ID:",
    "- Task Title:",
    "- Module:",
    "- Author:",
    "- Date:",
    "- Status:",
    "## 中文版",
    "## English Version",
    "## 1. Executive Summary",
    "## 2. What Changed",
    "## 3. Files Touched",
    "## 4. Behavior Impact",
    "### Expected New Behavior",
    "### Preserved Behavior",
    "### User-facing / CLI Impact",
    "### Output Format Impact",
    "## 5. Schema / Interface Impact",
    "## 6. Validation Performed",
    "### Commands Run",
    "### Result",
    "### Not Run",
    "## 7. Risks / Caveats",
    "## 8. Docs Impact",
    "## 9. Recommended Next Step",
]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check required Warden handoff-doc sections and metadata markers."
    )
    parser.add_argument("paths", nargs="+", help="One or more handoff Markdown files to check.")
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def lint_handoff_doc(path: Path) -> List[str]:
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
        issues = lint_handoff_doc(path)
        if issues:
            failed = True
            print(f"[handoff-doc] FAIL {path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[handoff-doc] OK   {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
