# WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1

## 中文版

### 摘要

本文档定义 Warden L1 的未来 `Text Semantic Concepts`、`vision_evidence`、结构化证据和 `Decision Head` 草案契约。

项目级威胁判定流程见 `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`。本文档中的 `text_semantic_concepts`、`vision_evidence` 和未来 `Decision Head` 字段应按该流程解释；本文档仍是 draft contract，不冻结 final runtime schema。

当前状态：

- `rule_router` 只做路由与证据充分性诊断。
- `text_semantic_concepts` 当前是 stub，未来由文本塔或蒸馏模型输出结构化语义概念。
- `vision_evidence` 当前是 stub，未来由 OCR / YOLO 提供补充证据。
- `decision_head.status` 当前为 `not_run`。
- 本文档是 draft contract，不改变 official runtime schema，不冻结 final L1 schema。

关键原则：

- Rule Router 不是 classifier；它不能输出最终 `benign / malicious / suspicious / unknown`。
- L1-text 是主要语义判断分支。
- L1-vision 是 Visual Evidence Recovery，只补证据，不独立判断恶意。
- OCR 用于恢复截图文字。
- YOLO / detector 用于定位输入框、按钮、二维码、钱包按钮、下载按钮、验证码等 UI 证据。
- CLIP / MobileCLIP、SNet、SpecularNet-like 不属于 Warden V1 default path。
- 无效采集、HTTP 错误页、空白页、纯色渲染页、严重渲染失败页、证据不可观测页面不是 L1 威胁标签；数据集构建时应在正式 train / validation / test 前移除。
- L1 Decision Head 未来消费文本语义概念、结构化证据和可选视觉补证据，再输出 future L1 final decision。

### L1 草案流程

```text
Processed Valid Dataset
  -> Evidence Pack Builder
  -> Rule Router / Evidence Sufficiency Diagnostic
  -> Text Semantic Concept Extractor
  -> Optional Visual Evidence Recovery
  -> Structured Feature Builder
  -> L1 Decision Head
  -> Evidence Renderer
```

### 核心约束

```text
action surface != threat action
```

登录表单、下载按钮、钱包按钮、支持页面、支付页面或第三方跳转是 action surface。它们必须结合欺骗身份、操纵叙事、异常目标、异常提交、业务上下文冲突或其他高风险上下文，才可能升级为 threat action。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden L1 Decision Head Contract V0.1

## 1. Purpose

This document defines the draft interface contract for future Warden L1 text semantic concepts, optional visual evidence recovery, structured evidence, and the L1 Decision Head.

This document is a contract draft for future implementation and training alignment. It is not final schema, not official runtime schema, not a model implementation, and not a benchmark claim.

The project-level threat adjudication flow is defined in `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`. Interpret `text_semantic_concepts`, `vision_evidence`, and future `Decision Head` fields through that flow; this document remains a draft contract and does not freeze final runtime schema.

The detailed text concept and relation-judgment target contract is defined in `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`. That document refines `claimed_identity_candidates`, `text_semantic_concepts`, relation judgments, Decision Head concept inputs, and concept-level evaluation requirements without changing official runtime schema.

Current status:

- `rule_router` is a routing and evidence-sufficiency diagnostic component.
- `text_semantic_concepts` is currently a stub placeholder.
- `vision_evidence` is currently a stub placeholder.
- `decision_head.status` is currently `not_run`.
- final-like `decision_head` fields are currently `null` in the draft sidecar.

## 2. L1 Stage Semantics

Warden L1 should be understood as this staged pipeline for the current offline experiment path:

```text
Processed Valid Dataset
  -> Evidence Pack Builder
  -> Rule Router / Evidence Sufficiency Diagnostic
  -> Text Semantic Concept Extractor
  -> Optional Visual Evidence Recovery
  -> Structured Feature Builder
  -> L1 Decision Head
  -> Evidence Renderer
```

Future online / wild-test adds capture and scope admission before the same evidence-pack and L1 path:

```text
Raw URL
  -> Capture Pipeline
  -> Capture QA / V1 Scope Admission
  -> Evidence Pack Builder
  -> L1 Main Judgment
  -> Wild-Test Report
```

Responsibilities:

- Evidence Pack Builder collects source-aware URL, visible text, actionable HTML, forms, network, artifact presence, and optional visual artifacts.
- Rule Router diagnoses evidence sufficiency and emits routing hints.
- Text Semantic Concept Extractor emits bounded semantic concept groups and relation judgments.
- Visual Evidence Recovery adds OCR text and detector-localized UI evidence when requested.
- Structured Feature Builder normalizes URL, HTML, forms, network, rule-router, text-concept, and visual evidence fields for the Decision Head.
- L1 Decision Head owns the future L1 final decision.
- Evidence Renderer renders deterministic explanations from evidence ledger, reason codes, and Decision Head outputs when the Decision Head has run.

## 3. Rule Router Contract

Rule Router is not a classifier.

It must not emit final labels:

```text
benign
malicious
suspicious
unknown
```

Rule Router may emit only diagnostic and routing-oriented fields.

Rule Router is a routing and evidence-sufficiency diagnostic component. It must not emit final-like benign / malicious / suspicious labels, and it must not implement recrawl / exclude / QA routing for invalid captures.

Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are not Warden threat-model samples. They must not be labeled as benign, malicious, or suspicious. In the dataset-building workflow, the project owner removes these samples before formal train / validation / test construction.

Draft `rule_router` shape:

```json
{
  "rule_router": {
    "rule_assessment": "needs_text_model_judgment",
    "routing_assessment": "route_to_text_tower",
    "routing_hints": {
      "need_text_tower": true,
      "need_ocr": false,
      "need_yolo": false,
      "need_review": false
    },
    "risk_hints": {
      "action_surface_present": true,
      "payload_surface_observed": true,
      "behavior_context_hint_present": false,
      "relation_conflict_hint_present": false,
      "strong_malicious_rule_hit": false,
      "high_risk_candidate": false,
      "low_risk_candidate": false,
      "benign_hard_negative_candidate": true
    },
    "evidence_sufficiency": {
      "visible_text_status": "sufficient",
      "html_action_status": "sufficient",
      "needs_visual_recovery": false
    },
    "reason_codes": [
      "login_surface_present",
      "benign_hard_negative_candidate"
    ]
  }
}
```

Allowed `rule_assessment` values:

```text
low_risk_candidate
benign_hard_negative_candidate
text_sufficient
text_sparse
html_action_sparse
needs_text_model_judgment
needs_vision_evidence
needs_review
insufficient_observability
high_risk_candidate
insufficient_evidence
```

Interpretation:

- `high_risk_candidate` is a routing / review candidate signal.
- `low_risk_candidate` is a routing / sufficiency signal.
- Neither value is an L1 final label.
- Rule Router output must not be reported as final accuracy.

## 4. Text Semantic Concept Extractor Contract

The future Text Semantic Concept Extractor consumes source-aware text evidence such as visible text, compact actionable HTML text, URL-derived text, form summaries, network summaries, and optional OCR text when available.

It must output structured semantic concepts and bounded relation judgments. It must not output chain-of-thought or free-form final judgment.

It should use claimed identity extraction as the primary identity path. Brand knowledge may enrich normalization and relation checks, but brand-list-first detection is not the primary entry point and must not become a malicious shortcut.

The detailed concept groups, including `identity_domain_relation`, `business_legitimacy_hint`, evidence-state concepts, and threat-action candidate concepts, are defined in `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`.

Draft shape:

```json
{
  "text_semantic_concepts": {
    "status": "ran",
    "model_id": "future_text_tower_or_distilled_model",
    "schema_version": "warden_l1_text_semantic_concepts_v0_1",
    "action_surfaces": {},
    "behavior_contexts": {},
    "relation_consistency": {},
    "risk_axes": {},
    "page_role_candidates": {},
    "routing_recommendations": {},
    "evidence_ids": []
  }
}
```

When the model is unavailable, current draft output should remain:

```json
{
  "text_semantic_concepts": {
    "status": "stub_not_run",
    "reason": "real_text_tower_not_available_yet",
    "concept_outputs": {}
  }
}
```

### 4.1 `action_surfaces`

Action surfaces describe observed or inferred user-action opportunities. They do not by themselves prove threat action.

Required principle:

```text
action surface != threat action
```

Draft fields:

```json
{
  "action_surfaces": {
    "login_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "signup_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "payment_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "wallet_connect_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "download_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "support_contact_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "pii_collection_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "third_party_redirect_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "otp_or_mfa_surface": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "seed_or_private_key_surface": {"present": false, "confidence": 0.0, "evidence_ids": []}
  }
}
```

Interpretation:

- A login form, download button, wallet button, support page, payment page, or third-party redirect is not automatically malicious.
- Threat action requires additional context such as deceptive identity, manipulative narrative, suspicious target, abnormal submission, business-context conflict, or inherently dangerous collection.

### 4.2 `behavior_contexts`

Behavior contexts describe social-engineering narrative, identity construction, or contextual manipulation.

Draft fields:

```json
{
  "behavior_contexts": {
    "brand_impersonation_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "authority_impersonation_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "fake_security_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "fake_financial_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "fake_reward_or_prize_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "fake_support_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "urgency_or_threat_context": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "deceptive_hosted_brand_shell": {"present": false, "confidence": 0.0, "evidence_ids": []},
    "suspicious_business_context": {"present": false, "confidence": 0.0, "evidence_ids": []}
  }
}
```

### 4.3 `relation_consistency`

Relation consistency fields compare claims, actions, and destinations.

Draft fields:

```json
{
  "relation_consistency": {
    "brand_domain_alignment": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "brand_url_token_consistency": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "claimed_brand_officiality": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "form_action_alignment": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "download_target_alignment": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "redirect_chain_reasonableness": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "hosted_platform_context": {"value": "unknown", "confidence": 0.0, "evidence_ids": []},
    "business_legitimacy_context": {"value": "unknown", "confidence": 0.0, "evidence_ids": []}
  }
}
```

Suggested values:

```text
aligned
weakly_aligned
conflict
insufficient_evidence
unknown
```

### 4.4 `risk_axes`

Risk axes are bounded model outputs used by the Decision Head.

Draft fields:

```json
{
  "risk_axes": {
    "human_exposure_risk": {"score": 0.0, "evidence_ids": []},
    "deceptive_identity_risk": {"score": 0.0, "evidence_ids": []},
    "observed_action_risk": {"score": 0.0, "evidence_ids": []},
    "payload_deployment_risk": {"score": 0.0, "evidence_ids": []},
    "evidence_incompleteness_risk": {"score": 0.0, "evidence_ids": []},
    "gate_or_evasion_risk": {"score": 0.0, "evidence_ids": []}
  }
}
```

Scores are draft model features, not final labels.

### 4.5 `page_role_candidates`

Draft fields:

```json
{
  "page_role_candidates": {
    "clear_benign": {"score": 0.0, "evidence_ids": []},
    "benign_hard_negative": {"score": 0.0, "evidence_ids": []},
    "brand_impersonation_shell_without_payload": {"score": 0.0, "evidence_ids": []},
    "credential_collection_page": {"score": 0.0, "evidence_ids": []},
    "payment_collection_page": {"score": 0.0, "evidence_ids": []},
    "wallet_abuse_page": {"score": 0.0, "evidence_ids": []},
    "fake_download_lure_page": {"score": 0.0, "evidence_ids": []},
    "fake_support_page": {"score": 0.0, "evidence_ids": []},
    "gate_or_evasion_shell": {"score": 0.0, "evidence_ids": []},
    "intermediary_or_redirector": {"score": 0.0, "evidence_ids": []},
    "unknown": {"score": 0.0, "evidence_ids": []}
  }
}
```

### 4.6 `routing_recommendations`

Draft fields:

```json
{
  "routing_recommendations": {
    "need_ocr": {"value": false, "reason_codes": []},
    "need_yolo": {"value": false, "reason_codes": []},
    "need_review": {"value": false, "reason_codes": []},
    "need_human_review": {"value": false, "reason_codes": []}
  }
}
```

These recommendations support routing and future Decision Head context. They do not override official runtime routing unless a later task explicitly integrates them.

## 5. Visual Evidence Recovery Contract

L1-vision is evidence recovery only.

Responsibilities:

- OCR recovers screenshot text when visible text or HTML-derived text is missing, sparse, image-rendered, or incomplete.
- YOLO / detector localizes UI components such as input boxes, password fields, OTP fields, card fields, wallet buttons, download buttons, QR codes, captcha widgets, popups, modals, and primary CTA buttons.
- Vision outputs must be converted into structured evidence before the Decision Head consumes them.
- Vision must not output final malicious / benign judgment.

CLIP / MobileCLIP, SNet, and SpecularNet-like routes are not part of the Warden V1 default path. They may remain offline research, ablation, clustering, template discovery, or future optional feature-flag topics only after separate approval.

Draft `vision_evidence` shape:

```json
{
  "vision_evidence": {
    "status": "not_run",
    "need_ocr": false,
    "need_yolo": false,
    "ocr_text_fragments": [],
    "detected_ui_components": [],
    "evidence_ids": [],
    "errors": []
  }
}
```

When visual recovery runs in the future:

```json
{
  "vision_evidence": {
    "status": "ran",
    "need_ocr": true,
    "need_yolo": true,
    "ocr_text_fragments": [
      {
        "text": "Verify your account",
        "bbox": [12, 40, 280, 78],
        "confidence": 0.91,
        "evidence_id": "vis_ocr_0001"
      }
    ],
    "detected_ui_components": [
      {
        "component_type": "password_input",
        "bbox": [40, 210, 420, 252],
        "confidence": 0.87,
        "evidence_id": "vis_ui_0001"
      }
    ],
    "evidence_ids": ["vis_ocr_0001", "vis_ui_0001"],
    "errors": []
  }
}
```

## 6. Structured Feature Builder Contract

The Structured Feature Builder normalizes current evidence into a Decision Head input bundle.

Draft input families:

- `url_features`
- `visible_text_features`
- `html_actionable_features`
- `form_features`
- `network_features`
- `rule_router`
- `text_semantic_concepts`
- `vision_evidence`
- `evidence_ledger`

The builder must keep source provenance. Dataset labels, triage labels, split names, folder labels, feed labels, and teacher labels must not enter model input or evidence text.

Draft shape:

```json
{
  "structured_decision_features": {
    "schema_version": "warden_l1_structured_decision_features_v0_1",
    "url_features": {},
    "visible_text_features": {},
    "html_actionable_features": {},
    "form_features": {},
    "network_features": {},
    "rule_router": {},
    "text_semantic_concepts": {},
    "vision_evidence": {},
    "evidence_ledger_refs": []
  }
}
```

## 7. L1 Decision Head Contract

The L1 Decision Head is the future component that owns the L1 final decision.

It consumes:

- text semantic concept outputs;
- claimed identity candidates;
- relation judgment outputs;
- URL/domain features;
- actionable HTML features;
- forms/network features;
- rule router diagnostics;
- OCR text evidence if available;
- YOLO UI-component evidence if available;
- evidence ledger references.

It may be implemented later with XGBoost or another lightweight decision head. This document does not implement it.

Decision Head concept inputs should follow `docs/l1/WARDEN_L1_TEXT_SEMANTIC_CONCEPTS_V1.md`. The text tower supplies concepts and relation judgments; it does not own the final decision.

Current draft stub:

```json
{
  "decision_head": {
    "status": "not_run",
    "reason": "real_text_tower_and_l1_decision_head_not_available_yet",
    "final_label": null,
    "risk_score": null,
    "confidence": null,
    "malicious_basis": null,
    "payload_observed": null
  }
}
```

Future Decision Head output:

```json
{
  "decision_head": {
    "status": "ran",
    "head_type": "xgb_or_lightweight_decision_head",
    "model_id": "future_l1_decision_head_v1",
    "final_label": "suspicious",
    "malicious_basis": "insufficient_evidence",
    "payload_observed": "unknown",
    "page_role": "unknown",
    "risk_score": 0.62,
    "confidence": 0.58,
    "routing": "need_review",
    "top_contributors": [
      {
        "feature": "rule_router.evidence_sufficiency.visible_text_status",
        "value": "sparse",
        "direction": "limits_confidence",
        "evidence_ids": []
      }
    ],
    "reason_codes": [
      "insufficient_evidence",
      "need_review"
    ]
  }
}
```

Allowed future `final_label` values:

```text
benign
malicious
suspicious
unknown
```

Allowed future `malicious_basis` values:

```text
no_malicious_evidence_observed
high_risk_behavior_observed
high_risk_action_observed
both_behavior_and_action_observed
insufficient_evidence
```

Allowed future `payload_observed` values:

```text
true
false
unknown
```

Allowed future `routing` values:

```text
stop
need_review
need_human_review
```

`risk_score` and `confidence` are floats from `0.0` to `1.0`.

These future Decision Head fields are draft terms. They are not currently emitted as official runtime schema.

## 8. Evidence Renderer Contract

The Evidence Renderer must render deterministic explanations from:

- evidence ledger;
- reason codes;
- rule router diagnostics;
- text semantic concepts;
- visual evidence;
- Decision Head output when `decision_head.status = ran`.

When `decision_head.status = not_run`, the renderer must produce routing diagnostics only and must not claim final malicious or benign judgment.

Draft current explanation:

```json
{
  "explanation": {
    "type": "routing_diagnostic",
    "summary": "Rule router produced routing diagnostics only.",
    "positive_evidence": [],
    "limiting_evidence": [],
    "uncertainty": [],
    "routing_explanation": "Follow-up routing requested: need_text_tower"
  }
}
```

Future decision explanation:

```json
{
  "explanation": {
    "type": "decision_explanation",
    "summary": "Decision Head selected suspicious because evidence is incomplete and review is required.",
    "positive_evidence": [],
    "limiting_evidence": [],
    "uncertainty": [],
    "routing_explanation": "Decision Head requested review.",
    "decision_head_status": "ran"
  }
}
```

## 9. Distillation And Training Alignment

Future teacher distillation should target bounded concepts, relation judgments, risk axes, and page-role candidates.

Recommended target families:

- action surfaces
- behavior contexts
- relation consistency
- risk axes
- page role candidates
- routing recommendations

Teacher outputs must be converted into structured fields before training. Free-form rationales should not become model outputs. If teacher labels are used, they must stay separate from manual gold labels and dataset-management metadata.

Decision Head training should consume structured features and concept outputs, not raw chain-of-thought.

## 10. Compatibility Statement

This document changes documentation only.

It does not:

- train models;
- run teacher distillation;
- run OCR;
- run YOLO / detector;
- run CLIP / MobileCLIP;
- run SNet / SpecularNet-like models;
- modify runtime behavior;
- modify official runtime result schema;
- modify official runtime trace schema;
- modify labels;
- modify manifests;
- modify data splits;
- modify sample files;
- freeze final L1 output schema.

The official runtime schema remains unchanged. The current L1 draft sidecar remains `draft=true` and `not_final_schema=true`.

## 11. Validation Checklist

For this documentation contract:

- task doc should pass `scripts/ci/check_task_doc.py`;
- handoff should pass `scripts/ci/check_handoff_doc.py`;
- this contract should contain required terms:
  - `Rule Router`
  - `Decision Head`
  - `text_semantic_concepts`
  - `vision_evidence`
  - `action surface != threat action`
  - `not final schema`
  - `not_run`

## 12. Future Work

Recommended follow-up tasks:

- define text semantic concept training targets;
- define teacher distillation data format;
- define Decision Head training data and evaluation split rules;
- implement a structured feature builder for Decision Head input;
- train and validate the future Decision Head;
- freeze final L1 output schema only after model and runtime validation.
