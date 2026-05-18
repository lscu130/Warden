# Handoff Metadata

- Handoff ID: HANDOFF_20260518_V1_MODEL_DATAFLOW_REFOCUS
- Related Task ID: WARDEN-TASK-20260518-V1-MODEL-DATAFLOW-REFOCUS
- Task Title: Refocus Warden V1 model structure and data flow around Evidence Pack Builder -> L1
- Module: Warden architecture / data pipeline / L1 inference design
- Author: Codex
- Date: 2026-05-18
- Status: DONE

## 中文版

本次交付按用户提供的 `WARDEN_TASK_20260518_V1_MODEL_DATAFLOW_REFOCUS.md` 执行，完成 Warden V1 模型结构与数据流的文档重聚焦。

当前 V1 离线实验链路已明确为：

```text
Processed Valid Dataset
  -> Evidence Pack Builder
  -> L1 Main Judgment / L1 Training / L1 Evaluation
  -> Metrics / Evidence Ledger / Ablation
```

未来 online / wild-test 链路已保留为：

```text
Raw URL
  -> Capture Pipeline
  -> Capture QA / V1 Scope Admission
  -> Evidence Pack Builder
  -> L1 Main Judgment
  -> Wild-Test Report
```

本次没有修改代码、schema、label enum、CLI、manifest 字段、JSON/YAML 输出或训练/runtime 行为。代码中仍存在 L0/L2/gate/evasion 兼容路径，按任务要求只记录为后续 implementation-alignment 风险。

接收补丁解释规则：对于当前 Warden V1 离线实验路径，本 handoff 覆盖并收束旧 handoff 或旧文档中保留的 `L0/L1 staged` wording。旧 wording 只能作为 legacy/runtime compatibility wording 解读；当前离线默认链路是 `Processed Valid Dataset -> Evidence Pack Builder -> L1`，L0 不属于该默认链路。

## English Version

AI note: English is authoritative for exact validation, compatibility, and residual-risk statements.

## 1. Executive Summary

Warden V1 model/dataflow documentation was refocused around `Processed Valid Dataset -> Evidence Pack Builder -> L1` for current offline experiments, while preserving `Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1` for future online/wild-test work.

The task reached its documentation-only stop condition. No runtime implementation, model code, training behavior, schema, label enum, manifest field, CLI flag, JSON/YAML output format, or dataset artifact was intentionally changed.

Acceptance interpretation rule: for the current Warden V1 offline experiment path, this handoff supersedes older handoff or documentation wording that preserved an `L0/L1 staged` framing. Such wording is legacy/runtime compatibility wording only. The current offline default path is `Processed Valid Dataset -> Evidence Pack Builder -> L1`, and L0 is not part of that default path.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/architecture/WARDEN_V1_MODEL_DATAFLOW_REFOCUS.md` as the central V1 model/dataflow refocus note.
- Updated top-level docs to state the current offline experiment path and future online/wild-test path.
- Updated runtime/inference/L1/text/vision/deployment docs to classify legacy L0 as compatibility screening / scope-admission support rather than the current V1 offline experiment default entrypoint.
- Updated CLIP / MobileCLIP / SNet wording from default online-path framing to out-of-default-V1-path framing.
- Updated OCR / YOLO wording so they are conditional L1 evidence recovery primitives, not always-on dataflow stages.
- Updated L2 reference docs so L2 remains future / opt-in / non-default.

### Output / Artifact Changes

- Added `docs/tasks/2026-05-18_v1_model_dataflow_refocus.md`.
- Added this handoff document.

## 3. Files Touched

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/architecture/WARDEN_V1_MODEL_DATAFLOW_REFOCUS.md`
- `docs/tasks/2026-05-18_v1_model_dataflow_refocus.md`
- `docs/handoff/2026-05-18_v1_model_dataflow_refocus.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/modules/Warden_MINICONDA_ENV_SETUP_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`

Note: the repository already had unrelated dirty files before this task, including distillation docs/code/tests and several untracked task/handoff docs. Those unrelated changes were not reverted.

## 4. Behavior Impact

### Expected New Behavior

- Documentation readers should treat `Processed Valid Dataset -> Evidence Pack Builder -> L1` as the current V1 offline experiment default path.
- Documentation readers should treat `Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1` as future online/wild-test architecture, not current implementation.
- OCR / YOLO should be understood as conditional L1 visual evidence recovery.
- CLIP / MobileCLIP / SNet should be understood as outside the Warden V1 default path.
- L2 should be understood as future / opt-in / non-default.

### Preserved Behavior

- Existing runtime code behavior is unchanged.
- Existing L0/L2 compatibility names and code paths are unchanged.
- Existing schema, CLI, labels, manifests, and JSON/YAML outputs are unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This is a documentation/specification refocus. Existing code still contains L0/L2 stage names and gate/evasion compatibility fields. Aligning runtime code with the new documentation contract requires a separate implementation task.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- user-provided external task: `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_MODEL_DATAFLOW_REFOCUS.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `README.md`
- active docs under `docs/modules/`, `docs/frozen/`, `docs/l1/`, `docs/data/`, and `docs/threat_model/`
- read-only code search under `src`, `scripts`, and `tests`

Counter-review performed:

- Fact: the task explicitly requires documentation/specification refocus and forbids code/schema/label/CLI/JSON/training/runtime changes.
- Fact: repository code still contains L0/L2 paths, including `src/warden/runtime/pipeline.py`, `src/warden/module/l0.py`, and `src/warden/module/l2.py`.
- Inference: code changes are out of scope and should be follow-up implementation-alignment work.
- Risk considered: renaming Capture QA / Scope Admission into a new default L0 would preserve the old framing under a different name.
- Alternative rejected: broad runtime refactor, because the task explicitly says to stop and report if code/schema/interface changes are needed.

## 6. Validation Performed

### Commands Run

```bash
rg -n "L0|L1|L2|CLIP|OCR|YOLO|adult|gambling|gate|evasion|Evidence Pack|evidence_pack|pipeline|runtime|inference|wild" . -g "*.md" -g "*.yaml" -g "*.yml" -g "*.json"
rg -n "CLIP|L2|direct_to_L2|needs_l2|evidence_pack|Evidence Pack|OCR|YOLO|gate|evasion" src scripts tests -g "*.py" -g "*.json" -g "*.yaml" -g "*.yml"
rg -n "default online|online mainline|Current Online Mainline|current online architecture defines|current online mainline|当前在线系统只定义|Raw sample|L0Router|default visual tower|official top-level runtime structure stays|official current `L0 / L1`|Every valid webpage sample not terminated by L0|L0 / L1 staged|L0 \+ L1" AGENTS.md PROJECT.md README.md docs\architecture docs\modules docs\frozen docs\l1 docs\data docs\threat_model -g "*.md"
rg -n "Processed Valid Dataset|Evidence Pack Builder|Capture QA|V1 Scope Admission|Wild-Test|Conditional Vision Evidence Recovery|Text / HTML / URL / Forms first pass" AGENTS.md PROJECT.md README.md docs\architecture docs\modules docs\frozen docs\l1 -g "*.md"
git diff --stat -- AGENTS.md PROJECT.md README.md docs\architecture\WARDEN_V1_MODEL_DATAFLOW_REFOCUS.md docs\modules\Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs\modules\MODULE_INFER.md docs\modules\L0_DESIGN_V1.md docs\frozen\Warden_L1_FRAMEWORK_V0.1.md docs\l1\WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md docs\modules\Warden_TEXT_PIPELINE_V1.md docs\tasks\2026-05-18_v1_model_dataflow_refocus.md
git diff --name-only -- AGENTS.md PROJECT.md README.md docs\architecture\WARDEN_V1_MODEL_DATAFLOW_REFOCUS.md docs\modules\Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs\modules\MODULE_INFER.md docs\modules\L0_DESIGN_V1.md docs\frozen\Warden_L1_FRAMEWORK_V0.1.md docs\l1\WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md docs\modules\Warden_TEXT_PIPELINE_V1.md docs\tasks\2026-05-18_v1_model_dataflow_refocus.md | rg "\.(py|json|ya?ml)$"
python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_v1_model_dataflow_refocus.md
python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_v1_model_dataflow_refocus.md
```

### Result

- Current offline path terms are present across top-level and active module docs.
- Future online/wild-test path terms are present and preserved.
- Remaining `L0Router` hits are explicitly classified as runtime compatibility / future online-wild-test support in `PROJECT.md`.
- Remaining `default online` hits are unrelated teacher-tool dependency statements or compatible negative statements.
- Remaining `L0 / L1 staged system` hit in `MODULE_PAPER.md` is conditional paper-framing language, not current default architecture.
- Code search confirmed implementation-risk residuals: runtime code still contains L0/L2 stage names and gate/evasion compatibility logic. No code was modified in this task.
- No Python/JSON/YAML files were found in the task-scoped changed-file check.
- Final task and handoff checker status: pass.

### Not Run

- unit tests
- runtime smoke tests
- schema validation against runtime artifacts
- training/evaluation commands

Reason:

The accepted task is documentation/specification-only and explicitly forbids runtime, schema, label, CLI, JSON, training, and implementation changes.

Next best check:

Open a separate implementation-alignment task if the runtime code should stop emitting L0/L2 stage names or if output schemas should expose the new Evidence Pack Builder / L1 dataflow contract.

## 7. Risks / Caveats

- Runtime code still has L0/L2 stage names and gate/evasion logic. This was found by read-only search and left unchanged by design.
- Some legacy docs retain historical or future-scope L2 references; they are classified as future / non-default rather than deleted.
- This task aligns documentation only; it does not prove runtime behavior follows the new model/dataflow contract.
- The worktree had pre-existing unrelated changes before this task.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- listed in `## 3. Files Touched`

Doc debt still remaining:

- Historical task/handoff/ADR documents may still contain old L0/L2/CLIP language as historical records.
- Runtime code and tests need a separate follow-up if the implementation should align with the new no-default-L0/no-default-L2 documentation.

## 9. Recommended Next Step

- Review and accept this documentation/specification refocus.
- If accepted, create a separate implementation-readiness task to audit `src/warden/runtime/pipeline.py`, `src/warden/module/l0.py`, `src/warden/module/l2.py`, and related tests for whether L0/L2 stage names should remain compatibility-only or be migrated.
