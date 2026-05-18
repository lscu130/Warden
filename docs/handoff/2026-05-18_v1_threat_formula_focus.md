# Handoff Metadata

- Handoff ID: HANDOFF_20260518_V1_THREAT_FORMULA_FOCUS
- Related Task ID: WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS
- Task Title: Refocus Warden V1 Threat Definition Around Context Plus Induced Action Formula
- Module: project governance / threat definition / L0-L1 documentation
- Author: Codex
- Date: 2026-05-18
- Status: DONE

## 中文版

本次交付按用户提供的 `WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS.md` 执行，完成了 Warden V1 主定义的文档对齐：V1 Web-SE Threat 需要同时满足 `ManipulativeContext` 和 `InducedHighRiskAction` 的充分证据，其中 induced action 包括 `DirectAction`、`RoutedAction` 或 `ActionPreparation`。

本次没有修改运行时代码、schema、字段名、枚举、CLI、JSON/YAML 输出或数据集样本。成人、博彩、枪支、毒品等 high-risk-content-only 页面，以及 gate-only / challenge-only / CAPTCHA-only / redirect-only / trusted-sink-only / evasion-only 捕获，被重新表述为 V1 主任务之外、辅助、排除或未来范围；没有删除相关历史标签或字段。

接收补丁说明：在 `HANDOFF_20260518_V1_MODEL_DATAFLOW_REFOCUS` 之后，本 handoff 中任何保留的 `L0/L1 staged` wording 都只能解释为 legacy/runtime compatibility wording。当前 Warden V1 离线实验默认链路是 `Processed Valid Dataset -> Evidence Pack Builder -> L1`，L0 不是当前 V1 离线实验默认链路的一部分。

GATA/GATE 文件名只读检查结果：`docs/data/` 下只存在 `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`。本 handoff 保留实际仓库文件名，不执行重命名。

## English Version

AI note: English is authoritative for exact validation, compatibility, and residual-risk statements.

## 1. Executive Summary

The active Warden V1 documentation was refocused around the final formula:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)
InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

The task reached its documentation-only stop condition. No runtime implementation, schema, CLI, output format, JSON/YAML artifact, dataset manifest, or label enum was intentionally changed.

Acceptance patch note:

- After `HANDOFF_20260518_V1_MODEL_DATAFLOW_REFOCUS`, any preserved `L0/L1 staged` wording in this handoff must be interpreted only as legacy/runtime compatibility wording. The current Warden V1 offline experiment default path is `Processed Valid Dataset -> Evidence Pack Builder -> L1`. L0 is not part of the current V1 offline experiment default path.
- A read-only GATA/GATE filename check found only `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md` under `docs/data/`. This handoff keeps the actual repository filename and does not rename it.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated central project docs to use the V1 formula instead of behavior-only or content-category threat wording.
- Clarified phishing as a subset of Web-SE Threat.
- Reclassified adult/gambling/guns/drugs high-risk-content-only pages as outside the V1 main objective unless they also satisfy the formula.
- Reclassified gate-only/challenge-only/CAPTCHA-only/redirect-only/trusted-sink-only/evasion-only captures as excluded, auxiliary, or future-scope unless downstream observed content satisfies the formula.
- Clarified legacy L2 or `needs_l2_candidate` language as review/future-escalation compatibility wording rather than a current online L2 architecture.
- Added a repo-local task wrapper conforming to the current checker markers.

### Output / Artifact Changes

- Added this handoff document.
- Added `docs/tasks/2026-05-18_v1_threat_formula_focus.md`.

## 3. Files Touched

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/tasks/2026-05-18_v1_threat_formula_focus.md`
- `docs/handoff/2026-05-18_v1_threat_formula_focus.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`

Note: the repository already had unrelated dirty files before this task, including distillation docs/code/tests and some untracked task/handoff/L1/threat-model docs. Those unrelated changes were not reverted.

## 4. Behavior Impact

### Expected New Behavior

- Documentation readers should now treat V1 Web-SE Threat as requiring both manipulative context and induced high-risk action evidence.
- Payload/action absence remains `payload not observed` or review state, not automatic benign and not sufficient by itself for V1 malicious.
- High-risk-content-only and gate/evasion-only categories should not be treated as V1 main-scope malicious classes solely by category or capture pattern.

### Preserved Behavior

- Existing labels, legacy route names, weak-candidate fields, and compatibility language were preserved.
- Preserved L0/L1 staged wording is legacy/runtime compatibility only after `HANDOFF_20260518_V1_MODEL_DATAFLOW_REFOCUS`; the current offline default path is `Processed Valid Dataset -> Evidence Pack Builder -> L1`, and L0 is not part of that default path.
- Historical or compatibility terms such as `needs_l2_candidate` were not removed.

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

This is a documentation-only contract refocus. Legacy fields and labels remain present. Any future schema fields for `manipulative_context_type`, `induced_action_type`, `payload_observed`, or similar formula-alignment fields require a separate schema task.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- user-provided external task: `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- targeted active docs under `docs/frozen/`, `docs/threat_model/`, `docs/data/`, `docs/modules/`, and `docs/l1/`

Retrieval / reading performed:

- Read governing docs before editing.
- Searched active docs for formula terms, behavior-only wording, adult/gambling/gate wording, and current-L2 wording.
- Inspected candidate stale sections before patching them.

Counter-review performed:

- Fact: the user task explicitly requires the formula definition and documentation-only scope.
- Fact: existing docs contained older behavior-only, category-only, and legacy L2-related wording.
- Inference: preserving fields while clarifying their V1 role is safer than deleting or renaming compatibility fields.
- Risk considered: behavior-only references could leak into future labeling or training interpretation if left active.
- Alternative rejected: schema/runtime changes, because they are out of scope and not required for this documentation definition task.

## 6. Validation Performed

### Commands Run

```bash
rg -n "behavior-only|behavior_only|malicious_behavior_only|high-risk deceptive behavior and/or|Social-engineering threat =|social-engineering threat means high-risk deceptive behavior|brand impersonation landing shell without payload observed|adult, gambling|adult / gambling / gate|current online L2|directly to L2|L0 handles only.*adult|Web-SE Threat|EvidenceSufficient|ManipulativeContext|InducedHighRiskAction|DirectAction|RoutedAction|ActionPreparation" AGENTS.md PROJECT.md README.md docs\frozen docs\threat_model docs\data docs\modules docs\l1 -g "*.md"
git diff --stat -- AGENTS.md PROJECT.md README.md docs\frozen\Warden_Threat_Definition_V1.md docs\threat_model\WARDEN_THREAT_ADJUDICATION_FLOW_V1.md docs\data\TRAIN_LABEL_DERIVATION_V1.md docs\data\GATA_EVASION_AUXILIARY_SET_V1.md docs\data\Warden_MANUAL_LABEL_POLICY_V1_CORE.md docs\data\Warden_RULE_LABEL_POLICY_V1_CORE.md docs\modules\L0_DESIGN_V1.md docs\modules\MODULE_INFER.md docs\modules\Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs\modules\Warden_TEXT_PIPELINE_V1.md docs\frozen\Warden_L1_FRAMEWORK_V0.1.md docs\l1\WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md
git diff --name-only -- AGENTS.md PROJECT.md README.md docs\frozen\Warden_Threat_Definition_V1.md docs\threat_model\WARDEN_THREAT_ADJUDICATION_FLOW_V1.md docs\data\TRAIN_LABEL_DERIVATION_V1.md docs\data\GATA_EVASION_AUXILIARY_SET_V1.md docs\data\Warden_MANUAL_LABEL_POLICY_V1_CORE.md docs\data\Warden_RULE_LABEL_POLICY_V1_CORE.md docs\modules\L0_DESIGN_V1.md docs\modules\MODULE_INFER.md docs\modules\Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs\modules\Warden_TEXT_PIPELINE_V1.md docs\frozen\Warden_L1_FRAMEWORK_V0.1.md docs\l1\WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md | rg "\.(json|ya?ml)$"
python scripts/ci/check_task_doc.py docs\tasks\2026-05-18_v1_threat_formula_focus.md
python scripts/ci/check_handoff_doc.py docs\handoff\2026-05-18_v1_threat_formula_focus.md
```

### Result

- Formula terms are present in central definition and active module docs.
- Stale active behavior-only wording found during validation was patched in manual-label, rule-label, runtime dataflow, threat-definition, threat-flow, inference, data, L0, and L1 docs.
- Remaining `adult/gambling/gate` and `current online L2` hits are compatible residuals that explicitly frame them as auxiliary, exclusion, future-scope, legacy compatibility, or "no current online L2".
- The GATA/GATE filename check found only `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`; no rename was performed.
- No JSON/YAML files were found in the task-scoped changed-file check.
- The first copied external task file failed the repo task checker because it lacked current checker markers; it was replaced with a repo-local wrapper task doc that preserves the external task boundary and passes the checker.
- Final task and handoff checker status: pass.

### Not Run

- unit tests
- runtime smoke tests
- schema validation against runtime artifacts

Reason:

The accepted task is documentation-definition only and explicitly out of scope for runtime, schema, CLI, output, and dataset changes.

Next best check:

If a later implementation task updates schema or runtime behavior, run targeted schema compatibility and inference smoke checks under that separate task.

## 7. Risks / Caveats

- Some legacy compatibility names remain by design, especially route/review terms such as `needs_l2_candidate`; future readers may still need the surrounding clarified wording.
- The repository was dirty before this task. This handoff only claims the task-scoped documentation edits listed above.
- Documentation has been aligned, but no implementation behavior has been validated or changed.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- listed in `## 3. Files Touched`

Doc debt still remaining:

- Future schema or runtime implementation may need explicit formula-alignment fields, but that is outside this task.
- Historical task/handoff docs may still contain older wording as historical records and were not rewritten.

## 9. Recommended Next Step

- Review and accept the documentation definition change.
- Open a separate implementation or schema task only if Warden should add explicit machine-readable fields for `ManipulativeContext`, `InducedHighRiskAction`, `DirectAction`, `RoutedAction`, or `ActionPreparation`.
