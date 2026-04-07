# 中文摘要

本任务用于为 Warden 提供一个最小、可审计、可复现的外部情报抓取脚本草案：从 PhishStats API 拉取自指定起始日期至当前日期区间内的 URL，并按 `score > 8` 与 `5 < score < 8` 两个风险段分别导出为纯文本 `txt` 文件。

本任务仅覆盖单个 Python 脚本与一个任务文档草案，不涉及仓库级 schema、训练逻辑、标签语义、推理主线或其他模块改造。由于官方公开文档明确给出了基础 API、分页、排序、字段与速率限制，但未展示按日期字段过滤的示例，因此本任务默认采用 **按 `date` 倒序分页 + 本地日期截断** 的保守实现，以避免基于未证实的服务端日期过滤语法做高风险假设。

英文版为权威版本。

---

# Task Metadata

- Task ID: TASK-2026-03-27-PHISHSTATS-URL-FETCH
- Task Title: Add a minimal PhishStats URL fetcher with score-band TXT export
- Owner Role: GPT Web / Task Drafter
- Priority: High
- Status: TODO
- Related Module: Data / External Feed Utility
- Related Issue / ADR / Doc: AGENTS.md; PROJECT.md; docs/workflow/GPT_CODEX_WORKFLOW.md; docs/templates/TASK_TEMPLATE.md; PhishStats API docs
- Created At: 2026-03-27
- Requested By: User

Use this template for any non-trivial engineering task in Warden.

---

## 1. Background

Warden is currently in a foundation and contract-freezing stage, where reproducible data tooling, explicit task boundaries, minimal patches, and auditability are prioritized over broad redesign. The user requested a concrete task document and a Python crawler script that pulls phishing URLs from the public PhishStats API and exports them into TXT files for downstream use. The requested behavior is bounded and operationally useful, but it changes CLI behavior and output artifacts, so it should be treated as non-trivial and frozen through a task document.

The current need is not a full ingestion pipeline redesign. The need is a small external-feed utility that:

1. accepts a start date at runtime;
2. fetches records from that start date through “today”;
3. splits URLs into two score bands;
4. writes plain-text TXT outputs;
5. remains simple, backward-compatible, dependency-light, and auditable.

Because the official public API documentation documents `_where`, `_sort`, `_p`, `_size`, `score`, `url`, and `date`, but does not provide a documented example for server-side date-range filtering on the `date` field, this task should implement descending pagination by `date` and perform date-range filtering locally in the script.

---

## 2. Goal

Produce one standalone Python script that fetches phishing records from the PhishStats public API, starting from a user-provided date in `YYYY/MM/DD` format and continuing up to the current day, then exports two TXT files: one containing URLs whose `score > 8`, and one containing URLs whose `5 < score < 8`. The script must preserve minimal operational complexity, avoid undocumented API assumptions where practical, and clearly report validation status, compatibility impact, and known limitations.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/malicious/fetch_phishstats_urls.py`
- `docs/tasks/2026-03-27_phishstats_url_fetch_task.md`
- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`

This task is allowed to change:

- add one new standalone Python utility script;
- define runtime input handling for start date and output directory;
- define TXT output artifact names and file-writing behavior for the two requested score bands.

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the Warden data pipeline, training logic, schema, labels, or inference routing;
- do not rename frozen fields, frozen files, or existing CLI interfaces elsewhere in the project;
- do not add third-party dependencies, database storage, async framework conversion, or service deployment logic.

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`

### Code / Scripts

- `scripts/data/malicious/fetch_phishstats_urls.py`
- `none`
- `none`

### Data / Artifacts

- PhishStats public API response JSON
- PhishStats API documentation
- PhishStats FAQ

### Prior Handoff

- `none`

### Missing Inputs

- `none`

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- one Python script that fetches and exports PhishStats URLs by date range and score band;
- one task document matching the Warden task-template structure;
- one handoff summary covering behavior impact, compatibility impact, validation, and known risks.

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

- Use the public PhishStats API endpoint and documented pagination / sorting behavior only.
- Treat `score` as an external confidence signal, not as manual gold truth.
- Implement date-range enforcement in script logic unless documented server-side date filtering is explicitly confirmed.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- no existing Warden CLI entrypoint may be modified by this task
- no existing dataset schema may be modified by this task
- no existing label schema may be modified by this task

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none
  - none
  - none

Downstream consumers to watch:

- future Warden data-ingestion helpers that may read the generated TXT files
- manual review or curation workflows that may consume one-URL-per-line output

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

- Fetch API pages sorted by descending `date`.
- Stop pagination once record dates are older than the requested start date and the page is fully outside the target range.
- Export one URL per line in two TXT files, with deterministic naming based on the requested start date and current date.

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
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] The script accepts a start date in `YYYY/MM/DD` format.
- [ ] The script exports two TXT files for `score > 8` and `5 < score < 8`.
- [ ] The script filters records to the inclusive range from the provided start date through the current day.

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile scripts/data/malicious/fetch_phishstats_urls.py
python scripts/data/malicious/fetch_phishstats_urls.py --start-date 2026/03/25 --output-dir ./tmp_phishstats
ls ./tmp_phishstats
```

Expected evidence to capture:

- script compiles without syntax error
- expected TXT files are created with one URL per line when the API is reachable

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

- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- exact upstream `date` string format is not documented in the public API examples, so the script must keep date parsing tolerant
