<!-- operator: Codex; task: primary-benign-manual-10-batches; date: 2026-04-27 -->

# 中文摘要

本任务把当前 primary benign 主目录中的直接样本目录分成 10 个人工分类批次。

范围：

- 输入目录：`E:\WardenData\raw\benign\benign`
- 批次目录：`E:\WardenData\raw\benign\benign\manual_batches_20260427\batch_01` 到 `batch_10`
- 只移动直接样本目录，即同时包含 `meta.json` 和 `url.json` 的子目录。
- 跳过非样本容器目录，例如旧 batch 容器和 `benign_classified`。

本任务不修改样本内部文件，不改 labels，不改 schema，不做分类判断。

---

# English Version

# Task Metadata

- Task ID: 2026-04-27_primary_benign_manual_10_batches
- Task Title: Primary Benign Manual 10 Batches
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data
- Related Issue / ADR / Doc:
  - `docs/handoff/2026-04-27_primary_benign_consistency_and_dedup.md`
  - `scripts/maintenance/benign_subcategory_classifier.py`
- Created At: 2026-04-27
- Requested By: User

---

## 1. Background

The primary benign bucket has been deduplicated and checked for consistency. The user now wants the remaining benign samples split into 10 batches so manual subcategory classification can proceed in smaller units.

---

## 2. Goal

Create 10 deterministic, count-balanced manual-review batch directories and move the current direct primary benign sample directories into those batches.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/split_primary_benign_manual_batches.py`
- `docs/tasks/2026-04-27_primary_benign_manual_10_batches.md`
- `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`
- `E:\WardenData\raw\benign\benign`
- `E:\WardenData\reviewed\benign_manual_batches_20260427`

This task is allowed to change:

- Move direct sample directories from `E:\WardenData\raw\benign\benign` into `manual_batches_20260427\batch_01..batch_10`.
- Generate dry-run/apply manifests and summaries.

---

## 4. Scope Out

This task must NOT do the following:

- Do not classify samples.
- Do not modify sample-internal files.
- Do not modify labels, schemas, frozen fields, or taxonomy.
- Do not process `adult`, `gambling`, `gate`, `evasion`, or `tranco` buckets.
- Do not move non-sample container directories.
- Do not delete samples.

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- `scripts/maintenance/benign_subcategory_classifier.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

### Data / Artifacts

- `E:\WardenData\raw\benign\benign`

### Prior Handoff

- `docs/handoff/2026-04-27_primary_benign_consistency_and_dedup.md`

### Missing Inputs

- none

---

## 6. Required Outputs

- Batch directories `batch_01` through `batch_10`.
- Dry-run summary and plan JSONL.
- Apply summary and log JSONL.
- Post-split inventory summary.
- Repo handoff document.

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Use dry-run before moving directories.
- Move only direct child directories that contain both `meta.json` and `url.json`.
- Preserve sample directory names.
- Do not treat weak labels as manual gold labels.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Existing manifest schema.
- Existing sample-internal file names.
- Existing manual classifier scripts.

Schema / field constraints:

- Schema changed allowed: No
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\data\build_manifest.py ...`
  - `python E:\Warden\scripts\data\check_dataset_consistency.py ...`

Downstream consumers to watch:

- Manifest builder, which scans sample directories recursively.
- Manual classifier, which scans selected batch roots recursively for supported screenshots.

---

## 9. Suggested Execution Plan

Recommended order:

1. Inventory current direct sample directories.
2. Add a bounded dry-run/apply split script.
3. Run dry-run and inspect batch counts.
4. Apply the move.
5. Verify batch counts and run manifest/consistency check on the split root.
6. Prepare handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] 10 batch directories exist.
- [ ] All moved sample directories remain under `E:\WardenData\raw\benign\benign`.
- [ ] Direct non-sample containers remain unmoved.
- [ ] Dry-run and apply logs are written.
- [ ] Post-split manifest build succeeds.
- [ ] Post-split consistency checker reports no errors or warnings, or any failures are reported exactly.
- [ ] No schema / interface break was introduced.
- [ ] Handoff is provided.

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] Run split dry-run.
- [ ] Run split apply.
- [ ] Count samples per batch.
- [ ] Rebuild manifest from `E:\WardenData\raw\benign\benign`.
- [ ] Run consistency checker on the post-split manifest.

Commands to run if applicable:

```powershell
python E:\Warden\scripts\data\benign\split_primary_benign_manual_batches.py --input-root "E:\WardenData\raw\benign\benign" --batch-root "E:\WardenData\raw\benign\benign\manual_batches_20260427" --out-dir "E:\WardenData\reviewed\benign_manual_batches_20260427"
python E:\Warden\scripts\data\benign\split_primary_benign_manual_batches.py --input-root "E:\WardenData\raw\benign\benign" --batch-root "E:\WardenData\raw\benign\benign\manual_batches_20260427" --out-dir "E:\WardenData\reviewed\benign_manual_batches_20260427" --apply
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\raw\benign\benign" --out-dir "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck\manifest.jsonl" --out-dir "E:\WardenData\processed\primary_benign_20260427_manual_batches_postcheck\consistency_check"
```

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path:

- `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`

---

## 13. Open Questions / Blocking Issues

- none
