# L0 Gate Specialized Tuning Task

## 中文版

> 面向人类阅读的摘要版。英文版为权威执行版本；若精确字段、范围、验收或兼容性要求有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前 L0 gate detector 从初版 keyword/routing signal 提升到类似 gambling/adult 的可量化特化配置。
- 本任务只处理 `gate`，不重新打开 L0 的 full HTML、default brand extraction、screenshot/OCR、heavy model 或 interaction recovery 路径。
- 本任务要求先量化当前 baseline，再基于 gate FN/FP mining 做低成本、可解释的 score-guided tuning。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- 任务标题：`L0 gate specialized tuning with score-guided low-cost evidence`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference / L0`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/modules/L0_DESIGN_V1.md`、`docs/modules/MODULE_INFER.md`、`docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`、`docs/handoff/2026-04-24_window_handoff_summary_for_gpt_web.md`
- 创建日期：`2026-04-28`
- 提出人：`用户`

## 背景

当前 `src/warden/module/l0.py` 已经有 gate 基础信号：`GATE_SURFACE_KEYWORDS`、`GATE_STRONG_KEYWORDS`、`gate_text`、`gate_url`、`possible_challenge_surface`、`possible_gate_or_evasion` 和 gate 相关 routing reason。但它还没有达到 gambling/adult 的特化程度：没有 gate 专属 score、没有稳定阈值、没有系统性 FN/FP mining，也没有把 `GATE_URL_KEYWORDS`、`GATE_SHORT_FLOW_KEYWORDS`、`GATE_IDENTITY_FLOW_KEYWORDS` 稳定沉入 legacy 配置源。

当前 L0 合同已经收紧：L0 只专注 `gambling / adult / gate`，默认只吃 URL、visible text/title、form summary、network summary、raw visible-text observability 和已有 compact diff/evasion hints。后续 gate tuning 必须保持这个低成本边界。

## 目标

在不扩大 L0 输入成本的前提下，模仿 gambling/adult 的调参流程，为 gate 建立一套可解释、可量化、可回归的特化策略：先统计当前 gate baseline，再针对 gate FN/FP 做 mining，补齐低成本关键词/结构信号，新增或稳定 gate score 与 reason codes，最后用 gate / gambling / adult / benign 控制集量化 precision、recall 和跨类误触。

## 允许修改范围

允许触碰：

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 与 L0 gate tuning 直接相关的评估 / 维护脚本，优先复用现有脚本
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

允许修改：

- gate keyword families
- gate low-cost structural cues
- `possible_challenge_surface` / `possible_gate_or_evasion` 的触发条件
- gate routing reason codes
- 可解释 gate score 字段和 score reasons
- gate tuning 的小批量评估脚本或评估命令
- L0 设计文档中 gate 专项策略说明

## 禁止修改范围

不得：

- 修改 L0 当前三类专项范围；只能处理 `gate`
- 重新加入 `possible_fake_verification` 或 `possible_interaction_required` 作为 L0 输出合同
- 默认读取完整 HTML
- 默认做 brand extraction
- 默认使用 screenshot/OCR
- 引入 heavy model、LLM、browser interaction、click-through recovery 或 gate solving
- 修改 gambling/adult 的既有触发策略，除非是为了修复本任务引入的直接冲突
- 改训练模块、数据 schema 或 frozen label 语义
- 新增第三方依赖

## 输入

需要阅读：

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- 现有 L0 specialized evaluation / benchmark 脚本或 handoff
- 当前可用的 gate 样本池、benign 样本池、gambling/adult 控制样本池

当前缺失项：

- gate 样本池的最新准确路径需在执行时从 repo / `E:\WardenData` 现有目录中确认
- 若缺少足够 gate true-positive / false-negative 样本，需要先输出缺口报告，不能伪造 recall 结论

## 输出

必须产出：

- 当前 gate baseline 统计
- gate FN mining 结果，重点关注 `matched_keywords = []` 或 gate weak-support miss
- gate FP mining 结果，重点关注 benign / ordinary 页面误触
- 低成本 gate evidence proposal
- 若实现调参：更新后的 gate detector / score / routing logic
- gate / gambling / adult / benign 控制集回归结果
- 更新后的 L0 gate 文档说明
- handoff 文档

## 硬约束

- 只使用当前 L0 允许的低成本输入
- 优先做可解释 score，不做黑盒分类器
- gate score 必须区分至少这些 evidence families：
  - strong challenge text
  - URL gate hint
  - short-flow / loading-flow text
  - identity / verification-flow text
  - captcha / anti-bot evidence from existing cheap evasion signals
  - dynamic / empty visible text observability support
- score reasons 必须可回溯到具体 evidence family
- 任何新增输出字段必须 backward compatible，并在 handoff 明确写出 schema/interface 影响
- 不允许为了提升 recall 大幅放宽到普通 login / security / verification 文本误触

## 接口 / 兼容性约束

- Schema changed allowed: `additive only`
- 允许新增候选字段：
  - `gate_weighted_score`
  - `gate_weighted_score_reasons`
  - `gate_score_evidence`
- 必须保留既有字段：
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - `specialized_fast_resolution_candidate`
- 若最终不新增字段，也必须在 handoff 中说明原因
- 旧 auto-label / compatibility entrypoint 必须继续可运行

## 建议执行顺序

1. 读取当前 L0 gate 实现和 legacy keyword source。
2. 找到当前 gate 样本池、benign 控制池、gambling/adult 控制池。
3. 跑当前 baseline，统计 `possible_gate_or_evasion`、`possible_challenge_surface`、matched keyword buckets、routing reason、latency。
4. 做 gate FN mining，优先分析 `matched_keywords.gate_text = []` 且人工/目录标签看起来是 gate 的样本。
5. 做 gate FP mining，区分普通 login/security/verification 页面与真实 challenge/gate 页面。
6. 设计低成本 gate score 和 reason code，不碰 heavy evidence。
7. 实现最小 patch。
8. 跑小批量回归：gate / benign / gambling / adult。
9. 更新 L0 文档和 task 状态。
10. 产出 handoff。

## 验收条件

- 当前 baseline 被量化并写入 handoff
- gate FN / FP 主要原因被分类
- gate tuning 不引入 full HTML / brand / screenshot/OCR / heavy interaction
- gate 输出仍只属于 weak-signal / routing-hint 语义
- gate recall 有可解释提升，或明确说明样本不足 / 低成本证据不足导致无法提升
- benign、gambling、adult 控制集误触不出现明显回退
- `specialized_fast_resolution_candidate` 的 gate 语义没有被静默扩大成最终裁决
- 文档和实现口径一致
- handoff 完整

## 最低验证要求

- Python syntax check：
  - `python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- gate focused baseline / after comparison
- benign control false-positive check
- gambling/adult control no-regression check
- key field spot check：
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - any new gate score fields
- latency spot check if matching logic changes materially

## 交接要求

- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

## 执行前开放问题

- 需要执行时确认当前 gate 样本池路径和样本数量。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- Task Title: `L0 gate specialized tuning with score-guided low-cost evidence`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference / L0`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/L0_DESIGN_V1.md`; `docs/modules/MODULE_INFER.md`; `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`; `docs/handoff/2026-04-24_window_handoff_summary_for_gpt_web.md`
- Created At: `2026-04-28`
- Requested By: `User`

Use this task to tune the current L0 gate detector into a measurable, explainable, score-guided specialized detector similar to the existing gambling/adult tuning path.

## 1. Background

The current `src/warden/module/l0.py` already contains basic gate signals: `GATE_SURFACE_KEYWORDS`, `GATE_STRONG_KEYWORDS`, `gate_text`, `gate_url`, `possible_challenge_surface`, `possible_gate_or_evasion`, and gate-related routing reasons. However, gate has not yet been tuned to the same level as gambling/adult. It has no dedicated gate score, no stable threshold policy, no systematic FN/FP mining, and some fallback keyword families such as `GATE_URL_KEYWORDS`, `GATE_SHORT_FLOW_KEYWORDS`, and `GATE_IDENTITY_FLOW_KEYWORDS` are not yet stabilized in the legacy compatibility source.

The current L0 contract is narrowed: L0 only specializes in `gambling / adult / gate`, and the default hot path only consumes URL, visible text/title, form summary, network summary, raw visible-text observability, and already available compact diff/evasion hints. Gate tuning must preserve that low-cost boundary.

## 2. Goal

Build a low-cost, explainable, measurable gate specialization strategy without expanding L0's input cost. The task must first measure the current gate baseline, then mine gate FN/FP cases, add low-cost keyword or structural evidence where justified, introduce or stabilize gate score and reason codes, and finally quantify precision, recall, and cross-family false positives on gate / gambling / adult / benign control sets.

## 3. Scope In

This task may touch:

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- L0 gate-tuning evaluation or maintenance scripts, preferably by reusing existing scripts
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

This task may change:

- gate keyword families
- gate low-cost structural cues
- trigger conditions for `possible_challenge_surface` / `possible_gate_or_evasion`
- gate routing reason codes
- explainable gate score fields and score reasons
- small-batch gate tuning evaluation commands or scripts
- L0 design documentation for gate specialization

## 4. Scope Out

This task must not:

- modify the current three-family L0 specialization scope; only `gate` is in scope
- reintroduce `possible_fake_verification` or `possible_interaction_required` as L0 output contracts
- read full HTML by default
- perform default brand extraction
- consume screenshot/OCR by default
- introduce heavy model, LLM, browser interaction, click-through recovery, or gate solving
- change gambling/adult trigger policy except to fix a direct conflict introduced by this task
- modify training modules, data schema, or frozen label semantics
- add third-party dependencies

## 5. Inputs

Docs / code:

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- existing L0 specialized evaluation / benchmark scripts or handoffs
- current available gate sample pool, benign pool, gambling control pool, and adult control pool

Missing inputs:

- The latest gate sample-pool path must be confirmed from the repo or `E:\WardenData` during execution.
- If there are not enough gate true-positive / false-negative samples, output a gap report instead of fabricating recall claims.

## 6. Required Outputs

- current gate baseline statistics
- gate FN mining results, especially `matched_keywords = []` or weak-support misses
- gate FP mining results, especially benign / ordinary page false triggers
- low-cost gate evidence proposal
- if implementation proceeds: updated gate detector / score / routing logic
- gate / gambling / adult / benign control-set regression results
- updated L0 gate documentation
- handoff document

## 7. Hard Constraints

- Use only current L0-allowed low-cost inputs.
- Prefer explainable scoring over any black-box classifier.
- Gate scoring must separate at least these evidence families:
  - strong challenge text
  - URL gate hint
  - short-flow / loading-flow text
  - identity / verification-flow text
  - captcha / anti-bot evidence from existing cheap evasion signals
  - dynamic / empty visible text observability support
- Score reasons must be traceable to concrete evidence families.
- Any new output field must be backward compatible and explicitly reported in the handoff.
- Do not improve recall by broadly matching ordinary login / security / verification text.

## 8. Interface / Schema Constraints

- Schema changed allowed: `additive only`
- Candidate additive fields:
  - `gate_weighted_score`
  - `gate_weighted_score_reasons`
  - `gate_score_evidence`
- Existing fields that must remain:
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - `specialized_fast_resolution_candidate`
- If no new fields are added, the handoff must explain why.
- The legacy auto-label compatibility entrypoint must remain runnable.

## 9. Suggested Execution Plan

1. Read the current L0 gate implementation and legacy keyword source.
2. Locate the current gate sample pool, benign control pool, gambling control pool, and adult control pool.
3. Run the current baseline and collect `possible_gate_or_evasion`, `possible_challenge_surface`, matched keyword buckets, routing reasons, and latency.
4. Mine gate FNs, focusing on samples that appear to be gate but have `matched_keywords.gate_text = []`.
5. Mine gate FPs, separating ordinary login/security/verification pages from true challenge/gate pages.
6. Design a low-cost gate score and reason-code policy without heavy evidence.
7. Implement the smallest valid patch.
8. Run small-batch regression across gate / benign / gambling / adult.
9. Update L0 docs and task status.
10. Produce the handoff.

## 10. Acceptance Criteria

- current baseline is measured and recorded in the handoff
- gate FN / FP causes are categorized
- gate tuning does not introduce full HTML, brand extraction, screenshot/OCR, or heavy interaction
- gate outputs remain weak-signal / routing-hint outputs
- gate recall improves explainably, or insufficient sample / low-cost evidence limits are stated explicitly
- benign, gambling, and adult controls show no obvious regression
- `specialized_fast_resolution_candidate` gate semantics are not silently widened into final judgment
- docs and implementation remain aligned
- handoff is complete

## 11. Validation Checklist

- Python syntax check:
  - `python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- gate-focused baseline / after comparison
- benign-control false-positive check
- gambling/adult-control no-regression check
- key-field spot check:
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - any new gate score fields
- latency spot check if matching logic changes materially

## 12. Handoff Requirements

- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

## 13. Open Questions / Blocking Issues

- Confirm the current gate sample-pool path and sample count during execution.
