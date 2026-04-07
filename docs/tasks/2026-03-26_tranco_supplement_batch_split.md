# 2026-03-26_tranco_supplement_batch_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Tranco 补充分片任务的任务定义。
- 若涉及精确输入 CSV、配额、批次编号、输出文件名或验证口径，以英文版为准。

## 1. 背景

当前仓库里的 Tranco 分片已经不足以支撑后续 benign 抓取，因为实际 benign yield 只有大约 `50%` 到 `60%`。
用户要求从新的 Tranco CSV 再切一批补充分片，但必须先排除旧分片里已经出现过的 rank / domain，并继续沿用原来冻结好的 rank bucket 配额和均匀选取规则。

## 2. 目标

在不覆盖旧分片结果的前提下，生成一批新的 supplemental Tranco CSV / TXT 批次与补充 summary，使后续 benign 抓取可以继续推进，同时保持和原分片策略兼容。

## 3. 范围

- 纳入：supplement split helper、补充批次工件、对应 task / handoff
- 排除：旧分片覆盖、capture 语义修改、rank bucket 政策重写

## English Version

# Task Metadata

- Task ID: WARDEN-TRANCO-SUPPLEMENT-BATCH-SPLIT-V1
- Task Title: Create a supplemental Tranco benign split tranche by excluding already-split rows and reapplying the frozen rank-bucket policy
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / benign batch staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/tasks/2026-03-23_tranco_batch_split.md`; `docs/handoff/2026-03-23_tranco_batch_split.md`
- Created At: 2026-03-26
- Requested By: user

---

## 1. Background

The current repository-local Tranco split under `E:\Warden\tranco csv` is no longer enough for benign capture because the observed benign capture yield is only around `50%` to `60%`.
The user explicitly requested a new supplemental split tranche from a newer Tranco CSV, while excluding all rows already represented in the existing repository-local split artifacts.

The prior Tranco split already froze:

- the four rank buckets,
- the per-bucket selected-row quotas,
- deterministic evenly spaced selection inside each bucket,
- 1000-row batch files plus companion `*_urls.txt`.

This new task must preserve that selection logic while excluding all rows/domains already emitted into the existing Tranco batch artifacts.

---

## 2. Goal

Produce a new supplemental set of Tranco CSV/TXT batch artifacts under `E:\Warden\tranco csv` by reading `C:\Users\20516\Downloads\tranco_9WYQ2.csv`, excluding already-split rows/domains from the existing Tranco artifacts, and then reapplying the same rank-bucket quotas and deterministic evenly spaced selection policy.

The output should continue the existing per-bucket batch numbering instead of overwriting prior files, and it should emit a new supplemental summary JSON instead of mutating the old split summary.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/`
- `docs/tasks/`
- `docs/handoff/`
- `E:\Warden\tranco csv\`

This task is allowed to change:

- additive Tranco supplement split helper code
- additive Tranco batch CSV/TXT artifacts
- additive Tranco supplemental summary documentation

---

## 4. Scope Out

This task must NOT do the following:

- do not overwrite the original Tranco split files
- do not change benign capture code or capture semantics
- do not change the frozen rank-bucket policy
- do not silently rename old batch files or old summary files

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/tasks/2026-03-23_tranco_batch_split.md`
- `docs/handoff/2026-03-23_tranco_batch_split.md`

### Code / Scripts

- `scripts/data/common/io_utils.py`
- `scripts/data/benign/run_benign_capture.py`

### Data / Artifacts

- `C:\Users\20516\Downloads\tranco_9WYQ2.csv`
- existing Tranco split artifacts under `E:\Warden\tranco csv`
- existing `split_summary.json`

### Prior Handoff

- `docs/handoff/2026-03-23_tranco_batch_split.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a reproducible supplement split helper script
- new additive Tranco batch CSV files
- new additive Tranco batch TXT files
- a supplemental summary JSON
- a repo handoff document

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

- Reapply the same frozen rank-bucket quotas as the original Tranco split.
- Exclude rows already represented by existing split artifacts before selecting new rows.
- Continue per-bucket batch numbering instead of overwriting prior files.
- Write a new supplemental summary JSON rather than modifying the old one in place.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing benign runner CLI
- existing Tranco batch file naming pattern
- existing original `split_summary.json`

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current benign batch capture commands
  - current existing Tranco batch file references

Downstream consumers to watch:

- operator use of `E:\Warden\tranco csv\*_urls.txt`
- later Day 2 / Day 3 benign execution planning

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the original Tranco split policy and current artifact set.
2. Enumerate already-split Tranco rows/domains from the existing batch CSV files.
3. Create a supplement split helper that excludes those rows/domains and reapplies the same quotas.
4. Emit new batch CSV/TXT files with continued per-bucket numbering.
5. Emit a separate supplemental summary JSON.
6. Validate counts and hand back the new artifact inventory.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] a supplement split helper script exists in the repo
- [ ] the new split excludes already-split rows/domains from existing artifacts
- [ ] the same rank-bucket quotas are reapplied
- [ ] new batch numbering continues without collisions
- [ ] a new supplemental summary JSON is written
- [ ] no old Tranco split artifact was overwritten
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] existing batch inventory was parsed successfully
- [ ] source CSV shape was parsed successfully
- [ ] new files were written without colliding with old filenames
- [ ] supplemental summary counts match the actual generated files

Commands to run if applicable:

```bash
python scripts/data/benign/split_tranco_supplement.py --source_csv "C:\Users\20516\Downloads\tranco_9WYQ2.csv"
```

Expected evidence to capture:

- generated supplemental summary JSON
- generated file count by bucket
- continued batch indices by bucket
