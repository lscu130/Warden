# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“中文长文档逐段英译增强”任务的正式任务单。
- 若中英文存在冲突，以英文版为准。

## English Version

# Task Metadata

- Task ID: 2026-03-23-chinese-longform-english-expansion
- Task Title: Expand English sections for long Chinese-origin documentation
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: project-documentation
- Related Issue / ADR / Doc: AGENTS.md; docs/workflow/GPT_CODEX_WORKFLOW.md; docs/tasks/2026-03-23_markdown_bilingualization.md; docs/handoff/2026-03-23_markdown_bilingualization.md
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

The previous Markdown bilingualization task converted most repository Markdown files into a Chinese-first / English-second structure and added English-authoritative notes for AI agents.
However, several long Chinese-origin documents still expose only a high-level English summary followed by preserved Chinese source text.
The user now wants deeper English coverage for those long Chinese-origin docs so the English section is more useful for AI and English-first readers.

---

## 2. Goal

Expand the English sections of the identified long Chinese-origin documentation files from summary-only coverage into fuller section-by-section or near-section-by-section English content, while preserving the original Chinese source body and keeping all technical meanings, contracts, frozen fields, workflow rules, and historical semantics unchanged.

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

- English documentation content before the preserved Chinese source sections
- section headings and structure inside the English version to mirror the Chinese document more closely
- wording needed to clarify existing rules and contracts in English without changing meaning

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify non-Markdown files
- rewrite or paraphrase the preserved Chinese source bodies
- change code behavior, schema, labels, CLI, or output contracts

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
- `E:\Warden\docs\tasks\2026-03-23_markdown_bilingualization.md`

### Code / Scripts

- none
- none
- none

### Data / Artifacts

- the current bilingualized versions of the seven scoped Markdown files
- `E:\Warden\docs\handoff\2026-03-23_markdown_bilingualization.md`
- current repository worktree state

### Prior Handoff

- `E:\Warden\docs\handoff\2026-03-23_markdown_bilingualization.md`

### Missing Inputs

- none
- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- fuller English sections for the scoped long Chinese-origin documents
- preserved Chinese source sections left intact below the expanded English content
- a repo handoff document summarizing the English-expansion work

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

- English content must remain the authoritative AI-facing version.
- The preserved Chinese source sections must stay in place and keep their meaning intact.
- Expanded English text must not invent requirements, fields, labels, or workflow rules that are not already supported by the existing documents.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- documented schema field names
- documented CLI examples
- documented workflow stage ordering

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: documented dataset, label, workflow, and output field names referenced by the scoped docs

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - all command snippets already documented in the scoped files
  - existing documented file names
  - existing documented field names

Downstream consumers to watch:

- AI agents relying on the English sections
- human readers relying on the preserved Chinese originals

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

- Expand the English version by mirroring major Chinese sections where the current English is only a summary.
- Keep the Chinese source under the English section as the preserved original reference.
- Prefer concise but complete English prose over excessive line-by-line duplication when one English section can safely cover one Chinese section.

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

- [ ] Each scoped file now contains substantially fuller English coverage than a short summary
- [ ] The preserved Chinese source sections are still present
- [ ] No workflow, schema, or label semantics were changed

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
rg -n "## English Version|Original Chinese Source|## 1\\.|## 2\\." README.md docs/workflow/GPT_CODEX_WORKFLOW.md docs/data/TRAINSET_V1.md docs/data/TRAIN_LABEL_DERIVATION_V1.md docs/data/GATA_EVASION_AUXILIARY_SET_V1.md docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md STRUCTION.md
Get-Content -Raw <spot-check-file>
git diff -- <scoped-files>
```

Expected evidence to capture:

- English sections in scoped files are materially expanded
- Chinese source sections remain present and intact

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

- `E:\Warden\docs\handoff\2026-03-23_chinese_longform_english_expansion.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- Whether “逐段英译增强” requires strict one-to-one section mirroring or fuller English coverage that closely follows the original structure; default interpretation for this task is fuller near-section-by-section English coverage.
- `docs/STRUCTION.md` remains outside scope because it was previously blocked for writes and the user already accepted that as non-blocking.
- none

If none, write `none`.
