<!-- operator: Codex; task: primary-benign-second-pass-policy; date: 2026-04-24 -->

# 中文摘要

## 任务元数据

- Task ID: `primary-benign-second-pass-policy-2026-04-24`
- Task Title: Freeze a primary-benign second-pass review policy
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Data / Labeling
- Related Issue / ADR / Doc: `docs/data/TRAINSET_V1.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`; `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`; `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`; `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- Created At: 2026-04-24
- Requested By: user

## 1. 背景

benign 数据已完成采集，并已完成第一轮粗分：`adult`、`gambling`、`gate`、`evasion` 已被先行分出。当前缺的是“剩余 `primary benign candidates` 的二筛口径”，即如何把看起来像 benign、但仍可能混入 threat-like 风险页、灰区页、内容残缺页和高混淆页的样本继续分流。

现有 data docs 已经冻结了大边界：

- `TrainSet V1 primary` 与 `gate / evasion auxiliary set` 的边界；
- `auto / rule / manual` 三层语义边界；
- `adult / gambling` 不作为第三个主 threat class，而应保留为独立 warning / scenario axis。

但仓库当前没有一份专门面向“remaining primary benign candidates second pass”的 active policy，导致后续让 Codex 或 Claude Code 执行二筛时，容易把 benign purity、内容 warning、threat judgment 和 auxiliary routing 混在一起。

## 2. 目标

在不改动现有顶层 TrainSet、auto/rule/manual、malicious taxonomy 合同的前提下，新增一份 repo 内 active bilingual policy，冻结 `primary benign candidates` 二筛的输入、输出桶、判定信号、人工复核条件和与现有 docs 的接口边界。该 policy 只负责 benign 二筛，不重写恶意 taxonomy，不重定义手工金标，不把 gate/evasion 并回 primary。

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

This task is allowed to change:

- documentation only
- active policy wording for primary-benign second-pass review
- task and handoff artifacts for this documentation change

## 4. Scope Out

This task must NOT do the following:

- do not modify code, scripts, schemas, or dataset directories
- do not redesign `TRAINSET_V1.md`, `GATA_EVASION_AUXILIARY_SET_V1.md`, or top-level malicious taxonomy
- do not promote weak labels into final truth or manual gold labels
- do not absorb `gate / evasion` into `TrainSet V1 primary`
- do not turn `adult / gambling` into a third main threat class parallel to `benign` and threat behavior classes

## 5. 输入

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`

### Code / Scripts

- none

### Data / Artifacts

- user-stated boundary: benign corpus already captured; first-pass buckets already split for `adult`, `gambling`, `gate`, `evasion`

### Prior Handoff

- none explicitly provided in-thread for this exact policy task

### Missing Inputs

- no repo-internal active benign second-pass policy exists yet

## 6. Required Outputs

This task should produce:

- a new active policy doc at `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- a repo task doc for this work
- a repo handoff doc for this work

## 7. 硬约束

- Preserve backward compatibility with current TrainSet / label-policy stack.
- Do not rename frozen fields or current active docs.
- Do not silently change output format or script defaults.
- Do not add dependencies.
- Keep this as a narrow documentation / policy freeze.
- Markdown outputs must be bilingual: Chinese summary first, full English second, with English authoritative.
- User-frozen boundary for this task:
  - `adult` and `gambling` are handled as high-risk content samples, not as the same thing as high-risk behavior samples.
  - true `malicious` means high-risk behavior samples.
  - `gate` / `evasion` remain auxiliary data and are not admitted into `TrainSet V1 primary`.

## 8. 接口 / Schema 约束

Public interfaces that must remain stable:

- `TrainSet V1 primary` meaning in `docs/data/TRAINSET_V1.md`
- `Gate / Evasion Auxiliary Set` meaning in `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `auto / rule / manual` role boundaries

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none; doc-only task

Downstream consumers to watch:

- future review-manifest generation
- future manual review queues
- future benign train-main admission decisions

## 9. 建议执行计划

Recommended order:

1. Read governing docs and current data-policy docs.
2. Freeze the user-requested boundary in the task doc.
3. Draft a narrow primary-benign second-pass policy.
4. Optionally ask Claude Code for bounded read-only structure review.
5. Finalize the doc with the smallest valid patch.
6. Run doc-level validation and produce handoff.

Task-specific execution notes:

- keep the policy focused on remaining `primary benign candidates`
- define second-pass outputs in routing terms rather than final truth claims
- explicitly separate benign purity, content warning, threat behavior, and auxiliary routing

## 10. 验收标准

This task is complete only if all items below are satisfied:

- [ ] goal is met
- [ ] scope-out items were not touched
- [ ] a new active benign second-pass policy doc exists in repo
- [ ] the policy preserves the current TrainSet / auxiliary / label-layer boundaries
- [ ] the policy clearly encodes the user-frozen boundary for `adult/gambling`, true `malicious`, and `gate/evasion`
- [ ] validation was run, or inability to run was explicitly stated
- [ ] handoff is provided

## 11. 验证清单

Minimum validation expected:

- [ ] content check against governing docs
- [ ] focused grep / spot-check for key terms and bucket names
- [ ] bilingual structure check
- [ ] repo file existence check for the new policy / task / handoff docs

Commands to run if applicable:

```bash
rg -n "primary benign|second pass|adult|gambling|gate|evasion|manual review|auxiliary" docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
Get-ChildItem docs/tasks/2026-04-24_primary_benign_second_pass_policy.md,docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md,docs/handoff/2026-04-24_primary_benign_second_pass_policy.md
```

Expected evidence to capture:

- key frozen bucket names
- clear statements for `adult/gambling`, `malicious`, and `gate/evasion` boundaries

## 12. Handoff 要求

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path:

- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

## 13. Open Questions / Blocking Issues

- Should later execution artifacts use `manual_review` vs `aux_only` as the default routing label for unresolved benign-like hard cases? For this task, keep the policy at documentation level and avoid freezing downstream JSON field names.

---

# English Version

# Task Metadata

- Task ID: `primary-benign-second-pass-policy-2026-04-24`
- Task Title: Freeze a primary-benign second-pass review policy
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Data / Labeling
- Related Issue / ADR / Doc: `docs/data/TRAINSET_V1.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`; `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`; `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`; `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- Created At: 2026-04-24
- Requested By: user

## 1. Background

The benign corpus has already been captured, and a first-pass rough split has already separated `adult`, `gambling`, `gate`, and `evasion`. The missing piece is a stable second-pass policy for the remaining `primary benign candidates`: samples that look benign enough to survive the first pass, but may still contain threat-like behavior, gray-zone signals, broken pages, or high-confusion surfaces.

The current data docs already freeze the large boundaries:

- the TrainSet V1 primary vs. gate/evasion auxiliary boundary;
- the `auto / rule / manual` semantic boundary;
- the rule that `adult / gambling` should remain a separate warning/scenario axis rather than becoming a third main threat class.

What is missing is a dedicated active policy for remaining-primary-benign second-pass review. Without that doc, future execution by Codex or Claude Code may mix together benign purity, content warning, threat judgment, and auxiliary routing.

## 2. Goal

Add a narrow active bilingual policy doc that freezes the inputs, output buckets, decision signals, manual-review triggers, and interface boundaries for second-pass review of `primary benign candidates`, without changing the existing top-level TrainSet, auto/rule/manual, or malicious-taxonomy contracts. This policy is only for benign second-pass review. It must not rewrite the malicious taxonomy, redefine human gold labels, or merge gate/evasion back into primary.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

This task is allowed to change:

- documentation only
- active policy wording for primary-benign second-pass review
- task and handoff artifacts for this documentation change

## 4. Scope Out

This task must NOT do the following:

- do not modify code, scripts, schemas, or dataset directories
- do not redesign `TRAINSET_V1.md`, `GATA_EVASION_AUXILIARY_SET_V1.md`, or the top-level malicious taxonomy
- do not promote weak labels into final truth or manual gold labels
- do not absorb `gate / evasion` into `TrainSet V1 primary`
- do not turn `adult / gambling` into a third main threat class parallel to `benign` and threat-behavior classes

## 5. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`

### Code / Scripts

- none

### Data / Artifacts

- user-stated boundary: the benign corpus is already captured; first-pass buckets already exist for `adult`, `gambling`, `gate`, and `evasion`

### Prior Handoff

- none explicitly provided in-thread for this exact policy task

### Missing Inputs

- no repo-internal active benign second-pass policy exists yet

## 6. Required Outputs

This task should produce:

- a new active policy doc at `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- a repo task doc for this work
- a repo handoff doc for this work

## 7. Hard Constraints

- Preserve backward compatibility with the current TrainSet / label-policy stack.
- Do not rename frozen fields or current active docs.
- Do not silently change output format or script defaults.
- Do not add dependencies.
- Keep this as a narrow documentation / policy freeze.
- Markdown outputs must be bilingual: Chinese summary first, full English second, with English authoritative.
- User-frozen boundary for this task:
  - `adult` and `gambling` are handled as high-risk content samples, not the same thing as high-risk behavior samples.
  - true `malicious` means high-risk behavior samples.
  - `gate / evasion` remain auxiliary data and are not admitted into `TrainSet V1 primary`.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- the `TrainSet V1 primary` meaning in `docs/data/TRAINSET_V1.md`
- the `Gate / Evasion Auxiliary Set` meaning in `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- the `auto / rule / manual` role boundaries

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none; doc-only task

Downstream consumers to watch:

- future review-manifest generation
- future manual-review queues
- future benign train-main admission decisions

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs and current data-policy docs.
2. Freeze the user-requested boundary in the task doc.
3. Draft a narrow primary-benign second-pass policy.
4. Optionally ask Claude Code for a bounded read-only structure review.
5. Finalize the doc with the smallest valid patch.
6. Run doc-level validation and produce handoff.

Task-specific execution notes:

- keep the policy focused on remaining `primary benign candidates`
- define second-pass outputs in routing terms rather than final-truth claims
- explicitly separate benign purity, content warning, threat behavior, and auxiliary routing

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] goal is met
- [ ] scope-out items were not touched
- [ ] a new active benign second-pass policy doc exists in repo
- [ ] the policy preserves the current TrainSet / auxiliary / label-layer boundaries
- [ ] the policy clearly encodes the user-frozen boundary for `adult/gambling`, true `malicious`, and `gate/evasion`
- [ ] validation was run, or inability to run was explicitly stated
- [ ] handoff is provided

## 11. Validation Checklist

Minimum validation expected:

- [ ] content check against governing docs
- [ ] focused grep / spot-check for key terms and bucket names
- [ ] bilingual structure check
- [ ] repo file existence check for the new policy / task / handoff docs

Commands to run if applicable:

```bash
rg -n "primary benign|second pass|adult|gambling|gate|evasion|manual review|auxiliary" docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
Get-ChildItem docs/tasks/2026-04-24_primary_benign_second_pass_policy.md,docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md,docs/handoff/2026-04-24_primary_benign_second_pass_policy.md
```

Expected evidence to capture:

- the frozen bucket names
- explicit statements for the `adult/gambling`, `malicious`, and `gate/evasion` boundaries

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path:

- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

## 13. Open Questions / Blocking Issues

- Should later execution artifacts use `manual_review` vs. `aux_only` as the default routing label for unresolved benign-like hard cases? For this task, keep the policy at documentation level and avoid freezing downstream JSON field names.
