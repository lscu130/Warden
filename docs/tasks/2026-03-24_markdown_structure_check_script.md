# 2026-03-24_markdown_structure_check_script

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“Markdown 结构检查脚本”任务的正式任务单。
- 若中英文存在冲突，以英文版为准。

### 摘要

- 任务 ID：WARDEN-MARKDOWN-STRUCTURE-CHECK-V1
- 任务主题：新增一个仓库内 Markdown 双语结构检查脚本
- 当前状态：DONE
- 相关模块：documentation maintenance

### 当前任务要点

- 目标是做只读检查，不做自动修复。
- 检查范围针对业务 Markdown，重点抓双语分区缺失、中文乱码标题、中文占位符残留和中文摘要过薄。
- 输出应适合日常手工运行，也适合后续接到更自动化的检查流程里。

## English Version

# Task Metadata

- Task ID: WARDEN-MARKDOWN-STRUCTURE-CHECK-V1
- Task Title: Add a repository-local Markdown bilingual-structure checking script
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: documentation maintenance
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. Background

The previous Markdown Chinese-summary repair pass closed with a clear follow-up: add a lightweight local checker that can catch broken bilingual structure before future doc maintenance drifts again.

The current repo has no dedicated script that validates:

- the presence of both `## 中文版` and `## English Version`
- Chinese-side garbled headings such as `## ???`
- unresolved template placeholders inside the Chinese section
- obviously too-thin Chinese summary blocks

Without a dedicated check, these issues are likely to reappear during future batch edits.

---

## 2. Goal

Add one repository-local Python script that scans the scoped business Markdown set and reports bilingual-structure issues in a deterministic, machine-readable, and operator-friendly way.

The script must be read-only and must not modify documents.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/maintenance/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- a new Markdown-structure checker script
- task tracking documentation
- delivery handoff documentation

---

## 4. Scope Out

This task must NOT do the following:

- auto-fix Markdown files
- rewrite existing docs
- change Python/script behavior outside the new checker
- introduce third-party dependencies

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`

### Code / Scripts

- existing repo Python script style under `scripts/data/`

### Data / Artifacts

- current repository Markdown files

### Prior Handoff

- `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a new Python checker under `scripts/maintenance/`
- a CLI that can scan the repo and return non-zero on violations
- optional JSON report output for later automation
- a task document and handoff document for this delivery

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format of existing scripts.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- The new script must be read-only.
- The checker must evaluate Chinese-section issues separately from the English section.
- Default exclusions must cover `data/processed/**`, `docs/STRUCTION.md`, and `STRUCTION.md`.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing repo scripts
- existing Markdown docs

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\data\build_manifest.py --help`
  - `python E:\Warden\scripts\data\check_dataset_consistency.py --help`
  - `python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help`

Downstream consumers to watch:

- human operators running repo maintenance checks
- any future automation that consumes a JSON report from the checker

---

## 9. Suggested Execution Plan

Recommended order:

1. Inspect existing script style and choose a minimal CLI shape.
2. Implement Markdown discovery with default exclusions.
3. Implement Chinese-section checks for structure, garbling, placeholders, and substantive-summary heuristics.
4. Add human-readable stdout summary and optional JSON report output.
5. Run the checker on the current repo and validate pass/fail behavior.
6. Prepare handoff.

Task-specific execution notes:

- Keep issue codes explicit and stable.
- Prefer deterministic heuristics over loose fuzzy scoring.
- Make the default run useful from the repo root with no extra arguments.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] The checker detects missing bilingual-section markers
- [x] The checker detects placeholder variables inside the Chinese section
- [x] The checker exits successfully on the currently repaired repo state

---

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted smoke test
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

```bash
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --help
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden
python -m py_compile E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py
```

Expected evidence to capture:

- repo summary counts from the checker
- zero-violation run on the current repaired repo state

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-03-24_markdown_structure_check_script.md`

---

## 13. Open Questions / Blocking Issues

- none
