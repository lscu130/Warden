# TASK_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1

## 中文版

### 摘要

本任务用于新增 Warden L1 Decision Head 与 Text Semantic Concept 的草案契约文档。当前 L1 draft 已拆分为 `rule_router`、`text_semantic_concepts`、`vision_evidence`、`decision_head`，其中 `decision_head.status = not_run`。本任务只写文档和 handoff，不训练模型、不实现 XGBoost / Decision Head、不跑 teacher、OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like，也不改 runtime schema、标签、manifest、样本或数据切分。

### 执行边界

- 新增 `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`。
- 新增本任务文档。
- 新增本任务 handoff。
- 禁止修改代码、正式 runtime schema、标签、manifest、样本和历史 handoff。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260512-WARDEN-L1-DECISION-HEAD-CONTRACT-V1
- Task Title: Design Warden L1 Decision Head And Text Semantic Concept Contract V1
- Owner Role: Codex executor, GPT Web reviewer, human final acceptor
- Priority: P0
- Status: TODO
- Related Module: Inference / L1 / Contract / Future Training Interface
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\TASK_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1.md`
- Created At: 2026-05-12
- Requested By: user
- Karpathy Guardrails Required: YES

Use this template for any non-trivial engineering task in Warden.

## 1. Background

Warden L1 recently realigned the rule-only baseline into a `rule_router / evidence_sufficiency` diagnostic component. The current draft sidecar separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`. The `decision_head` is currently `not_run`, with final-like fields set to `null`.

Future teacher distillation, text tower training, visual evidence recovery, and Decision Head / XGBoost training need a shared draft contract. This task creates that contract as documentation only.

## 2. Goal

Create a repository-ready bilingual contract document defining how future L1 text semantic concepts, optional vision evidence, structured evidence, and L1 Decision Head outputs should interoperate. The contract must state that `rule_router` is a diagnostic router, L1-text is the main semantic branch, L1-vision recovers evidence, and future L1 final decision fields belong to the Decision Head. It must also state that this is a draft contract and does not change official runtime schema.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

This task is allowed to change:

- add contract documentation
- add draft field definitions
- add draft JSON examples
- add validation and future-work notes

## 4. Scope Out

This task must NOT do the following:

- train a text tower
- train or implement XGBoost / Decision Head
- run teacher distillation
- call external APIs
- run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like models
- modify runtime behavior
- modify official runtime result / trace schema
- modify labels, manifests, data splits, or sample files
- edit existing code unless a narrow import/reference typo in docs tooling blocks validation
- rewrite historical handoffs

## 5. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`

### Missing Inputs

- none blocking

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

Output format requirements:

- Markdown documents must be bilingual.
- Contract doc must place the Chinese summary first and English authoritative section second.
- Contract doc must include draft field definitions and JSON examples.

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
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.
- Follow the Karpathy-style guardrails: think before acting, simplicity first, surgical changes, and goal-driven verification.

Task-specific constraints:

- documentation / contract only
- no code edits
- no runtime behavior change
- no official schema freeze
- no model training or heavy model execution

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- official runtime result schema
- official runtime trace schema
- existing L1 draft debug sidecar behavior
- existing labels, manifests, samples, and splits

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none may be changed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/ci/check_task_doc.py <task_doc>`
  - `python scripts/ci/check_handoff_doc.py <handoff_doc>`

Downstream consumers to watch:

- future text semantic concept training
- future Decision Head training
- future L1 output schema freeze

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- task scope is documentation only
- current L1 draft separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`
- Decision Head is currently `not_run`
- official runtime schema must remain unchanged

Allowed evidence sources:

- user-provided task document
- current repo task and handoff documents
- checker outputs
- focused grep output

Retrieval budget:

- Initial retrieval: task file, latest related task doc, latest related handoff, checker requirements, docs directory layout
- Additional retrieval is allowed only if validation fails or a required term is missing
- Stop retrieval when required docs exist and validation passes

Missing-evidence behavior:

- state missing validation or unsupported claims explicitly

### 9.1 Counter-Review Requirements

Current proposed framing:

Create a draft Decision Head and text semantic concept contract without implementation, training, schema freeze, or runtime behavior changes.

Hidden assumptions to check:

- contract wording will not be treated as official runtime schema
- future final labels belong to Decision Head
- visual evidence recovery remains evidence-only

Failure modes to consider:

- accidentally implying current official schema changed
- accidentally making rule_router a classifier again
- documenting OCR / YOLO / CLIP / SNet as current default online components
- over-specifying training implementation details

Counterexamples or contradictory cases to search for:

- benign action surfaces
- high-risk candidates requiring future model judgment
- sparse evidence requiring visual recovery

Alternative routes to compare:

- write implementation stubs now
- update only existing L1 framework doc
- add a separate focused contract doc

Required evidence before accepting the framing:

- user task explicitly limits changes to docs
- latest handoff says Decision Head is not run
- validation commands can verify doc structure and required terms

Decision rule:

- Accept the framing if all output files are documentation-only and validation passes.
- Stop and escalate if code/runtime/schema changes become necessary.

Output discipline:

- Separate source-backed facts from draft contract statements and future recommendations.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Assumptions allowed for this task: `docs/l1/` can be created because the task explicitly allows it if missing
- Ambiguities that require clarification before execution: any need to change code, runtime schema, labels, data, or training behavior
- Multiple plausible interpretations considered: update existing L1 framework doc or create a new focused contract doc
- Chosen interpretation and reason: create a focused contract doc because the task names an exact output path

Simplicity boundary:

- Simplest acceptable solution: three documentation files and required validation
- Complexity budget: no code, no generated artifacts outside docs, no broad doc rewrite
- Speculative features explicitly forbidden: model implementation, training, distillation, schema freeze
- New abstractions / dependencies allowed: none

Surgical change boundary:

- Every touched file must map to one of the three required output paths.
- Adjacent cleanup policy: none.
- Formatting-only changes allowed: only in new docs.
- Orphan cleanup allowed only for artifacts made obsolete by this task: no.

Goal-driven verification loop:

- task doc exists and passes checker -> `check_task_doc.py`
- handoff exists and passes checker -> `check_handoff_doc.py`
- contract contains required terms -> focused `rg`
- scope remains docs-only -> `git status --short --untracked-files=all`

## 10. Acceptance Criteria

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

- [ ] Task doc exists
- [ ] Contract doc exists
- [ ] Handoff exists
- [ ] Contract explicitly states rule_router is not a classifier
- [ ] Contract defines text semantic concept groups
- [ ] Contract defines vision evidence recovery semantics
- [ ] Contract defines future Decision Head inputs and outputs
- [ ] Contract states official runtime schema is not changed
- [ ] Contract states CLIP / SNet are not default online L1 components
- [ ] Validation commands were run or explicitly explained
- [ ] No code, schema, labels, manifests, or data were modified

## 11. Validation Checklist

Minimum validation expected:

- [ ] task doc checker
- [ ] handoff checker
- [ ] required-term grep
- [ ] changed-file scope inspection

Commands to run if applicable:

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md
rg -n "Rule Router|Decision Head|text_semantic_concepts|vision_evidence|action surface != threat action|not final schema|not_run" docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md
git status --short --untracked-files=all
```

Expected evidence to capture:

- checker OK lines
- grep matched required terms
- scope remains documentation-only for this task

If validation cannot be run:

- Not run: exact command
- Reason: exact blocker
- Next best check: exact fallback

## 12. Stop Rules

The executor should stop and report completion when all of the following are true:

- task doc, contract doc, and handoff are written
- required validation has passed or exact inability is documented
- no code, schema, label, manifest, sample, split, training, teacher, OCR, YOLO, CLIP, SNet, or runtime behavior change occurred

The executor should stop and escalate instead of continuing when any of the following happens:

- implementation appears necessary
- official runtime schema changes appear necessary
- validation requires changing tooling outside task scope

## 13. Suggested Execution Notes

Recommended order:

1. Read the user task, checker requirements, related handoff, and docs layout.
2. Create `docs/l1/` if needed.
3. Write the three required docs.
4. Run required validation.
5. Stop after documentation validation.

Task-specific execution notes:

- Keep contract wording clear that fields are draft.
- Keep future training notes separate from current runtime behavior.

## 14. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- files created
- contract content summary
- schema / interface impact
- validation performed
- explicit out-of-scope confirmation

Repo handoff path if one should be created:

- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

## 15. Open Questions / Blocking Issues

- none
