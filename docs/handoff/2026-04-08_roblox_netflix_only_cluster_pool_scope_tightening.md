# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-08-roblox-netflix-only-cluster-pool-scope-tightening
- Related Task ID: TASK-2026-04-08-ROBLOX-NETFLIX-ONLY-CLUSTER-POOL-SCOPE-TIGHTENING
- Task Title: 将当前 malicious cluster / pool 高级执行范围收紧为仅 Roblox + Netflix families
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-08
- Status: DONE

---

## 1. Executive Summary

本次交付没有推翻 Warden V1 的恶性 cluster / subcluster / train-reserve 通用能力边界，而是把**当前默认活动执行范围**从 **Roblox-only** 调整为 **Roblox + Netflix only**。  
代码上复用了已有的 family-scope 过滤机制，只把默认 advanced scope 从 `roblox` 扩到 `roblox,netflix`；文档上同步明确区分了“V1 通用能力边界”和“当前阶段实际 rollout 范围”。

---

## 2. What Changed

### Code Changes

- 在 `scripts/data/common/pool_utils.py` 中将默认高级 family scope 从 `roblox` 调整为 `("netflix", "roblox")`。
- 更新 `scripts/data/malicious/build_malicious_clusters.py`，默认 advanced cluster/subcluster 输出现在只包含 Roblox 和 Netflix families。
- 更新 `scripts/data/malicious/build_malicious_train_pool.py`，默认 train/reserve 现在只对 Roblox 和 Netflix families 生效。
- 更新 `scripts/data/maintenance/build_dedup_review_manifest.py` 与 `scripts/data/maintenance/build_training_exclusion_lists.py`，默认 review / exclusion 输出现在只覆盖 Roblox 和 Netflix advanced scope。

### Doc Changes

- 更新 `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`，明确：
  - V1 通用能力边界仍保留
  - 当前默认高级 cluster/pool rollout 只对 Roblox + Netflix families 启用
  - 其他 malicious families 仅保留基础 ingest/archive 路径和可选 exact-URL hygiene dedup
- 更新 `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`，明确同样的 rollout 收紧结论，并说明其他 families 当前不默认进入高级 cluster/subcluster/train-pool 链路。
- 新增任务单：`docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- 新增本 handoff 文档。

### Output / Artifact Changes

- 高级 cluster / train-pool / review / exclusion 脚本默认只处理 Roblox + Netflix families advanced scope。
- CLI 仍然使用加性参数 `--advanced_family_brands`；默认值行为现在等效于 `roblox,netflix`，传 `all` 仍可恢复全家族高级路径。
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
- `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

Optional notes per file:

- `pool_utils.py` 仍是这次最小共享逻辑落点；没有改动 frozen sample schema。
- 四个脚本继续采用加性 CLI 方式暴露 family scope，没有删除原有 entrypoint。
- 本次没有修改 2026-04-02 的 Roblox 历史 task/handoff；那两份文档保留为历史记录。

---

## 4. Behavior Impact

### Expected New Behavior

- 默认运行 `build_malicious_clusters.py` 时，只有 Roblox 和 Netflix families 会进入高级 cluster/subcluster 输出。
- 默认运行 `build_malicious_train_pool.py` 时，只有 Roblox 和 Netflix families 会进入高级 train/reserve 决策，即便输入 cluster records 来自全家族数据。
- 默认运行 review manifest / training exclusion 脚本时，只会为 Roblox + Netflix advanced scope 产出高级维护输出。
- 需要保留 V1 全家族高级能力时，仍必须显式传 `--advanced_family_brands all`。

### Preserved Behavior

- Warden V1 的 archive / train / reserve 三池概念保留不变。
- 恶性 cluster -> subcluster -> train/reserve 的通用能力边界保留不变，没有被文档或代码删除。
- 冻结 sample 输出结构、冻结字段名、冻结文件名、capture engine 和 benign pipeline 均未改动。
- `family_share_cap` 仍然存在，且仍是加性 CLI 配置项。

### User-facing / CLI Impact

- CLI 参数名不变：`--advanced_family_brands`
- 默认值行为从 Roblox-only 变为 Roblox+Netflix-only
- 若要恢复全家族高级路径，仍需显式传 `--advanced_family_brands all`

### Output Format Impact

- 样本级输出格式：无变化
- cluster / train-pool / review / exclusion 的**默认内容范围**变化为 Roblox+Netflix-only advanced scope
- CLI 暴露没有破坏性变化

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/build_malicious_clusters.py` CLI default behavior
- `scripts/data/malicious/build_malicious_train_pool.py` CLI default behavior
- `scripts/data/maintenance/build_dedup_review_manifest.py` CLI default behavior
- `scripts/data/maintenance/build_training_exclusion_lists.py` CLI default behavior

Compatibility notes:

没有修改任何冻结 sample schema、字段名、文件名或目录契约。  
接口变化不在参数名，而在四个脚本对 `--advanced_family_brands` 的**默认行为**：从 `roblox` 调整为 `roblox,netflix`。旧命令仍可运行；只是默认高级处理范围从 Roblox-only 收紧为 Roblox+Netflix-only。  
若已有历史 advanced cluster/pool 产物，用户需要重跑这些脚本，默认行为才会反映本次 rollout 调整。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\input_samples --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_clusters_abs
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\input_samples --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs\\malicious_cluster_records.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs\\malicious_cluster_records.jsonl --pool_decisions_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs\\pool_decisions.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_review_from_all_abs
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs\\pool_decisions.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_exclusions_from_all_abs
```

### Result

- `py_compile` 通过。
- 四个相关脚本的 `--help` 均正常。
- 本地 `data/raw/phish` 未找到可用 Netflix-tagged malicious 样本，因此使用了最小 synthetic smoke input：3 个样本目录，分别带 `roblox`、`netflix`、`microsoft` claimed_brands。
- synthetic smoke run 中：
  - 默认 cluster 输出为 2 条，且只包含 `netflix` 和 `roblox`
  - `--advanced_family_brands all` 的 control run 输出为 3 条，包含 `microsoft`、`netflix`、`roblox`
- 使用全家族 cluster 输入再跑默认 train pool 时，输出 decision 只有 2 条，且只包含 `netflix` 和 `roblox`
- review manifest 默认输出 2 条 advanced records，且只包含 `netflix` 和 `roblox`
- exclusion list 默认输出 0 条；这与 synthetic 输入中两个默认 advanced family 都成为 train_candidate 一致

### Not Run

- 基于真实 Netflix malicious 样本的 smoke run
- 基于大批量历史 malicious 数据的全量重建
- 非 Roblox/Netflix basic ingest/archive 路径的 end-to-end 上游运行验证

Reason:

本地当前没有可直接复用的 Netflix-tagged malicious 样本，因此这次最小必要验证采用了可审计 synthetic sample dirs。  
验证已覆盖语法、CLI 可见性，以及默认/对照路径下的 family-scope 行为边界。更大范围回归不属于本次最小补丁验证范围。

---

## 7. Risks / Caveats

- 当前 Netflix matcher 与 Roblox matcher 一样，依赖已有 `claimed_brands` 与 `family_key` token；若某些 Netflix 样本品牌抽取失败且 family token 也未命中，可能会被保守地留在 basic path。
- 这次 Netflix 验证依赖 synthetic smoke input，而不是本地真实 malicious Netflix 样本。
- 历史上已经生成的 advanced cluster/pool 输出不会被自动重写；要获得新默认行为，必须重跑相关脚本。

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 若后续拿到真实 Netflix malicious 样本，补一次真实数据 smoke，替换当前 synthetic-only Netflix 验证证据。
- 用当前默认配置对需要保留的 advanced artifacts 做一次正式重建，替换旧的 Roblox-only 输出。
- 二审时请重点确认：当前代码与文档是否都已明确区分 “V1 通用能力边界” 和 “当前 Roblox+Netflix-only rollout 范围”。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-08-roblox-netflix-only-cluster-pool-scope-tightening
- Related Task ID: TASK-2026-04-08-ROBLOX-NETFLIX-ONLY-CLUSTER-POOL-SCOPE-TIGHTENING
- Task Title: Tighten the current malicious advanced cluster/pool execution scope to Roblox and Netflix families only
- Module: data / malicious-ingest / maintenance / docs
- Author: Codex
- Date: 2026-04-08
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
Instead, it moved the **current default active execution scope** from **Roblox-only** to **Roblox+Netflix-only**.  
Code reused the existing family-scope gating mechanism and only expanded the default advanced scope from `roblox` to `roblox,netflix`; the docs were updated in parallel to distinguish the broader V1 capability boundary from the current rollout scope.

---

## 2. What Changed

### Code Changes

- Changed the default advanced family scope in `scripts/data/common/pool_utils.py` from `roblox` to `("netflix", "roblox")`.
- Updated `scripts/data/malicious/build_malicious_clusters.py` so the default advanced cluster/subcluster output now contains only Roblox and Netflix families.
- Updated `scripts/data/malicious/build_malicious_train_pool.py` so default train/reserve decisions now apply only to Roblox and Netflix families.
- Updated `scripts/data/maintenance/build_dedup_review_manifest.py` and `scripts/data/maintenance/build_training_exclusion_lists.py` so their default review / exclusion outputs now cover only the Roblox+Netflix advanced scope.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md` to state explicitly that:
  - the V1 general capability boundary remains intact,
  - the current default advanced cluster/pool rollout is enabled only for the Roblox and Netflix families,
  - all other malicious families currently remain on the basic ingest/archive path with optional exact-URL hygiene dedup only.
- Updated `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` to state the same rollout tightening and to clarify that all other families do not enter the advanced cluster/subcluster/train-pool chain by default at the current stage.
- Added the task doc `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`.
- Added this handoff document.

### Output / Artifact Changes

- The default advanced cluster / train-pool / review / exclusion scripts now process only the Roblox and Netflix families.
- CLI still uses the additive `--advanced_family_brands` parameter; the default behavior is now equivalent to `roblox,netflix`, while `all` still preserves the broader all-family V1 path.
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
- `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

Optional notes per file:

- `pool_utils.py` remains the only shared logic touchpoint in this patch; no frozen sample schema was changed there.
- All four scripts continue to expose the family scope as additive CLI without deleting any existing entrypoint.
- The historical 2026-04-02 Roblox task and handoff were kept unchanged as historical records.

---

## 4. Behavior Impact

### Expected New Behavior

- Running `build_malicious_clusters.py` with defaults now sends only Roblox and Netflix families into the advanced cluster/subcluster output.
- Running `build_malicious_train_pool.py` with defaults now sends only Roblox and Netflix families into advanced train/reserve decisions, even if the cluster input file contains additional families.
- Running the review-manifest and training-exclusion builders with defaults now emits advanced maintenance outputs only for the Roblox+Netflix scope.
- Preserving the broader V1 all-family advanced path still requires an explicit `--advanced_family_brands all`.

### Preserved Behavior

- The Warden V1 archive / train / reserve three-pool concept remains unchanged.
- The general malicious cluster -> subcluster -> train/reserve capability boundary remains intact in both docs and code.
- Frozen sample output structure, frozen field names, frozen file names, the capture engine, and the benign pipeline were not changed.
- `family_share_cap` still exists and remains an additive CLI configuration item.

### User-facing / CLI Impact

- CLI parameter name unchanged: `--advanced_family_brands`
- Default behavior changed from Roblox-only to Roblox+Netflix-only
- Restoring all-family advanced behavior still requires an explicit `--advanced_family_brands all`

### Output Format Impact

- Sample-level output format: unchanged
- The **default output scope** of cluster / train-pool / review / exclusion artifacts is now Roblox+Netflix-only for the advanced path
- CLI exposure did not change destructively

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/build_malicious_clusters.py` CLI default behavior
- `scripts/data/malicious/build_malicious_train_pool.py` CLI default behavior
- `scripts/data/maintenance/build_dedup_review_manifest.py` CLI default behavior
- `scripts/data/maintenance/build_training_exclusion_lists.py` CLI default behavior

Compatibility notes:

No frozen sample schema, field name, file name, or directory contract was changed.  
The interface change is not the flag name but the **default behavior** of `--advanced_family_brands` across four scripts: it now defaults to `roblox,netflix` instead of `roblox`. Existing commands remain runnable; the default advanced-processing scope is simply widened from Roblox-only to Roblox+Netflix-only.  
If older advanced cluster/pool artifacts already exist on disk, they must be rebuilt for the new default rollout to take effect in those outputs.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\input_samples --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_clusters_abs
python scripts/data/malicious/build_malicious_clusters.py --input_roots E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\input_samples --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs --advanced_family_brands all
python scripts/data/malicious/build_malicious_train_pool.py --clusters_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs\\malicious_cluster_records.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs
python scripts/data/maintenance/build_dedup_review_manifest.py --clusters_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\all_clusters_abs\\malicious_cluster_records.jsonl --pool_decisions_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs\\pool_decisions.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_review_from_all_abs
python scripts/data/maintenance/build_training_exclusion_lists.py --pool_decisions_path E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_pool_from_all_abs\\pool_decisions.jsonl --output_dir E:\\Warden\\tmp\\roblox_netflix_scope_smoke\\default_exclusions_from_all_abs
```

### Result

- `py_compile` passed.
- All four affected scripts still show normal `--help` output.
- No usable local Netflix-tagged malicious sample was found under the current local malicious dataset, so the minimum validation used synthetic sample directories with `roblox`, `netflix`, and `microsoft` claimed brands.
- In the synthetic smoke run:
  - the default cluster output contained 2 records and included only `netflix` and `roblox`,
  - the `--advanced_family_brands all` control run contained 3 records: `microsoft`, `netflix`, and `roblox`.
- Running the default train-pool builder against the all-family cluster file still produced only 2 decisions, containing only `netflix` and `roblox`.
- The default review manifest emitted 2 advanced records, containing only `netflix` and `roblox`.
- The default exclusion list emitted 0 rows, which matches the synthetic case where both default advanced families remained train candidates.

### Not Run

- a smoke run over real Netflix malicious samples
- a full rebuild over larger historical malicious datasets
- end-to-end upstream validation of the non-Roblox/non-Netflix basic ingest/archive path

Reason:

There was no directly reusable Netflix-tagged malicious sample in the local dataset, so the minimum necessary validation used auditable synthetic sample directories.  
The executed checks still covered syntax, CLI visibility, and the default/control family-scope behavior boundary. Broader regression was outside the intended scope of this minimal patch.

---

## 7. Risks / Caveats

- The Netflix matcher, like the Roblox matcher, depends on existing `claimed_brands` and `family_key` tokenization; if Netflix samples miss both signals, they may conservatively remain on the basic path.
- Netflix validation in this thread depends on synthetic smoke input rather than real local malicious Netflix samples.
- Older advanced cluster/pool artifacts already on disk are not rewritten automatically; the relevant scripts must be rerun to materialize the new default scope in those outputs.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If real Netflix malicious samples become available locally, add one real-data smoke run to replace the current synthetic-only Netflix evidence.
- Rebuild the required advanced artifacts with the new default so older Roblox-only outputs are no longer the active ones.
- In review, check specifically that the code and docs now distinguish the “general V1 capability boundary” from the “current Roblox+Netflix-only rollout scope.”
