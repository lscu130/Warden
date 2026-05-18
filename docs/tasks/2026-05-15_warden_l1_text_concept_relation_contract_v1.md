# Task Metadata

- Task ID: TASK-20260515-WARDEN-L1-TEXT-CONCEPT-RELATION-CONTRACT-V1
- Task Title: Define Warden L1 Text Semantic Concepts And Relation Judgments Contract V1
- Owner Role: Codex
- Priority: P0
- Status: TODO
- Related Module: L1 / Text Tower / Semantic Concepts / Decision Head / Distillation Targets
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260515_WARDEN_L1_TEXT_CONCEPT_RELATION_CONTRACT_V1.md
- Created At: 2026-05-15
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

### 1. 背景

Warden 已经冻结 L0 / L1、Rule Router、vision evidence recovery、Decision Head draft、distillation V0.2 和 threat adjudication flow 的基础合同。当前缺口是：未来小型文本塔到底输出哪些结构化语义概念和证据关系判断，尚未形成独立 L1 contract。

### 2. 目标

新增 L1 text semantic concepts / relation judgments 合同文档，明确 `claimed_identity_candidates`、`text_semantic_concepts`、relation judgments、future Decision Head inputs 和 concept-level evaluation 要求。

### 3. Scope In

允许修改：

- `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- `docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`

### 4. Scope Out

禁止：

- 训练模型；
- 运行 teacher distillation；
- 调用任何外部模型 API；
- 实现 text tower / Decision Head / OCR / YOLO / CLIP / SNet / SpecularNet-like；
- 修改 runtime official schema；
- 修改 label enums；
- 移动或修改 samples；
- 修改 manifests 或 splits；
- 改变 production inference behavior；
- 添加第三方依赖；
- 把本 draft 当 final frozen schema。

### 5. Inputs

- 外部任务文档：`C:\Users\20516\Downloads\TASK_20260515_WARDEN_L1_TEXT_CONCEPT_RELATION_CONTRACT_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`

### 6. Required Outputs

- 新增 `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`
- 新增本 task doc。
- 新增本 handoff。
- 必要时对 active Decision Head / distillation / text pipeline docs 增加短引用。

### 7. Hard Constraints

- Documentation / contract only.
- English section is authoritative.
- New concept JSON examples are draft / conceptual and do not freeze official runtime schema.
- Brand library must remain optional enhancement.
- Text tower must not own final decision.
- Rule Router must not become classifier.

### 8. Interface / Schema Constraints

- Schema changed: no.
- Labels changed: no.
- Runtime interface changed: no.
- CLI changed: no.
- Output schema changed: no.
- Draft examples are conceptual only.

### 9. Expected Outcome And Success Criteria

Expected outcome:

- Warden has a concrete L1 text concept / relation judgment contract for future distillation, text-tower multi-task heads, Decision Head inputs, and concept-level evaluation.

Success criteria:

- L1 text semantic concept groups are explicitly documented.
- Claimed identity candidate extraction is documented.
- Relation judgment concepts are explicitly documented.
- Decision Head concept-to-decision input contract is documented or refined.
- Concept-level evaluation requirements are documented.
- Validation commands run and pass or are explicitly reported.

### 10. Acceptance Criteria

- `claimed_identity_candidates` are documented.
- `text_semantic_concepts` are documented.
- `identity_domain_relation` and other required relation judgments are documented.
- `business_legitimacy_hint` is documented.
- `action surface != threat action` is explicit.
- `payload not observed != automatic benign` is explicit.
- `unknown relation is not malicious` is explicit.
- Rule Router is not a classifier.
- Brand library is optional enhancement, not primary path.
- Text tower does not own final decision.
- Concept-level evaluation is documented.
- No code / schema / labels / data / manifests / splits are changed.

### 11. Validation Checklist

- [ ] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- [ ] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- [ ] Required-term grep in active docs.
- [ ] If distillation docs are updated, grep confirms `rule_router` remains not a teacher label source.
- [ ] `git diff --name-only` scope check.

## English Version

## 1. Background

Warden now has active contracts for L0 / L1 routing, Rule Router diagnostics, visual evidence recovery, future Decision Head ownership, distillation V0.2, and the project-level threat adjudication flow. The remaining gap is a detailed contract for what the future small text tower should learn as structured semantic concepts and relation judgments.

## 2. Goal

Define Warden L1 text semantic concept groups and relation judgment targets so future teacher distillation, text-tower multi-task heads, Decision Head inputs, concept-level evaluation, and error analysis use the same draft contract.

## 3. Scope In

Allowed documentation changes:

- `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- `docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`

## 4. Scope Out

Do not:

- train any model;
- run teacher distillation;
- call MiMo, DeepSeek, OpenAI, Claude, Gemini, or any external model API;
- implement text tower model code;
- implement Decision Head model code;
- implement OCR / YOLO / CLIP / SNet / SpecularNet-like;
- modify runtime official schema;
- change label enums;
- move or modify samples;
- modify manifests or splits;
- change production inference behavior;
- add third-party dependencies;
- treat this draft as final frozen schema.

## 5. Inputs

- `C:\Users\20516\Downloads\TASK_20260515_WARDEN_L1_TEXT_CONCEPT_RELATION_CONTRACT_V1.md`
- Warden governing docs and templates.
- Current L1 / Decision Head / distillation / threat adjudication / text pipeline docs.

## 6. Required Outputs

- New or updated L1 concept contract documentation.
- Minimal active-doc references where needed.
- Task doc and handoff.

## 7. Hard Constraints

- Documentation-only.
- English authoritative.
- Draft JSON examples are not official runtime schema.
- Keep Rule Router, text tower, vision, and Decision Head responsibilities separate.

## 8. Interface / Schema Constraints

- Schema changed: no.
- Backward compatible: yes.
- Public interface changed: no.
- Existing CLI still valid: yes.

## 9. Expected Outcome And Success Criteria

Expected outcome:

- Future Warden L1 training and distillation can target explicit semantic concepts and relation judgments instead of direct final-label shortcuts.

Success criteria:

- Required concept groups are documented.
- Required relation judgments are documented.
- Decision Head input contract is refined at documentation level.
- Concept-level evaluation plan is documented.
- Task and handoff checkers pass.

## 10. Acceptance Criteria

- L1 text semantic concept groups are explicitly documented.
- Claimed identity candidate extraction is documented.
- Relation judgment concepts are explicitly documented.
- Decision Head concept-to-decision input contract is documented or refined.
- Concept-level evaluation requirements are documented.
- Required hard rules are explicit.
- No out-of-scope files or behavior are changed.

## 11. Validation Checklist

- [ ] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- [ ] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- [ ] `rg -n "claimed_identity_candidates|text_semantic_concepts|identity_domain_relation|business_legitimacy_hint|action surface != threat action|payload not observed|unknown relation is not malicious|Decision Head|concept-level evaluation|benign hard negative" docs/l1 docs/distillation docs/modules`
- [ ] `rg -n "rule_router.*not.*teacher label|not teacher label|not final model judgments" docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- [ ] `git diff --name-only`

## 12. Counter-Review Requirements

The handoff must answer whether this task accidentally:

- turned brand-library matching into the primary path;
- made action surfaces equivalent to threat actions;
- made Rule Router a classifier again;
- assigned final decision responsibility to the text tower;
- changed production schema or runtime behavior;
- required final dataset freeze or teacher API calls.

## 13. Stop Rules

Stop as done when required docs exist, references are aligned, validation runs, and scope remains documentation-only.

Stop as blocked if satisfying the task requires code, schema, label, data, manifest, split, runtime, or external API changes.
