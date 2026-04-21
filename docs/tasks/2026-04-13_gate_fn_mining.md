# Gate false-negative mining task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于专门处理 `gate` specialized detector 的 false negative。
- 本任务只盯 `matched_keywords = []` 的 gate 漏检页，不处理普通 benign 误触发，也不顺手扩到 `gambling` 或 `adult`。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-13-GATE-FN-MINING`
- 任务标题：`专项挖掘 gate false negative，聚焦 matched_keywords 为空的漏检页`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- 创建日期：`2026-04-13`
- 提出人：`用户`

## 背景

最新一轮 `gate / adult / gambling` specialized-detector tuning 已经显著压低了 `ordinary_benign` 上的 gate 误触发，也把 `adult / gambling -> gate` 的 cross-trigger 降到了接近零。  
当前剩余最明显的问题是：在 mixed-batch regression 中，`gate` aggregate 仍只有约 `62.9%`，且大量漏检样本的 `matched_keywords.gate_text` 为空。  
这说明还有一批 gate 页面没有被当前文本词表和轻量运行期支撑规则覆盖到，需要单独做 false-negative mining，而不是继续混着调整体阈值。

## 目标

围绕 `matched_keywords = []` 的 gate 漏检页，系统挖掘这批页面的 URL、visible-text、轻量运行期特征和结构模式，找出当前 `gate` trigger 没覆盖到的高显著信号，并在不显著抬高普通 benign gate 误触发的前提下，继续提升 gate specialized recall。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` 仅在契约 wording 确实需要同步时
- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

允许修改：

- `gate` 相关关键词、辅助匹配逻辑、轻量规则
- 与 `gate` 直接相关的 `l0_routing_hints` 形成逻辑
- 必要的文档 wording 同步

## 禁止修改范围

- 不得修改 `gambling` / `adult` specialized contract
- 不得重新引入 `possible_fake_verification`
- 不得重新引入 `possible_interaction_required`
- 不得顺手处理普通 benign 上的 `gambling` false positive
- 不得做 broad refactor
- 不得新增依赖

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `E:\Warden\data\raw\benign\gate`
- 回归中 `matched_keywords = []` 的 gate miss 样本清单

当前缺失项：

- `none`

## 输出

必须产出：

- 一份明确的 gate false-negative pattern note 或等价分析结论
- 更新后的 gate specialized trigger 实现
- focused validation 结果
- 一轮针对 gate FN 的 regression / spot-check
- handoff 文档

## 硬约束

- 先挖掘漏检样本模式，再改规则
- 只处理 `gate` false negative
- 优先增加可解释、可审计的高显著信号
- 不允许靠放宽泛化条件去硬提 recall
- 若 schema 变化，必须显式记录

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约
- 不允许修改现有 specialized field names
- `specialized_surface_signals` 和 `l0_routing_hints` 的字段集合默认保持不变

## 建议执行顺序

1. 汇总 `matched_keywords = []` 的 gate miss 样本。
2. 按 visible-text 缺失、URL 线索、运行期支撑、结构模板分组。
3. 提炼高显著 gate FN patterns。
4. 在实现中做最小 patch。
5. 运行 focused validation 和 gate-oriented regression。
6. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- 已实际查看一批 `matched_keywords = []` 的 gate miss
- 已给出明确的 gate FN pattern 归类
- gate recall 有实质提升，且 benign gate 误触发没有明显回弹
- focused validation 已运行
- handoff 完整

## 最低验证要求

- Python 语法检查
- gate 代表 miss 样本 smoke
- 一轮以 gate FN 为中心的小切片验证

## 交接要求

- `docs/handoff/2026-04-13_gate_fn_mining.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-13-GATE-FN-MINING`
- Task Title: `Mine gate false negatives with a strict focus on pages whose matched_keywords are empty`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- Created At: `2026-04-13`
- Requested By: `User`

Use this task to isolate and improve `gate` false negatives, specifically the misses whose `matched_keywords` remain empty.

## 1. Background

The most recent `gate / adult / gambling` specialized-detector tuning substantially reduced gate false triggering on `ordinary_benign` pages and drove `adult / gambling -> gate` cross-triggering close to zero.  
The main remaining gap is now concentrated in gate recall: the mixed-batch regression still reports only about `62.9%` aggregate gate recall, and many of the remaining misses have an empty `matched_keywords.gate_text`.  
That means there is still a family of gate pages that the current text lexicon and lightweight runtime-support rules do not cover, and that gap should be handled through dedicated false-negative mining rather than broad threshold loosening.

## 2. Goal

Systematically mine the `matched_keywords = []` gate misses by analyzing their URL, visible text, lightweight runtime features, and structural patterns, then improve the `gate` trigger logic so recall increases without materially rebounding gate false triggers on ordinary benign pages.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing
- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

This task may change:

- `gate` keyword families, helper matching logic, and lightweight rules
- `l0_routing_hints` logic that is directly tied to `gate`
- necessary documentation wording sync

## 4. Scope Out

This task must not:

- modify the `gambling` or `adult` specialized contract
- reintroduce `possible_fake_verification`
- reintroduce `possible_interaction_required`
- opportunistically fix ordinary-benign `gambling` false positives
- perform a broad refactor
- add dependencies

## 5. Inputs

Docs / code / data:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `E:\Warden\data\raw\benign\gate`
- the current list of gate misses whose `matched_keywords` are empty

Missing inputs:

- `none`

## 6. Required Outputs

- a concrete gate false-negative pattern note or an equivalent pattern summary
- updated gate specialized-trigger implementation
- focused validation results
- a gate-false-negative-oriented regression or spot-check summary
- a handoff document

## 7. Hard Constraints

- inspect and classify the misses before changing the rules
- address only `gate` false negatives
- prefer high-salience, auditable signals
- do not boost recall by broadly loosening the trigger conditions
- if schema changes, report it explicitly

## 8. Interface / Schema Constraints

- preserve the current `evt_v1.2` contract by default
- do not change existing specialized field names
- keep the field sets of `specialized_surface_signals` and `l0_routing_hints` unchanged by default

## 9. Suggested Execution Plan

1. Collect the gate misses whose `matched_keywords = []`.
2. Group them by visible-text absence, URL clues, runtime support, and structural template patterns.
3. Extract high-salience gate false-negative patterns.
4. Make the smallest valid implementation patch.
5. Run focused validation and a gate-oriented regression slice.
6. Produce the handoff and update the task status to `DONE`.

## 10. Acceptance Criteria

- a real set of `matched_keywords = []` gate misses was inspected
- explicit gate false-negative pattern categories were documented
- gate recall improved materially without a meaningful rebound in benign gate false triggers
- focused validation was run
- the handoff is complete

## 11. Validation Checklist

- Python syntax check
- representative gate-miss smoke tests
- one gate-false-negative-centered validation slice

## 12. Handoff Requirements

- `docs/handoff/2026-04-13_gate_fn_mining.md`

## 13. Open Questions / Blocking Issues

- `none`
