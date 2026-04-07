# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PT `verified_online.csv` 日期筛选辅助脚本的正式 handoff。
- 若涉及精确命令、输出字段、验证结果、兼容性结论或风险说明，以英文版为准。

### 摘要

- 对应任务：`WARDEN-PHISHTANK-VERIFIED-CSV-FILTER-V1`
- 任务主题：为 PT `verified_online.csv` 新增按 `verification_time` 日期筛选并导出 URL-only CSV 的辅助脚本
- 当前状态：`DONE`
- 所属模块：Data module / malicious staging

### 当前交付要点

- 新增了一个 PT 专用脚本，会先提示输入类似 `2026/3/27` 的日期，再按 `verification_time` 的 UTC 日期做包含式筛选。
- 输出 CSV 只有一列 `url`，用于后续单独抓取准备。
- 现有 malicious ingest / capture 主流程没有被改动，只补了 runbook 用法和任务交接文档。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-27-phishtank-verified-csv-filter-handoff
- Related Task ID: WARDEN-PHISHTANK-VERIFIED-CSV-FILTER-V1
- Task Title: Add a PT-specific verified_online CSV date filter that exports a URL-only CSV for later capture
- Module: Data module / malicious staging
- Author: Codex
- Date: 2026-03-27
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.
- Write this Markdown handoff in bilingual form by default: Chinese summary first, full English version second, with English authoritative for exact facts, commands, validation, and compatibility statements.

---

## 1. Executive Summary

Added a PT-specific helper script at `scripts/data/malicious/export_phishtank_verified_urls.py`.
The script prompts for a start date in `YYYY/M/D` style, filters a local `verified_online.csv` on or after that UTC verification date using the `verification_time` column, and writes an additive CSV containing only the `url` header and selected URLs.

Also updated the malicious ingest runbook with a documented operator workflow for this helper.
The existing public-feed ingest and capture scripts were not modified.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/malicious/export_phishtank_verified_urls.py`.

### Doc Changes

- Added `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`.
- Added `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`.
- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`.

### Output / Artifact Changes

- none committed
- a temporary validation CSV was generated under `data/processed/pt_csv_exports/` and removed after inspection
- no existing output artifacts were overwritten

---

## 3. Files Touched

- `scripts/data/malicious/export_phishtank_verified_urls.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`
- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`

Optional notes per file:

- The new script is additive and does not change the current malicious capture CLI.
- The runbook update documents the helper as a preprocessing step before later capture.
- The task and handoff files freeze scope and validation for this change.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now take a local PT `verified_online.csv`, enter a start date such as `2026/3/27`, and export a URL-only CSV for rows whose `verification_time` UTC date is on or after that day.
- The exported CSV contains only one header column: `url`.
- The helper preserves source row order instead of introducing a new sort policy.

### Preserved Behavior

- `scripts/data/malicious/ingest_public_malicious_feeds.py` behavior is unchanged.
- `scripts/data/malicious/run_malicious_capture.py` behavior is unchanged.
- Existing malicious capture output structure is unchanged.

### User-facing / CLI Impact

- additive only: there is a new helper command under `scripts/data/malicious/export_phishtank_verified_urls.py`

### Output Format Impact

- existing outputs are unchanged
- the new helper writes a new additive CSV format with a single `url` column

Do not hand-wave here.
If behavior did not change, say so explicitly.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This change is additive.
No existing script CLI, sample schema, manifest schema, or capture output contract was renamed or altered.
The new helper consumes existing PT CSV fields `url` and `verification_time` but does not change them.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

List what was actually checked.

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py
python subprocess wrapper invoking E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py with stdin "2026/3/27\n" and source C:\Users\20516\Downloads\verified_online.csv
inspect temporary output CSV header and first rows
```

### Result

- Confirmed the script passes `py_compile`.
- Confirmed the script accepted `2026/3/27` input and completed successfully against `C:\Users\20516\Downloads\verified_online.csv`.
- Confirmed the script reported:
  - `total_rows=56010`
  - `selected_urls=21`
  - `missing_url_rows=0`
  - `missing_verification_rows=0`
  - `invalid_verification_rows=0`
  - `latest_verification_time_utc=2026-03-27T07:03:16Z`
- Confirmed the temporary output CSV header was exactly `url`, and the first exported rows were URL values.

### Not Run

- live malicious capture using the exported CSV
- conversion from exported CSV to TXT for `run_malicious_capture.py`
- downstream cluster / pool / exclusion stages

Reason:

This task only adds the PT-specific preprocessing helper and its documentation.
Actual capture and later malicious data pipeline stages remain separate operator workflows.

---

## 7. Risks / Caveats

- The date boundary is interpreted against the source timestamp's UTC calendar date. This is intentional and auditable, but operators should not assume local-time conversion.
- The helper currently exports a URL-only CSV, not a one-URL-per-line TXT file. Later capture still needs a TXT path or another explicit extraction step for the `url` column.
- The validation used the provided `verified_online.csv` sample shape; if a future PT export changes column names, the script will fail fast with a missing-column error.

If there are no meaningful risks, say `none`.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`
- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`

Doc debt still remaining:

- none

If none, say `none`.

---

## 9. Recommended Next Step

- Use `scripts/data/malicious/export_phishtank_verified_urls.py` against the latest PT `verified_online.csv` whenever you need a fresh URL-only staging CSV for a date window.
- If you want direct capture from that export, add a tiny follow-up helper that converts the single-column CSV into a one-URL-per-line TXT file for `run_malicious_capture.py`.
- If PT later changes CSV field names or adds alternate timestamp columns, freeze that new schema explicitly in a follow-up task instead of patching assumptions ad hoc.
