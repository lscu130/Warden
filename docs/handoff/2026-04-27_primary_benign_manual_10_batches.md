<!-- operator: Codex; task: primary-benign-manual-10-batches; date: 2026-04-27 -->

# 中文摘要

已把当前 primary benign 主目录中的 `20171` 个直接样本目录移动到 10 个人工分类批次：

- 批次根目录：`E:\WardenData\raw\benign\benign\manual_batches_20260427`
- `batch_01`：`2018` 个样本
- `batch_02` 到 `batch_10`：每批 `2017` 个样本

本次只移动样本目录，不修改样本内部文件，不改 labels，不改 schema，不做分类判断。

验证结果：

- split dry-run：`20171` planned，`0` failures
- split apply：`20171` moved，`0` failures
- post-split manifest：`20088` valid records，`83` rejected，rejected 原因均为 `missing_required_files`
- post-split consistency：`errors=0`，`warnings=0`

注意：所有 `20171` 个样本都有 `screenshot_viewport.png`，但只有 `18748` 个有 `screenshot_full.png`。当前人工分类工具若只读 `screenshot_full.png` 或 `screenshot_view.png`，会漏掉 `1423` 个只有 viewport 截图的样本。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-27_primary_benign_manual_10_batches
- Related Task ID: 2026-04-27_primary_benign_manual_10_batches
- Task Title: Primary Benign Manual 10 Batches
- Module: Data
- Author: Codex
- Date: 2026-04-27
- Status: DONE

---

## 1. Executive Summary

The current primary benign direct sample directories were split into 10 count-balanced manual-review batches under:

- `E:\WardenData\raw\benign\benign\manual_batches_20260427`

This was done by moving direct child sample directories only. A direct sample directory was defined as a directory containing both `meta.json` and `url.json`.

No label, schema, taxonomy, CLI, or sample-internal file changes were made.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/split_primary_benign_manual_batches.py`.
- The script supports dry-run by default and apply mode via `--apply`.
- The script writes JSONL plans and JSON summaries.

### Doc Changes

- Added task document: `docs/tasks/2026-04-27_primary_benign_manual_10_batches.md`.
- Added this handoff document.

### Output / Artifact Changes

- Created batch root: `E:\WardenData\raw\benign\benign\manual_batches_20260427`.
- Moved `20171` direct sample directories into `batch_01` through `batch_10`.
- Wrote dry-run and apply artifacts under `E:\WardenData\reviewed\benign_manual_batches_20260427`.
- Wrote post-split manifest and consistency outputs under `E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck`.

---

## 3. Files Touched

- `scripts/data/benign/split_primary_benign_manual_batches.py`
- `docs/tasks/2026-04-27_primary_benign_manual_10_batches.md`
- `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`

Data directories moved:

- Source: direct sample directories under `E:\WardenData\raw\benign\benign`
- Destination: `E:\WardenData\raw\benign\benign\manual_batches_20260427\batch_01..batch_10`

---

## 4. Behavior Impact

### Expected New Behavior

- Manual review can now proceed one batch directory at a time.
- The primary benign root no longer has direct sample directories; direct samples are nested under the batch root.
- Recursive consumers such as `build_manifest.py` can still discover the moved samples.

### Preserved Behavior

- Sample directory names are preserved.
- Sample-internal files are preserved.
- Manifest schema and label semantics are preserved.

### User-facing / CLI Impact

- Existing CLI commands were not changed.
- A new helper script was added; no existing CLI behavior was modified.

### Output Format Impact

- Existing output formats were not changed.
- New script outputs are additive review/maintenance artifacts.

---

## 5. Schema / Interface Impact

- Schema changed: no
- Backward compatible: yes for recursive manifest consumers
- Public interface changed: no
- Existing CLI still valid: yes

Affected schema fields / interfaces:

- none

Compatibility notes:

The raw directory layout changed from direct sample children to nested batch children. Recursive scanners continue to work. Tools that only scan direct child directories must be pointed at a specific `batch_XX` directory or updated to scan recursively.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile E:\Warden\scripts\data\benign\split_primary_benign_manual_batches.py
python E:\Warden\scripts\data\benign\split_primary_benign_manual_batches.py --input-root "E:\WardenData\raw\benign\benign" --batch-root "E:\WardenData\raw\benign\benign\manual_batches_20260427" --out-dir "E:\WardenData\reviewed\benign_manual_batches_20260427"
python E:\Warden\scripts\data\benign\split_primary_benign_manual_batches.py --input-root "E:\WardenData\raw\benign\benign" --batch-root "E:\WardenData\raw\benign\benign\manual_batches_20260427" --out-dir "E:\WardenData\reviewed\benign_manual_batches_20260427" --apply
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\raw\benign\benign" --out-dir "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck\manifest.jsonl" --out-dir "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck\consistency_check"
```

### Result

- Python compile check passed.
- Dry-run planned `20171` sample moves with `0` failures.
- Apply moved `20171` sample directories with `0` failures.
- Direct sample directories remaining in primary benign root: `0`.
- Recursive sample directories under primary benign root after split: `20171`.
- Post-split manifest build:
  - `num_records=20088`
  - `num_rejected=83`
  - `rejected_reason_distribution.missing_required_files=83`
- Post-split consistency checker:
  - `rows=20088`
  - `errors=0`
  - `warnings=0`

Batch counts:

| Batch | Count | screenshot_viewport.png | screenshot_full.png |
|---|---:|---:|---:|
| `batch_01` | 2018 | 2018 | 1896 |
| `batch_02` | 2017 | 2017 | 1864 |
| `batch_03` | 2017 | 2017 | 1872 |
| `batch_04` | 2017 | 2017 | 1881 |
| `batch_05` | 2017 | 2017 | 1863 |
| `batch_06` | 2017 | 2017 | 1865 |
| `batch_07` | 2017 | 2017 | 1881 |
| `batch_08` | 2017 | 2017 | 1887 |
| `batch_09` | 2017 | 2017 | 1844 |
| `batch_10` | 2017 | 2017 | 1895 |

### Not Run

- No manual visual classification was performed.
- No classifier UI smoke test was run.

Reason:

The task scope was only to split samples into batches and verify data consistency after the move.

---

## 7. Risks / Caveats

- The manual classifier `scripts/maintenance/benign_subcategory_classifier.py` currently looks for `screenshot_view.png` first and `screenshot_full.png` second. It does not read `screenshot_viewport.png`.
- All `20171` moved samples have `screenshot_viewport.png`, but only `18748` have `screenshot_full.png`. A classifier run using the current image priority may miss `1423` samples unless the tool is updated or those samples receive a compatible screenshot alias.
- Three non-sample container directories were intentionally skipped:
  - `E:\WardenData\raw\benign\benign\2026-04-08_planA_day11_tranco_top_100001_500000_batch_0008`
  - `E:\WardenData\raw\benign\benign\2026-04-08_planA_day11_tranco_top_10001_100000_batch_0014`
  - `E:\WardenData\raw\benign\benign\benign_classified`
- The current live inventory at execution time was `20171` direct sample directories. This handoff reports the current filesystem state, not any older snapshot count.

---

## 8. Docs Impact

- Docs updated: yes

Docs touched:

- `docs/tasks/2026-04-27_primary_benign_manual_10_batches.md`
- `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`

Doc debt still remaining:

- If the batch workflow becomes the standard manual-classification path, document it in the data/manual-review docs.

---

## 9. Recommended Next Step

- Update `scripts/maintenance/benign_subcategory_classifier.py` to include `screenshot_viewport.png` as a supported screenshot source before large-scale manual classification.
- Start manual classification from `E:\WardenData\raw\benign\benign\manual_batches_20260427\batch_01`.
