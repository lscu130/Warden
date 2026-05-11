#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build the Warden Tranco benign clean-pool manifest and group-based split.

This script reads the already triaged T00/T01 benign directories, checks
minimum artifact completeness, writes clean/excluded CSV manifests, performs a
deterministic group-based train/val/test split, and writes a bilingual report.

It is read-only with respect to sample directories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse


TRIAGE_LABELS = {
    "T00_clear_benign": "normal_benign",
    "T01_benign_hard_negative": "hard_negative_benign",
}

SCREENSHOT_CANDIDATES = (
    "screenshot_viewport.png",
    "screenshot_view.png",
    "screenshot_full.png",
)

CSV_FIELDS = [
    "sample_id",
    "triage_label",
    "benign_weight_group",
    "usable_for_training",
    "current_path",
    "final_url",
    "final_host",
    "etld1",
    "group_key",
    "has_screenshot_viewport",
    "has_screenshot_view",
    "has_screenshot_full",
    "primary_screenshot_path",
    "has_visible_text",
    "visible_text_chars",
    "has_url_json",
    "has_forms_json",
    "form_count",
    "input_count",
    "has_password",
    "has_net_summary",
    "has_redirect_chain",
    "artifact_status",
    "exclude_reason",
    "notes",
]

EXCLUDED_EXTRA_FIELDS = [
    "missing_artifacts",
]

SPLIT_EXTRA_FIELDS = [
    "split",
    "split_seed",
    "split_method",
]

COMMON_SECOND_LEVEL_SUFFIXES = {
    "ac",
    "co",
    "com",
    "edu",
    "gov",
    "net",
    "org",
}


@dataclass(frozen=True)
class SplitTargets:
    train: int
    val: int
    test: int


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Optional[Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception:
        return None


def safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def bool_csv(value: bool) -> str:
    return "true" if value else "false"


def url_host(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").strip(".").lower()
    return host


def etld1_from_host(host: str) -> str:
    host = host.strip(".").lower()
    if not host:
        return ""
    parts = [part for part in host.split(".") if part]
    if len(parts) <= 2:
        return host
    if len(parts[-1]) == 2 and parts[-2] in COMMON_SECOND_LEVEL_SUFFIXES:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def dirname_url_fallback(sample_dir: Path) -> str:
    name = sample_dir.name
    if "_" in name:
        url_key = name.rsplit("_", 1)[0]
    else:
        url_key = name
    if "." not in url_key:
        return ""
    return "https://" + url_key.replace("\\", "/").strip("/") + "/"


def first_string(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def recover_final_url(sample_dir: Path, url_obj: Any, meta_obj: Any, redirect_obj: Any) -> tuple[str, str]:
    url_dict = url_obj if isinstance(url_obj, dict) else {}
    meta_dict = meta_obj if isinstance(meta_obj, dict) else {}

    final_url = first_string(
        url_dict.get("final_url"),
        url_dict.get("url"),
        url_dict.get("input_url"),
        meta_dict.get("final_url"),
        meta_dict.get("url"),
        meta_dict.get("input_url"),
    )
    if final_url:
        return final_url, "url_or_meta_json"

    redirect_chain = url_dict.get("redirect_chain")
    if isinstance(redirect_chain, list) and redirect_chain:
        candidate = first_string(redirect_chain[-1])
        if candidate:
            return candidate, "url_json_redirect_chain"

    if isinstance(redirect_obj, list) and redirect_obj:
        candidate = first_string(redirect_obj[-1])
        if candidate:
            return candidate, "redirect_chain_json"
    if isinstance(redirect_obj, dict):
        for key in ("final_url", "url", "location"):
            candidate = first_string(redirect_obj.get(key))
            if candidate:
                return candidate, "redirect_chain_json"

    fallback = dirname_url_fallback(sample_dir)
    if fallback:
        return fallback, "dirname_fallback"
    return "", ""


def count_forms(forms_obj: Any) -> tuple[int, int, bool]:
    forms: List[Any] = []
    if isinstance(forms_obj, dict) and isinstance(forms_obj.get("forms"), list):
        forms = forms_obj["forms"]
    elif isinstance(forms_obj, list):
        forms = forms_obj

    form_count = len(forms)
    input_count = 0
    has_password = False
    for form in forms:
        if not isinstance(form, dict):
            continue
        inputs = form.get("inputs")
        if isinstance(inputs, list):
            input_count += len(inputs)
            for item in inputs:
                if isinstance(item, dict):
                    typ = safe_str(item.get("type")).lower()
                    name = safe_str(item.get("name")).lower()
                    if typ == "password" or "password" in name or "passwd" in name:
                        has_password = True
    return form_count, input_count, has_password


def choose_primary_screenshot(sample_dir: Path) -> str:
    for name in SCREENSHOT_CANDIDATES:
        path = sample_dir / name
        if path.exists() and path.is_file():
            return str(path)
    return ""


def visible_text_chars(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    try:
        return len(path.read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception:
        return 0


def discover_samples(input_root: Path) -> tuple[List[tuple[str, Path]], List[str]]:
    samples: List[tuple[str, Path]] = []
    missing: List[str] = []
    for triage_label in TRIAGE_LABELS:
        root = input_root / triage_label
        if not root.exists() or not root.is_dir():
            missing.append(str(root))
            continue
        for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if child.is_dir():
                samples.append((triage_label, child))
    return samples, missing


def build_record(triage_label: str, sample_dir: Path) -> Dict[str, str]:
    meta_path = sample_dir / "meta.json"
    url_path = sample_dir / "url.json"
    forms_path = sample_dir / "forms.json"
    redirect_path = sample_dir / "redirect_chain.json"

    meta_obj = read_json(meta_path)
    url_obj = read_json(url_path)
    forms_obj = read_json(forms_path) if forms_path.exists() else None
    redirect_obj = read_json(redirect_path) if redirect_path.exists() else None

    final_url, url_source = recover_final_url(sample_dir, url_obj, meta_obj, redirect_obj)
    final_host = url_host(final_url)
    etld1 = etld1_from_host(final_host)
    group_key = etld1 or final_host or sample_dir.name

    primary_screenshot = choose_primary_screenshot(sample_dir)
    has_screenshot = bool(primary_screenshot)
    has_url_evidence = bool(final_url)

    form_count, input_count, has_password = count_forms(forms_obj)
    has_visible = (sample_dir / "visible_text.txt").exists()
    visible_chars = visible_text_chars(sample_dir / "visible_text.txt")

    missing_artifacts: List[str] = []
    if not sample_dir.exists() or not sample_dir.is_dir():
        missing_artifacts.append("sample_dir")
    if not has_screenshot:
        missing_artifacts.append("screenshot")
    if not has_url_evidence:
        missing_artifacts.append("url_evidence")

    usable = not missing_artifacts
    artifact_status = "clean" if usable else "incomplete"
    exclude_reason = "" if usable else "missing_minimum_artifacts"
    notes = f"url_source={url_source}" if url_source else ""

    sample_id = ""
    if isinstance(meta_obj, dict):
        sample_id = first_string(meta_obj.get("sample_id"))
    if not sample_id:
        sample_id = sample_dir.name

    return {
        "sample_id": sample_id,
        "triage_label": triage_label,
        "benign_weight_group": TRIAGE_LABELS[triage_label],
        "usable_for_training": bool_csv(usable),
        "current_path": str(sample_dir),
        "final_url": final_url,
        "final_host": final_host,
        "etld1": etld1,
        "group_key": group_key,
        "has_screenshot_viewport": bool_csv((sample_dir / "screenshot_viewport.png").exists()),
        "has_screenshot_view": bool_csv((sample_dir / "screenshot_view.png").exists()),
        "has_screenshot_full": bool_csv((sample_dir / "screenshot_full.png").exists()),
        "primary_screenshot_path": primary_screenshot,
        "has_visible_text": bool_csv(has_visible),
        "visible_text_chars": str(visible_chars),
        "has_url_json": bool_csv(url_path.exists()),
        "has_forms_json": bool_csv(forms_path.exists()),
        "form_count": str(form_count),
        "input_count": str(input_count),
        "has_password": bool_csv(has_password),
        "has_net_summary": bool_csv((sample_dir / "net_summary.json").exists()),
        "has_redirect_chain": bool_csv(redirect_path.exists()),
        "artifact_status": artifact_status,
        "exclude_reason": exclude_reason,
        "notes": notes,
        "missing_artifacts": ";".join(missing_artifacts),
    }


def write_csv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def stable_group_order(groups: Iterable[str], seed: int, label: str) -> List[str]:
    return sorted(
        groups,
        key=lambda key: hashlib.sha256(f"{seed}|{label}|{key}".encode("utf-8")).hexdigest(),
    )


def split_targets(total: int, split: Sequence[float]) -> SplitTargets:
    train = int(math.floor(total * split[0]))
    val = int(math.floor(total * split[1]))
    test = total - train - val
    return SplitTargets(train=train, val=val, test=test)


def assign_groups(clean_rows: Sequence[Dict[str, str]], split: Sequence[float], seed: int) -> Dict[str, str]:
    group_stats: Dict[str, Counter] = defaultdict(Counter)
    for row in clean_rows:
        group_stats[row["group_key"]][row["triage_label"]] += 1
        group_stats[row["group_key"]]["total"] += 1

    total_targets = split_targets(len(clean_rows), split)
    t01_total = sum(1 for row in clean_rows if row["triage_label"] == "T01_benign_hard_negative")
    t01_targets = split_targets(t01_total, split)
    targets = {
        "train": {"total": total_targets.train, "t01": t01_targets.train},
        "val": {"total": total_targets.val, "t01": t01_targets.val},
        "test": {"total": total_targets.test, "t01": t01_targets.test},
    }
    counts = {
        "train": {"total": 0, "t01": 0},
        "val": {"total": 0, "t01": 0},
        "test": {"total": 0, "t01": 0},
    }
    assignments: Dict[str, str] = {}

    def assign(group_key: str, candidate_splits: Sequence[str], weight_t01: float) -> str:
        stats = group_stats[group_key]
        best_split = ""
        best_score: Optional[tuple[float, str]] = None
        for split_name in candidate_splits:
            projected_total = counts[split_name]["total"] + stats["total"]
            projected_t01 = counts[split_name]["t01"] + stats["T01_benign_hard_negative"]
            total_target = max(1, targets[split_name]["total"])
            t01_target = max(1, targets[split_name]["t01"])
            total_gap = abs(targets[split_name]["total"] - projected_total) / total_target
            t01_gap = abs(targets[split_name]["t01"] - projected_t01) / t01_target
            over_total = max(0, projected_total - targets[split_name]["total"])
            over_t01 = max(0, projected_t01 - targets[split_name]["t01"])
            score = (
                total_gap
                + weight_t01 * t01_gap
                + (2.0 * over_total / total_target)
                + (weight_t01 * over_t01 / t01_target),
                split_name,
            )
            if best_score is None or score < best_score:
                best_score = score
                best_split = split_name
        assignments[group_key] = best_split
        counts[best_split]["total"] += stats["total"]
        counts[best_split]["t01"] += stats["T01_benign_hard_negative"]
        return best_split

    def assign_t01_group(group_key: str) -> str:
        stats = group_stats[group_key]
        positive_deficit_splits = [
            split_name
            for split_name in ("train", "val", "test")
            if targets[split_name]["t01"] - counts[split_name]["t01"] > 0
        ]
        candidates = positive_deficit_splits or ["train", "val", "test"]
        best_split = ""
        best_score: Optional[tuple[float, str]] = None
        for split_name in candidates:
            t01_deficit_before = targets[split_name]["t01"] - counts[split_name]["t01"]
            projected_t01 = counts[split_name]["t01"] + stats["T01_benign_hard_negative"]
            projected_total = counts[split_name]["total"] + stats["total"]
            t01_target = max(1, targets[split_name]["t01"])
            total_target = max(1, targets[split_name]["total"])
            score = (
                -t01_deficit_before / t01_target,
                abs(targets[split_name]["t01"] - projected_t01) / t01_target,
                abs(targets[split_name]["total"] - projected_total) / total_target,
                split_name,
            )
            if best_score is None or score < best_score:
                best_score = score
                best_split = split_name
        assignments[group_key] = best_split
        counts[best_split]["total"] += stats["total"]
        counts[best_split]["t01"] += stats["T01_benign_hard_negative"]
        return best_split

    def assign_total_group(group_key: str) -> str:
        stats = group_stats[group_key]
        positive_deficit_splits = [
            split_name
            for split_name in ("train", "val", "test")
            if targets[split_name]["total"] - counts[split_name]["total"] > 0
        ]
        candidates = positive_deficit_splits or ["train", "val", "test"]
        best_split = ""
        best_score: Optional[tuple[float, str]] = None
        for split_name in candidates:
            total_deficit_before = targets[split_name]["total"] - counts[split_name]["total"]
            projected_total = counts[split_name]["total"] + stats["total"]
            total_target = max(1, targets[split_name]["total"])
            score = (
                -total_deficit_before / total_target,
                abs(targets[split_name]["total"] - projected_total) / total_target,
                split_name,
            )
            if best_score is None or score < best_score:
                best_score = score
                best_split = split_name
        assignments[group_key] = best_split
        counts[best_split]["total"] += stats["total"]
        counts[best_split]["t01"] += stats["T01_benign_hard_negative"]
        return best_split

    t01_groups = [key for key, stats in group_stats.items() if stats["T01_benign_hard_negative"] > 0]
    t00_only_groups = [key for key, stats in group_stats.items() if stats["T01_benign_hard_negative"] == 0]

    t01_groups = stable_group_order(t01_groups, seed, "t01")
    t01_groups.sort(key=lambda key: (-group_stats[key]["T01_benign_hard_negative"], -group_stats[key]["total"], key))
    for group_key in t01_groups:
        assign_t01_group(group_key)

    t00_only_groups = stable_group_order(t00_only_groups, seed, "t00")
    t00_only_groups.sort(key=lambda key: (-group_stats[key]["total"], key))
    for group_key in t00_only_groups:
        assign_total_group(group_key)

    return assignments


def add_split_fields(rows: Sequence[Dict[str, str]], assignments: Dict[str, str], seed: int) -> List[Dict[str, str]]:
    output: List[Dict[str, str]] = []
    for row in rows:
        out = dict(row)
        out["split"] = assignments[row["group_key"]]
        out["split_seed"] = str(seed)
        out["split_method"] = "group_key_etld1_or_final_host_seeded_greedy_80_10_10"
        output.append(out)
    return sorted(output, key=lambda r: (r["split"], r["triage_label"], r["group_key"], r["sample_id"]))


def count_by_label(rows: Sequence[Dict[str, str]]) -> Counter:
    return Counter(row["triage_label"] for row in rows)


def count_by_split_and_label(rows: Sequence[Dict[str, str]]) -> Dict[str, Counter]:
    result: Dict[str, Counter] = {name: Counter() for name in ("train", "val", "test")}
    for row in rows:
        result[row["split"]][row["triage_label"]] += 1
        result[row["split"]]["total"] += 1
    return result


def leakage_check(split_rows: Sequence[Dict[str, str]]) -> tuple[bool, Dict[str, List[str]]]:
    seen: Dict[str, set[str]] = defaultdict(set)
    for row in split_rows:
        seen[row["group_key"]].add(row["split"])
    leaked = {key: sorted(values) for key, values in seen.items() if len(values) > 1}
    return not leaked, leaked


def largest_groups(rows: Sequence[Dict[str, str]], limit: int = 10) -> List[tuple[str, int, int]]:
    stats: Dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        stats[row["group_key"]]["total"] += 1
        if row["triage_label"] == "T01_benign_hard_negative":
            stats[row["group_key"]]["t01"] += 1
    return sorted(((key, c["total"], c["t01"]) for key, c in stats.items()), key=lambda x: (-x[1], x[0]))[:limit]


def write_report(
    path: Path,
    run_timestamp: str,
    input_root: Path,
    output_dir: Path,
    scanned_counts: Counter,
    clean_rows: Sequence[Dict[str, str]],
    excluded_rows: Sequence[Dict[str, str]],
    split_rows: Sequence[Dict[str, str]],
    leakage_pass: bool,
    split_counts: Dict[str, Counter],
    split: Sequence[float],
    seed: int,
    missing_roots: Sequence[str],
) -> None:
    clean_counts = count_by_label(clean_rows)
    excluded_counts = count_by_label(excluded_rows)
    groups = {row["group_key"] for row in clean_rows}
    largest = largest_groups(clean_rows)
    lines = [
        "# Tranco Benign Clean Pool Report V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告冻结当前 T00/T01 benign clean candidate pool 的 manifest 和 group-based train / val / test split。",
        f"- 输入根：`{input_root}`",
        f"- 输出目录：`{output_dir}`",
        f"- 扫描 T00：{scanned_counts['T00_clear_benign']}；扫描 T01：{scanned_counts['T01_benign_hard_negative']}。",
        f"- clean pool：{len(clean_rows)}；excluded / incomplete：{len(excluded_rows)}。",
        f"- group_key 数量：{len(groups)}；group leakage check：{'PASS' if leakage_pass else 'FAIL'}。",
        "- 本任务没有训练模型、没有运行 teacher distillation、没有运行 OCR / YOLO / CLIP，也没有移动或改写原始样本目录。",
        "",
        "## English Version",
        "",
        "This report is the authoritative record for the V1 Tranco benign clean-pool manifest and group-based split.",
        "",
        "## 1. Run Metadata",
        "",
        f"- Run timestamp UTC: `{run_timestamp}`",
        f"- Input root: `{input_root}`",
        f"- Output directory: `{output_dir}`",
        f"- Split policy: `{split[0]:.3f} / {split[1]:.3f} / {split[2]:.3f}`",
        f"- Split seed: `{seed}`",
        "- Split method: `group_key_etld1_or_final_host_seeded_greedy_80_10_10`",
        "",
        "## 2. Input Counts",
        "",
        "| Triage label | Scanned | Clean | Excluded / incomplete |",
        "|---|---:|---:|---:|",
    ]
    for label in TRIAGE_LABELS:
        lines.append(f"| `{label}` | {scanned_counts[label]} | {clean_counts[label]} | {excluded_counts[label]} |")
    lines.extend(
        [
            f"| `total` | {sum(scanned_counts.values())} | {len(clean_rows)} | {len(excluded_rows)} |",
            "",
        "## 3. Split Distribution",
        "",
        "Counts in this section are derived from the current generated split CSV files.",
        "",
        "| Split | T00_clear_benign | T01_benign_hard_negative | Total |",
            "|---|---:|---:|---:|",
        ]
    )
    for split_name in ("train", "val", "test"):
        c = split_counts[split_name]
        lines.append(f"| `{split_name}` | {c['T00_clear_benign']} | {c['T01_benign_hard_negative']} | {c['total']} |")
    lines.extend(
        [
            "",
            "## 4. Group Split Check",
            "",
            f"- Group key: `etld1`, falling back to `final_host`, then sample directory name only if URL grouping is unavailable.",
            f"- Unique group keys in clean pool: `{len(groups)}`",
            f"- Group leakage check: `{'PASS' if leakage_pass else 'FAIL'}`",
            "- Rule: no `group_key` may appear in more than one split.",
            "",
            "Largest groups:",
            "",
            "| group_key | samples | T01 samples |",
            "|---|---:|---:|",
        ]
    )
    for group_key, total, t01_count in largest:
        lines.append(f"| `{group_key}` | {total} | {t01_count} |")
    lines.extend(
        [
            "",
            "## 5. Completeness Policy",
            "",
            "Samples are included in the clean pool when:",
            "",
            "- the sample directory exists and is readable;",
            "- at least one screenshot exists among `screenshot_viewport.png`, `screenshot_view.png`, and `screenshot_full.png`;",
            "- URL evidence can be recovered from `url.json`, redirect artifacts, metadata, or directory naming.",
            "",
            "`visible_text.txt`, `forms.json`, and `net_summary.json` are recorded as flags and do not automatically exclude a sample.",
            "",
            "## 6. Output Files",
            "",
            "- `tranco_benign_clean_pool_v1.csv`",
            "- `tranco_benign_excluded_or_incomplete_v1.csv`",
            "- `benign_train_manifest_v1.csv`",
            "- `benign_val_manifest_v1.csv`",
            "- `benign_test_manifest_v1.csv`",
            "- `tranco_benign_cleaning_report_v1.md`",
            "",
            "## 7. Caveats",
            "",
        ]
    )
    if missing_roots:
        for root in missing_roots:
            lines.append(f"- Missing expected input root: `{root}`")
    else:
        lines.append("- Optional pHash / simhash cluster fields were not generated because this task did not add heavy dependencies or run visual/OCR models.")
        lines.append("- eTLD+1 extraction uses a conservative stdlib approximation, not the public suffix list.")
        lines.append("- Path-derived `triage_label` is a dataset management / supervision field and must not be used as future model input.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build benign clean-pool manifests and group split.")
    parser.add_argument(
        "--input-root",
        default=r"E:\WardenData\manifests\tranco_benign_triage_v1",
        help="Triage root containing T00_clear_benign and T01_benign_hard_negative.",
    )
    parser.add_argument(
        "--output-dir",
        default=r"E:\WardenData\manifests\benign_clean_v1",
        help="Output directory for generated manifests and report.",
    )
    parser.add_argument("--split", nargs=3, type=float, default=(0.8, 0.1, 0.1), metavar=("TRAIN", "VAL", "TEST"))
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    if abs(sum(args.split) - 1.0) > 1e-6:
        raise SystemExit("--split values must sum to 1.0")

    input_root = Path(args.input_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    run_timestamp = now_utc_iso()

    samples, missing_roots = discover_samples(input_root)
    if missing_roots:
        for root in missing_roots:
            print(f"MISSING_INPUT_ROOT {root}")
        return 2

    records = [build_record(label, sample_dir) for label, sample_dir in samples]
    scanned_counts = Counter(label for label, _ in samples)
    clean_rows = [row for row in records if row["usable_for_training"] == "true"]
    excluded_rows = [row for row in records if row["usable_for_training"] != "true"]

    clean_rows = sorted(clean_rows, key=lambda r: (r["triage_label"], r["group_key"], r["sample_id"]))
    excluded_rows = sorted(excluded_rows, key=lambda r: (r["triage_label"], r["sample_id"]))

    assignments = assign_groups(clean_rows, args.split, args.seed)
    split_rows = add_split_fields(clean_rows, assignments, args.seed)
    leakage_pass, leakage = leakage_check(split_rows)
    if not leakage_pass:
        print(f"GROUP_LEAKAGE_FAIL {len(leakage)} leaked group keys")
        return 3

    split_counts = count_by_split_and_label(split_rows)

    write_csv(output_dir / "tranco_benign_clean_pool_v1.csv", clean_rows, CSV_FIELDS)
    write_csv(output_dir / "tranco_benign_excluded_or_incomplete_v1.csv", excluded_rows, CSV_FIELDS + EXCLUDED_EXTRA_FIELDS)
    for split_name in ("train", "val", "test"):
        rows = [row for row in split_rows if row["split"] == split_name]
        write_csv(output_dir / f"benign_{split_name}_manifest_v1.csv", rows, CSV_FIELDS + SPLIT_EXTRA_FIELDS)

    write_report(
        output_dir / "tranco_benign_cleaning_report_v1.md",
        run_timestamp=run_timestamp,
        input_root=input_root,
        output_dir=output_dir,
        scanned_counts=scanned_counts,
        clean_rows=clean_rows,
        excluded_rows=excluded_rows,
        split_rows=split_rows,
        leakage_pass=leakage_pass,
        split_counts=split_counts,
        split=args.split,
        seed=args.seed,
        missing_roots=missing_roots,
    )

    print(f"INPUT_ROOT={input_root}")
    print(f"OUTPUT_DIR={output_dir}")
    print(f"SCANNED_T00={scanned_counts['T00_clear_benign']}")
    print(f"SCANNED_T01={scanned_counts['T01_benign_hard_negative']}")
    print(f"CLEAN_POOL={len(clean_rows)}")
    print(f"EXCLUDED_OR_INCOMPLETE={len(excluded_rows)}")
    for split_name in ("train", "val", "test"):
        c = split_counts[split_name]
        print(
            f"SPLIT_{split_name.upper()} total={c['total']} "
            f"T00={c['T00_clear_benign']} T01={c['T01_benign_hard_negative']}"
        )
    print("GROUP_LEAKAGE_CHECK=PASS")
    print("ORIGINAL_SAMPLE_DIRS_MUTATED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
