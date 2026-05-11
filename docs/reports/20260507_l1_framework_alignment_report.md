# Warden L1 Framework Alignment Report - 2026-05-07

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分只供人工快速阅读。

### 摘要

本次对齐把 L1 定义同步为：主判断层、非单体模型、文本/结构主路径、按需视觉证据恢复、OCR/YOLO/CLIP 职责分离、fusion 形成机器判断、解释由 evidence ledger 和 reason codes 确定性渲染。

本次没有修改代码、训练逻辑、CLI、冻结 schema、标签枚举或机器可读输出格式。

### 已更新文件

- `PROJECT.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md`
- `docs/tasks/2026-05-07_warden_l1_framework_definition_update_execution.md`

---

## English Version

> AI note: This English section is authoritative.

# Warden L1 Framework Alignment Report - 2026-05-07

## 1. Evidence Checked

Files read or searched during this alignment:

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `C:\Users\20516\Downloads\TASK_20260507_Warden_L1_Framework_Definition_Update_V0_1.md`
- `docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

Repository search was attempted with `rg`, but the bundled WindowsApps `rg.exe` failed with `拒绝访问`.
PowerShell `Get-ChildItem ... | Select-String` fallback was used for the required L1 / CLIP / OCR / YOLO / fusion / explanation searches.

## 2. Definitions Added Or Updated

### L1 Overall

- Added `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md` as the current L1 framework definition.
- Updated `PROJECT.md` and `MODULE_INFER.md` to state that L1 is the main judgment stage but not a monolithic model.
- Preserved the official `L0 / L1 / L2` top-level stage contract.

### Text Tower

- Updated `Warden_TEXT_PIPELINE_V1.md` to define the text tower as a structured semantic concept and relation-judgment branch.
- Added draft multi-task head groups for action surfaces, behavior contexts, relation/consistency checks, risk axes, page roles, and routing.
- Explicitly stated that action surfaces are not automatically threat actions.

### Visual Path

- Updated `Warden_VISION_PIPELINE_V1.md` to state that the visual path is evidence recovery and evidence localization, not an independent final visual threat judge.
- Preserved the existing decoupled OCR / image-text similarity / detector design.

### OCR / YOLO / CLIP Split

- Added the responsibility split in the new L1 framework doc.
- Updated vision and edge docs to state that CLIP / MobileCLIP provides weak page-level visual prior and routing help, not final malicious / benign judgment.
- Preserved trigger-based OCR and `YOLO26n` detector positioning.

### Fusion And Explanation

- Added a draft L1 fusion definition: concept outputs, structured features, joint signals, OCR evidence, YOLO evidence, and optional weak CLIP priors feed the L1 fusion head.
- Added the constraint that XGBoost, if used, consumes concept outputs and structured/joint features rather than raw text or raw screenshot pixels.
- Added deterministic explanation renderer wording: explanations come from evidence ledger entries and reason codes, not from free-form generation by BERT, CLIP, YOLO, or XGBoost.

## 3. Counter-Review Result

Original framing accepted with compatibility constraints.

Source-backed facts:

- Runtime/dataflow docs preserve `L0 / L1 / L2`, `SampleContext`, lazy heavy artifacts, and do not freeze final OCR / vision / multimodal policy.
- Edge profile freezes `MobileCLIP2-S2`, trigger-based `PP-OCRv4 mobile`, and `YOLO26n`.
- Vision pipeline already says visual outputs are evidence and not final maliciousness labels.
- Threat definition distinguishes high-risk behavior, high-risk action, and `payload not observed`.
- Schema registry does not freeze the draft L1 output names proposed here.

Engineering inference:

- The proposed L1 framework can be documented without changing code or schema because current active docs leave final L1 policy and exact output schema open.
- CLIP responsibility can be narrowed to weak visual prior while preserving `MobileCLIP2-S2` in the edge profile.

Assumption:

- The new framework doc can act as the current L1 design definition until a future implementation or schema task freezes narrower contracts.

Risks checked:

- CLIP is not documented as a final malicious / benign classifier.
- OCR remains trigger-based and not always-on.
- YOLO remains a local atomic evidence detector.
- Draft L1 output terms are marked conceptual rather than frozen schema.
- Login, download, payment, wallet, support, and redirect surfaces are not treated as automatically malicious.
- No brand-domain mismatch one-factor malicious rule was introduced.

Decision:

- Accept the proposed framing.
- No escalation was required because active docs did not force schema, code, runtime profile, or deployment-default changes.

## 4. Schema / Interface Impact

- Schema changed: No
- Public interface changed: No
- CLI changed: No
- Output JSON schema changed: No
- Backward compatible: Yes

Draft terms such as `final_label`, `risk_score`, `confidence`, `malicious_basis`, `payload_observed`, `page_role`, `risk_axes`, and routing decision are documented as draft / proposed / conceptual, not frozen machine-readable schema.

## 5. Unresolved Conflicts

None found in active docs checked for this task.

## 6. Remaining Future Work

- exact model training targets;
- exact OCR / YOLO / CLIP trigger thresholds;
- final output schema;
- evaluation buckets;
- teacher distillation schema;
- implementation and benchmark validation.
