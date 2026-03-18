# Warden Gate / Evasion Auxiliary Set V1

版本：v1.0  
状态：Draft  
放置位置：`docs/data/GATE_EVASION_AUXILIARY_SET_V1.md`

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