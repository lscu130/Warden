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

- Task ID: 2026-03-23-markdown-bilingualization
- Task Title: Convert repository Markdown documents to bilingual Chinese-first / English-second format
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: project-documentation
- Related Issue / ADR / Doc: AGENTS.md; docs/workflow/GPT_CODEX_WORKFLOW.md; docs/templates/TASK_TEMPLATE.md; docs/templates/HANDOFF_TEMPLATE.md
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

The user requested that every Markdown document in the repository be rewritten as a bilingual document with Chinese content first and English content second.
This is a non-trivial documentation-wide change because it touches many files across governance docs, templates, module specs, data docs, archived task docs, archived handoff docs, and one generated Markdown report.
The current repo also contains several Markdown files with mojibake-corrupted Chinese text, so this task must restore readable content rather than simply wrap the existing text.

---

## 2. Goal

Rewrite all repository Markdown files into a consistent bilingual format where the Chinese version appears before the English version, while preserving the original English meaning and keeping English as the authoritative version for AI agents such as GPT, Gemini, Codex, Grok, and Claude.
Historical task, handoff, and report documents must keep their factual content intact; this task may improve readability and bilingual presentation, but must not silently change the recorded decisions, outcomes, or evidence.

---

## 3. Scope In

This task is allowed to touch:

- repository root Markdown files
- `docs/**/*.md`
- `data/**/*.md`

This task is allowed to change:

- Markdown wording, structure, headings, and section layout to provide bilingual Chinese and English content
- corrupted Markdown text that must be rewritten into readable Chinese and English
- documentation-only notes clarifying that English is the AI-authoritative version

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify non-Markdown files
- change runtime code, schema, CLI behavior, or output-producing logic
- change the factual meaning of historical task docs, handoff docs, or generated report results

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`

### Code / Scripts

- none
- none
- none

### Data / Artifacts

- all repository `*.md` files returned by `rg --files -g '*.md'`
- `E:\Warden\PROJECT.md` as an existing but empty file
- `C:\Users\20516\Downloads\GPT_CODEX_WORKFLOW.md` as a referenced external copy with the same corrupted content as the repo workflow file

### Prior Handoff

- `E:\Warden\docs\handoff\2026-03-20_agents_workflow_contract_strengthening.md`

### Missing Inputs

- none
- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- bilingual Chinese-first / English-second content for every repository Markdown file
- explicit English-authoritative note for AI-facing interpretation where relevant
- a repo handoff document summarizing the documentation-wide change

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Chinese content must appear before the English content in each Markdown file.
- English wording must remain present and readable because it is the authoritative AI-facing version.
- Historical records must preserve facts, dates, status, commands, validation claims, and compatibility statements.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- repository file paths
- documented schema field names
- documented CLI names and command examples

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: documented manifest, metadata, label, and CLI names referenced in Markdown

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - all command snippets already documented in Markdown files
  - existing documented file paths
  - existing documented schema keys

Downstream consumers to watch:

- human readers using Chinese documentation
- AI agents instructed to rely on English documentation

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- Start with governance and template files because they define interpretation rules for the rest of the repo.
- Reconstruct mojibake-corrupted files into readable bilingual text rather than preserving corrupted strings.
- Keep historical task and handoff content semantically identical even when rewriting their presentation.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] Every repository `.md` file now contains Chinese-first / English-second content or equivalent bilingual structure
- [ ] AI-facing governance docs explicitly state that English is the authoritative version for AI agents
- [ ] No historical task, handoff, or report file silently changes its factual claims

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
rg --files -g '*.md'
rg -n "^## English Version$|^## 英文版$|AI-authoritative|English is the authoritative version" -g '*.md'
Get-Content -Raw <spot-check-file>
```

Expected evidence to capture:

- all Markdown files remain present and readable
- spot checks confirm Chinese appears before English and English-authoritative notes exist where required

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

- `E:\Warden\docs\handoff\2026-03-23_markdown_bilingualization.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- Whether generated report Markdown should remain machine-oriented after bilingualization; default interpretation for this task is yes, while preserving the recorded result.
- Whether every file needs a full translation versus a bilingual wrapper; default interpretation for this task is full bilingual content wherever practical.
- none

If none, write `none`.
