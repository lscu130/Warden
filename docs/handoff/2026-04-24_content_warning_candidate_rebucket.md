<!-- operator: Codex; task: content-warning-candidate-rebucket; date: 2026-04-24 -->

# 中文摘要

本次只处理 `content_warning_candidate != none` 的样本，没有处理其他行为风险 `exclude` 样本。

处理结果：

- 计划处理：2,432
- 实际移动：2,432
- 高置信 adult 自动移动：9
- 高置信 gambling 自动移动：167
- 高置信 adult_and_gambling 自动移动：0
- 低置信 / 需人工截图复核移动：2,256

目标目录：

- `E:\WardenData\raw\benign\hard benign\adult`
- `E:\WardenData\raw\benign\hard benign\gambling`
- `E:\WardenData\raw\benign\hard benign\adult_and_gambling`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

这次采用保守自动搬迁策略：只有 URL / 域名强命中 adult 或 gambling 的样本才自动移动；新闻站、音乐站、普通游戏站、文本弱命中、both 弱混杂样本全部放进人工复核目录。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_content_warning_candidate_rebucket
- Related Task ID: 2026-04-24_content_warning_candidate_rebucket
- Task Title: Content-Warning Candidate Rebucketing
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery handled only second-pass content-warning candidates from the primary benign pool. Non-content-warning `exclude` samples were intentionally left untouched.

The broad second-pass detector had false positives during screenshot spot checks, so this task used a stricter operational policy: automatically move only high-confidence URL/domain matches, and move all ambiguous content-warning candidates into a manual-review folder.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/rebucket_content_warning_candidates.py`.
- The script builds a dry-run move plan by default.
- The script applies moves only when `--apply` is passed.

### Doc Changes

- Added task doc `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`.
- Added this handoff.

### Output / Artifact Changes

- Wrote dry-run / applied plan: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_plan.jsonl`.
- Wrote summary: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_summary.json`.
- Wrote apply log: `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_apply_log.jsonl`.
- Moved content-warning candidates out of `E:\WardenData\raw\benign\benign`.

---

## 3. Files Touched

- `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
- `scripts/data/benign/rebucket_content_warning_candidates.py`
- `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`

External data artifacts / directories touched:

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_plan.jsonl`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_summary.json`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_apply_log.jsonl`
- `E:\WardenData\raw\benign\hard benign\adult`
- `E:\WardenData\raw\benign\hard benign\gambling`
- `E:\WardenData\raw\benign\hard benign\adult_and_gambling`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

---

## 4. Behavior Impact

### Expected New Behavior

- Content-warning candidates are no longer mixed into the primary benign source directory.
- High-confidence adult/gambling candidates are in their hard-benign content buckets.
- Ambiguous content-warning candidates are isolated for human screenshot review.

### Preserved Behavior

- No raw files inside sample directories were edited.
- Non-content-warning `exclude` rows were not moved.
- Existing scripts and schemas were not changed.

### User-facing / CLI Impact

New additive CLI:

```powershell
python E:\Warden\scripts\data\benign\rebucket_content_warning_candidates.py
python E:\Warden\scripts\data\benign\rebucket_content_warning_candidates.py --apply
```

### Output Format Impact

- Existing outputs are unchanged.
- New operational plan/log files are additive.

---

## 5. Schema / Interface Impact

- Schema changed: No.
- Backward compatible: Yes.
- Public interface changed: No existing CLI was changed.
- Existing CLI still valid: Yes.

Affected schema fields / interfaces:

- None.

Compatibility notes:

The move plan and apply log are operational artifacts. They are not manual labels and must not be treated as final dataset-admission truth.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile E:\Warden\scripts\data\benign\rebucket_content_warning_candidates.py
python E:\Warden\scripts\data\benign\rebucket_content_warning_candidates.py
python E:\Warden\scripts\data\benign\rebucket_content_warning_candidates.py --apply
Get-Content -LiteralPath 'E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_summary.json' -TotalCount 120
$log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_apply_log.jsonl'; $counts=@{}; Get-Content -LiteralPath $log | ForEach-Object { $row=$_ | ConvertFrom-Json; $s=[string]$row.status; if(-not $counts.ContainsKey($s)){$counts[$s]=0}; $counts[$s]++ }; $counts.GetEnumerator() | Sort-Object Name | ForEach-Object { "$($_.Key)`t$($_.Value)" }
$log='E:\WardenData\reviewed\benign_second_pass\2026-04-24_content_warning_rebucket_apply_log.jsonl'; $missingDst=0; $stillSrc=0; Get-Content -LiteralPath $log | ForEach-Object { $row=$_ | ConvertFrom-Json; if($row.status -eq 'moved'){ if(-not (Test-Path -LiteralPath $row.dst)){$missingDst++}; if(Test-Path -LiteralPath $row.src){$stillSrc++} } }; @{missing_destination=$missingDst; source_still_exists=$stillSrc} | ConvertTo-Json -Compress
```

### Result

- `py_compile` passed.
- Dry-run planned 2,432 content-warning candidates.
- Dry-run source check found no missing sources and no destination conflicts.
- Apply moved 2,432 directories.
- Apply status distribution: `moved = 2432`.
- Post-apply verification: `missing_destination = 0`, `source_still_exists = 0`.

Final target counts after moving, including historical existing samples:

- `E:\WardenData\raw\benign\hard benign\adult`: 895
- `E:\WardenData\raw\benign\hard benign\gambling`: 1195
- `E:\WardenData\raw\benign\hard benign\adult_and_gambling`: 0
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`: 2256

### Not Run

- No exhaustive manual screenshot review was performed.
- No training or inference run was performed.
- No non-content-warning exclusion cleanup was performed.

Reason:

The task scope was limited to moving high-confidence content-warning samples and isolating ambiguous content-warning samples for the user's manual reviewer.

---

## 7. Risks / Caveats

- Automatic movement is intentionally conservative. Some true adult/gambling samples may be in manual review.
- `adult_and_gambling` received no high-confidence automatic moves because none matched both strict adult and strict gambling URL/domain patterns.
- Manual-review samples include known false positives such as normal music, ordinary games, and news sites.
- Moved buckets are operational content buckets, not manual gold labels.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
- `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`

Doc debt still remaining:

- If this rebucket script becomes a recurring operator workflow, add it to the data-module operations docs.

---

## 9. Recommended Next Step

Open `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424` with `dataset_reviewed_switchable_targets.py` and manually move confirmed samples into:

- `E:\WardenData\raw\benign\hard benign\adult`
- `E:\WardenData\raw\benign\hard benign\gambling`
- `E:\WardenData\raw\benign\hard benign\adult_and_gambling`

Keep false positives out of hard-benign content buckets.
