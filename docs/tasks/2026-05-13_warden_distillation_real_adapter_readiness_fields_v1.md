# TASK_20260513_WARDEN_DISTILLATION_REAL_ADAPTER_READINESS_FIELDS_V1

## 中文版

### 摘要

本任务用于在 **mock-only / zero-external-call** 条件下补齐 Warden distillation runner 接入 real teacher adapter 前必须具备的输出字段、attempt/audit/review queue 结构。

本任务不实现 MiMo / DeepSeek / OpenAI / Claude 等真实 teacher adapter，不调用任何外部模型 API，不运行正式 teacher distillation，不生成可训练 teacher labels，不训练，不运行 OCR / YOLO / CLIP / MobileCLIP / SNet / SpecularNet-like，不修改数据、标签、manifest、split、runtime schema、训练、推理、采集、crawler 或 labeling 逻辑。

本任务的核心目标是修复上一轮 schema-readiness inspection 记录的 `BLOCKER` 缺口：稳定样本溯源、manifest/split 安全、teacher/prompt/version 审计、图像模态 guard、schema validation、错误状态和 per-attempt audit。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260513-WARDEN-DISTILLATION-REAL-ADAPTER-READINESS-FIELDS-V1
- Task Title: Add Real-Adapter-Readiness Fields To Distillation Runner Skeleton
- Owner Role: Codex executor, GPT reviewer, human final acceptor
- Priority: P0
- Status: TODO
- Related Module: Distillation / Runner / Schema Readiness
- Related Issue / ADR / Doc: `docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md`, `docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`, `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`, `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- Created At: 2026-05-13
- Requested By: 佶
- Karpathy Guardrails Required: YES

## 1. Background

The Warden distillation runner skeleton can already run in dry-run / mock mode and produce non-gold diagnostic records. A follow-up schema-readiness inspection found that the current mock output is safe as a skeleton smoke artifact, but it is not ready as a real teacher adapter output contract.

All 10 inspected mock records lacked these future-readiness fields:

- `sample_key`
- `source_manifest`
- `source_split`
- `teacher_profile`
- `teacher_run_id`
- `prompt_template_version`
- `image_input_passed_to_teacher`
- `validation`
- `error_status`

Those fields are required before any real teacher adapter is allowed to emit pilot outputs.

## 2. Goal

Extend the distillation runner skeleton output contract while staying strictly mock-only and zero-external-call.

The updated skeleton must emit real-adapter-readiness metadata for provenance, split safety, teacher routing audit, prompt/schema versioning, modality guardrails, structured validation, error status, attempt records, audit/report summaries, and richer review queue rows.

## 3. Scope In

This task is allowed to touch:

- `scripts/distillation/run_distillation_skeleton.py`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `src/warden/distillation/__init__.py`
- `src/warden/distillation/manifest_reader.py`
- `src/warden/distillation/evidence_pack.py`
- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/jsonl_writer.py`
- `src/warden/distillation/resume.py`
- `src/warden/distillation/review_queue.py`
- `src/warden/distillation/audit_log.py`
- `src/warden/distillation/runner.py`
- `tests/distillation/test_distillation_runner_skeleton.py`
- `tests/distillation/test_distillation_real_adapter_readiness_fields.py`
- `docs/tasks/2026-05-13_warden_distillation_real_adapter_readiness_fields_v1.md`
- `docs/handoff/2026-05-13_warden_distillation_real_adapter_readiness_fields_v1.md`

Allowed implementation changes:

- Add stable `sample_key` generation.
- Add per-record `source_manifest` and `source_split`.
- Add mock teacher routing metadata: `teacher_profile`, `teacher_run_id`, `prompt_template_version`.
- Add `image_input_passed_to_teacher=false` for the mock skeleton path.
- Add structured `validation` object.
- Add `error_status`.
- Add `attempts.jsonl` or an equivalent clearly named per-attempt JSONL artifact.
- Add prompt/raw-output/repair path placeholders only when no real external call is made.
- Expand review queue records with priority, evidence context, artifact references, reason taxonomy, and attempt linkage.
- Expand `run_audit.json` and `run_report.md` with output file inventory, review reason counts, duplicate key summary, schema/prompt version, and attempt counts.
- Update focused tests and read-only inspection helper accordingly.
- Add handoff.

## 4. Scope Out

This task must not:

- Call MiMo, DeepSeek, OpenAI, Claude, or any external model API.
- Implement real teacher adapters.
- Run real teacher distillation.
- Generate trainable teacher labels.
- Train any model.
- Run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference.
- Modify source sample directories.
- Modify dataset labels.
- Modify train/val/test splits.
- Modify existing manifests.
- Modify Warden runtime schema.
- Modify production training or inference logic.
- Modify capture, crawler, or labeling logic.
- Promote `warden_distill_v0.2_mock` or `warden_distill_v0.2` to a frozen production schema.
- Allow mock outputs to be consumed as training gold.

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`

### Code / Scripts

- current distillation runner skeleton under `src/warden/distillation/`
- `scripts/distillation/run_distillation_skeleton.py`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `tests/distillation/test_distillation_runner_skeleton.py`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- Use bounded mock smoke output only.
- Recommended smoke input:
  - `E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv`
- Recommended smoke output:
  - `E:\WardenData\manifests\distillation_skeleton_v1_readiness_fields`

### Prior Handoff

- `docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`

### Missing Inputs

- real teacher endpoint details
- final production teacher adapter interface
- final frozen benign + malicious manifests

## 6. Required Outputs

This task should produce:

- updated mock skeleton runner outputs with the real-adapter-readiness fields;
- updated focused tests;
- updated read-only inspection helper;
- `docs/handoff/2026-05-13_warden_distillation_real_adapter_readiness_fields_v1.md`;
- this task doc.

Required output artifacts from the smoke run:

- `distillation_records.jsonl`
- `review_queue.jsonl`
- `attempts.jsonl`
- `run_audit.json`
- `run_report.md`
- `errors.jsonl`

Every record must include at least:

- `sample_key`
- `source_manifest`
- `source_split`
- `teacher_profile`
- `teacher_run_id`
- `prompt_template_version`
- `image_input_passed_to_teacher`
- `validation`
- `error_status`

All records must still include:

- `do_not_train_as_gold=true`
- `diagnostic_only=true`
- `teacher_model=mock_teacher_v0`
- `schema_version=warden_distill_v0.2_mock`

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility for existing skeleton CLI flags.
- Do not rename existing output fields unless explicitly required and documented.
- Do not add third-party dependencies.
- Keep implementation standard-library only.
- Keep outputs non-gold and diagnostic-only.
- Keep all external/model/OCR/YOLO/CLIP call counters at `0`.
- Keep data reads read-only.
- Keep dataset-management metadata out of teacher-visible evidence text.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden manifests, labels, samples, split files, runtime outputs, and CLIs;
- current training, inference, capture, crawler, and labeling code;
- official runtime result / trace schema;
- existing skeleton CLI flags.

Schema / field constraints:

- Schema changed allowed: YES, but only for the mock skeleton output shape.
- Existing production schema changed: NO.
- Existing official runtime schema changed: NO.
- `warden_distill_v0.2_mock` remains draft/mock engineering shape.
- `warden_distill_v0.2` remains draft distillation-output schema.

CLI / output compatibility constraints:

- Existing `run_distillation_skeleton.py` flags must keep working.
- Existing required output files must still be generated.
- New `attempts.jsonl` must be additive.

Downstream consumers to watch:

- future real teacher adapters;
- future train-only teacher output consumers;
- future review queue tooling;
- future Decision Head training tasks.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- prior `BLOCKER` findings;
- current mock output fields;
- current runner design requirements;
- validation command results;
- output artifact invariants.

Allowed evidence sources:

- current task document;
- Warden governing docs and templates;
- current distillation docs and runner design;
- prior inspection report and handoff;
- focused tests and smoke output;
- read-only helper output.

Missing-evidence behavior:

- Do not claim real teacher quality has been validated.
- Do not claim production endpoint behavior has been validated.
- Do not claim production schema is frozen.
- Mark unresolved real-adapter details as future task inputs.

### 9.1 Counter-Review Requirements

Current proposed framing:

Patch the mock skeleton output contract before implementing any real teacher adapter.

Hidden assumptions to check:

- Adding provenance/version/validation fields in mock mode is sufficient preparation for a future real adapter task.
- New fields can be additive without breaking existing skeleton tests.
- `attempts.jsonl` can be introduced without changing production behavior.

Failure modes to consider:

- mock outputs become easier to mistake for trainable labels;
- field names diverge from the runner design contract;
- split/source fields leak into teacher-visible evidence text;
- image modality flags are ambiguous;
- validation object hides failures instead of exposing them;
- attempt records imply real teacher calls happened.

Alternative routes to compare:

- implement real adapter immediately;
- keep current skeleton and document gaps only;
- add readiness fields in mock-only mode first.

Decision rule:

- Accept this task only if all changes remain mock-only, additive, non-gold, diagnostic-only, standard-library-only, and zero-external-call.
- Stop and escalate if real teacher API access, schema freeze, training ingestion, or data mutation becomes necessary.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- The task is implementation work, but only for mock skeleton readiness fields.
- Existing dirty worktree entries outside this task must be left untouched.

Simplicity boundary:

- Add required readiness fields and tests only.
- Do not redesign the whole runner.
- Do not add production adapter abstractions unless needed to express mock metadata.

Surgical change boundary:

- Every touched file must be one of the scope-in paths.

Goal-driven verification loop:

- py_compile verifies syntax.
- targeted pytest verifies behavior.
- bounded mock smoke verifies output artifacts.
- inspection helper verifies required field coverage and invariants.
- task/handoff checkers verify workflow artifacts.
- required grep verifies report/handoff contain zero-external-call and non-gold statements.

## 10. Acceptance Criteria

This task is complete only if:

- [ ] The skeleton remains mock-only and zero-external-call.
- [ ] Existing skeleton CLI flags still work.
- [ ] All records include `sample_key`, `source_manifest`, `source_split`, `teacher_profile`, `teacher_run_id`, `prompt_template_version`, `image_input_passed_to_teacher`, `validation`, and `error_status`.
- [ ] `attempts.jsonl` or equivalent per-attempt JSONL exists.
- [ ] Review queue rows include richer context and link to attempts/records.
- [ ] `run_audit.json` and `run_report.md` include expanded readiness summaries.
- [ ] All records remain `do_not_train_as_gold=true`.
- [ ] All records remain `diagnostic_only=true`.
- [ ] `teacher_calls=0`, `external_api_calls=0`, `ocr_calls=0`, `yolo_calls=0`, and `clip_calls=0`.
- [ ] No forbidden gold-label or hidden-reasoning fields exist.
- [ ] Focused tests pass.
- [ ] Smoke run passes on a bounded manifest slice.
- [ ] Inspection helper reports no missing future-readiness fields for the new output.
- [ ] Task doc checker passes.
- [ ] Handoff checker passes.

## 11. Validation Checklist

Minimum validation expected:

```powershell
python -m py_compile scripts/distillation/run_distillation_skeleton.py scripts/distillation/inspect_distillation_runner_outputs.py src/warden/distillation/*.py
pytest tests/distillation/test_distillation_runner_skeleton.py -q
python scripts/distillation/run_distillation_skeleton.py `
  --manifest "E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv" `
  --output-dir "E:\WardenData\manifests\distillation_skeleton_v1_readiness_fields" `
  --split train `
  --mode mock `
  --limit 10 `
  --seed 42 `
  --overwrite
python scripts/distillation/inspect_distillation_runner_outputs.py --output-dir "E:\WardenData\manifests\distillation_skeleton_v1_readiness_fields" --pretty
python scripts/ci/check_task_doc.py docs/tasks/2026-05-13_warden_distillation_real_adapter_readiness_fields_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-13_warden_distillation_real_adapter_readiness_fields_v1.md
```

If wildcard `src/warden/distillation/*.py` does not work on Windows PowerShell, compile files explicitly.

Validation success must confirm:

- output files exist, including `attempts.jsonl`;
- all future-readiness fields are present;
- `do_not_train_as_gold` failures = 0;
- `diagnostic_only` failures = 0;
- forbidden field hits = none;
- duplicate `record_id` = none;
- duplicate `sample_key` = none;
- call counters remain 0;
- schema valid count equals processed count unless intentionally testing error behavior.

## 12. Stop Rules

Stop and report completion when:

- all scoped implementation changes are complete;
- all required output fields exist in the bounded mock smoke output;
- validation passes or failed checks are explained;
- handoff is written;
- no out-of-scope files are touched.

Stop and escalate if:

- real teacher API access becomes necessary;
- modifying existing schema, labels, split, runtime, training, inference, or data files becomes necessary;
- output changes would make mock records look trainable or production-grade;
- required readiness fields cannot be added without broad redesign.

## 13. Handoff Requirements

The handoff must include:

- files created / edited;
- exact output artifacts and counts;
- evidence / retrieval performed;
- validation commands and results;
- compatibility impact;
- confirmation that no real teacher calls, teacher distillation, teacher labels, data mutation, schema freeze, training change, runtime change, or existing CLI break happened;
- remaining risks and next steps.
