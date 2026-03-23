# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 data ingest runbook 文档任务的交接记录。
- 若中英内容冲突，以英文版为准。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-23-data-ingest-runbook-doc-handoff
- Related Task ID: WARDEN-DATA-INGEST-RUNBOOK-V1
- Task Title: Add a day-to-day usage runbook for benign/malicious ingest and daily malicious capture operations
- Module: Data module
- Author: Codex
- Date: 2026-03-23
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new bilingual operational runbook for the current data-ingest scripts.
The new document is focused on normal usage rather than architecture, with explicit commands for small benign runs, daily malicious batch capture of roughly 300 URLs, and post-capture cluster/pool/review/exclusion steps.
No ingest code was changed in this task.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` as a practical day-to-day runbook.
- Added a task document for this documentation delivery.
- Added this handoff document.

### Output / Artifact Changes

- Added a new repository runbook document for operators.
- Added a task record under `docs/tasks/`.
- Added a handoff record under `docs/handoff/`.

---

## 3. Files Touched

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-23_data_ingest_runbook_doc.md`
- `docs/handoff/2026-03-23_data_ingest_runbook_doc.md`

Optional notes per file:

- The runbook is bilingual and uses absolute-path placeholders intended for direct user replacement.
- The operational examples are aligned with the current ingest CLIs rather than hypothetical future wrappers.
- The runbook explicitly documents the Windows JSONL BOM pitfall encountered during validation.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have one dedicated document for normal ingest usage.
- The daily malicious-300 workflow is documented end to end.
- The benign, malicious, cluster, pool, review, and exclusion command sequence is now easier to follow repeatedly.

### Preserved Behavior

- No Python logic changed.
- No CLI flags changed.
- No output formats changed.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This task only added documentation.
No schema, code path, CLI behavior, or output structure was modified.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\data\malicious\build_malicious_clusters.py --help
python E:\Warden\scripts\data\malicious\build_malicious_train_pool.py --help
python E:\Warden\scripts\data\maintenance\build_dedup_review_manifest.py --help
python E:\Warden\scripts\data\maintenance\build_training_exclusion_lists.py --help
```

### Result

- Confirmed that all documented primary entry scripts still expose the expected CLI surfaces.
- Confirmed that the runbook commands align with the actual script names and argument structure.
- Confirmed that the new doc stays within documentation-only scope.

### Not Run

- live capture
- cluster generation
- pool generation

Reason:

This task only documents existing workflows.
It does not change runtime behavior, so CLI-surface validation was sufficient for this documentation pass.

---

## 7. Risks / Caveats

- The runbook is only as accurate as the current CLI contracts; if the scripts change later, the document must be updated with them.
- The example daily-300 manifest generation uses a Python inline snippet because there is no dedicated built-in `--limit` or sampling flag yet.
- Operators still need to replace placeholder absolute paths before running the examples.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/2026-03-23_data_ingest_runbook_doc.md`
- `docs/handoff/2026-03-23_data_ingest_runbook_doc.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If this runbook becomes the normal operational entry point, add a link to it from whichever top-level project doc the user treats as the main operator landing page.
- If daily malicious batches always target a fixed count, consider adding a dedicated helper script or CLI flag for subset manifest generation later.
- Keep the runbook updated whenever the ingest CLI or directory conventions change.
