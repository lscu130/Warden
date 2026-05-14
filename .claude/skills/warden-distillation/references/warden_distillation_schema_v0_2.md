# WARDEN_DISTILLATION_SCHEMA_V0_2

## 中文版

### 摘要

`warden_distill_v0.2` 是 draft distillation-output schema，只用于未来 teacher 输出、prompt pilot、QC 和 Decision Head 辅助目标设计。它不替代 Warden 既有 manifest、label、runtime result 或 trace schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Schema V0.2

## 1. Status

Schema name:

```text
warden_distill_v0.2
```

This is a draft distillation-output schema. It is not official runtime schema, not a manifest schema, not a label schema, and not a frozen training schema.

## 2. Top-Level Shape

```json
{
  "schema_version": "warden_distill_v0.2",
  "sample_id": "string",
  "teacher_metadata": {},
  "input_modalities": {},
  "observed_evidence_summary": {},
  "rule_router_context": {},
  "text_semantic_concepts": {},
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

- `action_surfaces`
- `behavior_contexts`
- `relation_consistency`
- `business_legitimacy`
- `context_legitimacy`
- `risk_axes`
- `page_role_candidates`
- `routing_recommendations`

Required phrase:

```text
action surface is not automatically threat action
```

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

These are advisory distillation targets, not gold labels. They must not override human labels. They must not be generated for val/test as training targets.

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
