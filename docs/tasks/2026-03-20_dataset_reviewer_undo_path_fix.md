# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-03-20-DATASET-REVIEWER-UNDO-PATH-FIX
- Task Title: Fix undo path nesting in dataset reviewer external script
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: external dataset review utility
- Related Issue / ADR / Doc: user thread request on 2026-03-20
- Created At: 2026-03-20
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.

---

## 1. Background

The user reported a path-recovery bug in `dataset_reviewed_switchable_targets.py`, currently provided from `C:\Users\20516\Downloads` and copied into the repo for traceability. When a sample directory is moved into a target folder such as `removed` and the action is later undone, the restored path can become nested under the wrong branch, producing structures such as `phish\removed\...` while `removed\phish\...` also remains. The script currently records move paths directly during remove/undo and does not enforce restoration to a canonical dataset-relative path.

---

## 2. Goal

Ensure undo for a remove action restores a sample to its canonical dataset-relative location instead of recreating reversed nested directory structures. Keep the existing UI, file names, and remove/keep workflow unchanged, and make the smallest safe patch needed to stabilize path handling and avoid obvious leftover directory confusion.

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\temp\dataset_reviewed_switchable_targets.py`
- `E:\Warden\docs\tasks\2026-03-20_dataset_reviewer_undo_path_fix.md`
- `E:\Warden\docs\handoff\2026-03-20_dataset_reviewer_undo_path_fix.md`

This task is allowed to change:

- remove/undo path restoration logic in the external script copy
- small internal helpers required to keep restore targets canonical
- task and handoff documentation for this change

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- redesign the full review workflow or UI
- rename existing public constants, buttons, or persisted state keys
- add third-party dependencies or broad cleanup unrelated to undo path recovery

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`

### Code / Scripts

- `C:\Users\20516\Downloads\dataset_reviewed_switchable_targets.py`
- `E:\Warden\temp\dataset_reviewed_switchable_targets.py`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`

### Data / Artifacts

- none
- none
- none

### Prior Handoff

- none

### Missing Inputs

- no reproducible sample directory was provided; validation will use targeted synthetic path scenarios
- no formal upstream spec exists for this external utility beyond current behavior and the user report

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- updated `E:\Warden\temp\dataset_reviewed_switchable_targets.py`
- validation summary for remove/undo canonical path behavior
- repo handoff document for this non-trivial change

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

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

Task-specific constraints:

- preserve the current keep/remove/undo control flow and button semantics
- do not change persisted state file names or log file names
- keep the fix self-contained inside the external script copy and repo workflow artifacts

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Tkinter button commands for keep/remove/undo
- current state JSON top-level sample status entries
- current target history file format

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `status`, `last_error`, `current_target_root`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\temp\dataset_reviewed_switchable_targets.py`
  - `python C:\Users\20516\Downloads\dataset_reviewed_switchable_targets.py`
  - none

Downstream consumers to watch:

- manual dataset review sessions relying on existing state files
- any operator expectation that removed samples preserve dataset-relative layout

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- use a canonical dataset-relative restore path for undo instead of trusting only the transient recorded source path
- add minimal directory cleanup only if needed to prevent obvious empty nested leftovers
- validate with a synthetic directory tree that mirrors `phish` and `removed`

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

- [ ] Undo restores a removed sample to `dataset_root / sample.key`
- [ ] The fix does not require changing state file or history file formats
- [ ] Validation covers the reported `phish` and `removed` path pattern

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\temp\dataset_reviewed_switchable_targets.py
python E:\Warden\tmp\dataset_reviewer_undo_validation.py
none
```

Expected evidence to capture:

- undo restores the sample directory to the canonical source path
- no extra nested `phish\removed` restore path is created in the validation scenario

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-03-20_dataset_reviewer_undo_path_fix.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- whether the reported visible problem is only wrong restore path or also unwanted empty directory leftovers
- none
- none

If none, write `none`.
