# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-02-roblox-only-cluster-pool-scope-tightening
- Related Task ID: TASK-2026-04-02-ROBLOX-ONLY-CLUSTER-POOL-SCOPE-TIGHTENING
- Task Title: 将当前 malicious cluster / pool 高级执行范围收紧为仅 Roblox family
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-02
- Status: DONE

---

## 1. Executive Summary

本次交付没有推翻 Warden V1 的恶性 cluster / subcluster / train-reserve 通用能力边界，而是把**当前默认活动执行范围**明确收紧为 **Roblox family only**。  
代码上新增了可审计的 family-scope 过滤，默认值为 `roblox`，并保留 `all` 这样的加性回退开关；文档上同步明确区分了“V1 通用能力边界”和“当前阶段实际 rollout 范围”。

---

## 2. What Changed

### Code Changes

- 在 `scripts/data/common/pool_utils.py` 中新增 Roblox-only advanced scope 解析与匹配辅助函数，默认高级 family scope 为 `roblox`，并允许用 `all` 保留全家族高级路径。
- 更新 `scripts/data/malicious/build_malicious_clusters.py`，默认只把 Roblox family 样本写入高级 cluster/subcluster 输出。
- 更新 `scripts/data/malicious/build_malicious_train_pool.py`，即便输入的是全家族 cluster records，默认 train/reserve 也只对 Roblox family 生效。
- 更新 `scripts/data/maintenance/build_dedup_review_manifest.py` 与 `scripts/data/maintenance/build_training_exclusion_lists.py`，默认只对 Roblox advanced scope 产出 review / exclusion 输出。

### Doc Changes

- 更新 `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`，明确：
  - V1 通用能力边界仍保留
  - 当前默认高级 cluster/pool rollout 只对 Roblox family 启用
  - 非 Roblox family 仅保留基础 ingest/archive 路径和可选 exact-URL hygiene dedup
- 更新 `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`，明确同样的 rollout 收紧结论，并说明非 Roblox family 当前不默认进入高级 cluster/subcluster/train-pool 链路。
- 将外部任务单落入仓库：`docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- 新增本 handoff 文档。

### Output / Artifact Changes

- 高级 cluster / train-pool / review / exclusion 脚本默认只处理 Roblox family advanced scope。
- CLI 新增加性参数 `--advanced_family_brands`；默认值等效于 `roblox`，传 `all` 可恢复全家族高级路径。
- 样本目录结构、冻结字段名、冻结文件名、三池概念和下游 sample schema 未改动。

---

## 3. Files Touched

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`

Optional notes per file:

- `pool_utils.py` 是这次最小共享逻辑落点；没有改动 frozen sample schema。
- 四个脚本都采用加性 CLI 方式暴露 family scope，没有删除原有 entrypoint。
- task doc 从仓库外路径复制进 repo，是为了满足 non-trivial 任务的持续协作追踪要求。

---

## 4. Behavior Impact

### Expected New Behavior

- 默认运行 `build_malicious_clusters.py` 时，只有 Roblox family 会进入高级 cluster/subcluster 输出。
- 默认运行 `build_malicious_train_pool.py` 时，只有 Roblox family 会进入高级 train/reserve 决策，即便输入 cluster records 来自全家族数据。
- 默认运行 review manifest / training exclusion 脚本时，只会为 Roblox advanced scope 产出高级维护输出。
- 需要保留 V1 全家族高级能力时，必须显式传 `--advanced_family_brands all`。

### Preserved Behavior

- Warden V1 的 archive / train / reserve 三池概念保留不变。
- 恶性 cluster -> subcluster -> train/reserve 的通用能力边界保留不变，没有被文档或代码删除。
- 冻结 sample 输出结构、冻结字段名、冻结文件名、capture engine 和 benign pipeline 均未改动。
- `family_share_cap` 仍然存在，且仍是加性 CLI 配置项。

### User-facing / CLI Impact

- 新增加性 CLI 参数：`--advanced_family_brands`
- 默认值收紧为 Roblox-only advanced scope
- 若要恢复全家族高级路径，需显式传 `--advanced_family_brands all`

### Output Format Impact

- 样本级输出格式：无变化
- cluster / train-pool / review / exclusion 的**默认内容范围**变化为 Roblox-only advanced scope
- CLI 暴露发生加性变化，非破坏性

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/build_malicious_clusters.py` CLI
- `scripts/data/malicious/build_malicious_train_pool.py` CLI
- `scripts/data/maintenance/build_dedup_review_manifest.py` CLI
- `scripts/data/maintenance/build_training_exclusion_lists.py` CLI

Compatibility notes:

没有修改任何冻结 sample schema、字段名、文件名或目录契约。  
接口变化仅限四个脚本新增了加性参数 `--advanced_family_brands`，旧命令仍可运行；只是默认高级处理范围从“隐式全家族”收紧为“显式 Roblox-only”。  
若已有历史全家族 advanced cluster/pool 产物，用户需要重跑这些脚本，默认行为才会反映本次 scope tightening。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots data/raw/phish --output_dir tmp/roblox_scope_smoke/default_clusters
python scripts/data/malicious/build_malicious_clusters.py --input_roots data/raw/phish --output_dir tmp/roblox_scope_smoke/all_clusters --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path tmp/roblox_scope_smoke/all_clusters/malicious_cluster_records.jsonl --output_dir tmp/roblox_scope_smoke/default_pool_from_all
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path tmp/roblox_scope_smoke/all_clusters/malicious_cluster_records.jsonl --pool_decisions_path tmp/roblox_scope_smoke/default_pool_from_all/pool_decisions.jsonl --output_dir tmp/roblox_scope_smoke/default_review_from_all
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path tmp/roblox_scope_smoke/default_pool_from_all/pool_decisions.jsonl --output_dir tmp/roblox_scope_smoke/default_exclusions_from_all
```

### Result

- `py_compile` 通过。
- 四个相关脚本的 `--help` 均显示了新的加性参数 `--advanced_family_brands`。
- 基于本地 5 个 malicious 样本的 smoke run 中：
  - 默认 cluster 输出为 4 条，且全部为 `roblox`
  - `--advanced_family_brands all` 的 control run 输出为 5 条，其中包含 1 条 `microsoft` 和 4 条 `roblox`
- 使用全家族 cluster 输入再跑默认 train pool 时，输出 decision 只有 4 条 Roblox，说明默认 train/reserve 也会再次收紧到 Roblox-only。
- review manifest 默认输出 4 条 Roblox advanced records。
- exclusion list 默认输出 3 条 Roblox reserve records。

### Not Run

- 基于大批量历史 malicious 数据的全量重建
- 非 Roblox basic ingest/archive 路径的 end-to-end 上游运行验证
- `--advanced_family_brands` 多品牌逗号列表的额外组合测试

Reason:

本任务按最小必要验证执行，已覆盖语法、CLI 可见性，以及真实 mixed-family 样本上的 Roblox-only default behavior。  
全量历史重建和更大范围回归不属于本次最小补丁验证范围。

---

## 7. Risks / Caveats

- 当前 Roblox matcher 依赖已有 `claimed_brands` 与 `family_key` token；若某些 Roblox 样本品牌抽取失败且 family token 也未命中，可能会被保守地留在 basic path。
- 历史上已经生成的全家族 advanced cluster/pool 输出不会被自动重写；要获得新默认行为，必须重跑相关脚本。
- 若后续确实要对更多 malicious family 启用高级 cluster/pool，需要先补任务单并明确 rollout 扩张，而不是直接改默认值。

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 用当前默认配置对需要保留的 malicious advanced artifacts 做一次正式重建，替换旧的全家族 cluster/pool 输出。
- 若后续要扩大 advanced family scope，先基于重复度证据补一份新 task，而不是直接把默认值从 `roblox` 改回全量。
- 二审时请重点确认：当前代码与文档是否都已明确区分 “V1 通用能力边界” 和 “当前 Roblox-only rollout 范围”。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-02-roblox-only-cluster-pool-scope-tightening
- Related Task ID: TASK-2026-04-02-ROBLOX-ONLY-CLUSTER-POOL-SCOPE-TIGHTENING
- Task Title: Tighten the current malicious advanced cluster/pool execution scope to Roblox family only
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-02
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

This delivery did not reverse the Warden V1 general malicious cluster / subcluster / train-reserve capability boundary.  
Instead, it made the **current default active execution scope** explicitly **Roblox-family-only**.  
Code now applies an auditable family-scope filter whose default is `roblox`, while keeping an additive fallback such as `all`; the docs were updated in parallel to distinguish the broader V1 capability boundary from the current rollout scope.

---

## 2. What Changed

### Code Changes

- Added Roblox-only advanced-scope parsing and matching helpers to `scripts/data/common/pool_utils.py`; the default advanced family scope is now `roblox`, with `all` preserving the broader V1 path.
- Updated `scripts/data/malicious/build_malicious_clusters.py` so the default advanced cluster/subcluster output contains only Roblox-family records.
- Updated `scripts/data/malicious/build_malicious_train_pool.py` so default train/reserve decisions are Roblox-only even when the input cluster file contains multiple families.
- Updated `scripts/data/maintenance/build_dedup_review_manifest.py` and `scripts/data/maintenance/build_training_exclusion_lists.py` so their default advanced maintenance outputs stay Roblox-only as well.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md` to state explicitly that:
  - the V1 general capability boundary remains intact,
  - the current default advanced cluster/pool rollout is Roblox-family-only,
  - non-Roblox families currently remain on the basic ingest/archive path with optional exact-URL hygiene dedup only.
- Updated `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` to state the same rollout tightening and to clarify that non-Roblox families do not enter the advanced cluster/subcluster/train-pool chain by default at the current stage.
- Copied the external task doc into the repository at `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`.
- Added this handoff document.

### Output / Artifact Changes

- The default advanced cluster / train-pool / review / exclusion scripts now process only the Roblox-family advanced scope.
- Added an additive CLI parameter: `--advanced_family_brands`; its default behavior is equivalent to `roblox`, while `all` preserves the broader V1 capability.
- Sample-directory structure, frozen field names, frozen file names, the three-pool concept, and downstream sample schema were not changed.

---

## 3. Files Touched

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`

Optional notes per file:

- `pool_utils.py` is the only shared logic touchpoint in this patch; no frozen sample schema was changed there.
- All four scripts expose the new family scope as additive CLI, without deleting any existing entrypoint.
- The repo task doc was copied in from an external path to keep this non-trivial task tracked inside the repository.

---

## 4. Behavior Impact

### Expected New Behavior

- Running `build_malicious_clusters.py` with defaults now sends only Roblox-family samples into the advanced cluster/subcluster output.
- Running `build_malicious_train_pool.py` with defaults now sends only Roblox-family samples into advanced train/reserve decisions, even if the cluster input file contains multiple families.
- Running the review-manifest and training-exclusion builders with defaults now emits advanced maintenance outputs only for the Roblox scope.
- Preserving the broader V1 all-family advanced path now requires an explicit `--advanced_family_brands all`.

### Preserved Behavior

- The Warden V1 archive / train / reserve three-pool concept remains unchanged.
- The general malicious cluster -> subcluster -> train/reserve capability boundary remains intact in both docs and code.
- Frozen sample output structure, frozen field names, frozen file names, the capture engine, and the benign pipeline were not changed.
- `family_share_cap` still exists and remains an additive CLI configuration item.

### User-facing / CLI Impact

- New additive CLI parameter: `--advanced_family_brands`
- Default advanced scope is now tightened to Roblox-only
- Restoring all-family advanced behavior requires an explicit `--advanced_family_brands all`

### Output Format Impact

- Sample-level output format: unchanged
- The **default output scope** of cluster / train-pool / review / exclusion artifacts is now Roblox-only for the advanced path
- CLI exposure changed additively, not destructively

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/build_malicious_clusters.py` CLI
- `scripts/data/malicious/build_malicious_train_pool.py` CLI
- `scripts/data/maintenance/build_dedup_review_manifest.py` CLI
- `scripts/data/maintenance/build_training_exclusion_lists.py` CLI

Compatibility notes:

No frozen sample schema, field name, file name, or directory contract was changed.  
The only interface change is the additive CLI parameter `--advanced_family_brands` on four scripts. Existing commands remain runnable; the main behavioral tightening is that the default advanced-processing scope is now explicitly Roblox-only instead of implicitly applying to every family.  
If older all-family advanced cluster/pool artifacts already exist on disk, they must be rebuilt for the new default scope tightening to take effect in those outputs.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots data/raw/phish --output_dir tmp/roblox_scope_smoke/default_clusters
python scripts/data/malicious/build_malicious_clusters.py --input_roots data/raw/phish --output_dir tmp/roblox_scope_smoke/all_clusters --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path tmp/roblox_scope_smoke/all_clusters/malicious_cluster_records.jsonl --output_dir tmp/roblox_scope_smoke/default_pool_from_all
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path tmp/roblox_scope_smoke/all_clusters/malicious_cluster_records.jsonl --pool_decisions_path tmp/roblox_scope_smoke/default_pool_from_all/pool_decisions.jsonl --output_dir tmp/roblox_scope_smoke/default_review_from_all
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path tmp/roblox_scope_smoke/default_pool_from_all/pool_decisions.jsonl --output_dir tmp/roblox_scope_smoke/default_exclusions_from_all
```

### Result

- `py_compile` passed.
- All four affected scripts show the new additive `--advanced_family_brands` parameter in `--help`.
- In a smoke run over 5 local malicious samples:
  - the default cluster output contained 4 records and all were `roblox`,
  - the `--advanced_family_brands all` control run contained 5 records: 1 `microsoft` and 4 `roblox`.
- Running the default train-pool builder against the all-family cluster file still produced only 4 Roblox decisions, confirming that the default train/reserve path also re-tightens itself to Roblox-only.
- The default review manifest emitted 4 Roblox advanced records.
- The default exclusion list emitted 3 Roblox reserve records.

### Not Run

- full rebuild over larger historical malicious datasets
- end-to-end upstream validation of the non-Roblox basic ingest/archive path
- extra combinational testing for multi-brand comma-separated `--advanced_family_brands` values

Reason:

This task used minimum necessary validation. The executed checks covered syntax, CLI visibility, and real mixed-family smoke behavior for the tightened Roblox-only default.  
Full historical rebuilds and broader regression passes were outside the intended validation scope for this minimal patch.

---

## 7. Risks / Caveats

- The current Roblox matcher depends on existing `claimed_brands` and `family_key` tokenization; if some Roblox samples miss both signals, they may conservatively remain on the basic path.
- Older all-family advanced cluster/pool artifacts already on disk are not rewritten automatically; the relevant scripts must be rerun to materialize the new default scope in those outputs.
- If more malicious families should later enter the advanced path, that rollout expansion should happen through a new scoped task rather than by silently changing the default again.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- Rebuild the required malicious advanced artifacts with the new default so older all-family cluster/pool outputs are no longer the active ones.
- If the advanced family scope should expand later, create a new task backed by duplication evidence instead of changing the default from `roblox` back to all families without review.
- In review, check specifically that the code and docs now distinguish the “general V1 capability boundary” from the “current Roblox-only rollout scope.”
