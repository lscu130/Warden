# 2026-04-28_plan_a_batch_capture_day18_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-28` Plan A Day 18 的 benign-only capture 任务定义。
- Day 18 最初只排 `1` 个批次；用户随后要求再补 `2` 个批次。
- 当前 Day 18 队列为 `3` 个 benign 批次：`0017`、`0018`、`0019`。
- 文件名保留 `single_batch` 是为了不打断上一轮已经写入 tracker 的引用；正文里的英文版为当前权威内容。

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY18-THREE-BATCH-V2
- Task Title: Freeze the 2026-04-28 Plan A Day 18 three-batch benign queue
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`
- Created At: 2026-04-28
- Requested By: user

---

## 1. Background

The 2026-04-27 Tranco supplement split generated six additional `top_100001_500000` benign candidate batches:

- `tranco_top_100001_500000_batch_0017` through `tranco_top_100001_500000_batch_0022`

Day 18 was first frozen as a single-batch queue using `batch_0017`.
The user then requested two more Day 18 batches.
Therefore Day 18 is updated to use:

- `tranco_top_100001_500000_batch_0017`
- `tranco_top_100001_500000_batch_0018`
- `tranco_top_100001_500000_batch_0019`

---

## 2. Goal

Freeze the 2026-04-28 Plan A Day 18 queue as a three-batch benign-only Tranco queue:

- benign:
  - `tranco_top_100001_500000_batch_0017`
  - `tranco_top_100001_500000_batch_0018`
  - `tranco_top_100001_500000_batch_0019`

No malicious batches are assigned to Day 18.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md`
- `docs/handoff/2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

This task is allowed to change:

- Day 18 queue planning docs
- Day 18 output-root mapping
- Day 18 recommended benign runner commands
- tracker continuity row and notes

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not close Day 18 receipt state in this turn
- do not schedule malicious batches for Day 18
- do not schedule batches beyond `batch_0019`
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-28 Day 18 queue has already been executed
- do not generate new Tranco split files

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
- `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_100001_500000_batch_0017_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0018_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0019_urls.txt`

### Missing Inputs

- returned Day 18 `benign_capture_run.json` files are not available yet

---

## 6. Required Outputs

This task should produce:

- an updated Day 18 repo task doc
- an updated Day 18 vm-prep handoff with exact commands and output roots
- an updated Day 18 tracker row with status `selected`

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

- Day 18 must be benign-only.
- Day 18 must contain exactly `3` benign batches after this update.
- Day 18 must use `tranco_top_100001_500000_batch_0017`, `batch_0018`, and `batch_0019`.
- Use the current hardened benign runner command pattern with:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`

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

---

## 9. Suggested Execution Plan

Recommended order:

1. Preserve Day 18 receipt state as `selected`.
2. Confirm `batch_0018` and `batch_0019` URL split files exist.
3. Update the Day 18 task and vm-prep docs from one batch to three batches.
4. Update the Plan A batch tracker in the same turn.
5. Verify the required CLI flags still exist or rely on the prior Day 18 preflight if no runner code changed.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the Day 18 task doc lists exactly three benign batches
- [ ] the Day 18 handoff provides exact output roots and commands for all three batches
- [ ] the tracker Day 18 row lists `batch_0017`, `batch_0018`, and `batch_0019`
- [ ] no code behavior changed
- [ ] no schema / interface change was introduced
- [ ] validation was run or explicitly caveated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local split filenames exist and match the doc
- [ ] tracker Day 18 row lists all three batches
- [ ] Day 18 is documented as a three-batch benign-only queue

Commands to run if applicable:

```powershell
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Where-Object { $_.Name -in @('tranco_top_100001_500000_batch_0017_urls.txt','tranco_top_100001_500000_batch_0018_urls.txt','tranco_top_100001_500000_batch_0019_urls.txt') } | Select-Object -ExpandProperty Name
Select-String -Path 'E:\Warden\docs\modules\Warden_PLAN_A_BATCH_TRACKER.md','E:\Warden\docs\tasks\2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md','E:\Warden\docs\handoff\2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md' -Pattern 'tranco_top_100001_500000_batch_0017','tranco_top_100001_500000_batch_0018','tranco_top_100001_500000_batch_0019'
```

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path:

- `docs/handoff/2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none
