# Warden Runtime L1/L2 Contract Refinement Handoff

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

## 1. 执行摘要

本次交付在不改变官方 `L0 / L1 / L2` 顶层合同的前提下，把 runtime skeleton 中三块原本偏薄的合同做细了：

- `L1 main-judgment input bundle`
- `L2 high-cost review contract`
- `routing outcome` 与更具体的 result/trace output contract

这次仍然没有实现最终 `L1` / `L2` 业务判断逻辑，完成的是更明确的 runtime 壳层合同和对应输出。

## 2. 实际变更

### 代码变更

- 更新 `src/warden/runtime/core.py`，让 stage trace 显式保留 `routing_outcome`、`input_contract`、`requested_heavy_artifacts`
- 更新 `src/warden/runtime/pipeline.py`，新增 `L1` input bundle 和 `L2` review contract 生成逻辑，并把它们写入 trace/result
- 把 skeleton 输出 `schema_version` 明确提升到 `warden_runtime_result_v0_2` / `warden_runtime_trace_v0_2`

### 文档变更

- 更新 `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- 新增本 task 文档和本 handoff 文档

### 输出 / 产物变更

- `runtime_result.json` 现在显式包含 terminal `routing_outcome`、`stage_sequence`、`stage_status_map`、`stage_routing_outcomes`、`result_contract`
- `runtime_trace.json` 现在显式包含 `trace_contract`、`routing_outcome_history`，以及每个 stage 的 `input_contract` / `requested_heavy_artifacts`

## 3. 触碰文件

- `docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

## 4. 行为影响

### 新增行为

- `L1` stage trace 现在有显式 `l1_main_judgment_input_bundle_v0_1`
- `L2` stage trace 现在有显式 `l2_high_cost_review_contract_v0_1`
- 每个 stage 现在都有显式 `routing_outcome`
- runtime result/trace 现在能区分 routing outcome 和 placeholder judgment output，而不是只靠 `next_stage` 隐含表达

### 保持不变

- 官方顶层阶段仍是 `L0 / L1 / L2`
- 没有改 frozen dataset artifact 名称
- 没有实现最终 `L1` main judgment 或最终 `L2` multimodal / OCR / interaction review 逻辑
- 现有 skeleton CLI 调用方式不变

### 用户侧 / CLI 影响

- CLI 参数不变
- CLI 输出内容更具体

### 输出格式影响

- `runtime_result.json` / `runtime_trace.json` 合同有 additive 扩展，并显式 bump 到 `v0_2`

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

兼容性说明：

变化仅限 runtime skeleton 自己的 result/trace 输出，属于 runtime-only additive 扩展；现有数据集 schema、artifact filename、以及 CLI 参数没有变化。

## 6. 实际验证

### 已运行

- `python -m py_compile src/warden/runtime/__init__.py src/warden/runtime/core.py src/warden/runtime/pipeline.py scripts/infer/run_runtime_dataflow_skeleton.py`
- `python scripts/infer/run_runtime_dataflow_skeleton.py --input E:\Warden\tmp\four_family_scope_smoke\input_samples --output-dir E:\Warden\tmp\runtime_dataflow_skeleton_smoke_contract_refinement --limit 3`
- 直接调用 `L0 -> L1 -> L2` wrapper，确认 `L2` contract 在 trace 中可达
- `python scripts/ci/check_task_doc.py docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`

### 结果

- 新 runtime 文件语法通过
- smoke 输出成功生成
- `runtime_result.json` 中可见 `routing_outcome` 和 `result_contract`
- `runtime_trace.json` 中可见 `trace_contract`、per-stage `input_contract` 和 `requested_heavy_artifacts`
- 直接调用三层 wrapper 时，stage trace 为 `["L0", "L1", "L2"]`

### 未运行

- repo-wide test suite
- benchmark
- 生产入口联调

原因：

本任务仍是 runtime shell 合同细化，不涉及成熟的生产入口或 benchmark 逻辑变更。

## 7. 风险 / Caveats

- `L1` / `L2` 现在是合同更清楚了，但业务逻辑仍然是 placeholder
- 当前 `L0` 复用仍依赖 legacy-compatible import alias 桥
- 如果后续继续扩展 runtime output 字段，建议尽快单独冻结正式 output contract，避免 skeleton 输出继续自由增长

## 8. 文档影响

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

Doc debt:

- `MODULE_INFER.md` 暂未同步补入更细的 result/trace 字段族；如果后续把 skeleton output 合同升级成正式 inference output 合同，再单独补更合适

## 9. 下一步建议

- 下一步可以单开窄任务，把 `L1` main-judgment shell 的内部字段族继续细化成 text-first judgment contract，并决定 `L2` 是否先承接 gate/evasion review 还是先承接 multimodal review

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-22-runtime-l1-l2-contract-refinement
- Related Task ID: TASK-RUNTIME-003
- Task Title: Refine L1 input bundle, L2 review contract, and routing outcome/output contract
- Module: Inference / Runtime
- Author: Codex
- Date: 2026-04-22
- Status: DONE

---

## 1. Executive Summary

This delivery refined three thin contract areas in the current runtime skeleton without changing the official `L0 / L1 / L2` top-level structure:

- the `L1` main-judgment input bundle
- the `L2` high-cost review contract
- explicit routing outcome fields plus a more concrete runtime result/trace output contract

This task still does not implement final `L1` / `L2` business logic.
What it completes is a clearer runtime-shell contract and clearer runtime outputs.

---

## 2. What Changed

### Code Changes

- updated `src/warden/runtime/core.py` so stage-trace entries explicitly preserve `routing_outcome`, `input_contract`, and `requested_heavy_artifacts`
- updated `src/warden/runtime/pipeline.py` to generate explicit `L1` input bundles and `L2` review contracts and write them into trace/result outputs
- bumped skeleton output schema markers to `warden_runtime_result_v0_2` and `warden_runtime_trace_v0_2`

### Doc Changes

- updated `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- added this task document and this handoff document

### Output / Artifact Changes

- `runtime_result.json` now explicitly includes terminal `routing_outcome`, `stage_sequence`, `stage_status_map`, `stage_routing_outcomes`, and `result_contract`
- `runtime_trace.json` now explicitly includes `trace_contract`, `routing_outcome_history`, and each stage's `input_contract` plus `requested_heavy_artifacts`

---

## 3. Files Touched

- `docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

Optional notes per file:

- `core.py`: expands the per-stage trace contract
- `pipeline.py`: refines the runtime shell with explicit `L1` / `L2` contract families and clearer result/trace outputs
- `Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`: now records the minimum `L1` bundle, `L2` review contract, and output field families

---

## 4. Behavior Impact

### Expected New Behavior

- the `L1` stage trace now exposes an explicit `l1_main_judgment_input_bundle_v0_1`
- the `L2` stage trace now exposes an explicit `l2_high_cost_review_contract_v0_1`
- each stage now exposes an explicit `routing_outcome`
- runtime result/trace outputs now distinguish routing outcome from placeholder judgment outputs instead of only implying routing through `next_stage`

### Preserved Behavior

- official top-level stage naming remains `L0 / L1 / L2`
- no frozen dataset artifact names were changed
- no final `L1` main-judgment logic or final `L2` multimodal / OCR / interaction review logic was implemented
- the current skeleton CLI invocation shape remains unchanged

### User-facing / CLI Impact

- CLI arguments remain unchanged
- CLI output content is now more explicit

### Output Format Impact

- `runtime_result.json` and `runtime_trace.json` received additive contract expansion and an explicit `v0_2` schema marker bump

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- runtime skeleton result output fields
- runtime skeleton trace output fields
- per-stage trace contract fields

Compatibility notes:

The change is limited to the runtime skeleton's own result/trace outputs and remains an additive runtime-only extension.
Dataset schema, sample artifact filenames, and CLI arguments were not changed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile src/warden/runtime/__init__.py src/warden/runtime/core.py src/warden/runtime/pipeline.py scripts/infer/run_runtime_dataflow_skeleton.py
python scripts/infer/run_runtime_dataflow_skeleton.py --input E:\Warden\tmp\four_family_scope_smoke\input_samples --output-dir E:\Warden\tmp\runtime_dataflow_skeleton_smoke_contract_refinement --limit 3
python -c "import sys, json; sys.path.insert(0, r'E:\\Warden'); sys.path.insert(0, r'E:\\Warden\\src'); from pathlib import Path; from warden.runtime.pipeline import build_sample_context, prepare_shared_evidence, run_l0_stage, run_l1_stage, run_l2_stage, build_result_payload; ctx = build_sample_context(Path(r'E:\\Warden\\tmp\\four_family_scope_smoke\\input_samples\\ledger_a')); prepare_shared_evidence(ctx); run_l0_stage(ctx); run_l1_stage(ctx); run_l2_stage(ctx); payload = build_result_payload(ctx); print(json.dumps({'schema_version': payload['schema_version'], 'routing_outcome_kind': payload['routing_outcome'].get('outcome_kind'), 'l2_input_contract': ctx.stage_trace[-1].input_contract.get('contract_name'), 'stages': [item.stage for item in ctx.stage_trace]}, ensure_ascii=False))"
python scripts/ci/check_task_doc.py docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md
```

### Result

- the touched runtime files compile successfully
- smoke output generation succeeds on sample folders
- `runtime_result.json` now exposes `routing_outcome` and `result_contract`
- `runtime_trace.json` now exposes `trace_contract`, per-stage `input_contract`, and `requested_heavy_artifacts`
- direct wrapper execution confirms that the `L2` contract is reachable in a `["L0", "L1", "L2"]` trace
- the task doc passes the repo checker

### Not Run

- repo-wide test suite
- benchmark
- production-entrypoint integration

Reason:

This task still refines the runtime shell contract rather than changing a mature production path or benchmark implementation.

---

## 7. Risks / Caveats

- `L1` / `L2` now have clearer contracts, but their business logic still remains placeholder-only
- the current `L0` reuse still depends on the legacy-compatible import alias bridge
- if runtime output fields continue to grow, a dedicated formal output-contract freeze task should follow soon

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

Doc debt still remaining:

- `MODULE_INFER.md` was not updated with these finer-grained result/trace field families; if the skeleton output contract is promoted toward an official inference output contract, that should be handled in a dedicated follow-up

---

## 9. Recommended Next Step

- run a narrow follow-up task to refine the internal `L1` main-judgment field families into a stronger text-first judgment contract and decide whether `L2` should first absorb gate/evasion review or multimodal review
