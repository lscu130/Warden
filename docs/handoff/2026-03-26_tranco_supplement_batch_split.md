# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Tranco 补充分片的正式 handoff。
- 若涉及精确输入文件、生成批次数、编号续接方式、验证结果或兼容性，以英文版为准。

### 摘要

- 对应任务：`WARDEN-TRANCO-SUPPLEMENT-BATCH-SPLIT-V1`
- 任务主题：排除旧分片已覆盖项后，再切一批新的 Tranco benign 分片
- 当前状态：`DONE`
- 所属模块：Data module / benign batch staging

### 当前交付要点

- 新补充分片基于新的 Tranco CSV 生成，同时排除了旧仓库分片里已经出现过的 rank / domain。
- 原来的 rank-bucket 配额、均匀选取逻辑和 `1000` 行 batch 结构被完整保留。
- 旧 `split_summary.json` 没有被覆盖，新的 supplemental summary 与新增 CSV / TXT 工件是增量交付。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-26-tranco-supplement-batch-split-handoff
- Related Task ID: WARDEN-TRANCO-SUPPLEMENT-BATCH-SPLIT-V1
- Task Title: Create a supplemental Tranco benign split tranche by excluding already-split rows and reapplying the frozen rank-bucket policy
- Module: Data module / benign batch staging
- Author: Codex
- Date: 2026-03-26
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Created a new supplemental Tranco benign split tranche from `C:\Users\20516\Downloads\tranco_9WYQ2.csv`.
The supplement excludes all rows/domains already represented in the existing repository-local Tranco split artifacts under `E:\Warden\tranco csv`, reapplies the same frozen rank-bucket quotas, continues per-bucket batch numbering without collisions, and writes a new supplemental summary JSON instead of modifying the old split summary.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/split_tranco_supplement.py`.

### Doc Changes

- Added `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`.
- Added `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`.

### Output / Artifact Changes

- Added `E:\Warden\tranco csv\supplement_split_summary_2026-03-26.json`.
- Added a new supplemental tranche of `20` Tranco CSV batch files.
- Added `20` new companion TXT files with one derived benign URL per line.

---

## 3. Files Touched

- `scripts/data/benign/split_tranco_supplement.py`
- `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`
- `E:\Warden\tranco csv\supplement_split_summary_2026-03-26.json`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0003.csv`
- `E:\Warden\tranco csv\tranco_top_1_10000_batch_0003_urls.txt`

Optional notes per file:

- The script is additive and does not modify the original split helper outputs.
- The summary JSON is the authoritative count record for this supplemental tranche.
- More generated CSV/TXT files exist than the few representative output files listed above.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can now consume an additional supplemental Tranco benign tranche without reusing already-split rows/domains.
- The supplemental split preserves the same frozen rank-bucket quotas and 1000-row batch size as the original split.
- Per-bucket batch numbering now continues from the prior maximum instead of restarting at `0001`.

### Preserved Behavior

- The original `split_summary.json` remains unchanged.
- Existing Tranco batch file names remain valid.
- No benign capture code or CLI changed.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for existing scripts; the new CSV/TXT files and supplemental summary JSON are additive operator artifacts.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This task only adds a supplemental Tranco split helper plus additive Tranco batch artifacts.
The current benign capture scripts keep the same CLI and runtime behavior.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\benign\split_tranco_supplement.py --source_csv "C:\Users\20516\Downloads\tranco_9WYQ2.csv"
python -m py_compile E:\Warden\scripts\data\benign\split_tranco_supplement.py
inspect E:\Warden\tranco csv\supplement_split_summary_2026-03-26.json
inspect generated file inventory under E:\Warden\tranco csv
```

### Result

- Confirmed the supplement script generated `20,000` new selected rows across `20` new batches.
- Confirmed the supplemental summary recorded exclusion of `20,000` existing ranks and `20,000` existing domains from the prior split tranche.
- Confirmed continued per-bucket batch numbering:
  - `top_1_10000`: starts at `batch_0003`
  - `top_10001_100000`: starts at `batch_0008`
  - `top_100001_500000`: starts at `batch_0009`
  - `top_500001_1000000`: starts at `batch_0004`
- Confirmed the script passes `py_compile`.

### Not Run

- live benign capture using the new supplemental batches
- downstream benign quality filtering / safety veto
- downstream cluster / train-pool stages

Reason:

This task only staged a new supplemental benign source tranche.
The downstream capture and later selection stages are separate operator workflows.

---

## 7. Risks / Caveats

- Exclusion is based on already-split `rank` and `domain` values from existing Tranco batch CSV artifacts; this is the correct practical operator boundary, but it is not a broader “content-level uniqueness” guarantee.
- The same caveat as the original split still applies: `url` is derived as `https://{domain}/`, so later capture may still fail, redirect, or yield low-value pages.
- This supplemental tranche preserves the original frozen quota mix; it does not rebalance the bucket mix around the recently observed real capture yield by bucket.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- Use the new supplemental `*_urls.txt` files as the next benign source tranche after the current planned batches are exhausted.
- Keep Day 2 / Day 3 benign execution planning auditable by referencing the new continued batch indices rather than renaming old files.
- If benign yield remains materially below target after this supplemental tranche, reuse `scripts/data/benign/split_tranco_supplement.py` against the next Tranco source CSV instead of hand-editing split files.
