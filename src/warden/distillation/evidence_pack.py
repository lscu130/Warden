"""Read-only evidence pack construction for distillation skeleton runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .manifest_reader import DistillationSampleRecord


METADATA_ONLY_FIELDS = {
    "triage_label",
    "split",
    "label",
    "human_label",
    "manual_label",
    "folder",
    "folder_name",
}


@dataclass(frozen=True)
class DistillationEvidencePack:
    sample_id: str
    sample_path: Path
    teacher_visible_evidence: dict[str, Any]
    metadata_not_for_prompt: dict[str, Any]
    missing_artifacts: list[str]
    bad_json_issues: list[dict[str, str]]
    review_reasons: list[str]
    input_modalities: list[str]

    def summary(self) -> dict[str, Any]:
        visible = self.teacher_visible_evidence.get("visible_text", {})
        return {
            "visible_text_length": visible.get("length", 0),
            "missing_artifacts": list(self.missing_artifacts),
            "bad_json_issues": list(self.bad_json_issues),
            "review_reasons": list(self.review_reasons),
            "input_modalities": list(self.input_modalities),
        }


def _row_to_fields(row_or_record: Mapping[str, str] | DistillationSampleRecord) -> tuple[str, Path, Mapping[str, str]]:
    if isinstance(row_or_record, DistillationSampleRecord):
        return row_or_record.sample_id, row_or_record.sample_path, row_or_record.row
    row = row_or_record
    sample_id = row.get("sample_id") or "unknown_sample"
    sample_path = Path(row.get("current_path") or row.get("sample_path") or row.get("path") or "")
    return sample_id, sample_path, row


def _read_json(path: Path, issues: list[dict[str, str]]) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception as exc:  # noqa: BLE001 - record artifact issue without aborting the run.
        issues.append({"artifact": path.name, "error": str(exc)})
        return None


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def _html_text(sample_path: Path) -> str | None:
    for name in ("html_rendered.html", "rendered.html", "page.html", "html.html"):
        text = _read_text(sample_path / name)
        if text is not None:
            return text
    json_payload = _read_json(sample_path / "html_rendered.json", [])
    if isinstance(json_payload, dict):
        value = json_payload.get("text") or json_payload.get("html")
        if isinstance(value, str):
            return value
    return None


def build_evidence_pack(row_or_record: Mapping[str, str] | DistillationSampleRecord) -> DistillationEvidencePack:
    sample_id, sample_path, row = _row_to_fields(row_or_record)
    missing: list[str] = []
    bad_json: list[dict[str, str]] = []
    review_reasons: list[str] = []
    modalities: list[str] = []

    url_payload = _read_json(sample_path / "url.json", bad_json)
    if url_payload is None:
        missing.append("url.json")
        review_reasons.append("url_json_missing")
    else:
        modalities.append("url")

    visible_text = _read_text(sample_path / "visible_text.txt")
    if visible_text is None:
        visible_text = ""
        missing.append("visible_text.txt")
        review_reasons.append("visible_text_missing")
    elif not visible_text.strip():
        review_reasons.append("visible_text_missing")
    elif len(visible_text.strip()) < 24:
        review_reasons.append("visible_text_sparse")
    if visible_text:
        modalities.append("visible_text")

    forms_payload = _read_json(sample_path / "forms.json", bad_json)
    if forms_payload is None:
        missing.append("forms.json")
    else:
        modalities.append("forms")

    net_payload = _read_json(sample_path / "net_summary.json", bad_json)
    if net_payload is None:
        missing.append("net_summary.json")
    else:
        modalities.append("network")

    html = _html_text(sample_path)
    if html is None:
        missing.append("html_actionable")
    else:
        modalities.append("html_actionable")

    if bad_json:
        review_reasons.append("bad_json_artifact")

    form_count = 0
    if isinstance(forms_payload, dict):
        forms = forms_payload.get("forms")
        if isinstance(forms, list):
            form_count = len(forms)
    if form_count:
        review_reasons.append("action_surface_present_with_mock_context")

    metadata = {key: value for key, value in row.items() if key in METADATA_ONLY_FIELDS and value}
    evidence = {
        "url": url_payload or {},
        "visible_text": {
            "length": len(visible_text),
            "excerpt": visible_text.strip()[:500],
        },
        "forms": {
            "form_count": form_count,
            "summary": forms_payload or {},
        },
        "network": net_payload or {},
        "html_actionable": {
            "available": html is not None,
            "length": len(html or ""),
            "excerpt": (html or "")[:500],
        },
    }

    return DistillationEvidencePack(
        sample_id=sample_id,
        sample_path=sample_path,
        teacher_visible_evidence=evidence,
        metadata_not_for_prompt=metadata,
        missing_artifacts=missing,
        bad_json_issues=bad_json,
        review_reasons=sorted(set(review_reasons)),
        input_modalities=modalities,
    )
