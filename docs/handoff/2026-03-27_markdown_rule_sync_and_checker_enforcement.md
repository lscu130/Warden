# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“Markdown 双语交付规则同步与检查器补强”任务的正式 handoff。
- 若涉及精确文件清单、CLI 参数、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`2026-03-27-markdown-rule-sync-and-checker-enforcement`
- 任务主题：同步 Markdown 双语交付规则到 workflow / template，并给检查器补上对应规则检查
- 当前状态：`DONE`
- 所属模块：`project-documentation`

### 当前交付要点

- 已在 workflow 和两个模板里显式写入“Markdown 默认双语、中文摘要在前、英文全文在后、英文权威”。
- 已扩展 Markdown 检查器，新增 `--require-authority-note` 严格模式，用来检查中英文区块的 authority note。
- 为保持向后兼容，默认扫描仍只检查原有结构规则；严格模式才启用新检查，避免把大量历史文档一并打爆。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-27-markdown-rule-sync-and-checker-enforcement
- Related Task ID: 2026-03-27-markdown-rule-sync-and-checker-enforcement
- Task Title: Synchronize the Markdown bilingual-delivery rule into workflow/templates and extend the Markdown checker to enforce the key rule structure
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

Updated the workflow and both Markdown templates so they explicitly inherit the repository rule that Markdown deliverables must be bilingual by default, with a Chinese summary first and the full English version second, while English remains authoritative for exact facts and contracts.

Extended `scripts/maintenance/check_markdown_bilingual_structure.py` with a new strict-mode rule check, `--require-authority-note`, that validates the presence of the AI-authoritative note in both the Chinese and English sections.
The stricter rule was made opt-in instead of default-on because a default-on change would have immediately failed many pre-existing repository docs outside this task's scope.

---

## 2. What Changed

### Code Changes

- Extended `scripts/maintenance/check_markdown_bilingual_structure.py` with an additive strict-mode flag `--require-authority-note`.
- Added two new issue codes used only when that flag is enabled:
  - `missing_cn_authority_note`
  - `missing_en_authority_note`
- Kept the default checker behavior backward compatible by leaving strict authority-note enforcement disabled unless explicitly requested.

### Doc Changes

- Updated `docs/workflow/GPT_CODEX_WORKFLOW.md` to state the Markdown bilingual-delivery rule in both the Chinese summary section and the English workflow rules/instructions.
- Updated `docs/templates/TASK_TEMPLATE.md` so Markdown-producing tasks explicitly define bilingual Chinese-summary-first / full-English-second outputs with English authoritative.
- Updated `docs/templates/HANDOFF_TEMPLATE.md` so Markdown handoffs explicitly follow the same bilingual rule.
- Added the scoped task doc for this change.
- Added this repo handoff document.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`
- `E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py`
- `E:\Warden\docs\tasks\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`
- `E:\Warden\docs\handoff\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`

Optional notes per file:

- The workflow/template changes are wording-only and contract-only.
- The checker change is additive and keeps the original default scan compatible.
- No repository-wide doc repair was performed in this task.

---

## 4. Behavior Impact

### Expected New Behavior

- Workflow guidance now explicitly tells future Warden work to write Markdown deliverables as bilingual Chinese-summary-first / full-English-second documents.
- The task and handoff templates now carry the same expectation directly into future task definitions and handoff outputs.
- Operators can now run the checker in a stricter mode with `--require-authority-note` to validate the AI-authoritative-note rule.

### Preserved Behavior

- Default checker runs remain compatible with the current repository and still pass on the current doc corpus.
- No code outside the Markdown checker changed.
- No existing CLI was removed or renamed.

### User-facing / CLI Impact

- New additive checker flag:
  - `--require-authority-note`

### Output Format Impact

- Default checker stdout/JSON structure remains compatible.
- Strict mode can now emit two additional issue codes:
  - `missing_cn_authority_note`
  - `missing_en_authority_note`

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- workflow wording for Markdown deliverables
- task/handoff template wording for Markdown deliverables
- checker CLI under `scripts/maintenance/check_markdown_bilingual_structure.py`

Compatibility notes:

The checker change is additive rather than breaking.
The new rule-aligned enforcement is opt-in through `--require-authority-note`, which preserves compatibility with the current repository state and avoids forcing a broad repo-wide doc repair outside this task boundary.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --help
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden\tmp\markdown_rule_strict_smoke --require-authority-note
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden\tmp\markdown_rule_negative_smoke --require-authority-note
rg -n "Markdown|bilingual|Chinese summary first|English remains the authoritative|英文全文在后|中文摘要在前|Markdown deliverables" E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md E:\Warden\docs\templates\TASK_TEMPLATE.md E:\Warden\docs\templates\HANDOFF_TEMPLATE.md
git status --short -- "docs/workflow/GPT_CODEX_WORKFLOW.md" "docs/templates/TASK_TEMPLATE.md" "docs/templates/HANDOFF_TEMPLATE.md" "scripts/maintenance/check_markdown_bilingual_structure.py" "docs/tasks/2026-03-27_markdown_rule_sync_and_checker_enforcement.md" "docs/handoff/2026-03-27_markdown_rule_sync_and_checker_enforcement.md"
```

### Result

- `py_compile` passed for the checker.
- `--help` shows the new additive flag `--require-authority-note`.
- Default repo-wide checker run passed with `87 / 87` files passing and `0` failures.
- Strict-mode smoke on copies of the updated workflow/template docs passed with `3 / 3` files passing.
- Strict-mode negative smoke on a bad sample failed as expected and reported:
  - `missing_cn_authority_note`
  - `missing_en_authority_note`
- `rg` confirmed the new Markdown rule wording is present in the workflow and both templates.

### Not Run

- repository-wide strict-mode repair pass
- CI integration
- automatic doc backfill for historical files outside scope

Reason:

The task scope was limited to synchronizing contracts and adding a checker rule, not repairing the entire historical document set.
A temporary repo-wide strict-mode run was evaluated during implementation and would have failed on many pre-existing files outside scope, so the new rule was kept opt-in for backward compatibility.

---

## 7. Risks / Caveats

- The new authority-note check is not enabled by default, so future operators must opt into strict mode if they want this stronger rule enforced.
- Historical repository docs still contain many files that would fail the strict authority-note rule; this task intentionally did not repair them.
- The checker script was edited under Windows shell encoding constraints, so future edits should keep using UTF-8-safe tooling or ASCII-only source patterns to avoid accidental corruption.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`
- `E:\Warden\docs\tasks\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`
- `E:\Warden\docs\handoff\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`

Doc debt still remaining:

- many historical Markdown docs still lack the strict authority-note structure and would need a separate scoped repair pass if strict enforcement should become the default
- no workflow/template text currently instructs operators when exactly to use `--require-authority-note`; that can be added later if desired

---

## 9. Recommended Next Step

- If you want strict enforcement repo-wide, open a separate scoped task to backfill the authority-note structure across historical Markdown docs first.
- After that repair pass, consider flipping `--require-authority-note` into the default checker behavior in another small task.
- Until then, use the default checker for backward-compatible maintenance scans and use strict mode when validating new or newly normalized Markdown documents.
