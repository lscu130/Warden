# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“英文措辞统一润色”任务的正式任务单。
- 若中英文存在冲突，以英文版为准。

### 摘要

- 任务 ID：2026-03-23-english-wording-consistency-polish
- 任务主题：对已经扩写的英文长文档做措辞统一和轻量润色
- 当前状态：DONE
- 相关模块：project-documentation

### 当前任务要点

- 本任务是 wording-only pass，不改技术语义、不改字段名、不改文档结论。
- 重点是统一长期文档里的术语、连字符写法和相近表达，避免不同文档之间漂移。
- 润色范围只覆盖英文区块，中文原文不跟着重写。

## English Version

# Task Metadata

- Task ID: 2026-03-23-english-wording-consistency-polish
- Task Title: Polish wording consistency across expanded English long-form docs
- Owner Role: Codex
- Priority: Medium
- Status: DONE
- Related Module: project-documentation
- Related Issue / ADR / Doc: AGENTS.md; docs/workflow/GPT_CODEX_WORKFLOW.md; docs/tasks/2026-03-23_chinese_longform_english_expansion.md; docs/handoff/2026-03-23_chinese_longform_english_expansion.md
- Created At: 2026-03-23
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.

---

## 1. Background

The previous task expanded the English sections of seven long Chinese-origin Markdown documents from summary-only coverage into fuller section-by-section English content.
The user now wants a follow-up pass focused on wording consistency inside those English sections.
This is a polish pass, not a semantic rewrite.

---

## 2. Goal

Make the English wording across the previously expanded long-form documents more consistent in tone, terminology, and repeated phrasing, while preserving all technical meaning, frozen terminology, workflow rules, and schema-related wording boundaries.

---

## 3. Scope In

This task is allowed to touch:

- `README.md`
- `STRUCTION.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`

This task is allowed to change:

- English wording inside the English sections only
- repeated terminology for consistency, such as hyphenation, noun phrase choices, and repeated wording patterns
- awkward or uneven phrasing that can be improved without changing meaning

---

## 4. Scope Out

This task must NOT do the following:

- modify any Chinese source block
- add new technical claims
- change schema, labels, CLI, output contracts, or workflow rules
- expand scope to unrelated Markdown files

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\tasks\2026-03-23_chinese_longform_english_expansion.md`
- `E:\Warden\docs\handoff\2026-03-23_chinese_longform_english_expansion.md`

### Data / Artifacts

- the current English-expanded versions of the seven scoped Markdown files
- current repository worktree state

### Missing Inputs

- none

---

## 6. Required Outputs

This task must produce:

- wording-only edits in the English sections of the scoped long-form docs as needed
- a completed task record for this polish pass
- a handoff document under `docs/handoff/`

---

## 7. Hard Constraints

- Preserve all technical meaning.
- Preserve all frozen field names exactly.
- Preserve all CLI names, file names, and JSON keys exactly.
- Do not rewrite Chinese source text.
- Prefer the smallest valid wording patch.

---

## 8. Interface / Schema Constraints

- Schema must remain unchanged.
- Public interfaces must remain unchanged.
- Documentation structure must remain Chinese first, English second.
- `### Original Chinese Source` markers must remain present.

---

## 9. Acceptance Criteria

This task is complete only if:

- the scoped English sections show reduced wording drift across repeated terms
- no technical meaning was changed
- no Chinese source block was modified
- a handoff record exists for this polish pass

---

## 10. Validation Checklist

- spot-check the edited files in UTF-8
- search the scoped files for targeted inconsistent phrases before and after the patch
- confirm preserved `## English Version` and `### Original Chinese Source` markers
- confirm the task remains documentation-only
