"""Source-aware evidence-pack construction for Warden L1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

from scripts.data.common.html_payload_utils import parse_html_payload


HTML_BYTE_LIMIT = 300_000
TEXT_CHAR_LIMIT = 120_000
HTML_ARTIFACT_CANDIDATES = (
    "html_rendered.json",
    "html_raw.json",
    "html.json",
    "rendered_html.json",
    "page.html",
    "index.html",
)
SCREENSHOT_CANDIDATES = ("screenshot_viewport.png", "screenshot_view.png", "screenshot_full.png")


def _sample_dir_from_source(source: Any) -> Path:
    if isinstance(source, (str, Path)):
        return Path(source)
    if isinstance(source, dict):
        current_path = source.get("current_path") or source.get("sample_dir")
        if current_path:
            return Path(str(current_path))
    artifacts = getattr(source, "artifacts", None)
    sample_dir = getattr(artifacts, "sample_dir", None) or getattr(source, "sample_dir", None)
    if sample_dir:
        return Path(sample_dir)
    raise ValueError("L1 evidence source must be a sample path, manifest row with current_path, or SampleContext-like object")


def _read_json(path: Path, issues: list[Dict[str, str]]) -> Any:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception as exc:
        issues.append({"artifact": path.name, "issue": "json_parse_failure", "detail": str(exc)})
        return {}


def _read_text(path: Path, issues: list[Dict[str, str]], *, max_chars: int = TEXT_CHAR_LIMIT) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
    except Exception as exc:
        issues.append({"artifact": path.name, "issue": "text_read_failure", "detail": str(exc)})
        return ""


def _read_html(sample_dir: Path, issues: list[Dict[str, str]], *, byte_limit: int) -> Tuple[str, str, bool]:
    for name in HTML_ARTIFACT_CANDIDATES:
        path = sample_dir / name
        if not path.exists():
            continue
        try:
            raw = path.read_bytes()
        except Exception as exc:
            issues.append({"artifact": name, "issue": "html_read_failure", "detail": str(exc)})
            return "", name, False
        truncated = len(raw) > byte_limit
        text = raw[:byte_limit].decode("utf-8", errors="ignore")
        if path.suffix.lower() == ".json":
            try:
                text = parse_html_payload(json.loads(text))
            except Exception as exc:
                issues.append({"artifact": name, "issue": "html_json_parse_failure", "detail": str(exc)})
                text = ""
        return text, name, truncated
    return "", "", False


def build_evidence_pack(source: Any, *, html_byte_limit: int = HTML_BYTE_LIMIT) -> Dict[str, Any]:
    sample_dir = _sample_dir_from_source(source)
    issues: list[Dict[str, str]] = []
    missing = []

    for required_name in ("url.json", "visible_text.txt", "forms.json", "net_summary.json"):
        if not (sample_dir / required_name).exists():
            missing.append(required_name)

    url_info = _read_json(sample_dir / "url.json", issues)
    visible_text = _read_text(sample_dir / "visible_text.txt", issues)
    forms_payload = _read_json(sample_dir / "forms.json", issues)
    net_summary = _read_json(sample_dir / "net_summary.json", issues)
    html_text, html_artifact, html_truncated = _read_html(sample_dir, issues, byte_limit=html_byte_limit)

    artifact_presence = {
        "url_json": (sample_dir / "url.json").exists(),
        "visible_text_txt": (sample_dir / "visible_text.txt").exists(),
        "forms_json": (sample_dir / "forms.json").exists(),
        "net_summary_json": (sample_dir / "net_summary.json").exists(),
        "html_artifact": bool(html_artifact),
        "html_artifact_name": html_artifact,
        "screenshot_viewport_png": (sample_dir / "screenshot_viewport.png").exists(),
        "screenshot_view_png": (sample_dir / "screenshot_view.png").exists(),
        "screenshot_full_png": (sample_dir / "screenshot_full.png").exists(),
    }
    artifact_presence["any_screenshot"] = any(artifact_presence[name] for name in artifact_presence if name.startswith("screenshot_"))

    return {
        "sample_dir": str(sample_dir),
        "url_info": url_info if isinstance(url_info, dict) else {},
        "visible_text": visible_text,
        "forms_payload": forms_payload,
        "net_summary": net_summary,
        "html_text": html_text,
        "html_artifact_name": html_artifact,
        "html_truncated": html_truncated,
        "artifact_presence": artifact_presence,
        "missing_artifacts": missing,
        "issues": issues,
    }
