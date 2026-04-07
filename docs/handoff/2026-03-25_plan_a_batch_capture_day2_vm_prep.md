# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-25` Plan A Day 2 队列冻结的正式 handoff。
- 若涉及精确批次、输出路径、推荐命令或验证口径，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY2-V1`
- 任务主题：冻结 `2026-03-25` 新一天的 malicious / benign 抓取队列
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- 这份 handoff 明确把 `2026-03-25` 作为独立的新日队列，而不是继续挤进延后的 `2026-03-24 Day 1`。
- 恶意与良性批次选择、输出根目录和默认命令都在这里冻结，供当天执行直接照着跑。
- 当前推荐路径继续使用 supervised skip-capable 命令，不回退到旧的批处理操作口径。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-plan-a-batch-capture-day2-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY2-V1
- Task Title: Freeze the 2026-03-25 new-day malicious and benign capture queue after the delayed 2026-03-24 Day 1 run
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-25
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new execution-prep handoff for the new 2026-03-25 capture queue.
This handoff is separate from the delayed 2026-03-24 Day 1 queue and should be treated as the start of a new-day queue with new output roots.
It freezes today’s malicious and benign batch selections and uses the current supervised skip-capable commands as the recommended default commands.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`.
- Added `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`.
- Froze the new 2026-03-25 queue as:
  - malicious `batch_0005` to `batch_0008`
  - benign `tranco_top_100001_500000_batch_0001`
  - benign `tranco_top_500001_1000000_batch_0001`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`

Optional notes per file:

- These files define a new-day queue boundary only.
- They do not claim that today’s queue has already finished.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for the 2026-03-25 queue instead of reusing the delayed 2026-03-24 Day 1 prep.
- Today’s malicious queue starts at `batch_0005`.
- Today’s benign queue starts from two new Tranco rank buckets not used in the delayed Day 1 queue.
- Both lanes use supervised skip-capable commands by default.

### Preserved Behavior

- 2026-03-24 Day 1 remains historically frozen under its original naming.
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

This prep artifact changes only daily execution planning and output-root naming for a new queue.
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
  - `phishtank_2026_only_batch_0005_urls.txt` through `batch_0008`
  - `tranco_top_100001_500000_batch_0001_urls.txt`
  - `tranco_top_500001_1000000_batch_0001_urls.txt`

### Not Run

- live VM malicious capture for today’s queue
- live physical-machine benign capture for today’s queue

Reason:

This handoff is an execution-prep artifact only.
Actual results must be written later from returned batch artifacts.

---

## 7. Risks / Caveats

- This doc assumes the delayed 2026-03-24 Day 1 queue already consumed the first two benign buckets as originally planned.
- If the user actually ran a different benign pair yesterday, today’s benign pair should be adjusted before execution to avoid accidental duplicate planning.
- This doc does not prove any of today’s batches succeeded; it only freezes the intended queue and commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the user returns actual artifacts from this queue

---

## 9. Recommended Next Step

- Use these exact output roots for today’s malicious queue:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0005`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0006`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0007`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0008`
- Use these exact output roots for today’s benign queue:
  - `E:\Warden\data\raw\benign\2026-03-25_planA_day2_tranco_top_100001_500000_batch_0001`
  - `E:\Warden\data\raw\benign\2026-03-25_planA_day2_tranco_top_500001_1000000_batch_0001`
- Run this VM/physical-machine preflight first:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious commands:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0005 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0005_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0005 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0006 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0006_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0006 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0007 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0007_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0007 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0008 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0008_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-25_planA_day2_phishtank_batch_0008 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- Use these exact benign commands:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0001_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-25_planA_day2_tranco_top_100001_500000_batch_0001 `
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
  --input_path "E:\Warden\tranco csv\tranco_top_500001_1000000_batch_0001_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-25_planA_day2_tranco_top_500001_1000000_batch_0001 `
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

- After the user runs today’s queue, the returned artifact package should include:
  - each input file path
  - each `output_root`
  - each `benign_capture_run.json` / `malicious_capture_run.json`
  - later malicious cluster/pool outputs when available
