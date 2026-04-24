# L0_DESIGN_V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于冻结 Warden 在当前阶段的 **L0 设计规范**。
- 本文档默认服务于推理模块与运行期路由，不负责训练期目标定义，也不重写冻结数据结构。
- 若涉及精确字段名、路由语义、阶段职责、阈值口径或兼容性约束，以英文版为准。
- 本文档当前版本明确采用 **脚本优先、规则优先、证据优先** 的实现立场，不将机器学习模型作为 L0 的默认前提。
- 当前 auto-label 参考实现的活动 L0 逻辑位于 `src/warden/module/l0.py`，`scripts/labeling/Warden_auto_label_utils_brandlex.py` 保留兼容入口与顶层编排职责。

# Warden L0 设计规范 V1

## 1. 文档目的

本文件用于冻结 Warden 当前阶段的 L0 设计边界、职责范围、输入输出口径、路由语义与实现原则。

本文件重点回答以下问题：

1. L0 在 Warden 中到底负责什么；
2. L0 不负责什么；
3. L0 应读取哪些低成本证据；
4. L0 如何做弱风险归纳与阶段路由；
5. `early_stop_low_risk` 应如何解释，哪些情况下不允许早停；
6. L0 与 L1 / L2，尤其是 gate / evasion 辅助协议，应如何衔接；
7. 当前阶段 L0 应以什么实现形态落地。

本文件不是：

- 训练文档；
- 模型设计文档；
- 数据 schema 重定义文档；
- 最终标签本体文档；
- benchmark 结果文档。

## 2. 设计定位

L0 是 Warden 的 **最低成本、最快路径、高召回筛查层**。

其核心定位是：

> 在受限运行时成本下，基于低成本网页证据，完成初步观察、弱风险归纳与显式阶段路由。

L0 的目标不是做最终裁决，而是：

- 尽快发现明显需要升级的样本；
- 在极少数、证据充分且低观察风险的情况下允许停止升级；
- 将主判断压力保留给 L1；
- 将 gate / evasion / hard case 等高不确定性样本交给更强阶段处理。

## 3. L0 的责任范围

L0 默认负责以下内容：

1. 运行时低成本输入准备；
2. 基础可用性与缺失信号检查；
3. URL、可见文本/标题、表单、轻量网络摘要，以及已存在的低成本 diff/evasion 摘要特征提取；
4. 基于规则与脚本的 observation-first 弱信号归纳；
5. 低成本弱风险分数与原因汇总；
6. 输出显式路由结果：
   - `early_stop_low_risk`
   - `escalate_to_L1`
   - `direct_to_L2`
7. 输出可审计的 route reasons、risk reasons 与 degraded-mode 说明。

## 4. L0 不负责的内容

L0 默认不负责以下内容：

- 最终恶意裁决；
- 最终 benign / safe 认定；
- 最终 page role；
- 最终 threat taxonomy；
- 最终 high-risk action class；
- 训练期目标映射；
- 重交互恢复；
- 复杂 gate / challenge 穿透；
- 全量点击流程恢复；
- 高成本多模态主判断；
- 将 challenge 页硬判为最终主体页；
- 使用机器学习模型作为默认前置条件。

## 5. 设计原则

### 5.1 脚本优先

L0 当前版本采用脚本与规则优先的实现策略。

默认形态应为：

- Python 脚本逻辑；
- 可审计规则；
- 显式触发器；
- 可回放的 route reasons；
- 可配置阈值与策略项。

### 5.2 证据优先

L0 应首先表达“当前页面状态下观察到了什么”，再表达“这些观察意味着哪些弱候选或弱风险”。

### 5.3 路由优先于裁决

L0 的主产品是路由结果，不是最终标签。

### 5.4 高召回优先于激进早停

若样本当前证据不足、信号冲突、存在 gate / evasion 痕迹或敏感意图迹象，优先升级而不是在 L0 直接停止。

### 5.5 显式降级

若输入工件缺失、解析失败或证据不充分，必须进入显式 degraded mode，而不是静默当作低风险。

## 6. 输入范围

### 6.1 默认允许的低成本输入

L0 在当前阶段默认允许读取以下低成本输入或等价运行时信息：

- URL 输入；
- host / path / query 等 URL 结构信息；
- 页面基础元信息；
- 可见文本；
- 表单摘要；
- 轻量网络摘要；
- 已经由上游生成的低成本 diff/evasion 摘要；
- 预先生成的低成本结构化特征；
- 下游兼容的弱标签输入（若部署路径明确允许）。

兼容说明：`html_features` 与 `brand_signals` 可以作为兼容字段保留默认安全结构，但当前 L0 默认热路径不主动计算完整 HTML 特征，也不做默认 brand 提取。

### 6.2 可对应的上游工件

若走离线或准离线路径，L0 可与以下工件对齐：

- `meta.json`
- `url.json`
- `forms.json`
- `visible_text.txt`
- `html_rendered.html`
- `net_summary.json`
- `auto_labels.json`

### 6.3 不作为 L0 默认前提的内容

以下内容不应成为 L0 的默认前置条件：

- 重视觉 backbone；
- OCR；
- LLM 推理；
- 全流程交互点击；
- `network.har`；
- `actions.jsonl`；
- `after_action/`；
- `variants/`；
- 生成 `variants/` 或产出 `diff_summary.json`；
- 需要额外重型依赖的处理链路。

这些内容可属于 L2、分析工具或后续增强路径，但不属于当前 L0 默认路径。若 `diff_summary.json` 已经存在，L0 可以把它作为低成本 evasion 路由摘要读取；生成 variants 或 diff_summary 不是 L0 职责。

## 7. L0 内部处理结构

L0 V1 默认按以下处理顺序组织：

1. 输入可用性检查；
2. 低成本观察型特征提取；
3. 弱信号归纳；
4. 弱风险汇总；
5. 显式路由；
6. 输出结构化原因与降级说明。

### 7.1 输入可用性检查

这一阶段应明确：

- 哪些关键输入存在；
- 哪些关键输入缺失；
- 当前页面是否为明显中间态、空白态或异常态；
- 当前样本是否处于 degraded mode。

该阶段不做最终风险裁决。

### 7.2 观察型特征提取

L0 可提取的默认低成本观察型特征包括但不限于：

#### URL 特征

- host 是否为 IP；
- 域名层级是否异常；
- path/query 是否包含 login / verify / update / unlock / connect 等高风险 token；
- host / path / query 中是否存在 gambling、adult、gate 等高显著专项垂类 token；
- 是否存在明显伪装、异常编码或可疑子域形式。

#### 表单特征

- 是否存在密码、OTP、支付卡、CVV、钱包连接、助记词、个人信息等字段证据；
- 是否存在 submit / continue / connect / verify 等敏感提交动作；
- 表单数量与字段结构是否异常；
- 表单目标是否呈现跨域或高可疑形式。

#### HTML / JS 轻特征

- 是否存在 meta refresh 或脚本跳转；
- 是否存在下载导向线索；
- 是否存在 CAPTCHA / challenge / anti-bot 线索；
- 是否存在强交互或主体未暴露的结构特征；
- 是否存在文本极少但脚本或交互异常偏重的情况。

#### 文本特征

- 是否存在凭证索取词；
- 是否存在 OTP / 验证码索取词；
- 是否存在支付信息索取词；
- 是否存在钱包授权 / 助记词相关词；
- 是否存在下载 / 安装 / 执行诱导词；
- 是否存在 verify human / challenge / cloudflare / captcha 等门页语义；
- 是否存在紧迫、风控、中奖、恢复、冻结解除等社会工程叙事词。

#### 轻量网络摘要特征

- 是否存在可疑外部 POST 目标；
- 是否存在异常跳转或重定向；
- 是否存在第三方域异常集中；
- 是否存在下载目标或异常资源请求线索。

### 7.3 弱信号归纳

L0 在 observation-first 特征之上，可归纳以下弱信号族，但这些信号仍然只是弱语义，不是最终标签。

#### intent_signals

例如：

- `credential_intent_candidate`
- `otp_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `seed_phrase_intent_candidate`
- `personal_info_intent_candidate`
- `download_intent_candidate`

#### brand_signals

例如：

- claimed brand token
- URL / text / form 中的品牌不一致
- 弱品牌仿冒支持信号

当前默认热路径中，L0 应将 `brand_signals` 视为兼容字段或显式预计算输入，不应执行默认 brand extraction，也不应把 brand matching 作为专项筛查合同的基础。

#### evasion_signals

例如：

- `captcha_present_candidate`
- `challenge_present_candidate`
- `dynamic_redirect_candidate`
- `anti_bot_or_cloaking_candidate`
- `needs_interaction_candidate`
- `content_unrevealed_candidate`

#### quality_signals

例如：

- 关键输入缺失；
- 页面文本极少；
- 主体未暴露；
- 当前证据与输入 URL 威胁上下文不一致；
- 当前样本无法稳定解释为正常低风险页面。

### 7.3A Specialized Detector Families（高显著垂类专项探测器）

在保留通用 observation-first 特征与通用弱信号族的前提下，L0 可额外支持少量 **specialized detector families**，用于处理在低成本证据下即可高显著暴露的垂类页面或页面表面。

当前优先支持的专项族包括但不限于：

- gambling / betting / casino lure
- adult / porn lure / age-gate-like adult surface
- gate / challenge / CAPTCHA surface

这些 specialized detectors 的目标不是替代通用 L0 路由，而是：

1. 更快识别明显不应被 `early_stop_low_risk` 放行的样本；
2. 更早输出高价值垂类弱信号，供后续 L1 / L2 使用；
3. 在极少数 **高显著、低歧义、低冲突** 的样本上，为后续快速处理提供 specialized fast-path 候选；
4. 降低 L1-text 对极其显著页面表面的无意义计算。

这些专项探测器默认仍然只能输出 **weak signals / candidates / routing hints**，而不是直接重写 Warden 的最终 threat taxonomy 或人工最终裁决。

### 7.3B Specialized Weak Signals

专项探测器可输出例如：

- `possible_gambling_lure`
- `possible_bonus_or_betting_induction`
- `gambling_weighted_score`
- `gambling_weighted_score_reasons`
- `possible_adult_lure`
- `possible_age_gate_surface`
- `possible_gate_or_evasion`
- `possible_challenge_surface`
- `specialized_fast_resolution_candidate`

其中：

- `specialized_fast_resolution_candidate` 仅表示该样本在当前低成本证据下呈现出高度显著、低歧义、低冲突的专项表面；
- `gambling_weighted_score` 与 `gambling_weighted_score_reasons` 属于 explainability / recovery-support 输出，用于表达为什么某个博彩页接近或达到专项触发阈值；
- 它们服务于审计、窄 recovery 与后续调参，不单独等价于最终 threat label；
- 它不是最终标签，不等价于最终良性，也不等价于最终恶意；
- 若后续实现希望允许真正的 L0 直接解决路径，必须通过显式任务与文档更新冻结新的路由策略，不能静默扩展当前契约。

### 7.3C Gambling Detector Guidance

对于博彩类页面，L0 当前应优先依赖低成本结构证据与文本证据的组合，并保持“结构证据优先于弱诱导词”的实现立场。当前优先级大致为：

- host / URL 结构证据：`bet`、`casino`、`slot`、`poker`、`lotto`、`sportsbook` 及其 host token 变体，尤其是 `bet+数字` 一类强结构模式；
- 可见文本中的强博彩词：如 `sportsbook`、`live dealer`、`cashier`、`bet365` 以及高显著中文博彩词；
- 交易面 / 落地页支持信号：敏感表单、注册 / 登录 / play-now / download-app / official-entry 一类 CTA，与博彩上下文组合出现；
- bonus / inducement 词：`welcome bonus`、`free spins`、`promo code`、`deposit bonus`、彩金 / 首存优惠 / 返水 等；
- editorial / guide / review / news 语义：用于抑制讨论页、导购页与资讯页被误抬升为博彩落地页。

当前 baseline 中，`possible_gambling_lure` 默认应由以下路径之一触发：

- 高置信博彩词直接命中；
- 强博彩文本命中达到足够密度；
- 强博彩文本与交易面信号共现；
- 博彩文本达到较高密度，且同时存在交易面支撑；
- bonus / inducement 词与博彩文本、交易面共同出现；
- URL / host 结构证据与博彩文本或 bonus 词形成低冲突组合。

当前 `gambling_weighted_score` 应被视为 explainable support score，而非独立分类器。它的作用是：

- 量化 URL / host、强文本、交易面、bonus 与 editorial suppression 的相对贡献；
- 为窄 recovery 提供可审计支撑；
- 帮助区分“真实博彩落地页”与“博彩讨论 / 导购 / review 内容页”。

当前实现应保持以下约束：

- host / URL 结构证据的权重高于单独的弱 bonus 词；
- `bonus`、`promotion`、`cashback`、`deposit`、`withdrawal` 一类弱诱导词不得单独构成 `possible_gambling_lure`；
- 当页面明显呈现 editorial / guide / review / news 语义，且缺少高置信博彩证据时，应触发 suppression，避免将资讯或 affiliate 页面抬成博彩落地页；
- `possible_bonus_or_betting_induction` 仅用于表达博彩诱导表面，默认需要 bonus 词与博彩上下文、域名结构线索或强文本 / CTA 支撑共同出现。

对路由层的默认影响应至少包括：

- 命中 `possible_gambling_lure` 时，禁止 `early_stop_low_risk`；
- 命中 `possible_gambling_lure` 时，默认输出面向 L1 的 text-semantic 路由提示；
- 若博彩页同时伴随卡支付、跨域敏感表单、第三方 POST 或等价高风险交付信号，应强化 `need_l2_candidate` 或等价升级提示。

在后续单独批准的快速处理策略下，极少数高度显著的博彩页面可被标记为 `specialized_fast_resolution_candidate`，但该逻辑不应在当前 baseline 中静默开启。

### 7.3D Adult Detector Guidance

对于成人类页面，L0 当前应优先依赖 URL、可见文本与 age-gate 语义的组合，并保持“adult surface 先路由、后细判”的实现立场。当前优先级大致为：

- URL / host 片段：`porn`、`porno`、`xxx`、`jav`、`91porn` 及其他高显著成人域名或路径 token；
- 可见文本中的成人词：成人视频、裸露描述、性交相关词、`theporndude`、`pornhub`、`bdsm`、`milf` 等；对少量重复出现且本地化成人语义明确的词，也可做极窄补充，例如 `colmek`；
- age-gate 语义：`18+`、`adults only`、`you must be 18`、`verify your age`、未成年人禁止进入等；
- adult-lure 或 access 语义：`watch now`、`unlock`、`premium access`、`verify age`、`create account` 等。

当前 baseline 中，`possible_adult_lure` 默认应由以下路径之一触发：

- adult URL / host 证据直接命中；
- 高置信成人词直接命中；
- 至少 `3` 个强成人文本词共同出现；
- 至少 `2` 个强成人文本词共同出现，且 URL / host 同时带有成人域名提示；
- 强成人文本与强 age-gate 语义共同出现。
- 在窄恢复白名单内，仅当页面恰好命中 `1` 个强成人文本词，且 URL / host 同时带有显著成人域名提示时，也可触发；当前仅允许极少数高显著 token，例如 `jav`、`porno`、`avxxx`。

当前 `possible_age_gate_surface` 的角色应单独明确：

- 它用于表达“当前页面呈现出明显的成人年龄门槛表面”；
- 它默认要求 age-gate 词与成人文本或成人 URL 线索共同出现；
- 它可以和 `possible_adult_lure` 同时出现，也可以作为更窄的 adult surface 补充信号出现。

当前实现还应明确区分 URL-only adult surface：

- 若 adult 信号主要来自 URL / host，而文本侧支撑不足，L0 应优先将其视为需要视觉或后续更强语义判读的成人表面；
- 这类样本不应在 L0 被当作“证据已充分的低风险页面”处理；
- 该场景默认应强化 `need_vision_candidate` 或等价视觉升级提示。

对路由层的默认影响应至少包括：

- 命中 `possible_adult_lure` 或明显的 adult surface 时，禁止 `early_stop_low_risk`；
- 命中 `possible_adult_lure` 时，默认输出面向 L1 的 text-semantic 路由提示；
- 若成人表面同时伴随下载诱导、异常跳转、第三方提交或等价高风险交付信号，应强化 `need_l2_candidate` 或等价升级提示。

当前实现还应保持一个误判控制约束：

- 当页面仅有成人叙事词，而缺少敏感表单、OTP、支付或真实交付证据时，L0 不应轻易把 generic credential / OTP / PII 词误解释为更高层的诈骗主标签。
- 弱内容分级词或弱成人缩写，例如 `nsfw`、`not safe for work`、泛化的 `age verification`、以及歧义较高的 `av`，不应单独构成 `possible_adult_lure`；
- 弱成人描述词，例如 `erotic`、`nude`、`nudity`、`anal`，默认应要求更强的成人上下文或更强的 age-gate 支撑，才进入 adult surface 判定。
- 在 generic host 上，仅凭 `1` 个强成人词配合弱词，或仅凭 `2` 个无 host 支撑的强成人词，不应默认进入 `possible_adult_lure`；这类页面应优先保留给后续更强语义层处理。
- 单强词恢复路径必须保持极窄：它只适用于带显著成人域名提示的页面，且 token 必须落在显式 allowlist 中；歧义 token 或 generic host 不得走这条路径。
- 本地化词缺口特化也必须保持极窄：只应补充在 mixed low-support miss 中重复出现、且在 benign 池反弹可控的词；当前保守补充包括 `colmek` 文本词与 `bokep` host/domain hint。

### 7.3E Gate / Challenge / CAPTCHA Detector Guidance

对于 gate / challenge / CAPTCHA 页面，L0 可优先依赖显著的验证语义、challenge 提示、主体未暴露特征与典型网关提供方线索进行探测。例如：

- text token：`verify you are human`、`captcha`、`cloudflare`、`challenge`、`security check`、`checking your browser`、`press and hold`、`request unsuccessful` 等；
- 结构特征：主体文本稀疏、单一强 CTA、主内容未展开、页面首先呈现验证或拦截提示；
- 运行期支持信号：captcha 命中、anti-bot / cloaking 提示、variant failed、dynamic redirect 等。

对于这类页面：

- 默认不得 `early_stop_low_risk`；
- 应输出 `possible_gate_or_evasion` 或 `possible_challenge_surface`；
- 若存在明显 challenge / anti-bot / cloaking / dynamic redirect / 主体未暴露等高不确定性迹象，应强化 `need_l2_candidate` 或等价升级提示；
- 对“普通 gate 页是否允许在 L0 直接解决”的更激进策略，必须通过显式任务和契约更新单独冻结，当前 baseline 不默认启用。

### 7.4 弱风险汇总

L0 可输出低成本弱风险汇总，例如：

- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`

但必须明确：

- 这是当前低成本证据下的弱风险输出；
- 不是最终恶意结论；
- 不是最终安全结论；
- 不能替代 L1/L2 或人工最终裁决。

## 8. 路由语义

L0 的默认路由结果应限制为以下三类：

- `early_stop_low_risk`
- `escalate_to_L1`
- `direct_to_L2`

### 8.1 `early_stop_low_risk` 的正式语义

`early_stop_low_risk` 是 **路由结果**，不是 **真值结果**。

它只表示：

> 在当前 L0 低成本证据与当前策略阈值下，样本未触发继续升级条件，因此在 L0 停止升级。

它不表示：

- 页面真实安全；
- 页面最终 benign；
- 页面不具有任何恶意可能；
- 页面不需要在未来策略下被重新升级。

### 8.2 `escalate_to_L1` 的语义

表示样本需要进入主判断层，以获得更强的语义 / 结构判断。

### 8.3 `direct_to_L2` 的语义

表示样本当前已表现出明显的 gate / evasion / hard-case / high-uncertainty 特征，应直接进入更高成本复核层，而不是在 L0 或普通 L1 路径中继续停留。

## 9. 早停条件与禁止早停条件

### 9.1 允许 `early_stop_low_risk` 的必要条件

L0 只有在以下条件同时满足时，才允许 `early_stop_low_risk`：

1. 当前低成本弱风险较低；
2. 关键输入充分，当前样本不是显式 degraded mode；
3. 不存在 credential / OTP / payment / wallet / seed phrase / download 等敏感意图弱信号；
4. 不存在显式预计算或兼容输入提供的明显品牌仿冒支持信号；
5. 不存在 gate / captcha / challenge / cloudflare / verify-human 语义；
6. 不存在 cloaking / dynamic redirect / needs interaction / content unrevealed 等规避信号；
7. 不存在关键证据冲突；
8. 当前页面可被稳定解释为普通低观察风险页面。

### 9.2 禁止 `early_stop_low_risk` 的触发族

只要命中以下任一族，L0 默认不得早停：

- 敏感意图信号；
- 显式预计算或兼容输入提供的品牌仿冒 / 品牌错配支持信号；
- gate / challenge / CAPTCHA / Cloudflare 语义；
- 动态跳转、anti-bot、cloaking、needs-interaction 信号；
- 输入缺失严重或解析失败；
- 文本 / URL / 表单 / 网络摘要之间存在明显冲突；
- 高风险输入 URL 与当前页面证据明显不匹配；
- 任何当前无法稳定判为正常低风险页的高不确定状态。

### 9.3 默认保守策略

当路由条件不充分时，默认不做激进早停，而是升级到 L1；
若存在明显 gate / evasion / hard-case 特征，则直接升级到 L2。

### 9.4 High-Salience Verticals 的快速处理约束

对于博彩、成人、gate 等 high-salience verticals，L0 可额外输出专项快速处理候选，但必须遵守以下约束：

1. 不能把专项词命中直接当作最终标签；
2. 不能把专项 detector 的低冲突命中自动解释为 `early_stop_low_risk`；
3. 专项 detector 的默认价值首先是：
   - 更稳地禁止不该早停的样本早停；
   - 更快地产生垂类弱信号；
   - 更早提供升级线索；
4. 若未来需要对某些极高显著页面表面启用 L0 直接解决路径，必须显式定义：
   - 适用页面族；
   - 允许的直接解决结果；
   - 与当前三类路由结果的关系；
   - 下游兼容性影响；
   - 验证与回退方案。

## 10. 与 Gate / Evasion Auxiliary Protocol 的关系

L0 对 gate / evasion 样本的职责是：

- 发现；
- 标记；
- 升级。

L0 不负责：

- 解决 gate；
- 完成挑战页穿透；
- 恢复完整点击流程；
- 将 challenge 页当作最终主体页硬判。

若命中明显 gate / evasion 语义，L0 可：

- 将样本升级到 L1，供主判断层识别样本家族；
- 在强 gate / strong evasion / high-uncertainty 条件下直接送 L2。

## 11. 与 L1 / L2 的边界

### 11.1 与 L1 的边界

L1 是主判断层。

L0 负责低成本筛查与路由，L1 负责更强的语义 / 结构判断。
L0 不应通过堆叠脚本复杂度偷偷变成 L1。

### 11.2 与 L2 的边界

L2 是高成本复核层。

L0 只负责发现需要 L2 的样本，不负责执行重交互、强复核或对抗恢复。

## 12. 输出要求

L0 的输出应保持结构化、可审计、可解释。

默认应能够表达以下信息：

- `stage`
- `route_target`
- `escalated`
- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`
- `route_reasons`
- `input_quality`
- `missing_signals`
- `degraded_mode`
- 适度的观察摘要与弱信号摘要

若某条部署路径不支持其中部分字段，也必须显式声明其降级行为。

## 13. 阈值与策略治理

L0 阈值属于策略项，不是隐藏魔法。

因此：

- 影响行为的阈值必须显式；
- 影响早停或升级的触发器必须显式；
- 阈值变化若会改变路由行为，必须被记录；
- 不允许将“模型分低”或“单一风险分低”直接等价为允许早停。

## 13A. Specialized Detector 的实现约束

当前阶段 Specialized Detector Families 的实现应满足：

- script-first
- evidence-first
- token family and pattern family based
- shared evidence object first, no repeated raw scanning
- detector family outputs weak signals first, routing second
- no hidden heavy dependency

建议实现路径：

- 共享 `evidence_preparer` 先统一产生 `url_signals`、`text_signals`、`form_signals`、`network_signals`、`quality_flags`；
- `gambling_detector`、`adult_detector`、`gate_detector` 在共享信号之上产出专项弱信号；
- `policies.py` 仅消费这些专项弱信号，进行 no-early-stop、upgrade、need_l2 等路由决策。

这类 detector 不应把原始文本、URL、表单和网络摘要在多个模块中重复扫描，也不应把复杂类别逻辑直接堆在 `policies.py` 中。

## 14. 当前实现立场

L0 V1 的默认实现立场为：

- script-first
- rule-first
- evidence-first
- routing-first
- explanation-first

当前版本不将以下内容设为 L0 默认组成部分：

- 机器学习分类器；
- URL-only 模型；
- URLNet 类模型；
- LLM；
- 高成本视觉模型；
- 重依赖推理链路。

若未来要对 L0 的 scoring 或 calibration 做增强，应在不破坏本文件冻结边界的前提下，以单独任务或版本更新显式推进。

## 15. 对训练与后续演进的约束

本文件冻结的是 L0 的当前职责与路由规范，不冻结未来所有阈值、权重或脚本细节。

后续在各层训练或评测阶段，可以：

- 调整阈值；
- 调整 risk reasons 组合；
- 调整 route trigger 的细粒度实现；
- 做小范围策略校准。

但默认不应：

- 改写 L0 的主职责；
- 把 L0 改成最终裁决层；
- 把 gate / evasion 重交互逻辑塞入 L0；
- 将 `early_stop_low_risk` 重新解释为真实安全结论。

## 16. 验证要求

凡涉及 L0 的非 trivial 改动，至少应验证：

1. 低成本输入准备可在 smoke sample 上运行；
2. L0 能正常输出结构化结果；
3. 路由结果与 route reasons 一致；
4. degraded mode 行为是显式的；
5. gate / evasion 明显样本不会被误当作普通低风险早停；
6. 输出结构与下游使用方契约一致。

若验证未运行，必须显式说明未运行项与原因。

## 17. Definition of Done

L0 设计规范 V1 可以视为冻结，当且仅当：

- L0 的职责明确；
- L0 的非职责明确；
- L0 的输入边界明确；
- L0 的路由语义明确；
- `early_stop_low_risk` 的正式含义明确；
- 禁止早停条件明确；
- 与 Gate / Evasion Auxiliary Protocol 的边界明确；
- 与 L1 / L2 的责任边界明确；
- 当前实现立场明确为脚本优先、规则优先；
- 本文件不与 `AGENTS.md`、`PROJECT.md`、`MODULE_INFER.md`、`TRAINSET_V1.md`、`GATA_EVASION_AUXILIARY_SET_V1.md` 和自动标签策略文档冲突。

### 原始中文说明

中文内容保留在前，供人工协作与快速导览。英文版为权威版本。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden L0 Design Specification V1

## 1. Purpose

This document freezes the current-stage L0 design boundary, responsibility scope, input/output expectations, routing semantics, and implementation stance for Warden.
For the current auto-label-backed reference path, the active L0 implementation lives in `src/warden/module/l0.py`, while `scripts/labeling/Warden_auto_label_utils_brandlex.py` remains the compatibility entrypoint and top-level orchestration layer.

For the current narrowed default hot path in that reference implementation:

- full `HTML` feature extraction is skipped by default;
- default `brand` extraction is skipped by default;
- `html_features` and `brand_signals` remain present as compatibility-safe default structures;
- ordinary non-specialized pages should normally continue toward `L1`, while `L0` stays focused on cheap `gambling / adult / gate` specialized screening and routing hints.

It answers the following questions:

1. what L0 is responsible for inside Warden;
2. what L0 is not responsible for;
3. which cheap evidence families L0 is allowed to consume;
4. how L0 should perform weak-risk aggregation and staged routing;
5. how `early_stop_low_risk` should be interpreted and when early stop is forbidden;
6. how L0 should connect to L1 / L2 and especially to the gate / evasion auxiliary protocol;
7. what implementation stance L0 should use at the current stage.

This file is not:

- a training document;
- a model-architecture document;
- a frozen-dataset schema redesign;
- a final-label ontology document;
- a benchmark-results document.

## 2. Positioning

L0 is Warden's **lowest-cost, fastest-path, high-recall screening stage**.

Its core role is:

> under bounded runtime cost, use cheap webpage evidence to perform initial observation, weak-risk aggregation, and explicit stage routing.

L0 is not the final adjudication stage. Its job is to:

- discover samples that clearly need escalation as early as possible;
- allow stop-without-escalation only for a small subset of sufficiently observed low-observed-risk samples;
- preserve the main judgment burden for L1;
- hand gate / evasion / hard-case and high-uncertainty samples to stronger stages.

## 3. L0 Responsibilities

By default, L0 owns the following responsibilities:

1. low-cost runtime input preparation;
2. basic input-availability and missing-signal checks;
3. cheap feature extraction from URL, visible text/title, forms, lightweight network summaries, and existing cheap diff/evasion summaries when already present;
4. observation-first weak-signal aggregation using scripts and rules;
5. low-cost weak-risk scoring and reason aggregation;
6. explicit routing output:
   - `early_stop_low_risk`
   - `escalate_to_L1`
   - `direct_to_L2`
7. auditable route reasons, risk reasons, and degraded-mode reporting.

## 4. What L0 Does Not Own

By default, L0 does not own the following:

- final malicious adjudication;
- final benign / safe adjudication;
- final page role;
- final threat taxonomy;
- final high-risk action class;
- training-target mapping;
- heavy interaction recovery;
- complex gate or challenge bypass;
- full click-through recovery;
- full HTML feature extraction as a default hot-path dependency;
- default brand extraction as a default hot-path dependency;
- screenshot/OCR or image-lite evidence as a default prerequisite;
- high-cost multimodal main judgment;
- hard-labeling a challenge page as if it were already the final landing page;
- using machine-learning models as a default prerequisite.

## 5. Design Principles

### 5.1 Script-first

L0 V1 uses a script-first and rule-first implementation stance.

The default implementation form should be:

- Python scripting logic;
- auditable rules;
- explicit trigger families;
- replayable route reasons;
- configurable thresholds and policy items.

### 5.2 Evidence-first

L0 should first express **what was observed from the current page state**, and only then express **what weak candidates or weak risks those observations support**.

### 5.3 Routing before adjudication

The primary product of L0 is a routing result, not a final label.

### 5.4 High recall before aggressive early stop

If the current sample is insufficiently observed, internally conflicting, gate/evasion-like, or indicative of sensitive intent, escalation should be preferred over stopping at L0.

### 5.5 Explicit degraded mode

If required evidence is missing, parsing fails, or observations are insufficient, the runtime path must enter explicit degraded mode rather than silently treating the sample as low risk.

## 6. Input Scope

### 6.1 Default allowed cheap inputs

At the current stage, L0 may consume the following cheap runtime inputs or equivalent precomputed runtime information:

- URL input;
- URL structure such as host / path / query;
- basic page metadata;
- page title and visible text;
- raw visible-text observability status;
- form summaries;
- lightweight network summaries;
- existing cheap diff/evasion summaries when already produced by upstream capture or analysis;
- precomputed cheap structured features;
- compatible weak-label inputs where the deployment path explicitly allows them.

Compatibility note: `html_features` and `brand_signals` may remain present in L0-compatible outputs with default-safe structures, but the current default L0 hot path does not eagerly compute full HTML features or perform default brand extraction.

### 6.2 Corresponding upstream artifacts

For offline or quasi-offline paths, L0 may align with artifacts such as:

- `meta.json`
- `url.json`
- `forms.json`
- `visible_text.txt`
- `net_summary.json`
- `diff_summary.json` when it already exists
- `auto_labels.json`

### 6.3 What must not be a default L0 prerequisite

The following must not become default prerequisites for L0:

- heavy visual backbones;
- OCR;
- LLM inference;
- full-flow interactive clicking;
- `network.har`;
- `actions.jsonl`;
- `after_action/`;
- `variants/`;
- generating `variants/` or producing `diff_summary.json`;
- any runtime path that requires heavyweight extra dependencies.

These may belong to L2, analysis utilities, or later enhancement paths, but not to the current default L0 path. Consuming an already available compact `diff_summary.json` for cheap evasion routing is allowed; creating heavy variants is not an L0 responsibility.

## 7. Internal Processing Structure

L0 V1 should be organized in the following order:

1. input availability check;
2. cheap observation-oriented feature extraction;
3. weak-signal aggregation;
4. weak-risk aggregation;
5. explicit routing;
6. structured reason output and degraded-mode reporting.

### 7.1 Input availability check

This stage should explicitly determine:

- which key inputs are present;
- which key inputs are missing;
- whether the current page is an obvious intermediate, blank, or abnormal state;
- whether the current sample is in degraded mode.

This stage does not perform final risk adjudication.

### 7.2 Observation-oriented feature extraction

By default, L0 may extract cheap observation-oriented features including but not limited to the following.

#### URL features

- whether the host is an IP;
- whether the domain depth is abnormal;
- whether the path/query contains high-risk tokens such as `login`, `verify`, `update`, `unlock`, or `connect`;
- whether host / path / query contain high-salience specialized vertical tokens for gambling, adult, or gate-like surfaces;
- whether the URL shows suspicious disguise patterns, odd encodings, or suspicious subdomain structure.

#### Form features

- evidence of password, OTP, payment-card, CVV, wallet-connect, seed-phrase, or personal-information fields;
- sensitive submit actions such as `submit`, `continue`, `connect`, or `verify`;
- abnormal form counts or abnormal field structure;
- suspicious or cross-domain form targets.

#### Compatibility and cheap precomputed feature fields

- default-safe `html_features` structures may be passed through for compatibility;
- compact upstream summaries may expose download, CAPTCHA, challenge, or anti-bot cues;
- existing `diff_summary` or network summaries may expose unrevealed-content, redirect, or variant-failure hints;
- the default L0 hot path must not load or scan full rendered/raw HTML to create these signals.

#### Text features

- credential-request wording;
- OTP or verification-code request wording;
- payment-information request wording;
- wallet-approval or seed-phrase wording;
- download / install / execution inducement wording;
- gate-page semantics such as verify-human / challenge / Cloudflare / CAPTCHA;
- social-engineering narratives such as urgency, security-control, prize, recovery, or unlock/freeze-release wording.

#### Lightweight network-summary features

- suspicious external POST targets;
- unusual redirect behavior;
- unusual concentration of third-party domains;
- download targets or abnormal resource-request cues.

### 7.3 Weak-signal aggregation

On top of observation-first features, L0 may aggregate the following weak-signal families. These remain weak semantics and must not be treated as final labels.

#### `intent_signals`

Examples:

- `credential_intent_candidate`
- `otp_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `seed_phrase_intent_candidate`
- `personal_info_intent_candidate`
- `download_intent_candidate`

#### `brand_signals`

Compatibility examples:

- claimed brand token;
- brand mismatch across URL / text / forms;
- weak supportive evidence of brand impersonation.

In the current default hot path, L0 must treat `brand_signals` as a compatibility field or explicitly precomputed side input. L0 must not perform default brand extraction or make brand matching the basis of its specialized screening contract.

#### `evasion_signals`

Examples:

- `captcha_present_candidate`
- `challenge_present_candidate`
- `dynamic_redirect_candidate`
- `anti_bot_or_cloaking_candidate`
- `needs_interaction_candidate`
- `content_unrevealed_candidate`

#### `quality_signals`

Examples:

- key-input absence;
- extremely low page text;
- unrevealed main content;
- mismatch between current evidence and the threat context implied by the input URL;
- a current state that cannot be stably explained as a normal low-risk page.

### 7.3A Specialized Detector Families for High-Salience Verticals

In addition to the generic observation-first features and generic weak-signal families, L0 may support a small number of **specialized detector families** for page verticals or page surfaces that can be exposed with high salience from cheap evidence alone.

Current-priority specialized families include, but are not limited to:

- gambling / betting / casino lure
- adult / porn lure / age-gate-like adult surface
- gate / challenge / CAPTCHA surface

These specialized detectors do not replace generic L0 routing. Their role is to:

1. more quickly identify samples that must not be released through `early_stop_low_risk`;
2. emit high-value vertical weak signals earlier for later L1 / L2 usage;
3. provide specialized fast-path candidates for a very small subset of **high-salience, low-ambiguity, low-conflict** samples;
4. reduce unnecessary L1-text computation on extremely obvious page surfaces.

By default, these detector families may emit **weak signals / candidates / routing hints** only. They must not directly rewrite Warden's final threat taxonomy or final human adjudication.

### 7.3B Specialized Weak Signals

Specialized detectors may emit signals such as:

- `possible_gambling_lure`
- `possible_bonus_or_betting_induction`
- `gambling_weighted_score`
- `gambling_weighted_score_reasons`
- `possible_adult_lure`
- `possible_age_gate_surface`
- `possible_gate_or_evasion`
- `possible_challenge_surface`
- `specialized_fast_resolution_candidate`

Here:

- `specialized_fast_resolution_candidate` only means that the current cheap evidence exposes a highly salient, low-ambiguity, low-conflict specialized surface;
- `gambling_weighted_score` and `gambling_weighted_score_reasons` are explainability / recovery-support outputs that express why a gambling page is near or above the specialized trigger boundary;
- they exist for auditing, narrow recovery, and later tuning support, and do not by themselves define the final threat label;
- it is not a final label, not equivalent to final benign, and not equivalent to final malicious;
- if a future implementation wants to allow true L0 direct-resolution paths, that change must be frozen via an explicit task and document update, rather than silently extending the current contract.

### 7.3C Gambling Detector Guidance

For gambling pages, the current L0 baseline should rely on combinations of cheap structural evidence and cheap textual evidence, while keeping the implementation stance that structural evidence is stronger than weak inducement wording alone. The current priority order is roughly:

- host / URL structural evidence such as `bet`, `casino`, `slot`, `poker`, `lotto`, `sportsbook`, including host-token variants and especially `bet+digits` style patterns;
- strong gambling wording in visible text, such as `sportsbook`, `live dealer`, `cashier`, `bet365`, and highly salient Chinese gambling terms;
- transactional or landing-page support signals, such as sensitive forms or register / login / play-now / download-app / official-entry CTA patterns appearing together with gambling context;
- bonus / inducement wording such as `welcome bonus`, `free spins`, `promo code`, `deposit bonus`, and equivalent Chinese inducement terms;
- editorial / guide / review / news semantics, which act as suppression signals so that discussion pages, guide pages, and affiliate-style pages are not promoted into gambling landing pages too easily.

In the current baseline, `possible_gambling_lure` should normally be triggered by at least one of the following paths:

- a direct high-confidence gambling hit;
- sufficiently dense strong gambling text;
- strong gambling text combined with transactional surface evidence;
- sufficiently dense gambling text combined with transactional support;
- bonus / inducement wording combined with gambling text and transactional support;
- low-conflict combinations of URL / host structural evidence with gambling text or bonus wording.

The current `gambling_weighted_score` should be treated as an explainable support score rather than a standalone classifier. Its role is to:

- quantify the relative contribution of URL / host evidence, strong text, transactional support, bonus cues, and editorial suppression;
- provide auditable support for narrow recovery clauses;
- help separate true gambling landing pages from gambling-related editorial, guide, review, or affiliate content.

The current implementation should keep the following constraints:

- host / URL structural evidence carries more weight than weak bonus-only wording;
- weak inducement words such as `bonus`, `promotion`, `cashback`, `deposit`, or `withdrawal` must not trigger `possible_gambling_lure` on their own;
- when a page is clearly editorial / guide / review / news-like and lacks high-confidence gambling evidence, suppression should apply so that informational or affiliate pages are not promoted into gambling landing pages;
- `possible_bonus_or_betting_induction` should express a gambling-inducement surface only, and should normally require bonus wording together with gambling context, domain-structure clues, or strong text / CTA support.

The default routing consequences should include at least:

- when `possible_gambling_lure` is hit, `early_stop_low_risk` must be forbidden;
- when `possible_gambling_lure` is hit, L0 should normally emit a text-semantic upgrade hint for later L1 processing;
- when a gambling page also shows card payment, off-domain sensitive forms, third-party POSTs, or equivalent high-risk delivery signals, `need_l2_candidate` or an equivalent upgrade hint should be strengthened.

Under a separately approved fast-handling policy, a very small subset of highly salient gambling pages may be marked as `specialized_fast_resolution_candidate`, but that behavior must not be silently enabled in the current baseline.

### 7.3D Adult Detector Guidance

For adult pages, the current L0 baseline should rely on combinations of URL evidence, visible-text evidence, and age-gate semantics, while keeping the implementation stance that adult surfaces should be routed first and judged more deeply later. The current priority order is roughly:

- URL / host fragments such as `porn`, `porno`, `xxx`, `jav`, `91porn`, and other highly salient adult-domain or path tokens;
- adult wording in visible text, including explicit adult-content terms, nudity-related wording, sexual-content wording, and strong tokens such as `theporndude`, `pornhub`, `bdsm`, or `milf`; a very small number of repeated localized adult terms may also be added when the evidence is clean, such as `colmek`;
- age-gate semantics such as `18+`, `adults only`, `you must be 18`, `verify your age`, and equivalent minors-forbidden wording;
- adult-lure or gated-access wording such as `watch now`, `unlock`, `premium access`, `verify age`, and `create account`.

In the current baseline, `possible_adult_lure` should normally be triggered by at least one of the following paths:

- a direct adult URL / host hit;
- a direct high-confidence adult hit;
- at least `3` strong adult text hits;
- at least `2` strong adult text hits together with an adult domain / host hint;
- strong adult text co-occurring with strong age-gate semantics.
- under a narrow recovery allowlist, exactly `1` strong adult text hit may also trigger when the URL / host carries a salient adult-domain hint; the current allowlist is intentionally tiny and limited to highly salient tokens such as `jav`, `porno`, and `avxxx`.

The role of `possible_age_gate_surface` should be stated separately:

- it expresses that the page currently exposes an obvious adult age-gate surface;
- it should normally require age-gate wording together with adult text or adult URL evidence;
- it may co-occur with `possible_adult_lure`, or appear as a narrower supporting adult-surface signal.

The current implementation should also distinguish URL-only adult surfaces:

- when the adult signal comes mainly from URL / host evidence and text-side support is weak, L0 should treat the page as an adult surface that still needs stronger visual or semantic follow-up;
- such cases should not be treated as sufficiently evidenced low-risk pages inside L0;
- this case should normally strengthen `need_vision_candidate` or an equivalent visual-upgrade hint.

The default routing consequences should include at least:

- when `possible_adult_lure` or an equally salient adult surface is hit, `early_stop_low_risk` must be forbidden;
- when `possible_adult_lure` is hit, L0 should normally emit a text-semantic upgrade hint for later L1 processing;
- when an adult surface also shows download inducement, redirect anomalies, third-party delivery, or equivalent high-risk delivery signals, `need_l2_candidate` or an equivalent upgrade hint should be strengthened.

The current implementation should also keep one false-positive control constraint:

- when a page contains adult narrative wording only, but lacks sensitive forms, OTP evidence, payment evidence, or real delivery evidence, L0 should avoid over-interpreting generic credential / OTP / PII language as a higher-layer fraud label.
- weak content-rating cues or weak adult abbreviations, such as `nsfw`, `not safe for work`, generic `age verification`, or the ambiguous token `av`, should not trigger `possible_adult_lure` on their own;
- weaker adult-description terms such as `erotic`, `nude`, `nudity`, or `anal` should normally require stronger adult context or stronger age-gate support before they contribute to an adult-surface decision.
- on generic hosts, a single strong adult token plus weak wording, or two unsupported strong adult tokens without host support, should not automatically become `possible_adult_lure`; those pages should be left to stronger later-stage semantics unless additional adult-domain or age-gate support exists.
- the single-strong-token recovery path must remain narrow: it applies only on pages with salient adult-domain hints, and the token must be inside an explicit allowlist; ambiguous tokens or generic hosts must not enter through this path.
- localized lexicon-gap refinements must also remain narrow: only terms that repeatedly appear inside the mixed low-support miss bucket and show controlled benign rebound should be added; the current conservative additions are the text token `colmek` and the host/domain hint token `bokep`.

### 7.3E Gate / Challenge / CAPTCHA Detector Guidance

For gate / challenge / CAPTCHA pages, L0 may rely primarily on highly salient verification semantics, challenge prompts, unrevealed-content patterns, and typical gateway-provider hints. Examples include:

- text tokens such as `verify you are human`, `captcha`, `cloudflare`, `challenge`, `security check`, `checking your browser`, `press and hold`, and `request unsuccessful`;
- structural signals such as sparse main text, a single strong CTA, unrevealed main content, and a verification/intercept-first page state;
- runtime support signals such as captcha evidence, anti-bot / cloaking hints, variant-failed pages, or dynamic redirects.

For this family:

- `early_stop_low_risk` must be forbidden by default;
- L0 should emit `possible_gate_or_evasion` or `possible_challenge_surface`;
- when challenge / anti-bot / cloaking / dynamic-redirect / unrevealed-content uncertainty is present, L0 should strengthen `need_l2_candidate` or an equivalent escalation hint;
- more aggressive policies that would allow ordinary gate pages to be directly resolved in L0 must be frozen separately through an explicit task and contract update, and are not enabled by default in the current baseline.

### 7.4 Weak-risk aggregation

L0 may emit cheap weak-risk outputs such as:

- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`

But it must remain explicit that:

- this is a weak-risk output under cheap current evidence;
- it is not a final malicious verdict;
- it is not a final safety verdict;
- it cannot replace L1/L2 or human final adjudication.

## 8. Routing Semantics

The default L0 routing result must be restricted to the following three outcomes:

- `early_stop_low_risk`
- `escalate_to_L1`
- `direct_to_L2`

### 8.1 Formal meaning of `early_stop_low_risk`

`early_stop_low_risk` is a **routing result**, not a **ground-truth result**.

It only means:

> under the current L0 cheap-evidence observations and current routing policy thresholds, the sample did not trigger further escalation and therefore stops at L0.

It does not mean:

- the page is truly safe;
- the page is finally benign;
- the page has no malicious possibility;
- the page would never escalate under a later policy revision.

### 8.2 Meaning of `escalate_to_L1`

This means the sample should enter the main judgment layer for stronger semantic / structural judgment.

### 8.3 Meaning of `direct_to_L2`

This means the sample already presents strong gate / evasion / hard-case / high-uncertainty characteristics and should enter the higher-cost review stage directly rather than staying in L0 or a normal L1 path.

## 9. Early-stop Conditions and No-Early-Stop Conditions

### 9.1 Necessary conditions for `early_stop_low_risk`

L0 may emit `early_stop_low_risk` only when all of the following are satisfied:

1. current weak risk is low;
2. key inputs are sufficiently available and the sample is not in explicit degraded mode;
3. there is no sensitive-intent weak signal such as credential / OTP / payment / wallet / seed phrase / download intent;
4. there is no obvious supportive brand-impersonation signal from explicitly precomputed or compatibility-provided brand inputs;
5. there is no gate / CAPTCHA / challenge / Cloudflare / verify-human semantics;
6. there is no cloaking / dynamic redirect / needs-interaction / unrevealed-content signal;
7. there is no key evidence conflict;
8. the current page can be stably explained as an ordinary low-observed-risk page.

### 9.2 No-early-stop trigger families

If any of the following trigger families is present, L0 must not early-stop by default:

- sensitive-intent signals;
- supportive brand-impersonation or brand-mismatch signals from explicitly precomputed or compatibility-provided brand inputs;
- gate / challenge / CAPTCHA / Cloudflare semantics;
- dynamic redirect, anti-bot, cloaking, or needs-interaction signals;
- severe input absence or parsing failure;
- obvious conflicts across text / URL / forms / network summary;
- strong mismatch between a high-risk input URL context and the currently exposed page evidence;
- any high-uncertainty state that cannot be stably interpreted as a normal low-risk page.

### 9.3 Conservative default policy

When routing conditions are not sufficiently satisfied, L0 should prefer escalation to L1 over aggressive early stop.
If strong gate / evasion / hard-case features are present, L0 should prefer direct escalation to L2.

### 9.4 Fast-Handling Constraints for High-Salience Verticals

For high-salience verticals such as gambling, adult, and gate-like pages, L0 may emit specialized fast-handling candidates, but must obey the following constraints:

1. a specialized token hit must not be treated as a final label;
2. a low-conflict specialized detector hit must not be reinterpreted as `early_stop_low_risk`;
3. the default value of specialized detectors is first to:
   - more reliably forbid early stop for samples that should not early-stop;
   - emit vertical weak signals earlier;
   - provide earlier escalation hints;
4. if future work wants to enable direct L0 resolution for some extremely high-salience page surfaces, it must explicitly define:
   - the eligible page families;
   - the allowed direct-resolution results;
   - the relationship to the current route-result contract;
   - downstream compatibility impact;
   - validation and rollback plan.

## 10. Relationship to the Gate / Evasion Auxiliary Protocol

For gate / evasion samples, L0 is responsible for:

- detection;
- marking;
- escalation.

L0 is not responsible for:

- solving the gate;
- bypassing challenge pages;
- recovering the full click-through flow;
- hard-labeling a challenge page as if it were the final landing page.

When obvious gate / evasion semantics are present, L0 may:

- escalate the sample to L1 so the main judgment layer can identify the sample family;
- send the sample directly to L2 under strong gate / strong evasion / high-uncertainty conditions.

## 11. Boundary with L1 / L2

### 11.1 Boundary with L1

L1 is the main judgment layer.

L0 performs low-cost screening and routing. L1 performs stronger semantic / structural judgment.
L0 must not silently turn itself into L1 by accumulating hidden complexity.

### 11.2 Boundary with L2

L2 is the high-cost review stage.

L0 is only responsible for discovering samples that need L2. It is not responsible for heavy interaction, stronger review, or adversarial recovery.

## 12. Output Expectations

L0 outputs must remain structured, auditable, and explainable.

By default, the output should be able to express at least:

- `stage`
- `route_target`
- `escalated`
- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`
- `route_reasons`
- `input_quality`
- `missing_signals`
- `degraded_mode`
- concise observation and weak-signal summaries

If a deployment path cannot support some of these fields, the degraded behavior must still be declared explicitly.

## 13. Threshold and Policy Governance

L0 thresholds are policy items, not hidden magic.

Therefore:

- behavior-affecting thresholds must remain explicit;
- triggers that affect early stop or escalation must remain explicit;
- threshold changes that affect routing behavior must be reported;
- low model score or low single risk score must not be treated as a sufficient condition for early stop.

## 13A. Implementation Constraints for Specialized Detectors

At the current stage, specialized detector families must satisfy the following implementation constraints:

- script-first
- evidence-first
- token-family and pattern-family based
- shared evidence object first, no repeated raw scanning
- detector families emit weak signals first, routing consequences second
- no hidden heavy dependency

Recommended implementation path:

- a shared `evidence_preparer` should first produce `url_signals`, `text_signals`, `form_signals`, `network_signals`, and `quality_flags`;
- `gambling_detector`, `adult_detector`, and `gate_detector` should then emit specialized weak signals on top of the shared evidence object;
- `policies.py` should consume those specialized weak signals only for no-early-stop, upgrade, and `need_l2` routing decisions.

These detectors must not repeatedly rescan raw text, URLs, forms, and network summaries across multiple modules, and must not collapse complex category logic directly into `policies.py`.

## 14. Current Implementation Stance

The default implementation stance of L0 V1 is:

- script-first
- rule-first
- evidence-first
- routing-first
- explanation-first

The current version does not make the following part of the default L0 composition:

- machine-learning classifiers;
- URL-only models;
- URLNet-like models;
- LLMs;
- high-cost visual models;
- heavyweight inference chains.

If later scoring or calibration enhancements are desired for L0, they must be introduced explicitly through separate tasking or later version updates without silently breaking the frozen boundary in this document.

## 15. Constraints on Training-Time and Later Evolution

This file freezes the current L0 responsibility and routing contract. It does not freeze every future threshold, weight, or script detail.

During later stage-specific training or evaluation work, it remains acceptable to:

- adjust thresholds;
- adjust risk-reason composition;
- refine route-trigger implementation details;
- perform small-scope policy calibration.

But the default boundary must still forbid:

- rewriting the core role of L0;
- turning L0 into a final-adjudication stage;
- pushing gate / evasion heavy-interaction logic into L0;
- reinterpreting `early_stop_low_risk` as a ground-truth safety conclusion.

## 16. Validation Requirements

For any non-trivial L0-related change, validate at least:

1. low-cost input preparation works on a smoke sample;
2. L0 can emit a structured output;
3. routing results are consistent with route reasons;
4. degraded-mode behavior is explicit;
5. obvious gate / evasion samples are not early-stopped as ordinary low-risk pages;
6. output structure remains consistent with downstream consumers.

If any validation was not run, state exactly what was not run and why.

## 17. Definition of Done

The L0 Design Specification V1 can be treated as frozen only if:

- the responsibilities of L0 are explicit;
- the non-responsibilities of L0 are explicit;
- the input boundary of L0 is explicit;
- the routing semantics of L0 are explicit;
- the formal meaning of `early_stop_low_risk` is explicit;
- the no-early-stop conditions are explicit;
- the boundary with the Gate / Evasion Auxiliary Protocol is explicit;
- the L1 / L2 responsibility boundary is explicit;
- the implementation stance is explicitly script-first and rule-first;
- the document does not conflict with `AGENTS.md`, `PROJECT.md`, `MODULE_INFER.md`, `TRAINSET_V1.md`, `GATA_EVASION_AUXILIARY_SET_V1.md`, or the auto-label policy document.
