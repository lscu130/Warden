# Handoff Metadata

- Handoff ID: HANDOFF-20260515-WARDEN-L1-TEXT-CONCEPT-RELATION-CONTRACT-V1
- Related Task ID: TASK-20260515-WARDEN-L1-TEXT-CONCEPT-RELATION-CONTRACT-V1
- Task Title: Define Warden L1 Text Semantic Concepts And Relation Judgments Contract V1
- Module: L1 / Text Tower / Semantic Concepts / Decision Head / Distillation Targets
- Author: Codex
- Date: 2026-05-15
- Status: DONE

## 中文版

### 1. 执行摘要

本次新增 `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`，把 Warden 未来 L1 文本塔要学习的结构化语义概念、关系判断、Decision Head 输入和 concept-level evaluation 要求写成 draft contract。

本任务只改文档。没有训练模型，没有运行 teacher distillation，没有调用外部 API，没有修改 runtime official schema、label enum、样本、manifest、split 或 production inference behavior。

## English Version

## 1. Executive Summary

This delivery added the Warden L1 text semantic concepts and relation judgments draft contract.

The new contract defines `claimed_identity_candidates`, `text_semantic_concepts`, identity claim concepts, action surface concepts, behavior context concepts, relation judgments, evidence state concepts, threat action candidate concepts, Decision Head concept inputs, and concept-level evaluation requirements.

The task reached its documentation-only stop condition after validation.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`.
- Added repo-local task doc.
- Added this handoff.
- Updated `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md` to reference the new concept contract and include claimed identity candidates / relation judgments as future Decision Head inputs.
- Updated `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md` to reference the new concept groups and relation-judgment principle.
- Updated `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md` to point prompt targets at the new concept contract.
- Updated `docs/modules/Warden_TEXT_PIPELINE_V1.md` with the detailed concept-contract reference and unknown-relation rule.

### Output / Artifact Changes

- New documentation contract under `docs/l1/`.
- No machine-readable runtime output or schema changed.

## 3. Files Touched

- `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`
- `docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- `docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`

## 4. Behavior Impact

### Expected New Behavior

- Future L1 text-tower and teacher-distillation design now has a concrete draft target contract for concept and relation heads.
- Future Decision Head design has a clearer conceptual input contract.
- Future evaluation planning can distinguish concept extraction errors, relation judgment errors, and Decision Head weighting errors.

### Preserved Behavior

- Rule Router remains a routing and evidence-sufficiency diagnostic component, not a classifier.
- Text tower outputs concepts and relation judgments, not final decisions.
- Vision remains OCR / YOLO evidence recovery only.
- Decision Head remains the future final-decision owner.
- Brand library remains optional enhancement, not the primary path.

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

All JSON examples in the new contract are draft / conceptual. They do not change official runtime schema, labels, manifests, splits, samples, or distillation runner outputs.

## 5.1 Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260515_WARDEN_L1_TEXT_CONCEPT_RELATION_CONTRACT_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`

Retrieval / reading performed:

- Read the external task and mandatory governing docs.
- Inspected existing L1, Decision Head, distillation, threat adjudication, and text pipeline docs before patching.
- Used focused grep / status validation after edits.

Claims supported by evidence:

- Existing L1 Decision Head contract already treated `text_semantic_concepts` as a stub placeholder and Decision Head as future final owner.
- Existing distillation V0.2 docs already treated `rule_router` as diagnostics and advisory targets as non-gold.
- Existing text pipeline docs already positioned text concepts as bounded concept heads, not free-form reasoning.

Claims left unsupported or assumed:

- none material for this documentation task

Retrieval stopped because:

- The active docs were sufficient to place a single detailed L1 concept contract and minimal references without duplicating conflicting contracts.

## 5.2 Counter-Review Performed

Original framing reviewed:

Define L1 text semantic concepts and relation judgments for future small text tower / distillation / Decision Head use.

Required risk checks:

1. Did this task accidentally turn brand-library matching into the primary path?
   - No. The new contract states `claimed_identity_candidates` are extracted from source-aware evidence, and brand library is optional enhancement only.

2. Did this task accidentally make action surfaces equivalent to threat actions?
   - No. The new contract explicitly states `action surface != threat action` and defines threat-action candidate escalation as action surface plus behavior context / relation conflict / illegitimate business context.

3. Did this task accidentally make Rule Router a classifier again?
   - No. Rule Router remains diagnostics only.

4. Did this task assign final decision responsibility to the text tower?
   - No. Text tower outputs concepts and relation judgments; Decision Head owns future final decision.

5. Did this task change production schema or runtime behavior?
   - No. This is documentation-only and all JSON examples are draft / conceptual.

6. Did this task require final dataset freeze or teacher API calls?
   - No. It defines future targets only and does not run teacher distillation.

Decision:

- Accept the task framing with documentation-only scope.
- Use one new central L1 concept contract plus minimal references in active docs.

## 6. Validation Performed

### Commands Run

```powershell
python scripts/ci/check_task_doc.py docs/tasks/2026-05-15_warden_l1_text_concept_relation_contract_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-15_warden_l1_text_concept_relation_contract_v1.md
rg -n "claimed_identity_candidates|text_semantic_concepts|identity_domain_relation|business_legitimacy_hint|action surface != threat action|payload not observed|unknown relation is not malicious|Decision Head|concept-level evaluation|benign hard negative" docs/l1 docs/distillation docs/modules
rg -n "rule_router.*not.*teacher label|not teacher label|not final model judgments" docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md
git diff --name-only
```

### Result

- Task doc checker: passed.
- Handoff checker: passed after heading-template alignment.
- Required-term grep: passed.
- Distillation Rule Router residual grep: passed.
- Scope check: task-scoped changes are documentation-only. Broader `git diff --name-only` also reports pre-existing dirty docs from earlier accepted work.

### Not Run

Full test suite was not run because this task is documentation-only and explicitly excludes code/runtime/data behavior changes.

## 7. Risks / Caveats

- Historical ADRs, old tasks, old handoffs, and historical benchmark reports were not rewritten.
- Current worktree had pre-existing dirty / untracked changes before this task. Review and staging should isolate this task's documentation files only.
- The new concept contract is draft / conceptual and not final runtime schema.

## 8. Docs Impact

- Adds a detailed active L1 text concept / relation judgment contract.
- Aligns active Decision Head, distillation, prompt, and text pipeline docs through short references.
- Does not change implementation requirements.

## 9. Recommended Next Step

Use this contract in a follow-up task to refine teacher prompt templates or mock distillation output shape, still without freezing official runtime schema.

## 10. Stop Condition

Stop when the new concept contract exists, active references are aligned, required validation runs, and scope remains documentation-only.
