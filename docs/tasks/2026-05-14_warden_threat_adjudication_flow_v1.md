# Task Metadata

- Task ID: TASK-20260514-WARDEN-THREAT-ADJUDICATION-FLOW-V1
- Task Title: Define Warden Threat Adjudication Flow V1
- Owner Role: Codex
- Priority: P0
- Status: TODO
- Related Module: Threat Model / L1 / Distillation / Decision Head
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260514_WARDEN_THREAT_ADJUDICATION_FLOW_V1.md
- Created At: 2026-05-14
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

### 1. 背景

Warden 已经完成 L0 / L1、invalid capture、Rule Router、Decision Head、vision evidence recovery 和 distillation V0.2 的多处局部定义，但还缺一个项目级威胁判定流程文档，把行为、动作表面、身份宣称、业务合法性、payload 观察状态和最终 L1 decision 语义连成一个可复用合同。

### 2. 目标

新增 `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`，并对齐相关 active 文档引用，使 Warden 的网页社会工程威胁判定流程可被人审、teacher distillation、`text_semantic_concepts`、`decision_head_auxiliary_targets`、未来 L1 Decision Head 和错误分析共同使用。

### 3. 范围内

- 新增 threat adjudication flow 文档。
- 新增本 repo-local task doc。
- 新增本任务 handoff。
- 必要时更新 `PROJECT.md`、`README.md`、L1 Decision Head contract、distillation V0.2 workflow / prompts、active module docs 的短引用或冲突措辞。

### 4. 范围外

- 不修改 production code。
- 不修改 runtime、CLI、schema、labels、manifest、split、samples 或数据文件。
- 不实现 OCR / YOLO / CLIP / SNet / SpecularNet-like 路径。
- 不训练模型。
- 不跑 teacher distillation。
- 不实现或改变 distillation runner behavior。
- 不冻结 final L1 output schema。
- 不添加依赖。
- 不调用外部 API。

### 5. 验收标准

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md` 存在。
- 文档双语：中文摘要在前，英文权威全文在后。
- 文档定义完整 adjudication flow。
- 文档包含 claimed identity extraction。
- 文档包含 action surface vs threat action。
- 文档包含 behavior-only malicious。
- 文档包含 benign hard negative。
- 文档包含 insufficient evidence / unknown。
- 文档说明 invalid capture outside threat labels。
- 文档说明 `payload not observed` is not automatic benign。
- 文档说明 `unknown is not malicious`。
- 文档说明 future Decision Head output examples are conceptual / draft, not final schema。
- Active related docs 已对齐或记录为不适用。
- 不修改代码、schema、labels、data、manifest、split。
- Task checker 和 handoff checker 通过。

### 6. 验证清单

- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `rg -n "action surface != threat action|payload not observed|claimed identity|business legitimacy|malicious_behavior_only|benign_hard_negative|unknown is not malicious|Rule Router|Decision Head|not final schema" docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `git diff --name-only`

## English Version

## 1. Background

Warden has already aligned several local contracts around L0 / L1 routing, invalid-capture handling, Rule Router diagnostics, Decision Head draft ownership, visual evidence recovery, and distillation V0.2. The project still needs one central threat adjudication flow document that connects observed webpage evidence to final L1 decision semantics.

## 2. Goal

Create a project-level threat adjudication flow document and align active documentation references so human labelers, teacher-distillation prompts, text semantic concept definitions, Decision Head design, L1 error analysis, and project-level threat-model explanations use the same adjudication contract.

## 3. Scope In

This task is allowed to touch documentation only:

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `PROJECT.md`
- `README.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`, only for a minimal active-reference note if needed
- `docs/modules/*`, only where active L1 / threat-model wording conflicts or needs a minimal reference
- `docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`

## 4. Scope Out

This task must not:

- modify production code;
- modify runtime behavior;
- modify CLI behavior;
- modify schemas or final output formats;
- modify labels or label enums;
- modify manifests, splits, samples, or data files;
- implement OCR, YOLO, CLIP, SNet, or SpecularNet-like paths;
- train models;
- run teacher distillation;
- change distillation runner behavior;
- freeze final L1 output schema;
- add dependencies;
- call external APIs.

## 5. Inputs

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

## 6. Required Outputs

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`
- Minimal active-doc reference updates where needed.

## 7. Hard Constraints

- Documentation-only task.
- English authoritative in Markdown deliverables.
- Active docs only; historical ADRs, old tasks, old handoffs, and old benchmark reports must not be rewritten unless they are active contracts.
- Future Decision Head fields must be marked conceptual / draft / not final runtime schema.

## 8. Interface / Schema Constraints

- Schema changed: no.
- Labels changed: no.
- Runtime interface changed: no.
- CLI changed: no.
- Output schema changed: no.
- New document examples are conceptual / draft only and do not freeze final runtime schema.

## 9. Expected Outcome And Success Criteria

Expected outcome:

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md` becomes the central active contract for Warden threat adjudication semantics.
- Active related docs point to the new document or remain already compatible.

Success criteria:

- The new document includes every required adjudication section from the external task.
- Active related docs do not contradict the new flow.
- No code, runtime, schema, label, manifest, split, sample, data, crawler, training, inference, or distillation-runner changes are made.
- Required checkers and grep validation pass.

## 10. Acceptance Criteria

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md` exists.
- It is bilingual: Chinese summary first, English authoritative section second.
- It defines the full adjudication flow.
- It includes claimed identity extraction.
- It includes action surface vs threat action.
- It includes behavior-only malicious.
- It includes benign hard negative.
- It includes insufficient evidence / unknown behavior.
- It states invalid capture is outside threat labels.
- It states `payload not observed` is not automatic benign.
- It states `unknown is not malicious`.
- It states future Decision Head output examples are conceptual / draft, not final schema.
- Active related docs are aligned or marked as not applicable.
- No code / schema / labels / data / manifests / splits are changed.
- Task checker and handoff checker pass.

## 11. Validation Checklist

- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`
- [x] Required-term grep on `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- [x] `git diff --name-only`

## 12. Detailed Scope Notes

This task is allowed to touch:

- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- `PROJECT.md`
- `README.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`, only for a minimal active-reference note if needed
- `docs/modules/*`, only where active L1 / threat-model wording conflicts or needs a minimal reference
- `docs/tasks/2026-05-14_warden_threat_adjudication_flow_v1.md`
- `docs/handoff/2026-05-14_warden_threat_adjudication_flow_v1.md`

This task is allowed to change:

- Documentation wording and references only.
- Contract alignment text only.

## 13. Detailed Scope Out Notes

This task must not:

- modify production code;
- modify runtime behavior;
- modify CLI behavior;
- modify schemas or final output formats;
- modify labels or label enums;
- modify manifests, splits, samples, or data files;
- implement OCR, YOLO, CLIP, SNet, or SpecularNet-like paths;
- train models;
- run teacher distillation;
- change distillation runner behavior;
- freeze final L1 output schema;
- add dependencies;
- call external APIs.

## 14. Detailed Inputs

### Docs

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

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- Previous invalid-capture residual cleanup context, used only as current repository state and not as authority over this task.

### Missing Inputs

- none identified before execution.

## 15. Evidence / Retrieval Rules

Facts or claims that require support:

- Current L0 / L1 architecture statements.
- Rule Router and Decision Head ownership statements.
- Distillation target and prompt alignment statements.
- Invalid-capture boundary statements.

Allowed evidence sources:

- Current user-provided task file.
- Active Warden governing docs.
- Active module and distillation docs.
- Focused grep / checker output.

Retrieval budget:

- Initial retrieval: task doc, governing docs, PROJECT, README, L1 Decision Head contract, distillation V0.2 workflow and prompts, active module docs found by focused grep.
- Additional retrieval is allowed only when a referenced active doc is missing or grep reveals a direct conflict.
- Stop retrieval when the central document can be written and active related docs can be aligned with minimal changes.

Missing-evidence behavior:

- Record missing docs in the handoff and continue with available active docs.

### 15.1 Counter-Review Requirements

Required. Before completion, check:

- brand/domain mismatch does not become a single-factor malicious rule;
- action surface does not become automatic threat action;
- `payload not observed` does not become benign;
- invalid capture does not become a threat label;
- Rule Router is not treated as classifier;
- CLIP / SNet are not implied as online default L1 modules;
- final runtime schema is not frozen accidentally;
- `unknown` is not equivalent to malicious;
- benign hard negatives are preserved;
- behavior-only malicious pages are preserved.

## 16. Additional Hard Constraints

- Documentation-only task.
- English authoritative in Markdown deliverables.
- Active docs only; historical ADRs, old tasks, old handoffs, and old benchmark reports must not be rewritten unless they are active contracts.
- Future Decision Head fields must be marked conceptual / draft / not final runtime schema.

## 17. Validation Checklist Detail

- Same as section 11.

## 18. Stop Rules

Stop as done when:

- the central threat adjudication flow document exists and contains required sections;
- active related docs are minimally aligned or explicitly recorded as already compatible / not applicable;
- required validation commands are run and reported;
- scope check confirms no code/schema/data files were changed by this task.

Stop as blocked when:

- the repository requires changes outside documentation scope to satisfy the task;
- checker failures require non-document changes;
- active docs conflict in a way that cannot be resolved without changing frozen schema, labels, runtime, or data.
