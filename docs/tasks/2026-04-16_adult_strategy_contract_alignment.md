# Adult strategy contract alignment task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前代码中的 `adult` L0 触发策略整理成正式双语设计段落，并回写到仓库设计文档。
- 本任务只做文档对齐，不继续调规则，也不改代码。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-16-ADULT-STRATEGY-CONTRACT-ALIGNMENT`
- 任务标题：`对齐并固化当前 adult L0 策略文档`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`
- 创建日期：`2026-04-16`
- 提出人：`用户`

## 1. 背景

当前代码里的 `adult` L0 策略已经有稳定结构：

- `possible_adult_lure`
- `possible_age_gate_surface`
- adult URL-only 场景下的 `need_vision_candidate`
- adult + download / redirect / third-party delivery 场景下的 `need_l2_candidate`

但 `L0_DESIGN_V1.md` 里的 `7.3D` 仍然偏粗，没有完整表达当前实际契约。

## 2. 目标

把当前代码中已经稳定下来的 `adult` L0 触发策略整理成正式双语设计文字，补进 `L0_DESIGN_V1.md`，让文档准确表达当前的证据层次、age-gate 角色、URL-only 场景、以及 `L1 / L2` 路由影响，同时保持代码与 schema 不变。

## 3. Scope In

This task is allowed to touch:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_strategy_contract_alignment.md`
- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

This task is allowed to change:

- adult strategy documentation inside the L0 design spec
- task / handoff docs
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue adult tuning
- modify `gambling` / `gate`
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

- current in-repo adult strategy implementation
- current specialized signal names and routing flags
- none

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- an updated bilingual `L0_DESIGN_V1.md` section for the current adult strategy
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
- keep the patch scoped to the adult strategy wording
- state clearly how `possible_adult_lure`, `possible_age_gate_surface`, `need_vision_candidate`, and `need_l2_candidate` are intended to relate

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

- readers of `L0_DESIGN_V1.md`
- future adult tuning tasks that will rely on the documented contract

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- update only `7.3D`
- reflect the actual adult trigger structure and routing impact
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

- [ ] the design doc now reflects the current adult trigger strategy
- [ ] the role of age-gate and URL-only adult surfaces is described accurately
- [ ] routing impact for adult surfaces is documented

## 11. Validation Checklist

Minimum validation expected:

- [ ] scoped doc diff review
- [ ] terminology spot-check against current code
- [ ] bilingual structure spot-check
- [ ] handoff produced

Commands to run if applicable:

```bash
git diff -- "E:\Warden\L0_DESIGN_V1.md" "E:\Warden\docs\tasks\2026-04-16_adult_strategy_contract_alignment.md" "E:\Warden\docs\handoff\2026-04-16_adult_strategy_contract_alignment.md"
```

Expected evidence to capture:

- updated `7.3D` text
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

- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-16-ADULT-STRATEGY-CONTRACT-ALIGNMENT`
- Task Title: `Align and freeze the current adult L0 strategy in docs`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`
- Created At: `2026-04-16`
- Requested By: `User`

Use this task to document the current in-code `adult` L0 trigger strategy as a formal bilingual design contract, without changing behavior.

## 1. Background

The current in-code `adult` L0 strategy already has a stable structure:

- `possible_adult_lure`
- `possible_age_gate_surface`
- `need_vision_candidate` for adult URL-only cases
- `need_l2_candidate` for adult surfaces combined with download / redirect / third-party delivery signals

However, `L0_DESIGN_V1.md` still describes adult at a coarse guidance level and does not fully reflect the current contract.

## 2. Goal

Document the current stabilized `adult` L0 strategy from code into formal bilingual design text inside `L0_DESIGN_V1.md`, so the design spec accurately reflects the current evidence hierarchy, the role of age-gate signals, URL-only adult cases, and the routing impact into `L1 / L2` while leaving code and schema unchanged.

## 3. Scope In

This task is allowed to touch:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_strategy_contract_alignment.md`
- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

This task is allowed to change:

- adult strategy documentation inside the L0 design spec
- task / handoff docs
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue adult tuning
- modify `gambling` / `gate`
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

- current in-repo adult strategy implementation
- current specialized signal names and routing flags
- none

### Prior Handoff

- `docs/handoff/2026-04-15_gambling_strategy_contract_alignment.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- an updated bilingual `L0_DESIGN_V1.md` section for the current adult strategy
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
- keep the patch scoped to the adult strategy wording
- state clearly how `possible_adult_lure`, `possible_age_gate_surface`, `need_vision_candidate`, and `need_l2_candidate` are intended to relate

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

- readers of `L0_DESIGN_V1.md`
- future adult tuning tasks that will rely on the documented contract

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- update only `7.3D`
- reflect the actual adult trigger structure and routing impact
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

- [x] the design doc now reflects the current adult trigger strategy
- [x] the role of age-gate and URL-only adult surfaces is described accurately
- [x] routing impact for adult surfaces is documented

## 11. Validation Checklist

Minimum validation expected:

- [x] scoped doc diff review
- [x] terminology spot-check against current code
- [x] bilingual structure spot-check
- [x] handoff produced

Commands to run if applicable:

```bash
git diff -- "E:\Warden\L0_DESIGN_V1.md" "E:\Warden\docs\tasks\2026-04-16_adult_strategy_contract_alignment.md" "E:\Warden\docs\handoff\2026-04-16_adult_strategy_contract_alignment.md"
```

Expected evidence to capture:

- updated `7.3D` text
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

- `docs/handoff/2026-04-16_adult_strategy_contract_alignment.md`

## 13. Open Questions / Blocking Issues

- `none`
