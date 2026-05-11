# Task Metadata

- Task ID: TASK-20260509-BENIGN-REVIEW-QUEUE-EXPORT-V1
- Task Title: Export Benign Review Queue For Missing Text And Duplicate / Template Candidates
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260509_BENIGN_REVIEW_QUEUE_EXPORT_V1.md
- Created At: 2026-05-09
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

本任务把 `benign_clean_v1` 中需要人工复核的 missing visible text 样本和 duplicate/template candidate 导出到单独 review queue。导出是复制/复核副本，不移动、不删除、不重命名、不改标签、不改 split manifest。

默认输出目录：`E:\WardenData\manifests\benign_clean_v1_review_queue`。

## English Version

This English section is authoritative.

## 1. Background

`benign_clean_v1` completed loader smoke and duplicate/template candidate review. The previous accepted result reported `20` missing or unreadable `visible_text.txt` samples and `513` duplicate/template review candidates. These are review hints, not confirmed leakage or confirmed bad samples.

## 2. Goal

Create and run a read-only exporter that builds a separate review queue directory for manual inspection while preserving original benign sample directories, labels, split manifests, schemas, training logic, inference logic, capture logic, and evaluation logic.

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/export_benign_review_queue.py`
- `docs/tasks/2026-05-09_benign_review_queue_export_v1.md`
- `docs/handoff/2026-05-09_benign_review_queue_export_v1.md`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\review_queue_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\missing_visible_text_review_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\duplicate_template_review_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\benign_review_queue_export_report_v1.md`
- review bucket directories under `E:\WardenData\manifests\benign_clean_v1_review_queue`

This task is allowed to change:

- Add one focused export script.
- Add repo-local task and handoff docs.
- Generate review queue copies and review manifests under the new output directory.

## 4. Scope Out

This task must NOT do the following:

- move, delete, rename, or relabel original samples
- edit existing train/validation/test manifests
- regenerate split manifests
- change human labels
- modify schema, labels, enums, training code, inference code, capture code, or evaluation logic
- run model training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or external web lookup
- add third-party dependencies
- convert review candidates into confirmed leakage or confirmed bad samples automatically
- make benchmark-readiness claims

## 5. Inputs

### Docs

- `C:\Users\20516\Downloads\TASK_20260509_BENIGN_REVIEW_QUEUE_EXPORT_V1.md`
- `docs/handoff/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`

### Code / Scripts

- `scripts/data/benign/smoke_benign_clean_loader.py`
- `scripts/data/benign/review_benign_split_duplicate_candidates.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1\benign_loader_smoke_artifact_summary_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_duplicate_template_review_candidates_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- source sample directories referenced by review rows, read-only source side

### Prior Handoff

- `docs/handoff/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- `scripts/data/benign/export_benign_review_queue.py`
- `docs/tasks/2026-05-09_benign_review_queue_export_v1.md`
- `docs/handoff/2026-05-09_benign_review_queue_export_v1.md`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\review_queue_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\missing_visible_text_review_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\duplicate_template_review_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\benign_review_queue_export_report_v1.md`
- `R01_missing_visible_text`
- `R02_visible_text_exact`
- `R03_dom_exact`
- `R04_visible_text_simhash`
- `R05_dom_simhash`
- `R99_unresolved_or_manifest_only`

## 7. Hard Constraints

- Read-only with respect to source sample directories and existing manifests.
- Do not mutate labels or splits.
- Do not add third-party dependencies.
- Preserve traceability from every review copy back to the original sample path.
- Do not call duplicate/template candidates leakage unless manually confirmed in a later task.
- Do not make benchmark-readiness claims.

## 8. Interface / Schema Constraints

- Schema changed allowed: no.
- Review CSVs are dataset-management artifacts only.
- Existing CSVs under `benign_clean_v1` must not be modified.
- New script CLI is additive and standard-library based.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- missing visible text exported count
- duplicate/template candidate processed count
- bucket counts
- output CSV row counts and headers
- source manifest hash stability
- source sample directory existence

Allowed evidence sources:

- current repo files listed in Scope In and Inputs
- existing manifests and review outputs under `E:\WardenData`
- command output from validation runs

Retrieval budget:

- Initial retrieval: task file, source CSV headers, prior review outputs, generated review queue report.
- Additional retrieval is allowed only when a required count, field, or validation result is missing.
- Stop retrieval when the export artifacts and validation output provide the required evidence.

Missing-evidence behavior:

- Record unresolved rows as `manifest_only` or bucket them under `R99_unresolved_or_manifest_only`; do not silently drop them.

### 9.1 Counter-Review Requirements

Required because this task affects dataset/evaluation hygiene.

- Confirm review export does not mutate the source dataset.
- Confirm candidates remain review hints and are not converted into labels.
- Confirm final benchmark leakage-free claims are not made.

## 10. Acceptance Criteria

- Export script compiles and runs.
- Review queue output directory is generated.
- Required review CSVs and report are generated.
- Missing-visible-text count is `20` unless input changed.
- Duplicate/template candidate count is `513` unless input changed.
- Bucket directories exist and counts match the generated report.
- Source split manifest hashes are unchanged before/after export.
- Task and handoff docs pass repo checkers.

## 11. Validation Checklist

- [x] `python -m py_compile scripts/data/benign/export_benign_review_queue.py`
- [x] `python scripts/data/benign/export_benign_review_queue.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1_review_queue" --copy-mode minimal`
- [x] Confirm source split manifest hashes unchanged.
- [x] Confirm output root and bucket directories exist.
- [x] Confirm output CSVs open and have headers.
- [x] Confirm missing-visible-text exported count is `20`.
- [x] Confirm duplicate/template candidate processed count is `513`.
- [x] Confirm source sample directories still exist by spot check.
- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-09_benign_review_queue_export_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-09_benign_review_queue_export_v1.md`
- [x] `git status --short --untracked-files=all`

## 12. Stop Rules

Stop as done when review queue script is added, output directory is generated, required CSVs/report are generated, validation passes, and handoff is produced.

Stop as partial when some candidates cannot be resolved but are recorded in manifest-only output, or counts differ because input files changed.

Stop as blocked when required inputs are missing, source paths cannot be resolved at all, output directory cannot be written, or source manifests/samples would need mutation.
