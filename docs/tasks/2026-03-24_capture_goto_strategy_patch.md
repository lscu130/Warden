# 2026-03-24_capture_goto_strategy_patch

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于给当前抓取链路补充最小导航等待策略参数与超时回退逻辑。
- 若涉及精确 CLI、兼容性、脚本路径或验证结果，以英文版为准。

## English Version

# Task Metadata

- Task ID: WARDEN-CAPTURE-GOTO-STRATEGY-PATCH-V1
- Task Title: Add optional goto wait-until control and load-timeout fallback to the current capture pipeline without changing output contracts
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-24_capture_proxy_timeout_patch.md`; `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. Background

The current capture script navigates with `page.goto(..., wait_until="load", timeout=...)`.
The user has already tested longer timeout and optional proxy overrides, but some sites still fail in scripted capture even though the page appears to open manually.
This strongly suggests the main issue is the success criterion at navigation time rather than simple reachability, so the next minimal patch should make the goto wait-until strategy operator-controllable and add a conservative fallback path when `load` times out.

---

## 2. Goal

Add a backward-compatible optional `--goto_wait_until` CLI flag to the current capture path and implement a minimal fallback from `load` to `domcontentloaded` when the initial `load` navigation attempt times out, without changing frozen outputs or default file contracts.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- CLI argument parsing for the three entrypoints above
- runtime navigation behavior inside the capture script
- operator documentation for the new optional flag and fallback behavior

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the whole capture pipeline
- do not remove the existing `load` default
- do not force all captures to use `domcontentloaded` by default without preserving compatibility
- do not change output schema, frozen filenames, or sample directory contracts
- do not modify training, inference, clustering, labeling, or pool logic
- do not add new third-party dependencies

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-24_capture_proxy_timeout_patch.md`
- `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`

### Data / Artifacts

- none

### Prior Handoff

- `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated capture CLI with optional `--goto_wait_until`
- minimal fallback from `load` timeout to `domcontentloaded`
- updated benign/malicious runners that expose and forward the new optional flag
- updated runbook documentation
- a formal repo handoff document

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

- `load` must remain the default operator-visible wait-until mode.
- The fallback should only trigger for navigation-timeout-like failures on the initial `load` attempt.
- Existing commands without the new flag must keep working.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing `run_benign_capture.py` commands
- existing `run_malicious_capture.py` commands
- existing `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` commands

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --input_path ...`
  - `python scripts/data/malicious/run_malicious_capture.py --input_path ... --source ...`
  - `python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --input_path ... --label ...`

Downstream consumers to watch:

- operator commands in the runbook
- VM capture commands that may later opt into the new flag

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current capture navigation path and existing runner CLIs.
2. Add `--goto_wait_until` to the capture script.
3. Add the minimal `load` timeout fallback to `domcontentloaded`.
4. Expose and forward the new flag from the benign and malicious runners.
5. Update the runbook with practical examples.
6. Run the smallest meaningful validation.
7. Prepare handoff.

Task-specific execution notes:

- Keep the fallback narrowly scoped to timeout-like failures from the initial `load` navigation.
- Do not expand this patch into a larger navigation-policy redesign.
- Do not change output files just to record the fallback; logging is sufficient for this patch.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] capture script accepts optional `--goto_wait_until`
- [ ] capture script falls back from `load` timeout to `domcontentloaded`
- [ ] benign runner accepts and forwards `--goto_wait_until`
- [ ] malicious runner accepts and forwards `--goto_wait_until`
- [ ] existing commands remain valid without modification
- [ ] no schema / output contract changed
- [ ] runbook docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

Task-specific acceptance checks:

- [ ] `--help` output shows `--goto_wait_until` on the affected CLIs
- [ ] `py_compile` passes for the touched Python files
- [ ] documentation reflects that `load` remains default and fallback is automatic only for timeout-like failures

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
python scripts/data/benign/run_benign_capture.py --help
python scripts/data/malicious/run_malicious_capture.py --help
python -m py_compile scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py scripts/data/benign/run_benign_capture.py scripts/data/malicious/run_malicious_capture.py
```

Expected evidence to capture:

- help output showing the new flag
- successful `py_compile` run

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

- `docs/handoff/2026-03-24_capture_goto_strategy_patch.md`

---

## 13. Open Questions / Blocking Issues

- none
