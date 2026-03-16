
---

## 3) `HANDOFF_TEMPLATE.md`

```md
# HANDOFF_TEMPLATE.md

# Handoff Metadata

- Handoff ID: {{HANDOFF_ID}}
- Related Task ID: {{TASK_ID}}
- Task Title: {{TASK_TITLE}}
- Module: {{MODULE_NAME}}
- Author: {{AUTHOR}}
- Date: {{DATE}}
- Status: {{DONE / PARTIAL / BLOCKED}}

---

## 1. Executive Summary

{{EXECUTIVE_SUMMARY}}

State in plain language:
- what was changed
- why it was changed
- current completion state

Keep this short and concrete.

---

## 2. What Changed

Describe the actual changes.

### Code Changes
- {{CODE_CHANGE_1}}
- {{CODE_CHANGE_2}}
- {{CODE_CHANGE_3}}

### Doc Changes
- {{DOC_CHANGE_1}}
- {{DOC_CHANGE_2}}

### Output / Artifact Changes
- {{ARTIFACT_CHANGE_1}}
- {{ARTIFACT_CHANGE_2}}

If nothing changed in one category, say "none".

---

## 3. Files Touched

List only files actually touched.

- {{FILE_1}}
- {{FILE_2}}
- {{FILE_3}}

Optional notes per file:

- {{FILE_NOTE_1}}
- {{FILE_NOTE_2}}

---

## 4. Behavior Impact

Describe what behavior is now different.

### Expected New Behavior
- {{NEW_BEHAVIOR_1}}
- {{NEW_BEHAVIOR_2}}

### Preserved Behavior
- {{PRESERVED_BEHAVIOR_1}}
- {{PRESERVED_BEHAVIOR_2}}

### User-facing / CLI Impact
- {{CLI_IMPACT}}

### Output Format Impact
- {{OUTPUT_IMPACT}}

Do not hand-wave here.
If behavior did not change, say so explicitly.

---

## 5. Schema / Interface Impact

- Schema changed: {{YES / NO}}
- Backward compatible: {{YES / NO / PARTIAL}}
- Public interface changed: {{YES / NO}}
- Existing CLI still valid: {{YES / NO / PARTIAL}}

Affected schema fields / interfaces:

- {{FIELD_OR_INTERFACE_1}}
- {{FIELD_OR_INTERFACE_2}}

Compatibility notes:

{{COMPATIBILITY_NOTES}}

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

List what was actually checked.

### Commands Run

```bash
{{COMMAND_1}}
{{COMMAND_2}}
{{COMMAND_3}}