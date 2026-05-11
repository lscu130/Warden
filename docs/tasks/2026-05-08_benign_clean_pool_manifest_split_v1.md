# TASK_20260508_BENIGN_CLEAN_POOL_MANIFEST_SPLIT_V1

## 中文版

本任务把已经人工清洗的 Tranco benign `T00_clear_benign` / `T01_benign_hard_negative` 样本冻结为可复现的 clean-pool manifest 和 group-based train / val / test split。

执行范围只包括 manifest 脚本、生成的 CSV / Markdown 报告、以及本任务 / handoff 文档。不训练模型，不运行 teacher distillation，不运行 OCR / YOLO / CLIP，不移动或修改原始样本目录，不改变标签、schema、训练、推理、采集或评估逻辑。

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260508-BENIGN-CLEAN-POOL-MANIFEST-SPLIT-V1
- Task Title: Build Clean Benign Pool Manifest And Group-Based Train/Val/Test Split
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; external task `C:\Users\20516\Downloads\TASK_20260508_BENIGN_CLEAN_POOL_MANIFEST_SPLIT_V1.md`
- Created At: 2026-05-08
- Requested By: User

## 1. Background

The Tranco benign data has already been manually cleaned into triage buckets under `E:\WardenData\manifests\tranco_benign_triage_v1`.
The active clean candidate inputs for this task are:

- `T00_clear_benign`
- `T01_benign_hard_negative`

The task converts those directories into auditable CSV manifests and deterministic group-based train / validation / test splits.

## 2. Goal

Generate a reproducible benign clean-pool manifest set for V1, including artifact completeness checks, group keys, group-based splits, and a bilingual cleaning report.

## 3. Scope In

Allowed files / artifacts:

- `scripts/data/benign/build_benign_clean_pool_manifest.py`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_excluded_or_incomplete_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_cleaning_report_v1.md`
- `docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md`
- `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`

Allowed changes:

- Add a standalone manifest / split builder script.
- Generate CSV manifests and a Markdown report.
- Add repo-local task and handoff documents.

## 4. Scope Out

This task must not:

- train any model;
- run teacher distillation;
- run OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or any inference model;
- modify L1/L2 schema;
- modify frozen labels or enums;
- change sample labels;
- move or delete original sample directories;
- mix T90/T99 or suspicious / bad-capture samples into the clean benign pool;
- use external web lookup;
- change unrelated CLI behavior;
- add third-party dependencies;
- perform broad unrelated refactors.

## 5. Inputs

Input triage root:

- `E:\WardenData\manifests\tranco_benign_triage_v1`

Input buckets:

- `T00_clear_benign`
- `T01_benign_hard_negative`

Relevant docs:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Missing inputs:

- none after local path inspection.

## 6. Required Outputs

Required output files:

- `tranco_benign_clean_pool_v1.csv`
- `tranco_benign_excluded_or_incomplete_v1.csv`
- `benign_train_manifest_v1.csv`
- `benign_val_manifest_v1.csv`
- `benign_test_manifest_v1.csv`
- `tranco_benign_cleaning_report_v1.md`
- repo-local handoff document
- script path and regeneration command

Regeneration command:

```powershell
python scripts/data/benign/build_benign_clean_pool_manifest.py `
  --input-root "E:\WardenData\manifests\tranco_benign_triage_v1" `
  --output-dir "E:\WardenData\manifests\benign_clean_v1" `
  --split 0.8 0.1 0.1 `
  --seed 42
```

## 7. Hard Constraints

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content.
- Markdown documents must be bilingual by default.
- Do not train models.
- Do not run teacher distillation.
- Do not run visual or OCR models.
- Do not alter original manual labels.
- Do not use generated `triage_label` as future model input; it is a supervision / dataset-management field only.

## 8. Interface / Schema Constraints

- Schema change allowed: NO.
- Frozen field names involved: none.
- New CSV manifests are dataset-management artifacts only, not frozen model output schema.
- Existing dataset artifact names and existing CLI commands are preserved.

## 9. Evidence / Retrieval Rules

Required evidence:

- actual scanned T00/T01 counts;
- clean and excluded counts;
- split counts by T00/T01;
- group leakage check;
- source directory count check after generation;
- generated CSV structure check;
- deterministic rerun hash check for CSV outputs;
- git status for scoped files.

Allowed evidence sources:

- local filesystem scan;
- generated CSV files;
- script stdout;
- repository docs and scripts;
- Git status / diff output.

## 10. Acceptance Criteria

- [x] Manifest generation script exists.
- [x] Clean-pool CSV exists.
- [x] Excluded / incomplete CSV exists.
- [x] Train / val / test CSV manifests exist.
- [x] Split is group-based.
- [x] Group leakage check passes.
- [x] T00/T01 distribution per split is recorded.
- [x] Validation and test splits retain enough T01 hard negatives for later false-positive analysis.
- [x] Cleaning report exists.
- [x] Original sample directories and manual labels were not modified by the script.
- [x] No model training, distillation, OCR, YOLO, CLIP, or external web lookup was performed.

## 11. Validation Checklist

Commands run:

```powershell
python -m py_compile scripts/data/benign/build_benign_clean_pool_manifest.py
python scripts/data/benign/build_benign_clean_pool_manifest.py --input-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1" --split 0.8 0.1 0.1 --seed 42
python - <inline CSV validation and group leakage check>
python - <inline CSV hash before/after deterministic rerun check>
python scripts/ci/check_task_doc.py docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md
git status --short --untracked-files=all
```

Validation results are recorded in the handoff.

