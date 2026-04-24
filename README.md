# Warden

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是 Warden 的项目级导览，不是任务单或模块细则。
- 涉及精确术语、状态边界或历史事实时，以英文版为准。

## 1. 项目概览

Warden 当前不是狭义的品牌钓鱼检测器，而是一个网页社工风险判断系统。
它关注页面是否通过布局、文案、交互和视觉伪装诱导用户执行高风险操作，例如账号窃取、品牌冒充、支付欺诈、钱包滥用等。

## 2. 当前主线

当前主线强调：

- 分层判断架构（L0 / L1 / L2）
- 可复现的数据与文档流程
- 冻结 schema 和清晰模块边界
- 面向普通边缘设备的可部署路径

## 3. 中文阅读建议

如果你只想快速理解项目，先看英文版的这些部分：

- `What The Project Is Doing Now`
- `Mainline Focus`
- `What Warden Is Not Trying To Do`
- `Current Engineering State`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden

This README describes Warden as a web social-engineering threat judgment system rather than a narrow phishing-brand detector.

## 1. What The Project Is Doing Now

Warden is building a system that judges whether a webpage presents meaningful social-engineering risk, including credential theft, brand impersonation, misleading redirects, payment fraud, wallet abuse, and other high-risk induced actions.

The project is therefore no longer limited to the narrow question "is this a phishing page for some brand." It asks whether a page is trying to push a user into dangerous behavior through layout, wording, interaction flow, and visual disguise.

In practice, Warden cares about questions such as:

- whether the page is performing social-engineering induction;
- whether it is asking for passwords, OTP codes, payment details, wallet approvals, seed phrases, or other sensitive information;
- whether it is pretending to be a known brand, platform, institution, or service;
- whether the page is risky enough to require escalation to a stronger review stage;
- whether the system can remain useful under lightweight and edge-deployable constraints.

Warden is not meant to be a logo recognizer. It is meant to be a web threat-judgment system that combines screenshot, HTML, URL, form, brand, and intent evidence.

## 2. Current Project Positioning

### 2.1 Research Position

The current research position is lightweight, multimodal, staged social-engineering threat judgment for real webpages.

Its defining properties are:

1. Multimodal inputs: screenshots, HTML text, URLs, forms, brand clues, and page metadata.
2. Staged judgment: route cases through L0, L1, and L2 instead of sending every sample to the most expensive path.
3. Lightweight-first engineering: deployment and cost constraints are treated as first-class requirements.
4. Threat-oriented framing: the core question is social-engineering threat judgment, not merely brand matching.
5. Explainable and engineering-stable design: labels, fields, manifests, weak-label rules, and interfaces should remain auditable and stable.

### 2.2 Difference From Traditional Phishing Detection

Warden explicitly moves beyond a simple `phishing` versus `benign` framing.

It does not focus only on:

- logo matching;
- reference-list lookup;
- static benchmark-style page recognition.

Instead, it asks whether the page is structurally and semantically trying to induce a dangerous user action. That makes the project closer to web social-engineering analysis than to narrow brand-impersonation detection.

## 3. Current System Shape: L0 / L1 / L2

Warden currently uses a staged architecture.

### L0: Lightweight Fast Screening

L0 is not the final judge. Its job is low-cost screening:

- quickly inspect cheap URL, visible-text/title, form-summary, network-summary, and existing cheap diff/evasion observability signals;
- detect obvious `gambling / adult / gate` specialized surfaces and high-risk routing anchors;
- let low-risk samples stop cheaply only when the policy allows it and cheap evidence is sufficiently observed;
- forward suspicious samples to a stronger layer.

The current L0 default hot path does not eagerly read full HTML, run default brand extraction, consume screenshots/OCR, or perform heavy interaction recovery. Those heavier or more semantic signals belong to L1, L2, or explicitly gated follow-up paths. L0 should stay fast, small, and edge-friendly. It should favor conservative routing over pretending to be an all-purpose one-layer solution.

### L1: Multimodal Risk-Judgment Layer

L1 is the main judgment layer in the current design. It combines evidence such as:

- visual impersonation from the screenshot;
- brand, wording, and interaction semantics from HTML and visible text;
- consistency or conflict between the URL and the page content;
- whether forms request sensitive information;
- whether the page shows login, verification, payment, wallet-connect, or recovery-seed intent.

Its job is to produce a stronger risk judgment, provide finer risk tags, and prepare better candidates and evidence for L2.

### L2: Stronger Review / Escalation Layer

L2 is currently a reserved higher-cost layer for hard, high-risk, or ambiguous cases.

It is intended to handle:

- difficult open-world samples;
- stronger multimodal review and consistency checks;
- future adversarial, generalization, and hard-case analysis.

The current goal is not to make L2 huge by default. The goal is to reserve a stable place for it so the system does not need a later redesign.

## 4. Current Core Focus: Data And Labels

The present core priority is not a flashy model score. It is making the data foundation stable enough that later training and evaluation do not collapse on bad assumptions.

### 4.1 Data Collection Is Ongoing

The project is building a structured capture pipeline around more than screenshots alone. The capture outputs include:

- screenshots;
- HTML;
- URLs;
- page metadata;
- forms and interaction clues;
- brand candidates;
- auto-derived label artifacts.

The goal is to build reproducible, auditable, trainable data assets that are ready for offline backfill rather than a pile of disconnected samples.

### 4.2 The Label System Is Being Frozen As V1

Warden is intentionally freezing a V1 label system to avoid endless field renaming, semantic drift, and broken downstream scripts.

The current label design already goes beyond "is this phishing" and instead covers:

- base classes;
- risk labels;
- brand labels;
- page-intent labels;
- credential / payment / wallet-related sensitive-intent labels;
- auxiliary rule-derived labels;
- manual correction and offline backfill outputs.

The working principle is:

- freeze field names where possible;
- keep label semantics stable;
- allow filling values later without casually redesigning structure;
- preserve a stable baseline for papers and training pipelines.

### 4.3 Auto-Backfill And Manual Correction Run In Parallel

Warden is not using a pure fully manual labeling path, and it is not pretending rule-based auto-labeling is enough by itself. The current direction is auto backfill plus selective human correction plus gradual stabilization of label standards.

The practical work already underway includes:

- offline backfill of captured samples;
- improving brand recognition through brand lexicons;
- checking rule-label coverage and error modes;
- validating on smaller batches before scaling up.

If the labels are unstable, even a good model just becomes a high-performance nonsense generator.

## 5. Current Model Route: Lightweight, Multimodal, Deployable

The model route is already constrained in a fairly clear way.

### 5.1 Text Tower And Vision Tower Direction

The project currently leans toward:

- a lightweight text tower such as DistilBERT or TinyBERT;
- a lightweight vision tower such as MobileNetV3-Small or MobileNetV4;
- stronger teacher models or CLIP-like models for distillation where useful;
- fusion or gating logic that can combine URL, HTML, screenshot, form, and brand evidence.

The point is not to chase the largest model. The point is to control parameter count, memory, and deployment cost while still supporting staged L0 / L1 / L2 responsibilities.

### 5.2 Edge Constraints Are A Premise, Not An Afterthought

Deployment realism is not treated as a later optimization step. It is a design premise from the beginning.

That means current model and system choices are shaped by practical constraints such as:

- limited hardware budget;
- non-trivial inference cost;
- no assumption that a giant live-updated reference list is always available;
- no assumption that every decision can be outsourced to an expensive API;
- the need to remain usable in local, edge, or resource-constrained settings.

### 5.3 The Project Is Still In The Foundation Phase

Warden is not yet in the full-scale formal-training phase. The current emphasis is still on:

- data collection;
- label freezing;
- brand lexicon completion;
- script and directory cleanup;
- module-boundary definition;
- training and inference documentation.

That is not a weakness. It is the normal phase where the foundation is being built.

## 6. Current Engineering Work

Warden is also turning the project into an explicit engineering system rather than leaving it as a loose idea.

### 6.1 Repository And Module Documentation Is Being Built Out

The repository is gradually being filled with:

- project overview docs;
- repository-structure guidance;
- data-module docs;
- labeling-module docs;
- training-module docs;
- inference-module docs;
- paper-support docs;
- workflow and template docs.

These documents are not there for decoration. They reduce semantic drift across people, windows, and model agents.

### 6.2 Naming And Structure Have Been Unified Under Warden

An important cleanup has already happened: the project naming has been unified from EVT to Warden.

That affects:

- repository naming;
- document naming;
- module naming;
- data-file naming;
- paper wording.

The point is to stop mixed EVT / Warden naming from creating avoidable confusion.

### 6.3 Data Fields And File Structure Are Being Stabilized

The project is actively freezing:

- which files exist under each captured sample;
- what metadata files such as `env.json` and `meta.json` should mean;
- where auto labels, rule labels, and manual labels belong;
- which fields should stop changing casually.

That work directly affects reproducibility, script stability, paper consistency, and the ability to add more data later without breaking the pipeline.

## 7. The Main Research Line Has Shifted To Web Social-Engineering Threat Judgment

This is the most important direction change so far.

The project no longer limits itself to:

- traditional phishing-site detection;
- pure brand recognition;
- reference-list lookup style recognition.

It is explicitly moving toward web social-engineering threat judgment.

That matters because:

1. The research object becomes broader than classic fake-login pages.
2. The threat semantics become richer, covering credentials, payments, wallets, verification, and induced actions.
3. The method framing becomes more correct: brand evidence helps, but it is not the whole threat.
4. The problem becomes more realistic for real-world webpages.
5. The paper story becomes easier to extend toward open-world, adversarial, generalization, and explainability directions.

## 8. What Is Still Not Finished

Several important things are still unfinished:

- the large-scale high-quality dataset is not yet fully accumulated;
- the full label layer is not yet fully stabilized and verified;
- the brand lexicon is still expanding;
- formal training, system evaluation, and ablation work are not yet complete;
- adversarial robustness and open-world generalization remain future priorities rather than completed deliverables.

The current stance is straightforward: define the problem correctly and stabilize the data first, then chase model results.

## 9. Current-Stage Summary

As of 2026-03-16, the practical state of Warden is:

- the project direction has been upgraded from narrow phishing detection to web social-engineering threat judgment;
- the staged L0 / L1 / L2 system shape is already defined;
- data work is still the current mainline focus;
- the model route has converged toward lightweight text plus lightweight vision plus fusion or distillation support;
- engineering docs and repository contracts are being built out;
- the immediate goal is to stabilize the foundation rather than chase a leaderboard.

In one sentence: Warden is turning web threat judgment from a loose idea into a reproducible data-label-model-engineering system.

## 10. Recommended Current Use Of This README

At the current stage, this README is best used as:

- the repository front-page overview;
- a stage-status explanation of the project;
- shared background material for collaborators and model agents;
- an upper-level summary that can feed later `PROJECT.md`, `MODULE_*.md`, and paper materials.

As the dataset, training, and experiments mature, this README can later grow into a broader entry point for data structure, module relations, training and inference entry points, experimental milestones, and paper alignment.

### Original Chinese Source

The original Chinese source text is kept below for human readers and traceability.

# Warden

> 截至 2026-03-16，Warden 正在从“传统钓鱼网站检测”进一步收敛为一个**网页社会工程威胁判断系统**。项目当前重点不是做一个花里胡哨的大而全平台，而是先把**数据、标签、分层判断逻辑、轻量模型路线、工程化落地约束**这几件硬骨头啃下来。

---

## 1. 项目现在在做什么

Warden 当前在做的事情，可以概括为一句话：

**把网页是否存在社会工程诱导、凭证索取、品牌冒充、误导跳转、支付/钱包诱导等风险，做成一个可数据化、可训练、可分层部署、可解释的判断系统。**

这意味着，Warden 不再只盯着“这个网页是不是某品牌钓鱼页”这一件事，而是把研究对象扩大成：

- 网页是否在实施社会工程诱导；
- 网页是否存在明显的账号、密码、验证码、助记词、钱包授权、支付信息等索取意图；
- 网页是否在伪装成知名品牌、平台、机构或服务；
- 网页风险是否足够高，需要进入更高层级模型复核；
- 在边缘部署、轻量推理、低成本约束下，能否仍然保持可用的识别效果。

换句话说，Warden 的目标不是做一个只会认 logo 的“品牌脸盲矫正器”，而是做一个能综合网页截图、HTML、URL、表单、品牌线索与行为意图的**网页威胁判断器**。

---

## 2. 当前已经明确的项目定位

### 2.1 研究定位

Warden 当前的研究定位是：

**面向真实网页场景的轻量级、多模态、分层式社会工程威胁判断。**

核心特点不是单一模态，也不是单一步骤，而是：

1. **多模态输入**：网页截图、HTML 文本、URL、表单元素、品牌线索、页面元数据等；
2. **分层判断**：按风险强弱走 L0 / L1 / L2，不把所有样本都硬塞给最重模型；
3. **轻量优先**：优先考虑边缘部署与成本约束，而不是默认拿大模型暴力碾；
4. **威胁导向**：核心问题从“品牌识别”上升为“社会工程威胁判断”；
5. **可解释与工程化**：标签体系、字段结构、数据清单、规则补标、模型接口尽量固定，避免后期论文和工程一起翻车。

### 2.2 与传统钓鱼检测的区别

Warden 当前已经明确不再满足于传统的二分类思路：

- 不是只看 phishing / benign；
- 不是只看 logo 是否匹配；
- 不是只依赖 reference list；
- 不是只做学术数据集上的静态检测。

它更关心的是：

**网页是否正在通过页面结构、文案、交互和视觉伪装，诱导用户做出高风险行为。**

这使得 Warden 更接近“网页社会工程分析”，而不是单纯的“品牌冒充识别”。

---

## 3. 当前的系统形态：L0 / L1 / L2

截至今天，Warden 的系统设计已经明确采用分层架构。

### L0：轻量快速筛查层

L0 的目标不是做最终裁决，而是做**低成本初筛**：

- 快速检查 URL、可见文本/标题、表单摘要、网络摘要，以及已存在的低成本 diff/evasion 可观测信号；
- 识别明显的 `gambling / adult / gate` 专项表面和高风险路由锚点；
- 仅在策略允许且低成本证据足够可观测时，让低风险样本低成本停止；
- 把可疑样本送往更强层级复核。

这一层强调：

- 快；
- 小；
- 能在边缘侧或资源受限环境中跑起来；
- 默认不吃完整 HTML、不做默认品牌提取、不吃截图/OCR、不做重交互恢复；
- 宁可保守路由，也不追求单层“全能”。

### L1：多模态风险判断层

L1 是当前设计中的主力层，负责把多个线索拼起来看：

- 页面截图中的视觉冒充；
- HTML 中的品牌、文案、交互语义；
- URL 与页面内容的一致性/冲突；
- 表单是否索要敏感信息；
- 是否出现登录、验证、支付、钱包连接、恢复短语等危险意图。

这一层的任务是：

- 输出更稳的风险判断；
- 给出更细的风险标签；
- 为 L2 提供更高质量的候选样本与证据。

### L2：强判定 / 复核层

L2 当前更多是研究与扩展方向，主要负责：

- 处理高风险、高歧义、开放世界样本；
- 做更强的多模态复核与一致性判断；
- 作为未来对抗、泛化、复杂案例分析的承载层。

现阶段，L2 不是优先做“大而重”，而是先在整体框架里预留位置，避免后续系统结构推倒重来。

---

## 4. 当前最核心的工作重心：数据与标签

到今天为止，Warden 最核心的工作其实不是“训练出一个漂亮分数的模型”，而是**把数据基础设施定稳**。

### 4.1 数据采集在持续推进

当前项目已经围绕网页采集建立了比较明确的数据思路，采集对象不只是页面截图，还包括：

- screenshot / 页面截图；
- HTML；
- URL；
- 页面元信息；
- 表单与交互相关线索；
- 品牌候选信息；
- 自动规则补充信息。

目标不是攒一堆散装样本，而是形成**可复现、可检查、可补标、可训练**的数据资产。

### 4.2 标签体系正在 V1 冻结

当前已明确，Warden 先把标签体系做成 **V1 稳定版**，减少后期字段反复改名、语义漂移、脚本不兼容的问题。

当前标签设计已经从“是否钓鱼”扩展到更细粒度的风险描述，重点围绕：

- 基础类别；
- 风险标签；
- 品牌标签；
- 页面意图标签；
- 凭证/支付/钱包等敏感索取标签；
- 自动规则生成的辅助标签；
- 人工修订与离线补标结果。

目前的原则是：

- **字段名尽量冻结**；
- **标签语义尽量固定**；
- **允许补值，不轻易改结构**；
- **先保证论文和训练流水线能稳定跑通**。

### 4.3 自动补标 + 人工校正并行

Warden 当前不是走纯人工全量标注，也不是迷信规则自动标完就万事大吉，而是采用：

**自动规则补标 + 小批量人工校正 + 逐步固化标签标准**。

当前你已经在推进的重点包括：

- 对已抓取数据进行离线补标；
- 通过品牌字典增强自动识别；
- 检查规则标签的覆盖率与误标情况；
- 先在小批量样本上验证，再逐步扩大。

这一步很关键。因为如果数据标签本身发癫，后面模型再聪明也只是高性能胡说八道机。

---

## 5. 当前模型路线：轻量、多模态、可部署

到今天为止，Warden 的模型方向已经有比较清晰的约束。

### 5.1 文本塔与视觉塔路线已基本明确

当前讨论中，Warden 倾向采用：

- **文本塔**：DistilBERT / TinyBERT 一类轻量编码器；
- **视觉塔**：MobileNetV3-Small、MobileNetV4 等轻量视觉骨干；
- **教师模型 / 蒸馏来源**：更强的 CLIP 类或多模态教师；
- **融合与门控**：用于整合 URL、HTML、截图、表单、品牌线索等证据。

这条路线的核心不是追逐最大模型，而是：

- 控制参数量；
- 控制显存与部署成本；
- 兼顾精度、速度与可迁移性；
- 支持 L0/L1/L2 逐层分工。

### 5.2 边缘部署约束不是附属条件，而是前提条件

Warden 当前很明确的一点是：

**“能落地”不是最后再考虑的事，而是设计一开始就纳入约束。**

所以当前模型选择和系统设计都在围绕这些现实问题收缩：

- 单卡资源有限；
- 推理成本不能太离谱；
- 不能依赖天天在线更新的大型 reference list；
- 不能把所有判断都交给昂贵外部 API；
- 需要在本地/边缘/资源受限场景有可行性。

### 5.3 当前还没有进入“大规模正式训练”阶段

截至今天，Warden 的工作重点仍然偏向：

- 数据采集；
- 标签体系冻结；
- 品牌字典补全；
- 脚本与目录结构整理；
- 模块边界定义；
- 训练/推理文档准备。

也就是说，项目当前是在**打地基**，不是已经进入“模型排行榜冲分阶段”。这不丢人，反而正常。很多项目死得很快，就是因为地基拿牙签搭。

---

## 6. 当前正在推进的工程化工作

Warden 不是只停留在“想法不错”，而是在把想法往工程结构上压实。

### 6.1 仓库与模块文档正在成型

当前已经围绕 Warden 逐步形成和补齐以下文档/模块设计方向：

- 项目总览文档；
- 仓库目录建议；
- 数据模块文档；
- 标注模块文档；
- 训练模块文档；
- 推理模块文档；
- 论文模块文档；
- 协作与任务模板文档。

这些文档的作用不是“看起来很专业”，而是减少多人/多模型/多轮迭代时的语义漂移。

### 6.2 命名与结构已经统一到 Warden

当前项目已完成一个重要但很容易被忽视的动作：

**项目命名从 EVT 统一切换为 Warden。**

这意味着后续：

- 仓库名称；
- 文档名称；
- 模块命名；
- 数据文件命名；
- 论文表述；

都将围绕 Warden 统一展开，避免 EVT / Warden 混用导致的混乱。

### 6.3 数据字段和文件结构正在固化

当前你已经在推进：

- 明确采集产物下面都有哪些文件；
- 明确 env.json、meta.json 等元数据内容；
- 明确自动标签、人工标签、规则标签分别放哪里；
- 明确哪些字段后续不再轻易改动。

这一步会直接影响：

- 数据统计是否可复现；
- 训练脚本是否稳定；
- 推理论文是否一致；
- 后期补数据时会不会把自己坑进泥潭。

---

## 7. 当前的研究主线已经转向“网页社会工程威胁判断”

这是 Warden 到今天为止最重要的方向变化。

项目当前已经不再把自己局限为：

- 单纯钓鱼网站检测；
- 单纯品牌识别；
- 单纯 reference-list 检索式识别。

而是明确转向：

**网页社会工程威胁判断（Web Social Engineering Threat Judgement）**。

这个转向的含义很大：

1. 研究对象更广：不仅是传统仿冒登录页；
2. 风险语义更丰富：包括凭证、支付、钱包、验证、诱导操作等；
3. 方法更合理：不再把“识别品牌”误当成“识别威胁”的全部；
4. 更贴近真实世界：很多高风险网页并不严格符合经典钓鱼模板；
5. 更有论文延展性：后续可自然扩展到开放世界、对抗、泛化和解释性研究。

这也是 Warden 当前最值得坚持的主线，因为它比“又一个品牌钓鱼检测器”更有研究空间，也更贴近真实攻击面。

---

## 8. 当前项目还没做完什么

实话实说，截至今天，Warden 还有几件关键事情**还没正式完成**：

- 大规模高质量数据集尚未完全收齐；
- 全量标签尚未完成稳定校验；
- 品牌字典仍在持续扩充；
- 正式训练、系统评测与消融实验还没有全面展开；
- 对抗鲁棒性、开放世界泛化等内容目前仍属于后续重点，而非当前已完成部分。

这不代表项目慢，而是说明当前阶段判断是清醒的：

**先把数据和问题定义搞对，再谈模型成绩。**

科研里最怕的不是慢，是从一开始就跑错方向，还越跑越自信，那就很有节目效果了。

---

## 9. 当前阶段总结

截至 2026-03-16，Warden 的实际状态可以总结为：

- **项目方向已完成升级**：从传统钓鱼检测转向网页社会工程威胁判断；
- **系统框架已初步明确**：采用 L0 / L1 / L2 分层架构；
- **数据工作是当前主线**：采集、字段、标签、字典、补标正在持续推进；
- **模型路线已收敛**：轻量文本塔 + 轻量视觉塔 + 融合/蒸馏；
- **工程文档正在成型**：仓库结构、模块文档、任务模板等逐步补齐；
- **当前目标不是冲榜，而是打稳地基**：让后续训练、论文、部署都有统一基线。

一句话概括：

**Warden 现在正在把“网页威胁判断”这件事，从一个概念，压成一个可落地的数据—标签—模型—工程体系。**

这一步不 flashy，但很关键。没有这一步，后面的模型实验很容易只是给混乱数据刷一层漂亮油漆。

---

## 10. 现阶段建议的 README 使用方式

当前这份 README 更适合作为：

- 仓库首页说明；
- 项目阶段性状态说明；
- 与协作者/模型代理沟通时的统一背景材料；
- 后续补写 PROJECT.md、MODULE_*.md、论文摘要时的上位概述。

后续随着数据集规模、模型训练、实验结果推进，这份 README 可以继续扩展为：

- 数据结构说明；
- 模块依赖关系；
- 训练与推理入口；
- 实验结果与里程碑；
- 论文对应关系。

