# 2026-04-13_legacy_html_dry_run_clarity

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于收紧 `convert_legacy_html_to_json.py` 的操作提示，避免把 `--dry_run` 误解成实际转换。
- 本次不改转换核心逻辑，只改提示与运行说明。

## English Version

# Task Metadata

- Task ID: WARDEN-LEGACY-HTML-DRYRUN-CLARITY-V1
- Task Title: Clarify dry-run and post-conversion operator messaging for the legacy HTML-to-JSON conversion utility
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module / maintenance utility / operator docs
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/handoff/2026-04-10_capture_html_json_storage.md`
- Created At: 2026-04-13
- Requested By: user

---

## 1. Background

The new legacy HTML conversion utility currently behaves correctly: `--dry_run` reports what would be converted and does not write files.
However, the operator-facing output is still easy to misread during real usage because it does not explicitly say that no files were written and does not clearly remind the user that default conversion keeps legacy `.html` files unless `--delete_original_html` is supplied.

---

## 2. Goal

Make the conversion utility and runbook more explicit so operators can immediately tell whether they only ran a report, whether JSON files were written, and whether legacy `.html` files were intentionally retained or deleted.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/maintenance/convert_legacy_html_to_json.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- operator-facing terminal messaging
- runbook wording for `--dry_run` and `--delete_original_html`

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the conversion logic
- do not change the default conversion semantics
- do not rename CLI flags
- do not touch unrelated capture or downstream-reader code

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/maintenance/convert_legacy_html_to_json.py`

### Prior Handoff

- `docs/handoff/2026-04-10_capture_html_json_storage.md`

### Missing Inputs

- none

---

## 6. Required Outputs

- clearer dry-run and post-run console messages in the conversion utility
- updated runbook wording that explains report-only mode versus actual conversion and optional old-file deletion
- a repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve current CLI flags and default behavior.
- Do not change conversion results for non-dry-run execution.
- Do not add dependencies.
- Prefer minimal patch over broader refactor.
- Update docs if operator-facing behavior description changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.

Task-specific constraints:

- `--dry_run` must remain read-only.
- Default non-dry-run conversion must still retain legacy `.html` files unless `--delete_original_html` is explicitly provided.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: NO
- Public interface changed: NO
- Existing CLI still valid: YES

Affected interfaces:

- console output of `convert_legacy_html_to_json.py`
- runbook instructions for conversion usage

---

## 9. Suggested Execution Plan

1. Reproduce the reported `--dry_run` behavior.
2. Add explicit operator messages for dry-run, conversion-with-retain, and conversion-with-delete.
3. Update the runbook wording.
4. Run targeted validation and prepare handoff.

---

## 10. Acceptance Criteria

- [ ] `--dry_run` output explicitly states that no files were written
- [ ] non-dry-run output explicitly states whether legacy `.html` files were retained or deleted
- [ ] runbook wording matches actual behavior
- [ ] validation was run or inability to run was explicitly stated
- [ ] handoff is provided

---

## 11. Validation Checklist

```bash
python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots E:\Warden\data\raw\benign\evasion --dry_run
python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots E:\Warden\data\raw\benign\evasion --limit 1
```

Expected evidence:

- dry-run logs explicitly say no files were written
- non-dry-run logs explicitly say legacy `.html` files were retained unless delete mode is used

---

## 12. Handoff Requirements

- `docs/handoff/2026-04-13_legacy_html_dry_run_clarity.md`

---

## 13. Open Questions / Blocking Issues

- none
