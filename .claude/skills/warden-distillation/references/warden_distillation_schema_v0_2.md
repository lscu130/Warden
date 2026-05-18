# WARDEN_DISTILLATION_SCHEMA_V0_2

## 中文版

### 摘要

`warden_distill_v0.2` 是 historical / compatibility reference。当前默认 distillation semantic contract 是 V0.3 / `warden_distill_v0.3_mock`。本文件不得作为当前默认输出合同，不替代 Warden 既有 manifest、label、runtime result 或 trace schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Schema V0.2

## 1. Status

Historical / compatibility status:

```text
V0.2 is not the current default distillation semantic contract.
Current default: Warden Distillation V0.3 / warden_distill_v0.3_mock.
```

Schema name:

```text
warden_distill_v0.2
```

This is a historical / compatibility draft distillation-output schema. It is not the current default contract, not official runtime schema, not a manifest schema, not a label schema, and not a frozen training schema.

Current V0.3 formula:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

Current V0.3 mock records should use `formula_semantics` and `formula_concepts` with `manipulative_context`, `action_surface`, `risk_bearing_engagement`, `context_engagement_relation`, `url_claim_analysis`, `visible_impersonation_analysis`, `funnel_affordance_analysis`, `risk_outcome_axes`, `evidence_sufficiency`, and `formula_result`. `induced_high_risk_action` is compatibility / child concept only.

## 2. Top-Level Shape

```json
{
  "schema_version": "warden_distill_v0.2",
  "sample_id": "string",
  "teacher_metadata": {},
  "input_modalities": {},
  "observed_evidence_summary": {},
  "rule_router_context": {},
  "claimed_identity_candidates": [],
  "text_semantic_concepts": {
    "identity_claim": {},
    "action_surface": {},
    "behavior_context": {},
    "relation_judgments": {},
    "evidence_state": {},
    "threat_action_candidate": {},
    "concept_level_evaluation_readiness": {}
  },
  "vision_evidence_observations": {},
  "decision_head_auxiliary_targets": {},
  "quality_control": {},
  "human_review": {}
}
```

## 3. Field Rules

### `teacher_metadata`

Required draft fields:

- `teacher_model`
- `teacher_role`
- `teacher_run_id`
- `fallback_used`
- `fallback_reason`
- `source_split`
- `created_at`

### `input_modalities`

Required draft fields:

- `url_json_available`
- `visible_text_available`
- `html_summary_available`
- `forms_json_available`
- `net_summary_available`
- `screenshot_available`
- `image_input_passed_to_teacher`
- `ocr_text_available`
- `yolo_observations_available`

### `observed_evidence_summary`

Summarize only observed evidence. Do not invent evidence.

Required principle:

```text
payload not observed != benign
weak labels are evidence, not gold labels
```

### `rule_router_context`

Router context must be diagnostic only.

Required statement:

```text
rule_router outputs are routing / evidence sufficiency diagnostics only.
They are not gold labels, not teacher labels, and not final model judgments.
```

### `text_semantic_concepts`

Required groups:

- `claimed_identity_candidates`
- `identity_claim`
- `action_surface`
- `behavior_context`
- `relation_judgments`
- `evidence_state`
- `threat_action_candidate`
- `concept_level_evaluation_readiness`

Required phrase:

```text
action surface is not automatically threat action
unknown relation is not malicious
```

`claimed_identity_candidates` are evidence candidates only. Brand-library matching is optional enhancement, not the primary path.

### `vision_evidence_observations`

Vision observations are evidence only. A teacher may describe screenshot-visible observations only when image input is actually passed.

Text-only fallback outputs must set:

```json
{
  "fallback_modality_loss": true
}
```

when visual input was needed but unavailable.

### `decision_head_auxiliary_targets`

Draft advisory fields:

- `final_label_advisory`
- `malicious_basis_advisory`
- `payload_observed_advisory`
- `page_role_advisory`
- `risk_score_advisory`
- `confidence_advisory`
- `do_not_train_as_gold`

These are advisory distillation targets, not gold labels. They must not override human labels. They must not be generated for val/test as training targets. `do_not_train_as_gold` must remain `true` for mock and pilot outputs.

### `quality_control`

Required flags:

- `needs_human_review`
- `do_not_train_as_gold`
- `teacher_disagrees_with_human_label`
- `teacher_confidence_low`
- `fallback_modality_loss`
- `visual_text_conflict`
- `rule_router_teacher_conflict`
- `evidence_incomplete`
- `possible_cloak_or_gate`

### `human_review`

Required draft fields:

- `review_priority`
- `review_reasons`
- `short_packet`
- `evidence_ids`
- `suggested_next_action`

## 4. Split Policy

Formal distillation waits for final benign + malicious manifests to be frozen and runs on train split by default.

Val/test teacher outputs are diagnostics only and must not become training targets, prompt tuning input, threshold selection input, or model selection input.

Pilot outputs before final dataset freeze must set:

```json
{
  "do_not_train_as_gold": true
}
```
