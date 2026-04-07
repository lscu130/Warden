# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-28` Plan A Day 5 队列冻结的正式 handoff。
- 若涉及精确批次、输出目录、推荐命令或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-DAY5-V1`
- 任务主题：继续维持 8 批 malicious 日量，并让 benign 开始接入 supplemental Tranco 高 rank 分片
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- Day 5 的 malicious 继续保持 `8` 批/天，不因为前面低 yield 问题而提前缩回去。
- Day 5 的 benign 不再只依赖原始 Tranco 分片，而是开始使用新增的 supplemental 高 rank 批次。
- 推荐命令继续采用当前 supervised skip-capable 默认值，不引入新的操作语义。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-28-plan-a-batch-capture-day5-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY5-V1
- Task Title: Freeze the 2026-03-28 Plan A Day 5 queue with sustained doubled malicious volume and the first supplemental Tranco benign pair
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-27
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new execution-prep handoff for the 2026-03-28 Plan A Day 5 queue.
This handoff keeps malicious daily volume at the doubled 8-batch level because the reported public-feed effective malicious yield is still only around `5%` to `10%`.
It also starts consuming the first supplemental high-rank Tranco pair for benign capture because the original high-rank Tranco pair was already exhausted by the earlier queue design.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`.
- Added `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`.
- Froze the 2026-03-28 Day 5 queue as:
  - malicious `batch_0021` to `batch_0028`
  - benign `tranco_top_1_10000_batch_0003`
  - benign `tranco_top_10001_100000_batch_0008`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`
- `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`

Optional notes per file:

- These files define a Day 5 queue boundary only.
- They do not claim that the 2026-03-28 queue has already finished.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for the 2026-03-28 Day 5 queue.
- Day 5 malicious daily volume remains at 8 batches.
- Day 5 benign starts using the supplemental Tranco split for the next high-rank pair.
- Both lanes use supervised skip-capable commands by default.

### Preserved Behavior

- Day 1 to Day 4 remain historically separate queues with their own output roots.
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
  - `phishtank_2026_only_batch_0021_urls.txt` through `batch_0028`
  - `tranco_top_1_10000_batch_0003_urls.txt`
  - `tranco_top_10001_100000_batch_0008_urls.txt`

### Not Run

- live VM malicious capture for the 2026-03-28 queue
- live physical-machine benign capture for the 2026-03-28 queue
- reconciliation against actual returned Day 1 to Day 4 artifacts

Reason:

This handoff is an execution-prep artifact only.
Actual results must be written later from returned batch artifacts.

---

## 7. Risks / Caveats

- This doc assumes the still-pending returned Day 1 to Day 4 artifact package does not force a queue reorder before Day 5 starts.
- Keeping malicious at 8 batches continues the higher operator/runtime burden, but it matches the current low-yield reality.
- This doc does not prove any Day 5 batch succeeded; it only freezes the intended queue and commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md`
- `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the user returns actual Day 1 to Day 5 artifacts

---

## 9. Recommended Next Step

- Use these exact output roots for the 2026-03-28 malicious queue:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0021`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0022`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0023`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0024`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0025`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0026`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0027`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0028`
- Use these exact output roots for the 2026-03-28 benign queue:
  - `E:\Warden\data\raw\benign\2026-03-28_planA_day5_tranco_top_1_10000_batch_0003`
  - `E:\Warden\data\raw\benign\2026-03-28_planA_day5_tranco_top_10001_100000_batch_0008`
- Run this VM/physical-machine preflight first:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious commands:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0021 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0021_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0021 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0022 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0022_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0022 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0023 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0023_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0023 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0024 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0024_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0024 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0025 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0025_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0025 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0026 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0026_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0026 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0027 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0027_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0027 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0028 | Out-Null
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0028_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-28_planA_day5_phishtank_batch_0028 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- Use these exact benign commands:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0003_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-28_planA_day5_tranco_top_1_10000_batch_0003 `
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
  --input_path "E:\Warden\tranco csv\tranco_top_10001_100000_batch_0008_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-28_planA_day5_tranco_top_10001_100000_batch_0008 `
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

- After the user runs the 2026-03-28 queue, the returned artifact package should include:
  - each input file path
  - each `output_root`
  - each `benign_capture_run.json` / `malicious_capture_run.json`
  - later malicious cluster/pool outputs when available
