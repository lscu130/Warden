# Warden_MALICIOUS_SOURCE_POLICY_V1

## 中文版

## 1. 文档目的

本文档定义 Warden V1 恶性样本来源、准入、分桶与训练池构建的最小规范。

本文档聚焦于：
- 恶性来源优先级与可用性假设
- 公开基线来源的接入方式
- 恶性样本的原始归档、训练池与保留池分层
- 恶意页面的有效性检查、去重、聚类与子簇抽样
- 老数据回处理与可复现性要求

本文档不定义：
- 最终训练标签映射
- L1/L2 训练方法细节
- 恶性 taxonomy 的最终冻结版本
- 推理期 runtime 逻辑

---

## 2. V1 核心立场

### 2.1 公开基线来源

Warden V1 的公开恶性来源基线固定为：
- **OpenPhish Community**
- **PhishTank**

原因：
- 这两者是当前最现实、最可获取、最容易持续接入的公开来源。
- OpenPhish 的学术/付费访问虽然理论上存在，但 V1 不将其作为默认前提。
- 对个人或小型研究团队而言，学术/付费通道不可作为必须依赖，否则会让数据策略失去可执行性。

因此，Warden V1 明确采用：
**OpenPhish Community + PhishTank 作为公开基线，其他高级来源作为可选增强。**

### 2.2 不把单一 feed 直接当金标

任何单一 feed 都不能被视为“抓到即入训练池”的金标真相。

原因包括：
- 页面失活很快
- 同一 campaign 会高密度重复出现
- 不同 feed 的收集方式不同
- 相同主站和模板会形成严重样本相关性
- 公开 feed 规模、覆盖和时间分布均不稳定

因此，恶性样本必须经过：
- 来源记录
- 页面有效性检查
- URL 级去重
- campaign / template 级聚类
- 训练池抽样

### 2.3 当前活动 rollout 范围（2026-04-08 收紧）

本策略文档保留 Warden V1 的**通用能力边界**：
- Raw Archive / Train Pool / Reserve Pool 三层概念仍成立
- cluster / subcluster / family share cap 仍是 V1 支持的高级恶性处理能力

但 **当前默认活动执行范围** 已收紧为：
- 仅 **Roblox + Netflix families** 默认启用高级 cluster / subcluster / train-reserve handling
- 对其他 malicious families，当前默认只保留：
  - source recording
  - page-validity checks
  - raw archive handling
  - optional exact-URL hygiene dedup only
- 其他 malicious families 当前不得默认进入更广的 family/template clustering 与 train-reserve compression

---

## 3. 恶性来源优先级

### 3.1 默认公开基线

#### OpenPhish Community

角色定位：
- active phishing feed 主来源之一
- 提供持续、新鲜、现实世界恶意 URL 流

风险：
- 生命周期短
- 重复 campaign 多
- 公开 feed 配额与覆盖有限

#### PhishTank

角色定位：
- 免费公开补充源
- 与 OpenPhish 形成来源多样性互补
- 适合作为交叉补充与时间扩充

风险：
- 提交与验证机制不同于 OpenPhish
- 时间新鲜度、覆盖目标与分布可能不同

### 3.2 可选增强来源

以下来源允许在 V1 后续阶段接入，但不作为当前默认前提：
- APWG eCX
- Netcraft
- 其他研究合作源

若后续获得接入权限，应作为**来源增强**接入，而不是重写 V1 公开基线策略。

---

## 4. 三层恶性样本池

Warden V1 不采用“抓到多少就训练多少”的单池设计。

必须至少拆成以下三层：

### 4.1 Raw Malicious Archive

含义：
- 所有抓到的恶性来源样本的原始归档层
- 不因为重复、失活或 cluster overflow 默认物理删除

作用：
- 审计
- 回溯
- 再聚类
- 未来 benchmark / drift / campaign 演化分析

### 4.2 Train-Eligible Canonical Pool

含义：
- 经过有效性检查、去重、campaign/template 聚类后，适合进入训练的 canonical 恶性样本池

作用：
- 作为默认训练主池
- 控制 family dominance
- 控制近重复污染
- 保留跨品牌、跨场景、跨模板多样性

### 4.3 Reserve / Holdout Pool

含义：
- 从训练池中排除但仍保留价值的样本
- 包括近重复、cluster overflow、时间漂移样本、可用于鲁棒性测试的 campaign 变体

作用：
- hard-case 评测
- campaign 演化评测
- 模板鲁棒性评测
- 未来 L2 / frontier 技术研究

---

## 5. 页面有效性检查

一个恶性 URL 只有在能够形成足够网页证据时，才可以进入 Raw Archive 的有效样本子集，进一步参与训练池构建。

建议至少满足以下之一：
- 页面成功抓取
- 存在有效 viewport screenshot
- 存在可见文本 / HTML / 表单等主体证据
- 页面状态足以支持后续训练、复核或分析

应进入 rejected / invalid bucket 的情况包括：
- 页面完全失活，且无可用历史证据
- 仅返回错误页/空白页
- 只剩无意义跳转
- 抓取失败且无可补救输出
- 无主体网页内容，无法支持后续使用

---

## 6. 去重与聚类策略

## 6.1 不冻结固定“每簇最多保留 N 条”

Warden V1 不冻结类似“每个重复簇最多保留 15 条”这类魔法数字为硬规则。

原因：
- 当前没有足够强的公开文献能直接支持某个固定整数阈值是普遍最优。
- 同一主站下可能包含多个不同模板、不同页面阶段、不同语言、不同高风险动作。
- 只按大簇截断，容易误删真正有价值的子模板差异。

因此，V1 冻结的是**流程与约束**，不是固定整数上限。

## 6.2 去重与聚类的层次

恶性去重必须至少包含以下层次：

### Level 1: Exact URL
- 完全相同 URL 去重

### Level 2: Normalized / Final URL
- 归一化 URL
- 最终落地 URL
- 常见跟踪参数剔除后的 URL

### Level 3: Campaign / Template Cluster
- hostname / registrable domain
- URL path pattern
- DOM/HTML 结构相似度
- screenshot 近重复
- 页面文本与表单结构近重复

### Level 4: Subcluster
在大簇内部继续切分子簇，优先依据：
- 页面模板差异
- 页面阶段差异（登录 / 验证 / 支付 / 钱包连接 / 恢复等）
- 语言差异
- 品牌壳差异
- 时间差异

## 6.3 训练池抽样原则

训练池抽样遵循：
- **先 family / campaign 聚类**
- **再做子簇切分**
- **优先保留子簇覆盖，而不是保留单一大簇的大量近重复页**

推荐默认规则：
1. 每个子簇至少保留 1 个 canonical 样本。
2. 若子簇在时间或页面状态上存在明确差异，可额外保留少量代表样本。
3. 对单一 family 施加**全局 share cap**，避免训练池被少数 campaign 主导。
4. 原始 archive 不做默认物理删除。

当前活动执行范围补充：
- 上述高级 cluster / subcluster / train-pool sampling 链路，在当前阶段默认只对 Roblox + Netflix families 启用。
- 其他 malicious families 当前默认不进入该高级链路；它们停留在基础 ingest/archive 路径，并只保留可选 exact-URL hygiene dedup。

### 6.4 Family Share Cap

V1 默认不写死绝对样本上限，但要求：
- 单一 family / campaign 在训练池中的占比必须被限制。
- 当某一 family 规模远超其他 family 时，优先压缩该 family 的近重复和同模板子簇，而不是继续等比例保留。

推荐工程写法：
- 训练池中，任一 family 默认不应超过恶性训练样本总量的一个小比例阈值。
- 具体阈值应作为配置项，而不是写死在文档里。

---

## 7. 来源记录与元数据要求

每条恶性样本至少记录：
- source = `openphish_community` / `phishtank`
- ingest timestamp
- original URL
- normalized URL
- final URL（若可获得）
- domain / registrable domain
- capture timestamp
- capture status
- page validity status
- archive bucket / train pool status / reserve status

建议额外记录：
- first_seen（若可获得）
- feed row timestamp（若可获得）
- brand / target（若可推断）
- scenario / scene type（若可推断）
- language
- redirect count
- screenshot availability
- OCR availability
- dedup cluster id
- subcluster id

---

## 8. 老数据处理原则

历史 malicious 数据不应直接删除，也不应假设旧数据天然可训练。

V1 要求：
- 为老数据补做 fingerprint
- 为老数据构建 dedup cluster 与 subcluster
- 生成 review manifest
- 生成默认训练排除清单
- 默认只做“报告与标记”，不做物理删除

---

## 9. 与训练和评测的关系

该策略的目标不是减少恶性数据，而是把恶性数据**从单一堆积池转成可控的多池结构**。

影响如下：
- Raw Archive：保持规模与历史价值
- Train Pool：降低重复污染，提高 family/template 多样性
- Reserve Pool：保留 hard cases、campaign 演化样本、鲁棒性测试样本

因此，去重与聚类的正确结果不是“数据被浪费”，而是“训练、评估、分析三者各用不同子集”。

---

## 10. V1 冻结结论

Warden V1 冻结以下结论：

1. **公开恶性基线来源固定为 OpenPhish Community + PhishTank。**
2. **不假设 OpenPhish 学术/付费访问可作为默认前提。**
3. **恶性数据至少拆成 Raw Archive / Train-Eligible Canonical Pool / Reserve Pool 三层。**
4. **恶性去重采用 campaign → subcluster 两级抽样，不冻结固定每簇最大保留条数。**
5. **老数据默认做回处理与标记，不默认物理删除。**

---

## English Version

# Warden_MALICIOUS_SOURCE_POLICY_V1

## 1. Purpose

This document defines the minimum malicious-source, admission, bucketization, and train-pool construction policy for Warden V1.

This document covers:
- source priority and availability assumptions,
- public-baseline source selection,
- raw archive / train pool / reserve pool separation,
- page validity checks, deduplication, clustering, and subcluster sampling,
- legacy-data backfill and reproducibility requirements.

This document does not define:
- final training label mapping,
- detailed L1/L2 training method,
- final malicious taxonomy,
- runtime inference logic.

---

## 2. Core Position for V1

### 2.1 Public Baseline Sources

The public malicious-source baseline for Warden V1 is fixed as:
- **OpenPhish Community**
- **PhishTank**

Rationale:
- these are the most realistic, continuously accessible, and operationally obtainable public sources,
- OpenPhish academic or paid access may exist, but V1 does not assume it as a default dependency,
- for individuals or small research teams, premium or academic channels are not reliable enough to serve as a mandatory baseline assumption.

Therefore, Warden V1 explicitly adopts:
**OpenPhish Community + PhishTank as the public malicious baseline, with higher-tier feeds treated as optional extensions.**

### 2.2 No Single Feed Is Treated as Ready-to-Train Gold

No single feed should be treated as immediate gold data.

Reasons include:
- pages expire quickly,
- a single campaign may appear in dense repeated variants,
- collection methodology differs across feeds,
- the same host or kit may create severe sample correlation,
- public-feed coverage, freshness, and composition are unstable.

Therefore, malicious data must pass through:
- source recording,
- page-validity checks,
- URL-level deduplication,
- campaign/template clustering,
- train-pool sampling.

### 2.3 Current Active Rollout Scope (Tightened On 2026-04-08)

This policy document still preserves the **general V1 capability boundary**:
- the Raw Archive / Train Pool / Reserve Pool separation remains valid,
- cluster / subcluster / family-share-cap handling remains part of the supported V1 malicious-processing capability.

However, the **current default active execution scope** is now tightened to:
- enable advanced cluster / subcluster / train-reserve handling by default only for the **Roblox, Netflix, Trezor, and Ledger families**,
- keep all other malicious families on:
  - source recording,
  - page-validity checks,
  - raw archive handling,
  - optional exact-URL hygiene dedup only,
- keep all other malicious families out of broader family/template clustering and train-reserve compression by default at the current stage.

---

## 3. Source Priority

### 3.1 Default Public Baseline

#### OpenPhish Community

Role:
- one of the primary active phishing-feed sources,
- provides fresh real-world malicious URLs.

Risks:
- short page lifetime,
- many repeated campaigns,
- limited public-feed quota and coverage.

#### PhishTank

Role:
- free public supplementary source,
- adds source diversity relative to OpenPhish,
- useful for cross-source supplementation and time-span expansion.

Risks:
- submission and validation workflow differs from OpenPhish,
- freshness, targets, and distribution may differ.

### 3.2 Optional Extension Sources

The following may be added later, but are not part of the default V1 assumption:
- APWG eCX,
- Netcraft,
- other collaboration-based research sources.

If access is obtained later, they should be added as **source extensions**, not as a rewrite of the V1 public-baseline policy.

---

## 4. Three-Layer Malicious Data Pools

Warden V1 does not use a single “all captured malicious samples” pool.

At minimum, malicious data must be split into:

### 4.1 Raw Malicious Archive

Meaning:
- raw archival layer for all captured malicious-source samples,
- no default physical deletion due to duplicates, expiry, or cluster overflow.

Purpose:
- audit,
- backtracking,
- reclustering,
- future benchmark, drift, and campaign-evolution analysis.

### 4.2 Train-Eligible Canonical Pool

Meaning:
- malicious samples suitable for training after validity checks, deduplication, and campaign/template clustering.

Purpose:
- default training pool,
- control family dominance,
- reduce near-duplicate contamination,
- preserve cross-brand, cross-scenario, and cross-template diversity.

### 4.3 Reserve / Holdout Pool

Meaning:
- samples excluded from the default training pool but still valuable,
- includes near-duplicates, cluster overflow samples, time-shift samples, and campaign variants useful for robustness evaluation.

Purpose:
- hard-case evaluation,
- campaign-evolution evaluation,
- template-robustness evaluation,
- future L2 / frontier-tech research.

---

## 5. Page Validity Checks

A malicious URL may enter the usable archival subset only when it yields sufficient webpage evidence.

At least one of the following should hold:
- successful capture,
- valid viewport screenshot,
- visible text / HTML / forms / other core evidence,
- enough page state to support downstream training, review, or analysis.

Rejected or invalid cases include:
- fully expired page with no usable historical evidence,
- error page or blank page only,
- meaningless redirect residue,
- failed capture with no usable output,
- no substantive webpage content.

---

## 6. Deduplication and Clustering Policy

### 6.1 No Frozen Magic Number Such as “Keep at Most 15 Per Cluster”

Warden V1 does not freeze a hard rule such as “keep at most 15 per duplicate cluster.”

Reasons:
- there is not enough strong public evidence supporting one universal integer cap as broadly optimal,
- the same main host may contain multiple templates, multiple page stages, multiple languages, and multiple high-risk actions,
- truncating only at the large-cluster level may remove valuable sub-template diversity.

Therefore, V1 freezes the **process and constraints**, not one universal integer threshold.

### 6.2 Deduplication and Clustering Levels

Malicious deduplication must include at least the following levels:

#### Level 1: Exact URL
- exact same URL deduplication.

#### Level 2: Normalized / Final URL
- normalized URL,
- landing final URL,
- URL after removing common tracking parameters.

#### Level 3: Campaign / Template Cluster
- hostname / registrable domain,
- URL path pattern,
- DOM / HTML structural similarity,
- screenshot near-duplicate similarity,
- page text and forms near-duplicate similarity.

#### Level 4: Subcluster
Large clusters must be further split by:
- template differences,
- page-stage differences (login / verification / payment / wallet connect / recovery / etc.),
- language differences,
- brand-shell differences,
- time differences.

### 6.3 Train-Pool Sampling Principles

Train-pool sampling must follow:
- **cluster by family / campaign first**,
- **split into subclusters next**,
- **prioritize subcluster coverage instead of keeping many near-duplicates from one large cluster**.

Recommended default behavior:
1. keep at least one canonical sample per subcluster,
2. keep a small number of additional representatives only when time or page-state differences are meaningful,
3. apply a **global family share cap** so that no single family dominates the train pool,
4. do not physically delete the raw archive by default.

Current active rollout note:
- the advanced cluster / subcluster / train-pool sampling chain above is currently enabled by default only for the Roblox, Netflix, Trezor, and Ledger families;
- all other malicious families do not enter that advanced chain by default at the current stage and remain on the basic ingest/archive path with optional exact-URL hygiene dedup only.

Current V1 planning target:
- the default malicious train-pool planning target is **20,000**
- this is aligned with the current regular benign target so the paired dataset planning target is **40,000 total**
- this is a practical planning value under the current public-source constraint, not a claim of universal optimality

### 6.4 Family Share Cap

V1 does not freeze one absolute numeric per-cluster maximum, but it does require:
- the train-pool share of any single family / campaign must be limited,
- when one family is disproportionately larger than others, its near-duplicates and same-template subclusters should be compressed before proportional retention continues.

Recommended engineering form:
- any single family should be bounded by a configurable small fraction of the malicious training pool,
- the exact threshold should remain a configuration value rather than a hard-coded document constant.

---

## 7. Source Recording and Metadata Requirements

Each malicious sample must record at least:
- source = `openphish_community` or `phishtank`,
- ingest timestamp,
- original URL,
- normalized URL,
- final URL if available,
- domain / registrable domain,
- capture timestamp,
- capture status,
- page validity status,
- archive bucket / train-pool status / reserve status.

Recommended additional fields:
- first_seen if available,
- feed row timestamp if available,
- brand / target if inferable,
- scenario / scene type if inferable,
- language,
- redirect count,
- screenshot availability,
- OCR availability,
- dedup cluster id,
- subcluster id.

---

## 8. Legacy Data Handling

Historical malicious data must not be deleted blindly and must not be assumed train-ready by default.

V1 requires:
- fingerprint backfill,
- dedup cluster and subcluster construction,
- review manifest generation,
- default training-exclusion list generation,
- report-and-mark behavior by default, not physical deletion.

---

## 9. Relationship to Training and Evaluation

The goal of this policy is not to shrink malicious data for its own sake.
The goal is to convert malicious data from a single overloaded pile into a controlled multi-pool structure.

Effects:
- Raw Archive preserves scale and historical value.
- Train Pool reduces duplicate contamination and improves family/template diversity.
- Reserve Pool preserves hard cases, campaign-evolution samples, and robustness-evaluation samples.

Thus, correct deduplication and clustering should not be understood as “wasting data,” but as separating training, evaluation, and analysis subsets appropriately.

---

## 10. V1 Frozen Conclusions

Warden V1 freezes the following:

1. **The public malicious baseline is OpenPhish Community + PhishTank.**
2. **OpenPhish academic or premium access is not assumed as a default dependency.**
3. **Malicious data must be split into Raw Archive / Train-Eligible Canonical Pool / Reserve Pool.**
4. **Malicious deduplication uses a campaign -> subcluster two-stage sampling policy rather than a frozen fixed per-cluster cap.**
5. **Legacy data is backfilled and marked by default, not physically deleted.**

---

## 11. Current Implementation Mapping (2026-03-23)

The current script entrypoints that map to this policy are:

- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`

Current implementation status:

- the default public sources are OpenPhish Community and PhishTank;
- train / reserve decisions are built on top of cluster / subcluster records rather than a fixed per-cluster cap;
- family share cap is exposed as a CLI configuration item instead of being frozen as a document-level magic number;
- the current default family share cap used by the active train-pool / maintenance paths is `0.25`, while CLI override remains available;
- the broader V1 advanced malicious dedup / cluster / pool path remains available as a supported capability boundary, while the current default active advanced scope is Roblox+Netflix+Trezor+Ledger-only;
- legacy-data handling emits fingerprints, cluster/subcluster outputs, review manifests, and exclusion lists without default physical deletion.
