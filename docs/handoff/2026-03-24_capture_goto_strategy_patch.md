# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“导航等待策略与超时回退补丁”的正式交接文档。
- 若涉及精确 CLI、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CAPTURE-GOTO-STRATEGY-PATCH-V1`
- 当前状态：`DONE`
- 本轮没有改输出结构，只补了导航等待策略控制与最小回退。
- 现在 capture 脚本和两条 runner 都支持可选 `--goto_wait_until`。
- 默认仍从 `load` 开始，但如果 `load` 导航超时，会自动回退再试一次 `domcontentloaded`。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-24-capture-goto-strategy-patch
- Related Task ID: WARDEN-CAPTURE-GOTO-STRATEGY-PATCH-V1
- Task Title: Add optional goto wait-until control and load-timeout fallback to the current capture pipeline without changing output contracts
- Module: Data module / capture operations
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

Added an optional `--goto_wait_until` CLI control to the current capture path and implemented a minimal fallback from `load` timeout to `domcontentloaded`.
The base capture script now starts with the operator-selected wait-until mode, defaults to `load`, and automatically retries once with `domcontentloaded` when the initial `load` navigation attempt times out.
The benign and malicious runners now expose and forward the new flag, and the runbook was updated to explain the new behavior and when to use it explicitly.

---

## 2. What Changed

### Code Changes

- Updated `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` to accept optional `--goto_wait_until`.
- Added a narrow navigation helper that retries once with `domcontentloaded` when the initial `wait_until="load"` navigation times out.
- Updated both the main capture path and the variant-capture path to use the new wait-until parameter and fallback behavior.
- Updated `scripts/data/benign/run_benign_capture.py` and `scripts/data/malicious/run_malicious_capture.py` to expose and forward `--goto_wait_until`.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` with new troubleshooting guidance for timeout-prone sites and explicit `--goto_wait_until domcontentloaded` examples.
- Added the active task document for this patch.
- Added this handoff document.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-24_capture_goto_strategy_patch.md`
- `docs/handoff/2026-03-24_capture_goto_strategy_patch.md`

Optional notes per file:

- The capture script still defaults to `load`, so existing commands preserve the prior visible navigation mode.
- The runner scripts only forward the new flag; they do not force a new default at the upper layer.
- The runbook now documents both the automatic fallback and the explicit override path.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now explicitly choose `--goto_wait_until load` or `--goto_wait_until domcontentloaded`.
- If the current mode is `load` and the navigation attempt times out, the capture script now retries once with `domcontentloaded`.
- Timeout-prone sites that still render meaningful DOM before full page `load` can now succeed without requiring a broader pipeline rewrite.

### Preserved Behavior

- Existing commands without the new flag keep `load` as the initial navigation mode.
- Existing proxy and navigation-timeout behavior remains available and unchanged.
- No sample-output filenames or directory contracts changed.

### User-facing / CLI Impact

- New optional CLI flag available on:
  - `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
  - `scripts/data/benign/run_benign_capture.py`
  - `scripts/data/malicious/run_malicious_capture.py`

### Output Format Impact

- none

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` CLI
- `scripts/data/benign/run_benign_capture.py` CLI
- `scripts/data/malicious/run_malicious_capture.py` CLI

Compatibility notes:

This patch is additive at the CLI level only.
Existing commands still work because the new flag is optional, `load` remains the default initial mode, and the fallback only activates on timeout-like failure for the initial `load` attempt.
No JSON schema, sample file naming, or downstream artifact structure changed.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py E:\Warden\scripts\data\benign\run_benign_capture.py E:\Warden\scripts\data\malicious\run_malicious_capture.py
```

### Result

- Confirmed the capture script help now shows `--goto_wait_until {load,domcontentloaded}`.
- Confirmed the benign runner help now shows `--goto_wait_until {load,domcontentloaded}`.
- Confirmed the malicious runner help now shows `--goto_wait_until {load,domcontentloaded}`.
- Confirmed all three touched Python files pass `py_compile`.
- Confirmed the runbook now documents:
  - the automatic fallback from `load` timeout to `domcontentloaded`,
  - the explicit `--goto_wait_until domcontentloaded` override path,
  - the recommendation to try longer timeout first, then explicit looser navigation mode, then proxy if still needed.

### Not Run

- live capture with timeout-prone real URLs in the VM
- live A/B comparison between `load` and `domcontentloaded` on the same site set

Reason:

This task was scoped to a minimal, backward-compatible navigation-strategy patch plus documentation.
Real effectiveness on the user’s timeout-prone sites still depends on VM-side live capture and should be verified there.

---

## 7. Risks / Caveats

- `domcontentloaded` is looser than `load`, so some pages may be captured slightly earlier in their render lifecycle when this mode is used or when fallback succeeds.
- The fallback only addresses timeout-prone navigation completion; it does not solve all causes of blocked, blank, or anti-bot pages.
- If a site still fails under longer timeout plus `domcontentloaded`, the next step is likely a more specific navigation/readiness heuristic rather than another generic timeout increase.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-24_capture_goto_strategy_patch.md`
- `docs/handoff/2026-03-24_capture_goto_strategy_patch.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- In the VM, retry a small batch of the previously timeout-prone URLs with:
  - `--nav_timeout_ms 45000`
  - default `load` first, letting the new automatic fallback run if needed
- If that still leaves a cluster of failures, run an explicit comparison with `--goto_wait_until domcontentloaded`.
- If both paths still fail on the same sites, the next patch should target page-readiness success criteria rather than generic navigation timeout alone.
