# TASK_20260511_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1

## 中文版

### 摘要

本任务修正当前 L1 skeleton / rule baseline 的语义：规则基线必须降级为 rule router / evidence sufficiency diagnostic，不能输出 final-like `benign / suspicious / malicious` label。L1 final label 属于未来 L1 Decision Head，本任务只修正工程骨架、字段语义、文档和 benchmark 统计口径。

### 执行边界

- 允许修改 `src/warden/l1/rule_baseline.py`、`src/warden/l1/l1_runner.py`、`src/warden/l1/explanation_renderer.py`。
- 允许检查并按需窄修 `src/warden/runtime/l1_draft_bridge.py`、`src/warden/runtime/pipeline.py`。
- 允许修改 `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py` 和相关 targeted tests。
- 禁止训练模型、跑 teacher、OCR、YOLO、CLIP、MobileCLIP、SNet、SpecularNet-like、改标签、移动样本、重切数据或冻结 final L1 schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK_20260511_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1
- Task Title: Realign Warden L1 Rule Router And Decision Head Semantics V1
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Inference / L1
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1.md`
- Created At: 2026-05-12
- Requested By: user
- Karpathy Guardrails Required: YES

Use this template for any non-trivial engineering task in Warden.

## 1. Background

The current L1 skeleton exposes rule-baseline outputs as final-like classifier fields such as `label`, `risk_score`, and `confidence`. This creates misleading benchmark distributions such as `benign / suspicious / malicious` from a rule-only component. In the current Warden L0+L1 architecture, the rule baseline is a router and evidence-sufficiency diagnostic. The future final label must come from an L1 Decision Head after text semantic concepts, structured evidence, and optional visual evidence are available.

## 2. Goal

Realign L1 skeleton semantics so rule baseline output becomes `rule_assessment`, `routing_hints`, `risk_hints`, and `evidence_sufficiency`; the L1 draft sidecar separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`; the decision head is explicitly `not_run`; explanations are routing diagnostics; and benchmarks report routing/assessment distributions without final-like label distribution metrics.

## 3. Scope In

This task is allowed to touch:

- `src/warden/l1/rule_baseline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/explanation_renderer.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`

This task is allowed to change:

- rule-baseline output semantics from classifier-like fields to routing diagnostics
- L1 draft sidecar shape for debug-only draft output
- benchmark per-sample and summary fields for routing semantics
- targeted tests and docs for the new semantics

## 4. Scope Out

This task must NOT do the following:

- train text tower, XGB, fusion, or L1 Decision Head models
- run teacher distillation
- run OCR, YOLO / detector, CLIP, MobileCLIP, SNet, or SpecularNet-like inference
- modify labels, source samples, manifests, or train / val / test split
- freeze final L1 output schema
- promote rule router output to official runtime label or production judgment
- report rule-router output as accuracy or final model metric

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- user-provided task document from Downloads

### Code / Scripts

- `src/warden/l1/rule_baseline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/explanation_renderer.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`

### Data / Artifacts

- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv` for bounded benign smoke

### Prior Handoff

- `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`

### Missing Inputs

- none blocking

## 6. Required Outputs

This task should produce:

- updated L1 router-style draft output
- updated benchmark routing-semantics report
- updated targeted tests
- this repo task doc
- repo handoff doc

Output format requirements:

- L1 draft sidecar must include `draft=true` and `not_final_schema=true`.
- L1 draft result must include `rule_router`, `text_semantic_concepts`, `vision_evidence`, `decision_head`, `evidence_ledger`, and `explanation`.
- `decision_head.final_label`, `risk_score`, `confidence`, `malicious_basis`, and `payload_observed` must be null while the decision head is not run.

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

- rule baseline must not emit final-like `benign`, `suspicious`, or `malicious` labels
- high-risk can only be represented as `high_risk_candidate`
- low-risk can only be represented as `low_risk_candidate` or evidence sufficiency status
- explanations must not say the page is malicious or benign
- benchmark must report routing and rule-assessment distributions, not accuracy-like label distribution

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- official runtime `final_stage`, `terminal_routing`, `routing_outcome`, and `stage_sequence`
- feature flag behavior for `WARDEN_ENABLE_L1_DRAFT`
- existing sample and manifest inputs

Schema / field constraints:

- Schema changed allowed: NO for official runtime schema
- If yes, required compatibility plan: not applicable
- Frozen field names involved: official runtime result fields must remain unchanged

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py` with existing manifest flags

Downstream consumers to watch:

- L1 draft sidecar consumers
- future L1 Decision Head integration

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- current rule baseline emits final-like fields
- benchmark currently reports label distribution
- runtime bridge keeps draft sidecar debug-only and errors non-fatal
- official runtime fields are unchanged after flag-on versus flag-off run

Allowed evidence sources:

- current repository files
- targeted tests and smoke outputs
- user-provided task file

Retrieval budget:

- Initial retrieval: task file, current L1 modules, runtime bridge, runtime pipeline, benchmark script, targeted tests
- Additional retrieval is allowed only for validation failures or doc checker requirements
- Stop retrieval when the implementation and validation evidence cover acceptance criteria

Missing-evidence behavior:

- mark unsupported claims as risks or not run

### 9.1 Counter-Review Requirements

Current proposed framing:

Rule baseline must be demoted from temporary classifier to router / diagnostic; future final label belongs to L1 Decision Head.

Hidden assumptions to check:

- removing top-level final-like rule fields does not break official runtime fields
- benchmark can inspect sidecar result without treating it as accuracy
- tests can detect final-like label leakage

Failure modes to consider:

- keeping hidden `label` fields in nested router output
- leaving benchmark label distribution text in reports
- explanations still implying final malicious or benign judgment
- decision head fields accidentally populated by rule router values

Counterexamples or contradictory cases to search for:

- benign pages with action surfaces
- sparse pages requiring visual evidence
- high-risk candidates needing model judgment or review

Alternative routes to compare:

- preserve old fields for compatibility but null them
- remove top-level fields entirely and expose nulls only under `decision_head`
- wire decision head stub as a separate component

Required evidence before accepting the framing:

- task explicitly requires rule baseline not to emit final-like labels
- runtime official fields stay unchanged in tests
- benchmark reports routing/assessment metrics and leakage warning count

Decision rule:

- Accept revised output shape if official runtime fields remain unchanged and final-like rule-label leakage is zero.
- Stop and escalate if existing consumers require final-like rule labels as a stable interface.

Output discipline:

- Report facts from commands separately from recommendations and risks.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Assumptions allowed for this task: L1 draft sidecar shape may change because it is marked draft and not final schema
- Ambiguities that require clarification before execution: any need to change official runtime fields, labels, manifests, dependencies, or production judgment
- Multiple plausible interpretations considered: null old fields or remove top-level fields
- Chosen interpretation and reason: remove top-level rule `label` and keep null final-like fields only under `decision_head`

Simplicity boundary:

- Simplest acceptable solution: update rule router output, runner shape, explanation text, benchmark metrics, and targeted tests
- Complexity budget: no new dependencies, no model integrations, no broad runtime refactor
- Speculative features explicitly forbidden: training, model scoring, accuracy claims, final schema freeze
- New abstractions / dependencies allowed: no new third-party dependencies

Surgical change boundary:

- Every touched file must map to a listed scope item.
- Adjacent cleanup policy: no unrelated cleanup.
- Formatting-only changes allowed: only in touched task files.
- Orphan cleanup allowed only for artifacts made obsolete by this task: no.

Goal-driven verification loop:

- final-like labels removed from rule baseline output -> targeted pytest
- decision head not run -> targeted pytest
- benchmark routing metrics -> targeted pytest and bounded smoke
- official runtime fields unchanged -> targeted runtime integration pytest

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

- [ ] rule baseline no longer emits final-like benign / malicious / suspicious labels
- [ ] L1 draft sidecar separates rule router, text concepts, vision evidence, and decision head
- [ ] decision head is `not_run`
- [ ] explanations are routing diagnostics
- [ ] benchmark reports routing / assessment distributions
- [ ] official runtime output remains unchanged unless draft sidecar flag is enabled
- [ ] targeted tests, doc checkers, and bounded benign smoke pass

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted unit and integration tests
- [ ] bounded benign runtime smoke
- [ ] doc checker validation
- [ ] changed-file scope inspection

Commands to run if applicable:

```bash
python -m py_compile src/warden/l1/rule_baseline.py src/warden/l1/l1_runner.py src/warden/l1/explanation_renderer.py src/warden/runtime/l1_draft_bridge.py scripts/l1/run_l1_draft_mixed_runtime_benchmark.py
pytest tests/infer/test_l1_pipeline_skeleton.py tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md
python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_routing_semantics_v1" --limit-per-bucket 25 --seed 42
```

Expected evidence to capture:

- command outputs and exit status
- benchmark report metrics
- final-like label leakage warning count

If validation cannot be run:

- Not run: exact command
- Reason: exact blocker
- Next best check: exact fallback

## 12. Stop Rules

The executor should stop and report completion when all of the following are true:

- rule router semantics are implemented
- decision head is clearly not run
- benchmark routing metrics and leakage warning count are available
- targeted tests and doc checks pass

The executor should stop and escalate instead of continuing when any of the following happens:

- official runtime schema must change
- labels, manifests, samples, or split logic must change
- model training or heavy inference becomes necessary
- validation fails for an unclear reason

## 13. Suggested Execution Notes

Recommended order:

1. Read current task and affected files.
2. Update tests first and confirm RED.
3. Apply minimal implementation changes.
4. Run targeted validation and bounded smoke.
5. Write handoff with actual evidence.

Task-specific execution notes:

- Preserve runtime bridge exception behavior.
- Keep `WARDEN_ENABLE_L1_DRAFT` default off.
- Keep explanations deterministic.

## 14. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- rule router output changes
- L1 draft sidecar shape
- benchmark metric changes
- runtime official-field compatibility
- validation results
- explicit statement that no training, teacher, OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like path was run

Repo handoff path if one should be created:

- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`

## 15. Open Questions / Blocking Issues

- none
