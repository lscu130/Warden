# Task Metadata

- Task ID: WARDEN-TASK-20260518-DISTILLATION-V03-CONTRACT-AND-ADAPTER-READINESS
- Task Title: Distillation V0.3 Record Contract Review and Real-Teacher Adapter Readiness
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: distillation / record contract / adapter readiness / audit / validation
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_CONTRACT_AND_ADAPTER_READINESS.md
- Created At: 2026-05-18
- Requested By: project owner
- Karpathy Guardrails Required: YES

## 中文版

### 摘要

本任务把 Warden Distillation V0.3 mock output shape 审查并冻结为 no-network adapter-readiness baseline。允许补 real-teacher adapter readiness placeholders，但禁止真实 teacher/API/OCR/YOLO/CLIP 调用、训练、评估、数据集/manifest 修改和 production runtime schema 变更。

### 当前权威公式

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

## 1. Background

The previous V0.3 work aligned the distillation mock contract to `RiskBearingEngagement`. The follow-up requirement is to review and freeze the current mock output shape as a candidate record contract, then add no-network adapter-readiness provenance, prompt, modality, attempt, repair, validation, cost/token, failure, and rollback placeholders.

This task remains mock-only and no-network.

## 2. Goal

Produce a Warden Distillation V0.3 record-contract and no-network adapter-readiness baseline that can support a later, separately approved small live-provider pilot task.

The task must not approve or execute live provider calls, training ingestion, large-scale distillation, provider budget, OCR, YOLO, CLIP, or evaluation.

## 3. Scope In

Allowed files:

- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/runner.py`
- `src/warden/distillation/audit_log.py`
- `src/warden/distillation/review_queue.py`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `tests/distillation/*`
- `docs/distillation/*.md`
- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/templates/*.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `docs/tasks/2026-05-18_warden_distillation_v03_contract_and_adapter_readiness.md`
- `docs/handoff/2026-05-18_warden_distillation_v03_contract_and_adapter_readiness.md`

Allowed changes:

- Add/freeze mock record readiness fields.
- Add no-network output placeholder files/directories.
- Improve review queue, audit, report, and inspect helper readiness checks.
- Update V0.3 docs/templates/Skill to document the contract.

## 4. Scope Out

Do not modify or execute:

- production runtime schema;
- `src/warden/runtime/*`;
- `src/warden/module/*`;
- training code, configs, jobs, or ingestion;
- evaluation jobs;
- dataset files;
- manifest contents outside temporary smoke manifests under `.codex_tmp`;
- production labels / label enums;
- live teacher/API calls;
- OCR / YOLO / CLIP execution;
- network calls;
- provider billing path.

## 5. Inputs

### Docs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_DISTILLATION_V03_CONTRACT_AND_ADAPTER_READINESS.md`
- `AGENTS.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- `src/warden/distillation/*.py`
- `scripts/distillation/inspect_distillation_runner_outputs.py`
- `tests/distillation/*`

### Data / Artifacts

- Temporary smoke artifacts under `.codex_tmp/distillation_v03_adapter_readiness_smoke/`.

### Prior Handoff

- `docs/handoff/2026-05-18_warden_distillation_v03_risk_engagement_readiness.md`

### Missing Inputs

- none.

## 6. Required Outputs

- Updated mock V0.3 record contract with adapter-readiness fields.
- Updated runner output layout with `attempts.jsonl`, `validation_summaries.jsonl`, `prompt_snapshots/`, `raw_outputs/`, `repaired_outputs/`, and `adapter_readiness_report.md`.
- Updated review queue, audit/report, and inspect helper.
- Updated docs/templates/Skill.
- Repo-local task and handoff.
- Validation evidence.

## 7. Hard Constraints

- No real teacher/API/OCR/YOLO/CLIP/network calls.
- No training, evaluation, threshold tuning, or model selection.
- No production runtime schema, official label, dataset, or manifest changes.
- All mock outputs remain `diagnostic_only=true` and `do_not_train_as_gold=true`.
- `adapter_readiness_status` may be `ready_for_no_network_dry_run`; live readiness must remain `not_ready_for_live_teacher`.

## 8. Interface / Schema Constraints

Schema changed allowed:

- Yes, only for mock-only `warden_distill_v0.3_mock` output.

Required compatibility plan:

- Preserve existing mock runner CLI.
- Keep `induced_high_risk_action` compatibility-only.
- Keep all new adapter-readiness fields as placeholders until a separate live-provider task approves real calls.

Existing commands that must keep working:

- `pytest tests/distillation -q`
- `python scripts\distillation\run_distillation_skeleton.py --manifest ... --output-dir ... --split train --mode mock --limit 1 --seed 42 --overwrite`
- `python scripts\distillation\inspect_distillation_runner_outputs.py --output-dir ... --pretty`

## 9. Evidence / Retrieval Rules

Evidence sources:

- User-provided task document.
- Current repo docs/code/tests.
- Fresh command outputs.

Retrieval budget:

- Read the task document and only the files required to patch/validate the scoped implementation.

Missing-evidence behavior:

- Report unverified claims explicitly; do not infer live-provider readiness from mock checks.

## 9.1 Counter-Review Requirements

Original framing:

- Freeze mock V0.3 record contract and add no-network adapter-readiness fields.

Assumptions checked:

- Mock runner can create placeholders without provider calls.
- Existing CLI can remain backward compatible.
- New readiness fields can stay outside production runtime schema.

Failure modes considered:

- Accidentally implying live provider readiness.
- Treating mock records as training gold.
- Missing output artifacts required for later audit.
- Hidden out-of-scope runtime/data changes.

Decision:

- Proceed only with mock-only readiness placeholders and validation.

## 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- The supplied task document is the active hard boundary.
- `real-teacher adapter readiness` means placeholders and no-network checks only.

Simplicity boundary:

- Add the smallest structured fields and placeholder artifacts needed by the task.
- Do not introduce new dependencies or new provider abstractions.

Surgical change boundary:

- Every changed file must map to Scope In.
- No unrelated cleanup.

Goal-driven verification loop:

- Required fields -> targeted test.
- Output layout -> smoke run and inspect helper.
- No-network guarantee -> audit call counters.
- Workflow compliance -> task/handoff checkers.

## 10. Acceptance Criteria

- Current mock V0.3 record shape is reviewed and documented.
- Required adapter-readiness fields are present in mock records.
- Required placeholder output files/directories are produced.
- Review queue includes formula and engagement uncertainty context.
- Audit/report include attempt, repair, validation, inventory, duplicate, cost/token placeholder, and readiness status summaries.
- Inspect helper reports `machine_readiness_ok=true` for a bounded mock run.
- All real teacher/API/OCR/YOLO/CLIP counters remain zero.
- No runtime/data/training/manifest out-of-scope paths are changed.

## 11. Validation Checklist

- `pytest tests/distillation -q`
- `python scripts\distillation\run_distillation_skeleton.py --manifest .codex_tmp\distillation_v03_adapter_readiness_smoke\manifest.csv --output-dir .codex_tmp\distillation_v03_adapter_readiness_smoke\out --split train --mode mock --limit 1 --seed 42 --overwrite`
- `python scripts\distillation\inspect_distillation_runner_outputs.py --output-dir .codex_tmp\distillation_v03_adapter_readiness_smoke\out --pretty`
- Required-term residual search over docs/Skill/src/tests/scripts.
- `python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_warden_distillation_v03_contract_and_adapter_readiness.md`
- `python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_warden_distillation_v03_contract_and_adapter_readiness.md`
- `git diff --name-only -- src\warden\runtime src\warden\module data datasets manifests`
- `git status --short -- src\warden\runtime src\warden\module data datasets manifests`

## 12. Stop Rules

Stop as done when validation passes and the handoff records actual results.

Stop as blocked if the task requires:

- live provider/API calls;
- OCR / YOLO / CLIP execution;
- training/evaluation;
- production runtime schema or label enum changes;
- dataset or manifest mutation outside temporary smoke artifacts.
