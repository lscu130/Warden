# HANDOFF_TEMPLATE.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Warden 的标准交接模板。
- 涉及交接字段、状态、验证、兼容性、证据规则、运行参数和停止条件时，以英文版为准。
- 本模板本身就是 Markdown 交付物，默认按双语结构书写：中文摘要在前，英文全文在后，英文仍为权威版本。

## 1. 模板用途

该模板用于把一次非 trivial 交付压缩成可复盘、可续做、可审计的 handoff。
新版模板按 GPT-5.5 的提示词思路增加了：实际采用的模型/agent 参数、证据/检索情况、验证情况、停止条件和未完成边界。
重点不是写感想，而是写清楚：改了什么、影响什么、验证了什么、证据够不够、何时停止、还缺什么。

## 2. 填写重点

- 只能写实际发生的事实，不能把计划当成结果。
- 验证未跑就必须明确写未跑和原因。
- 若接口、schema、CLI 或输出受影响，必须写兼容性结论。
- 若使用了搜索、文件读取、工具调用或 agent 流程，必须写清证据范围、反审结果和停止条件。
- 若使用 GPT-5.5 / Codex / API agent，建议记录 reasoning effort、verbosity、preamble、工具链和结构化输出方式。

## 3. 中文阅读建议

优先看英文版的 `Behavior Impact`、`Schema / Interface Impact`、`Evidence / Retrieval Performed`、`Counter-Review Performed`、`Validation Performed`、`Stop Condition` 和 `Risks / Caveats`。

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
- Keep claims auditable against diffs, commands, current files, cited sources, or tool outputs.
- Distinguish source-backed facts from assumptions, recommendations, risks, and planned follow-up work.
- Write this Markdown handoff in bilingual form by default: Chinese summary first, full English version second, with English authoritative for exact facts, commands, validation, and compatibility statements.

---

## 1. Executive Summary

{{EXECUTIVE_SUMMARY}}

State in plain language:

- what was changed
- why it was changed
- current completion state
- whether the task reached its defined stop condition

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

## 6. Evidence / Retrieval Performed

Use this section when the task depended on search, repository inspection, external sources, uploaded files, internal docs, meetings, emails, tickets, papers, or other evidence. If it does not apply, write `not applicable`.

Evidence sources actually checked:

- {{EVIDENCE_SOURCE_CHECKED_1}}
- {{EVIDENCE_SOURCE_CHECKED_2}}
- {{EVIDENCE_SOURCE_CHECKED_3}}

Retrieval / reading performed:

- {{RETRIEVAL_OR_READING_1}}
- {{RETRIEVAL_OR_READING_2}}
- {{RETRIEVAL_OR_READING_3}}

Claims supported by evidence:

- {{SUPPORTED_CLAIM_1}}
- {{SUPPORTED_CLAIM_2}}

Claims left unsupported or assumed:

- {{UNSUPPORTED_OR_ASSUMED_CLAIM_1}}
- {{UNSUPPORTED_OR_ASSUMED_CLAIM_2}}

Retrieval stopped because:

- {{RETRIEVAL_STOP_REASON}}

Rules:

- Do not state that a file, source, or command was checked unless it was actually checked.
- Do not turn missing evidence into a factual negative claim.
- If evidence is insufficient, mark the handoff as `PARTIAL` or list the remaining gap.

---


## 6.1 Counter-Review Performed

Use this section when the task required counter-review.
If not applicable, write `not applicable` and briefly state why.

Original framing reviewed:

{{ORIGINAL_FRAMING}}

Assumptions checked:

- {{ASSUMPTION_CHECK_1}}
- {{ASSUMPTION_CHECK_2}}
- {{ASSUMPTION_CHECK_3}}

Failure modes considered:

- {{FAILURE_MODE_CHECK_1}}
- {{FAILURE_MODE_CHECK_2}}
- {{FAILURE_MODE_CHECK_3}}

Counterexamples or contradictory evidence found:

- {{COUNTEREVIDENCE_1}}
- {{COUNTEREVIDENCE_2}}
- {{COUNTEREVIDENCE_3}}

Alternative routes considered:

- {{ALTERNATIVE_CONSIDERED_1}}
- {{ALTERNATIVE_CONSIDERED_2}}
- {{ALTERNATIVE_CONSIDERED_3}}

Framing changed: {{YES / NO / PARTIAL}}

If changed, what changed:

{{FRAMING_CHANGE_SUMMARY}}

Claims left unsupported or assumed after counter-review:

- {{COUNTER_REVIEW_UNSUPPORTED_OR_ASSUMED_1}}
- {{COUNTER_REVIEW_UNSUPPORTED_OR_ASSUMED_2}}

Residual risks after counter-review:

- {{COUNTER_REVIEW_RESIDUAL_RISK_1}}
- {{COUNTER_REVIEW_RESIDUAL_RISK_2}}

Decision after counter-review:

- {{ACCEPT_ORIGINAL / REVISE_FRAMING / KEEP_EXPLORATORY / ESCALATE / BLOCK}}

Rules:

- Do not claim counter-review happened unless assumptions, failure modes, evidence gaps, or alternatives were actually checked.
- Do not rewrite planned counter-review as completed counter-review.
- If counter-review was required but not performed, mark the handoff as `PARTIAL` or `BLOCKED` and state the reason.


## 6.2 Karpathy Guardrail Check

Use this section when the task involved repository edits, code changes, workflow changes, documentation contract changes, or any non-trivial delivery.
If not applicable, write `not applicable` and briefly state why.

### Think Before Acting

Assumptions surfaced before or during execution:

- {{ASSUMPTION_SURFACED_1}}
- {{ASSUMPTION_SURFACED_2}}

Ambiguities resolved or escalated:

- {{AMBIGUITY_RESOLUTION_1}}
- {{AMBIGUITY_RESOLUTION_2}}

### Simplicity First

Simplest acceptable route used:

- {{SIMPLE_ROUTE_USED}}

Larger or more speculative routes rejected:

- {{REJECTED_COMPLEX_ROUTE_1}}
- {{REJECTED_COMPLEX_ROUTE_2}}

### Surgical Changes

Touched-file to task-scope mapping:

- {{FILE_TO_SCOPE_MAPPING_1}}
- {{FILE_TO_SCOPE_MAPPING_2}}
- {{FILE_TO_SCOPE_MAPPING_3}}

Adjacent cleanup or formatting-only changes:

- {{ADJACENT_CLEANUP_OR_FORMATTING}}

### Goal-Driven Verification

Verification loop:

- {{GOAL_OR_CRITERION_1}} -> {{VERIFICATION_RESULT_1}}
- {{GOAL_OR_CRITERION_2}} -> {{VERIFICATION_RESULT_2}}
- {{GOAL_OR_CRITERION_3}} -> {{VERIFICATION_RESULT_3}}

Rules:

- Do not claim the guardrails were followed unless the assumptions, simplicity boundary, surgical change boundary, and verification loop were actually checked.
- If a guardrail was not applicable, state why.
- If a guardrail failed or could not be checked, list it under `Risks / Caveats` and mark the handoff `PARTIAL` when it affects acceptance.

---

## 7. Validation Performed

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

### Manual / Artifact Checks

- {{MANUAL_CHECK_1}}
- {{MANUAL_CHECK_2}}
- {{ARTIFACT_CHECK_1}}

### Not Run

- {{NOT_RUN_1}}
- {{NOT_RUN_2}}
- {{NOT_RUN_3}}

Reason:

{{NOT_RUN_REASON}}

Next best check:

{{NEXT_BEST_CHECK}}

---

## 8. Model / Agent Runtime Used

Use this section when GPT-5.5, Codex, Claude Code, or another agent was used materially. If it does not apply, write `not applicable`.

- Executor: {{GPT_WEB / CLAUDE_CODE / CODEX / OTHER}}
- Model or agent: {{MODEL_OR_AGENT}}
- Reasoning effort: {{none / low / medium / high / xhigh / unknown / not applicable}}
- Verbosity: {{low / medium / high / unknown / not applicable}}
- Preamble used before tool-heavy work: {{YES / NO / NOT_APPLICABLE}}
- Progress updates provided: {{YES / NO / NOT_APPLICABLE}}
- Tools used: {{TOOLS_USED}}
- Structured output used: {{YES / NO / NOT_APPLICABLE}}
- Notes on deviations from task guidance: {{RUNTIME_DEVIATIONS}}

---

## 9. Stop Condition

Completion stop condition reached: {{YES / NO / PARTIAL}}

Reason:

{{STOP_CONDITION_REASON}}

Escalation triggered: {{YES / NO}}

If yes, escalation reason:

{{ESCALATION_REASON}}

Remaining blockers:

- {{REMAINING_BLOCKER_1}}
- {{REMAINING_BLOCKER_2}}

---

## 10. Risks / Caveats

- {{RISK_1}}
- {{RISK_2}}
- {{RISK_3}}
- Counter-review residual risk: {{COUNTER_REVIEW_RESIDUAL_RISK}}
- Karpathy guardrail residual risk: {{KARPATHY_GUARDRAIL_RESIDUAL_RISK}}

If there are no meaningful risks, say `none`.

---

## 11. Docs Impact

- Docs updated: {{YES / NO / NEEDED}}

Docs touched:

- {{DOC_TOUCHED_1}}
- {{DOC_TOUCHED_2}}

Doc debt still remaining:

- {{DOC_DEBT_1}}
- {{DOC_DEBT_2}}

If none, say `none`.

---

## 12. Recommended Next Step

- {{NEXT_STEP_1}}
- {{NEXT_STEP_2}}
- {{NEXT_STEP_3}}

If the task is blocked or partial, the first next step should say exactly what is needed to continue.
