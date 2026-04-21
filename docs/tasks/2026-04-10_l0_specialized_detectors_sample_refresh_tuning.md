# L0 specialized detectors sample-refresh tuning task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于利用补充后的 `gambling / adult / gate` 样本，继续优化 L0 specialized detectors 的触发逻辑。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。
- 本任务会基于补充样本先做观察，再调整规则和验证。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SAMPLE-REFRESH-TUNING`
- 任务标题：`基于补充样本继续优化 L0 gambling / adult / gate specialized triggers`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- 创建日期：`2026-04-10`
- 提出人：`用户`

## 背景

用户已经补充了 `gambling / adult / gate` 样本。当前 L0 specialized-detector 契约已收紧到三类信号，但触发逻辑仍需要结合更新后的样本池继续细化，尤其要利用新增覆盖来优化高显著 trigger、压误触发，并改进代表样本和小批量回归表现。

## 目标

基于补充后的 `gambling / adult / gate` 样本，重新观察这三类页面的 URL / visible-text / 轻量运行期信号模式，进一步优化当前 `Warden_auto_label_utils_brandlex.py` 中的 specialized trigger 逻辑，并用 focused validation 与小切片回归验证优化结果。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` 仅在实现契约确实需要同步时
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

允许修改：

- `gambling` / `adult` / `gate` 关键词与触发逻辑
- 与这三类直接相关的 routing-hint 逻辑
- 必要的契约 wording 同步

## 禁止修改范围

- 不得重新引入 `possible_fake_verification`
- 不得重新引入 `possible_interaction_required`
- 不得改 unrelated 模块
- 不得顺手做 broad refactor
- 不得新增依赖

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- 补充后的 `gambling / adult / gate` 样本池
- 最近两次相关 handoff

当前缺失项：

- `none`

## 输出

必须产出：

- 更新后的 specialized trigger 实现
- focused validation 结果
- 小切片回归结果或 spot-check 汇总
- handoff 文档

## 硬约束

- 先观察补充样本，再调规则
- 只优化 `gambling / adult / gate`
- 保持当前三类 specialized contract，不回退到旧字段
- 若 schema 发生变化，必须显式记录

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约
- 如需进一步调整字段集合，必须在 handoff 中明确说明

## 建议执行顺序

1. 识别补充后的样本池变化。
2. 抽取新增代表样本，观察模式。
3. 在实现中收紧或补强三类触发。
4. 运行 focused validation 与小切片回归。
5. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- 已实际查看补充样本
- 三类 trigger 有实质优化
- focused validation 已运行
- 回归或小切片验证已运行
- handoff 完整

## 最低验证要求

- Python 语法检查
- 三类代表样本 smoke
- 一轮小切片验证

## 交接要求

- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SAMPLE-REFRESH-TUNING`
- Task Title: `Continue optimizing L0 gambling/adult/gate specialized triggers using the supplemented samples`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- Created At: `2026-04-10`
- Requested By: `User`

Use this task to further optimize the `gambling` / `adult` / `gate` specialized triggers using the supplemented sample pools.

## 1. Background

The user has supplemented the `gambling / adult / gate` samples. The L0 specialized-detector contract has already been trimmed to these three families, but the trigger logic still needs further refinement against the refreshed sample pools so the stronger coverage can be used to improve salient triggers, reduce false triggers, and improve focused validation plus small-slice regression behavior.

## 2. Goal

Re-observe the URL / visible-text / lightweight runtime patterns of the supplemented `gambling / adult / gate` sample pools, further refine the specialized trigger logic in `Warden_auto_label_utils_brandlex.py`, and validate the result with focused validation and a small regression slice.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` only if wording sync is actually needed
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

This task may change:

- keyword families and trigger logic for `gambling` / `adult` / `gate`
- routing-hint logic directly related to those three families
- necessary contract wording sync

## 4. Scope Out

This task must not:

- reintroduce `possible_fake_verification`
- reintroduce `possible_interaction_required`
- modify unrelated modules
- perform a broad opportunistic refactor
- add dependencies

## 5. Inputs

Docs / code / data:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- the supplemented `gambling / adult / gate` sample pools
- the two most recent related handoffs

Missing inputs:

- `none`

## 6. Required Outputs

- updated specialized-trigger implementation
- focused validation results
- a small regression slice or spot-check summary
- a handoff document

## 7. Hard Constraints

- inspect the supplemented samples before tuning the rules
- optimize only `gambling` / `adult` / `gate`
- keep the current three-family specialized contract and do not revert to the old removed fields
- if schema changes again, report it explicitly

## 8. Interface / Schema Constraints

- preserve the current `evt_v1.2` contract by default
- if the field set changes again, report it explicitly in the handoff

## 9. Suggested Execution Plan

1. Identify how the supplemented sample pools changed.
2. Pull representative newly covered samples and inspect the patterns.
3. Tighten or strengthen the three trigger families in code.
4. Run focused validation and a small regression slice.
5. Produce the handoff and update the task status to `DONE`.

## 10. Acceptance Criteria

- the supplemented samples were actually inspected
- the three trigger families received substantive tuning
- focused validation was run
- a regression or small-slice validation was run
- the handoff is complete

## 11. Validation Checklist

- Python syntax check
- representative-sample smoke tests for the three families
- one small-slice validation run

## 12. Handoff Requirements

- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

## 13. Open Questions / Blocking Issues

- `none`
