# Gambling lure recall recovery task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于在当前 explainable weighted score 基线之上，继续回收高特征博彩页的 `possible_gambling_lure`。
- 重点是看 true recovery 样本、接近阈值的博彩页，以及当前仍未命中的高分页。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-14-GAMBLING-LURE-RECALL-RECOVERY`
- 任务标题：`基于 explainable score 回收 gambling lure recall`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- 创建日期：`2026-04-14`
- 提出人：`用户`

## 背景

当前 `gambling` specialized detector 已新增 explainable weighted score。当前验证基线是：

- `ordinary_benign`: `possible_gambling_lure = 11 / 800`
- `gambling`: `possible_gambling_lure = 513 / 804`
- true `gambling_weighted_score_recovery = 12 / 804`

这说明 score 已经能补回一小批高特征博彩页，但还有一批高特征博彩页仍停在阈值附近，或者仍被过严的组合条件挡住。用户当前目标是继续把高特征博彩页压在 `L0` 完成，不把负担推给 `L1`。

## 目标

在不明显拉高 ordinary-benign 误触发的前提下，基于当前 score、true recovery 样本和接近阈值的博彩 miss 样本，做一轮最小化的 recall recovery tuning，优先回收应当留在 `L0` 的高特征博彩页。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing

This task is allowed to change:

- `possible_gambling_lure` internal trigger logic
- gambling score thresholds or score-guided fallback details
- gambling-specific explainability reason codes if needed
- necessary task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify the `adult` or `gate` specialized contract
- redesign `possible_bonus_or_betting_induction`
- add dependencies
- change CLI
- push heavy semantic reasoning into `L0`
- broaden scope into full mixed-batch regression cleanup

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\gambling`
- current weighted-score quantification outputs from this thread

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized list of score-near-threshold gambling misses
- one minimal recall-recovery patch
- a focused validation summary on ordinary-benign and gambling pools
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

- tune from real miss samples, not from intuition alone
- preserve the current explainability path
- keep the recovery logic low-cost and L0-safe

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `evt_v1.2` structure

Schema / field constraints:

- Schema changed allowed: `YES`, additive only if necessary
- If yes, required compatibility plan: `any new explainability output must remain optional and additive`
- Frozen field names involved: `possible_gambling_lure`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream gambling trigger-rate statistics

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- mine the true-recovery set and the `score in [7, 9]` gambling misses first
- prefer threshold and evidence-combination tuning over adding many new keywords
- validate against the same `ordinary_benign = 800` and `gambling = 804` pools for comparability

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

- [x] current gambling miss patterns near the score threshold are categorized
- [x] `possible_gambling_lure` on the gambling pool improves on the reproducible baseline
- [x] `possible_gambling_lure` on the ordinary-benign pool stays at or below `15 / 800`

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# quantify ordinary-benign 800 and gambling 804 with fixed seed 20260414
PY
```

Expected evidence to capture:

- updated ordinary-benign vs gambling hit counts
- representative recovered and still-missed sample list

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

- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-RECALL-RECOVERY`
- Task Title: `Recover gambling lure recall using the explainable score baseline`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `TODO`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- Created At: `2026-04-14`
- Requested By: `User`

Use this task to recover `possible_gambling_lure` recall for high-feature gambling pages using the current explainable-score baseline, while preventing material regression on ordinary-benign pages.

## 1. Background

The current `gambling` specialized detector now includes an explainable weighted score. The current validated baseline is:

- `ordinary_benign`: `possible_gambling_lure = 11 / 800`
- `gambling`: `possible_gambling_lure = 513 / 804`
- true `gambling_weighted_score_recovery = 12 / 804`

This shows that the score already recovers a small set of high-feature gambling pages, but another set of high-feature gambling pages still sits near the threshold or remains blocked by conservative boolean combinations. The current user goal is to keep more high-feature gambling pages completed in `L0` instead of pushing them to `L1`.

## 2. Goal

Using the current score outputs, the true-recovery set, and near-threshold gambling misses, perform one minimal recall-recovery tuning round that recovers more high-feature gambling pages that should stay in `L0`, without materially raising ordinary-benign false positives.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing

This task is allowed to change:

- internal `possible_gambling_lure` trigger logic
- gambling score thresholds or score-guided fallback details
- gambling-specific explainability reason codes if needed
- necessary task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify the `adult` or `gate` specialized contract
- redesign `possible_bonus_or_betting_induction`
- add dependencies
- change CLI
- push heavy semantic reasoning into `L0`
- broaden scope into full mixed-batch regression cleanup

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\gambling`
- current weighted-score quantification outputs from this thread

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized list of score-near-threshold gambling misses
- one minimal recall-recovery patch
- a focused validation summary on ordinary-benign and gambling pools
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

- tune from real miss samples, not from intuition alone
- preserve the current explainability path
- keep the recovery logic low-cost and L0-safe

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `evt_v1.2` structure

Schema / field constraints:

- Schema changed allowed: `YES`, additive only if necessary
- If yes, required compatibility plan: `any new explainability output must remain optional and additive`
- Frozen field names involved: `possible_gambling_lure`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream gambling trigger-rate statistics

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- mine the true-recovery set and the `score in [7, 9]` gambling misses first
- prefer threshold and evidence-combination tuning over adding many new keywords
- validate against the same `ordinary_benign = 800` and `gambling = 804` pools for comparability

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

- [ ] current gambling miss patterns near the score threshold are categorized
- [ ] `possible_gambling_lure` on the gambling pool improves beyond `513 / 804`
- [ ] `possible_gambling_lure` on the ordinary-benign pool stays at or below `15 / 800`

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# quantify ordinary-benign 800 and gambling 804 with fixed seed 20260414
PY
```

Expected evidence to capture:

- updated ordinary-benign vs gambling hit counts
- representative recovered and still-missed sample list

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

- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

## 13. Open Questions / Blocking Issues

- `none`
