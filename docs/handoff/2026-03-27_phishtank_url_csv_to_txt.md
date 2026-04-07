# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PT URL-only CSV 转 TXT 辅助脚本的正式 handoff。
- 若涉及精确命令、文件路径、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-PHISHTANK-URL-CSV-TO-TXT-V1`
- 任务主题：新增一个把 PT URL-only CSV 转成一行一个 URL 的 TXT 的辅助脚本，并补全完整使用命令
- 当前状态：`DONE`
- 所属模块：Data module / malicious staging

### 当前交付要点

- 新增 `convert_url_csv_to_txt.py`，输入 `url` 列 CSV，输出一行一个 URL 的 TXT。
- runbook 已补齐完整 PT 本地三步命令：导出 CSV、转 TXT、运行抓取。
- 现有 PT 过滤脚本和 malicious capture 主链路均未修改。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-27-phishtank-url-csv-to-txt-handoff
- Related Task ID: WARDEN-PHISHTANK-URL-CSV-TO-TXT-V1
- Task Title: Add a minimal helper that converts the PT URL-only CSV export into a one-URL-per-line TXT for capture
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

Added a small helper at `scripts/data/malicious/convert_url_csv_to_txt.py`.
It reads a URL-only CSV with a `url` header and writes a UTF-8 TXT file with one URL per line for `run_malicious_capture.py --input_path`.

Also updated the ingest runbook to document the full PT local workflow explicitly:

1. filter `verified_online.csv` into a URL-only CSV,
2. convert that CSV into a TXT file,
3. run malicious capture with `--input_path`.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/malicious/convert_url_csv_to_txt.py`.

### Doc Changes

- Added `docs/tasks/2026-03-27_phishtank_url_csv_to_txt.md`.
- Added `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`.
- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`.

### Output / Artifact Changes

- none committed
- temporary validation files were created under `E:\Warden\tmp\` and inspected
- no existing malicious artifacts were overwritten

---

## 3. Files Touched

- `scripts/data/malicious/convert_url_csv_to_txt.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-27_phishtank_url_csv_to_txt.md`
- `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`

Optional notes per file:

- The new script is additive and intentionally narrow.
- The runbook now includes the complete PT local command chain instead of stopping at the CSV export.
- The task and handoff files freeze scope and validation for this follow-up.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now turn the PT URL-only CSV export into a one-URL-per-line TXT without manual editing.
- The TXT output preserves source row order and contains no header row.
- The runbook now shows an explicit end-to-end PT local workflow.

### Preserved Behavior

- `scripts/data/malicious/export_phishtank_verified_urls.py` behavior is unchanged.
- `scripts/data/malicious/run_malicious_capture.py` behavior is unchanged.
- Existing malicious capture output contracts are unchanged.

### User-facing / CLI Impact

- additive only: there is a new helper command under `scripts/data/malicious/convert_url_csv_to_txt.py`

### Output Format Impact

- existing outputs are unchanged
- the new helper writes a plain TXT file with one URL per line

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This is an additive operator helper only.
No existing schema, manifest format, capture CLI, or output directory structure was changed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\data\malicious\convert_url_csv_to_txt.py
python subprocess wrapper invoking E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py with stdin "2026/3/27\n" and output E:\Warden\tmp\pt_validation_urls.csv
python E:\Warden\scripts\data\malicious\convert_url_csv_to_txt.py --input_csv E:\Warden\tmp\pt_validation_urls.csv --output_txt E:\Warden\tmp\pt_validation_urls.txt
inspect E:\Warden\tmp\pt_validation_urls.csv
inspect E:\Warden\tmp\pt_validation_urls.txt
```

### Result

- Confirmed `convert_url_csv_to_txt.py` passes `py_compile`.
- Confirmed the temporary PT URL-only CSV was generated successfully from `C:\Users\20516\Downloads\verified_online.csv` using the earlier helper.
- Confirmed the CSV contained the `url` header.
- Confirmed the TXT output contained one URL per line with no header row.
- Confirmed the temporary conversion counts were:
  - `total_rows=21`
  - `selected_urls=21`
  - `missing_url_rows=0`

### Not Run

- live malicious capture from the generated TXT
- downstream cluster / pool / exclusion stages

Reason:

This follow-up only adds the CSV-to-TXT bridge helper and the missing operator commands.
Actual capture remains a separate operational step.

---

## 7. Risks / Caveats

- The helper expects a CSV with a `url` column and fails fast if that column is missing.
- The helper does not deduplicate or normalize URLs; it preserves the CSV row order and values as provided.
- This closes the format gap to `run_malicious_capture.py`, but it does not change any capture-time timeout, proxy, or routing behavior.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-27_phishtank_url_csv_to_txt.md`
- `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- Use the documented three-step PT workflow from the runbook for future local PT batch preparation.
- If you later want this to be a single command, do that as a separate additive task instead of silently merging the two helpers now.
- If a future input CSV uses a different URL column name, freeze that change explicitly before broadening this helper.
