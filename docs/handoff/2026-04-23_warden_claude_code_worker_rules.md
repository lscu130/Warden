<!-- operator: Codex; task: warden-claude-code-worker-rules; date: 2026-04-23 -->

# 2026-04-23 Warden Claude Code Worker Rules Handoff

## 中文摘要

已为 Warden 新增项目级 `CLAUDE.md`，明确 Claude Code 在本仓库内只能作为 Codex 的受控 worker 执行简单或中等任务，并要求操作标记与交接说明。本次为文档治理改动，不涉及代码、schema、CLI 或运行时行为。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-23_warden_claude_code_worker_rules
- Related Task ID: 2026-04-23_warden_claude_code_worker_rules
- Task Title: Add Warden project-level Claude Code worker rules
- Module: workflow / repository governance
- Author: Codex
- Date: 2026-04-23
- Status: DONE

## 1. Executive Summary

Added a root-level `CLAUDE.md` for Warden. It defines Claude Code as a subordinate worker delegated by Codex, keeps Codex responsible for user-facing coordination and review, and records default safety boundaries, operation marker rules, task intake requirements, and final handoff requirements.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `CLAUDE.md` with bilingual project-level Claude Code worker rules.
- Added a task document for this governance change.
- Added this handoff document.

### Output / Artifact Changes

- none

## 3. Files Touched

- `CLAUDE.md`
- `docs/tasks/2026-04-23_warden_claude_code_worker_rules.md`
- `docs/handoff/2026-04-23_warden_claude_code_worker_rules.md`

## 4. Behavior Impact

### Expected New Behavior

- Future Claude Code work inside Warden has a project-level rule file.
- Claude Code is expected to stay inside Codex-provided scope boundaries.
- Claude Code is expected to add operation markers to touched text files and return factual handoff content.

### Preserved Behavior

- Existing Warden workflow authority remains in `AGENTS.md` and `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Existing schemas, CLI, labels, runtime behavior, and code behavior are unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This is a doc-only workflow governance addition.

## 6. Validation Performed

### Commands Run

```powershell
Get-Content -LiteralPath 'E:\Warden\AGENTS.md' -TotalCount 220
Get-Content -LiteralPath 'E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md' -TotalCount 180
Get-Content -LiteralPath 'E:\Warden\docs\templates\TASK_TEMPLATE.md' -TotalCount 220
Get-Content -LiteralPath 'E:\Warden\docs\templates\HANDOFF_TEMPLATE.md' -TotalCount 220
```

### Result

- Governing Warden workflow and template rules were read before editing.
- `CLAUDE.md` was added with project-level Claude Code worker boundaries.
- Operation markers were added to the new Markdown files.

### Not Run

- Runtime tests
- Schema tests
- CLI tests

Reason:

This task only adds documentation and workflow guidance. It does not change runtime code, schema, CLI, or data processing behavior.

## 7. Risks / Caveats

- Existing open Warden Codex threads may not automatically load the new `CLAUDE.md`; fresh threads are safer for using the new CC workflow.
- Claude Code still requires Codex review after delegated work; `CLAUDE.md` is a guardrail, not a proof of correctness.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `CLAUDE.md`
- `docs/tasks/2026-04-23_warden_claude_code_worker_rules.md`
- `docs/handoff/2026-04-23_warden_claude_code_worker_rules.md`

Doc debt still remaining:

- none

## 9. Recommended Next Step

Use a fresh Warden Codex thread for future work that should rely on `cc-direct.cmd`, `cc-delegation`, and this project-level `CLAUDE.md`.
