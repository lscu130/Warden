# L0 module extraction task

## 中文版

> 面向人类阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前 `auto_label` 内嵌的 L0 逻辑拆成独立 module。
- 用户要求保持 `auto_label` 对外功能不变，不允许把阶段逻辑继续混在同一个大脚本里。
- 本任务采用的代码组织假设是：在 `src/warden` 下新增 `module/` 包，并建立 `l0.py`、`l1.py`、`l2.py`。

## 任务元信息

- Task ID: `TASK-L0-2026-04-21-MODULE-EXTRACTION`
- Task Title: `Extract L0 into a dedicated warden module package while keeping auto_label behavior unchanged`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

## 1. Background

当前 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 同时承载了通用 auto-label 入口、L0 阶段逻辑、brand 逻辑、风险汇总逻辑以及样本目录读取逻辑，文件职责偏混合。

用户已明确要求把 L0 独立拆出，同时保持 `auto_label` 的现有功能和外部调用方式不变，并在 `warden` 包内新增 module 目录来承接 `L0 / L1 / L2` 的阶段代码组织。

这个任务需要完成一次以代码组织为主、行为保持稳定的最小重构。

## 2. Goal

在不改变 `derive_auto_labels(...)`、`derive_auto_labels_from_sample_dir(...)` 以及当前 backfill / capture 调用方式和输出结构的前提下，把当前 L0 相关实现抽到 `src/warden/module/l0.py`，同时建立 `src/warden/module/l1.py` 和 `src/warden/module/l2.py` 作为明确阶段入口或占位模块；让 `Warden_auto_label_utils_brandlex.py` 保留 auto-label 编排与兼容入口，但不再把 L0 阶段实现和这些入口混写在一起。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `src/warden/__init__.py`
- `src/warden/module/__init__.py`
- `src/warden/module/l0.py`
- `src/warden/module/l1.py`
- `src/warden/module/l2.py`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_module_extraction.md`
- `docs/handoff/2026-04-21_l0_module_extraction.md`

This task is allowed to change:

- internal code organization for L0-stage logic
- imports needed to load the new `warden.module` package
- internal delegation from auto-label entrypoints into the extracted L0 module
- docs describing where L0 implementation now lives

## 4. Scope Out

This task must NOT do the following:

- change the external behavior or output schema of `derive_auto_labels(...)`
- rename frozen label fields or routing keys
- redesign L1 or L2 semantics
- add third-party dependencies
- combine L0, L1, and L2 back into a single module after extraction

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- current sample-dir based auto-label flow
- current capture-side auto-label flow

### Prior Handoff

- `none required`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a new `src/warden/module/` package with `l0.py`, `l1.py`, and `l2.py`
- a minimal refactor that delegates current L0 logic into the extracted module
- unchanged external auto-label entrypoints
- doc updates reflecting the new code location
- one repo handoff document

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

- keep `derive_auto_labels(...)` and `derive_auto_labels_from_sample_dir(...)` callable from their current script path
- treat this as a code-organization refactor first, not a detector redesign
- keep L1 and L2 modules minimal if they are only placeholders in this round
- avoid broad migration of unrelated brand or dataset logic into the new package

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- current capture-side import path for auto-label entrypoints
- current backfill-side import path for auto-label entrypoints

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `specialized_surface_signals`; `l0_routing_hints`; `brand_signals`; `intent_signals`; `evasion_signals`; `risk_outputs`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current capture flow that imports `derive_auto_labels`
  - current sample-dir auto-label flow

Downstream consumers to watch:

- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- future inference-module implementation work

## 9. Suggested Execution Plan

Recommended order:

1. Read the current L0-related functions in `Warden_auto_label_utils_brandlex.py`.
2. Create the new `src/warden/module/` package.
3. Move or re-home L0 logic into `l0.py` with the smallest viable import surface.
4. Keep `auto_label` entrypoints stable and delegate into the new module.
5. Add minimal `l1.py` and `l2.py` placeholders.
6. Run syntax and smoke validation.
7. Update docs and prepare handoff.

Task-specific execution notes:

- prefer a thin compatibility layer in `Warden_auto_label_utils_brandlex.py`
- keep placeholders explicit rather than inventing fake L1/L2 logic
- record any import-path assumption added for the new package

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] `src/warden/module/l0.py` exists and owns the extracted L0 logic
- [x] `src/warden/module/l1.py` exists
- [x] `src/warden/module/l2.py` exists
- [x] current auto-label callers still import and run through their existing script entrypoints
- [x] output schema remains unchanged on smoke validation

## 11. Validation Checklist

Minimum validation expected:

- [x] `py_compile` on touched Python files
- [x] one direct import smoke test for the current auto-label entrypoints
- [x] one small sample-dir auto-label smoke run
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\src\warden\module\l1.py
python -m py_compile E:\Warden\src\warden\module\l2.py
```

Expected evidence to capture:

- unchanged importability of existing auto-label entrypoints
- unchanged schema keys on a smoke sample
- clear note on where L0 logic now lives

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- code-organization change summary
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_module_extraction.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-MODULE-EXTRACTION`
- Task Title: `Extract L0 into a dedicated warden module package while keeping auto_label behavior unchanged`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to extract the current L0 implementation out of `Warden_auto_label_utils_brandlex.py` into a dedicated `src/warden/module/` package while keeping the current auto-label entrypoints and behavior unchanged.

## 1. Background

The current `scripts/labeling/Warden_auto_label_utils_brandlex.py` file mixes general auto-label entrypoints, L0-stage logic, brand logic, risk aggregation, and sample-dir reading inside one large script.

The user has explicitly requested that L0 be split out into its own dedicated module while preserving the current `auto_label` behavior and current external call sites, and that a new module folder be created inside the `warden` package to host `L0 / L1 / L2`.

This task is needed to complete a code-organization-first refactor with stable behavior.

## 2. Goal

Without changing the current behavior, call pattern, or output structure of `derive_auto_labels(...)`, `derive_auto_labels_from_sample_dir(...)`, or the current backfill and capture call paths, extract the current L0-related implementation into `src/warden/module/l0.py`, create `src/warden/module/l1.py` and `src/warden/module/l2.py` as explicit stage entrypoint or placeholder modules, and keep `Warden_auto_label_utils_brandlex.py` as the auto-label orchestration and compatibility layer rather than a file that still mixes the L0 stage implementation into the same body.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `src/warden/__init__.py`
- `src/warden/module/__init__.py`
- `src/warden/module/l0.py`
- `src/warden/module/l1.py`
- `src/warden/module/l2.py`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_module_extraction.md`
- `docs/handoff/2026-04-21_l0_module_extraction.md`

This task is allowed to change:

- internal code organization for L0-stage logic
- imports needed to load the new `warden.module` package
- internal delegation from auto-label entrypoints into the extracted L0 module
- docs describing where the L0 implementation now lives

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- change the external behavior or output schema of `derive_auto_labels(...)`
- rename frozen label fields or routing keys
- redesign L1 or L2 semantics
- add third-party dependencies
- combine L0, L1, and L2 back into a single module after extraction

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- current sample-dir based auto-label flow
- current capture-side auto-label flow

### Prior Handoff

- `none required`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a new `src/warden/module/` package with `l0.py`, `l1.py`, and `l2.py`
- a minimal refactor that delegates current L0 logic into the extracted module
- unchanged external auto-label entrypoints
- doc updates reflecting the new code location
- one repo handoff document

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

- keep `derive_auto_labels(...)` and `derive_auto_labels_from_sample_dir(...)` callable from their current script path
- treat this as a code-organization refactor first, not a detector redesign
- keep L1 and L2 modules minimal if they are only placeholders in this round
- avoid broad migration of unrelated brand or dataset logic into the new package

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- current capture-side import path for auto-label entrypoints
- current backfill-side import path for auto-label entrypoints

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `specialized_surface_signals`; `l0_routing_hints`; `brand_signals`; `intent_signals`; `evasion_signals`; `risk_outputs`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current capture flow that imports `derive_auto_labels`
  - current sample-dir auto-label flow

Downstream consumers to watch:

- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- future inference-module implementation work

## 9. Suggested Execution Plan

Recommended order:

1. Read the current L0-related functions in `Warden_auto_label_utils_brandlex.py`.
2. Create the new `src/warden/module/` package.
3. Move or re-home L0 logic into `l0.py` with the smallest viable import surface.
4. Keep `auto_label` entrypoints stable and delegate into the new module.
5. Add minimal `l1.py` and `l2.py` placeholders.
6. Run syntax and smoke validation.
7. Update docs and prepare handoff.

Task-specific execution notes:

- prefer a thin compatibility layer in `Warden_auto_label_utils_brandlex.py`
- keep placeholders explicit rather than inventing fake L1/L2 logic
- record any import-path assumption added for the new package

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] `src/warden/module/l0.py` exists and owns the extracted L0 logic
- [x] `src/warden/module/l1.py` exists
- [x] `src/warden/module/l2.py` exists
- [x] current auto-label callers still import and run through their existing script entrypoints
- [x] output schema remains unchanged on smoke validation

## 11. Validation Checklist

Minimum validation expected:

- [x] `py_compile` on touched Python files
- [x] one direct import smoke test for the current auto-label entrypoints
- [x] one small sample-dir auto-label smoke run
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\src\warden\module\l1.py
python -m py_compile E:\Warden\src\warden\module\l2.py
```

Expected evidence to capture:

- unchanged importability of existing auto-label entrypoints
- unchanged schema keys on a smoke sample
- clear note on where L0 logic now lives

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- code-organization change summary
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_module_extraction.md`

## 13. Open Questions / Blocking Issues

- none
