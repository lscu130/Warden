# TASK_20260512_WARDEN_DISTILLATION_RUNNER_IMPLEMENTATION_SKELETON_V1

## 中文版

### 摘要

本任务实现 Warden distillation runner 的 dry-run / mock 工程骨架。交付允许新增独立 CLI、`warden.distillation` 内部组件、mock teacher、schema validation、JSONL writer、resume/idempotency、review queue、audit log、focused tests、task doc 和 handoff。

本任务禁止调用真实 teacher API，禁止运行正式蒸馏，禁止生成可训练 teacher labels，禁止训练模型，禁止运行 OCR / YOLO / CLIP / MobileCLIP / SNet / SpecularNet-like 路径，禁止修改数据、标签、manifest、split、runtime schema、训练或推理逻辑。

所有 skeleton 输出必须标记为 `do_not_train_as_gold=true`、`diagnostic_only=true`、`teacher_model=mock_teacher_v0`、`schema_version=warden_distill_v0.2_mock`。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260512-WARDEN-DISTILLATION-RUNNER-IMPLEMENTATION-SKELETON-V1
- Task Title: Implement Warden Distillation Runner Skeleton V1
- Owner Role: Codex executor, GPT reviewer, human final acceptor
- Priority: P0
- Status: TODO
- Related Module: Distillation / Labeling / Runner Skeleton
- Related Issue / ADR / Doc: `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`, `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`, `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`, `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`, `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- Created At: 2026-05-12
- Requested By: 佶
- Karpathy Guardrails Required: YES

## 1. Background

Warden has a distillation prompt / Skill contract and a distillation runner design contract. This task implements only a local runner skeleton that can exercise manifest reading, evidence-pack construction, split-policy checks, JSONL output, schema validation, resume/idempotency, review queue generation, and audit logging without calling real teacher APIs.

Current L1 semantics must be preserved:

- `rule_router` is routing and evidence-sufficiency diagnostic only; it is not a teacher label source.
- `text_semantic_concepts` are the primary future distillation target area.
- `vision_evidence` records OCR / YOLO-style evidence observations only; this skeleton must not run OCR or YOLO.
- `decision_head_auxiliary_targets` are advisory targets for a future Decision Head; they are not gold labels.
- Weak labels are evidence, not gold.
- `payload not observed` is not automatic benign.
- Action surface is not automatically threat action.

## 2. Goal

Implement a dry-run/mock-capable Warden distillation runner skeleton that follows the V0.2 distillation workflow and runner design contracts while preserving all existing Warden runtime, schema, dataset, split, and training behavior.

The runner must create reproducible draft outputs that are clearly marked as non-gold and non-production.

## 3. Scope In

Allowed implementation areas:

- `scripts/distillation/run_distillation_skeleton.py`
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
- `docs/tasks/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`

Allowed behavior:

- Add a new standalone CLI script.
- Add a new internal `warden.distillation` package.
- Add standard-library-only schema validation helpers.
- Add mock teacher output generation for local validation.
- Add JSONL output writer and audit log writer.
- Add review queue output generation.
- Add focused tests.
- Add task and handoff docs.

## 4. Scope Out

This task must not:

- Call real teacher APIs.
- Use MiMo, DeepSeek, OpenAI, Claude, or any external API.
- Run real teacher distillation.
- Implement production batch execution.
- Train any model.
- Run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference.
- Modify existing Warden schemas, label enums, runtime result schema, training code, inference code, crawler/capture code, or existing CLI behavior.
- Modify samples, labels, manifests, split files, or dataset directories.
- Add third-party dependencies.
- Treat mock output as gold label.
- Write val/test official distillation outputs unless explicitly in diagnostic-only mode and marked `do_not_train_as_gold=true`.

## 5. Inputs

Required CLI inputs:

- `--manifest <path to manifest CSV>`
- `--output-dir <output directory>`
- `--split train|val|test|unknown`
- `--mode dry-run|mock`
- `--limit <optional int>`
- `--seed <optional int>`
- `--resume`
- `--overwrite`
- `--diagnostic-only`

Input manifest assumptions:

- Manifest may contain `sample_id`.
- Manifest must contain `current_path`, `sample_path`, or `path`.
- Manifest may contain `triage_label`, `split`, or dataset-management metadata, but those metadata fields must not be inserted into model-visible evidence text.

## 6. Required Outputs

The runner must create the following files under `--output-dir`:

- `distillation_records.jsonl`
- `review_queue.jsonl`
- `run_audit.json`
- `run_report.md`
- `errors.jsonl`

Each distillation record must include at least:

- `schema_version`
- `record_id`
- `sample_id`
- `sample_path`
- `split`
- `diagnostic_only`
- `do_not_train_as_gold`
- `teacher_model`
- `teacher_role`
- `input_modalities`
- `fallback_reason`
- `evidence_pack_summary`
- `rule_router_observation`
- `text_semantic_concepts`
- `vision_evidence`
- `decision_head_auxiliary_targets`
- `quality_flags`
- `review_reasons`
- `created_at`

Required fixed output markers:

- `schema_version == "warden_distill_v0.2_mock"`
- `teacher_model == "mock_teacher_v0"`
- `teacher_role == "mock_skeleton"`
- `do_not_train_as_gold == true`
- `diagnostic_only == true`

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.
- Keep all skeleton outputs non-gold and diagnostic-only.
- Keep all external/API/OCR/YOLO/CLIP call counters at `0`.
- Keep evidence pack reads read-only.
- Keep dataset-management metadata out of teacher-visible evidence text.

Task-specific constraints:

- `train` split may write mock records, but they remain `do_not_train_as_gold=true`.
- `val` and `test` require `--diagnostic-only`; otherwise fail closed.
- Existing output files require `--resume` or `--overwrite`; otherwise fail closed.
- `--resume` must append only new records and skip already processed records.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden manifests, labels, samples, split files, runtime outputs, and CLIs;
- current training, inference, capture, crawler, and labeling code;
- official runtime result / trace schema.

Schema / field constraints:

- Schema changed allowed: NO for existing schemas.
- New mock runner output schema allowed only under `warden_distill_v0.2_mock`.
- The mock schema is not production teacher output.

Forbidden output fields:

- `final_gold_label`
- `final_training_label`
- `gold_malicious_label`
- `chain_of_thought`
- `hidden_reasoning`
- `teacher_cot`

Downstream consumers to watch:

- future production distillation runner;
- future train-split teacher output consumers;
- future review queue tooling;
- future Decision Head training tasks.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- current L1 structure;
- current distillation V0.2 schema and prompt policy;
- runner design contract requirements;
- workflow, task, and handoff structure.

Allowed evidence sources:

- current task document;
- Warden repo docs and handoffs;
- current V0.2 distillation docs and Skill;
- current L1 Decision Head contract;
- focused tests and validation outputs.

Missing-evidence behavior:

- Do not invent production endpoint details.
- Do not claim model quality or teacher-output quality has been validated.
- Do not claim official distillation was run.

### 9.1 Counter-Review Requirements

Current proposed framing:

Implement the runner skeleton now, with only dry-run/mock behavior.

Hidden assumptions to check:

- A mock skeleton can validate runner mechanics without validating teacher quality.
- The draft `warden_distill_v0.2_mock` record shape can be checked with standard-library validation.
- Split-policy safety can be enforced before real teacher adapters exist.

Failure modes to consider:

- mock outputs treated as gold;
- val/test contamination;
- router diagnostics treated as teacher labels;
- metadata leakage into evidence text;
- resume overwriting successful records;
- hidden reasoning fields written to JSONL;
- external calls accidentally introduced.

Decision rule:

- Accept the skeleton route if all required outputs are local, diagnostic-only, non-gold, schema-validated, resumable, and audited with zero external call counters.
- Stop and escalate if real teacher access, data mutation, production schema changes, or training changes become necessary.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- The task is implementation skeleton only.
- Mock output is for runner validation and must not be used for training.
- Existing dirty worktree entries outside the task scope must be left untouched.

Simplicity boundary:

- Use standard-library-only Python modules.
- Add only the allowed CLI, package modules, tests, task doc, and handoff.

Surgical change boundary:

- Every touched file must be one of the scope-in paths.

Goal-driven verification loop:

- py_compile verifies import/syntax sanity.
- targeted pytest verifies skeleton behavior.
- real benign train manifest smoke verifies bounded local execution.
- output spot-check verifies required files and non-gold/diagnostic/counter invariants.
- task doc checker and handoff checker verify workflow artifacts.

## 10. Acceptance Criteria

This task is complete only if:

- [ ] The runner skeleton CLI exists and can run in mock mode.
- [ ] It reads a manifest and writes all required output artifacts.
- [ ] It does not call any external model APIs.
- [ ] It does not run OCR / YOLO / CLIP / SNet / SpecularNet.
- [ ] It does not modify existing samples, manifests, labels, or splits.
- [ ] It enforces split policy fail-closed behavior.
- [ ] It supports resume/idempotency.
- [ ] It validates output schema.
- [ ] It produces review queue and audit log.
- [ ] Focused tests pass.
- [ ] Task doc checker passes.
- [ ] Handoff checker passes.
- [ ] Handoff clearly states that this is not production distillation and not training gold.

## 11. Validation Checklist

Minimum validation expected:

```powershell
python -m py_compile scripts/distillation/run_distillation_skeleton.py src/warden/distillation/*.py
pytest tests/distillation/test_distillation_runner_skeleton.py -q
python scripts/distillation/run_distillation_skeleton.py `
  --manifest "E:\WardenData\manifests\benign_clean_v1\benign_train_manifest_v1.csv" `
  --output-dir "E:\WardenData\manifests\distillation_skeleton_v1" `
  --split train `
  --mode mock `
  --limit 10 `
  --seed 42 `
  --overwrite
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md
```

If wildcard `src/warden/distillation/*.py` does not work on Windows PowerShell, compile files explicitly.

Validation success must confirm:

- output files exist;
- `run_audit.json` reports `teacher_calls=0`, `external_api_calls=0`, `ocr_calls=0`, `yolo_calls=0`, and `clip_calls=0`;
- all records have `do_not_train_as_gold=true`;
- all records have `diagnostic_only=true`;
- no forbidden fields exist;
- schema valid count equals processed count unless intentionally testing error behavior.

## 12. Stop Rules

Stop and report completion when:

- all scoped code, tests, task doc, and handoff are created;
- validation passes or failed checks are explained;
- no out-of-scope files are touched by this task.

Stop and escalate if:

- real teacher API access becomes necessary;
- modifying existing schema, labels, split, runtime, training, inference, or data files becomes necessary;
- the skeleton cannot keep outputs non-gold and diagnostic-only.

## 13. Handoff Requirements

The handoff must include:

- files created / edited;
- evidence / retrieval performed;
- validation commands and results;
- compatibility impact;
- confirmation that no real teacher calls, teacher distillation, teacher labels, data mutation, schema freeze, training change, runtime change, or existing CLI change happened;
- risks and next steps.
