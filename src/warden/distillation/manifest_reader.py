"""Manifest reading helpers for the distillation runner skeleton."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


PATH_FIELDS = ("current_path", "sample_path", "path")


@dataclass(frozen=True)
class DistillationSampleRecord:
    sample_id: str
    sample_path: Path
    split: str
    row: Mapping[str, str]
    row_index: int


def _first_nonempty(row: Mapping[str, str], fields: Iterable[str]) -> str:
    for field in fields:
        value = row.get(field)
        if value:
            return value
    return ""


def read_manifest_records(
    manifest: str | Path,
    requested_split: str = "unknown",
    limit: int | None = None,
) -> list[DistillationSampleRecord]:
    manifest_path = Path(manifest)
    records: list[DistillationSampleRecord] = []
    with manifest_path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"manifest has no header: {manifest_path}")
        if not any(field in reader.fieldnames for field in PATH_FIELDS):
            raise ValueError(f"manifest is missing a sample path column: {manifest_path}")
        for index, row in enumerate(reader):
            if limit is not None and limit > 0 and len(records) >= limit:
                break
            sample_path = _first_nonempty(row, PATH_FIELDS)
            if not sample_path:
                raise ValueError(f"manifest row {index + 1} has no sample path")
            sample_id = row.get("sample_id") or f"row_{index + 1:06d}"
            split = row.get("split") or requested_split or "unknown"
            records.append(
                DistillationSampleRecord(
                    sample_id=sample_id,
                    sample_path=Path(sample_path),
                    split=split,
                    row=dict(row),
                    row_index=index,
                )
            )
    return records
