# Warden_PLAN_A_BATCH_TRACKER

## 涓枃鐗?
> 闈㈠悜 AI 鐨勮鏄庯細GPT銆丟emini銆丆odex銆丟rok銆丆laude 浠呭皢涓嬫柟鑻辨枃鐗堣涓烘潈濞佺増鏈€備腑鏂囦粎渚涗汉绫婚槄璇汇€佸崗浣滀笌蹇€熷瑙堛€?
### 浣跨敤璇存槑

- 杩欐槸 Plan A 鏃ュ父鎵规杩借釜鎬昏〃銆?- 瀹冨彧璁板綍鈥滃凡缁忛€夊畾瑕佽窇鐨勬壒娆♀€濆拰鈥滄槸鍚﹀凡缁忓洖浼犵粨鏋溾€濓紝涓嶇瓑浠蜂簬鏈€缁堟姄鍙栨垚鍔熺粺璁°€?- 鍚庣画姣忔鏂板缓鏂扮殑 Day N 浠诲姟鏃讹紝閮藉簲鍚屾鏇存柊杩欎唤鏂囨。銆?
### 褰撳墠鎽樿

- 褰撳墠宸插洖濉?Day 1 鍒?Day 11 鐨勫凡閫夋壒娆°€?- Day 1 鍒?Day 10 宸插洖浼犲苟鏀跺彛锛汥ay 11 浠呭畬鎴愭帓闃燂紝灏氭湭鍥炰紶缁撴灉銆?- Day 7 鍒?Day 11 澶勪簬 benign-only銆佹瘡澶?3 鎵圭殑鏂版棩甯稿彛寰勩€?- 姣忓ぉ浠嶄互瀵瑰簲鐨?day-level task / vm-prep 鏂囨。涓烘潈濞佺粏鑺傛潵婧愩€?
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
| Day 10 | 2026-04-07 | results_received | `none` | `tranco_top_10001_100000_batch_0012`; `tranco_top_100001_500000_batch_0007`; `tranco_top_500001_1000000_batch_0006` | `docs/tasks/2026-04-07_plan_a_batch_capture_day10_execution_task.md` | `docs/handoff/2026-04-07_plan_a_batch_capture_day10_vm_prep.md` |
| Day 11 | 2026-04-08 | results_received | `none` | `tranco_top_10001_100000_batch_0013`; `tranco_top_10001_100000_batch_0014`; `tranco_top_100001_500000_batch_0008` | `docs/tasks/2026-04-08_plan_a_batch_capture_day11_execution_task.md` | `docs/handoff/2026-04-08_plan_a_batch_capture_day11_vm_prep.md` |
| Day 12 | 2026-04-15 | results_received | `none` | `tranco_top_100001_500000_batch_0009`; `tranco_top_100001_500000_batch_0010`; `tranco_top_100001_500000_batch_0011` | `docs/tasks/2026-04-15_plan_a_batch_capture_day12_execution_task.md` | `docs/handoff/2026-04-15_plan_a_batch_capture_day12_vm_prep.md` |
| Day 13 | 2026-04-16 | results_received | `none` | `tranco_top_1_10000_batch_0005`; `tranco_top_1_10000_batch_0006`; `tranco_top_10001_100000_batch_0003` | `docs/tasks/2026-04-16_plan_a_batch_capture_day13_execution_task.md` | `docs/handoff/2026-04-16_plan_a_batch_capture_day13_vm_prep.md` |
| Day 14 | 2026-04-17 | selected | `none` | `tranco_top_10001_100000_batch_0004`; `tranco_top_10001_100000_batch_0005`; `tranco_top_10001_100000_batch_0006` | `docs/tasks/2026-04-17_plan_a_batch_capture_day14_execution_task.md` | `docs/handoff/2026-04-17_plan_a_batch_capture_day14_vm_prep.md` |
| Day 15 | 2026-04-21 | selected | `none` | `tranco_top_10001_100000_batch_0007`; `tranco_top_10001_100000_batch_0008`; `tranco_top_10001_100000_batch_0009` | `docs/tasks/2026-04-21_plan_a_batch_capture_day15_execution_task.md` | `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md` |

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
- Day 12 continues the benign-only daily cap of `3` batches.
- Day 13 continues the benign-only daily cap of `3` batches.
- The Day 1 to Day 6 status upgrade to `results_received` is based on the returned JSON package now present in `E:\Warden\channel`.
- Day 7 is marked `results_received` based on the returned Day 7 benign JSON package paths provided in the thread.
- Day 8 is marked `results_received` based on the returned Day 8 benign JSON package paths provided in the thread.
- Day 9 is marked `results_received` based on the returned Day 9 benign JSON package paths provided in the thread.
- Day 10 is marked `results_received` based on two returned `benign_capture_run.json` files plus the user-approved fallback of `batch_0012` `.review_state.json` and `review_actions.log`, because the `batch_0012` `benign_capture_run.json` is missing.
- Day 11 is marked `results_received` based on the three returned Day 11 `benign_capture_run.json` files now present under `data/raw/benign/2026-04-08_planA_day11_*`.
- Day 12 is marked `results_received` based on the three returned Day 12 `benign_capture_run.json` files, with an explicit caveat that `batch_0011` is a partial-interruption artifact (`321` JSON result rows and `592` current subdirectories at inspection time) and not a full 1000-row batch.
- Day 8 through Day 11 do not use a new `top_1_10000` tranche because `tranco_top_1_10000_batch_0005_urls.txt` is absent in the current repo-local split.
- Day 11 is the first queued day after `top_500001_1000000` is exhausted at `batch_0006`, so it continues with two `top_10001_100000` batches plus one `top_100001_500000` batch to preserve remaining rank priority.
- Day 12 is the first queued day where the current local benign queue can only continue with `top_100001_500000`, because `top_1_10000_batch_0005` is still missing, `top_10001_100000` is exhausted through `batch_0014`, and `top_500001_1000000` is exhausted through `batch_0006`.
- As of 2026-04-15, a new repo-local Tranco replenishment from `tranco csv/sources/tranco_PL9GJ.csv` restored `top_1_10000` as `tranco_top_1_10000_batch_0005` and `batch_0006`, so future Day 13+ benign planning can use that tranche again.
- Day 13 is the first queued day after that replenishment and therefore returns to the restored highest-rank tranche with `top_1_10000_batch_0005`, `top_1_10000_batch_0006`, and then `top_10001_100000_batch_0003`.
- Day 13 is now marked `results_received` based on the user-provided returned Day 13 `benign_capture_run.json` paths and counts recorded in `docs/handoff/2026-04-17_plan_a_batch_capture_day13_result_receipt.md`; unlike Day 12, no partial caveat was reported for Day 13.
- In the current Codex turn, a second repo-local Day 13 output-directory read was not available under `data/raw/benign`, so the Day 13 receipt closure explicitly documents that validation boundary instead of hiding it.
- Day 14 continues the benign-only daily cap of `3` batches.
- Day 14 uses `tranco_top_10001_100000_batch_0004`, `batch_0005`, and `batch_0006` because Day 13 already consumed the restored `top_1_10000` `batch_0005` and `batch_0006`, while `top_500001_1000000` remains exhausted.
- In the current 2026-04-21 Codex turn, Day 14 was not upgraded to `results_received`; the workspace exposed the `batch_0006` output directory, but the expected repo-local `batch_0004` and `batch_0005` output directories were not visible at the referenced paths.
- Day 15 continues the benign-only daily cap of `3` batches.
- Day 15 uses `tranco_top_10001_100000_batch_0007`, `batch_0008`, and `batch_0009` because Day 14 already froze `batch_0004` through `batch_0006`, making `batch_0007` through `batch_0009` the next highest-priority remaining unassigned Tranco benign batches.
- This tracker records selected queue membership and receipt state only. Final benign / malicious effectiveness analysis may still require separate reconciliation.

---

## 5. Update Rule

When a new Plan A Day N task is created:

1. add a new row to this tracker in the same turn;
2. mark the new row as `selected` or `results_pending` as appropriate;
3. link the new day-level task doc and prep/handoff doc;
4. do not mark `results_received` until the returned artifact package has actually been provided.


