# 2026-03-27_phishtank_verified_csv_filter

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PT `verified_online.csv` 日期筛选脚本的任务定义。
- 若涉及精确输入列名、日期边界、输出 CSV 结构、CLI 路径或验证结论，以英文版为准。

## 1. 背景

当前仓库已有 `OpenPhish` / `PhishTank` feed ingest 与 malicious capture 流程，但它默认围绕 feed 或普通本地 CSV ingest。
用户当前的实际需求更窄：针对 `verified_online.csv` 这类 PT 导出文件，按 `verification_time` 做日期截断，快速导出一份仅含 `url` 列的 CSV，供后续单独抓取使用。

## 2. 目标

新增一个 PT 专用辅助脚本，在运行时先提示输入类似 `2026/3/27` 的日期，然后从 `verified_online.csv` 中筛出 `verification_time` 在该日期及之后的记录，输出一份仅包含 `url` 列的 CSV，并补充最小必要文档与 handoff。

## 3. 范围

- 纳入：PT CSV 过滤导出脚本、对应 runbook 文档补充、task / handoff
- 排除：现有 malicious capture 主流程重写、schema 改名、训练或推理模块修改

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHTANK-VERIFIED-CSV-FILTER-V1
- Task Title: Add a PT-specific verified_online CSV date filter that exports a URL-only CSV for later capture
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / malicious staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
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

The repository already contains malicious feed ingest and malicious capture scripts, but those workflows are centered on public feed ingest or generic local ingest.
The user requested a narrower PT-specific helper for `verified_online.csv`-style inputs: prompt for a date, filter rows by the PT confirmation timestamp, and export a URL-only CSV that can be consumed by later capture steps.

The provided example file `C:\Users\20516\Downloads\verified_online.csv` contains at least these relevant columns:

- `url`
- `verification_time`

The sample timestamps are ISO 8601 timestamps with explicit UTC offset such as `2026-03-27T07:03:16+00:00`.

---

## 2. Goal

Add a PT-specific helper script under `scripts/data/malicious/` that prompts the operator for a start date in `YYYY/M/D` style, filters `verified_online.csv` rows whose `verification_time` falls on or after that UTC calendar date, and writes an additive CSV containing only one header column: `url`.

Also update the data-ingest runbook minimally so the new helper has an auditable usage path, and produce the required handoff.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/malicious/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- additive PT-specific CSV preprocessing helper code
- additive operator documentation for the new helper
- additive task / handoff documents

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not change existing `run_malicious_capture.py` behavior
- do not redesign the existing public feed ingest flow
- do not rename any existing schema fields or CLI flags
- do not add third-party dependencies

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

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

- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/common/io_utils.py`

### Data / Artifacts

- `C:\Users\20516\Downloads\verified_online.csv`
- existing PT / OpenPhish local workflow examples under `E:\Warden\phishtank csv\`

### Prior Handoff

- none

### Missing Inputs

- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- a PT-specific CSV filter/export script
- a minimal runbook update documenting the new helper
- a repo handoff document

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

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

- The date prompt must accept operator input in `YYYY/M/D` style such as `2026/3/27`.
- Filtering must use the PT `verification_time` column and include the selected day itself.
- The exported CSV must contain only the `url` header and URL rows.
- Interpret the date boundary against the source timestamp's UTC calendar date rather than silently converting to another timezone.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing `ingest_public_malicious_feeds.py` CLI
- existing `run_malicious_capture.py` CLI
- existing malicious capture output structure

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current public malicious feed ingest commands
  - current malicious capture commands
  - current local TXT / manifest capture workflows

Downstream consumers to watch:

- operators preparing PT URL batches for malicious capture
- later `run_malicious_capture.py --input_path` usage against exported URL lists

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- Read the example `verified_online.csv` header before coding.
- Preserve source row order rather than inventing new sort behavior.
- Validate by running the new script against the provided CSV with a piped interactive date input.

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
- [ ] A PT-specific helper script prompts for `YYYY/M/D` input and accepts `2026/3/27` style input
- [ ] The script filters by `verification_time` inclusively from the chosen day to the latest row in the file
- [ ] The exported CSV contains only the `url` column

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] source CSV header was inspected successfully
- [ ] the new script runs against the provided sample CSV
- [ ] the output CSV has only one header column: `url`
- [ ] the script passes syntax validation

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py --source_csv "C:\Users\20516\Downloads\verified_online.csv" --output_csv E:\Warden\data\processed\pt_csv_exports\validation_verified_online_since_2026-03-27_urls.csv
python -m py_compile E:\Warden\scripts\data\malicious\export_phishtank_verified_urls.py
```

Expected evidence to capture:

- operator prompt accepts `2026/3/27`
- output CSV header equals `url`
- selected row count is printed by the script
