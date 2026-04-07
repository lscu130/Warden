# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 benign 抓取卡住 / 人工 skip 控制这条线的正式 handoff。
- 若涉及精确 CLI、验证结果、兼容性和未完成项，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BENIGN-HANG-SKIP-CONTROL-V1`
- 任务主题：为 benign 抓取加入 supervised skip 与单 URL 硬超时控制
- 当前状态：`PARTIAL`
- 所属模块：Data module / benign capture operations

### 当前交付要点

- benign 上层 runner 已支持 supervised per-URL 模式、人工 `skip`、以及可选的单 URL 硬超时。
- recovery helper 也被补强，可从磁盘样本目录盘点 partial leftovers，并生成 `partial_retry_*` 工件。
- 默认 benign 路径在新 flag 缺省时保持不变，sample sidecar schema 没被改动。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-benign-hang-skip-control
- Related Task ID: WARDEN-BENIGN-HANG-SKIP-CONTROL-V1
- Task Title: Add supervised benign capture mode with manual skip and per-URL hard timeout without changing sample sidecar schema
- Module: Data module / benign capture operations
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

Updated the benign upper-layer runner so it can switch into a supervised per-URL mode when explicitly requested.
In supervised mode, the runner launches one child capture subprocess per URL, supports operator-entered `skip` to abort only the current URL, and supports an optional per-URL hard timeout.
The recovery helper was also tightened so interrupted or skipped runs can be inventoried from on-disk sample directories, with explicit `partial_retry_*` artifacts and an optional quarantine step for half-written sample directories before retry.
This directly addresses the main batch-stall failure mode in the old strategy: the old benign runner waited on one long-lived batch subprocess and had no outer watchdog or operator escape hatch once a single URL wedged that child process.
A real minimal probe was later run outside the sandbox: `https://flowroute.com/` was skipped successfully and the next URL `https://example.com/` still completed successfully.

---

## 2. What Changed

### Code Changes

- Updated `scripts/data/benign/run_benign_capture.py` to add:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
  - supervised per-URL execution when either of those flags is enabled
  - Windows process-tree termination via `taskkill /PID /T /F` for the current URL worker
  - additive batch summary fields in `benign_capture_run.json` for supervised runs
- Updated `scripts/data/benign/recover_benign_batch.py` to add:
  - `partial_retry_urls.txt`
  - `partial_retry_sample_dirs.txt`
  - `partial_retry_samples.json`
  - `--quarantine_partial_dirs` to move retry-required partial sample directories under `_recovery\...\partial_quarantine` before rerun
- Left the default benign path unchanged when the new supervision flags are absent.
- Did not modify the shared sample sidecar schema under each saved sample directory.

### Doc Changes

- Added `docs/tasks/2026-03-25_benign_hang_skip_control.md`.
- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` with a supervised benign mode section covering:
  - why to use it
  - how to type `skip`
  - how to use `--url_hard_timeout_ms`
  - how to inventory and quarantine partial sample directories after interruption
- Added this handoff document.

### Output / Artifact Changes

- `benign_capture_run.json` now carries additive supervision fields when supervised mode is used:
  - `supervised_mode`
  - `interactive_skip`
  - `url_hard_timeout_ms`
  - `all_success`
  - `child_returncodes`
  - `skipped_urls`
  - `timed_out_urls`
  - `results`

If supervision is not enabled, the old summary shape remains in place.
- Recovery output now also includes `partial_retry_*` artifacts derived from on-disk sample completeness rather than from a batch manifest.

---

## 3. Files Touched

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/benign/recover_benign_batch.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-25_benign_hang_skip_control.md`
- `docs/handoff/2026-03-25_benign_hang_skip_control.md`

Optional notes per file:

- The benign runner remains the only live-capture code path changed because the requested skip control is scoped to benign batch operation.
- The recovery helper is now the authoritative way to identify partial skip leftovers from sample directories already on disk.
- The shared capture script was inspected to diagnose the stall mode, but not modified in this patch.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now run benign capture in supervised mode and type `skip` in the terminal to abort only the current URL.
- Operators can now place a hard ceiling on each benign URL with `--url_hard_timeout_ms`.
- A stalled child capture worker no longer has to block the rest of the benign batch when supervision is enabled.
- Operators can now inventory interrupted batches and isolate retry-required partial sample directories before rerun instead of guessing from a manifest.

### Preserved Behavior

- Existing benign commands without the new flags still use the old single-subprocess batch strategy.
- The shared capture script CLI remains unchanged.
- Sample sidecar names and sample directory contracts remain unchanged.
- Label semantics, training logic, and inference logic remain unchanged.

### User-facing / CLI Impact

- New benign runner flags:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
- New recovery helper flag:
  - `--quarantine_partial_dirs`

### Output Format Impact

- Existing sample-output structure: unchanged.
- Batch summary file `benign_capture_run.json`: additive fields only when supervised mode is used.
- Recovery bookkeeping under `_recovery`: additive `partial_retry_*` files plus optional quarantine records.

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: PARTIAL
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/benign/run_benign_capture.py` CLI
- `scripts/data/benign/recover_benign_batch.py` CLI / `_recovery` artifacts
- `benign_capture_run.json` batch summary, supervised-mode additive fields only

Compatibility notes:

No sample sidecar schema changed.
The only output-contract expansion is additive batch-summary metadata for supervised benign runs.
Interrupted-batch recovery is still based on on-disk sample directories, not on dataset manifests.
Existing benign commands remain valid because the new flags are optional and the old path remains the default when they are absent.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\benign\recover_benign_batch.py --help
python -m py_compile E:\Warden\scripts\data\benign\run_benign_capture.py E:\Warden\scripts\data\benign\recover_benign_batch.py
python E:\Warden\scripts\data\benign\recover_benign_batch.py --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt" --output_root "E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001" --source tranco --rank_bucket top_1_10000 --page_type homepage --language en --inventory_only
python E:\Warden\scripts\data\benign\recover_benign_batch.py --input_path "E:\Warden\tmp\hardening_smoke_v4_urls.txt" --output_root "E:\Warden\data\raw\benign\2026-03-24_hardening_smoke_v4" --source manual_benign --rank_bucket smoke --page_type homepage --language en --inventory_only
python E:\Warden\scripts\data\benign\recover_benign_batch.py --input_path "E:\Warden\tmp\benign_skip_probe_urls.txt" --output_root "E:\Warden\tmp\benign_skip_probe_out" --source manual_benign --rank_bucket probe --page_type homepage --language en --inventory_only
```

### Result

- Confirmed `run_benign_capture.py --help` shows `--interactive_skip` and `--url_hard_timeout_ms`.
- Confirmed `recover_benign_batch.py --help` shows `--quarantine_partial_dirs`.
- Confirmed the updated benign runner and the previously added benign recovery helper both pass `py_compile`.
- Confirmed the supervised path uses:
  - one child capture subprocess per URL
  - `stdin=subprocess.DEVNULL` for child workers
  - Windows process-tree termination via `taskkill`
  - additive summary fields for supervised mode
- Confirmed the recovery helper now writes `partial_retry_urls.txt`, `partial_retry_sample_dirs.txt`, and `partial_retry_samples.json`.
- Ran inventory against `E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001`; current repo state there contains no sample directories, so inventory reported `sample_dir_count=0` and `captured_count=0`.
- Ran inventory against `E:\Warden\data\raw\benign\2026-03-24_hardening_smoke_v4`; recovery artifacts were written successfully, including the new `partial_retry_*` files.
- Ran a real supervised benign probe outside the sandbox using `E:\Warden\tmp\benign_skip_probe_urls.txt`; `https://flowroute.com/` was recorded as `skipped_by_user` and the next URL `https://example.com/` completed successfully.
- Ran recovery inventory against `E:\Warden\tmp\benign_skip_probe_out`; the probe output contained one successful sample directory and no partial sample directories, so this particular skip did not leave a partial leftover.

### Not Run

- a quarantine run against a real partial-sample batch

Reason:

Live benign probing is now possible outside the current sandbox boundary and was used for a minimal supervised probe.
The remaining gap is narrower: this thread still has not observed a real benign skip case that produced a partial sample directory and then required quarantine.

---

## 7. Risks / Caveats

- The new skip logic is implemented in the benign runner, not in the shared capture core, so it only helps runs started through the benign upper-layer entrypoint.
- If a worker is killed while it is already writing a sample directory, a partial sample directory may still be left behind; downstream recovery tooling should treat partial directories carefully.
- Inventory matching currently trusts `url.json -> input_url` canonicalization; sites that drift between `google.com` and `www.google.com` may still appear as outside-input until normalization policy is tightened explicitly.
- The real minimal probe showed `flowroute.com` could be skipped and the next URL could still complete, but it did not reproduce a partial benign leftover on disk.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-25_benign_hang_skip_control.md`
- `docs/handoff/2026-03-25_benign_hang_skip_control.md`

Doc debt still remaining:

- A future handoff should append real `flowroute.com` repro findings after an outside-sandbox browser run succeeds.
- If `google.com` / `www.google.com` equivalence needs to be treated as the same input for recovery, that should be a separate explicit task because it changes matching policy.

---

## 9. Recommended Next Step

- Point recovery at the real batch output root that actually contains the first-batch sample directories; the user-provided path currently has only `_recovery` in the repo state I could inspect.
- Start with:
  - `--disable_route_intercept`
  - `--url_hard_timeout_ms 120000`
  - `--goto_wait_until commit`
- If you need to exercise the quarantine path specifically, run one more supervised benign probe on a site that is more likely to leave a half-written sample directory before skip.
