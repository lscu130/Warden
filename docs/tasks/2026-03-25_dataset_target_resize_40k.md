# 2026-03-25_dataset_target_resize_40k

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次数据集目标从 `50K` 下调到 `40K` 的任务定义。
- 若涉及精确数字、文档路径、约束边界或验证口径，以英文版为准。

## 1. 背景

当前公开恶意来源约束比预期更紧，继续沿用 `50K` 总量规划已经不稳。
本任务的核心不是改脚本或改训练逻辑，而是把当前有效的配对数据目标明确冻结为：

- 常规 benign `20,000`
- malicious train-pool 目标 `20,000`

## 2. 目标

同步更新相关规划文档，让 Warden V1 当前有效的成对数据目标明确变成 `40K total`，并把这次下调写成现实约束驱动的规划决定，而不是方法论上的永久结论。

## 3. 范围

- 纳入：benign 采样策略文档、malicious 来源策略文档、对应 task / handoff
- 排除：capture、label、training 逻辑和任何 schema / CLI 改动

## English Version

# Task Metadata

- Task ID: WARDEN-DATASET-TARGET-RESIZE-40K-V1
- Task Title: Reduce the current V1 paired benign-malicious dataset target from 50K total to 40K total under public-source constraints
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / dataset planning docs
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The user decided to compress the current paired dataset planning target from 50K total samples to 40K total samples.
The reason is practical rather than methodological: under a public-source-only malicious baseline, continuing to plan around the larger target is not currently justified.
The new working target should therefore be:

- 20,000 regular benign samples
- 20,000 malicious train-pool target samples

This needs to be reflected in the relevant planning/specification docs without changing capture logic, labeling logic, or training logic.

---

## 2. Goal

Update the relevant dataset-planning documents so the active Warden V1 paired data target is 40K total rather than 50K total.
The docs should explicitly reflect that the target reduction is driven by public-source constraints on the malicious side, and that benign target sizing remains aligned with the current malicious target.

---

## 3. Scope In

This task is allowed to touch:

- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- dataset target numbers in planning/spec docs
- benign quota breakdown that depends on the paired target size
- textual rationale around public-source limitations

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture scripts
- do not change sample schema, label semantics, or train-pool logic
- do not change source-policy baseline away from OpenPhish Community + PhishTank
- do not invent new commercial-source dependencies

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`

### Code / Scripts

- none

### Data / Artifacts

- current operational conclusion in-thread: public malicious sources are limited, and the planned paired total should be reduced to 40K

### Prior Handoff

- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated benign sampling strategy doc with a 20K benign target and adjusted sub-quota split
- updated malicious source policy doc with a 20K malicious train-pool planning target
- a repo handoff documenting the target change and its rationale

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Keep the public malicious baseline fixed as OpenPhish Community + PhishTank.
- Make the target reduction explicit as a planning decision, not as a claim that 40K is universally optimal.
- Keep benign sizing aligned with the current malicious target.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- none

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none

Downstream consumers to watch:

- operators using the benign sampling strategy as a collection target
- operators using the malicious source policy as a planning baseline

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current benign and malicious planning docs.
2. Update the benign target from 25K to 20K and compress the quota split proportionally.
3. Add an explicit malicious train-pool planning target of 20K under the public-source baseline.
4. Add task/handoff continuity artifacts.
5. Run lightweight validation on the touched docs.

Task-specific execution notes:

- Keep the wording practical and constraint-driven.
- Make clear that raw malicious capture volume still needs to exceed the train-pool target because deduplication and reserve routing remain in effect.
- Avoid rewriting unrelated architecture or source-policy sections.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] benign planning target is updated from 25K to 20K
- [ ] benign sub-quota split is updated consistently
- [ ] malicious source policy explicitly states the current 20K train-pool planning target
- [ ] the 40K total paired target is clear from the combined docs
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] search for stale `25,000` benign targets in the touched doc
- [ ] search for new `20,000` target wording in both touched docs

Commands to run if applicable:

```bash
rg -n "25,000|20,000|40K|40,000|50K|50,000" docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md docs/tasks/2026-03-25_dataset_target_resize_40k.md docs/handoff/2026-03-25_dataset_target_resize_40k.md
```

Expected evidence to capture:

- benign target numbers updated consistently
- malicious target planning note added
- new task and handoff docs exist
