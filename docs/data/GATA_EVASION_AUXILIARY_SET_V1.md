# Warden Gate / Evasion Auxiliary Set V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Gate / Evasion Auxiliary Set V1

This document defines how Warden should position and handle gate / evasion samples without mixing them into the TrainSet V1 primary training contract.

## 1. Purpose

This file explains:

1. what counts as a gate / evasion sample;
2. why such samples do not enter TrainSet V1 primary by default;
3. how they should be handled across L0 / L1 / L2;
4. how they may still be used for training-adjacent research, evaluation, and analysis;
5. how this protocol stays consistent with the README, the current scripts, and the main training line.

## 2. Applicable Background

Warden's mainline problem is web social-engineering threat judgment, not a dedicated interaction-recovery or anti-bot-bypass system.

Therefore, in Warden V1, gate / evasion behavior is treated as a real deployment-side auxiliary problem rather than the primary training objective itself.

The target sample families include:

- Cloudflare or challenge-style pages;
- CAPTCHA or verify-human pages;
- pages that reveal real content only after further clicking or interaction;
- pages that use gate or verification surfaces to delay or hide real content;
- fake verification or fake CAPTCHA pages that may themselves act as social-engineering pages.

## 3. Relationship To The Mainline Design

### 3.1 It Does Not Change Warden's Main Inputs

Warden still uses multimodal webpage evidence such as:

- screenshots;
- HTML and visible text;
- URLs;
- forms and interaction clues;
- brand evidence;
- page metadata.

### 3.2 It Does Not Change The Main L0 / L1 / L2 Structure

This document adds a special handling protocol for one difficult sample family. It does not redesign the main staged architecture.

### 3.3 It Does Not Redefine TrainSet V1 Primary

TrainSet V1 remains focused on standard page-level primary training samples.

Gate / evasion samples are managed separately and do not automatically enter TrainSet V1 primary.

### 3.4 It Does Not Change Default Script Behavior

This document does not require dataset scripts such as manifest-building or consistency-check scripts to absorb this auxiliary set by default.

If a future script-side interface is added, it should be:

- optional;
- off by default;
- backward compatible;
- non-destructive to primary manifest semantics.

## 4. Positioning Principle

In Warden V1, gate / evasion samples belong to an Auxiliary Set rather than to TrainSet V1 primary.

The reasons are:

1. These samples are meaningful and should not simply be thrown away.
2. They often do not stably represent a fully exposed page-level landing sample.
3. If they are merged directly into the main primary set, the model may learn gate pages as if they were the final malicious page.
4. They are better used as:
   - L2 escalation candidates;
   - auxiliary evaluation material;
   - case-study / error-analysis / robustness-analysis material;
   - future interaction-recovery inputs.

## 5. Sample Scope

### 5.1 Gate / Challenge Pages

A sample may be treated as a gate / challenge candidate when it explicitly shows things like:

- verify-you-are-human language;
- CAPTCHA, Cloudflare, or challenge semantics;
- a need for extra interaction before the main content appears;
- page structure that looks like a gate page rather than a final business page.

### 5.2 Evasion / Cloaking Pages

A sample may be treated as an evasion / cloaking candidate when:

- the current page content does not match the threat context of the input URL;
- the main content is hidden until later clicks, waits, or interactions;
- scripts, gates, or light interaction block direct capture of the real content;
- the current evidence is insufficient but the page still does not look like a normal low-risk page.

### 5.3 Fake Verification / Fake CAPTCHA Pages

If a page outwardly presents gate / verification / CAPTCHA semantics but already performs social-engineering induction, for example by pushing the user to:

- download or install something;
- copy and paste commands;
- grant dangerous approvals or perform risky actions;

then its threat nature is no longer equivalent to an ordinary gate page. Such samples may later be upgraded into true social-engineering threat pages during review.

## 6. Core Handling Principles

### 6.1 Keep Them, But Do Not Merge Them Into TrainSet V1 Primary

These samples should be preserved. They should not be deleted casually. But by default they should not be merged into the TrainSet V1 primary training set.

### 6.2 Recognize First, Then Escalate

Warden V1 uses a recognize-and-escalate strategy for this family rather than trying to solve interaction recovery directly in L1.

### 6.3 Put Heavy Interactive Handling In L2, Not L1

L1 should identify likely gate / evasion behavior and prepare escalation. L2 should carry the higher-cost interactive attempts and deeper review.

### 6.4 L2 Should Only Process The Escalated Subset

L2 is not supposed to process the full corpus with equal cost. It should only process the escalated gate / evasion subset.

## 7. Staged Handling Protocol

## 7.1 L0 Responsibilities

L0 only performs cheap screening. It does not try to bypass gates or complete heavy interactions.

L0 may:

- extract URL, DOM, text, and basic visual signals;
- detect obvious verify-human / CAPTCHA / Cloudflare / challenge keywords;
- detect visible gate-page cues;
- forward suspicious samples to L1.

### 7.2 L1 Responsibilities

L1 is the main judgment layer, but under this protocol it should not:

- directly break through gates;
- perform full click-through recovery;
- hard-label a challenge page as if it were already the final page.

Its responsibilities are to:

1. combine screenshot, HTML, text, URL, form, and weak-label evidence;
2. determine whether the sample currently looks more like:
   - a normal page-level sample;
   - a gate / challenge page;
   - an unresolved evasion candidate;
   - a fake verification or fake CAPTCHA social-engineering page;
3. recommend escalation where needed;
4. prepare evidence summaries for L2.

### 7.3 L2 Responsibilities

L2 handles the escalated gate / evasion subset.

Possible L2 actions include:

- light interaction or clicking;
- continuing the page flow;
- recording before / after state changes;
- consistency and diff analysis across stages;
- stronger review of ambiguous samples;
- final routing into categories such as ordinary gate page, unresolved evasion, recovered landing page, fake verification page, or other abnormal sample.

## 8. Relationship To Dataset And Training

### 8.1 It Does Not Enter Primary Training By Default

This auxiliary set does not automatically enter TrainSet V1 primary. Its existence does not redefine the main training set.

### 8.2 It Should Be Preserved As An Auxiliary Set

Its main uses include:

- L2 escalation input;
- robustness and deployment-oriented evaluation;
- cloaking and evasion case studies;
- error analysis;
- human-review candidate pools.

### 8.3 Adversarial Recovery Is Not The Main V1 Training Goal

Warden V1 remains focused on page-level social-engineering threat recognition. Gate / evasion recovery is not the main supervised-training target.

## 9. Recommended Usage

### 9.1 As An Auxiliary Evaluation Set

After the main model is trained, this set can be used to evaluate:

- whether ordinary gate pages are wrongly judged as final malicious pages;
- whether the system can reliably identify samples that should escalate to L2;
- whether fake verification or fake CAPTCHA pages remain detectable;
- whether the model behaves conservatively on complex evidence.

### 9.2 As An Escalation Trigger Set

Samples may be prioritized for L2 when they show signals such as:

- verify-human / CAPTCHA / Cloudflare / challenge semantics;
- hidden or unrevealed main content;
- a high-risk input URL but insufficient current page evidence;
- anti-bot, cloaking, or interaction-required signals.

### 9.3 As A Case-Study / Error-Analysis Set

This set is suitable for:

- gate / evasion phenomenon categorization;
- model error analysis;
- before / after interaction comparison;
- adversarial or robustness appendices.

## 10. Consistency With The README

This document does not change the main README claims that:

1. Warden is a web social-engineering threat judgment system.
2. The inputs remain screenshots, HTML, URLs, forms, brand evidence, and metadata.
3. The system still uses an L0 / L1 / L2 staged design.
4. The mainline focus is still data, labels, weak-rule backfill, training routes, and lightweight model design.
5. Adversarial or anti-gate work exists, but it is not the center of V1.

This document only adds one clarification:

gate / evasion is a real deployment-side subproblem, and Warden V1 keeps it as an auxiliary sample set plus escalation protocol rather than redefining the main training set around it.

## 11. Recommended Current Execution Stance

At the current stage, the recommended stance is:

- TrainSet V1 primary stays dedicated to standard page-level training;
- current dataset scripts remain focused on that primary path by default;
- the Gate / Evasion Auxiliary Set is kept separately, documented separately, and evaluated separately;
- L1 recognizes and escalates but does not do heavy interaction;
- L2 handles only the escalated subset;
- README and paper framing stay centered on web social-engineering threat recognition rather than anti-evasion recovery.

## 12. Definition Of Done

This auxiliary protocol can be considered established when:

- the repository contains a dedicated document for gate / evasion positioning;
- the document explicitly states that the set is not part of TrainSet V1 primary;
- the L1 and L2 responsibility boundary is explicit;
- the main uses are stated as auxiliary evaluation, escalation, and case study;
- the document explicitly states that the README main design and main input definition are unchanged.

### Original Chinese Source

The original Chinese source text is kept below for human readers and traceability.

# Warden Gate / Evasion Auxiliary Set V1

版本：v1.0  
状态：Draft  
放置位置：`docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

命名说明：

- 当前仓库中的实际文件名保留为 `GATA_EVASION_AUXILIARY_SET_V1.md`
- 本文讨论的语义对象仍然是 gate / evasion auxiliary set
- 当前阶段先统一文档引用与工程口径，不在本任务中重命名文件路径

---

## 1. 文档目的

本文件用于定义 Warden 中 gate / evasion 类样本的定位、处理方式与使用边界。

本文件不是主训练集规范，不替代 `TRAINSET_V1.md`，也不修改冻结数据结构。  
本文件只回答以下问题：

1. 什么是 gate / evasion 类样本；
2. 为什么这类样本不进入 TrainSet V1 primary；
3. 这类样本在 Warden 的 L0 / L1 / L2 中如何处理；
4. 这类样本在训练、评估、分析中的用途是什么；
5. 本文件与 README 主设计、当前抓取脚本、现有训练主线的关系是什么。

---

## 2. 适用背景

Warden 当前主线是“网页社会工程威胁判断”，而不是单独做对抗恢复系统。  
因此，gate / evasion 问题在 Warden V1 中被视为现实部署中必须承认的辅助问题，而不是主训练任务本身。

本文件针对的对象包括但不限于：

- Cloudflare / challenge / verify-human 类型门页；
- CAPTCHA / anti-bot / needs-interaction 页面；
- 仅在进一步点击、验证、交互后才暴露真实内容的页面；
- 利用 gate / verification 外观进行规避、延迟暴露或阶段隐藏的页面；
- 与之相近、但本身可能是社会工程诱导页的 fake captcha / fake verification 页面。

---

## 3. 与主线设计的关系

### 3.1 不改变 Warden 主输入

本文件不改变 Warden 当前主输入设计。  
Warden 仍以多模态网页证据为核心输入，包括但不限于：

- screenshot / 页面截图
- HTML / 可见文本
- URL
- 表单与交互线索
- 品牌线索
- 页面元信息

### 3.2 不改变 Warden 主系统分层

本文件不改变 Warden 的 L0 / L1 / L2 主架构。  
本文件只是对其中一类特殊样本给出附加协议。

### 3.3 不改变 TrainSet V1 主定义

本文件不修改 `TRAINSET_V1.md` 的主训练集定义。  
TrainSet V1 仍然面向页面级 primary 训练样本。  
gate / evasion 类样本单独管理，不并入 TrainSet V1 primary。

### 3.4 不改变当前 data scripts 的默认行为

本文件不要求 `scripts/data/build_manifest.py` 或 `scripts/data/check_dataset_consistency.py` 默认感知、默认纳入或默认扩展处理本集合。  
当前阶段，auxiliary set 与 TrainSet V1 primary 的边界主要通过文档与任务口径冻结。  

若后续需要脚本侧接口：

- 必须是可选开启
- 必须默认关闭
- 必须保持向后兼容
- 不得改变 TrainSet V1 primary manifest 的核心语义

---

## 4. 定位原则

Warden V1 对 gate / evasion 类样本的定位是：

> 它们属于 Auxiliary Set（辅助样本集），而不是 TrainSet V1 primary。

原因如下：

1. 这类样本具有现实意义，不能简单删除；
2. 这类样本通常不能稳定代表“已暴露完整主体内容的标准页面级样本”；
3. 若直接并入 primary，容易把“反机器人门页”误学成“恶意主体页面”；
4. 这类样本更适合作为：
   - L2 升级触发对象；
   - 辅助评估集合；
   - case study / error analysis / robustness analysis 集合；
   - 后续交互式恢复与复杂复核的输入集合。

---

## 5. 样本范围

本文件中的 gate / evasion Auxiliary Set 包括以下页面类型：

### 5.1 Gate / Challenge 页面

满足以下之一的页面可视为 gate / challenge 候选：

- 页面显式要求 verify you are human；
- 页面显式出现 captcha / cloudflare / challenge / attention required 等拦截语义；
- 页面主体内容尚未展开，且需要进一步交互才能继续；
- 页面结构明显属于门页、检查页、验证页，而非最终业务落地页。

### 5.2 Evasion / Cloaking 页面

满足以下之一的页面可视为 evasion / cloaking 候选：

- 当前页面内容与输入 URL 的威胁上下文不一致；
- 页面主体信息被阶段性隐藏，需要点击、等待或额外交互才呈现；
- 页面通过门页、脚本、延迟跳转或其他轻交互方式阻断直接内容采集；
- 样本表现出“当前证据不足，但并非正常低风险页面”的特征。

### 5.3 Fake Verification / Fake CAPTCHA 页面

若页面表面上呈现 gate / verification / captcha 语义，但其本身已经承担社会工程诱导作用，例如：

- 诱导下载、安装、执行；
- 诱导复制粘贴命令；
- 诱导额外授权、连接或危险操作；

则该页面虽可保留在本集合说明中，但其风险性质不再等同于普通 gate 页。  
这类页面在后续复核中可被提升为真正的社会工程威胁页面。

---

## 6. 核心处理原则

### 6.1 保留，但不纳入 TrainSet V1 primary

这类样本应保留，不建议简单删除。  
但默认不纳入 TrainSet V1 primary，不作为标准页面级监督训练样本。

### 6.2 先识别，再升级，不在 L1 直接强行解锁

Warden V1 对这类样本采用“识别并升级”的策略，而不是在 L1 直接做重交互恢复。

### 6.3 交互式处理放在 L2，而不是 L1

L1 的职责是识别“这可能是 gate / evasion 类页面”，并把样本送往 L2。  
L2 才负责更高成本、更完整的交互式尝试和复核分析。

### 6.4 L2 只处理升级子集，不处理全量样本

L2 不应对全量样本一视同仁地启用重处理。  
L2 只针对被升级的 gate / evasion 候选子集执行更完整的点击、交互、恢复、差分与复核流程。

---

## 7. 分层处理协议

## 7.1 L0 的职责

L0 只做低成本初筛，不负责解 gate 或完成复杂交互。  
L0 可做的事情包括：

- 抽取 URL / DOM / 文本 / 基础视觉信号；
- 检测明显的 verify-human / captcha / cloudflare / challenge 关键词；
- 检测页面是否具有明显的门页特征；
- 将可疑样本送往 L1。

L0 的目标是“发现像 gate / evasion 的东西”，而不是“解决它”。

## 7.2 L1 的职责

L1 是主判断层，但在本协议下：

- L1 不负责直接穿透 gate；
- L1 不负责完整点击恢复；
- L1 不负责把 challenge 页硬判成最终主体页面。

L1 的职责是：

1. 结合截图、HTML、文本、URL、表单与弱标签证据；
2. 识别当前页面是否更像：
   - 正常页面级主体样本；
   - gate / challenge 页；
   - unresolved / evasion 候选；
   - 可能的 fake verification / fake captcha 诱导页；
3. 对疑似 gate / evasion 样本给出升级建议；
4. 为 L2 提供候选样本与证据摘要。

## 7.3 L2 的职责

L2 负责处理被升级的 gate / evasion 子集。  
L2 可承担的动作包括：

- 尝试点击或轻交互；
- 尝试继续页面流程；
- 记录前后状态变化；
- 对交互前后页面做一致性和差分分析；
- 对高歧义样本做更强复核；
- 将样本分流为：
  - 普通 gate 页；
  - unresolved evasion；
  - 已恢复的真实落地页；
  - fake verification / fake captcha 社工页；
  - 其他异常样本。

L2 的定位是“高成本复核层”，不是默认全量处理层。

---

## 8. 与数据集和训练的关系

### 8.1 不进入主训练 primary

本集合样本默认不进入 TrainSet V1 primary。  
其存在不应改变主训练样本的定义。

### 8.2 可作为 Auxiliary Set 保留

本集合应被保留为 Auxiliary Set。  
其主要用途包括：

- L2 升级输入；
- robustness / deployment-oriented evaluation；
- cloaking / evasion case study；
- error analysis；
- 人工复核候选池。

### 8.3 不把对抗恢复作为 V1 主训练目标

Warden V1 的主训练目标仍然是页面级社会工程威胁识别。  
gate / evasion 恢复不作为 V1 主监督训练目标。

---

## 9. 建议的使用方式

Warden V1 对本集合建议采用以下使用方式：

### 9.1 作为辅助评估集

主模型训练完成后，可单独在本集合上评估：

- 是否会把普通门页错误强判为恶意主体页；
- 是否能稳定识别“需要升级到 L2”的样本；
- 是否对 fake verification / fake captcha 样本保留足够敏感性；
- 是否对复杂样本保持保守而不是盲判。

### 9.2 作为升级触发集

若样本命中以下任一现象，可优先进入 L2：

- verify-human / captcha / cloudflare / challenge 语义明显；
- 页面主体内容未展开；
- 输入 URL 已知高风险，但当前页面缺乏完整主体信息；
- 页面存在明显 anti-bot / cloaking / needs-interaction 信号。

### 9.3 作为 case study / error analysis 集

本集合适合单独做：

- gate / evasion 现象归类；
- 主模型误判分析；
- 交互前后变化分析；
- 对抗相关附录实验。

---

## 10. 与 README 的一致性说明

本文件不改变 README 中的以下主线：

1. Warden 仍然是网页社会工程威胁判断系统；
2. 输入仍然是截图、HTML、URL、表单、品牌线索、元信息等多模态网页证据；
3. 系统仍然采用 L0 / L1 / L2 分层；
4. 当前主线仍然是数据、标签、规则补标、训练通路与轻量模型路线；
5. 对抗问题存在，但不是 V1 主线中心。

本文件只是补充说明：

> gate / evasion 属于现实网页环境中的特殊子问题，Warden V1 承认其存在并保留其样本，但将其定位为辅助样本集与升级处理协议，而不是主训练定义本身。

---

## 11. 当前阶段建议执行口径

在当前阶段，建议统一采用以下口径：

- TrainSet V1 primary：只用于标准页面级主训练；
- 当前 data scripts 默认仍面向 TrainSet V1 primary，不默认把 auxiliary set 并入 primary manifest；
- Gate / Evasion Auxiliary Set：单独保存、单独说明、单独评估；
- L1：只识别并升级，不负责重交互；
- L2：只处理升级子集，负责交互式恢复与复核；
- 论文与 README 主线：仍聚焦网页社会工程威胁识别，不把对抗恢复写成核心贡献。

---

## 12. Definition of Done

当以下条件满足时，可认为本辅助协议已建立：

- 仓库中存在独立文档说明 gate / evasion 的定位；
- 文档明确其不属于 TrainSet V1 primary；
- 文档明确 L1 与 L2 的职责边界；
- 文档明确其主要用途是辅助评估、升级处理与 case study；
- 文档明确其不改变 README 主设计与主输入定义。
