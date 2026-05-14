"""Resume helpers for distillation skeleton outputs."""

from __future__ import annotations

from pathlib import Path

from .jsonl_writer import read_jsonl


def load_processed_record_ids(records_path: Path) -> set[str]:
    processed: set[str] = set()
    for row in read_jsonl(records_path):
        record_id = row.get("record_id")
        if isinstance(record_id, str):
            processed.add(record_id)
    return processed
