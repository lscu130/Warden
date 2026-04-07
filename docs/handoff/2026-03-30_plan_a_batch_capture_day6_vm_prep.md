# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-30` Plan A Day 6 队列冻结的正式 handoff。
- 若涉及精确批次、输出目录、推荐命令或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY6-V1`
- 任务主题：为今天的 Day 6 冻结新队列，并将 malicious 日量退回到 `4` 批
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- Day 6 的 malicious 不再维持 `8` 批，而是按用户要求退回到 `4` 批。
- Day 6 的 benign 继续沿用既有 rank-bucket 轮换节奏，使用下一组 lower-rank 对。
- 推荐命令仍然采用当前 supervised skip-capable 默认值，不引入新的操作语义。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-30-plan-a-batch-capture-day6-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY6-V1
- Task Title: Freeze the 2026-03-30 Plan A Day 6 queue with malicious volume reduced back to four batches
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-30
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new execution-prep handoff for the 2026-03-30 Plan A Day 6 queue.
This handoff reduces malicious daily volume back to `4` batches because the user explicitly requested that planning change.
It keeps the current supervised skip-capable capture commands unchanged and continues the benign lane on the next lower-rank pair in the existing queue cadence.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-03-30_plan_a_batch_capture_day6_execution_task.md`.
- Added `docs/handoff/2026-03-30_plan_a_batch_capture_day6_vm_prep.md`.
- Updated `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`.
- Froze the 2026-03-30 Day 6 queue as:
  - malicious `batch_0029` to `batch_0032`
  - benign `tranco_top_100001_500000_batch_0003`
  - benign `tranco_top_500001_1000000_batch_0003`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-03-30_plan_a_batch_capture_day6_execution_task.md`
- `docs/handoff/2026-03-30_plan_a_batch_capture_day6_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

Optional notes per file:

- These files define a Day 6 queue boundary only.
- They do not claim that the 2026-03-30 queue has already finished.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for the 2026-03-30 Day 6 queue.
- Day 6 malicious daily volume is reduced to 4 batches.
- Day 6 benign continues the alternating queue cadence with the next lower-rank pair.
- Both lanes use supervised skip-capable commands by default.
- The Plan A batch tracker now includes Day 6 in the selected queue history.

### Preserved Behavior

- Day 1 to Day 5 remain historically separate queues with their own output roots.
- Current capture hardening defaults remain unchanged.
- Current CLI behavior remains unchanged.

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

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`

Compatibility notes:

This prep artifact changes only daily execution planning, output-root naming for a new queue, and tracker continuity docs.
It does not change any runner or capture interface.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
```

### Result

- Confirmed the current benign runner still exposes:
  - `--disable_route_intercept`
  - `--goto_wait_until {load,domcontentloaded,commit,networkidle}`
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
- Confirmed the current malicious runner still exposes:
  - `--disable_route_intercept`
  - `--goto_wait_until {load,domcontentloaded,commit,networkidle}`
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
- Confirmed the local batch filenames for:
  - `phishtank_2026_only_batch_0029_urls.txt` through `batch_0032`
  - `tranco_top_100001_500000_batch_0003_urls.txt`
  - `tranco_top_500001_1000000_batch_0003_urls.txt`
- Confirmed `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md` now contains a Day 6 row.

### Not Run

- live VM malicious capture for the 2026-03-30 queue
- live physical-machine benign capture for the 2026-03-30 queue
- reconciliation against actual returned Day 1 to Day 5 artifacts

Reason:

This handoff is an execution-prep artifact only.
Actual results must be written later from returned batch artifacts.

---

## 7. Risks / Caveats

- This doc assumes the still-pending returned Day 1 to Day 5 artifact package does not force a queue reorder before Day 6 starts.
- Reducing malicious back to 4 batches may slow malicious raw-volume growth compared with Day 4 and Day 5.
- This doc does not prove any Day 6 batch succeeded; it only freezes the intended queue and commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-30_plan_a_batch_capture_day6_execution_task.md`
- `docs/handoff/2026-03-30_plan_a_batch_capture_day6_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the user returns actual Day 1 to Day 6 artifacts

---

## 9. Recommended Next Step

- Use these exact output roots for the 2026-03-30 malicious queue:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0029`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0030`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0031`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0032`
- Use these exact output roots for the 2026-03-30 benign queue:
  - `E:\Warden\data\raw\benign\2026-03-30_planA_day6_tranco_top_100001_500000_batch_0003`
  - `E:\Warden\data\raw\benign\2026-03-30_planA_day6_tranco_top_500001_1000000_batch_0003`
- Run this VM/physical-machine preflight first:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious commands:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0029 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0029_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0029 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0030 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0030_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0030 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0031 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0031_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0031 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0032 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0032_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-30_planA_day6_phishtank_batch_0032 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- Use these exact benign commands:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0003_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-30_planA_day6_tranco_top_100001_500000_batch_0003 `
  --source tranco `
  --rank_bucket top_100001_500000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_500001_1000000_batch_0003_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-30_planA_day6_tranco_top_500001_1000000_batch_0003 `
  --source tranco `
  --rank_bucket top_500001_1000000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- After the user runs the 2026-03-30 queue, the returned artifact package should include:
  - each input file path
  - each `output_root`
  - each `benign_capture_run.json` / `malicious_capture_run.json`
  - later malicious cluster/pool outputs when available
