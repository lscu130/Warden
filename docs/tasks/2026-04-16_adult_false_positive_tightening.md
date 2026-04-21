# Adult false-positive tightening task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于先压缩当前 `adult` 在普通 benign 上的误触，再在不引入重证据的前提下看是否还能改善 precision / recall 平衡。
- 本任务允许修改当前 `adult` L0 触发逻辑，但范围只限 `adult`。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-16-ADULT-FALSE-POSITIVE-TIGHTENING`
- 任务标题：`压缩 adult 误触并收紧当前策略`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`
- 创建日期：`2026-04-16`
- 提出人：`用户`

## 1. 背景

当前工作树下，`possible_adult_lure` 的代理指标大致为：

- adult pool recall proxy: `439 / 530 = 82.83%`
- ordinary benign 上 adult 误触: `182 / 16339 = 1.11%`
- precision proxy: `70.69%`

用户当前优先目标是先处理 ordinary benign 上的 adult false positives，再看是否还能继续收紧策略，改善 precision / recall 平衡。

## 2. 目标

定位当前 ordinary benign 上 `adult` 误触的主要模式，做最小可审计的规则收紧，尽量先压掉明显误触；在此基础上，复算当前 adult pool 与 ordinary benign pool 的代理指标，评估是否实现了更合理的 precision / recall 平衡。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

This task is allowed to change:

- adult-specific low-cost trigger tightening
- adult-specific explainability reason codes if strictly needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `gambling` / `gate`
- add heavy HTML parsing, OCR, or screenshot semantics to L0
- add dependencies
- change CLI
- redesign unrelated threat-taxonomy logic

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\benign`
- current `possible_adult_lure` outputs

### Prior Handoff

- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- an updated `L0_DESIGN_V1.md` note if adult trigger semantics change
- a categorized summary of current adult false-positive patterns
- one minimal patch to tighten adult triggers if justified
- before/after quantification on adult and ordinary-benign pools
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

- inspect the false positives before patching
- keep the fix low-cost and L0-compatible
- do not trade away large adult recall blindly just to reduce benign hits

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- downstream adult trigger-rate statistics
- downstream routing flags derived from adult surfaces

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- mine ordinary-benign false positives first
- prefer narrow tightening over broad token deletion
- quantify both adult recall proxy and benign false-positive rate after the patch

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

- [ ] dominant adult false-positive patterns are explicitly identified
- [ ] adult false positives on ordinary benign are reduced
- [ ] adult recall impact is measured and reported

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] adult vs ordinary-benign quantification
- [ ] targeted false-positive spot-check
- [ ] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# quantify adult and ordinary-benign pools before/after
PY
```

Expected evidence to capture:

- false-positive pattern summary
- before/after adult recall proxy
- before/after benign false-positive count

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

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-16-ADULT-FALSE-POSITIVE-TIGHTENING`
- Task Title: `Tighten adult false positives and refine the current strategy`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`
- Created At: `2026-04-16`
- Requested By: `User`

Use this task to reduce current `adult` false positives on ordinary benign samples first, then evaluate whether the tightened strategy also improves the current precision / recall balance without adding heavy evidence.

## 1. Background

In the current working tree, `possible_adult_lure` shows the following proxy metrics:

- adult pool recall proxy: `439 / 530 = 82.83%`
- ordinary-benign adult false positives: `182 / 16339 = 1.11%`
- precision proxy: `70.69%`

The user's immediate priority is to handle adult false positives on ordinary benign pages first, then see whether the strategy can be tightened further to improve the precision / recall balance.

## 2. Goal

Identify the dominant false-positive patterns for `adult` on ordinary benign pages, implement the smallest auditable tightening patch to reduce clearly bad hits first, and then recompute the current adult-pool and ordinary-benign proxy metrics to evaluate whether the precision / recall balance improved.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

This task is allowed to change:

- adult-specific low-cost trigger tightening
- adult-specific explainability reason codes if strictly needed
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `gambling` / `gate`
- add heavy HTML parsing, OCR, or screenshot semantics to L0
- add dependencies
- change CLI
- redesign unrelated threat-taxonomy logic

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\benign`
- current `possible_adult_lure` outputs

### Prior Handoff

- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a categorized summary of current adult false-positive patterns
- one minimal patch to tighten adult triggers if justified
- before/after quantification on adult and ordinary-benign pools
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

- inspect the false positives before patching
- keep the fix low-cost and L0-compatible
- do not trade away large adult recall blindly just to reduce benign hits

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- downstream adult trigger-rate statistics
- downstream routing flags derived from adult surfaces

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- mine ordinary-benign false positives first
- prefer narrow tightening over broad token deletion
- quantify both adult recall proxy and benign false-positive rate after the patch

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

- [x] dominant adult false-positive patterns are explicitly identified
- [x] adult false positives on ordinary benign are reduced
- [x] adult recall impact is measured and reported

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] adult vs ordinary-benign quantification
- [x] targeted false-positive spot-check
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# quantify adult and ordinary-benign pools before/after
PY
```

Expected evidence to capture:

- false-positive pattern summary
- before/after adult recall proxy
- before/after benign false-positive count

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

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

## 13. Open Questions / Blocking Issues

- `none`
