# Handoff: Benign Clean Pool Manifest Split V1

## 中文版

本 handoff 记录 `TASK-20260508-BENIGN-CLEAN-POOL-MANIFEST-SPLIT-V1` 的实际执行结果。

已新增一个只读 manifest/split 生成脚本，并在 `E:\WardenData\manifests\benign_clean_v1` 生成 clean pool CSV、excluded/incomplete CSV、train/val/test split CSV 和双语清洗报告。没有移动或删除原始 T00/T01 样本目录，没有改人工标签，没有训练模型，没有运行 teacher distillation、OCR、YOLO、CLIP 或外部检索。

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF-20260508-BENIGN-CLEAN-POOL-MANIFEST-SPLIT-V1
- Related Task ID: TASK-20260508-BENIGN-CLEAN-POOL-MANIFEST-SPLIT-V1
- Task Title: Build Clean Benign Pool Manifest And Group-Based Train/Val/Test Split
- Module: Dataset / Manifest / Benign Cleaning
- Author: Codex
- Date: 2026-05-08
- Status: DONE

## 1. Executive Summary

Generated a reproducible V1 benign clean-pool manifest set from `T00_clear_benign` and `T01_benign_hard_negative`.

Actual input root:

- `E:\WardenData\manifests\tranco_benign_triage_v1`

Output directory:

- `E:\WardenData\manifests\benign_clean_v1`

The task reached its defined stop condition: script, manifests, group split, cleaning report, handoff, and validation evidence exist.

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/build_benign_clean_pool_manifest.py`.
- The script scans only T00/T01, checks minimum artifacts, derives URL / host / eTLD+1 / group key fields, writes clean and excluded CSVs, performs group-based split, and writes a bilingual report.

### Doc Changes

- Added `docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md`.
- Added `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`.

### Output / Artifact Changes

- Created `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`.
- Created `E:\WardenData\manifests\benign_clean_v1\tranco_benign_excluded_or_incomplete_v1.csv`.
- Created `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`.
- Created `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`.
- Created `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`.
- Created `E:\WardenData\manifests\benign_clean_v1\tranco_benign_cleaning_report_v1.md`.

## 3. Files Touched

- `scripts/data/benign/build_benign_clean_pool_manifest.py`
- `docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md`
- `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_excluded_or_incomplete_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_cleaning_report_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- A reproducible command can regenerate benign clean-pool manifests and group-based splits:

```powershell
python scripts/data/benign/build_benign_clean_pool_manifest.py `
  --input-root "E:\WardenData\manifests\tranco_benign_triage_v1" `
  --output-dir "E:\WardenData\manifests\benign_clean_v1" `
  --split 0.8 0.1 0.1 `
  --seed 42
```

- The script preserves group integrity: one `group_key` appears in only one split.
- The script records excluded/incomplete samples instead of silently dropping them.

### Preserved Behavior

- Original sample directories are read-only inputs.
- Manual labels are not changed.
- Existing scripts and CLI behavior are not changed.
- Warden schema, labels, training, inference, capture, and evaluation logic are unchanged.

### User-facing / CLI Impact

- New standalone CLI script only. No existing CLI is changed.

### Output Format Impact

- New dataset-management CSV / Markdown artifacts were added under `E:\WardenData\manifests\benign_clean_v1`.
- Existing output formats were not changed.

## 5. Schema / Interface Impact

- Schema changed: NO.
- Backward compatible: YES.
- Public interface changed: NO.
- Existing CLI still valid: YES.

Affected schema fields / interfaces:

- none.

Compatibility notes:

The generated CSV columns are dataset-management artifacts and are not frozen model output schema.

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile scripts/data/benign/build_benign_clean_pool_manifest.py
python scripts/data/benign/build_benign_clean_pool_manifest.py --input-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1" --split 0.8 0.1 0.1 --seed 42
python - <inline CSV validation and group leakage check>
python - <inline CSV hash before/after deterministic rerun check>
python scripts/ci/check_task_doc.py docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md
git status --short --untracked-files=all
```

### Result

- Script syntax check passed.
- Manifest generation command completed successfully.
- Actual scanned counts:
  - `T00_clear_benign`: 18,149
  - `T01_benign_hard_negative`: 2,105
  - total scanned: 20,254
- Clean pool count: 20,253.
- Excluded / incomplete count: 1.
- Clean plus excluded equals scanned: 20,253 + 1 = 20,254.
- Source directories still exist with counts:
  - `T00_clear_benign`: 18,149
  - `T01_benign_hard_negative`: 2,105
- Group leakage check: PASS.
- Unique group keys in clean pool: 19,694.
- Split counts:
  - train: total 16,202; T00 14,518; T01 1,684
  - val: total 2,025; T00 1,815; T01 210
  - test: total 2,026; T00 1,815; T01 211
- CSV row counts:
  - clean pool: 20,253 rows
  - excluded / incomplete: 1 row
  - train: 16,202 rows
  - val: 2,025 rows
  - test: 2,026 rows
- CSV deterministic rerun check passed: SHA-256 hashes for all five CSV files were identical before and after rerun.
- The generated report records the same counts.

### Not Run

- Model training: not run.
- Teacher distillation: not run.
- OCR / YOLO / CLIP / MobileCLIP / SpecularNet: not run.
- External web lookup: not run.
- pHash / simhash clustering: not run.

Reason:

All are out of scope for this manifest-only task.

Next best check:

Use these manifests in a future read-only data-loader smoke before training starts.

## 7. Risks / Caveats

- The task text expected `T00_clear_benign = 18,152`, but actual scan found 18,149 T00 sample directories under the current input root. The generated report records the actual local count.
- One T00 directory named `removed` was excluded as incomplete because it lacked screenshot and URL evidence.
- Validation/test T01 counts are 210 and 211, matching the target of around 200 while preserving group integrity.
- eTLD+1 extraction uses a conservative Python stdlib approximation, not the public suffix list.
- pHash / simhash cluster fields were not generated because the task forbids adding heavy dependencies or running visual/OCR models.
- `triage_label` is a dataset-management / supervision field and must not be used as future model input.

## 8. Docs Impact

- Docs updated: YES.

Docs touched:

- `docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md`
- `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`

Doc debt still remaining:

- none for this task.

## 9. Recommended Next Step

- Run a read-only loader smoke against `benign_train_manifest_v1.csv`, `benign_val_manifest_v1.csv`, and `benign_test_manifest_v1.csv`.
- Before training, decide whether the conservative eTLD+1 grouping is sufficient or whether a public-suffix-list-backed grouping utility should be introduced in a separate task.
