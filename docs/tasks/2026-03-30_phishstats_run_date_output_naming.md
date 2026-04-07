# 2026-03-30_phishstats_run_date_output_naming

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PhishStats 输出命名收口任务单。
- 若涉及精确文件名模式、CLI 兼容性、验证命令或风险判断，以英文版为准。

## 1. 背景

上一轮已把 PhishStats 脚本改成“默认抓昨天的完整一天”，但输出文件名仍然按目标抓取日命名。用户进一步要求把产物命名固定下来，日期按脚本运行当天计算，而不是按目标抓取日计算。

## 2. 目标

把两份 repo 内 PhishStats 脚本的 TXT 产物命名改成“按运行当天日期命名”，同时保留单日抓取逻辑和 TXT 输出结构。

## 3. 范围

- 纳入：两份脚本副本、task、handoff
- 排除：抓取逻辑重写、输出目录变更、JSON/CSV 新产物、429 退避机制改造

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHSTATS-RUN-DATE-OUTPUT-NAMING-V1
- Task Title: Change PhishStats TXT artifact naming to use the script run date instead of the fetched target date
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data / External Feed Utility
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `E:\Warden\fetch_phishstats_urls.py`; `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`; `E:\Warden\docs\tasks\2026-03-30_phishstats_previous_day_fetch.md`; `E:\Warden\docs\handoff\2026-03-30_phishstats_previous_day_fetch.md`
- Created At: 2026-03-30
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

The previous PhishStats change already converted the fetcher into a one-day utility that defaults to yesterday.
However, the TXT file naming still reflects the fetched target date.

The user explicitly requested a tighter artifact convention:

- keep fetching the previous complete day by default
- keep TXT outputs
- name the artifacts using the script run date, not the fetched target date

Example:

- on `2026-03-30`, the script fetches the complete day `2026-03-29`
- but the generated TXT filenames should carry `20260330`

---

## 2. Goal

Update both repository-local PhishStats script copies so their TXT artifact names are based on the local script run date.

The script must continue to fetch one complete target day only, continue to output TXT files split by score bands, and keep the rest of the fetch logic unchanged.

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\fetch_phishstats_urls.py`
- `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`
- `E:\Warden\docs\tasks\2026-03-30_phishstats_run_date_output_naming.md`
- `E:\Warden\docs\handoff\2026-03-30_phishstats_run_date_output_naming.md`

This task is allowed to change:

- TXT artifact naming logic
- terminal summary text that explains the output naming date
- documentation needed to record the naming change

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not change the target-day selection behavior added in the prior task
- do not change the output directory default
- do not add new dependencies
- do not redesign pagination, provider interaction, or retry logic

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `E:\Warden\docs\tasks\2026-03-30_phishstats_previous_day_fetch.md`
- `E:\Warden\docs\handoff\2026-03-30_phishstats_previous_day_fetch.md`

### Code / Scripts

- `E:\Warden\fetch_phishstats_urls.py`
- `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`

### Data / Artifacts

- none

### Prior Handoff

- `E:\Warden\docs\handoff\2026-03-30_phishstats_previous_day_fetch.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated root PhishStats fetch script with run-date-based TXT naming
- updated repo mirror PhishStats fetch script with the same naming logic
- repo task document for this naming change
- repo handoff document for this naming change

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

- The fetched target day must remain unchanged from the previous task.
- TXT contents must remain one URL per line.
- Only the artifact naming basis changes: fetched target date -> script run date.
- The terminal summary must make both dates explicit to reduce operator confusion.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `--target-date` and `--start-date` CLI behavior
- TXT line-based output content
- dependency-free runtime

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\fetch_phishstats_urls.py`
  - `python E:\Warden\fetch_phishstats_urls.py --target-date 2026/03/29`
  - `python E:\Warden\fetch_phishstats_urls.py --output-dir E:\Warden\phishstats`

Downstream consumers to watch:

- any manual operator expecting filenames based on fetched target date
- any local scripts that glob these TXT files by name pattern

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current output naming logic in both script copies.
2. Replace fetched-date-based filename tokens with run-date-based tokens.
3. Update the terminal summary to print both the fetched target date and the artifact naming date.
4. Run syntax and small helper-level naming checks.
5. Write task and handoff docs.

Task-specific execution notes:

- Keep the file name prefix stable.
- Reduce ambiguity by not overloading the printed target date as the output naming date.

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
- [ ] Output filenames now use the script run date
- [ ] Terminal summary shows both the target date and the naming date
- [ ] TXT line format remains unchanged

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] output naming helper spot-check
- [ ] summary-path logic spot-check

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\fetch_phishstats_urls.py
python -m py_compile E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py
```

Expected evidence to capture:

- `build_output_paths(..., date(2026, 3, 30))` produces filenames ending in `20260330.txt`
- both script copies stay aligned

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

- `E:\Warden\docs\handoff\2026-03-30_phishstats_run_date_output_naming.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
