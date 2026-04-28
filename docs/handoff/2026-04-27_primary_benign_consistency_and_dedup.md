<!-- operator: Codex; task: primary-benign-consistency-and-dedup; date: 2026-04-27 -->

# 中文摘要

本次对 `E:\WardenData\raw\benign\benign` 做了 primary benign 一致性检查和 URL-key 去重。

结论：

- 最终 post-dedup manifest 有 `20183` 条有效记录，全部 `label_hint=benign`。
- manifest 拒收 `84` 条，原因均为 `missing_required_files`。
- consistency checker 最终结果为 `errors=0`、`warnings=0`。
- URL-key 去重删除了 1 个重复目录：`ezfly.com_20260424T020005Z`。
- 保留目录为：`ezfly.com_20260423T111919Z`。
- post-dedup URL-key dry-run 结果为重复数 `0`。
- 本次没有修改 labels、schema、CLI、样本内部文件。

注意：去重工具跳过了 3 个不符合样本目录模式的子目录，它们没有参与 URL-key 去重。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-04-27_primary_benign_consistency_and_dedup
- Related Task: `docs/tasks/2026-04-27_primary_benign_consistency_and_dedup.md`
- Owner Role: Codex
- Date: 2026-04-27
- Module: Data
- Status: Complete

---

## 1. Executive Summary

The primary benign directory was rebuilt into a fresh manifest, checked for consistency, deduplicated by URL key with the existing keep-oldest maintenance tool, and checked again after deletion.

Final state:

- Input directory: `E:\WardenData\raw\benign\benign`
- Final manifest rows: `20183`
- Final rejected rows: `84`
- Final consistency result: `errors=0`, `warnings=0`
- Final URL-key duplicate count: `0`

---

## 2. What Changed

One confirmed URL-key duplicate sample directory was deleted by the existing dedup tool:

- Kept: `E:\WardenData\raw\benign\benign\ezfly.com_20260423T111919Z`
- Deleted: `E:\WardenData\raw\benign\benign\ezfly.com_20260424T020005Z`
- URL key: `ezfly.com`
- Dedup rule: keep oldest timestamped directory

No sample-internal files were edited.

---

## 3. Files Touched

Repository docs:

- `docs/tasks/2026-04-27_primary_benign_consistency_and_dedup.md`
- `docs/handoff/2026-04-27_primary_benign_consistency_and_dedup.md`

Raw data:

- Deleted one duplicate directory under `E:\WardenData\raw\benign\benign`

Generated outputs:

- `E:\WardenData\processed\primary_benign_20260427_consistency`
- `E:\WardenData\processed\primary_benign_20260427_consistency_after_dedup`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup_delete`
- `E:\WardenData\processed\primary_benign_20260427_url_dedup_postcheck`

---

## 4. Behavior Impact

The primary benign raw bucket now has one fewer duplicate URL-key sample directory. Downstream manifest builds from `E:\WardenData\raw\benign\benign` will see `20183` valid rows instead of `20184`.

The final manifest still reports all valid rows as `label_hint=benign`.

---

## 5. Schema / Interface Impact

- Schema changed: no
- CLI changed: no
- Output format changed: no
- Backward compatible: yes
- Docs updated: yes

No label semantics were changed. Weak fields such as `risk_level_weak_distribution` remain weak metadata and were not treated as manual gold labels.

---

## 6. Validation Performed

Manifest build before delete:

```powershell
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\raw\benign\benign" --out-dir "E:\WardenData\processed\primary_benign_20260427_consistency" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
```

Result:

- `num_records=20184`
- `num_rejected=84`
- `rejected_reason_distribution.missing_required_files=84`

Consistency check before delete:

```powershell
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\primary_benign_20260427_consistency\manifest.jsonl" --out-dir "E:\WardenData\processed\primary_benign_20260427_consistency\consistency_check"
```

Result:

- `rows=20184`
- `errors=0`
- `warnings=0`

URL-key dedup dry-run:

```powershell
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root "E:\WardenData\raw\benign\benign" --output-dir "E:\WardenData\processed\primary_benign_20260427_url_dedup"
```

Result:

- `mode=dry_run`
- `num_matching_dirs=20268`
- `num_unique_url_keys=20267`
- `num_duplicate_dirs=1`
- `num_skipped_dirs=3`

URL-key dedup delete:

```powershell
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root "E:\WardenData\raw\benign\benign" --output-dir "E:\WardenData\processed\primary_benign_20260427_url_dedup_delete" --delete
```

Result:

- `mode=delete`
- `num_duplicate_dirs=1`
- `num_deleted_dirs=1`
- `num_delete_failures=0`

Manifest build after delete:

```powershell
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\raw\benign\benign" --out-dir "E:\WardenData\processed\primary_benign_20260427_consistency_after_dedup" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
```

Result:

- `num_records=20183`
- `num_rejected=84`
- `rejected_reason_distribution.missing_required_files=84`
- `usable_for_text=20163`
- `usable_for_vision=20183`
- `usable_for_multimodal=20163`

Consistency check after delete:

```powershell
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\primary_benign_20260427_consistency_after_dedup\manifest.jsonl" --out-dir "E:\WardenData\processed\primary_benign_20260427_consistency_after_dedup\consistency_check"
```

Result:

- `rows=20183`
- `errors=0`
- `warnings=0`

URL-key dedup postcheck:

```powershell
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root "E:\WardenData\raw\benign\benign" --output-dir "E:\WardenData\processed\primary_benign_20260427_url_dedup_postcheck"
```

Result:

- `mode=dry_run`
- `num_matching_dirs=20267`
- `num_unique_url_keys=20267`
- `num_duplicate_dirs=0`
- `num_skipped_dirs=3`

---

## 7. Open Risks / Caveats

Three child directories were skipped by the URL-key dedup tool because they do not match the timestamped sample-directory pattern:

- `E:\WardenData\raw\benign\benign\2026-04-08_planA_day11_tranco_top_100001_500000_batch_0008`
- `E:\WardenData\raw\benign\benign\2026-04-08_planA_day11_tranco_top_10001_100000_batch_0014`
- `E:\WardenData\raw\benign\benign\benign_classified`

These skipped directories were not deduplicated. If they contain nested samples, they need a separate nested-directory audit.

The 84 rejected rows remain unresolved. They are excluded from the valid manifest because required files are missing.

---

## 8. Recommended Next Step

Run a narrow audit on the three skipped child directories and the 84 `missing_required_files` rejects if those samples are expected to remain part of the primary benign training pool.
