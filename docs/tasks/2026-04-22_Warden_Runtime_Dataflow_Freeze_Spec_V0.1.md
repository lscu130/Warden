# Warden Runtime/Dataflow Freeze Spec V0.1 Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 中文摘要

本任务用于为 Warden 先冻结一版 **runtime/dataflow 最小规格**，服务当前 **L0 / L1 / L2** 主线。

本任务不负责实现最终 threat logic，而是负责把以下内容先写清楚并冻结到文档层：

- `ArtifactPackage` 与 `SampleContext` 的职责边界
- 便宜证据与重资源的生命周期边界
- L0 / L1 / L2 的最小运行时输入输出 contract
- 哪些内容现在就能冻结
- 哪些内容目前只能保持为配置位或后续任务项

当前版本特别强调：

- **项目结构保持为 L0 / L1 / L2**
- runtime/dataflow 规格服务于该结构，而不是替代该结构
- 允许后续在 L1 内部继续细化实现，但本任务不把内部实现细化上升为新的项目级层次
- 当前优先冻结“运行时壳子与接口边界”，不冻结最终业务阈值与最终模型细节

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-RUNTIME-002
- Task Title: Freeze Warden Runtime/Dataflow Spec V0.1
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Inference / Runtime / Project Contracts
- Related Issue / ADR / Doc: AGENTS.md; PROJECT.md; GPT_CODEX_WORKFLOW.md; TASK_TEMPLATE.md; HANDOFF_TEMPLATE.md; current L0/L1/L2 mainline
- Created At: 2026-04-22
- Requested By: User / project owner

Use this template for this non-trivial engineering task in Warden.

---

## 1. Background

Warden already has a project-level mainline that explicitly organizes the system as **L0 / L1 / L2**. However, the runtime/dataflow layer still needs a minimum frozen specification so that future implementation work does not drift across windows, reviewers, and execution agents.

Without a frozen runtime/dataflow specification, later work risks silently redefining stage boundaries, mixing runtime orchestration with business logic, introducing inconsistent sample-context assumptions, or baking implementation-specific routing ideas into project-level architecture prematurely.

This task is needed now to freeze the minimum runtime/dataflow contract while preserving the active top-level structure as **L0 / L1 / L2** and explicitly separating what is frozen now from what remains configurable or deferred.

---

## 2. Goal

Produce a bilingual, execution-oriented runtime/dataflow specification document that freezes the minimum contract needed for future implementation around **L0 / L1 / L2**. The frozen content must define runtime object responsibilities, shared sample-context boundaries, cheap-vs-heavy artifact lifecycle rules, top-level stage input/output contracts, and the distinction between what is stable now versus what must remain configurable. The result must reduce future drift without prematurely freezing final model logic, thresholds, or multimodal policy details.

---

## 3. Scope In

This task is allowed to touch:

- runtime/dataflow specification documents
- inference/runtime module documentation directly related to runtime orchestration
- new docs created to freeze runtime/dataflow contracts

This task is allowed to change:

- documentation that defines runtime/dataflow responsibilities
- documentation that defines `ArtifactPackage`, `SampleContext`, and runtime lifecycle boundaries
- documentation that defines top-level stage I/O expectations for `L0`, `L1`, and `L2`
- documentation that explicitly marks configurable items vs frozen items

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not implement final L0/L1/L2 threat logic
- do not redesign the top-level project architecture away from L0/L1/L2
- do not modify frozen dataset fields, filenames, or enumerations
- do not change label semantics or threat taxonomy
- do not freeze final routing thresholds, final OCR policy thresholds, or final L2 escalation thresholds
- do not perform broad code refactors as part of this spec task

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- AGENTS.md
- PROJECT.md
- docs/workflow/GPT_CODEX_WORKFLOW.md
- docs/templates/TASK_TEMPLATE.md
- docs/templates/HANDOFF_TEMPLATE.md
- relevant inference/data docs that constrain runtime assumptions

### Code / Scripts

- current inference/runtime entrypoints if they exist
- any current sample-loading or routing helpers if they exist

### Data / Artifacts

- current sample artifact directory layout
- current runtime-relevant artifact names and assumptions

### Prior Handoff

- latest relevant runtime/inference handoff if one exists

### Missing Inputs

- repo path where the frozen runtime/dataflow doc should live if not obvious
- confirmation of any already-existing runtime contract doc that should be extended rather than replaced

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- one bilingual runtime/dataflow freeze-spec Markdown document
- explicit definitions for runtime/dataflow responsibilities
- explicit minimum `SampleContext` field-family freeze
- explicit minimum stage contracts for `L0`, `L1`, and `L2`
- explicit lifecycle rules for cheap evidence, heavy artifacts, and result retention
- explicit statement of what remains configurable and is **not** frozen yet
- a repo handoff document for this non-trivial documentation change

Be concrete.

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- Preserve the project-level top-level structure as **L0 / L1 / L2**.
- Do not freeze any alternative top-level stage taxonomy in a way that conflicts with the current project contract.
- Freeze only the minimum runtime/dataflow contract needed now.
- Leave thresholds, detailed model internals, and final stage-specific threat logic explicitly configurable unless already frozen elsewhere.
- Make the separation between runtime orchestration and business judgment logic explicit.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen dataset artifact names and sample-structure expectations
- existing public inference entrypoint assumptions unless a compatibility note explicitly says otherwise
- existing project-level L0/L1/L2 stage framing

Schema / field constraints:

- Schema changed allowed: YES for new internal runtime/dataflow documentation structures; NO for frozen public dataset fields
- If yes, required compatibility plan: any new runtime field families must be internal/documentation-level additions and must not redefine existing frozen dataset outputs
- Frozen field names involved: existing documented dataset / manifest / label / metadata fields that are already frozen by project contract

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current primary inference command if one exists
  - current runtime/benchmark entrypoint if one exists and is active
  - current sample-directory invocation pattern if active

Downstream consumers to watch:

- runtime implementation task(s)
- future L0/L1/L2 execution logic
- benchmark/export paths
- future review and handoff tasks that depend on stable runtime terminology

---

## 9. Suggested Execution Plan

Recommended order:

1. Read governing project and workflow docs.
2. Confirm the currently active L0/L1/L2 top-level architecture from project-level contracts.
3. Identify which runtime/dataflow concepts are already stable enough to freeze now.
4. Define runtime object responsibility boundaries.
5. Define minimum `SampleContext` field families.
6. Define top-level stage contracts for `L0`, `L1`, and `L2`.
7. Define lifecycle rules for cheap evidence, heavy artifacts, outputs, and cleanup.
8. Explicitly mark configurable items that remain unfrozen.
9. Write the bilingual freeze-spec doc.
10. Produce handoff.

Task-specific execution notes:

- Keep the document contract-first and implementation-agnostic where possible.
- Avoid overspecifying current internal stage mechanics beyond what is needed for a stable runtime contract.
- Preserve room for later implementation details inside L0/L1/L2 without redefining the top-level architecture.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] The frozen spec explicitly preserves **L0 / L1 / L2** as the top-level runtime stage structure
- [ ] Runtime/dataflow responsibilities are separated clearly from final threat-judgment logic
- [ ] Minimum field families for `SampleContext` are frozen at a useful level
- [ ] Minimum stage contracts for `L0`, `L1`, and `L2` are documented
- [ ] Lifecycle rules for cheap evidence, heavy resources, and output retention are documented
- [ ] Configurable vs frozen items are clearly separated

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] Markdown structure sanity
- [ ] consistency spot-check against AGENTS.md / PROJECT.md / workflow docs
- [ ] terminology consistency spot-check for L0/L1/L2 naming
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
# Replace with actual repo-local checks if the repo has markdown lint or doc validation helpers.
# Otherwise perform a manual consistency check and state that explicitly in handoff.
```

Expected evidence to capture:

- the freeze-spec doc exists and is internally consistent
- terminology aligns with current project-level L0/L1/L2 mainline
- frozen vs configurable boundaries are explicitly stated

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- docs touched
- contract impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- exact repo path for the runtime/dataflow spec doc if not obvious
- whether an existing module doc should host the frozen content instead of creating a new dedicated runtime spec doc
- whether current inference docs already define any runtime terminology that must be preserved verbatim

If none, write `none`.
