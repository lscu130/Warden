# Warden_DATA_INGEST_ARCHITECTURE_V1

## 中文版

## 1. 文档目的

本文档定义 Warden V1 的数据摄取架构边界，用于指导 Codex 落地 benign 与 malicious 两条数据管线，并明确：
- 现有 capture 引擎的保留方式
- benign / malicious 两条上层 pipeline 的职责边界
- malicious 的三层样本池、聚类与子簇抽样策略
- 老数据回处理脚本要求

本文档不是训练文档，也不是推理文档。
它只回答以下问题：
- benign 与 malicious 的采样 / 摄取脚本是否共用
- capture 是否需要重写
- malicious 去重与抽样的正确架构是什么
- 老数据应该如何回处理

---

## 2. 结论

Warden V1 的数据摄取应采用：
- **一个共享 capture 引擎**
- **两条独立的数据管线**
  - benign sampling pipeline
  - malicious ingestion pipeline
- **一层公共工具模块**
- **一套统一输出结构**
- **两套不同的业务状态机与准入策略**
- **恶性三层样本池：archive / train / reserve**

直接结论：
1. 不建议把 benign 与 malicious 的策略塞进一个大脚本。
2. 不建议推倒现有 capture 重写。
3. 建议保留现有 capture 作为底层抓取引擎，只做最小必要抽象。
4. 建议新增 benign 与 malicious 两个上层入口脚本。
5. 建议新增老数据回处理脚本，用于 fingerprint 回填、cluster / subcluster 构建、review manifest 生成、训练排除清单生成。

---

## 3. 架构分层

### 3.1 底层：Capture Engine

现有 capture 脚本继续作为低层证据生产引擎，负责：
- 输入 URL
- 打开页面
- 抓取 screenshot / HTML / visible text / forms / redirect / net summary
- 按冻结结构落盘
- 可选写出弱标签或辅助元数据

它不负责：
- benign 分层抽样
- malicious 来源 triage
- 训练切分
- family/template 去重
- 训练池抽样

### 3.2 中层：Common Utilities

共享公共模块，负责：
- URL 规范化
- 域名规范化
- fingerprint 生成
- 近重复度量
- manifest 生成
- 质量检查
- dedup / cluster helper

### 3.3 上层：Benign Pipeline

负责：
- Tranco 分层抽样
- 榜单外可信长尾补充
- 类别 / 页面类型 / 语言覆盖控制
- quality veto
- hard-benign bucket 采样
- benign manifest 输出

### 3.4 上层：Malicious Pipeline

负责：
- OpenPhish Community + PhishTank 摄取
- 页面有效性检查
- URL 级去重
- campaign/template 聚类
- subcluster 切分
- train pool / reserve pool 构建
- malicious manifest 输出

### 3.5 维护层：Maintenance Pipeline

负责：
- 老样本 fingerprint 回填
- 历史样本 cluster / subcluster 构建
- dedup review manifest 生成
- 训练排除清单生成
- 兼容现有目录结构的批量回处理

---

## 4. 与现有 capture 脚本的关系

当前 `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` 已经是完整的抓取引擎，不应被继续扩展为 benign/malicious 策略脚本。

Warden V1 对它的要求是：
- **保留主抓取逻辑**
- **做最小必要抽象改造**
- **移除对交互式 label 选择的依赖**
- **允许上层脚本以无交互方式调用**

允许的小改动：
1. 将交互式 label 选择改成 CLI，例如 `--label benign|phish`。
2. 提供可编排调用入口，允许外部脚本传入 URL 列表与输出根目录。
3. 允许附加外部采样元数据，例如 benign sampling bucket 或 malicious source tag。
4. 保持已冻结输出结构和文件名不变。

不允许的事：
- 不得把 benign / malicious 的策略写死进 capture。
- 不得把 split / sampling / cluster logic 写进 capture 主循环。
- 不得重命名冻结的 top-level 输出文件。
- 不得引入不必要的新依赖。

---

## 5. 推荐目录结构

```text
scripts/
  capture/
    capture_url_v6_optimized_v6_2_plus_labels_brandlex.py

  data/
    common/
      io_utils.py
      url_utils.py
      domain_utils.py
      fingerprint_utils.py
      similarity_utils.py
      dedup_utils.py
      manifest_utils.py
      quality_checks.py

    benign/
      build_benign_candidates.py
      run_benign_capture.py

    malicious/
      ingest_public_malicious_feeds.py
      run_malicious_capture.py
      build_malicious_clusters.py
      build_malicious_train_pool.py

    maintenance/
      backfill_existing_sample_fingerprints.py
      build_dedup_review_manifest.py
      build_training_exclusion_lists.py
```

---

## 6. 恶性数据的三层样本池

## 6.1 Raw Archive

作用：
- 保存原始恶性样本
- 不默认物理删除重复或过量样本
- 支持追溯、再聚类、未来 benchmark 与 campaign 演化分析

## 6.2 Train-Eligible Canonical Pool

作用：
- 作为默认训练主池
- 降低近重复污染
- 防止单一 family 主导
- 保留跨品牌、跨模板、跨场景多样性

## 6.3 Reserve / Holdout Pool

作用：
- 保存近重复、cluster overflow、时间漂移样本
- 作为鲁棒性测试与未来 hard-case 研究储备

原则：
- Raw Archive 保存规模
- Train Pool 保证可学多样性
- Reserve Pool 保存“没进训练但仍有价值”的样本

---

## 7. 恶性去重与抽样架构

## 7.1 不采用固定“每簇最多 15 条”规则

Warden V1 不再采用固定的 per-cluster magic number。

原因：
- 缺乏足够强的公开证据支持某个固定整数作为普适最优值。
- 同一主站下可能存在多个不同模板、阶段、语言与动作页面。
- 只按大簇数量截断，会误伤真正有价值的子模板差异。

因此，V1 冻结的是**流程**：
- cluster first
- subcluster next
- family share cap
- raw/train/reserve 三池分流

## 7.2 推荐层次

### Level 1: Exact URL
- 完全重复 URL 去重

### Level 2: Normalized / Final URL
- 归一化 URL 与最终 URL 去重

### Level 3: Campaign / Template Cluster
- hostname / registrable domain
- path pattern
- DOM/HTML 结构相似
- screenshot 近重复
- text/form 近重复

### Level 4: Subcluster
在大簇内部继续分成子簇，按：
- 模板
- 页面阶段
- 语言
- 品牌壳
- 时间差异

## 7.3 Train Pool 抽样原则

训练池默认执行：
1. 每个子簇至少保留 1 个 canonical 样本。
2. 若子簇存在明确时间差异或页面状态差异，可额外保留少量代表样本。
3. 对单一 family 施加全局 share cap，避免少数 campaign 吞掉训练预算。
4. 从训练池剔除的样本进入 reserve，而不是默认删除。

## 7.4 Family Share Cap

文档冻结原则，不冻结具体数值：
- 任一 family 在训练池中的占比必须被限制。
- 具体阈值应作为配置项，由实现脚本暴露。
- 若 family 占比超标，优先压缩其近重复与同模板子簇，而不是机械压缩所有 family。

---

## 8. Benign 与 Malicious 为什么不能共用单策略脚本

虽然两者最终都调用浏览器抓取，但业务目标不同：

### Benign
- sampling + vetting
- 覆盖来源、类别、页面类型、语言、hard-benign

### Malicious
- ingestion + triage + clustering
- 处理来源、有效性、重复、family dominance、时间信息

如果强行写成一个大脚本，后果通常是：
- 参数过多
- `if benign` / `if malicious` 逻辑四处蔓延
- manifest 语义混乱
- 维护成本持续升高

因此，Warden V1 采用：
**共享底层 capture 与工具层，分开上层 benign / malicious pipeline。**

---

## 9. 老数据回处理要求

V1 必须支持对历史恶性样本进行回处理。

最低要求：
1. 计算并回填 fingerprint
2. 构建 cluster 与 subcluster
3. 生成 review manifest
4. 生成训练排除清单
5. 默认只做“报告 + 标记”，不做物理删除

老数据回处理输出至少应包括：
- sample_id -> fingerprint
- sample_id -> cluster_id
- sample_id -> subcluster_id
- keep_in_train / move_to_reserve / reject
- reason_code

---

## 10. V1 冻结结论

Warden V1 冻结以下结论：
1. Capture 保留为底层证据引擎，不重写。
2. Benign 与 malicious 使用两条独立上层 pipeline。
3. 恶性来源公开基线为 OpenPhish Community + PhishTank。
4. 恶性去重采用 cluster -> subcluster -> train/reserve 三层决策，不冻结固定每簇保留条数。
5. 老数据默认做回处理与标记，不默认物理删除。

---

## English Version

# Warden_DATA_INGEST_ARCHITECTURE_V1

## 1. Purpose

This document defines the Warden V1 data-ingest architecture boundary and guides Codex implementation for:
- how the existing capture engine should be preserved,
- how the benign and malicious upper-layer pipelines should be separated,
- how malicious archive / train / reserve pools should be constructed,
- how legacy-data backfill should be handled.

This is not a training document and not an inference document.
It answers only:
- whether benign and malicious should share one strategy script,
- whether capture should be rewritten,
- what the correct malicious deduplication and sampling architecture should be,
- how historical data should be backfilled.

---

## 2. Frozen Conclusion

Warden V1 data ingest should use:
- **one shared capture engine**,
- **two separate upper-layer pipelines**
  - benign sampling pipeline,
  - malicious ingestion pipeline,
- **one shared common-utilities layer**,
- **one unified output structure**,
- **two different business state machines and admission policies**,
- **three malicious data pools: archive / train / reserve**.

Direct conclusions:
1. Do not collapse benign and malicious strategy logic into one monolithic script.
2. Do not rewrite the current capture engine.
3. Preserve the current capture engine and make only minimal abstraction changes.
4. Add separate benign and malicious upper-layer entrypoints.
5. Add legacy-data backfill scripts for fingerprinting, cluster/subcluster construction, review manifests, and training exclusion lists.

---

## 3. Architectural Layers

### 3.1 Lower Layer: Capture Engine

The current capture script remains the low-level evidence-production engine and is responsible for:
- taking URLs as input,
- opening webpages,
- collecting screenshots / HTML / visible text / forms / redirect / net summary,
- writing outputs using the frozen sample structure,
- optionally emitting weak labels or helper metadata.

It is not responsible for:
- benign stratified sampling,
- malicious source triage,
- train/test split,
- family/template deduplication,
- train-pool sampling decisions.

### 3.2 Middle Layer: Common Utilities

Shared modules handle:
- URL normalization,
- domain normalization,
- fingerprint generation,
- near-duplicate similarity,
- manifest generation,
- quality checks,
- dedup / clustering helpers.

### 3.3 Upper Layer: Benign Pipeline

Responsible for:
- Tranco stratified sampling,
- trusted long-tail supplementation,
- category / page-type / language coverage control,
- quality veto,
- hard-benign sampling,
- benign manifest generation.

### 3.4 Upper Layer: Malicious Pipeline

Responsible for:
- OpenPhish Community + PhishTank ingestion,
- page-validity checks,
- URL-level deduplication,
- campaign/template clustering,
- subcluster splitting,
- train-pool / reserve-pool construction,
- malicious manifest generation.

### 3.5 Maintenance Layer: Legacy Data Backfill

Responsible for:
- fingerprint backfill for historical samples,
- historical cluster/subcluster construction,
- dedup review-manifest generation,
- training exclusion-list generation,
- batch backfill compatible with existing directory structure.

---

## 4. Relationship to the Existing Capture Script

`capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` is already a full capture engine and should not be expanded into a benign/malicious strategy script.

Warden V1 requires:
- **preserve the main capture logic**,
- **make only minimal abstraction changes**,
- **remove dependency on interactive label selection**,
- **allow non-interactive orchestration from upper-layer scripts**.

Allowed changes:
1. replace interactive label selection with an explicit CLI flag such as `--label benign|phish`,
2. expose a schedulable call path so upper-layer scripts can pass URL lists and output roots,
3. allow external sampling metadata such as benign sampling bucket or malicious source tag,
4. keep frozen output filenames and structure unchanged.

Disallowed changes:
- do not hardcode benign or malicious strategy logic into capture,
- do not move split / sampling / clustering logic into the capture main loop,
- do not rename frozen top-level output files,
- do not introduce unnecessary new dependencies.

---

## 5. Recommended Directory Structure

```text
scripts/
  capture/
    capture_url_v6_optimized_v6_2_plus_labels_brandlex.py

  data/
    common/
      io_utils.py
      url_utils.py
      domain_utils.py
      fingerprint_utils.py
      similarity_utils.py
      dedup_utils.py
      manifest_utils.py
      quality_checks.py

    benign/
      build_benign_candidates.py
      run_benign_capture.py

    malicious/
      ingest_public_malicious_feeds.py
      run_malicious_capture.py
      build_malicious_clusters.py
      build_malicious_train_pool.py

    maintenance/
      backfill_existing_sample_fingerprints.py
      build_dedup_review_manifest.py
      build_training_exclusion_lists.py
```

---

## 6. Three Malicious Data Pools

### 6.1 Raw Archive

Purpose:
- preserve raw malicious captures,
- avoid default physical deletion of duplicates or overflow samples,
- support audit, backtracking, reclustering, and future campaign-evolution analysis.

### 6.2 Train-Eligible Canonical Pool

Purpose:
- serve as the default training pool,
- reduce near-duplicate contamination,
- prevent single-family dominance,
- preserve cross-brand, cross-template, and cross-scenario diversity.

### 6.3 Reserve / Holdout Pool

Purpose:
- keep near-duplicates, cluster-overflow samples, and time-shift samples,
- support robustness evaluation and future hard-case research.

Principle:
- Raw Archive preserves scale,
- Train Pool preserves learnable diversity,
- Reserve Pool preserves value outside the default train pool.

---

## 7. Malicious Deduplication and Sampling Architecture

### 7.1 No Fixed “Keep at Most 15 per Cluster” Rule

Warden V1 no longer uses a fixed per-cluster magic number.

Reasons:
- there is insufficient strong public evidence supporting one universal integer threshold,
- the same host may contain multiple templates, stages, languages, and action pages,
- truncating only at the large-cluster level can destroy valuable subtemplate diversity.

Therefore, V1 freezes the **process**:
- cluster first,
- subcluster next,
- family share cap,
- archive / train / reserve split.

### 7.2 Recommended Levels

#### Level 1: Exact URL
- exact same URL deduplication.

#### Level 2: Normalized / Final URL
- normalized URL,
- final landing URL deduplication.

#### Level 3: Campaign / Template Cluster
- hostname / registrable domain,
- path pattern,
- DOM / HTML structural similarity,
- screenshot near-duplicate similarity,
- text/form near-duplicate similarity.

#### Level 4: Subcluster
Further split large clusters into subclusters by:
- template,
- page stage,
- language,
- brand shell,
- time differences.

### 7.3 Train-Pool Sampling Principles

The train pool should:
1. retain at least one canonical sample per subcluster,
2. retain a small number of extra representatives only when page-state or time differences are meaningful,
3. enforce a global family share cap so that no small number of campaigns dominates the pool,
4. move excluded samples to reserve rather than deleting them by default.

### 7.4 Family Share Cap

The document freezes the principle, not one numeric threshold:
- any single family’s share in the train pool must be bounded,
- the exact threshold should be exposed as configuration,
- if a family exceeds the cap, compress its near-duplicates and same-template subclusters first rather than shrinking all families equally.

---

## 8. Why Benign and Malicious Must Not Share One Strategy Script

Although both eventually invoke browser capture, their business goals differ:

### Benign
- sampling + vetting,
- coverage of source, category, page type, language, and hard-benign cases.

### Malicious
- ingestion + triage + clustering,
- handling source metadata, validity, duplicates, family dominance, and time information.

If forced into one monolithic strategy script, the likely results are:
- too many parameters,
- widespread `if benign` / `if malicious` branching,
- manifest semantic confusion,
- steadily rising maintenance cost.

Therefore, Warden V1 uses:
**shared lower-layer capture and common utilities, but separate upper-layer benign and malicious pipelines.**

---

## 9. Legacy Data Backfill Requirements

V1 must support historical malicious-sample backfill.

Minimum requirements:
1. compute and backfill fingerprints,
2. build clusters and subclusters,
3. generate review manifests,
4. generate training exclusion lists,
5. default to report-and-mark behavior instead of physical deletion.

At minimum, legacy-data outputs should include:
- sample_id -> fingerprint,
- sample_id -> cluster_id,
- sample_id -> subcluster_id,
- keep_in_train / move_to_reserve / reject,
- reason_code.

---

## 10. V1 Frozen Conclusions

Warden V1 freezes the following:
1. capture remains the lower-layer evidence-production engine and is not rewritten,
2. benign and malicious use two separate upper-layer pipelines,
3. the public malicious-source baseline is OpenPhish Community + PhishTank,
4. malicious deduplication uses cluster -> subcluster -> train/reserve decisions rather than a fixed per-cluster cap,
5. legacy data is backfilled and marked by default, not physically deleted.

---

## 11. Current Implementation Mapping (2026-03-23)

The current script entrypoints are:

- capture engine: `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- benign upper-layer entrypoint: `scripts/data/benign/run_benign_capture.py`
- malicious public-feed ingest: `scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious upper-layer entrypoint: `scripts/data/malicious/run_malicious_capture.py`
- malicious cluster / subcluster construction: `scripts/data/malicious/build_malicious_clusters.py`
- malicious train / reserve construction: `scripts/data/malicious/build_malicious_train_pool.py`
- legacy-data backfill: `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`
- dedup review manifest: `scripts/data/maintenance/build_dedup_review_manifest.py`
- training exclusion list: `scripts/data/maintenance/build_training_exclusion_lists.py`

The current capture CLI exposes these orchestration hooks:

- `--label`
- `--output_root`
- `--ingest_metadata_json`
- `--dry_run`

Current implementation status:

- upper-layer orchestrators can invoke capture non-interactively;
- malicious family share cap is exposed as a CLI configuration parameter in the train-pool and maintenance scripts;
- the original capture logic was preserved instead of rewritten;
- legacy-data handling defaults to review / exclusion outputs rather than physical deletion.
