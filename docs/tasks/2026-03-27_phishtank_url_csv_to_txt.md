# 2026-03-27_phishtank_url_csv_to_txt

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PT URL-only CSV 转 TXT 辅助脚本的任务定义。
- 若涉及精确命令、输入输出结构、列名、兼容性或验证口径，以英文版为准。

## 1. 背景

仓库里已经新增了 PT `verified_online.csv` 按 `verification_time` 过滤并导出 URL-only CSV 的脚本。
但现有 `run_malicious_capture.py` 更直接的输入仍是一行一个 URL 的 TXT，因此用户要求再补一个衔接脚本，并把完整使用命令写入文档。

## 2. 目标

新增一个最小辅助脚本，把 URL-only CSV 转成一行一个 URL 的 TXT，供后续 `run_malicious_capture.py --input_path` 直接使用，并更新 runbook 与 handoff。

## 3. 范围

- 纳入：CSV 转 TXT 脚本、runbook 命令补充、task / handoff
- 排除：现有 PT 过滤逻辑重写、capture 主流程改造、schema 变更

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHTANK-URL-CSV-TO-TXT-V1
- Task Title: Add a minimal helper that converts the PT URL-only CSV export into a one-URL-per-line TXT for capture
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / malicious staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/tasks/2026-03-27_phishtank_verified_csv_filter.md`; `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`
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

The repository now has a PT-specific helper that filters `verified_online.csv` by `verification_time` and writes a URL-only CSV.
However, `run_malicious_capture.py` is still most directly driven by a one-URL-per-line TXT file.
The user requested a follow-up helper to bridge those two steps and asked for the full operator commands to be written down explicitly.

---

## 2. Goal

Add a minimal helper under `scripts/data/malicious/` that reads a URL-only CSV with a `url` header and writes a one-URL-per-line TXT file for `run_malicious_capture.py --input_path`.

Also update the ingest runbook so the full PT workflow is documented end to end: PT CSV filter export, CSV-to-TXT conversion, and capture command.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/malicious/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- additive CSV-to-TXT helper code
- additive runbook command examples
- additive task / handoff documents

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not change the existing PT filter script semantics
- do not change `run_malicious_capture.py` input handling
- do not add dependencies
- do not rename existing fields or files

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
- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`

### Code / Scripts

- `scripts/data/malicious/export_phishtank_verified_urls.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/common/io_utils.py`

### Data / Artifacts

- URL-only CSV outputs from the PT filter helper

### Prior Handoff

- `docs/handoff/2026-03-27_phishtank_verified_csv_filter.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a helper that converts a URL-only CSV into a one-URL-per-line TXT
- a runbook update with the full PT command chain
- a repo handoff document

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

- The helper must accept a CSV with a `url` column.
- The helper output must be a plain UTF-8 TXT file with one URL per line.
- Source row order must be preserved.
- The runbook must show the explicit three-step PT flow: export CSV, convert TXT, run capture.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing PT filter helper CLI
- existing `run_malicious_capture.py` CLI
- existing malicious capture outputs

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current PT filter export command
  - current malicious capture commands

Downstream consumers to watch:

- operator use of `run_malicious_capture.py --input_path`

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current PT helper and runbook section.
2. Add a minimal additive CSV-to-TXT helper.
3. Update the runbook with the full PT command chain.
4. Run minimal validation with a temporary CSV and inspect the TXT output.
5. Write handoff.

Task-specific execution notes:

- Reuse the existing `write_lines` helper instead of inventing a new file-writing path.
- Fail fast if the CSV does not contain `url`.

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
- [ ] The new helper writes one URL per line from a URL-only CSV
- [ ] The runbook includes the full PT workflow commands

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] the helper passes syntax validation
- [ ] a temporary URL-only CSV was converted successfully
- [ ] the TXT output preserves one URL per line
- [ ] the runbook examples were updated

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\malicious\convert_url_csv_to_txt.py --input_csv E:\Warden\tmp\pt_validation_urls.csv --output_txt E:\Warden\tmp\pt_validation_urls.txt
python -m py_compile E:\Warden\scripts\data\malicious\convert_url_csv_to_txt.py
```

Expected evidence to capture:

- printed selected row count from the helper
- inspected TXT output headerless one-URL-per-line format
