# 2026-03-24_benign_batch_recovery_retry

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务单覆盖 `tranco_top_1_10000_batch_0001` 这一批 benign 的中断恢复与缺失补抓。
- 若涉及精确 CLI、输出文件名、兼容性约束或验证结果，以英文版为准。

## English Version

# Task Metadata

- Task ID: WARDEN-BENIGN-BATCH-RECOVERY-RETRY-V1
- Task Title: Recover and retry missing benign samples for tranco_top_1_10000_batch_0001 without changing sample schema
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data module / benign capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`; `docs/handoff/2026-03-24_capture_hardening_day1_support.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. Background

The benign batch rooted at `E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001` was interrupted manually around `https://powerbi.com/`.
Because the upper-layer benign runner writes `benign_capture_run.json` only after the subprocess returns, the interrupted batch does not have a trustworthy batch-level summary file even though many sample directories already exist.
The requested fix is not a schema redesign: it is a bounded recovery path that inventories what already succeeded, identifies what is still missing, and retries only the missing benign URLs while keeping successful retry samples under the original output root.

---

## 2. Goal

Add a dedicated benign recovery helper that can reconstruct batch state from the existing sample directories, write an auditable recovery inventory, and retry only missing benign URLs for the current interrupted Tranco batch.
The result must preserve existing sample sidecar names and label semantics while producing a recovery-specific bookkeeping trail under `_recovery`.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/`
- `docs/handoff/`
- the existing benign output root under `data/raw/benign/2026-03-24_planA_day1_tranco_top_1_10000_batch_0001/`

This task is allowed to change:

- benign recovery helper CLI and recovery bookkeeping files under `_recovery`
- operator docs for interrupted benign recovery
- recovery-related task and handoff documents
- the current interrupted benign output root only by adding new successful retry sample directories and `_recovery` bookkeeping

---

## 4. Scope Out

This task must NOT do the following:

- do not change label semantics
- do not change training logic or inference logic
- do not rename frozen sample sidecar files
- do not expand `env.json`
- do not treat `final_url` as the recovery matching key
- do not rewrite or delete existing successful sample directories
- do not modify malicious capture behavior

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-03-24_capture_hardening_day1_support.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/common/io_utils.py`
- `scripts/data/common/url_utils.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt`
- `E:\Warden\data\raw\benign\2026-03-24_planA_day1_tranco_top_1_10000_batch_0001`

### Prior Handoff

- `docs/handoff/2026-03-24_capture_hardening_day1_support.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a new benign recovery helper script under `scripts/data/benign/`
- recovery inventory artifacts under `<output_root>\_recovery\<UTC_TS>\`
- a targeted recovery pilot that includes `https://powerbi.com/`
- updated operator documentation for interrupted benign recovery
- a formal repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format for existing sample sidecars.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Recovery matching must use canonicalized `url.json -> input_url`.
- A sample counts as captured only if the required recovery sidecars exist and at least one content sidecar exists.
- Partial sample directories must be reported explicitly instead of silently treated as success.
- Successful retries must still write sample directories under the original benign `output_root`.
- Recovery bookkeeping must stay under `<output_root>\_recovery\`.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py`
- existing sample sidecar filenames under benign sample directories
- current capture schema consumed downstream by manifest and review tooling

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --input_path ...`
  - `python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --input_path ... --label benign ...`

Downstream consumers to watch:

- `build_manifest.py` and related manifest / consistency paths
- batch-level operator review of the current Tranco benign output root

---

## 9. Suggested Execution Plan

Recommended order:

1. Inspect the interrupted benign output root and confirm current sample count.
2. Implement a benign recovery helper that inventories captured, missing, and partial samples.
3. Add recovery bookkeeping under `_recovery`.
4. Run `--inventory_only` and confirm the expected counts.
5. Run a tiny recovery pilot centered on `https://powerbi.com/`.
6. Continue retrying missing URLs with the helper.
7. Prepare handoff with actual validation results and any residual missing URLs.

Task-specific execution notes:

- Start recovery with explicit `--disable_route_intercept`.
- Keep `--goto_wait_until commit` and `--nav_timeout_ms 60000` for the first recovery pass.
- If the pilot still stalls at the same site, the next comparison should switch only `goto_wait_until`, not schema or sample layout.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] a dedicated benign recovery helper exists
- [ ] recovery inventory writes `inventory.json`, `captured_urls.txt`, `missing_urls.txt`, and `partial_samples.json`
- [ ] matching uses canonicalized `input_url` rather than `final_url`
- [ ] existing successful sample directories remain untouched
- [ ] successful retries continue writing to the original benign `output_root`
- [ ] docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

Task-specific acceptance checks:

- [ ] inventory-only validation reports `input_count = 1000`, `captured_count = 277`, and `missing_count = 723` for the current batch before retries
- [ ] recovery bookkeeping produces unique per-chunk summary copies
- [ ] a targeted retry pilot covering `https://powerbi.com/` was attempted
- [ ] no label, training, inference, or `env.json` schema change was introduced

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] inventory-only recovery audit
- [ ] targeted retry pilot
- [ ] sample-output spot-check
- [ ] recovery-bookkeeping spot-check

Commands to run if applicable:

```bash
python scripts/data/benign/recover_benign_batch.py --help
python -m py_compile scripts/data/benign/recover_benign_batch.py
python scripts/data/benign/recover_benign_batch.py --input_path ... --output_root ... --inventory_only
```

Expected evidence to capture:

- recovery inventory counts
- recovery directory paths
- targeted pilot command and result
- any residual missing URLs after attempted recovery

---

## 12. Handoff Requirements

This task must end with a handoff that follows `docs/templates/HANDOFF_TEMPLATE.md`.

The handoff must explicitly cover:

- what the recovery helper writes under `_recovery`
- how captured vs partial vs missing URLs are determined
- what retry pilot was actually run
- whether the interrupted batch was fully recovered or only partially recovered
- compatibility notes for existing sample directories

Recommended repo handoff path:

- `docs/handoff/2026-03-24_benign_batch_recovery_retry.md`
