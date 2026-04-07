# 2026-03-28_plan_a_batch_capture_day5_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-28` Plan A Day 5 抓取队列的任务定义。
- 若涉及精确批次规模、输出根目录、命令参数或日间边界，以英文版为准。

## 1. 背景

用户要求先把 Day 5 的任务冻结下来，之后再一次性交接 Day 1 到 Day 5 的实际运行结果。
当前有效规划事实是：

- 公共 PhishTank 的实际有效 malicious yield 仍只有大约 `5%` 到 `10%`
- Day 4 已经把 malicious 日量从 `4` 批提升到了 `8` 批
- 原始 Tranco 分片不够用，已经新增了一轮 supplemental Tranco 分片

因此 Day 5 不应把 malicious 日量降回去，同时 benign 应开始使用新的 supplemental 高 rank 分片。

## 2. 目标

提前冻结 `2026-03-28` Day 5 的 malicious / benign 抓取队列，使 Day 5 能继续沿用当前 skip-capable 与 hardening 默认命令，并在 benign 侧正式切入 supplemental Tranco 分片。

## 3. 范围

- 纳入：Day 5 队列任务定义与对应 handoff
- 排除：Day 1 到 Day 4 实际结果补录、capture 代码逻辑、malicious/benign 策略重设计

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY5-V1
- Task Title: Freeze the 2026-03-28 Plan A Day 5 queue with sustained doubled malicious volume and the first supplemental Tranco benign pair
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`; `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`; `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`; `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- Created At: 2026-03-27
- Requested By: user

---

## 1. Background

The user requested that Day 5 should be prepared now and said the full Day 1 to Day 5 returned artifacts will be handed back later in one package.
That means the next daily queue still needs to be frozen in advance instead of waiting for every prior run-result handoff to land first.

The current planning facts that now matter are:

- PhishTank practical effective malicious yield has been reported at only around `5%` to `10%`,
- Day 4 already doubled malicious daily volume from `4` batches to `8`,
- the original repository-local Tranco split was no longer enough, and a supplemental Tranco split tranche was added on 2026-03-26.

Because the malicious bottleneck still exists, Day 5 should keep the doubled malicious daily volume.
Because the original high-rank `top_1_10000` pair was exhausted by the earlier queue design, Day 5 should start consuming the first high-rank supplemental Tranco pair instead of waiting until the original Tranco artifacts are fully depleted.

---

## 2. Goal

Create an execution-ready task definition for the 2026-03-28 Plan A Day 5 queue.
This task should explicitly freeze which malicious and benign batches belong to Day 5, which output roots they should use, and which supervised commands should be treated as the recommended default commands for that day.

The intended 2026-03-28 Day 5 queue is:

- malicious: `phishtank_2026_only_batch_0021` to `phishtank_2026_only_batch_0028` inclusive
- benign:
  - `tranco_top_1_10000_batch_0003`
  - `tranco_top_10001_100000_batch_0008`

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- current Plan A execution-prep docs

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 5
- operator command examples for Day 5

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite historical Day 1 to Day 4 artifacts as if they belonged to Day 5
- do not change capture code or runner behavior
- do not rename frozen sample files, schema fields, or CLI flags
- do not pretend the 2026-03-28 queue has already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`
- `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`
- `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `phishtank csv/phishtank_2026_only_batch_0021_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0022_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0023_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0024_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0025_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0026_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0027_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0028_urls.txt`
- `tranco csv/tranco_top_1_10000_batch_0003_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0008_urls.txt`

### Prior Handoff

- `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`

### Missing Inputs

- actual returned artifacts from the user’s Day 1 to Day 4 queues are not available yet and must not be fabricated

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-03-28 Day 5 queue
- a repo prep/handoff doc with exact commands and output roots for Day 5

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

- Keep Day 1 to Day 4 queue artifacts frozen as historical context.
- Use new output roots for the 2026-03-28 queue so lineage remains auditable.
- Use the current supervised skip-capable commands as the recommended default commands for Day 5.
- Keep malicious Day 5 at the doubled 8-batch daily volume because no newer evidence yet justifies shrinking it back.
- Start consuming the supplemental Tranco split for the Day 5 benign high-rank pair.

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

1. Keep the Day 1 to Day 4 prep docs as frozen context only.
2. Create a new 2026-03-28 task boundary for Day 5.
3. Freeze the 8-batch malicious queue and the 2-batch benign queue for Day 5.
4. Freeze exact supervised commands and output roots for Day 5.
5. Hand back the new prep doc for operator execution and later artifact return.

Task-specific execution notes:

- malicious Day 5 starts from `batch_0021` and continues through `batch_0028`
- benign Day 5 returns to the higher-rank pair and starts using the new supplemental Tranco tranche
- both lanes should use supervised skip-capable commands by default

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-03-28 Day 5 queue has its own repo task doc
- [ ] the doc freezes malicious `batch_0021` to `batch_0028`
- [ ] the doc freezes benign `top_1_10000_batch_0003` and `top_10001_100000_batch_0008`
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

- confirmed input filenames for the Day 5 queue
- exact output roots for the Day 5 queue
- exact supervised commands for the Day 5 queue
