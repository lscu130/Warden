# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-26` Plan A Day 3 队列冻结的正式 handoff。
- 若涉及精确批次、输出目录、推荐命令或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY3-V1`
- 任务主题：在 Day 2 返回产物 handoff 未补回前，先冻结 Day 3 队列
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- 这份 handoff 把 `2026-03-26` 的 malicious / benign 批次与输出根目录先冻结为 forward execution-prep 工件。
- 它和延后的 Day 1 队列、以及仍待补回的 Day 2 返回产物 handoff 都是分开的边界。
- 推荐命令继续采用当前 supervised skip-capable 默认值，不引入新的操作语义。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-26-plan-a-batch-capture-day3-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY3-V1
- Task Title: Freeze the 2026-03-26 Plan A Day 3 malicious and benign capture queue before the pending Day 2 artifact handoff
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

Added a new execution-prep handoff for the 2026-03-26 Plan A Day 3 queue.
This handoff is separate from the delayed 2026-03-24 Day 1 queue and from the still-pending 2026-03-25 Day 2 returned-artifact handoff.
It freezes the intended Day 3 malicious and benign batch selections, assigns new output roots for 2026-03-26, and uses the current supervised skip-capable commands as the recommended default commands.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`.
- Added `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`.
- Froze the 2026-03-26 Day 3 queue as:
  - malicious `batch_0009` to `batch_0012`
  - benign `tranco_top_1_10000_batch_0002`
  - benign `tranco_top_10001_100000_batch_0002`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`
- `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`

Optional notes per file:

- These files define a Day 3 queue boundary only.
- They do not claim that the 2026-03-26 queue has already finished.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for the 2026-03-26 Day 3 queue instead of extending the Day 2 prep by hand.
- Day 3 malicious starts at `batch_0009`.
- Day 3 benign returns to the second batch of the two higher-rank Tranco buckets to stay aligned with the documented quota mix.
- Both lanes use supervised skip-capable commands by default.

### Preserved Behavior

- 2026-03-24 Day 1 remains historically frozen under its original naming.
- 2026-03-25 Day 2 remains a separate queue with its own output roots.
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
  - `phishtank_2026_only_batch_0009_urls.txt` through `batch_0012`
  - `tranco_top_1_10000_batch_0002_urls.txt`
  - `tranco_top_10001_100000_batch_0002_urls.txt`

### Not Run

- live VM malicious capture for the 2026-03-26 queue
- live physical-machine benign capture for the 2026-03-26 queue
- post-Day-2 reconciliation against actual returned artifacts

Reason:

This handoff is an execution-prep artifact only.
Actual results must be written later from returned batch artifacts.
The user explicitly asked to prepare Day 3 first and hand back Day 2 artifacts later.

---

## 7. Risks / Caveats

- This doc assumes the currently planned Day 2 benign pair remains `tranco_top_100001_500000_batch_0001` and `tranco_top_500001_1000000_batch_0001`.
- If the user’s actual Day 2 benign execution deviates from that pair before Day 3 starts, the Day 3 benign pair should be rechecked to avoid accidental duplicate planning.
- This doc does not prove any Day 3 batch succeeded; it only freezes the intended queue and commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`
- `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the user returns actual Day 2 and Day 3 artifacts

---

## 9. Recommended Next Step

- Use these exact output roots for the 2026-03-26 malicious queue:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0009`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0010`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0011`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0012`
- Use these exact output roots for the 2026-03-26 benign queue:
  - `E:\Warden\data\raw\benign\2026-03-26_planA_day3_tranco_top_1_10000_batch_0002`
  - `E:\Warden\data\raw\benign\2026-03-26_planA_day3_tranco_top_10001_100000_batch_0002`
- Run this VM/physical-machine preflight first:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious commands:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0009 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0009_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0009 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0010 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0010_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0010 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0011 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0011_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0011 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0012 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0012_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-26_planA_day3_phishtank_batch_0012 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- Use these exact benign commands:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0002_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-26_planA_day3_tranco_top_1_10000_batch_0002 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_10001_100000_batch_0002_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-26_planA_day3_tranco_top_10001_100000_batch_0002 `
  --source tranco `
  --rank_bucket top_10001_100000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- After the user runs the 2026-03-26 queue, the returned artifact package should include:
  - each input file path
  - each `output_root`
  - each `benign_capture_run.json` / `malicious_capture_run.json`
  - later malicious cluster/pool outputs when available
