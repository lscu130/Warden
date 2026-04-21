# L0 specialized detectors contract trim task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于收紧 L0 specialized detectors 的契约，只保留 `gambling`、`adult`、`gate` 三类信号。
- 本任务会移除 `possible_fake_verification` 与 `possible_interaction_required` 的 L0 输出语义，并同步实现与文档。
- 本任务会继续细化 `gambling`、`adult`、`gate` 的触发条件。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-CONTRACT-TRIM`
- 任务标题：`收紧 L0 specialized detectors 契约并移除 fake verification 与 interaction required 输出`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/tasks/2026-04-09_l0_specialized_detectors.md`、`docs/handoff/2026-04-09_l0_specialized_detectors.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- 创建日期：`2026-04-10`
- 提出人：`用户`

## 背景

当前 L0 specialized detectors 已经实现并完成了 100 样本小批量回归。回归显示：`gambling` 和 `adult` 有可用区分度，`gate` 仍需收紧；同时 `possible_fake_verification` 在该批样本中没有覆盖到，`possible_interaction_required` 几乎全量触发，区分力很差。用户因此要求收紧 L0 契约，移除这两个 L0 输出，只保留 `gambling`、`adult`、`gate` 三类显著专项信号，并继续细化这三类的触发条件。

## 目标

更新当前 L0 specialized-detector 实现和设计文档，使 L0 只保留 `possible_gambling_lure`、`possible_bonus_or_betting_induction`、`possible_adult_lure`、`possible_age_gate_surface`、`possible_gate_or_evasion`、`possible_challenge_surface` 及其相关 routing hints；移除 `possible_fake_verification` 与 `possible_interaction_required` 的 L0 语义和输出，并进一步收紧 `gambling`、`adult`、`gate` 的触发规则。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

允许修改：

- L0 specialized detector 关键词与触发逻辑
- `specialized_surface_signals` 中与 `gambling` / `adult` / `gate` 相关的输出
- `l0_routing_hints` 中与三类信号相关的 routing hints
- `L0_DESIGN_V1.md` 中对应契约 wording

## 禁止修改范围

不得：

- 改 unrelated 模块
- 加新依赖
- 顺手重构 brand / scenario 主逻辑
- 发明新的 L0 专项类别
- 静默保留 `possible_fake_verification` 或 `possible_interaction_required` 的 L0 契约表述

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

当前缺失项：

- `none`

## 输出

必须产出：

- 更新后的 L0 specialized-detector 实现
- 更新后的 `L0_DESIGN_V1.md`
- 代表样本验证结果
- handoff 文档

## 硬约束

- 明确移除 `possible_fake_verification`
- 明确移除 `possible_interaction_required`
- 只保留 `gambling`、`adult`、`gate` 三类 L0 specialized signals
- 继续细化三类触发，不做 broadening
- 如有 schema 破坏，必须在 handoff 里明确写出

## 接口 / 兼容性约束

- 允许改 `specialized_surface_signals` 输出字段集合
- 允许改 `l0_routing_hints` 相关语义
- 若删除字段，必须在 final 和 handoff 中明确写 `Schema changed`

## 建议执行顺序

1. 识别当前代码和文档里 `fake verification` 与 `interaction required` 的所有落点。
2. 更新实现，只保留 `gambling` / `adult` / `gate`。
3. 同步更新 `L0_DESIGN_V1.md`。
4. 用代表样本做 focused validation。
5. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- `possible_fake_verification` 已从 L0 输出和 L0 文档语义中移除
- `possible_interaction_required` 已从 L0 输出和 L0 文档语义中移除
- `gambling` / `adult` / `gate` 仍能在代表样本上稳定触发
- 文档和实现口径一致
- handoff 完整

## 最低验证要求

- Python 语法检查
- 赌博样本 smoke
- 成人样本 smoke
- gate 样本 smoke
- 关键字段 spot check

## 交接要求

- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-CONTRACT-TRIM`
- Task Title: `Tighten the L0 specialized-detector contract and remove fake-verification and interaction-required outputs`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/tasks/2026-04-09_l0_specialized_detectors.md`; `docs/handoff/2026-04-09_l0_specialized_detectors.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- Created At: `2026-04-10`
- Requested By: `User`

Use this task to tighten the L0 specialized-detector contract so that L0 keeps only `gambling`, `adult`, and `gate` signals.

## 1. Background

The current L0 specialized detectors have already been implemented and measured on a 100-sample regression slice. That regression showed usable separation for `gambling` and `adult`, further tightening need for `gate`, no actual coverage for `possible_fake_verification`, and extremely poor discrimination for `possible_interaction_required`. The user therefore wants the L0 contract tightened so that those two L0 outputs are removed, while `gambling`, `adult`, and `gate` are retained and further specialized.

## 2. Goal

Update the current L0 specialized-detector implementation and design docs so that L0 keeps only `possible_gambling_lure`, `possible_bonus_or_betting_induction`, `possible_adult_lure`, `possible_age_gate_surface`, `possible_gate_or_evasion`, `possible_challenge_surface`, and their related routing hints; remove the L0 semantics and outputs for `possible_fake_verification` and `possible_interaction_required`; and further tighten the trigger rules for `gambling`, `adult`, and `gate`.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

This task may change:

- L0 specialized-detector keywords and trigger logic
- `specialized_surface_signals` outputs related to `gambling` / `adult` / `gate`
- `l0_routing_hints` semantics related to those three signal families
- corresponding contract wording in `L0_DESIGN_V1.md`

## 4. Scope Out

This task must not:

- modify unrelated modules
- add dependencies
- opportunistically refactor the main brand / scenario logic
- invent new L0 specialized categories
- silently keep the `possible_fake_verification` or `possible_interaction_required` L0 contract wording

## 5. Inputs

Docs / code:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

Missing inputs:

- `none`

## 6. Required Outputs

- updated L0 specialized-detector implementation
- updated `L0_DESIGN_V1.md`
- representative-sample validation
- a handoff document

## 7. Hard Constraints

- explicitly remove `possible_fake_verification`
- explicitly remove `possible_interaction_required`
- retain only `gambling`, `adult`, and `gate` as L0 specialized signals
- further tighten those three trigger families rather than broadening them
- if schema breaks, report it explicitly in the handoff

## 8. Interface / Schema Constraints

- changing the `specialized_surface_signals` field set is allowed
- changing `l0_routing_hints` semantics is allowed
- if fields are removed, the final response and handoff must explicitly say `Schema changed`

## 9. Suggested Execution Plan

1. Identify all code and doc locations that still mention `fake verification` and `interaction required`.
2. Update the implementation so that only `gambling` / `adult` / `gate` remain.
3. Sync `L0_DESIGN_V1.md`.
4. Run focused validation on representative samples.
5. Produce the handoff and update the task status to `DONE`.

## 10. Acceptance Criteria

- `possible_fake_verification` is removed from L0 outputs and L0 docs
- `possible_interaction_required` is removed from L0 outputs and L0 docs
- `gambling` / `adult` / `gate` still fire stably on representative samples
- docs and implementation are aligned
- handoff is complete

## 11. Validation Checklist

- Python syntax check
- gambling-sample smoke test
- adult-sample smoke test
- gate-sample smoke test
- key-field spot check

## 12. Handoff Requirements

- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

## 13. Open Questions / Blocking Issues

- `none`
