<!-- operator: Codex; task: rebucket-content-warning-back-to-benign; date: 2026-04-24 -->

# 中文摘要

本次按用户要求完成两类目录调整：

- 将 `content_warning_manual_review_20260424` 中剩余 1421 个样本移回 `E:\WardenData\raw\benign\benign`。
- 将 `hard benign\adult` 和 `hard benign\gambling` 提升到 `E:\WardenData\raw\benign` 顶层。

最终结果：

- `E:\WardenData\raw\benign\benign`: 19338
- `E:\WardenData\raw\benign\adult`: 917
- `E:\WardenData\raw\benign\gambling`: 1305
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`: 0
- `E:\WardenData\raw\benign\hard benign\adult`: 不存在
- `E:\WardenData\raw\benign\hard benign\gambling`: 不存在

本次没有修改样本内部文件，没有改 labels，没有改 schema。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_rebucket_content_warning_back_to_benign
- Related Task ID: 2026-04-24_rebucket_content_warning_back_to_benign
- Task Title: Rebucket Content-Warning Review Back To Benign And Promote Adult/Gambling
- Module: Data
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery moved the remaining content-warning manual-review samples back into the main benign directory and promoted the adult/gambling content buckets from `hard benign` to the top-level `raw\benign` layer.

No sample internals, labels, schemas, scripts, training logic, or inference logic were changed.

---

## 2. What Changed

### Code Changes

- None.

### Doc Changes

- Added task doc `docs/tasks/2026-04-24_rebucket_content_warning_back_to_benign.md`.
- Added this handoff.

### Output / Artifact Changes

- Wrote move log: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_rebucket_content_warning_back_to_benign_apply_log.jsonl`.
- Wrote promote log: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_promote_adult_gambling_apply_log.jsonl`.
- Moved 1421 sample directories back to `E:\WardenData\raw\benign\benign`.
- Moved `adult` and `gambling` directories to the top-level `E:\WardenData\raw\benign` layer.

---

## 3. Files Touched

- `docs/tasks/2026-04-24_rebucket_content_warning_back_to_benign.md`
- `docs/handoff/2026-04-24_rebucket_content_warning_back_to_benign.md`

External data artifacts / directories touched:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\benign`
- `E:\WardenData\raw\benign\adult`
- `E:\WardenData\raw\benign\gambling`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_rebucket_content_warning_back_to_benign_apply_log.jsonl`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_promote_adult_gambling_apply_log.jsonl`

---

## 4. Behavior Impact

### Expected New Behavior

- Adult and gambling content buckets now live directly under `E:\WardenData\raw\benign`.
- Remaining content-warning manual-review samples are back in the main benign folder.

### Preserved Behavior

- Sample directory contents were preserved.
- No labels were edited.
- No schema or CLI was changed.

### User-facing / CLI Impact

- None.

### Output Format Impact

- Existing output formats are unchanged.
- Move logs are additive.

---

## 5. Schema / Interface Impact

- Schema changed: No.
- Backward compatible: Yes for schemas and CLIs.
- Public interface changed: No.
- Existing CLI still valid: Yes.

Compatibility notes:

Downstream scripts that assumed adult/gambling lived under `hard benign` should now use the top-level paths:

- `E:\WardenData\raw\benign\adult`
- `E:\WardenData\raw\benign\gambling`

---

## 6. Validation Performed

### Commands Run

```powershell
foreach($p in @('E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424','E:\WardenData\raw\benign\benign','E:\WardenData\raw\benign\hard benign\adult','E:\WardenData\raw\benign\hard benign\gambling','E:\WardenData\raw\benign\adult','E:\WardenData\raw\benign\gambling')){ $exists=Test-Path -LiteralPath $p; $count='NA'; if($exists){ $count=(Get-ChildItem -LiteralPath $p -Directory -ErrorAction SilentlyContinue | Measure-Object).Count }; "$p`t$exists`t$count" }
$src='E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424'; $dst='E:\WardenData\raw\benign\benign'; $count=0; $conflict=0; if(Test-Path -LiteralPath $src){ Get-ChildItem -LiteralPath $src -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne 'removed' } | ForEach-Object { $count++; if(Test-Path -LiteralPath (Join-Path $dst $_.Name)){ $conflict++ } } }; @{planned_move_back=$count; destination_conflicts=$conflict} | ConvertTo-Json -Compress
```

Move and promote commands were run with `Move-Item -LiteralPath` and wrote JSONL logs.

### Result

- Precheck: `planned_move_back = 1421`, `destination_conflicts = 0`.
- Content-warning move-back result: `moved = 1421`.
- Content-warning move-back postcheck: `rows = 1421`, `missing_destination = 0`, `source_still_exists = 0`.
- Adult promote result: `moved`.
- Gambling promote result: `moved`.
- Final counts:
  - `E:\WardenData\raw\benign\benign`: 19338
  - `E:\WardenData\raw\benign\adult`: 917
  - `E:\WardenData\raw\benign\gambling`: 1305
  - `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`: 0

### Not Run

- No training run.
- No inference run.
- No data consistency script rerun.

Reason:

The task was a directory rebucketing operation only.

---

## 7. Risks / Caveats

- Any downstream command that still points to `hard benign\adult` or `hard benign\gambling` must be updated by the operator or a follow-up doc/script cleanup task.
- The top-level `hard benign` directory still exists, but no longer contains `adult` or `gambling`.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/tasks/2026-04-24_rebucket_content_warning_back_to_benign.md`
- `docs/handoff/2026-04-24_rebucket_content_warning_back_to_benign.md`

Doc debt still remaining:

- If adult/gambling top-level paths are now a durable contract, update data-module docs and any operator instructions that still mention `hard benign\adult` or `hard benign\gambling`.

---

## 9. Recommended Next Step

Run a quick search for stale `hard benign\adult` / `hard benign\gambling` path references in docs or scripts before the next batch operation.
