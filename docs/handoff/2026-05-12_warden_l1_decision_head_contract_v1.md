# HANDOFF_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1

## 中文版

### 摘要

本次交付新增了 Warden L1 Decision Head / Text Semantic Concept 草案契约文档。交付范围仅限文档：新增 task doc、contract doc 和 handoff。未修改代码、runtime、official schema、标签、manifest、样本、数据切分，也未运行训练、teacher、OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like。

契约文档明确：

- Rule Router 只做路由与证据充分性诊断。
- Text Semantic Concepts 是未来文本塔输出的结构化语义概念。
- vision_evidence 是补证据路径。
- Decision Head 未来负责 L1 final decision。
- 当前契约是 draft，不改变 official runtime schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1
- Related Task ID: TASK-20260512-WARDEN-L1-DECISION-HEAD-CONTRACT-V1
- Task Title: Design Warden L1 Decision Head And Text Semantic Concept Contract V1
- Module: Inference / L1 / Contract / Future Training Interface
- Author: Codex
- Date: 2026-05-12
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

Added a documentation-only draft contract for future L1 Text Semantic Concepts, Visual Evidence Recovery, Structured Feature Builder, L1 Decision Head, Evidence Renderer, and distillation/training alignment. The contract explicitly keeps Rule Router as diagnostics, keeps visual evidence as evidence recovery, assigns future L1 final decision ownership to Decision Head, and states that official runtime schema is unchanged. The task reached its documentation stop condition after required validation.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`.
- Added `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`.
- Added `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`.

### Output / Artifact Changes

- none outside repository docs

## 3. Files Touched

- `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- No runtime behavior changes.
- Future L1 work now has a repository-local draft contract for text semantic concepts and Decision Head inputs / outputs.

### Preserved Behavior

- Official runtime result / trace schema remains unchanged.
- Existing L1 draft sidecar behavior remains unchanged.
- Existing labels, manifests, data splits, and samples remain unchanged.
- Rule Router remains a diagnostic router.
- Decision Head remains `not_run` until a future implementation task.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for runtime outputs
- new documentation defines future draft output terms only

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The contract doc defines draft terms for future implementation. It does not freeze official runtime schema or final L1 output schema.

## 6. Validation Performed

### Commands Run

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md
rg -n "Rule Router|Decision Head|text_semantic_concepts|vision_evidence|action surface != threat action|not final schema|not_run" docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md
```

### Result

- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`
  - `[task-doc] OK   docs\tasks\2026-05-12_warden_l1_decision_head_contract_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`
  - `[handoff-doc] OK   docs\handoff\2026-05-12_warden_l1_decision_head_contract_v1.md`
- Required-term grep matched all required contract terms:
  - `Rule Router`
  - `Decision Head`
  - `text_semantic_concepts`
  - `vision_evidence`
  - `action surface != threat action`
  - `not final schema`
  - `not_run`

### Not Run

- Code tests.
- Runtime smoke.
- Model training.
- Teacher distillation.
- OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference.

Reason:

This task is documentation-only. Code tests and runtime smoke are outside the requested validation. Heavy model paths are explicitly out of scope.

Next best check:

If this draft contract is accepted, run a separate review pass against future implementation task docs before freezing any official runtime schema.

## 7. Risks / Caveats

- This is a draft contract, not final schema.
- Future implementation may need a schema-freeze task before downstream consumers rely on field names.
- The contract does not validate model quality, teacher targets, or Decision Head accuracy.
- Counter-review residual risk: future training work may discover that some fields need versioning or refinement.
- Karpathy guardrail residual risk: validation was limited to documentation checks.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

Doc debt still remaining:

- Future implementation tasks should update module docs when they implement text semantic concepts, visual evidence recovery, structured feature builder, or Decision Head.

## 9. Recommended Next Step

- Review the draft contract for field naming and semantic coverage.
- If accepted, create a separate task for text semantic concept target definitions or Decision Head structured feature builder design.
- Defer final L1 schema freeze until after model and runtime validation.

## 10. Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_L1_DECISION_HEAD_CONTRACT_V1.md`
- `docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`
- `docs/` directory layout

Retrieval / reading performed:

- confirmed `docs/l1/` did not exist and was allowed to be created
- confirmed checker marker requirements
- confirmed latest L1 realignment handoff states Decision Head is `not_run`

Claims supported by evidence:

- The user task requires documentation-only contract work.
- Latest L1 draft semantics separate Rule Router, Text Semantic Concepts, Visual Evidence, and Decision Head.
- Required validation is doc-checker and required-term grep based.

Claims left unsupported or assumed:

- none blocking

Retrieval stopped because:

- The required documentation scope and validation commands were clear.

## 10.1 Counter-Review Performed

Original framing reviewed:

Create a draft contract for future Text Semantic Concepts and L1 Decision Head without implementation, training, heavy inference, or schema freeze.

Assumptions checked:

- `docs/l1/` may be created because the task explicitly permits it.
- Contract wording must not imply official runtime schema change.
- Vision evidence must remain evidence recovery.

Failure modes considered:

- documenting Rule Router as a classifier
- implying current Decision Head is implemented
- treating CLIP / SNet as default online L1 components
- over-specifying model training implementation details

Counterexamples or contradictory evidence found:

- none

Alternative routes considered:

- update existing L1 framework doc
- create a focused new contract doc
- implement code stubs

Framing changed: NO

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- exact future model choice remains unresolved by design

Residual risks after counter-review:

- future implementation may refine field names before final schema freeze

Decision after counter-review:

- ACCEPT_ORIGINAL

## 10.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- The contract is draft and cannot change official runtime schema.
- Any implementation or training work is out of scope.

Ambiguities resolved or escalated:

- No blocker. The task provided exact file paths and validation commands.

### Simplicity First

Simplest acceptable route used:

- Add only the three required Markdown files and run documentation validation.

Larger or more speculative routes rejected:

- code edits
- runtime integration
- model stubs
- schema freeze

### Surgical Changes

Touched-file to task-scope mapping:

- `docs/tasks/2026-05-12_warden_l1_decision_head_contract_v1.md`: active task doc
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`: required contract doc
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`: required handoff

Adjacent cleanup or formatting-only changes:

- none

### Goal-Driven Verification

Verification loop:

- task doc checker -> passed
- handoff checker -> passed
- required-term grep -> matched all required terms
