# Warden Runtime L1/L2 Contract Refinement Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 中文摘要

本任务用于在不改变官方 `L0 / L1 / L2` 顶层合同的前提下，继续细化 runtime skeleton 中与 `L1` / `L2` 直接相关的最小合同。

本任务只做以下三件事：

- 把 `L1 main-judgment input bundle` 写得更明确；
- 把 `L2 high-cost review contract` 写得更明确；
- 把 `routing outcome` 字段和更具体的 result/trace output contract 补进现有 skeleton。

本任务不负责实现最终 `L1` / `L2` threat logic，也不负责重写现有 `L0` 逻辑。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-RUNTIME-003
- Task Title: Refine L1 input bundle, L2 review contract, and routing outcome/output contract
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Inference / Runtime
- Related Issue / ADR / Doc: AGENTS.md; PROJECT.md; docs/workflow/GPT_CODEX_WORKFLOW.md; docs/templates/TASK_TEMPLATE.md; docs/templates/HANDOFF_TEMPLATE.md; docs/modules/MODULE_INFER.md; docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md; docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md
- Created At: 2026-04-22
- Requested By: User / project owner

Use this template for this non-trivial engineering task in Warden.

---

## 1. Background

The current runtime/dataflow skeleton already provides additive `ArtifactPackage`, `SampleContext`, cheap evidence preparation, lazy heavy-artifact hooks, explicit `L0 / L1 / L2` wrappers, and minimal result/trace writeback. However, the contract remains intentionally thin around three areas that are now needed for the next implementation step:

- the explicit `L1` main-judgment input bundle;
- the explicit `L2` high-cost review contract;
- clearer routing outcome fields and a more concrete runtime result/trace output contract.

This refinement is needed now so later `L1` / `L2` implementation work can plug into a more stable shell without redefining stage boundaries or overloading stage outputs ad hoc.

---

## 2. Goal

Refine the existing runtime/dataflow spec and skeleton so that `L1` receives an explicit main-judgment input bundle, `L2` receives an explicit high-cost review contract, and runtime result/trace outputs expose clearer routing outcome/status fields and more concrete contract families. The result must stay additive, preserve the official `L0 / L1 / L2` top-level structure, and avoid claiming final `L1` / `L2` threat logic is already implemented.

---

## 3. Scope In

This task is allowed to touch:

- the active runtime/dataflow freeze spec
- the current runtime skeleton package
- the thin runtime skeleton CLI if needed for output exposure
- a new task doc and a new handoff doc for this refinement

This task is allowed to change:

- runtime/dataflow documentation for `L1` input bundle and `L2` review contract
- runtime-only dataclasses and helper structures
- runtime result/trace payload fields for clearer routing outcome/status exposure
- placeholder stage-wrapper outputs where needed to expose the refined contract

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the official `L0 / L1 / L2` top-level stage structure
- do not implement final `L1` main judgment logic
- do not implement final `L2` multimodal / OCR / interaction review logic
- do not rename frozen dataset artifact names
- do not change label semantics
- do not replace or rewrite the existing `L0` business logic
- do not add third-party dependencies
- do not refactor unrelated inference modules

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- AGENTS.md
- PROJECT.md
- docs/workflow/GPT_CODEX_WORKFLOW.md
- docs/templates/TASK_TEMPLATE.md
- docs/templates/HANDOFF_TEMPLATE.md
- docs/modules/MODULE_INFER.md
- docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md
- docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md

### Code / Scripts

- src/warden/runtime/core.py
- src/warden/runtime/pipeline.py
- scripts/infer/run_runtime_dataflow_skeleton.py

### Data / Artifacts

- tmp/four_family_scope_smoke/input_samples
- tmp/runtime_dataflow_skeleton_smoke

### Prior Handoff

- docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- one active task doc for this refinement
- updated runtime/dataflow freeze-spec wording for `L1` input bundle and `L2` review contract
- updated runtime skeleton code exposing the refined contract families
- clearer routing outcome/status fields in runtime result/trace outputs
- one repo handoff document for this non-trivial refinement

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format for existing consumers.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow AGENTS.md.
- Follow docs/workflow/GPT_CODEX_WORKFLOW.md.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- Preserve the official top-level `L0 / L1 / L2` contract.
- Treat `L1` and `L2` as runtime-shell refinements, not final business-logic completion.
- Keep new structures runtime-only and additive.
- Do not silently promote routing outcome into final truth semantics.
- Keep heavy artifacts summarized or referenced, not embedded wholesale into result/trace outputs.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen dataset artifact names
- existing sample-directory invocation pattern for the new skeleton CLI
- official stage naming `L0 / L1 / L2`

Schema / field constraints:

- Schema changed allowed: YES for runtime-only additive result/trace/output structures; NO for frozen public dataset fields
- If yes, required compatibility plan: new fields remain additive under the runtime skeleton outputs and do not change existing dataset artifacts
- Frozen field names involved: existing documented dataset / manifest / metadata / label fields already frozen elsewhere

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/infer/run_runtime_dataflow_skeleton.py --input <sample_root> --output-dir <out_dir>`
  - `python -m py_compile <touched_python_files>`

Downstream consumers to watch:

- future `L1` implementation work
- future `L2` implementation work
- future runtime output-contract freeze task

---

## 9. Suggested Execution Plan

Recommended order:

1. Create the active task doc.
2. Refine the runtime freeze spec for `L1` input bundle and `L2` review contract.
3. Update runtime dataclasses / stage outputs to expose explicit contract families.
4. Refine result/trace output payloads with clearer routing outcome/status fields.
5. Run focused syntax and smoke validation.
6. Produce handoff.

Task-specific execution notes:

- Keep the implementation narrow and contract-first.
- Prefer bundle summaries over dumping raw heavy payloads into outputs.
- Preserve the current additive runtime package shape unless a smaller path is clearly better.

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

- [ ] `L1` main-judgment input bundle is documented and exposed more explicitly
- [ ] `L2` high-cost review contract is documented and exposed more explicitly
- [ ] runtime result/trace outputs expose clearer routing outcome/status fields
- [ ] the refinement stays additive and does not claim final `L1` / `L2` business logic completion

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile src/warden/runtime/__init__.py src/warden/runtime/core.py src/warden/runtime/pipeline.py scripts/infer/run_runtime_dataflow_skeleton.py
python scripts/ci/check_task_doc.py docs/tasks/2026-04-22_runtime_l1_l2_contract_refinement.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md
python scripts/infer/run_runtime_dataflow_skeleton.py --input E:\Warden\tmp\four_family_scope_smoke\input_samples --output-dir E:\Warden\tmp\runtime_dataflow_skeleton_smoke_contract_refinement --limit 3
```

Expected evidence to capture:

- updated result/trace outputs include routing outcome/status fields
- `L1` and `L2` stage outputs expose more explicit contract families
- smoke execution still completes on sample folders

---

## 12. Handoff Requirements

This task must end with handoff coverage matching docs/templates/HANDOFF_TEMPLATE.md.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
