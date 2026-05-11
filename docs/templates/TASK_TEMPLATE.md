# TASK_TEMPLATE.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Warden 的标准任务单模板。
- 涉及模板字段、必填项、验收字段、运行参数和停止规则时，以英文版为准。
- 若任务产出包含 Markdown 文档，默认按双语交付：中文摘要在前，英文全文在后，英文仍为权威版本。

## 1. 模板用途

该模板用于把非 trivial 工作冻结成可执行、可审计、可交接的任务定义。
新版模板按 GPT-5.5 的提示词思路调整：优先写清目标、成功标准、证据规则、约束、输出形态、验证方式和停止规则，避免用大量过程步骤替代验收标准。

## 2. 填写重点

- 必须在执行前填写，而不是事后补写。
- `Scope In` 和 `Scope Out` 必须明确。
- `Expected Outcome`、`Success Criteria`、`Evidence / Retrieval Rules`、`Counter-Review Requirements`、`Validation Checklist` 和 `Stop Rules` 是最关键的执行边界。
- `Reasoning Effort` 和 `Verbosity` 只在使用 GPT-5.5 / Codex / API agent 时填写；不用时写 `not applicable`。
- 新增 `Karpathy-Style Execution Guardrails`：把假设/歧义、最小方案、外科手术式改动边界和验证闭环写进任务单，防止执行者过度设计或顺手改无关内容。

## 3. 中文阅读建议

优先查看英文版的模板字段和默认规则，不要根据中文摘要自行发明新字段。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

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
- Karpathy Guardrails Required: {{YES / NO}}

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- Use outcome-first wording: define the expected outcome, success criteria, constraints, evidence rules, validation, and stop rules before describing any preferred process.
- Do not over-specify step-by-step process unless the exact execution path is part of the contract.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.
- If the task will produce Markdown deliverables, define them as bilingual by default: Chinese summary first, full English version second, with English authoritative for exact facts and contract wording.

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

## 3. Expected Outcome And Success Criteria

Expected outcome:

{{EXPECTED_OUTCOME}}

Success criteria:

- {{SUCCESS_CRITERION_1}}
- {{SUCCESS_CRITERION_2}}
- {{SUCCESS_CRITERION_3}}

Notes:

- Success criteria describe what good looks like.
- Do not replace success criteria with a long implementation procedure.
- If the exact procedure matters, put it under `Execution Notes` and explain why it is mandatory.

---

## 4. Scope In

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

## 5. Scope Out

This task must NOT do the following:

- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}
- {{OUT_OF_SCOPE_3}}

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task
- do not change output schemas unless explicitly approved

---

## 6. Inputs

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

## 7. Evidence / Retrieval Rules

Facts or claims that require support:

- {{CLAIM_REQUIRING_SUPPORT_1}}
- {{CLAIM_REQUIRING_SUPPORT_2}}
- {{CLAIM_REQUIRING_SUPPORT_3}}

Allowed evidence sources:

- {{EVIDENCE_SOURCE_1}}
- {{EVIDENCE_SOURCE_2}}
- {{EVIDENCE_SOURCE_3}}

Retrieval budget:

- Initial retrieval: {{INITIAL_RETRIEVAL_SCOPE}}
- Additional retrieval is allowed only when: {{FOLLOW_UP_RETRIEVAL_CONDITION}}
- Stop retrieval when: {{RETRIEVAL_STOP_RULE}}

Missing-evidence behavior:

- {{MISSING_EVIDENCE_BEHAVIOR}}

Rules:

- Do not turn absence of evidence into a factual negative conclusion.
- Do not invent repository state, experiment results, external facts, citations, or validation results.
- If a specific file, URL, paper, issue, ticket, email, meeting, dataset, or artifact is named, read it before making concrete claims about it.


### 7.1 Counter-Review Requirements

Use this section for architecture, labeling, dataset, model, evaluation, workflow, research, governance, or other high-impact tasks.
If not applicable, write `not applicable` and briefly state why.

Current proposed framing:

{{CURRENT_FRAMING}}

Hidden assumptions to check:

- {{ASSUMPTION_1}}
- {{ASSUMPTION_2}}
- {{ASSUMPTION_3}}

Failure modes to consider:

- {{FAILURE_MODE_1}}
- {{FAILURE_MODE_2}}
- {{FAILURE_MODE_3}}

Counterexamples or contradictory cases to search for:

- {{COUNTEREXAMPLE_1}}
- {{COUNTEREXAMPLE_2}}
- {{COUNTEREXAMPLE_3}}

Alternative routes to compare:

- {{ALTERNATIVE_1}}
- {{ALTERNATIVE_2}}
- {{ALTERNATIVE_3}}

Required evidence before accepting the framing:

- {{REQUIRED_EVIDENCE_1}}
- {{REQUIRED_EVIDENCE_2}}
- {{REQUIRED_EVIDENCE_3}}

Decision rule:

- Accept original framing only if: {{ACCEPT_ORIGINAL_RULE}}
- Revise framing if: {{REVISE_RULE}}
- Stop and escalate if: {{ESCALATION_RULE}}

Output discipline:

- Separate `fact`, `inference`, `assumption`, `recommendation`, and `risk`.
- Do not treat a plausible explanation as a verified fact.
- Do not continue into implementation if counter-review changes the task class, scope, schema / interface risk, or acceptance criteria.


### 7.2 Karpathy-Style Execution Guardrails

Use this section for non-trivial tasks, code changes, repository edits, documentation contract changes, workflow changes, and any task where over-engineering or scope drift is a realistic risk.
If not applicable, write `not applicable` and briefly state why.

Assumptions and ambiguity handling:

- Assumptions allowed for this task: {{ALLOWED_ASSUMPTIONS}}
- Ambiguities that require clarification before execution: {{AMBIGUITIES_REQUIRING_CLARIFICATION}}
- Multiple plausible interpretations considered: {{INTERPRETATIONS_CONSIDERED}}
- Chosen interpretation and reason: {{CHOSEN_INTERPRETATION_REASON}}

Simplicity boundary:

- Simplest acceptable solution: {{SIMPLEST_ACCEPTABLE_SOLUTION}}
- Complexity budget: {{COMPLEXITY_BUDGET}}
- Speculative features explicitly forbidden: {{SPECULATIVE_FEATURES_FORBIDDEN}}
- New abstractions / dependencies allowed: {{YES_OR_NO_AND_CONDITIONS}}

Surgical change boundary:

- Every touched file must map to this scope item: {{TOUCHED_FILE_TO_SCOPE_MAPPING_RULE}}
- Adjacent cleanup policy: {{ADJACENT_CLEANUP_POLICY}}
- Formatting-only changes allowed: {{YES_OR_NO_AND_SCOPE}}
- Orphan cleanup allowed only for artifacts made obsolete by this task: {{YES_OR_NO_AND_SCOPE}}

Goal-driven verification loop:

- Goal / criterion 1: {{GOAL_OR_CRITERION_1}} -> verification: {{VERIFY_1}}
- Goal / criterion 2: {{GOAL_OR_CRITERION_2}} -> verification: {{VERIFY_2}}
- Goal / criterion 3: {{GOAL_OR_CRITERION_3}} -> verification: {{VERIFY_3}}

Rules:

- Do not continue into implementation if ambiguity can change scope, schema, labels, routing, acceptance criteria, or downstream compatibility.
- Do not add future-proofing, optional configurability, broad abstractions, or unrelated cleanup unless explicitly listed in `Scope In`.
- Do not touch files that cannot be mapped to a stated scope item.
- Stop when the verification loop is satisfied, blocked, or honestly reported as not run.


---

## 8. Required Outputs

This task should produce:

- {{OUTPUT_1}}
- {{OUTPUT_2}}
- {{OUTPUT_3}}

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- Markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

Output format requirements:

- {{OUTPUT_FORMAT_REQUIREMENT_1}}
- {{OUTPUT_FORMAT_REQUIREMENT_2}}
- {{OUTPUT_FORMAT_REQUIREMENT_3}}

---

## 9. Hard Constraints

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
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.
- Keep stable prompt/context content before task-specific dynamic content when preparing agent prompts.
- Use structured outputs or schema validation outside the prompt when the execution environment supports it.
- Follow the Karpathy-style guardrails: think before acting, simplicity first, surgical changes, and goal-driven verification.

Task-specific constraints:

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}
- {{CONSTRAINT_3}}

---

## 10. Interface / Schema Constraints

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

## 11. Model / Agent Runtime Guidance

Use this section when the task is executed by GPT-5.5, Codex, Claude Code, or another agent. If it does not apply, write `not applicable`.

Target executor:

- {{GPT_WEB / CLAUDE_CODE / CODEX / OTHER}}

Suggested reasoning effort:

- Reasoning effort: {{none / low / medium / high / xhigh / not applicable}}
- Rationale: {{REASONING_EFFORT_RATIONALE}}

Suggested verbosity:

- Verbosity: {{low / medium / high / not applicable}}
- Rationale: {{VERBOSITY_RATIONALE}}

Preamble / progress behavior:

- Preamble required before tool-heavy work: {{YES_OR_NO}}
- Progress updates required: {{YES_OR_NO}}
- Update cadence or trigger: {{UPDATE_CADENCE_OR_TRIGGER}}

Tool-use guidance:

- Tools allowed: {{TOOLS_ALLOWED}}
- Tools forbidden: {{TOOLS_FORBIDDEN}}
- Tool side effects to avoid: {{TOOL_SIDE_EFFECTS_TO_AVOID}}

Structured output guidance:

- Use API structured outputs if available: {{YES_OR_NO_OR_NA}}
- If prompt-only output is required, exact final format: {{PROMPT_ONLY_FINAL_FORMAT}}

Rules:

- Start with `medium` reasoning as the balanced default for GPT-5.5 unless latency or task simplicity justifies `low`.
- Evaluate `low` before using `none` for latency-sensitive work that still needs planning, search, or tool calls.
- Use `high` or `xhigh` only when task complexity or eval results justify extra latency and cost.
- Use lower verbosity for routine status, review, or mechanical edits; use higher verbosity only when the deliverable needs detailed rationale.

---

## 12. Suggested Execution Notes

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Reject speculative abstractions, future-proofing, or adjacent cleanup unless the task explicitly requires them.
5. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- {{EXEC_NOTE_1}}
- {{EXEC_NOTE_2}}
- {{EXEC_NOTE_3}}

Do not treat this section as a license to over-specify the solution path. Add process constraints only when the path is required for correctness, reproducibility, or safety.

---

## 13. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Expected outcome and success criteria are satisfied
- [ ] Scope-out items were not touched
- [ ] Karpathy-style guardrails were followed or explicitly marked not applicable
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Evidence rules were followed, or missing evidence was explicitly stated
- [ ] Counter-review requirements were satisfied or explicitly marked not applicable
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Stop rules were satisfied
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] {{ACCEPTANCE_1}}
- [ ] {{ACCEPTANCE_2}}
- [ ] {{ACCEPTANCE_3}}

---

## 14. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted unit test, if behavior changed and tests exist
- [ ] targeted smoke test
- [ ] type check / lint check, if applicable
- [ ] build check, if applicable
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check
- [ ] changed-file / changed-line scope trace spot-check

Commands to run if applicable:

```bash
{{VALIDATION_COMMAND_1}}
{{VALIDATION_COMMAND_2}}
{{VALIDATION_COMMAND_3}}
```

Expected evidence to capture:

- {{VALIDATION_EVIDENCE_1}}
- {{VALIDATION_EVIDENCE_2}}

If validation cannot be run:

- Not run: {{VALIDATION_NOT_RUN}}
- Reason: {{VALIDATION_NOT_RUN_REASON}}
- Next best check: {{NEXT_BEST_VALIDATION_CHECK}}

---

## 15. Stop Rules

The executor should stop and report completion when all of the following are true:

- {{COMPLETION_STOP_RULE_1}}
- {{COMPLETION_STOP_RULE_2}}
- {{COMPLETION_STOP_RULE_3}}

The executor should stop and escalate instead of continuing when any of the following happens:

- {{ESCALATION_STOP_RULE_1}}
- {{ESCALATION_STOP_RULE_2}}
- {{ESCALATION_STOP_RULE_3}}

Default escalation triggers:

- scope becomes ambiguous
- required input is missing
- frozen schema, label, CLI, output, or interface would need to change without approval
- validation fails and root cause is unclear
- counter-review changes the task framing, scope, acceptance criteria, or routing class
- the task class should be upgraded from low to medium or from medium to high

---

## 16. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- evidence / retrieval performed
- counter-review performed or marked not applicable
- validation performed
- stop condition reached
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- {{HANDOFF_OUTPUT_PATH}}

---

## 17. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- {{OPEN_QUESTION_1}}
- {{OPEN_QUESTION_2}}
- {{BLOCKER_1}}

If none, write `none`.
