# TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1

## 中文版

### 摘要

本任务把 `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1.md` 作为当前执行边界，落到仓库内用于审计与延续。目标是在不训练模型、不修改冻结 schema、不改标签和样本的前提下，新增 Warden L1 可插拔管线骨架、规则基线、证据账本、确定性解释器、模型 adapter stub、只读 smoke CLI 和基础测试。

### 执行边界

- 允许新增 `src/warden/l1/**`、`scripts/l1/run_l1_baseline_smoke.py`、`tests/infer/test_l1_pipeline_skeleton.py`。
- 允许新增本任务文档和对应 handoff。
- 禁止运行 OCR、YOLO、CLIP、MobileCLIP、SNet、teacher、蒸馏或训练。
- 禁止修改原始样本、manifest、标签枚举、冻结 schema 或现有公开输出契约。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1
- Task Title: Build Warden L1 Pipeline Skeleton And Rule Baseline V1
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Inference / L1
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1.md`; `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`; `PROJECT.md`
- Created At: 2026-05-11
- Requested By: user
- Karpathy Guardrails Required: YES

Use this template for any non-trivial engineering task in Warden.

## 1. Background

Warden currently defines the online architecture as `L0 + L1`, with future heavier review left for later definition. L1 is the main judgment layer and should consume source-aware evidence from URL, visible text, actionable HTML, forms, network, and structured or joint signals. The current task requires an implementation skeleton that is runnable and testable before trained text, fusion, OCR, or detector models exist.

## 2. Goal

Add a replaceable L1 pipeline skeleton and conservative rule baseline that can read sample evidence, extract lightweight features, generate joint signals, build an evidence ledger, emit reason codes, render deterministic explanations, and produce an internal draft L1 baseline result without modifying frozen project schema or running heavy models.

## 3. Scope In

This task is allowed to touch:

- `src/warden/l1/**`
- `scripts/l1/run_l1_baseline_smoke.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`
- `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`

This task is allowed to change:

- add a new L1 skeleton package under the existing `src/warden` package style
- add a read-only manifest smoke runner that reads `current_path` and writes JSONL results
- add tests for missing files, bad JSON, actionable HTML, forms, sparse text, reason codes, deterministic explanations, and CLI smoke

## 4. Scope Out

This task must NOT do the following:

- do not train BERT, e5, text tower, fusion head, or any other model
- do not run teacher distillation, MIMO, DeepSeek, GPT, Gemini, OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like online inference
- do not modify frozen schema, label enums, existing manifest semantics, source samples, human labels, or train / val / test splits
- do not define L2 in this task
- do not make final benchmark or accuracy claims
- do not add third-party dependencies

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`

### Code / Scripts

- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `src/warden/module/l1.py`
- `scripts/data/common/html_payload_utils.py`
- `scripts/data/common/io_utils.py`

### Data / Artifacts

- sample directories containing any subset of `url.json`, `visible_text.txt`, `forms.json`, `net_summary.json`, optional HTML artifacts, and screenshot files
- manifest rows containing `current_path`

### Prior Handoff

- none required for execution

### Missing Inputs

- none blocking

## 6. Required Outputs

This task should produce:

- new L1 skeleton code under `src/warden/l1/**`
- new smoke CLI at `scripts/l1/run_l1_baseline_smoke.py`
- new tests at `tests/infer/test_l1_pipeline_skeleton.py`
- repo task doc and repo handoff doc

Output format requirements:

- draft L1 result JSON must include `label`, `risk_score`, `confidence`, `malicious_basis`, `payload_observed`, `page_role`, `risk_axes`, `routing`, `reason_codes`, `evidence_ledger`, and `explanation`
- CLI output must be JSONL, one result per manifest row processed
- output fields are internal draft result fields for this task and must not be claimed as frozen project schema

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
- Keep stable prompt/context content before task-specific dynamic content when preparing agent prompts.
- Use structured outputs or schema validation outside the prompt when the execution environment supports it.
- Follow the Karpathy-style guardrails: think before acting, simplicity first, surgical changes, and goal-driven verification.

Task-specific constraints:

- missing files and bad JSON must record issues and must not crash the L1 baseline
- heavy HTML artifacts must be size-limited and record truncation when truncated
- human folder names, triage labels, split names, source feed labels, teacher labels, and manual labels must not enter evidence text
- action surfaces are only evidence and routing hints; login, payment, wallet, download, support, and redirect do not imply malicious by themselves
- CLIP / MobileCLIP and SNet / SpecularNet-like are offline or future optional routes only and are not implemented here
- explanations must come from evidence ledger plus reason codes through deterministic rendering

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden runtime result and trace contracts
- existing manifests and sample directories
- existing label enums and frozen schema fields

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none may be changed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing runtime and data scripts under `scripts/**`
  - existing tests and checkers

Downstream consumers to watch:

- future L1 training and fusion implementation
- future runtime integration

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- existing package layout supports `src/warden/l1`
- current L1 definition excludes default online CLIP / SNet
- current runtime has `SampleContext`-like contracts
- task and handoff docs satisfy repo checker markers

Allowed evidence sources:

- current repository files
- user-provided task document
- targeted command output
- local tests and smoke outputs

Retrieval budget:

- Initial retrieval: governing docs, task file, current package layout, existing runtime contracts, relevant utilities, and checkers
- Additional retrieval is allowed only when implementation needs a concrete existing convention or validation failure requires diagnosis
- Stop retrieval when implementation and validation requirements are covered

Missing-evidence behavior:

- mark the item as unsupported or partial rather than inventing repository state

### 9.1 Counter-Review Requirements

Current proposed framing:

Build an L1 skeleton and rule baseline now, while keeping heavy trained models and final schema freeze for later tasks.

Hidden assumptions to check:

- `src/warden/l1` is compatible with current package layout
- a rule baseline can produce draft internal output without freezing project schema
- CLI smoke can write only to the requested output path without modifying samples or manifests

Failure modes to consider:

- accidentally treating action surfaces as malicious truth
- accidentally ingesting labels or folder names into evidence text
- silently turning draft output fields into frozen schema
- running heavy models or network calls through stubs

Counterexamples or contradictory cases to search for:

- benign login, download, wallet, or support pages
- sparse text pages where screenshot or HTML evidence is missing
- hosted-platform shells with brand tokens but insufficient deception evidence

Alternative routes to compare:

- implement only docs
- wire into existing runtime immediately
- build isolated L1 skeleton with no integration side effects

Required evidence before accepting the framing:

- current project docs describe L1 as staged main judgment with deterministic explanation
- current task explicitly requests skeleton, rule baseline, stubs, and read-only smoke CLI
- no task permission exists to modify frozen schema, labels, or runtime contracts

Decision rule:

- Accept original framing only if the implementation stays isolated, conservative, and testable.
- Revise framing if existing package layout conflicts with `src/warden/l1`.
- Stop and escalate if schema, label, dependency, or data mutation changes become necessary.

Output discipline:

- Separate facts, inferences, assumptions, recommendations, and risks in the handoff.
- Do not treat heuristic baseline output as ground truth.
- Do not continue into implementation if counter-review changes the task class, scope, schema / interface risk, or acceptance criteria.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Assumptions allowed for this task: implement a new isolated `warden.l1` package under existing `src/warden`; treat draft L1 fields as internal output; use Python standard library only
- Ambiguities that require clarification before execution: any need to change frozen schema, labels, existing runtime output, dependencies, or sample data
- Multiple plausible interpretations considered: integrate directly into existing runtime, create separate skeleton package, or docs-only delivery
- Chosen interpretation and reason: create separate skeleton package because it satisfies the task while preserving existing runtime contracts

Simplicity boundary:

- Simplest acceptable solution: deterministic standard-library extractors, conservative rules, model stubs that return placeholders, and focused tests
- Complexity budget: no new dependency, no model loading, no browser rendering, no broad runtime refactor
- Speculative features explicitly forbidden: training, teacher paths, online CLIP / SNet, final schema freeze, broad runtime integration
- New abstractions / dependencies allowed: new local modules inside `src/warden/l1`; no third-party dependencies

Surgical change boundary:

- Every touched file must map to this scope item: L1 skeleton code, smoke CLI, tests, repo task doc, or repo handoff
- Adjacent cleanup policy: no unrelated cleanup
- Formatting-only changes allowed: only inside newly created files
- Orphan cleanup allowed only for artifacts made obsolete by this task: no

Goal-driven verification loop:

- L1 skeleton import and basic modules compile -> `python -m py_compile ...`
- feature extraction and rule baseline behavior -> targeted pytest
- CLI smoke output -> run smoke CLI on a local tiny manifest and, if available, a small subset of `benign_val_manifest_v1.csv`
- task and handoff structure -> repo checker scripts

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

- [ ] L1 skeleton package is added
- [ ] evidence pack can be built from sample directory and manifest row
- [ ] URL, visible text, actionable HTML, forms, and network features are extracted
- [ ] joint signals, evidence ledger, reason codes, deterministic explanation, and draft result JSON are produced
- [ ] CLI smoke can run on a small manifest subset
- [ ] missing files, bad JSON, and malformed HTML do not crash
- [ ] source samples, manifests, labels, frozen schema, OCR, YOLO, CLIP, SNet, teacher, and training remain untouched
- [ ] task doc and handoff pass repository CI checkers

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted unit test, if behavior changed and tests exist
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check
- [ ] changed-file / changed-line scope trace spot-check

Commands to run if applicable:

```bash
python -m py_compile src/warden/l1/evidence_pack.py
python -m py_compile src/warden/l1/html_action_extractor.py
python -m py_compile src/warden/l1/l1_runner.py
python -m py_compile scripts/l1/run_l1_baseline_smoke.py
pytest tests/infer/test_l1_pipeline_skeleton.py -q
python scripts/l1/run_l1_baseline_smoke.py --manifest "<manifest>" --limit 100 --output "<output>"
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md
git status --short --untracked-files=all
```

Expected evidence to capture:

- command exit status and output summary
- smoke output count and output path
- scope impact from git status

If validation cannot be run:

- Not run: list exact command
- Reason: list exact environment or missing-data reason
- Next best check: list exact replacement check

## 12. Stop Rules

The executor should stop and report completion when all of the following are true:

- required code, CLI, tests, task doc, and handoff have been created
- targeted validations have passed or exact inability has been reported
- no forbidden training, teacher, heavy model, sample, manifest, label, schema, or split side effect occurred

The executor should stop and escalate instead of continuing when any of the following happens:

- frozen schema, label enum, existing manifest semantics, or public output compatibility must change
- new third-party dependencies appear necessary
- OCR, YOLO, CLIP, SNet, teacher, or training becomes necessary to satisfy the task
- validation fails for an unclear reason after focused diagnosis

## 13. Suggested Execution Notes

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Reject speculative abstractions, future-proofing, or adjacent cleanup unless the task explicitly requires them.
5. Run the smallest meaningful validation.
6. Summarize compatibility impact.
7. Prepare handoff.

Task-specific execution notes:

- start from focused tests for required behavior
- keep `warden.l1` isolated from existing runtime integration unless a later task wires it in
- use deterministic, auditable logic and standard library parsing

## 14. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- added files
- L1 pipeline skeleton structure
- evidence pack supported artifacts
- actionable HTML extractor supported tags
- rule baseline output fields
- evidence ledger, reason code, and explanation renderer design
- CLI smoke result
- missing artifact and bad JSON handling
- explicit statement that training, teacher, OCR, YOLO, CLIP, and SNet were not run
- risks and next steps

Repo handoff path if one should be created:

- `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`

## 15. Open Questions / Blocking Issues

- none
