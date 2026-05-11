# Task Metadata

- Task ID: TASK-20260509-BENIGN-APPLY-MANUAL-REMOVED-SAMPLES-V1
- Task Title: Apply Manual Removed R01 Samples To Benign Clean Manifests And Source Directories
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Related Issue / ADR / Doc: user instruction in current thread; docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md
- Created At: 2026-05-09
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

本任务按用户明确指令，把人工 review queue 中 R01 已移除的样本同步应用到 `benign_clean_v1`，并删除 review queue 与 `tranco_benign_triage_v1` 中对应目录。

这是 targeted destructive cleanup：只处理 `manual_review_decisions_v1.csv` 中 `manual_status=removed_from_review_queue_by_manual_action` 的 4 个 R01 样本。

## English Version

This English section is authoritative.

## 1. Background

The user reviewed the benign review queue and asked to remove the corresponding samples from `benign_clean_v1`, the review queue, and the original `tranco_benign_triage_v1` sample directories.

The authoritative source for this task is `manual_review_decisions_v1.csv`, specifically R01 rows with `manual_status=removed_from_review_queue_by_manual_action`.

## 2. Goal

Apply the manually removed R01 samples to `benign_clean_v1` manifests and delete the corresponding review-copy directories and original triage sample directories, while preserving all unrelated samples, labels, schemas, and code behavior.

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/apply_benign_review_queue_removed_samples.py`
- `docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_report_v1.md`
- corresponding deleted review queue R01 removed directories
- corresponding deleted original sample directories under `E:\WardenData\manifests\tranco_benign_triage_v1`

This task is allowed to change:

- Remove only the 4 manually removed R01 sample rows from clean pool and split manifests.
- Delete only the corresponding review queue removed-copy directories.
- Delete only the corresponding original triage sample directories under the approved triage root.

## 4. Scope Out

This task must NOT do the following:

- regenerate the split
- change remaining sample labels
- modify schemas, label enums, training code, inference code, capture code, or evaluation logic
- run model training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or external web lookup
- delete any sample not listed as `removed_from_review_queue_by_manual_action`
- change duplicate/template candidate decisions

## 5. Inputs

### Docs

- `docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md`

### Code / Scripts

- `scripts/data/benign/freeze_benign_review_queue_manual_decisions.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decisions_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- corresponding source sample directories under `E:\WardenData\manifests\tranco_benign_triage_v1`

### Prior Handoff

- `docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- `scripts/data/benign/apply_benign_review_queue_removed_samples.py`
- `docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_report_v1.md`

## 7. Hard Constraints

- Delete only the 4 sample IDs identified by the manual decision CSV.
- Enforce path safety: review queue deletions must stay under the review root; original sample deletions must stay under `tranco_benign_triage_v1`.
- Preserve unrelated samples and manifests.
- Do not relabel remaining data.
- Do not regenerate split membership.

## 8. Interface / Schema Constraints

- Existing manifest schemas must stay unchanged.
- Row counts may change only by targeted row removal.
- New apply CSV/report are dataset-management artifacts only.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- exact sample IDs removed
- before/after row counts
- source directory deletion status
- review queue directory deletion status
- residual sample ID search in clean manifests

Allowed evidence sources:

- current review decision CSV
- current clean/split manifests
- filesystem existence checks
- generated apply CSV/report
- command output from validation runs

Retrieval budget:

- Initial retrieval: manual decisions, clean/split manifest hits, review queue removed directories.
- Additional retrieval is allowed only when a required count or deletion status is missing.
- Stop retrieval when apply report and validation output provide the required evidence.

Missing-evidence behavior:

- Report missing rows or missing directories explicitly; do not infer successful deletion without checking.

### 9.1 Counter-Review Requirements

Required because this task performs destructive data cleanup.

- Confirm only the 4 approved sample IDs are targeted.
- Confirm path safety before deletion.
- Confirm derived reports may be stale after targeted row removal.

## 10. Acceptance Criteria

- Apply script compiles and runs.
- Clean pool rows decrease from `20253` to `20249`.
- Train rows decrease from `16202` to `16200`.
- Validation rows decrease from `2025` to `2023`.
- Test rows remain `2026`.
- Removed sample IDs no longer appear in clean/split manifests.
- Corresponding review queue removed-copy directories no longer exist.
- Corresponding original triage sample directories no longer exist.
- Task and handoff docs pass repo checkers.

## 11. Validation Checklist

- [x] `python -m py_compile scripts/data/benign/apply_benign_review_queue_removed_samples.py`
- [x] Run apply script with manifest, review, and triage roots.
- [x] Verify removed sample IDs no longer appear in clean/split manifests.
- [x] Verify corresponding original triage sample directories no longer exist.
- [x] Verify corresponding review queue removed-copy directories no longer exist.
- [x] Read generated apply CSV/report.
- [x] Verify latest split row and label counts.
- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- [x] `git status --short --untracked-files=all`

## 12. Stop Rules

Stop as done when the targeted removals are applied, deletion status is verified, apply report is generated, and validation passes.

Stop as blocked if any target path falls outside the approved roots.
