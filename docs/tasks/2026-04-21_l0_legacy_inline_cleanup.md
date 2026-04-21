# L0 legacy inline cleanup task

## 中文版

> 面向人类阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于清理旧脚本里已经失活的 L0 内联实现。
- 边界很窄：删除 legacy L0 inline code，只保留兼容入口、brand 逻辑和 I/O 编排。
- 完成后必须做一轮 review，确认没有和其他调用方冲突，也没有引入编译或运行错误。

## 任务元信息

- Task ID: `TASK-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Task Title: `Delete the legacy inline L0 implementation from the old auto-label script while keeping compatibility entrypoints`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_module_extraction.md`; `docs/handoff/2026-04-21_l0_module_extraction.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

## 1. Background

上一条 L0 module extraction 已把 active L0 逻辑迁到 `src/warden/module/l0.py`，并让 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 的 active `derive_auto_labels(...)` 路径改为委托新模块执行。

但旧脚本里仍留着一整份 legacy L0 内联实现，包括 L0 prep helpers、stage helpers 和 risk helpers。这些代码当前不再走 active path，继续保留会造成双份实现和后续维护冲突。

用户已明确要求开一条很窄的 cleanup，删除这份 legacy inline L0 实现，只保留兼容入口、brand 和 I/O 编排，并在交付前 review 是否与其他部分冲突或导致报错。

## 2. Goal

Make `scripts/labeling/Warden_auto_label_utils_brandlex.py` stop carrying the legacy inline L0 implementation by fully relocating any remaining L0-owned helper logic into `src/warden/module/l0.py`, deleting the dead inline L0 block from the old script, preserving existing compatibility entrypoints and current caller behavior, and finishing with a concrete compile/import/smoke review for conflicts and errors.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

This task is allowed to change:

- ownership location of L0 prep/helper functions
- the old script body so it keeps only compatibility entrypoints, brand logic, shared helpers still actually needed, and sample-dir I/O orchestration
- validation and review notes proving no obvious conflict or error remains

## 4. Scope Out

This task must NOT do the following:

- redesign L0 detector behavior
- change the output schema of `derive_auto_labels(...)`
- rename frozen fields or routing keys
- modify capture/backfill call patterns
- redesign L1 or L2
- add dependencies

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_module_extraction.md`
- `docs/handoff/2026-04-21_l0_module_extraction.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- one or more real sample directories for smoke validation

### Prior Handoff

- `docs/handoff/2026-04-21_l0_module_extraction.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one minimal cleanup patch that removes the dead inline L0 block from the old script
- any required relocation of remaining L0-owned helpers into `src/warden/module/l0.py`
- one review-backed validation summary covering conflicts and error checks
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

- keep `derive_auto_labels(...)`, `derive_auto_labels_from_sample_dir(...)`, and `derive_rule_labels(...)` callable from the old script path
- keep brand extraction logic in the old script unless a tiny supporting move is strictly necessary
- delete the legacy inline L0 implementation instead of leaving duplicate dead code behind
- finish with an explicit conflict / breakage review across current callers

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- current script import path used by backfill and capture

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `html_features`; `brand_signals`; `intent_signals`; `evasion_signals`; `specialized_surface_signals`; `l0_routing_hints`; `risk_outputs`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current capture flow importing `derive_auto_labels`
  - current sample-dir auto-label flow

Downstream consumers to watch:

- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

## 9. Suggested Execution Plan

Recommended order:

1. Confirm which inline helpers in the old script are now dead or duplicated.
2. Move any still-needed L0-owned helper logic into `src/warden/module/l0.py`.
3. Delete the dead inline L0 block from the old script.
4. Run compile, import, and real-sample smoke checks.
5. Review for conflicts and document conclusions in the handoff.

Task-specific execution notes:

- prefer deleting code rather than leaving shadow copies
- keep the old script readable as a compatibility layer after cleanup
- the final review must state clearly whether any conflict or obvious breakage was found

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

- [ ] the dead inline L0 implementation is removed from the old script
- [ ] the old script still exports the same compatibility entrypoints
- [ ] current backfill and capture-side imports still compile
- [ ] smoke validation shows no obvious schema-key loss
- [ ] the final review explicitly states whether any conflict or error was found

## 11. Validation Checklist

Minimum validation expected:

- [ ] `py_compile` on touched Python files and current callers
- [ ] one import smoke test on the compatibility entrypoints
- [ ] one real-sample `derive_auto_labels_from_sample_dir(...)` smoke run
- [ ] one explicit review of conflicts / breakage findings
- [ ] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python ...
```

Expected evidence to capture:

- successful imports from existing callers
- smoke output still containing the expected top-level keys
- a written conclusion on conflict/error review

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- what dead code was removed
- behavior impact
- schema / interface impact
- validation performed
- conflict/error review conclusion
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Task Title: `Delete the legacy inline L0 implementation from the old auto-label script while keeping compatibility entrypoints`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_module_extraction.md`; `docs/handoff/2026-04-21_l0_module_extraction.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to delete the now-dead inline L0 implementation from the legacy auto-label script, keep only compatibility entrypoints plus brand logic and I/O orchestration there, and finish with an explicit conflict/error review.

## 1. Background

The previous L0 module extraction moved the active L0 implementation into `src/warden/module/l0.py` and changed the active `derive_auto_labels(...)` path in `scripts/labeling/Warden_auto_label_utils_brandlex.py` to delegate into that new module.

However, the old script still contains a full legacy inline L0 implementation, including L0 prep helpers, stage helpers, and risk helpers. That code is no longer on the active path and now creates duplicate implementation risk.

The user explicitly asked for a very narrow cleanup task that deletes this legacy inline L0 implementation, keeps only compatibility entrypoints plus brand logic and I/O orchestration in the old script, and ends with a review of conflict/error risk.

## 2. Goal

Make `scripts/labeling/Warden_auto_label_utils_brandlex.py` stop carrying the legacy inline L0 implementation by fully relocating any remaining L0-owned helper logic into `src/warden/module/l0.py`, deleting the dead inline L0 block from the old script, preserving existing compatibility entrypoints and current caller behavior, and finishing with a concrete compile/import/smoke review for conflicts and errors.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

This task is allowed to change:

- ownership location of L0 prep/helper functions
- the old script body so it keeps only compatibility entrypoints, brand logic, shared helpers still actually needed, and sample-dir I/O orchestration
- validation and review notes proving no obvious conflict or error remains

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- redesign L0 detector behavior
- change the output schema of `derive_auto_labels(...)`
- rename frozen fields or routing keys
- modify capture/backfill call patterns
- redesign L1 or L2
- add dependencies

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_module_extraction.md`
- `docs/handoff/2026-04-21_l0_module_extraction.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- one or more real sample directories for smoke validation

### Prior Handoff

- `docs/handoff/2026-04-21_l0_module_extraction.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one minimal cleanup patch that removes the dead inline L0 block from the old script
- any required relocation of remaining L0-owned helpers into `src/warden/module/l0.py`
- one review-backed validation summary covering conflicts and error checks
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

- keep `derive_auto_labels(...)`, `derive_auto_labels_from_sample_dir(...)`, and `derive_rule_labels(...)` callable from the old script path
- keep brand extraction logic in the old script unless a tiny supporting move is strictly necessary
- delete the legacy inline L0 implementation instead of leaving duplicate dead code behind
- finish with an explicit conflict/breakage review across current callers

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- current script import path used by backfill and capture

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `html_features`; `brand_signals`; `intent_signals`; `evasion_signals`; `specialized_surface_signals`; `l0_routing_hints`; `risk_outputs`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current capture flow importing `derive_auto_labels`
  - current sample-dir auto-label flow

Downstream consumers to watch:

- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

## 9. Suggested Execution Plan

Recommended order:

1. Confirm which inline helpers in the old script are now dead or duplicated.
2. Move any still-needed L0-owned helper logic into `src/warden/module/l0.py`.
3. Delete the dead inline L0 block from the old script.
4. Run compile, import, and real-sample smoke checks.
5. Review for conflicts and document conclusions in the handoff.

Task-specific execution notes:

- prefer deleting code rather than leaving shadow copies
- keep the old script readable as a compatibility layer after cleanup
- the final review must state clearly whether any conflict or error was found

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

- [x] the dead inline L0 implementation is removed from the old script
- [x] the old script still exports the same compatibility entrypoints
- [x] current backfill and capture-side imports still compile
- [x] smoke validation shows no obvious schema-key loss
- [x] the final review explicitly states whether any conflict or error was found

## 11. Validation Checklist

Minimum validation expected:

- [x] `py_compile` on touched Python files and current callers
- [x] one import smoke test on the compatibility entrypoints
- [x] one real-sample `derive_auto_labels_from_sample_dir(...)` smoke run
- [x] one explicit review of conflicts / breakage findings
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python ...
```

Expected evidence to capture:

- successful imports from existing callers
- smoke output still containing the expected top-level keys
- a written conclusion on conflict/error review

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- what dead code was removed
- behavior impact
- schema / interface impact
- validation performed
- conflict/error review conclusion
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

## 13. Open Questions / Blocking Issues

- none
