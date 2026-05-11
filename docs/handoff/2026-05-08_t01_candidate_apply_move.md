# Handoff: T01 Candidate Apply Move

## 中文版

本次已按更新后的阈值执行 T01 候选移动：

- `C02` 到 `C09` 中无 `exclude_reasons` 的样本：249 个。
- `C01_login_auth` 中 `candidate_score >= 15` 且无 `exclude_reasons` 的样本：971 个。
- 总移动数：1220 个。
- `C99_mixed_or_uncertain`：9 个，未移动。
- 符合桶/分数条件但带 `exclude_reasons` 的样本：436 个，未移动。

移动目标：

`E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`

移动前后计数：

- T00: 19369 -> 18149
- T01: 885 -> 2105
- T90: 20 -> 20

验证结论：

- 移动前源路径缺失：0。
- 移动前目标重名冲突：0。
- 移动后源路径仍存在：0。
- 移动后目标路径存在：1220。
- T01 增量：1220。
- C99 和带 `exclude_reasons` 的排除样本未进入 T01。

---

## English Version

# Handoff Metadata

- Handoff ID: `HANDOFF-20260508-T01-CANDIDATE-APPLY-MOVE`
- Related Task ID: `TASK-20260508-T01-CANDIDATE-APPLY-MOVE`
- Task Title: Apply Selected T01 Candidate Moves Into T01 Benign Hard Negative Bucket
- Module: dataset cleaning / benign pool / triage bucket maintenance
- Author: Codex
- Date: 2026-05-08
- Status: DONE
- Quota Mode: CODEX_QUOTA_CONSTRAINED
- Task Difficulty: HIGH
- Executor: CODEX
- Required Reviewer: GPT_WEB
- Codex Review Required: NO
- Codex Review Performed: NOT_APPLICABLE

## 1. Executive Summary

Applied the selected T01 candidate move using the updated owner-approved threshold: `C01_login_auth` candidates with `candidate_score >= 15`, plus C02-C09 candidates, excluding all rows with `exclude_reasons` and excluding C99.

The task reached its stop condition. 1220 sample directories were moved into `T01_benign_hard_negative`; excluded C99 and excluded-reason rows were not moved.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-05-08_t01_candidate_apply_move_task.md`.
- Added this handoff.

### Output / Artifact Changes

Generated apply artifacts under:

- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_manifest.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_c99.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_with_reasons.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_summary.json`

Moved 1220 sample directories into:

- `E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`

## 3. Files Touched

Repository files:

- `docs/tasks/2026-05-08_t01_candidate_apply_move_task.md`
- `docs/handoff/2026-05-08_t01_candidate_apply_move.md`

Data artifacts:

- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_manifest.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_c99.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\excluded_with_reasons.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_summary.json`

Data directories:

- 1220 selected sample directories moved from `T00_clear_benign` into `T01_benign_hard_negative`.

## 4. Behavior Impact

### Expected New Behavior

- The T01 triage bucket now contains the selected high-confidence candidate directories.
- The apply manifests document exactly which directories were moved and which candidates were excluded.

### Preserved Behavior

- Sample directory names were preserved.
- Sample-internal files were not edited.
- C99 rows were not moved.
- Rows with `exclude_reasons` were not moved.
- T90 count did not change.

### User-facing / CLI Impact

- Existing CLIs unchanged.
- No new CLI was added in this task.

### Output Format Impact

- Existing output formats unchanged.
- New apply CSV/JSON artifacts were added outside the repo for auditability.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This task changes triage bucket membership by moving directories only. It does not change label enums, final manifest schema, train split logic, L1/L2 outputs, or model inputs.

## 6. Validation Performed

### Commands Run

```powershell
# Latest precheck after owner changed threshold to >= 15.
$csv = Import-Csv -LiteralPath 'E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_manifest_v1.csv'
$eligiblePattern = $csv | Where-Object { ($_.candidate_bucket -match '^C0[2-9]_') -or ($_.candidate_bucket -eq 'C01_login_auth' -and [int]$_.candidate_score -ge 15) }
$move = $eligiblePattern | Where-Object { -not $_.exclude_reasons }
$excludedReasons = $eligiblePattern | Where-Object { $_.exclude_reasons }

# Apply command summary:
# PowerShell generated manifests, checked missing/collisions, then ran:
Move-Item -LiteralPath <source_path> -Destination "E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative"
```

```powershell
python scripts\ci\check_task_doc.py docs\tasks\2026-05-08_t01_candidate_apply_move_task.md
```

### Result

- Latest precheck selected 1220 move rows.
- C02-C09 without exclusions: 249.
- C01 score greater than or equal to 15 without exclusions: 971.
- C99 excluded: 9.
- Eligible-pattern rows excluded due to `exclude_reasons`: 436.
- Missing source paths before move: 0.
- Existing target collisions before move: 0.
- Moved directories: 1220.
- Post-move source paths still existing: 0.
- Post-move target paths present: 1220.
- T01 delta: 1220.
- Excluded C99 target-present count: 0.
- Excluded-with-reasons target-present count: 0.
- `check_task_doc.py`: OK.

Directory counts:

- `T00_clear_benign`: 19369 -> 18149.
- `T01_benign_hard_negative`: 885 -> 2105.
- `T90_uncertain_or_suspicious`: 20 -> 20.

Manifest counts:

- `move_manifest.csv`: 1220.
- `excluded_c99.csv`: 9.
- `excluded_with_reasons.csv`: 436.
- `check_handoff_doc.py`: OK.

### Not Run

- No train/validation/test split was generated.
- No model, OCR, YOLO, CLIP, teacher distillation, or final clean-pool manifest generation was run.
- No manual visual review of moved samples was performed during this apply step.

## 7. Risks / Caveats

- The move is based on heuristic candidate-mining scores and the owner's threshold decision; it is not a manual visual review result.
- 436 eligible-pattern rows were held back because they had `exclude_reasons`.
- The original candidate CSV still points to old `current_path` values for moved rows; use the apply manifest for the post-move target paths.
- Future split/final-manifest work should rebuild from the current triage tree, not from stale candidate `current_path` values.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-08_t01_candidate_apply_move_task.md`
- `docs/handoff/2026-05-08_t01_candidate_apply_move.md`

Doc debt still remaining:

- none for this apply step.

## 9. Recommended Next Step

- Rebuild or rerun any downstream clean-pool manifest process from the updated triage tree.
- Keep `E:\WardenData\manifests\t01_candidate_mining_v1_apply\move_manifest.csv` as the audit trail for the 1220 moved directories.
- Review the 436 `excluded_with_reasons.csv` rows separately before any further T01 movement.
