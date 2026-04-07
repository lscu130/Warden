# 2026-03-26_plan_a_batch_capture_day3_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-03-26` Plan A Day 3 抓取队列的任务定义。
- 若涉及精确批次、输出根目录、命令参数或日间边界，以英文版为准。

## 1. 背景

用户要求在 Day 2 返回产物 handoff 还没补回来的情况下，先把下一天的队列冻结下来，避免执行边界继续漂移。
当前有效操作规则仍然是 supervised skip、benign 不足靠新 Tranco 批次扩充、malicious partial leftovers 自动删、硬化默认值维持 `commit` / `60000ms` / stealth / Google consent / Chromium fallback。

## 2. 目标

提前冻结 `2026-03-26` Day 3 的 malicious / benign 抓取队列，并明确 benign 桶位继续遵守当前配额策略，不因 Day 2 的进行中状态而临时乱改下一天的批次选择。

## 3. 范围

- 纳入：Day 3 队列任务定义与对应 handoff
- 排除：Day 2 实际结果补录、capture 代码逻辑、配额策略重写

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY3-V1
- Task Title: Freeze the 2026-03-26 Plan A Day 3 malicious and benign capture queue before the pending Day 2 artifact handoff
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`; `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The user explicitly requested that the next-day queue should be prepared now, before the returned Day 2 artifacts are handed back later in the same thread.
That means the Day 3 capture boundary must be frozen as a forward execution-prep artifact rather than waiting for the full Day 2 result handoff.

Current repo-effective operator rules remain:

- both benign and malicious use supervised skip-capable runners,
- benign shortfall is handled by expanding fresh Tranco batches instead of recovery-based second-pass recapture,
- malicious partial leftovers are deleted automatically in supervised mode,
- the current hardened defaults remain `commit`, `60000ms`, stealth, Google consent handling, and Chromium fallback.

The benign bucket choice for Day 3 should also stay aligned with the current documented quota strategy in `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`.
Because Day 1 already consumed the first high-rank pair and Day 2 widened coverage into the two lower-rank buckets, the next benign pair should return to the second batch of the higher-rank buckets instead of over-shifting toward the lower-rank side too early.

---

## 2. Goal

Create an execution-ready task definition for the 2026-03-26 Plan A Day 3 queue.
This task should explicitly freeze which malicious and benign batches belong to Day 3, which output roots they should use, and which supervised commands should be treated as the recommended default commands for that day.

The intended 2026-03-26 Day 3 queue is:

- malicious: `phishtank_2026_only_batch_0009` to `phishtank_2026_only_batch_0012`
- benign:
  - `tranco_top_1_10000_batch_0002`
  - `tranco_top_10001_100000_batch_0002`

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- current Plan A execution-prep docs

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 3
- operator command examples for Day 3

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite historical Day 1 or Day 2 artifacts as if they belonged to Day 3
- do not change capture code or runner behavior
- do not rename frozen sample files, schema fields, or CLI flags
- do not pretend the 2026-03-26 queue has already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `phishtank csv/phishtank_2026_only_batch_0009_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0010_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0011_urls.txt`
- `phishtank csv/phishtank_2026_only_batch_0012_urls.txt`
- `tranco csv/tranco_top_1_10000_batch_0002_urls.txt`
- `tranco csv/tranco_top_10001_100000_batch_0002_urls.txt`

### Prior Handoff

- `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`

### Missing Inputs

- actual returned artifacts from the user’s 2026-03-25 Day 2 queue are not available yet and must not be fabricated

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-03-26 Day 3 queue
- a repo prep/handoff doc with exact commands and output roots for Day 3

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

- Keep Day 1 and Day 2 queue artifacts frozen as historical context.
- Use new output roots for the 2026-03-26 queue so lineage remains auditable.
- Use the current supervised skip-capable commands as the recommended default commands for Day 3.
- Keep Day 3 benign bucket selection aligned with the documented Tranco quota mix instead of drifting further toward lower-rank buckets by default.

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

1. Keep the Day 1 and Day 2 prep docs as frozen context only.
2. Create a new 2026-03-26 task boundary for Day 3.
3. Freeze exact malicious and benign batch selections for Day 3.
4. Freeze exact supervised commands and output roots for Day 3.
5. Hand back the new prep doc for operator execution and later artifact return.

Task-specific execution notes:

- malicious Day 3 starts from `batch_0009`
- benign Day 3 returns to the second high-rank pair to stay closer to the documented quota mix
- both lanes should use supervised skip-capable commands by default

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-03-26 Day 3 queue has its own repo task doc
- [ ] the doc freezes malicious `batch_0009` to `batch_0012`
- [ ] the doc freezes benign `top_1_10000_batch_0002` and `top_10001_100000_batch_0002`
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

- confirmed input filenames for the Day 3 queue
- exact output roots for the Day 3 queue
- exact supervised commands for the Day 3 queue
