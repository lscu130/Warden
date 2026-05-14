---
name: warden-distillation
description: Warden distillation prompt and teacher-output workflow support. Use when working on Warden teacher distillation, prompt packs, teacher-label auditing, warden_distill_v0.2 schema drafts, rule_router_context handling, text_semantic_concepts targets, vision_evidence observations, Decision Head auxiliary targets, or human-review packets.
---

# Warden Distillation

## 中文版

### 摘要

使用本 Skill 协助 Warden 蒸馏 prompt、schema draft、teacher output 审核和 human-review packet。只处理文档、prompt、schema reference 和审查建议。不得调用模型 API，不得运行 teacher batch，不得修改数据、标签、split、训练、推理或 runtime schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

## Core Rules

Follow Warden repository rules first:

1. Read the active task document and scope boundaries before editing.
2. Treat `rule_router` as routing / evidence-sufficiency diagnostics only.
3. Use `rule_router_context` or `routing_hints` when router output is included in teacher input.
4. Do not treat router output as gold label, teacher label, or final model judgment.
5. Keep `warden_distill_v0.2` as draft distillation-output schema only.
6. Do not override human gold labels with teacher advisory targets.
7. Do not use teacher outputs from val/test as training targets.
8. Do not disclose hidden chain-of-thought in generated prompts or teacher outputs.

Required phrases for prompt or schema work:

```text
weak labels are evidence
payload not observed
action surface is not automatically threat action
DeepSeek-V4 fallback
needs_human_review
do_not_train_as_gold
```

## Allowed Work

You may assist with:

- Warden distillation workflow documentation.
- Prompt templates for primary teacher, judge teacher, DeepSeek-V4 fallback, schema repair, and human-review packet.
- Draft `warden_distill_v0.2` output schema review.
- JSON shape and required-key checks.
- Human-review packet compression from evidence and teacher disagreements.

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

## Resource Map

Load only what is needed:

- `references/warden_distillation_schema_v0_2.md`: draft output schema and field rules.
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
