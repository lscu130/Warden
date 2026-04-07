# 2026-04-08_plan_a_batch_capture_day11_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-08` Plan A Day 11 抓取队列的任务定义。
- 当前日常口径仍是“只跑 benign，每天 3 批”。
- 若涉及精确批次、输出根目录、命令参数或日间边界，以英文版为准。

## 1. 背景

Day 7 到 Day 10 已经进入 benign-only、每天 3 批的新日常口径。用户现在要求在保留 Day 10 为 `results_pending` 的前提下，继续把 Day 11 排出来。

当前仓库里的 Tranco 已划分批次仍然缺少 `top_1_10000_batch_0005`；同时 `top_500001_1000000` 也已经在 Day 10 用到 `batch_0006`，当前本地 split 不再有后续新批次。因此 Day 11 不能继续沿用前三天那种“三个不同 bucket 各拿一批”的排法，只能从仍有余量的更高优先级 benign bucket 里继续取 3 批。

## 2. 目标

冻结 `2026-04-08` Day 11 的 benign-only 抓取队列，给出可直接执行的 3 个 benign 批次、输出根目录和推荐命令，并同步更新 tracker。

## 3. 范围

- 纳入：Day 11 队列任务定义、对应 vm prep / handoff、tracker 同步
- 排除：capture 代码逻辑、Day 10 结果收口、malicious 队列、cluster / pool、历史样本重算

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY11-V1
- Task Title: Freeze the 2026-04-08 Plan A Day 11 benign-only queue at three batches per day
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`; `docs/tasks/2026-04-07_plan_a_batch_capture_day10_execution_task.md`; `docs/handoff/2026-04-07_plan_a_batch_capture_day10_vm_prep.md`
- Created At: 2026-04-07
- Requested By: user

---

## 1. Background

Day 7 through Day 10 already established the benign-only steady-state with exactly `3` benign batches per day.
The user now requested that Day 11 should be queued without pretending that Day 10 has already completed; Day 10 must remain `results_pending` until its returned artifacts are actually provided.

Within the currently available repo-local Tranco split, `tranco_top_1_10000_batch_0005_urls.txt` is still absent.
Also, the current `top_500001_1000000` queue is exhausted at `batch_0006`, which was already assigned to Day 10.
That means Day 11 cannot continue the recent one-batch-per-bucket pattern and must instead continue with the next `3` available benign batches that preserve rank priority among the remaining buckets.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-08 Plan A Day 11 queue.
This task must freeze:

- the exact `3` benign batches assigned to Day 11,
- the exact output roots for each batch,
- the exact supervised skip-capable commands that remain the recommended default commands,
- and the matching tracker update while preserving Day 10 as `results_pending`.

The intended 2026-04-08 Day 11 queue is:

- benign:
  - `tranco_top_10001_100000_batch_0013`
  - `tranco_top_10001_100000_batch_0014`
  - `tranco_top_100001_500000_batch_0008`

No malicious batches are assigned to Day 11.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 11
- tracker continuity docs
- operator command examples for Day 11

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not mark Day 10 as completed or `results_received`
- do not schedule malicious batches for Day 11
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-08 queue has already been executed

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
- `docs/tasks/2026-04-07_plan_a_batch_capture_day10_execution_task.md`
- `docs/handoff/2026-04-07_plan_a_batch_capture_day10_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_10001_100000_batch_0013_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0014_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0008_urls.txt`

### Missing Inputs

- no new malicious artifacts are required for Day 11 because malicious is intentionally out of scope for this day
- no `tranco_top_1_10000_batch_0005_urls.txt` exists in the current repo-local split
- no new `top_500001_1000000` batch remains after `tranco_top_500001_1000000_batch_0006_urls.txt`

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-08 Day 11 queue
- a repo prep/handoff doc with exact commands and output roots for Day 11
- a tracker update row for Day 11 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 11 must be benign-only.
- Day 11 must contain exactly `3` benign batches.
- Use the current supervised skip-capable commands as the recommended default commands for Day 11.
- Be explicit that Day 11 still cannot use `top_1_10000_batch_0005` because that file remains absent in the current split.
- Be explicit that Day 11 cannot use a new `top_500001_1000000` batch because the current repo-local queue is exhausted at `batch_0006`.
- Keep rank priority explicit: continue with the highest-value remaining benign batches instead of inventing a new lower-priority bucket source.

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

1. Preserve Day 10 as `results_pending` because no returned Day 10 artifact package has been provided yet.
2. Create a new 2026-04-08 task boundary for Day 11.
3. Freeze the `3`-batch benign-only queue for Day 11.
4. Freeze exact supervised commands and output roots for Day 11.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 11 uses no malicious batches
- Day 11 selects `3` benign batches in rank-priority order from the remaining non-exhausted buckets
- `top_10001_100000_batch_0013` and `batch_0014` are both selected before another lower-priority bucket because `top_10001_100000` remains the highest-value available tranche
- `top_500001_1000000` contributes no Day 11 batch because the current local queue is exhausted

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-08 Day 11 queue has its own repo task doc
- [ ] the doc freezes the exact `3` benign batches listed above
- [ ] the doc states that Day 11 has no malicious queue
- [ ] the doc explains why no `top_1_10000` batch is used
- [ ] the doc explains why no `top_500001_1000000` batch is used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] Day 10 remains `results_pending`
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local batch filenames exist and match the doc
- [ ] referenced runner scripts still expose the required supervised flags
- [ ] tracker row for Day 11 was added
- [ ] Day 10 tracker status remains `results_pending`

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

Expected evidence to capture:

- confirmed input filenames for the Day 11 queue
- exact output roots for the Day 11 queue
- exact supervised commands for the Day 11 queue
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

- `docs/handoff/2026-04-08_plan_a_batch_capture_day11_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
