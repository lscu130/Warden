# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-27` Plan A Day 4 队列冻结的正式 handoff。
- 若涉及精确抓取量、批次、输出目录、推荐命令或验证口径，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY4-V1`
- 任务主题：因公共恶意源有效产出偏低而冻结 Day 4 加倍的 malicious 抓取量
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- Day 4 的 malicious 日抓取量已明确加倍，以回应 Day 1 到 Day 3 只有约 `5%` 到 `10%` 的实际有效 yield。
- benign 侧仍保持两批，不因为恶意侧低产出而同步乱改 benign 日队列规模。
- 当前推荐命令继续沿用 supervised skip-capable 路径与已冻结的 hardening 默认值。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-27-plan-a-batch-capture-day4-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY4-V1
- Task Title: Freeze the 2026-03-27 Plan A Day 4 queue with doubled malicious capture volume due to low effective public-feed yield
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-26
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new execution-prep handoff for the 2026-03-27 Plan A Day 4 queue.
This handoff freezes a doubled malicious daily volume because the user reported only around `5%` to `10%` practical effective malicious yield from public PhishTank capture across Day 1 to Day 3.
It keeps the benign lane at two batches, assigns new output roots for 2026-03-27, and uses the current supervised skip-capable commands as the recommended default commands.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`.
- Added `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`.
- Froze the 2026-03-27 Day 4 queue as:
  - malicious `batch_0013` to `batch_0020`
  - benign `tranco_top_100001_500000_batch_0002`
  - benign `tranco_top_500001_1000000_batch_0002`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`
- `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`

Optional notes per file:

- These files define a Day 4 queue boundary only.
- They do not claim that the 2026-03-27 queue has already finished.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for the 2026-03-27 Day 4 queue.
- Day 4 malicious daily volume is doubled from the prior 4-batch default to 8 batches.
- Day 4 benign remains a 2-batch queue.
- Both lanes use supervised skip-capable commands by default.

### Preserved Behavior

- Day 1 to Day 3 remain historically separate queues with their own output roots.
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
  - `phishtank_2026_only_batch_0013_urls.txt` through `batch_0020`
  - `tranco_top_100001_500000_batch_0002_urls.txt`
  - `tranco_top_500001_1000000_batch_0002_urls.txt`

### Not Run

- live VM malicious capture for the 2026-03-27 queue
- live physical-machine benign capture for the 2026-03-27 queue
- reconciliation against actual returned Day 2 and Day 3 artifacts

Reason:

This handoff is an execution-prep artifact only.
Actual results must be written later from returned batch artifacts.

---

## 7. Risks / Caveats

- This doc assumes the still-pending Day 2 and Day 3 returned artifact handoffs do not force a queue reorder before Day 4 starts.
- Doubling malicious batch count increases operator load and live-run time even though it matches the user-reported low effective yield.
- This doc does not prove any Day 4 batch succeeded; it only freezes the intended queue and commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`
- `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the user returns actual Day 2, Day 3, and Day 4 artifacts

---

## 9. Recommended Next Step

- Use these exact output roots for the 2026-03-27 malicious queue:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0013`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0014`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0015`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0016`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0017`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0018`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0019`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0020`
- Use these exact output roots for the 2026-03-27 benign queue:
  - `E:\Warden\data\raw\benign\2026-03-27_planA_day4_tranco_top_100001_500000_batch_0002`
  - `E:\Warden\data\raw\benign\2026-03-27_planA_day4_tranco_top_500001_1000000_batch_0002`
- Run this VM/physical-machine preflight first:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious commands:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0013 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0013_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0013 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0014 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0014_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0014 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0015 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0015_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0015 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0016 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0016_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0016 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0017 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0017_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0017 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0018 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0018_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0018 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0019 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0019_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0019 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0020 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0020_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-27_planA_day4_phishtank_batch_0020 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- Use these exact benign commands:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_100001_500000_batch_0002_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-27_planA_day4_tranco_top_100001_500000_batch_0002 `
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
  --input_path "E:\Warden\tranco csv\tranco_top_500001_1000000_batch_0002_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-27_planA_day4_tranco_top_500001_1000000_batch_0002 `
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

- After the user runs the 2026-03-27 queue, the returned artifact package should include:
  - each input file path
  - each `output_root`
  - each `benign_capture_run.json` / `malicious_capture_run.json`
  - later malicious cluster/pool outputs when available
