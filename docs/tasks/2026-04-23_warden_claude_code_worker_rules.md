<!-- operator: Codex; task: warden-claude-code-worker-rules; date: 2026-04-23 -->

# 2026-04-23 Warden Claude Code Worker Rules Task

## 中文摘要

本任务为 Warden 增加项目级 `CLAUDE.md`，用于约束 Claude Code 作为 Codex 副手时的职责、边界、操作标记和 handoff 格式。

## English Version

# Task Metadata

- Task ID: 2026-04-23_warden_claude_code_worker_rules
- Task Title: Add Warden project-level Claude Code worker rules
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: workflow / repository governance
- Related Issue / ADR / Doc: `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, `docs/templates/HANDOFF_TEMPLATE.md`
- Created At: 2026-04-23
- Requested By: user

## 1. Background

The user established a new workflow where Claude Code acts as a subordinate worker for Codex. The global Codex and Claude Code skills already define the general role split, but Warden needs a project-level rule file so Claude Code can load repository-specific expectations in future fresh threads.

## 2. Goal

Create a minimal project-level `CLAUDE.md` that constrains Claude Code work inside Warden to bounded simple or medium tasks, requires operation markers, and requires factual handoff back to Codex.

## 3. Scope In

This task is allowed to touch:

- `CLAUDE.md`
- `docs/tasks/2026-04-23_warden_claude_code_worker_rules.md`
- `docs/handoff/2026-04-23_warden_claude_code_worker_rules.md`

This task is allowed to change:

- add project-level Claude Code worker rules
- add the corresponding task record
- add the corresponding handoff record

## 4. Scope Out

This task must not:

- modify existing Warden workflow contracts
- modify code, tests, schemas, labels, CLI, or runtime behavior
- install new tools or dependencies
- change existing dirty worktree files
- promote Claude Code beyond the default simple/medium worker boundary

## 5. Inputs

Docs:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Code / Scripts:

- none

Data / Artifacts:

- none

Prior Handoff:

- none used directly

Missing Inputs:

- none

## 6. Required Outputs

This task should produce:

- `CLAUDE.md`
- this task document
- a handoff document

## 7. Hard Constraints

Must obey all of the following:

- Keep the change doc-only.
- Preserve existing Warden workflow authority.
- Do not alter existing files with unrelated dirty changes.
- Keep Claude Code as a subordinate worker reviewed by Codex.
- Require operation markers for touched text files where the format allows comments.

Task-specific constraints:

- Do not install extra Claude Code skills for now.
- Do not expand Claude Code authority without a later user-approved promotion report.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Warden runtime interfaces
- Warden schema fields
- Warden CLI commands

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working: all existing commands

## 9. Acceptance Criteria

- `CLAUDE.md` exists at repository root.
- `CLAUDE.md` states that Codex supervises and reviews Claude Code work.
- `CLAUDE.md` states that Claude Code must stay inside `Scope In` and `Scope Out`.
- `CLAUDE.md` forbids deletion, dependency installation, network use, global config changes, and unsafe destructive commands by default.
- `CLAUDE.md` defines operation marker and handoff requirements.
- Task and handoff documents are created for auditability.

## 10. Validation Checklist

- Confirm `CLAUDE.md` exists.
- Confirm key phrases are present with `Select-String`.
- Confirm git status shows only the intended new files from this task, aside from pre-existing unrelated dirty files.
