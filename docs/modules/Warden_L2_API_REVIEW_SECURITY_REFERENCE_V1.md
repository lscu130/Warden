# Warden L2 API Review Security Reference V1

## 中文摘要

### 1. 文档目的

本文档用于为 Warden 的 L2 设计提供一份**可直接融入工程的安全参考稿**。
目标不是把 L2 变成一个“安全研究系统”，而是把 **StruQ + SelfDefend + RPO** 三类思想，连同面向真实网页交互的最小防御要求，压缩成一套**轻量、可落地、不过度头重脚轻**的设计建议。

本文档面向的 L2 形态是：

- `opt-in`
- `default-off`
- `high-cost`
- `case-level review`
- 仅在 `gate / evasion / hard L1 cases` 时触发
- 只消费来自 L1 / wrapper 的标准化 `case JSON`
- 只输出受限、结构化的 `decision JSON`

本文档**不主张**：

- 把 L2 做成自由浏览网页的通用代理；
- 把“防御能力”写成 L2 的主贡献；
- 让 prompt 防御盖过 Warden 的主线问题定义；
- 在 V1 就引入重型、多层、难维护的安全流水线。

### 2. 项目内定位

根据当前 Warden 项目规格：

- Warden 当前主线是 **lightweight, multimodal, staged social-engineering threat judgment**；
- **L1 是当前主判断层**；
- **L2 保留给高风险、困难、开放世界和后续鲁棒性问题**；
- gate / evasion 当前应保持在 **auxiliary** 位置，而不是静默吸收进 primary training objective；
- 当前阶段的完成标准首先是：**可复现、可审计、可交接**，而不是“看起来很先进”。

因此，本文档中的 L2 安全设计必须满足两条硬约束：

1. **不能把 L2 变成默认主路径；**
2. **不能让防御复杂度反客为主。**

### 3. 推荐论文与使用方式

本文档建议使用两层文献：

#### 3.1 核心防御思想（必须融入）

1. **StruQ (USENIX Security 2025, CCF-A)**  
   用于定义 L2 的**输入边界**：trusted prompt / untrusted data 双通道。

2. **SelfDefend (USENIX Security 2025, CCF-A)**  
   用于定义 L2 的**薄 guard 机制**：前置检查 + 后置动作检查，而不是把 guard 做成主系统。

3. **RPO (NeurIPS 2024, CCF-A)**  
   用于定义 L2 的**system prompt hardening**：安全 system prompt 需要固定模板、版本化、红队测试，而不是临时手写。

#### 3.2 交互与评测参考（建议吸收）

4. **Formalizing and Benchmarking Prompt Injection Attacks and Defenses (USENIX Security 2024, CCF-A)**  
   用于定义 L2 release 前的**红队清单和验线标准**。

5. **AgentFuzz / Make Agent Defeat Agent (USENIX Security 2025, CCF-A)**  
   用于定义 L2 的**交互前 fuzzing / taint-style vulnerability 检测**。

6. **ToolHijacker / Prompt Injection Attack to Tool Selection in LLM Agents (NDSS 2026, CCF-A)**  
   用于提醒：一旦 L2 拥有工具或动作选择能力，**动作库与候选动作文档本身也会成为攻击面**。

7. **ObliInjection (NDSS 2026, CCF-A)**  
   用于提醒：多源输入场景下，攻击者即使只控制部分输入片段，也可能利用排序不确定性达成注入。

### 4. Warden L2 的最小安全架构

建议把 L2 安全设计压成 **五层轻防护**：

#### 层 1：结构化输入边界（来自 StruQ）

- L2 只接受固定 schema 的 `case JSON`
- 任何网页文本、OCR、按钮文案都进入 `untrusted_*` 字段
- 系统规则、预算、允许动作只在 `trusted_*` 区域出现
- 禁止把网页原文直接拼到 system prompt 主体中

#### 层 2：动作白名单

L2 不直接操作浏览器，不生成任意动作。
它只能从 wrapper 提供的 `allowed_actions` 中做选择，例如：

- `click_candidate(candidate_id)`
- `wait(seconds)`
- `capture_next_state()`
- `stop_unresolved()`
- `escalate_manual()`

#### 层 3：薄 guard（来自 SelfDefend）

- **pre-check**：检查当前 case 是否包含明显注入、站外越界、敏感动作风险
- **post-check**：检查 L2 输出动作是否越过 allowlist / budget / domain fence

guard 必须是**门卫**，不是主判断器。

#### 层 4：prompt hardening（来自 RPO）

L2 的 system prompt 不应自由生长，而应当：

- 短小、固定模板
- 版本化管理
- 明确 trusted / untrusted 分区
- 明确禁止执行网页中的任何命令性文本
- 明确只允许结构化 JSON 输出
- 明确预算耗尽后的 `stop_unresolved`

#### 层 5：release 前攻击与交互验证

- 用 USENIX 2024 benchmark 思路做 prompt injection 红队
- 用 AgentFuzz 思路做 taint-style vulnerability 探测
- 用 ToolHijacker / ObliInjection 的威胁模型构造交互式对抗样例

### 5. 真实网站交互时必须补充的运行时防御

如果 L2 对 gate / evasion 采取真实网页交互，则仅靠 prompt 安全不够，还必须补以下运行时约束：

#### 5.1 浏览器上下文隔离

- 每个 case 使用新的无状态 browser context
- 不复用 cookies / local storage / session storage
- case 结束后销毁上下文

#### 5.2 域名与网络围栏

- 仅允许当前 case 主域和显式白名单辅助域
- 禁止任意站外导航
- 禁止访问内网 / 回环 / 未授权第三方域

#### 5.3 默认无身份模式

- 默认无真实登录态
- 不挂真实邮箱、钱包、支付信息、密码库
- 不允许输入凭据、OTP、助记词、支付信息

#### 5.4 敏感动作硬封禁

执行器层直接禁止：

- 登录提交
- 支付确认
- 钱包签名 / 授权
- 输入真实凭据
- 文件上传 / 下载执行
- 任意自由搜索与站外跳转

#### 5.5 严格预算

示例：

- `max_turns = 2`
- `max_clicks = 1`
- `max_captures = 2`
- `max_cross_domain_redirects = 1`
- 预算耗尽后必须 `stop_unresolved`

### 6. 不要把防御做成 L2 主体

为了避免 L2 “头重脚轻”，建议按下列优先级落地：

#### 必须做

- 结构化输入边界
- 动作白名单
- 预算上限
- 域名围栏
- 结构化输出
- 最小日志回放

#### 应该做

- pre-check / post-check 双 guard
- prompt 版本化与红队测试
- release 前 taint-style fuzzing

#### 先不做

- 多个 LLM 彼此辩论
- 自由网页浏览代理
- 全量多模态原图直接输入 L2
- 运行时复杂防御流水线叠加

### 7. 推荐的 V1 方案

#### V1.0

- L2 只处理 `case JSON`
- 只输出结构化决策
- 只允许极少量候选动作
- 不输入敏感数据
- 不跑完整业务流程
- 允许 `unresolved_requires_manual_review`

#### V1.5

- 增加更稳的 guard
- 增加 fuzzing / red-team 验线
- 对少量 gate case 做半自动 follow-up

#### V2

- 视数据与脚本成熟度，再考虑更强的交互能力
- 但仍应保持“受限复核器”定位，而不是自由代理

### 8. 结论

Warden 的 L2 如果引入 LLM，最稳的路线不是“把安全当主体”，而是：

- 用 **StruQ** 定输入边界；
- 用 **SelfDefend** 定薄 guard；
- 用 **RPO** 定 system prompt 强化；
- 用 **Formalizing & Benchmarking** 和 **AgentFuzz** 做 release 前验证；
- 用 **ToolHijacker / ObliInjection** 作为交互型威胁模型参考。

最终目标是：

> **让 L2 成为受限、可复盘、难越界的高成本复核器，而不是一个被网页牵着走的脆弱代理。**

### 9. References

1. StruQ: Defending Against Prompt Injection with Structured Queries. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe
2. SelfDefend: LLMs Can Defend Themselves against Jailbreaking in a Practical Manner. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/wang-xunguang
3. Robust Prompt Optimization for Defending Language Models Against Jailbreaking Attacks. NeurIPS 2024.  
   https://proceedings.neurips.cc/paper_files/paper/2024/hash/46ed503889ab232c21c1162340ee17b2-Abstract-Conference.html
4. Formalizing and Benchmarking Prompt Injection Attacks and Defenses. USENIX Security 2024.  
   https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei
5. Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu
6. Prompt Injection Attack to Tool Selection in LLM Agents. NDSS 2026.  
   https://www.ndss-symposium.org/ndss-paper/prompt-injection-attack-to-tool-selection-in-llm-agents/
7. ObliInjection: Order-Oblivious Prompt Injection Attack to LLM Agents with Multi-source Data. NDSS 2026.  
   https://www.ndss-symposium.org/ndss-paper/obliinjection-order-oblivious-prompt-injection-attack-to-llm-agents-with-multi-source-data/

---

## English Version

# Warden L2 API Review Security Reference V1

## 1. Purpose

This document defines a **lightweight, integration-oriented security reference** for Warden L2.
It is not intended to turn L2 into a standalone “LLM security system.”
Instead, it compresses the practical value of **StruQ + SelfDefend + RPO**, together with interaction-time defenses, into a form that can be integrated into Warden without making L2 top-heavy.

The intended L2 form is:

- `opt-in`
- `default-off`
- `high-cost`
- `case-level review`
- triggered only for `gate / evasion / hard L1 cases`
- consuming only standardized `case JSON` from L1 / wrappers
- producing only constrained, structured `decision JSON`

This document does **not** recommend:

- turning L2 into a general-purpose free-browsing agent;
- making defense the primary contribution of L2;
- letting security complexity overshadow Warden’s main problem framing;
- introducing a heavy, multi-layered, hard-to-maintain defense pipeline in V1.

## 2. Project-Level Fit

Under the current Warden project specification:

- the mainline problem is **lightweight, multimodal, staged social-engineering threat judgment**;
- **L1 is the current main judgment layer**;
- **L2 is reserved for high-risk, hard, open-world, and later robustness-oriented problems**;
- gate / evasion should stay in an **auxiliary** position rather than being silently absorbed into the primary training objective;
- the current-stage completion standard prioritizes **reproducibility, auditability, and handoffability**, not superficial sophistication.

Therefore, L2 security design must satisfy two hard constraints:

1. **L2 must not become a default path.**
2. **Defense complexity must not dominate the module.**

## 3. Recommended Literature and How to Use It

This document uses two literature layers.

### 3.1 Core Defense Ideas (must be integrated)

1. **StruQ (USENIX Security 2025, CCF-A)**  
   Used to define the **input boundary** of L2: a strict two-channel separation between trusted instructions and untrusted data.

2. **SelfDefend (USENIX Security 2025, CCF-A)**  
   Used to define a **thin guard mechanism** around L2: a pre-check and a post-check, rather than a defense-heavy core.

3. **RPO (NeurIPS 2024, CCF-A)**  
   Used to define **system prompt hardening**: the L2 system prompt should be short, versioned, and red-team tested rather than improvised.

### 3.2 Interaction and Validation References (strongly recommended)

4. **Formalizing and Benchmarking Prompt Injection Attacks and Defenses (USENIX Security 2024, CCF-A)**  
   Used to define the **release-time red-team checklist and validation scope** for L2.

5. **AgentFuzz / Make Agent Defeat Agent (USENIX Security 2025, CCF-A)**  
   Used to define **pre-release taint-style vulnerability testing** for interaction-capable L2 paths.

6. **ToolHijacker / Prompt Injection Attack to Tool Selection in LLM Agents (NDSS 2026, CCF-A)**  
   Used as a threat reference to show that once L2 can select tools or actions, **the action library and candidate-action descriptions themselves become an attack surface**.

7. **ObliInjection (NDSS 2026, CCF-A)**  
   Used as a threat reference for **multi-source input settings**, where attackers may control only a subset of inputs yet still succeed via ordering-insensitive injection.

## 4. Minimal Security Architecture for Warden L2

The recommended L2 security design should be compressed into **five thin protection layers**.

### Layer 1: Structured Input Boundary (from StruQ)

- L2 accepts only a fixed-schema `case JSON`
- all webpage-derived text, OCR, and button strings are placed into `untrusted_*` fields
- system rules, budgets, and allowed actions appear only in `trusted_*` areas
- raw webpage text must never be concatenated directly into the main system prompt

### Layer 2: Action Allowlist

L2 must not operate as a free agent.
It should only choose from wrapper-defined actions such as:

- `click_candidate(candidate_id)`
- `wait(seconds)`
- `capture_next_state()`
- `stop_unresolved()`
- `escalate_manual()`

### Layer 3: Thin Guard (from SelfDefend)

- **pre-check**: inspect the case for obvious injection, off-domain drift, or sensitive-action risk
- **post-check**: inspect the model-selected action for allowlist, budget, and domain-boundary violations

The guard must remain a **gatekeeper**, not the main case reasoner.

### Layer 4: Prompt Hardening (from RPO)

The L2 system prompt should not evolve ad hoc.
It should be:

- short
- template-based
- version-controlled
- explicit about trusted vs untrusted regions
- explicit about ignoring all operational instructions from webpage-derived content
- explicit about structured JSON-only outputs
- explicit about mandatory `stop_unresolved` at budget exhaustion

### Layer 5: Release-Time Attack and Interaction Validation

- use the USENIX 2024 benchmark mindset for prompt-injection red teaming
- use AgentFuzz-style taint-vulnerability testing before release
- use ToolHijacker and ObliInjection threat models to build interaction-time adversarial test cases

## 5. Additional Runtime Defenses Required for Real-Web Interaction

If L2 actually interacts with real websites during gate / evasion handling, prompt safety alone is insufficient.
The following runtime defenses must also be added.

### 5.1 Browser Context Isolation

- each case uses a fresh, non-persistent browser context
- cookies, local storage, and session storage are not reused
- the context is destroyed after the case ends

### 5.2 Domain and Network Fencing

- only the main case domain and explicitly approved auxiliary domains are allowed
- arbitrary off-domain navigation is disallowed
- internal IPs, loopback addresses, and unauthorized third-party domains are blocked

### 5.3 Logged-Out, No-Identity Default Mode

- no real login state by default
- no real email, wallet, payment identity, or password store attached
- no credential, OTP, seed phrase, or payment entry allowed

### 5.4 Hard Blocking of Sensitive Actions

The executor must directly forbid:

- login submission
- payment confirmation
- wallet signing or authorization
- entering real credentials
- file upload / executable download
- arbitrary free search or off-domain travel

### 5.5 Strict Interaction Budget

Example:

- `max_turns = 2`
- `max_clicks = 1`
- `max_captures = 2`
- `max_cross_domain_redirects = 1`
- mandatory `stop_unresolved` at budget exhaustion

## 6. Do Not Turn Defense into the Main Body of L2

To avoid a top-heavy L2, implementation priority should be:

### Must-have

- structured input boundary
- action allowlist
- hard budgets
- domain fencing
- structured output
- minimal replay logging

### Should-have

- pre-check / post-check guards
- system-prompt versioning and red-team testing
- release-time taint-style fuzzing

### Not for V1

- multi-LLM debate systems
- free-browsing web agents
- direct unrestricted multimodal raw-image ingestion into L2
- stacked runtime defense pipelines

## 7. Recommended V1 Plan

### V1.0

- L2 consumes only `case JSON`
- L2 emits only structured decisions
- only a very small number of candidate actions are allowed
- no sensitive data entry is permitted
- full business-flow completion is disallowed
- `unresolved_requires_manual_review` is a valid outcome

### V1.5

- stronger guards
- fuzzing / red-team validation
- semi-automatic follow-up for a small subset of gate cases

### V2

- stronger interaction ability can be considered if data and tooling mature
- but the “constrained reviewer” identity should remain unchanged

## 8. Conclusion

If Warden introduces an API-backed LLM into L2, the safest route is not to make security the core of the module.
Instead:

- use **StruQ** to define the input boundary;
- use **SelfDefend** to define a thin guard;
- use **RPO** to harden the system prompt;
- use **Formalizing & Benchmarking** and **AgentFuzz** for release-time validation;
- use **ToolHijacker / ObliInjection** as interaction-time threat references.

The design goal is:

> **Make L2 a constrained, replayable, hard-to-abuse high-cost reviewer rather than a fragile agent led by webpage content.**

## 9. References

1. StruQ: Defending Against Prompt Injection with Structured Queries. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe
2. SelfDefend: LLMs Can Defend Themselves against Jailbreaking in a Practical Manner. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/wang-xunguang
3. Robust Prompt Optimization for Defending Language Models Against Jailbreaking Attacks. NeurIPS 2024.  
   https://proceedings.neurips.cc/paper_files/paper/2024/hash/46ed503889ab232c21c1162340ee17b2-Abstract-Conference.html
4. Formalizing and Benchmarking Prompt Injection Attacks and Defenses. USENIX Security 2024.  
   https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei
5. Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents. USENIX Security 2025.  
   https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu
6. Prompt Injection Attack to Tool Selection in LLM Agents. NDSS 2026.  
   https://www.ndss-symposium.org/ndss-paper/prompt-injection-attack-to-tool-selection-in-llm-agents/
7. ObliInjection: Order-Oblivious Prompt Injection Attack to LLM Agents with Multi-source Data. NDSS 2026.  
   https://www.ndss-symposium.org/ndss-paper/obliinjection-order-oblivious-prompt-injection-attack-to-llm-agents-with-multi-source-data/
