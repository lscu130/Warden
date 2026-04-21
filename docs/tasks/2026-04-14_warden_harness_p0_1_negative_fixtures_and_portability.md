# 2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Warden Harness P0.1 任务的正式任务单。
- 若中英文存在冲突，以英文版为准。
- 本任务的 Markdown 交付默认采用中文摘要在前、英文全文在后。

### 摘要

- 任务 ID：WARDEN-HARNESS-P0-1-NEGATIVE-FIXTURES-AND-PORTABILITY
- 任务主题：Warden Harness P0.1 Negative Fixtures and Portability Cleanup
- 当前状态：DONE
- 相关模块：documentation maintenance / harness baseline

### 当前任务要点

- 目标是在不改变训练、推理、capture 输出和既有冻结契约的前提下，对 Harness P0 做最小补强。
- 本任务只修 4 类已知缺口：negative fixtures、统一入口、路径可移植性、task doc metadata 检查补齐。
- 不得把本任务膨胀成 benchmark、CI 平台化或 schema 深度重构。

## English Version

# Task Metadata

- Task ID: WARDEN-HARNESS-P0-1-NEGATIVE-FIXTURES-AND-PORTABILITY
- Task Title: Warden Harness P0.1 Negative Fixtures and Portability Cleanup
- Owner Role: Codex execution engineer
- Priority: P0
- Status: DONE
- Related Module: documentation maintenance / harness baseline
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/harness/WARDEN_HARNESS_BASELINE.md`; `docs/frozen/SCHEMA_REGISTRY.md`; `docs/tasks/2026-04-10_warden_harness_p0_guardrails.md`; `docs/handoff/2026-04-10_warden_harness_p0_guardrails.md`
- Created At: 2026-04-20
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.
- If the task will produce Markdown deliverables, define them as bilingual by default: Chinese summary first, full English version second, with English authoritative for exact facts and contract wording.

---

## 1. Background

Harness P0 already introduced the first repo-native guardrail layer for Warden: task doc lint, handoff lint, schema compatibility guard, a schema registry, a harness baseline doc, and a smoke baseline skeleton.

The current known gaps are narrower and already identified:

- the three existing checkers still lack checked-in negative fixtures;
- there is no unified local runner for the existing harness checks;
- the harness doc and schema guard still hardcode `E:\Warden...` paths;
- the task-doc checker does not yet enforce all key task-template metadata markers.

This follow-up is needed to make the current P0 harness easier to validate, more portable across repo locations, and easier to extend later without turning the harness into a larger platform project.

---

## 2. Goal

Deliver the minimum P0.1 harness reinforcement for Warden by adding positive and negative fixtures for the three existing checkers, adding a thin unified runner, replacing hardcoded Windows repo paths with repo-relative or script-derived path logic, tightening task-doc metadata validation to include the missing template fields, and updating the corresponding documentation and handoff, while preserving all existing frozen contracts and existing checker purpose boundaries.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/harness/`
- `docs/frozen/`
- `scripts/ci/`
- `tests/smoke/`
- `tests/fixtures/`
- `README.md` or a docs index file only if a minimal pointer becomes necessary

This task is allowed to change:

- small additive harness checker enhancements
- positive and negative fixtures for the existing three checkers
- a unified local harness runner
- path portability fixes for current harness docs and schema guard logic
- task-doc metadata marker checks
- minimal harness-documentation updates

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify training logic
- modify inference routing logic
- modify capture output structure
- modify TrainSet V1 semantics
- modify Gate / Evasion protocol semantics
- rename any frozen field, file name, enumeration, or existing CLI
- add third-party dependencies
- expand the schema guard into a deep nested-schema validator
- build a corpus-level benchmark platform
- add heavyweight CI platform integration
- clean up unrelated repository changes

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/harness/WARDEN_HARNESS_BASELINE.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/tasks/2026-04-10_warden_harness_p0_guardrails.md`
- `docs/handoff/2026-04-10_warden_harness_p0_guardrails.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`
- `scripts/ci/check_schema_compat.py`

### Data / Artifacts

- `tests/smoke/golden_manifest.example.json`
- current `tests/smoke/` contents
- current repo task and handoff docs used as structure references

### Prior Handoff

- `docs/handoff/2026-04-10_warden_harness_p0_guardrails.md`

### Missing Inputs

- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- `docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- positive and negative fixtures under `tests/fixtures/harness/`
- `scripts/ci/run_harness_checks.py`
- an updated `scripts/ci/check_task_doc.py`
- portability updates in `docs/harness/WARDEN_HARNESS_BASELINE.md`
- portability updates in `scripts/ci/check_schema_compat.py`

Be concrete.

Examples:

- updated Python script
- new additive local CLI
- markdown doc update
- new repo-local fixtures
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
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- Keep P0.1 narrow and additive.
- Keep the doc lints structural only.
- Keep the schema guard top-level-only and do not expand it into nested-schema enforcement.
- Do not upgrade `uncertain / needs confirmation` surfaces to confirmed without explicit source support.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen field names and file-name conventions
- current training, inference, and data-protocol semantics
- the existing purpose boundary of the three P0 checker scripts

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: existing manifest-record fields, selected top-level keys checked by the schema guard, and current documented contract surfaces in `docs/frozen/SCHEMA_REGISTRY.md`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/ci/check_task_doc.py ...`
  - `python scripts/ci/check_handoff_doc.py ...`
  - `python scripts/ci/check_schema_compat.py --kind ... --path ...`

Downstream consumers to watch:

- operators using the existing P0 harness locally
- future local automation that may call the new unified runner

---

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs, P0 baseline docs, and the three existing checker scripts.
2. Create the formal task doc before implementation.
3. Add a minimal fixture tree for task-doc, handoff-doc, and schema checks.
4. Expand `check_task_doc.py` metadata marker coverage.
5. Add `run_harness_checks.py` as a thin local unified runner.
6. Replace hardcoded repo paths with repo-relative or script-derived logic.
7. Update the baseline doc and only touch README if a minimal pointer is still necessary.
8. Run the minimum required validation, including both positive and negative fixtures.
9. Create the repo handoff last.

Task-specific execution notes:

- Keep the unified runner thin and local.
- Prefer importing the existing checker modules instead of shelling out.
- Use manifest-record fixtures for schema positive and negative checks so validation remains repo-native and deterministic.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] each of the three checkers has at least one positive fixture and one negative fixture
- [x] `check_task_doc.py` enforces the missing task metadata markers
- [x] the unified runner executes and returns non-zero on failure
- [x] baseline doc commands and path examples no longer depend on `E:\Warden...`
- [x] no existing schema, CLI, or output compatibility break was introduced
- [x] docs were updated or any doc debt was explicitly listed
- [x] a repo handoff document was created

---

## 11. Validation Checklist

Minimum validation expected:

- [x] `python -m py_compile` for `check_task_doc.py`
- [x] `python -m py_compile` for `check_handoff_doc.py`
- [x] `python -m py_compile` for `check_schema_compat.py`
- [x] `python -m py_compile` for `run_harness_checks.py`
- [x] task-doc positive fixture passes
- [x] task-doc negative fixture fails
- [x] handoff-doc positive fixture passes
- [x] handoff-doc negative fixture fails
- [x] schema positive fixture passes
- [x] schema negative fixture fails
- [x] unified runner positive suite passes
- [x] unified runner negative suite fails with non-zero
- [x] baseline-doc path and command spot-check passes

Commands to run if applicable:

```bash
python -m py_compile scripts/ci/check_task_doc.py
python -m py_compile scripts/ci/check_handoff_doc.py
python -m py_compile scripts/ci/check_schema_compat.py
python -m py_compile scripts/ci/run_harness_checks.py
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/positive_minimal.md
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/negative_missing_requested_by.md
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/positive_minimal.md
python scripts/ci/check_handoff_doc.py tests/fixtures/handoff_doc/negative_missing_not_run.md
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/positive_manifest_record.json
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json
python scripts/ci/run_harness_checks.py
python scripts/ci/run_harness_checks.py --suite negative
```

Expected evidence to capture:

- clear PASS output on positive fixtures
- clear FAIL output on negative fixtures
- non-zero exit behavior from the unified runner on the negative suite
- confirmation that `docs/harness/WARDEN_HARNESS_BASELINE.md` uses repo-relative commands

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

- `E:\Warden\docs\handoff\2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
