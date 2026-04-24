<!-- operator: Codex; task: rebucket-content-warning-back-to-benign; date: 2026-04-24 -->

# 中文摘要

本任务按用户要求执行目录回迁和层级调整：

- 将 `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424` 中剩余样本移回 `E:\WardenData\raw\benign\benign`。
- 将 `E:\WardenData\raw\benign\hard benign\adult` 提升为 `E:\WardenData\raw\benign\adult`。
- 将 `E:\WardenData\raw\benign\hard benign\gambling` 提升为 `E:\WardenData\raw\benign\gambling`。

本任务不改样本内部文件，不改 labels，不改 schema。

---

# English Version

# Task Metadata

- Task ID: 2026-04-24_rebucket_content_warning_back_to_benign
- Task Title: Rebucket Content-Warning Review Back To Benign And Promote Adult/Gambling
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data
- Related Issue / ADR / Doc:
  - `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
  - `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`
- Created At: 2026-04-24
- Requested By: User

---

## 1. Background

The user requested that the remaining content-warning manual-review samples be moved back into the main benign folder, and that adult/gambling buckets be promoted from under `hard benign` to the top-level `raw\benign` layer.

---

## 2. Goal

Perform the requested directory rebucketing without modifying sample internals, labels, schemas, or existing scripts.

---

## 3. Scope In

Allowed source directories:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\hard benign\adult`
- `E:\WardenData\raw\benign\hard benign\gambling`

Allowed destination directories:

- `E:\WardenData\raw\benign\benign`
- `E:\WardenData\raw\benign\adult`
- `E:\WardenData\raw\benign\gambling`

Allowed repo files:

- this task doc
- matching handoff doc

---

## 4. Scope Out

- Do not modify raw sample files.
- Do not modify `manual_labels.json`.
- Do not move template-noise buckets.
- Do not move primary benign template-noise dry-run candidates.
- Do not change schema, CLI, training, inference, or capture logic.

---

## 5. Inputs

- User request in current thread.
- Existing WardenData directory structure.

---

## 6. Required Outputs

- Move log under `E:\WardenData\reviewed\benign_second_pass`.
- Handoff document.

---

## 7. Hard Constraints

- Verify source and target conflicts before moving.
- Use path-literal PowerShell moves.
- Record exact moved/skipped counts.
- Preserve sample directory contents.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: No.
- Existing CLI changed: No.
- Existing output formats changed: No.

---

## 9. Acceptance Criteria

- Remaining content-warning manual-review sample directories are moved back to `raw\benign\benign`.
- Adult and gambling directories are promoted to top-level `raw\benign`.
- Move log records statuses.
- Post-move checks show expected target paths and counts.

---

## 10. Validation Checklist

- Precheck source counts and destination conflicts.
- Apply move.
- Verify source residue and destination counts.
- Write handoff.
