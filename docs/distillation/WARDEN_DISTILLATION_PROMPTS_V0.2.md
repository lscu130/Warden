# WARDEN_DISTILLATION_PROMPTS_V0.2

## 中文版

### 摘要

本文档汇总 Warden 蒸馏 prompt pack V0.2。V0.2 已被 `WARDEN_DISTILLATION_PROMPTS_V0.3.md` supersede，用于历史和兼容参考；当前 Warden V1 formula-aligned prompt contract 以 V0.3 为准。所有 prompt 都必须输出 JSON，不输出 hidden chain-of-thought，只给短证据摘录。Prompt 必须明确：

- `rule_router` 只提供 `rule_router_context` / routing hints，不能作为 teacher label。
- `weak labels are evidence`。
- `payload not observed` 不能自动等同于 benign。
- `action surface is not automatically threat action`。
- 视觉输入缺失时不能声称看过截图像素。
- advisory targets 不覆盖人工 gold label。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Prompt Pack V0.2

Supersession note: V0.2 is superseded by `WARDEN_DISTILLATION_PROMPTS_V0.3.md` for current Warden V1 formula-aligned distillation. Keep this document as historical and compatibility context only.

## 1. Global Prompt Contract

All Warden distillation prompts must enforce:

- JSON-only output.
- No hidden chain-of-thought disclosure.
- Concise evidence quotes only.
- No unsupported visual claims.
- `weak labels are evidence`, never gold labels.
- `payload not observed` is not automatic benign.
- `action surface is not automatically threat action`.
- `unknown relation is not malicious`.
- `rule_router` is not a final label source.
- `rule_router is not a teacher label source`.
- Advisory labels do not override human gold labels.
- `needs_human_review` and `do_not_train_as_gold` flags are required.
- Threat adjudication semantics follow `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`.
- Text concept and relation-judgment targets follow `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`.
- Claimed identity extraction is the primary identity path; brand lists are optional enhancement only.
- `unknown` is not malicious.

The target schema is `warden_distill_v0.2`.

## 2. Shared Evidence Priority

Use this priority order:

```text
human-visible evidence:
  screenshot / OCR text / visible_text
URL/domain evidence:
  URL, final_host, redirect_chain
interaction evidence:
  actionable HTML, forms, input types, buttons, links, form actions
network evidence:
  net_summary / redirects / request destinations
metadata / weak labels:
  evidence only, never gold
```

## 3. Primary MLLM Teacher Prompt

Template file:

- `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`

Purpose:

- Produce the full `warden_distill_v0.2` JSON draft.
- Extract `text_semantic_concepts`.
- Record `vision_evidence_observations` only when image input is provided.
- Produce Decision Head auxiliary targets as advisory signals.

Required output keys:

- `schema_version`
- `sample_id`
- `teacher_metadata`
- `input_modalities`
- `observed_evidence_summary`
- `rule_router_context`
- `text_semantic_concepts`
- `claimed_identity_candidates`
- `relation_judgments`
- `evidence_state`
- `threat_action_candidate`
- `vision_evidence_observations`
- `decision_head_auxiliary_targets`
- `quality_control`
- `human_review`

## 4. Judge Teacher Prompt

Template file:

- `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`

Purpose:

- Compare teacher output, raw evidence, optional human label, and optional `rule_router_context`.
- Identify schema drift, unsupported visual claims, rule-router misuse, weak-label overreach, advisory-label overreach, and split-policy violations.
- Output repair or human-review recommendations without chain-of-thought.

## 5. DeepSeek-V4 Fallback Prompt

Template file:

- `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`

Purpose:

- Provide fallback for text / metadata / judge / schema repair roles.
- Support JSON-only output.
- Explicitly include modality limits.

Required modality rule:

```text
DeepSeek-V4 fallback must not claim direct visual inspection unless the configured endpoint is verified to support image input and image input is actually passed.
```

## 6. Schema Repair Prompt

Template file:

- `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`

Purpose:

- Repair JSON shape only.
- Preserve semantic content.
- Do not invent evidence, labels, or visual observations.

## 7. Human Review Packet Prompt

Template file:

- `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`

Purpose:

- Compress raw evidence, teacher outputs, conflicts, low-confidence findings, and QC flags for manual review.
- Preserve short evidence snippets and provenance.
- Avoid turning teacher advisory targets into gold labels.

## 8. Required QC Flags

Every prompt that emits an assessment must include:

```text
needs_human_review
do_not_train_as_gold
teacher_disagrees_with_human_label
teacher_confidence_low
fallback_modality_loss
visual_text_conflict
rule_router_teacher_conflict
evidence_incomplete
possible_cloak_or_gate
```

## 9. Split Discipline

Formal teacher outputs for training must be generated only after final benign + malicious manifests are frozen and, by default, only for the train split.

Val/test teacher outputs are diagnostics only. They must not be used for training targets, prompt tuning, threshold selection, or model selection.

Pilot outputs before final dataset freeze must set:

```json
{
  "do_not_train_as_gold": true
}
```

## 10. Template Inventory

- Primary MLLM teacher prompt: full `warden_distill_v0.2` output.
- Judge teacher prompt: audit and review recommendations.
- DeepSeek-V4 fallback prompt: text / metadata / judge / schema repair fallback with modality limits.
- Schema repair prompt: JSON shape repair only.
- Human review packet prompt: fast manual-review packet.

All templates must keep concept-level evaluation readiness metadata when repairing, auditing, or compressing teacher output. That metadata is readiness evidence only and must not be promoted to a gold label.
