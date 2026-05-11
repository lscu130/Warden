# Handoff Metadata

- Handoff ID: HANDOFF-20260509-BENIGN-APPLY-MANUAL-REMOVED-SAMPLES-V1
- Related Task ID: TASK-20260509-BENIGN-APPLY-MANUAL-REMOVED-SAMPLES-V1
- Task Title: Apply Manual Removed R01 Samples To Benign Clean Manifests And Source Directories
- Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Author: Codex
- Date: 2026-05-09
- Status: DONE

## 中文版

已按用户要求应用 R01 人工移除结果：从 `benign_clean_v1` clean pool / split manifest 中删除 4 个样本行，同时删除 review queue 中对应 R01 removed 副本目录，并删除 `tranco_benign_triage_v1` 下对应原始样本目录。

最新行数：clean pool 20,249；train 16,200；val 2,023；test 2,026。4 个 sample_id 在 clean/split manifests 中剩余命中为 0。没有重切 split，没有改标签，没有改 schema、训练或推理逻辑。

## English Version

This English section is authoritative.

## 1. Executive Summary

Added and ran `scripts/data/benign/apply_benign_review_queue_removed_samples.py` to apply the 4 manually removed R01 samples.

The script removed matching rows from `benign_clean_v1` clean/split manifests, deleted the matching R01 review-queue `removed` copy directories, and deleted the matching original sample directories under `E:\WardenData\manifests\tranco_benign_triage_v1`.

The task reached its defined stop condition.

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/apply_benign_review_queue_removed_samples.py`.
- The script enforces deletion safety by checking review deletion paths stay under the review root and original sample deletion paths stay under the triage root.

### Doc Changes

- Added `docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`.
- Added `docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`.

### Output / Artifact Changes

- Generated `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_v1.csv`.
- Generated `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_report_v1.md`.
- Updated `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`.
- Updated `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`.
- Updated `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`.
- `benign_test_manifest_v1.csv` was checked and unchanged in row count.
- Deleted 4 review queue removed-copy directories.
- Deleted 4 original triage sample directories.

## 3. Files Touched

- `scripts/data/benign/apply_benign_review_queue_removed_samples.py`
- `docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_removed_samples_apply_report_v1.md`
- deleted review/source sample directories listed in the apply report

## 4. Behavior Impact

### Expected New Behavior

- Future consumers of `benign_clean_v1` clean/split manifests will no longer see the 4 manually removed samples.
- The corresponding original triage sample directories and review removed-copy directories are gone.
- The apply report records the destructive cleanup.

### Preserved Behavior

- Remaining samples and labels were not changed.
- Split was not regenerated.
- Existing manifest schemas were preserved.
- Training, inference, capture, teacher, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, schema logic, and evaluation logic were not changed.

### User-facing / CLI Impact

- New additive CLI script only. Existing CLIs are unchanged.

### Output Format Impact

- Existing manifest columns are unchanged.
- Row counts changed due to targeted removals.

## 5. Schema / Interface Impact

- Schema changed: no
- Backward compatible: partially
- Public interface changed: no
- Existing CLI still valid: yes

Affected schema fields / interfaces:

- none

Compatibility notes:

The manifest row set changed. Any derived reports generated before this cleanup may now be stale for row counts.

## 5.1 Evidence / Retrieval Performed

Evidence sources actually checked:

- `E:\WardenData\manifests\benign_clean_v1_review_queue\manual_review_decisions_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\tranco_benign_clean_pool_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- filesystem existence checks for deleted review and source directories
- generated apply CSV/report

Retrieval / reading performed:

- Identified the 4 R01 removed sample IDs.
- Checked their presence in clean/split manifests before apply.
- Ran the apply script.
- Verified residual hits are `0` in clean/split manifests.
- Verified source directories and review-copy directories no longer exist.
- Checked latest split row and label counts.

Claims supported by evidence:

- Removed samples: `hbwrapper.com_20260327T092406Z`, `tipsport.org_20260330T033620Z`, `offthepress.com_20260422T131113Z`, `wha.com_20260413T045537`.
- Clean pool rows changed `20253 -> 20249`.
- Train rows changed `16202 -> 16200`.
- Validation rows changed `2025 -> 2023`.
- Test rows stayed `2026`.
- Removed sample IDs have `0` remaining hits in clean/split manifests.
- Four original triage sample directories no longer exist.
- Four review queue removed-copy directories no longer exist.

Claims left unsupported or assumed:

- No claim is made that derived audit/review reports were regenerated.
- No claim is made that split ratios were rebalanced.

Retrieval stopped because:

- Targeted removal and validation evidence were complete.

## 5.2 Counter-Review Performed

Original framing reviewed:

Delete samples that were manually removed from the review queue from benign clean manifests and source locations.

Assumptions checked:

- Only the 4 `removed_from_review_queue_by_manual_action` R01 samples are in scope.
- Deleting original sample directories is allowed because the user explicitly requested it.
- Re-splitting is out of scope.

Failure modes considered:

- Deleting outside the intended roots. Prevented by path safety checks.
- Accidentally deleting non-target samples. Prevented by sample-id filtering.
- Leaving stale reports. Reported as caveat.

Counterexamples or contradictory evidence found:

- none after apply; all 4 targets were found and deleted from source directories.

Alternative routes considered:

- Quarantine instead of delete. Not used because user explicitly requested deletion.
- Re-run full split generation. Not used because the task requested targeted removal.

Framing changed: no

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- Downstream regenerated audit metrics remain future work.

Residual risks after counter-review:

- Prior audit/smoke/review reports may show stale row counts until regenerated.

Decision after counter-review:

- ACCEPT_ORIGINAL

## 5.3 Tool / Agent Parameters

- Agent: Codex
- Reasoning effort: default session setting
- Verbosity: concise engineering handoff
- External web: not used
- Third-party dependencies: not added

## 6. Validation Performed

### Commands Run

- `python -m py_compile scripts/data/benign/apply_benign_review_queue_removed_samples.py`
- `python scripts/data/benign/apply_benign_review_queue_removed_samples.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --review-root "E:\WardenData\manifests\benign_clean_v1_review_queue" --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1"`
- residual search for removed sample IDs in clean/split manifests
- source directory existence checks
- review queue removed-copy directory existence checks
- read generated apply CSV/report
- latest split label-count check
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-09_benign_apply_manual_removed_samples_v1.md`
- `git status --short --untracked-files=all`

### Result

- Compile passed.
- Apply script passed.
- Clean/split manifest residual hits: `0`.
- Source sample directories: all 4 `exists=False`.
- Review queue removed-copy directories: all 4 `exists=False`.
- Task doc checker passed.
- Handoff checker passed.
- `git status` completed; unrelated pre-existing dirty files remain.

### Not Run

- No split regeneration.
- No training, inference, teacher, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, screenshot pHash/dHash, or external lookup.
- No derived audit/review report regeneration.

## 7. Risks / Caveats

- Prior reports under `benign_clean_v1` and review queue may be stale for row counts.
- The split was not rebalanced after removing 2 train and 2 validation rows.
- Deleted original sample directories are destructive filesystem changes.

## 8. Docs Impact

- Docs updated: yes.
- Updated docs are limited to this task and handoff.
- No workflow, schema, label, training, inference, capture, or evaluation documentation was changed.

## 9. Recommended Next Step

- Regenerate loader smoke / leakage audit summaries if current row counts must be reflected in reports.
- If exact 80/10/10 ratios matter, create a separate re-split task.

## 10. Stop Condition

Stop condition reached: targeted removals were applied, deletion status was verified, apply report was generated, and validation passed.
