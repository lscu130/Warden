# 2026-03-30_plan_a_batch_capture_day6_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-30` Plan A Day 6 抓取队列的任务定义。
- 若涉及精确批次规模、输出根目录、命令参数或日间边界，以英文版为准。

## 1. 背景

用户要求直接给出今天的 Day 6 任务，并明确将 malicious 日量从 Day 4 到 Day 5 的 `8` 批退回到 `4` 批。
benign 侧继续沿用既有分层节奏，不改变当前抓取脚本和 supervised skip 默认命令。

## 2. 目标

冻结 `2026-03-30` Day 6 的 malicious / benign 抓取队列，给出可直接执行的批次、输出根目录和推荐命令。

## 3. 范围

- 纳入：Day 6 队列任务定义、对应 vm prep / handoff、tracker 同步
- 排除：历史 Day 1 到 Day 5 结果补录、capture 代码逻辑、malicious/benign 策略重设计

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY6-V1
- Task Title: Freeze the 2026-03-30 Plan A Day 6 queue with malicious volume reduced back to four batches
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`; `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- Created At: 2026-03-30
- Requested By: user

---

## 1. Background

The user requested a new Day 6 queue for today and explicitly asked to reduce malicious daily volume back to `4` batches.
This request overrides the recent Day 4 and Day 5 planning choice that temporarily kept malicious at `8` batches per day.

The benign lane should continue the existing rank-bucket cadence instead of introducing a new sampling rule.
No capture code or runner logic should change as part of this task.

---

## 2. Goal

Create an execution-ready task definition for the 2026-03-30 Plan A Day 6 queue.
This task must freeze:

- the exact malicious and benign batches assigned to Day 6,
- the exact output roots for each batch,
- and the exact supervised skip-capable commands that remain the recommended default commands.

The intended 2026-03-30 Day 6 queue is:

- malicious: `phishtank_2026_only_batch_0029` to `phishtank_2026_only_batch_0032` inclusive
- benign:
  - `tranco_top_100001_500000_batch_0003`
  - `tranco_top_500001_1000000_batch_0003`

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 6
- tracker continuity docs
- operator command examples for Day 6

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite historical Day 1 to Day 5 artifacts
- do not change capture code or runner behavior
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-03-30 queue has already been executed

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
- `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`
- `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `phishtank csv/phishtank_2026_only_batch_0029_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0030_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0031_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0032_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0003_urls.txt`
- `tranco csv/tranco_top_500001_1000000_batch_0003_urls.txt`

### Missing Inputs

- actual returned artifacts from Day 1 to Day 5 are still not fully recorded here and must not be fabricated

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-03-30 Day 6 queue
- a repo prep/handoff doc with exact commands and output roots for Day 6
- a tracker update row for Day 6 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Keep Day 1 to Day 5 queue artifacts frozen as historical context.
- Use new output roots for the 2026-03-30 queue so lineage remains auditable.
- Use the current supervised skip-capable commands as the recommended default commands for Day 6.
- Reduce malicious Day 6 back to `4` batches because the user explicitly requested that queue change.
- Keep the benign lane on the existing alternating rank-bucket cadence.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py` CLI
- `scripts/data/malicious/run_malicious_capture.py` CLI
- current output-root naming discipline

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current benign runner commands
  - current malicious runner commands
  - current capture script commands

Downstream consumers to watch:

- operators resuming or auditing Plan A batch lineage
- later day-wise handoff writing
- the Plan A batch tracker

---

## 9. Suggested Execution Plan

Recommended order:

1. Keep Day 1 to Day 5 docs as frozen historical context.
2. Create a new 2026-03-30 task boundary for Day 6.
3. Freeze the 4-batch malicious queue and the 2-batch benign queue for Day 6.
4. Freeze exact supervised commands and output roots for Day 6.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- malicious Day 6 starts from `batch_0029` and ends at `batch_0032`
- benign Day 6 uses the next lower-rank pair in the existing cadence
- both lanes should use supervised skip-capable commands by default

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-03-30 Day 6 queue has its own repo task doc
- [ ] the doc freezes malicious `batch_0029` to `batch_0032`
- [ ] the doc freezes benign `top_100001_500000_batch_0003` and `top_500001_1000000_batch_0003`
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local batch filenames exist and match the doc
- [ ] referenced runner scripts still expose the required supervised flags
- [ ] tracker row for Day 6 was added

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
python scripts/data/malicious/run_malicious_capture.py --help
```

Expected evidence to capture:

- confirmed input filenames for the Day 6 queue
- exact output roots for the Day 6 queue
- exact supervised commands for the Day 6 queue
- tracker update evidence
