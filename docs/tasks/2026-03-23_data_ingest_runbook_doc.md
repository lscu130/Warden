# 2026-03-23_data_ingest_runbook_doc

## 中文版

# Task Metadata

- Task ID: WARDEN-DATA-INGEST-RUNBOOK-V1
- Task Title: Add a day-to-day usage runbook for benign/malicious ingest and daily malicious capture operations
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`; `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`; `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- Created At: 2026-03-23
- Requested By: user

---

## 1. Background

The data-ingest pipeline scripts now exist, but there is no single operational Markdown guide that explains normal day-to-day usage.
The user specifically needs a practical runbook for repeated usage, especially the common case of capturing roughly 300 malicious URLs in a daily batch, plus smaller benign usage and post-capture follow-up commands.

---

## 2. Goal

Add one repository Markdown runbook that explains how to operate the current ingest scripts in normal usage.
The runbook must be practical, command-oriented, and easy to adapt by replacing absolute paths in the examples.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- operational documentation
- task tracking documentation
- delivery handoff documentation

---

## 4. Scope Out

This task must NOT do the following:

- change ingest script behavior
- change CLI arguments
- add dependencies
- redesign the ingest architecture

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`

### Data / Artifacts

- current ingest scripts
- the existing data-ingest task and handoff

### Prior Handoff

- `docs/handoff/2026-03-23_data_ingest_pipeline.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a new Markdown runbook for normal ingest usage
- a task document for this documentation task
- a handoff document for this documentation task

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

- Keep the runbook aligned with the existing script CLIs.
- Use absolute-path examples that the user can edit directly.
- Cover the daily malicious-batch use case explicitly.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- the current ingest script CLIs
- the existing capture output filenames
- the current sample-directory conventions

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --help`
  - `python scripts/data/malicious/run_malicious_capture.py --help`
  - `python scripts/data/malicious/build_malicious_train_pool.py --help`

Downstream consumers to watch:

- operators using the current ingest scripts manually
- future task and handoff docs that reference the runbook

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable CLI and output contracts.
3. Add a practical bilingual runbook.
4. Run minimal validation on the doc content and references.
5. Prepare handoff.

Task-specific execution notes:

- Focus on operational clarity, not architecture theory.
- Include a repeatable daily malicious-300 example.
- Document the JSONL BOM pitfall on Windows.

---

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

- [x] A daily malicious-batch workflow is documented
- [x] Benign usage is documented
- [x] Post-capture clustering and pool commands are documented

---

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted smoke test
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

- `python E:\Warden\scripts\data\benign\run_benign_capture.py --help`
- `python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py --help`
- `python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help`

## English Version

# Task Metadata

- Task ID: WARDEN-DATA-INGEST-RUNBOOK-V1
- Task Title: Add a day-to-day usage runbook for benign/malicious ingest and daily malicious capture operations
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`; `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`; `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- Created At: 2026-03-23
- Requested By: user

---

## 1. Background

The data-ingest pipeline scripts now exist, but there is no single operational Markdown guide that explains normal day-to-day usage.
The user specifically needs a practical runbook for repeated usage, especially the common case of capturing roughly 300 malicious URLs in a daily batch, plus smaller benign usage and post-capture follow-up commands.

---

## 2. Goal

Add one repository Markdown runbook that explains how to operate the current ingest scripts in normal usage.
The runbook must be practical, command-oriented, and easy to adapt by replacing absolute paths in the examples.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- operational documentation
- task tracking documentation
- delivery handoff documentation

---

## 4. Scope Out

This task must NOT do the following:

- change ingest script behavior
- change CLI arguments
- add dependencies
- redesign the ingest architecture

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`

### Data / Artifacts

- current ingest scripts
- the existing data-ingest task and handoff

### Prior Handoff

- `docs/handoff/2026-03-23_data_ingest_pipeline.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a new Markdown runbook for normal ingest usage
- a task document for this documentation task
- a handoff document for this documentation task

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

- Keep the runbook aligned with the existing script CLIs.
- Use absolute-path examples that the user can edit directly.
- Cover the daily malicious-batch use case explicitly.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- the current ingest script CLIs
- the existing capture output filenames
- the current sample-directory conventions

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --help`
  - `python scripts/data/malicious/run_malicious_capture.py --help`
  - `python scripts/data/malicious/build_malicious_train_pool.py --help`

Downstream consumers to watch:

- operators using the current ingest scripts manually
- future task and handoff docs that reference the runbook

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable CLI and output contracts.
3. Add a practical bilingual runbook.
4. Run minimal validation on the doc content and references.
5. Prepare handoff.

Task-specific execution notes:

- Focus on operational clarity, not architecture theory.
- Include a repeatable daily malicious-300 example.
- Document the JSONL BOM pitfall on Windows.

---

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

- [x] A daily malicious-batch workflow is documented
- [x] Benign usage is documented
- [x] Post-capture clustering and pool commands are documented

---

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted smoke test
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

- `python E:\Warden\scripts\data\benign\run_benign_capture.py --help`
- `python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py --help`
- `python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help`