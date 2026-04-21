# Gambling low-cost toto/togel host recovery task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务继续 `gambling` 的低成本 recall recovery。
- 本任务只允许使用 `host / url / page_title / visible_text` 这类低成本证据。
- 本任务不允许引入完整 HTML 扫描、OCR、截图语义、重 DOM 解析。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-15-GAMBLING-LOW-COST-TOTO-TOGEL-HOST-RECOVERY`
- 任务标题：`补 toto/togel host 的低成本 gambling recovery`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`
- 创建日期：`2026-04-15`
- 提出人：`用户`

## 背景

当前 `gambling` 低成本 recovery 已经补了：

- explainable score fallback
- `score=7 + domain_hint` 的窄 recovery
- `1xbet / 1xbt` landing recovery
- 印尼系 multilingual title-token recovery

剩余 miss 里仍然有一批 `toto/togel` host 模式，属于低成本结构证据，符合 `L0` 定位。

## 目标

分析当前剩余 miss 中 `toto/togel` host 模式的可分性，只在有足够 specificity 时，增加一个极窄的低成本 recovery，继续回收应当在 `L0` 完成的博彩页，同时控制 benign 回弹。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

This task is allowed to change:

- gambling-specific low-cost host recovery logic
- gambling-specific explainability reason codes if needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- add heavy HTML parsing to `L0`
- add OCR, screenshot semantics, or heavy DOM parsing
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
- current full `gambling` pool

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized summary of `toto/togel` host miss patterns
- one minimal low-cost patch if justified by evidence
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

- only use low-cost evidence types
- avoid broad host-token expansion
- validate against the same reproducible benign baseline

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

- isolate `toto/togel` host misses first
- compare them against benign controls before patching
- prefer a narrow recovery clause over broad token expansion

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

- [x] `toto/togel` host miss patterns are categorized
- [x] any new recovery rule uses only low-cost signals
- [x] ordinary-benign increase stays tightly controlled on the reproducible baseline

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
# quantify ordinary-benign 800 and current gambling pool
PY
```

Expected evidence to capture:

- `toto/togel` host pattern summary
- before/after ordinary-benign and gambling hit counts

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

- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-15-GAMBLING-LOW-COST-TOTO-TOGEL-HOST-RECOVERY`
- Task Title: `Recover gambling misses using low-cost toto/togel host patterns`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `TODO`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`
- Created At: `2026-04-15`
- Requested By: `User`

Use this task to continue low-cost gambling recall recovery through narrow `toto/togel` host patterns only, while keeping benign regression tightly controlled.

## 1. Background

Current low-cost `gambling` recovery already includes:

- explainable score fallback
- the narrow `score=7 + domain_hint` recovery
- the `1xbet / 1xbt` landing recovery
- the Indonesian multilingual title-token recovery

The remaining miss pool still contains a set of `toto/togel` host patterns that are structurally low-cost and still fit `L0`.

## 2. Goal

Analyze the remaining `toto/togel` host patterns in the current miss pool and, only if specificity is good enough, add one extremely narrow low-cost recovery that keeps more gambling pages in `L0` while controlling benign regression.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

This task is allowed to change:

- gambling-specific low-cost host recovery logic
- gambling-specific explainability reason codes if needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- add heavy HTML parsing to `L0`
- add OCR, screenshot semantics, or heavy DOM parsing
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
- current full `gambling` pool

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized summary of `toto/togel` host miss patterns
- one minimal low-cost patch if justified by evidence
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

- only use low-cost evidence types
- avoid broad host-token expansion
- validate against the same reproducible benign baseline

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

- isolate `toto/togel` host misses first
- compare them against benign controls before patching
- prefer a narrow recovery clause over broad token expansion

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

- [ ] `toto/togel` host miss patterns are categorized
- [ ] any new recovery rule uses only low-cost signals
- [ ] ordinary-benign increase stays tightly controlled on the reproducible baseline

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
# quantify ordinary-benign 800 and the current gambling pool
PY
```

Expected evidence to capture:

- `toto/togel` host pattern summary
- before/after ordinary-benign and gambling hit counts

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

- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

## 13. Open Questions / Blocking Issues

- `none`
