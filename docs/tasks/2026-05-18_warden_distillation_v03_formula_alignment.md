# Task Metadata

- Task ID: WARDEN-TASK-20260518-DISTILLATION-V03-FORMULA-ALIGNMENT
- Task Title: Refocus Warden Distillation V0.3 Around V1 Threat Formula
- Owner Role: Codex
- Priority: HIGH
- Status: DONE
- Related Module: distillation / prompt templates / L1 semantic concepts / evidence pack contract
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FORMULA_ALIGNMENT.md`
- Created At: 2026-05-18
- Requested By: Project owner

## 中文版

本任务用于把 Warden distillation spec 和 prompt templates 从 V0.2 L1-aligned 语义升级为 V0.3 formula-aligned 语义。执行边界是 documentation / prompt-template contract only，不允许修改 runtime、training、schema、label enum、manifest、dataset、Python 代码或 JSON/YAML 生产输出合同。

## English Version

## 1. Background

Warden V1 threat semantics are now defined by:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

Existing distillation V0.2 docs and templates still contain older L1-aligned wording such as broad action surfaces, `rule_router_context`, `possible_cloak_or_gate`, `suspicious`, and older advisory-basis values. This task creates a V0.3 documentation and prompt-template layer that aligns teacher outputs with the final V1 formula.

## 2. Goal

Create documentation and prompt-contract updates so Warden distillation teachers produce formula-aligned structured targets around `ManipulativeContext`, `InducedHighRiskAction`, the context-action relation, evidence sufficiency, and the final formula result.

Expected outcome:

- V0.3 distillation docs supersede V0.2 for current Warden V1 formula semantics.
- Prompt templates require formula-aligned structured output.
- `rule_router_context` is downgraded to legacy optional / non-label context.
- Out-of-V1-scope categories are not promoted to Web-SE threat targets.
- `suspicious` is not a V1 training target.
- OCR / YOLO remain conditional evidence recovery only.
- No runtime, schema, CLI, model API, training, dataset, manifest, or sample files are changed.

## 3. Scope In

Allowed files:

- `docs/distillation/*.md`
- `.claude/skills/warden-distillation/templates/*.md`
- `docs/tasks/2026-05-18_warden_distillation_v03_formula_alignment.md`
- `docs/handoff/2026-05-18_warden_distillation_v03_formula_alignment.md`

## 4. Scope Out

Do not modify:

- production runner implementation;
- teacher adapter implementation;
- model API call logic;
- training ingestion code;
- inference/runtime code;
- L1, L0, or L2 implementation code;
- OCR / YOLO implementation;
- CLIP / MobileCLIP / SNet code;
- dataset manifests;
- label enums;
- official runtime schemas;
- JSON/YAML output contracts outside documentation-only schema-delta text;
- actual data samples.

Do not run teacher distillation, model API calls, OCR, YOLO, CLIP, training, or evaluation jobs.

## 5. Inputs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FORMULA_ALIGNMENT.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- Existing distillation V0.2 docs and prompt templates.
- Current Warden V1 architecture and threat-formula docs.

## 6. Required Outputs

- V0.3 distillation workflow doc.
- V0.3 prompt-pack doc.
- V0.3 schema-delta documentation only.
- Runner-design addendum for V1 scope and Evidence Pack visibility.
- Formula-aligned updates to allowed prompt templates.
- New handoff document.

## 7. Hard Constraints

- Do not run teacher model calls.
- Do not create teacher labels.
- Do not run OCR / YOLO / CLIP.
- Do not modify runtime code.
- Do not modify training code.
- Do not modify official schema or label enums.
- Do not change dataset manifests or samples.
- Do not use val/test teacher outputs for training, prompt tuning, threshold selection, model selection, acceptance metrics, or final claims.

## 8. Interface / Schema Constraints

- Production/runtime schema changed: no.
- Label enum changed: no.
- CLI changed: no.
- JSON/YAML production output contracts changed: no.
- V0.3 schema delta is documentation only and must not be treated as implementation.

## 9. Evidence / Retrieval Rules

Search active distillation docs and prompt templates for:

```text
rule_router
rule_router_context
possible_cloak_or_gate
suspicious
malicious_basis_advisory
final_label_advisory
action_surface
threat_action_candidate
vision_evidence
OCR
YOLO
CLIP
MobileCLIP
SNet
SpecularNet
gate
evasion
adult
gambling
EvidenceSufficient
ManipulativeContext
InducedHighRiskAction
DirectAction
RoutedAction
ActionPreparation
```

Stop retrieval when all active distillation docs and prompt templates containing those terms have been inspected and patched or explicitly classified as compatible residuals.

Counter-review requirements:

Check:

- whether V0.2 docs should be patched directly or superseded by V0.3 docs;
- whether `rule_router_context` is still default teacher-visible context;
- whether `suspicious` remains in training-target wording;
- whether out-of-scope categories can still be interpreted as V1 malicious classes;
- whether OCR / YOLO wording implies always-on vision or standalone visual classification;
- whether any required change would cross into runtime, schema, label, training, or data scope.

Implementation plan:

1. Create V0.3 distillation workflow and prompt-pack docs.
2. Create a V0.3 schema-delta doc instead of modifying official runtime schema.
3. Create a runner-design addendum clarifying V1 scope, evidence-pack visibility, and non-default router context.
4. Patch prompt templates in place with formula-aligned output constraints.
5. Add a handoff documenting changes, validation, and residual risks.

## 10. Acceptance Criteria

- V0.3 docs contain the final threat formula.
- V0.3 docs define `manipulative_context`, `action_surface`, `induced_high_risk_action`, `context_action_relation`, `evidence_sufficiency`, and `formula_result`.
- V0.3 docs state `action_surface != induced_high_risk_action`.
- V0.3 docs define out-of-V1-scope categories and require non-gold diagnostic handling.
- V0.3 docs replace normal `possible_cloak_or_gate` use with precise diagnostic / out-of-scope flags.
- V0.3 docs remove `suspicious` as a V1 training target and allow only diagnostic-only unknown / out-of-scope values.
- Prompt templates preserve JSON-only, no hidden chain-of-thought, short evidence quotes, split safety, and visual-modality guardrails.
- Validation confirms no Python, JSON, YAML, runtime, schema, manifest, training, or data files were changed by this task.

## 11. Validation Checklist

Run:

```powershell
rg -n "EvidenceSufficient|ManipulativeContext|InducedHighRiskAction|DirectAction|RoutedAction|ActionPreparation" docs\distillation .claude\skills -g "*.md"
rg -n "possible_cloak_or_gate|suspicious|malicious_basis_advisory|final_label_advisory|rule_router_context|action_surface|threat_action_candidate" docs\distillation .claude\skills -g "*.md"
rg -n "adult|gambling|gate|evasion|redirect-only|trusted-sink|CLIP|MobileCLIP|SNet|SpecularNet|OCR|YOLO" docs\distillation .claude\skills -g "*.md"
git diff --name-only -- docs\distillation .claude\skills docs\tasks docs\handoff | rg "\.(py|json|ya?ml)$"
python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_warden_distillation_v03_formula_alignment.md
python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_warden_distillation_v03_formula_alignment.md
```

If any Python / JSON / YAML file is changed, stop and report why.

## 12. Stop Rules

Stop when:

- the V0.3 formula-aligned distillation contract is documented;
- prompt templates use the formula-driven teacher flow;
- out-of-V1-scope and diagnostic-only rules are explicit;
- validation commands have been run and reported;
- no runtime/schema/training/data files were changed.

Stop and report without editing further if a required change needs schema enum changes, runner implementation, actual teacher calls, or repository files are missing in a way that changes scope.
