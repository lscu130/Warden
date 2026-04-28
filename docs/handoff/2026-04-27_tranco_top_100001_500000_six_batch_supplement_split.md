# 2026-04-27_tranco_top_100001_500000_six_batch_supplement_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

- 已按 `E:\Warden\tranco csv` 内现有 `top_100001_500000` 最高批次位置继续切分。
- 新增 `6` 个批次：`batch_0017` 到 `batch_0022`。
- 每个批次都有规范化 CSV 和 URL-only TXT。
- 新源文件已复制到 repo：`E:\Warden\tranco csv\sources\tranco_QW4P4.csv`。
- 这次只生成 split artifacts，不安排 Day N capture 队列。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-27-tranco-top100001-500000-six-batch-supplement-split
- Related Task ID: WARDEN-TRANCO-TOP100001-500000-SIX-BATCH-SUPPLEMENT-SPLIT-V1
- Task Title: Generate six additional Tranco top_100001_500000 benign split batches after the current folder position
- Module: Data module / benign batch staging
- Author: Codex
- Date: 2026-04-27
- Status: DONE

---

## 1. Executive Summary

Generated six additional repo-local Tranco benign split batches from the user-provided source CSV.
The split continues the current `top_100001_500000` folder position after `batch_0016`, producing `batch_0017` through `batch_0022`.

No existing split artifact was overwritten.
No capture job was scheduled or executed.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`.
- Added `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`.

### Output / Artifact Changes

- Added `E:\Warden\tranco csv\sources\tranco_QW4P4.csv`.
- Added `E:\Warden\tranco csv\supplement_split_summary_2026-04-27_top_100001_500000_batches_0017_0022.json`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022.csv`.
- Added `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022_urls.txt`.

---

## 3. Files Touched

- `docs/tasks/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`
- `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`
- `E:\Warden\tranco csv\sources\tranco_QW4P4.csv`
- `E:\Warden\tranco csv\supplement_split_summary_2026-04-27_top_100001_500000_batches_0017_0022.json`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022_urls.txt`

---

## 4. Behavior Impact

### Expected New Behavior

- Future benign capture planning can assign six additional Tranco `top_100001_500000` batches.
- The new batches continue local numbering after `tranco_top_100001_500000_batch_0016`.
- The new TXT files can be passed directly to `scripts/data/benign/run_benign_capture.py`.

### Preserved Behavior

- Existing split artifacts remain unchanged.
- Existing CSV schema remains `rank,domain,url`.
- Existing URL TXT format remains one URL per line.
- Existing capture runner behavior is unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for existing outputs; new files follow the existing output format.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This delivery adds data artifacts only.
It does not modify runner scripts, CLI flags, JSON schemas, label semantics, or capture output contracts.

---

## 6. Validation Performed

### Commands Run

```powershell
Get-ChildItem -LiteralPath 'E:\Warden\tranco csv' | Sort-Object Name | Select-Object -ExpandProperty Name
Get-Content -LiteralPath 'C:\Users\20516\Downloads\tranco_QW4P4.csv' -TotalCount 5
Copy-Item -LiteralPath 'C:\Users\20516\Downloads\tranco_QW4P4.csv' -Destination 'E:\Warden\tranco csv\sources\tranco_QW4P4.csv' -Force
generated batches with a bounded Python split script using existing split CSVs as the exclusion set
validated generated CSV/TXT row counts, headers, duplicate domains, and summary JSON with a bounded Python validation script
```

### Result

- Confirmed source format is headerless `rank,domain`.
- Confirmed current `top_100001_500000` max local batch index was `0016` before generation.
- Generated exactly `6000` selected rows.
- Generated exactly `6` batches: `0017` through `0022`.
- Confirmed `available_rows_after_exclusion` was `369542`.
- Confirmed each generated CSV has `1000` data rows and header `rank,domain,url`.
- Confirmed each generated TXT has `1000` URL lines.
- Confirmed no generated domains overlap existing repo-local Tranco split domains.
- Confirmed no generated domains duplicate across the six new batches.

Generated rank ranges:

- `batch_0017`: `100003` to `167577`
- `batch_0018`: `167644` to `234226`
- `batch_0019`: `234290` to `300992`
- `batch_0020`: `301059` to `367445`
- `batch_0021`: `367510` to `433931`
- `batch_0022`: `433995` to `499934`

### Not Run

- live benign capture on the new batches
- Day N capture planning / tracker assignment for these new batches
- downstream deduplication or TrainSet V1 admission checks

Reason:

The user requested split generation only.
Capture scheduling and result receipt are separate tasks.

---

## 7. Risks / Caveats

- These are benign candidate input batches, not verified successful benign captures.
- The source CSV has more than one million rows; this task intentionally used only the `top_100001_500000` bucket to continue the current folder position.
- Future planning should still account for duplicate removal, capture failures, redirects, gated pages, and TrainSet V1 admission rules.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`
- `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`

Doc debt still remaining:

- none for the split-generation task

---

## 9. Recommended Next Step

- If these six batches should be scheduled, create the next Day N Plan A capture task and assign the desired subset from `batch_0017` through `batch_0022`.
- Keep using `E:\WardenData\raw\benign\tranco\...` as the output root for future Tranco benign capture runs.
