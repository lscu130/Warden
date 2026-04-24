# 2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-24` Plan A Day 17 的 benign 补量 vm-prep handoff。
- 用户最新要求把最后一个剩余 Tranco 批次也补到 Day 17，因此 Day 17 现在包含 `2` 个 benign 批次。
- Day 17 仍不包含 malicious 队列。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY17-SUPPLEMENT-V2`
- 当前状态：`DONE`
- Day 17 已写入 tracker，状态为 `selected`
- Day 17 批次：
  - `tranco_top_100001_500000_batch_0015`
  - `tranco_top_100001_500000_batch_0016`
- Day 17 排完后，当前 repo-local Tranco benign split inventory 已全部分配。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-24-plan-a-batch-capture-day17-supplement-vm-prep-v2
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY17-SUPPLEMENT-V2
- Task Title: Freeze the 2026-04-24 Plan A Day 17 final two-batch benign supplement queue
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

Updated the 2026-04-24 Plan A Day 17 execution-prep handoff from a one-batch supplement to a final two-batch benign-only supplement.
Day 17 now queues:

- `tranco_top_100001_500000_batch_0015`
- `tranco_top_100001_500000_batch_0016`

After this update, the current repo-local Tranco benign split inventory is fully allocated.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `docs/tasks/2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md`.
- Updated `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`.
- Updated `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`.
- Added `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`.
- Froze the 2026-04-24 Day 17 queue as benign `tranco_top_100001_500000_batch_0015` and `tranco_top_100001_500000_batch_0016`.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md`
- `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have Day 17 prep commands for both final benign Tranco supplement batches.
- Day 17 contains exactly `2` benign Tranco batches and no malicious queue.
- Day 17 consumes the final remaining repo-local Tranco benign split.
- The Tranco benign selection rationale is documented in a module-level Markdown file.

### Preserved Behavior

- Current benign capture hardening defaults remain unchanged.
- Current CLI behavior remains unchanged.
- Output-root naming remains auditable and day-specific.
- Day 16 and Day 17 remain `selected` until returned artifacts are received and closed separately.

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

This delivery changes only daily execution planning and documentation.
It does not change runner behavior, capture output format, frozen JSON fields, labels, or public CLI interfaces.

---

## 6. Validation Performed

### Commands Run

```powershell
Test-Path -LiteralPath 'E:\Warden\tranco csv\tranco_top_100001_500000_batch_0016_urls.txt'
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
rg "current repo-local Tranco benign split inventory is fully allocated|tranco_top_100001_500000_batch_0016" E:\Warden\docs\modules\Warden_PLAN_A_BATCH_TRACKER.md E:\Warden\docs\tasks\2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md E:\Warden\docs\handoff\2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md E:\Warden\docs\modules\Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md
```

### Result

- Confirmed `tranco_top_100001_500000_batch_0016_urls.txt` exists.
- Confirmed the current benign runner still exposes:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
  - `--nav_timeout_ms`
  - `--goto_wait_until {load,domcontentloaded,commit,networkidle}`
- Confirmed the current capture script still exposes:
  - `--disable_route_intercept`
  - `--nav_timeout_ms`
  - `--goto_wait_until {load,domcontentloaded,commit,networkidle}`
- Confirmed the updated docs reference `tranco_top_100001_500000_batch_0016`.
- Confirmed no updated Day 17 doc should still state that `batch_0016` remains unqueued after Day 17.

### Not Run

- live physical-machine benign capture for the 2026-04-24 Day 17 queue
- Day 16 receipt closure
- Day 17 receipt closure

Reason:

This handoff is an execution-prep and documentation update only.
Actual receipt closure requires returned `benign_capture_run.json` files.

---

## 7. Risks / Caveats

- Day 16 remains `selected` in the tracker because result receipt closure is out of scope for this turn.
- Day 17 also remains `selected` until both returned Day 17 `benign_capture_run.json` files are available.
- This doc does not prove the Day 17 supplement is sufficient by actual post-dedup row count; it freezes the requested final Tranco supplement queue.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-24_plan_a_batch_capture_day17_supplement_execution_task.md`
- `docs/handoff/2026-04-24_plan_a_batch_capture_day17_supplement_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`

Doc debt still remaining:

- a later Day 16 result-receipt closure is still needed
- a later Day 17 run-result handoff is still needed after the user returns actual Day 17 artifacts

---

## 9. Recommended Next Step

Run these two Day 17 benign supplement batches.

### Batch 0015 Output Root

```text
E:\WardenData\raw\benign\tranco\2026-04-24_planA_day17_tranco_top_100001_500000_batch_0015
```

### Batch 0015 Command

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0015_urls.txt" `
  --output_root E:\WardenData\raw\benign\tranco\2026-04-24_planA_day17_tranco_top_100001_500000_batch_0015 `
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

### Batch 0016 Output Root

```text
E:\WardenData\raw\benign\tranco\2026-04-24_planA_day17_tranco_top_100001_500000_batch_0016
```

### Batch 0016 Command

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0016_urls.txt" `
  --output_root E:\WardenData\raw\benign\tranco\2026-04-24_planA_day17_tranco_top_100001_500000_batch_0016 `
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

After the user runs the 2026-04-24 Day 17 queue, the returned artifact package should include:

- both input file paths
- both `output_root` values
- both `benign_capture_run.json` files
