# TASK: T01 Candidate Apply Move

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分供人工快速阅读与执行确认。

### 任务摘要

本任务把上一轮 T01 hard-negative candidate mining 输出中的一部分样本目录，从当前 Tranco benign triage 桶移动到：

`E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`

移动范围已经冻结：

- 移动 `C02` 到 `C09` 中无 `exclude_reasons` 的样本。
- 移动 `C01_login_auth` 中 `candidate_score >= 15` 且无 `exclude_reasons` 的样本。
- 不移动 `C99_mixed_or_uncertain`。
- 不移动任何带 `exclude_reasons` 的样本。

本任务只移动整个 sample directory，不编辑样本内部文件，不生成 split，不跑模型，不改 schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: `TASK-20260508-T01-CANDIDATE-APPLY-MOVE`
- Task Title: Apply Selected T01 Candidate Moves Into T01 Benign Hard Negative Bucket
- Owner Role: Codex
- Quota Mode: CODEX_QUOTA_CONSTRAINED
- Task Difficulty: HIGH
- Target Executor: CODEX
- Required Reviewer: GPT_WEB
- Human Manual Required: NO
- Codex Review Required: NO
- Priority: High
- Status: TODO
- Related Module: dataset cleaning / benign pool / triage bucket maintenance
- Related Issue / ADR / Doc: `docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md`
- Created At: 2026-05-08
- Requested By: project owner

## 1. Background

The previous T01 candidate-mining task generated a review queue under:

`E:\WardenData\manifests\t01_candidate_mining_v1`

The owner approved a bounded apply move from the review queue into the existing T01 hard-negative triage bucket, with suspicious/exclusion rows held back.

## 2. Goal

Move only the selected candidate sample directories into `T01_benign_hard_negative`, while producing apply manifests and validation evidence.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-05-08_t01_candidate_apply_move_task.md`
- `docs/handoff/2026-05-08_t01_candidate_apply_move.md`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\`
- selected source sample directories listed in the generated `move_manifest.csv`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative\`

This task is allowed to change:

- Move selected sample directories from their current triage bucket into `T01_benign_hard_negative`.
- Write apply manifests and summary files under `t01_candidate_mining_v1_apply`.

## 4. Scope Out

This task must NOT do the following:

- Do not move `C99_mixed_or_uncertain`.
- Do not move candidates with non-empty `exclude_reasons`.
- Do not edit sample-internal files.
- Do not delete sample directories.
- Do not rename sample directories.
- Do not modify schema, label enums, L1/L2 outputs, or final manifest schema.
- Do not generate train/validation/test splits.
- Do not run models, OCR, YOLO, CLIP, teacher distillation, or external web lookup.

## 5. Inputs

Relevant inputs:

- Candidate CSV: `E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_manifest_v1.csv`
- Triage root: `E:\WardenData\manifests\tranco_benign_triage_v1`
- Target T01 bucket: `E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`

Selection rule:

- Include if `candidate_bucket` matches `C02_` through `C09_` and `exclude_reasons` is empty.
- Include if `candidate_bucket == C01_login_auth`, `candidate_score >= 15`, and `exclude_reasons` is empty.
- Exclude if `candidate_bucket == C99_mixed_or_uncertain`.
- Exclude if `exclude_reasons` is non-empty.

Current precheck:

- Move rows: 1220.
- C02-C09 without exclusions: 249.
- C01 score greater than or equal to 15 without exclusions: 971.
- C99 excluded: 9.
- Eligible-pattern rows excluded due to `exclude_reasons`: 436.
- Missing source paths: 0.
- Existing target collisions: 0.

## 6. Required Outputs

This task should produce:

- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_manifest.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_c99.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_with_reasons.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_summary.json`
- `docs/handoff/2026-05-08_t01_candidate_apply_move.md`

## 7. Hard Constraints

- Move exactly the selected rows if the latest precheck still reports 1220 rows, 0 missing sources, and 0 target collisions.
- Stop without moving if source paths are missing or target collisions are detected.
- Preserve sample directory names.
- Do not edit sample-internal files.
- Do not move C99 or rows with `exclude_reasons`.
- Human final acceptance remains required.

## 8. Interface / Schema Constraints

- Schema changed allowed: NO.
- Label enum changed allowed: NO.
- Existing CLI changed: NO.
- Public output schema changed: NO.
- This task changes triage bucket membership only by moving selected sample directories.

## 9. Execution Notes

Recommended execution:

1. Generate apply manifests from the candidate CSV.
2. Record pre-move T00/T01/T90 directory counts.
3. Recheck missing sources and target collisions.
4. Move selected directories with `Move-Item -LiteralPath`.
5. Record post-move counts and path validation.
6. Write handoff with exact counts and validation output.

## 10. Acceptance Criteria

This task is complete only if:

- [ ] `move_manifest.csv` contains exactly 1220 rows.
- [ ] `excluded_c99.csv` contains exactly 9 rows.
- [ ] `excluded_with_reasons.csv` contains exactly 436 rows.
- [ ] Pre-move missing source count is 0.
- [ ] Pre-move target collision count is 0.
- [ ] All selected source directories are moved to `T01_benign_hard_negative`.
- [ ] Post-move source-missing count for moved rows is 1220.
- [ ] Post-move target-present count for moved rows is 1220.
- [ ] T01 directory count increases by 1220.
- [ ] C99 and excluded rows are not moved.
- [ ] No schema, labels, sample-internal files, split files, or model artifacts are changed.

## 11. Validation Checklist

Minimum validation:

- [ ] Verify latest candidate selection counts before move.
- [ ] Verify source path existence before move.
- [ ] Verify target collision count before move.
- [ ] Verify T00/T01/T90 directory counts before and after move.
- [ ] Verify all moved target paths exist after move.
- [ ] Verify all moved source paths no longer exist after move.
- [ ] Run task-doc checker.
- [ ] Run handoff-doc checker.

Commands:

```powershell
python scripts\ci\check_task_doc.py docs\tasks\2026-05-08_t01_candidate_apply_move_task.md
python scripts\ci\check_handoff_doc.py docs\handoff\2026-05-08_t01_candidate_apply_move.md
```

## 12. Stop Rules

Stop as done when all acceptance criteria are met and handoff is written.

Stop blocked if:

- selected row count differs from 1220 before move;
- any source path is missing before move;
- any target path collision exists before move;
- move command fails before all rows are moved;
- post-move validation does not match expected counts.
