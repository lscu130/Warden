# TASK_20260512_WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_SCHEMA_READINESS_V1

## 中文版

### 摘要

本任务对上一轮 Warden distillation runner implementation skeleton 产生的 mock / dry-run 输出做只读 inspection 和 schema-readiness review。任务目标是判断当前输出是否适合作为未来 real teacher adapter 接入前的工程基础，并列出接入前必须修正的问题。

本任务只读取输出和相关合同文档。允许新增一个标准库只读 helper。禁止调用真实模型、运行正式蒸馏、训练、运行 OCR / YOLO / CLIP / MobileCLIP / SNet / SpecularNet-like，禁止修改数据、标签、manifest、split、runtime schema、训练或推理逻辑。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260512-WARDEN-DISTILLATION-RUNNER-OUTPUT-INSPECTION-SCHEMA-READINESS-V1
- Task Title: Inspect Distillation Runner Mock Outputs And Review Schema Readiness
- Owner Role: Codex executor, GPT reviewer, human final acceptor
- Priority: P1
- Status: TODO
- Related Module: Distillation / Runner / Schema Readiness
- Related Issue / ADR / Doc: `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`, `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`, `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`, `docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`
- Created At: 2026-05-12
- Requested By: 佶
- Karpathy Guardrails Required: YES

## 1. Background

A local Warden distillation runner skeleton produced mock output under `E:\WardenData\manifests\distillation_skeleton_v1`. Before real teacher adapters are implemented, the mock output needs a read-only inspection for file readiness, schema readiness, split-safety, review-queue usability, audit completeness, and training-contamination risks.

## 2. Goal

Inspect the existing mock distillation runner outputs and produce a schema-readiness report that identifies whether any `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW` issues must be fixed before real teacher adapter work.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`
- `scripts/distillation/inspect_distillation_runner_outputs.py`

This task is allowed to read:

- Warden governing docs and templates.
- Current distillation docs and Skill references when needed.
- Prior runner skeleton handoff.
- Output files under `E:\WardenData\manifests\distillation_skeleton_v1`.
- Skeleton distillation source files for schema and output-field interpretation.

## 4. Scope Out

This task must not:

- Call MiMo, DeepSeek, OpenAI, Claude, or any external model API.
- Run real teacher distillation.
- Train any model.
- Run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference.
- Modify source sample directories.
- Modify dataset labels.
- Modify train/val/test splits.
- Modify existing manifests.
- Modify Warden runtime schema.
- Modify production training or inference logic.
- Implement real teacher adapters.
- Convert mock outputs into trainable labels.
- Mark mock teacher outputs as gold labels.
- Promote `warden_distill_v0.2_mock` or `warden_distill_v0.2` to a frozen production schema.

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`

### Code / Scripts

- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/runner.py`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- `E:\WardenData\manifests\distillation_skeleton_v1\distillation_records.jsonl`
- `E:\WardenData\manifests\distillation_skeleton_v1\review_queue.jsonl`
- `E:\WardenData\manifests\distillation_skeleton_v1\run_audit.json`
- `E:\WardenData\manifests\distillation_skeleton_v1\run_report.md`
- `E:\WardenData\manifests\distillation_skeleton_v1\errors.jsonl`

### Prior Handoff

- `docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`

### Missing Inputs

- real teacher adapter implementation details
- production teacher endpoint behavior
- final frozen benign + malicious manifests

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md`
- `scripts/distillation/inspect_distillation_runner_outputs.py`

Output format requirements:

- Markdown documents must be bilingual: Chinese summary first, English authoritative section second.
- The report must include severity levels: `BLOCKER`, `HIGH`, `MEDIUM`, and `LOW`.
- The helper script must be read-only and standard-library only.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.
- Keep this task read-only with respect to data, labels, manifests, splits, runtime schema, model code, and existing runner behavior.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden manifests, labels, samples, split files, runtime outputs, and CLIs;
- current training, inference, capture, crawler, and labeling code;
- official runtime result / trace schema.

Schema / field constraints:

- Schema changed allowed: NO.
- `warden_distill_v0.2_mock` remains a draft/mock engineering shape.
- `warden_distill_v0.2` remains a draft distillation-output schema.

Downstream consumers to watch:

- future real teacher adapters;
- future train-only teacher output consumers;
- future review queue tooling;
- future Decision Head training tasks.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- current output file existence and parse status;
- audit/report counts;
- required field coverage;
- forbidden field absence;
- L1 contract alignment;
- split-safety and contamination risks;
- real teacher adapter readiness gaps.

Allowed evidence sources:

- current task document;
- Warden governing docs and templates;
- current distillation docs and runner design;
- prior runner skeleton handoff;
- current output files;
- read-only helper output.

Missing-evidence behavior:

- Do not claim real teacher quality has been validated.
- Do not claim production endpoint behavior has been validated.
- Mark real-adapter conclusions as readiness findings, not production validation.

### 9.1 Counter-Review Requirements

Current proposed framing:

Inspect mock outputs before implementing real teacher adapters.

Hidden assumptions to check:

- Mock output shape can reveal real-adapter readiness gaps.
- Machine-parse success is not enough for real-adapter readiness.
- Split-safety can be audited from output fields.

Failure modes to consider:

- mock output accidentally treated as training gold;
- missing provenance fields block real-adapter auditability;
- review queue lacks enough context for human review;
- audit log lacks prompt/schema/model routing details;
- val/test diagnostic records cannot be separated downstream;
- rule-router diagnostics become final labels.

Decision rule:

- Accept the inspection framing if the task remains read-only and produces concrete severity findings.
- Stop and escalate if real adapter implementation, data mutation, or schema freeze becomes necessary.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- The latest output directory is the path recorded in the prior handoff: `E:\WardenData\manifests\distillation_skeleton_v1`.
- The runner design doc exists as `WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`, even though the task text mentions V1 as an optional name.

Simplicity boundary:

- Add one read-only helper only because manual JSONL inspection is error-prone.
- Do not change runner behavior.

Surgical change boundary:

- Every touched file must be one of the scope-in paths.

Goal-driven verification loop:

- helper py_compile verifies syntax.
- helper run verifies output parse and field coverage.
- task checker verifies task doc structure.
- handoff checker verifies handoff structure.
- required-term grep verifies report coverage.

## 10. Acceptance Criteria

This task is complete only if:

- [ ] It remains read-only with respect to data, labels, manifests, splits, runtime schema, and model code.
- [ ] It does not call external APIs or real teachers.
- [ ] It produces a clear schema-readiness report.
- [ ] It identifies whether any `BLOCKER` issues exist before real teacher adapter implementation.
- [ ] It verifies that mock outputs are not trainable gold.
- [ ] It verifies that rule-router outputs are not final labels.
- [ ] It documents split-safety and review-queue readiness.
- [ ] It provides a concrete recommended next task.
- [ ] Task doc checker passes.
- [ ] Handoff checker passes.
- [ ] Required-term grep passes.

## 11. Validation Checklist

Minimum validation expected:

```powershell
python -m py_compile scripts/distillation/inspect_distillation_runner_outputs.py
python scripts/distillation/inspect_distillation_runner_outputs.py --output-dir "E:\WardenData\manifests\distillation_skeleton_v1" --pretty
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_distillation_runner_output_inspection_schema_readiness_v1.md
rg -n "BLOCKER|HIGH|do_not_train_as_gold|diagnostic_only|rule_router|text_semantic_concepts|vision_evidence|decision_head_auxiliary_targets|payload not observed|action surface is not automatically threat action|weak labels are evidence|real teacher adapter" docs/distillation/WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1.md
```

## 12. Stop Rules

Stop and report completion when:

- scoped docs and helper are created;
- output inspection has been run;
- validation passes or failures are honestly reported;
- no out-of-scope files are touched.

Stop and escalate if:

- real teacher API access becomes necessary;
- modifying existing schema, labels, split, runtime, training, inference, or data files becomes necessary;
- the output directory cannot be located.

## 13. Handoff Requirements

The handoff must include:

- files created / edited;
- evidence / retrieval performed;
- validation commands and results;
- compatibility impact;
- confirmation that no real teacher calls, teacher distillation, teacher labels, data mutation, schema freeze, training change, runtime change, or existing CLI change happened;
- risks and next steps.
