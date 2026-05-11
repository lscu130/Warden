"""Deterministic explanation rendering from evidence ledger and reason codes."""

from __future__ import annotations

from typing import Any, Dict, List


def _claims(entries: List[Dict[str, Any]], stances: set[str], limit: int = 5) -> List[str]:
    output: List[str] = []
    for entry in entries:
        if str(entry.get("stance")) not in stances:
            continue
        claim = str(entry.get("claim") or "").strip()
        value = entry.get("value")
        if value not in (None, "", [], {}):
            claim = f"{claim}: {value}"
        if claim:
            output.append(claim)
        if len(output) >= limit:
            break
    return output


def render_explanation(
    *,
    label: str,
    malicious_basis: str,
    risk_axes: List[str],
    reason_codes: List[str],
    evidence_ledger: List[Dict[str, Any]],
    routing: Dict[str, Any],
) -> Dict[str, Any]:
    positive = _claims(evidence_ledger, {"supports"})
    limiting = _claims(evidence_ledger, {"limits"})
    conflicts = _claims(evidence_ledger, {"conflicts"})
    uncertainty = limiting + conflicts
    if "insufficient_evidence" in reason_codes and not any("insufficient" in item for item in uncertainty):
        uncertainty.append("evidence is insufficient for confident decision")

    if positive:
        summary = f"L1 draft label is {label} based on {malicious_basis}; top evidence: {positive[0]}"
    else:
        summary = f"L1 draft label is {label} based on {malicious_basis}; no positive evidence was recorded"

    routing_reasons = [key for key, value in routing.items() if key.startswith("need_") and value]
    routing_explanation = "No follow-up routing requested."
    if routing_reasons:
        routing_explanation = "Follow-up routing requested: " + ", ".join(routing_reasons)

    return {
        "summary": summary,
        "positive_evidence": positive,
        "limiting_evidence": limiting,
        "uncertainty": uncertainty[:8],
        "routing_explanation": routing_explanation,
        "risk_axes": list(risk_axes),
        "reason_codes": list(reason_codes),
    }
