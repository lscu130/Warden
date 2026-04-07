# 2026-04-01_cert_domains_2026_batch_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 CERT 域名 CSV 的时间切分与分批导出任务单。
- 若涉及精确列名、时间过滤规则、批次文件名或输出路径，以英文版为准。

## 1. 背景

用户提供了 `C:\Users\20516\Downloads\domains.csv`，要求按时间只保留 `2026` 年内的数据，再按每批 `500` 条切分，只保留 domain 并导出为 TXT，且批次名称必须带有 `CERT` 来表示来源。

## 2. 目标

把输入 CSV 中 `2026` 年内的域名筛出来，分成多个每批 `500` 行的 TXT 文件，输出到仓库内目录，并使用带 `CERT` 的批次命名。

## 3. 范围

- 纳入：输入 CSV 读取、时间过滤、TXT 批次导出、task、handoff
- 排除：抓取执行、CSV 列重命名、下游 capture、脚本长期产品化

## English Version

# Task Metadata

- Task ID: WARDEN-CERT-DOMAINS-2026-BATCH-SPLIT-V1
- Task Title: Filter the provided CERT domains CSV to 2026-only rows and split domains into 500-line TXT batches with CERT in the filenames
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data / External Feed Utility
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `C:\Users\20516\Downloads\domains.csv`
- Created At: 2026-04-01
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

The user provided `C:\Users\20516\Downloads\domains.csv`.
Its relevant columns are:

- `AdresDomeny` for the domain value
- `DataWpisu` for the timestamp

The user wants only rows inside calendar year `2026`, then wants the kept domains split into TXT batches of `500` lines each.
The batch filenames must clearly indicate the source via `CERT`.

---

## 2. Goal

Read the provided CSV, retain only rows whose `DataWpisu` falls in year `2026`, extract the `AdresDomeny` values, and write them into `500`-line TXT batches.

The output should be stored inside the repository in a directory dedicated to this source, and the filenames must include `CERT`.

---

## 3. Scope In

This task is allowed to touch:

- `C:\Users\20516\Downloads\domains.csv`
- `E:\Warden\cert csv\`
- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_batch_split.md`

This task is allowed to change:

- generated TXT batch artifacts
- task / handoff documentation that records the execution result

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not modify the source CSV
- do not add new Python dependencies
- do not run downstream crawling or capture
- do not rename source columns in the input file

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- none

### Data / Artifacts

- `C:\Users\20516\Downloads\domains.csv`

### Prior Handoff

- none

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a repo-local output directory for CERT batches
- TXT batch files containing only domains from 2026 rows
- a repo handoff document with counts and file paths

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

- Retain only calendar-year `2026` rows based on `DataWpisu`.
- Export only the `AdresDomeny` values.
- Each TXT batch must contain at most `500` domains.
- Filenames must include `CERT`.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- source CSV remains untouched
- TXT output is one domain per line

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `AdresDomeny`, `DataWpisu`

CLI / output compatibility constraints:

- none

Downstream consumers to watch:

- any later manual or scripted use of the generated TXT batches

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the CSV header and confirm the date/domain columns.
2. Filter to rows where `DataWpisu` falls in year `2026`.
3. Extract domains only.
4. Write `500`-line TXT batches into a repo-local CERT directory with `CERT` in each filename.
5. Validate the batch counts and line counts.
6. Record the result in a handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Only `2026` rows were kept
- [ ] Only domains were exported
- [ ] Each batch contains at most `500` lines
- [ ] Every batch filename includes `CERT`

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] input-header check
- [ ] filtered-row count check
- [ ] output batch file existence check
- [ ] per-file line count check

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_batch_split.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
