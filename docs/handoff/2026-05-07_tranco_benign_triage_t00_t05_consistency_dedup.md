<!-- operator: Codex; task: tranco-benign-triage-t00-t05-consistency-dedup; date: 2026-05-07 -->

# 中文摘要

已对 `E:\WardenData\manifests\tranco_benign_triage_v1` 下 `T00` 到 `T05` 六个目录做一致性检查和去重。

实际目录名：

- `T00_clear_benign`
- `T01_benign_hard_negative`
- `T02_gamble`
- `T03_adult`
- `T04_gate`
- `T05_evasion`

结果：

- pre-dedup manifest：`22856` valid，`106` rejected，rejected 原因均为 `missing_required_files`
- pre-dedup consistency：`errors=0`，`warnings=1`
- dedup dry-run：发现 `46` 个 URL-key duplicate，其中 `39` 个同 bucket duplicate，`7` 个 cross-bucket duplicate
- apply delete：删除 `39` 个同 bucket duplicate，`0` delete failures
- cross-bucket duplicate：`7` 个全部保留，只记录为 triage conflict
- post-dedup manifest：`22817` valid，`106` rejected
- post-dedup consistency：`errors=0`，`warnings=1`
- post-dedup dedup check：同 bucket duplicate 已清零；仍有 `7` 个 cross-bucket duplicate 保留

本次不修改样本内部文件，不改 labels，不改 schema，不移动样本到其他 T bucket。

---

# English Version

# Handoff Metadata

- Handoff ID: 2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup
- Related Task ID: 2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup
- Task Title: Tranco Benign Triage T00-T05 Consistency And Dedup
- Module: Data
- Author: Codex
- Date: 2026-05-07
- Status: DONE

---

## 1. Executive Summary

The T00-T05 Tranco benign triage buckets were checked for manifest consistency and deduplicated by directory-name URL key.

Same-bucket URL-key duplicates were removed. Cross-bucket duplicates were preserved because they are triage-conflict evidence and deleting them could silently collapse a content/risk bucket into a different T bucket.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/dedup_tranco_benign_triage_buckets.py`.
- The script scans selected T-bucket direct child sample directories.
- Dry-run is the default.
- `--delete` deletes same-bucket duplicates only.
- `--delete-cross-bucket` exists as an explicit escape hatch, but it was not used.

### Doc Changes

- Added task document: `docs/tasks/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`.
- Added this handoff document.

### Output / Artifact Changes

- Generated pre-dedup manifest and consistency outputs:
  - `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\pre_dedup`
- Generated dedup dry-run, delete, and postcheck outputs:
  - `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507`
- Generated post-dedup manifest and consistency outputs:
  - `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup`

---

## 3. Files Touched

Repository files:

- `scripts/data/benign/dedup_tranco_benign_triage_buckets.py`
- `docs/tasks/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`
- `docs/handoff/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`

Data directories:

- Deleted `39` same-bucket duplicate sample directories under T00-T05.
- Did not delete or move cross-bucket duplicates.

---

## 4. Behavior Impact

### Expected New Behavior

- T00-T05 no longer contain same-bucket URL-key duplicates matched by the timestamped directory-name policy.
- Cross-bucket duplicate URL keys remain available for manual triage conflict review.
- Recursive manifest consumers can still build a manifest from the six T bucket roots.

### Preserved Behavior

- T bucket names and meanings were not changed.
- Sample-internal files were not changed.
- Existing manifest and consistency checker CLIs were not changed.

### User-facing / CLI Impact

- Existing CLIs unchanged.
- New additive maintenance CLI:

```powershell
python E:\Warden\scripts\data\benign\dedup_tranco_benign_triage_buckets.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507"
```

### Output Format Impact

- Existing output formats unchanged.
- New script writes additive JSONL/JSON maintenance artifacts.

---

## 5. Schema / Interface Impact

- Schema changed: no
- Backward compatible: yes
- Public interface changed: no
- Existing CLI still valid: yes

Affected schema fields / interfaces:

- none

Compatibility notes:

No frozen field names, labels, schema, or T bucket semantics were changed. The `label_hint_distribution` includes weak `phish` labels from existing artifacts; these were not treated as manual gold labels or final judgment.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile E:\Warden\scripts\data\benign\dedup_tranco_benign_triage_buckets.py
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\manifests\tranco_benign_triage_v1\T00_clear_benign" "E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative" "E:\WardenData\manifests\tranco_benign_triage_v1\T02_gamble" "E:\WardenData\manifests\tranco_benign_triage_v1\T03_adult" "E:\WardenData\manifests\tranco_benign_triage_v1\T04_gate" "E:\WardenData\manifests\tranco_benign_triage_v1\T05_evasion" --out-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\pre_dedup" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\pre_dedup\manifest.jsonl" --out-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\pre_dedup\consistency_check"
python E:\Warden\scripts\data\benign\dedup_tranco_benign_triage_buckets.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507"
python E:\Warden\scripts\data\benign\dedup_tranco_benign_triage_buckets.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507" --delete
python E:\Warden\scripts\data\benign\dedup_tranco_benign_triage_buckets.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_dedup_20260507\postcheck"
python E:\Warden\scripts\data\build_manifest.py --input-roots "E:\WardenData\manifests\tranco_benign_triage_v1\T00_clear_benign" "E:\WardenData\manifests\tranco_benign_triage_v1\T01_benign_hard_negative" "E:\WardenData\manifests\tranco_benign_triage_v1\T02_gamble" "E:\WardenData\manifests\tranco_benign_triage_v1\T03_adult" "E:\WardenData\manifests\tranco_benign_triage_v1\T04_gate" "E:\WardenData\manifests\tranco_benign_triage_v1\T05_evasion" --out-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup" --manifest-name manifest.jsonl --rejected-name manifest_rejected.jsonl --summary-name build_summary.json
python E:\Warden\scripts\data\check_dataset_consistency.py --manifest "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup\manifest.jsonl" --out-dir "E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup\consistency_check"
```

### Result

Initial T00-T05 direct sample inventory:

| Bucket | Direct Sample Dirs |
|---|---:|
| `T00_clear_benign` | 19522 |
| `T01_benign_hard_negative` | 743 |
| `T02_gamble` | 1454 |
| `T03_adult` | 1003 |
| `T04_gate` | 220 |
| `T05_evasion` | 19 |

Pre-dedup manifest:

- `num_records=22856`
- `num_rejected=106`
- rejected reason: `missing_required_files=106`
- `label_hint_distribution.benign=22245`
- `label_hint_distribution.phish=611`

Pre-dedup consistency:

- `rows=22856`
- `errors=0`
- `warnings=1`

Dedup dry-run:

- timestamp-pattern sample dirs scanned: `22940`
- unique URL keys: `22894`
- duplicate dirs: `46`
- same-bucket duplicate keys: `39`
- cross-bucket duplicate keys: `7`
- skipped nonmatching dirname dirs: `21`

Dedup delete:

- deleted same-bucket duplicate dirs: `39`
- skipped cross-bucket duplicates: `7`
- delete failures: `0`

Post-dedup dedup check:

- timestamp-pattern sample dirs scanned: `22901`
- unique URL keys: `22894`
- duplicate dirs remaining: `7`
- same-bucket duplicate keys: `0`
- cross-bucket duplicate keys: `7`
- skipped nonmatching dirname dirs: `21`

Post-dedup manifest:

- `num_records=22817`
- `num_rejected=106`
- rejected reason: `missing_required_files=106`
- `label_hint_distribution.benign=22206`
- `label_hint_distribution.phish=611`

Post-dedup consistency:

- `rows=22817`
- `errors=0`
- `warnings=1`
- status: `pass`

Consistency warning:

- code: `domain_etld1_mismatch`
- count: `3`
- examples:
  - `courrierdurif.com_20260330T035606Z`
  - `smsm.ph_20260402T062124Z`
  - `yydsong.com_20260407T120027Z`

Final direct sample inventory:

| Bucket | Direct Sample Dirs |
|---|---:|
| `T00_clear_benign` | 19522 |
| `T01_benign_hard_negative` | 741 |
| `T02_gamble` | 1437 |
| `T03_adult` | 985 |
| `T04_gate` | 218 |
| `T05_evasion` | 19 |

### Not Run

- No screenshot review was performed.
- No label correction was performed.
- No deletion of cross-bucket duplicates was performed.
- No cleanup of the 21 nonmatching-dirname sample directories was performed.
- No repair of the 106 missing-required-files rejected samples was performed.

Reason:

These actions are outside the frozen consistency and safe dedup scope for this task.

---

## 7. Risks / Caveats

- There are still `7` cross-bucket duplicate URL keys. They were intentionally preserved for manual conflict review.
- One preserved cross-bucket case is `kingsdalewines.com`, where pure keep-oldest would have kept `T00_clear_benign` and deleted `T02_gamble`; this is why cross-bucket duplicates were not auto-deleted.
- There are `21` sample directories with `meta.json` and `url.json` but nonmatching timestamp directory names, mostly under `T02_gamble` and `T04_gate`; the URL-key dedup script skipped them.
- There are `106` manifest rejected samples due to missing required files.
- The manifest has `611` weak `phish` label hints inside these triage buckets. This is recorded as existing weak-label metadata, not manual gold label evidence.
- The consistency warning is limited to IP-based `domain_etld1_mismatch` cases and did not fail the consistency check.

Cross-bucket duplicate URL keys preserved:

- `101.ru`: `T00_clear_benign` / `T03_adult`
- `cyberleninka.ru`: `T00_clear_benign` / `T03_adult`
- `edimaxcloud.com`: `T00_clear_benign` / `T05_evasion`
- `kill-bot.net`: `T00_clear_benign` / `T04_gate`
- `kingsdalewines.com`: `T00_clear_benign` / `T02_gamble`
- `osnews.com`: `T00_clear_benign` / `T03_adult`
- `privatehomeclips.com`: `T00_clear_benign` / `T03_adult`

---

## 8. Docs Impact

- Docs updated: yes

Docs touched:

- `docs/tasks/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`
- `docs/handoff/2026-05-07_tranco_benign_triage_t00_t05_consistency_dedup.md`

Doc debt still remaining:

- If this T-bucket dedup policy becomes standard, document the rule that cross-bucket duplicates are triage conflicts and must not be deleted by default.

---

## 9. Recommended Next Step

- Manually inspect the `7` cross-bucket duplicate URL keys and decide whether to keep one bucket, keep both as evidence, or move one into a conflict-review bucket.
- Separately audit the `21` nonmatching-dirname sample directories because URL-key dedup could not parse them.
- Separately handle the `106` `missing_required_files` rejected samples if they should remain in the usable triage pool.
