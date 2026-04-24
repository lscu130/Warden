<!-- operator: Codex; task: template-noise-plan-content-and-benign; date: 2026-04-24 -->

# 中文摘要

本次按用户建议同时扫描了两个池：

- content-warning 人工复核池：`E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- primary benign 池：`E:\WardenData\raw\benign\benign`

实际结果：

- 总模板候选：653
- content-warning 池命中：630
- primary benign 池命中：23
- content-warning 建议保留代表：100
- content-warning 建议后续移到 template noise：530
- primary benign 建议保留代表：12
- primary benign 建议后续移到 template noise：11

本次没有移动任何样本。输出只是 dry-run plan，不是人工金标，也不是最终清洗结果。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_template_noise_plan_content_and_benign
- Related Task ID: 2026-04-24_template_noise_plan_content_and_benign
- Task Title: Template Noise Plan For Content-Warning And Benign Pools
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery created a dry-run template-noise plan for both the content-warning manual-review pool and the current primary benign pool. It identifies repeated template-like pages represented by the `bookiestation.com` / `bonushaven.de` family and recommends which examples to keep as representatives versus which examples can later be moved into template-noise buckets.

No samples were moved.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/plan_template_noise_candidates.py`.
- The script scans two source pools and emits a dry-run JSONL plan plus summary.
- It uses repeated text-template markers such as `Your Ultimate Guide to`, `Latest Update`, `All Posts`, `Business`, `Esports`, `Fashion`, `Featured`, `Contact Us`, `Ryan Jones`, and `Megan Ward`.

### Doc Changes

- Added task doc `docs/tasks/2026-04-24_template_noise_plan_content_and_benign.md`.
- Added this handoff.

### Output / Artifact Changes

- Wrote `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan.jsonl`.
- Wrote `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_summary.json`.

---

## 3. Files Touched

- `docs/tasks/2026-04-24_template_noise_plan_content_and_benign.md`
- `scripts/data/benign/plan_template_noise_candidates.py`
- `docs/handoff/2026-04-24_template_noise_plan_content_and_benign.md`

External artifacts written:

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan.jsonl`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_summary.json`

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can generate a dry-run plan for template-noise cleanup across content-warning and primary benign pools.
- The plan separates representative keeps from future move candidates.

### Preserved Behavior

- Raw sample directories are unchanged.
- No labels are changed.
- No existing script CLI is changed.

### User-facing / CLI Impact

New additive CLI:

```powershell
python E:\Warden\scripts\data\benign\plan_template_noise_candidates.py
```

### Output Format Impact

- Existing outputs are unchanged.
- New dry-run artifacts are additive.

---

## 5. Schema / Interface Impact

- Schema changed: No.
- Backward compatible: Yes.
- Public interface changed: No existing CLI was changed.
- Existing CLI still valid: Yes.

Compatibility notes:

The plan is an operational cleanup suggestion. It is not a manual gold label and should not be consumed as final dataset admission.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile E:\Warden\scripts\data\benign\plan_template_noise_candidates.py
python E:\Warden\scripts\data\benign\plan_template_noise_candidates.py
Get-Content -LiteralPath 'E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_summary.json' -TotalCount 220
Select-String -LiteralPath 'E:\WardenData\reviewed\benign_second_pass\2026-04-24_template_noise_content_and_benign_plan.jsonl' -Pattern 'bookiestation.com|bonushaven.de'
```

### Result

- `py_compile` passed.
- Dry-run generated 653 template candidates.
- `bookiestation.com` and `bonushaven.de` both appeared in the plan with high template scores.
- No files were moved.

Dry-run count summary:

- `content_warning_manual_review:keep_representative`: 100
- `content_warning_manual_review:move_to_template_noise`: 530
- `primary_benign:keep_representative`: 12
- `primary_benign:move_to_template_noise`: 11

### Not Run

- No apply/move command was run.
- No full screenshot review was run.
- No training/inference validation was run.

Reason:

The task was intentionally limited to dry-run planning.

---

## 7. Risks / Caveats

- Template detection is text-structure based, not visual-template hashing.
- Some real sites can share generic markers such as `Your Ultimate Guide`; this is why the plan should be reviewed before applying.
- Primary benign had only 23 hits; several are legitimate sites and should not be bulk moved without review.
- The content-warning pool has much stronger evidence of repeated generated template pages.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/tasks/2026-04-24_template_noise_plan_content_and_benign.md`
- `docs/handoff/2026-04-24_template_noise_plan_content_and_benign.md`

Doc debt still remaining:

- If this becomes a recurring cleanup step, add it to data-module operations documentation.

---

## 9. Recommended Next Step

Review the dry-run plan first. If acceptable, the next task should apply only:

- content-warning `move_to_template_noise` rows: likely safe to move after quick spot-check;
- primary benign `move_to_template_noise` rows: review first, because only 11 rows are affected and false positives matter more in the main benign pool.
