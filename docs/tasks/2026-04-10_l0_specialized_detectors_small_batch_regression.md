# L0 specialized detectors small-batch regression task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于对刚实现的 specialized detectors 做一轮约 100 样本的小批量回归。
- 本任务只做抽样、运行、统计和文档交付，不改 detector 实现。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SMALL-BATCH-REGRESSION`
- 任务标题：`运行 L0 specialized detectors 约 100 样本小批量回归并统计触发率`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/tasks/2026-04-09_l0_specialized_detectors.md`、`docs/handoff/2026-04-09_l0_specialized_detectors.md`
- 创建日期：`2026-04-10`
- 提出人：`用户`

## 背景

`L0 specialized detectors` 已经在 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中落地，并完成了少量代表样本 smoke。用户现在要求做一轮更大的小批量回归，观察新增字段在 `gambling`、`adult`、`gate`、`ordinary benign` 四类样本上的触发率和基础分布，验证这次实现是否具备可用的区分度。

## 目标

抽取约 100 个样本，覆盖 `gambling`、`adult`、`gate`、`ordinary benign` 四组，运行当前弱信号链路，统计 `specialized_surface_signals` 和 `rule_flags` 中新增字段的触发率、主标签分布和明显异常点，并把结果收敛成 handoff。

## 允许修改范围

允许触碰：

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

允许修改：

- repo task / handoff 文档
- 运行时命令
- 临时统计脚本或一次性命令输出

## 禁止修改范围

不得：

- 修改 detector 实现逻辑
- 修改 schema 或字段名
- 改采样数据内容
- 顺手改无关代码

## 输入

需要读取：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`
- `E:\Warden\data\raw\...` 中可用样本目录

当前缺失项：

- `none`

## 输出

必须产出：

- 约 100 样本的小批量回归统计
- 四组样本的新增字段触发率摘要
- 明显误报 / 漏报样本备注
- handoff 文档

## 硬约束

- 不改 detector 代码
- 抽样总量约 100，允许轻微浮动
- 四组样本都必须覆盖
- 结果必须诚实记录实际抽样与命令

## 接口 / 兼容性约束

- 本任务不改变任何接口
- 本任务不改变任何 schema
- 统计对象以当前 working tree 中的 specialized-detector 版本为准

## 建议执行顺序

1. 从数据目录识别四组样本池。
2. 每组抽取约 25 个样本。
3. 运行 `derive_auto_labels_from_sample_dir` 与 `derive_rule_labels`。
4. 汇总触发率、主标签分布和异常样本。
5. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- 总样本量约 100
- 四组样本都有覆盖
- 新字段触发率已统计
- 至少记录若干明显异常点
- handoff 完整

## 最低验证要求

- 样本数量核对
- 统计脚本成功运行
- 输出结果 spot check

## 交接要求

- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SMALL-BATCH-REGRESSION`
- Task Title: `Run an approximately 100-sample small-batch regression for L0 specialized detectors and summarize trigger rates`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-09_l0_specialized_detectors.md`; `docs/handoff/2026-04-09_l0_specialized_detectors.md`
- Created At: `2026-04-10`
- Requested By: `User`

Use this task for a small-batch regression of the newly added specialized detectors.

## 1. Background

The specialized detectors were just implemented in `scripts/labeling/Warden_auto_label_utils_brandlex.py` and validated on a few representative smoke samples. The user now wants a larger small-batch regression to observe how the new fields fire across `gambling`, `adult`, `gate`, and `ordinary benign` samples, and to check whether the new logic shows useful separation.

## 2. Goal

Sample approximately 100 examples across `gambling`, `adult`, `gate`, and `ordinary benign`, run the current weak-signal path, summarize trigger rates for the new fields in `specialized_surface_signals` and `rule_flags`, record obvious outliers, and produce a handoff.

## 3. Scope In

This task may touch:

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

This task may change:

- repo task and handoff docs
- runtime commands
- temporary one-off analysis commands or scripts

## 4. Scope Out

This task must not:

- modify the detector implementation
- modify schema or field names
- modify sampled data
- change unrelated code

## 5. Inputs

Docs / code / data:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`
- available sample directories under `E:\Warden\data\raw\...`

Missing inputs:

- `none`

## 6. Required Outputs

- an approximately 100-sample small-batch regression summary
- per-group trigger-rate summaries for the new fields
- notes for obvious false positives / false negatives / outliers
- a handoff document

## 7. Hard Constraints

- do not modify detector code
- keep the total sample count around 100, with minor deviation allowed
- all four groups must be covered
- report the actual sample selection and commands honestly

## 8. Interface / Schema Constraints

- this task changes no interface
- this task changes no schema
- the regression must use the current specialized-detector version in the working tree

## 9. Suggested Execution Plan

1. Identify candidate pools for the four groups from the dataset roots.
2. Sample about 25 per group.
3. Run `derive_auto_labels_from_sample_dir` and `derive_rule_labels`.
4. Aggregate trigger rates, primary-label distributions, and outliers.
5. Produce the handoff and update the task status to `DONE`.

## 10. Acceptance Criteria

- total sample count is around 100
- all four groups are covered
- trigger rates for the new fields are summarized
- several obvious outliers are recorded
- handoff is complete

## 11. Validation Checklist

- sample-count check
- successful stats execution
- output spot-check

## 12. Handoff Requirements

- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

## 13. Open Questions / Blocking Issues

- `none`
