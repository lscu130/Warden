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


## 2. Global execution rules

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


## 3. Source of truth priority

When multiple sources exist, use this priority order:

1. Explicit user request in the current task
2. AGENTS.md
3. PROJECT.md
4. module specification docs
5. task document
6. existing code behavior
7. comments / TODOs in code

If two sources conflict, do not silently choose one.
State the conflict and continue with the safest compatible interpretation.


## 4. Warden-specific engineering constraints

### 4.1 Schema discipline

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

### 4.2 Label discipline

Warden labels are part of the research and engineering contract.

Rules:

- Do not invent new label semantics casually.
- Do not reinterpret an existing label without documenting it.
- Preserve compatibility with existing labeling scripts where possible.
- If auto-label logic is heuristic, make that explicit.
- Separate "observed signal" from "final judgment" where relevant.

### 4.3 Brand-related logic

Brand matching is supportive evidence, not the entire system.

Rules:

- Do not assume all risky pages are brand-imitating pages.
- Do not make brand logic the only decision basis unless task scope says so.
- Alias matching should be transparent and auditable.
- If brand inference is heuristic, expose confidence or rule path when practical.

### 4.4 L0 / L1 / L2 discipline

Warden is a staged system.

Rules:

- Keep stage responsibilities clear.
- Do not push expensive logic into L0 unless requested.
- Do not bypass escalation logic silently.
- Preserve explainability of stage transition conditions.

Default expectation:

- L0 favors speed and recall
- L1 adds stronger semantic/structural evidence
- L2 handles hard ambiguous high-risk cases


## 5. Module boundary rules

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


## 6. Editing policy

Before making changes:

1. identify the target files
2. identify the contracts that must remain stable
3. identify explicit non-goals
4. prefer the smallest valid patch

When editing:

- preserve style consistency with the surrounding file
- do not reformat whole files unnecessarily
- avoid touching unrelated lines
- preserve comments unless they are clearly wrong
- add comments only when they clarify non-obvious logic

After editing:

- verify imports / references / CLI flags
- verify changed paths / filenames / keys
- run the smallest useful validation available


## 7. Testing and validation rules

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


## 8. Documentation update rules

Update docs whenever one of these changes:

- CLI parameters
- output files
- field semantics
- directory conventions
- module responsibilities
- stage routing logic
- evaluation procedure

At minimum, mention needed doc updates in the final handoff even if you do not edit them directly.


## 9. Forbidden behaviors

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


## 10. Required final response format for engineering tasks

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


## 11. Task interpretation defaults

Unless the task says otherwise, assume:

- backward compatibility matters
- reproducibility matters
- auditability matters
- module boundaries matter
- documentation is part of the deliverable
- partial safe completion is better than speculative overreach


## 12. Handoff requirement

Any non-trivial change should be accompanied by a handoff summary using the project handoff template.

Minimum handoff content:

- what changed
- why it changed
- affected files
- validation run
- compatibility notes
- known risks
- next recommended task