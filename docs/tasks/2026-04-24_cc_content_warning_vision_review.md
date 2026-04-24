<!-- operator: Codex; task: cc-content-warning-vision-review; date: 2026-04-24 -->

# 中文摘要

本任务定义 Claude Code 对 content-warning 人工复核目录做截图视觉二筛的边界。

已确认能力边界：

- CC 不能直接读取 `E:\WardenData` 下的 PNG。
- CC 可以读取仓库内 `E:\Warden\tmp\...` 下复制出来的 PNG，并能基于图像像素做 adult / gambling / benign 判断。

执行规则：

- Codex 负责 staging、基准样本选择、CC prompt、结果验收和最终移动。
- CC 只负责看仓库内 staging PNG 并写结构化 JSONL 判定。
- CC 不允许移动、删除、重命名或修改原始样本。
- CC 不允许只根据 URL / 文件名判断，必须基于截图可见内容。
- 低置信、截图不完整、内容不确定的样本必须标 `uncertain`。

---

# English Version

# Task Metadata

- Task ID: 2026-04-24_cc_content_warning_vision_review
- Task Title: Claude Code Content-Warning Screenshot Vision Review
- Owner Role: Codex
- Worker Role: ClaudeCode
- Priority: P1
- Status: TODO
- Related Module: Data / Labeling
- Related Issue / ADR / Doc:
  - `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
  - `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`
  - `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- Created At: 2026-04-24
- Requested By: User

---

## 1. Background

After conservative rebucketing, 2,256 ambiguous content-warning candidates were moved to:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

The user asked Codex to delegate screenshot review to Claude Code where possible. Capability probing showed that Claude Code cannot read external `E:\WardenData` images directly, but can inspect copied repo-local PNGs under `E:\Warden\tmp`.

---

## 2. Goal

Create a controlled CC screenshot-review workflow that classifies staged screenshots into:

- `adult`
- `gambling`
- `adult_and_gambling`
- `benign_or_false_positive`
- `uncertain`

The workflow must preserve Codex control over final movement and avoid CC making unreviewed data changes.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/stage_cc_content_warning_vision_batch.py`
- `docs/tasks/2026-04-24_cc_content_warning_vision_review.md`
- `tmp/cc_content_warning_vision_review_20260424/`
- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424` for read-only source screenshots.

This task is allowed to change:

- Add a staging helper script.
- Copy screenshots into ignored repo-local `tmp/` staging directories.
- Ask CC to write JSONL verdicts under the staging directory.

---

## 4. Scope Out

This task must NOT do the following:

- Do not let CC move, delete, rename, or edit original sample directories.
- Do not let CC write into `E:\WardenData`.
- Do not treat CC output as manual gold labels.
- Do not move any sample without Codex-side review of CC results.
- Do not review non-content-warning behavior-risk exclusions in this task.

---

## 5. Inputs

### Baseline Screenshots

- Adult baseline: `18porncomic.com_20260420T113554Z`
- Gambling baseline: `1xbet-benv.top_20260330T085847Z`
- Benign false-positive baseline: `101.ru_20260422T041006Z`
- Optional benign false-positive baselines: ordinary games/news sites from the manual-review folder.

### Review Source

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`

### Missing Inputs

- No final human labels exist for the 2,256 manual-review samples.

---

## 6. Required Outputs

- Repo-local staged screenshot batches under `tmp/`.
- A batch manifest JSONL mapping staged PNG names to original sample directories.
- CC-produced JSONL verdicts per batch.
- Codex-side validation summary before any movement.

---

## 7. Hard Constraints

- CC must judge from actual visual pixels.
- CC must not infer from filename or URL alone.
- CC must use `uncertain` for cropped, blank, ambiguous, or low-confidence screenshots.
- `adult` means explicit adult/porn/sexual content visible.
- `gambling` means betting/casino/bookmaker/lottery/slot/poker/sportsbook content visible.
- Normal games, news, music, shopping, ordinary login, ordinary ads, and age gates without adult/gambling content should be `benign_or_false_positive`.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: No.
- Existing CLI changed: No.
- CC verdict files are additive operational artifacts.

Expected CC JSONL fields:

- `sample_id`
- `staged_image`
- `visual_label`
- `confidence`
- `visible_evidence`
- `needs_human_review`

---

## 9. Acceptance Criteria

- CC successfully classifies a pilot batch from repo-local images.
- CC output is parseable JSONL.
- Codex checks the output before deciding any move.
- No original data is changed by CC.

---

## 10. Validation Checklist

- Stage a small pilot batch with baselines.
- Run CC on the pilot batch.
- Parse CC verdict JSONL.
- Spot-check a few CC labels manually.
- Only then decide whether to scale batch size.
