# 2026-03-27_plan_a_batch_capture_day4_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-27` Plan A Day 4 抓取队列的任务定义。
- 若涉及精确批次规模、输出根目录、命令默认值或操作边界，以英文版为准。

## 1. 背景

用户明确反馈 Day 1 到 Day 3 的 PhishTank 实际有效恶意产出只有约 `5%` 到 `10%`，显著低于早先较乐观的估计。
当前瓶颈已经转向 malicious train-eligible volume，而不是 benign 批次是否够用，因此 Day 4 需要把 malicious 日抓取量翻倍，并单独冻结成新一天的计划边界。

## 2. 目标

为 `2026-03-27` Day 4 队列明确一份独立任务定义：保持 benign 双批次不变，但把 malicious 当日抓取量加倍，并继续沿用当前 skip-capable 与 hardening 默认命令。

## 3. 范围

- 纳入：Day 4 队列任务定义与对应 handoff
- 排除：前几天实际结果改写、capture 核心逻辑变更、benign 策略重设计

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY4-V1
- Task Title: Freeze the 2026-03-27 Plan A Day 4 queue with doubled malicious capture volume due to low effective public-feed yield
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`; `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- Created At: 2026-03-26
- Requested By: user

---

## 1. Background

The user explicitly reported that the practical effective malicious yield from PhishTank across Day 1 to Day 3 is only around `5%` to `10%`.
That is materially lower than the earlier optimistic planning assumption and is still consistent with public-feed churn and early-2026 site decay.

Because the current bottleneck is malicious train-eligible volume rather than benign batch availability, the user explicitly requested that Day 4 should double the malicious capture amount.
The Day 4 queue therefore needs a new frozen planning boundary rather than silently reusing the Day 3 daily volume assumption.

The current repo-effective operator rules remain:

- both benign and malicious use supervised skip-capable runners,
- benign shortfall is handled by expanding fresh Tranco batches instead of recovery-based second-pass recapture,
- malicious partial leftovers are deleted automatically in supervised mode,
- the current hardened defaults remain `commit`, `60000ms`, stealth, Google consent handling, and Chromium fallback.

---

## 2. Goal

Create an execution-ready task definition for the 2026-03-27 Plan A Day 4 queue.
This task should explicitly freeze which malicious and benign batches belong to Day 4, which output roots they should use, and which supervised commands should be treated as the recommended default commands for that day.

The intended 2026-03-27 Day 4 queue is:

- malicious: `phishtank_2026_only_batch_0013` to `phishtank_2026_only_batch_0020` inclusive
- benign:
  - `tranco_top_100001_500000_batch_0002`
  - `tranco_top_500001_1000000_batch_0002`

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- current Plan A execution-prep docs

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 4
- operator command examples for Day 4

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite historical Day 1 to Day 3 artifacts as if they belonged to Day 4
- do not change capture code or runner behavior
- do not rename frozen sample files, schema fields, or CLI flags
- do not pretend the 2026-03-27 queue has already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`
- `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `phishtank csv/phishtank_2026_only_batch_0013_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0014_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0015_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0016_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0017_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0018_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0019_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0020_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0002_urls.txt`
- `tranco csv/tranco_top_500001_1000000_batch_0002_urls.txt`

### Prior Handoff

- `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`

### Missing Inputs

- actual returned artifacts from the user’s Day 2 and Day 3 queues are not available yet and must not be fabricated

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-03-27 Day 4 queue
- a repo prep/handoff doc with exact commands and output roots for Day 4

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

- Keep Day 1 to Day 3 queue artifacts frozen as historical context.
- Use new output roots for the 2026-03-27 queue so lineage remains auditable.
- Use the current supervised skip-capable commands as the recommended default commands for Day 4.
- Double malicious Day 4 batch volume from the prior 4-batch daily default to 8 batches because the user-reported practical effective yield is only around `5%` to `10%`.

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

1. Keep the Day 1 to Day 3 prep docs as frozen context only.
2. Create a new 2026-03-27 task boundary for Day 4.
3. Freeze the 8-batch malicious queue and the 2-batch benign queue for Day 4.
4. Freeze exact supervised commands and output roots for Day 4.
5. Hand back the new prep doc for operator execution and later artifact return.

Task-specific execution notes:

- malicious Day 4 starts from `batch_0013` and continues through `batch_0020`
- benign Day 4 uses the second batch from the two lower-rank buckets so the cross-bucket schedule remains balanced
- both lanes should use supervised skip-capable commands by default

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-03-27 Day 4 queue has its own repo task doc
- [ ] the doc freezes malicious `batch_0013` to `batch_0020`
- [ ] the doc freezes benign `top_100001_500000_batch_0002` and `top_500001_1000000_batch_0002`
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

- confirmed input filenames for the Day 4 queue
- exact output roots for the Day 4 queue
- exact supervised commands for the Day 4 queue
