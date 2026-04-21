# L0 specialized detectors insert task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把专项探测器相关正式双语段落并入 `L0_DESIGN_V1.md`。
- 本任务只改文档，不改推理代码、schema、CLI 或运行时输出结构。
- 本任务保持 `L0` 仍为低成本前置筛查层、`L1` 仍为主判断层、`L2` 仍为高成本升级层。

## 任务元信息

- 任务 ID：`TASK-2026-04-10-L0-SPECIALIZED-DETECTORS-INSERT`
- 任务标题：`把 specialized detector 正式双语段落补入 L0_DESIGN_V1.md`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference / L0 design`
- 相关文档：`AGENTS.md`、`PROJECT.md`、`L0_DESIGN_V1.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- 创建日期：`2026-04-10`
- 提出人：`用户`

## 背景

`L0_DESIGN_V1.md` 已冻结 L0 的职责、输入边界、路由语义与 no-early-stop 约束，但尚未正式纳入高显著垂类专项探测器的双语契约正文。用户提供了专项插入草稿，目标是把该草稿整理并并入 repo 内的正式 L0 设计文档。

## 目标

更新 `L0_DESIGN_V1.md`，补充 specialized detector families、high-salience vertical fast-handling constraints，以及 specialized detector implementation constraints 的正式双语段落，同时保持现有 `L0 / L1 / L2` 分层契约不变。

## 允许修改范围

允许触碰：

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

允许修改：

- `L0_DESIGN_V1.md` 中关于弱信号归纳、早停约束、实现约束的正式文档表述
- 对应 task / handoff 文档

## 禁止修改范围

不得：

- 改 inference 代码或 detector 实现
- 改 schema、CLI、输出 contract
- 重写 `L0`、`L1`、`L2` 官方阶段语义
- 把 specialized detector 写成默认最终裁决器
- 顺手重构其他模块文档

## 输入

需要阅读：

- `L0_DESIGN_V1.md`
- 用户提供的 `L0_SPECIALIZED_DETECTORS_INSERT_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

当前缺失项：

- `none`

## 输出

必须产出：

- 更新后的 `L0_DESIGN_V1.md`
- 记录本次变更的 handoff 文档

## 硬约束

- 只做文档修改
- 不改代码
- 不改 schema
- specialized detector 默认只能输出 weak signals / candidates / routing hints
- 不得把专项命中写成最终标签或默认 L0 直接裁决

## 接口 / 兼容性约束

- `L0_DESIGN_V1.md` 仍必须是 L0 设计规范文档
- 官方路由结果仍保持 `early_stop_low_risk`、`escalate_to_L1`、`direct_to_L2`
- 文档新增内容必须与 `MODULE_INFER.md` 和 gate/evasion auxiliary protocol 一致

## 建议执行顺序

1. 阅读现有 `L0_DESIGN_V1.md` 与插入草稿。
2. 将新增内容插入到弱信号、早停约束和实现约束的合适位置。
3. 检查中英文内容是否一致，编号是否合理。
4. 产出 handoff。

## 验收条件

- `L0_DESIGN_V1.md` 已补入 specialized detector 正式双语段落
- 新增内容没有改变既有 `L0 / L1 / L2` 契约
- specialized detector 仍被约束为 weak-signal / routing-hint 级别
- task 与 handoff 已生成

## 最低验证要求

- 文档结构检查
- 中英双语一致性检查
- diff scope 检查

## 交接要求

- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-2026-04-10-L0-SPECIALIZED-DETECTORS-INSERT`
- Task Title: `Insert the formal bilingual specialized-detector sections into L0_DESIGN_V1.md`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference / L0 design`
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `L0_DESIGN_V1.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- Created At: `2026-04-10`
- Requested By: `User`

Use this task for the documentation-only insertion of the formal bilingual specialized-detector sections into `L0_DESIGN_V1.md`.

## 1. Background

`L0_DESIGN_V1.md` already freezes L0 responsibilities, input boundaries, routing semantics, and no-early-stop constraints, but it does not yet include the formal bilingual contract text for high-salience specialized detector families. The user provided a draft insert document, and the goal is to merge that material into the repo-resident L0 design specification.

## 2. Goal

Update `L0_DESIGN_V1.md` to add formal bilingual sections for specialized detector families, fast-handling constraints for high-salience verticals, and implementation constraints for specialized detectors, while preserving the current `L0 / L1 / L2` staged contract.

## 3. Scope In

This task may touch:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

This task may change:

- formal wording in `L0_DESIGN_V1.md` around weak-signal aggregation, early-stop constraints, and implementation constraints
- the associated task and handoff docs

## 4. Scope Out

This task must not:

- modify inference code or detector implementations
- modify schema, CLI, or output contracts
- rewrite the official `L0 / L1 / L2` stage semantics
- turn specialized detectors into default final adjudicators
- refactor unrelated module docs

## 5. Inputs

Docs:

- `L0_DESIGN_V1.md`
- user-provided `L0_SPECIALIZED_DETECTORS_INSERT_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

Missing inputs:

- `none`

## 6. Required Outputs

- updated `L0_DESIGN_V1.md`
- a handoff document recording the change

## 7. Hard Constraints

- documentation-only change
- no code change
- no schema change
- specialized detectors must remain weak-signal / candidate / routing-hint level by default
- no wording that turns a specialized hit into a final label or default L0 direct adjudication

## 8. Interface / Schema Constraints

- `L0_DESIGN_V1.md` must remain the L0 design specification
- official route results remain `early_stop_low_risk`, `escalate_to_L1`, and `direct_to_L2`
- new wording must remain compatible with `MODULE_INFER.md` and the gate/evasion auxiliary protocol

## 9. Suggested Execution Plan

1. Read the current `L0_DESIGN_V1.md` and the insert draft.
2. Insert the new material into the weak-signal, early-stop, and implementation-constraint sections.
3. Verify Chinese/English alignment and numbering sanity.
4. Produce handoff.

## 10. Acceptance Criteria

- `L0_DESIGN_V1.md` contains the formal bilingual specialized-detector sections
- the new content does not change the existing `L0 / L1 / L2` contract
- specialized detectors remain constrained to weak signals / routing hints
- task and handoff are present

## 11. Validation Checklist

- document-structure check
- bilingual consistency check
- diff scope check

## 12. Handoff Requirements

- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

## 13. Open Questions / Blocking Issues

- `none`
