# Warden_PLAN_A_BATCH_TRACKER

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Plan A 日常批次追踪总表。
- 它只记录“已经选定要跑的批次”和“是否已经回传结果”，不等价于最终抓取成功统计。
- 后续每次新建新的 Day N 任务时，都应同步更新这份文档。

### 当前摘要

- 当前已回填 Day 1 到 Day 11 的已选批次。
- Day 1 到 Day 9 已回传并收口；Day 10 仍是 `results_pending`；Day 11 仅完成排队，尚未回传结果。
- Day 7 到 Day 11 处于 benign-only、每天 3 批的新日常口径。
- 每天仍以对应的 day-level task / vm-prep 文档为权威细节来源。

## English Version

## 1. Purpose

This document is the living Plan A batch tracker for daily malicious and benign capture queues.
It records which batches have already been selected for each day and whether returned result artifacts have been received yet.

It does **not** replace the day-level task docs or prep handoffs.
It is a compact continuity layer so future daily planning does not lose track of already-assigned batches.

Important rule:

- Every time a new Day N Plan A task is created, this tracker must be updated in the same turn.

---

## 2. Status Legend

- `selected`: the daily queue was frozen in repo docs
- `results_pending`: selected to run, but returned result artifacts are not yet fully recorded here
- `results_received`: the returned result artifact package for that day has been received and linked here

---

## 3. Daily Tracker

| Day | Calendar Date | Status | Malicious Batches Selected | Benign Batches Selected | Primary Task Doc | Primary Prep / Handoff |
| --- | --- | --- | --- | --- | --- | --- |
| Day 1 | 2026-03-24 | results_received | `phishtank_2026_only_batch_0001` - `phishtank_2026_only_batch_0004` | `tranco_top_1_10000_batch_0001`; `tranco_top_10001_100000_batch_0001` | `docs/tasks/2026-03-24_plan_a_batch_capture_execution_task.md` | `docs/handoff/2026-03-24_plan_a_batch_capture_vm_prep.md` |
| Day 2 | 2026-03-25 | results_received | `phishtank_2026_only_batch_0005` - `phishtank_2026_only_batch_0008` | `tranco_top_100001_500000_batch_0001`; `tranco_top_500001_1000000_batch_0001` | `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md` | `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md` |
| Day 3 | 2026-03-26 | results_received | `phishtank_2026_only_batch_0009` - `phishtank_2026_only_batch_0012` | `tranco_top_1_10000_batch_0002`; `tranco_top_10001_100000_batch_0002` | `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md` | `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md` |
| Day 4 | 2026-03-27 | results_received | `phishtank_2026_only_batch_0013` - `phishtank_2026_only_batch_0020` | `tranco_top_100001_500000_batch_0002`; `tranco_top_500001_1000000_batch_0002` | `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md` | `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md` |
| Day 5 | 2026-03-28 | results_received | `phishtank_2026_only_batch_0021` - `phishtank_2026_only_batch_0028` | `tranco_top_1_10000_batch_0003`; `tranco_top_10001_100000_batch_0008` | `docs/tasks/2026-03-28_plan_a_batch_capture_day5_execution_task.md` | `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md` |
| Day 6 | 2026-03-30 | results_received | `phishtank_2026_only_batch_0029` - `phishtank_2026_only_batch_0032` | `tranco_top_100001_500000_batch_0003`; `tranco_top_500001_1000000_batch_0003` | `docs/tasks/2026-03-30_plan_a_batch_capture_day6_execution_task.md` | `docs/handoff/2026-03-30_plan_a_batch_capture_day6_vm_prep.md` |
| Day 7 | 2026-04-01 | results_received | `none` | `tranco_top_1_10000_batch_0004`; `tranco_top_10001_100000_batch_0009`; `tranco_top_100001_500000_batch_0004` | `docs/tasks/2026-04-01_plan_a_batch_capture_day7_execution_task.md` | `docs/handoff/2026-04-01_plan_a_batch_capture_day7_vm_prep.md` |
| Day 8 | 2026-04-02 | results_received | `none` | `tranco_top_10001_100000_batch_0010`; `tranco_top_100001_500000_batch_0005`; `tranco_top_500001_1000000_batch_0004` | `docs/tasks/2026-04-02_plan_a_batch_capture_day8_execution_task.md` | `docs/handoff/2026-04-02_plan_a_batch_capture_day8_vm_prep.md` |
| Day 9 | 2026-04-03 | results_received | `none` | `tranco_top_10001_100000_batch_0011`; `tranco_top_100001_500000_batch_0006`; `tranco_top_500001_1000000_batch_0005` | `docs/tasks/2026-04-03_plan_a_batch_capture_day9_execution_task.md` | `docs/handoff/2026-04-03_plan_a_batch_capture_day9_vm_prep.md` |
| Day 10 | 2026-04-07 | results_pending | `none` | `tranco_top_10001_100000_batch_0012`; `tranco_top_100001_500000_batch_0007`; `tranco_top_500001_1000000_batch_0006` | `docs/tasks/2026-04-07_plan_a_batch_capture_day10_execution_task.md` | `docs/handoff/2026-04-07_plan_a_batch_capture_day10_vm_prep.md` |
| Day 11 | 2026-04-08 | selected | `none` | `tranco_top_10001_100000_batch_0013`; `tranco_top_10001_100000_batch_0014`; `tranco_top_100001_500000_batch_0008` | `docs/tasks/2026-04-08_plan_a_batch_capture_day11_execution_task.md` | `docs/handoff/2026-04-08_plan_a_batch_capture_day11_vm_prep.md` |

---

## 4. Notes

- Day 4 is the first day where malicious daily volume was explicitly doubled from `4` batches to `8` batches due to the user-reported low practical PhishTank effective yield.
- Day 5 is the first day that starts consuming the supplemental Tranco split tranche created on 2026-03-26.
- Day 6 returns malicious daily volume to `4` batches because the user explicitly requested that planning change.
- Day 7 is the first benign-only day and sets the new daily cap to `3` benign batches.
- Day 8 continues the benign-only daily cap of `3` batches.
- Day 9 continues the benign-only daily cap of `3` batches.
- Day 10 continues the benign-only daily cap of `3` batches.
- Day 11 continues the benign-only daily cap of `3` batches.
- The Day 1 to Day 6 status upgrade to `results_received` is based on the returned JSON package now present in `E:\Warden\channel`.
- Day 7 is marked `results_received` based on the returned Day 7 benign JSON package paths provided in the thread.
- Day 8 is marked `results_received` based on the returned Day 8 benign JSON package paths provided in the thread.
- Day 9 is marked `results_received` based on the returned Day 9 benign JSON package paths provided in the thread.
- Day 8 through Day 11 do not use a new `top_1_10000` tranche because `tranco_top_1_10000_batch_0005_urls.txt` is absent in the current repo-local split.
- Day 11 is the first queued day after `top_500001_1000000` is exhausted at `batch_0006`, so it continues with two `top_10001_100000` batches plus one `top_100001_500000` batch to preserve remaining rank priority.
- This tracker records selected queue membership and receipt state only. Final benign / malicious effectiveness analysis may still require separate reconciliation.

---

## 5. Update Rule

When a new Plan A Day N task is created:

1. add a new row to this tracker in the same turn;
2. mark the new row as `selected` or `results_pending` as appropriate;
3. link the new day-level task doc and prep/handoff doc;
4. do not mark `results_received` until the returned artifact package has actually been provided.

