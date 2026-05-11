<!-- operator: Codex; task: tranco-benign-triage-t00-t05-consistency-dedup; date: 2026-05-07 -->

# 中文摘要

本任务对 `E:\WardenData\manifests\tranco_benign_triage_v1` 下 `T00` 到 `T05` 六个 triage 子目录做一致性检查和 URL-key 去重。

范围：

- `T00_clear_benign`
- `T01_benign_hard_negative`
- `T02_gamble`
- `T03_adult`
- `T04_gate`
- `T05_evasion`

本任务不修改样本内部文件，不改 labels，不改 schema，不改变 T 类语义。去重必须先 dry-run 输出计划；若执行删除，只删除现有 URL-key 去重规则确认的重复样本目录，并保留日志。

---

# English Version

# Task Metadata

- Task ID: 2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup
- Task Title: Tranco Benign Triage T00-T05 Consistency And Dedup
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data
- Related Issue / ADR / Doc:
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
  - `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`
- Created At: 2026-05-07
- Requested By: User

---

## 1. Background

The Tranco benign triage v1 buckets now need a consistency and deduplication pass before further manual or training-pool use.

---

## 2. Goal

Run manifest consistency checks and URL-key deduplication for the T00-T05 triage buckets, using a dry-run plan before any destructive operation.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/dedup_tranco_benign_triage_buckets.py`
- `docs/tasks/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`
- `docs/handoff/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T00_clear_benign`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T02_gamble`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T03_adult`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T04_gate`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T05_evasion`
- `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507`
- `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507`

This task is allowed to change:

- Delete same-bucket URL-key duplicate sample directories only after dry-run review.
- Report cross-bucket URL-key duplicates as triage conflicts unless explicitly approved for deletion.
- Generate manifest, rejected manifest, consistency reports, dedup keep/delete manifests, and summaries.

---

## 4. Scope Out

This task must NOT do the following:

- Do not touch T06, T90, or T99.
- Do not modify sample-internal files.
- Do not modify labels, schemas, frozen fields, or taxonomy.
- Do not reinterpret T bucket semantics.
- Do not move samples between T buckets.
- Do not add dependencies.

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`

### Data / Artifacts

- `E:\WardenData\manifests\tranco_benign_triage_v1\T00_clear_benign`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T02_gamble`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T03_adult`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T04_gate`
- `E:\WardenData\manifests\tranco_benign_triage_v1\T05_evasion`

### Prior Handoff

- `docs/handoff/2026-04-27_primary_benign_manual_10_batches.md`

### Missing Inputs

- none

---

## 6. Required Outputs

- Fresh manifest JSONL.
- Manifest rejected JSONL.
- Manifest build summary JSON.
- Consistency report JSON/MD/summary.
- Dedup dry-run keep/delete manifests and summary.
- Dedup apply keep/delete manifests and summary if duplicates are deleted.
- Post-dedup manifest and consistency report.
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

- Run consistency before and after delete when delete is applied.
- Run dedup dry-run before delete.
- Deduplicate same-bucket duplicates by directory-name URL key and keep the oldest timestamped sample.
- Keep cross-bucket duplicate evidence in the delete manifest and do not delete it by default.
- Do not treat weak labels as manual gold labels.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Existing manifest schema.
- Existing sample-internal file names.
- Existing build and consistency CLI behavior.

Schema / field constraints:

- Schema changed allowed: No
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\data\build_manifest.py ...`
  - `python E:\Warden\scripts\data\check_dataset_consistency.py ...`

Downstream consumers to watch:

- Manifest consumers.
- Manual triage consumers of T bucket directories.

---

## 9. Suggested Execution Plan

Recommended order:

1. Inventory T00-T05.
2. Run manifest build across T00-T05.
3. Run consistency checker.
4. Run URL-key dedup dry-run across T00-T05.
5. If duplicates exist, apply delete to same-bucket duplicates using the frozen keep-oldest policy.
6. Rebuild manifest and rerun consistency.
7. Write handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] T00-T05 inventory is recorded.
- [ ] Pre-dedup manifest and consistency check complete.
- [ ] Dedup dry-run complete.
- [ ] If duplicates are found and deletion is applied, delete log reports zero failures.
- [ ] Post-dedup manifest and consistency check complete.
- [ ] No sample-internal file, schema, label, or T bucket semantic change is introduced.
- [ ] Handoff is provided.

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] Run Python compile check for any new script.
- [ ] Run manifest build before dedup.
- [ ] Run consistency checker before dedup.
- [ ] Run dedup dry-run.
- [ ] Run dedup apply if needed.
- [ ] Run manifest build after dedup.
- [ ] Run consistency checker after dedup.

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path:

- `docs/handoff/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`

---

## 13. Open Questions / Blocking Issues

- none
