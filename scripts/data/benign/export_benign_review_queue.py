#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Export a read-only benign review queue from existing smoke/review artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


SPLIT_FILES = {
    "train": "benign_train_manifest_v1.csv",
    "val": "benign_val_manifest_v1.csv",
    "test": "benign_test_manifest_v1.csv",
}

LIGHTWEIGHT_ARTIFACTS = (
    "screenshot_viewport.png",
    "screenshot_view.png",
    "screenshot_full.png",
    "visible_text.txt",
    "url.json",
    "forms.json",
    "net_summary.json",
)

BUCKET_DIRS = {
    "missing_visible_text": "R01_missing_visible_text",
    "visible_text_exact": "R02_visible_text_exact",
    "dom_exact": "R03_dom_exact",
    "visible_text_simhash_candidate": "R04_visible_text_simhash",
    "dom_simhash_candidate": "R05_dom_simhash",
    "unresolved": "R99_unresolved_or_manifest_only",
}

MANIFEST_FIELDS = [
    "review_id",
    "review_bucket",
    "candidate_type",
    "candidate_rank",
    "split",
    "triage_label",
    "sample_id",
    "source_path",
    "review_path",
    "copy_status",
    "missing_files",
    "source_row_id",
    "details",
    "recommendation",
]

MISSING_FIELDS = [
    "review_id",
    "split",
    "triage_label",
    "sample_id",
    "source_path",
    "review_path",
    "visible_text_status",
    "has_screenshot",
    "has_url_json",
    "has_forms_json",
    "has_net_summary_json",
    "recommendation",
]

DUP_FIELDS = [
    "candidate_id",
    "candidate_type",
    "severity_or_score",
    "split_a",
    "split_b",
    "sample_id_a",
    "sample_id_b",
    "source_path_a",
    "source_path_b",
    "review_path_a",
    "review_path_b",
    "copy_status",
    "details",
    "recommendation",
]


@dataclass
class CopyResult:
    status: str
    missing_files: List[str]
    copied_files: int


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_name(value: str, max_len: int = 120) -> str:
    safe = re.sub(r"[^A-Za-z0-9._=-]+", "_", value.strip())
    safe = safe.strip("._")
    return (safe or "unknown")[:max_len]


def ensure_bucket_dirs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for dirname in BUCKET_DIRS.values():
        (output_dir / dirname).mkdir(parents=True, exist_ok=True)


def load_manifest_index(manifest_dir: Path) -> Tuple[Dict[str, Dict[str, str]], Dict[str, str]]:
    index: Dict[str, Dict[str, str]] = {}
    hashes: Dict[str, str] = {}
    for split, filename in SPLIT_FILES.items():
        path = manifest_dir / filename
        if not path.exists():
            raise SystemExit(f"missing required split manifest: {path}")
        hashes[str(path)] = sha256_file(path)
        for row in read_csv(path):
            row["split"] = split
            index[row.get("sample_id", "")] = row
    return index, hashes


def copy_review_artifacts(source_dir: Path, target_dir: Path, copy_mode: str) -> CopyResult:
    target_dir.mkdir(parents=True, exist_ok=True)
    if copy_mode == "manifest-only":
        return CopyResult("manifest_only", [], 0)
    if not source_dir.exists() or not source_dir.is_dir():
        return CopyResult("manifest_only", ["source_path"], 0)

    missing: List[str] = []
    copied = 0
    if copy_mode == "full":
        for item in source_dir.iterdir():
            dest = target_dir / item.name
            try:
                if item.is_file():
                    shutil.copy2(item, dest)
                    copied += 1
            except Exception:
                missing.append(item.name)
        return CopyResult("copied" if copied else "manifest_only", missing, copied)

    for name in LIGHTWEIGHT_ARTIFACTS:
        src = source_dir / name
        if not src.exists() or not src.is_file():
            missing.append(name)
            continue
        try:
            shutil.copy2(src, target_dir / name)
            copied += 1
        except Exception:
            missing.append(name)
    return CopyResult("copied" if copied else "manifest_only", missing, copied)


def artifact_bool(source_dir: Path, name: str) -> str:
    return "true" if (source_dir / name).exists() and (source_dir / name).is_file() else "false"


def has_any_screenshot(source_dir: Path) -> str:
    return "true" if any((source_dir / name).exists() and (source_dir / name).is_file() for name in LIGHTWEIGHT_ARTIFACTS[:3]) else "false"


def bucket_for_candidate(candidate_type: str) -> str:
    if candidate_type == "visible_text_exact":
        return BUCKET_DIRS["visible_text_exact"]
    if candidate_type == "dom_exact":
        return BUCKET_DIRS["dom_exact"]
    if candidate_type == "visible_text_simhash_candidate":
        return BUCKET_DIRS["visible_text_simhash_candidate"]
    if candidate_type == "dom_simhash_candidate":
        return BUCKET_DIRS["dom_simhash_candidate"]
    return BUCKET_DIRS["unresolved"]


def export_missing_visible_text(
    smoke_rows: Sequence[Dict[str, str]],
    output_dir: Path,
    copy_mode: str,
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], Counter]:
    queue_rows: List[Dict[str, str]] = []
    missing_rows: List[Dict[str, str]] = []
    counts: Counter = Counter()
    bucket = BUCKET_DIRS["missing_visible_text"]
    rank = 0
    for idx, row in enumerate(smoke_rows, start=1):
        if row.get("artifact") != "visible_text.txt":
            continue
        details = (row.get("details") or "").lower()
        if "missing" not in details and "unreadable" not in details and row.get("issue_type") != "missing_artifact":
            continue
        rank += 1
        review_id = f"R01_{rank:06d}"
        source_dir = Path(row.get("current_path", ""))
        item_dir = output_dir / bucket / f"{review_id}_{sanitize_name(row.get('sample_id', ''))}"
        result = copy_review_artifacts(source_dir, item_dir, copy_mode)
        counts[bucket] += 1
        counts[f"copy_status:{result.status}"] += 1
        for missing in result.missing_files:
            counts[f"missing_file:{missing}"] += 1
        queue_rows.append(
            {
                "review_id": review_id,
                "review_bucket": bucket,
                "candidate_type": "missing_visible_text",
                "candidate_rank": str(rank),
                "split": row.get("split", ""),
                "triage_label": row.get("triage_label", ""),
                "sample_id": row.get("sample_id", ""),
                "source_path": row.get("current_path", ""),
                "review_path": str(item_dir),
                "copy_status": result.status,
                "missing_files": ";".join(result.missing_files),
                "source_row_id": str(idx),
                "details": row.get("details", ""),
                "recommendation": "manual_decision_accept_repair_recrawl_or_exclude_from_text_tower",
            }
        )
        missing_rows.append(
            {
                "review_id": review_id,
                "split": row.get("split", ""),
                "triage_label": row.get("triage_label", ""),
                "sample_id": row.get("sample_id", ""),
                "source_path": row.get("current_path", ""),
                "review_path": str(item_dir),
                "visible_text_status": "missing_or_unreadable",
                "has_screenshot": has_any_screenshot(source_dir),
                "has_url_json": artifact_bool(source_dir, "url.json"),
                "has_forms_json": artifact_bool(source_dir, "forms.json"),
                "has_net_summary_json": artifact_bool(source_dir, "net_summary.json"),
                "recommendation": "review_before_repair_or_text_training_exclusion",
            }
        )
    return queue_rows, missing_rows, counts


def export_duplicate_candidates(
    candidate_rows: Sequence[Dict[str, str]],
    output_dir: Path,
    copy_mode: str,
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], Counter]:
    queue_rows: List[Dict[str, str]] = []
    duplicate_rows: List[Dict[str, str]] = []
    counts: Counter = Counter()
    for idx, row in enumerate(candidate_rows, start=1):
        candidate_type = row.get("candidate_type", "") or "unknown"
        bucket = bucket_for_candidate(candidate_type)
        candidate_id = f"CAND_{idx:06d}"
        candidate_dir = output_dir / bucket / f"candidate_{idx:06d}"
        source_a = Path(row.get("current_path_a", ""))
        source_b = Path(row.get("current_path_b", ""))
        target_a = candidate_dir / f"A_{sanitize_name(row.get('sample_id_a', ''))}"
        target_b = candidate_dir / f"B_{sanitize_name(row.get('sample_id_b', ''))}"
        result_a = copy_review_artifacts(source_a, target_a, copy_mode)
        result_b = copy_review_artifacts(source_b, target_b, copy_mode)
        combined_missing = sorted(set(result_a.missing_files + result_b.missing_files))
        if result_a.status == "copied" and result_b.status == "copied":
            status = "copied"
        elif result_a.status == "manifest_only" and result_b.status == "manifest_only":
            status = "manifest_only"
        else:
            status = "partial"
        counts[bucket] += 1
        counts[f"copy_status:{status}"] += 1
        for missing in combined_missing:
            counts[f"missing_file:{missing}"] += 1

        meta = {
            "candidate_id": candidate_id,
            "candidate_type": candidate_type,
            "source_row_id": idx,
            "source_a": str(source_a),
            "source_b": str(source_b),
            "sample_id_a": row.get("sample_id_a", ""),
            "sample_id_b": row.get("sample_id_b", ""),
            "similarity_or_distance": row.get("similarity_or_distance", ""),
            "review_hint": row.get("review_hint", ""),
            "note": "candidate is a review hint, not confirmed leakage",
        }
        candidate_dir.mkdir(parents=True, exist_ok=True)
        (candidate_dir / "candidate_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        duplicate_rows.append(
            {
                "candidate_id": candidate_id,
                "candidate_type": candidate_type,
                "severity_or_score": row.get("severity", ""),
                "split_a": row.get("split_a", ""),
                "split_b": row.get("split_b", ""),
                "sample_id_a": row.get("sample_id_a", ""),
                "sample_id_b": row.get("sample_id_b", ""),
                "source_path_a": row.get("current_path_a", ""),
                "source_path_b": row.get("current_path_b", ""),
                "review_path_a": str(target_a),
                "review_path_b": str(target_b),
                "copy_status": status,
                "details": f"{row.get('similarity_or_distance', '')}; hint={row.get('review_hint', '')}",
                "recommendation": "manual_review_candidate_pair_before_benchmark_claims",
            }
        )
        for side, sample_key, split_key, label_key, source_path, review_path, result in (
            ("A", "sample_id_a", "split_a", "triage_label_a", row.get("current_path_a", ""), str(target_a), result_a),
            ("B", "sample_id_b", "split_b", "triage_label_b", row.get("current_path_b", ""), str(target_b), result_b),
        ):
            queue_rows.append(
                {
                    "review_id": f"{candidate_id}_{side}",
                    "review_bucket": bucket,
                    "candidate_type": candidate_type,
                    "candidate_rank": str(idx),
                    "split": row.get(split_key, ""),
                    "triage_label": row.get(label_key, ""),
                    "sample_id": row.get(sample_key, ""),
                    "source_path": source_path,
                    "review_path": review_path,
                    "copy_status": result.status,
                    "missing_files": ";".join(result.missing_files),
                    "source_row_id": str(idx),
                    "details": f"{row.get('similarity_or_distance', '')}; hint={row.get('review_hint', '')}",
                    "recommendation": "manual_review_candidate_pair_before_benchmark_claims",
                }
            )
    return queue_rows, duplicate_rows, counts


def write_report(
    path: Path,
    manifest_dir: Path,
    output_dir: Path,
    copy_mode: str,
    input_files: Sequence[Path],
    missing_count: int,
    candidate_count: int,
    queue_count: int,
    bucket_counts: Counter,
    before_hashes: Dict[str, str],
    after_hashes: Dict[str, str],
) -> None:
    unresolved = bucket_counts.get(BUCKET_DIRS["unresolved"], 0) + bucket_counts.get("copy_status:manifest_only", 0)
    missing_file_total = sum(count for key, count in bucket_counts.items() if str(key).startswith("missing_file:"))
    lines: List[str] = [
        "# Benign Review Queue Export V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告记录 `benign_clean_v1` 人工复核队列导出结果。",
        f"- 输出目录：`{output_dir}`",
        f"- copy mode：`{copy_mode}`",
        f"- missing visible text items：{missing_count}",
        f"- duplicate/template candidates：{candidate_count}",
        "- 这是复核副本导出，不移动、不删除、不重命名、不改标签、不改 split manifest。",
        "- duplicate/template candidates 不是 confirmed leakage。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Run timestamp UTC: `{now_utc_iso()}`",
        f"- Manifest directory: `{manifest_dir}`",
        f"- Output root: `{output_dir}`",
        f"- Copy mode used: `{copy_mode}`",
        f"- Missing-visible-text items exported: `{missing_count}`",
        f"- Duplicate/template candidates processed: `{candidate_count}`",
        f"- Review queue manifest rows: `{queue_count}`",
        f"- Unresolved or manifest-only count: `{unresolved}`",
        f"- Missing files observed during copying: `{missing_file_total}`",
        "- Original samples and existing manifests were not modified by this exporter.",
        "- Review candidates are not confirmed leakage and must not be treated as labels.",
        "",
        "## 2. Input Files Checked",
        "",
    ]
    for item in input_files:
        lines.append(f"- `{item}`")
    lines.extend(["", "## 3. Review Bucket Counts", "", "| Bucket | Count |", "|---|---:|"])
    for bucket in (
        "R01_missing_visible_text",
        "R02_visible_text_exact",
        "R03_dom_exact",
        "R04_visible_text_simhash",
        "R05_dom_simhash",
        "R99_unresolved_or_manifest_only",
    ):
        lines.append(f"| `{bucket}` | {bucket_counts.get(bucket, 0)} |")

    lines.extend(["", "## 4. Copy Status Counts", "", "| Status | Count |", "|---|---:|"])
    for key, count in sorted(bucket_counts.items()):
        if str(key).startswith("copy_status:"):
            lines.append(f"| `{str(key).split(':', 1)[1]}` | {count} |")

    lines.extend(["", "## 5. Missing Files During Copy", "", "| File | Count |", "|---|---:|"])
    missing_keys = [key for key in bucket_counts if str(key).startswith("missing_file:")]
    if missing_keys:
        for key in sorted(missing_keys):
            lines.append(f"| `{str(key).split(':', 1)[1]}` | {bucket_counts[key]} |")
    else:
        lines.append("| none | 0 |")

    hashes_unchanged = before_hashes == after_hashes
    lines.extend(
        [
            "",
            "## 6. Source Manifest Hash Check",
            "",
            f"- Source split manifest hashes unchanged after export: `{str(hashes_unchanged).lower()}`",
            "",
            "| Manifest | Before SHA256 | After SHA256 |",
            "|---|---|---|",
        ]
    )
    for key in sorted(before_hashes):
        lines.append(f"| `{key}` | `{before_hashes[key]}` | `{after_hashes.get(key, '')}` |")

    lines.extend(
        [
            "",
            "## 7. Manual Review Order",
            "",
            "1. `R01_missing_visible_text`",
            "2. `R02_visible_text_exact`",
            "3. `R03_dom_exact`",
            "4. top-ranked `R04_visible_text_simhash`",
            "5. top-ranked `R05_dom_simhash`",
            "",
            "## 8. Caveats",
            "",
            "- Exported files are review copies only.",
            "- Missing files in review copies are recorded and do not imply source mutation.",
            "- No OCR, YOLO, CLIP, MobileCLIP, SpecularNet, teacher, training, or external lookup was run.",
            "- This export does not make benchmark-readiness claims.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_copy_mode(value: str) -> str:
    allowed = {"minimal", "full", "manifest-only"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(f"copy mode must be one of {sorted(allowed)}")
    return value


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export benign clean V1 manual review queue.")
    parser.add_argument("--manifest-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--output-dir", default=r"E:\WardenData\manifests\benign_clean_v1_review_queue")
    parser.add_argument("--copy-mode", type=validate_copy_mode, default="minimal")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest_dir = Path(args.manifest_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    ensure_bucket_dirs(output_dir)

    smoke_path = manifest_dir / "benign_loader_smoke_artifact_summary_v1.csv"
    candidates_path = manifest_dir / "benign_duplicate_template_review_candidates_v1.csv"
    if not smoke_path.exists():
        raise SystemExit(f"missing loader smoke CSV: {smoke_path}")
    if not candidates_path.exists():
        raise SystemExit(f"missing duplicate candidate CSV: {candidates_path}")

    _manifest_index, before_hashes = load_manifest_index(manifest_dir)
    smoke_rows = read_csv(smoke_path)
    candidate_rows = read_csv(candidates_path)

    queue_missing, missing_review, missing_counts = export_missing_visible_text(smoke_rows, output_dir, args.copy_mode)
    queue_duplicate, duplicate_review, duplicate_counts = export_duplicate_candidates(candidate_rows, output_dir, args.copy_mode)
    queue_rows = queue_missing + queue_duplicate
    bucket_counts = missing_counts + duplicate_counts
    _manifest_index_after, after_hashes = load_manifest_index(manifest_dir)

    review_manifest = output_dir / "review_queue_manifest_v1.csv"
    missing_manifest = output_dir / "missing_visible_text_review_v1.csv"
    duplicate_manifest = output_dir / "duplicate_template_review_v1.csv"
    report = output_dir / "benign_review_queue_export_report_v1.md"
    write_csv(review_manifest, queue_rows, MANIFEST_FIELDS)
    write_csv(missing_manifest, missing_review, MISSING_FIELDS)
    write_csv(duplicate_manifest, duplicate_review, DUP_FIELDS)
    write_report(
        report,
        manifest_dir,
        output_dir,
        args.copy_mode,
        [smoke_path, candidates_path, *(manifest_dir / filename for filename in SPLIT_FILES.values())],
        len(missing_review),
        len(duplicate_review),
        len(queue_rows),
        bucket_counts,
        before_hashes,
        after_hashes,
    )

    print(f"MANIFEST_DIR={manifest_dir}")
    print(f"OUTPUT_DIR={output_dir}")
    print(f"COPY_MODE={args.copy_mode}")
    print(f"MISSING_VISIBLE_TEXT_EXPORTED={len(missing_review)}")
    print(f"DUPLICATE_TEMPLATE_CANDIDATES_PROCESSED={len(duplicate_review)}")
    print(f"REVIEW_QUEUE_ROWS={len(queue_rows)}")
    for bucket in (
        "R01_missing_visible_text",
        "R02_visible_text_exact",
        "R03_dom_exact",
        "R04_visible_text_simhash",
        "R05_dom_simhash",
        "R99_unresolved_or_manifest_only",
    ):
        print(f"BUCKET_{bucket}={bucket_counts.get(bucket, 0)}")
    print(f"SOURCE_MANIFEST_HASHES_UNCHANGED={before_hashes == after_hashes}")
    print(f"OUTPUT_REVIEW_MANIFEST={review_manifest}")
    print(f"OUTPUT_MISSING_MANIFEST={missing_manifest}")
    print(f"OUTPUT_DUPLICATE_MANIFEST={duplicate_manifest}")
    print(f"OUTPUT_REPORT={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
