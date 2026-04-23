# 2026-04-22_plan_a_batch_capture_day16_final_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-22` Plan A Day 16 的 benign 目标收尾任务定义。
- 当前约束不是清空剩余 benign inventory，而是再跑 `3` 批后让 benign 总量达到 `20k`。
- 若涉及精确批次、输出根目录、推荐命令或 20k 收尾边界，以英文版为准。

## 1. 背景

当前 tracker 中已冻结到 Day 15。
结合 tracker 已分配批次与 repo-local split 文件，当前未分配的下一个 benign Tranco 批次从 `tranco_top_100001_500000_batch_0012` 开始。

用户刚刚明确补充：这里的“最后一批”含义是再来 `3` 批后 benign 总量达到 `20k`，不是把剩余 benign inventory 全部清空。
因此 Day 16 应继续保持 `3` 批，而不是扩成 `5` 批。

## 2. 目标

冻结 `2026-04-22` Day 16 的 benign-only 收尾队列，覆盖达到 benign `20k` 目标所需的最后 `3` 个 Tranco benign split，明确输出根目录和推荐命令，并在 tracker 中写明该日完成后当前 benign 目标已完成。

## 3. 范围

- 纳入：Day 16 final execution task、对应 vm-prep handoff、tracker 同步
- 排除：capture 代码逻辑、Day 14/Day 15 receipt 收口、malicious 队列、额外 split 生成

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY16-FINAL-V1
- Task Title: Freeze the 2026-04-22 Plan A Day 16 final benign-only queue to reach the 20k benign target
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/tasks/2026-04-21_plan_a_batch_capture_day15_execution_task.md`; `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- Created At: 2026-04-22
- Requested By: user

---

## 1. Background

Plan A has continued under a benign-only daily cadence, and Day 15 already froze the next `3` Tranco benign batches under `top_10001_100000_batch_0007` through `batch_0009`.

When the currently frozen tracker rows are combined with the repo-local Tranco split files, the next unassigned benign Tranco tranche begins at:

- `tranco_top_100001_500000_batch_0012`
- `tranco_top_100001_500000_batch_0013`
- `tranco_top_100001_500000_batch_0014`

The user then clarified the actual stopping rule:
Day 16 should add only `3` more benign batches, because that is sufficient to bring the benign total to `20k`.
So the target is not full inventory exhaustion.

Per the source-of-truth order in `AGENTS.md`, that explicit user request overrides the prior default daily planning rhythm.
So Day 16 must be documented as the final benign target-closure day at `3` batches, with the remaining unqueued `batch_0015` and `batch_0016` left intentionally unused because the benign target is already met.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-22 Plan A Day 16 final benign queue.
This task must freeze:

- the exact final `3` benign Tranco batches assigned to Day 16,
- the exact output roots for each batch,
- the exact recommended benign runner command pattern for the final Day 16 run,
- and the matching tracker update while explicitly documenting that the benign `20k` target is reached after Day 16.

The intended 2026-04-22 Day 16 queue is:

- benign:
  - `tranco_top_100001_500000_batch_0012`
  - `tranco_top_100001_500000_batch_0013`
  - `tranco_top_100001_500000_batch_0014`

No malicious batches are assigned to Day 16.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 16
- tracker continuity docs
- operator command examples for the Day 16 final run

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not close Day 14 or Day 15 receipt state in this turn
- do not schedule malicious batches for Day 16
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-22 queue has already been executed

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
- `docs/tasks/2026-04-21_plan_a_batch_capture_day15_execution_task.md`
- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_100001_500000_batch_0012_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0013_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0014_urls.txt`
### Missing Inputs

- no additional split generation is required for Day 16 queue selection
- Day 14 and Day 15 receipt closure remain out of scope in this turn

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-22 Day 16 final queue
- a repo prep/handoff doc with exact commands and output roots for Day 16
- a tracker update row for Day 16 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 16 must be benign-only.
- Day 16 must contain exactly `3` benign batches.
- Day 16 is the final benign target-closure day because these `3` batches bring benign total volume to `20k`.
- Day 16 must continue using repo-local Tranco split files.
- Use the current hardened benign runner command pattern with:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`
- Be explicit that `batch_0015` and `batch_0016` remain unqueued on purpose because the benign `20k` target is already met after Day 16.

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

1. Preserve Day 14 and Day 15 receipt state as-is in this turn.
2. Create a new 2026-04-22 final task boundary for Day 16.
3. Freeze the final `3`-batch benign-only Tranco queue for Day 16.
4. Freeze exact supervised commands and output roots for the Day 16 final run.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 16 uses no malicious batches.
- Day 16 is the final benign-only queue needed to reach the `20k` benign target.
- Day 16 uses `top_100001_500000_batch_0012` through `batch_0014` because they are the next highest-priority unassigned benign Tranco batches.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-22 Day 16 final queue has its own repo task doc
- [ ] the doc freezes the exact `3` benign batches listed above
- [ ] the doc states that Day 16 has no malicious queue
- [ ] the doc states that Day 16 closes the benign `20k` target
- [ ] the doc explains why `top_100001_500000_batch_0012` through `batch_0014` are used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] the tracker notes that the benign `20k` target is complete after Day 16
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local split filenames exist and match the doc
- [ ] referenced runner scripts still expose the required CLI flags or sub-flags
- [ ] tracker row for Day 16 was added
- [ ] Day 16 is documented as the final queue needed to reach benign `20k`

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Where-Object { $_.Name -in @('tranco_top_100001_500000_batch_0012_urls.txt','tranco_top_100001_500000_batch_0013_urls.txt','tranco_top_100001_500000_batch_0014_urls.txt','tranco_top_100001_500000_batch_0015_urls.txt','tranco_top_100001_500000_batch_0016_urls.txt') } | Select-Object -ExpandProperty Name
```

Expected evidence to capture:

- confirmed input filenames for the Day 16 final queue
- exact output roots for the Day 16 final queue
- exact recommended commands for the Day 16 final queue
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

- `docs/handoff/2026-04-22_plan_a_batch_capture_day16_final_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
