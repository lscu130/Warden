# Gambling strategy contract alignment task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前代码中的 `gambling` L0 触发策略整理成正式双语设计段落，并回写到仓库设计文档。
- 任务目标是文档对齐，不是继续调规则，也不改代码行为。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-15-GAMBLING-STRATEGY-CONTRACT-ALIGNMENT`
- 任务标题：`对齐并固化当前 gambling L0 策略文档`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`
- 创建日期：`2026-04-15`
- 提出人：`用户`

## 1. 背景

当前代码里的 `gambling` L0 策略已经演化出明确的结构：

- 主触发规则
- explainable weighted score
- 窄 recovery 条件
- editorial suppression
- routing 约束

但 `L0_DESIGN_V1.md` 里的 `7.3B / 7.3C` 仍然停留在较粗的 guidance 级别，没有完整描述当前实际契约。

## 2. 目标

把当前代码中已经稳定下来的 `gambling` L0 触发策略整理成正式双语设计文字，补进 `L0_DESIGN_V1.md`，让文档能够准确表达当前的证据层次、score 角色、suppression 规则、induction 语义和 routing 影响，同时保持现有代码与 schema 不变。

## 3. Scope In

This task is allowed to touch:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-15_gambling_strategy_contract_alignment.md`
- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

This task is allowed to change:

- gambling strategy documentation inside the L0 design spec
- specialized weak-signal documentation if needed for gambling score fields
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue gambling tuning or threshold changes
- modify `adult` / `gate` logic
- add dependencies
- change CLI or schema

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current in-repo gambling strategy implementation
- current specialized signal names and routing flags
- none

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- an updated bilingual `L0_DESIGN_V1.md` section for the current gambling strategy
- a repo task doc with final status
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

- document the current code behavior rather than proposing a new policy
- keep the patch scoped to gambling strategy wording
- state clearly that weighted score is explainability and recovery support, not a replacement for all rule logic

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_bonus_or_betting_induction`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- readers of `L0_DESIGN_V1.md`
- future gambling tuning tasks that will rely on the documented contract

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- update `7.3B` only if the current gambling score outputs need explicit documentation
- update `7.3C` to reflect actual current trigger structure and routing impact
- avoid drifting into unrelated detector-family prose

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

- [ ] the design doc now reflects current gambling trigger strategy
- [ ] weighted score and recovery role are described accurately
- [ ] routing impact for gambling surfaces is documented

## 11. Validation Checklist

Minimum validation expected:

- [ ] scoped doc diff review
- [ ] terminology spot-check against current code
- [ ] bilingual structure spot-check
- [ ] handoff produced

Commands to run if applicable:

```bash
git diff -- "E:\Warden\L0_DESIGN_V1.md" "E:\Warden\docs\tasks\2026-04-15_gambling_strategy_contract_alignment.md" "E:\Warden\docs\handoff\2026-04-15_gambling_strategy_contract_alignment.md"
```

Expected evidence to capture:

- updated `7.3B / 7.3C` text
- no code behavior changes

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

- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-15-GAMBLING-STRATEGY-CONTRACT-ALIGNMENT`
- Task Title: `Align and freeze the current gambling L0 strategy in docs`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`
- Created At: `2026-04-15`
- Requested By: `User`

Use this task to document the current in-code `gambling` L0 trigger strategy as a formal bilingual design contract, without changing behavior.

## 1. Background

The current in-code `gambling` L0 strategy now has a clear structure:

- primary trigger rules
- an explainable weighted score
- narrow recovery clauses
- editorial suppression
- routing constraints

However, `L0_DESIGN_V1.md` still describes gambling at a coarse guidance level and does not fully reflect the current contract.

## 2. Goal

Document the current stabilized `gambling` L0 strategy from code into formal bilingual design text inside `L0_DESIGN_V1.md`, so the design spec accurately reflects the current evidence hierarchy, score role, suppression behavior, induction semantics, and routing impact while leaving code and schema unchanged.

## 3. Scope In

This task is allowed to touch:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-15_gambling_strategy_contract_alignment.md`
- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

This task is allowed to change:

- gambling strategy documentation inside the L0 design spec
- specialized weak-signal documentation if needed for gambling score outputs
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue gambling tuning or threshold changes
- modify `adult` / `gate`
- add dependencies
- change CLI or schema

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current in-repo gambling strategy implementation
- current specialized signal names and routing flags
- none

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- an updated bilingual `L0_DESIGN_V1.md` section for the current gambling strategy
- a repo task doc with final status
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

- document the current code behavior rather than proposing a new policy
- keep the patch scoped to the gambling strategy wording
- state clearly that weighted score is explainability and recovery support, not a replacement for all rule logic

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_bonus_or_betting_induction`; `gambling_weighted_score`; `gambling_weighted_score_reasons`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- readers of `L0_DESIGN_V1.md`
- future gambling tuning tasks that will rely on the documented contract

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- update `7.3B` only if the current gambling score outputs need explicit documentation
- update `7.3C` to reflect the actual current trigger structure and routing impact
- avoid drifting into unrelated detector-family prose

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

- [x] the design doc now reflects the current gambling trigger strategy
- [x] the weighted score and recovery role are described accurately
- [x] routing impact for gambling surfaces is documented

## 11. Validation Checklist

Minimum validation expected:

- [x] scoped doc diff review
- [x] terminology spot-check against current code
- [x] bilingual structure spot-check
- [x] handoff produced

Commands to run if applicable:

```bash
git diff -- "E:\Warden\L0_DESIGN_V1.md" "E:\Warden\docs\tasks\2026-04-15_gambling_strategy_contract_alignment.md" "E:\Warden\docs\handoff\2026-04-15_gambling_strategy_contract_alignment.md"
```

Expected evidence to capture:

- updated `7.3B / 7.3C` text
- no code behavior changes

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

- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

## 13. Open Questions / Blocking Issues

- `none`
