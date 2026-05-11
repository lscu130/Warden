# Handoff Metadata

- Handoff ID: HANDOFF-20260508-BENIGN-SPLIT-LEAKAGE-AUDIT-V1
- Related Task ID: TASK-20260508-BENIGN-SPLIT-LEAKAGE-AUDIT-V1
- Task Title: Audit Benign Train/Val/Test Split For Leakage And Temporal Distribution
- Module: Dataset / Manifest / Benign Cleaning / Evaluation Hygiene
- Author: Codex
- Date: 2026-05-08
- Status: DONE

## 中文版

已完成 benign clean V1 split 的只读泄露与时间分布审计。现有 manifest 层面的 `sample_id`、`current_path`、`final_url`、`final_host`、`etld1`、`group_key` 跨 split 泄露均为 0。

需要保留的风险：visible-text 和 HTML/DOM 指纹存在跨 split 精确或近似重复候选；screenshot hash 未运行；DOM 检查为有界轻量检查，不是完整模板聚类证明。

## English Version

This English section is authoritative.

## 1. Executive Summary

A read-only audit script was added and run against the existing benign clean V1 train/validation/test manifests. It generated a CSV audit artifact and a bilingual Markdown report under `E:\WardenData\manifests\benign_clean_v1`.

The manifest-key leakage result is clean: `sample_id`, `current_path`, `final_url`, `final_host`, `etld1`, and `group_key` each have `0` cross-split leaked keys. The audit still found visible-text and HTML/DOM duplicate or near-duplicate candidates, so the split should not be treated as fully leakage-free for benchmark claims without follow-up review.

The task reached its defined stop condition.

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/audit_benign_split_leakage.py`.
- The script reads existing split manifests and referenced lightweight artifacts in read-only mode.
- The script computes exact key leakage, label distribution, host/eTLD/group concentration, visible-text hashes, DOM/tag-sequence hashes, lightweight simhash near-duplicate candidates, temporal distribution, and artifact availability.

### Doc Changes

- Added `docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`.
- Added `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`.

### Output / Artifact Changes

- Generated `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_v1.csv`.
- Generated `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_report_v1.md`.

## 3. Files Touched

- `scripts/data/benign/audit_benign_split_leakage.py`
- `docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`
- `docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_split_leakage_audit_report_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- Maintainers can run a read-only split leakage audit with:
  `python scripts/data/benign/audit_benign_split_leakage.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1"`
- The command writes a CSV findings table and Markdown report without modifying existing manifests or sample directories.
- The report gives a direct evidence trail for split counts, label counts, exact leakage, near-duplicate candidates, temporal distribution, and not-run checks.

### Preserved Behavior

- Existing train/validation/test manifests were not regenerated or edited.
- Existing samples were not moved, copied, deleted, renamed, or relabeled.
- Training, inference, capture, teacher, OCR, YOLO, CLIP, MobileCLIP, SpecularNet, workflow rules, schemas, and labels were not changed.

### User-facing / CLI Impact

- New additive CLI script only. Existing CLIs are unchanged.

### Output Format Impact

- New additive audit CSV columns: `audit_type`, `severity`, `status`, `split_a`, `split_b`, `key_type`, `key_value`, `count_a`, `count_b`, `example_sample_a`, `example_sample_b`, `details`, `recommendation`.
- Existing output formats are unchanged.

## 5. Schema / Interface Impact

- Schema changed: no
- Backward compatible: yes
- Public interface changed: no
- Existing CLI still valid: yes

Affected schema fields / interfaces:

- none

Compatibility notes:

The new audit CSV is additive and does not modify any existing manifest schema or downstream training interface.

## 5.1 Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260508_BENIGN_SPLIT_LEAKAGE_AUDIT_V1.md`
- `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`
- `E:\WardenData\manifests\benign_clean_v1\benign_test_manifest_v1.csv`
- sample artifacts referenced by `current_path`, read-only
- generated audit CSV and generated audit report

Retrieval / reading performed:

- Read the task definition and current manifest directory.
- Ran the audit script over all `20253` split rows.
- Re-read the generated report and sampled the generated CSV.

Claims supported by evidence:

- Split counts are train `16202`, validation `2025`, test `2026`.
- Label counts are train T00 `14518` / T01 `1684`, validation T00 `1815` / T01 `210`, test T00 `1815` / T01 `211`.
- Exact manifest-key leakage for `sample_id`, `current_path`, `final_url`, `final_host`, `etld1`, and `group_key` is `0`.
- Visible-text exact cross-split hash keys: `22`; visible-text simhash candidate pairs: `1022`; visible-text oversized simhash bands skipped: `4`.
- HTML/DOM exact structure cross-split hash keys: `67`; HTML/DOM simhash candidate pairs: `91050`; HTML/DOM oversized simhash bands skipped: `47`.
- Artifact availability: visible text read `20233` / missing `20`; HTML/DOM parsed `20248` / missing `5` / truncated `12892`.
- Screenshot hash near-duplicate check is `not_run`.

Claims left unsupported or assumed:

- No claim is made that screenshot-level leakage is absent.
- No claim is made that DOM simhash candidates are confirmed semantic duplicates.
- No benchmark-readiness claim is made from this audit alone.

Retrieval stopped because:

- Required audit artifacts were generated and validation commands completed.

## 5.2 Counter-Review Performed

Original framing reviewed:

Run a read-only leakage and temporal-distribution audit before training or evaluation use of the benign split.

Assumptions checked:

- Existing split membership should remain unchanged during audit.
- Manifest-key leakage and near-duplicate risk are different questions.
- Missing screenshot hash means visual leakage absence cannot be claimed.

Failure modes considered:

- A group-key split can still contain text or DOM template duplicates across splits.
- Conservative stdlib eTLD grouping may miss public-suffix-level grouping issues.
- Large simhash buckets can overstate or understate near-duplicate risk if treated as final proof.

Counterexamples or contradictory evidence found:

- Manifest-key leakage is `0`, but visible-text and DOM duplicate/near-duplicate candidates are nonzero.

Alternative routes considered:

- Add screenshot image hashing. Rejected for this task because dependency-free image hashing was not implemented and new dependencies were out of scope.
- Run stronger clustering. Deferred as a follow-up because this task was bounded to a lightweight audit.

Framing changed: no

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- Public-suffix-list-backed grouping strength remains unverified.
- Screenshot near-duplicate status remains unknown.

Residual risks after counter-review:

- Visible-text and DOM candidates may require review or cluster-based re-splitting before final benchmark claims.
- Temporal holdout suitability remains a separate evaluation-design question.

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

- `python -m py_compile scripts/data/benign/audit_benign_split_leakage.py`
- `python scripts/data/benign/audit_benign_split_leakage.py --manifest-dir "E:\WardenData\manifests\benign_clean_v1" --output-dir "E:\WardenData\manifests\benign_clean_v1"`
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-08_benign_split_leakage_audit_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-08_benign_split_leakage_audit_v1.md`
- `git status --short --untracked-files=all`

### Result

- `py_compile`: passed.
- Audit script: passed and generated the required CSV/report artifacts.
- Task doc checker: passed.
- Handoff checker: passed.
- `git status`: completed; worktree contains unrelated pre-existing modified/untracked files in addition to this task's files.

### Not Run

- Screenshot hash near-duplicate detection was not run because the task prohibited new dependencies and no dependency-free image-hash path was implemented.
- Training, inference, teacher, OCR, YOLO, CLIP, MobileCLIP, and SpecularNet were not run because they are out of scope.

## 7. Risks / Caveats

- Visible-text and DOM near-duplicate candidates are warnings, not manual-confirmed leakage labels.
- DOM checks are partial because HTML artifacts are read with a bounded byte limit.
- Screenshot leakage status is unknown.
- Public-suffix-list-backed grouping remains a follow-up if stronger grouping guarantees are needed.
- The split is acceptable for preliminary training only with these caveats; it is not enough for strong final benchmark claims.

## 8. Docs Impact

- Docs updated: yes
- Updated docs are limited to the task and handoff for this audit.
- No workflow, schema, label, training, inference, capture, or evaluation documentation was changed.

## 9. Recommended Next Step

- Review the top visible-text and DOM duplicate/near-duplicate examples before using the split for benchmark claims.
- If the candidates are material, create a follow-up task for stronger cluster-based re-splitting.
- Create a separate public-suffix-list grouping task and temporal-holdout design task if final evaluation hygiene requires them.

## 10. Stop Condition

Stop condition reached: required audit artifacts were generated, repo docs were added, and validation commands passed.
