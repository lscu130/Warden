# Handoff Metadata

- Handoff ID: HANDOFF-2026-03-20-TEMPLATE-NORMALIZATION
- Related Task ID: TASK-2026-03-20-TEMPLATE-NORMALIZATION
- Task Title: Normalize TASK_TEMPLATE and HANDOFF_TEMPLATE into complete executable templates
- Module: workflow / templates / project-governance
- Author: Codex
- Date: 2026-03-20
- Status: DONE

---

## 1. Executive Summary

Completed the normalization of the repository task and handoff templates.
The task template is now a complete execution contract, and the handoff template is now a complete delivery template instead of a truncated fragment.
Current completion state: done.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Rewrote `docs/templates/TASK_TEMPLATE.md` into a complete, directly fillable execution template.
- Rewrote `docs/templates/HANDOFF_TEMPLATE.md` into a complete, directly fillable handoff template.
- Added a formal task document for this template-normalization work.

### Output / Artifact Changes

- Added `docs/handoff/2026-03-20_template_normalization.md`.

---

## 3. Files Touched

- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-20_template_normalization_task.md`
- `docs/handoff/2026-03-20_template_normalization.md`

Optional notes per file:

- `docs/templates/HANDOFF_TEMPLATE.md`: removed wrapper/truncation and restored complete structure.
- `docs/templates/TASK_TEMPLATE.md`: expanded to cover missing-input handling, handoff requirements, and blocker tracking.

---

## 4. Behavior Impact

### Expected New Behavior

- Future non-trivial tasks can be framed with a complete repo-native task template.
- Future non-trivial deliveries can be documented with a complete repo-native handoff template.
- Threads following `AGENTS.md` now have complete template artifacts to comply with.

### Preserved Behavior

- No runtime code, CLI, dataset schema, or model behavior was changed.
- Existing governance direction from `AGENTS.md` and `GPT_CODEX_WORKFLOW.md` remains intact.

### User-facing / CLI Impact

- none

### Output Format Impact

- No runtime output format changed.
- Governance-template output expectations are now more complete and explicit.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- repository task-template contract
- repository handoff-template contract

Compatibility notes:

This change affects project-process documentation only.
The practical effect is stronger template completeness for future threads, not runtime interface change.

---

## 6. Validation Performed

### Commands Run

```bash
Get-Content -Path 'E:\Warden\docs\templates\TASK_TEMPLATE.md'
Get-Content -Path 'E:\Warden\docs\templates\HANDOFF_TEMPLATE.md'
rg -n "Task Metadata|Validation Checklist|Handoff Requirements" 'E:\Warden\docs\templates\TASK_TEMPLATE.md'
rg -n "Handoff Metadata|Validation Performed|Recommended Next Step" 'E:\Warden\docs\templates\HANDOFF_TEMPLATE.md'
```

### Result

- both templates are present as complete markdown files
- required task-template sections are present
- required handoff-template sections are present

### Not Run

- syntax / import checks
- runtime smoke tests
- CLI validation

Reason:

This was a documentation-only governance task with no executable code changes.

---

## 7. Risks / Caveats

- The templates are stricter than before, so future ad-hoc work may need more explicit framing.
- Existing older task docs in the repository may still use lighter structure until they are refreshed.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Doc debt still remaining:

- example task and handoff docs could still be added as canonical “golden examples”

---

## 9. Recommended Next Step

- add one canonical filled example based on `TASK_TEMPLATE.md`
- add one canonical filled example based on `HANDOFF_TEMPLATE.md`
- optionally normalize older repo tasks to the new template structure when they are next touched
