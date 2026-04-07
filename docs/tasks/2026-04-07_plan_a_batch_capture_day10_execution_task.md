# 2026-04-07_plan_a_batch_capture_day10_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-07` Plan A Day 10 抓取队列的任务定义。
- 当前日常口径仍是“只跑 benign，每天 3 批”。
- 若涉及精确批次、输出根目录、命令参数或日间边界，以英文版为准。

## 1. 背景

Day 7 到 Day 9 已经进入 benign-only、每天 3 批的新日常口径。用户现在要求直接给出 Day 10。
在当前仓库里的 Tranco 已划分批次中，`top_1_10000_batch_0005` 仍不存在，因此 Day 10 仍无法继续从该 bucket 取新批次，只能沿用下一个可用的 benign 三批。

## 2. 目标

冻结 `2026-04-07` Day 10 的 benign-only 抓取队列，给出可直接执行的 3 个 benign 批次、输出根目录和推荐命令，并同步更新 tracker。

## 3. 范围

- 纳入：Day 10 队列任务定义、对应 vm prep / handoff、tracker 同步
- 排除：capture 代码逻辑、malicious 队列、cluster / pool、历史样本重算

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY10-V1
- Task Title: Freeze the 2026-04-07 Plan A Day 10 benign-only queue at three batches per day
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`; `docs/tasks/2026-04-03_plan_a_batch_capture_day9_execution_task.md`; `docs/handoff/2026-04-03_plan_a_batch_capture_day9_vm_prep.md`
- Created At: 2026-04-07
- Requested By: user

---

## 1. Background

Day 7 through Day 9 already established the benign-only steady-state with exactly `3` benign batches per day.
The user now requested the next day queue for 2026-04-07.

Within the currently available repo-local Tranco split, `tranco_top_1_10000_batch_0005_urls.txt` is still absent.
That means Day 10 cannot resume a new `top_1_10000` tranche and must instead continue with the next 3 available benign batches.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-07 Plan A Day 10 queue.
This task must freeze:

- the exact 3 benign batches assigned to Day 10,
- the exact output roots for each batch,
- the exact supervised skip-capable commands that remain the recommended default commands,
- and the matching tracker update.

The intended 2026-04-07 Day 10 queue is:

- benign:
  - `tranco_top_10001_100000_batch_0012`
  - `tranco_top_100001_500000_batch_0007`
  - `tranco_top_500001_1000000_batch_0006`

No malicious batches are assigned to Day 10.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 10
- tracker continuity docs
- operator command examples for Day 10

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not schedule malicious batches for Day 10
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-07 queue has already been executed

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
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- `docs/tasks/2026-04-03_plan_a_batch_capture_day9_execution_task.md`
- `docs/handoff/2026-04-03_plan_a_batch_capture_day9_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_10001_100000_batch_0012_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0007_urls.txt`
- `tranco csv/tranco_top_500001_1000000_batch_0006_urls.txt`

### Missing Inputs

- no new malicious artifacts are required for Day 10 because malicious is intentionally out of scope for this day
- no `tranco_top_1_10000_batch_0005_urls.txt` exists in the current repo-local split

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-07 Day 10 queue
- a repo prep/handoff doc with exact commands and output roots for Day 10
- a tracker update row for Day 10 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 10 must be benign-only.
- Day 10 must contain exactly 3 benign batches.
- Use the current supervised skip-capable commands as the recommended default commands for Day 10.
- Be explicit that no `top_1_10000` batch is used on Day 10 because the next expected file is still absent in the current split.

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

1. Mark Day 7 as `results_received` because the returned benign JSON package has now been provided.
2. Create a new 2026-04-07 task boundary for Day 10.
3. Freeze the 3-batch benign-only queue for Day 10.
4. Freeze exact supervised commands and output roots for Day 10.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 10 uses no malicious batches
- Day 10 continues from the next available repo-local Tranco files
- the missing `top_1_10000_batch_0005` tranche is treated as an availability constraint, not as a reason to stop planning

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-07 Day 10 queue has its own repo task doc
- [ ] the doc freezes the exact 3 benign batches listed above
- [ ] the doc states that Day 10 has no malicious queue
- [ ] the doc explains why no `top_1_10000` batch is used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] Day 7 is marked `results_received`
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local batch filenames exist and match the doc
- [ ] referenced runner scripts still expose the required supervised flags
- [ ] tracker row for Day 10 was added
- [ ] Day 7 tracker status was updated to `results_received`

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
```

Expected evidence to capture:

- confirmed input filenames for the Day 10 queue
- exact output roots for the Day 10 queue
- exact supervised commands for the Day 10 queue
- tracker update evidence

