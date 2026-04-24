<!-- operator: Codex; task: template-noise-content-warning-v3-apply; date: 2026-04-24 -->

# 中文摘要

本次按用户确认，执行 v3 plan 中所有剩余 `content_warning_manual_review` 模板候选移动。

实际移动：

- 计划移动：117
- 成功移动：117
- 缺失源目录：0
- 目标冲突：0
- 移动后源目录仍存在：0
- 移动后目标缺失：0

目标目录：

- `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`

未处理：

- `content_warning_manual_review_removed` 只作为 reference，未移动。
- `primary_benign` 未移动。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_template_noise_content_warning_v3_apply
- Related Task ID: 2026-04-24_template_noise_plan_content_and_benign
- Task Title: Apply Remaining Content-Warning Template-Noise V3 Candidates
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery applied the user's confirmation to move all remaining `content_warning_manual_review` template candidates from the v3 plan. It moved 117 sample directories into the existing content-warning template-noise bucket.

No `removed` reference samples and no `primary_benign` samples were moved.

---

## 2. What Changed

### Code Changes

- None.

### Doc Changes

- Added this handoff.

### Output / Artifact Changes

- Wrote apply log: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_v3_apply_log.jsonl`.
- Moved 117 sample directories to `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`.

---

## 3. Files Touched

- `docs/handoff/2026-04-24_template_noise_content_warning_v3_apply.md`

External data artifacts / directories touched:

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_v3_apply_log.jsonl`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`

---

## 4. Behavior Impact

### Expected New Behavior

- The content-warning manual-review folder has fewer repeated template pages.
- The content-warning template-noise bucket now contains the prior 530 moved samples plus these 117 newly moved samples.

### Preserved Behavior

- No raw files inside sample directories were edited.
- No primary benign samples were moved.
- The `removed` folder under content-warning manual review was not modified.
- No manual labels were changed.

### User-facing / CLI Impact

- None.

### Output Format Impact

- Existing outputs are unchanged.
- Apply log is additive.

---

## 5. Schema / Interface Impact

- Schema changed: No.
- Backward compatible: Yes.
- Public interface changed: No.
- Existing CLI still valid: Yes.

Compatibility notes:

The target bucket means repeated template noise, not malicious, adult, gambling, or manual gold.

---

## 6. Validation Performed

### Commands Run

```powershell
$plan='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan_v3.jsonl'; $target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; $count=0; $missing=0; $destExists=0; Get-Content -LiteralPath $plan | ForEach-Object { if($_.Trim()){ $row=$_ | ConvertFrom-Json; if($row.source_pool -eq 'content_warning_manual_review'){ $count++; $src=Join-Path 'E:\WardenData' $row.sample_dir; $dst=Join-Path $target $row.sample_id; if(-not (Test-Path -LiteralPath $src)){$missing++}; if(Test-Path -LiteralPath $dst){$destExists++} } } }; @{planned=$count; missing_source=$missing; destination_exists=$destExists} | ConvertTo-Json -Compress
$plan='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan_v3.jsonl'; $target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; $log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_v3_apply_log.jsonl'; New-Item -ItemType Directory -Force -Path $target | Out-Null; if(Test-Path -LiteralPath $log){ Remove-Item -LiteralPath $log -Force }; Get-Content -LiteralPath $plan | ForEach-Object { if($_.Trim()){ $row=$_ | ConvertFrom-Json; if($row.source_pool -eq 'content_warning_manual_review'){ $src=Join-Path 'E:\WardenData' $row.sample_dir; $dst=Join-Path $target $row.sample_id; $status=''; if(-not (Test-Path -LiteralPath $src)){ $status='missing_source' } elseif(Test-Path -LiteralPath $dst){ $status='destination_exists' } else { Move-Item -LiteralPath $src -Destination $dst; $status='moved' }; [pscustomobject]@{sample_id=$row.sample_id; source_pool=$row.source_pool; suggested_action=$row.suggested_action; src=$src; dst=$dst; status=$status; template_score=$row.template_score; first_line=$row.first_line} | ConvertTo-Json -Compress } } } | Set-Content -LiteralPath $log -Encoding UTF8; Get-Content -LiteralPath $log | ForEach-Object { ($_ | ConvertFrom-Json).status } | Group-Object | Sort-Object Name | ForEach-Object { "$($_.Name)`t$($_.Count)" }
$target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; (Get-ChildItem -LiteralPath $target -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
$log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_v3_apply_log.jsonl'; $missingDst=0; $stillSrc=0; $rows=0; Get-Content -LiteralPath $log | ForEach-Object { if($_.Trim()){ $row=$_ | ConvertFrom-Json; $rows++; if($row.status -eq 'moved'){ if(-not (Test-Path -LiteralPath $row.dst)){$missingDst++}; if(Test-Path -LiteralPath $row.src){$stillSrc++} } } }; @{rows=$rows; missing_destination=$missingDst; source_still_exists=$stillSrc} | ConvertTo-Json -Compress
```

### Result

- Precheck: `planned = 117`, `missing_source = 0`, `destination_exists = 0`.
- Apply result: `moved = 117`.
- Target directory count after move: `647`.
- Post-apply verification: `rows = 117`, `missing_destination = 0`, `source_still_exists = 0`.
- Remaining content-warning manual-review directory count: `1549`.

### Not Run

- No primary benign move was applied.
- No `removed` reference move was applied.
- No training/inference validation was run.

Reason:

The user explicitly requested moving the newly found content-warning template samples.

---

## 7. Risks / Caveats

- This move is based on text-template signals plus user-confirmed pattern examples, not image hashing.
- The template-noise bucket is an operational cleanup bucket.
- Apply log can be used to audit or reverse individual moves manually if needed.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/handoff/2026-04-24_template_noise_content_warning_v3_apply.md`

Doc debt still remaining:

- None for this one-off apply step.

---

## 9. Recommended Next Step

Continue manual review in:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

The folder now contains 1,549 top-level sample directories after this template-noise cleanup pass.
