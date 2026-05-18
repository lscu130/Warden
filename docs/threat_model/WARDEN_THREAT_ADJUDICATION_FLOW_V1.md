# Warden 威胁判定流程 V1

## 中文版

> 面向 AI 的说明：英文版为权威执行规范。中文部分用于项目负责人快速确认任务边界与目标。

## 0. 中文摘要

Warden V1 的网页社会工程威胁公式为：

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

本文件冻结 Warden 从网页证据到未来 L1 final decision 的判定流程。核心结论：

- `invalid capture != benign / malicious / suspicious`
- `action surface != threat action`
- `claimed identity != confirmed impersonation`
- `brand/domain mismatch candidate != automatic malicious`
- `payload not observed != automatic benign`
- `business legitimacy unknown != malicious`
- `rule_router != classifier`
- `vision evidence != final judgment`

Warden 的主路径先抽取页面宣称身份，再结合 URL / domain、可见文本、title / heading / meta、actionable HTML、forms、network / redirect、OCR、YOLO / detector 证据判断风险。品牌库可以增强识别，但不是入口条件，也不能把“品牌出现”改写成恶意捷径。

操纵性上下文本身不能单独构成 V1 malicious。若当前 payload / action 未观察到，应记录为 `payload not observed`，不能自动判为 benign；V1 主判断还需要被诱导的高风险动作、可观测路由动作或动作准备信号。

普通登录、下载、支付、钱包、客服、KYC、二维码、第三方跳转等只是 action surface。只有当它们处在异常、欺骗、操纵、身份冲突、业务不合法、提交目标异常、下载目标异常或授权目标异常上下文中，才升级为 threat action candidate。

无效采集、HTTP 错误页、空白页、纯色页、严重渲染失败页和证据不可观测页是数据质量 / 可观测性失败。它们在正式 train / validation / test 构建前移除，不进入威胁标签体系。本文件不要求实现 recrawl / exclude / QA 队列。

## English Version

> AI note: This English section is authoritative. This document is a documentation contract. It does not change code, runtime behavior, labels, schemas, manifests, splits, samples, or final L1 output schema.

# Warden Threat Adjudication Flow V1

## 1. Purpose

This document defines Warden's project-level threat adjudication flow: how observed webpage evidence should move toward future L1 final decision semantics.

The document is intended for:

- human labelers;
- teacher-distillation prompts;
- `text_semantic_concepts` target definitions;
- `decision_head_auxiliary_targets`;
- future L1 Decision Head design and training;
- L1 error analysis;
- project-level threat-model explanations.

This document is not an implementation task, not a model-training task, not a schema migration, and not a final runtime schema freeze.

## 2. Core Definition

A Warden V1 Web-SE Threat is:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)

InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

A web-based social-engineering threat is a webpage for which observable evidence is sufficient to support both: (1) a deceptive, manipulative, or coercive context; and (2) an induced high-risk user action. The induced high-risk action may be directly requested on the current page, routed through an observable next-step action, or strongly prepared by page elements that move the user toward credential disclosure, PII submission, payment, wallet authorization, malicious download, fake support contact, account verification, or similar user-action risk.

This definition is broader than phishing-only detection. Phishing websites are a subset of Web-SE Threat, typically involving brand, identity, authority, institution, or service impersonation plus induced credential or sensitive-information disclosure.

## 3. Core Distinctions

These distinctions are mandatory:

```text
invalid capture != benign / malicious / suspicious
action surface != threat action
claimed identity != confirmed impersonation
brand/domain mismatch candidate != automatic malicious
payload not observed != automatic benign
business legitimacy unknown != malicious
rule_router != classifier
vision evidence != final judgment
```

Interpretation:

- Invalid captures are dataset-quality / observability failures, not threat samples.
- Action surfaces are opportunities for user action; they require context before becoming threat actions.
- Claimed identity extraction finds what the page says or implies; it does not prove impersonation by itself.
- Brand/domain mismatch is a candidate conflict signal; it needs evidence context.
- `payload not observed` is an evidence state, not a benign rule.
- `business legitimacy unknown` requires caution, review, or more evidence; it is not malicious by itself.
- Rule Router emits routing and evidence-sufficiency diagnostics only.
- Vision evidence recovers OCR text and UI evidence; it does not own the final decision.

## 4. Adjudication Flow Overview

The Warden adjudication flow has seven steps:

```text
Step 0: Sample validity / observability assumption
Step 1: Evidence sufficiency
Step 2: Claimed identity extraction and claim-strength assessment
Step 3: Action surface extraction
Step 4: Manipulative context assessment
Step 5: Identity / domain / business / action-target consistency assessment
Step 6: Induced high-risk action assessment
Step 7: Final decision semantics and reason-code rendering
```

Each step must preserve evidence provenance and must avoid one-factor malicious shortcuts.

## 5. Step 0: Sample Validity / Observability Assumption

Warden threat adjudication assumes a valid, observable webpage sample.

Invalid captures are removed during dataset construction and cleaning. They do not enter benign / malicious / suspicious / unknown threat labels.

Examples include:

- HTTP error page;
- blank page;
- pure-color page;
- severe broken render;
- evidence-unobservable page;
- structurally unusable page that cannot support basic human review.

This document does not require recrawl / exclude / QA queue implementation. Future capture infrastructure may separately decide how to retry or repair capture failures, but that is outside current threat adjudication semantics.

## 6. Step 1: Evidence Sufficiency

Warden should first assess whether enough evidence exists to adjudicate a valid webpage sample.

Evidence sources include:

- URL / domain / redirect;
- `visible_text`;
- title / heading / meta;
- actionable HTML;
- forms;
- network / redirect summary;
- OCR text, if triggered;
- YOLO / detector UI evidence, if triggered.

If evidence is insufficient:

- trigger OCR when screenshot text may recover missing or sparse text;
- trigger YOLO / detector evidence recovery when UI components may be visible but text / HTML is incomplete;
- output `unknown`, `insufficient_evidence`, or `needs_review` if evidence remains insufficient.

Never infer benign solely from `payload not observed`.

## 7. Step 2: Claimed Identity Extraction And Claim-Strength Assessment

`claimed_identity_extraction` is Warden's primary identity path. Warden should not start from a brand-list-first detector as the main entry point.

### 7.1 Structured Extraction

Structured extraction generates claimed identity candidates from:

- title;
- h1 / h2;
- meta;
- `visible_text`;
- logo alt text;
- image alt text;
- `aria-label`;
- copyright footer;
- form labels;
- button text;
- URL tokens;
- OCR text.

### 7.2 Text Semantic Concepts

`text_semantic_concepts` should decide whether a candidate is:

- an actual self-claim;
- a quoted mention;
- a third-party login;
- advertising;
- footer text;
- irrelevant reference.

It should also estimate:

- claim strength;
- identity type;
- evidence sources.

### 7.3 Brand Knowledge

Brand knowledge is optional enhancement only.

It can help normalize identities, detect known domains, or enrich relation checks. It is not the primary entry point and must not convert "brand appears in malicious samples" into a malicious shortcut.

Expected conceptual output example:

```json
{
  "claimed_identity_present": true,
  "claimed_identity_strength": "strong",
  "claimed_identity_type": "financial_service",
  "claim_sources": ["title", "heading", "visible_text", "url"]
}
```

These fields are conceptual / draft and are not final runtime schema.

## 8. Step 3: Action Surface Extraction

Action surfaces are sensitive or user-interactive opportunities exposed by the page.

Action surfaces include:

- login / password;
- MFA / OTP / verification code;
- card / payment / billing;
- wallet connect;
- seed phrase / private key;
- download / install / APK / EXE / extension;
- support / contact / chat / WhatsApp / Telegram;
- KYC / PII / identity collection;
- QR code;
- third-party redirect.

Mandatory principle:

```text
Action surface only means the page exposes a sensitive or user-interactive action surface.
It is not a threat action by itself.
```

## 9. Step 4: Manipulative Context Assessment

Manipulative context describes deceptive, manipulative, coercive, or abnormal context construction.

Categories include:

- identity impersonation;
- authority impersonation;
- claimed identity / domain conflict;
- fake security verification;
- fake account locked / account abnormality;
- fake support / fake technical assistance;
- fake prize / reward / airdrop / claim;
- fake investment / high-return manipulation;
- fake download / fake update;
- urgency / coercive / manipulative language;
- abnormal third-party submission / redirect;
- business-context inconsistency.

Manipulative context is required for a V1 Web-SE Threat, but it is not sufficient by itself. If direct payload / action is not observed, preserve `payload not observed` and evaluate whether routed action or action-preparation evidence is sufficient.

## 10. Step 5: Relation Consistency / Business Legitimacy

Warden must assess whether identity, domain, action, target, and business context are mutually consistent.

Relationship checks include:

- claimed identity vs host / domain / URL path;
- claimed identity vs page action;
- form action / redirect target consistency;
- download target consistency;
- wallet / payment / KYC consistency;
- hosted platform / SSO / OAuth / marketplace / CDN legitimate contexts.

Mandatory principle:

```text
unknown is not malicious
```

Unknown relation or unknown business legitimacy should usually produce caution, evidence limitation, or review. It must not become a one-factor malicious rule.

## 11. Step 6: Induced High-Risk Action Assessment

Induced high-risk action assessment combines action surface evidence with manipulative context and relation context.

Rules:

```text
ManipulativeContext ∧ (DirectAction ∨ RoutedAction ∨ ActionPreparation) ∧ EvidenceSufficient(...) = Web-SE Threat candidate
action surface + business legitimacy support = benign hard negative
action surface + insufficient evidence = needs_review / unknown
```

Examples:

- Normal login on official or otherwise legitimate context -> `benign_hard_negative`.
- Login with strong identity conflict and verification / account-locked narrative -> malicious when evidence is sufficient for both manipulative context and induced credential or sensitive-information disclosure.
- Normal download from official store, GitHub, or official CDN -> `benign_hard_negative`.
- Fake security update or suspicious executable under abnormal context -> malicious when the page induces, routes, or strongly prepares malicious download / installation action.
- Seed phrase / private key input -> high-risk action candidate, usually escalates strongly when context supports it.

## 12. Step 7: Final Decision Semantics And Reason-Code Rendering

The future L1 Decision Head owns final L1 decision semantics. Rule Router does not.

Decision rendering should preserve:

- final label;
- malicious basis;
- payload observation state;
- high-risk behavior evidence;
- action surface evidence;
- threat action evidence;
- business legitimacy assessment;
- evidence sufficiency;
- reason codes;
- review need.

Final malicious semantics require sufficient evidence for both manipulative context and an induced high-risk action. `payload not observed` may still coexist with routed action or action-preparation evidence; absent all induced-action evidence, the page should remain suspicious / needs_review / unknown rather than V1 malicious.

## 13. Decision Matrix

| manipulative context | induced high-risk action | evidence sufficiency | decision |
|---|---|---|---|
| strong | observed | sufficient | malicious / behavior+action |
| strong | routed or prepared | sufficient | malicious / context+routed-or-prepared-action |
| strong | not observed and not prepared/routed | sufficient | suspicious_high_risk / needs_review, not V1 malicious |
| weak/candidate | action surface present | sufficient | suspicious / needs_review unless evidence becomes sufficient for both formula terms |
| none | action surface present | sufficient and business-normal | benign_hard_negative |
| none | none | sufficient | benign |
| any | any | insufficient | unknown / insufficient_evidence / needs_review |

Notes:

- `payload not observed` is an evidence state. It does not automatically make a page benign, and it does not by itself make a page V1 malicious.
- `benign_hard_negative` means a page has action surfaces or confusing features but is supported by normal business context.
- `unknown` and `insufficient_evidence` are not malicious conclusions.

## 14. Conceptual Future L1 Decision Head Output

The following example is conceptual / draft. It is not final runtime schema and must not be treated as a schema freeze.

```json
{
  "final_label": "benign | malicious | suspicious | unknown",
  "malicious_basis": "none | direct_action | routed_action | action_preparation | context_and_action | insufficient_evidence",
  "payload_observed": true,
  "high_risk_behavior": {
    "present": true,
    "types": ["identity_impersonation", "brand_domain_conflict"]
  },
  "action_surface": {
    "present": true,
    "types": ["login", "download", "wallet_connect"]
  },
  "threat_action": {
    "present": true,
    "types": ["credential_collection"]
  },
  "business_legitimacy": {
    "assessment": "supported | weak | conflict_candidate | unknown"
  },
  "evidence_sufficiency": "sufficient | partial | insufficient",
  "reason_codes": [],
  "needs_review": false
}
```

This example does not change official runtime result schema, official trace schema, label enums, manifests, splits, or dataset files.

## 15. Relationship To L1 Components

### 15.1 Rule Router

Rule Router is a routing and evidence-sufficiency diagnostic component.

It may emit:

- evidence sufficiency diagnostics;
- OCR / YOLO need hints;
- review need hints;
- routing support signals.

It must not emit final benign / malicious / suspicious / unknown labels and must not be evaluated as final classifier accuracy.

### 15.2 Text Semantic Concepts

`text_semantic_concepts` are the main future structured semantic target layer.

They should support:

- claimed identity extraction;
- action surface extraction;
- behavior context assessment;
- relation consistency;
- business legitimacy;
- risk axes;
- page role candidates;
- routing recommendations.

They should not output hidden chain-of-thought or free-form final judgment.

### 15.3 Vision Evidence

Vision evidence is evidence recovery only.

Allowed online visual evidence roles:

- OCR recovers screenshot text;
- YOLO / detector localizes visible action components and UI evidence.

Vision evidence must not make the final malicious / benign decision. CLIP / MobileCLIP, SNet, and SpecularNet-like modules are not Warden V1 default-path components.

### 15.4 L1 Decision Head

The future L1 Decision Head is the owner of final L1 decision semantics.

It consumes structured evidence, `text_semantic_concepts`, optional OCR / YOLO evidence, Rule Router diagnostics, and evidence ledger references.

It is not trained or integrated yet. Its future output fields remain conceptual / draft until a separate schema-freeze task explicitly changes that status.

## 16. Distillation Alignment

Teacher distillation prompts should use this adjudication flow to produce advisory structured targets.

Required constraints:

- `rule_router` context is evidence / diagnostics only.
- `text_semantic_concepts` are primary structured targets.
- `decision_head_auxiliary_targets` are advisory only.
- Teacher output must not override human gold labels.
- `payload not observed` is not automatic benign.
- `action surface != threat action`.
- `unknown is not malicious`.
- V1 malicious requires sufficient evidence for both `ManipulativeContext` and `InducedHighRiskAction`.
- Visual observations must be made only when image input or OCR / detector evidence is actually available.

## 17. Non-Goals And Compatibility

This document does not:

- modify production code;
- modify runtime;
- modify L0 / L1 implementation;
- modify labels or label enums;
- modify schema files;
- modify manifests, splits, or samples;
- implement OCR / YOLO / CLIP / SNet / SpecularNet-like paths;
- train models;
- run teacher distillation;
- implement or change distillation runner behavior;
- freeze final L1 output schema;
- add dependencies;
- call external APIs.

Backward compatibility:

- Existing docs, schemas, code, and data artifacts remain compatible.
- This document clarifies adjudication semantics and aligns future documentation / training targets.

## 18. Counter-Review Checklist

Before using this document as a downstream prompt or training target contract, verify:

- brand/domain mismatch is not treated as a single-factor malicious rule;
- login, download, payment, wallet, support, KYC, QR, and redirect surfaces are not automatic threat actions;
- `payload not observed` is not treated as benign;
- V1 malicious is not inferred from manipulative context alone;
- invalid capture is outside threat labels;
- Rule Router is not treated as a classifier;
- CLIP / SNet are not implied as V1 default modules;
- conceptual Decision Head fields are not treated as final runtime schema;
- `unknown` is not equivalent to malicious;
- benign hard negatives remain represented;
- routed-action and action-preparation cases remain represented without reintroducing behavior-only malicious as a V1 main rule.
