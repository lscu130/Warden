# Warden Runtime/Dataflow Skeleton V0.1 Handoff

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

## 1. 执行摘要

本次交付新增了一个 additive runtime/dataflow skeleton：独立的 `src/warden/runtime/` 子包、一个薄 CLI、shared cheap evidence 预处理、heavy artifact lazy load、`L0 / L1 / L2` stage wrapper、以及最小 result/trace 写回。

现有 frozen artifact 名称和现有 auto-label 对外入口未改。当前 skeleton 主要是 runtime 壳层，不是最终 threat judgment 实现。

## 2. 实际变更

### 代码变更

- 新增 `src/warden/runtime/__init__.py`
- 新增 `src/warden/runtime/core.py`
- 新增 `src/warden/runtime/pipeline.py`
- 新增 `scripts/infer/run_runtime_dataflow_skeleton.py`

### 文档变更

- none beyond handoff/task status

### 输出 / 产物变更

- CLI 现在可向输出目录写 `runtime_result.json` 和 `runtime_trace.json`
- 新增本 handoff 文档

## 3. 触碰文件

- `src/warden/runtime/__init__.py`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `scripts/infer/run_runtime_dataflow_skeleton.py`
- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`

## 4. 行为影响

### 新增行为

- sample folder 现在可以先构造成 immutable `ArtifactPackage`
- 每个 sample 现在可以用 shared `SampleContext` 复用一次性 cheap evidence
- `html_rendered`、`html_raw`、viewport screenshot 现在有显式 lazy-load hook
- runtime shell 现在能按 `L0 -> L1 -> L2` 路由并写出最小 result/trace

### 保持不变

- 官方顶层阶段仍是 `L0 / L1 / L2`
- 没有修改任何 frozen dataset artifact 名称
- 没有改现有 auto-label CLI 或 schema
- `L1` / `L2` 仍是 placeholder shell，不宣称最终业务判断能力

### 用户侧 / CLI 影响

- 新增本地脚本 `scripts/infer/run_runtime_dataflow_skeleton.py`

### 输出格式影响

- 新增 skeleton 专用输出 `runtime_result.json` / `runtime_trace.json`
- 现有输出不受影响

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

兼容性说明：

本次只新增 additive runtime-only 结构和新脚本，不改现有 public artifact schema，也不替换现有入口。

## 6. 实际验证

### 已运行

- `py_compile` 语法检查
- 用 `tmp/four_family_scope_smoke/input_samples` 跑 targeted smoke
- spot-check 输出目录中生成的 `runtime_result.json` / `runtime_trace.json`

### 未运行

- repo-wide test suite
- benchmark
- 真实生产入口联调

原因：

本任务只新增 skeleton 壳层，仓库内没有更成熟的 inference test harness 可直接复用到该新入口。

## 7. 风险 / Caveats

- `L1` / `L2` 目前仍是 placeholder shell，后续还需要逐步接入真实主判断逻辑
- `L0` 复用当前 legacy-compatible 逻辑时，仍依赖一次 import alias 兼容桥

## 8. 文档影响

- Docs updated: NO

Docs touched:

- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`

Doc debt:

- 如果这个 skeleton 后续继续演进，建议补一份更细的 runtime output contract 文档

## 9. 下一步建议

- 在不改 `L0 / L1 / L2` 顶层合同的前提下，把 `L1` 主判断输入束和 `L2` 高成本 review 接口继续细化

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-22-runtime-dataflow-skeleton-v0-1
- Related Task ID: TASK-RUNTIME-001
- Task Title: Implement Warden Runtime/Dataflow Skeleton V0.1
- Module: Inference / Runtime
- Author: Codex
- Date: 2026-04-22
- Status: DONE

---

## 1. Executive Summary

This delivery added an additive runtime/dataflow skeleton under `src/warden/runtime/` plus a thin CLI under `scripts/infer/`.
The skeleton introduces immutable artifact handles, a shared per-sample runtime context, prepare-once cheap evidence, lazy heavy-artifact access, explicit `L0 / L1 / L2` stage wrappers, and minimal result/trace writeback.

No frozen dataset artifact names, existing auto-label interfaces, or official top-level stage names were changed.
`L1` and `L2` remain placeholder runtime shells rather than final threat-logic implementations.

---

## 2. What Changed

### Code Changes

- added `src/warden/runtime/__init__.py`
- added `src/warden/runtime/core.py`
- added `src/warden/runtime/pipeline.py`
- added `scripts/infer/run_runtime_dataflow_skeleton.py`

### Doc Changes

- none beyond handoff/task status updates

### Output / Artifact Changes

- the new CLI writes per-sample `runtime_result.json` and `runtime_trace.json`
- added this handoff document

---

## 3. Files Touched

- `src/warden/runtime/__init__.py`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `scripts/infer/run_runtime_dataflow_skeleton.py`
- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`

Optional notes per file:

- `core.py`: defines immutable artifact handles, shared runtime context, and trace dataclasses
- `pipeline.py`: implements cheap-evidence preparation, lazy heavy loading, stage wrappers, and result/trace writeback
- `run_runtime_dataflow_skeleton.py`: thin local CLI for smoke execution

---

## 4. Behavior Impact

### Expected New Behavior

- a sample directory can now be wrapped as an immutable `ArtifactPackage`
- a per-sample `SampleContext` now allows cheap evidence to be prepared once and reused across stages
- `html_rendered`, `html_raw`, and viewport screenshot access now exist as explicit lazy-load hooks
- the runtime shell can now route through explicit `L0 -> L1 -> L2` wrappers and emit minimal result/trace outputs

### Preserved Behavior

- official top-level stage naming remains `L0 / L1 / L2`
- no frozen dataset artifact names were changed
- no existing auto-label CLI or schema was replaced
- `L1` / `L2` still behave as placeholder runtime shells and do not claim final business-logic completeness

### User-facing / CLI Impact

- added a new local CLI: `scripts/infer/run_runtime_dataflow_skeleton.py`

### Output Format Impact

- added skeleton-specific `runtime_result.json` and `runtime_trace.json` outputs
- existing outputs remain unchanged

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- additive runtime-only structures `ArtifactPackage`, `SampleContext`, and per-stage trace/result payloads

Compatibility notes:

This delivery only adds runtime-only structures and a new local CLI.
It does not change existing public artifact schemas or replace existing entrypoints.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile src/warden/runtime/__init__.py src/warden/runtime/core.py src/warden/runtime/pipeline.py scripts/infer/run_runtime_dataflow_skeleton.py
python scripts/infer/run_runtime_dataflow_skeleton.py --input E:\Warden\tmp\four_family_scope_smoke\input_samples --output-dir E:\Warden\tmp\runtime_dataflow_skeleton_smoke --limit 3
```

### Result

- the new runtime package and CLI compile successfully
- the skeleton processes smoke sample directories and writes `runtime_result.json` plus `runtime_trace.json`
- output spot-check confirms stage-trace content and heavy-cache-release bookkeeping are present

### Not Run

- repo-wide test suite
- benchmark
- production-entrypoint integration

Reason:

This task adds a new runtime skeleton shell.
The repository does not currently expose a more mature inference harness wired to this new entrypoint.

---

## 7. Risks / Caveats

- `L1` / `L2` remain placeholder shells and still need real main-judgment and high-cost review logic later
- the current `L0` reuse still depends on a legacy-compatible import alias bridge for `Warden_auto_label_utils_brandlex`

---

## 8. Docs Impact

- Docs updated: NO

Docs touched:

- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`

Doc debt still remaining:

- a later task should freeze a more concrete runtime output contract if this skeleton becomes the active inference shell

---

## 9. Recommended Next Step

- refine the `L1` main-judgment input bundle and the `L2` higher-cost review interface without changing the top-level `L0 / L1 / L2` contract
