# 2026-03-27_phishstats_task_handoff_compliance_repair

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 PhishStats task / handoff 合规修复的任务定义。
- 若涉及精确路径、状态字段、验证表述或修复边界，以英文版为准。

## 1. 背景

仓库里已经有 `2026-03-27_phishstats_url_fetch_task.md` 与 `2026-03-27_phishstats_url_fetch_handoff.md` 两份文档，但前一轮审查确认它们存在合规问题：任务边界中的脚本路径与缺失输入表述互相冲突，handoff 仍把仓库外草稿状态写成 `DONE` 交付。

## 2. 目标

在不修改抓取脚本逻辑的前提下，修复这两份文档的路径、状态、验证和仓库内落盘表述，使其与当前仓库真实状态一致并满足 Warden 模板要求。

## 3. 范围

- 纳入：PhishStats task / handoff 文档修复、对应修复 handoff
- 排除：脚本功能修改、抓取策略重写、额外模块文档扩写

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHSTATS-TASK-HANDOFF-COMPLIANCE-REPAIR-V1
- Task Title: Repair the repo-local PhishStats task and handoff so they match current repo state and Warden template expectations
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data / External Feed Utility docs
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-27_phishstats_url_fetch_task.md`; `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`
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

The repository now contains repo-local copies of:

- `docs/tasks/2026-03-27_phishstats_url_fetch_task.md`
- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`
- `scripts/data/malicious/fetch_phishstats_urls.py`

A review found that the task and handoff still reflect an external-draft state rather than the current repository state.
Specifically:

- the task doc lists a target script path that conflicts with its own missing-input note
- the handoff marks the work as `DONE` while still describing the artifacts as external `/mnt/data` drafts
- the handoff validation section does not include the later repo-local sandbox fetch result

These are documentation-contract issues, not script-logic issues.

---

## 2. Goal

Repair the repo-local PhishStats task and handoff so they accurately describe the current repository paths, current delivery state, and current validation facts, while keeping scope strictly limited to documentation consistency and compliance.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-03-27_phishstats_url_fetch_task.md`
- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`
- `docs/tasks/2026-03-27_phishstats_task_handoff_compliance_repair.md`
- `docs/handoff/2026-03-27_phishstats_task_handoff_compliance_repair.md`

This task is allowed to change:

- repo path references
- status and validation wording
- explicit compatibility / docs-impact wording

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not modify `scripts/data/malicious/fetch_phishstats_urls.py`
- do not redesign the PhishStats fetch strategy
- do not add dependencies
- do not broaden into unrelated worktree cleanup

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-27_phishstats_url_fetch_task.md`
- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`

### Code / Scripts

- `scripts/data/malicious/fetch_phishstats_urls.py`

### Data / Artifacts

- sandbox output under `tmp/phishstats_sandbox_test/`

### Prior Handoff

- `docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a corrected repo-local PhishStats task doc
- a corrected repo-local PhishStats handoff doc
- a repair handoff for this compliance-fix task

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

- Keep the repair limited to documentation truthfulness and compliance.
- Align paths with the repo-local copies actually used in this thread.
- Do not claim validations that were not run in this environment.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/malicious/fetch_phishstats_urls.py` CLI
- existing Warden schema
- existing Warden capture CLI

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/malicious/fetch_phishstats_urls.py --start-date ...`

Downstream consumers to watch:

- later operator use of the PhishStats task/handoff docs

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the repo-local task and handoff.
2. Patch path, status, and validation wording to match current facts.
3. Re-check the final text against the templates.
4. Write a repair handoff.

Task-specific execution notes:

- Prefer correcting contradictory wording over rewriting the whole documents.
- Record the sandbox fetch result factually.

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
- [ ] The repo-local task no longer contradicts itself about the target path
- [ ] The repo-local handoff no longer describes the artifacts as external drafts
- [ ] The repo-local handoff status and validation reflect current repo facts

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] inspect corrected task wording
- [ ] inspect corrected handoff wording
- [ ] verify the sandbox fetch result is reflected accurately

Commands to run if applicable:

```bash
inspect docs/tasks/2026-03-27_phishstats_url_fetch_task.md
inspect docs/handoff/2026-03-27_phishstats_url_fetch_handoff.md
inspect tmp/phishstats_sandbox_test/*
```

Expected evidence to capture:

- corrected repo path references
- corrected status / validation wording

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

- `docs/handoff/2026-03-27_phishstats_task_handoff_compliance_repair.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
