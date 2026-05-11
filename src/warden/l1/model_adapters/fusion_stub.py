"""Fusion adapter stub for future trained fusion heads."""

from __future__ import annotations

from typing import Any, Dict


class FusionAdapterStub:
    def predict(self, features: Dict[str, Any], text_outputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {
            "adapter": "FusionAdapterStub",
            "loaded_model": False,
            "logits": {},
            "fusion_outputs": {},
            "notes": ["placeholder_only"],
        }
