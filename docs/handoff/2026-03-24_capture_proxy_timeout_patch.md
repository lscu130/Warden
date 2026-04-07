# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“可选代理与导航超时参数补丁”的正式交接文档。
- 若涉及精确 CLI、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CAPTURE-PROXY-TIMEOUT-PATCH-V1`
- 当前状态：`DONE`
- 本轮没有改默认行为，只给现有抓取链路补了可选参数。
- 现在 benign runner、malicious runner 和底层 capture 脚本都支持可选代理与 `nav_timeout_ms` 覆盖。
- runbook 已补充“Timeout 25000ms exceeded”时的操作建议。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-24-capture-proxy-timeout-patch
- Related Task ID: WARDEN-CAPTURE-PROXY-TIMEOUT-PATCH-V1
- Task Title: Add optional proxy and navigation-timeout CLI overrides to the current capture pipeline without changing defaults
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

Added optional proxy and navigation-timeout CLI overrides to the current capture path without changing default behavior.
The base capture script now accepts runtime `--proxy_*` and `--nav_timeout_ms` overrides, and the benign/malicious upper-layer runners now expose and forward the same knobs.
The runbook was updated with operator guidance for handling `Timeout 25000ms exceeded` cases using a longer timeout first and proxy only as an optional escalation.

---

## 2. What Changed

### Code Changes

- Updated `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` to accept optional `--proxy_server`, `--proxy_username`, `--proxy_password`, and `--nav_timeout_ms` CLI flags.
- Updated the capture script to apply the runtime navigation-timeout override to both the main capture path and the variant-capture path.
- Updated `scripts/data/benign/run_benign_capture.py` and `scripts/data/malicious/run_malicious_capture.py` to expose and forward the same optional flags to the capture script.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` with a new troubleshooting section for `Timeout 25000ms exceeded`, including concrete examples for timeout-only and timeout-plus-proxy runs.
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
- `docs/tasks/2026-03-24_capture_proxy_timeout_patch.md`
- `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`

Optional notes per file:

- The capture script still defaults to the same built-in timeout and no proxy unless explicitly overridden by CLI.
- The runner scripts only forward optional flags; they do not impose proxy usage automatically.
- The runbook guidance explicitly recommends longer timeout first and proxy second.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now retry capture with `--nav_timeout_ms <value>` without editing the script.
- Operators can now pass an explicit proxy through the benign/malicious runners instead of modifying hard-coded script constants.
- Variant capture inherits the same runtime navigation-timeout override as the main path.

### Preserved Behavior

- Existing commands without the new flags keep the previous behavior.
- Default navigation timeout remains `25000` ms.
- Default proxy behavior remains off unless explicitly configured.
- No sample-output filenames or directory contracts changed.

### User-facing / CLI Impact

- New optional CLI flags are available on:
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
Existing commands still work because all new flags are optional and default behavior remains unchanged.
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

- Confirmed the capture script help now shows `--proxy_server`, `--proxy_username`, `--proxy_password`, and `--nav_timeout_ms`.
- Confirmed the benign runner help now shows the same optional flags.
- Confirmed the malicious runner help now shows the same optional flags.
- Confirmed all three touched Python files pass `py_compile`.
- Confirmed the runbook contains both Chinese and English operator notes for timeout/proxy troubleshooting and usage examples.

### Not Run

- live capture with a real proxy
- live capture with an extended timeout in the VM

Reason:

This task was scoped to a minimal, backward-compatible CLI patch plus documentation.
The live effectiveness of proxy and timeout combinations depends on the user’s VM network environment and should be verified there during real capture runs.

---

## 7. Risks / Caveats

- This patch does not change `wait_until="load"`; it only exposes the timeout as a runtime override.
- A longer timeout can reduce false negatives for slow pages, but it can also slow batch completion on truly stuck pages.
- Proxy support is now operator-friendly, but using a bad or unstable proxy can create a different failure mode rather than fixing the original one.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-24_capture_proxy_timeout_patch.md`
- `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- In the VM, retry a small batch of the timeout-prone URLs with `--nav_timeout_ms 45000` first.
- If the same URLs still cluster as timeouts, run a small A/B comparison with and without `--proxy_server` instead of switching the whole pipeline to proxy-by-default.
- If timeout failures remain common even after longer timeout and proxy testing, the next patch should target navigation strategy itself, not just the timeout knob.
