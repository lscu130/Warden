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
    rule_assessment: str,
    routing_hints: Dict[str, Any],
    risk_hints: Dict[str, Any],
    evidence_sufficiency: Dict[str, Any],
    reason_codes: List[str],
    evidence_ledger: List[Dict[str, Any]],
    routing: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    positive = _claims(evidence_ledger, {"supports"})
    limiting = _claims(evidence_ledger, {"limits"})
    conflicts = _claims(evidence_ledger, {"conflicts"})
    uncertainty = limiting + conflicts
    if "insufficient_evidence" in reason_codes and not any("insufficient" in item for item in uncertainty):
        uncertainty.append("evidence is insufficient for confident decision")

    status_parts = [
        f"rule_assessment={rule_assessment}",
        f"visible_text={evidence_sufficiency.get('visible_text_status')}",
        f"html_action={evidence_sufficiency.get('html_action_status')}",
    ]
    if risk_hints.get("action_surface_present"):
        status_parts.append("action_surface_present")
    if risk_hints.get("high_risk_candidate"):
        status_parts.append("high_risk_candidate_needs_model_judgment_or_review")
    summary = "Rule router produced routing diagnostics only: " + "; ".join(status_parts)

    routing_source = routing_hints or routing or {}
    routing_reasons = [key for key, value in routing_source.items() if key.startswith("need_") and value]
    routing_explanation = "No follow-up routing requested."
    if routing_reasons:
        routing_explanation = "Follow-up routing requested: " + ", ".join(routing_reasons)

    return {
        "type": "routing_diagnostic",
        "summary": summary,
        "positive_evidence": positive,
        "limiting_evidence": limiting,
        "uncertainty": uncertainty[:8],
        "routing_explanation": routing_explanation,
        "evidence_sufficiency_summary": dict(evidence_sufficiency),
        "reason_codes": list(reason_codes),
    }
