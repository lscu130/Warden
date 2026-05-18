# Handoff Metadata

- Handoff ID: HANDOFF_20260518_DISTILLATION_V03_FORMULA_ALIGNMENT
- Related Task ID: WARDEN-TASK-20260518-DISTILLATION-V03-FORMULA-ALIGNMENT
- Task Title: Refocus Warden Distillation V0.3 Around V1 Threat Formula
- Module: distillation / prompt templates / L1 semantic concepts / evidence pack contract
- Author: Codex
- Date: 2026-05-18
- Status: DONE

## 中文版

本次交付按 `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FORMULA_ALIGNMENT.md` 执行，把 Warden distillation spec 层从 V0.2 L1-aligned 语义升级为 V0.3 formula-aligned 语义。

核心公式已写入 V0.3 docs 和 prompt templates：

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

本次没有修改 runtime、training、schema、label enum、manifest、dataset、Python 代码、JSON/YAML 输出合同，也没有运行 teacher、OCR、YOLO、CLIP、训练或评估。

## English Version

AI note: English is authoritative for exact validation, compatibility, and residual-risk statements.

## 1. Executive Summary

Warden distillation documentation and prompt-template contracts were refocused to V0.3 around the Warden V1 formula:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

V0.3 supersedes V0.2 for current formula-aligned distillation semantics while preserving still-valid V0.2 safety principles: JSON-only output, no hidden chain-of-thought, short evidence quotes, non-gold teacher output, train-only official distillation, val/test diagnostic-only use, and modality honesty.

The task reached its documentation/prompt-contract stop condition. No runtime implementation, production schema, label enum, manifest, dataset, training, inference, model API call, OCR, YOLO, CLIP, or evaluation job was changed or run.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added V0.3 workflow documentation.
- Added V0.3 prompt-pack documentation.
- Added a V0.3 schema-delta documentation file instead of modifying official runtime schema.
- Added a runner-design addendum clarifying V1 scope, Evidence Pack visibility, and non-default router context.
- Added a repo-local task document for checker-facing workflow compliance.
- Added this handoff document.
- Added supersession notes to V0.2 workflow and prompt docs so V0.2 remains historical / compatibility context rather than current formula semantics.

### Prompt Template Changes

- Updated the five allowed prompt templates to use `warden_distill_v0.3` / V0.3 packet wording.
- Added the final Warden V1 formula to teacher, fallback, judge, repair, and human-review templates.
- Added formula-aligned output groups: `manipulative_context`, `action_surface`, `induced_high_risk_action`, `context_action_relation`, `evidence_sufficiency`, and `formula_result`.
- Replaced normal `possible_cloak_or_gate` output in templates with more precise V0.3 diagnostic / out-of-scope flags.
- Removed teacher-visible weak-label / human-label / split values from the primary and fallback prompt input packets; those remain metadata outside teacher-visible evidence by default.

## 3. Files Touched

- `docs/tasks/2026-05-18_warden_distillation_v03_formula_alignment.md`
- `docs/handoff/2026-05-18_warden_distillation_v03_formula_alignment.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_SCHEMA_DELTA_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1_ADDENDUM_V1_SCOPE.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`
- `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`
- `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`

Note: the worktree already had unrelated dirty files before this task, including distillation code/tests, `.claude/skills/warden-distillation/SKILL.md`, `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`, and broader Warden docs. They were not reverted.

## 4. Behavior Impact

### Expected New Behavior

- Documentation readers should treat V0.3 as the current Warden V1 distillation semantic contract.
- Teacher prompts should target formula-aligned concepts rather than broad "malicious-looking page" judgment.
- `action_surface` is explicitly separated from `induced_high_risk_action`.
- `rule_router_context` is downgraded to legacy optional context and is not a label source, teacher label source, or final judgment.
- Adult-content-only, gambling-content-only, gate-only, evasion-only, redirect-only, and trusted-sink-only samples are out of V1 main scope unless downstream observable evidence satisfies the formula.
- `suspicious` is not a V1 training target; unknown / out-of-scope values are diagnostic-only and non-gold.

### Preserved Behavior

- V0.2 safety principles remain preserved.
- Existing V0.2 docs remain available as historical / compatibility context.
- Existing runner implementation behavior is unchanged.
- Existing schema, CLI, labels, manifests, JSON/YAML outputs, and dataset samples are unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for production/runtime outputs
- documentation-only schema delta added for distillation teacher-output contracts

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none in production/runtime schema
- V0.3 distillation schema-delta documentation only

Compatibility notes:

V0.3 prompt templates and docs refer to `warden_distill_v0.3` as a distillation teacher-output contract. This is not an official runtime schema change and does not modify Python schema validators or JSON/YAML production outputs.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- user-provided task: `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FORMULA_ALIGNMENT.md`
- `AGENTS.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md`
- `.claude/skills/warden-distillation/templates/*.md`

Retrieval / reading performed:

- Searched distillation docs and `.claude/skills` markdown for router, QC, advisory, visual, formula, and out-of-scope terms required by the task.
- Inspected existing V0.2 docs and prompt templates before editing.
- Checked current worktree status before editing and treated pre-existing dirty files as unrelated unless they were in this task's scope.

Counter-review performed:

- Fact: the task requires documentation and prompt-template contract updates only.
- Fact: no V0.3 distillation docs existed before this task.
- Fact: V0.2 docs still called themselves current before patching.
- Fact: existing prompt templates exposed older V0.2 fields and `possible_cloak_or_gate`.
- Inference: creating V0.3 docs and adding V0.2 supersession notes is safer than rewriting V0.2 history in place.
- Inference: schema-delta documentation is the correct route because production schema changes are out of scope.
- Risk considered: leaving split / weak-label / human-label values in primary teacher-visible prompt input could bias teacher output.
- Alternative rejected: modifying Python schema / runner / validators, because the task explicitly forbids implementation, schema, training, and runtime changes.

## 6. Validation Performed

### Commands Run

```powershell
rg -n "rule_router|rule_router_context|possible_cloak_or_gate|suspicious|malicious_basis_advisory|final_label_advisory|action_surface|threat_action_candidate|vision_evidence|OCR|YOLO|CLIP|MobileCLIP|SNet|SpecularNet|gate|evasion|adult|gambling|EvidenceSufficient|ManipulativeContext|InducedHighRiskAction|DirectAction|RoutedAction|ActionPreparation" docs\distillation .claude\skills\warden-distillation -g "*.md"
rg -n "EvidenceSufficient|ManipulativeContext|InducedHighRiskAction|DirectAction|RoutedAction|ActionPreparation" docs\distillation .claude\skills -g "*.md"
rg -n "possible_cloak_or_gate|suspicious|malicious_basis_advisory|final_label_advisory|rule_router_context|action_surface|threat_action_candidate" docs\distillation .claude\skills -g "*.md"
rg -n "adult|gambling|gate|evasion|redirect-only|trusted-sink|CLIP|MobileCLIP|SNet|SpecularNet|OCR|YOLO" docs\distillation .claude\skills -g "*.md"
git diff --name-only -- docs\distillation .claude\skills docs\tasks docs\handoff | rg "\.(py|json|ya?ml)$"
python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_warden_distillation_v03_formula_alignment.md
python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_warden_distillation_v03_formula_alignment.md
```

### Result

- Required formula terms are present in V0.3 docs and all five prompt templates.
- Required V0.3 target groups are documented.
- `action_surface != induced_high_risk_action` is documented and present in templates.
- V1 out-of-scope categories and diagnostic-only handling are documented.
- `rule_router_context` is documented as legacy optional / non-label / non-final context.
- Prompt templates no longer emit normal `possible_cloak_or_gate`; they use V0.3 diagnostic / out-of-scope flags.
- Residual `possible_cloak_or_gate`, `suspicious`, older advisory, and V0.2 schema hits remain in V0.2 historical docs, the runner output inspection report, `.claude/skills/warden-distillation/SKILL.md`, and `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`. These are classified as historical / compatibility / out-of-scope residuals, not current V0.3 prompt-template output.
- The scoped Python/JSON/YAML changed-file check found no matching changed files.
- Task and handoff checker status: pass.

### Not Run

- unit tests
- runtime smoke tests
- teacher model calls
- OCR / YOLO / CLIP
- training / evaluation jobs
- schema validator tests

Reason:

The accepted task is documentation and prompt-template contract only, and explicitly forbids runtime, schema, model-call, training, evaluation, and data changes.

Next best check:

If a later implementation task upgrades the mock runner or validator to V0.3, run `pytest tests/distillation -q` and a mock-only runner smoke with zero teacher/API/OCR/YOLO/CLIP calls.

## 7. Risks / Caveats

- `.claude/skills/warden-distillation/SKILL.md` and `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md` still contain V0.2 wording. They were not in this task's allowed prompt-template paths.
- Existing Python schema/runner/mock output still refers to V0.2 concepts. This is expected because implementation changes were out of scope.
- V0.3 is now documented as a contract, but no runtime validator enforces it yet.
- The worktree had substantial pre-existing dirty state before this task.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- listed in `## 3. Files Touched`

Doc debt still remaining:

- A future task should update the distillation Skill entrypoint and V0.2 schema reference if the project wants `.claude/skills/warden-distillation` to advertise V0.3 as the default skill-level contract.
- A future implementation task is needed if `src/warden/distillation/*` should emit or validate V0.3 records.

## 9. Recommended Next Step

- Review and accept the V0.3 documentation/prompt-contract update.
- Open a separate mock-only implementation task to align `src/warden/distillation/schema.py`, `mock_teacher.py`, `schema_validator.py`, review queue reasons, audit/report output, and `tests/distillation` with the V0.3 formula contract, while keeping zero real teacher/API/OCR/YOLO/CLIP calls.
