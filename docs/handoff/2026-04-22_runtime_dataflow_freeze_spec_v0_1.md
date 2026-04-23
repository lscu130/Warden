# Warden Runtime/Dataflow Freeze Spec V0.1 Handoff

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

## 1. 执行摘要

本次交付完成了 runtime/dataflow 的最小冻结规格文档，明确了 `ArtifactPackage`、`SampleContext`、cheap/heavy artifact 生命周期，以及 `L0 / L1 / L2` 的最小 runtime 输入输出边界。

这是文档级合同冻结，不包含最终 threat logic 冻结。

## 2. 实际变更

### 代码变更

- none

### 文档变更

- 新增 `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`

### 输出 / 产物变更

- 新增本 handoff 文档

## 3. 触碰文件

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`

## 4. 行为影响

### 新增约束

- runtime shell 现在明确区分 immutable `ArtifactPackage` 和 mutable `SampleContext`
- cheap evidence 现在被明确规定为每个 sample 只准备一次
- heavy artifacts 现在被明确规定为默认 lazy load
- `L0 / L1 / L2` 最小 runtime I/O 和 trace 要求现在有独立冻结文档

### 保持不变

- 官方顶层阶段命名仍是 `L0 / L1 / L2`
- 没有修改任何现有 schema、字段名、CLI 或样本工件名
- 没有冻结最终 threat logic 或阈值

### 用户侧 / CLI 影响

- none

### 输出格式影响

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

兼容性说明：

本次只新增一份 runtime/dataflow 合同文档，没有修改任何现有 public schema、artifact filename 或 CLI。

## 6. 实际验证

### 已运行

- 文档内容自检，确认 `L0 / L1 / L2` 口径未漂移
- 对照 `MODULE_INFER.md`、`L0_DESIGN_V1.md`、`TRAINSET_V1.md` 做 terminology spot-check

### 未运行

- markdown lint
- repo-wide doc validation helper

原因：

仓库内没有明确的 runtime-spec 专用文档校验入口；本次采用 focused content check。

## 7. 风险 / Caveats

- 该规格只冻结最小 runtime shell，后续若要冻结 concrete inference output schema 仍需单独任务
- `L1` / `L2` 的最终业务逻辑仍未冻结

## 8. 文档影响

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`

Doc debt:

- `MODULE_INFER.md` 未来如果需要显式链接本 spec，可在后续小任务里补

## 9. 下一步建议

- 用这份 freeze spec 约束后续 runtime skeleton 和更细的 inference output contract 任务

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-22-runtime-dataflow-freeze-spec-v0-1
- Related Task ID: TASK-RUNTIME-002
- Task Title: Freeze Warden Runtime/Dataflow Spec V0.1
- Module: Inference / Runtime / Project Contracts
- Author: Codex
- Date: 2026-04-22
- Status: DONE

---

## 1. Executive Summary

This delivery added a dedicated runtime/dataflow freeze-spec document that defines the minimum Warden runtime shell contract around `ArtifactPackage`, `SampleContext`, cheap-vs-heavy artifact lifecycle discipline, and minimum `L0 / L1 / L2` runtime I/O expectations.

This is a documentation-level contract freeze.
It does not freeze final threat logic, thresholds, or the final inference output schema.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- added `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`

### Output / Artifact Changes

- added this handoff document

---

## 3. Files Touched

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`

Optional notes per file:

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`: freezes the minimum runtime/dataflow contract without redefining top-level stage naming
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`: records the scope, compatibility, and validation facts for the doc-only freeze task

---

## 4. Behavior Impact

### Expected New Behavior

- runtime readers now have a dedicated freeze-spec for the immutable `ArtifactPackage` and mutable `SampleContext` split
- cheap evidence is now explicitly frozen as a prepare-once-per-sample family
- heavy artifacts are now explicitly frozen as lazy-loaded-by-default families
- minimum `L0 / L1 / L2` runtime I/O expectations now live in a dedicated contract document

### Preserved Behavior

- official top-level stage naming remains `L0 / L1 / L2`
- no existing schema, field names, sample artifact names, or CLI entrypoints were changed
- final threat logic and thresholds remain unfrozen

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- runtime/dataflow contract wording only
- official stage naming `L0 / L1 / L2`

Compatibility notes:

This delivery only adds a new contract document.
It does not modify any existing public schema, sample artifact filename, or CLI interface.

---

## 6. Validation Performed

### Commands Run

```bash
manual content review against AGENTS.md, PROJECT.md, MODULE_INFER.md, L0_DESIGN_V1.md, and TRAINSET_V1.md
```

### Result

- the freeze-spec preserves the official `L0 / L1 / L2` top-level structure
- the document keeps runtime orchestration separate from final threat logic
- the document explicitly separates frozen items from still-configurable items

### Not Run

- markdown lint
- repo-wide doc validation helper

Reason:

There is no explicit repo-local runtime-spec validator.
Focused content checks were the smallest meaningful validation for this doc-only task.

---

## 7. Risks / Caveats

- this spec freezes only the minimum runtime shell and does not yet freeze a concrete inference output schema
- final `L1` / `L2` business logic remains outside this document by design

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`

Doc debt still remaining:

- a later small task may still add an explicit pointer from `MODULE_INFER.md` to this runtime/dataflow spec if desired

---

## 9. Recommended Next Step

- implement or extend runtime skeleton work under this frozen contract
- freeze the concrete inference output contract only in a separate explicit task
