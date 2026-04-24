<!-- operator: Codex; task: content-warning-candidate-rebucket; date: 2026-04-24 -->

# 中文摘要

本任务只处理 primary benign 二筛 manifest 中 `content_warning_candidate != none` 的样本。

执行边界：

- 高置信 adult / gambling 样本从 `raw\benign\benign` 移到 `raw\benign\hard benign\adult` 或 `raw\benign\hard benign\gambling`。
- 高置信 both 样本如存在，移到 `raw\benign\hard benign\adult_and_gambling`。
- 低置信或截图/文本不确定样本移到人工复核目录，供 `dataset_reviewed_switchable_targets.py` 继续人工筛。
- 不处理非 content-warning 的 `exclude` 样本。
- 不把 weak labels 当 manual gold labels。

---

# English Version

# Task Metadata

- Task ID: 2026-04-24_content_warning_candidate_rebucket
- Task Title: Content-Warning Candidate Rebucketing
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data / Labeling
- Related Issue / ADR / Doc:
  - `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
  - `docs/tasks/2026-04-24_primary_benign_second_pass_review_manifest.md`
  - `docs/handoff/2026-04-24_primary_benign_second_pass_review_manifest.md`
- Created At: 2026-04-24
- Requested By: User

---

## 1. Background

The second-pass manifest found 2,432 content-warning candidates in the remaining primary benign pool: adult, gambling, and adult-and-gambling. Spot-checking screenshots showed that the broad content-warning detector has false positives, including normal music, games, and news sites.

The user confirmed that non-content-warning behavior-risk exclusions should not be handled now because the URLs came from Tranco and were already first-pass reviewed from a human screenshot-template perspective.

---

## 2. Goal

Move only high-confidence adult/gambling content-warning samples into their hard-benign content buckets, and move all low-confidence content-warning candidates into a new manual-review folder for human screening.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/`
- `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
- `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`
- `E:\WardenData\raw\benign\benign`
- `E:\WardenData\raw\benign\hard benign\adult`
- `E:\WardenData\raw\benign\hard benign\gambling`
- `E:\WardenData\raw\benign\hard benign\adult_and_gambling`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\reviewed\benign_second_pass\`

This task is allowed to change:

- Add a move-plan script.
- Generate dry-run and apply manifests.
- Move sample directories according to the generated plan.

---

## 4. Scope Out

This task must NOT do the following:

- Do not handle non-content-warning `exclude` rows.
- Do not delete sample directories.
- Do not edit raw sample files.
- Do not modify `manual_labels.json`.
- Do not claim moved samples are final manual labels.
- Do not change TrainSet V1 schema.
- Do not run training or inference.

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`

### Code / Scripts

- `scripts/data/benign/build_primary_benign_second_pass_review.py`
- `scripts/maintenance/dataset_reviewed_switchable_targets.py`

### Data / Artifacts

- `E:\WardenData\reviewed\benign_second_pass\2026-04-24_primary_benign_second_pass_review_manifest.jsonl`
- `E:\WardenData\raw\benign\benign`

### Prior Handoff

- `docs/handoff/2026-04-24_primary_benign_second_pass_review_manifest.md`

### Missing Inputs

- No exhaustive human visual review is available for all 2,432 candidates.

---

## 6. Required Outputs

- A dry-run move plan.
- An applied move log.
- High-confidence samples moved into adult/gambling/both target buckets.
- Low-confidence samples moved into a manual-review folder.
- A handoff document with exact counts and caveats.

---

## 7. Hard Constraints

- Preserve raw sample contents.
- Move directories only; do not rewrite their internal files.
- Use strict high-confidence URL/domain rules for automatic adult/gambling movement.
- Send all weak or ambiguous matches to manual review.
- Keep weak-label and routing-suggestion status explicit.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: No.
- Existing commands changed: No.
- Existing output formats changed: No.

The move plan is an additive operational artifact.

---

## 9. Acceptance Criteria

- Dry-run counts are generated before applying moves.
- Apply mode records every move or skip.
- Source and destination counts are reported.
- No non-content-warning candidates are moved.
- Manual-review folder is ready for `dataset_reviewed_switchable_targets.py`.

---

## 10. Validation Checklist

- Run dry-run plan.
- Inspect counts and representative screenshots.
- Run apply mode.
- Verify target directories exist.
- Verify moved counts from the apply log.
- Record any conflicts or skipped rows.
