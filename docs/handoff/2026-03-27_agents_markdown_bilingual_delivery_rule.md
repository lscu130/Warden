# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 `AGENTS.md` Markdown 双语交付规则补充任务的正式 handoff。
- 若涉及精确文件清单、规则措辞、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`2026-03-27-agents-markdown-bilingual-delivery-rule`
- 任务主题：在 `AGENTS.md` 中补充 Markdown 文档必须双语、中文摘要在前、英文全文在后的仓库级规则
- 当前状态：`DONE`
- 所属模块：`project-documentation`

### 当前交付要点

- 已在 `AGENTS.md` 的中文摘要区和英文权威区补入新的 Markdown 双语交付规则。
- 规则明确要求：给用户的 Markdown 文档默认采用双语结构，中文摘要在前，英文全文在后。
- 同时保留了英文版对 AI 的权威口径，没有扩散修改到 workflow、template 或检查脚本。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-27-agents-markdown-bilingual-delivery-rule
- Related Task ID: 2026-03-27-agents-markdown-bilingual-delivery-rule
- Task Title: Add a repository-level rule in AGENTS.md requiring bilingual Markdown delivery with Chinese summary first and English full text second
- Module: project-documentation
- Author: Codex
- Date: 2026-03-27
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Updated `AGENTS.md` to add an explicit repository-level Markdown delivery rule.
The new rule states that Markdown documents delivered to the user must be bilingual by default, with a Chinese summary first for human reading and the full English version afterward for AI reading.

The existing interpretation rule was preserved: English remains authoritative for AI whenever exact wording, fields, commands, priorities, or historical facts matter.
The change was intentionally limited to `AGENTS.md` plus the task and handoff documents for this edit.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added a Chinese-summary-side note in `AGENTS.md` stating that user-facing Markdown documents must default to a bilingual structure.
- Added a Chinese key-rule bullet in `AGENTS.md` requiring bilingual Markdown with Chinese summary first and English full text second.
- Added two English authoritative rules in `AGENTS.md` under Global execution rules defining the bilingual Markdown requirement and reaffirming English as the authoritative version.
- Added the scoped task doc for this non-trivial contract update.
- Added this repo handoff document.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\tasks\2026-03-27_agents_markdown_bilingual_delivery_rule.md`
- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

Optional notes per file:

- `AGENTS.md` received the actual contract change.
- The task and handoff files were added to satisfy the repository workflow for a non-trivial documentation-contract edit.
- No workflow/template/script files were modified.

---

## 4. Behavior Impact

### Expected New Behavior

- Future Markdown documents delivered to the user are now explicitly required by `AGENTS.md` to use a bilingual structure by default.
- The expected ordering is now explicit: Chinese summary first, full English version second.
- AI-facing interpretation remains explicit: English is the authoritative version for exact facts and contract reading.

### Preserved Behavior

- Existing repository code behavior is unchanged.
- Existing workflow/template filenames and process contracts outside `AGENTS.md` were not edited.
- No schema, CLI, runtime output, or module-boundary behavior changed.

### User-facing / CLI Impact

- No CLI impact.
- Documentation/process expectations for future Markdown deliverables are now stricter and clearer.

### Output Format Impact

- Runtime output format did not change.
- Markdown delivery expectations changed at the repository-contract level.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `AGENTS.md` documentation contract wording
- user-facing Markdown delivery format expectations
- AI-facing interpretation rule for Markdown documents

Compatibility notes:

This is a governance/documentation-contract change only.
It does not modify code interfaces, schema fields, CLI commands, or runtime outputs.
The main downstream effect is procedural: future Markdown docs created under this contract should follow the bilingual Chinese-summary-first / English-full-second structure.

---

## 6. Validation Performed

### Commands Run

```bash
rg -n "bilingual|Markdown documents delivered|English remains the authoritative|中文摘要在前|双语结构" E:\Warden\AGENTS.md
Get-Content -Raw E:\Warden\AGENTS.md
git status --short
```

### Result

- Confirmed the new bilingual Markdown delivery rules appear in `AGENTS.md` in both the Chinese summary section and the English authoritative section.
- Confirmed `AGENTS.md` still explicitly preserves English as the authoritative version for AI-facing exact interpretation.
- Confirmed the worktree is already dirty with many unrelated pre-existing changes; the files touched by this task are limited to the three scoped documentation files listed above.

### Not Run

- Markdown checker script run
- cross-document synchronization updates to workflow/template docs
- rendered Markdown viewer check

Reason:

The task scope was limited to adding one repository-level contract rule in `AGENTS.md`.
Direct content inspection and search were sufficient for this minimal documentation-only validation pass.
Workflow/template synchronization was intentionally left out of scope for this task.

---

## 7. Risks / Caveats

- `AGENTS.md` now states the Markdown rule explicitly, but `docs/workflow/` and `docs/templates/` were not synchronized in this pass.
- Because the repository worktree already contains many unrelated user changes, `git status --short` cannot by itself prove exclusivity; scope control depended on intentional file targeting.
- Future enforcement is still manual unless a separate task adds or updates repository checks.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\tasks\2026-03-27_agents_markdown_bilingual_delivery_rule.md`
- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

Doc debt still remaining:

- `docs/workflow/GPT_CODEX_WORKFLOW.md` and the templates do not yet restate this new Markdown delivery rule
- no automatic checker enforcement was added for the new contract in this task

---

## 9. Recommended Next Step

- If you want this rule enforced beyond `AGENTS.md`, update `docs/workflow/GPT_CODEX_WORKFLOW.md` and the Markdown-related templates in a separate scoped task.
- If you want automatic enforcement, add or extend a repository-local Markdown policy checker in a separate task.
- For now, treat `AGENTS.md` as the active source of truth for this Markdown delivery requirement.
