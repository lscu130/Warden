# 2026-03-27_phishtank_single_step_export

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PT 单脚本导出整合任务的任务定义。
- 若涉及精确 CLI、默认输出路径、兼容性、保留旧脚本与否、验证结论或文档命令，以英文版为准。

## 1. 背景

仓库里已经有两个串联脚本：

- 按 `verification_time` 从 PT `verified_online.csv` 导出 URL-only CSV
- 把 URL-only CSV 转成一行一个 URL 的 TXT

用户现在要求把它们“合成一个”，同时还要求说明当前仓库里与本任务无关的脏改动情况。

## 2. 目标

在不破坏现有兼容性的前提下，把主 PT 导出脚本升级成一次运行同时产出 URL-only CSV 和一行一个 URL 的 TXT，并把 runbook 命令改成单脚本主路径；旧的 CSV-to-TXT helper 保留为兼容工具，不做删除。

## 3. 范围

- 纳入：PT 主导出脚本整合、runbook 命令更新、task / handoff
- 排除：删除旧 helper、capture 主流程改造、无关脏改动清理

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHTANK-SINGLE-STEP-EXPORT-V1
- Task Title: Merge the PT CSV export and TXT staging flow into the main PT helper while keeping backward compatibility
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / malicious staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`; `docs/tasks/2026-03-27_phishtank_url_csv_to_txt.md`; `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`; `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`
- Created At: 2026-03-27
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

The repository now has two additive PT preprocessing helpers:

- `export_phishtank_verified_urls.py` filters `verified_online.csv` by `verification_time` and writes a URL-only CSV
- `convert_url_csv_to_txt.py` converts that CSV into a one-URL-per-line TXT for capture

The user asked to merge that flow into a single script and also asked for a concrete explanation of the current unrelated dirty worktree state.

---

## 2. Goal

Upgrade the main PT export helper so one execution produces both the URL-only CSV and the one-URL-per-line TXT needed for `run_malicious_capture.py --input_path`.

Keep the existing helper interfaces backward compatible where practical, keep the separate CSV-to-TXT helper as an additive fallback instead of deleting it, and update the runbook to show the new single-script PT path.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/malicious/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- additive main-helper behavior that also writes TXT
- additive runbook command updates for the new PT single-step path
- additive task / handoff documents

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not delete `convert_url_csv_to_txt.py`
- do not change `run_malicious_capture.py`
- do not clean unrelated dirty worktree changes
- do not rename existing output columns or CLI flags

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
- `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`
- `docs/tasks/2026-03-27_phishtank_url_csv_to_txt.md`
- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`
- `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`

### Code / Scripts

- `scripts/data/malicious/export_phishtank_verified_urls.py`
- `scripts/data/malicious/convert_url_csv_to_txt.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/common/io_utils.py`

### Data / Artifacts

- `C:\Users\20516\Downloads\verified_online.csv`
- current git worktree status output

### Prior Handoff

- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`
- `docs/handoff/2026-03-27_phishtank_url_csv_to_txt.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- an updated PT main export helper that also writes TXT
- updated runbook commands for the single-step PT path
- a repo handoff document
- a concise summary of unrelated dirty worktree changes in the final response

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

- One PT helper execution must write both a URL-only CSV and a TXT file.
- The TXT file must preserve URL row order and contain one URL per line.
- Existing `--output_csv` usage must remain valid.
- Do not delete the existing CSV-to-TXT helper in this task.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing PT helper required input format
- existing `run_malicious_capture.py` CLI
- existing URL-only CSV output with `url` header

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `url`, `verification_time`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current `export_phishtank_verified_urls.py --source_csv ... --output_csv ...`
  - current `convert_url_csv_to_txt.py --input_csv ... --output_txt ...`
  - current `run_malicious_capture.py --input_path ...`

Downstream consumers to watch:

- operators relying on the CSV artifact
- operators relying on TXT for direct capture

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current PT helper, converter helper, and runbook section.
2. Add TXT writing to the main PT helper with minimal interface expansion.
3. Update the runbook to prefer the single-step PT path while keeping the converter helper as an optional fallback.
4. Validate both CSV and TXT outputs from one PT helper run.
5. Write handoff and summarize unrelated dirty worktree categories.

Task-specific execution notes:

- Reuse `write_lines` from `io_utils.py`.
- Do not broaden scope into worktree cleanup.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] The main PT helper now writes both CSV and TXT from one run
- [ ] The runbook shows the single-step PT export command plus capture command
- [ ] The final response explains the unrelated dirty worktree changes concretely

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] the updated PT helper passes syntax validation
- [ ] one PT helper run produces both CSV and TXT outputs
- [ ] the CSV still contains the `url` header
- [ ] the TXT contains one URL per line

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py
python subprocess wrapper invoking E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py with stdin "2026/3/27\n", output CSV E:\Warden\tmp\pt_merged_validation_urls.csv, and output TXT E:\Warden\tmp\pt_merged_validation_urls.txt
```

Expected evidence to capture:

- logged CSV output path
- logged TXT output path
- inspected first CSV rows and first TXT rows
