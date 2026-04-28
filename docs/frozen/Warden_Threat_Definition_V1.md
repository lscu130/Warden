# Warden Threat Definition V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

Warden 的社会工程威胁定义为：**高危欺骗行为和/或高危诱导动作**。

高危欺骗行为包括虚假或误导性的身份、品牌、权威、机构、安全、金融、客服、奖励或访问控制上下文构造。页面即使当前没有观察到登录框、支付框、钱包流程、下载、POST 提交或其他高危动作，也可能因为高危欺骗行为构成 malicious。

高危诱导动作包括凭证收集、OTP 收集、支付信息收集、钱包授权或助记词索取、PII/KYC 收集、恶意下载、假客服引流或攻击链跳转。

如果当前证据没有观察到 payload / action，应表述为 `payload not observed`，不能自动判为 benign。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Threat Definition V1

## 1. Canonical Definition

Warden defines a webpage social-engineering threat as a webpage that exhibits high-risk deceptive behavior and/or induces, prepares, or routes the user toward high-risk actions.

High-risk deceptive behavior includes false or misleading identity, brand, authority, institution, security, financial, support, reward, or access-control context construction.

Such behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other high-risk action is currently observed.

High-risk actions include attempts to collect credentials, OTP codes, payment details, wallet approvals or seed phrases, PII/KYC data, malicious downloads, fake-support contact diversion, or attack-chain redirects.

Short form:

**Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.**

## 2. Required Distinctions

- `high-risk behavior`: the page constructs a deceptive identity, trust context, scenario, authority, brand surface, or access-control context.
- `high-risk action`: the page asks, routes, pressures, or enables the user to enter, approve, pay, download, contact, authorize, or otherwise perform a dangerous action.
- `payload not observed`: no currently captured form, POST, wallet flow, payment flow, download flow, or other high-risk action component is observed.
- `malicious by behavior`: the page is malicious because high-risk deceptive behavior is observed, even if payload/action is not yet observed.

## 3. Non-Goals

This definition does not rename schema fields, label enums, CLI commands, or output formats.

It does not make brand mismatch a universal one-factor malicious rule.

It does not reduce Warden to brand phishing, logo matching, or payload-only detection.

## 4. Compatibility Notes

Existing label schemas may continue to use stable action-oriented fields for compatibility.

Behavior/action split fields such as `malicious_basis`, `high_risk_behavior_type`, `high_risk_action_type`, or `payload_observed` require a future explicit schema task before implementation.
