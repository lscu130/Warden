"""Core runtime/dataflow dataclasses for the Warden V0.1 skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from scripts.data.common.html_payload_utils import html_payload_exists, read_html_payload_text
from scripts.data.common.io_utils import read_json


def _read_json_optional(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return read_json(path)
    except Exception:
        return default


def _read_text_optional(path: Path, max_chars: int | None = None) -> str:
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if max_chars is None:
        return text
    return text[:max_chars]


@dataclass(frozen=True)
class ArtifactPackage:
    """Immutable per-sample artifact handle for runtime access."""

    sample_dir: Path

    @classmethod
    def from_sample_dir(cls, sample_dir: Path) -> "ArtifactPackage":
        sample_dir = sample_dir.resolve()
        if not sample_dir.is_dir():
            raise ValueError(f"sample_dir is not a directory: {sample_dir}")
        if not (sample_dir / "meta.json").exists():
            raise ValueError(f"sample_dir is missing meta.json: {sample_dir}")
        if not (sample_dir / "url.json").exists():
            raise ValueError(f"sample_dir is missing url.json: {sample_dir}")
        return cls(sample_dir=sample_dir)

    def path(self, name: str) -> Path:
        return self.sample_dir / name

    def read_json_optional(self, name: str, default: Any) -> Any:
        return _read_json_optional(self.path(name), default)

    def read_text_optional(self, name: str, max_chars: int | None = None) -> str:
        return _read_text_optional(self.path(name), max_chars=max_chars)

    def read_html_payload_optional(self, name: str, max_chars: int | None = None) -> str:
        return read_html_payload_text(self.sample_dir, name, max_chars=max_chars)

    def read_bytes_optional(self, name: str) -> bytes:
        path = self.path(name)
        if not path.exists():
            return b""
        try:
            return path.read_bytes()
        except Exception:
            return b""

    def artifact_presence(self) -> Dict[str, bool]:
        return {
            "meta_json": self.path("meta.json").exists(),
            "url_json": self.path("url.json").exists(),
            "forms_json": self.path("forms.json").exists(),
            "net_summary_json": self.path("net_summary.json").exists(),
            "diff_summary_json": self.path("diff_summary.json").exists(),
            "auto_labels_json": self.path("auto_labels.json").exists(),
            "visible_text_txt": self.path("visible_text.txt").exists(),
            "html_rendered": html_payload_exists(self.sample_dir, "html_rendered.json"),
            "html_raw": html_payload_exists(self.sample_dir, "html_raw.json"),
            "screenshot_viewport_png": self.path("screenshot_viewport.png").exists(),
            "screenshot_full_png": self.path("screenshot_full.png").exists(),
        }


@dataclass
class StageResult:
    """Per-stage audit record for the runtime trace."""

    stage: str
    status: str
    next_stage: str
    reason_codes: List[str] = field(default_factory=list)
    routing_outcome: Dict[str, Any] = field(default_factory=dict)
    input_contract: Dict[str, Any] = field(default_factory=dict)
    requested_heavy_artifacts: List[str] = field(default_factory=list)
    outputs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "next_stage": self.next_stage,
            "reason_codes": list(self.reason_codes),
            "routing_outcome": self.routing_outcome,
            "input_contract": self.input_contract,
            "requested_heavy_artifacts": list(self.requested_heavy_artifacts),
            "outputs": self.outputs,
        }


@dataclass
class SampleContext:
    """Shared mutable per-sample runtime state."""

    artifacts: ArtifactPackage
    sample_id: str
    input_url: str
    final_url: str
    page_title: str = ""
    label_hint: str = ""
    cheap_evidence: Dict[str, Any] = field(default_factory=dict)
    heavy_cache: Dict[str, Any] = field(default_factory=dict)
    stage_trace: List[StageResult] = field(default_factory=list)
    runtime_notes: List[str] = field(default_factory=list)
    terminal_outputs: Dict[str, Any] = field(default_factory=dict)

    def append_stage(self, result: StageResult) -> StageResult:
        self.stage_trace.append(result)
        return result

    def cache_heavy(self, cache_key: str, value: Any) -> Any:
        self.heavy_cache[cache_key] = value
        return value

    def get_heavy(self, cache_key: str) -> Any:
        return self.heavy_cache.get(cache_key)

    def release_heavy_cache(self) -> int:
        released = len(self.heavy_cache)
        self.heavy_cache.clear()
        return released
