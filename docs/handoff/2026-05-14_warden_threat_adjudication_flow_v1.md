# Handoff Metadata

- Handoff ID: HANDOFF-20260514-WARDEN-THREAT-ADJUDICATION-FLOW-V1
- Related Task ID: TASK-20260514-WARDEN-THREAT-ADJUDICATION-FLOW-V1
- Task Title: Define Warden Threat Adjudication Flow V1
- Module: Threat Model / L1 / Distillation / Decision Head
- Author: Codex
- Date: 2026-05-15
- Status: DONE

## 中文版

### 1. 执行摘要

本次新增了 Warden 项目级威胁判定流程文档 `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`，并对 active PROJECT / README / L1 / distillation / text pipeline / L1 framework 文档做了最小引用对齐。

核心语义已冻结到文档层：`action surface != threat action`、`payload not observed != automatic benign`、`unknown is not malicious`、宣称身份抽取是主路径、品牌库只是可选增强、Rule Router 不是 classifier、vision evidence 不是 final judgment、future Decision Head 字段是 conceptual / draft 且 not final schema。

本任务只改文档。没有修改代码、runtime、CLI、schema、labels、manifest、split、samples、data、crawler、training、inference 或 distillation runner。

## English Version

## 1. Executive Summary

This delivery added the central Warden threat adjudication flow document and aligned active related documentation with it.

The new document defines the full evidence-to-decision flow for Warden social-engineering threat adjudication, including claimed identity extraction, action surface extraction, high-risk behavior context, relation / business legitimacy checks, action-surface to threat-action escalation, final decision semantics, behavior-only malicious cases, benign hard negatives, and unknown / insufficient-evidence handling.

The task reached its documentation-only stop condition after required validation.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`.
- Added repo-local task doc.
- Added this handoff.
- Updated `PROJECT.md` and `README.md` to point to the new central adjudication-flow document.
- Updated `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md` so text concepts, vision evidence, and future Decision Head fields are interpreted through the new flow.
- Updated distillation V0.2 workflow / prompt pack to reference the flow and preserve claimed identity, action-surface, advisory target, and `unknown` semantics.
- Updated active text / L1 framework docs with minimal references to the central flow.

### Output / Artifact Changes

- New documentation contract under `docs/threat_model/`.
- No runtime output or machine-readable schema changed.

## 3. Files Touched

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `PROJECT.md`
- `README.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`

## 4. Behavior Impact

### Expected New Behavior

- Documentation consumers now have one central threat adjudication flow to use for L1 semantics.
- Active docs now point to that flow for claimed identity extraction, action-surface escalation, business legitimacy, behavior-only malicious, benign hard negative, and unknown / insufficient-evidence semantics.

### Preserved Behavior

- No code behavior changed.
- Rule Router remains a routing and evidence-sufficiency diagnostic component.
- Vision evidence remains OCR / YOLO evidence recovery only.
- CLIP / MobileCLIP / SNet / SpecularNet-like routes remain outside the default online L1 mainline.
- Future Decision Head fields remain conceptual / draft and not final runtime schema.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: no
- Backward compatible: yes
- Public interface changed: no
- Existing CLI still valid: yes

Affected schema fields / interfaces:

- none

Compatibility notes:

This task is documentation-only. The conceptual Decision Head output example in the new document is explicitly marked as not final runtime schema and does not change any current runtime result, trace, manifest, label, or split format.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260514_WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `README.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- active module docs found by focused grep

Retrieval / reading performed:

- Read the external task document and mandatory governing docs.
- Inspected active project, README, L1, distillation, frozen L1 framework, text pipeline, and vision pipeline docs.
- Ran focused search for action-surface, claimed-identity, business-legitimacy, Rule Router, Decision Head, CLIP / SNet, and schema-boundary wording.

Claims supported by evidence:

- Existing active docs already defined L0 / L1, Rule Router, Decision Head draft, distillation V0.2, and vision evidence recovery boundaries.
- The repo did not have `docs/threat_model/` before this task; it was created for the required new document.

Claims left unsupported or assumed:

- none material for this documentation task

Retrieval stopped because:

- Required docs were available, the central adjudication flow could be written, and active related docs could be aligned with minimal documentation patches.

## 6.1 Counter-Review Performed

Original framing reviewed:

Define Warden threat adjudication flow as a project-level contract that can guide labels, distillation, text concepts, Decision Head design, and L1 explanations.

Assumptions checked:

- Brand/domain mismatch must remain a candidate conflict signal, not a single-factor malicious rule.
- Login / download / payment / wallet / support / KYC / QR / redirect surfaces must remain action surfaces until context supports threat-action escalation.
- `payload not observed` must remain an evidence state and must not become benign.
- Invalid capture must remain outside threat labels.
- Rule Router must remain non-classifier.
- CLIP / SNet must remain outside the default online L1 mainline.
- Future Decision Head examples must remain conceptual / draft and not final schema.
- `unknown` must remain separate from malicious.
- Benign hard negatives and behavior-only malicious pages must both remain represented.

Decision:

- Accept the task framing with documentation-only scope.
- Use a central threat-model document and minimal references in active docs.

## 6. Validation Performed

### Commands Run

```powershell
python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md
rg -n "action surface != threat action|payload not observed|claimed identity|business legitimacy|malicious_behavior_only|benign_hard_negative|unknown is not malicious|Rule Router|Decision Head|not final schema" docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md
git diff --name-only
```

### Result

- Initial `check_task_doc.py`: failed on required fixed heading markers; task doc was patched to include the checker-required markers.
- Initial `check_handoff_doc.py`: failed on required fixed heading markers; handoff was patched to include the checker-required markers.
- Final `check_task_doc.py`: passed.
- Final `check_handoff_doc.py`: passed.
- Required-term grep: passed and returned hits for all required terms in `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`.
- `git diff --name-only`: completed and showed documentation-only tracked diffs for this task plus existing dirty documentation state. Untracked task / handoff / threat-model files are reported separately by `git status`.

### Not Run

Full test suite was not run because this is documentation-only and explicitly excludes code/runtime/data behavior changes.

## 7. Risks / Caveats

- Historical ADRs, older tasks, older handoffs, and historical benchmark reports were not rewritten.
- Current worktree had pre-existing dirty / untracked changes before this task. Review and staging should isolate this task's documentation files only.
- The new document provides conceptual future Decision Head output examples. They are explicitly not final runtime schema.

## 8. Docs Impact

- Adds a new central active adjudication-flow reference under `docs/threat_model/`.
- Active related docs now reference it.
- No implementation instructions were added beyond documentation semantics.

## 9. Recommended Next Step

Use the new adjudication flow as the reference for a follow-up task that refines `text_semantic_concepts` and `decision_head_auxiliary_targets` training-target definitions without changing runtime schema.

## 10. Stop Condition

Stop when the central threat adjudication flow document exists, active related docs are minimally aligned, required checker and grep validation are run, and no code/schema/data scope change is introduced.
