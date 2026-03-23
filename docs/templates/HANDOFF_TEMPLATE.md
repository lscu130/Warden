# HANDOFF_TEMPLATE.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# HANDOFF_TEMPLATE.md

# Handoff Metadata

- Handoff ID: {{HANDOFF_ID}}
- Related Task ID: {{TASK_ID}}
- Task Title: {{TASK_TITLE}}
- Module: {{MODULE_NAME}}
- Author: {{AUTHOR}}
- Date: {{DATE}}
- Status: {{DONE / PARTIAL / BLOCKED}}

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

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
- {{DOC_CHANGE_3}}

### Output / Artifact Changes

- {{ARTIFACT_CHANGE_1}}
- {{ARTIFACT_CHANGE_2}}
- {{ARTIFACT_CHANGE_3}}

If nothing changed in one category, say `none`.

---

## 3. Files Touched

List only files actually touched.

- {{FILE_1}}
- {{FILE_2}}
- {{FILE_3}}

Optional notes per file:

- {{FILE_NOTE_1}}
- {{FILE_NOTE_2}}
- {{FILE_NOTE_3}}

---

## 4. Behavior Impact

Describe what behavior is now different.

### Expected New Behavior

- {{NEW_BEHAVIOR_1}}
- {{NEW_BEHAVIOR_2}}
- {{NEW_BEHAVIOR_3}}

### Preserved Behavior

- {{PRESERVED_BEHAVIOR_1}}
- {{PRESERVED_BEHAVIOR_2}}
- {{PRESERVED_BEHAVIOR_3}}

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
- {{FIELD_OR_INTERFACE_3}}

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
```

### Result

- {{RESULT_1}}
- {{RESULT_2}}
- {{RESULT_3}}

### Not Run

- {{NOT_RUN_1}}
- {{NOT_RUN_2}}
- {{NOT_RUN_3}}

Reason:

{{NOT_RUN_REASON}}

---

## 7. Risks / Caveats

- {{RISK_1}}
- {{RISK_2}}
- {{RISK_3}}

If there are no meaningful risks, say `none`.

---

## 8. Docs Impact

- Docs updated: {{YES / NO / NEEDED}}

Docs touched:

- {{DOC_TOUCHED_1}}
- {{DOC_TOUCHED_2}}

Doc debt still remaining:

- {{DOC_DEBT_1}}
- {{DOC_DEBT_2}}

If none, say `none`.

---

## 9. Recommended Next Step

- {{NEXT_STEP_1}}
- {{NEXT_STEP_2}}
- {{NEXT_STEP_3}}

If the task is blocked or partial, the first next step should say exactly what is needed to continue.
