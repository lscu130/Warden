#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List


def log(message: str) -> None:
    print(message, flush=True)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", errors="ignore") as handle:
        for lineno, line in enumerate(handle, 1):
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except Exception as exc:
                raise ValueError(f"{path} line {lineno} is not valid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path} line {lineno} is not a JSON object")
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_lines(path: Path, lines: Iterable[str]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for line in lines:
            handle.write(f"{line}\n")
            count += 1
    return count


def relpath_or_abs(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception:
        return str(path.resolve())


def discover_sample_dirs(roots: Iterable[Path], meta_name: str = "meta.json", url_name: str = "url.json") -> Iterator[Path]:
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        if root.is_dir() and (root / meta_name).exists() and (root / url_name).exists():
            key = str(root.resolve())
            if key not in seen:
                seen.add(key)
                yield root
        for meta_path in root.rglob(meta_name):
            sample_dir = meta_path.parent
            if not (sample_dir / url_name).exists():
                continue
            key = str(sample_dir.resolve())
            if key in seen:
                continue
            seen.add(key)
            yield sample_dir
