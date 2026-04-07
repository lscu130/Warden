# 2026-03-27_plan_a_batch_capture_tracker_setup

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Plan A 日常批次追踪文档的建立任务。
- 若涉及精确文档路径、追踪字段或更新规则，以英文版为准。

## 1. 背景

Day 1 到 Day 5 的计划文档已经逐日新增，但当前仓库里还缺一份统一的、持续更新的 tracker 文档，专门记录“每天已经选定要跑哪些批次”。
用户明确要求新增这样一份独立 md，并要求后续每次新建新一天的任务时都同步更新它。

## 2. 目标

新增一个单独的 Plan A batch tracker 文档，回填当前 Day 1 到 Day 5 的已选批次，并把后续更新规则写清楚。

## 3. 范围

- 纳入：tracker 文档、对应 task / handoff
- 排除：既有日任务重写、capture 代码逻辑、历史结果改写

## English Version

# Task Metadata

- Task ID: WARDEN-PLAN-A-BATCH-TRACKER-SETUP-V1
- Task Title: Add a living Plan A batch tracker document that records which daily malicious and benign batches have already been selected to run
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module / operator planning docs
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`; `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`; `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`; `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`; `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`
- Created At: 2026-03-27
- Requested By: user

---

## 1. Background

Plan A daily queue docs already exist for Day 1 through Day 5, but the repository does not yet contain a single living tracker document that records which batches have already been selected for each day.
The user explicitly requested a separate md for this purpose and required that future new-day task creation should update that tracker as part of the workflow.

---

## 2. Goal

Add one durable Plan A batch tracker document that:

- records the currently selected Day 1 through Day 5 malicious and benign batch sets,
- points back to the corresponding day-level task/prep docs,
- states that future new-day task creation must update this tracker.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- additive operator-planning documentation
- additive batch-tracker documentation

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite prior day queue definitions
- do not modify capture code or runner behavior
- do not fabricate run-result status for any day
- do not treat “selected to run” as “confirmed completed”

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`
- `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`
- `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`
- `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`
- related day-level VM prep handoffs

### Code / Scripts

- none

### Data / Artifacts

- none

### Prior Handoff

- day-level Plan A prep handoffs for Day 1 to Day 5

### Missing Inputs

- actual Day 1 to Day 5 returned artifacts are still pending and must not be invented

---

## 6. Required Outputs

This task should produce:

- a living Plan A batch tracker markdown document
- a repo task doc
- a repo handoff doc

---

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

Task-specific constraints:

- The tracker must distinguish “selected to run” from “returned results received”.
- The tracker must backfill Day 1 to Day 5 from existing repo docs only.
- Future update responsibility must be written explicitly inside the tracker.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing day-level task docs
- existing day-level prep handoffs

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none

Downstream consumers to watch:

- operator planning and daily queue continuity across threads

---

## 9. Suggested Execution Plan

Recommended order:

1. Read Day 1 through Day 5 task/prep docs.
2. Extract the selected malicious and benign batch sets for each day.
3. Create one living tracker markdown file under `docs/modules/`.
4. State future update rules explicitly in that tracker.
5. Produce the corresponding handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] a single tracker md exists in the repo
- [ ] Day 1 to Day 5 selected batch sets are backfilled
- [ ] the tracker distinguishes planning selection from actual returned results
- [ ] the tracker states that future new-day task creation must update it
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] Day 1 to Day 5 selections were copied from existing repo docs
- [ ] tracker paths and day references are consistent
- [ ] no run-result claims were fabricated

Commands to run if applicable:

```bash
inspect existing Day 1 to Day 5 task and prep docs
inspect the final tracker markdown
```

Expected evidence to capture:

- one tracker file path
- backfilled Day 1 to Day 5 rows
- explicit future update rule
