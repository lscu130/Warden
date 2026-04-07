# 2026-03-30_phishstats_previous_day_fetch

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PhishStats 脚本改为“只抓完整前一日”的任务定义。
- 若涉及精确 CLI、默认日期行为、镜像脚本路径或验证口径，以英文版为准。

## 1. 背景

当前 `fetch_phishstats_urls.py` 仍按“起始日期到今天”抓取，会把未完整的当天混进目标时间窗，也不适合稳定日跑。用户明确要求按天抓取，并且默认抓“前一完整自然日”，例如 `2026-03-30` 运行时抓完整的 `2026-03-29`。

## 2. 目标

把当前 PhishStats 抓取脚本改成单日抓取模式：默认抓昨天，显式给日期时也只抓那一天，并继续输出 TXT。

## 3. 范围

- 纳入：root 脚本、repo 镜像脚本、task / handoff
- 排除：PhishStats API 逻辑重写、CSV/JSONL 新输出、runbook 大扩写

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHSTATS-PREVIOUS-DAY-FETCH-V1
- Task Title: Change the PhishStats fetch script to fetch one complete day only, defaulting to yesterday
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data / External Feed Utility
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `fetch_phishstats_urls.py`; `scripts/data/malicious/fetch_phishstats_urls.py`
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

The current `fetch_phishstats_urls.py` behavior still treats the fetch window as `start_date -> today`.
That is awkward for steady daily operation because it includes the current day, which is not yet complete, and it is broader than the user now wants.

The user explicitly requested a daily single-day mode:

- on `2026-03-30`, fetch the full day `2026-03-29`
- keep TXT outputs
- treat the script as a one-day fetcher rather than a growing-range fetcher

There are currently two repository-local copies of the script:

- `E:\Warden\fetch_phishstats_urls.py`
- `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`

This task keeps them aligned to avoid drift.

---

## 2. Goal

Update both repository-local copies of the PhishStats fetch script so they fetch exactly one full calendar day.
If no date is provided, the script should default to yesterday.
If a date is provided, the script should fetch only that date and reject today or future dates because they are not complete days.

The script should keep TXT output behavior and remain dependency-free.

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\fetch_phishstats_urls.py`
- `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`
- `E:\Warden\docs\tasks\2026-03-30_phishstats_previous_day_fetch.md`
- `E:\Warden\docs\handoff\2026-03-30_phishstats_previous_day_fetch.md`

This task is allowed to change:

- default date-window behavior
- date-related CLI parsing and help text
- in-file comments / docstrings that describe the fetch window

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not add third-party dependencies
- do not redesign the pagination / sorting logic
- do not add CSV / JSONL outputs
- do not change unrelated Warden scripts

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- `E:\Warden\fetch_phishstats_urls.py`
- `E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py`

### Data / Artifacts

- none

### Prior Handoff

- `none`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated root PhishStats fetch script
- updated repo mirror PhishStats fetch script
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

- Default behavior must fetch yesterday only.
- Explicit date input must fetch only that exact day.
- The script must reject today and future dates as incomplete / invalid targets.
- TXT outputs must be preserved.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- output TXT format
- PhishStats API usage pattern
- dependency-free runtime

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python fetch_phishstats_urls.py --output-dir ...`
  - `python fetch_phishstats_urls.py --max-pages 1`

Downstream consumers to watch:

- manual TXT review workflows
- later daily physical-machine fetch runs

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current script copies.
2. Replace the start-date-through-today behavior with exact-single-day behavior.
3. Keep the two script copies aligned.
4. Run syntax and small date-behavior checks.
5. Prepare handoff.

Task-specific execution notes:

- Prefer a small helper that resolves the target day cleanly.
- Keep the old `--start-date` flag as a tolerated alias only if needed for compatibility.

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
- [ ] Default run targets yesterday only
- [ ] Explicit date input targets exactly one day only
- [ ] TXT outputs are preserved

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] date-target resolution check
- [ ] output naming spot-check

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\fetch_phishstats_urls.py
python -m py_compile E:\Warden\scripts\data\malicious\fetch_phishstats_urls.py
```

Expected evidence to capture:

- default mode resolves to yesterday
- explicit target date rejects today / future and sets start=end=target

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

- `E:\Warden\docs\handoff\2026-03-30_phishstats_previous_day_fetch.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
