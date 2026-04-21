# Gambling score<4 low-cost evidence-gap mining task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务只处理 `gambling` 剩余 miss 中 `score < 4` 的 evidence gap。
- 本任务只允许挖和落低成本证据，不允许把重证据推进 `L0`。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-14-GAMBLING-SCORE-LT4-LOW-COST-EVIDENCE-GAP-MINING`
- 任务标题：`挖 score<4 的 gambling miss，并只补低成本 L0 证据`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- 创建日期：`2026-04-14`
- 提出人：`用户`

## 背景

当前 `gambling` recall 已连续做了几轮回收，剩余 miss 里最大头已经是 `score < 4`。这类页通常证据很弱，或者当前 `L0` 没拿到足够可用的低成本线索。

用户明确要求：

- `L0` 要保持特化目标的快速判断
- 不碰重证据
- 不把完整 HTML 扫描、OCR、截图语义推进 `L0`

## 目标

只针对 `score < 4` 的 `gambling` miss 做一轮 low-cost evidence-gap mining，并只在发现可解释、低成本、低误触发风险的信号时，做最小 patch，继续回收一小批应当留在 `L0` 的高特征博彩页。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

This task is allowed to change:

- gambling-specific low-cost feature extraction
- `possible_gambling_lure` low-cost recovery logic
- gambling-specific explainability reason codes if needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- read or scan large HTML payloads for new L0 logic
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
- full `gambling = 804` pool

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized summary of `score < 4` gambling misses
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
- do not introduce full-HTML scanning into `L0`
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

- mine `score < 4` misses first
- only consider low-cost evidence such as host, URL, page title, and existing visible-text patterns
- reject any candidate signal that would require heavy content parsing

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

- [x] `score < 4` misses are categorized by low-cost evidence gap
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
# quantify ordinary-benign 800 and gambling 804 on the reproducible sorted+seeded baseline
PY
```

Expected evidence to capture:

- low-cost miss categories
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

- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-14-GAMBLING-SCORE-LT4-LOW-COST-EVIDENCE-GAP-MINING`
- Task Title: `Mine score<4 gambling misses and add only low-cost L0 evidence`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `TODO`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- Created At: `2026-04-14`
- Requested By: `User`

Use this task to mine the remaining `score < 4` gambling misses and recover only the subset that can be justified with low-cost L0 evidence, without introducing heavy evidence into `L0`.

## 1. Background

After multiple gambling recall-recovery rounds, the largest remaining miss bucket is now `score < 4`. These pages usually have very weak evidence, or the current `L0` pipeline is not seeing enough usable low-cost signals.

The user explicitly requires:

- `L0` must remain a fast specialized judgment layer
- no heavy evidence
- no pushing full HTML scanning, OCR, or screenshot semantics into `L0`

## 2. Goal

Mine the remaining `score < 4` gambling misses, identify low-cost evidence gaps, and only if justified by real evidence, implement one minimal patch that recovers a small subset of high-feature gambling pages that should still finish in `L0`.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

This task is allowed to change:

- gambling-specific low-cost feature extraction
- low-cost recovery logic for `possible_gambling_lure`
- gambling-specific explainability reason codes if needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `adult` / `gate`
- redesign `possible_bonus_or_betting_induction`
- read or scan large HTML payloads for new L0 logic
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
- full `gambling = 804` pool

### Prior Handoff

- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized summary of `score < 4` gambling misses
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
- do not introduce full-HTML scanning into `L0`
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

- mine `score < 4` misses first
- only consider low-cost evidence such as host, URL, page title, and existing visible-text patterns
- reject any candidate signal that would require heavy content parsing

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

- [ ] `score < 4` misses are categorized by low-cost evidence gap
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
# quantify ordinary-benign 800 and gambling 804 on the reproducible sorted+seeded baseline
PY
```

Expected evidence to capture:

- low-cost miss categories
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

- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

## 13. Open Questions / Blocking Issues

- `none`
