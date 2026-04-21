# Handoff Metadata

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-15` 的 Tranco `top_1_10000` 补充分片正式 handoff。
- 本次只补了 `top_1_10000`，没有重跑其它 bucket。
- 若涉及精确源文件路径、新 batch 编号、剩余容量估算或兼容性结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-TRANCO-TOP1-REPLENISHMENT-SPLIT-V1`
- 任务主题：用新的 Tranco CSV 补回缺失的 `top_1_10000` tranche，并重算剩余 benign split 余量
- 当前状态：`DONE`
- 所属模块：Data module / benign batch staging

### 当前交付要点

- 新的源文件已复制进仓库：`E:\Warden\tranco csv\sources\tranco_PL9GJ.csv`
- `split_tranco_supplement.py` 现在支持只生成指定 bucket
- 新增 `top_1_10000` 的 `batch_0005` 和 `batch_0006`
- 补片后，按 tracker 到 Day 12 计，剩余已划分 benign 余量是 `12` 个 batch，约 `12k` 原始站点

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-15-tranco-top1-replenishment-split
- Related Task ID: WARDEN-TRANCO-TOP1-REPLENISHMENT-SPLIT-V1
- Task Title: Replenish the missing top_1_10000 Tranco tranche from a new CSV and reassess remaining benign split capacity
- Module: Data module / benign batch staging
- Author: Codex
- Date: 2026-04-15
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Copied the new user-provided Tranco source into the repo, extended the supplemental split helper so it can target specific rank buckets, and generated a new additive `top_1_10000` tranche only.
This replenishment restores `tranco_top_1_10000_batch_0005` and `batch_0006` without changing any existing split artifact or any already-frozen daily capture queue.

The remaining split-capacity assessment is:

- before this replenishment, the already-split inventory left after Day 11 was `13` batches (`~13k` raw sites, `~6.5k` effective at the user's `50%` assumption),
- after this replenishment, the inventory left after Day 11 is `15` batches (`~15k` raw, `~7.5k` effective),
- and after the currently frozen Day 12 queue is consumed, the remaining inventory is `12` batches (`~12k` raw, `~6k` effective).

That means the old remaining split was borderline if the current benign pool is truly around `15k`, while the replenished split is enough to cross the `20k` benign target with some buffer, but still not a large one.

---

## 2. What Changed

### Code Changes

- Updated `scripts/data/benign/split_tranco_supplement.py`.
- Added an optional `--bucket_labels` argument so the helper can generate only selected rank buckets while preserving the previous default behavior when the flag is omitted.

### Doc Changes

- Added `docs/tasks/2026-04-15_tranco_top_1_10000_replenishment_split.md`.
- Added `docs/handoff/2026-04-15_tranco_top_1_10000_replenishment_split.md`.
- Updated `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`.

### Output / Artifact Changes

- Added the repo-local source copy `E:\Warden\tranco csv\sources\tranco_PL9GJ.csv`.
- Added `E:\Warden\tranco csv\supplement_split_summary_2026-04-15_top_1_10000.json`.
- Added `E:\Warden\tranco csv\tranco_top_1_10000_batch_0005.csv`.
- Added `E:\Warden\tranco csv\tranco_top_1_10000_batch_0005_urls.txt`.
- Added `E:\Warden\tranco csv\tranco_top_1_10000_batch_0006.csv`.
- Added `E:\Warden\tranco csv\tranco_top_1_10000_batch_0006_urls.txt`.

---

## 3. Files Touched

- `scripts/data/benign/split_tranco_supplement.py`
- `docs/tasks/2026-04-15_tranco_top_1_10000_replenishment_split.md`
- `docs/handoff/2026-04-15_tranco_top_1_10000_replenishment_split.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `E:\Warden\tranco csv\sources\tranco_PL9GJ.csv`
- `E:\Warden\tranco csv\supplement_split_summary_2026-04-15_top_1_10000.json`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0005.csv`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0005_urls.txt`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0006.csv`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0006_urls.txt`

Optional notes per file:

- The helper change is backward-compatible because the new bucket filter is optional.
- The new source file now lives inside the repo so future threads do not depend on the Downloads folder.
- The new generated batches are additive and continue numbering after `batch_0004`.

---

## 4. Behavior Impact

### Expected New Behavior

- Future supplement generation can target only specific rank buckets using `--bucket_labels`.
- Future Day N planning can use `tranco_top_1_10000_batch_0005` and `batch_0006`.
- The current Tranco split inventory now contains `42` total batches instead of `40`.

### Preserved Behavior

- Existing invocations of `split_tranco_supplement.py --source_csv ...` remain valid because omitting `--bucket_labels` still targets all frozen buckets.
- Existing Tranco batch file names remain valid.
- Day 12 queue membership remains unchanged.
- Benign capture code and capture semantics remain unchanged.

### User-facing / CLI Impact

- The internal helper script now accepts optional `--bucket_labels <comma-separated-labels>`.

### Output Format Impact

- none for existing files; the new summary JSON and batch CSV/TXT artifacts are additive.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/benign/split_tranco_supplement.py`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

Compatibility notes:

The helper-script interface changed only by adding an optional argument.
Existing calls that do not pass `--bucket_labels` still follow the prior all-bucket behavior.
No existing batch artifact was renamed or overwritten.

---

## 6. Validation Performed

### Commands Run

```bash
Copy-Item -LiteralPath 'C:\Users\20516\Downloads\tranco_PL9GJ.csv' -Destination 'E:\Warden\tranco csv\sources\tranco_PL9GJ.csv' -Force
python -m py_compile E:\Warden\scripts\data\benign\split_tranco_supplement.py
python E:\Warden\scripts\data\benign\split_tranco_supplement.py --source_csv "E:\Warden\tranco csv\sources\tranco_PL9GJ.csv" --bucket_labels top_1_10000 --summary_name supplement_split_summary_2026-04-15_top_1_10000.json
inspect E:\Warden\tranco csv\supplement_split_summary_2026-04-15_top_1_10000.json
inspect E:\Warden\tranco csv\tranco_top_1_10000_batch_0005.csv
inspect E:\Warden\tranco csv\tranco_top_1_10000_batch_0006.csv
```

### Result

- Confirmed the new source CSV now exists at `E:\Warden\tranco csv\sources\tranco_PL9GJ.csv`.
- Confirmed the updated helper passes `py_compile`.
- Confirmed the bucket-restricted run generated exactly `2000` rows across exactly `2` batches.
- Confirmed the new summary JSON records `requested_bucket_labels=["top_1_10000"]`.
- Confirmed the new batch numbering starts at `batch_0005` and `batch_0006`.
- Confirmed the replenishment source had `3742` available unique rows left in `top_1_10000` after exclusion, and this turn selected `2000` of them.
- Confirmed the remaining inventory after Day 11 is now `15` batches total.
- Confirmed the remaining inventory after the currently frozen Day 12 queue would be `12` batches total.

### Not Run

- old full-bucket script invocation as an execution smoke test
- live benign capture using the new `top_1_10000` batches
- downstream filtering / veto / review on the new batches

Reason:

This task only stages new additive split artifacts and continuity updates.
Backward compatibility of the old invocation path is inferred from the new flag being optional, plus compile sanity, rather than from a full second split run.

---

## 7. Risks / Caveats

- The new source CSV appears to contain `4,266,193` rows, so it is not a one-million-row Tranco snapshot like the older files; this is acceptable for the replenishment because the helper only consumes the needed rank bucket and still excludes already-split ranks/domains.
- Even after replenishment, the remaining benign inventory is not abundant: after Day 12 it is only `~12k` raw, which is `~6k` effective at the user's `50%` assumption.
- This replenishment improves head-domain coverage but also increases future reliance on `top_1_10000`; if the benign pool needs stronger long-tail balance later, more non-head replenishment may still be needed.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-15_tranco_top_1_10000_replenishment_split.md`
- `docs/handoff/2026-04-15_tranco_top_1_10000_replenishment_split.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

Doc debt still remaining:

- none for this replenishment turn

---

## 9. Recommended Next Step

- Use `tranco_top_1_10000_batch_0005_urls.txt` before continuing deeper down the remaining lower-priority benign inventory.
- Treat the current split inventory as enough to get past the `20k` benign target if the user's `~15k` current-size estimate and `~50%` effective-yield assumption are both roughly correct.
- Do not treat the buffer as generous; if actual effective yield drops below `50%`, prepare another supplemental tranche before the post-Day-12 inventory gets too low.
