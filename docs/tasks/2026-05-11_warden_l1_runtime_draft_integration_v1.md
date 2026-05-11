# Warden L1 Runtime Draft Integration V1

## 中文版

> 面向人类阅读的摘要版。英文版为权威执行版本；若精确范围、字段、验收或验证要求有冲突，以英文版为准。

## 1. 背景

当前 isolated `warden.l1` skeleton 已经可以独立从样本或 manifest row 构建 evidence pack、reason codes、evidence ledger 和 deterministic explanation，但尚未接入现有 Warden runtime。本任务只把它接成 feature-flagged draft/debug sidecar，不上线 L1 正式判断。

## 2. 目标

通过显式 `WARDEN_ENABLE_L1_DRAFT=1` feature flag，把 `warden.l1.run_l1_baseline_for_sample(...)` 接到 runtime 末尾。flag 默认关闭；关闭时 runtime 输出保持原状；开启时只附加 L1 draft trace/sidecar，不改变正式 routing、decision、label、score 或 frozen schema。

## 3. 范围内

允许触碰：

- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`

允许修改：

- 新增 L1 draft bridge；
- 新增 feature flag 读取逻辑；
- 在 runtime result/trace 中按 flag 追加 draft/debug sidecar；
- 新增 focused pytest；
- 新增 task/handoff 文档。

## 4. 范围外

不得：

- 训练模型；
- 跑 teacher distillation；
- 跑 OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like inference；
- 接真实 text tower 或 fusion head；
- 修改 frozen schema 或 label enum；
- 修改样本、manifest split 或训练标签；
- 把 L1 draft result 作为最终输出、训练标签或 benchmark 指标；
- 改变现有 CLI 默认行为。

## 5. 输入

需要读取：

- `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_RUNTIME_DRAFT_INTEGRATION_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/evidence_pack.py`
- `scripts/infer/run_runtime_dataflow_skeleton.py`

缺失项：

- 无阻塞缺失项。真实 benign smoke 使用本机 `E:\WardenData\raw\benign\tranco` 中存在的样本路径。

## 6. 必需输出

- repo-local task doc；
- runtime L1 draft bridge；
- feature flag integration；
- focused pytest；
- 至少一个真实 benign sample 的 runtime smoke；
- repo-local handoff doc。

## 7. 硬约束

- flag 默认关闭；
- flag 关闭时不附加 L1 draft sidecar；
- flag 开启时只输出 draft/debug sidecar；
- bridge 异常必须被捕获并记录，不允许中断主 runtime；
- 不把 label、split、triage label 或 folder label 注入 L1 evidence input；
- 不改变正式 runtime decision/routing；
- 不引入第三方依赖。

## 8. 接口 / Schema 约束

- Schema changed: `YES, additive debug sidecar only when feature flag is enabled`
- Backward compatible: `YES`
- Existing CLI default behavior must remain valid.
- Draft output must include `draft: true` and `not_final_schema: true`.
- Draft output must not be treated as frozen schema.

## 9. 执行说明

- 优先最小补丁；
- bridge 只传 sample directory 给 L1 runner；
- runtime result/trace 只在 feature flag 开启且 bridge 执行后追加 `debug_sidecars.l1_draft`；
- pytest 覆盖 flag、异常、trace、正式结果不覆盖和 metadata 隔离。

## 10. 验收标准

- feature flag 默认关闭；
- flag 关闭时 runtime 不调用 L1 draft runner，也不写 draft sidecar；
- flag 开启时 runtime 额外写入 L1 draft trace/sidecar；
- L1 bridge 异常不会中断主 runtime；
- draft output 明确标记 draft / not final schema；
- targeted pytest 通过；
- 至少一个真实 benign sample runtime smoke 通过；
- `py_compile` 通过；
- task doc / handoff doc checker 通过；
- handoff 明确说明未运行 training、teacher、OCR、YOLO、CLIP、SNet。

## 11. 验证清单

- `python -m py_compile src/warden/runtime/l1_draft_bridge.py src/warden/runtime/pipeline.py src/warden/l1/l1_runner.py`
- `pytest tests/infer/test_l1_runtime_draft_integration.py -q`
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `WARDEN_ENABLE_L1_DRAFT=0` runtime smoke
- `WARDEN_ENABLE_L1_DRAFT=1` runtime smoke

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative execution contract.

# Task Metadata

- Task ID: `TASK-20260511-WARDEN-L1-RUNTIME-DRAFT-INTEGRATION-V1`
- Task Title: `Warden L1 Runtime Draft Integration V1`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Runtime / L1`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_RUNTIME_DRAFT_INTEGRATION_V1.md`
- Created At: `2026-05-11`
- Requested By: `User`
- Karpathy Guardrails Required: `YES`

## 1. Background

The isolated `warden.l1` skeleton can already build evidence packs, reason codes, evidence ledger entries, and deterministic explanations from sample paths or manifest rows. It is not connected to the existing Warden runtime. This task wires it into runtime as a feature-flagged draft/debug sidecar only.

## 2. Goal

Add an explicit `WARDEN_ENABLE_L1_DRAFT=1` integration path that runs `warden.l1.run_l1_baseline_for_sample(...)` after the official runtime path. The flag defaults to disabled. Disabled output must remain unchanged. Enabled output may include L1 draft/debug sidecar data, but must not alter official routing, final decision, label, score, or frozen schema.

## 3. Scope In

This task is allowed to touch:

- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`

This task is allowed to change:

- Add an L1 draft bridge.
- Add feature-flag reading logic.
- Add optional runtime result/trace draft sidecar output.
- Add focused pytest coverage.
- Add task and handoff documents.

## 4. Scope Out

This task must not:

- train models;
- run teacher distillation;
- run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference;
- connect a real text tower or fusion head;
- modify frozen schema or label enums;
- modify samples, manifest splits, or training labels;
- promote L1 draft output to final output;
- write L1 draft output into training labels or benchmark metrics;
- change existing CLI default behavior.

## 5. Inputs

Relevant inputs for this task:

- `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_RUNTIME_DRAFT_INTEGRATION_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/evidence_pack.py`
- `scripts/infer/run_runtime_dataflow_skeleton.py`

Missing inputs:

- None blocking. Real benign smoke may use an existing local sample under `E:\WardenData\raw\benign\tranco`.

## 6. Required Outputs

- Repo-local task document.
- Runtime L1 draft bridge.
- Feature flag integration.
- Focused pytest.
- At least one real benign sample runtime smoke.
- Repo-local handoff document.

## 7. Hard Constraints

- The feature flag must default to disabled.
- Disabled runtime must not attach an L1 draft sidecar.
- Enabled runtime may only attach draft/debug sidecar data.
- Bridge exceptions must be captured and recorded without failing the main runtime.
- Labels, split names, triage labels, and folder labels must not be injected into L1 evidence input.
- Official runtime decision/routing must not be changed.
- No third-party dependency may be added.

## 8. Interface / Schema Constraints

- Schema changed: `YES, additive debug sidecar only when the feature flag is enabled`.
- Backward compatible: `YES`.
- Existing CLI default behavior must remain valid.
- Draft output must include `draft: true` and `not_final_schema: true`.
- Draft output must not be treated as frozen schema.

## 9. Execution Notes

- Prefer the smallest valid patch.
- The bridge passes only the sample directory to the L1 runner.
- Runtime result/trace append `debug_sidecars.l1_draft` only when the feature flag is enabled and the bridge executes.
- Pytest covers flags, exceptions, trace output, official-result preservation, and metadata isolation.

## 10. Acceptance Criteria

- The feature flag defaults to disabled.
- Disabled runtime does not call the L1 draft runner and does not write a draft sidecar.
- Enabled runtime writes an additional L1 draft trace/sidecar.
- L1 bridge exceptions do not interrupt the main runtime.
- Draft output is clearly marked as draft / not final schema.
- Targeted pytest passes.
- At least one real benign sample runtime smoke passes.
- `py_compile` passes.
- Task and handoff doc checkers pass.
- Handoff explicitly states that training, teacher, OCR, YOLO, CLIP, and SNet were not run.

## 11. Validation Checklist

- `python -m py_compile src/warden/runtime/l1_draft_bridge.py src/warden/runtime/pipeline.py src/warden/l1/l1_runner.py`
- `pytest tests/infer/test_l1_runtime_draft_integration.py -q`
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- runtime smoke with `WARDEN_ENABLE_L1_DRAFT=0`
- runtime smoke with `WARDEN_ENABLE_L1_DRAFT=1`
