# Warden_FRONTIER_TECH_WATCHLIST_2026

## 中文版

### 1. 文档定位

本文件是 **Warden 的前沿技术观察清单（watchlist）**，用于记录**值得持续跟踪、但尚未冻结为默认主线实现**的外部技术方向。

本文件不是：

- 默认训练方案文档
- 默认部署方案文档
- 已冻结的模型选择文档
- 立即执行的任务单

本文件的作用是：

1. 记录与 Warden 当前方向高度相关的新技术。
2. 区分“论文可信”与“对 Warden 可直接落地”之间的差异。
3. 给后续实验、二审与路线升级提供候选池。
4. 防止外部新论文被过度神化后直接污染当前主线。

---

### 2. 当前结论

截至 2026 年 3 月，本 watchlist **仅保留两条方向**：

1. **Agentic Knowledge Distillation（Agentic KD）**
2. **SpecularNet**

以下方向当前**不纳入本 watchlist 的重点保留项**：

- GWO + Random Forest 浏览器扩展路线

原因不是该路线无价值，而是它更适合作为 tabular baseline / ablation 候选，而不是当前 Warden 的前沿升级主线。

---

### 3. 纳入标准

技术被纳入本 watchlist，需要同时满足以下条件：

1. **与 Warden 当前问题空间高度相关**，即与网页社会工程威胁判断、网页结构分析、文本/视觉/结构证据融合或开放世界泛化直接相关。
2. **具备真实外部论文或公开技术出处**，不能仅凭二手转述或模型口头总结纳入。
3. **对 Warden 存在明确的潜在补强点**，而不是只在别的任务上表现好。
4. **不会直接破坏当前冻结边界**，尤其不能要求立即推翻 TrainSet V1、L0/L1 主线或现有边缘部署约束。
5. **值得进入小规模验证实验**，而不是一眼就应判定为与当前阶段无关。

---

### 4. Watchlist Item A：Agentic Knowledge Distillation

#### 4.1 简述

Agentic Knowledge Distillation（Agentic KD）是一类“**离线教师自动化蒸馏**”思路：
由强推理模型或多代理教师在离线阶段生成、修正、迭代高质量监督信号，再将这些知识压缩到小型学生模型中。

#### 4.2 与 Warden 的相关性

对 Warden 而言，Agentic KD 最可能补强的是：

- **L1 文本侧训练质量**
- **概念标签生成质量**
- **弱监督/伪监督信号的上限**
- **零日与高歧义样本的文本概念泛化能力**

它最合理的落点不是运行时推理，而是：

- 离线 teacher labeling
- concept bottleneck supervision
- 训练阶段的数据增强与标签精炼

#### 4.3 当前判断

当前对 Agentic KD 的判断是：

- **论文方向真实，值得保留**
- **与 Warden 有明确互补性**
- **可作为 L1 训练侧升级实验项**
- **暂不应写成默认主线收益承诺**

#### 4.4 当前不能直接下结论的地方

以下说法当前不能直接冻结为 Warden 事实：

- “Agentic KD 一定能把 Warden 的零日 F1 提升 10% 以上”
- “Agentic KD 一定优于单 teacher 标注”
- “Agentic KD 可以直接证明 Warden 的网页场景收益”

原因很直接：现有公开论文主要证明的是**特定任务与特定教师/学生配置**下的效果，而不是对 Warden 当前网页样本分布的直接结论。

#### 4.5 在 Warden 中的正确定位

Agentic KD 在 Warden 中应被定义为：

**训练侧候选增强项，而不是默认运行时组件。**

建议实验问题：

1. 单教师概念打标 vs agentic 多代理概念打标，哪个对 L1 文本概念头更稳？
2. 在 Warden 的真实网页样本上，agentic teacher 是否真的比普通 teacher 带来更好的零日泛化？
3. Agentic KD 的额外成本，是否值得相对于普通 teacher labeling 承担？

#### 4.6 进入主线的前置条件

只有在满足以下条件后，Agentic KD 才应考虑进入更正式文档：

- 在 Warden 自有数据上完成 A/B 对照
- 相比普通 teacher labeling，有稳定且可复现的增益
- 不引入不可接受的标注成本或流程复杂度
- 输出标签格式能对齐当前冻结 schema 与训练流程

---

### 5. Watchlist Item B：SpecularNet

#### 5.1 简述

SpecularNet 是一条 **reference-free 的网页钓鱼/恶意网页结构检测路线**。
它强调：

- 不依赖大型外部品牌知识库
- 不依赖复杂多模态重管线
- 只依赖轻量输入（如 domain + HTML / DOM structure）
- 在标准 CPU 上保持较快推理

#### 5.2 与 Warden 的相关性

对 Warden 而言，SpecularNet 最有价值的地方不是替代现有 L1 文本/视觉路线，而是补充：

- **结构侧独立复核能力**
- **reference-free fallback 能力**
- **开放世界 / 0-day 结构泛化能力**
- **对仅依赖文本或视觉时的盲区补强**

它尤其适合未来这些方向：

- DOM/domain 轻量复核分支
- 结构一致性辅助判断
- 未来 L2 或 L1-structure 支路候选

#### 5.3 当前判断

当前对 SpecularNet 的判断是：

- **论文方向真实，且技术含金量较高**
- **与 Warden 的互补性很强**
- **比一般“再加一个大模型”更符合当前工程方向**
- **值得作为未来结构侧重点候选保留**

#### 5.4 当前不能直接下结论的地方

以下说法当前不能直接冻结为 Warden 事实：

- “SpecularNet 接进来就能让 Warden 0-day 召回提升 15–25%”
- “SpecularNet 可以一周内无痛替换成 L2 兜底主模块”
- “SpecularNet 等价于 benign reference KB 异常检测器”

原因是：SpecularNet 的论文原型是**reference-free 的结构建模检测器**，它不是一个“只靠 benign 知识库做 anomaly score”的简单替代品。

#### 5.5 在 Warden 中的正确定位

SpecularNet 在 Warden 中应被定义为：

**未来结构复核/结构分支的重点候选技术，而不是当前 V1 的默认模块。**

更准确地说，它适合作为：

- L1 之后的结构复核候选
- L2 预研方向候选
- 结构侧独立支路候选

而不应被直接改写成：

- “reference KB build 脚本扩展版”
- “SQLite + NetworkX 的轻量 anomaly 模块”

#### 5.6 进入主线的前置条件

只有在满足以下条件后，SpecularNet 才应考虑进入更正式文档：

- 明确其输入契约与当前 Warden 样本结构的对接方式
- 证明它能在 Warden 当前数据上提供独立增益
- 明确它是作为 L1 支路、L2 支路，还是单独的结构模型存在
- 明确部署成本与现有边缘约束是否兼容

---

### 6. 当前不保留的方向：GWO-RF

#### 6.1 当前判断

GWO + Random Forest 路线并非无效，但当前不作为前沿 watchlist 的重点保留项。

#### 6.2 原因

1. 它更像 **tabular 特征选择 / baseline 增强路线**。
2. 它与 Warden 当前的结构升级、零日补强、开放世界补强相比，战略意义较小。
3. 它更适合在具体实验阶段做：
   - RF baseline
   - XGBoost baseline
   - GWO+RF 对照实验
4. 它不应抢占 Agentic KD 和 SpecularNet 这种更具潜在战略价值的升级方向。

因此，当前结论为：

**不删除该方向的存在价值，但不纳入本 watchlist 的重点保留清单。**

---

### 7. 对当前 Warden 主线的影响

本 watchlist 的两条技术，当前都**不改变**以下主线结论：

1. Warden V1 的默认主线仍然是 L0 + L1。
2. L1 当前主设计仍然围绕：
   - 文本轻量编码器
   - 视觉轻量编码器
   - 触发式 OCR
   - 原子 detector
   - late fusion
3. L2 当前仍然先冻结职责，不冻结完整实现。
4. 当前训练、推理、部署文档不应因为 watchlist 的存在而直接改写成“默认启用新技术”。

换句话说：

**watchlist 是前沿候选池，不是当前主线替代品。**

---

### 8. 推荐的后续动作

#### 8.1 Agentic KD

建议作为 **训练侧小规模验证实验**：

- 对比对象：普通单 teacher 概念打标
- 验证目标：
  - 概念标签质量
  - 文本概念头效果
  - 零日泛化
  - 成本/增益比

#### 8.2 SpecularNet

建议作为 **结构侧预研实验**：

- 先做 paper reading + input contract mapping
- 再做最小可运行原型
- 最后决定它更适合：
  - L1 结构支路
  - L2 复核支路
  - 独立 fallback 结构模型

---

### 9. 当前冻结结论

截至本文件版本，冻结结论如下：

- **保留**：Agentic KD、SpecularNet
- **不作为当前重点保留项**：GWO-RF
- **不允许**把 watchlist 论文结果直接写成 Warden 既成事实
- **不允许**把 watchlist 技术直接替换当前 V1 主线设计
- **允许**后续围绕这两条方向开小规模验证实验与专项评估

---

### 10. 一句话总结

Warden 当前应把 **Agentic KD** 视为“训练侧教师标注升级候选”，把 **SpecularNet** 视为“未来结构复核/结构分支重点候选”；两者都值得保留，但都还没有资格直接改写当前 V1 主线。

---

## English Version

### 1. Document Positioning

This file is Warden's **frontier technology watchlist**, used to track external technical directions that are **worth following but are not yet frozen as default implementation paths**.

This file is **not**:

- a default training-method document
- a default deployment document
- a frozen model-selection document
- an immediate execution task sheet

Its purpose is to:

1. record new technical directions that are highly relevant to Warden;
2. separate “the paper is real” from “it is directly ready for Warden integration”;
3. provide a candidate pool for later experiments, review, and roadmap upgrades;
4. prevent new external papers from being overhyped and prematurely injected into the current mainline.

---

### 2. Current Conclusion

As of March 2026, this watchlist keeps **only two directions**:

1. **Agentic Knowledge Distillation (Agentic KD)**
2. **SpecularNet**

The following direction is **not retained as a priority item** in this watchlist:

- GWO + Random Forest browser-extension route

This does not mean it has no value.
It means it is currently better treated as a tabular baseline / ablation candidate rather than a frontier upgrade line for Warden.

---

### 3. Inclusion Criteria

A technology enters this watchlist only if it satisfies all of the following:

1. it is highly relevant to Warden's current problem space, including web social-engineering threat judgment, webpage structure analysis, multimodal evidence fusion, or open-world generalization;
2. it has a real external paper or public technical source;
3. it offers a clear potential strengthening point for Warden rather than merely looking good on a different task;
4. it does not require immediate disruption of current frozen boundaries, especially TrainSet V1, the L0/L1 mainline, or current edge-deployment constraints;
5. it is worth entering small-scale validation rather than being obviously irrelevant to the current stage.

---

### 4. Watchlist Item A: Agentic Knowledge Distillation

#### 4.1 Summary

Agentic Knowledge Distillation (Agentic KD) is a family of **offline teacher-driven distillation** approaches.
A strong reasoning model or a multi-agent teacher generates, revises, and iteratively improves high-quality supervision signals offline, and then compresses that knowledge into a smaller student model.

#### 4.2 Relevance to Warden

For Warden, Agentic KD most plausibly strengthens:

- **L1 text-side training quality**
- **concept-label generation quality**
- **the ceiling of weak / pseudo supervision**
- **text-side zero-day and high-ambiguity generalization**

Its most reasonable placement is not runtime inference, but:

- offline teacher labeling
- concept-bottleneck supervision
- training-time data enrichment and label refinement

#### 4.3 Current Judgment

The current judgment on Agentic KD is:

- **the paper direction is real and worth retaining**
- **it has a clear complementarity with Warden**
- **it is suitable as an L1 training-side upgrade candidate**
- **it should not yet be written as a default guaranteed gain for Warden**

#### 4.4 What Cannot Be Concluded Yet

The following statements must not be frozen as Warden facts at this stage:

- “Agentic KD will definitely improve Warden zero-day F1 by more than 10%.”
- “Agentic KD will definitely outperform single-teacher labeling.”
- “Agentic KD already proves gains for Warden's webpage setting.”

The reason is simple: current public evidence shows effectiveness on **specific tasks and specific teacher/student setups**, not on Warden's own webpage distribution.

#### 4.5 Correct Positioning Inside Warden

Inside Warden, Agentic KD should be defined as:

**a training-side enhancement candidate, not a default runtime component.**

Recommended experimental questions:

1. single-teacher concept labeling vs agentic multi-agent concept labeling: which is more stable for Warden's L1 text concept heads?
2. on Warden's real webpage samples, does an agentic teacher truly improve zero-day generalization over a standard teacher?
3. is the extra cost of Agentic KD justified relative to ordinary teacher labeling?

#### 4.6 Preconditions Before Entering the Mainline

Agentic KD should only be considered for more formal Warden documents if all of the following are satisfied:

- A/B validation is completed on Warden-owned data;
- it shows stable and reproducible gains over ordinary teacher labeling;
- it does not introduce unacceptable annotation cost or workflow complexity;
- its output labels align with the current frozen schema and training process.

---

### 5. Watchlist Item B: SpecularNet

#### 5.1 Summary

SpecularNet is a **reference-free webpage phishing / malicious-page structural detection** direction.
It emphasizes:

- no reliance on large external brand knowledge bases;
- no reliance on heavy multimodal pipelines;
- lightweight inputs such as domain plus HTML / DOM structure;
- fast inference on standard CPUs.

#### 5.2 Relevance to Warden

For Warden, the main value of SpecularNet is not to replace the current L1 text/vision path, but to supplement:

- **independent structure-side review capability**
- **reference-free fallback capability**
- **open-world / zero-day structural generalization**
- **coverage of blind spots left by text-only or vision-only cues**

It is especially relevant to future directions such as:

- a lightweight DOM/domain review branch
- structure-consistency-assisted judgment
- a future L2 or L1-structure side branch

#### 5.3 Current Judgment

The current judgment on SpecularNet is:

- **the paper direction is real and technically meaningful**
- **its complementarity with Warden is strong**
- **it matches Warden's engineering direction better than simply adding another heavyweight model**
- **it should be retained as a priority candidate for future structure-side work**

#### 5.4 What Cannot Be Concluded Yet

The following statements must not be frozen as Warden facts at this stage:

- “Plugging in SpecularNet will automatically improve Warden zero-day recall by 15–25%.”
- “SpecularNet can painlessly become the default L2 fallback module within one week.”
- “SpecularNet is equivalent to a benign reference-KB anomaly detector.”

The reason is that the paper prototype is a **reference-free structural detector**, not a simple “benign knowledge-base anomaly score engine.”

#### 5.5 Correct Positioning Inside Warden

Inside Warden, SpecularNet should be defined as:

**a priority candidate for future structural review / structural branching, not a default V1 module.**

More precisely, it is suitable as a candidate for:

- a structure-review branch after L1,
- an L2 pre-research direction,
- an independent structure-side model.

It should **not** be directly rewritten as:

- “an extension of the reference-KB build script,” or
- “a lightweight anomaly module based on SQLite plus NetworkX.”

#### 5.6 Preconditions Before Entering the Mainline

SpecularNet should only be considered for more formal Warden documents if all of the following are satisfied:

- its input contract is mapped clearly to the current Warden sample structure;
- it demonstrates independent gain on Warden's current data;
- its role is made explicit: L1 side branch, L2 side branch, or separate structural model;
- its deployment cost is shown to be compatible with current edge constraints.

---

### 6. Direction Not Retained as a Priority: GWO-RF

#### 6.1 Current Judgment

The GWO + Random Forest route is not treated as invalid, but it is not currently retained as a priority item in this frontier watchlist.

#### 6.2 Reasons

1. It is closer to a **tabular feature-selection / baseline-enhancement route**.
2. Compared with Warden's current needs in structural upgrading, zero-day reinforcement, and open-world support, its strategic importance is lower.
3. It is better suited for concrete experiment-stage comparisons such as:
   - RF baseline
   - XGBoost baseline
   - GWO+RF ablation
4. It should not displace Agentic KD and SpecularNet, which currently have stronger strategic upside for Warden.

Therefore, the current conclusion is:

**its existence value is not denied, but it is not retained in this watchlist as a priority item.**

---

### 7. Impact on the Current Warden Mainline

The two retained watchlist items do **not** change the following current mainline conclusions:

1. Warden V1 still centers on L0 + L1.
2. The current L1 main design still revolves around:
   - a lightweight text encoder,
   - a lightweight vision encoder,
   - triggered OCR,
   - an atomic detector,
   - late fusion.
3. L2 still freezes responsibilities first and does not yet freeze a full implementation.
4. Current training, inference, and deployment documents must not be rewritten as “new technology enabled by default” simply because these items exist in the watchlist.

In other words:

**the watchlist is a frontier candidate pool, not a replacement for the current mainline.**

---

### 8. Recommended Next Actions

#### 8.1 Agentic KD

Recommended as a **small-scale training-side validation experiment**:

- comparator: standard single-teacher concept labeling
- evaluation targets:
  - concept-label quality
  - text concept-head effectiveness
  - zero-day generalization
  - cost / gain ratio

#### 8.2 SpecularNet

Recommended as a **structure-side pre-research experiment**:

- start with paper reading plus input-contract mapping;
- then build a minimal runnable prototype;
- then decide whether it fits better as:
  - an L1 structure side branch,
  - an L2 review side branch,
  - an independent fallback structural model.

---

### 9. Frozen Conclusion at This Stage

As of this document version, the frozen conclusions are:

- **retain**: Agentic KD, SpecularNet
- **not retained as a current priority item**: GWO-RF
- it is **not allowed** to rewrite watchlist paper results as established Warden facts;
- it is **not allowed** to use watchlist technologies to directly replace the current V1 mainline;
- it is **allowed** to open small-scale validation experiments and dedicated evaluations around these two directions later.

---

### 10. One-Sentence Summary

At the current stage, Warden should treat **Agentic KD** as a candidate upgrade for training-side teacher labeling, and **SpecularNet** as a priority candidate for future structural review / structural branching; both are worth retaining, but neither is yet qualified to rewrite the current V1 mainline.
