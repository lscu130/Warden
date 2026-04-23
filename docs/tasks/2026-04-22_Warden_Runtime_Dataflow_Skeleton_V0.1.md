# Warden Runtime/Dataflow Skeleton V0.1 Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 中文摘要

本任务用于在 **保持 Warden 当前结构为 L0 / L1 / L2** 的前提下，先实现一版可运行的 **runtime/dataflow skeleton**。

本任务的目标不是冻结最终 threat logic，也不是一次性定稿 L0/L1/L2 的细节，而是先把以下运行时基础设施搭起来：

- 从样本目录构造静态 `ArtifactPackage`
- 为单样本建立共享 `SampleContext`
- 一次性解析便宜证据
- 对重资源实施惰性加载
- 为 L0、L1、L2 提供统一 stage routing 外壳
- 回写阶段输出、trace 与最小结果
- 在样本处理结束后释放重缓存

当前阶段明确要求：

- **结构仍然按 L0 / L1 / L2 组织**
- 不在本任务中冻结 L0/L1/L2 的最终判定算法
- 不在本任务中引入大重构或新依赖
- 不修改冻结字段、冻结文件名、冻结枚举
- 以最小侵入方式为后续 inference 演进提供稳定 runtime 壳子

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-RUNTIME-001
- Task Title: Implement Warden Runtime/Dataflow Skeleton V0.1
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Inference / Runtime
- Related Issue / ADR / Doc: AGENTS.md; PROJECT.md; GPT_CODEX_WORKFLOW.md; TASK_TEMPLATE.md; HANDOFF_TEMPLATE.md; TRAINSET_V1-related runtime assumptions; current L0/L1/L2 mainline
- Created At: 2026-04-22
- Requested By: User / project owner

Use this template for this non-trivial engineering task in Warden.

---

## 1. Background

Warden is a staged webpage social-engineering threat judgment system with an active mainline organized around **L0 / L1 / L2**.

At the current stage, the project has already frozen the high-level system identity, the L0/L1/L2 responsibility framing, the documentation-first workflow, and the importance of lightweight deployable inference. However, the runtime/dataflow layer has not yet been stabilized as an explicit engineering skeleton.

Right now, there is a meaningful risk that later inference work could drift into a pattern where each stage reads sample files independently, reparses the same artifacts repeatedly, and silently mixes business logic with runtime orchestration logic. This task is needed now to create a stable runtime shell that later L0/L1/L2 implementations can plug into without repeatedly redesigning sample loading, shared context handling, lazy loading, cache release, and stage-result writeback.

This task exists to implement the **runtime/dataflow skeleton only**, while keeping the current system structure explicitly aligned with **L0 / L1 / L2**, not replacing that structure with a new top-level stage naming scheme.

---

## 2. Goal

Implement a minimal but execution-ready Warden runtime/dataflow skeleton that supports static sample artifact access, shared per-sample runtime state, one-time preparation of cheap evidence, lazy loading of heavy resources, top-level routing across **L0**, **L1**, and **L2**, stage result writeback, and cache release after processing. The outcome must provide a stable runtime shell for future inference evolution while preserving backward compatibility, avoiding frozen-contract violations, and keeping final L0/L1/L2 decision logic explicitly out of scope for this task.

---

## 3. Scope In

This task is allowed to touch:

- inference entrypoints and runtime orchestration code
- sample loading / artifact access utilities
- evidence preparation utilities
- runtime context management code
- stage routing skeleton code
- minimal runtime/dataflow documentation created for this task

This task is allowed to change:

- internal runtime control flow for sample loading and shared context management
- addition of new runtime/dataflow helper modules or files
- placeholder stage wrappers for `L0`, `L1`, and `L2`
- minimal result/trace writing for runtime execution
- minimal smoke-test scaffolding for the runtime skeleton

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the L0/L1/L2 system into a different top-level stage structure
- do not finalize threat-judgment logic inside L0, L1, or L2
- do not change frozen schema fields, frozen filenames, or frozen enumerations
- do not redesign training logic, labeling logic, or dataset contracts
- do not implement the final vision tower, OCR path, or final multimodal fusion policy
- do not add third-party dependencies
- do not silently refactor unrelated modules

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- AGENTS.md
- PROJECT.md
- docs/workflow/GPT_CODEX_WORKFLOW.md
- docs/templates/TASK_TEMPLATE.md
- docs/templates/HANDOFF_TEMPLATE.md
- relevant inference/data docs already governing current runtime assumptions

### Code / Scripts

- current inference entrypoint(s)
- current sample-loading code if any
- current artifact-reading utilities if any
- current runtime/export/benchmark entrypoints if any

### Data / Artifacts

- current Warden sample directory layout
- a real example sample folder for smoke testing
- currently expected inference-time artifact files such as URL/text/forms/net/html/screenshot assets

### Prior Handoff

- none required if no prior runtime/dataflow handoff exists; otherwise include the latest relevant runtime/inference handoff

### Missing Inputs

- exact repo paths for the current inference entrypoint(s) if not obvious from the repository
- exact preferred location for new runtime/dataflow modules if not obvious from current repository structure

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- runtime/dataflow skeleton code implementing shared sample-context handling
- an `ArtifactPackage` / `SampleContext` based execution shell or equivalent internal structure
- one-time cheap-evidence preparation logic
- lazy-loading hooks for heavy artifacts
- top-level `L0` / `L1` / `L2` stage wrapper skeletons or equivalent routing hooks
- minimal result / trace writeout path
- a smoke-test path or CLI example proving the skeleton runs on at least one sample folder
- a repo handoff document for this non-trivial change

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

- Preserve the project-level **L0 / L1 / L2** top-level structure.
- Do not silently introduce a replacement top-level stage taxonomy such as `fast_stage / text_stage / mm_stage` as the new official system structure.
- If internal helper sub-stages are needed inside the code, keep them implementation-local and do not redefine the project-level architecture in this task.
- Cheap evidence must be prepared once per sample whenever practical.
- Heavy artifacts must not be loaded eagerly by default.
- Runtime/dataflow logic must remain separable from final stage-specific threat logic.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen dataset artifact names
- existing top-level sample artifact contract relied on by current tooling
- existing inference/public entrypoints unless an explicit compatibility plan is documented

Schema / field constraints:

- Schema changed allowed: NO for frozen public dataset fields; YES for new internal runtime-only structures if they are backward compatible and documented
- If yes, required compatibility plan: new runtime-only structures must be internal, additive, and must not break existing external artifact expectations
- Frozen field names involved: any existing documented dataset / manifest / metadata / label fields already treated as frozen by current project contracts

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current primary inference entrypoint if one exists
  - current smoke/benchmark entrypoint if one exists and is in active use
  - current sample-directory based invocation pattern if one exists

Downstream consumers to watch:

- inference wrappers
- benchmark/export utilities
- any future L0/L1/L2 implementations that will rely on the runtime shell

---

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs and current inference/runtime-related files.
2. Identify current stable contracts that must remain unchanged.
3. Identify the most natural location for runtime/dataflow code with minimal repo disturbance.
4. Implement additive `ArtifactPackage` and `SampleContext` concepts or their equivalent.
5. Implement one-time cheap-evidence preparation.
6. Implement lazy-loading hooks for heavy artifacts.
7. Implement top-level routing skeleton for `L0`, `L1`, and `L2`.
8. Implement minimal result/trace writeback and heavy-cache release.
9. Run the smallest meaningful smoke validation on a real sample folder.
10. Summarize compatibility impact and produce handoff.

Task-specific execution notes:

- Preserve the project-level L0/L1/L2 naming in runtime control flow visible to users/docs.
- Treat stage internals as placeholders if final logic is not yet frozen.
- Keep runtime/dataflow code explicitly infrastructure-oriented rather than threat-logic-oriented.

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

- [ ] A shared per-sample runtime context exists or is clearly implemented via an equivalent documented structure
- [ ] Cheap evidence is prepared once and reused across stages whenever practical
- [ ] Heavy artifacts are lazy-loadable rather than eagerly loaded by default
- [ ] There is an explicit runtime path for `L0`, `L1`, and `L2`
- [ ] The runtime skeleton does not redefine final L0/L1/L2 business logic
- [ ] At least one smoke-test path proves that a real sample folder can enter the skeleton and produce a minimal result/trace

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
# Replace with actual repo-local commands once paths are confirmed.
python <inference_entry_or_smoke_test> --sample <sample_dir>
python -m py_compile <touched_python_files>
```

Expected evidence to capture:

- successful creation of runtime/sample context for one real sample folder
- evidence that stage routing through top-level L0/L1/L2 skeleton completes without obvious breakage
- evidence that result / trace output is written and heavy-cache cleanup path is reachable

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- runtime/dataflow behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- exact repo path for the active inference entrypoint if not obvious
- exact preferred path for new runtime/dataflow code if repo organization leaves multiple reasonable choices
- whether current repo already has partial runtime/context abstractions that should be extended instead of introducing new ones

If none, write `none`.
