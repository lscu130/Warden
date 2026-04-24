<!-- operator: Codex; task: primary-benign-second-pass-review-manifest; date: 2026-04-24 -->

# 中文摘要

本次交付已完成 `primary benign candidates` 二筛 review manifest 的可执行入口和全量输出。

实际完成内容：

- 新增只读二筛脚本：`scripts/data/benign/build_primary_benign_second_pass_review.py`
- 新增执行任务单：`docs/tasks/2026-04-24_primary_benign_second_pass_review_manifest.md`
- 生成全量 review manifest：`E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_review_manifest.jsonl`
- 生成 summary：`E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_summary.json`

全量结果覆盖 `E:\WardenData\raw\benign\benign` 下 20,347 个可识别样本目录。输出是 routing / review suggestion，不是人工金标，也不是最终 dataset admission。

关键分布：

- `train_main`: 598
- `eval_main`: 8
- `aux_only`: 2,024
- `exclude`: 17,568
- `uncertain`: 149
- `needs_manual_review`: 17,756
- `requires_screenshot_review`: 9,020
- content warning candidates: `adult` 675, `gambling` 1,586, `adult_and_gambling` 171

注意：该二筛策略偏高召回。大量样本因表单强证据、gate/evasion 表面、login/payment/download 混杂信号进入复核或排除建议。后续进入训练前仍需要人工或更窄规则复核，不能直接把 `exclude` 当最终恶意标签。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-24_primary_benign_second_pass_review_manifest
- Related Task ID: 2026-04-24_primary_benign_second_pass_review_manifest
- Task Title: Primary Benign Second-Pass Review Manifest
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

---

## 1. Executive Summary

This delivery added a bounded, read-only second-pass manifest builder for remaining primary benign candidates and generated a full review manifest for `E:\WardenData\raw\benign\benign`.

The output records are routing and review suggestions only. They are not manual gold labels and are not final dataset-admission decisions.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/build_primary_benign_second_pass_review.py`.
- The script reads priority artifacts in the approved order: `url.json`, `auto_labels.json`, optional `rule_labels.json`, `forms.json`, `net_summary.json`, `visible_text.txt`, and screenshot presence.
- The script emits per-sample `dataset_routing_suggestion`, `needs_manual_review`, `requires_screenshot_review`, `content_warning_candidate`, `reason_codes`, and key evidence.

### Doc Changes

- Added and completed the execution task doc.
- Added this handoff.

### Output / Artifact Changes

- Generated `E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_review_manifest.jsonl`.
- Generated `E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_summary.json`.
- Kept earlier limit-200 smoke outputs in the same output directory for traceability.

---

## 3. Files Touched

- `docs/tasks/2026-04-24_primary_benign_second_pass_review_manifest.md`
- `scripts/data/benign/build_primary_benign_second_pass_review.py`
- `docs/handoff/2026-04-24_primary_benign_second_pass_review_manifest.md`

External artifacts written:

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_review_manifest.jsonl`
- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_summary.json`

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can run an additive second-pass scan over primary benign candidate roots.
- The script separates high-risk content candidates, high-risk behavior surfaces, auxiliary gate/evasion candidates, screenshot-required cases, and low-risk benign candidates.
- The generated manifest gives a train-main prefilter and a manual-review queue without modifying raw samples.

### Preserved Behavior

- Existing manifest, consistency, capture, labeling, training, and inference scripts are unchanged.
- Raw sample directories are unchanged.
- Existing TrainSet V1 schema is unchanged.

### User-facing / CLI Impact

- New additive CLI:

```powershell
python E:\Warden\scripts\data\benign\build_primary_benign_second_pass_review.py
```

### Output Format Impact

- Existing output formats are unchanged.
- New additive review output uses `schema_version = primary_benign_second_pass_review_v1`.
- New additive summary output uses `schema_version = primary_benign_second_pass_summary_v1`.

---

## 5. Schema / Interface Impact

- Schema changed: No for existing project schemas.
- Backward compatible: Yes.
- Public interface changed: No existing CLI was changed.
- Existing CLI still valid: Yes.

Affected schema fields / interfaces:

- New additive review artifact fields only.

Compatibility notes:

The new manifest should be treated as an intermediate review artifact. It must not be consumed as `manual_labels.json`, final malicious labels, or final TrainSet V1 admission without a downstream acceptance step.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile E:\Warden\scripts\data\benign\build_primary_benign_second_pass_review.py
python E:\Warden\scripts\data\benign\build_primary_benign_second_pass_review.py --limit 200 --manifest-name 2026-04-24_primary_benign_second_pass_review_manifest_limit200_v3.jsonl --summary-name 2026-04-24_primary_benign_second_pass_summary_limit200_v3.json
python E:\Warden\scripts\data\benign\build_primary_benign_second_pass_review.py --manifest-name 2026-04-24_primary_benign_second_pass_review_manifest.jsonl --summary-name 2026-04-24_primary_benign_second_pass_summary.json
$path='E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_review_manifest.jsonl'; $n=0; $bad=0; $missing=0; Get-Content -LiteralPath $path | ForEach-Object { if($_.Trim()){ $row = $_ | ConvertFrom-Json; $n++; if($row.schema_version -ne 'primary_benign_second_pass_review_v1'){ $bad++ }; foreach($k in @('sample_id','dataset_routing_suggestion','needs_manual_review','content_warning_candidate','reason_codes','weak_label_warning')){ if(-not ($row.PSObject.Properties.Name -contains $k)){ $missing++; break } } } }; @{rows=$n; bad_schema_rows=$bad; rows_missing_required_keys=$missing} | ConvertTo-Json -Compress
Get-ChildItem -LiteralPath 'E:\WardenData\raw\benign\benign' -Directory -ErrorAction SilentlyContinue | Where-Object { -not (Test-Path -LiteralPath (Join-Path $_.FullName 'meta.json')) -or -not (Test-Path -LiteralPath (Join-Path $_.FullName 'url.json')) } | Select-Object FullName
```

### Result

- `py_compile` passed.
- Limit-200 smoke generation passed.
- Full generation passed with 20,347 manifest rows.
- JSONL parse check passed: `bad_schema_rows = 0`, `rows_missing_required_keys = 0`.
- Two top-level directories under `raw\benign\benign` were not sample directories because they lacked `meta.json` or `url.json`.

### Not Run

- No destructive deduplication.
- No raw sample move/delete.
- No manual screenshot adjudication.
- No training pipeline run.

Reason:

These actions are outside this task boundary. The task only creates review suggestions and a pre-training cleanup manifest.

---

## 7. Risks / Caveats

- The rule set is intentionally recall-heavy. It may over-route benign login/payment/download pages into review.
- `exclude` means "do not use as primary benign without further review"; it does not mean final malicious.
- `adult` / `gambling` are high-risk content candidates, not true malicious behavior labels.
- `gate` / `evasion` are auxiliary-route suggestions.
- CC reviewed the script and policy, but its sample-directory inspection was blocked by its permission mode. Codex performed local sample/output validation.

---

## 8. Docs Impact

- Docs updated: Yes.

Docs touched:

- `docs/tasks/2026-04-24_primary_benign_second_pass_review_manifest.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_review_manifest.md`

Doc debt still remaining:

- If this script becomes a stable operator entrypoint, add it to the relevant data-module operations documentation.

---

## 9. Recommended Next Step

Review the generated manifest by bucket. Start with:

- `dataset_routing_suggestion = train_main` for quick admission sampling.
- `dataset_routing_suggestion = uncertain` for manual boundary calibration.
- `content_warning_candidate != none` to confirm adult/gambling separation.
- `reason_codes` containing `mixed_surface:web3`, `mixed_surface:download`, `mixed_surface:login_or_credential`, or `mixed_surface:payment` for the hard mixed cases requested by the user.
