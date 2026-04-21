# Adult moved-55 spot-check and lost-44 review task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于复核上一条 adult cleanup / tightening 任务的分析质量。
- 本任务只做分析与文档交付，不改代码、不改数据池、不改 schema。
- 重点分两部分：
  - 抽样复核这 `55` 个 moved contamination samples 的质量；
  - 专门审查掉出去的 `44` 个 adult 样本。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-20-ADULT-MOVED55-SPOTCHECK-AND-LOST44-REVIEW`
- 任务标题：`复核 moved 55 样本质量并审查 lost 44 adult 样本`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`；`docs/workflow/GPT_CODEX_WORKFLOW.md`；`docs/templates/TASK_TEMPLATE.md`；`docs/templates/HANDOFF_TEMPLATE.md`；`docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- 创建日期：`2026-04-20`
- 提出人：`User`

## 1. 背景

上一条任务中，adult 路径完成了两轮 benign 池清理和一轮更窄的 adult L0 tightening：

- moved contamination samples: `55`
- stricter rule 下掉出去的 adult samples: `44`

在继续任何 recall recovery 或进一步策略决策前，先复核这两部分质量是必要的：

- moved 的 `55` 个样本到底有多少看起来确实该移出 ordinary benign；
- 掉出去的 `44` 个 adult 样本主要是什么类型，是否存在值得回收的明显高特征页。

## 2. 目标

对 moved 的 `55` 个 contamination samples 做一轮 focused spot-check，评估当前 rebucketing 质量；同时专看 stricter adult rule 下掉出去的 `44` 个 adult samples，归纳其主要丢失模式，并判断是否值得后续单开 narrow recall recovery。

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

This task is allowed to change:

- task / handoff docs
- analysis summary content
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- move any additional dataset directories
- retune `adult`, `gambling`, or `gate`
- rename files, schema fields, or CLI flags
- add dependencies

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- moved `55` sample directories now under `E:\Warden\data\raw\benign\hard benign\adult`
- the `44` adult samples reported as dropped under the stricter rule
- current per-sample outputs from `derive_auto_labels_from_sample_dir`

### Prior Handoff

- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one spot-check summary for the moved `55` contamination samples
- one dropped-pattern review for the lost `44` adult samples
- one recommendation on whether narrow recall recovery is justified
- one repo handoff document

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

- do not patch logic in this task
- make clear where conclusions come from spot-checks versus full-list pattern review
- keep the moved-sample review focused and auditable instead of pretending to fully human-label all 55 samples

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- future adult recall-recovery work
- future adult contamination cleanup review

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the moved-55 and lost-44 facts from the prior handoff
- sample the moved-55 set intentionally rather than randomly if that yields better coverage
- summarize dominant lost-44 patterns, not just raw filenames

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] a focused moved-55 spot-check is documented
- [x] the dominant lost-44 patterns are documented
- [x] a clear recommendation is given on whether recall recovery should be reopened

## 11. Validation Checklist

Minimum validation expected:

- [x] moved-55 sample list assembled
- [x] lost-44 sample list assembled
- [x] spot-check evidence captured
- [x] handoff produced

Commands to run if applicable:

```bash
python - <<'PY'
# assemble moved-55 and lost-44 lists, inspect sample evidence, and summarize patterns
PY
```

Expected evidence to capture:

- spot-check sample names and observations
- dominant lost-44 pattern buckets
- recall-recovery recommendation

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-20-ADULT-MOVED55-SPOTCHECK-AND-LOST44-REVIEW`
- Task Title: `Review moved-55 sample quality and inspect the lost-44 adult samples`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- Created At: `2026-04-20`
- Requested By: `User`

Use this task to quality-check the `55` moved contamination samples from the previous adult cleanup / tightening task and to inspect the `44` adult samples that dropped out under the stricter adult rule.

## 1. Background

The previous adult task completed two benign-pool cleanup moves and one narrower adult L0 tightening:

- moved contamination samples: `55`
- dropped adult samples under the stricter rule: `44`

Before any recall-recovery decision is made, both sides should be reviewed:

- how many of the moved `55` samples really look directionally correct as contamination removals from ordinary benign;
- what kinds of adult samples make up the dropped `44`, and whether any clearly merit a narrow recall recovery.

## 2. Goal

Run a focused spot-check over the moved `55` contamination samples to assess the current rebucketing quality, then inspect the dropped `44` adult samples to summarize the dominant lost patterns and decide whether reopening a narrow recall-recovery task is justified.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

This task is allowed to change:

- task / handoff docs
- analysis summary content
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- move any additional dataset directories
- retune `adult`, `gambling`, or `gate`
- rename files, schema fields, or CLI flags
- add dependencies

## 5. Inputs

Relevant inputs for this task:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- moved `55` sample directories now under `E:\Warden\data\raw\benign\hard benign\adult`
- the `44` adult samples reported as dropped under the stricter rule
