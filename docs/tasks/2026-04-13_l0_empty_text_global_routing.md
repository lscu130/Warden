# L0 empty-text global routing task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把“可视文本为空”从单一 `gate` 问题提升为整个 `L0` 的全局路由问题。
- 本任务只处理 `L0` 路由语义，不把空文本直接判成风险标签。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-13-EMPTY-TEXT-GLOBAL-ROUTING`
- 任务标题：`将 empty visible-text 上升为整个 L0 的全局路由语义`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/modules/MODULE_INFER.md`、`docs/handoff/2026-04-13_gate_fn_mining.md`
- 创建日期：`2026-04-13`
- 提出人：`用户`

## 背景

上一条 `gate FN mining` 任务已经证明，剩余大量 gate miss 的主因是 `visible_text.txt` 为空，而不是 gate 词表继续漏词。  
这类问题并不只影响 `gate`，也可能出现在 Vue / React / 强客户端渲染 / capture gap 页面。  
因此，“empty visible-text” 不应继续被视作某一类 specialized detector 的局部问题，而应上升为整个 `L0` 的全局可观测性与路由问题。

## 目标

在 `L0` 中引入统一的 empty-text routing 语义：当原始 `visible_text` 为空或几乎为空时，`L0` 应禁止低风险早停，并优先把样本送往 `L1` 做更完整内容判断；同时保持这一路径是 routing 语义，不是直接风险判定。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-13_l0_empty_text_global_routing.md`
- `docs/handoff/2026-04-13_l0_empty_text_global_routing.md`

允许修改：

- `L0` 的全局路由逻辑
- `l0_routing_hints` 的形成规则和 reason code
- 与 empty-text routing 直接相关的模块文档 wording

## 禁止修改范围

- 不得把 empty-text 直接等价为风险标签
- 不得修改 `gambling / adult / gate` specialized field 集合
- 不得新增依赖
- 不得顺手重构整个 labeling / inference 脚本
- 不得改 `L1 / L2` 合约边界

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`
- 代表性 empty-text 样本

当前缺失项：

- `none`

## 输出

必须产出：

- 更新后的 `L0` empty-text routing 实现
- focused validation 结果
- repo handoff 文档

## 硬约束

- empty-text 只能作为 routing 语义，不能直接当最终风险结论
- 优先复用现有 `l0_routing_hints` 字段，不轻易改字段集合
- 若 schema 发生变化，必须显式记录
- 必须说明 empty-text 当前到底触发什么路由策略

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约
- 默认不修改输出 schema
- 若仅新增 routing reason code，应视为行为变化而不是 schema 变更

## 建议执行顺序

1. 明确 raw `visible_text` 与带 `page_title` 的当前输入拼接点。
2. 设计 empty-text 的 `L0` 路由条件。
3. 做最小 patch。
4. 跑 focused validation。
5. 更新模块文档与 handoff。
6. 把 task 状态更新为 `DONE`。

## 验收条件

- empty-text 已进入全局 `L0` 路由逻辑
- empty-text 不被直接写成风险结论
- 输出 schema 没有被随意改动
- focused validation 已运行
- handoff 完整

## 最低验证要求

- Python 语法检查
- empty-text 代表样本 smoke
- 一组 non-empty control 样本 smoke

## 交接要求

- `docs/handoff/2026-04-13_l0_empty_text_global_routing.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-13-EMPTY-TEXT-GLOBAL-ROUTING`
- Task Title: `Promote empty visible-text into a global L0 routing semantic`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `docs/handoff/2026-04-13_gate_fn_mining.md`
- Created At: `2026-04-13`
- Requested By: `User`

Use this task to treat empty `visible_text` as a global L0 routing problem rather than as a narrow gate-only issue.

## 1. Background

The previous `gate FN mining` task showed that a large portion of the remaining gate misses are caused by empty `visible_text.txt` rather than by uncovered gate lexicon alone.  
That issue is not exclusive to `gate`; it can also happen on Vue / React / strongly client-rendered pages or on general capture-gap pages.  
For that reason, empty `visible_text` should no longer be treated as only a specialized-detector local issue. It should be elevated into a global L0 observability and routing concern.

## 2. Goal

Introduce a global empty-text routing semantic in L0: when the raw `visible_text` is empty or nearly empty, L0 should forbid low-risk early stop and prefer routing the sample to L1 for fuller-content judgment, while keeping this path explicitly as a routing semantic rather than a direct risk verdict.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-13_l0_empty_text_global_routing.md`
- `docs/handoff/2026-04-13_l0_empty_text_global_routing.md`

This task may change:

- global L0 routing logic
- the formation rules and reason codes inside `l0_routing_hints`
- module-document wording directly related to empty-text routing

## 4. Scope Out

This task must not:

- treat empty-text as a direct risk label
- modify the specialized field set for `gambling` / `adult` / `gate`
- add dependencies
- opportunistically refactor the whole labeling / inference script
- change the L1 / L2 contract boundary

## 5. Inputs

Docs / code / data:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`
- representative empty-text samples

Missing inputs:

- `none`

## 6. Required Outputs

- updated L0 empty-text routing implementation
- focused validation results
- a repo handoff document

## 7. Hard Constraints

- empty-text must remain a routing semantic rather than a final risk verdict
- prefer reusing the existing `l0_routing_hints` fields instead of changing the field set casually
- if schema changes, report it explicitly
- the delivery must explain exactly what routing behavior empty-text now triggers

## 8. Interface / Schema Constraints

- preserve the current `evt_v1.2` contract by default
- avoid output-schema changes by default
- if only new routing reason codes are added, treat that as behavior change rather than schema change

## 9. Suggested Execution Plan

1. Identify the distinction between raw `visible_text` and the current title-prepended input path.
2. Design the empty-text L0 routing condition.
3. apply the smallest valid patch.
4. run focused validation.
5. update the module doc and handoff.
6. mark the task status as `DONE`.

## 10. Acceptance Criteria

- empty-text is handled inside the global L0 routing logic
- empty-text is not turned into a direct risk verdict
- the output schema was not casually changed
- focused validation was run
- the handoff is complete

## 11. Validation Checklist

- Python syntax check
- representative empty-text smoke tests
- a non-empty control smoke set

## 12. Handoff Requirements

- `docs/handoff/2026-04-13_l0_empty_text_global_routing.md`

## 13. Open Questions / Blocking Issues

- `none`
