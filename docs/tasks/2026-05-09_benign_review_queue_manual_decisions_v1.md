# Task Metadata

- Task ID: TASK-20260509-BENIGN-REVIEW-QUEUE-MANUAL-DECISIONS-V1
- Task Title: Freeze Benign Review Queue Manual Decisions From Directory State
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Related Issue / ADR / Doc: user review note in current thread; docs/handoff/2026-05-09_benign_review_queue_export_v1.md
- Created At: 2026-05-09
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

本任务按用户确认的规则，把当前 `benign_clean_v1_review_queue` 目录状态固化为人工审查结论：以 bucket 内仍存在的候选/样本子文件夹为准，仍存在即保留；原 CSV 有但当前目录不存在的条目视为已从复核队列人工移除。

本任务只生成 review decision CSV/report，不改原始样本、不改标签、不改 split manifest、不自动重切分。

## English Version

This English section is authoritative.

## 1. Background

The benign review queue was exported under `E:\WardenData\manifests\benign_clean_v1_review_queue`. The user manually reviewed the queue and stated that current directory subfolders should be treated as authoritative.

Manual review notes supplied by the user:

- R01 screenshots have visible text, likely client-rendered text not captured by the crawler.
- R02 does not need removal.
- R03 can keep candidates that remain in the candidate folders.
- R04 can keep candidates that remain in the candidate folders.
- R05 can all be kept because similar DOM hashes did not correspond to the same webpage in screenshot review.

## 2. Goal

Generate a reproducible, read-only decision manifest and report that freeze the current manual review queue directory state into dataset-management decisions without mutating source samples, labels, split manifests, or schemas.

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/freeze_benign_review_queue_manual_decisions.py`
- `docs/tasks/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- `docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decisions_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decision_report_v1.md`

This task is allowed to change:

- Add one read-only decision-freezing script.
- Add repo-local task and handoff docs.
- Generate manual decision CSV/report under the existing review queue root.

## 4. Scope Out

This task must NOT do the following:

- move, delete, rename, or relabel original source samples
- edit existing train/validation/test manifests
- regenerate split manifests
- change human labels
- modify schema, labels, enums, training code, inference code, capture code, or evaluation logic
- run model training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or external web lookup
- convert review candidates into confirmed leakage or confirmed bad samples
- make benchmark-readiness claims

## 5. Inputs

### Docs

- `docs/handoff/2026-05-09_benign_review_queue_export_v1.md`

### Code / Scripts

- `scripts/data/benign/export_benign_review_queue.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1_review_queue\review_queue_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\missing_visible_text_review_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\duplicate_template_review_v1.csv`
- current review queue bucket directories under `E:\WardenData\manifests\benign_clean_v1_review_queue`

### Prior Handoff

- `docs/handoff/2026-05-09_benign_review_queue_export_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- `scripts/data/benign/freeze_benign_review_queue_manual_decisions.py`
- `docs/tasks/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- `docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decisions_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decision_report_v1.md`

## 7. Hard Constraints

- Use current review queue subdirectories as the authority.
- Ignore administrative folders such as `removed` when counting kept candidate/sample folders.
- Treat missing original CSV rows as removed from the review queue only, not removed from source data.
- Preserve traceability to source paths.
- Do not mutate source samples, labels, manifests, schemas, training, inference, capture, or evaluation logic.

## 8. Interface / Schema Constraints

- Schema changed allowed: no.
- Manual decision CSV is a dataset-management artifact only.
- Existing manifests and review queue source CSVs must not be modified.
- New script CLI is additive and standard-library based.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- current bucket directory counts
- keep/remove decision counts
- specific removed R01 sample IDs
- generated decision CSV/report paths
- checker validation results

Allowed evidence sources:

- current review queue directories and CSVs
- generated manual decision CSV/report
- command output from validation runs

Retrieval budget:

- Initial retrieval: current bucket directory listing and review CSV headers.
- Additional retrieval is allowed only when a required count or mapping is ambiguous.
- Stop retrieval when the decision CSV/report and validation output provide the required evidence.

Missing-evidence behavior:

- Mark unmatched directories as `directory_only`; do not silently drop them.

### 9.1 Counter-Review Requirements

Required because this task records manual review decisions affecting dataset hygiene.

- Confirm decisions are review-queue decisions, not label changes.
- Confirm R05 DOM hash similarity is not treated as confirmed same-page leakage.
- Confirm R01 visible text gaps are not automatically repaired or excluded in this task.

## 10. Acceptance Criteria

- Decision-freezing script compiles and runs.
- Manual decision CSV/report are generated.
- Administrative `removed` folders are not counted as kept candidates.
- Current kept directory counts are recorded.
- Removed review queue items are recorded.
- Task and handoff docs pass repo checkers.

## 11. Validation Checklist

- [x] `python -m py_compile scripts/data/benign/freeze_benign_review_queue_manual_decisions.py`
- [x] `python scripts/data/benign/freeze_benign_review_queue_manual_decisions.py --review-root "E:\WardenData\manifests\benign_clean_v1_review_queue"`
- [x] Read generated manual decision report.
- [x] Group generated decisions by bucket/status.
- [x] List removed R01 sample IDs.
- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-09_benign_review_queue_manual_decisions_v1.md`
- [x] `git status --short --untracked-files=all`

## 12. Stop Rules

Stop as done when manual decision CSV/report are generated, validation passes, and handoff records actual counts and caveats.

Stop as partial if directory-only rows remain and cannot be reconciled.

Stop as blocked if review queue manifests are missing or the directory state cannot be read.
