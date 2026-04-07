# 2026-04-01_cert_domains_2026_03_only_batch_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 CERT 域名 CSV 缩窄到 `2026-03` 月份的重新分批任务单。
- 若涉及精确时间边界、批次文件名或输出路径，以英文版为准。

## 1. 背景

前一轮已经生成了 `2026-02-01` 起的 CERT 批次，但用户还想继续缩小范围，只保留 `2026-03` 月份的数据。

## 2. 目标

从 `C:\Users\20516\Downloads\domains.csv` 中仅保留 `2026-03-01 00:00:00+00:00` 到 `2026-04-01 00:00:00+00:00` 之前的数据，只导出域名列，并按 `500` 一批生成新的 CERT TXT 批次。

## 3. 范围

- 纳入：输入 CSV 读取、时间过滤、TXT 批次导出、task、handoff
- 排除：旧批次删除、源 CSV 改写、抓取执行、脚本产品化

## English Version

# Task Metadata

- Task ID: WARDEN-CERT-DOMAINS-2026-03-ONLY-BATCH-SPLIT-V1
- Task Title: Filter the provided CERT domains CSV to March 2026 only and split domains into 500-line TXT batches
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data / External Feed Utility
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `C:\Users\20516\Downloads\domains.csv`; `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_02_01_to_2026_04_01_batch_split.md`
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

The earlier narrowed CERT export kept rows from `2026-02-01` onward.
The user now wants a tighter window: March 2026 only.

This request is interpreted using explicit UTC timestamp boundaries from the CSV field values:

- inclusive lower bound: `2026-03-01T00:00:00+00:00`
- exclusive upper bound: `2026-04-01T00:00:00+00:00`

The new March-only batch set should be generated separately so the earlier broader exports remain available.

---

## 2. Goal

Generate a new CERT batch set from `C:\Users\20516\Downloads\domains.csv` that includes only rows whose `DataWpisu` is in March 2026.

Extract only `AdresDomeny`, write one domain per line, split into batches of `500`, and keep the new outputs separate from the earlier broader CERT exports.

---

## 3. Scope In

This task is allowed to touch:

- `C:\Users\20516\Downloads\domains.csv`
- `E:\Warden\cert csv\`
- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_03_only_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_03_only_batch_split.md`

This task is allowed to change:

- generated March-only TXT batch artifacts
- task / handoff documentation recording the March-only export

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not delete the earlier `CERT_2026_only_...` or `CERT_2026_02_01_to_2026_04_01_...` batch files
- do not modify the source CSV
- do not add new dependencies
- do not run downstream crawling or capture

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_02_01_to_2026_04_01_batch_split.md`

### Code / Scripts

- none

### Data / Artifacts

- `C:\Users\20516\Downloads\domains.csv`

### Prior Handoff

- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_02_01_to_2026_04_01_batch_split.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a March-2026-only CERT batch set under `E:\Warden\cert csv\`
- a repo handoff document with counts and file paths for the March-only export

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

- Lower bound is inclusive: `2026-03-01T00:00:00+00:00`
- Upper bound is exclusive: `2026-04-01T00:00:00+00:00`
- Retain only `AdresDomeny`
- Each batch must contain at most `500` lines
- Filenames must include `CERT`
- New March-only outputs must not overwrite the prior broader export sets

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- source CSV remains untouched
- TXT output remains one domain per line

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `AdresDomeny`, `DataWpisu`

CLI / output compatibility constraints:

- none

Downstream consumers to watch:

- later manual or scripted use of multiple CERT batch sets with different time windows

---

## 9. Suggested Execution Plan

Recommended order:

1. Count rows whose `DataWpisu` falls within March 2026.
2. Generate a separate March-only batch set under `E:\Warden\cert csv\`.
3. Validate batch count and line-count limits.
4. Record the result in a handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Only rows in March 2026 were kept
- [ ] Only domains were exported
- [ ] Each batch contains at most `500` lines
- [ ] Filenames include `CERT`
- [ ] Earlier broader CERT artifacts were not deleted

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] March-only count check
- [ ] output batch file existence check
- [ ] per-file line count check

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_03_only_batch_split.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
