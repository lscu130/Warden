# 2026-04-27_tranco_top_100001_500000_six_batch_supplement_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于把用户提供的新 Tranco CSV 继续切出 `6` 个 benign 候选批次。
- 切分位置按 `E:\Warden\tranco csv` 里已有的 `top_100001_500000` 最高批次继续，从 `batch_0017` 到 `batch_0022`。
- 本任务只生成 split artifacts 和 handoff，不安排新的 Day N capture 队列。

## English Version

# Task Metadata

- Task ID: WARDEN-TRANCO-TOP100001-500000-SIX-BATCH-SUPPLEMENT-SPLIT-V1
- Task Title: Generate six additional Tranco top_100001_500000 benign split batches after the current folder position
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / benign batch staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`
- Created At: 2026-04-27
- Requested By: user

---

## 1. Background

The user provided a new Tranco source CSV:

- `C:\Users\20516\Downloads\tranco_QW4P4.csv`

The current repo-local Tranco split folder already contains `top_100001_500000` batches through:

- `tranco_top_100001_500000_batch_0016`

The user requested six more batches following the split position already present in the Tranco folder.

---

## 2. Goal

Copy the provided source CSV into the repo-local Tranco source archive and generate six additional `top_100001_500000` split batches:

- `tranco_top_100001_500000_batch_0017`
- `tranco_top_100001_500000_batch_0018`
- `tranco_top_100001_500000_batch_0019`
- `tranco_top_100001_500000_batch_0020`
- `tranco_top_100001_500000_batch_0021`
- `tranco_top_100001_500000_batch_0022`

Each batch must have both:

- normalized CSV: `rank,domain,url`
- URL-only TXT: one URL per line

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\tranco csv\sources\tranco_QW4P4.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0018_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0019_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0020_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0021_urls.txt`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022.csv`
- `E:\Warden\tranco csv\tranco_top_100001_500000_batch_0022_urls.txt`
- `E:\Warden\tranco csv\supplement_split_summary_2026-04-27_top_100001_500000_batches_0017_0022.json`
- `docs/tasks/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`
- `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`

This task is allowed to change:

- additive split artifacts only
- additive task and handoff documentation only

---

## 4. Scope Out

This task must NOT do the following:

- do not overwrite existing Tranco batch artifacts
- do not modify capture code
- do not modify split helper behavior
- do not update Day N capture scheduling
- do not mark any capture result as received
- do not change schema, labels, CLI, or output format contracts

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/modules/Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY.md`
- `docs/handoff/2026-04-15_tranco_top_1_10000_replenishment_split.md`

### Code / Scripts

- `scripts/data/benign/split_tranco_supplement.py` as the existing policy reference

### Data / Artifacts

- `C:\Users\20516\Downloads\tranco_QW4P4.csv`
- existing files under `E:\Warden\tranco csv`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- one repo-local source copy under `tranco csv\sources`
- six new normalized batch CSV files
- six new URL-only TXT files
- one summary JSON for this supplement split
- one handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Generate exactly `6` new batches.
- Continue `top_100001_500000` local batch numbering after `batch_0016`.
- Use batch size `1000`.
- Exclude ranks and domains already present in existing repo-local Tranco split CSVs.
- Do not overwrite any existing batch file.
- Keep TXT files URL-only.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Tranco batch CSV format: `rank,domain,url`
- existing URL TXT format: one URL per line

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `rank`, `domain`, `url`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing benign runner commands using `*_urls.txt`
  - existing benign runner commands using CSV with `--csv_url_column url`

Downstream consumers to watch:

- Plan A benign capture planning
- benign result receipt handoffs
- later deduplication and TrainSet V1 admission checks

---

## 9. Suggested Execution Plan

Recommended order:

1. Confirm the source file exists and has rank/domain rows.
2. Confirm current `top_100001_500000` max batch index is `0016`.
3. Copy the source CSV into `E:\Warden\tranco csv\sources`.
4. Generate `batch_0017` through `batch_0022` without overwriting existing files.
5. Validate row counts, TXT line counts, headers, duplicate domains, and summary JSON.
6. Write a handoff.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] source CSV is copied into repo-local `tranco csv\sources`
- [ ] exactly six new CSV files exist
- [ ] exactly six new TXT files exist
- [ ] each CSV has `1000` data rows plus header
- [ ] each TXT has `1000` URL lines
- [ ] generated CSV headers are exactly `rank,domain,url`
- [ ] no generated domains duplicate existing repo-local Tranco split domains
- [ ] generated batch numbering is `0017` through `0022`
- [ ] summary JSON records source, policy, exclusion counts, and generated batches
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] source existence check
- [ ] generated file existence check
- [ ] per-file CSV/TXT row count check
- [ ] duplicate generated domain check against existing split inventory
- [ ] no overwrite check for previous `batch_0016`
- [ ] summary JSON spot-check

Commands to run if applicable:

```powershell
Test-Path -LiteralPath 'C:\Users\20516\Downloads\tranco_QW4P4.csv'
Test-Path -LiteralPath 'E:\Warden\tranco csv\tranco_top_100001_500000_batch_0017.csv'
Get-Content -LiteralPath 'E:\Warden\tranco csv\supplement_split_summary_2026-04-27_top_100001_500000_batches_0017_0022.json'
```

Expected evidence to capture:

- generated batch names
- generated row counts
- rank min/max for each generated batch
- duplicate-check result

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path:

- `docs/handoff/2026-04-27_tranco_top_100001_500000_six_batch_supplement_split.md`

---

## 13. Open Questions / Blocking Issues

- none
