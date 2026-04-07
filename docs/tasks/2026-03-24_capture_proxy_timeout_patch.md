# 2026-03-24_capture_proxy_timeout_patch

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于给现有抓取链路补充最小的可选代理与导航超时参数。
- 若涉及精确 CLI、兼容性、脚本路径或验证结果，以英文版为准。

## English Version

# Task Metadata

- Task ID: WARDEN-CAPTURE-PROXY-TIMEOUT-PATCH-V1
- Task Title: Add optional proxy and navigation-timeout CLI overrides to the current capture pipeline without changing defaults
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`; `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. Background

The current capture script already contains internal proxy support and a fixed `NAV_TIMEOUT_MS = 25000`, but those knobs are not exposed as operator-facing CLI parameters.
The user is seeing cases where the page can eventually open in a browser, while the scripted capture path still fails with navigation timeout.
The requested change is a minimal patch: make proxy and navigation-timeout overrides available through the existing capture path and the current benign/malicious runner scripts, without changing default behavior.

---

## 2. Goal

Add backward-compatible optional CLI flags for proxy and navigation-timeout control so operators can retry capture with a proxy and/or a longer timeout when needed, while keeping current defaults unchanged for existing commands.

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

- CLI argument parsing for the three existing entrypoints above
- parameter forwarding from benign/malicious runners into the capture script
- operator documentation for the new optional flags

---

## 4. Scope Out

This task must NOT do the following:

- do not change the default timeout value
- do not force all capture traffic through a proxy by default
- do not redesign navigation strategy beyond exposing the current timeout knob
- do not modify output schema, frozen filenames, or sample directory contracts
- do not change training, inference, labeling, clustering, or pool logic
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
- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`

### Data / Artifacts

- none

### Prior Handoff

- `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated capture CLI with optional `--proxy_server`, `--proxy_username`, `--proxy_password`, and `--nav_timeout_ms`
- updated benign/malicious runners that expose and forward the same optional knobs where relevant
- updated runbook documentation showing optional usage
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

- The new flags must be optional.
- Existing commands without the new flags must keep current behavior.
- The default `NAV_TIMEOUT_MS` behavior must remain `25000` unless overridden by CLI.

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

- VM operator commands documented in the current prep handoff
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current capture and runner CLIs.
2. Add optional proxy and nav-timeout args to the capture script.
3. Add matching optional forwarding args to the benign and malicious runners.
4. Update the runbook with one or two concrete operator examples.
5. Run the smallest meaningful validation.
6. Prepare handoff.

Task-specific execution notes:

- Do not change default constants beyond allowing CLI override.
- Prefer passing runtime overrides through local variables instead of rewriting unrelated logic.
- Keep the patch focused on operator control, not heuristic redesign.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] capture script accepts optional proxy and nav-timeout CLI flags
- [ ] benign runner accepts and forwards the new optional flags
- [ ] malicious runner accepts and forwards the new optional flags
- [ ] existing commands remain valid without modification
- [ ] no schema / output contract changed
- [ ] runbook docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

Task-specific acceptance checks:

- [ ] `--help` output shows the new flags on the affected CLIs
- [ ] `py_compile` passes for the touched Python files
- [ ] documentation reflects that proxy use is optional rather than default

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

- help output showing the new flags
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

- `docs/handoff/2026-03-24_capture_proxy_timeout_patch.md`

---

## 13. Open Questions / Blocking Issues

- none
