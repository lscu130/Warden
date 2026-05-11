"""Text tower adapter stub.

The stub does not load models, access the network, or generate explanations.
"""

from __future__ import annotations

from typing import Any, Dict


class TextTowerAdapterStub:
    def predict(self, evidence_pack: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": "TextTowerAdapterStub",
            "loaded_model": False,
            "logits": {},
            "concept_outputs": {},
            "notes": ["placeholder_only"],
        }
