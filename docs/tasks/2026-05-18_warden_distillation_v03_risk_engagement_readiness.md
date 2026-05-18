# Task Metadata

- Task ID: WARDEN-TASK-20260518-DISTILLATION-V03-RISK-ENGAGEMENT-AND-READINESS
- Task Title: Align Warden Distillation V0.3 with Risk-Bearing Engagement Formula and Mock-Only Readiness
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: distillation / prompt templates / Skill entrypoint / schema delta / mock runner / validator / tests
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_RISK_ENGAGEMENT_AND_READINESS.md
- Created At: 2026-05-18
- Requested By: project owner
- Karpathy Guardrails Required: YES

## 中文版

### 摘要

本任务按外部任务单执行 Warden Distillation V0.3 公式升级：把当前 V0.3 distillation 合同从 `ManipulativeContext ∧ InducedHighRiskAction` 对齐到 `ManipulativeContext ∧ RiskBearingEngagement`，并保持 mock-only、diagnostic-only、non-gold、zero-external-call 边界。

### 执行边界

- 只允许修改 distillation 文档、`.claude/skills/warden-distillation` Skill 和模板、mock runner / validator / tests / inspect helper、以及 repo-local task / handoff。
- 不允许修改 production runtime schema、official label enum、dataset manifests、dataset samples、training ingestion、real teacher adapter、OCR、YOLO、CLIP、L1 runtime inference 或 L0 / L2 runtime 模块。
- 不允许执行真实 teacher/API/OCR/YOLO/CLIP/training/evaluation。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

## 1. Background

Warden Distillation V0.3 previously used `InducedHighRiskAction` as the second top-level term in the formula. The current accepted task requires V0.3 to use `RiskBearingEngagement` instead, because the distillation target must cover direct high-risk action, routed high-risk action, action preparation, and deceptive funnel priming while rejecting URL-only or visible-impersonation-only overreach.

## 2. Goal

Align current V0.3 distillation documentation, prompt templates, Skill entrypoint, mock output schema, validator, runner audit readiness, inspection helper, and tests to:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

## 3. Scope In

This task is allowed to touch:

- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_SCHEMA_DELTA_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1_ADDENDUM_V1_SCOPE.md`
- `.claude/skills/warden-distillation/**`
- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/runner.py`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `tests/distillation/*`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- V0.3 distillation formula wording and mock-only field requirements.
- Prompt/template required concept groups.
- Validator enum and required-key checks for mock V0.3 records.
- Mock runner audit/readiness counters and tests.

Expected outcome:

- V0.3 docs/templates/mock records use `RiskBearingEngagement` as the second top-level formula concept.
- `induced_high_risk_action` remains only as compatibility / child concept.
- URL-only brand claim and visible impersonation without funnel affordance are explicitly bounded away from strong V1 positives.
- Mock outputs remain diagnostic-only, non-gold, and zero-external-call.

## 4. Scope Out

This task must NOT do the following:

- Modify production runtime schema, official label enum, dataset manifests, dataset samples, training ingestion, model training code outside mock distillation tests, real teacher adapter, API config, OCR, YOLO, CLIP, L1 runtime inference, or L0 / L2 runtime modules.
- Execute real teacher/API/OCR/YOLO/CLIP calls, training jobs, evaluation jobs, threshold tuning, or model selection.
- Promote mock teacher output into gold labels.
- Introduce new dependencies.

## 5. Inputs

### Docs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_RISK_ENGAGEMENT_AND_READINESS.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- `src/warden/distillation/*.py`
- `scripts/distillation/*.py`
- `tests/distillation/*`

### Data / Artifacts

- Mock smoke artifacts may be written under `.codex_tmp/distillation_v03_risk_engagement_smoke/`.

### Prior Handoff

- Prior V0.3 distillation follow-up artifacts are context only and do not override this task.

### Missing Inputs

- none.

## 6. Required Outputs

This task should produce:

- Updated V0.3 distillation docs/templates and Skill references.
- Updated mock schema/validator/runner/inspect helper/tests.
- Repo-local task wrapper.
- Repo-local handoff.
- Validation command results.

Output format requirements:

- Markdown docs are bilingual with Chinese summary first and English authoritative.
- Final response must report schema/interface impact, validation performed, residual risks, and stop condition.

## 7. Hard Constraints

Must obey all of the following:

- Preserve mock-only, diagnostic-only, non-gold behavior.
- Preserve zero real teacher/API/OCR/YOLO/CLIP calls.
- Do not modify production runtime schema, official labels, manifests, datasets, training, inference, or real adapters.
- Do not add dependencies.
- Keep changes minimal and reversible.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Existing mock runner CLI commands.
- Existing distillation test entrypoints.
- Production runtime schema and label enums.

Schema / field constraints:

- Schema changed allowed: yes, only for `warden_distill_v0.3_mock` distillation mock output.
- Compatibility plan: keep `induced_high_risk_action` as compatibility / child concept while adding `risk_bearing_engagement`.
- Frozen field names involved: no production field rename.

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/distillation/run_distillation_skeleton.py ... --mode mock`
  - `python scripts/distillation/inspect_distillation_runner_outputs.py --output-dir ...`
  - `pytest tests/distillation -q`

Downstream consumers to watch:

- Review queue inspection.
- Future training ingestion must not consume mock output as gold without separate approval.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- Current V0.3 formula references and residual old-formula references.
- Mock-only zero-call behavior.
- Task/handoff checker compliance.

Allowed evidence sources:

- The user-provided task document.
- Current repository files and command output.
- No external web retrieval is required for this implementation task.

Retrieval budget:

- Initial retrieval: task document, governing templates, target docs/templates/code/tests.
- Additional retrieval is allowed only when a failing test, checker, or residual search indicates missing context.
- Stop retrieval when required residual search, tests, smoke, and checker validation are satisfied.

Missing-evidence behavior:

- Report any unverified claim as not run or unsupported.

## 9.1 Counter-Review Requirements

Current proposed framing:

- Replace V0.3 top-level `InducedHighRiskAction` formula term with `RiskBearingEngagement`.

Hidden assumptions to check:

- Existing mock runner can preserve zero-call behavior.
- V0.3 templates can be updated without modifying production schemas.
- V0.2 references can remain historical / compatibility only.

Failure modes to consider:

- Residual prompts still teaching `InducedHighRiskAction` as top-level formula term.
- URL-only brand claims or visible impersonation without funnel affordance become false positives.
- Mock outputs silently become trainable gold labels.

Alternative routes to compare:

- Documentation-only update.
- Mock-only schema/test alignment.
- Production runtime schema change.

Required evidence before accepting the framing:

- Residual `rg` classification.
- Passing distillation tests.
- Mock smoke counters showing zero calls.

Decision rule:

- Accept original framing only if it can be implemented inside the listed mock-only scope.
- Revise framing if a required change would touch production runtime or datasets.
- Stop and escalate if real teacher/API/OCR/YOLO/CLIP calls are required.

## 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Assumption: `RiskBearingEngagement` is the authoritative current V0.3 formula term for this task.
- Ambiguities requiring clarification: none found that would change scope.
- Chosen interpretation: perform the smallest mock-only and docs/templates alignment that satisfies the task.

Simplicity boundary:

- Simplest acceptable solution: targeted docs/template/code/test edits plus repo-local task and handoff.
- Complexity budget: no new modules, no new dependencies, no production integration.
- Speculative features explicitly forbidden: real teacher adapter, OCR/YOLO/CLIP, training/evaluation, runtime inference changes.

Surgical change boundary:

- Every touched file must map to the Scope In list.
- Adjacent cleanup policy: no unrelated cleanup.
- Formatting-only changes allowed: only when needed inside touched paragraphs or JSON examples.

Goal-driven verification loop:

- Formula alignment -> residual search.
- Mock contract alignment -> `pytest tests/distillation -q`.
- Workflow artifacts -> task/handoff checker scripts.
- Zero-call guarantees -> bounded mock smoke and inspect helper.

## 9.3 Model / Agent Runtime Guidance

Target executor:

- Codex

Suggested reasoning effort:

- high, because the task spans docs, prompts, mock schema, validator, tests, and handoff.

Verbosity:

- medium for execution updates and final handoff.

## 10. Acceptance Criteria

- V0.3 docs and templates use `ManipulativeContext ∧ RiskBearingEngagement`.
- `RiskBearingEngagement` has the four required subtypes.
- URL-only brand claim is explicitly not V1 positive.
- Visible impersonation without funnel affordance is not a strong positive.
- Visible impersonation with funnel affordance can support `DeceptiveFunnelPriming`, `RoutedHighRiskAction`, or `ActionPreparation`.
- Skill entrypoint says V0.3 is current default semantic contract.
- V0.2 reference is historical / compatibility only.
- Mock schema / validator / runner / tests are aligned to V0.3.
- Mock outputs remain diagnostic-only and non-gold.
- Teacher/API/OCR/YOLO/CLIP call counters remain zero in mock smoke.
- No out-of-scope production, data, training, inference, or adapter changes are made.

## 11. Validation Checklist

- Run residual search for old and new formula terms.
- Run `pytest tests/distillation -q`.
- Run bounded mock-only smoke and inspect output.
- Run `python scripts/ci/check_task_doc.py` on this task file.
- Run `python scripts/ci/check_handoff_doc.py` on the handoff file.
- Run scope check for out-of-scope runtime/data paths.

## 12. Stop Rules

Stop as done when:

- Acceptance criteria are satisfied and validation is run or honestly reported.

Stop as blocked when:

- A required change would modify production runtime schema, official label enum, manifests, datasets, real teacher/API config, OCR, YOLO, CLIP, training, evaluation, or inference.

Escalate when:

- The mock runner cannot preserve zero-call guarantees or V0.2/V0.3 references cannot be separated with small changes.
