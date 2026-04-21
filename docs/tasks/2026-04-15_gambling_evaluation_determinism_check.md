# Gambling evaluation determinism check task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于检查并修复当前 `gambling` 评估统计的 determinism 问题。
- 重点不是继续调 recall，而是保证同一代码、同一数据、同一抽样规则下的结果稳定可复现。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-15-GAMBLING-EVALUATION-DETERMINISM-CHECK`
- 任务标题：`检查并修复 gambling evaluation determinism`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- 创建日期：`2026-04-15`
- 提出人：`用户`

## 背景

在本轮 `gambling` 规则调优过程中，已经多次观察到：

- 同一代码
- 同一 seed
- 看似相同的样本池

跑出来的总量统计会漂移。

这类问题会直接破坏：

- recall / precision 对比的可信度
- task 间前后结果的可审计性
- 后续 L0 调优的判断质量

## 目标

定位当前 `gambling` evaluation 漂移的根因，并在不改变业务逻辑目标的前提下，做最小修复，使同一代码、同一数据、同一抽样规则下的统计结果稳定一致。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

This task is allowed to change:

- evaluation-related determinism bugs inside the labeling script
- internal state handling if it causes cross-sample drift
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- continue gambling recall tuning unless required by the determinism fix
- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- add dependencies
- change CLI

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- reproducible `ordinary_benign = 800` slice with sorted+seeded sampling
- current full `gambling` pool

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a concrete determinism root-cause finding
- one minimal fix if the root cause is confirmed
- repeated-run validation showing stable counts
- a repo handoff document

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
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- prove the drift before fixing it
- keep the fix minimal and auditable
- do not mix determinism repair with unrelated recall tuning

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `evt_v1.2` structure

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream evaluation scripts relying on repeated stable counts

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reproduce the drift with repeated runs first
- inspect global mutable state and order-sensitive code paths
- validate by rerunning the same quantification multiple times

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] determinism root cause is explicitly identified or ruled out
- [ ] repeated-run counts are stable after the fix
- [ ] no gambling business-rule expansion was mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted repeated-run validation
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# run the same quantification multiple times and compare counts
PY
```

Expected evidence to capture:

- before-fix repeated-run drift
- after-fix repeated-run stability

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

Repo handoff path if one should be created:

- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-15-GAMBLING-EVALUATION-DETERMINISM-CHECK`
- Task Title: `Check and fix gambling evaluation determinism`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- Created At: `2026-04-15`
- Requested By: `User`

Use this task to identify and fix the current evaluation determinism problem in the gambling labeling flow, while keeping business logic scope unchanged.

## 1. Background

During the recent gambling tuning work, repeated observations showed that:

- the same code
- the same seed
- and seemingly the same sample pool

could still produce drifting aggregate counts.

That directly undermines:

- trustworthiness of recall / precision comparisons
- auditability of before/after task results
- the quality of subsequent L0 tuning decisions

## 2. Goal

Identify the current root cause of evaluation drift in the gambling labeling flow and, without changing the intended business logic scope, implement the smallest fix that makes the same code, same data, and same sampling rule produce stable repeated counts.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

This task is allowed to change:

- evaluation-related determinism bugs inside the labeling script
- internal state handling if it causes cross-sample drift
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- continue gambling recall tuning unless required by the determinism fix
- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- add dependencies
- change CLI

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- reproducible `ordinary_benign = 800` slice with sorted+seeded sampling
- current full `gambling` pool

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a concrete determinism root-cause finding
- one minimal fix if the root cause is confirmed
- repeated-run validation showing stable counts
- a repo handoff document

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
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- prove the drift before fixing it
- keep the fix minimal and auditable
- do not mix determinism repair with unrelated recall tuning

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `evt_v1.2` structure

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream evaluation scripts relying on repeated stable counts

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reproduce the drift with repeated runs first
- inspect global mutable state and order-sensitive code paths
- validate by rerunning the same quantification multiple times

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] determinism root cause is explicitly identified or ruled out
- [x] repeated-run counts are stable after the fix
- [x] no gambling business-rule expansion was mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted repeated-run validation
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# run the same quantification multiple times and compare counts
PY
```

Expected evidence to capture:

- before-fix repeated-run drift
- after-fix repeated-run stability

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

Repo handoff path if one should be created:

- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

## 13. Open Questions / Blocking Issues

- `none`
