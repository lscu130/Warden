<!-- operator: Codex; task: template-noise-plan-content-and-benign; date: 2026-04-24 -->

# 中文摘要

本任务只做模板噪声 dry-run 计划，不移动文件。

范围：

- content-warning 人工复核池：`E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- 当前 primary benign 池：`E:\WardenData\raw\benign\benign`

目标：

- 找出类似 `bookiestation.com` / `bonushaven.de` 的重复模板内容站。
- 对每个池保留一小部分代表样本。
- 把大部分重复模板样本标记为后续可移动的 template-noise 候选。

本任务不把模板候选当作 manual gold labels，也不处理非模板样本。

---

# English Version

# Task Metadata

- Task ID: 2026-04-24_template_noise_plan_content_and_benign
- Task Title: Template Noise Plan For Content-Warning And Benign Pools
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data / Labeling
- Related Issue / ADR / Doc:
  - `docs/tasks/2026-04-24_content_warning_candidate_rebucket.md`
  - `docs/handoff/2026-04-24_content_warning_candidate_rebucket.md`
  - `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- Created At: 2026-04-24
- Requested By: User

---

## 1. Background

During manual content-warning review, the user identified a frequent template-page family represented by `bookiestation.com` and `bonushaven.de`. These pages often use generic news/blog layouts, placeholder images, repeated menu structure, and repeated authors such as Ryan Jones or Megan Ward.

The user suggested handling this template family in both the content-warning manual-review pool and the remaining benign pool.

---

## 2. Goal

Generate a dry-run plan that identifies repeated template-like pages in both pools, recommends a small representative keep set, and marks the remaining duplicate template pages as template-noise candidates for later movement.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/plan_template_noise_candidates.py`
- `docs/tasks/2026-04-24_template_noise_plan_content_and_benign.md`
- `docs/handoff/2026-04-24_template_noise_plan_content_and_benign.md`
- `E:\WardenData\reviewed\benign_second_pass\`

This task is allowed to read:

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\benign`

This task is allowed to change:

- Add a dry-run planning script.
- Write plan and summary artifacts.

---

## 4. Scope Out

This task must NOT do the following:

- Do not move sample directories.
- Do not delete sample directories.
- Do not edit raw sample files.
- Do not modify manual labels.
- Do not treat template-plan output as manual gold labels.
- Do not process adult/gambling/both visual decisions directly.

---

## 5. Inputs

### Data / Artifacts

- `E:\WardenData\raw\benign\hard benign\content_warning_manual_review_20260424`
- `E:\WardenData\raw\benign\benign`

### Pattern Seeds

- `bookiestation.com`
- `bonushaven.de`
- repeated visible-text markers such as `Your Ultimate Guide to`, `Latest Update`, `All Posts`, `Business`, `Esports`, `Fashion`, `Featured`, `Contact Us`, `Ryan Jones`, and `Megan Ward`.

### Missing Inputs

- No full manual review of all template-like pages exists.

---

## 6. Required Outputs

- A JSONL dry-run plan.
- A JSON summary with counts by source pool and suggested action.
- A handoff document.

---

## 7. Hard Constraints

- Dry-run only.
- Preserve raw sample contents.
- Keep a small representative set per pool.
- Prefer under-removal over accidental removal of real sites.
- Do not classify template noise as malicious.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: No.
- Existing CLI changed: No.
- Existing output formats changed: No.

The template plan is an additive operational artifact.

---

## 9. Acceptance Criteria

- The script scans both target pools.
- The plan includes source pool, template score, matched patterns, first line, suggested action, and suggested future target.
- The summary reports counts by source pool and action.
- No sample is moved.

---

## 10. Validation Checklist

- Run `py_compile` on the new script.
- Run the script in dry-run mode.
- Inspect summary counts.
- Spot-check known examples `bookiestation.com` and `bonushaven.de` appear as template candidates.
