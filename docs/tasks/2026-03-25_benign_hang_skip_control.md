# 2026-03-25_benign_hang_skip_control

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务单覆盖 benign 抓取中的“单 URL 卡住导致整批被拖死”问题，以及人工 `skip` 跳过当前 URL 的操作能力。
- 若涉及精确 CLI、默认值、输出字段、兼容性或验证结果，以英文版为准。

## English Version

# Task Metadata

- Task ID: WARDEN-BENIGN-HANG-SKIP-CONTROL-V1
- Task Title: Add supervised benign capture mode with manual skip and per-URL hard timeout without changing sample sidecar schema
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data module / benign capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/handoff/2026-03-24_capture_hardening_day1_support.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The current benign runner invokes the shared capture script once for the entire batch and then waits until that single subprocess returns.
This means one pathological URL can consume the whole batch slot, and the operator has no supported way to skip only the current URL and continue with the remaining benign URLs.
The user explicitly asked to inspect why the batch appears to get stuck, adjust the strategy, and add an operator-side `skip` capability that can abort only the current URL and continue the rest of the benign batch.

---

## 2. Goal

Add a supervised benign capture mode that runs URLs one by one through child capture subprocesses, allowing an operator to type `skip` in the terminal to abort only the current URL and continue the batch, while also supporting an optional per-URL hard timeout.
This change must keep existing sample sidecar names stable and avoid changing label semantics, training logic, or inference behavior.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/benign/recover_benign_batch.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- benign runner CLI
- batch supervision strategy for benign runs when explicitly enabled
- batch-level benign summary content if required to record supervised skip/timeout outcomes
- interrupted-batch recovery artifacts for partial benign sample directories
- operator documentation for supervised benign capture

---

## 4. Scope Out

This task must NOT do the following:

- do not change sample sidecar filenames under each saved sample directory
- do not change label semantics
- do not modify training logic or inference logic
- do not redesign malicious runner behavior
- do not rewrite the shared capture script into a new framework
- do not change default benign behavior when supervision flags are not enabled

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

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/benign/recover_benign_batch.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `https://flowroute.com/` as the user-named benign sample to investigate

### Prior Handoff

- `docs/handoff/2026-03-24_capture_hardening_day1_support.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- an updated benign runner with optional supervised mode
- operator-facing `skip` support for the current benign URL
- an optional per-URL hard timeout for supervised benign mode
- a recovery helper that can identify and optionally quarantine partial benign sample directories before retry
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

- Default benign behavior must remain the current single-subprocess batch mode unless supervision flags are explicitly enabled.
- Manual `skip` must abort only the current URL, not the whole benign batch.
- The benign batch summary must record whether supervised mode, skip, or hard timeout was used.
- Partial-sample retry decisions must be derived from on-disk sample directories rather than assuming a batch manifest exists.
- Any strategy adjustment must stay inside the benign runner rather than broad capture-pipeline redesign unless a smaller change proves impossible.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing benign runner commands without the new flags
- existing capture script commands
- existing sample sidecar filenames and directory contracts

Schema / field constraints:

- Schema changed allowed: PARTIAL
- If yes, required compatibility plan: only additive batch-summary fields under `benign_capture_run.json` are allowed; sample sidecar schemas must not change
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --input_path ...`
  - `python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --input_path ... --label benign ...`

Downstream consumers to watch:

- operator review of `benign_capture_run.json`
- recovery tooling that copies or reads `benign_capture_run.json`
- operators triaging partial sample directories after `skip` or manual interruption

---

## 9. Suggested Execution Plan

Recommended order:

1. Inspect the current benign runner and capture control flow to explain why one URL can stall the whole batch.
2. Add supervised benign mode to the runner behind explicit flags.
3. Add `skip` control and per-URL hard-timeout handling to the supervised path.
4. Ensure interrupted runs can be inventoried for partial sample directories and, when requested, quarantined before retry.
5. Update docs and task/handoff artifacts.
6. Validate CLI/help and syntax.
7. If the environment allows browser launch, attempt a targeted benign repro using `https://flowroute.com/`.

Task-specific execution notes:

- Keep the shared capture script as the per-URL worker to avoid larger behavioral drift.
- In supervised mode, child capture workers should not inherit interactive stdin.
- On Windows, killing the current URL should terminate the worker process tree instead of leaving browser children behind.
- Recovery should treat on-disk sample completeness as the source of truth for partial skip leftovers.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] benign runner supports supervised mode
- [ ] operator can type `skip` to abort only the current URL when supervised mode is enabled
- [ ] benign runner supports optional per-URL hard timeout
- [ ] default benign runner behavior remains backward compatible when the new flags are absent
- [ ] sample sidecar schema did not change
- [ ] docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

Task-specific acceptance checks:

- [ ] `--help` exposes the new supervision flags
- [ ] `py_compile` passes for the touched Python files
- [ ] `benign_capture_run.json` records supervised skip/timeout outcomes when the feature is used
- [ ] recovery artifacts explicitly list partial retry URLs and partial sample directories
- [ ] if `https://flowroute.com/` cannot be tested locally, the blocking reason is stated explicitly

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] CLI help check
- [ ] supervised-mode dry or targeted run
- [ ] batch-summary spot-check

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
python scripts/data/benign/recover_benign_batch.py --help
python -m py_compile scripts/data/benign/run_benign_capture.py scripts/data/benign/recover_benign_batch.py
python scripts/data/benign/run_benign_capture.py --input_path ... --output_root ... --interactive_skip --url_hard_timeout_ms ...
python scripts/data/benign/recover_benign_batch.py --input_path ... --output_root ... --inventory_only
```

Expected evidence to capture:

- help output showing the new flags
- batch summary fields for supervised mode
- recovery inventory showing partial retry artifacts
- any repro result or blocker for `https://flowroute.com/`

---

## 12. Handoff Requirements

This task must end with a handoff that follows `docs/templates/HANDOFF_TEMPLATE.md`.

The handoff must explicitly cover:

- why the old benign strategy could stall the whole batch
- what the supervised strategy changes
- how manual `skip` and hard timeout behave
- how partial sample directories are identified and optionally quarantined before retry
- whether `flowroute.com` was actually reproduced or blocked by environment constraints
- compatibility notes for `benign_capture_run.json`

Recommended repo handoff path:

- `docs/handoff/2026-03-25_benign_hang_skip_control.md`
