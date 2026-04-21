# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-10-l0-specialized-detectors-insert
- Related Task ID: TASK-2026-04-10-L0-SPECIALIZED-DETECTORS-INSERT
- Task Title: 把 specialized detector 正式双语段落补入 `L0_DESIGN_V1.md`
- Module: Inference / L0 design
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

本次交付将用户提供的 specialized detector 草稿正式并入 `L0_DESIGN_V1.md`。新增内容覆盖三块：高显著垂类专项探测器家族、high-salience vertical 的快速处理约束、以及 specialized detector 的实现约束。  
改动只发生在文档层，没有修改推理代码、schema、CLI 或路由结果枚举。

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- 更新 `L0_DESIGN_V1.md`
- 新增本 task 文档
- 新增本 handoff 文档

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

Optional notes per file:

- `L0_DESIGN_V1.md` 中新增了三组正式双语段落，未改已有路由枚举

---

## 4. Behavior Impact

### Expected New Behavior

- `L0_DESIGN_V1.md` 现在明确允许少量 high-salience specialized detector families
- 文档现在明确博彩、成人、gate/challenge/fake verification 三类 detector 的弱信号与 no-early-stop 约束
- 文档现在明确 high-salience vertical 的 fast-handling candidate 不是最终标签，也不是默认 L0 直接裁决
- 文档现在明确 specialized detector 的推荐实现边界与 shared evidence object 约束

### Preserved Behavior

- `L0` 仍是低成本前置筛查层
- `L1` 仍是主判断层
- `L2` 仍是高成本升级层
- 官方路由结果仍是 `early_stop_low_risk`、`escalate_to_L1`、`direct_to_L2`

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

- `L0_DESIGN_V1.md` contract wording only

Compatibility notes:

This change is documentation-only.
It adds specialized-detector guidance without changing route-result names, schema fields, CLI behavior, or output structure.

---

## 6. Validation Performed

### Commands Run

```bash
Get-Content -Raw "E:\Warden\L0_DESIGN_V1.md"
Get-Content -Raw "C:\Users\20516\Downloads\L0_SPECIALIZED_DETECTORS_INSERT_V1.md"
```

### Result

- confirmed the insert draft was merged into the repo-resident `L0_DESIGN_V1.md`
- confirmed the new sections were placed in the intended weak-signal, early-stop, and implementation-constraint areas
- confirmed the wording keeps specialized detectors at weak-signal / routing-hint level

### Not Run

- runtime inference test
- CLI validation
- schema-consumer validation

Reason:

This task is documentation-only and does not modify code, CLI entrypoints, or output schemas.

---

## 7. Risks / Caveats

- the newly documented detector families still need separate implementation tasks if code support is desired
- the specialized fast-resolution concept is documented only as a constrained candidate path, not as an enabled baseline behavior

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 如果要把这些 detector 落到代码里，单独开 implementation task，先冻结 shared `evidence_preparer` 与 detector outputs

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-10-l0-specialized-detectors-insert
- Related Task ID: TASK-2026-04-10-L0-SPECIALIZED-DETECTORS-INSERT
- Task Title: Insert the formal bilingual specialized-detector sections into `L0_DESIGN_V1.md`
- Module: Inference / L0 design
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

This delivery formally merged the user-provided specialized-detector draft into `L0_DESIGN_V1.md`. The added material covers three areas: high-salience specialized detector families, fast-handling constraints for high-salience verticals, and implementation constraints for specialized detectors.  
The change is documentation-only and does not modify inference code, schema, CLI, or route-result enums.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- updated `L0_DESIGN_V1.md`
- added this task doc
- added this handoff doc

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

Optional notes per file:

- `L0_DESIGN_V1.md` gained three formal bilingual section groups without changing existing route-result enums

---

## 4. Behavior Impact

### Expected New Behavior

- `L0_DESIGN_V1.md` now explicitly allows a small number of high-salience specialized detector families
- the document now explicitly defines weak signals and no-early-stop constraints for gambling, adult, and gate/challenge/fake-verification detectors
- the document now explicitly states that fast-handling candidates are not final labels and not default L0 direct adjudication
- the document now explicitly defines recommended implementation boundaries for specialized detectors and the shared-evidence-object approach

### Preserved Behavior

- `L0` remains the low-cost front screening stage
- `L1` remains the main judgment stage
- `L2` remains the high-cost escalation stage
- official route results remain `early_stop_low_risk`, `escalate_to_L1`, and `direct_to_L2`

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

- `L0_DESIGN_V1.md` contract wording only

Compatibility notes:

This change is documentation-only.
It adds specialized-detector guidance without changing route-result names, schema fields, CLI behavior, or output structure.

---

## 6. Validation Performed

### Commands Run

```bash
Get-Content -Raw "E:\Warden\L0_DESIGN_V1.md"
Get-Content -Raw "C:\Users\20516\Downloads\L0_SPECIALIZED_DETECTORS_INSERT_V1.md"
```

### Result

- confirmed the insert draft was merged into the repo-resident `L0_DESIGN_V1.md`
- confirmed the new sections were placed in the intended weak-signal, early-stop, and implementation-constraint areas
- confirmed the wording keeps specialized detectors at weak-signal / routing-hint level

### Not Run

- runtime inference test
- CLI validation
- schema-consumer validation

Reason:

This task is documentation-only and does not modify code, CLI entrypoints, or output schemas.

---

## 7. Risks / Caveats

- the newly documented detector families still need separate implementation tasks if code support is desired
- the specialized fast-resolution concept is documented only as a constrained candidate path, not as an enabled baseline behavior

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_insert.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_insert.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- if code support is desired for these detector families, open a separate implementation task and freeze the shared `evidence_preparer` and detector outputs first
