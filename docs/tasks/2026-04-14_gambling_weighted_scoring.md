# Gambling weighted scoring task

## 中文版
> 面向人工阅读的摘要版。英文版是权威执行版本；若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于分析 `gambling` specialized detector 的特征区分度，并落一个可解释的加权 score。
- 重点是把 `url / host / text / bonus / editorial suppression` 做成更量化的证据组合。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-14-GAMBLING-WEIGHTED-SCORING`
- 任务标题：`分析 gambling 特征区分度，并实现 explainable weighted score`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`docs/handoff/2026-04-13_gambling_false_positive_tightening.md`、`docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- 创建日期：`2026-04-14`
- 提出人：`用户`

## 背景

当前 `gambling` specialized detector 已做过一轮 false-positive tightening 和一轮 induction narrowing。现状是：

- `possible_gambling_lure` 在 ordinary benign 上的误触发已明显下降
- `possible_bonus_or_betting_induction` 最新一轮过度偏向 precision
- 当前逻辑仍以手工布尔组合为主，量化结构不足

用户希望把触发逻辑做得更可解释，例如区分：

- `casino` 出现在 URL / host 与出现在正文中的证据强度
- `bet + digits` 这类 host 线索与弱 `bonus` 文本的证据强度
- `url > host > strong text > weak text > editorial suppression` 这类位置与语义层级

## 目标

用当前博彩样本池与 ordinary benign 对照切片分析特征区分度，提炼一套最小可用的 explainable weighted gambling score，并把它落到现有 `gambling` specialized detector 中，保持 L0 低成本，并完成一轮定量验证。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- `L0_DESIGN_V1.md` 仅在 contract wording 确实需要同步时

允许修改：

- `gambling` 相关特征提取
- `gambling` 的内部加权 / score 逻辑
- 必要的 explainability 输出
- 必要的文档同步

## 禁止修改范围

- 不得修改 `adult` / `gate` specialized contract
- 不得 broad refactor
- 不得新增依赖
- 不得改 CLI
- 不得把高成本语义判断推进 L0

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- 当前博彩样本池
- ordinary benign 对照切片

当前缺失项：

- `none`

## 输出

必须产出：

- 一份 gambling 特征区分度总结
- 一份 explainable weighted-score 设计结论
- 更新后的脚本实现
- 一轮 focused smoke
- 一轮定量验证
- handoff 文档

## 硬约束

- 先做样本分析，再改规则
- score 必须能解释为具体证据贡献
- 优先 additive / backward-compatible 方案
- 若新增输出字段，必须明确记录 schema 变化
- 不得把 L0 变成高成本统计模型

## 接口 / 兼容性约束

- 默认保持当前 `evt_v1.2` 契约，除非新增 explainability 字段确有必要
- 若新增字段，只能 additive，且必须显式记录
- 不允许重命名现有 specialized field names

## 建议执行顺序

1. 读取目标脚本和最近两条 gambling handoff
2. 枚举候选特征并统计 gambling / benign 差异
3. 设计 explainable weighted score
4. 做最小 patch
5. 跑 focused validation 和一轮量化
6. 产出 handoff，并把 task 状态改为 `DONE`

## 验收条件

- 已实际统计一轮 gambling vs benign 特征差异
- 已给出明确的 weighted-score 解释
- 已落到脚本，或明确说明为什么不宜落地
- 验证结果已说明 precision / recall tradeoff
- handoff 完整

## 最低验证要求

- Python 语法检查
- representative gambling / benign smoke
- 一轮 fixed-slice quantification

## 交接要求

- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-14-GAMBLING-WEIGHTED-SCORING`
- Task Title: `Analyze gambling feature separability and implement an explainable weighted score`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `L0_DESIGN_V1.md`; `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`; `docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- Created At: `2026-04-14`
- Requested By: `User`

Use this task to analyze `gambling` feature separability and, if supported by the sample evidence, implement an explainable weighted score for the existing gambling specialized detector.

## 1. Background

The current `gambling` specialized detector has already gone through one false-positive tightening round and one induction-narrowing round.
The current state is:

- `possible_gambling_lure` false positives on ordinary-benign slices have already dropped materially
- the most recent `possible_bonus_or_betting_induction` change is now precision-heavy and recall-light
- the current logic is still dominated by manual boolean combinations, with limited quantitative structure

The user requested a more explainable weighted approach, for example distinguishing:

- `casino` in URL / host from `casino` in body text
- `bet + digits` host evidence from weak generic bonus terms
- evidence layers such as `url > host > strong text > weak text > editorial suppression`

## 2. Goal

Use the current gambling sample pool and an ordinary-benign control slice to analyze separability of gambling-related features, derive a minimal explainable weighted gambling score, and integrate it into the existing `gambling` specialized detector while keeping L0 low-cost and producing one quantitative validation round.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- `L0_DESIGN_V1.md` only if contract wording truly needs syncing

This task may change:

- gambling-related feature extraction
- internal gambling weighting / score logic
- necessary explainability outputs
- necessary documentation wording sync

## 4. Scope Out

This task must not:

- modify the `adult` or `gate` specialized contract
- perform a broad refactor
- add dependencies
- change CLI
- push high-cost semantic reasoning into L0

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current gambling sample pool
- ordinary-benign control slice

### Prior Handoff

- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a concrete gambling feature-separability summary
- an explainable weighted-score design conclusion
- an updated script implementation
- a focused smoke-test summary
- one quantitative validation summary
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

- inspect real sample differences before changing the rules
- the score must remain explainable in terms of concrete evidence contributions
- prefer additive and backward-compatible outputs
- if a new output field is introduced, report the schema change explicitly

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `evt_v1.2` structure unless additive explainability output is justified

Schema / field constraints:

- Schema changed allowed: `YES`, but additive only if necessary
- If yes, required compatibility plan: `new explainability fields must be optional/additive and documented`
- Frozen field names involved: `possible_gambling_lure`; `possible_bonus_or_betting_induction`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current repo validation snippets using `derive_auto_labels_from_sample_dir`

Downstream consumers to watch:

- downstream readers of `specialized_surface_signals`
- downstream trigger-rate statistics based on previous gambling behavior

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- use the existing gambling sample pool and a fixed ordinary-benign slice for comparability
- keep the score explainable by concrete evidence buckets rather than opaque normalization
- if score output is added, keep it additive and scoped to gambling only

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
