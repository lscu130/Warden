#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Read-only loader smoke for benign_clean_v1 manifests and sample artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


SPLIT_FILES = {
    "train": "benign_train_manifest_v1.csv",
    "val": "benign_val_manifest_v1.csv",
    "test": "benign_test_manifest_v1.csv",
}

REQUIRED_COLUMNS = {
    "sample_id",
    "triage_label",
    "current_path",
    "final_url",
    "final_host",
    "etld1",
    "group_key",
}

ISSUE_FIELDS = ["split", "triage_label", "sample_id", "current_path", "issue_type", "artifact", "details"]
JSON_ARTIFACTS = ("url.json", "forms.json", "net_summary.json")
SCREENSHOT_ARTIFACTS = ("screenshot_viewport.png", "screenshot_view.png", "screenshot_full.png")


@dataclass
class SmokeStats:
    rows_by_split: Counter
    labels_by_split: Dict[str, Counter]
    labels_by_split_label: Counter
    path_missing: Counter
    artifact_missing: Counter
    json_parse_failure: Counter
    text_buckets: Counter
    issue_totals: Counter
    issue_examples: List[Dict[str, str]]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(f"missing CSV header: {path}")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            raise SystemExit(f"missing required columns in {path}: {missing}")
        return list(reader)


def write_csv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def issue_key(split: str, label: str, issue_type: str, artifact: str) -> tuple[str, str, str, str]:
    return split, label, issue_type, artifact


def add_issue(
    stats: SmokeStats,
    per_issue_limit: int,
    row: Dict[str, str],
    issue_type: str,
    artifact: str,
    details: str,
) -> None:
    split = row["split"]
    label = row["triage_label"]
    key = issue_key(split, label, issue_type, artifact)
    stats.issue_totals[key] += 1
    if stats.issue_totals[key] <= per_issue_limit:
        stats.issue_examples.append(
            {
                "split": split,
                "triage_label": label,
                "sample_id": row["sample_id"],
                "current_path": row.get("current_path", ""),
                "issue_type": issue_type,
                "artifact": artifact,
                "details": details,
            }
        )


def visible_text_bucket(path: Path) -> tuple[str, int]:
    text_path = path / "visible_text.txt"
    if not text_path.exists() or not text_path.is_file():
        return "missing", 0
    try:
        text = text_path.read_text(encoding="utf-8-sig", errors="ignore")
    except Exception:
        return "missing", 0
    length = len(text)
    if length == 0:
        return "empty", length
    if length < 100:
        return "<100", length
    if length < 300:
        return "<300", length
    return ">=300", length


def json_parse_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            json.load(handle)
        return True
    except Exception:
        return False


def load_manifests(manifest_dir: Path) -> tuple[List[Dict[str, str]], Dict[str, List[Dict[str, str]]]]:
    all_rows: List[Dict[str, str]] = []
    by_split: Dict[str, List[Dict[str, str]]] = {}
    for split, filename in SPLIT_FILES.items():
        rows = read_csv(manifest_dir / filename)
        for row in rows:
            row["split"] = split
        by_split[split] = rows
        all_rows.extend(rows)
    return all_rows, by_split


def run_smoke(rows: Sequence[Dict[str, str]], max_examples: int) -> SmokeStats:
    stats = SmokeStats(Counter(), defaultdict(Counter), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), [])
    for row in rows:
        split = row["split"]
        label = row["triage_label"]
        stats.rows_by_split[split] += 1
        stats.labels_by_split[split][label] += 1
        stats.labels_by_split_label[(split, label)] += 1

        base = Path(row.get("current_path", ""))
        if not base.exists() or not base.is_dir():
            stats.path_missing[(split, label)] += 1
            add_issue(stats, max_examples, row, "missing_current_path", "current_path", "current_path does not exist")
            continue

        screenshot_found = any((base / name).exists() and (base / name).is_file() for name in SCREENSHOT_ARTIFACTS)
        if not screenshot_found:
            stats.artifact_missing[(split, label, "screenshot_any")] += 1
            add_issue(stats, max_examples, row, "missing_artifact", "screenshot_any", "no known screenshot artifact found")

        bucket, text_len = visible_text_bucket(base)
        stats.text_buckets[(split, label, bucket)] += 1
        if bucket == "missing":
            stats.artifact_missing[(split, label, "visible_text.txt")] += 1
            add_issue(stats, max_examples, row, "missing_artifact", "visible_text.txt", "visible_text.txt missing or unreadable")
        elif bucket == "empty":
            add_issue(stats, max_examples, row, "empty_visible_text", "visible_text.txt", "visible_text.txt has 0 characters")

        for artifact in JSON_ARTIFACTS:
            path = base / artifact
            if not path.exists() or not path.is_file():
                stats.artifact_missing[(split, label, artifact)] += 1
                add_issue(stats, max_examples, row, "missing_artifact", artifact, f"{artifact} missing")
                continue
            if not json_parse_ok(path):
                stats.json_parse_failure[(split, label, artifact)] += 1
                add_issue(stats, max_examples, row, "json_parse_failure", artifact, f"{artifact} failed JSON parse")

    return stats


def count_lines(counter: Counter, keys: Iterable[tuple]) -> List[str]:
    lines = ["| Split | Triage label | Artifact / bucket | Count |", "|---|---|---|---:|"]
    for key in sorted(keys):
        if len(key) == 3:
            split, label, name = key
            count = counter[key]
        else:
            split, label, name = key[0], key[1], ""
            count = counter[key]
        lines.append(f"| `{split}` | `{label}` | `{name}` | {count} |")
    return lines


def write_report(path: Path, manifest_dir: Path, output_dir: Path, stats: SmokeStats) -> None:
    total = sum(stats.rows_by_split.values())
    lines: List[str] = [
        "# Benign Clean V1 Loader Smoke Report",
        "",
        "## 中文摘要",
        "",
        "- 本报告只读检查 benign clean V1 的 train / validation / test manifest 和核心本地 artifacts。",
        f"- 总行数：{total}。",
        "- `triage_label` 仅可作为 supervision / dataset-management 字段，禁止进入模型输入 evidence pack。",
        "- 本 smoke 不训练模型，不运行 teacher，不修改样本、标签或现有 manifest。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Manifest directory: `{manifest_dir}`",
        f"- Output directory: `{output_dir}`",
        f"- Rows checked: `{total}`",
        "- The check is read-only and did not modify source samples, labels, or existing split manifests.",
        "- `triage_label`, human folder names, and split names must remain outside future model input evidence packs.",
        "- Conclusion: the split is usable for preliminary loader / training-pipeline smoke if the listed artifact gaps are accepted.",
        "",
        "## 2. Split And Label Distribution",
        "",
        "| Split | Rows | T00_clear_benign | T01_benign_hard_negative |",
        "|---|---:|---:|---:|",
    ]
    for split in ("train", "val", "test"):
        labels = stats.labels_by_split[split]
        lines.append(
            f"| `{split}` | {stats.rows_by_split[split]} | {labels['T00_clear_benign']} | {labels['T01_benign_hard_negative']} |"
        )

    lines.extend(["", "## 3. Missing Artifacts", ""])
    if stats.artifact_missing:
        lines.extend(count_lines(stats.artifact_missing, stats.artifact_missing.keys()))
    else:
        lines.append("- No missing core artifacts found.")

    lines.extend(["", "## 4. JSON Parse Failures", ""])
    if stats.json_parse_failure:
        lines.extend(count_lines(stats.json_parse_failure, stats.json_parse_failure.keys()))
    else:
        lines.append("- No JSON parse failures found for checked JSON artifacts.")

    lines.extend(["", "## 5. Visible Text Length Buckets", ""])
    lines.extend(count_lines(stats.text_buckets, stats.text_buckets.keys()))

    lines.extend(
        [
            "",
            "## 6. Loader Evidence-Pack Boundary",
            "",
            "- Allowed model input evidence should come from page artifacts such as URL, rendered text/DOM, screenshots, forms, and network summaries.",
            "- `triage_label` is supervision / dataset-management metadata and must not be included in the model input evidence pack.",
            "- Human folder names and split names are also dataset-management metadata, not model evidence.",
            "",
            "## 7. Caveats",
            "",
            "- This smoke validates local loader readiness, not model quality.",
            "- Missing artifacts should be reviewed before full training, but they do not imply relabeling.",
            "- This task did not run screenshot hashing or visual duplicate checks.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-check benign clean V1 manifest loader readiness.")
    parser.add_argument("--manifest-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--output-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--max-examples-per-issue", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest_dir = Path(args.manifest_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, _ = load_manifests(manifest_dir)
    stats = run_smoke(rows, args.max_examples_per_issue)

    summary_csv = output_dir / "benign_loader_smoke_artifact_summary_v1.csv"
    report = output_dir / "benign_loader_smoke_report_v1.md"
    write_csv(summary_csv, stats.issue_examples, ISSUE_FIELDS)
    write_report(report, manifest_dir, output_dir, stats)

    print(f"MANIFEST_DIR={manifest_dir}")
    print(f"OUTPUT_DIR={output_dir}")
    print(f"ROWS={sum(stats.rows_by_split.values())}")
    for split in ("train", "val", "test"):
        labels = stats.labels_by_split[split]
        print(f"SPLIT_{split.upper()} rows={stats.rows_by_split[split]} T00={labels['T00_clear_benign']} T01={labels['T01_benign_hard_negative']}")
    print(f"ISSUE_EXAMPLES={len(stats.issue_examples)}")
    print(f"MISSING_ARTIFACT_TOTAL={sum(stats.artifact_missing.values())}")
    print(f"JSON_PARSE_FAILURE_TOTAL={sum(stats.json_parse_failure.values())}")
    print(f"OUTPUT_CSV={summary_csv}")
    print(f"OUTPUT_REPORT={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
