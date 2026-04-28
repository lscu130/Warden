<!-- operator: Codex; task: primary-benign-consistency-and-dedup; date: 2026-04-27 -->

# 中文摘要

本任务对当前 primary benign 主目录做一次一致性检查和 URL 去重。

范围：

- 输入目录：`E:\WardenData\raw\benign\benign`
- 不处理：`adult`、`gambling`、`gate`、`evasion`、`tranco`
- 先做去重 dry-run；确认只有 1 个 URL-key 重复后，删除较新的重复目录，并做 postcheck。

本任务不修改样本内部文件，不改 labels，不改 schema；只删除一个已确认 URL-key 重复的样本目录。

---

# English Version

# Task Metadata

- Task ID: 2026-04-27_primary_benign_consistency_and_dedup
- Task Title: Primary Benign Consistency And Dedup
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data
- Related Issue / ADR / Doc:
  - `docs/data/TRAINSET_V1.md`
  - `docs/handoff/2026-04-24_rebucket_content_warning_back_to_benign.md`
- Created At: 2026-04-27
- Requested By: User

---

## 1. Background

After recent content-warning and template-noise rebucketing, the current primary benign directory should be checked again for manifest consistency and URL-key duplicates.

---

## 2. Goal

Generate a fresh primary benign manifest, run the existing consistency checker, run URL-key deduplication in dry-run mode, delete the confirmed duplicate directory after review, and run post-dedup validation.

---

## 3. Scope In

Allowed input:

- `E:\WardenData\raw\benign\benign`

Allowed outputs:

- `E:\WardenData\processed\primary_benign_20260427_consistency`
- `E:\WardenData\processed\primary_benign_20260427_consistency_after_dedup`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup_delete`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup_postcheck`
- matching handoff doc

---

## 4. Scope Out

- Do not move sample directories.
- Do not edit raw sample files.
- Do not modify labels.
- Do not process adult/gambling/gate/evasion/tranco buckets.
- Do not change schema, CLI, training, inference, or capture logic.

---

## 5. Inputs

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `E:\WardenData\raw\benign\benign`

---

## 6. Required Outputs

- Fresh manifest JSONL.
- Manifest rejected JSONL.
- Manifest build summary JSON.
- Consistency report JSON/MD/summary.
- URL dedup keep/delete manifests and summary for dry-run, delete, and postcheck.
- Handoff document.

---

## 7. Hard Constraints

- Run dry-run before delete.
- Delete only URL-key duplicates reported by the existing keep-oldest dedup tool.
- Record exact counts and validation output.
- Treat weak labels as weak labels, not manual gold labels.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: No.
- Existing CLI changed: No.
- Existing output formats changed: No.

---

## 9. Acceptance Criteria

- Manifest build completes or reports rejected rows.
- Consistency checker completes and reports pass/fail.
- Dedup dry-run completes and reports duplicate count.
- Delete pass removes only confirmed URL-key duplicate directories.
- Post-dedup dry-run reports zero duplicate directories.
- Post-dedup consistency checker reports no errors or warnings.

---

## 10. Validation Checklist

- Run manifest build for primary benign.
- Run consistency checker on that manifest.
- Run URL-key dedup dry-run on primary benign.
- Verify dedup summary mode is `dry_run`.
- Run URL-key dedup delete for confirmed duplicates.
- Run post-dedup manifest build.
- Run post-dedup consistency checker.
- Run post-dedup URL-key dedup dry-run.
- Write handoff.
