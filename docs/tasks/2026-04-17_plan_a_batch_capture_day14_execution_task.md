# 2026-04-17_plan_a_batch_capture_day14_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-17` Plan A Day 14 抓取队列的任务定义。
- 当前日常口径继续是 benign-only、每天 `3` 批。
- 若涉及精确批次、输出根目录、推荐命令或优先级理由，以英文版为准。

## 1. 背景

Day 13 已在当前线程中按回传事实收口为 `results_received`。
Day 13 已经用完补回的 `top_1_10000_batch_0005` 和 `batch_0006`，`top_500001_1000000` 也早已耗尽。
在当前剩余 benign inventory 中，最高优先级且未分配的批次就是：

- `tranco_top_10001_100000_batch_0004`
- `tranco_top_10001_100000_batch_0005`
- `tranco_top_10001_100000_batch_0006`

## 2. 目标

冻结 `2026-04-17` Day 14 的 benign-only 三批队列，明确批次、输出根目录和推荐命令，并同步更新 tracker。

## 3. 范围

- 纳入：Day 14 execution task、对应 vm-prep handoff、tracker 同步
- 排除：capture 代码逻辑、Day 13 之外的结果复盘、malicious 队列、额外 inventory 重排

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY14-V1
- Task Title: Freeze the 2026-04-17 Plan A Day 14 benign-only queue at three batches per day
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/tasks/2026-04-17_plan_a_batch_capture_day13_result_receipt_task.md`; `docs/handoff/2026-04-17_plan_a_batch_capture_day13_result_receipt.md`; `docs/tasks/2026-04-16_plan_a_batch_capture_day13_execution_task.md`; `docs/handoff/2026-04-16_plan_a_batch_capture_day13_vm_prep.md`
- Created At: 2026-04-17
- Requested By: user

---

## 1. Background

Plan A continues on the benign-only daily cadence of exactly `3` benign batches per day.
In the current thread, Day 13 has been closed from `selected` to `results_received` for continuity purposes.

Day 13 already consumed the restored `top_1_10000` replenishment headroom:

- `tranco_top_1_10000_batch_0005`
- `tranco_top_1_10000_batch_0006`

The `top_500001_1000000` tranche was already exhausted earlier at `batch_0006`.
Given the remaining current benign inventory, the highest-priority unassigned benign batches now available are:

- `tranco_top_10001_100000_batch_0004`
- `tranco_top_10001_100000_batch_0005`
- `tranco_top_10001_100000_batch_0006`

The user also confirmed that the split files for those three batches already exist under `E:\Warden\tranco csv\`.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-17 Plan A Day 14 queue.
This task must freeze:

- the exact `3` benign batches assigned to Day 14,
- the exact output roots for each batch,
- the exact recommended benign runner command pattern for Day 14,
- and the matching tracker update while preserving the benign-only daily planning semantics.

The intended 2026-04-17 Day 14 queue is:

- benign:
  - `tranco_top_10001_100000_batch_0004`
  - `tranco_top_10001_100000_batch_0005`
  - `tranco_top_10001_100000_batch_0006`

No malicious batches are assigned to Day 14.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 14
- tracker continuity docs
- operator command examples for Day 14

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not reopen Day 13 receipt closure
- do not schedule malicious batches for Day 14
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-17 queue has already been executed

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
- `docs/tasks/2026-04-17_plan_a_batch_capture_day13_result_receipt_task.md`
- `docs/handoff/2026-04-17_plan_a_batch_capture_day13_result_receipt.md`
- `docs/tasks/2026-04-16_plan_a_batch_capture_day13_execution_task.md`
- `docs/handoff/2026-04-16_plan_a_batch_capture_day13_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_10001_100000_batch_0004_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0005_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0006_urls.txt`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-17 Day 14 queue
- a repo prep/handoff doc with exact commands and output roots for Day 14
- a tracker update row for Day 14 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 14 must be benign-only.
- Day 14 must contain exactly `3` benign batches.
- Use the current hardened benign runner command pattern with:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`
- Be explicit that Day 14 starts after Day 13 consumed the restored `top_1_10000` `batch_0005` and `batch_0006`.
- Be explicit that `top_500001_1000000` remains exhausted.
- Be explicit that Day 14 therefore consumes the current highest-priority remaining benign inventory from `top_10001_100000`.

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

1. Preserve Day 13 as `results_received` based on the current receipt closure docs.
2. Create a new 2026-04-17 task boundary for Day 14.
3. Freeze the `3`-batch benign-only queue for Day 14.
4. Freeze exact supervised commands and output roots for Day 14.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 14 uses no malicious batches.
- Day 14 continues benign-only daily planning at exactly `3` batches.
- Day 14 uses `top_10001_100000_batch_0004`, `batch_0005`, and `batch_0006` because they are the highest-priority remaining unassigned benign batches after Day 13.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-17 Day 14 queue has its own repo task doc
- [ ] the doc freezes the exact `3` benign batches listed above
- [ ] the doc states that Day 14 has no malicious queue
- [ ] the doc explains why `top_10001_100000_batch_0004` through `batch_0006` are used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] Day 13 remains `results_received`
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local split filenames exist and match the doc
- [ ] referenced runner scripts still expose the required CLI flags or sub-flags
- [ ] tracker row for Day 14 was added
- [ ] Day 13 tracker status now reads `results_received`

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Where-Object { $_.Name -in @('tranco_top_10001_100000_batch_0004_urls.txt','tranco_top_10001_100000_batch_0005_urls.txt','tranco_top_10001_100000_batch_0006_urls.txt') } | Select-Object -ExpandProperty Name
```

Expected evidence to capture:

- confirmed input filenames for the Day 14 queue
- exact output roots for the Day 14 queue
- exact recommended commands for the Day 14 queue
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

- `docs/handoff/2026-04-17_plan_a_batch_capture_day14_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
