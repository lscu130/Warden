# fixture_task_doc_negative_missing_requested_by

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

- 这是 task doc checker 的负例 fixture。

## English Version

# Task Metadata

- Task ID: FIXTURE-TASK-DOC-NEGATIVE
- Task Title: Negative task doc fixture missing requested by
- Owner Role: Codex execution engineer
- Priority: P0
- Status: TODO
- Related Module: harness fixtures
- Related Issue / ADR / Doc: `docs/templates/TASK_TEMPLATE.md`
- Created At: 2026-04-20

---

## 1. Background

Minimal negative fixture for the task-doc checker.

---

## 2. Goal

Fail the structural task-doc lint.

---

## 3. Scope In

This task is allowed to touch:

- `tests/fixtures/`

This task is allowed to change:

- this file only

---

## 4. Scope Out

This task must NOT do the following:

- touch production code

---

## 5. Inputs

### Docs

- `docs/templates/TASK_TEMPLATE.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- none

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- one failing task-doc fixture

---

## 7. Hard Constraints

Must obey all of the following:

- remain minimal

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- none

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/negative_missing_requested_by.md`

Downstream consumers to watch:

- local harness tests

---

## 9. Suggested Execution Plan

Recommended order:

1. Run the checker.

---

## 10. Acceptance Criteria

- [ ] The fixture fails

---

## 11. Validation Checklist

- [ ] Run the task-doc checker
