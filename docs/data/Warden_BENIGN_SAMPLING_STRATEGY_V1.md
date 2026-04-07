# Warden_BENIGN_SAMPLING_STRATEGY_V1

## 中文版

### 1. 文档目的

本文档定义 Warden V1 的常规良性网站（benign）采样策略，用于构建与恶性样本规模相匹配、分布更合理、误报控制更稳的良性训练与评估样本池。

本文档聚焦于：
- 良性来源选择
- 分层采样配额
- 质量过滤与安全否决（veto）
- 页面类型覆盖要求
- 数据记录与复现要求

本文档不定义：
- 恶性样本来源策略
- 训练方法细节
- 标签体系映射
- 最终 split 规则

---

### 2. V1 总体目标

Warden V1 的常规良性样本目标量设定为：

- **20,000 个常规良性样本**

该规模与当前恶性样本目标量对齐，目的是：
- 保持训练与评估阶段的样本规模平衡
- 提高文本塔、视觉塔和融合层对常规互联网页面的覆盖能力
- 强化对“粗糙但合法页面”的识别能力，降低误报率

---

### 3. 设计原则

#### 3.1 不能只依赖头部榜单

只从头部热门域名中抽取 benign，会导致样本过于“体面”和“企业化”，容易把模型训练成：
- 对大厂官网非常稳
- 对中长尾、粗糙合法站点误报偏高

#### 3.2 Tranco 作为主榜单来源

V1 默认使用 **Tranco** 作为主榜单来源。

原因：
- 更适合研究复现
- 可归档
- 排名分层可操作性更高
- 相比 Cloudflare Radar，更适合作为细粒度排名分层抽样主来源

#### 3.3 排名分层不够，必须补内容分层

仅按排名抽样不够。
在每个排名层内部，还必须尽可能覆盖：
- 不同行业类别
- 不同页面类型
- 不同语言/地区
- 不同页面质量水平

#### 3.4 必须引入榜单外可信长尾

如果所有 benign 都来自 top list，即使做了排名分层，整体分布仍然会偏向热门站点。
因此 V1 必须额外引入一部分：
- 非热门但可信的长尾合法域名
- 容易被误报的 hard-benign 页面

---

### 4. V1 采样配额

#### 4.1 总量

- **总量：20,000**

#### 4.2 主来源与配额

##### A. Tranco 主榜单样本：16,000

建议分配如下：

- **Top 1 – 10,000：2,000**
- **Top 10,001 – 100,000：7,000**
- **Top 100,001 – 500,000：8,000**
- **Top 500,001 – 1,000,000：3,000**

##### B. 榜单外可信长尾样本：4,000

建议来源包括：
- 合法但不热门的中小企业官网
- 地方机构/协会/学校/社区组织网站
- 地方媒体、论坛、博客
- 小型 SaaS / 工具站 / 文档站
- 容易与 phishing/SE 页面视觉或文本风格混淆的合法页面

---

### 5. 二次分层要求

在上述 20,000 样本中，不应仅满足“排名配额”，还应尽量满足以下二次覆盖要求。

#### 5.1 行业类别覆盖

建议覆盖：
- 金融 / 银行 / 支付
- 电商 / 零售
- SaaS / 企业服务
- 政府 / 教育 / 医疗
- 新闻 / 媒体
- 社区 / 论坛 / 博客
- 邮箱 / 账号体系 / 身份平台
- 本地 SMB / 地方服务 / 小微企业官网

#### 5.2 页面类型覆盖

不能只抓首页。
应尽可能覆盖：
- 首页
- 登录页
- 注册页
- 密码重置页
- 账号验证页
- 客服 / 工单 / 支持页
- 支付 / 账单 / 订单页
- 下载 / 更新 / 通知页
- 联系我们 / 表单页

#### 5.3 语言与地区覆盖

Warden 文本端默认走多语言路线，因此 benign 样本不应只集中于英语页面。
在资源允许的前提下，应记录并尽量覆盖：
- 英语
- 中文
- 欧洲主要语言
- 东南亚/拉美等高 phishing 暴露区域的常见语言

#### 5.4 页面质量覆盖

必须刻意保留部分：
- UI 简陋
- 文案不规范
- 表单明显
- 结构“看上去像诈骗页”但其实合法

这类样本应单独标记为：
- **hard-benign / confusion-benign bucket**

---

### 6. 质量过滤与安全否决

所有 benign 样本都必须经过最小质量过滤与安全否决。

#### 6.1 页面质量过滤

应剔除：
- 无法访问或抓取失败页面
- parked domains
- 占位页 / construction page
- 无主体内容页
- 纯跳转页
- 纯 CDN / 纯 API / 纯静态资源域

#### 6.2 安全否决

应尽量剔除：
- 被多个高可信安全信号标记为可疑/恶意的域名或页面
- 明显存在 brand abuse / phishing 痕迹的页面
- 短期异常跳转或内容明显不稳定页面

#### 6.3 内容有效性要求

一个 benign 样本至少应满足以下之一：
- 页面有可见正文内容
- 页面存在稳定导航/结构内容
- 页面存在真实服务表单或真实业务内容
- 页面可形成对文本塔或视觉塔有价值的正常网页证据

---

### 7. 采样记录要求

为了后续复现与审计，每个 benign 样本建议至少记录：
- 来源（Tranco / long-tail curated / other）
- Tranco rank bucket（如适用）
- 域名
- URL
- 抓取日期
- 页面类型
- 语言
- 行业类别（若可判定）
- hard-benign 标志
- veto 过滤结果

---

### 8. 与训练/评估的关系

本文件只定义 benign 采样与准入策略，不直接定义训练集和测试集切分。

后续训练/评估时，应进一步控制：
- 同域名泄漏
- 同品牌泄漏
- 同模板/近重复页面泄漏
- 时间泄漏

---

### 9. V1 推荐结论

Warden V1 常规 benign 采样策略冻结如下：

- 总量：**20,000**
- 主榜单：**Tranco**
- 结构：**排名分层 + 类别/页面类型二次分层 + 榜单外可信长尾补充**
- 必做：**页面质量过滤 + 安全否决 + hard-benign 单独保留**

该策略优先目标不是“构造最干净的 benign 集”，而是：
- 构造**更接近真实互联网**的 benign 分布
- 提高 Warden 对普通合法页面的适应性
- 降低对长尾合法站点的误报

---

## English Version

## 1. Purpose

This document defines the benign website sampling strategy for Warden V1.
It is intended to build a benign pool that is:
- large enough to match the current malicious sample target,
- more representative of real-world benign web pages,
- better suited for false-positive control.

This document defines:
- benign source selection,
- stratified sampling quotas,
- quality filtering and safety veto,
- page-type coverage,
- logging and reproducibility requirements.

This document does not define:
- malicious-source policy,
- training procedure,
- label mapping,
- final train/val/test split policy.

---

## 2. V1 Target Size

Warden V1 sets the target size of the regular benign pool to:

- **20,000 benign samples**

This is intentionally aligned with the current malicious target size in order to:
- maintain a balanced working scale,
- improve coverage for the text tower, vision tower, and fusion layer,
- strengthen robustness against legitimate but rough-looking websites.

---

## 3. Design Principles

### 3.1 Do not rely only on top-ranked domains

If the benign pool is built only from highly popular websites, the data distribution becomes overly “clean”, polished, and enterprise-like.
That tends to produce models that:
- behave well on large corporate sites,
- but over-fire on long-tail legitimate websites.

### 3.2 Use Tranco as the primary ranking source

Warden V1 uses **Tranco** as the default primary ranking source because it is better suited for research reproducibility and fine-grained rank-bucket sampling.

### 3.3 Rank stratification alone is insufficient

Rank stratification is necessary but not sufficient.
Inside each rank bucket, the pool should also cover:
- industry/category diversity,
- page-type diversity,
- language/region diversity,
- different quality levels.

### 3.4 Add trustworthy long-tail benign sources outside top lists

Even a rank-stratified top-list-only pool still remains popularity-biased.
Therefore, Warden V1 must include additional benign samples from:
- trustworthy but non-popular long-tail domains,
- hard-benign pages that are likely to be confused with phishing or social-engineering pages.

---

## 4. V1 Sampling Quotas

## 4.1 Total

- **Total benign samples: 20,000**

## 4.2 Source mix

### A. Tranco main pool: 16,000

Recommended allocation:

- **Top 1 – 10,000: 2,000**
- **Top 10,001 – 100,000: 7,000**
- **Top 100,001 – 500,000: 8,000**
- **Top 500,001 – 1,000,000: 3,000**

### B. Trustworthy long-tail pool outside Tranco: 4,000

Suggested sources include:
- legitimate but non-popular SMB websites,
- local institutions / associations / schools / community websites,
- local media, forums, blogs,
- small SaaS / utility / documentation websites,
- legitimate pages that visually or textually resemble phishing / SE pages.

---

## 5. Secondary Stratification Requirements

The 20,000 benign samples should not only satisfy rank quotas.
They should also cover the following dimensions as much as practical.

### 5.1 Category coverage

Recommended coverage includes:
- finance / banking / payment,
- e-commerce / retail,
- SaaS / enterprise services,
- government / education / healthcare,
- news / media,
- community / forum / blog,
- webmail / account systems / identity platforms,
- local SMB / local services / small business websites.

### 5.2 Page-type coverage

Do not capture homepage-only benign data.
Try to include:
- homepages,
- login pages,
- signup pages,
- password reset pages,
- account verification pages,
- support / helpdesk pages,
- billing / payment / order pages,
- download / update / notification pages,
- contact / form pages.

### 5.3 Language and regional coverage

Warden’s text side is designed for multilingual operation.
Therefore, the benign pool should not be English-only.
When possible, record and diversify across:
- English,
- Chinese,
- major European languages,
- common languages from regions with strong phishing exposure.

### 5.4 Quality coverage

The pool must intentionally retain some legitimate pages that are:
- visually rough,
- textually awkward,
- heavily form-driven,
- superficially similar to scam-like pages.

These should be marked as:
- **hard-benign / confusion-benign bucket**

---

## 6. Quality Filtering and Safety Veto

All benign samples must pass minimum quality filtering and safety veto.

### 6.1 Page-quality filtering

Remove:
- inaccessible pages,
- parked domains,
- placeholder / under-construction pages,
- pages with no meaningful main content,
- pure redirect pages,
- pure CDN / pure API / pure static-asset domains.

### 6.2 Safety veto

Remove whenever possible:
- domains/pages flagged as suspicious by multiple trusted security signals,
- pages showing obvious brand abuse or phishing-like artifacts,
- unstable pages with abnormal redirects or rapidly changing content.

### 6.3 Minimum content usefulness

A benign sample should satisfy at least one of the following:
- has visible main content,
- has stable navigation / structural content,
- contains a real service form or real business content,
- provides useful normal-web evidence for the text tower or vision tower.

---

## 7. Logging Requirements

For reproducibility and auditability, each benign sample should record at least:
- source (`Tranco`, `long-tail curated`, or other),
- Tranco rank bucket if applicable,
- domain,
- URL,
- capture date,
- page type,
- language,
- industry/category if available,
- hard-benign flag,
- veto/filtering outcome.

---

## 8. Relation to Training and Evaluation

This document defines only benign sampling and admission policy.
It does not define final split policy.

Later training/evaluation should still control for:
- same-domain leakage,
- same-brand leakage,
- same-template / near-duplicate leakage,
- temporal leakage.

---

## 9. Frozen V1 Recommendation

Warden V1 freezes the regular benign sampling policy as follows:

- total size: **20,000**,
- primary ranking source: **Tranco**,
- structure: **rank stratification + secondary stratification by category/page type + trustworthy long-tail supplementation**,
- mandatory controls: **quality filtering + safety veto + dedicated hard-benign retention**.

The primary goal is not to build the cleanest possible benign pool.
The primary goal is to build a benign pool that is closer to the real web and better suited for reducing false positives on legitimate long-tail websites.

---

## 10. Current Implementation Mapping (2026-03-23)

The current script entrypoint that maps to this policy is:

- `scripts/data/benign/run_benign_capture.py`

Current implementation boundary:

- this entrypoint passes benign upper-layer ingest metadata into capture;
- the benign candidate list is still prepared outside the script and then passed through `--input_path`;
- `source`, `rank_bucket`, `page_type`, `language`, and `hard_benign` are propagated as upper-layer ingest metadata;
- capture remains a lower-layer evidence engine and does not implement benign quota logic by itself.
