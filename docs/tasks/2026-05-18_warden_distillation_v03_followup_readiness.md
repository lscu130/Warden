# Task Metadata

- Task ID: WARDEN-TASK-20260518-DISTILLATION-V03-FOLLOWUP-READINESS
- Task Title: Align Warden Distillation V0.3 Skill Entrypoint And Mock-Only Runner / Validator
- Owner Role: Codex
- Priority: HIGH
- Status: DONE
- Related Module: distillation / Claude Skill / mock runner / schema validator / tests
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FOLLOWUP_READINESS.md`
- Created At: 2026-05-18
- Requested By: User

## 中文版

本任务把 Warden Distillation V0.3 从文档 / prompt-template contract 扩展到 Skill 入口和 mock-only runner / validator 层。执行边界是 mock-only：不允许真实 teacher/API/OCR/YOLO/CLIP 调用，不允许训练接入，不允许 production runtime schema、正式 label enum、manifest 或 dataset 变更。

## English Version

## 1. Background

The previous V0.3 handoff established a documentation and prompt-template baseline. Follow-up readiness gaps remained in the Skill entrypoint and the mock runner / validator layer.

The V0.3 formula is:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

## 2. Goal

Align the Warden distillation Skill entrypoint, V0.2 reference status, mock schema, mock teacher output, validator, runner audit/report, inspection helper, and tests with the V0.3 formula contract while preserving mock-only, diagnostic-only, non-gold, zero-call safety.

## 3. Scope In

Allowed files:

- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/runner.py`
- `src/warden/distillation/audit_log.py`
- `tests/distillation/*`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `docs/tasks/2026-05-18_warden_distillation_v03_followup_readiness.md`
- `docs/handoff/2026-05-18_warden_distillation_v03_followup_readiness.md`

Note: `src/warden/distillation/audit_log.py` is included because the task requires audit/report output to expose V0.3 schema, prompt/schema version, validation summary, review reason counts, and zero-call counters.

## 4. Scope Out

Do not:

- call any real teacher model;
- call any external API;
- run OCR, YOLO, or CLIP;
- connect outputs to training;
- change production runtime schema;
- change formal label enums;
- change manifests;
- change dataset samples;
- change L1 runtime inference;
- change the Evidence Pack Builder implementation;
- change the online pipeline;
- integrate a real MiMo / DeepSeek / OpenAI / Claude adapter;
- mark any mock output as gold;
- restore `suspicious` as a V1 training target;
- restore `possible_cloak_or_gate` as a V0.3 default output field;
- restore `rule_router_context` as a teacher-visible label hint.

## 5. Inputs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_FOLLOWUP_READINESS.md`
- `docs/handoff/2026-05-18_warden_distillation_v03_formula_alignment.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_SCHEMA_DELTA_V0.3.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1_ADDENDUM_V1_SCOPE.md`
- current Skill, schema reference, mock runner, validator, inspection helper, and tests.

## 6. Required Outputs

- Updated Skill entrypoint declaring V0.3 as default.
- Updated V0.2 reference marking it historical / compatibility-only.
- Updated V0.3 mock output shape and constants.
- Updated V0.3 validator checks.
- Updated audit/report and inspection helper readiness checks.
- Updated mock-only tests.
- New task and handoff docs.

## 7. Hard Constraints

- No real teacher calls.
- No external API calls.
- No OCR calls.
- No YOLO calls.
- No CLIP calls.
- No training ingestion.
- No production runtime schema changes.
- No formal label enum changes.
- No manifest changes.
- No dataset changes.
- All mock outputs remain diagnostic-only and non-gold.

## 8. Interface / Schema Constraints

- Production runtime schema changed: no.
- Distillation mock schema changed: yes, from V0.2 mock to V0.3 mock.
- Backward compatibility: production interfaces unchanged; V0.2 reference preserved as historical / compatibility.
- CLI changed: no.
- Manifest fields changed: no.

## 9. Evidence / Retrieval Rules

Required evidence:

- search current V0.3 / V0.2 wording;
- inspect mock output fields and validator checks;
- run `pytest tests/distillation -q`;
- run a mock-only runner smoke if the script exists;
- inspect mock output with `inspect_distillation_runner_outputs.py`;
- run task / handoff checkers;
- verify no production runtime/schema/label/manifest/dataset files were changed.

Counter-review:

- This is a mock-only readiness task, not real-adapter readiness.
- If production schema, training, manifest, dataset, or real API changes are needed, stop and report.

## 10. Acceptance Criteria

- `SKILL.md` states V0.3 is the current default distillation semantic contract.
- V0.2 reference is historical / compatibility-only.
- Mock outputs include `formula_semantics` and `formula_concepts`.
- Mock outputs include the V0.3 formula groups.
- Validator rejects missing required V0.3 groups.
- Review reasons use V0.3 taxonomy.
- Audit/report expose schema version, prompt template version, validation summary, review reason counts, and zero-call counters.
- Tests pass.
- Mock smoke confirms zero real teacher/API/OCR/YOLO/CLIP calls.

## 11. Validation Checklist

Run:

```powershell
rg -n "V0.3|warden_distill_v0.3|EvidenceSufficient|ManipulativeContext|InducedHighRiskAction|DirectAction|RoutedAction|ActionPreparation" .claude\skills\warden-distillation docs\distillation src\warden\distillation tests\distillation -g "*.md" -g "*.py"
rg -n "possible_cloak_or_gate|suspicious|malicious_basis_advisory|rule_router_context|warden_distill_v0.2" .claude\skills\warden-distillation src\warden\distillation tests\distillation -g "*.md" -g "*.py"
pytest tests/distillation -q
python scripts\distillation\run_distillation_skeleton.py --manifest <small_manifest> --output-dir <mock_output_dir> --split train --mode mock --limit 1 --seed 42 --overwrite
python scripts\distillation\inspect_distillation_runner_outputs.py --output-dir <mock_output_dir> --pretty
python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_warden_distillation_v03_followup_readiness.md
python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_warden_distillation_v03_followup_readiness.md
```

## 12. Stop Rules

Stop when:

- Skill entrypoint is aligned to V0.3;
- mock runner / validator / tests represent and validate V0.3;
- zero-call invariants are verified;
- checkers pass;
- handoff records unrun or unavailable checks honestly.

Stop and report if any required change needs real teacher/API/OCR/YOLO/CLIP calls, production runtime schema changes, formal label enum / manifest / dataset changes, or training ingestion.
