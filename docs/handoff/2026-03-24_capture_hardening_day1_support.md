# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Day 1 抓取稳定性补丁的正式交接，不是最终的 Day 1 批次执行结果交接。
- 涉及精确 CLI、字段、默认值、验证结果时，以英文版为准。

### 摘要

- 对应任务：`WARDEN-BATCH-CAPTURE-PLAN-A-V1`
- 当前交付状态：`DONE`
- 本轮已把 `playwright-stealth` 接入抓取主链路，并把默认导航改成 `commit + 60s`，同时补了 Google consent 处理，以及仅对 benign 路径收紧 `blocked_or_error` 的 Cloudflare 误杀判定。
- 本地静态检查已通过，并在物理机对 `google.com`、`cloudflare.com`、`zoom.us`、`example.com` 做了真实 smoke，4 个站点都成功落样本。
- 这不等于 Day 1 批次执行已经完成；Day 1 最终状态仍取决于你回传的真实 batch 产物。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-24-capture-hardening-day1-support
- Related Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-V1
- Task Title: Execute Plan A Day 1 batch capture for current PhishTank and Tranco local batches, and prepare the remaining day-wise operator queue
- Module: Data module / capture engine
- Author: Codex
- Date: 2026-03-24
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Implemented the Day 1 capture hardening patch directly in the current Warden capture stack.
The patch introduces one approved new dependency, `playwright-stealth`, switches the default navigation strategy from `load` to `commit` with a 60-second timeout, and adds Google-domain consent handling.
Static validation passed, and a real local benign smoke against `https://www.google.com`, `https://cloudflare.com`, `https://zoom.us`, and `https://example.com` succeeded with sample outputs written under `data/raw/benign/2026-03-24_hardening_smoke_v4`.

---

## 2. What Changed

### Code Changes

- Updated `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` to:
  - require `playwright-stealth` at runtime with a clear fatal message if missing;
  - enable page-level stealth by default in both the main path and the variant path;
  - add fixed Chromium launch args for the Day 1 anti-bot hardening path;
  - fall back from `channel="chrome"` to bundled Chromium if the Chrome-channel launch fails;
  - change the default navigation mode to `commit` and the default navigation timeout to `60000`;
  - keep the old `load -> domcontentloaded` timeout fallback path when `load` is explicitly requested;
  - insert a post-navigation `domcontentloaded` wait plus a short hydration delay;
  - add Google-domain consent handling before screenshot and text extraction;
  - add an optional `--disable_route_intercept` escape hatch for navigation debugging;
  - relax the `cloudflare` blocked/error heuristic only when `label=benign`, leaving the phish path unchanged.
- Updated `scripts/data/benign/run_benign_capture.py` so `--goto_wait_until` now accepts `commit` and `networkidle`, with `commit` as the default.
- Updated `scripts/data/malicious/run_malicious_capture.py` so `--goto_wait_until` now accepts `commit` and `networkidle`, with `commit` as the default.
- Updated both upper-layer runners to expose `--disable_route_intercept`.

### Doc Changes

- Updated `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md` so the Day 1 task explicitly allows the approved dependency `playwright-stealth`.
- Updated `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md` to reflect the built-in hardening path instead of describing the old behavior.
- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` to document the new default navigation behavior, the new dependency requirement, and the revised timeout guidance.

### Output / Artifact Changes

- Existing sample-directory names and summary filenames did not change.
- A local smoke output root was created at `data/raw/benign/2026-03-24_hardening_smoke_v2` for validation.

---

## 3. Files Touched

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-24_capture_hardening_day1_support.md`

Optional notes per file:

- The capture script carries the actual hardening logic.
- The two runners only received the smallest CLI-surface change needed to expose the new navigation modes.
- The Day 1 task and prep handoff now match the new allowed scope and the actual default behavior.

---

## 4. Behavior Impact

### Expected New Behavior

- Default capture now navigates with `wait_until="commit"` instead of `load`.
- Default capture now waits for `domcontentloaded` and a short hydration window after navigation.
- Default capture now applies stealth to every new page in both the main capture path and the variant path.
- Google-domain pages now attempt a lightweight consent click before screenshot and content extraction.
- Benign capture no longer treats a bare `cloudflare` text hit as an automatic blocked/error signal.

### Preserved Behavior

- Existing runner entrypoints and existing command shapes remain valid.
- Sample folder naming, summary filenames, and the core A~H sample structure remain unchanged.
- No training logic, labeling logic, or manifest downstream contracts were renamed or removed.

### User-facing / CLI Impact

- `--goto_wait_until` now accepts `commit` and `networkidle`.
- `--disable_route_intercept` is now available for narrow debugging comparisons.
- Existing CLI flags remain valid.
- Existing commands continue to run without adding new required arguments because the new hardening path is now the default.

### Output Format Impact

- No output file shape changed.
- No frozen filenames or directory contracts changed.

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `--goto_wait_until` in the capture script and both upper-layer runners
- `--disable_route_intercept` in the capture script and both upper-layer runners
- runtime dependency set for the capture environment
- default capture navigation behavior

Compatibility notes:

The CLI change is additive only: previous choices still work, and existing commands remain valid.
The only new runtime dependency is `playwright-stealth`; if it is missing in an execution environment, the capture script now fails fast with an explicit error instead of silently downgrading behavior.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python -m pip install playwright-stealth
python -c "from playwright_stealth import Stealth; print('playwright_stealth_import_ok')"
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py E:\Warden\scripts\data\benign\run_benign_capture.py E:\Warden\scripts\data\malicious\run_malicious_capture.py
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --input_path E:\Warden\tmp\hardening_smoke_urls_v3.txt --output_root E:\Warden\data\raw\benign\2026-03-24_hardening_smoke_v4 --source hardening_smoke --rank_bucket manual_smoke --page_type homepage --language en
Get-Content -Encoding utf8 E:\Warden\data\raw\benign\2026-03-24_hardening_smoke_v4\benign_capture_run.json
Get-ChildItem -Directory E:\Warden\data\raw\benign\2026-03-24_hardening_smoke_v4
```

### Result

- Confirmed `playwright-stealth` installs successfully in the local Python environment.
- Confirmed the currently installed `playwright-stealth` package exports `Stealth` rather than `stealth_sync`, and the implementation was adapted to the real local API.
- Confirmed all three Python files compile successfully.
- Confirmed the capture script and both runners expose `--goto_wait_until {load,domcontentloaded,commit,networkidle}` in `--help`.
- Confirmed the local benign smoke completed successfully with:
  - `https://www.google.com`
  - `https://cloudflare.com`
  - `https://zoom.us`
  - `https://example.com`
- Confirmed the smoke output root contains four sample directories:
  - `www.google.com_20260324T110456Z`
  - `cloudflare.com_20260324T110517Z`
  - `zoom.us_20260324T110540Z`
  - `example.com_20260324T110614Z`
- Confirmed `benign_capture_run.json` reports `returncode = 0`.
- Confirmed the smoke output root contains standard sample sidecars and screenshots without requiring any new output filenames.
- Confirmed the final cleaned-up `env.json` stays in its original compact shape and does not include the earlier experimental audit fields.

### Not Run

- a full 5-10 repetition Google stress run
- live malicious capture in the VM under the new hardening path
- the final Day 1 execution handoff at `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`

Reason:

This delivery was scoped to implementing and validating the minimum viable hardening patch.
The full Day 1 batch result still depends on the operator running the actual benign and malicious batch commands in the designated environments and returning the resulting artifacts.

---

## 7. Risks / Caveats

- The new dependency `playwright-stealth` must exist in every real execution environment, including the VM, or capture will now fail fast.
- The current local smoke proves the patch works on one Google URL and one stable control site, but it does not prove broad success across all anti-bot targets.
- Google consent handling is intentionally narrow and selector-based; it is not a generic consent framework.
- This patch does not include CDP mode, real-Chrome attachment, request-route blocking, or broader retry redesign.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-24_capture_hardening_day1_support.md`

Doc debt still remaining:

- `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` still depends on the returned batch artifacts.

---

## 9. Recommended Next Step

- Install `playwright-stealth` in the VM as well, before running malicious Day 1 batches there.
- Use the existing Day 1 commands without extra hardening flags first; the new default behavior is already built in.
- If Google-like targets still fail in a real batch, compare:
  - default `commit`
  - explicit `domcontentloaded`
  - explicit `networkidle`
  on a tiny batch before changing wider operational defaults again.
