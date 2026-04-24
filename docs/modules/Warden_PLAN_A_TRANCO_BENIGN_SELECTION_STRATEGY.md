# Warden_PLAN_A_TRANCO_BENIGN_SELECTION_STRATEGY

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档说明 Plan A 中通过 Tranco 选择 benign capture 批次的策略。
- 它解释为什么使用 Tranco、如何按 rank bucket 选择批次、为什么要避免重复分配，以及为什么后期会出现 Day 17 补量。
- 精确规则、批次状态和兼容性结论以英文版为准。

### 核心结论

- Tranco 用作 benign 候选来源，因为它提供公开、可复现、按流量/排名组织的网站清单。
- Plan A benign 选择优先使用更高排名、更常见的网站区间，再逐步向长尾区间推进。
- 每个 split 批次只分配一次；是否真正进入训练集，还要看 capture 成功、后续去重和 TrainSet V1 admissibility。
- Day 17 把 `tranco_top_100001_500000_batch_0015` 和 `batch_0016` 都纳入补量后，当前 repo-local Tranco benign split inventory 已全部分配。

## English Version

# Warden Plan A Tranco Benign Selection Strategy

## 1. Purpose

This document records the Plan A strategy for selecting benign webpage capture batches from repo-local Tranco split files.
It exists so future batch planning does not rely only on chat context or the compact tracker.

This document describes queue selection only.
It does not redefine TrainSet V1 admission, capture output schema, label semantics, or model training policy.

---

## 2. Why Tranco Is Used For Benign Candidates

Tranco is used as the default benign candidate source for Plan A because it has four useful properties:

- It is public and reproducible enough for audit-oriented dataset construction.
- It ranks real, commonly visited domains rather than synthetic or hand-picked benign examples.
- It can be split into deterministic local URL batches.
- Its rank buckets allow the project to control sample diversity across high-traffic and longer-tail websites.

The working assumption is that high-ranked and mid-ranked Tranco domains are reasonable benign capture candidates.
That assumption does not mean every captured page is automatically a clean training sample.
Final usability still depends on capture success, content availability, deduplication, and the TrainSet V1 admission rules.

---

## 3. Selection Principles

Plan A benign batch selection follows these principles:

- Prefer already-generated repo-local Tranco split files over generating new splits during daily planning.
- Allocate each split batch at most once.
- Prefer higher-rank buckets before lower-rank buckets when multiple unassigned options exist.
- Preserve day-level continuity in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`.
- Keep daily benign-only planning auditable through a task doc plus a vm-prep handoff.
- Do not mark a selected day as `results_received` until returned artifacts are available.

The rank-priority interpretation used in this tracker is:

- `top_1_10000` has the highest benign priority when available.
- `top_10001_100000` follows after higher-rank splits are exhausted or already assigned.
- `top_100001_500000` is used after the higher-priority available buckets are exhausted or already assigned.
- `top_500001_1000000` was used earlier for broader benign diversity and is exhausted in the current Plan A tracker state.

---

## 4. Why This Strategy Is Used

The strategy is deliberately conservative.
It favors reproducibility, auditability, and practical capture yield over one-off manual picking.

The benefits are:

- The queue can be reconstructed from split filenames and tracker rows.
- Later result-receipt docs can compare expected queue membership against returned `benign_capture_run.json` files.
- Duplicate removal can be handled downstream without losing the original queue lineage.
- Daily planning can continue without reusing the same benign URLs by accident.
- The benign pool covers both common sites and progressively lower-rank sites, which helps avoid an overly narrow benign distribution.

The main tradeoff is that Tranco rank is a source-selection heuristic, not a semantic guarantee.
Captured pages can still be unusable, duplicated, unavailable, redirected, parked, adult/gambling-like, gated, or otherwise unsuitable for a final primary benign training set.

---

## 5. Current Plan A Allocation State

As of the 2026-04-24 Day 17 update, the current tracker allocation state is:

- `top_1_10000`: allocated through `tranco_top_1_10000_batch_0006`
- `top_10001_100000`: allocated through `tranco_top_10001_100000_batch_0014`
- `top_500001_1000000`: allocated through `tranco_top_500001_1000000_batch_0006`
- `top_100001_500000`: allocated through `tranco_top_100001_500000_batch_0016`

Day 17 consumes the final remaining repo-local Tranco benign split:

- `tranco_top_100001_500000_batch_0015`
- `tranco_top_100001_500000_batch_0016`

After this update, the current repo-local Tranco benign split inventory is fully allocated.

---

## 6. Operational Rules For Future Planning

Future planning should follow these rules unless the user explicitly changes the strategy:

- If more benign samples are needed after Day 17, first reconcile actual successful and post-dedup counts from returned artifacts.
- Do not infer that the benign target was reached from selected batch count alone.
- If more Tranco benign input is needed, create a new explicit split-generation task before assigning new Day N batches.
- Keep output roots under `E:\WardenData\raw\benign\tranco\...` for Tranco benign capture artifacts.
- Continue using the hardened benign command pattern unless a later task changes the capture contract:
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms 120000`
  - `--nav_timeout_ms 60000`
  - `--goto_wait_until commit`

---

## 7. Compatibility Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI changed: NO
- Output format changed: NO

This document is a planning and audit artifact only.
It does not change scripts, capture outputs, labels, or TrainSet V1 admission rules.
