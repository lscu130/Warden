# Gambling lure domain-hint score-7 recovery task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务只处理 `gambling` recall recovery 里最窄的一档剩余 miss：`score = 7` 且 `domain_hint = true`。
- 目标是最小化回收这批高特征博彩页，同时控制 benign 回弹。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-14-GAMBLING-LURE-DOMAIN-HINT-SCORE7-RECOVERY`
- 任务标题：`回收 score=7 且 domain_hint=true 的 gambling lure miss`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`
- 创建日期：`2026-04-14`
- 提出人：`用户`

## 背景

上一轮 `gambling lure recall recovery` 已把可复现基线从：

- `gambling`: `525 / 804 -> 534 / 804`
- `ordinary_benign`: `11 / 800 -> 12 / 800`

剩余 miss 已明显收缩，当前最值得继续追的一档是：

- `score = 7`
- `domain_hint = true`
- 当前仍未触发 `possible_gambling_lure`

这批样本通常已经具备明显博彩正文语义，但被 `editorial:-4` 压到阈值下方。

## 目标

只针对 `score = 7 且 domain_hint = true` 的剩余 miss 做一轮最小化 recovery tuning，优先回收应当在 `L0` 完成的高特征博彩页，同时把 ordinary-benign 回弹控制在极小范围内。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

This task is allowed to change:

- `possible_gambling_lure` internal recovery conditions
- gambling-specific explainability reason codes if necessary
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- broaden threshold tuning beyond the target bucket
- add dependencies
- change CLI

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- reproducible `ordinary_benign = 800` slice with sorted+seeded sampling
- full `gambling = 804` pool

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized list of the target `score=7 and domain_hint=true` misses
- one minimal code patch
- a focused before/after quantification
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

- only tune the target bucket
- preserve the current score explainability path
- validate against the same reproducible baseline

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

- isolate the exact target misses first
- inspect benign control pages that would also match any new condition
- prefer a narrow recovery clause over another broad threshold change

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

- [x] all target misses are explicitly identified
- [x] at least one target miss is recovered
- [x] ordinary-benign increase stays at or below `+1` on the reproducible baseline

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
# quantify ordinary-benign 800 and gambling 804 on the reproducible sorted+seeded baseline
PY
```

Expected evidence to capture:

- target-miss before/after examples
- ordinary-benign and gambling hit counts

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

- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-DOMAIN-HINT-SCORE7-RECOVERY`
- Task Title: `Recover score=7 and domain_hint=true gambling lure misses`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `TODO`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`
- Created At: `2026-04-14`
- Requested By: `User`

Use this task to recover the narrow remaining bucket of `gambling` lure misses where `score = 7` and `domain_hint = true`, while keeping ordinary-benign regression tightly controlled.

## 1. Background

The previous `gambling lure recall recovery` round improved the reproducible baseline from:

- `gambling`: `525 / 804 -> 534 / 804`
- `ordinary_benign`: `11 / 800 -> 12 / 800`

The remaining misses are now much narrower. The highest-value remaining bucket is:

- `score = 7`
- `domain_hint = true`
- still not triggering `possible_gambling_lure`

These pages typically already carry clear gambling body-text semantics but are pushed below threshold by `editorial:-4`.

## 2. Goal

Perform one minimal recovery tuning round targeting only the remaining `score = 7 and domain_hint = true` misses, prioritizing pages that should finish in `L0`, while keeping ordinary-benign regression extremely small.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

This task is allowed to change:

- internal recovery conditions for `possible_gambling_lure`
- gambling-specific explainability reason codes if necessary
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- broaden threshold tuning beyond the target bucket
- add dependencies
- change CLI

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- reproducible `ordinary_benign = 800` slice with sorted+seeded sampling
- full `gambling = 804` pool

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized list of the target `score=7 and domain_hint=true` misses
- one minimal code patch
- a focused before/after quantification
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

- only tune the target bucket
- preserve the current score explainability path
- validate against the same reproducible baseline

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

- isolate the exact target misses first
- inspect benign control pages that would also match any new condition
- prefer a narrow recovery clause over another broad threshold change

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

- [ ] all target misses are explicitly identified
- [ ] at least one target miss is recovered
- [ ] ordinary-benign increase stays at or below `+1` on the reproducible baseline

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
# quantify ordinary-benign 800 and gambling 804 on the reproducible sorted+seeded baseline
PY
```

Expected evidence to capture:

- target-miss before/after examples
- ordinary-benign and gambling hit counts

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

- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

## 13. Open Questions / Blocking Issues

- `none`
