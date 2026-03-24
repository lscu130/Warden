# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-03-20-TEMPLATE-NORMALIZATION
- Task Title: Normalize TASK_TEMPLATE and HANDOFF_TEMPLATE into complete executable templates
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: workflow / templates / project-governance
- Related Issue / ADR / Doc: `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`
- Created At: 2026-03-20
- Requested By: user

---

## 1. Background

The repository now treats `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, and `docs/templates/HANDOFF_TEMPLATE.md` as mandatory project-governance files.
However, the current `HANDOFF_TEMPLATE.md` is truncated and the current `TASK_TEMPLATE.md` is incomplete as an execution contract.
This task is needed so future threads can use complete, repo-native templates instead of relying on ad-hoc structure.

---

## 2. Goal

Produce complete, directly usable task and handoff templates that match Warden's workflow rules, reflect actual repository usage, and can be filled in without ambiguity for future non-trivial tasks.

---

## 3. Scope In

This task is allowed to touch:

- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-20_template_normalization_task.md`
- `docs/handoff/2026-03-20_template_normalization.md`

This task is allowed to change:

- template structure
- template section completeness
- template guidance text

---

## 4. Scope Out

This task must NOT do the following:

- change runtime code or data-processing behavior
- weaken `AGENTS.md` governance rules
- invent new product schema semantics

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- none

### Data / Artifacts

- `docs/handoff/2026-03-18_repo_alignment_smoke_freeze.md`
- `docs/handoff/2026-03-18_aux_set_linkage_interface.md`

### Prior Handoff

- `docs/handoff/2026-03-20_agents_workflow_contract_strengthening.md`

### Missing Inputs

- none

---

## 6. Required Outputs

- completed `docs/templates/TASK_TEMPLATE.md`
- completed `docs/templates/HANDOFF_TEMPLATE.md`
- repo handoff for this normalization task

---

## 7. Hard Constraints

- Preserve backward compatibility unless explicitly waived.
- Do not silently change output format expectations for runtime artifacts.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Keep template wording concrete and executable.

Task-specific constraints:

- the templates must stay markdown-only
- the templates must be usable directly in the repository without external context
- the handoff template must cover actual repository handoff usage

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- repository governance expectations

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none

Downstream consumers to watch:

- future Warden engineering threads
- future repo task docs and handoff docs

---

## 9. Suggested Execution Plan

1. Read current templates and real handoff examples.
2. Identify missing sections and truncation points.
3. Rewrite both templates into complete executable forms.
4. Create a handoff for this template normalization task.
5. Validate by reading the resulting files and checking required sections.

Task-specific execution notes:

- keep wording strict rather than inspirational
- align with actual handoff structure already used in repo
- avoid introducing process contradictions with `AGENTS.md`

---

## 10. Acceptance Criteria

- [ ] `TASK_TEMPLATE.md` is complete and directly fillable
- [ ] `HANDOFF_TEMPLATE.md` is complete and directly fillable
- [ ] No runtime code or schema behavior was changed
- [ ] Template guidance matches current workflow rules
- [ ] A repo handoff is added for this task

Task-specific acceptance checks:

- [ ] `HANDOFF_TEMPLATE.md` is no longer truncated
- [ ] `TASK_TEMPLATE.md` explicitly covers inputs, validation, and handoff requirements
- [ ] the templates can be understood without external wrapper text

---

## 11. Validation Checklist

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
Get-Content -Path 'E:\Warden\docs\templates\TASK_TEMPLATE.md'
Get-Content -Path 'E:\Warden\docs\templates\HANDOFF_TEMPLATE.md'
rg -n "Task Metadata|Validation Checklist|Handoff Requirements" 'E:\Warden\docs\templates\TASK_TEMPLATE.md'
rg -n "Handoff Metadata|Validation Performed|Recommended Next Step" 'E:\Warden\docs\templates\HANDOFF_TEMPLATE.md'
```

Expected evidence to capture:

- both templates render as complete markdown files
- required sections are present

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- what changed
- behavior impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-03-20_template_normalization.md`

---

## 13. Open Questions / Blocking Issues

- none