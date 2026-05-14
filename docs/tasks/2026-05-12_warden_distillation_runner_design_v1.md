# TASK_20260512_WARDEN_DISTILLATION_RUNNER_DESIGN_V1

## 中文版

### 摘要

本任务用于设计 Warden 蒸馏 runner 的工程合同。交付只包含文档和 handoff，不实现生产 runner，不调用 MiMo / DeepSeek / OpenAI / Claude 或任何外部模型 API，不运行 teacher distillation，不生成 teacher labels，不修改数据、标签、manifest、split、训练、推理、runtime schema 或 CLI。

设计必须对齐当前 L1：`rule_router` 只做路由和证据充分性诊断；`text_semantic_concepts` 是主要蒸馏目标；`vision_evidence` 只记录 OCR / YOLO 证据观察；`decision_head_auxiliary_targets` 是未来 Decision Head advisory targets，不能覆盖人工 gold label。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260512-WARDEN-DISTILLATION-RUNNER-DESIGN-V1
- Task Title: Design Warden Distillation Runner Contract V1
- Owner Role: Codex executor, GPT reviewer, human final acceptor
- Priority: P0
- Status: TODO
- Related Module: Distillation / Labeling / Data Quality / Runner Design
- Related Issue / ADR / Doc: `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`, `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`, `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`, `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- Created At: 2026-05-12
- Requested By: 佶
- Karpathy Guardrails Required: YES

Use this template for any non-trivial engineering task in Warden.

## 1. Background

Warden has a V0.2 distillation prompt / Skill package aligned with the current L1 draft structure: `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`. The next step is to freeze a runner design contract before any implementation work begins. This task defines the future runner's CLI, API shape, input evidence pack, output JSONL layout, validation, repair, resume, split policy, review queue, logging, and pilot strategy.

This is a design-only task.

## 2. Goal

Create a bilingual, repository-ready runner design specification for future Warden distillation. The design must let a later implementation task build the runner without re-deciding architecture, split safety, schema repair boundaries, teacher routing, fallback modality policy, review queue logic, or validation expectations.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`

Optional file allowed only if necessary:

- `docs/distillation/README.md`

This task is allowed to define draft future contracts for:

- runner CLI;
- internal Python API;
- input manifest handling;
- evidence pack construction;
- teacher routing and fallback logging;
- JSONL output layout;
- schema validation and schema repair;
- train-only official distillation;
- diagnostic-only val/test handling;
- review queue generation;
- resume and idempotency;
- logging and audit;
- pilot stages.

## 4. Scope Out

This task must NOT do the following:

- Do not implement the production distillation runner.
- Do not call MiMo, DeepSeek, OpenAI, Claude, or any other model API.
- Do not run teacher distillation.
- Do not create generated teacher labels.
- Do not modify dataset files, manifest files, labels, split files, or sample directories.
- Do not modify training, inference, capture, crawler, or labeling code.
- Do not modify official Warden runtime schema or L1 output schema.
- Do not add third-party dependencies.
- Do not freeze `warden_distill_v0.2` as production schema.
- Do not use val/test teacher outputs for training, prompt tuning, threshold selection, model selection, or acceptance metrics.

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_DISTILLATION_RUNNER_DESIGN_V1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none; data artifacts must not be read or changed for this design-only task.

### Prior Handoff

- `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`

### Missing Inputs

- final frozen benign + malicious dataset manifests;
- exact production teacher endpoints and credentials;
- exact production runner storage root;
- empirical teacher pilot results.

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`

Output format requirements:

- Markdown documents must be bilingual: Chinese summary first, English authoritative section second.
- The runner design must be marked as design contract / draft.
- The handoff must record actual validation results.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.
- Keep `warden_distill_v0.2` as a draft distillation-output schema.
- Keep `rule_router` as evidence / routing diagnostics only.
- Keep official distillation train-only by default.
- Keep val/test teacher outputs diagnostic-only.

Task-specific constraints:

- Future runner design must include CLI and Python API shape.
- Future runner design must include evidence pack and prompt-packet rules.
- Future runner design must include JSONL output, schema validation, schema repair, resume, review queue, logging, and audit requirements.
- Future runner design must document DeepSeek-V4 fallback modality limits.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden manifests, labels, samples, split files, runtime outputs, and CLIs;
- current training, inference, capture, crawler, and labeling code;
- official runtime result / trace schema.

Schema / field constraints:

- Schema changed allowed: NO for existing schemas.
- New draft runner output schema allowed: documentation only.
- `warden_distill_v0.2` remains draft and unfrozen.

CLI / output compatibility constraints:

- No existing CLI command may be edited.
- The future CLI described in the design is not implemented by this task.

Downstream consumers to watch:

- future production distillation runner;
- future train-split teacher output consumers;
- future review queue tooling;
- future Decision Head training tasks.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- current L1 structure;
- current `warden_distill_v0.2` schema and prompt policy;
- Warden workflow, task, and handoff structure;
- previous distillation realignment validation and caveats.

Allowed evidence sources:

- current task document;
- Warden repo docs and handoffs;
- current V0.2 distillation docs and Skill;
- current L1 Decision Head contract.

Missing-evidence behavior:

- Do not invent production endpoint details.
- Mark future implementation details as draft design only.
- Do not claim model behavior or prompt quality has been validated.

### 9.1 Counter-Review Requirements

Current proposed framing:

Create a runner design contract now, before implementing the production runner.

Hidden assumptions to check:

- A design document can freeze safety policy without implementing code.
- `warden_distill_v0.2` is sufficient as a draft target reference.
- Split contamination can be prevented by runner contract and later implementation validation.

Failure modes to consider:

- design accidentally implies production schema freeze;
- val/test teacher outputs become training targets;
- router diagnostics become teacher labels;
- schema repair invents evidence;
- text-only fallback claims visual inspection;
- resume overwrites successful JSONL records.

Alternative routes to compare:

- implement runner immediately;
- keep only prompt docs without runner design;
- create a focused design contract.

Decision rule:

- Accept the focused design contract if all safety and split-policy requirements can be documented without code changes.
- Stop and escalate if implementation, schema freeze, API calls, or data changes become necessary.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- The optional `docs/distillation/README.md` is unnecessary unless cross-linking becomes required.
- This task is design-only and no code should be created.

Simplicity boundary:

- Add the three required Markdown files only.

Surgical change boundary:

- Every touched file must be one of the three required scope-in paths.

Goal-driven verification loop:

- Task doc checker -> verifies task artifact shape.
- Handoff checker -> verifies delivery artifact shape.
- Required-term grep -> verifies design contains required safety and runner terms.
- Targeted status -> verifies touched paths stay in scope.

## 10. Acceptance Criteria

This task is complete only if:

- [ ] The runner design document exists.
- [ ] The task doc exists.
- [ ] The handoff exists.
- [ ] The design is bilingual with Chinese summary first and English authoritative section second.
- [ ] The design aligns with current L1 structure.
- [ ] The design explicitly says rule-router outputs are evidence / routing diagnostics, not teacher labels or final labels.
- [ ] The design treats `text_semantic_concepts` as the primary distillation target area.
- [ ] The design treats `vision_evidence` as evidence observations only.
- [ ] The design treats `decision_head_auxiliary_targets` as advisory and non-gold.
- [ ] The design enforces train-only official distillation.
- [ ] The design defines diagnostic-only val/test policy.
- [ ] The design defines JSONL outputs, schema validation, schema repair, resume, review queue, and logging.
- [ ] The design documents DeepSeek-V4 fallback modality limits.
- [ ] No production runner was implemented.
- [ ] No external model API was called.
- [ ] No data, labels, manifest, split, code runtime, official schema, or CLI behavior was changed.

## 11. Validation Checklist

Minimum validation expected:

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md
rg -n "warden_distill_v0.2|rule_router|text_semantic_concepts|vision_evidence|decision_head|train split|diagnostic_only|do_not_train_as_gold|needs_human_review|resume|JSONL|schema repair|fallback_reason|DeepSeek-V4 fallback|payload not observed|weak labels are evidence" docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md
```

Scope check:

```bash
git status --short --untracked-files=all -- docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md
```

## 12. Stop Rules

Stop and report completion when:

- all scoped docs are created;
- validation passes or failed checks are explained;
- handoff is written;
- no out-of-scope files are touched.

Stop and escalate if:

- implementing runner code becomes necessary;
- modifying existing schema, labels, split, runtime, or training logic becomes necessary;
- teacher API access is required for correctness;
- the design cannot align with current L1 structure.

## 13. Handoff Requirements

The handoff must include:

- files created / edited;
- evidence / retrieval performed;
- validation commands and results;
- compatibility impact;
- confirmation that no runner, API call, teacher labels, data mutation, schema freeze, training change, runtime change, or CLI change happened;
- risks and next steps.
