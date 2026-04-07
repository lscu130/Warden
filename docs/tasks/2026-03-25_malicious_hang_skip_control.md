# 2026-03-25_malicious_hang_skip_control

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。
### 使用说明

- 本任务单覆盖 malicious 抓取中的“单 URL 卡住导致整批被拖死”问题，以及人工 `skip` 跳过当前 URL 的能力。
- benign 的 partial recovery 不属于本任务；对 malicious，卡住或失败后留下的新 partial 样本目录直接删除，不做 recovery。

## English Version

# Task Metadata

- Task ID: WARDEN-MALICIOUS-HANG-SKIP-CONTROL-V1
- Task Title: Add supervised malicious capture mode with manual skip, per-URL hard timeout, and automatic deletion of newly created partial sample directories on failed or aborted URLs
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data module / malicious capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The current malicious runner still invokes the shared capture script in larger grouped subprocesses and then waits for those subprocesses to return.
This leaves the operator without a supported way to skip only the current pathological malicious URL when that URL wedges the child process.
The user explicitly requested that malicious runs also support terminal `skip`, but unlike benign runs, any partial sample directories left by a stuck or aborted malicious URL should be deleted directly instead of being recovered later.

---

## 2. Goal

Add an optional supervised malicious mode that runs one malicious URL per child capture subprocess, allows the operator to type `skip` to abort only the current URL, supports an optional per-URL hard timeout, and deletes any sample directories newly created during that failed or aborted URL attempt.
This change must preserve the existing default malicious runner behavior when the new supervision flags are not enabled.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/malicious/run_malicious_capture.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- malicious runner CLI
- malicious batch supervision strategy when explicitly enabled
- batch-level malicious summary content if required to record supervised skip/timeout/delete outcomes
- operator documentation for supervised malicious capture

---

## 4. Scope Out

This task must NOT do the following:

- do not change sample sidecar filenames under each saved sample directory
- do not change label semantics
- do not modify training logic or inference logic
- do not add a malicious recovery helper analogous to benign recovery
- do not rewrite the shared capture script into a new framework
- do not change default malicious behavior when supervision flags are not enabled

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- current malicious batch execution flow through `--feed_manifest` or `--input_path`

### Prior Handoff

- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- an updated malicious runner with optional supervised mode
- operator-facing `skip` support for the current malicious URL
- an optional per-URL hard timeout for supervised malicious mode
- automatic deletion of newly created sample directories for skipped, timed-out, or failed malicious URLs
- updated operator docs
- a formal repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change sample-output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Default malicious behavior must remain the current grouped-subprocess mode unless supervision flags are explicitly enabled.
- Manual `skip` must abort only the current malicious URL, not the whole batch.
- Any new sample directories created during a skipped, timed-out, or failed malicious URL attempt must be deleted immediately instead of being preserved for later recovery.
- Any strategy adjustment must stay inside the malicious runner rather than broad capture-pipeline redesign unless a smaller change proves impossible.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing malicious runner commands without the new flags
- existing capture script commands
- existing sample sidecar filenames and directory contracts

Schema / field constraints:

- Schema changed allowed: PARTIAL
- If yes, required compatibility plan: only additive batch-summary fields under `malicious_capture_run.json` are allowed; sample sidecar schemas must not change
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/malicious/run_malicious_capture.py --feed_manifest ...`
  - `python scripts/data/malicious/run_malicious_capture.py --input_path ...`
  - `python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --input_path ... --label phish ...`

Downstream consumers to watch:

- operator review of `malicious_capture_run.json`
- VM execution notes and prep docs for Day 1 batches

---

## 9. Suggested Execution Plan

Recommended order:

1. Inspect the current malicious runner and capture control flow to explain why one URL can stall the whole grouped subprocess.
2. Add supervised malicious mode behind explicit flags.
3. Add `skip` control and per-URL hard-timeout handling to the supervised path.
4. Delete newly created partial sample directories for skipped, timed-out, or failed malicious URLs.
5. Update docs and task/handoff artifacts.
6. Validate CLI/help and syntax.

Task-specific execution notes:

- Keep the shared capture script as the per-URL worker to avoid larger behavioral drift.
- In supervised mode, child capture workers should not inherit interactive stdin.
- On Windows, killing the current URL should terminate the worker process tree instead of leaving browser children behind.
- Cleanup should only target sample directories created during the current URL attempt; do not delete unrelated earlier outputs.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] malicious runner supports supervised mode
- [ ] operator can type `skip` to abort only the current URL when supervised mode is enabled
- [ ] malicious runner supports optional per-URL hard timeout
- [ ] newly created partial sample directories for skipped, timed-out, or failed malicious URLs are deleted
- [ ] default malicious runner behavior remains backward compatible when the new flags are absent
- [ ] sample sidecar schema did not change
- [ ] docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

Task-specific acceptance checks:

- [ ] `--help` exposes the new supervision flags
- [ ] `py_compile` passes for the touched Python files
- [ ] `malicious_capture_run.json` records supervised skip/timeout/delete outcomes when the feature is used

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] CLI help check
- [ ] supervised-mode dry or targeted run
- [ ] batch-summary spot-check

Commands to run if applicable:

```bash
python scripts/data/malicious/run_malicious_capture.py --help
python -m py_compile scripts/data/malicious/run_malicious_capture.py
python scripts/data/malicious/run_malicious_capture.py --input_path ... --output_root ... --interactive_skip --url_hard_timeout_ms ...
```

Expected evidence to capture:

- help output showing the new flags
- batch summary fields for supervised mode
- cleanup accounting for deleted partial sample directories

---

## 12. Handoff Requirements

This task must end with a handoff that follows `docs/templates/HANDOFF_TEMPLATE.md`.

The handoff must explicitly cover:

- why the old malicious strategy could stall the whole batch
- what the supervised strategy changes
- how manual `skip` and hard timeout behave
- how newly created partial sample directories are deleted for malicious failures or aborts
- compatibility notes for `malicious_capture_run.json`

Recommended repo handoff path:

- `docs/handoff/2026-03-25_malicious_hang_skip_control.md`
