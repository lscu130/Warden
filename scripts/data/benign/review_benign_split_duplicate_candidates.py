#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build bounded human-review candidates from benign split leakage audit rows."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence


SPLIT_FILES = {
    "train": "benign_train_manifest_v1.csv",
    "val": "benign_val_manifest_v1.csv",
    "test": "benign_test_manifest_v1.csv",
}

CANDIDATE_FIELDS = [
    "candidate_type",
    "severity",
    "split_a",
    "split_b",
    "sample_id_a",
    "sample_id_b",
    "triage_label_a",
    "triage_label_b",
    "current_path_a",
    "current_path_b",
    "final_url_a",
    "final_url_b",
    "final_host_a",
    "final_host_b",
    "etld1_a",
    "etld1_b",
    "group_key_a",
    "group_key_b",
    "similarity_or_distance",
    "shared_key_or_band",
    "visible_text_chars_a",
    "visible_text_chars_b",
    "dom_nodes_or_tags_a",
    "dom_nodes_or_tags_b",
    "review_hint",
    "recommended_human_action",
]

TYPE_MAP = {
    "visible_text_exact_hash": "visible_text_exact",
    "visible_text_near_duplicate": "visible_text_simhash_candidate",
    "html_dom_exact_hash": "dom_exact",
    "html_dom_structure_near_duplicate": "dom_simhash_candidate",
}


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def load_manifest_index(manifest_dir: Path) -> Dict[str, Dict[str, str]]:
    index: Dict[str, Dict[str, str]] = {}
    for split, filename in SPLIT_FILES.items():
        for row in read_csv(manifest_dir / filename):
            row["split"] = split
            index[row["sample_id"]] = row
    return index


def review_hint(candidate_type: str, left: Dict[str, str], right: Dict[str, str], distance_or_key: str) -> str:
    if left.get("final_url") and left.get("final_url") == right.get("final_url"):
        return "strict_duplicate_possible"
    if left.get("final_host") and left.get("final_host") == right.get("final_host"):
        return "same_site_or_same_host_variant"
    chars_a = int(left.get("visible_text_chars") or 0)
    chars_b = int(right.get("visible_text_chars") or 0)
    if chars_a < 100 or chars_b < 100:
        return "too_sparse_to_judge"
    if candidate_type in {"dom_exact", "dom_simhash_candidate"}:
        return "template_overlap_possible"
    if candidate_type == "visible_text_exact":
        return "boilerplate_or_footer_possible"
    if "hamming_distance=0" in distance_or_key:
        return "public_template_possible"
    return "needs_manual_review"


def build_candidate(
    audit_row: Dict[str, str],
    candidate_type: str,
    left: Dict[str, str],
    right: Dict[str, str],
) -> Dict[str, str]:
    distance_or_key = audit_row.get("key_value", "")
    hint = review_hint(candidate_type, left, right, distance_or_key)
    return {
        "candidate_type": candidate_type,
        "severity": audit_row.get("severity", "warning") or "warning",
        "split_a": audit_row.get("split_a", left.get("split", "")),
        "split_b": audit_row.get("split_b", right.get("split", "")),
        "sample_id_a": left.get("sample_id", ""),
        "sample_id_b": right.get("sample_id", ""),
        "triage_label_a": left.get("triage_label", ""),
        "triage_label_b": right.get("triage_label", ""),
        "current_path_a": left.get("current_path", ""),
        "current_path_b": right.get("current_path", ""),
        "final_url_a": left.get("final_url", ""),
        "final_url_b": right.get("final_url", ""),
        "final_host_a": left.get("final_host", ""),
        "final_host_b": right.get("final_host", ""),
        "etld1_a": left.get("etld1", ""),
        "etld1_b": right.get("etld1", ""),
        "group_key_a": left.get("group_key", ""),
        "group_key_b": right.get("group_key", ""),
        "similarity_or_distance": distance_or_key,
        "shared_key_or_band": audit_row.get("key_value", ""),
        "visible_text_chars_a": left.get("visible_text_chars", ""),
        "visible_text_chars_b": right.get("visible_text_chars", ""),
        "dom_nodes_or_tags_a": "",
        "dom_nodes_or_tags_b": "",
        "review_hint": hint,
        "recommended_human_action": "review_pair_before_benchmark_claims",
    }


def allowed_for_limit(candidate_type: str, counts: Counter, args: argparse.Namespace) -> bool:
    if sum(counts.values()) >= args.max_total_pairs:
        return False
    if candidate_type in {"visible_text_exact", "dom_exact"}:
        return counts[candidate_type] < args.max_exact_per_type
    return counts[candidate_type] < args.max_simhash_per_type


def build_candidates(manifest_dir: Path, args: argparse.Namespace) -> tuple[List[Dict[str, str]], Counter, Counter, int]:
    audit_path = manifest_dir / "benign_split_leakage_audit_v1.csv"
    if not audit_path.exists():
        raise SystemExit(f"missing audit CSV: {audit_path}")

    index = load_manifest_index(manifest_dir)
    audit_rows = read_csv(audit_path)
    audit_finding_counts = Counter()
    output_counts = Counter()
    missing_pairs = 0
    candidates: List[Dict[str, str]] = []

    for row in audit_rows:
        audit_type = row.get("audit_type", "")
        candidate_type = TYPE_MAP.get(audit_type)
        if not candidate_type or row.get("status") != "finding":
            continue
        audit_finding_counts[candidate_type] += 1
        if not allowed_for_limit(candidate_type, output_counts, args):
            continue
        sid_a = row.get("example_sample_a", "")
        sid_b = row.get("example_sample_b", "")
        left = index.get(sid_a)
        right = index.get(sid_b)
        if not left or not right:
            missing_pairs += 1
            continue
        candidates.append(build_candidate(row, candidate_type, left, right))
        output_counts[candidate_type] += 1

    return candidates, audit_finding_counts, output_counts, missing_pairs


def write_report(
    path: Path,
    manifest_dir: Path,
    output_dir: Path,
    candidates: Sequence[Dict[str, str]],
    audit_counts: Counter,
    output_counts: Counter,
    missing_pairs: int,
) -> None:
    lines: List[str] = [
        "# Benign Duplicate / Template Candidate Review V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告把上一轮 split leakage audit 的 visible-text / DOM 候选整理成人工复核队列。",
        "- 这些候选是 near-duplicate / template review candidates，不是 confirmed leakage。",
        "- screenshot hash 未运行，因此不能声明视觉重复风险已排除。",
        "- 当前 split 可用于 preliminary training / loader smoke，但不能单独支撑 final benchmark leakage-free claim。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Manifest directory: `{manifest_dir}`",
        f"- Output directory: `{output_dir}`",
        "- Audit source: `benign_split_leakage_audit_v1.csv`",
        f"- Output candidates: `{len(candidates)}`",
        f"- Missing manifest pairs while resolving audit rows: `{missing_pairs}`",
        "- Candidate rows are hints for human review only and do not modify labels or split membership.",
        "",
        "## 2. Candidate Counts",
        "",
        "| Candidate type | Audit finding rows | Output rows |",
        "|---|---:|---:|",
    ]
    for candidate_type in ("visible_text_exact", "visible_text_simhash_candidate", "dom_exact", "dom_simhash_candidate"):
        lines.append(f"| `{candidate_type}` | {audit_counts[candidate_type]} | {output_counts[candidate_type]} |")

    lines.extend(
        [
            "",
            "## 3. Top Examples",
            "",
            "| Candidate type | Split A | Split B | Sample A | Sample B | Hint |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in list(candidates)[:20]:
        lines.append(
            f"| `{row['candidate_type']}` | `{row['split_a']}` | `{row['split_b']}` | `{row['sample_id_a']}` | `{row['sample_id_b']}` | `{row['review_hint']}` |"
        )

    lines.extend(
        [
            "",
            "## 4. Counter-Review Classification",
            "",
            "- Strict leakage means same sample, same URL, same host, or same group key across split. Previous manifest-level audit reported these as `0`.",
            "- Near-duplicate contamination means high text, DOM, or screenshot similarity across split. This report covers text/DOM candidates only.",
            "- Natural template reuse includes public templates, CMS layouts, shared boilerplate, and repeated footer/header patterns.",
            "- Template reuse is part of real web distribution; whether to isolate it depends on the evaluation goal.",
            "",
            "## 5. Usage Recommendation",
            "",
            "- Current benign split is suitable for preliminary training and loader/pipeline smoke.",
            "- Current benign split must not be the only evidence for final benchmark leakage-free claims.",
            "- Review material visible-text and DOM candidates before benchmark claims or publishable evaluation.",
            "- Screenshot-level duplicate risk remains unknown because screenshot hashing was not run.",
            "",
            "## 6. Follow-Up Options",
            "",
            "- Manual review of candidate pairs in the generated CSV.",
            "- Stronger cluster-based re-splitting if template candidates are material.",
            "- Separate screenshot perceptual-hash audit if visual duplicate exclusion is required.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build benign duplicate/template review candidates.")
    parser.add_argument("--manifest-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--output-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--max-exact-per-type", type=int, default=300)
    parser.add_argument("--max-simhash-per-type", type=int, default=300)
    parser.add_argument("--max-total-pairs", type=int, default=1000)
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest_dir = Path(args.manifest_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    candidates, audit_counts, output_counts, missing_pairs = build_candidates(manifest_dir, args)
    candidates_csv = output_dir / "benign_duplicate_template_review_candidates_v1.csv"
    report = output_dir / "benign_duplicate_template_review_report_v1.md"
    write_csv(candidates_csv, candidates, CANDIDATE_FIELDS)
    write_report(report, manifest_dir, output_dir, candidates, audit_counts, output_counts, missing_pairs)

    print(f"MANIFEST_DIR={manifest_dir}")
    print(f"OUTPUT_DIR={output_dir}")
    print(f"CANDIDATES={len(candidates)}")
    for candidate_type in ("visible_text_exact", "visible_text_simhash_candidate", "dom_exact", "dom_simhash_candidate"):
        print(f"{candidate_type.upper()} audit_rows={audit_counts[candidate_type]} output_rows={output_counts[candidate_type]}")
    print(f"MISSING_MANIFEST_PAIRS={missing_pairs}")
    print("SCREENSHOT_DUPLICATE_STATUS=NOT_RUN")
    print(f"OUTPUT_CSV={candidates_csv}")
    print(f"OUTPUT_REPORT={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
