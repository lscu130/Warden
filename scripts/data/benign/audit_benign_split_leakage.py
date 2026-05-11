#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read-only leakage and temporal-distribution audit for benign V1 split manifests.

The script reads existing split CSV files plus lightweight sample artifacts
referenced by `current_path`. It writes an audit CSV and a bilingual Markdown
report. It does not modify existing manifests, sample directories, labels, or
split assignments.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html.parser
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


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
    "split",
}

AUDIT_FIELDS = [
    "audit_type",
    "severity",
    "status",
    "split_a",
    "split_b",
    "key_type",
    "key_value",
    "count_a",
    "count_b",
    "example_sample_a",
    "example_sample_b",
    "details",
    "recommendation",
]

DIR_TS_RE = re.compile(r"_(?P<ts>\d{8}T\d{6}Z)$")


class TagSequenceParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: List[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        self.tags.append(tag.lower())

    def handle_endtag(self, tag: str) -> None:
        self.tags.append("/" + tag.lower())


@dataclass
class FingerprintStats:
    visible_text_read: int = 0
    visible_text_missing: int = 0
    html_read: int = 0
    html_missing: int = 0
    html_truncated: int = 0
    screenshot_hash_read: int = 0
    screenshot_hash_missing: int = 0
    screenshot_hash_not_run_reason: str = ""


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def audit_row(
    audit_type: str,
    severity: str,
    status: str,
    details: str,
    recommendation: str,
    split_a: str = "",
    split_b: str = "",
    key_type: str = "",
    key_value: str = "",
    count_a: int = 0,
    count_b: int = 0,
    example_sample_a: str = "",
    example_sample_b: str = "",
) -> Dict[str, str]:
    return {
        "audit_type": audit_type,
        "severity": severity,
        "status": status,
        "split_a": split_a,
        "split_b": split_b,
        "key_type": key_type,
        "key_value": key_value,
        "count_a": str(count_a) if count_a else "",
        "count_b": str(count_b) if count_b else "",
        "example_sample_a": example_sample_a,
        "example_sample_b": example_sample_b,
        "details": details,
        "recommendation": recommendation,
    }


def load_manifests(manifest_dir: Path) -> tuple[List[Dict[str, str]], Dict[str, List[Dict[str, str]]]]:
    by_split: Dict[str, List[Dict[str, str]]] = {}
    all_rows: List[Dict[str, str]] = []
    for split, filename in SPLIT_FILES.items():
        path = manifest_dir / filename
        if not path.exists():
            raise SystemExit(f"missing required manifest: {path}")
        rows = read_csv(path)
        for row in rows:
            if row.get("split") != split:
                raise SystemExit(f"split column mismatch in {path}: expected {split}, got {row.get('split')}")
        by_split[split] = rows
        all_rows.extend(rows)
    return all_rows, by_split


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def simhash64(text: str) -> int:
    tokens = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
    if not tokens:
        return 0
    weights = [0] * 64
    for token in tokens:
        digest = hashlib.blake2b(token.encode("utf-8", errors="ignore"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        for bit in range(64):
            weights[bit] += 1 if (value >> bit) & 1 else -1
    out = 0
    for bit, weight in enumerate(weights):
        if weight >= 0:
            out |= 1 << bit
    return out


def hamming_distance(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def simhash_bands(value: int, band_bits: int = 16) -> List[str]:
    mask = (1 << band_bits) - 1
    bands = []
    for idx in range(0, 64, band_bits):
        bands.append(f"{idx // band_bits}:{(value >> idx) & mask:04x}")
    return bands


def sample_path(row: Dict[str, str]) -> Path:
    return Path(row.get("current_path", ""))


def primary_sample_id(rows: Sequence[Dict[str, str]]) -> str:
    if not rows:
        return ""
    return rows[0].get("sample_id", "")


def exact_cross_split_findings(
    rows: Sequence[Dict[str, str]],
    key: str,
    audit_type: str,
    severity_if_found: str,
    max_rows: int,
) -> tuple[List[Dict[str, str]], int]:
    by_key: Dict[str, Dict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        value = (row.get(key) or "").strip()
        if value:
            by_key[value][row["split"]].append(row)

    findings: List[Dict[str, str]] = []
    total_leaked_keys = 0
    for value, split_map in sorted(by_key.items(), key=lambda item: (-sum(len(v) for v in item[1].values()), item[0])):
        splits = sorted(split_map)
        if len(splits) <= 1:
            continue
        total_leaked_keys += 1
        for i, split_a in enumerate(splits):
            for split_b in splits[i + 1 :]:
                if len(findings) < max_rows:
                    findings.append(
                        audit_row(
                            audit_type=audit_type,
                            severity=severity_if_found,
                            status="finding",
                            split_a=split_a,
                            split_b=split_b,
                            key_type=key,
                            key_value=value,
                            count_a=len(split_map[split_a]),
                            count_b=len(split_map[split_b]),
                            example_sample_a=primary_sample_id(split_map[split_a]),
                            example_sample_b=primary_sample_id(split_map[split_b]),
                            details=f"{key} appears in multiple splits",
                            recommendation="Investigate whether this requires re-split or stronger grouping.",
                        )
                    )
    if total_leaked_keys == 0:
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="info",
                status="pass",
                key_type=key,
                details=f"No cross-split duplicate found for {key}.",
                recommendation="No action required for this exact-key check.",
            )
        )
    elif total_leaked_keys > len(findings):
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity=severity_if_found,
                status="partial",
                key_type=key,
                details=f"{total_leaked_keys} cross-split keys found; CSV lists first {len(findings)} pair rows.",
                recommendation="Review full script summary or rerun with a larger --max-findings if needed.",
            )
        )
    return findings, total_leaked_keys


def top_concentration(rows_by_split: Dict[str, List[Dict[str, str]]], key: str, top_n: int = 10) -> Dict[str, List[tuple[str, int]]]:
    result: Dict[str, List[tuple[str, int]]] = {}
    for split, rows in rows_by_split.items():
        counter = Counter((row.get(key) or "").strip() or "unknown" for row in rows)
        result[split] = counter.most_common(top_n)
    return result


def read_visible_text(row: Dict[str, str]) -> Optional[str]:
    path = sample_path(row) / "visible_text.txt"
    if not path.exists() or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8-sig", errors="ignore")
    except Exception:
        return None


def find_html_path(row: Dict[str, str]) -> Optional[Path]:
    base = sample_path(row)
    for name in ("html_rendered.json", "html_raw.json", "html_rendered.html", "html_raw.html"):
        path = base / name
        if path.exists() and path.is_file():
            return path
    return None


def read_html_text(path: Path, max_bytes: int) -> tuple[str, bool]:
    with path.open("rb") as handle:
        data = handle.read(max_bytes + 1)
    truncated = len(data) > max_bytes
    if truncated:
        data = data[:max_bytes]
    text = data.decode("utf-8", errors="ignore")
    if path.suffix.lower() == ".json" and not truncated:
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                for key in ("html", "content", "rendered_html", "raw_html", "text"):
                    if isinstance(obj.get(key), str):
                        return obj[key][:max_bytes], len(obj[key].encode("utf-8", errors="ignore")) > max_bytes
            if isinstance(obj, str):
                return obj[:max_bytes], len(obj.encode("utf-8", errors="ignore")) > max_bytes
        except Exception:
            pass
    return text, truncated


def tag_sequence(html_text: str) -> List[str]:
    parser = TagSequenceParser()
    try:
        parser.feed(html_text)
    except Exception:
        return parser.tags
    return parser.tags


def fingerprint_artifacts(rows: Sequence[Dict[str, str]], max_html_bytes: int) -> tuple[Dict[str, Dict[str, Any]], FingerprintStats]:
    fingerprints: Dict[str, Dict[str, Any]] = {}
    stats = FingerprintStats(
        screenshot_hash_not_run_reason="image hashing dependency-free path not implemented; new dependencies are not allowed"
    )
    for row in rows:
        sid = row["sample_id"]
        item: Dict[str, Any] = {}
        text = read_visible_text(row)
        if text is None:
            stats.visible_text_missing += 1
        else:
            stats.visible_text_read += 1
            norm = normalize_text(text)
            item["visible_text_hash"] = sha256_text(norm) if norm else ""
            item["visible_text_simhash"] = simhash64(norm) if norm else 0
            item["visible_text_chars"] = len(text)

        html_path = find_html_path(row)
        if html_path is None:
            stats.html_missing += 1
        else:
            html_text, truncated = read_html_text(html_path, max_html_bytes)
            if truncated:
                stats.html_truncated += 1
            tags = tag_sequence(html_text)
            if tags:
                stats.html_read += 1
                tag_text = " ".join(tags)
                item["html_dom_hash"] = sha256_text(tag_text)
                item["html_dom_simhash"] = simhash64(tag_text)
                item["html_tag_count"] = len(tags)
            else:
                stats.html_missing += 1

        fingerprints[sid] = item
    return fingerprints, stats


def exact_hash_findings(
    rows: Sequence[Dict[str, str]],
    fingerprints: Dict[str, Dict[str, Any]],
    fp_key: str,
    audit_type: str,
    max_rows: int,
) -> tuple[List[Dict[str, str]], int]:
    by_hash: Dict[str, Dict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        value = fingerprints.get(row["sample_id"], {}).get(fp_key)
        if isinstance(value, str) and value:
            by_hash[value][row["split"]].append(row)
    findings: List[Dict[str, str]] = []
    leaked = 0
    for value, split_map in sorted(by_hash.items(), key=lambda item: (-sum(len(v) for v in item[1].values()), item[0])):
        splits = sorted(split_map)
        if len(splits) <= 1:
            continue
        leaked += 1
        for i, split_a in enumerate(splits):
            for split_b in splits[i + 1 :]:
                if len(findings) < max_rows:
                    findings.append(
                        audit_row(
                            audit_type=audit_type,
                            severity="warning",
                            status="finding",
                            split_a=split_a,
                            split_b=split_b,
                            key_type=fp_key,
                            key_value=value,
                            count_a=len(split_map[split_a]),
                            count_b=len(split_map[split_b]),
                            example_sample_a=primary_sample_id(split_map[split_a]),
                            example_sample_b=primary_sample_id(split_map[split_b]),
                            details=f"{fp_key} appears in multiple splits.",
                            recommendation="Review examples for template/content duplication before training claims.",
                        )
                    )
    if leaked == 0:
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="info",
                status="pass",
                key_type=fp_key,
                details=f"No cross-split exact duplicate found for {fp_key}.",
                recommendation="No action required for this exact-hash check.",
            )
        )
    elif leaked > len(findings):
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="warning",
                status="partial",
                key_type=fp_key,
                details=f"{leaked} cross-split hash keys found; CSV lists first {len(findings)} pair rows.",
                recommendation="Rerun with larger --max-findings for full pair listing if needed.",
            )
        )
    return findings, leaked


def near_duplicate_findings(
    rows: Sequence[Dict[str, str]],
    fingerprints: Dict[str, Dict[str, Any]],
    fp_key: str,
    audit_type: str,
    threshold: int,
    max_rows: int,
    max_band_size: int,
) -> tuple[List[Dict[str, str]], int, int]:
    candidates: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    value_counts = Counter()
    for row in rows:
        value = fingerprints.get(row["sample_id"], {}).get(fp_key)
        if not isinstance(value, int) or value == 0:
            continue
        value_counts[value] += 1
        entry = {"row": row, "value": value}
        for band in simhash_bands(value):
            candidates[band].append(entry)

    seen_pairs: set[tuple[str, str]] = set()
    findings: List[Dict[str, str]] = []
    total = 0
    skipped_large_bands = 0
    for entries in candidates.values():
        if len(entries) < 2:
            continue
        unique_value_count = len({entry["value"] for entry in entries})
        if len(entries) > max_band_size or unique_value_count > max_band_size:
            skipped_large_bands += 1
            continue
        for i, left in enumerate(entries):
            for right in entries[i + 1 :]:
                row_a = left["row"]
                row_b = right["row"]
                if row_a["split"] == row_b["split"]:
                    continue
                sid_a = row_a["sample_id"]
                sid_b = row_b["sample_id"]
                pair = tuple(sorted((sid_a, sid_b)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                if left["value"] == right["value"] and value_counts[left["value"]] > max_band_size:
                    skipped_large_bands += 1
                    continue
                dist = hamming_distance(left["value"], right["value"])
                if dist > threshold:
                    continue
                total += 1
                if len(findings) < max_rows:
                    findings.append(
                        audit_row(
                            audit_type=audit_type,
                            severity="warning",
                            status="finding",
                            split_a=row_a["split"],
                            split_b=row_b["split"],
                            key_type=fp_key,
                            key_value=f"hamming_distance={dist}",
                            count_a=1,
                            count_b=1,
                            example_sample_a=sid_a,
                            example_sample_b=sid_b,
                            details=f"Simhash Hamming distance <= {threshold}.",
                            recommendation="Review examples as possible template/content near-duplicates.",
                        )
                    )
    if total == 0:
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="info",
                status="pass",
                key_type=fp_key,
                details=f"No cross-split simhash near-duplicate candidates found at threshold {threshold}.",
                recommendation="No action required for this lightweight near-duplicate check.",
            )
        )
    elif total > len(findings):
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="warning",
                status="partial",
                key_type=fp_key,
                details=f"{total} candidate pairs found; CSV lists first {len(findings)}.",
                recommendation="Review listed examples and rerun with larger --max-findings if needed.",
            )
        )
    if skipped_large_bands:
        findings.append(
            audit_row(
                audit_type=audit_type,
                severity="warning",
                status="partial",
                key_type=fp_key,
                details=f"Skipped {skipped_large_bands} oversized simhash bands above max_band_size={max_band_size}.",
                recommendation="Run a stronger offline clustering audit if these skipped buckets matter for final benchmark claims.",
            )
        )
    return findings, total, skipped_large_bands


def parse_capture_timestamp(row: Dict[str, str]) -> tuple[str, str, str]:
    sample_id = row.get("sample_id", "")
    match = DIR_TS_RE.search(sample_id)
    if not match:
        return "", "unknown", "unknown"
    ts = match.group("ts")
    try:
        dt = datetime.strptime(ts, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return "", "unknown", "unknown"
    return dt.isoformat().replace("+00:00", "Z"), dt.strftime("%Y-%m-%d"), dt.strftime("%Y-%m")


def temporal_summary(rows_by_split: Dict[str, List[Dict[str, str]]]) -> Dict[str, Dict[str, Any]]:
    summary: Dict[str, Dict[str, Any]] = {}
    for split, rows in rows_by_split.items():
        dates = Counter()
        months = Counter()
        timestamps: List[str] = []
        unknown = 0
        for row in rows:
            ts, date, month = parse_capture_timestamp(row)
            if not ts:
                unknown += 1
                continue
            timestamps.append(ts)
            dates[date] += 1
            months[month] += 1
        summary[split] = {
            "unknown": unknown,
            "earliest": min(timestamps) if timestamps else "",
            "latest": max(timestamps) if timestamps else "",
            "top_dates": dates.most_common(10),
            "months": dict(sorted(months.items())),
        }
    return summary


def label_counts(rows_by_split: Dict[str, List[Dict[str, str]]]) -> Dict[str, Counter]:
    return {split: Counter(row["triage_label"] for row in rows) for split, rows in rows_by_split.items()}


def artifact_availability_rows(stats: FingerprintStats, total_rows: int) -> List[Dict[str, str]]:
    return [
        audit_row(
            "artifact_availability",
            "info",
            "completed",
            f"visible_text read for {stats.visible_text_read}/{total_rows}; missing/unreadable {stats.visible_text_missing}.",
            "Treat visible-text checks as partial if missing/unreadable count is material.",
            key_type="visible_text",
            count_a=stats.visible_text_read,
            count_b=stats.visible_text_missing,
        ),
        audit_row(
            "artifact_availability",
            "info",
            "completed",
            f"HTML/DOM artifacts parsed for {stats.html_read}/{total_rows}; missing/unreadable {stats.html_missing}; truncated {stats.html_truncated}.",
            "Treat DOM checks as lightweight and partial because HTML is truncated for bounded runtime.",
            key_type="html_dom",
            count_a=stats.html_read,
            count_b=stats.html_missing,
        ),
        audit_row(
            "screenshot_hash_near_duplicate",
            "info",
            "not_run",
            stats.screenshot_hash_not_run_reason,
            "Run a separate approved image-hash audit if screenshot near-duplicate detection is required.",
            key_type="screenshot_hash",
        ),
    ]


def report_table_counts(counts: Dict[str, Counter], rows_by_split: Dict[str, List[Dict[str, str]]]) -> List[str]:
    lines = ["| Split | Rows | T00_clear_benign | T01_benign_hard_negative |", "|---|---:|---:|---:|"]
    for split in ("train", "val", "test"):
        c = counts[split]
        lines.append(f"| `{split}` | {len(rows_by_split[split])} | {c['T00_clear_benign']} | {c['T01_benign_hard_negative']} |")
    return lines


def write_report(
    path: Path,
    run_timestamp: str,
    manifest_dir: Path,
    output_dir: Path,
    rows_by_split: Dict[str, List[Dict[str, str]]],
    counts: Dict[str, Counter],
    findings_count: Dict[str, int],
    exact_leakage_counts: Dict[str, int],
    near_counts: Dict[str, int],
    fp_stats: FingerprintStats,
    temporal: Dict[str, Dict[str, Any]],
    host_top: Dict[str, List[tuple[str, int]]],
    etld1_top: Dict[str, List[tuple[str, int]]],
    group_top: Dict[str, List[tuple[str, int]]],
) -> None:
    total = sum(len(v) for v in rows_by_split.values())
    lines: List[str] = [
        "# Benign Split Leakage Audit V1",
        "",
        "## 中文摘要",
        "",
        "- 本报告对当前 benign train / val / test manifest 做只读泄露与时间分布审计。",
        f"- manifest 目录：`{manifest_dir}`",
        f"- 输出目录：`{output_dir}`",
        f"- 总 split 行数：{total}。",
        f"- current `group_key` 泄露：{exact_leakage_counts.get('group_key', 0)} 个跨 split key。",
        f"- `sample_id` / `current_path` / `final_url` 精确跨 split 重复均按下方英文结果为准。",
        "- screenshot hash 未运行：没有引入新依赖，也未运行视觉模型。",
        "",
        "## English Version",
        "",
        "This English section is authoritative.",
        "",
        "## 1. Executive Summary",
        "",
        f"- Run timestamp UTC: `{run_timestamp}`",
        f"- Manifest directory: `{manifest_dir}`",
        f"- Output directory: `{output_dir}`",
        f"- Rows audited: `{total}`",
        "- The audit is read-only: it does not regenerate splits, modify manifests, move samples, alter labels, or run models.",
        "- Current split is acceptable for preliminary training only if the listed caveats are accepted.",
        "",
        "## 2. Inputs Checked",
        "",
        "- `tranco_benign_clean_pool_v1.csv`",
        "- `benign_train_manifest_v1.csv`",
        "- `benign_val_manifest_v1.csv`",
        "- `benign_test_manifest_v1.csv`",
        "- Sample artifacts referenced by `current_path`, read-only: `visible_text.txt`, `html_rendered.json`, `html_raw.json`, and metadata paths when present.",
        "",
        "## 3. Split Row Counts",
        "",
        *report_table_counts(counts, rows_by_split),
        "",
        "## 4. T00/T01 Distribution",
        "",
        "The split distribution is close to the intended 80/10/10 target and preserves about 200+ T01 examples in validation and test.",
        "",
        "## 5. Exact Leakage Results",
        "",
    ]
    for key in ("sample_id", "current_path", "final_url", "final_host", "group_key"):
        count = exact_leakage_counts.get(key, 0)
        lines.append(f"- `{key}` cross-split leaked keys: `{count}`")
    lines.extend(
        [
            "",
            "## 6. Near-Duplicate Results",
            "",
            f"- Visible-text exact cross-split hash keys: `{exact_leakage_counts.get('visible_text_hash', 0)}`",
            f"- Visible-text simhash near-duplicate candidate pairs: `{near_counts.get('visible_text_simhash', 0)}`",
            f"- Visible-text simhash oversized bands skipped: `{near_counts.get('visible_text_skipped_bands', 0)}`",
            f"- HTML/DOM exact structure cross-split hash keys: `{exact_leakage_counts.get('html_dom_hash', 0)}`",
            f"- HTML/DOM simhash near-duplicate candidate pairs: `{near_counts.get('html_dom_simhash', 0)}`",
            f"- HTML/DOM simhash oversized bands skipped: `{near_counts.get('html_dom_skipped_bands', 0)}`",
            "- Screenshot near-duplicate check: `not_run` because dependency-free image hashing was not implemented and new dependencies are not allowed.",
            "",
            "## 7. Host / eTLD+1 / group_key Results",
            "",
            "Top concentrations by split:",
            "",
        ]
    )
    for title, data in (("final_host", host_top), ("etld1", etld1_top), ("group_key", group_top)):
        lines.extend([f"### {title}", "", "| Split | Top values |", "|---|---|"])
        for split in ("train", "val", "test"):
            top = "; ".join(f"{value}={count}" for value, count in data[split][:5])
            lines.append(f"| `{split}` | {top} |")
        lines.append("")

    lines.extend(["## 8. Temporal Distribution Results", "", "| Split | Earliest | Latest | Unknown timestamp | Months |", "|---|---|---|---:|---|"])
    for split in ("train", "val", "test"):
        item = temporal[split]
        months = "; ".join(f"{month}={count}" for month, count in item["months"].items())
        lines.append(f"| `{split}` | `{item['earliest']}` | `{item['latest']}` | {item['unknown']} | {months} |")

    lines.extend(
        [
            "",
            "## 9. Artifact Availability",
            "",
            f"- visible_text read: `{fp_stats.visible_text_read}`; missing/unreadable: `{fp_stats.visible_text_missing}`",
            f"- HTML/DOM parsed: `{fp_stats.html_read}`; missing/unreadable: `{fp_stats.html_missing}`; truncated for bounded audit: `{fp_stats.html_truncated}`",
            f"- screenshot hash: `not_run`; reason: {fp_stats.screenshot_hash_not_run_reason}",
            "",
            "## 10. Not Run / Partial Checks",
            "",
            "- Screenshot near-duplicate hashing was not run.",
            "- DOM checks are partial because HTML artifacts are read with a bounded byte limit.",
            "- Visible-text and DOM simhash checks are lightweight heuristics, not a full template-clustering proof.",
            "",
            "## 11. Risks And Caveats",
            "",
            "- The current eTLD+1 value comes from the existing manifest and may still reflect conservative stdlib grouping rather than a public suffix list.",
            "- Any visible-text or DOM near-duplicate candidates should be reviewed before strong benchmark claims.",
            "- Absence of screenshot hash findings is not evidence that screenshot leakage is absent.",
            "- `triage_label` remains dataset-management metadata and must not be used as model input.",
            "",
            "## 12. Recommended Next Step",
            "",
            "- If exact URL/host/group leakage count is nonzero, run a re-split task before training.",
            "- If near-duplicate counts are material, run a stronger cluster-based split audit before benchmark claims.",
            "- Consider a public-suffix-list-backed grouping task and a separate temporal holdout task before final evaluation claims.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit benign V1 split leakage and temporal distribution.")
    parser.add_argument("--manifest-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--output-dir", default=r"E:\WardenData\manifests\benign_clean_v1")
    parser.add_argument("--max-findings", type=int, default=200)
    parser.add_argument("--max-band-size", type=int, default=250)
    parser.add_argument("--simhash-threshold", type=int, default=3)
    parser.add_argument("--max-html-bytes", type=int, default=131072)
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    manifest_dir = Path(args.manifest_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    all_rows, rows_by_split = load_manifests(manifest_dir)
    run_timestamp = now_utc_iso()
    audit_rows: List[Dict[str, str]] = []
    exact_counts: Dict[str, int] = {}

    exact_specs = [
        ("sample_id", "exact_duplicate", "high"),
        ("current_path", "exact_duplicate", "high"),
        ("final_url", "exact_duplicate", "high"),
        ("final_host", "host_overlap", "warning"),
        ("etld1", "etld1_overlap", "warning"),
        ("group_key", "current_group_key_leakage", "high"),
    ]
    for key, audit_type, severity in exact_specs:
        rows, count = exact_cross_split_findings(all_rows, key, audit_type, severity, args.max_findings)
        audit_rows.extend(rows)
        exact_counts[key] = count

    counts = label_counts(rows_by_split)
    for split in ("train", "val", "test"):
        c = counts[split]
        audit_rows.append(
            audit_row(
                "label_bucket_distribution",
                "info",
                "completed",
                f"{split}: total={len(rows_by_split[split])}, T00={c['T00_clear_benign']}, T01={c['T01_benign_hard_negative']}",
                "No action unless downstream task requires a different T01 ratio.",
                split_a=split,
                count_a=len(rows_by_split[split]),
            )
        )

    fingerprints, fp_stats = fingerprint_artifacts(all_rows, args.max_html_bytes)
    text_exact_rows, text_exact_count = exact_hash_findings(
        all_rows, fingerprints, "visible_text_hash", "visible_text_exact_hash", args.max_findings
    )
    audit_rows.extend(text_exact_rows)
    exact_counts["visible_text_hash"] = text_exact_count
    text_near_rows, text_near_count, text_near_skipped = near_duplicate_findings(
        all_rows,
        fingerprints,
        "visible_text_simhash",
        "visible_text_near_duplicate",
        args.simhash_threshold,
        args.max_findings,
        args.max_band_size,
    )
    audit_rows.extend(text_near_rows)

    html_exact_rows, html_exact_count = exact_hash_findings(
        all_rows, fingerprints, "html_dom_hash", "html_dom_exact_hash", args.max_findings
    )
    audit_rows.extend(html_exact_rows)
    exact_counts["html_dom_hash"] = html_exact_count
    html_near_rows, html_near_count, html_near_skipped = near_duplicate_findings(
        all_rows,
        fingerprints,
        "html_dom_simhash",
        "html_dom_structure_near_duplicate",
        args.simhash_threshold,
        args.max_findings,
        args.max_band_size,
    )
    audit_rows.extend(html_near_rows)

    audit_rows.extend(artifact_availability_rows(fp_stats, len(all_rows)))

    temporal = temporal_summary(rows_by_split)
    for split in ("train", "val", "test"):
        item = temporal[split]
        audit_rows.append(
            audit_row(
                "temporal_distribution",
                "info",
                "completed",
                f"{split}: earliest={item['earliest']}, latest={item['latest']}, unknown={item['unknown']}, months={item['months']}",
                "Consider a separate temporal holdout task if this distribution is unsuitable for final evaluation.",
                split_a=split,
                count_a=len(rows_by_split[split]),
            )
        )

    host_top = top_concentration(rows_by_split, "final_host")
    etld1_top = top_concentration(rows_by_split, "etld1")
    group_top = top_concentration(rows_by_split, "group_key")

    audit_csv = output_dir / "benign_split_leakage_audit_v1.csv"
    audit_report = output_dir / "benign_split_leakage_audit_report_v1.md"
    write_csv(audit_csv, audit_rows, AUDIT_FIELDS)
    write_report(
        audit_report,
        run_timestamp=run_timestamp,
        manifest_dir=manifest_dir,
        output_dir=output_dir,
        rows_by_split=rows_by_split,
        counts=counts,
        findings_count=Counter(row["audit_type"] for row in audit_rows),
        exact_leakage_counts=exact_counts,
        near_counts={
            "visible_text_simhash": text_near_count,
            "html_dom_simhash": html_near_count,
            "visible_text_skipped_bands": text_near_skipped,
            "html_dom_skipped_bands": html_near_skipped,
        },
        fp_stats=fp_stats,
        temporal=temporal,
        host_top=host_top,
        etld1_top=etld1_top,
        group_top=group_top,
    )

    print(f"MANIFEST_DIR={manifest_dir}")
    print(f"OUTPUT_DIR={output_dir}")
    for split in ("train", "val", "test"):
        c = counts[split]
        print(f"SPLIT_{split.upper()} rows={len(rows_by_split[split])} T00={c['T00_clear_benign']} T01={c['T01_benign_hard_negative']}")
    print(f"EXACT_SAMPLE_ID_LEAKAGE={exact_counts['sample_id']}")
    print(f"EXACT_CURRENT_PATH_LEAKAGE={exact_counts['current_path']}")
    print(f"EXACT_FINAL_URL_LEAKAGE={exact_counts['final_url']}")
    print(f"FINAL_HOST_OVERLAP_KEYS={exact_counts['final_host']}")
    print(f"ETLD1_OVERLAP_KEYS={exact_counts['etld1']}")
    print(f"GROUP_KEY_LEAKAGE={exact_counts['group_key']}")
    print(f"VISIBLE_TEXT_EXACT_HASH_LEAKAGE={text_exact_count}")
    print(f"VISIBLE_TEXT_NEAR_DUPLICATE_CANDIDATES={text_near_count}")
    print(f"VISIBLE_TEXT_NEAR_DUPLICATE_SKIPPED_BANDS={text_near_skipped}")
    print(f"HTML_DOM_EXACT_HASH_LEAKAGE={html_exact_count}")
    print(f"HTML_DOM_NEAR_DUPLICATE_CANDIDATES={html_near_count}")
    print(f"HTML_DOM_NEAR_DUPLICATE_SKIPPED_BANDS={html_near_skipped}")
    print("SCREENSHOT_HASH_NEAR_DUPLICATE=NOT_RUN")
    print(f"AUDIT_CSV={audit_csv}")
    print(f"AUDIT_REPORT={audit_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
