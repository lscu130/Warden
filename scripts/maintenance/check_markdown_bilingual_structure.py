#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
check_markdown_bilingual_structure.py

用途：
- 检查 Warden 仓库内业务 Markdown 的中英双语结构
- 只读扫描，不自动修复文档
- 支持终端摘要输出和可选 JSON 报告

默认检查：
1) 是否同时存在 `## 中文版` 和 `## English Version`
2) 中文区块是否存在明显乱码标题，如 `## ???`
3) 中文区块是否残留模板占位符，如 `$taskId`
4) 中文区块是否过薄，接近“只有中文壳没有实质摘要”

默认排除：
- data/processed/**
- docs/STRUCTION.md
- STRUCTION.md
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


DEFAULT_EXCLUDE_GLOBS = [
    "data/processed/**",
    "docs/STRUCTION.md",
    "STRUCTION.md",
]

CN_MARKER = "## 中文版"
EN_MARKER = "## English Version"

PLACEHOLDER_RE = re.compile(r"\$taskId|\$status|\$module|\$title")
GARBLED_HEADING_RE = re.compile(r"(?m)^(?:##|###)\s+[?？]{2,}\s*$")
CODE_BLOCK_RE = re.compile(r"(?s)```.*?```")
CJK_RE = re.compile(r"[\u3400-\u9fff]")
NON_USAGE_HEADING_RE = re.compile(r"(?m)^##\s+(?!中文版\s*$).+|^###\s+(?!使用说明\s*$).+")
BULLET_LINE_RE = re.compile(r"(?m)^- ")


def log(message: str) -> None:
    print(message, flush=True)


def normalize_rel_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def should_exclude(rel_path: str, exclude_globs: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in exclude_globs)


def discover_markdown_files(root: Path, exclude_globs: Sequence[str]) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*.md"):
        if not path.is_file():
            continue
        rel_path = normalize_rel_path(path, root)
        if should_exclude(rel_path, exclude_globs):
            continue
        files.append(path)
    return sorted(files)


def strip_code_blocks(text: str) -> str:
    return CODE_BLOCK_RE.sub("", text)


def collect_cn_metrics(cn_section: str) -> Dict[str, int]:
    cn_no_code = strip_code_blocks(cn_section)
    return {
        "cn_char_count": len(CJK_RE.findall(cn_no_code)),
        "non_usage_heading_count": len(NON_USAGE_HEADING_RE.findall(cn_no_code)),
        "bullet_line_count": len(BULLET_LINE_RE.findall(cn_no_code)),
    }


def add_issue(issues: List[Dict[str, str]], code: str, message: str) -> None:
    issues.append({"code": code, "message": message})


def analyze_markdown(
    path: Path,
    root: Path,
    min_cn_chars: int,
    min_non_usage_headings: int,
    min_bullet_lines: int,
) -> Dict[str, Any]:
    rel_path = normalize_rel_path(path, root)
    text = path.read_text(encoding="utf-8-sig", errors="ignore")

    issues: List[Dict[str, str]] = []
    cn_metrics: Dict[str, int] = {
        "cn_char_count": 0,
        "non_usage_heading_count": 0,
        "bullet_line_count": 0,
    }

    cn_index = text.find(CN_MARKER)
    en_index = text.find(EN_MARKER)

    if cn_index < 0:
        add_issue(issues, "missing_cn_marker", f"{rel_path}: missing `{CN_MARKER}`")
    if en_index < 0:
        add_issue(issues, "missing_en_marker", f"{rel_path}: missing `{EN_MARKER}`")

    if cn_index >= 0 and en_index >= 0:
        if en_index <= cn_index:
            add_issue(issues, "section_order_invalid", f"{rel_path}: English section appears before Chinese section")
        else:
            cn_section = text[cn_index:en_index]
            cn_metrics = collect_cn_metrics(cn_section)

            if GARBLED_HEADING_RE.search(cn_section):
                add_issue(issues, "garbled_cn_heading", f"{rel_path}: Chinese section contains garbled heading marker")

            if PLACEHOLDER_RE.search(cn_section):
                add_issue(issues, "placeholder_in_cn", f"{rel_path}: Chinese section contains unresolved template placeholder")

            is_substantive = (
                cn_metrics["cn_char_count"] >= min_cn_chars
                or cn_metrics["non_usage_heading_count"] >= min_non_usage_headings
                or cn_metrics["bullet_line_count"] >= min_bullet_lines
            )
            if not is_substantive:
                add_issue(
                    issues,
                    "thin_cn_summary",
                    (
                        f"{rel_path}: Chinese summary looks too thin "
                        f"(cn_chars={cn_metrics['cn_char_count']}, "
                        f"headings={cn_metrics['non_usage_heading_count']}, "
                        f"bullets={cn_metrics['bullet_line_count']})"
                    ),
                )

    return {
        "path": rel_path,
        "issue_count": len(issues),
        "issues": issues,
        "cn_metrics": cn_metrics,
    }


def build_summary(results: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    counter: Counter[str] = Counter()
    failed_files = 0
    passed_files = 0
    for result in results:
        if result["issues"]:
            failed_files += 1
            for issue in result["issues"]:
                counter[issue["code"]] += 1
        else:
            passed_files += 1

    return {
        "total_files": len(results),
        "passed_files": passed_files,
        "failed_files": failed_files,
        "issue_counts": dict(sorted(counter.items())),
    }


def print_summary(root: Path, exclude_globs: Sequence[str], summary: Dict[str, Any], results: Sequence[Dict[str, Any]]) -> None:
    log(f"[markdown-check] root: {root.resolve()}")
    log(f"[markdown-check] excludes: {', '.join(exclude_globs)}")
    log(f"[markdown-check] total files: {summary['total_files']}")
    log(f"[markdown-check] passed files: {summary['passed_files']}")
    log(f"[markdown-check] failed files: {summary['failed_files']}")

    if summary["issue_counts"]:
        log("[markdown-check] issue counts:")
        for code, count in summary["issue_counts"].items():
            log(f"  - {code}: {count}")
    else:
        log("[markdown-check] issue counts: none")

    failing_results = [result for result in results if result["issues"]]
    if failing_results:
        log("[markdown-check] failing files:")
        for result in failing_results:
            log(f"  - {result['path']}")
            for issue in result["issues"]:
                log(f"      * {issue['code']}: {issue['message']}")


def write_json_report(report_path: Path, payload: Dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check bilingual Markdown structure across the Warden repository."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Default: current working directory.",
    )
    parser.add_argument(
        "--exclude-glob",
        action="append",
        default=[],
        help="Additional glob pattern to exclude. Can be passed multiple times.",
    )
    parser.add_argument(
        "--min-cn-chars",
        type=int,
        default=80,
        help="Minimum Chinese character threshold used by the thin-summary heuristic.",
    )
    parser.add_argument(
        "--min-non-usage-headings",
        type=int,
        default=2,
        help="Minimum non-usage heading threshold used by the thin-summary heuristic.",
    )
    parser.add_argument(
        "--min-bullet-lines",
        type=int,
        default=6,
        help="Minimum bullet-line threshold used by the thin-summary heuristic.",
    )
    parser.add_argument(
        "--report-json",
        default="",
        help="Optional JSON report output path.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    exclude_globs = DEFAULT_EXCLUDE_GLOBS + list(args.exclude_glob)

    if not root.exists() or not root.is_dir():
        log(f"[markdown-check] root does not exist or is not a directory: {root}")
        return 2

    files = discover_markdown_files(root, exclude_globs)
    if not files:
        log(f"[markdown-check] no markdown files found under: {root}")
        return 2

    results = [
        analyze_markdown(
            path=path,
            root=root,
            min_cn_chars=args.min_cn_chars,
            min_non_usage_headings=args.min_non_usage_headings,
            min_bullet_lines=args.min_bullet_lines,
        )
        for path in files
    ]
    summary = build_summary(results)
    print_summary(root, exclude_globs, summary, results)

    payload = {
        "root": str(root),
        "exclude_globs": exclude_globs,
        "summary": summary,
        "results": results,
    }
    if args.report_json:
        write_json_report(Path(args.report_json), payload)
        log(f"[markdown-check] wrote JSON report: {Path(args.report_json).resolve()}")

    return 0 if summary["failed_files"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
