# AGENTS.md

## 1. Project identity

Project name: Warden

Warden is a webpage social-engineering threat judgment system.
It is not limited to classic phishing-site detection.
Its goal is to judge whether a webpage presents meaningful social-engineering risk,
using signals such as screenshot, HTML, URL, DOM/text cues, intent cues, credential request cues,
brand-related evidence, and risk escalation logic.

Default system view:

- L0: fast low-cost screening
- L1: stronger semantic / structural judgment
- L2: highest-cost escalation for hard or ambiguous cases

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

### 8.4 L0 / L1 / L2 discipline

Warden is a staged system.

Rules:

- Keep stage responsibilities clear.
- Do not push expensive logic into L0 unless requested.
- Do not bypass escalation logic silently.
- Preserve explainability of stage transition conditions.

Default expectation:

- L0 favors speed and recall
- L1 adds stronger semantic / structural evidence
- L2 handles hard ambiguous high-risk cases


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

