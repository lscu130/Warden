# Task Metadata

- Task ID: TASK-20260508-BENIGN-SPLIT-LEAKAGE-AUDIT-V1
- Task Title: Audit Benign Train/Val/Test Split For Leakage And Temporal Distribution
- Owner Role: CODEX
- Priority: High
- Status: DONE
- Related Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260508_BENIGN_SPLIT_LEAKAGE_AUDIT_V1.md; docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md
- Created At: 2026-05-08
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

本任务对现有 benign clean V1 train / val / test manifest 做只读泄露与时间分布审计。任务只允许新增审计脚本、repo task/handoff、以及 `E:\WardenData\manifests\benign_clean_v1` 下的审计 CSV/Markdown 报告。

硬边界：不重新切分，不移动样本，不修改人工标签，不修改现有 manifest，不训练模型，不运行 teacher / OCR / YOLO / CLIP / MobileCLIP / SpecularNet，不新增第三方依赖。

## English Version

This English section is authoritative.

## 1. Background

The benign clean pool V1 split has already been generated from manually triaged `T00_clear_benign` and `T01_benign_hard_negative` samples. Before using the split for training or evaluation claims, Warden needs a read-only leakage and temporal-distribution audit over the existing manifests.

The accepted current split inputs report:

- clean pool rows: `20253`
- train rows: `16202`
- validation rows: `2025`
- test rows: `2026`
- train T01: `1684`
- validation T01: `210`
- test T01: `211`

## 2. Goal

Create and run a reproducible, read-only audit that checks the existing benign train/validation/test manifests for exact split leakage, lightweight near-duplicate risk, grouping concentration, label-bucket balance, and capture-time distribution.

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/audit_benign_split_leakage.py`
- `docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`
- `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_report_v1.md`

This task is allowed to change:

- Add a read-only audit script.
- Add repo-local task and handoff documentation.
- Write the two audit output artifacts listed above.

## 4. Scope Out

This task must NOT do the following:

- regenerate train / validation / test split files
- modify existing manifest files or sample directories
- move, rename, delete, or copy samples
- change any human labels, label semantics, schema, CLI contracts, model outputs, training, inference, capture, or evaluation logic
- run teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, or external web services
- add third-party dependencies
- use `triage_label` as model input
- make benchmark or paper claims beyond this audit result

## 5. Inputs

### Docs

- `C:\Users\20516\Downloads\TASK_20260508_BENIGN_SPLIT_LEAKAGE_AUDIT_V1.md`
- `docs/tasks/2026-05-08_benign_clean_pool_manifest_split_v1.md`
- `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`

### Code / Scripts

- `scripts/data/benign/build_benign_clean_pool_manifest.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- sample artifacts referenced by `current_path`, read-only

### Prior Handoff

- `docs/handoff/2026-05-08_benign_clean_pool_manifest_split_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- `scripts/data/benign/audit_benign_split_leakage.py`
- `docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`
- `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_report_v1.md`

Required report content:

- split row counts and T00/T01 counts
- exact leakage counts
- visible-text and DOM duplicate / near-duplicate findings
- host, eTLD+1, and group concentration
- temporal distribution
- artifact availability
- not-run and partial-check caveats
- recommended follow-up tasks

## 7. Hard Constraints

- Keep the audit read-only for existing manifests and samples.
- Do not alter split membership or labels.
- Do not add dependencies.
- Do not run model or visual inference tooling.
- Do not modify unrelated workflow, schema, label, training, inference, capture, or evaluation files.

## 8. Interface / Schema Constraints

- Existing manifest schemas must remain unchanged.
- Existing split CSV files must remain unchanged.
- New audit CSV is an additive report artifact only.
- New audit script CLI must be self-contained and use only standard-library dependencies.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- split row counts and label counts
- exact cross-split leakage counts
- artifact availability and near-duplicate counts
- temporal distribution

Allowed evidence sources:

- current repo files listed in Scope In and Inputs
- existing manifests under `E:\WardenData\manifests\benign_clean_v1`
- read-only sample artifacts referenced by the manifests
- command output from validation runs

Retrieval budget:

- Initial retrieval: user task file, relevant prior task/handoff, current manifests, and sample artifacts referenced by manifests.
- Additional retrieval is allowed only when a required count, field, or validation result is missing.
- Stop retrieval when the audit report and validation output provide the required evidence.

Missing-evidence behavior:

- Mark the affected check as `not_run`, `partial`, or caveated. Do not infer absence of leakage from a check that was not run.

### 9.1 Counter-Review Requirements

Required because this task affects dataset/evaluation hygiene.

- Check whether the existing group-key split eliminates manifest-key leakage.
- Check whether exact URL/path/group leakage differs from visible-text or DOM near-duplicate risk.
- Check whether missing screenshot hashing prevents a strong "no visual leakage" claim.
- Keep the result exploratory for benchmark claims if near-duplicate or screenshot checks remain incomplete.

## 10. Acceptance Criteria

- A new audit script reads the existing manifests and lightweight sample artifacts referenced by `current_path`.
- The script writes `benign_split_leakage_audit_v1.csv` and `benign_split_leakage_audit_report_v1.md`.
- The report separates confirmed leakage, possible near-duplicate risk, grouping caveats, temporal caveats, and recommended follow-up.
- `python -m py_compile scripts/data/benign/audit_benign_split_leakage.py` succeeds.
- The audit script completes against `E:\WardenData\manifests\benign_clean_v1`.
- The generated CSV and Markdown report exist at the required paths.
- The report includes split counts, T00/T01 counts, exact leakage counts, near-duplicate counts, artifact availability, temporal distribution, not-run checks, caveats, and recommended next steps.
- Task and handoff docs pass repo checkers.

## 11. Validation Checklist

- [x] `python -m py_compile scripts/data/benign/audit_benign_split_leakage.py`
- [x] `python scripts/data/benign/audit_benign_split_leakage.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1"`
- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`
- [x] `git status --short --untracked-files=all`

## 12. Stop Rules

Stop as done when the audit artifacts are generated and validation commands pass.

Stop as partial if the script can produce manifest-level leakage results but a requested artifact class cannot be checked dependency-free; the report must mark that check as `not_run` or `partial`.

Stop as blocked if required manifest files or required CSV headers are missing.
