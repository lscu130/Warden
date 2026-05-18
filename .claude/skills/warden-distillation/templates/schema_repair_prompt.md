# SCHEMA_REPAIR_PROMPT_V0_3

## 中文版

### 摘要

这是 schema repair 模板。只能修复 JSON shape、缺失必需 key、类型和明显格式错误。不得改写语义，不得发明证据。

---

## English Version

> AI note: This English section is authoritative. The prompt below is the template body.

# Schema Repair Prompt

You repair Warden distillation JSON shape only.

Return JSON only. Do not reveal hidden chain-of-thought. Do not add new evidence. Do not change semantic content unless the caller explicitly instructs a semantic correction.

Required rules:

- Preserve the sample's semantic meaning.
- Preserve `needs_human_review` and `do_not_train_as_gold` if present.
- Preserve modality limitations.
- Preserve `weak labels are evidence`.
- Preserve `payload not observed`.
- Preserve `action_surface != risk_bearing_engagement`.
- Preserve `induced_high_risk_action` as compatibility / child concept only.
- Preserve `unknown relation is not malicious`.
- Preserve `rule_router_context` as context only.
- Preserve `rule_router is not a teacher label source`.
- Preserve Warden V1 formula: `Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)`.
- Preserve `RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming`.
- Preserve required formula concept groups: `manipulative_context`, `action_surface`, `risk_bearing_engagement`, `direct_high_risk_action`, `routed_high_risk_action`, `action_preparation`, `deceptive_funnel_priming`, `context_engagement_relation`, `url_claim_analysis`, `visible_impersonation_analysis`, `funnel_affordance_analysis`, `risk_outcome_axes`, `evidence_sufficiency`, and `formula_result`.
- Preserve compatibility concept groups when present: `claimed_identity_candidates`, `identity_claim`, `behavior_context`, `relation_judgments`, `evidence_state`, `threat_action_candidate`, and `decision_head_auxiliary_targets`.

Input:

```json
{
  "target_schema_version": "warden_distill_v0.3",
  "invalid_json_or_object": {{invalid_json_or_object}},
  "repair_notes": {{repair_notes}}
}
```

Output JSON:

```json
{
  "schema_version": "warden_distill_v0.3",
  "repair_metadata": {
    "repair_type": "json_shape_only",
    "semantic_content_changed": false,
    "fields_added_as_empty_defaults": [],
    "missing_required_concept_fields_repaired": []
  },
  "repaired_object": {}
}
```
