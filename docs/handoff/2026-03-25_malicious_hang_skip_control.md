# Handoff Metadata

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。
### 使用说明

- 这是 malicious 抓取卡住 / 人工 skip 控制这条线的正式 handoff。
- benign 的 partial recovery 不属于这份 handoff；对 malicious，当前策略是当前 URL 失败或中断后直接删除这次尝试中新建的样本目录。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-malicious-hang-skip-control
- Related Task ID: WARDEN-MALICIOUS-HANG-SKIP-CONTROL-V1
- Task Title: Add supervised malicious capture mode with manual skip, per-URL hard timeout, and automatic deletion of newly created partial sample directories on failed or aborted URLs
- Module: Data module / malicious capture operations
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

Updated the malicious upper-layer runner so it can switch into a supervised per-URL mode when explicitly requested.
In supervised mode, the runner launches one child capture subprocess per URL, supports operator-entered `skip` to abort only the current URL, supports an optional per-URL hard timeout, and deletes any sample directories newly created during a skipped, timed-out, or failed malicious URL attempt.
This keeps the default grouped malicious path intact while giving operators a way to keep the batch moving without preserving partial malicious leftovers for later recovery.
Real minimal probes were later run outside the sandbox: a single-URL `facebook.com` probe was skipped successfully, and a two-URL `facebook.com` + `example.com` probe confirmed that skipping the first URL did not block the second URL from completing successfully.

---

## 2. What Changed

### Code Changes

- Updated `scripts/data/malicious/run_malicious_capture.py` to add:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
  - supervised per-URL execution when either of those flags is enabled
  - Windows process-tree termination via `taskkill /PID /T /F` for the current URL worker
  - automatic deletion of newly created sample directories for skipped, timed-out, or failed malicious URLs
  - additive batch summary fields in `malicious_capture_run.json` for supervised runs
- Left the default malicious grouped path unchanged when the new supervision flags are absent.
- Did not modify the shared sample sidecar schema under each saved sample directory.

### Doc Changes

- Added `docs/tasks/2026-03-25_malicious_hang_skip_control.md`.
- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` with an English supervised malicious mode section covering:
  - why to use it
  - how to type `skip`
  - how to use `--url_hard_timeout_ms`
  - how failed malicious partial leftovers are deleted immediately instead of going through recovery
- Updated `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md` so the current Day 1 prep doc also mentions supervised malicious mode.
- Added this handoff document.

### Output / Artifact Changes

- `malicious_capture_run.json` now carries additive supervision fields when supervised mode is used:
  - `supervised_mode`
  - `interactive_skip`
  - `url_hard_timeout_ms`
  - `skipped_urls`
  - `timed_out_urls`
  - `deleted_partial_sample_dirs`
  - `results`

If supervision is not enabled, the old summary shape remains in place.
For supervised malicious runs, this batch summary should be treated as operator telemetry rather than the authoritative malicious sample-count source; authoritative counting must come from saved sample directories and downstream cluster records.

---

## 3. Files Touched

- `scripts/data/malicious/run_malicious_capture.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-25_malicious_hang_skip_control.md`
- `docs/handoff/2026-03-25_malicious_hang_skip_control.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

Optional notes per file:

- The malicious runner is the only live-capture code path changed because the requested skip control is scoped to malicious batch operation.
- The shared capture script was inspected but not modified in this patch.
- The VM prep handoff was refreshed because the current Day 1 operator instructions now need to mention malicious supervised mode too.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now run malicious capture in supervised mode and type `skip` in the terminal to abort only the current URL.
- Operators can now place a hard ceiling on each malicious URL with `--url_hard_timeout_ms`.
- A stalled child capture worker no longer has to block the rest of the malicious batch when supervision is enabled.
- If a malicious URL is skipped, times out, or fails after creating new sample directories, those newly created directories are deleted immediately.

### Preserved Behavior

- Existing malicious commands without the new flags still use the old grouped-subprocess batch strategy.
- The shared capture script CLI remains unchanged.
- Sample sidecar names and sample directory contracts remain unchanged.
- Label semantics, training logic, and inference logic remain unchanged.
- There is still no malicious recovery helper analogous to benign recovery.

### User-facing / CLI Impact

- New malicious runner flags:
  - `--interactive_skip`
  - `--url_hard_timeout_ms`

### Output Format Impact

- Existing sample-output structure: unchanged.
- Batch summary file `malicious_capture_run.json`: additive fields only when supervised mode is used.

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: PARTIAL
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/run_malicious_capture.py` CLI
- `malicious_capture_run.json` batch summary, supervised-mode additive fields only

Compatibility notes:

No sample sidecar schema changed.
The only output-contract expansion is additive batch-summary metadata for supervised malicious runs.
Existing malicious commands remain valid because the new flags are optional and the old path remains the default when they are absent.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python -m py_compile E:\Warden\scripts\data\malicious\run_malicious_capture.py
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --input_path "E:\Warden\tmp\malicious_supervised_dryrun_urls.txt" --source manual_malicious --output_root "E:\Warden\tmp\malicious_supervised_dryrun_out" --dry_run --url_hard_timeout_ms 10000
Get-Content E:\Warden\tmp\malicious_supervised_dryrun_out\malicious_capture_run.json
Get-Content E:\Warden\tmp\malicious_facebook_probe_out\malicious_capture_run.json
Get-Content E:\Warden\tmp\malicious_two_url_probe_out\malicious_capture_run.json
```

### Result

- Confirmed `run_malicious_capture.py --help` shows `--interactive_skip` and `--url_hard_timeout_ms`.
- Confirmed the updated malicious runner passes `py_compile`.
- Confirmed the supervised path writes `malicious_capture_run.json` with:
  - `supervised_mode`
  - `interactive_skip`
  - `url_hard_timeout_ms`
  - `skipped_urls`
  - `timed_out_urls`
  - `deleted_partial_sample_dirs`
  - `results`
- Confirmed the dry supervised run produced a failed child result and still wrote the supervised summary correctly.
- Ran a real single-URL supervised malicious probe outside the sandbox using `https://facebook.com/`; the URL was recorded as `skipped_by_user`, and the output root contained only `malicious_capture_run.json` with no sample directory left behind.
- Ran a real two-URL supervised malicious probe outside the sandbox using `https://facebook.com/` followed by `https://example.com/`; the first URL was skipped successfully and the second URL completed successfully, confirming that malicious `skip` does not block subsequent URLs.

### Not Run

- a case that actually created then deleted a partial malicious sample directory during supervision

Reason:

Live malicious probing is now possible outside the current sandbox boundary and was used for real supervised probes.
The remaining gap is narrower: this thread still has not observed a malicious URL that created a sample directory before being skipped or failing, so `deleted_partial_sample_dirs` has not yet been exercised with a non-empty result.

---

## 7. Risks / Caveats

- The new skip logic is implemented in the malicious runner, not in the shared capture core, so it only helps runs started through the malicious upper-layer entrypoint.
- Cleanup deletes any sample directories newly created during the current failed malicious URL attempt; it does not try to infer or repair older partial outputs from previous runs.
- Real supervised malicious probes now confirm that skipped URLs do not block later URLs, but the exact real-world partial-directory deletion path still has not been observed against a browser-created sample directory in-thread.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-25_malicious_hang_skip_control.md`
- `docs/handoff/2026-03-25_malicious_hang_skip_control.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

Doc debt still remaining:

- The Chinese half of the runbook was not updated for the new malicious supervised section because the current file encoding is already visibly degraded in terminal output; the English authoritative half was updated first to avoid corrupting the file further.

---

## 9. Recommended Next Step

- If the malicious lane stalls in the VM, rerun that batch with this full supervised command:

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

- Treat skipped, timed-out, or failed malicious URLs as disposable for that attempt; do not add a malicious recovery flow unless a later task explicitly requests it.
- If you need to exercise `deleted_partial_sample_dirs` explicitly, choose a target that is more likely to create a sample directory before being skipped or failing, and rerun one supervised malicious probe outside the sandbox.
