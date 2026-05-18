# Task Metadata

- Task ID: TASK-20260515-WARDEN-DISTILLATION-PROMPT-MOCK-OUTPUT-CONCEPT-ALIGNMENT-V1
- Task Title: Align Distillation Prompts And Mock Output Shape With L1 Text Semantic Concept Contract
- Owner Role: Codex executor
- Priority: P0
- Status: TODO
- Related Module: Distillation / L1 / Text Concepts / Mock Runner
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\TASK_20260515_WARDEN_DISTILLATION_PROMPT_MOCK_OUTPUT_CONCEPT_ALIGNMENT_V1.md`
- Created At: 2026-05-15
- Requested By: Project owner
- Karpathy Guardrails Required: YES

## 中文版

### 1. 背景

Warden 已新增 L1 Text Semantic Concept Contract。当前 distillation prompt、schema reference 和 mock runner output shape 需要同步到该合同，避免 future teacher output、mock output、text tower target 和 Decision Head input 语义不一致。

### 2. 目标

把 distillation workflow、prompt pack、Skill schema reference、mock teacher output、schema validator、review queue、audit/report、inspection helper 和 focused tests 对齐到最新 concept contract。

### 3. Scope In

- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/**`
- `src/warden/distillation/**`
- `scripts/distillation/**`
- `tests/**/distillation*`
- `docs/tasks/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md`
- `docs/handoff/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md`

### 4. Scope Out

禁止调用真实 teacher API、正式蒸馏、训练模型、运行 OCR / YOLO / CLIP / SNet、修改 runtime official schema、label enum、dataset samples、manifest、split 或 production inference behavior。

### 5. Required Outputs

- updated prompt / schema reference docs;
- updated mock output shape;
- updated validator and inspection/report readiness checks;
- focused tests;
- mock-only smoke output;
- handoff.

### 6. Validation Checklist

- task doc checker;
- handoff checker;
- `py_compile` for runner / validator / mock teacher;
- targeted distillation pytest;
- small mock-only smoke;
- output inspection confirming zero external / real teacher / OCR / YOLO / CLIP calls and no missing required concept fields;
- required-term grep.

## English Version

> AI note: This English section is authoritative.

## 1. Background

Warden now has an active L1 Text Semantic Concept Contract. Distillation prompts, draft schema references, and the mock runner output shape must align with that contract so future teacher outputs, mock records, text tower targets, and Decision Head inputs use the same concept groups.

## 2. Goal

Align distillation workflow docs, prompt pack docs, Claude Code Skill references/templates, draft distillation schema reference, mock teacher output shape, schema validator, review queue, audit/report fields, inspection helper, and focused tests with the L1 concept contract.

## 3. Scope In

This task is allowed to touch:

- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/**`
- `src/warden/distillation/**`
- `scripts/distillation/**`
- `tests/**/distillation*`
- `docs/tasks/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md`
- `docs/handoff/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md`

Allowed changes:

- prompt / schema reference alignment;
- mock output shape alignment;
- validator required-field checks;
- review queue / audit / report / inspection concept-readiness fields;
- focused tests and mock-only smoke output.

## 4. Scope Out

This task must not:

- call real teacher APIs;
- run official teacher distillation;
- train text tower or Decision Head;
- run OCR / YOLO / CLIP / SNet;
- change official runtime schema;
- change production inference output;
- change Warden label enum;
- change dataset samples, manifests, or splits;
- produce gold labels;
- use val/test teacher output for training, tuning, threshold selection, or model selection.

## 5. Inputs

Relevant inputs:

- `C:\Users\20516\Downloads\TASK_20260515_WARDEN_DISTILLATION_PROMPT_MOCK_OUTPUT_CONCEPT_ALIGNMENT_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`
- current distillation docs, Skill references/templates, mock runner, validator, inspection helper, and tests.

Missing inputs:

- none material for mock-only alignment.

## 6. Required Outputs

- repo-local task doc;
- updated distillation docs and prompt templates;
- updated mock output shape including required concept groups;
- validator checks for missing concept fields;
- review queue / audit / report / inspection concept-level readiness fields;
- focused test updates;
- repo handoff.

## 7. Hard Constraints

- Keep outputs mock-only / diagnostic-only / non-gold.
- Keep `teacher_model=mock_teacher_v0`.
- Keep `do_not_train_as_gold=true`.
- Keep `diagnostic_only=true`.
- Preserve `external_api_calls=0`, `ocr_calls=0`, `yolo_calls=0`, `clip_calls=0`, and `real_teacher_calls=0`.
- Preserve `rule_router` as routing / evidence-sufficiency diagnostic only.
- Preserve `rule_router is not a teacher label source`.
- Preserve `action surface is not automatically threat action`.
- Preserve `payload not observed is not automatic benign`.
- Preserve `unknown relation is not malicious`.

## 8. Interface / Schema Constraints

- Official runtime schema changed: no.
- Draft mock output shape change allowed: yes.
- Backward compatibility requirement: existing mock CLI must keep working.
- Frozen label enum changed: no.
- Dataset / manifest / split changed: no.

## 10. Acceptance Criteria

- Prompt pack is aligned to L1 text semantic concept contract.
- Draft schema reference and mock output include `claimed_identity_candidates`, `text_semantic_concepts.identity_claim`, `text_semantic_concepts.action_surface`, `text_semantic_concepts.behavior_context`, `text_semantic_concepts.relation_judgments`, `text_semantic_concepts.evidence_state`, `text_semantic_concepts.threat_action_candidate`, and `decision_head_auxiliary_targets`.
- Validator rejects missing required concept groups.
- Review queue / audit / report expose concept-level readiness.
- Mock-only smoke output is schema-valid.
- No real API / OCR / YOLO / CLIP / SNet calls occur.
- Task checker and handoff checker pass.

## 11. Validation Checklist

Run:

```powershell
python -m py_compile scripts/distillation/run_distillation_skeleton.py
python -m py_compile src/warden/distillation/schema_validator.py
python -m py_compile src/warden/distillation/mock_teacher.py
pytest tests/distillation -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-15_warden_distillation_prompt_mock_output_concept_alignment_v1.md
python scripts/distillation/run_distillation_skeleton.py --manifest "E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv" --output-dir "E:\WardenData\manifests\distillation_concept_alignment_smoke_v1" --limit 10 --mode mock --split train --overwrite
python scripts/distillation/inspect_distillation_runner_outputs.py --output-dir "E:\WardenData\manifests\distillation_concept_alignment_smoke_v1" --pretty
```

Expected checks:

- records parse ok;
- `schema_valid_count == processed_count`;
- `schema_invalid_count == 0`;
- `do_not_train_as_gold_failures == 0`;
- `diagnostic_only_failures == 0`;
- missing required concept field count is zero;
- `external_api_calls == 0`;
- `ocr_calls == 0`;
- `yolo_calls == 0`;
- `clip_calls == 0`;
- `real_teacher_calls == 0`.

## 12. Stop Rules

Stop as complete when docs, prompt templates, mock output shape, validator checks, review/audit/report/inspection readiness, focused tests, mock-only smoke, task checker, and handoff checker pass.

Stop and escalate if completion would require a real teacher API call, official runtime schema change, label enum change, dataset split change, production training / inference change, or concept contract conflict.
