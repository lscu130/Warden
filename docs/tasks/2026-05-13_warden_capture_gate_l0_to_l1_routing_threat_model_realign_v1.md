# Task Metadata

- Task ID: TASK_20260513_WARDEN_L0_TO_L1_ROUTING_THREAT_MODEL_REALIGN_V1
- Task Title: Warden Capture Gate L0 To L1 Routing Threat Model Realign V1
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: docs / runtime / l1
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260513_WARDEN_L0_TO_L1_ROUTING_THREAT_MODEL_REALIGN_V1_REVISED.md
- Created At: 2026-05-13
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

### 1. 背景

用户提供的外部任务文件要求修正 Warden 的 L0 -> L1 路由定义和威胁模型边界。核心修正点是：无效采集样本不进入 Warden 威胁标签体系；L0 只处理少数便宜 terminal / auxiliary bucket；所有有效且未被 L0 终止的样本进入 L1；Rule Router 只能做路由与证据充分性诊断。

### 2. 目标

将文档、runtime skeleton 和 L1 draft Rule Router 的窄合同对齐到以下语义：

- 无效采集、HTTP 错误页、空白页、纯色渲染页、严重渲染失败页、证据不可观测页面在正式 train / validation / test 前由项目负责人移除。
- L0 只处理 adult、gambling、明显 gate / challenge / verification 等高置信、低成本 terminal / auxiliary bucket。
- 所有有效且未被 L0 terminal 的网页样本进入 L1。
- L1 text branch 是默认判断路径。
- L1 vision 只做 evidence recovery。
- Rule Router 不输出 final-like labels，也不实现 recrawl / exclude / QA 路由。

### 3. 范围内

- 更新 L0 / L1 路由相关文档。
- 更新威胁模型和数据集边界文档。
- 对已有 runtime L0 routing contract 做最小必要修正。
- 对已有 L1 draft Rule Router 做最小必要修正。
- 调整窄测试覆盖本任务验收点。
- 新增 handoff。

### 4. 范围外

- 不训练模型。
- 不跑 teacher distillation。
- 不调用外部模型。
- 不跑 OCR / YOLO / CLIP / MobileCLIP / SNet / SpecularNet-like。
- 不修改真实数据集样本。
- 不移动、删除、重命名样本目录。
- 不修改 manifest / split。
- 不把 invalid capture 标记为 benign、malicious 或 suspicious。
- 不实现 recrawl / exclude / QA 队列。
- 不创建无效样本保留池。
- 不冻结最终 L1 output schema。

### 5. 验收标准

- 文档不把无效采集样本写成 Warden 威胁模型标签。
- 文档说明无效采集样本由项目负责人在正式 split 前移除。
- 文档不要求实现 recrawl / exclude / QA 路由或无效样本保留池。
- L0 定义为 cheap screening / terminal routing。
- 有效 non-terminal 样本 route to L1。
- L1 text branch 是默认判断路径。
- L1 vision 是 evidence recovery。
- Rule Router 不输出 final-like labels。
- 代码改动保持 official runtime schema 兼容。
- 测试覆盖 L0 terminal auxiliary、valid non-terminal route to L1、invalid capture 不转成 final labels、Rule Router 不输出 final-like labels。

### 6. 验证清单

- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `pytest tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_pipeline_skeleton.py -q`
- Focused grep for invalid capture / recrawl / route_to_l1 / Rule Router / final-like residuals.

## English Version

## 1. Background

The user-provided external task file requires realigning Warden's L0 -> L1 routing definition and threat-model boundary. The key correction is that invalid captures are not Warden threat-model samples; L0 handles only a small set of cheap terminal / auxiliary buckets; every valid sample not terminated by L0 routes to L1; and Rule Router remains a routing and evidence-sufficiency diagnostic component.

## 2. Goal

Align docs, the runtime skeleton, and the L1 draft Rule Router to these semantics:

- Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are removed by the project owner before formal train / validation / test construction.
- L0 handles only high-confidence cheap terminal or auxiliary buckets such as adult, gambling, and obvious gate / challenge / verification.
- Every valid webpage sample not terminated by L0 routes to L1.
- The L1 text branch is the default judgment path.
- L1 vision is evidence recovery only.
- Rule Router must not emit final-like labels or implement recrawl / exclude / QA routing.

## 3. Scope In

This task is allowed to touch:

- `AGENTS.md`
- `PROJECT.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `src/warden/runtime/pipeline.py`
- `src/warden/l1/rule_baseline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- task and handoff docs for this task

This task is allowed to change:

- Documentation wording for invalid captures, L0 / L1 routing, L1 vision, and Rule Router boundaries.
- Runtime L0 next-stage selection so valid non-terminal samples route to L1 by default.
- L1 draft Rule Router so insufficient observability stays diagnostic and does not emit recrawl routing.
- Narrow tests for the above.

## 4. Scope Out

This task must NOT do the following:

- Train models.
- Run teacher distillation.
- Call external model APIs.
- Run OCR / YOLO / CLIP / MobileCLIP / SNet / SpecularNet-like.
- Modify real dataset samples.
- Move, delete, or rename sample directories.
- Modify manifest / split files.
- Label invalid captures as benign, malicious, or suspicious.
- Implement recrawl / exclude / QA queues.
- Create an invalid-sample retention pool.
- Freeze final L1 output schema.
- Change official runtime output contract except through compatible existing fields and draft/debug sidecar behavior.

## 5. Inputs

Relevant inputs for this task:

### Docs

- `C:\Users\20516\Downloads\TASK_20260513_WARDEN_L0_TO_L1_ROUTING_THREAT_MODEL_REALIGN_V1_REVISED.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- L0 / L1 / runtime / threat-model / dataset docs listed in scope.

### Code / Scripts

- `src/warden/runtime/pipeline.py`
- `src/warden/l1/rule_baseline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- `docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`

### Missing Inputs

- none

## 6. Required Outputs

- Updated docs / code / tests in the repo.
- `docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- Final response with summary, files changed, validation, compatibility impact, risks, evidence, and stop condition.

## 7. Hard Constraints

- Keep changes surgical and traceable to this task.
- Preserve backward compatibility for official runtime result / trace schema.
- Treat existing dirty worktree changes as prior/user work; do not revert them.
- Do not broaden the task into model training, dataset editing, or visual-model execution.

## 8. Interface / Schema Constraints

- Schema changed: no intended official schema change.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.
- Draft/debug L1 sidecar may change only within existing draft status.

## 9. Expected Outcome And Success Criteria

Expected outcome:

Warden's active docs and narrow runtime / L1 draft routing behavior reflect the revised L0 -> L1 and invalid-capture semantics without expanding scope into training, dataset mutation, visual-model execution, or final L1 schema freeze.

Success criteria:

- Docs do not describe invalid captures as Warden threat labels.
- Docs state invalid captures are removed by the project owner before formal train / validation / test construction.
- Docs do not require recrawl / exclude / QA routing or invalid-sample retention.
- L0 is defined as cheap screening / terminal routing rather than ordinary benign / malicious classification.
- Valid non-terminal samples route to L1.
- L1 text branch is the default judgment path.
- L1 vision is evidence recovery, not a final classifier.
- Rule Router does not emit final-like labels.
- Official runtime schema compatibility is preserved.
- Narrow tests cover the relevant routing semantics.

## 10. Acceptance Criteria

- Docs do not describe invalid captures as Warden threat labels.
- Docs state invalid captures are removed by the project owner before formal train / validation / test construction.
- Docs do not require recrawl / exclude / QA routing or invalid-sample retention.
- L0 is defined as cheap screening / terminal routing rather than ordinary benign / malicious classification.
- Valid non-terminal samples route to L1.
- L1 text branch is the default judgment path.
- L1 vision is evidence recovery, not a final classifier.
- Rule Router does not emit final-like labels.
- Official runtime schema compatibility is preserved.
- Narrow tests cover the relevant routing semantics.

## 11. Validation Checklist

- Run task doc checker.
- Run handoff checker.
- Run targeted infer tests.
- Run focused grep over docs / src / tests for invalid capture, recrawl, route_to_l1, Rule Router, and final-like residuals.

## 12. Evidence / Retrieval Rules

Facts or claims that require support:

- Current L0 / L1 routing and Rule Router behavior.
- Existing docs that mention invalid captures, recrawl routing, L0 terminal buckets, L1 vision, or final-like labels.
- Validation results.

Allowed evidence sources:

- Current repository files.
- User-provided task file.
- Local command output.

Retrieval budget:

- Initial retrieval: governing docs, task file, L0 / L1 / runtime docs, runtime and L1 draft code, focused tests.
- Additional retrieval is allowed only when a residual grep hit or failing test points to another active contract.
- Stop retrieval when focused docs/code/tests cover all acceptance criteria or when a scope conflict requires user approval.

Missing-evidence behavior:

- Mark any unverified claim explicitly and do not infer results from planned checks.

### 7.1 Counter-Review Requirements

Required because this task touches architecture, threat-model semantics, labels, dataset admission, and routing behavior.

Counter-review checks:

- Do not convert invalid captures into benign / malicious / suspicious labels.
- Do not turn Rule Router into a classifier.
- Do not implement recrawl / exclude / QA queues.
- Do not freeze final L1 output schema.
- Preserve official runtime result / trace compatibility.

## 13. Stop Rules

Stop as done when:

- All acceptance criteria are represented in docs and targeted code/tests.
- Targeted validation passes or any non-run item is explicitly reported.
- Handoff records docs changed, code changed, schema impact, validation, risks, and next step.

Stop as blocked when:

- A required change would need dataset mutation, manifest / split edits, external model execution, or final L1 schema freeze.

## 14. Output

- Updated docs / code / tests in the repo.
- `docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- Final response with summary, files changed, validation, compatibility impact, risks, evidence, and stop condition.
