"""Vision evidence adapter stub.

The stub emits trigger placeholders only. It does not run OCR, YOLO, CLIP,
MobileCLIP, SNet, or SpecularNet-like inference.
"""

from __future__ import annotations

from typing import Any, Dict


class VisionEvidenceAdapterStub:
    def recover(self, evidence_pack: Dict[str, Any], routing: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": "VisionEvidenceAdapterStub",
            "loaded_model": False,
            "ocr_ran": False,
            "yolo_ran": False,
            "clip_ran": False,
            "recovered_text": "",
            "localized_ui_evidence": [],
            "requested_triggers": {
                "need_ocr_candidate": bool(routing.get("need_ocr_candidate")),
                "need_yolo_candidate": bool(routing.get("need_yolo_candidate")),
            },
            "notes": ["placeholder_only"],
        }
