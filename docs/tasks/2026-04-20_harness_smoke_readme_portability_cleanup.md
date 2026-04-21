# 2026-04-20_harness_smoke_readme_portability_cleanup

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 harness smoke README 路径清理任务的正式任务单。
- 若中英文存在冲突，以英文版为准。
- 本任务的 Markdown 交付默认采用中文摘要在前、英文全文在后。

### 摘要

- 任务 ID：WARDEN-HARNESS-SMOKE-README-PORTABILITY-CLEANUP
- 任务主题：只修 smoke README 的旧绝对路径示例，并检查其他 harness-facing 文档是否仍有残留
- 当前状态：DONE
- 相关模块：documentation maintenance / harness baseline

### 当前任务要点

- 只修 `tests/smoke/README.md` 中残留的 `E:\Warden...` 示例。
- 顺手检查其他 harness-facing 文档是否还有同类残留。
- 不修改脚本逻辑，不修改 schema，不修改 runner。

## English Version

# Task Metadata

- Task ID: WARDEN-HARNESS-SMOKE-README-PORTABILITY-CLEANUP
- Task Title: Harness smoke README portability cleanup
- Owner Role: Codex execution engineer
- Priority: P0
- Status: DONE
- Related Module: documentation maintenance / harness baseline
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/harness/WARDEN_HARNESS_BASELINE.md`; `tests/smoke/README.md`; `docs/tasks/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`; `docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
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

The harness baseline doc was already updated to use repo-relative commands, but `tests/smoke/README.md` still contains older `E:\Warden...` absolute-path examples.

A read-only scan across harness-facing docs confirms:

- `tests/smoke/README.md` still contains two `E:\Warden...` command examples;
- `docs/harness/*.md` does not currently contain remaining `E:\Warden...` absolute-path examples.

This follow-up is needed to finish the documentation-facing portability cleanup for the smoke README without changing code or expanding scope.

---

## 2. Goal

Update `tests/smoke/README.md` so that its harness command examples use repo-relative invocation rather than hardcoded `E:\Warden...` paths, verify whether any other harness-facing Markdown docs still contain that old absolute-path pattern, and document the result in a repo handoff, without changing scripts, schema, runner behavior, or broader harness design.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `tests/smoke/README.md`
- harness-facing Markdown docs only for read-only checking

This task is allowed to change:

- one new formal task doc
- one new formal handoff doc
- the smoke README command examples only

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify any Python script
- modify schema guard logic
- modify runner behavior
- modify schema docs or contract semantics
- touch unrelated docs
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
- `tests/smoke/README.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- current harness-facing Markdown docs under `docs/harness/` and `tests/smoke/`

### Prior Handoff

- `docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`

### Missing Inputs

- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-04-20_harness_smoke_readme_portability_cleanup.md`
- `docs/handoff/2026-04-20_harness_smoke_readme_portability_cleanup.md`
- an updated `tests/smoke/README.md`

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

- only fix the smoke README absolute-path examples
- do not touch scripts, schema, or runner
- report whether any other harness-facing docs still contain `E:\Warden...`

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing harness checker CLIs
- existing harness runner CLI
- existing schema and contract semantics

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/smoke/golden_manifest.example.json`
  - `python scripts/ci/run_harness_checks.py`

Downstream consumers to watch:

- local harness operators reading smoke-baseline guidance

---

## 9. Suggested Execution Plan

Recommended order:

1. Confirm the remaining absolute-path occurrences in harness-facing docs.
2. Create the formal task doc before editing.
3. Update only the smoke README command examples to repo-relative form.
4. Re-scan harness-facing docs to confirm the cleanup result.
5. Validate the new task doc and handoff structure.
6. Produce the repo handoff last.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] `tests/smoke/README.md` no longer contains the old `E:\Warden...` command examples
- [x] any remaining `E:\Warden...` occurrences in harness-facing docs are explicitly reported
- [x] no script, schema, or runner logic changed
- [x] repo handoff was created

---

## 11. Validation Checklist

Minimum validation expected:

- [x] search `tests/smoke/README.md` before and after the update
- [x] search `docs/harness/*.md` and `tests/smoke/*.md` for remaining `E:\Warden...` occurrences
- [x] task-doc lint on this task doc
- [x] handoff-doc lint on the new handoff

Commands to run if applicable:

```bash
Select-String -Path tests/smoke/README.md -Pattern "E:\\Warden" -Context 1,1
Select-String -Path docs/harness/*.md,tests/smoke/*.md -Pattern "E:\\Warden" -CaseSensitive:$false
python scripts/ci/check_task_doc.py docs/tasks/2026-04-20_harness_smoke_readme_portability_cleanup.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-04-20_harness_smoke_readme_portability_cleanup.md
```

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-20_harness_smoke_readme_portability_cleanup.md`
