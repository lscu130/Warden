# Adult post-cleanup metrics rerun task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于在 benign 池完成清理后，重新计算当前 `adult` 的 ordinary-benign 误触统计和代理 precision / recall。
- 本任务只做统计复算和文档交付，不改代码、不改规则、不改 schema。
- 默认使用当前工作树下的 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 和当前数据根目录。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-17-ADULT-POST-CLEANUP-METRICS-RERUN`
- 任务标题：`重跑 adult 在清理后 benign 池上的误触统计`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`；`docs/workflow/GPT_CODEX_WORKFLOW.md`；`docs/templates/TASK_TEMPLATE.md`；`docs/templates/HANDOFF_TEMPLATE.md`；`docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`
- 创建日期：`2026-04-17`
- 提出人：`User`

## 1. 背景

上一条任务已把 `78` 个 `likely screening miss / pool contamination` 样本从 `E:\Warden\data\raw\benign\benign` 移到 `E:\Warden\data\raw\benign\hard benign\adult`。清理完成后，之前的 ordinary-benign adult 误触统计已经过时。

现在需要基于清理后的 benign 池重新计算：

- ordinary-benign 上的 `possible_adult_lure` 误触数和误触率
- adult pool 上的 `possible_adult_lure` 命中数和 recall proxy
- 由这两组池子推导出的 precision proxy

## 2. 目标

使用当前工作树下的 adult labeling 逻辑，对清理后的 `E:\Warden\data\raw\benign\benign` 与当前 `E:\Warden\data\raw\benign\hard benign\adult` 重新做一轮同口径统计，产出新的 adult ordinary-benign false-positive 指标、adult recall proxy、precision proxy，并记录与清理前的差异。

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

This task is allowed to change:

- task / handoff docs
- metric summary content for the rerun
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- retune `adult`, `gambling`, or `gate`
- move additional dataset directories
- rename files, schema fields, or CLI flags
- add dependencies

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- current `possible_adult_lure` outputs from the working-tree labeling logic

### Prior Handoff

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one repo task doc for the rerun
- one quantified metric summary for cleaned benign vs adult pool
- one repo handoff document
- explicit compatibility notes confirming no logic change

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

- do not change adult logic during this task
- keep metric computation on the same signal: `possible_adult_lure`
- make clear that the result is still a proxy metric based on current pool composition

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
  - current adult evaluation snippets

Downstream consumers to watch:

- future adult precision analysis
- future adult precision-tightening work

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the current working-tree adult labeling logic without patching it
- recompute both pool counts and derived proxy metrics
- compare the cleaned-pool result against the last reported pre-cleanup baseline

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

- [x] cleaned benign pool ordinary-benign false-positive count is recomputed
- [x] adult pool recall proxy is recomputed
- [x] precision proxy is recomputed and reported
- [x] no code or dataset move is mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [x] current labeling entry point check
- [x] cleaned benign pool metric rerun
- [x] adult pool metric rerun
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# recompute adult-pool and cleaned ordinary-benign metrics using current working-tree logic
PY
```

Expected evidence to capture:

- cleaned benign total count and `possible_adult_lure` hit count
- adult total count and `possible_adult_lure` hit count
- updated precision / recall proxies

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

- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-17-ADULT-POST-CLEANUP-METRICS-RERUN`
- Task Title: `Rerun adult false-positive statistics on the cleaned benign pool`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`
- Created At: `2026-04-17`
- Requested By: `User`

Use this task to recompute current `adult` proxy metrics after the benign-pool cleanup moved `78` likely adult-contamination samples out of `E:\Warden\data\raw\benign\benign`.

## 1. Background

The previous cleanup task moved `78` samples from `E:\Warden\data\raw\benign\benign` into `E:\Warden\data\raw\benign\hard benign\adult`. After that cleanup, the previously reported ordinary-benign adult false-positive statistics are stale.

The current rerun needs to recompute:

- ordinary-benign `possible_adult_lure` false-positive count and rate
- adult-pool `possible_adult_lure` hit count and recall proxy
- the resulting precision proxy derived from those two pools

## 2. Goal

Use the current working-tree adult labeling logic to rerun the same-scope statistics on the cleaned `E:\Warden\data\raw\benign\benign` pool and the current `E:\Warden\data\raw\benign\hard benign\adult` pool, then report the new adult ordinary-benign false-positive metrics, adult recall proxy, precision proxy, and the difference relative to the last pre-cleanup baseline.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

This task is allowed to change:

- task / handoff docs
- metric summary content for the rerun
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- retune `adult`, `gambling`, or `gate`
- move additional dataset directories
- rename files, schema fields, or CLI flags
- add dependencies

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- current `possible_adult_lure` outputs from the working-tree labeling logic

### Prior Handoff

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one repo task doc for the rerun
- one quantified metric summary for cleaned benign vs adult pool
- one repo handoff document
- explicit compatibility notes confirming no logic change

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

- do not change adult logic during this task
- keep metric computation on the same signal: `possible_adult_lure`
- make clear that the result is still a proxy metric based on current pool composition

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
