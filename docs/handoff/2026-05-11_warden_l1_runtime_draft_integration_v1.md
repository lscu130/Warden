# Warden L1 Runtime Draft Integration V1 Handoff

## 中文版

> 面向人类阅读的摘要版。英文版为权威执行记录；若精确命令、验证结果、兼容性结论或未运行项有冲突，以英文版为准。

# Handoff Metadata

- Handoff ID: `HANDOFF-20260511-WARDEN-L1-RUNTIME-DRAFT-INTEGRATION-V1`
- Related Task ID: `TASK-20260511-WARDEN-L1-RUNTIME-DRAFT-INTEGRATION-V1`
- Task Title: `Warden L1 Runtime Draft Integration V1`
- Module: `Runtime / L1`
- Author: `Codex`
- Date: `2026-05-11`
- Status: `DONE`

## 1. Executive Summary

本次交付把 isolated `warden.l1` skeleton 接到 runtime 末尾，并由 `WARDEN_ENABLE_L1_DRAFT=1` 显式控制。flag 默认关闭；关闭时 runtime result/trace 不新增 L1 draft 字段。flag 开启时，runtime 额外写入 `debug_sidecars.l1_draft`，字段明确标记 `draft: true` 与 `not_final_schema: true`，不改变正式 routing、final stage、terminal routing 或 stage sequence。

任务达到停止条件：focused pytest、py_compile、真实 benign runtime smoke、task doc checker 和 handoff doc checker 均已通过。

## 2. What Changed

### Code Changes

- 新增 `src/warden/runtime/l1_draft_bridge.py`，提供 feature flag、bridge 执行、异常捕获和 draft trace shape。
- 更新 `src/warden/runtime/pipeline.py`，在正式 L0/L1/L2 runtime path 结束后按 flag 附加 L1 draft sidecar。
- 新增 `tests/infer/test_l1_runtime_draft_integration.py`，覆盖 flag、异常、sidecar、正式结果不覆盖和 metadata 隔离。

### Doc Changes

- 新增 `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`。
- 新增 `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`。

### Output / Artifact Changes

- flag 关闭：无新增 output field。
- flag 开启：`runtime_result.json` 和 `runtime_trace.json` 可包含 additive `debug_sidecars.l1_draft`。
- smoke 产物写入 `E:\Warden\tmp\l1_draft_runtime_smoke_off` 与 `E:\Warden\tmp\l1_draft_runtime_smoke_on`。

## 3. Files Touched

- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- `WARDEN_ENABLE_L1_DRAFT=1` 时，runtime 会额外调用 L1 draft runner，并把结果写入 `debug_sidecars.l1_draft`。
- L1 draft trace 包含 `stage`、`enabled`、`draft`、`not_final_schema`、`status`、`result`、`error` 和 `duration_ms`。
- L1 bridge 异常会记录为 `status: error`，不会中断主 runtime。

### Preserved Behavior

- `WARDEN_ENABLE_L1_DRAFT` 未设置或为 `0` 时，不写 `debug_sidecars`。
- 正式 `final_stage`、`terminal_routing`、`routing_outcome`、`stage_sequence` 与 feature flag 无关。
- L1 draft result 不作为最终判断、训练标签或 benchmark metric。

### User-facing / CLI Impact

- 现有 runtime smoke CLI 未新增必填参数，默认行为保持不变。
- 用户可通过环境变量 `WARDEN_ENABLE_L1_DRAFT=1` 启用 draft sidecar。

### Output Format Impact

- Schema changed: additive debug sidecar only when feature flag is enabled.
- Added optional path: `debug_sidecars.l1_draft`.

## 5. Schema / Interface Impact

- Schema changed: `YES, additive and feature-flagged only`
- Backward compatible: `YES`
- Public interface changed: `YES, optional environment flag`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `WARDEN_ENABLE_L1_DRAFT`
- Optional `runtime_result.json.debug_sidecars.l1_draft`
- Optional `runtime_trace.json.debug_sidecars.l1_draft`

Compatibility notes:

Flag-off output does not include the new sidecar. Flag-on output is explicitly draft/debug and not frozen schema.

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile src/warden/runtime/l1_draft_bridge.py src/warden/runtime/pipeline.py src/warden/l1/l1_runner.py
pytest tests/infer/test_l1_runtime_draft_integration.py -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md

$env:WARDEN_ENABLE_L1_DRAFT='0'
python scripts/infer/run_runtime_dataflow_skeleton.py --input 'E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0018\11toon146.com_20260428T081511Z' --output-dir 'E:\Warden\tmp\l1_draft_runtime_smoke_off' --limit 1

$env:WARDEN_ENABLE_L1_DRAFT='1'
python scripts/infer/run_runtime_dataflow_skeleton.py --input 'E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0018\11toon146.com_20260428T081511Z' --output-dir 'E:\Warden\tmp\l1_draft_runtime_smoke_on' --limit 1
```

### Result

- `py_compile`: passed.
- Targeted pytest: `6 passed in 0.13s`.
- Task doc checker: passed.
- Handoff doc checker: passed.
- Runtime smoke flag off: processed `1`, no `debug_sidecars` in result or trace.
- Runtime smoke flag on: processed `1`, `debug_sidecars.l1_draft.status = ok`, `draft = true`, `not_final_schema = true`.
- Flag-on L1 draft smoke output contained evidence ledger, reason codes, and explanation.
- Flag-on and flag-off official runtime fields matched for the smoke sample: `final_stage = L1`, `terminal_routing = STOP`, `stage_sequence = L0,L1`.

### Not Run

- Training was not run.
- Teacher distillation was not run.
- OCR was not run.
- YOLO was not run.
- CLIP / MobileCLIP was not run.
- SNet / SpecularNet-like inference was not run.
- Full dataset runtime benchmark was not run.
- Frozen schema promotion was not run.

## 7. Risks / Caveats

- The current L1 output remains draft-only and must not be consumed as a frozen schema.
- The integration passes sample directory into the existing L1 evidence pack, so L1 may read available HTML artifacts as part of draft L1 behavior; this is allowed for L1 and does not change L0.
- The repository had a large dirty worktree before this task started. This handoff only claims the files listed above.

## 8. Docs Impact

- Docs updated: `YES`
- Task doc added.
- Handoff doc added.
- No frozen schema doc was updated because the sidecar is draft/debug only.

## 9. Recommended Next Step

- If this draft sidecar will become durable, open a separate schema-freeze task for L1 runtime output.
- If performance matters, run a focused runtime benchmark with `WARDEN_ENABLE_L1_DRAFT=1` over a bounded mixed sample set.

## English Version

> AI note: The English section is authoritative for exact validation, compatibility, and follow-up boundaries.

# Handoff Metadata

- Handoff ID: `HANDOFF-20260511-WARDEN-L1-RUNTIME-DRAFT-INTEGRATION-V1`
- Related Task ID: `TASK-20260511-WARDEN-L1-RUNTIME-DRAFT-INTEGRATION-V1`
- Task Title: `Warden L1 Runtime Draft Integration V1`
- Module: `Runtime / L1`
- Author: `Codex`
- Date: `2026-05-11`
- Status: `DONE`

## 1. Executive Summary

This delivery wires the isolated `warden.l1` skeleton into the end of the runtime path behind the explicit `WARDEN_ENABLE_L1_DRAFT=1` feature flag. The flag defaults to disabled. When disabled, runtime result/trace output does not add L1 draft fields. When enabled, runtime writes `debug_sidecars.l1_draft`, clearly marked with `draft: true` and `not_final_schema: true`, without changing official routing, final stage, terminal routing, or stage sequence.

The task reached its stop condition: focused pytest, py_compile, real benign runtime smoke, the task doc checker, and the handoff doc checker passed.

## 2. What Changed

### Code Changes

- Added `src/warden/runtime/l1_draft_bridge.py` with feature flag handling, bridge execution, exception capture, and draft trace shape.
- Updated `src/warden/runtime/pipeline.py` to attach an L1 draft sidecar after the official L0/L1/L2 runtime path when the flag is enabled.
- Added `tests/infer/test_l1_runtime_draft_integration.py` covering flags, exceptions, sidecar output, official-result preservation, and metadata isolation.

### Doc Changes

- Added `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`.
- Added `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`.

### Output / Artifact Changes

- Flag disabled: no new output field.
- Flag enabled: `runtime_result.json` and `runtime_trace.json` may include additive `debug_sidecars.l1_draft`.
- Smoke artifacts were written under `E:\Warden\tmp\l1_draft_runtime_smoke_off` and `E:\Warden\tmp\l1_draft_runtime_smoke_on`.

## 3. Files Touched

- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- With `WARDEN_ENABLE_L1_DRAFT=1`, runtime additionally calls the L1 draft runner and writes `debug_sidecars.l1_draft`.
- The L1 draft trace includes `stage`, `enabled`, `draft`, `not_final_schema`, `status`, `result`, `error`, and `duration_ms`.
- L1 bridge exceptions are recorded as `status: error` and do not interrupt the main runtime.

### Preserved Behavior

- When `WARDEN_ENABLE_L1_DRAFT` is unset or `0`, `debug_sidecars` is not written.
- Official `final_stage`, `terminal_routing`, `routing_outcome`, and `stage_sequence` are independent of the feature flag.
- L1 draft result is not used as a final judgment, training label, or benchmark metric.

### User-facing / CLI Impact

- The existing runtime smoke CLI has no new required parameter and keeps its default behavior.
- Users may enable the draft sidecar with environment variable `WARDEN_ENABLE_L1_DRAFT=1`.

### Output Format Impact

- Schema changed: additive debug sidecar only when the feature flag is enabled.
- Added optional path: `debug_sidecars.l1_draft`.

## 5. Schema / Interface Impact

- Schema changed: `YES, additive and feature-flagged only`
- Backward compatible: `YES`
- Public interface changed: `YES, optional environment flag`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `WARDEN_ENABLE_L1_DRAFT`
- Optional `runtime_result.json.debug_sidecars.l1_draft`
- Optional `runtime_trace.json.debug_sidecars.l1_draft`

Compatibility notes:

Flag-off output does not include the new sidecar. Flag-on output is explicitly draft/debug and not frozen schema.

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile src/warden/runtime/l1_draft_bridge.py src/warden/runtime/pipeline.py src/warden/l1/l1_runner.py
pytest tests/infer/test_l1_runtime_draft_integration.py -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md

$env:WARDEN_ENABLE_L1_DRAFT='0'
python scripts/infer/run_runtime_dataflow_skeleton.py --input 'E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0018\11toon146.com_20260428T081511Z' --output-dir 'E:\Warden\tmp\l1_draft_runtime_smoke_off' --limit 1

$env:WARDEN_ENABLE_L1_DRAFT='1'
python scripts/infer/run_runtime_dataflow_skeleton.py --input 'E:\WardenData\raw\benign\tranco\2026-04-28_planA_day18_tranco_top_100001_500000_batch_0018\11toon146.com_20260428T081511Z' --output-dir 'E:\Warden\tmp\l1_draft_runtime_smoke_on' --limit 1
```

### Result

- `py_compile`: passed.
- Targeted pytest: `6 passed in 0.13s`.
- Task doc checker: passed.
- Handoff doc checker: passed.
- Runtime smoke flag off: processed `1`, no `debug_sidecars` in result or trace.
- Runtime smoke flag on: processed `1`, `debug_sidecars.l1_draft.status = ok`, `draft = true`, `not_final_schema = true`.
- Flag-on L1 draft smoke output contained evidence ledger, reason codes, and explanation.
- Flag-on and flag-off official runtime fields matched for the smoke sample: `final_stage = L1`, `terminal_routing = STOP`, `stage_sequence = L0,L1`.

### Not Run

- Training was not run.
- Teacher distillation was not run.
- OCR was not run.
- YOLO was not run.
- CLIP / MobileCLIP was not run.
- SNet / SpecularNet-like inference was not run.
- Full dataset runtime benchmark was not run.
- Frozen schema promotion was not run.

## 7. Risks / Caveats

- The current L1 output remains draft-only and must not be consumed as a frozen schema.
- The integration passes sample directory into the existing L1 evidence pack, so L1 may read available HTML artifacts as part of draft L1 behavior; this is allowed for L1 and does not change L0.
- The repository had a large dirty worktree before this task started. This handoff only claims the files listed above.

## 8. Docs Impact

- Docs updated: `YES`
- Task doc added.
- Handoff doc added.
- No frozen schema doc was updated because the sidecar is draft/debug only.

## 9. Recommended Next Step

- If this draft sidecar will become durable, open a separate schema-freeze task for L1 runtime output.
- If performance matters, run a focused runtime benchmark with `WARDEN_ENABLE_L1_DRAFT=1` over a bounded mixed sample set.
