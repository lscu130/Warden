# 2026-04-24_plan_a_batch_capture_day17_supplement_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-24` Plan A Day 17 的 benign 补量任务定义。
- 用户最新要求把最后一个剩余 Tranco 批次也补到 Day 17，所以 Day 17 从单批补量更新为双批补量。
- Day 17 仍是 benign-only，不安排 malicious 批次。
- 若涉及精确批次、输出根目录、推荐命令或剩余 inventory 状态，以英文版为准。

### 当前结论

- Day 17 批次：
  - `tranco_top_100001_500000_batch_0015`
  - `tranco_top_100001_500000_batch_0016`
- 输出根目录使用 `E:\WardenData\raw\benign\tranco\...`。
- Day 17 排完后，当前 repo-local Tranco benign split inventory 已全部分配。

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY17-SUPPLEMENT-V2
- Task Title: Freeze the 2026-04-24 Plan A Day 17 final two-batch benign supplement queue
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`; `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`
- Created At: 2026-04-24
- Requested By: user

---

## 1. Background

Day 17 was first documented as a one-batch supplement using:

- `tranco_top_100001_500000_batch_0015`

The user then explicitly requested that the last remaining Tranco batch also be added to Day 17.
That changes the Day 17 supplement boundary from one batch to two batches.

Before this update, the only remaining unqueued repo-local Tranco benign split was:

- `tranco_top_100001_500000_batch_0016`

This task updates Day 17 to consume that final remaining split.

---

## 2. Goal

Freeze the 2026-04-24 Plan A Day 17 benign-only supplement queue as a final two-batch queue.
The queue is:

- benign:
  - `tranco_top_100001_500000_batch_0015`
  - `tranco_top_100001_500000_batch_0016`

No malicious batches are assigned to Day 17.
After this Day 17 queue is selected, the current repo-local Tranco benign split inventory is fully allocated.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md`
- `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`

This task is allowed to change:

- the Day 17 batch list from one benign batch to two benign batches
- the Day 17 output-root mapping
- the Day 17 recommended benign runner commands
- the Plan A tracker continuity notes
- the repo documentation describing the Tranco benign selection strategy

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not close Day 16 receipt state in this turn
- do not close Day 17 receipt state before returned artifacts exist
- do not schedule malicious batches for Day 17
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-24 Day 17 queue has already been executed
- do not create new Tranco split files

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
- `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_100001_500000_batch_0015_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0016_urls.txt`

### Missing Inputs

- returned Day 17 `benign_capture_run.json` files are not available yet
- Day 16 receipt closure remains out of scope in this turn

---

## 6. Required Outputs

This task should produce:

- an updated Day 17 repo task doc freezing both final benign Tranco batches
- an updated Day 17 prep/handoff doc with exact commands and output roots for both batches
- a tracker update that records both Day 17 batches
- a repo Markdown strategy doc explaining how Tranco benign batches are chosen and why that strategy is used

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

- Day 17 must be benign-only.
- Day 17 must contain exactly `2` benign batches after this update.
- Day 17 must continue using repo-local Tranco split files.
- Use the current hardened benign runner command pattern with:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`
- Document that the current repo-local Tranco benign split inventory is fully allocated after Day 17.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py` CLI
- current capture script CLI
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
- downstream benign sample reconciliation after deduplication

---

## 9. Suggested Execution Plan

Recommended order:

1. Preserve Day 16 and Day 17 receipt states as `selected`.
2. Update the Day 17 task boundary from one-batch supplement to final two-batch supplement.
3. Add `tranco_top_100001_500000_batch_0016` to the Day 17 queue.
4. Freeze exact command and output root for both Day 17 batches.
5. Update the Plan A batch tracker in the same turn.
6. Add a strategy document explaining the Tranco benign selection policy.

Task-specific execution notes:

- Day 17 uses no malicious batches.
- Day 17 consumes the final remaining repo-local Tranco benign split.
- The strategy document should describe rank-priority ordering, no-reuse discipline, daily cap exceptions, and why Tranco is suitable for benign capture.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-24 Day 17 supplement task doc lists both final benign batches
- [ ] the Day 17 handoff provides exact output roots and commands for both batches
- [ ] the tracker Day 17 row lists both final benign batches
- [ ] tracker notes no longer say `batch_0016` remains unqueued
- [ ] a Tranco benign selection strategy Markdown doc exists
- [ ] the strategy doc explains why Tranco is used for benign selection
- [ ] no code behavior changed
- [ ] no schema / interface change was introduced
- [ ] validation was run or explicitly caveated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local split filenames exist and match the docs
- [ ] referenced runner scripts still expose the required CLI flags or sub-flags
- [ ] tracker Day 17 row lists both batches
- [ ] no tracker note still states `batch_0016` is unqueued after Day 17
- [ ] strategy doc exists and contains the intended selection rationale

Commands to run if applicable:

```powershell
Test-Path -LiteralPath 'E:\Warden\tranco csv\tranco_top_100001_500000_batch_0016_urls.txt'
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
rg "current repo-local Tranco benign split inventory is fully allocated|tranco_top_100001_500000_batch_0016" E:\Warden\docs\modules\Warden_PLAN_A_BATCH_TRACKER.md E:\Warden\docs\tasks\2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md E:\Warden\docs\handoff\2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md E:\Warden\docs\modules\Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md
```

Expected evidence to capture:

- confirmed input filenames for both Day 17 supplement batches
- exact output roots for both Day 17 supplement batches
- exact recommended commands for both Day 17 supplement batches
- tracker update evidence
- strategy doc presence and content spot-check

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

Repo handoff path:

- `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
