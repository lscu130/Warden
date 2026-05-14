# Handoff Metadata

- Handoff ID: HANDOFF_20260513_WARDEN_L0_TO_L1_ROUTING_THREAT_MODEL_REALIGN_V1
- Related Task ID: TASK_20260513_WARDEN_L0_TO_L1_ROUTING_THREAT_MODEL_REALIGN_V1
- Task Title: Warden Capture Gate L0 To L1 Routing Threat Model Realign V1
- Module: docs / runtime / l1
- Author: Codex
- Date: 2026-05-13
- Status: DONE

## 中文版

### 1. 执行摘要

本次按用户修订任务对齐了 Warden 的 invalid capture、L0 -> L1 路由、L1 vision、Rule Router 边界。无效采集样本被定义为数据集构建阶段移除对象，不进入 benign / malicious / suspicious 威胁标签体系。L0 现在在 runtime skeleton 中对有效 non-terminal 样本默认进入 L1；高置信 specialized terminal / auxiliary bucket 可在 L0 终止。L1 draft Rule Router 取消 `need_recrawl` / `route_to_recrawl` 输出，保留证据充分性诊断和 review routing。

### 2. 实际变更

代码变更：

- `src/warden/runtime/pipeline.py`：L0 routing fallback 改为 valid non-terminal -> L1；新增 L0 specialized terminal auxiliary 终止分支。
- `src/warden/l1/rule_baseline.py`：Rule Router 不再输出 `need_recrawl` / `route_to_recrawl`；无效采集类观测不足样本转为 `insufficient_observability` / `need_review` 诊断。
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`：移除 L1 draft benchmark 中的 `need_recrawl` CSV 列和 routing count。

文档变更：

- 更新 `AGENTS.md`、`PROJECT.md`、threat definition、dataset spec、L1 framework、MODULE_DATA、L0 design、runtime dataflow spec、L1 Decision Head contract。
- 新增 repo-local task doc。
- 本 handoff 记录实际执行结果。

测试变更：

- 增加 valid non-terminal L0 sample route to L1 覆盖。
- 增加 L0 terminal auxiliary bucket 不进入普通 L1 覆盖。
- 增加 invalid-capture-like L1 draft diagnostic-only 覆盖。
- 更新 benchmark 测试，移除 `need_recrawl` 期望。

### 3. 触及文件

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
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`

### 4. 行为影响

- 有效且未被 L0 terminal 的样本在 runtime skeleton 中进入 L1。
- 高置信 specialized fast-resolution adult / gambling / gate auxiliary bucket 可在 L0 以 `l0_terminal_auxiliary_bucket` 终止。
- L1 draft Rule Router 对证据不可观测样本只输出诊断和 review routing，不输出 recrawl routing，也不输出 final label。

### 5. Schema / 接口影响

- Schema changed: no for official runtime result / trace schema versions.
- Backward compatible: partially. Official runtime schema shape/version preserved, but L0 routing outcome values and L1 draft/debug-sidecar metric fields changed.
- Public interface changed: no public CLI change.
- Existing CLI still valid: yes.
- Docs updated: yes.

兼容性说明：`routing_outcome.outcome_kind` 新增/改用 `route_to_l1_default` 和 `l0_terminal_auxiliary_bucket`。这是现有 routing outcome 字段内的值变化，不是 schema version bump。L1 draft benchmark CSV 移除了 `l1_draft_need_recrawl`，属于 draft/debug review layer 变化。

### 6. 证据 / 检索

实际检查：

- 用户任务文件。
- `AGENTS.md`、workflow、task template、handoff template。
- L0 / L1 / runtime / threat-model / dataset 相关文档。
- `src/warden/runtime/pipeline.py`、`src/warden/l1/rule_baseline.py`、相关 tests 和 benchmark script。
- Focused grep residuals。

反审结论：

- 不能把 invalid capture 写成 benign / malicious / suspicious。
- 不能把 Rule Router 写成 classifier。
- 不能在本任务实现 recrawl / exclude / QA 队列。
- 不能冻结最终 L1 output schema。
- official runtime result / trace schema 版本保持不变。

### 7. 验证

已执行并通过：

- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `pytest tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_pipeline_skeleton.py tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q` -> `21 passed`
- `python -m py_compile src/warden/runtime/pipeline.py src/warden/l1/rule_baseline.py scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- Focused grep over `AGENTS.md PROJECT.md docs src tests`

### 8. 残余命中分类

- Active aligned hits: `AGENTS.md`、`PROJECT.md`、`docs/frozen/Warden_Threat_Definition_V1.md`、dataset spec、runtime dataflow spec、L0 design、L1 framework、L1 contract 中新增的 invalid capture / Rule Router 边界说明。
- Expected test/code hits: `route_to_l1_default`、negative assertions for `need_recrawl` / `route_to_recrawl`。
- Historical / previous-task hits: old handoffs, old tasks, superseded ADR, and prior benchmark handoff text mentioning `need_recrawl`.
- Data-policy residuals: `docs/data/*` contains prior blank / auxiliary / bad-capture policy wording. These were not fully rewritten because the active task was satisfied through current threat-model, dataset spec, runtime, L0, and L1 contracts; future cleanup can target those docs separately if desired.

### 9. 风险 / 注意事项

- 当前工作树在任务开始前已有大量 dirty / untracked 变更，本次没有回退。
- `docs/l1/`、benchmark script、benchmark test 是未跟踪目录/文件的一部分，但它们是当前 L1 draft routing surface，已按任务要求做增量对齐。
- `docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md` 仍有历史 `need_recrawl` 命中，未在本任务改写历史 ADR。
- 没有运行 full test suite。

### 10. 推荐下一步

单独开一个文档清理任务，处理 `docs/data/*` 和历史 ADR / handoff 中的旧 `blank`、`need_recrawl`、auxiliary wording 残余；不要并入本任务。

### 11. 停止条件

本任务达到停止条件：核心文档、runtime skeleton、L1 draft Rule Router、benchmark review layer 和窄测试已对齐；targeted validation 已通过；未处理残余已分类。

## English Version

## 1. Executive Summary

This delivery realigned Warden's invalid-capture, L0 -> L1 routing, L1 vision, and Rule Router boundaries according to the revised user task. Invalid captures are defined as dataset-building removals and must not enter the benign / malicious / suspicious threat-label system. In the runtime skeleton, valid non-terminal samples now route to L1 by default. High-confidence specialized terminal / auxiliary buckets may terminate in L0. The L1 draft Rule Router no longer emits `need_recrawl` / `route_to_recrawl`; it keeps evidence-sufficiency diagnostics and review routing.

## 2. What Changed

### Code Changes

- `src/warden/runtime/pipeline.py`: L0 routing fallback now sends valid non-terminal samples to L1; a specialized L0 terminal auxiliary branch was added.
- `src/warden/l1/rule_baseline.py`: Rule Router no longer emits `need_recrawl` / `route_to_recrawl`; insufficient-observability samples remain diagnostic and route to review.
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`: removed `need_recrawl` CSV and routing-count output.

### Doc Changes

- Updated `AGENTS.md`, `PROJECT.md`, threat definition, dataset spec, L1 framework, MODULE_DATA, L0 design, runtime dataflow spec, and L1 Decision Head contract.
- Added the repo-local task doc.
- Added this handoff.

### Output / Artifact Changes

- Task doc added under `docs/tasks/`.
- Handoff added under `docs/handoff/`.

## 3. Files Touched

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
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- Valid samples not terminated by L0 route to L1 in the runtime skeleton.
- High-confidence specialized fast-resolution adult / gambling / gate auxiliary buckets may terminate in L0 as `l0_terminal_auxiliary_bucket`.
- L1 draft Rule Router treats insufficient-observability samples as diagnostics and review routing only.

### Preserved Behavior

- Official runtime result / trace schema versions remain unchanged.
- No model training, distillation, visual-model execution, dataset mutation, manifest edit, split edit, or final L1 schema freeze was introduced.

### User-facing / CLI Impact

- No public CLI change.

### Output Format Impact

- Official runtime output schema shape/version is preserved.
- Draft/debug review-layer benchmark CSV no longer has `l1_draft_need_recrawl`.

## 5. Schema / Interface Impact

- Schema changed: no for official runtime result / trace schema versions.
- Backward compatible: partially.
- Public interface changed: no.
- Existing CLI still valid: yes.

Affected schema fields / interfaces:

- Existing `routing_outcome.outcome_kind` values now include `route_to_l1_default` and `l0_terminal_auxiliary_bucket`.
- L1 draft/debug sidecar routing hints no longer include `need_recrawl`.
- L1 draft mixed benchmark CSV no longer includes `l1_draft_need_recrawl`.

Compatibility notes:

Official runtime schema versions remain `warden_runtime_result_v0_2` / `warden_runtime_trace_v0_2`. Consumers that hard-code routing outcome values or draft benchmark CSV columns may need a small update.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- User task file in Downloads.
- Governing files and templates.
- L0 / L1 / runtime / threat-model / dataset docs.
- Runtime and L1 draft code.
- Targeted tests and benchmark script.
- Focused grep output.

Claims supported by evidence:

- Runtime L0 previously had a stop path; it now routes valid non-terminal samples to L1 by default.
- L1 draft Rule Router no longer emits `need_recrawl` / `route_to_recrawl`.
- Targeted tests pass.

Claims left unsupported or assumed:

- Full-suite compatibility was not verified.
- External downstream consumers outside the checked tests were not audited.

Retrieval stopped because:

- The checked files and targeted tests covered the active task acceptance criteria; remaining hits were classifiable as active aligned, expected tests/code, historical, or future cleanup candidates.

## 6.1 Counter-Review Performed

Original framing reviewed:

Realign invalid capture semantics, L0 terminal / L1 routing, L1 vision, and Rule Router boundaries.

Assumptions checked:

- Invalid captures must not become benign / malicious / suspicious labels.
- Rule Router must not become a classifier.
- Recrawl / exclude / QA routing must not be implemented in this task.
- Final L1 output schema must not be frozen.
- Official runtime schema versions must remain stable.

Counter-review result:

The implemented route stays inside the task boundary. It changes runtime routing behavior and draft/debug review-layer fields, while preserving official runtime schema versions and avoiding dataset mutation or model execution.

## 6. Validation Performed

### Commands Run

- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-13_warden_capture_gate_l0_to_l1_routing_threat_model_realign_v1.md`
- `pytest tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_pipeline_skeleton.py tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q`
- `python -m py_compile src/warden/runtime/pipeline.py src/warden/l1/rule_baseline.py scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `rg -n "need_recrawl|route_to_recrawl|recrawl / exclude / QA|invalid capture|Invalid captures|404|blank|pure-color|broken render|insufficient-observability|route_to_l1|Rule Router|final-like" AGENTS.md PROJECT.md docs src tests`

### Result

- Task doc checker passed.
- Handoff doc checker passed.
- Targeted pytest passed: `21 passed`.
- Py compile passed.
- Focused grep residuals were classified.

### Not Run

- Full test suite.
- Model training, teacher distillation, external model calls, OCR, YOLO, CLIP, MobileCLIP, SNet, SpecularNet-like.
- Dataset sample edits, manifest edits, split edits.

## 6.2 Residual Hit Classification

- Active aligned hits: updated invalid capture and Rule Router boundary text in active docs.
- Expected code/test hits: `route_to_l1_default` and negative assertions for removed recrawl routing.
- Historical hits: old handoffs, old tasks, superseded ADR, and previous benchmark handoff text that still mention `need_recrawl`.
- Data-policy residuals: `docs/data/*` still contains prior blank / auxiliary / bad-capture wording. Those were not fully rewritten because this task reached its acceptance criteria through current threat-model, dataset spec, runtime, L0, and L1 contracts.

## 7. Risks / Caveats

- The worktree had substantial dirty / untracked changes before this task; they were not reverted.
- `docs/l1/`, the benchmark script, and the benchmark test are part of an untracked current L1 draft surface; this task updated them because they directly referenced removed routing semantics.
- Historical ADR / handoff residuals remain.
- Full-suite compatibility is unverified.

## 8. Docs Impact

- Docs updated: yes.
- Code updated: yes.
- Task doc added: yes.
- Handoff added: yes.
- Remaining doc cleanup needed: historical ADR / handoff residuals and `docs/data/*` wording can be handled in a separate cleanup task.

## 9. Recommended Next Step

Open a separate documentation cleanup task for `docs/data/*` and historical ADR / handoff residual wording around `blank`, `need_recrawl`, and auxiliary capture states.

## 10. Stop Condition

Stop condition reached. Core docs, runtime skeleton, L1 draft Rule Router, benchmark review layer, and narrow tests are aligned; targeted validation passed; remaining residuals are classified.
