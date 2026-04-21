# Gambling false-positive tightening task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于专门收紧 `gambling` specialized detector 的 false positive。
- 本任务重点处理普通内容站、博彩资讯页、联盟页、SEO 聚合页、术语密集页上的博彩误触发。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-13-GAMBLING-FALSE-POSITIVE-TIGHTENING`
- 任务标题：`收紧 gambling false positive，聚焦普通内容站和 affiliate / news 页面误触发`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`TODO`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- 创建日期：`2026-04-13`
- 提出人：`用户`

## 背景

最近两轮 specialized-detector 调整已经显著提升了 `gambling` 的 recall，并把 `adult / gambling -> gate` 的 cross-trigger 压到很低。  
当前更突出的问题转到了 `gambling` false positive：在普通 benign 切片中，仍能看到博彩资讯页、联盟页、SEO 聚合页或术语密集内容页被 `possible_gambling_lure` 误打中。  
这类页面常见特征是含有 `casino / betting / slots / bonus / deposit / payout` 等词，但并不构成真正的赌博诱导落地页。

## 目标

围绕 `gambling` false positive 样本，找出导致普通内容页被误打成 `possible_gambling_lure` 的主要词组和形成路径，在尽量不伤害当前赌博页 recall 的前提下，收紧 `gambling` specialized trigger。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` 仅在契约 wording 确实需要同步时
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

允许修改：

- `gambling` 相关关键词与触发逻辑
- 与 `gambling` 直接相关的 routing-hint 形成逻辑
- 必要的文档 wording 同步

## 禁止修改范围

- 不得修改 `adult` / `gate` specialized contract
- 不得重新引入已删除字段
- 不得新增依赖
- 不得 broad refactor
- 不得顺手处理空文本全局路由以外的问题

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- 这轮 mixed-batch regression 里命中的普通 benign gambling false-positive 样本

当前缺失项：

- `none`

## 输出

必须产出：

- 一份 gambling false-positive pattern note 或等价分析结论
- 更新后的 gambling specialized trigger 实现
- focused validation 结果
- 一轮以 gambling false positive 为中心的 regression / spot-check
- handoff 文档

## 硬约束

- 先分析 false positive，再改规则
- 只处理 `gambling` false positive
- 不允许靠简单砍掉大量核心赌博词硬压误触发
- 必须显式报告 recall / false-positive 的取舍
- 若 schema 变化，必须显式记录

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约
- 默认不修改输出 schema
- 不允许改现有 specialized field names

## 建议执行顺序

1. 汇总普通 benign 上的 gambling false-positive 样本。
2. 分析哪些词、哪些组合、哪些页面类型导致误触发。
3. 做最小 patch。
4. 运行 focused validation 和控制切片回归。
5. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- 已实际查看一批 gambling false-positive 样本
- 已给出明确的误触发模式归类
- 普通 benign 上的 gambling 误触发下降
- 赌博页 recall 没有明显塌陷
- focused validation 已运行
- handoff 完整

## 最低验证要求

- Python 语法检查
- 赌博代表样本 smoke
- 普通 benign false-positive 代表样本 smoke
- 一轮小切片验证

## 交接要求

- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-13-GAMBLING-FALSE-POSITIVE-TIGHTENING`
- Task Title: `Tighten gambling false positives with a focus on ordinary content sites and affiliate/news pages`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- Created At: `2026-04-13`
- Requested By: `User`

Use this task to tighten `gambling` false positives, especially on ordinary content sites, gambling-news pages, affiliate pages, SEO aggregation pages, and terminology-heavy pages.

## 1. Background

The recent specialized-detector tuning rounds have already improved `gambling` recall materially and pushed `adult / gambling -> gate` cross-triggering close to zero.  
The more visible remaining problem is now `gambling` false positives: ordinary benign slices still contain gambling-news, affiliate, SEO aggregation, or terminology-heavy content pages that fire `possible_gambling_lure`.  
Those pages often contain terms such as `casino`, `betting`, `slots`, `bonus`, `deposit`, or `payout`, but they are not true gambling-lure landing pages.

## 2. Goal

Analyze the current `gambling` false-positive samples, identify the dominant token and formation paths that cause ordinary content pages to emit `possible_gambling_lure`, and tighten the `gambling` specialized trigger without materially damaging current gambling-page recall.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

This task may change:

- `gambling` keyword families and trigger logic
- routing-hint logic directly related to `gambling`
- necessary documentation wording sync

## 4. Scope Out

This task must not:

- modify the `adult` or `gate` specialized contract
- reintroduce removed legacy fields
- add dependencies
- perform a broad refactor
- opportunistically tackle unrelated routing problems

## 5. Inputs

Docs / code / data:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- the current ordinary-benign gambling false-positive samples from the mixed-batch regression

Missing inputs:

- `none`

## 6. Required Outputs

- a concrete gambling false-positive pattern note or equivalent pattern summary
- updated gambling specialized-trigger implementation
- focused validation results
- a gambling-false-positive-oriented regression or spot-check summary
- a handoff document

## 7. Hard Constraints

- inspect the false positives before changing the rules
- address only `gambling` false positives
- do not suppress false positives by simply deleting too many core gambling terms
- explicitly report the recall / false-positive tradeoff
- if schema changes, report it explicitly

## 8. Interface / Schema Constraints

- preserve the current `evt_v1.2` contract by default
- avoid output-schema changes by default
- do not change existing specialized field names

## 9. Suggested Execution Plan

1. Collect the ordinary-benign gambling false-positive samples.
2. Analyze which terms, combinations, and page types are causing the false positives.
3. Make the smallest valid patch.
4. Run focused validation and a control-slice regression.
5. Produce the handoff and mark the task status as `DONE`.

## 10. Acceptance Criteria

- a real set of gambling false-positive samples was inspected
- explicit false-positive pattern categories were documented
- ordinary-benign gambling false positives decreased
- gambling-page recall did not materially collapse
- focused validation was run
- the handoff is complete

## 11. Validation Checklist

- Python syntax check
- representative gambling-sample smoke tests
- representative benign false-positive smoke tests
- one small validation slice

## 12. Handoff Requirements

- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

## 13. Open Questions / Blocking Issues

- `none`
