# Handoff Metadata

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。
### 使用说明

- 这是 2026-03-25 的 Plan A Day 1 执行准备续版 handoff。
- 它不是新的 Day 1 计划，也不是最终执行结果 handoff。
- 本版唯一目的，是在不改 2026-03-24 冻结批次编号和 output root 命名的前提下，把最新 benign 执行说明补齐到当前 repo 状态。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-plan-a-batch-capture-vm-prep-refresh
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-V1
- Task Title: Execute Plan A Day 1 batch capture for current PhishTank and Tranco local batches, and prepare the remaining day-wise operator queue
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-25
- Status: PARTIAL

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a refreshed VM/physical-machine execution-prep handoff for the still-unfinished Plan A Day 1 queue.
This refresh does not renumber the unfinished Day 1 batches and does not rename any existing `2026-03-24_planA_day1_*` output roots.
Its purpose is to carry forward the latest repo-effective operator guidance:
the built-in capture hardening remains in place, benign runs have an optional supervised skip path, malicious runs also have an optional supervised skip path for stalled URLs, and benign shortfall should now be handled by expanding fresh Tranco batches rather than recovery-based second-pass recapture.

---

## 2. What Changed

### Code Changes

- none

This refresh assumes the already-landed repo state from prior work, including:

- default `goto_wait_until=commit`
- default `NAV_TIMEOUT_MS=60000`
- page-level stealth enabled by default
- Google-domain consent handling
- optional benign supervised mode via `--interactive_skip` and `--url_hard_timeout_ms`
- optional malicious supervised mode via `--interactive_skip` and `--url_hard_timeout_ms`

### Doc Changes

- Added `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`.
- Carried forward the unfinished 2026-03-24 Day 1 queue without changing its batch IDs or output-root naming.
- Updated the execution-prep guidance so operators can use supervised skip on both benign and malicious lanes if either lane stalls.
- Explicitly froze the current operator strategy for benign shortfall: expand fresh Tranco batches instead of making recovery-based second-pass recapture part of the normal workflow.

### Output / Artifact Changes

- none

This refresh does not create new capture outputs and does not mark any Day 1 batch as completed.

---

## 3. Files Touched

- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

Optional notes per file:

- This file is a prep-stage continuity artifact only.
- The previous prep handoff at `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md` remains useful for the original Day 1 frozen queue, but this newer file should be treated as the current prep reference.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have one prep document that matches the current repo behavior as of 2026-03-25.
- Unfinished Day 1 execution continues under the original 2026-03-24 batch numbering and output-root naming instead of being silently re-dated.
- If benign capture stalls on the physical machine, the operator may use supervised benign mode with terminal `skip` instead of abandoning the whole batch.
- If malicious capture stalls in the VM, the operator may use supervised malicious mode with terminal `skip` instead of abandoning the whole batch.
- If final benign volume is still short after a run, the operator should expand with additional Tranco batches rather than defaulting to recovery-based second-pass recapture.

### Preserved Behavior

- The frozen Day 1 queue remains:
  - malicious `batch_0001` to `batch_0004`
  - benign `tranco_top_1_10000_batch_0001`
  - benign `tranco_top_10001_100000_batch_0001`
- Existing `2026-03-24_planA_day1_*` output roots remain the canonical naming pattern for this unfinished Day 1 work.
- No schema, label semantics, training logic, or inference logic changed in this refresh.

### User-facing / CLI Impact

- No new CLI change was introduced by this refresh itself.
- The current effective benign operator options already present in the repo are:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
- The current effective malicious operator options already present in the repo are:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`

### Output Format Impact

- none in this refresh

The only operator-level rule change is procedural:
do not rename unfinished Day 1 output roots from `2026-03-24_*` to `2026-03-25_*`.

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

This handoff refresh does not introduce a new interface change.
It only documents the repo-effective interfaces that already exist as of 2026-03-25.
The unfinished Day 1 queue continues to use the original `2026-03-24_planA_day1_*` naming, so lineage remains continuous and auditable.

If there is any downstream risk, spell it out clearly.

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
  - proxy and navigation-timeout passthrough flags

### Not Run

- live VM malicious capture
- live physical-machine benign capture
- final Day 1 result handoff under `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`

Reason:

This refresh is a documentation continuity step only.
It does not claim new live execution results.
The Day 1 queue is still unfinished and must continue from returned or newly generated real batch artifacts.

---

## 7. Risks / Caveats

- If the operator mistakenly renames unfinished Day 1 output roots to a new 2026-03-25 naming pattern, lineage across the interrupted run becomes harder to audit.
- Benign `skip` can still leave partial sample directories behind on disk; this refresh does not add cleanup automation for those leftovers.
- The current repo still contains benign recovery helper code, but it is no longer part of the recommended operator path for normal batch continuation.
- This document does not prove any Day 1 batch finished successfully; it only refreshes the execution prep instructions.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

Doc debt still remaining:

- `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` still needs to be written after real Day 1 artifacts are returned.
- If a later operator needs a single canonical prep entry, the older 2026-03-24 prep handoff may eventually be superseded explicitly, but this refresh does not rewrite history.

---

## 9. Recommended Next Step

- Continue the unfinished Day 1 queue under the original 2026-03-24 naming and batch IDs.
- Keep malicious in the VM and benign on the physical machine.
- Ensure `playwright-stealth` is installed in every environment that will run capture.
- For malicious, continue to use the frozen Day 1 output roots:
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003`
  - `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004`
- For benign, continue to use the frozen Day 1 output roots:
  - `E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001`
  - `E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_10001_100000_batch_0001`
- Run this VM preflight first and stop immediately if any command fails:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use these exact malicious VM commands for the unfinished Day 1 queue:

```powershell
New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001 | Out-Null

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0001_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002 | Out-Null

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0002_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003 | Out-Null

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0003_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003

New-Item -ItemType Directory -Force C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004 | Out-Null

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0004_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004
```

- If the malicious lane stalls on a single URL and you need operator control, the current repo also supports a supervised malicious mode:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0001_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- In supervised malicious mode:
  - type `skip` in the terminal to abort only the current malicious URL
  - skipped, timed-out, or failed malicious URLs do not go through recovery
  - any sample directories newly created during that failed URL attempt are deleted immediately

- If you want a safer benign retry/pilot command on the physical machine, use:
- If you want a safer benign retry/pilot command on the physical machine, use:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- If a benign batch is interrupted or skipped mid-run, keep the partial outputs as evidence, continue using supervised `skip` when needed, and if final benign volume is still short, prepare another fresh Tranco batch instead of defaulting to recovery-based second-pass recapture.

- After real batch artifacts are available, write the final Day 1 result handoff at `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` using actual evidence only.
