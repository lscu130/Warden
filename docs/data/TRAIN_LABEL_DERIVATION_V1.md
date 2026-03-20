# Warden 恶性样本标签结构草案（V1）

## 1. 文档目的

本文用于冻结 Warden 项目中恶性网页样本的标签分层思路。  
目标不是简单给网页贴一个“钓鱼/非钓鱼”标签，而是建立一个更适合 **网页社会工程威胁判断** 的标签体系，使后续数据采集、人工标注、训练集构建、模型训练、误差分析和论文写作都能使用同一套口径。

本版本强调：

1. **一级主标签按“最终高风险动作/恶意目标”划分**
2. **二级标签按“行业/场景外壳”划分**
3. **辅助标签按“社工叙事、页面行为、对抗/规避特征”划分**

---

## 2. 设计原则

### 2.1 不采用混合维度并列分类

以下几类概念不能作为同一级主标签并列使用：

- 社工页面
- 加密货币
- 黑灰产
- 常规钓鱼

原因是它们来自不同维度：

- “社工页面”是**手法/叙事**
- “加密货币”是**行业/场景**
- “黑灰产”是**内容生态/违法属性**
- “常规钓鱼”是**传统安全类别**

如果把这些直接并列，会导致：

- 标签边界混乱
- 同一样本可能同时属于多个类
- 模型训练目标不清晰
- 论文问题定义发散
- 后续统计分析很难解释

### 2.2 一级主标签应围绕“用户将被诱导做什么”

Warden 的核心不是判断网页“长得像不像某品牌”，而是判断网页是否在诱导用户执行高风险动作。  
因此一级主标签应按 **恶意目标 / 最终危害动作** 划分。

### 2.3 行业、叙事、规避方式应下沉为副标签

行业场景（如 crypto、物流、金融）、社工叙事（如客服、促销、赠品）、规避方式（如 gate、blank、click-through）都很重要，但不应取代主标签，而应作为副标签保留。

---

## 3. 一级主标签（Primary Threat Label）

一级主标签用于定义样本的主要恶意目标，是训练和论文主任务的核心标签。

### 3.1 credential_theft

**定义**：诱导用户输入账号、密码、短信验证码、邮箱验证码、恢复码、2FA 令牌等认证信息。  
**典型页面**：

- 登录页
- 邮箱验证页
- 账号恢复页
- 安全校验页
- 风控验证页

### 3.2 payment_fraud

**定义**：诱导用户输入银行卡、信用卡、CVV、账单信息，或直接付款。  
**典型页面**：

- 补缴运费
- 账单异常补款
- 订阅续费
- 欠费缴费
- 罚款/税费缴纳

### 3.3 wallet_drain_or_web3_approval_fraud

**定义**：诱导用户连接钱包、签名、授权、approve 或发起链上交易，从而导致资产被转移。  
**典型页面**：

- 空投 claim
- NFT/DeFi mint
- 钱包升级/安全验证
- 领取奖励/赠币
- 交易所安全校验

### 3.4 pii_kyc_harvesting

**定义**：诱导用户提交个人身份信息或实名/KYC 材料。  
**典型页面**：

- KYC 验证
- 实名补录
- 中奖领奖实名
- 招聘入职信息
- 身份信息补全

### 3.5 fake_support_or_contact_diversion

**定义**：诱导用户联系假客服、拨打电话、加入 Telegram/WhatsApp、下载远控工具或转入站外私聊。  
**典型页面**：

- 技术支持弹窗
- 账户冻结联系客服
- 交易异常联系专员
- 物流/电商假客服
- 假官方服务入口

### 3.6 malware_or_fake_download

**定义**：诱导用户下载恶意软件、假更新、恶意浏览器扩展、假 App、带毒文档或其他可执行内容。  
**典型页面**：

- 浏览器更新
- Flash/播放器更新
- 验证插件安装
- 办公文档下载
- 钱包/聊天工具假客户端下载

### 3.7 benign

**定义**：正常网页，不具有明确的社会工程威胁主目标。

### 3.8 uncertain

**定义**：样本信息不足、证据冲突、页面损坏或当前无法稳定判定。

---

## 4. 二级场景标签（Scenario / Vertical Label）

二级标签用于表示样本所在的行业或叙事外壳，不作为主任务标签，但用于分析和分层统计。

建议固定如下枚举：

- finance_banking
- ecommerce_retail
- payment_platform
- logistics_delivery
- enterprise_mail_cloud
- social_media
- government_public_service
- crypto_web3
- gaming
- telecom_utility
- tech_support
- job_recruitment
- other

说明：

- “加密货币”应主要放在这里，而不是一级主标签
- 同一 crypto_web3 场景下，主标签可能是 wallet drain、fake support、download fraud、PII harvesting 中任意一种
- 同一 customer service 页面，可能最终对应 payment_fraud，也可能对应 credential_theft 或 contact_diversion

---

## 5. 辅助属性标签（Narrative / Tactic / Evidence Labels）

辅助标签不直接替代主类，而是用于描述样本的社工叙事、显式证据和规避行为，便于模型设计和误差分析。

### 5.1 社工叙事类

- brand_impersonation
- customer_service_narrative
- promo_discount_narrative
- giveaway_airdrop_narrative
- urgency_or_loss_framing
- authority_impersonation

### 5.2 页面证据类

- credential_form_present
- payment_form_present
- wallet_connect_present
- download_prompt_present
- contact_redirect_present
- qr_present

### 5.3 对抗/规避/动态行为类

- gate_or_verification_present
- requires_interaction_to_reveal
- blank_or_sparse_initial_page
- redirect_chain_present

### 5.4 生态/内容属性类

- illicit_service_content

说明：

- `illicit_service_content` 仅表示页面含有灰黑产内容，不等于其自动成为主恶性类
- 黑灰产属性不应直接吞并 Warden 主任务
- 只有当黑灰产页面明确诱导高风险动作时，才应映射到一级主标签中的某个类

---

## 6. “黑灰产”在 Warden 中的处理方式

### 6.1 不建议把“黑灰产”作为一级主标签

原因：

1. 范围过宽
2. 很多黑灰产页违法，但不一定是社会工程威胁页
3. 会让任务从“网页社会工程威胁判断”滑向“违法网页识别”
4. 会破坏论文主问题边界

### 6.2 推荐处理方式

将“黑灰产”视为：

- **辅助属性标签**
- 或 **后续扩展评估集合**

而不是 V1 主训练标签中心。

只有满足以下条件时，黑灰产页才应纳入主恶性样本：

- 明确诱导用户提交凭证
- 明确诱导付款/转账
- 明确诱导连接钱包/签名
- 明确诱导下载恶意内容
- 明确诱导联系站外假客服或远控

---

## 7. “促销 / 客服 / 赠品 / 验证”为什么不作为一级主类

这些概念更适合作为 **叙事模板**，而不是主威胁类别。

例如：

- “客服页”可能最终是 `credential_theft`
- “客服页”也可能最终是 `payment_fraud`
- “促销页”可能最终是 `wallet_drain_or_web3_approval_fraud`
- “验证页”可能最终是 `malware_or_fake_download`

如果把这些叙事模板直接当主类，会导致：

- 同名页面背后危害类型混杂
- 训练目标不稳定
- 统计结果难以解释
- 模型学到的是表面话术，而不是风险行为

---

## 8. V1 推荐冻结版本

当前建议的 V1 一级主类如下：

- credential_theft
- payment_fraud
- wallet_drain_or_web3_approval_fraud
- pii_kyc_harvesting
- fake_support_or_contact_diversion
- malware_or_fake_download
- benign
- uncertain

当前建议的 V1 设计原则如下：

1. 主类按最终危害动作划分
2. 场景按行业/外壳划分
3. 叙事和规避行为按辅助属性保存
4. gate/evasion 不作为一级恶性类
5. “加密货币”不作为一级恶性类
6. “黑灰产”不作为一级恶性类
7. “客服/促销/赠品/验证”不作为一级恶性类

---

## 9. 对 Warden 后续模块设计的意义

这种标签结构更适合 Warden 的分层系统：

### 对 L0

L0 可先做低成本初筛：

- 是否出现登录/支付/钱包/下载/客服等高风险锚点
- 是否出现品牌仿冒、紧迫性用语、二维码、联系方式外跳等信号

### 对 L1

L1 可做更强的语义/结构判断：

- 页面主要目标是什么
- 诱导动作属于哪种一级主威胁类
- 哪些叙事和证据支持该判断

### 对 L2

L2 可处理复杂和困难样本：

- gate/evasion
- click-through
- delayed reveal
- blank page
- 多步交互后暴露恶意行为
- 证据冲突样本

---

## 10. 结论

Warden 的恶性样本标签不应采用“社工页面 / 加密货币 / 黑灰产 / 常规钓鱼”这类混合维度并列分类。  
更合理的做法是：

- **一级主标签按恶意目标划分**
- **二级场景标签按行业外壳划分**
- **辅助属性标签按叙事、证据和规避行为划分**

这样更适合：

- 数据集标注
- 多模态模型训练
- 分层推理
- 错误分析
- 鲁棒性评估
- 顶会论文写作

---

## 11. `threat_taxonomy_v1` 落地与使用边界

基于当前项目决议，本文定义的多威胁标签结构不应停留在实验草案层。
它应长期保留为 `rule_labels.json` 下的活跃弱标签输出命名空间：

- `rule_labels.json -> threat_taxonomy_v1`

当前口径如下：

- `threat_taxonomy_v1` 是 Warden 多威胁主问题定义的规则派生候选标签层
- 它应继续通过统一离线 backfill 提高覆盖率，而不是只覆盖新样本
- 它应优先服务于弱监督分析、样本分层、冲突发现、人工审核排队和后续标签治理
- 对高价值、高冲突、高不确定子集，应继续通过人工审核补全

同时必须保持以下边界：

- 它不是人工金标，不得直接等同于 `TrainSet V1 primary` 默认主标签
- 它不应默认写入 primary manifest 核心字段
- 它可以长期存在于 `rule_labels.json`，但仍需保持 candidate 语义和弱标签安全语义
