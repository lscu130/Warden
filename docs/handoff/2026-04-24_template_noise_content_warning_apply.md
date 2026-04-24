<!-- operator: Codex; task: template-noise-content-warning-apply; date: 2026-04-24 -->

# 中文摘要

本次只执行 dry-run plan 中的：

- `source_pool = content_warning_manual_review`
- `suggested_action = move_to_template_noise`

实际移动：

- 计划移动：530
- 成功移动：530
- 缺失源目录：0
- 目标冲突：0
- 移动后源目录仍存在：0
- 移动后目标缺失：0

目标目录：

- `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`

未处理：

- primary benign 中的 11 条 `move_to_template_noise` 建议未移动。
- content-warning 中的 100 条 `keep_representative` 未移动。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_template_noise_content_warning_apply
- Related Task ID: 2026-04-24_template_noise_plan_content_and_benign
- Task Title: Apply Content-Warning Template-Noise Moves
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery applied only the content-warning template-noise subset from the prior dry-run plan. It moved 530 repeated template-like samples from the content-warning manual-review folder into a dedicated template-noise bucket.

No primary benign samples were moved.

---

## 2. What Changed

### Code Changes

- None.

### Doc Changes

- Added this handoff.

### Output / Artifact Changes

- Wrote apply log: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_apply_log.jsonl`.
- Created/used target directory: `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`.
- Moved 530 sample directories into the target directory.

---

## 3. Files Touched

- `docs/handoff/2026-04-24_template_noise_content_warning_apply.md`

External data artifacts / directories touched:

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_apply_log.jsonl`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424`

---

## 4. Behavior Impact

### Expected New Behavior

- The content-warning manual-review folder now excludes 530 repeated template-like samples.
- The moved samples are isolated in a dedicated template-noise bucket.

### Preserved Behavior

- No raw files inside sample directories were edited.
- No primary benign samples were moved.
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

The template-noise bucket is an operational cleanup bucket. It is not a manual gold label and should not be treated as a malicious or content-warning class.

---

## 6. Validation Performed

### Commands Run

```powershell
$plan='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan.jsonl'; $count=0; $missing=0; $destExists=0; $target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; Get-Content -LiteralPath $plan | ForEach-Object { $row=$_ | ConvertFrom-Json; if($row.source_pool -eq 'content_warning_manual_review' -and $row.suggested_action -eq 'move_to_template_noise'){ $count++; $src=Join-Path 'E:\WardenData' $row.sample_dir; $dst=Join-Path $target $row.sample_id; if(-not (Test-Path -LiteralPath $src)){$missing++}; if(Test-Path -LiteralPath $dst){$destExists++} } }; @{planned=$count; missing_source=$missing; destination_exists=$destExists} | ConvertTo-Json -Compress
$plan='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan.jsonl'; $target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; $log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_apply_log.jsonl'; New-Item -ItemType Directory -Force -Path $target | Out-Null; if(Test-Path -LiteralPath $log){ Remove-Item -LiteralPath $log -Force }; Get-Content -LiteralPath $plan | ForEach-Object { $row=$_ | ConvertFrom-Json; if($row.source_pool -eq 'content_warning_manual_review' -and $row.suggested_action -eq 'move_to_template_noise'){ $src=Join-Path 'E:\WardenData' $row.sample_dir; $dst=Join-Path $target $row.sample_id; $status=''; if(-not (Test-Path -LiteralPath $src)){ $status='missing_source' } elseif(Test-Path -LiteralPath $dst){ $status='destination_exists' } else { Move-Item -LiteralPath $src -Destination $dst; $status='moved' }; [pscustomobject]@{sample_id=$row.sample_id; source_pool=$row.source_pool; suggested_action=$row.suggested_action; src=$src; dst=$dst; status=$status; template_score=$row.template_score; first_line=$row.first_line} | ConvertTo-Json -Compress } } | Set-Content -LiteralPath $log -Encoding UTF8; Get-Content -LiteralPath $log | ForEach-Object { ($_ | ConvertFrom-Json).status } | Group-Object | Sort-Object Name | ForEach-Object { "$($_.Name)`t$($_.Count)" }
$target='E:\WardenData\raw\benign\hard benign\template_noise_content_warning_20260424'; (Get-ChildItem -LiteralPath $target -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
$log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_warning_apply_log.jsonl'; $missingDst=0; $stillSrc=0; $rows=0; Get-Content -LiteralPath $log | ForEach-Object { if($_.Trim()){ $row=$_ | ConvertFrom-Json; $rows++; if($row.status -eq 'moved'){ if(-not (Test-Path -LiteralPath $row.dst)){$missingDst++}; if(Test-Path -LiteralPath $row.src){$stillSrc++} } } }; @{rows=$rows; missing_destination=$missingDst; source_still_exists=$stillSrc} | ConvertTo-Json -Compress
```

### Result

- Precheck: `planned = 530`, `missing_source = 0`, `destination_exists = 0`.
- Apply result: `moved = 530`.
- Target directory count after move: `530`.
- Post-apply verification: `rows = 530`, `missing_destination = 0`, `source_still_exists = 0`.
- Remaining content-warning manual-review directory count: `1704`.

### Not Run

- No primary benign move was applied.
- No screenshot/manual adjudication was performed.
- No training/inference validation was run.

Reason:

The user explicitly requested applying only the content-warning `move_to_template_noise` subset.

---

## 7. Risks / Caveats

- The move is based on the previously generated text-template dry-run plan, not visual hashing.
- The bucket means repeated template noise, not malicious, adult, gambling, or manual gold.
- If needed, moved samples can be audited using the apply log.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/handoff/2026-04-24_template_noise_content_warning_apply.md`

Doc debt still remaining:

- If template-noise cleanup becomes recurring, add a stable operations doc.

---

## 9. Recommended Next Step

Continue manual review in:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

The folder now contains 1,704 samples after template-noise removal.
