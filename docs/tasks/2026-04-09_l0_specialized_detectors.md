# L0 specialized detectors task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于在现有 cheap-evidence / weak-signal 链路上实现 `gambling`、`adult`、`gate` 三类专项探测器。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。
- 本任务要求先看真实样本，再固化规则，不允许靠纯猜测扩展关键词表。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-09-SPECIALIZED-DETECTORS`
- 任务标题：`实现 L0 博彩 / 成人 / gate 专项探测器并接入现有弱信号链路`
- 执行角色：`Codex 执行工程师`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`PROJECT.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/modules/MODULE_INFER.md`、`L0_DESIGN_V1.md`
- 创建日期：`2026-04-09`
- 提出人：`用户`

## 背景

仓库里没有独立成型的 `src/infer/L0-fast` 实现基线。当前实际可运行、可扩展、且已被采集链路消费的轻量弱信号路径位于 `scripts/labeling/Warden_auto_label_utils_brandlex.py`，并由 `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` 调用生成 `auto_labels` / `rule_labels`。本任务需要在这条现有 cheap-evidence 链路上补入 specialized detectors，而不是虚构新的 runtime 基线。

## 目标

在现有 cheap-evidence / weak-signal 链路上实现 `gambling`、`adult`、`gate / challenge / fake verification` 三类 specialized detectors，基于真实样本观察补充专项弱信号、禁止不该 low-risk early-stop 的页面被轻放，并产出保守的升级提示，同时保持当前 schema、stage semantics 和 rule-label contract 的向后兼容。

## 允许修改范围

允许触碰：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

允许修改：

- cheap-evidence 上的专项 token / pattern family 识别
- additive weak-signal 输出
- additive routing-hint 输出
- 与专项探测器相关的最小弱风险和升级提示逻辑

## 禁止修改范围

不得：

- 重构整个 inference pipeline
- 发明新的 `src/infer` 运行时基线
- 新增第三方依赖
- 改 frozen schema 字段名
- 静默改 route-result contract
- 把专项命中直接当 final label
- 顺手清理无关脚本

## 输入

需要阅读：

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `L0_DESIGN_V1.md`

已识别样本：

- 赌博样本：`E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
- 赌博样本：`E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\thescore.bet_20260408T072233Z`
- 成人样本：`E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
- 成人样本：`E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\avxxxmini.com_20260408T071508Z`
- gate 样本：`E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- gate 样本：`E:\Warden\data\raw\benign\gate\hertz.com_20260401T082852Z`

当前缺失项：

- `none`

## 输出

必须产出：

- 已实现的 gambling / adult / gate specialized weak-signal 逻辑
- additive 专项弱信号输出，例如 `possible_gambling_lure`、`possible_adult_lure`、`possible_gate_or_evasion`、`possible_fake_verification`
- additive routing-hint 输出，用于表达 forbid-early-stop / escalation tendency
- 代表样本 smoke 验证记录
- handoff 文档

## 硬约束

- 只在现有 cheap-evidence 链路上做最小实现
- 先看真实样本再固化规则
- 专项输出保持 weak-signal / routing-hint 级别
- additive only；不破坏现有消费者
- gate / fake verification 页面默认不得落入低风险早停语义

## 接口 / 兼容性约束

- `derive_auto_labels`、`derive_rule_labels` 现有调用方式必须继续可用
- 现有输出字段不得重命名
- 若新增字段，只能 additive，并在 handoff 中显式说明
- 现有 `rule_flags.escalate_to_l2_candidate` 语义可增强，但不能被重写成新 contract

## 建议执行顺序

1. 继续检查真实样本并归纳高显著模式。
2. 在 `Warden_auto_label_utils_brandlex.py` 中实现专项探测和 routing hints。
3. 只在必要处连接到现有 risk / rule flag 逻辑。
4. 跑 Python 语法检查与代表样本 smoke。
5. 产出 handoff，并把 task 状态更新为 `DONE`。

## 验收条件

- 已实际检查赌博 / 成人 / gate 代表样本
- 代码能输出专项 weak signals
- 代码能输出保守的 early-stop / escalation hints
- 没有静默改 schema 或现有调用方式
- 验证结果和风险记录完整

## 最低验证要求

- `python -m py_compile` 检查改动脚本
- 至少 1 个赌博样本 smoke
- 至少 1 个成人样本 smoke
- 至少 1 个 gate 样本 smoke
- spot check 新字段和现有字段同时存在

## 交接要求

- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

## 执行前开放问题

- `none`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-09-SPECIALIZED-DETECTORS`
- Task Title: `Implement L0 specialized detectors for gambling, adult, and gate surfaces on the existing weak-signal path`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `L0_DESIGN_V1.md`
- Created At: `2026-04-09`
- Requested By: `User`

Use this task for implementing specialized detectors for `gambling`, `adult`, and `gate` surfaces on the existing cheap-evidence / weak-signal path.

## 1. Background

The repo does not currently contain a standalone, implementation-ready `src/infer/L0-fast` baseline. The actual lightweight weak-signal path already used by the capture flow lives in `scripts/labeling/Warden_auto_label_utils_brandlex.py` and is consumed by `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` to generate `auto_labels` and `rule_labels`. This task must extend that existing cheap-evidence path rather than inventing a new runtime baseline.

## 2. Goal

Implement specialized detectors for `gambling`, `adult`, and `gate / challenge / fake verification` surfaces on the existing cheap-evidence / weak-signal path, using real-sample observation to add specialized weak signals, prevent inappropriate low-risk early-stop interpretation, and emit conservative escalation hints while preserving backward compatibility for the current schema, stage semantics, and rule-label contract.

## 3. Scope In

This task may touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

This task may change:

- specialized token / pattern family detection on cheap evidence
- additive specialized weak-signal outputs
- additive routing-hint outputs
- the minimum weak-risk and escalation logic needed for the specialized detectors

## 4. Scope Out

This task must not:

- refactor the full inference pipeline
- invent a new `src/infer` runtime baseline
- add third-party dependencies
- rename frozen schema fields
- silently change the route-result contract
- treat a specialized hit as a final label
- perform unrelated cleanup in adjacent scripts

## 5. Inputs

Docs / code:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `L0_DESIGN_V1.md`

Observed representative samples:

- gambling sample: `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
- gambling sample: `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\thescore.bet_20260408T072233Z`
- adult sample: `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
- adult sample: `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\avxxxmini.com_20260408T071508Z`
- gate sample: `E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- gate sample: `E:\Warden\data\raw\benign\gate\hertz.com_20260401T082852Z`

Missing inputs:

- `none`

## 6. Required Outputs

- implemented specialized weak-signal logic for gambling / adult / gate families
- additive specialized weak-signal outputs such as `possible_gambling_lure`, `possible_adult_lure`, `possible_gate_or_evasion`, and `possible_fake_verification`
- additive routing-hint outputs expressing forbid-early-stop and escalation tendency
- representative-sample smoke validation notes
- a handoff document

## 7. Hard Constraints

- keep the implementation minimal and inside the existing cheap-evidence path
- inspect real samples before freezing rules
- keep specialized outputs at weak-signal / routing-hint level
- additive only; do not break current consumers
- gate / fake verification pages must not default to low-risk early-stop semantics

## 8. Interface / Schema Constraints

- the current `derive_auto_labels` and `derive_rule_labels` call pattern must keep working
- existing output fields must not be renamed
- any new fields must be additive and explicitly documented in the handoff
- the existing `rule_flags.escalate_to_l2_candidate` semantics may be strengthened but must not be rewritten into a new contract

## 9. Suggested Execution Plan

1. Continue inspecting real samples and summarize high-salience patterns.
2. Implement specialized detection and routing hints in `Warden_auto_label_utils_brandlex.py`.
3. Connect the new logic to existing risk / rule-flag logic only where necessary.
4. Run Python syntax checks and representative-sample smoke tests.
5. Produce the handoff and update the task status to `DONE`.

## 10. Acceptance Criteria

- representative gambling / adult / gate samples were actually inspected
- the code emits specialized weak signals
- the code emits conservative early-stop / escalation hints
- no schema or call pattern was silently broken
- validation results and risks are documented

## 11. Validation Checklist

- `python -m py_compile` on changed scripts
- at least one gambling-sample smoke test
- at least one adult-sample smoke test
- at least one gate-sample smoke test
- a spot-check showing both new and existing fields coexist

## 12. Handoff Requirements

- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

## 13. Open Questions / Blocking Issues

- `none`
