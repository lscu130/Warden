# 2026-04-28_plan_a_batch_capture_day18_vm_prep

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

- Day 18 日期：`2026-04-28`
- 状态：`selected`
- 队列：benign-only，`3` 个批次
- 批次：
  - `tranco_top_100001_500000_batch_0017`
  - `tranco_top_100001_500000_batch_0018`
  - `tranco_top_100001_500000_batch_0019`
- 文件名保留 `single_batch` 是为了保持上一轮 tracker 链接稳定；正文为当前权威内容。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-28-plan-a-batch-capture-day18-three-batch-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY18-THREE-BATCH-V2
- Task Title: Freeze the 2026-04-28 Plan A Day 18 three-batch benign queue
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-04-28
- Status: DONE

---

## 1. Executive Summary

Updated the 2026-04-28 Plan A Day 18 execution-prep docs from a one-batch queue to a three-batch benign-only queue.
Day 18 now uses:

- `tranco_top_100001_500000_batch_0017`
- `tranco_top_100001_500000_batch_0018`
- `tranco_top_100001_500000_batch_0019`

No malicious batches are assigned.
The tracker remains `selected` for Day 18 until returned result artifacts are available.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `docs/tasks/2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md`.
- Updated `docs/handoff/2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md`.
- Updated `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md`
- `docs/handoff/2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have frozen Day 18 prep commands for three benign Tranco batches.
- Day 18 consumes `batch_0017`, `batch_0018`, and `batch_0019` from the 2026-04-27 supplemental split.
- Day 18 remains `selected` until returned result artifacts are available.

### Preserved Behavior

- Current benign capture hardening defaults remain unchanged.
- Current CLI behavior remains unchanged.
- Existing Tranco split files remain unchanged.
- Existing capture output format remains unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This delivery changes only daily execution planning and tracker continuity docs.
It does not change runner behavior, capture output format, frozen JSON fields, labels, or public CLI interfaces.

---

## 6. Validation Performed

### Commands Run

```powershell
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Where-Object { $_.Name -in @('tranco_top_100001_500000_batch_0018_urls.txt','tranco_top_100001_500000_batch_0019_urls.txt') } | Select-Object -ExpandProperty Name
Select-String -Path 'E:\Warden\docs\modules\Warden_PLAN_A_BATCH_TRACKER.md','E:\Warden\docs\tasks\2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md','E:\Warden\docs\handoff\2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md' -Pattern 'tranco_top_100001_500000_batch_0017','tranco_top_100001_500000_batch_0018','tranco_top_100001_500000_batch_0019'
```

### Result

- Confirmed `tranco_top_100001_500000_batch_0018_urls.txt` exists.
- Confirmed `tranco_top_100001_500000_batch_0019_urls.txt` exists.
- Confirmed the tracker and Day 18 docs reference `batch_0017`, `batch_0018`, and `batch_0019`.
- Runner CLI flags were already verified in the previous Day 18 preflight, and no runner code changed in this update.

### Not Run

- live physical-machine benign capture for the 2026-04-28 Day 18 queue
- Day 18 result receipt closure

Reason:

This handoff is an execution-prep and tracker update only.
Actual receipt closure requires returned `benign_capture_run.json` files.

---

## 7. Risks / Caveats

- Day 18 remains `selected` until its returned `benign_capture_run.json` files are available.
- `batch_0020` through `batch_0022` remain unassigned after this Day 18 planning turn.
- The repo path still contains `single_batch` in the filename for continuity, but the document content now describes the current three-batch Day 18 queue.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-28_plan_a_batch_capture_day18_single_batch_execution_task.md`
- `docs/handoff/2026-04-28_plan_a_batch_capture_day18_single_batch_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

Doc debt still remaining:

- a later Day 18 result-receipt handoff is needed after returned artifacts exist

---

## 9. Recommended Next Step

Run these exact benign commands.

### Batch 0017

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017_urls.txt" `
  --output_root E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0017 `
  --source tranco `
  --rank_bucket top_100001_500000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

### Batch 0018

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018_urls.txt" `
  --output_root E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0018 `
  --source tranco `
  --rank_bucket top_100001_500000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

### Batch 0019

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019_urls.txt" `
  --output_root E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0019 `
  --source tranco `
  --rank_bucket top_100001_500000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

After the user runs Day 18, the returned artifact package should include:

- each input file path
- each `output_root`
- each `benign_capture_run.json`
