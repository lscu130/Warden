# Gambling induction narrowing task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务专门收紧 `possible_bonus_or_betting_induction`
- 目标是减少普通内容页、博彩资讯页、affiliate / SEO 页对该弱信号的误触发
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-14-GAMBLING-INDUCTION-NARROWING`
- 任务标题：`收紧 possible_bonus_or_betting_induction，并完成一轮量化`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/tasks/2026-04-13_gambling_false_positive_tightening.md`、`docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- 创建日期：`2026-04-14`
- 提出人：`用户`

## 背景

上一轮 `gambling false-positive tightening` 已把 `possible_gambling_lure` 在固定普通样本切片上的误触发从 `15 / 400` 压到 `3 / 400`。  
当前更突出的剩余问题转到 `possible_bonus_or_betting_induction`：该字段现在仍然偏宽，普通资讯页、博彩导购页、SEO 聚合页、体育内容页容易因为 `bonus / promotion / payout / withdrawal / deposit` 这类词直接命中。  
用户要求单独收紧这个字段，然后再做一轮量化。

## 目标

围绕 `possible_bonus_or_betting_induction` 的误触发样本，识别当前导致普通内容页触发该字段的主要 token 和形成路径，在不改 schema、不扩 scope 到 `adult / gate / possible_gambling_lure` 大改的前提下，对该字段做最小有效收紧，并用固定切片完成一轮定量验证。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- `L0_DESIGN_V1.md` 仅在 contract wording 确实需要同步时

允许修改：

- `possible_bonus_or_betting_induction` 的形成逻辑
- 与该字段直接相关的 bonus / promotion 词族
- 必要的文档 wording 同步

## 禁止修改范围

- 不得修改 `adult` / `gate` specialized contract
- 不得重写 `possible_gambling_lure` 的整套策略
- 不得新增依赖
- 不得 broad refactor
- 不得改 schema、字段名、CLI

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- 当前 fixed-slice 里 `possible_bonus_or_betting_induction` 的代表误触发样本

当前缺失项：

- `none`

## 输出

必须产出：

- 一份 `possible_bonus_or_betting_induction` 误触发模式总结
- 更新后的 induction trigger 实现
- 一轮 focused smoke
- 一轮 fixed-slice quantification summary
- handoff 文档

## 硬约束

- 先分析误触发样本，再改规则
- 只处理 `possible_bonus_or_betting_induction`
- 不得通过粗暴删除大量核心 bonus 词来掩盖问题
- 必须显式报告收紧前后触发率变化
- 若 schema 变化，必须显式记录

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约
- 默认不修改输出 schema
- 不允许改现有 specialized field names

## 建议执行顺序

1. 汇总固定切片里 `possible_bonus_or_betting_induction` 的普通页误触发样本
2. 分析哪些 token、组合和页面类型在导致误触发
3. 做最小 patch
4. 运行 focused smoke 和一轮 fixed-slice 量化
5. 产出 handoff，并把 task 状态改为 `DONE`

## 验收条件

- 已实际查看一批 induction false-positive 样本
- 已给出明确的误触发模式归类
- fixed-slice 上 `possible_bonus_or_betting_induction` 的普通页误触发下降
- 没有引入 schema / interface break
- focused validation 已运行
- handoff 完整

## 最低验证要求

- Python 语法检查
- representative induction false-positive smoke
- representative gambling sample smoke
- 一轮 fixed-slice 量化

## 交接要求

- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-14-GAMBLING-INDUCTION-NARROWING`
- Task Title: `Tighten possible_bonus_or_betting_induction and run one quantification round`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`; `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- Created At: `2026-04-14`
- Requested By: `User`

Use this task to narrow `possible_bonus_or_betting_induction` only.

## 1. Background

The previous `gambling false-positive tightening` round already reduced `possible_gambling_lure` false positives on the fixed ordinary slice from `15 / 400` to `3 / 400`.  
The more visible remaining issue has shifted to `possible_bonus_or_betting_induction`: this field is still too broad, and ordinary news pages, gambling guide pages, affiliate / SEO pages, and sports-content pages can still trigger it because of terms such as `bonus`, `promotion`, `payout`, `withdrawal`, or `deposit`.  
The user requested a dedicated tightening round for this field, followed by one quantification pass.

## 2. Goal

Inspect current `possible_bonus_or_betting_induction` false-positive samples, identify the dominant token and page-formation paths that cause ordinary content pages to emit this field, and apply the smallest valid tightening patch without changing schema, without broadening scope into `adult / gate`, and without turning this into a full redesign of `possible_gambling_lure`. Then run one fixed-slice quantification round.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing

This task may change:

- the formation logic of `possible_bonus_or_betting_induction`
- bonus / promotion keyword families directly related to that field
- necessary documentation wording sync

## 4. Scope Out

This task must not:

- modify the `adult` or `gate` specialized contract
- rewrite the full `possible_gambling_lure` strategy
- add dependencies
- perform a broad refactor
- change schema, field names, or CLI

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current fixed-slice `possible_bonus_or_betting_induction` false-positive samples
- current fixed-slice gambling samples
- current fixed-slice ordinary-benign samples

### Prior Handoff

- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a concrete `possible_bonus_or_betting_induction` false-positive pattern summary
- updated induction-trigger implementation
- a focused smoke-test summary
- a fixed-slice quantification summary
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

- inspect real induction false positives before changing rules
- change only `possible_bonus_or_betting_induction`
- explicitly report pre/post trigger rates on the validation slice

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `specialized_surface_signals`
- `matched_keywords`
- current `evt_v1.2` output structure

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_bonus_or_betting_induction`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream trigger-rate statistics based on previous induction behavior

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- use the same fixed-slice style as the previous gambling task where practical
- keep `possible_gambling_lure` changes out unless a tiny supporting adjustment is unavoidable
- report the tradeoff honestly even if induction recall also moves

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
