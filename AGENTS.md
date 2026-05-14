# AGENTS.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是 Warden 的仓库级工程约束文件。
- 涉及精确字段名、接口、模板字段、优先级或历史事实时，以英文版为准。
- 中文区块只保留面向人类的压缩摘要，不替代英文约束正文。
- 给用户的 Markdown 文档默认必须采用双语结构：前置中文摘要供人工阅读，后置英文全文供 AI 读取。

## 1. 文档作用

`AGENTS.md` 用于冻结 Warden 的全局工程规则、工作边界、优先级顺序、模块职责和交付格式。
它不是建议清单，而是仓库内默认生效的执行契约。

## 2. 关键规则摘要

- 非 trivial 工作必须遵守 workflow、task 和 handoff 三件套。
- 默认优先最小、可验证、可回退的改动，不允许顺手大改或无关清理。
- 冻结字段名、文件名、CLI、输出结构和标签语义时，不允许静默改动。
- 给用户的 Markdown 文档必须中英双语，中文摘要在前，英文全文在后。
- 若需求与文档约束冲突，应明确指出冲突，而不是自行猜测。
- Warden 的社会工程威胁定义包括高危欺骗行为和/或高危诱导动作；未观察到 payload / action 不能自动等同于 benign。
- 无效采集、HTTP 错误页、空白页、纯色渲染页、严重渲染失败页、证据不可观测页面不是 Warden 威胁模型样本，不能标记为 benign、malicious 或 suspicious；数据集构建时由项目负责人在正式 train / validation / test 前移除。
- 当前在线架构只定义 `L0` 和 `L1`：`L0` 是低成本筛查与路由层，`L1` 是主判断层；更重的未来复核或升级路径必须另行定义。
- 面向 GPT-5.5 / Codex / Claude Code 的任务提示默认采用 outcome-first：先写目标、成功标准、证据规则、约束、输出形态、验证和停止规则；只有路径本身影响正确性时才写死步骤。
- 对架构、标签、数据集、模型、评估、workflow 和论文定位等高影响问题，默认执行反审：先检查隐含假设、失败场景、反例、证据缺口和备选路线。
- 需要记录或约束 reasoning effort、verbosity、retrieval budget、preamble、工具副作用、反审要求和验证方式时，应写入任务单或 handoff。
- 新增 Karpathy-style 执行护栏：先澄清假设和歧义，再执行；默认选择能满足成功标准的最小方案；每个改动必须能追溯到任务目标；交付前必须完成最小验证闭环或明确说明未验证原因。

## 3. 阅读重点

优先阅读英文版的以下部分：

- `Global execution rules`
- `Source of truth priority`
- `Workflow compliance is mandatory`
- `Schema discipline` / `Label discipline`
- `Required final response format`
- `GPT-5.5 prompt and agent defaults`
- `Counter-review and anti-closed-loop reasoning defaults`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# AGENTS.md

## 1. Project identity

Project name: Warden

Warden is a webpage social-engineering threat judgment system.
It is not limited to classic phishing-site detection.
Its goal is to judge whether a webpage presents meaningful social-engineering risk,
using signals such as screenshot, HTML, URL, DOM/text cues, intent cues, credential request cues,
brand-related evidence, and risk escalation logic.
Warden defines a webpage social-engineering threat as high-risk deceptive behavior and/or high-risk induced action.
High-risk deceptive behavior includes false or misleading identity, brand, authority, institution, security, financial, support, reward, or access-control context construction.
Such behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other high-risk action is currently observed.
Absence of observed payload should be treated as `payload not observed`, not as automatic benign.
Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are not Warden threat-model samples. They must not be labeled as benign, malicious, or suspicious. In the dataset-building workflow, the project owner removes these samples before formal train / validation / test construction.

Current online system view:

- L0: cheapest rule hot path, cheap screening, and low-cost routing
- L1: main judgment layer, including evidence-pack construction, text judgment, trigger-based vision evidence recovery, structured / joint signals, fusion, evidence ledger, and deterministic explanation rendering
- Future heavier review or escalation may be defined later, but no current L2 architecture is defined by default.

L0 handles only a small set of high-confidence cheap terminal or auxiliary buckets, such as adult, gambling, and obvious gate / challenge / verification cases. L0 does not decide ordinary benign or malicious webpage status. Every valid webpage sample not terminated by L0 must route to L1, and the L1 text branch is the default judgment path.

Primary engineering goals:

- reproducible data pipeline
- frozen schema discipline
- explicit module boundaries
- edge-deployable inference path
- documentation-first workflow
- safe iterative refinement

Non-goals unless explicitly requested:

- silent large-scale refactor
- arbitrary schema renaming
- adding dependencies without approval
- changing public interfaces for convenience
- inventing undocumented labels or fields
- replacing stable logic with speculative redesign


## 2. Mandatory governing files

The following files are not optional references. They are active process contracts.
Any thread working inside `E:\Warden` must treat them as mandatory.

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Interpretation rule:

- `AGENTS.md` defines project-wide engineering and delivery rules.
- `GPT_CODEX_WORKFLOW.md` defines the required collaboration sequence and role boundaries.
- `TASK_TEMPLATE.md` defines the minimum structure of an execution-ready task.
- `HANDOFF_TEMPLATE.md` defines the minimum structure of a non-trivial delivery handoff.

Do not treat these files as examples.
Treat them as rules.


## 3. Global execution rules

You are working inside a real engineering project, not a demo sandbox.

Follow these rules strictly:

1. Prefer minimal, testable, reversible changes.
2. Read relevant files before editing.
3. Respect frozen field names and documented contracts.
4. Do not "clean up" unrelated code.
5. Do not rename files, keys, CLI flags, functions, or folders unless explicitly asked.
6. Do not add third-party dependencies unless explicitly approved.
7. Do not change output formats silently.
8. When behavior changes, update the corresponding docs.
9. When unsure, preserve backward compatibility.
10. If a task conflicts with documented constraints, state the conflict explicitly rather than guessing.
11. Do not skip required workflow artifacts just because the task seems small.
12. Do not claim compliance with workflow, task, or handoff requirements if the artifact was not actually read or produced.
13. Markdown documents delivered to the user must be bilingual by default: a Chinese summary first for human reading, followed by the full English version for AI reading.
14. For Markdown documents, English remains the authoritative version whenever exact wording, fields, commands, priorities, or historical facts matter.
15. For GPT-5.5-class agents, prefer outcome-first prompts over process-heavy prompt stacks.
16. Define success criteria, evidence rules, validation expectations, and stop rules before asking for implementation.
17. Use detailed step-by-step process guidance only when the exact process is required by correctness, reproducibility, safety, or a project contract.
18. For tool-heavy work, provide a short preamble before running tools and keep progress updates factual.
19. Do not assume the user's proposed framing, architecture, taxonomy, model choice, experiment design, workflow change, or research claim is correct when the task is high-impact.
20. For architecture, labeling, dataset, model, evaluation, workflow, and research decisions, perform counter-review before turning the proposal into execution work.
21. Distinguish source-backed facts, engineering inferences, assumptions, recommendations, and unresolved risks.
22. If evidence is insufficient to accept or reject a framing, mark the claim as unsupported or partial instead of filling the gap with speculation.


### 3.0 Karpathy-derived agent guardrails

Warden adopts the Karpathy-inspired coding-agent guardrails as operational discipline, not as a new architecture or executor route.
These guardrails apply to non-trivial GPT Web, Human Manual, Codex, and any explicitly approved autonomous-agent work.
For trivial one-line edits, apply them lightly without creating unnecessary process overhead.

#### Think before acting

Before implementation or task routing, the agent must surface material uncertainty instead of silently choosing an interpretation.

Required behavior:

- State assumptions when they affect scope, compatibility, labels, schema, evaluation, or user-facing output.
- Present multiple plausible interpretations when the request can reasonably mean more than one thing.
- Push back when the requested route is more complex, riskier, or less testable than a simpler route that satisfies the same goal.
- Stop and clarify, mark missing evidence, or keep the task exploratory when ambiguity could corrupt data, labels, metrics, interfaces, or research conclusions.

#### Simplicity first

Prefer the smallest design, patch, prompt, script, or document change that satisfies the success criteria.

Rules:

- Do not add speculative features, optional flexibility, general frameworks, broad abstractions, or future-proofing that the task did not ask for.
- Do not introduce new dependencies, new schema fields, new CLI flags, or new modules merely to make the solution look cleaner.
- If a shorter local change satisfies the task and preserves contracts, prefer it over a broad redesign.
- If the proposed implementation starts to look over-engineered, reduce it before editing.

#### Surgical changes

Every changed line must trace to the active task goal, `scope_in`, success criteria, or required validation.

Rules:

- Do not reformat whole files or clean adjacent code unless the task explicitly asks for that cleanup.
- Match existing file style even when a different style would be preferred.
- Mention unrelated dead code, stale comments, or design debt in the handoff instead of silently changing it.
- Remove only the imports, variables, comments, generated artifacts, or references made obsolete by the current change.

#### Goal-driven verification loop

For non-trivial work, convert the task into a small set of observable checks and stop only when those checks are satisfied or honestly reported as not run.

Required behavior:

- Map each material change to a verification check: text search, diff inspection, schema compatibility check, smoke test, unit test, build, artifact inspection, or manual review.
- Prefer tests or checks that directly falsify the intended behavior over broad low-signal validation.
- If validation cannot run, state exactly what was not run, why, and the next best check.
- Do not continue tool use after the stop rule is satisfied unless a material unresolved risk remains.


### 3.1 GPT-5.5 prompt and agent defaults

For GPT-5.5, Codex, Claude Code, and comparable reasoning agents, Warden prompts should use an outcome-first contract.

Default prompt shape:

1. `Role`: the agent role and responsibility boundary.
2. `Goal`: the concrete outcome to produce.
3. `Success criteria`: observable checks for completion.
4. `Scope in`: files, modules, commands, or artifacts that may be touched.
5. `Scope out`: files, modules, behavior, schemas, labels, or contracts that must not be touched.
6. `Evidence rules`: what must be read, searched, cited, or verified before making claims.
7. `Validation`: the smallest useful checks that must be run or explicitly marked as not run.
8. `Stop rules`: when to stop as done, when to stop as blocked, and when to escalate.
9. `Output`: exact final response or handoff format.

Do not carry forward long legacy prompt stacks merely because they existed before. Keep stable project contracts in governing docs and task templates. Keep the task-specific request short, concrete, and placed after stable context when possible.

Runtime defaults:

- `reasoning.effort`: start from `medium` for GPT-5.5 when quality, reliability, latency, and cost must be balanced.
- Use `low` for mechanical, local, or latency-sensitive tasks that still need light planning or tool use.
- Use `none` only for latency-critical tasks that do not need reasoning, multi-step planning, or chained tool calls.
- Use `high` or `xhigh` only for difficult architecture, debugging, agentic, evaluation, or cross-module work where the extra latency and cost are justified.
- `text.verbosity`: use `low` for routine status and mechanical reviews, `medium` for normal engineering handoff, and `high` only for specs, audits, research notes, or complex tradeoff analysis.

Evidence and retrieval defaults:

- Define a retrieval budget for grounded tasks.
- Start with the smallest retrieval set that can answer the core question.
- Continue retrieval only when a required fact, file, source, date, owner, command output, or citation is missing.
- Stop retrieval when additional search is unlikely to change the answer or reduce a material risk.
- Do not search again only to improve phrasing, add nonessential examples, or decorate the answer.
- Do not turn absence of evidence into a factual negative claim.

Validation defaults:

- When validation is possible, run the most relevant targeted check: syntax/import sanity, targeted unit test, type/lint check, build check, smoke test, or output artifact inspection.
- If validation cannot be run, report what was not run, why it was not run, and the next best check.
- For visual or generated artifacts, inspect the rendered or generated output before final delivery when the environment allows it.

Tool-heavy workflow defaults:

- Give a short preamble before long or tool-heavy work.
- Preserve tool side-effect boundaries: read-only tasks must stay read-only; write tasks must stay inside `scope_in`.
- In Responses-API-style workflows, preserve `phase`, preambles, and assistant-item replay semantics when the application exposes them.
- Prefer structured output or external schema validation when available instead of embedding large schema definitions in prompt text.


### 3.2 Counter-review and anti-closed-loop reasoning defaults

Counter-review is Warden's default defense against closed-loop reasoning, user-framing bias, and plausible but unsupported project drift.
It is mandatory for high-impact decisions involving architecture, module boundaries, threat-definition semantics, labels, dataset admission, model selection, fusion design, training or evaluation methodology, research novelty, workflow rules, or agent routing.

Counter-review must check at least the following:

- current proposed framing
- hidden assumptions
- likely failure modes
- counterexamples or contradictory evidence
- missing evidence or missing repository context
- alternative routes
- compatibility and downstream risks
- whether the task should remain exploratory, become a task document, or be escalated

Counter-review output should distinguish:

- `fact`: directly supported by a checked source, current file, command output, cited paper, official documentation, or supplied artifact
- `inference`: derived from supported facts but not directly stated by the evidence source
- `assumption`: used temporarily because evidence is incomplete
- `recommendation`: the agent's proposed action or design choice
- `risk`: a failure mode, uncertainty, compatibility issue, or validation gap

Counter-review must not become unbounded debate.
Use the retrieval budget and stop rules from the task document.
Stop when the framing is sufficiently supported for the current decision, when evidence is insufficient and must be reported, or when the task boundary needs human approval before execution.

## 4. Source of truth priority

When multiple sources exist, use this priority order:

1. Explicit user request in the current task
2. `AGENTS.md`
3. `docs/workflow/GPT_CODEX_WORKFLOW.md`
4. Approved active task document based on `docs/templates/TASK_TEMPLATE.md`
5. `PROJECT.md`
6. module specification docs
7. relevant prior handoff documents
8. existing code behavior
9. comments / TODOs in code

Important clarifications:

- A handoff is context, not authority to override contracts.
- A task doc cannot silently override `AGENTS.md` or workflow rules.
- If `PROJECT.md` is referenced but missing, state that explicitly.
- If no active task doc exists for a non-trivial task, do not pretend one exists.

If two sources conflict, do not silently choose one.
State the conflict and continue with the safest compatible interpretation.


## 5. Workflow compliance is mandatory

All non-trivial work in Warden must follow the workflow in `docs/workflow/GPT_CODEX_WORKFLOW.md`.
The required order is:

1. requirement clarification
2. task definition
3. execution
4. review / acceptance

Do not reorder these stages silently.

### 5.1 What counts as non-trivial

Treat a task as non-trivial if any of the following is true:

- touches more than one file
- changes behavior, outputs, schema, labels, CLI, routing, or docs
- affects multiple modules
- requires validation beyond syntax sanity
- depends on prior handoff context
- has unclear scope or meaningful compatibility risk

### 5.2 What must happen before non-trivial execution

Before non-trivial implementation, there must be an active task definition that covers the required `TASK_TEMPLATE.md` fields.

Acceptable forms:

- an existing repo task doc under `docs/tasks/`
- a user-provided task doc that is explicitly adopted
- a task definition produced in the current thread that clearly covers the template requirements

Not acceptable:

- vague paragraph instructions with missing scope boundaries
- "just fix it" with no stated constraints when schema / interfaces may be affected
- treating prior handoff as a substitute for a task doc

### 5.3 When to stop and escalate instead of coding

Stop and ask for clarification, or explicitly mark missing inputs, when:

- the task is non-trivial and no task boundary can be derived safely
- schema / labels / CLI / outputs may change but permission is unclear
- the requested change conflicts with frozen contracts
- the task spans multiple modules but no scope boundary exists


## 6. Task document rules

`docs/templates/TASK_TEMPLATE.md` is mandatory for non-trivial work.

Every active non-trivial task must define, at minimum:

- background
- goal
- scope in
- scope out
- inputs
- required outputs
- hard constraints
- interface / schema constraints
- acceptance criteria
- validation checklist

Rules:

- Do not execute broad changes without explicit `scope_in` and `scope_out`.
- Do not accept fuzzy phrases such as "optimize if needed", "refactor when appropriate", or "adjust structure if necessary".
- Replace vague language with hard constraints.
- If a task doc is partial, state exactly what is missing before proceeding.
- If the task changes during execution, update the task boundary explicitly instead of drifting silently.

Recommended repo location for active task docs:

- `docs/tasks/<date>_<short_name>.md`


## 7. Handoff rules

`docs/templates/HANDOFF_TEMPLATE.md` is mandatory for any non-trivial change.

For non-trivial work, the final delivery must include handoff content covering the template fields.
When practical, create or update a repo handoff document under:

- `docs/handoff/<date>_<short_name>.md`

Minimum required handoff coverage:

- metadata
- executive summary
- what changed
- files touched
- behavior impact
- schema / interface impact
- validation performed
- open risks / caveats
- recommended next step

Rules:

- Do not hand-wave behavior impact.
- Do not omit compatibility notes when interfaces, schema, CLI, or outputs are touched.
- Do not claim validation that was not run.
- If docs were not updated, say whether they were unnecessary or still needed.


## 8. Warden-specific engineering constraints

### 8.1 Schema discipline

Schema stability is critical.

Rules:

- Treat documented manifest / meta / label field names as frozen.
- Do not rename existing keys for style reasons.
- Do not merge semantically different fields into one field.
- Do not split one field into many fields unless explicitly requested.
- New fields must be backward compatible and documented.
- If a field is deprecated, do not remove it unless explicitly requested.

Whenever a task touches schema-related logic, explicitly report:

- whether any schema changed
- whether output compatibility was preserved
- whether downstream scripts may be affected

### 8.2 Label discipline

Warden labels are part of the research and engineering contract.

Rules:

- Do not invent new label semantics casually.
- Do not reinterpret an existing label without documenting it.
- Preserve compatibility with existing labeling scripts where possible.
- If auto-label logic is heuristic, make that explicit.
- Separate "observed signal" from "final judgment" where relevant.
- Do not treat weak labels as manual gold labels.

### 8.3 Brand-related logic

Brand matching is supportive evidence, not the entire system.

Rules:

- Do not assume all risky pages are brand-imitating pages.
- Do not make brand logic the only decision basis unless task scope says so.
- Alias matching should be transparent and auditable.
- If brand inference is heuristic, expose confidence or rule path when practical.
- Strong deceptive brand, authority, institution, security, financial, support, reward, or access-control context can be high-risk behavior, but brand mismatch alone must not become a universal one-factor malicious rule without supporting context.

### 8.4 L0 / L1 discipline

Warden is a staged system.

Rules:

- Keep stage responsibilities clear.
- Do not push expensive logic into L0 unless requested.
- Do not bypass escalation logic silently.
- Preserve explainability of stage transition conditions.
- Do not define a current L2 architecture unless a separate accepted task explicitly introduces it.

Default expectation:

- L0 favors speed and recall
- L0 handles only high-confidence cheap terminal / auxiliary buckets such as adult, gambling, and obvious gate / challenge / verification; ordinary valid non-terminal webpages route to L1 instead of receiving final benign / malicious status in L0
- L1 is the main judgment layer, with the text branch as the default judgment path, trigger-based vision evidence recovery, structured / joint signals, fusion, evidence ledger, and deterministic explanation rendering
- L1 vision is evidence recovery: OCR recovers screenshot text and YOLO / detector localizes visible action components; vision evidence feeds the evidence pack / decision process but does not independently determine malicious or benign
- Future heavier review or escalation remains out of scope until separately defined


## 9. Module boundary rules

Unless explicitly requested, keep these responsibilities separate.

### Data module
Owns:

- dataset layout
- manifests
- metadata generation
- sampling / split logic
- consistency checks

Does not own:

- model architecture decisions
- inference policy redesign

### Labeling module
Owns:

- label schema application
- rule-based auto-labeling
- alias / brand dictionary matching
- conflict reports
- manual review support outputs

Does not own:

- final training pipeline behavior
- model-side threshold policy

### Training module
Owns:

- loaders
- configs
- training loop
- loss logic
- checkpointing
- eval metrics implementation

Does not own:

- raw data schema redesign

### Inference module
Owns:

- runtime pipeline
- stage routing
- threshold application
- export / benchmark / deployment path

Does not own:

- training dataset relabeling

### Paper / experiment support module
Owns:

- experiment configs archive
- result aggregation
- tables / figures generation helpers
- reproducibility notes

Does not own:

- undocumented rewriting of method logic


## 10. Editing policy

Before making changes:

1. identify the target files
2. identify the contracts that must remain stable
3. identify explicit non-goals
4. identify whether a task doc and handoff are required
5. prefer the smallest valid patch

When editing:

- preserve style consistency with the surrounding file
- do not reformat whole files unnecessarily
- avoid touching unrelated lines
- preserve comments unless they are clearly wrong
- add comments only when they clarify non-obvious logic
- do not silently broaden scope beyond the task boundary

After editing:

- verify imports / references / CLI flags
- verify changed paths / filenames / keys
- run the smallest useful validation available
- report compatibility impact explicitly
- produce handoff content if the task is non-trivial


## 11. Testing and validation rules

Use the lightest validation that can still catch obvious breakage.

Default order:

1. syntax / import sanity
2. targeted unit or smoke test
3. module-level command
4. broader integration test if task risk justifies it

If you cannot run tests, state exactly:

- what was not run
- why it was not run
- what should be run next

For data or labeling changes, prefer small-batch smoke validation first.
For schema or CLI changes, explicitly verify backward compatibility when possible.
For non-trivial work, validation reporting must satisfy both the task doc and the handoff template.


## 12. Documentation update rules

Update docs whenever one of these changes:

- CLI parameters
- output files
- field semantics
- directory conventions
- module responsibilities
- stage routing logic
- evaluation procedure
- workflow behavior
- task execution expectations

At minimum, mention needed doc updates in the final handoff even if you do not edit them directly.


## 13. Forbidden behaviors

Do not do the following unless explicitly requested:

- broad refactor across unrelated modules
- dependency upgrades
- silent schema changes
- changing naming conventions project-wide
- converting stable scripts into a new framework
- adding speculative abstractions, optional flexibility, or adjacent cleanup that is not required by the active task
- deleting fallback logic without checking compatibility
- replacing documented behavior with "better" guessed behavior
- fabricating experiment results
- claiming tests passed if they were not run
- skipping `GPT_CODEX_WORKFLOW.md`
- skipping `TASK_TEMPLATE.md` for non-trivial work
- skipping `HANDOFF_TEMPLATE.md` for non-trivial work
- treating handoff as optional when the change is non-trivial
- pretending a repository-external task doc or handoff is safely tracked if it was never copied into the repo when ongoing collaboration depends on it


## 14. Required final response format for engineering tasks

For non-trivial tasks, structure the result as:

1. Summary
2. Files changed
3. Key logic changes
4. Validation performed
5. Compatibility impact
6. Risks / caveats
7. Recommended next step
8. Evidence / retrieval performed, if the task depended on external or internal sources
9. Stop condition reached, if the task had explicit stop rules

If schema, labels, CLI, or outputs were touched, explicitly include:

- Schema changed: yes / no
- Backward compatible: yes / no / partially
- Docs updated: yes / no / needed

If the task is non-trivial, the final response must also map cleanly onto the project handoff template.


## 15. Task interpretation defaults

Unless the task says otherwise, assume:

- backward compatibility matters
- reproducibility matters
- auditability matters
- module boundaries matter
- documentation is part of the deliverable
- partial safe completion is better than speculative overreach
- workflow compliance matters as much as code correctness
- outcome-first task definitions are preferred over process-heavy instructions
- evidence rules, validation rules, and stop rules should be explicit for non-trivial work


## 16. Required handoff and acceptance discipline

Any non-trivial change must be accompanied by a handoff summary using the project handoff template.

Minimum handoff content:

- what changed
- why it changed
- affected files
- validation run
- compatibility notes
- known risks
- next recommended task

Final acceptance is not delegated to the model.
The model may implement, summarize, and self-check.
It may not pretend to be the final approver.


## 17. Cross-thread continuity rules

When work continues across threads or windows:

- carry forward the active task boundary
- carry forward the latest relevant handoff
- state what inputs are missing
- do not assume a new thread inherited unstated context
- if active work artifacts live outside the repo and ongoing collaboration depends on them, copy them into the repo and reference the repo path

If context gets long or brittle, summarize the state before switching threads.
Do not continue high-risk work on half-remembered context.
