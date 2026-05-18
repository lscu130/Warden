# WARDEN_DISTILLATION_WORKFLOW_V0.2

## 中文版

### 摘要

本文档定义 Warden 蒸馏工作流 V0.2。V0.2 已被 `WARDEN_DISTILLATION_WORKFLOW_V0.3.md` supersede，用于历史和兼容参考；当前 Warden V1 formula-aligned distillation 以 V0.3 为准。

关键约束：

- `rule_router` outputs are routing / evidence sufficiency diagnostics only. They are not gold labels, not teacher labels, and not final model judgments.
- `text_semantic_concepts` 是主要蒸馏目标：动作表面、行为上下文、关系一致性、业务/上下文合法性提示、风险轴、页面角色候选和路由建议。
- `vision_evidence` 只记录视觉观察和 OCR / YOLO 证据恢复，不输出最终恶意判断。
- `decision_head` 是未来最终裁决组件；本工作流只产生 advisory distillation targets。
- `payload not observed` 不能自动等同于 benign。
- `weak labels are evidence`，不得提升成人工 gold label。
- 正式蒸馏必须等待 benign + malicious 最终数据集 manifest 冻结，默认只对 train split 跑 teacher。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Workflow V0.2

## 1. Status And Supersession

This document defines the Warden distillation V0.2 workflow for prompt / Skill alignment with earlier Warden L1 semantics.

V0.2 is superseded by `WARDEN_DISTILLATION_WORKFLOW_V0.3.md` for current Warden V1 formula-aligned distillation. Keep this document as historical and compatibility context only.

V0.2 supersedes V0.1 for current Warden L1 semantics. Older V0.1 task or prompt files, if present, remain historical artifacts and must not be deleted by this task.

This document is documentation only. It does not implement a production runner, call model APIs, run teacher distillation, change schemas, change labels, move data, or alter training / inference code.

Distillation targets and prompts should follow `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md` for threat adjudication semantics. In particular, claimed identity extraction is the primary identity path, action surfaces are not threat actions by themselves, `unknown` is not malicious, and Decision Head auxiliary targets remain advisory.

Detailed L1 text concept and relation-judgment targets are defined in `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`. Teacher outputs should use that document for `claimed_identity_candidates`, `text_semantic_concepts`, `identity_domain_relation`, `business_legitimacy_hint`, evidence-state concepts, and threat-action candidate concepts.

## 2. L1-Aligned Distillation Targets

Warden L1 currently separates these draft components:

- `rule_router`
- `text_semantic_concepts`
- `vision_evidence`
- `decision_head`

Distillation V0.2 targets the following output groups:

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

The schema is a draft distillation-output schema. It is not official runtime schema and not a replacement for any existing Warden manifest, label, runtime result, or trace schema.

## 3. Rule Router Policy

Required statement:

```text
rule_router outputs are routing / evidence sufficiency diagnostics only.
They are not gold labels, not teacher labels, and not final model judgments.
```

When rule-router output is supplied to a teacher, it must be named `rule_router_context` or `routing_hints`.

Forbidden usage:

- no `rule_router` output may be converted into a gold label;
- no `rule_router` field may be treated as a final teacher label;
- no prompt may ask the teacher to accept a router candidate as truth;
- no benchmark may report router values as final malicious / benign accuracy.

## 4. Evidence Priority

Teacher prompts must preserve this evidence priority:

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

Required principles:

```text
payload not observed != benign
weak labels are evidence, not gold labels
action surface is not automatically threat action
unknown is not malicious
```

## 5. Text Semantic Concepts

Teacher outputs should produce structured targets for future text tower concept heads.

Required concept groups:

- `claimed_identity_candidates`
- `text_semantic_concepts.identity_claim`
- `text_semantic_concepts.action_surface`
- `text_semantic_concepts.behavior_context`
- `relation_judgments`
- `text_semantic_concepts.evidence_state`
- `text_semantic_concepts.threat_action_candidate`
- `text_semantic_concepts.concept_level_evaluation_readiness`
- `business_legitimacy_hint`
- `context_legitimacy`
- `risk_axes`
- `page_role_candidates`
- `routing_recommendations`

Action surfaces include login, signup, payment, wallet connect, download, support contact, PII collection, third-party redirect, OTP / MFA, seed phrase, private key, QR code, and account recovery surfaces.

Action surfaces are not final threat actions by themselves:

```text
action surface is not automatically threat action
```

Threat escalation requires additional context such as deceptive identity, manipulative narrative, abnormal destination, inconsistent business context, suspicious submission target, or inherently dangerous collection.

Required relation-judgment principle:

```text
unknown relation is not malicious
```

## 6. Vision Evidence Observations

Vision observations are evidence, not final labels.

Allowed future visual evidence roles:

- OCR recovers screenshot-visible text when DOM / visible text is missing, sparse, or image-rendered.
- YOLO / detector localizes UI evidence such as inputs, password fields, OTP fields, card fields, wallet buttons, download buttons, QR codes, captchas, popups, modals, and primary CTA buttons.

Prompt and workflow constraints:

- The teacher may describe screenshot-visible observations only when image input is actually provided.
- A text-only fallback must not claim it saw screenshot pixels.
- `vision_evidence_observations` must remain evidence for later structured reasoning.
- Visual observation must not become standalone malicious / benign classification.
- CLIP / MobileCLIP, SNet, and SpecularNet-like paths are not Warden V1 default online L1 components.
- CLIP / SNet / SpecularNet-like may be mentioned only as offline research, clustering, ablation, template discovery, or separately approved future optional work.

## 7. Decision Head Auxiliary Targets

Teacher output may include advisory targets for future Decision Head analysis:

```text
final_label_advisory
malicious_basis_advisory
payload_observed_advisory
page_role_advisory
risk_score_advisory
confidence_advisory
do_not_train_as_gold
```

Required interpretation:

```text
These are advisory distillation targets, not gold labels.
They must not override human labels.
They must not be generated for val/test as training targets.
```

Allowed future advisory label values should follow the L1 Decision Head draft contract when used:

- `final_label_advisory`: `benign`, `malicious`, `suspicious`, `unknown`
- `malicious_basis_advisory`: `no_malicious_evidence_observed`, `high_risk_behavior_observed`, `high_risk_action_observed`, `both_behavior_and_action_observed`, `insufficient_evidence`
- `payload_observed_advisory`: `true`, `false`, `unknown`

These remain advisory and draft.

Mock runner alignment:

- mock output must include `claimed_identity_candidates`;
- mock output must include the required `text_semantic_concepts` subgroups;
- mock output must include `decision_head_auxiliary_targets.do_not_train_as_gold=true`;
- mock audit/report output should expose missing required concept fields and concept-level readiness counts;
- mock output remains `diagnostic_only=true`, `do_not_train_as_gold=true`, `teacher_model=mock_teacher_v0`, and zero-call for external API / OCR / YOLO / CLIP.

## 8. Split Policy

Formal policy:

```text
Run official teacher distillation only after final benign + malicious dataset manifests are frozen.
Default: run teacher only on train split.
Val/test may be manually gold-labeled and may be teacher-audited for diagnostics only, but teacher outputs must not be used for training, prompt tuning, threshold selection, or model selection.
```

Pilot policy:

```text
Small prompt/schema pilot is allowed before final dataset freeze, but pilot outputs must be marked do_not_train_as_gold=true and must not be merged into final training labels.
```

## 9. Required Review And QC Flags

Every output must include these flags:

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

Set `needs_human_review = true` when evidence is incomplete, the teacher confidence is low, the teacher disagrees with a human label, rule-router context strongly conflicts with teacher observations, visual and text evidence conflict, or a fallback lost modalities needed for a reliable judgment.

Set `do_not_train_as_gold = true` for pilots, val/test diagnostics, malformed outputs, fallback modality loss, low confidence, missing required evidence, unresolved teacher / human disagreement, or any output produced before the final dataset freeze.

## 10. Model Routing And External Facts

Source-backed facts checked on 2026-05-12:

- Official MiMo website states that MiMo-V2.5 series models are available under Token Plan and that the ecosystem integration includes Claude Code.
- Official DeepSeek API docs list `deepseek-v4-flash` and `deepseek-v4-pro`, with JSON Output support.
- Official DeepSeek JSON Output docs describe `response_format: {"type": "json_object"}` and require the prompt to include the word `json` and an example.
- Official Claude Code docs describe project Skills under `.claude/skills/<skill-name>/SKILL.md` and YAML frontmatter for Skill configuration.

Unverified for production:

- exact local MiMo invocation method inside this repository;
- exact user endpoint for MiMo or DeepSeek;
- whether the configured DeepSeek-V4 endpoint supports image input.

DeepSeek-V4 fallback policy:

```text
DeepSeek-V4 fallback is allowed for text / metadata / judge / schema repair roles.
It must not claim direct visual inspection unless the configured endpoint is verified to support image input and image input is actually passed.
```

## 11. Prompt Roles

Primary multimodal teacher:

- use MiMo-V2.5 or another verified multimodal teacher when image input is actually available;
- produce the full `warden_distill_v0.2` JSON draft;
- separate observations from advisory targets.

Judge teacher:

- compare teacher output, raw evidence, human label if provided, and `rule_router_context`;
- output audit / repair / review recommendations;
- avoid chain-of-thought.

DeepSeek-V4 fallback:

- use for text / metadata / judge / schema repair unless image support is verified;
- mark `fallback_modality_loss = true` when visual information was required but unavailable.

Schema repair:

- repair JSON shape only;
- preserve semantic content unless the caller explicitly asks for a semantic correction.

Human review packet:

- compress evidence, conflicts, teacher disagreements, and QC flags for fast manual review.

## 12. Negative Calibration Example

Benign university or institutional homepages may include search forms, cookie banners, analytics, third-party resources, login links, or support pages. These action surfaces and weak crawler labels must not produce malicious targets by themselves.

The teacher should ask whether the action surface is connected to deceptive identity, abnormal destination, manipulative narrative, suspicious submission, or inconsistent business context.

## 13. Logging And Future Runner Requirements

A future runner should log:

- `sample_id`
- `source_manifest`
- `split`
- `teacher_model`
- `teacher_role`
- `teacher_metadata`
- `input_modalities`
- `fallback_reason`
- `schema_version`
- `needs_human_review`
- `do_not_train_as_gold`
- parse / schema validation status
- retry / repair count

This task does not implement that runner.

## 14. Stop Conditions

For this documentation task, stop after the workflow, prompt pack, Skill, schema reference, prompt templates, task doc, and handoff are generated and validated.

Do not continue into:

- production runner implementation;
- model API calls;
- pilot distillation;
- training code;
- data movement;
- schema freeze;
- label changes.
