# Warden Threat Definition V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

Warden V1 的核心威胁公式为：

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

操纵性上下文包括虚假或误导性的身份、品牌、权威、机构、安全、金融、客服、奖励或访问控制上下文构造。被诱导的高风险动作包括凭证收集、OTP 收集、支付信息收集、钱包授权或助记词索取、PII/KYC 收集、恶意下载、假客服引流、账户验证/解锁或可观测的高风险动作入口。

如果当前证据没有观察到 payload / action，应表述为 `payload not observed`，不能自动判为 benign；该状态本身也不足以构成 V1 malicious。

成人、博彩、枪支、毒品或其他 high-risk-content-only 页面不属于 V1 主任务，除非页面同时有充分证据支持操纵性上下文和被诱导的高风险动作。gate-only、challenge-only、CAPTCHA-only、human-verification-only、redirect-only、trusted-sink-only 和 evasion/cloaking 捕获不因捕获形态直接成为 V1 malicious。

无效采集、HTTP 错误页、空白页、纯色渲染页、严重渲染失败页、证据不可观测页面不是 Warden 威胁模型样本。它们不能被标记为 benign、malicious 或 suspicious。在数据集构建流程中，项目负责人会在正式 train / validation / test 前移除这些样本。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Threat Definition V1

## 1. Canonical Definition

A web-based social-engineering threat is a webpage for which observable evidence is sufficient to support both: (1) a deceptive, manipulative, or coercive context; and (2) an induced high-risk user action.

Canonical formula:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

`ManipulativeContext` includes deceptive, manipulative, or coercive identity, brand, authority, institution, security, financial, support, reward, or access-control context construction.

`InducedHighRiskAction` may be directly requested on the current page, routed through an observable next-step action, or strongly prepared by page elements that move the user toward credential disclosure, OTP disclosure, payment, wallet authorization, seed/private-key disclosure, PII/KYC submission, malicious download, fake-support contact, account verification/unlock, or a similar user-action risk.

Phishing websites are a subset of Web-SE Threat. In Warden V1, phishing typically involves brand, identity, authority, institution, or service impersonation plus induced credential or sensitive-information disclosure.

## 2. Required Distinctions

- `ManipulativeContext`: the page constructs a deceptive, manipulative, or coercive identity, trust context, scenario, authority, brand surface, or access-control context.
- `DirectAction`: the page directly asks the user to enter, approve, pay, download, contact, authorize, or otherwise perform a dangerous action.
- `RoutedAction`: the page provides an observable next-step path toward a high-risk action.
- `ActionPreparation`: the page strongly prepares the user for a high-risk action through page elements, prompts, or staged flow even when the final action component is not yet captured.
- `EvidenceSufficient(...)`: the available URL, text, DOM/HTML, forms, network, screenshot/OCR, detector, relation, and context evidence is sufficient for the stated claim.
- `payload not observed`: no currently captured form, POST, wallet flow, payment flow, download flow, or other high-risk action component is observed.

Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are not Warden threat-model samples. They must not be labeled as benign, malicious, or suspicious. In the dataset-building workflow, the project owner removes these samples before formal train / validation / test construction.

Adult, gambling, guns, drugs, or other regulated/high-risk-content-only pages are outside the V1 main task unless the page also contains sufficient evidence of manipulative context inducing a high-risk user action.

Gate-only, challenge-only, CAPTCHA-only, human-verification-only, redirect-only, trusted-sink-only, and insufficient-observability captures are excluded from the V1 main benchmark and must not be labeled as V1 malicious solely due to their capture pattern. If downstream content is observed and satisfies the Web-SE Threat formula, the downstream threat page may be admitted. Evasion/cloaking-aware detection is deferred to V2/V3 or a separate auxiliary study.

## 3. Non-Goals

This definition does not rename schema fields, label enums, CLI commands, or output formats.

It does not make brand mismatch a universal one-factor malicious rule.

It does not reduce Warden to brand phishing, logo matching, or payload-only detection.

## 4. Compatibility Notes

Existing label schemas may continue to use stable action-oriented fields for compatibility.

Formula-alignment fields such as `manipulative_context`, `direct_action`, `routed_action`, `action_preparation`, `malicious_basis`, `high_risk_action_type`, or `payload_observed` require a future explicit schema task before implementation.
