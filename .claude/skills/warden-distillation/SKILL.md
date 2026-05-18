---
name: warden-distillation
description: Warden distillation prompt and teacher-output workflow support. Use when working on Warden teacher distillation, prompt packs, teacher-label auditing, warden_distill_v0.3 mock/schema drafts, formula_concepts targets, rule_router_context legacy handling, vision evidence observations, Decision Head advisory targets, or human-review packets.
---

# Warden Distillation

## 中文版

### 摘要

使用本 Skill 协助 Warden Distillation V0.3 prompt、mock schema draft、teacher output 审核和 human-review packet。V0.3 是当前默认 distillation semantic contract。不得调用模型 API，不得运行真实 teacher batch，不得修改数据、标签、split、训练、推理或 production runtime schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

## Core Rules

Follow Warden repository rules first:

1. Read the active task document and scope boundaries before editing.
2. Treat V0.3 as the current default distillation semantic contract.
3. Use the Warden V1 formula: `Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)`.
4. Use `RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming`.
5. Treat `rule_router_context` as legacy optional context only; it is not a label source, teacher label source, or final judgment.
6. Keep `warden_distill_v0.3_mock` as mock-only, diagnostic-only, non-gold output. Keep `warden_distill_v0.2` as historical / compatibility reference only.
7. Do not override human gold labels with teacher advisory targets.
8. Do not use teacher outputs from val/test as training targets.
9. Do not disclose hidden chain-of-thought in generated prompts or teacher outputs.

Required phrases for prompt or schema work:

```text
weak labels are evidence
payload not observed
action_surface != risk_bearing_engagement
induced_high_risk_action is compatibility / child concept only
URL-only brand claim is not a V1 positive
visible impersonation without funnel affordance is not a strong positive
visible impersonation with funnel affordance may support DeceptiveFunnelPriming / RoutedHighRiskAction / ActionPreparation
unknown relation is not malicious
rule_router is not a teacher label source
manipulative_context
risk_bearing_engagement
context_engagement_relation
evidence_sufficiency
formula_result
DeepSeek-V4 fallback
needs_human_review
do_not_train_as_gold
```

## Allowed Work

You may assist with:

- Warden distillation workflow documentation.
- Prompt templates for primary teacher, judge teacher, DeepSeek-V4 fallback, schema repair, and human-review packet.
- Draft `warden_distill_v0.3_mock` output schema review.
- JSON shape and required-key checks.
- Human-review packet compression from evidence and teacher disagreements.
- No-network real-teacher adapter readiness placeholders and audit layout checks.

## Forbidden Work

Do not:

- implement or run a production distillation runner;
- call MiMo, DeepSeek, OpenAI, Claude, or any external model API;
- run teacher distillation batches;
- modify datasets, labels, manifests, train / val / test split, or samples;
- modify training, inference, capture, crawler, or labeling code;
- change existing Warden schema fields, output schema, label enums, or CLI commands;
- add third-party dependencies;
- claim empirical prompt validity without a pilot result.
- claim live-provider readiness, training-ingestion readiness, or provider budget approval.

## Resource Map

Load only what is needed:

- `references/warden_distillation_schema_v0_2.md`: historical / compatibility V0.2 reference only; do not use as the current default contract.
- `templates/primary_mllm_teacher_prompt.md`: full primary teacher prompt.
- `templates/judge_teacher_prompt.md`: judge / audit prompt.
- `templates/deepseek_v4_fallback_prompt.md`: text / metadata / judge / schema repair fallback prompt.
- `templates/schema_repair_prompt.md`: JSON shape repair prompt.
- `templates/human_review_packet_prompt.md`: manual review packet prompt.

## Workflow

1. Confirm the active task permits distillation prompt / Skill work.
2. Identify whether the request is workflow drafting, prompt drafting, schema review, teacher-output audit, or human-review packet generation.
3. Load the smallest relevant reference or template.
4. Preserve evidence priority:
   - screenshot / OCR text / visible_text;
   - URL, final_host, redirect_chain;
   - actionable HTML, forms, buttons, links, form actions;
   - net_summary / redirects / request destinations;
   - metadata and weak labels as evidence only.
5. Enforce split discipline:
   - official teacher distillation waits for frozen final benign + malicious manifests;
   - train split by default;
   - val/test teacher use is diagnostics only;
   - pilots set `do_not_train_as_gold = true`.
6. Return JSON-only output when generating or repairing teacher outputs.
7. Mark unsupported modality claims for review.

## Modality Rules

Vision evidence is evidence recovery only. OCR and YOLO observations may support later Decision Head inputs, but visual observations must not become final malicious / benign judgments.

DeepSeek-V4 fallback is allowed for text / metadata / judge / schema repair roles. It must not claim direct visual inspection unless the configured endpoint is verified to support image input and image input is actually passed.

CLIP / MobileCLIP, SNet, and SpecularNet-like routes are not Warden V1 default online L1 components.

## V0.3 Formula Contract

Default distillation output should expose:

```text
formula_semantics
formula_concepts.manipulative_context
formula_concepts.action_surface
formula_concepts.risk_bearing_engagement.direct_high_risk_action
formula_concepts.risk_bearing_engagement.routed_high_risk_action
formula_concepts.risk_bearing_engagement.action_preparation
formula_concepts.risk_bearing_engagement.deceptive_funnel_priming
formula_concepts.context_engagement_relation
formula_concepts.url_claim_analysis
formula_concepts.visible_impersonation_analysis
formula_concepts.funnel_affordance_analysis
formula_concepts.risk_outcome_axes
formula_concepts.evidence_sufficiency
formula_concepts.formula_result
teacher_provider
prompt_template_id
prompt_snapshot_path
raw_output_path
validation_status
adapter_readiness_status
```

The output must remain `diagnostic_only=true` and `do_not_train_as_gold=true` until a separate approved training-ingestion task says otherwise.

No-network adapter readiness may create placeholders such as `attempts.jsonl`, `validation_summaries.jsonl`, `prompt_snapshots/`, `raw_outputs/`, `repaired_outputs/`, and `adapter_readiness_report.md`. These artifacts must use `mock_only=true`, keep all real call counters at zero, and report `live_teacher_readiness = not_ready_for_live_teacher`.

## Output Discipline

When drafting or auditing output, require:

- concise evidence snippets;
- source-aware evidence references;
- no hidden chain-of-thought;
- no weak-label promotion;
- no advisory-label promotion;
- `needs_human_review`;
- `do_not_train_as_gold`;
- explicit modality limitations.
