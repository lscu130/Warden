# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Plan A Day 1 的仓库侧执行准备交接，不是最终抓取结果交接。
- 若涉及精确命令、批次、路径、状态或后续接受条件，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-V1`
- 当前状态：`PARTIAL`
- 本轮只完成了 VM 执行包冻结，没有在本地工作区做真实抓取。
- 已确认真实 runner / CLI、Day 1 固定批次、跨 bucket 的 benign 选择、独立 output root、停止规则与回传产物格式。
- 正式 Day 1 handoff 仍待 VM 产物回传后再写入 `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-24-plan-a-batch-capture-vm-prep
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-V1
- Task Title: Execute Plan A Day 1 batch capture for current PhishTank and Tranco local batches, and prepare the remaining day-wise operator queue
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-03-24
- Status: PARTIAL

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Prepared the repository-side execution package for Plan A Day 1 under a VM-only live-capture assumption.
Confirmed the real benign runner, malicious runner, and shared capture CLI from the current repo, locked the exact Day 1 batch set and per-batch output roots, and documented the stop rules plus the returned-artifact contract the user must send back after VM execution.
No live capture was executed in this workspace as part of this delivery, and the final Day 1 result handoff remains pending until VM artifacts are returned.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md` to mark the task `IN_PROGRESS` and to record that live capture for this task is VM-only.
- Added this formal prep-stage handoff documenting the exact VM Day 1 execution package and the post-run artifact requirements.

### Output / Artifact Changes

- Reserved the final result-handoff target: `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`.
- Did not create new capture outputs in scope for this handoff.

---

## 3. Files Touched

- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`

Optional notes per file:

- The task doc now explicitly records the VM-only execution assumption and that final Day 1 handoff must wait for returned VM artifacts.
- This handoff is a preparation-stage relay artifact, not the final Day 1 execution record.

---

## 4. Behavior Impact

### Expected New Behavior

- The repository now contains an explicit VM-only Day 1 execution contract instead of relying on thread memory.
- The next operator step is fixed to six specific Day 1 batches with dedicated output roots and fixed stop rules.
- The user can return a bounded set of VM artifacts and those artifacts will be sufficient to determine whether the task should be marked `DONE` or remain `PARTIAL`.

### Preserved Behavior

- No capture, ingest, training, inference, or labeling code changed.
- Existing benign and malicious runner CLIs remain unchanged.
- No frozen output filenames, schema fields, or directory contracts were modified.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

Compatibility notes:

This delivery only documented and froze the execution path that already exists in the repo.
No CLI flags, sample fields, output filenames, or directory contracts were changed.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
Get-Content -Raw E:\Warden\phishtank csv\split_summary.json
Get-Content -Raw E:\Warden\tranco csv\split_summary.json
Get-Content -Raw E:\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001\malicious_capture_run.json
```

### Result

- Confirmed the malicious runner entrypoint is `scripts/data/malicious/run_malicious_capture.py` with the current CLI flags `--feed_manifest`, `--input_path`, `--source`, `--output_root`, `--brand_lexicon`, and `--dry_run`.
- Confirmed the benign runner entrypoint is `scripts/data/benign/run_benign_capture.py` with the current CLI flags `--input_path`, `--input_format`, `--csv_url_column`, `--output_root`, `--source`, `--rank_bucket`, `--page_type`, `--language`, `--hard_benign`, `--brand_lexicon`, and `--dry_run`.
- Confirmed the shared capture engine entrypoint is `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` with the current non-interactive orchestration flags `--label`, `--output_root`, `--ingest_metadata_json`, and `--dry_run`.
- Confirmed PhishTank Day 1 is fixed to `batch_0001` through `batch_0004`.
- Confirmed the selected benign Day 1 batches are:
  - `E:\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt`
  - `E:\Warden\tranco csv\tranco_top_10001_100000_batch_0001_urls.txt`
- Confirmed these two benign batches come from different rank buckets and therefore satisfy the task constraint.
- Confirmed the current local workspace already contains an earlier failed local pilot artifact at `E:\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001\malicious_capture_run.json` with `all_success = false`, which is consistent with using the VM as the only approved live-capture environment for this task.

### Not Run

- live malicious capture in this local workspace
- live benign capture in this local workspace
- final Day 1 result handoff under `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`

Reason:

The active plan for this task is VM-only live capture.
The current repository-side delivery freezes the execution package and waits for the user to return VM-generated summary JSON files, logs, and sample counts before final acceptance and final Day 1 handoff are written.

---

## 7. Risks / Caveats

- The VM root path in the frozen commands assumes `C:\Users\lscu1\Desktop\Warden`; if the VM repo root differs, only the root prefix should be replaced.
- The final task status still depends on returned VM artifacts; without them this task cannot honestly be marked `DONE`.
- The existing local failed pilot folder under `data/raw/phish/2026-03-24_planA_day1_phishtank_batch_0001` must not be treated as Day 1 completion evidence for this task.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`

Doc debt still remaining:

- `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` still needs to be written after VM artifacts are returned.

---

## 9. Recommended Next Step

- Run this preflight in the VM first and stop immediately if any command fails:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\data\benign\run_benign_capture.py --help
python C:\Users\lscu1\Desktop\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Run the frozen preflight and Day 1 batch commands in the VM, using these exact Day 1 output roots:
  - malicious `batch_0001` -> `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001`
  - malicious `batch_0002` -> `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002`
  - malicious `batch_0003` -> `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003`
  - malicious `batch_0004` -> `C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004`
  - benign `tranco_top_1_10000_batch_0001` -> `C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001`
  - benign `tranco_top_10001_100000_batch_0001` -> `C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_10001_100000_batch_0001`
- Use these exact VM commands:

```powershell
python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0001_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001 `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0001\run.log

python C:\Users\lscu1\Desktop\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt" `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001\run.log

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0002_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002 `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0002\run.log

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0003_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003 `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0003\run.log

python C:\Users\lscu1\Desktop\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\phishtank csv\phishtank_2026_only_batch_0004_urls.txt" `
  --source phishtank `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004 `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\phish\2026-03-24_planA_day1_phishtank_batch_0004\run.log

python C:\Users\lscu1\Desktop\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "C:\Users\lscu1\Desktop\Warden\tranco csv\tranco_top_10001_100000_batch_0001_urls.txt" `
  --output_root C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_10001_100000_batch_0001 `
  --source tranco `
  --rank_bucket top_10001_100000 `
  --page_type homepage `
  --language en `
  *> C:\Users\lscu1\Desktop\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_10001_100000_batch_0001\run.log
```

- Use this fixed pilot-first order:
  - malicious `batch_0001`
  - benign `tranco_top_1_10000_batch_0001`
  - if both pass, malicious `batch_0002` to `batch_0004`
  - then benign `tranco_top_10001_100000_batch_0001`
- Apply these stop rules exactly:
  - if malicious `batch_0001` fails due shared engine or VM environment issues, stop all remaining five batches
  - if malicious `batch_0001` fails due malicious-lane-specific wrapper or input issues, stop remaining malicious batches but still run the first benign pilot
  - if the benign pilot fails due shared engine or VM environment issues, stop all remaining not-yet-run batches
  - if the benign pilot fails due benign-lane-specific wrapper or input issues, stop the second benign batch but continue malicious only if the malicious pilot already succeeded
  - if an output root already exists, treat that batch as `skipped_existing` unless the existing root clearly belongs to this same Day 1 plan and is being intentionally resumed
- Return, for every attempted batch:
  - output-root path
  - `malicious_capture_run.json` or `benign_capture_run.json`
  - `run.log`
  - sample-subdirectory count
  - short note on success, failure, skip, or stop reason
- Keep the remaining queue frozen as:
  - Day 2: malicious `batch_0005` to `batch_0008`; benign 2 more batches from different or not-yet-covered preferred buckets
  - Day 3: malicious `batch_0009` to `batch_0012`; benign 2 batches
  - Day 4: malicious `batch_0013` to `batch_0016`; benign 2 batches
  - Day 5: malicious `batch_0017` to `batch_0020`; benign 2 batches
  - Day 6: malicious `batch_0021` to `batch_0024`; benign 2 batches
  - Day 7: malicious `batch_0025` to `batch_0028`; benign 2 batches
  - Day 8: malicious `batch_0029` to `batch_0032`; benign 2 batches
  - Day 9: no new malicious main batches; use for retry / review / exclusion / cluster-check
  - Day 10: remaining benign 2 batches plus global cleanup
- After those VM artifacts are returned, write the final result handoff at `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` and set the task to `DONE` or `PARTIAL` based on actual evidence.
