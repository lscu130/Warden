# TASK_TEMPLATE.md

# Task Metadata

- Task ID: {{TASK_ID}}
- Task Title: {{TASK_TITLE}}
- Owner Role: {{OWNER_ROLE}}
- Priority: {{PRIORITY}}
- Status: TODO
- Related Module: {{MODULE_NAME}}
- Related Issue / ADR / Doc: {{RELATED_LINKS_OR_DOCS}}
- Created At: {{DATE}}
- Requested By: {{REQUESTED_BY}}

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.

---

## 1. Background

{{BACKGROUND}}

Explain the engineering context briefly and concretely.

Include only relevant context:

- what currently exists
- what problem is happening
- why this task is needed now

Do not paste unrelated project history.

---

## 2. Goal

{{GOAL}}

Write the target outcome in one paragraph.

Good goal characteristics:

- specific
- observable
- bounded
- compatible with current project rules

---

## 3. Scope In

This task is allowed to touch:

- {{FILE_OR_DIR_1}}
- {{FILE_OR_DIR_2}}
- {{FILE_OR_DIR_3}}

This task is allowed to change:

- {{ALLOWED_CHANGE_1}}
- {{ALLOWED_CHANGE_2}}
- {{ALLOWED_CHANGE_3}}

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}
- {{OUT_OF_SCOPE_3}}

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- {{DOC_1}}
- {{DOC_2}}
- {{DOC_3}}

### Code / Scripts

- {{SCRIPT_1}}
- {{SCRIPT_2}}
- {{SCRIPT_3}}

### Data / Artifacts

- {{DATA_1}}
- {{DATA_2}}
- {{DATA_3}}

### Prior Handoff

- {{HANDOFF_DOC}}

### Missing Inputs

- {{MISSING_INPUT_1}}
- {{MISSING_INPUT_2}}

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- {{OUTPUT_1}}
- {{OUTPUT_2}}
- {{OUTPUT_3}}

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

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}
- {{CONSTRAINT_3}}

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- {{INTERFACE_1}}
- {{INTERFACE_2}}
- {{INTERFACE_3}}

Schema / field constraints:

- Schema changed allowed: {{YES_OR_NO}}
- If yes, required compatibility plan: {{PLAN}}
- Frozen field names involved: {{FIELD_LIST}}

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - {{CMD_1}}
  - {{CMD_2}}
  - {{CMD_3}}

Downstream consumers to watch:

- {{DOWNSTREAM_1}}
- {{DOWNSTREAM_2}}

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

- {{EXEC_NOTE_1}}
- {{EXEC_NOTE_2}}
- {{EXEC_NOTE_3}}

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

- [ ] {{ACCEPTANCE_1}}
- [ ] {{ACCEPTANCE_2}}
- [ ] {{ACCEPTANCE_3}}

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
{{VALIDATION_COMMAND_1}}
{{VALIDATION_COMMAND_2}}
{{VALIDATION_COMMAND_3}}
```

Expected evidence to capture:

- {{VALIDATION_EVIDENCE_1}}
- {{VALIDATION_EVIDENCE_2}}

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

- {{HANDOFF_OUTPUT_PATH}}

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- {{OPEN_QUESTION_1}}
- {{OPEN_QUESTION_2}}
- {{BLOCKER_1}}

If none, write `none`.
