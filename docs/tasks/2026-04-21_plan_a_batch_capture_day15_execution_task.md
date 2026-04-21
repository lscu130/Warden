# 2026-04-21_plan_a_batch_capture_day15_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-21` Plan A Day 15 抓取队列的任务定义。
- 当前日常口径继续是 benign-only、每天 `3` 批，来源继续是 Tranco split。
- 若涉及精确批次、输出根目录、推荐命令或优先级理由，以英文版为准。

## 1. 背景

Day 14 已经在 repo 中冻结为 `tranco_top_10001_100000_batch_0004/0005/0006`。
当前线程里，Day 14 的 repo-local result receipt 还没有完成收口，因此 tracker 先保留 `selected`。
在不重排已冻结队列的前提下，当前剩余最高优先级且未分配的 Tranco benign 批次就是：

- `tranco_top_10001_100000_batch_0007`
- `tranco_top_10001_100000_batch_0008`
- `tranco_top_10001_100000_batch_0009`

## 2. 目标

冻结 `2026-04-21` Day 15 的 Tranco benign-only 三批队列，明确批次、输出根目录和推荐命令，并同步更新 tracker。

## 3. 范围

- 纳入：Day 15 execution task、对应 vm-prep handoff、tracker 同步
- 排除：capture 代码逻辑、Day 14 receipt 收口、malicious 队列、额外 inventory 重排

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY15-V1
- Task Title: Freeze the 2026-04-21 Plan A Day 15 benign-only Tranco queue at three batches per day
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/tasks/2026-04-17_plan_a_batch_capture_day14_execution_task.md`; `docs/handoff/2026-04-17_plan_a_batch_capture_day14_vm_prep.md`
- Created At: 2026-04-21
- Requested By: user

---

## 1. Background

Plan A continues on the benign-only daily cadence of exactly `3` benign batches per day, with the current benign queue still coming from repo-local Tranco split files.

Day 14 already froze the following Tranco benign queue membership:

- `tranco_top_10001_100000_batch_0004`
- `tranco_top_10001_100000_batch_0005`
- `tranco_top_10001_100000_batch_0006`

In this turn, Day 14 is still left as `selected` in the tracker because a full repo-local receipt closure was not completed.
The current workspace exposes the Day 14 `batch_0006` output directory, but not the expected `batch_0004` and `batch_0005` output directories at the exact repo-local paths that were referenced.

Queue planning can still continue safely from the already-frozen membership baseline.
Given the remaining current Tranco benign inventory, the highest-priority unassigned benign batches now available are:

- `tranco_top_10001_100000_batch_0007`
- `tranco_top_10001_100000_batch_0008`
- `tranco_top_10001_100000_batch_0009`

The split files for those three batches exist under `E:\Warden\tranco csv\`.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-21 Plan A Day 15 queue.
This task must freeze:

- the exact `3` Tranco benign batches assigned to Day 15,
- the exact output roots for each batch,
- the exact recommended benign runner command pattern for Day 15,
- and the matching tracker update while preserving the benign-only daily planning semantics.

The intended 2026-04-21 Day 15 queue is:

- benign:
  - `tranco_top_10001_100000_batch_0007`
  - `tranco_top_10001_100000_batch_0008`
  - `tranco_top_10001_100000_batch_0009`

No malicious batches are assigned to Day 15.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 15
- tracker continuity docs
- operator command examples for Day 15

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not close Day 14 receipt state in this turn
- do not schedule malicious batches for Day 15
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-21 queue has already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/tasks/2026-04-17_plan_a_batch_capture_day14_execution_task.md`
- `docs/handoff/2026-04-17_plan_a_batch_capture_day14_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_10001_100000_batch_0007_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0008_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0009_urls.txt`

### Missing Inputs

- no additional inputs are required for Day 15 queue selection
- Day 14 repo-local receipt closure remains incomplete in this turn

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-21 Day 15 queue
- a repo prep/handoff doc with exact commands and output roots for Day 15
- a tracker update row for Day 15 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 15 must be benign-only.
- Day 15 must contain exactly `3` benign batches.
- Day 15 must continue using Tranco split files.
- Use the current hardened benign runner command pattern with:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`
- Be explicit that Day 15 uses `top_10001_100000_batch_0007`, `batch_0008`, and `batch_0009` because they are the highest-priority remaining unassigned Tranco benign batches after the already-frozen Day 14 queue.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py` CLI
- current output-root naming discipline

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current benign runner commands
  - current capture script commands

Downstream consumers to watch:

- operators resuming or auditing Plan A batch lineage
- later benign run-result handoff writing
- the Plan A batch tracker

---

## 9. Suggested Execution Plan

Recommended order:

1. Preserve Day 14 as `selected` until a separate receipt closure is produced.
2. Create a new 2026-04-21 task boundary for Day 15.
3. Freeze the `3`-batch benign-only Tranco queue for Day 15.
4. Freeze exact supervised commands and output roots for Day 15.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 15 uses no malicious batches.
- Day 15 continues benign-only daily planning at exactly `3` batches.
- Day 15 uses `top_10001_100000_batch_0007`, `batch_0008`, and `batch_0009` because Day 14 already froze `batch_0004` through `batch_0006`.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-21 Day 15 queue has its own repo task doc
- [ ] the doc freezes the exact `3` benign batches listed above
- [ ] the doc states that Day 15 has no malicious queue
- [ ] the doc explains why `top_10001_100000_batch_0007` through `batch_0009` are used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] Day 14 remains `selected` in this turn
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local split filenames exist and match the doc
- [ ] referenced runner scripts still expose the required CLI flags or sub-flags
- [ ] tracker row for Day 15 was added
- [ ] Day 14 tracker status remains `selected`

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Where-Object { $_.Name -in @('tranco_top_10001_100000_batch_0007_urls.txt','tranco_top_10001_100000_batch_0008_urls.txt','tranco_top_10001_100000_batch_0009_urls.txt') } | Select-Object -ExpandProperty Name
```

Expected evidence to capture:

- confirmed input filenames for the Day 15 queue
- exact output roots for the Day 15 queue
- exact recommended commands for the Day 15 queue
- tracker update evidence

---

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

- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
