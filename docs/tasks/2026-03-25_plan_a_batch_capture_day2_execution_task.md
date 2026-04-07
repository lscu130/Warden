# 2026-03-25_plan_a_batch_capture_day2_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-25` Plan A Day 2 抓取队列的任务定义。
- 若涉及精确批次选择、输出根目录、CLI 参数或执行边界，以英文版为准。

## 1. 背景

此前名义上的 `2026-03-24 Day 1` 实际因为脚本加固延后到 `2026-03-25` 才完成，因此不能把当天新开的抓取队列继续混在旧任务里。
这份任务文档的作用，是把 `2026-03-25` 这一天的新恶意 / 良性抓取队列单独冻结下来，并明确沿用当前仓库内已经生效的 supervised skip 与加固默认值。

## 2. 目标

为 `2026-03-25` 这一天生成独立的执行边界，明确当天应该抓哪些 malicious / benign 批次、输出路径落到哪里、以及操作侧应该使用哪些当前有效的默认命令。

## 3. 范围

- 纳入：Day 2 队列任务定义与对应 handoff
- 排除：返回产物验收、旧 Day 1 队列重写、capture 核心逻辑改动

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY2-V1
- Task Title: Freeze the 2026-03-25 new-day malicious and benign capture queue after the delayed 2026-03-24 Day 1 run
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`; `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The prior Plan A Day 1 queue was originally dated 2026-03-24, but the user explicitly clarified that script hardening and stability work pushed its actual completion into 2026-03-25.
That means the previous execution-prep artifact should remain a frozen reference for the delayed Day 1 queue, while the newly started work on 2026-03-25 needs its own execution task boundary.

The current repo-effective operator rules are already different from the older Plan A docs:

- both benign and malicious can use supervised `skip`,
- benign shortfall is handled by expanding new batches rather than recovery-based second-pass recapture,
- malicious partial leftovers are deleted automatically in supervised mode,
- current hardening defaults are `commit`, `60000ms`, stealth, Google consent handling, and Chromium fallback.

The purpose of this task is to freeze the new-day queue for 2026-03-25 rather than silently extending the older 2026-03-24 task.

---

## 2. Goal

Create an execution-ready task definition for the new 2026-03-25 capture queue.
This task should explicitly freeze which malicious and benign batches belong to the new day, which output roots they should use, and which supervised commands are now the recommended default commands for today’s run.

The intended 2026-03-25 queue is:

- malicious: `batch_0005` to `batch_0008`
- benign: two new Tranco batches from buckets not used in the delayed Day 1 queue, namely:
  - `top_100001_500000_batch_0001`
  - `top_500001_1000000_batch_0001`

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- current Plan A execution-prep docs

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for the new day
- operator command examples for the new day

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite the historical 2026-03-24 Day 1 queue as if it belonged to 2026-03-25
- do not change capture code or runner behavior
- do not rename frozen sample files, schema fields, or CLI flags
- do not pretend the new 2026-03-25 batches have already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `phishtank csv/phishtank_2026_only_batch_0005_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0006_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0007_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0008_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0001_urls.txt`
- `tranco csv/tranco_top_500001_1000000_batch_0001_urls.txt`

### Prior Handoff

- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`

### Missing Inputs

- actual returned artifacts from the user’s 2026-03-25 queue are not available yet and must not be fabricated

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-03-25 new-day queue
- a repo prep/handoff doc with exact commands and output roots for today’s queue

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

- Keep the 2026-03-24 Day 1 queue frozen as historical context.
- Use new output roots for the 2026-03-25 queue so lineage remains auditable.
- Use the current supervised skip-capable commands as the recommended default commands for today’s queue.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py` CLI
- `scripts/data/malicious/run_malicious_capture.py` CLI
- current output-root naming discipline

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current benign runner commands
  - current malicious runner commands
  - current capture script commands

Downstream consumers to watch:

- operators resuming or auditing Plan A batch lineage
- later day-wise handoff writing

---

## 9. Suggested Execution Plan

Recommended order:

1. Keep the old Day 1 prep doc as frozen context only.
2. Create a new 2026-03-25 task boundary for the new day.
3. Freeze exact malicious and benign batch selections for today.
4. Freeze exact supervised commands and output roots for today.
5. Hand back the new-day prep doc for operator execution and later artifact return.

Task-specific execution notes:

- malicious today starts from `batch_0005`
- benign today starts from the next two not-yet-used rank buckets to widen coverage
- both lanes should use supervised skip-capable commands by default

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-03-25 new-day queue has its own repo task doc
- [ ] the doc freezes malicious `batch_0005` to `batch_0008`
- [ ] the doc freezes two new benign Tranco batches from different buckets
- [ ] the doc provides exact output roots and exact commands
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local batch filenames exist and match the doc
- [ ] referenced runner scripts still expose the required supervised flags

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
python scripts/data/malicious/run_malicious_capture.py --help
```

Expected evidence to capture:

- confirmed input filenames for the new-day queue
- exact output roots for the new-day queue
- exact supervised commands for the new-day queue
