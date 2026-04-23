# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-22-four-family-cluster-pool-scope-and-cap-relaxation
- Related Task ID: TASK-2026-04-22-FOUR-FAMILY-CLUSTER-POOL-SCOPE-AND-CAP-RELAXATION
- Task Title: 将当前 malicious advanced cluster/pool 默认范围扩到 Roblox + Netflix + Trezor + Ledger，并放宽默认 family share cap
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-22
- Status: DONE

---

## 1. Executive Summary

本次交付没有改写 Warden V1 的通用 malicious cluster / subcluster / train-reserve 能力边界，只把 **当前默认活动 advanced scope** 从 `roblox,netflix` 扩到 `roblox,netflix,trezor,ledger`。  
同时，把当前默认 `family_share_cap` 从 `0.10` 放宽到 `0.25`，降低默认 train-pool 压缩强度，但保留按 family 做上限压缩的机制与 CLI 覆盖能力。

---

## 2. What Changed

### Code Changes

- 在 `scripts/data/common/pool_utils.py` 中将默认 advanced family 集合从 `("netflix", "roblox")` 调整为 `("ledger", "netflix", "roblox", "trezor")`。
- 在 `scripts/data/malicious/build_malicious_clusters.py`、`scripts/data/malicious/build_malicious_train_pool.py`、`scripts/data/maintenance/build_dedup_review_manifest.py`、`scripts/data/maintenance/build_training_exclusion_lists.py` 中，把 `--advanced_family_brands` 的默认值从 `roblox,netflix` 调整为 `roblox,netflix,trezor,ledger`。
- 在 `scripts/data/malicious/build_malicious_train_pool.py` 与 `scripts/data/maintenance/backfill_existing_sample_fingerprints.py` 中，把默认 `family_share_cap` 从 `0.10` 调整为 `0.25`。

### Doc Changes

- 更新 `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`，明确当前默认 advanced rollout scope 现在是 Roblox + Netflix + Trezor + Ledger，并记录当前默认 `family_share_cap = 0.25` 仍可通过 CLI 覆盖。
- 更新 `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`，同步写清当前活动 rollout scope 与默认 cap 的实现状态。
- 新增任务单：`docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`。
- 新增本次 handoff 文档。

### Output / Artifact Changes

- 默认 cluster / train-pool / review / exclusion advanced 路径现在只覆盖 Roblox、Netflix、Trezor、Ledger 四类 family。
- 默认 `pool_summary.json` 与 backfill pool summary 现在会报告 `family_share_cap = 0.25`。
- 样本目录结构、冻结字段名、冻结文件名、三池概念和 `--advanced_family_brands all` escape hatch 未改。

---

## 3. Files Touched

- `docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/handoff/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`

Optional notes per file:

- 本次没有改动任何 frozen schema 字段、frozen file name 或目录契约。
- `backfill_existing_sample_fingerprints.py` 本次只同步默认 `family_share_cap`，没有顺手为其新增 `advanced_family_brands` gating。
- 其他工作树里的 data-externalization 相关脏改未触碰。

---

## 4. Behavior Impact

### Expected New Behavior

- 默认运行 `build_malicious_clusters.py` 时，advanced cluster 输出现在只包含 Roblox、Netflix、Trezor、Ledger 四类 family。
- 默认运行 `build_malicious_train_pool.py` 时，advanced train/reserve 路径现在只对这四类 family 生效。
- 默认 review manifest 与 training exclusion 输出现在只覆盖这四类 family 的 advanced records。
- 默认 `family_share_cap` 现在是 `0.25`，单 family 的 train-pool 压缩强度低于原来的 `0.10`。

### Preserved Behavior

- 更宽的 V1 cluster -> subcluster -> train/reserve 通用能力边界仍保留。
- 非目标 family 仍不得默认进入更广的 advanced cluster / subcluster / train-reserve 路径。
- `--advanced_family_brands all` 仍然可用，用于显式回到更宽的 all-family advanced capability。
- `--family_share_cap` 参数名不变，仍然可以显式覆盖默认值。
- `backfill_existing_sample_fingerprints.py` 仍然是全输入 roots 的 maintenance/backfill 路径；本次没有把它改造成新的 family-gated advanced orchestrator。

### User-facing / CLI Impact

- CLI 参数名未变：`--advanced_family_brands`
- CLI 参数名未变：`--family_share_cap`
- 默认行为变化：
  - `--advanced_family_brands` 的默认等效值从 `roblox,netflix` 变为 `roblox,netflix,trezor,ledger`
  - `--family_share_cap` 的默认值从 `0.10` 变为 `0.25`，影响 train-pool 与 backfill maintenance 默认压缩强度

### Output Format Impact

- 输出结构未变
- 默认 advanced 输出范围变了
- 默认 pool summary / backfill pool summary 里的 `family_share_cap` 数值变了

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/common/pool_utils.py` default advanced family scope
- `scripts/data/malicious/build_malicious_clusters.py` default `--advanced_family_brands`
- `scripts/data/malicious/build_malicious_train_pool.py` default `--advanced_family_brands` and default `--family_share_cap`
- `scripts/data/maintenance/build_dedup_review_manifest.py` default `--advanced_family_brands`
- `scripts/data/maintenance/build_training_exclusion_lists.py` default `--advanced_family_brands`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py` default `--family_share_cap`

Compatibility notes:

没有修改任何 frozen sample schema、字段名、文件名或目录契约。  
接口变化全部体现在默认行为，而不是参数名、输出结构或 entrypoint 删除。  
现有命令仍然可运行；如果要恢复旧的更窄 advanced family 默认范围或更激进的 cap，用户可以显式传原参数值。  
若磁盘上已有旧默认生成的 cluster / pool / review / exclusion 产物，需要重跑相关脚本，默认行为才会反映这次新范围和新 cap。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py scripts/data/maintenance/backfill_existing_sample_fingerprints.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/maintenance/backfill_existing_sample_fingerprints.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\default_clusters_abs
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs\malicious_cluster_records.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs\malicious_cluster_records.jsonl --pool_decisions_path E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs\pool_decisions.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_review_from_all_abs
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs\pool_decisions.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_exclusions_from_all_abs
python scripts/data/maintenance/backfill_existing_sample_fingerprints.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\backfill_abs --emit_review_manifest --emit_exclusion_list
```

### Result

- `py_compile` passed.
- All five affected CLIs still expose normal `--help` output.
- Synthetic smoke input used 10 sample directories:
  - target families: 3 `roblox`, 2 `netflix`, 2 `trezor`, 2 `ledger`
  - control family: 1 `microsoft`
- Default cluster output contained 9 records and included only `roblox`, `netflix`, `trezor`, and `ledger`.
- All-family control cluster output contained 10 records and additionally included `microsoft`.
- Default train-pool summary reported:
  - `total_records = 9`
  - `train_count = 8`
  - `reserve_count = 1`
  - `reject_count = 0`
  - `family_share_cap = 0.25`
- In that smoke case, the only overflow moved to reserve was one extra `roblox` record, with `reason_code = family_share_cap`.
- Default review manifest output contained 9 rows covering only the four target families.
- Default exclusion list output contained 1 row with `reason_code = family_share_cap`.
- Backfill maintenance summary reported `family_share_cap = 0.25`, confirming the relaxed default also reached the backfill maintenance path.

### Not Run

- real-sample smoke over local Trezor malicious samples
- real-sample smoke over local Ledger malicious samples
- broader regression over historical malicious datasets
- end-to-end revalidation of non-target-family basic ingest/archive path

Reason:

当前线程没有提供可直接复用的本地 Trezor / Ledger 真实 malicious 样本，因此最小验证使用了可审计 synthetic sample dirs。  
验证已经覆盖语法、CLI 可见性、默认 family gate、`all` control run，以及新的默认 `family_share_cap = 0.25` 行为边界。更大范围回归不属于本次最小补丁验证范围。

---

## 7. Risks / Caveats

- 当前四-family matcher 仍依赖 `claimed_brands` 与 `family_key` token；若 Trezor 或 Ledger 样本两者都未命中，仍可能保守地留在 basic path。
- 本次 Trezor / Ledger 验证依赖 synthetic smoke，而不是本地真实 malicious 样本。
- 默认 `family_share_cap = 0.25` 只是较温和的放宽，不是数据驱动调参结论；更优默认值仍应基于真实分布再评估。
- `backfill_existing_sample_fingerprints.py` 仍不是 family-gated advanced orchestrator；本次只同步它的默认 cap，避免其默认压缩强度与 active train-pool 路径不一致。

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/handoff/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 如有本地真实 Trezor / Ledger malicious 样本，补一轮真实数据 smoke，替换当前 synthetic-only 证据。
- 用新的默认范围与 `family_share_cap = 0.25` 重建实际需要保留的 advanced cluster / pool / review / exclusion 产物，避免继续沿用旧默认产物。
- 二审时重点确认：`0.25` 作为默认 cap 是否满足当前数据分布；如果仍偏紧或偏松，再开单独任务做参数评估，而不要顺手改成全局 cluster/pool 重写。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-22-four-family-cluster-pool-scope-and-cap-relaxation
- Related Task ID: TASK-2026-04-22-FOUR-FAMILY-CLUSTER-POOL-SCOPE-AND-CAP-RELAXATION
- Task Title: Expand the current malicious advanced cluster/pool scope to Roblox, Netflix, Trezor, and Ledger, and relax the default family share cap
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-22
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

This delivery did not redesign the Warden V1 general malicious cluster / subcluster / train-reserve capability boundary.  
It widened the **current default active advanced scope** from `roblox,netflix` to `roblox,netflix,trezor,ledger`.  
It also relaxed the default `family_share_cap` from `0.10` to `0.25`, reducing the default train-pool compression strength while preserving bounded family-share control and explicit CLI override.

---

## 2. What Changed

### Code Changes

- In `scripts/data/common/pool_utils.py`, changed the default advanced family tuple from `("netflix", "roblox")` to `("ledger", "netflix", "roblox", "trezor")`.
- In `scripts/data/malicious/build_malicious_clusters.py`, `scripts/data/malicious/build_malicious_train_pool.py`, `scripts/data/maintenance/build_dedup_review_manifest.py`, and `scripts/data/maintenance/build_training_exclusion_lists.py`, changed the default `--advanced_family_brands` value from `roblox,netflix` to `roblox,netflix,trezor,ledger`.
- In `scripts/data/malicious/build_malicious_train_pool.py` and `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`, changed the default `family_share_cap` from `0.10` to `0.25`.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md` so the current default advanced rollout scope is now explicitly Roblox + Netflix + Trezor + Ledger, and so the current default `family_share_cap = 0.25` is recorded as an implementation detail with CLI override still available.
- Updated `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` with the same active rollout scope and default-cap implementation statement.
- Added the task doc `docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`.
- Added this handoff document.

### Output / Artifact Changes

- The default advanced cluster / train-pool / review / exclusion path now covers only the Roblox, Netflix, Trezor, and Ledger families.
- Default `pool_summary.json` and backfill pool summaries now report `family_share_cap = 0.25`.
- Sample-directory structure, frozen field names, frozen file names, the three-pool concept, and the `--advanced_family_brands all` escape hatch were preserved.

---

## 3. Files Touched

- `docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/handoff/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`

Optional notes per file:

- No frozen schema field, frozen file name, or directory contract was changed.
- `backfill_existing_sample_fingerprints.py` was only aligned on the default `family_share_cap`; it was not expanded into a new family-gated advanced orchestrator in this task.
- The unrelated dirty data-externalization changes already present in the worktree were not touched.

---

## 4. Behavior Impact

### Expected New Behavior

- Running `build_malicious_clusters.py` with defaults now emits advanced cluster records only for Roblox, Netflix, Trezor, and Ledger.
- Running `build_malicious_train_pool.py` with defaults now applies the advanced train/reserve path only to those four families.
- Running the default review-manifest and training-exclusion builders now covers only advanced records from those four families.
- The default `family_share_cap` is now `0.25`, so the default family-level train-pool compression is less aggressive than before.

### Preserved Behavior

- The broader V1 cluster -> subcluster -> train/reserve capability boundary remains intact.
- Non-target families still do not enter the broader advanced cluster / subcluster / train-reserve path by default.
- `--advanced_family_brands all` remains available as the explicit escape hatch back to the broader all-family advanced capability.
- The `--family_share_cap` parameter name is unchanged and can still override the default explicitly.
- `backfill_existing_sample_fingerprints.py` remains a full-input maintenance/backfill path; this task did not convert it into a new family-gated advanced-scope orchestrator.

### User-facing / CLI Impact

- CLI parameter name unchanged: `--advanced_family_brands`
- CLI parameter name unchanged: `--family_share_cap`
- Default behavior changed:
  - the effective default `--advanced_family_brands` value is now `roblox,netflix,trezor,ledger`
  - the default `--family_share_cap` value is now `0.25` instead of `0.10`, affecting default train-pool and backfill maintenance compression strength

### Output Format Impact

- Output structure unchanged
- Default advanced output scope changed
- The `family_share_cap` value reported in default pool summaries changed

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/common/pool_utils.py` default advanced family scope
- `scripts/data/malicious/build_malicious_clusters.py` default `--advanced_family_brands`
- `scripts/data/malicious/build_malicious_train_pool.py` default `--advanced_family_brands` and default `--family_share_cap`
- `scripts/data/maintenance/build_dedup_review_manifest.py` default `--advanced_family_brands`
- `scripts/data/maintenance/build_training_exclusion_lists.py` default `--advanced_family_brands`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py` default `--family_share_cap`

Compatibility notes:

No frozen sample schema, field name, file name, or directory contract was changed.  
All interface changes are default-behavior changes only; there was no parameter rename, no output-structure change, and no entrypoint removal.  
Existing commands still run; if the old narrower advanced-family default or the old more aggressive cap is needed, the user can pass the old values explicitly.  
If older cluster / pool / review / exclusion artifacts already exist on disk, the relevant scripts must be rerun for the new default scope and cap to appear in those outputs.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py scripts/data/maintenance/backfill_existing_sample_fingerprints.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/maintenance/backfill_existing_sample_fingerprints.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\default_clusters_abs
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs\malicious_cluster_records.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path E:\Warden\tmp\four_family_scope_smoke\all_clusters_abs\malicious_cluster_records.jsonl --pool_decisions_path E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs\pool_decisions.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_review_from_all_abs
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path E:\Warden\tmp\four_family_scope_smoke\default_pool_from_all_abs\pool_decisions.jsonl --output_dir E:\Warden\tmp\four_family_scope_smoke\default_exclusions_from_all_abs
python scripts/data/maintenance/backfill_existing_sample_fingerprints.py --input_roots E:\Warden\tmp\four_family_scope_smoke\input_samples --output_dir E:\Warden\tmp\four_family_scope_smoke\backfill_abs --emit_review_manifest --emit_exclusion_list
```

### Result

- `py_compile` passed.
- All five affected CLIs still show normal `--help` output.
- The synthetic smoke input used 10 sample directories:
  - target families: 3 `roblox`, 2 `netflix`, 2 `trezor`, 2 `ledger`
  - control family: 1 `microsoft`
- The default cluster output contained 9 records and included only `roblox`, `netflix`, `trezor`, and `ledger`.
- The all-family control cluster output contained 10 records and additionally included `microsoft`.
- The default train-pool summary reported:
  - `total_records = 9`
  - `train_count = 8`
  - `reserve_count = 1`
  - `reject_count = 0`
  - `family_share_cap = 0.25`
- In that smoke case, the only overflow moved to reserve was one extra `roblox` record with `reason_code = family_share_cap`.
- The default review manifest contained 9 rows covering only the four target families.
- The default exclusion list contained 1 row with `reason_code = family_share_cap`.
- The backfill maintenance summary reported `family_share_cap = 0.25`, confirming that the relaxed default also reached the backfill maintenance path.

### Not Run

- a real-sample smoke over local Trezor malicious samples
- a real-sample smoke over local Ledger malicious samples
- a broader regression over historical malicious datasets
- end-to-end revalidation of the non-target-family basic ingest/archive path

Reason:

No directly reusable local Trezor or Ledger malicious samples were provided in this thread, so the minimum validation used auditable synthetic sample directories.  
The executed checks still covered syntax, CLI visibility, default family gating, the `all` control run, and the new default `family_share_cap = 0.25` behavior boundary. Broader regression was outside this minimal patch scope.

---

## 7. Risks / Caveats

- The four-family matcher still depends on `claimed_brands` and `family_key` tokenization; if Trezor or Ledger samples miss both signals, they may still conservatively remain on the basic path.
- Trezor and Ledger validation in this thread depends on synthetic smoke rather than real local malicious samples.
- The default `family_share_cap = 0.25` is a moderate relaxation, not a data-driven optimum; a better default may still need later tuning against real distribution statistics.
- `backfill_existing_sample_fingerprints.py` still is not a family-gated advanced orchestrator; this task only aligned its default cap so its maintenance compression would not stay harsher than the active train-pool path.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`
- `docs/handoff/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If real local Trezor / Ledger malicious samples are available, add one real-data smoke run to replace the current synthetic-only evidence.
- Rebuild the actual advanced cluster / pool / review / exclusion artifacts with the new default scope and `family_share_cap = 0.25`, so older outputs do not remain the active reference by inertia.
- In review, check whether `0.25` is the right default cap for the current data distribution; if it is still too tight or too loose, open a separate parameter-evaluation task rather than expanding this into a global cluster/pool rewrite.
