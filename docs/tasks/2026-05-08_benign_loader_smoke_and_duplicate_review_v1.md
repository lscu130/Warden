# Task Metadata

- Task ID: TASK-20260508-BENIGN-LOADER-SMOKE-AND-DUPLICATE-REVIEW-V1
- Task Title: Benign Clean V1 Loader Smoke And Duplicate / Template Candidate Review
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260508_BENIGN_LOADER_SMOKE_AND_DUPLICATE_REVIEW_V1.md; docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md
- Created At: 2026-05-08
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

本任务对 `benign_clean_v1` 做两个只读检查：loader smoke 和 duplicate/template candidate review。任务只新增脚本、repo task/handoff、以及 `E:\WardenData\manifests\benign_clean_v1` 下的四个输出报告/CSV。

硬边界：不修改标签，不移动/删除/重命名/复制样本，不重切 split，不修改已有 manifest，不训练模型，不运行 teacher/OCR/YOLO/CLIP/MobileCLIP/SpecularNet，不新增重依赖。

## English Version

This English section is authoritative.

## 1. Background

`benign_clean_v1` has already gone through T00/T01 manual triage, manifest generation, group-based train/validation/test split, and read-only leakage audit. The prior audit reported strict manifest-level leakage as `0` for `sample_id`, `current_path`, `final_url`, `final_host`, `etld1`, and `group_key`, while visible-text and HTML/DOM duplicate or near-duplicate candidates remained.

Known split counts:

- train: `16202` rows, T00 `14518`, T01 `1684`
- validation: `2025` rows, T00 `1815`, T01 `210`
- test: `2026` rows, T00 `1815`, T01 `211`

## 2. Goal

Create read-only tooling and reports to validate `benign_clean_v1` loader readiness and organize visible-text / DOM duplicate-template candidates into a bounded human-review queue.

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/smoke_benign_clean_loader.py`
- `scripts/data/benign/review_benign_split_duplicate_candidates.py`
- `docs/tasks/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- `docs/handoff/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_loader_smoke_artifact_summary_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_loader_smoke_report_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_duplicate_template_review_candidates_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_duplicate_template_review_report_v1.md`

This task is allowed to change:

- Add two read-only scripts.
- Add repo-local task and handoff docs.
- Generate the four output artifacts listed above.

## 4. Scope Out

This task must NOT do the following:

- modify T00/T01/T90/T99 manual labels
- move, delete, rename, or copy source sample directories
- regenerate train/validation/test split manifests
- edit existing manifest CSVs
- train any model or run teacher distillation
- run OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or external lookup
- add heavy dependencies
- modify schema, label enums, CLI, training logic, inference logic, or runtime dataflow
- include `triage_label`, human folder names, or split names in future model input evidence packs
- describe visible-text or DOM candidates as confirmed leakage without exact sample/URL evidence

## 5. Inputs

### Docs

- `C:\Users\20516\Downloads\TASK_20260508_BENIGN_LOADER_SMOKE_AND_DUPLICATE_REVIEW_V1.md`
- `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`

### Code / Scripts

- `scripts/data/benign/audit_benign_split_leakage.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_excluded_or_incomplete_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_report_v1.md`
- sample artifacts referenced by `current_path`, read-only

### Prior Handoff

- `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- `scripts/data/benign/smoke_benign_clean_loader.py`
- `scripts/data/benign/review_benign_split_duplicate_candidates.py`
- `docs/tasks/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- `docs/handoff/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_loader_smoke_artifact_summary_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_loader_smoke_report_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_duplicate_template_review_candidates_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_duplicate_template_review_report_v1.md`

## 7. Hard Constraints

- Keep checks read-only for existing manifests and samples.
- Do not alter split membership or labels.
- Do not add dependencies.
- Do not run model or visual inference tooling.
- Do not modify unrelated workflow, schema, label, training, inference, capture, or evaluation files.
- Treat `triage_label` as supervision / dataset-management metadata, not model input evidence.

## 8. Interface / Schema Constraints

- Existing manifest schemas must remain unchanged.
- Existing split CSV files must remain unchanged.
- New CSV outputs are additive review artifacts only.
- New script CLIs must be self-contained and standard-library based.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- split row counts and label counts
- missing artifact and JSON parse failure counts
- visible-text length bucket counts
- duplicate/template candidate counts
- whether screenshot duplicate checks were run

Allowed evidence sources:

- current repo files listed in Scope In and Inputs
- existing manifests and audit outputs under `E:\WardenData\manifests\benign_clean_v1`
- read-only sample artifacts referenced by the manifests
- command output from validation runs

Retrieval budget:

- Initial retrieval: user task file, prior audit handoff, current manifests, existing audit CSV/report, and referenced sample artifacts.
- Additional retrieval is allowed only when a required count, field, or validation result is missing.
- Stop retrieval when required output artifacts and validation output provide the needed evidence.

Missing-evidence behavior:

- Mark the affected check as `not_run`, `partial`, or caveated. Do not infer absence of leakage from a check that was not run.

### 9.1 Counter-Review Requirements

Required because this task affects dataset/evaluation hygiene.

- Distinguish strict leakage from near-duplicate contamination and natural template reuse.
- Preserve the prior strict manifest-level leakage result as evidence, not as proof that all duplicate risks are absent.
- State that screenshot-level duplicate risk remains unknown because screenshot hashing was not run.
- State that current split is suitable for preliminary training / loader smoke, but not sufficient alone for final benchmark leakage-free claims.

## 10. Acceptance Criteria

- Both scripts compile and run successfully.
- Two CSV files and two Markdown reports are generated under `E:\WardenData\manifests\benign_clean_v1`.
- Loader smoke report includes split/T00/T01 counts, missing artifact counts, parse failure counts, visible-text length buckets, and `triage_label` evidence-pack warning.
- Duplicate review report does not describe candidates as confirmed leakage.
- Existing source samples, labels, and train/validation/test manifests are not modified.
- Task and handoff docs pass repo checkers.

## 11. Validation Checklist

- [x] `python -m py_compile scripts/data/benign/smoke_benign_clean_loader.py`
- [x] `python -m py_compile scripts/data/benign/review_benign_split_duplicate_candidates.py`
- [x] `python scripts/data/benign/smoke_benign_clean_loader.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1"`
- [x] `python scripts/data/benign/review_benign_split_duplicate_candidates.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1"`
- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-08_benign_loader_smoke_and_duplicate_review_v1.md`
- [x] `git status --short --untracked-files=all`

## 12. Stop Rules

Stop as done when both scripts complete, four output artifacts are generated, validation passes, and handoff reports actual results and caveats.

Stop as partial if loader smoke completes but duplicate review can only generate summary-level candidates, or artifacts are too incomplete but no data was modified.

Stop as blocked if required split manifests are missing, `current_path` is massively invalid, or continuing requires label edits, split regeneration, heavy dependencies, or model execution.
