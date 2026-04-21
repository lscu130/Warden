# 2026-04-15_tranco_top_1_10000_replenishment_split

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-15` 的 Tranco `top_1_10000` 补充分片任务定义。
- 本任务只补 `top_1_10000`，不重跑其它 rank bucket。
- 若涉及精确输入源、batch 编号、输出文件名、剩余容量估算或兼容性结论，以英文版为准。

## 1. 背景

当前仓库本地 Tranco split 中，`top_1_10000` 只有 `batch_0001` 到 `batch_0004`，后续高 rank tranche 已断档。
用户提供了新的 `C:/Users/20516/Downloads/tranco_PL9GJ.csv`，要求用它补 `1-10000`。

同时，按当前 Plan A 队列进度估算，Day 11 收口后 benign 规模大约在 `15k` 左右，而剩余已划分 Tranco 余量偏紧。
考虑到每 `1000` 个站点大约只有 `50%` 有效，这次需要补一个新的 `top_1_10000` tranche，并给出剩余库存是否够用的明确判断。

## 2. 目标

在不覆盖旧分片、也不改 Day 12 已冻结队列的前提下：

- 把新的 Tranco CSV 复制进仓库内可追踪位置；
- 给现有 supplement split helper 增加“只补指定 bucket”的能力；
- 仅为 `top_1_10000` 生成新的 additive CSV / TXT batch；
- 记录这次补充分片后的剩余 benign split 余量判断；
- 更新 continuity 文档，让后续 Day N 排队知道 `top_1_10000_batch_0005` 已重新可用。

## 3. 范围

- 纳入：Tranco supplement split helper、repo 内 source copy、补充 batch 工件、task / handoff、必要 continuity 注记
- 排除：capture 代码语义、已冻结的 Day 12 队列、其它 bucket 的新补片、训练/标注逻辑

## English Version

# Task Metadata

- Task ID: WARDEN-TRANCO-TOP1-REPLENISHMENT-SPLIT-V1
- Task Title: Replenish the missing top_1_10000 Tranco tranche from a new CSV and reassess remaining benign split capacity
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / benign batch staging
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/tasks/2026-03-23_tranco_batch_split.md`; `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`; `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- Created At: 2026-04-15
- Requested By: user

---

## 1. Background

The current repository-local Tranco split under `E:\Warden\tranco csv` contains only `top_1_10000` batches `0001` through `0004`.
That left later daily benign planning without any `top_1_10000_batch_0005` artifact and forced Day 8 onward to route around the missing high-rank tranche.

The user has now provided a new source CSV at `C:\Users\20516\Downloads\tranco_PL9GJ.csv` and explicitly requested that it should be used to replenish `top_1_10000`.
At the same time, the user stated that the current benign set is roughly `15k` after including Day 11, while the practical effective yield is only around `50%` per `1000` input websites.

That means this task needs to do two things together:

- replenish the missing high-rank tranche safely and additively,
- and assess whether the already-split remaining benign inventory is enough without that replenishment.

---

## 2. Goal

Create an additive `top_1_10000` replenishment from the new Tranco CSV without disturbing existing split artifacts or already-frozen daily capture queues.

This task must:

- copy the new source CSV into a repository-local tracked location for future continuity,
- extend the existing supplement split helper so it can target only specified rank buckets,
- generate only new `top_1_10000` batch artifacts with continued numbering,
- write a new supplemental summary JSON for this replenishment,
- and update continuity docs so future Day N planning knows that `top_1_10000_batch_0005` is available again.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/`
- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`
- `E:\Warden\tranco csv\`

This task is allowed to change:

- additive helper-script CLI for bucket-restricted supplement generation
- additive Tranco source copy inside the repo
- additive `top_1_10000` batch CSV/TXT artifacts
- additive summary JSON and continuity docs

---

## 4. Scope Out

This task must NOT do the following:

- do not overwrite the original Tranco split files
- do not regenerate other rank buckets in this turn
- do not change benign capture code or capture semantics
- do not silently modify the frozen Day 12 queue
- do not rename existing batch files or old summary files

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
- `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

### Code / Scripts

- `scripts/data/benign/split_tranco_supplement.py`
- `scripts/data/common/io_utils.py`

### Data / Artifacts

- `C:\Users\20516\Downloads\tranco_PL9GJ.csv`
- existing Tranco split artifacts under `E:\Warden\tranco csv`
- existing `split_summary.json`
- existing `supplement_split_summary_2026-03-26.json`

### Prior Handoff

- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`

### Missing Inputs

- none, if the user-provided CSV is readable

---

## 6. Required Outputs

This task should produce:

- a repo-local copy of `tranco_PL9GJ.csv`
- a backward-compatible supplement helper update that supports bucket-restricted generation
- new additive `tranco_top_1_10000_batch_*.csv` files
- new additive `tranco_top_1_10000_batch_*_urls.txt` files
- a new supplemental summary JSON for this replenishment
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

- The new source CSV must be copied into the repo because future collaboration depends on it.
- The replenishment must be additive and must continue batch numbering after `top_1_10000_batch_0004`.
- The helper update must remain backward-compatible with the prior full-supplement workflow.
- This turn should generate only `top_1_10000` supplement output.
- The final response must explicitly state whether the already-split remaining benign inventory is enough under the user's `~50%` effective-yield assumption.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Tranco batch naming pattern
- existing batch CSV columns: `rank`, `domain`, `url`
- existing prior supplement script invocation

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `rank`, `domain`, `url`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/split_tranco_supplement.py --source_csv "..."`
  - current benign batch capture commands against old `*_urls.txt`

Downstream consumers to watch:

- future Day N benign queue planning
- operators consuming `E:\Warden\tranco csv\*_urls.txt`
- continuity reads of `Warden_PLAN_A_BATCH_TRACKER.md`

---

## 9. Suggested Execution Plan

Recommended order:

1. Copy the new user-provided Tranco CSV into a repository-local source path.
2. Assess current remaining split inventory and effective-yield headroom.
3. Extend the supplement helper to support bucket-restricted generation.
4. Generate only the new `top_1_10000` supplement tranche with continued numbering.
5. Validate generated artifacts and summary counts.
6. Update continuity docs and handoff.

Task-specific execution notes:

- Keep Day 12 unchanged.
- Preserve the prior supplement script default behavior when no bucket filter is provided.
- Treat inventory sufficiency as an explicit engineering conclusion, not an implicit assumption.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the new Tranco CSV is copied into the repo
- [ ] the supplement helper remains backward-compatible
- [ ] the helper can now target only `top_1_10000`
- [ ] new `top_1_10000` batch numbering starts after `0004`
- [ ] a new replenishment summary JSON is written
- [ ] no old Tranco split artifact was overwritten
- [ ] continuity docs reflect that `top_1_10000_batch_0005` is available again
- [ ] final response states whether the remaining already-split inventory is enough under the `~50%` effective-yield assumption
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] the new source CSV was copied into the repo successfully
- [ ] the script still runs with the old required arguments
- [ ] the bucket-restricted invocation generates only `top_1_10000` output
- [ ] the new summary JSON matches actual generated files
- [ ] the tracker continuity note reflects the replenishment

Commands to run if applicable:

```bash
python scripts/data/benign/split_tranco_supplement.py --source_csv "<repo-local-source-copy>"
python scripts/data/benign/split_tranco_supplement.py --source_csv "<repo-local-source-copy>" --bucket_labels top_1_10000 --summary_name "<new-summary>.json"
python -m py_compile scripts/data/benign/split_tranco_supplement.py
```

Expected evidence to capture:

- repo-local source path
- generated `top_1_10000` file inventory
- new summary JSON
- remaining-inventory estimate before and after replenishment

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-15_tranco_top_1_10000_replenishment_split.md`

---

## 13. Open Questions / Blocking Issues

- none
