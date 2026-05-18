# Warden L1 Text Semantic Concepts And Relation Judgments V1

## 中文版

> 面向 AI 的说明：英文版为权威执行规范。中文部分用于项目负责人快速确认任务边界和目标。

## 0. 中文摘要

本文档定义 Warden L1 文本塔未来要学习的结构化语义概念和证据关系判断。它不是训练任务、不是代码实现、不是 final schema freeze。

核心分工：

```text
结构化提取负责找出候选证据；
文本塔负责理解语义概念与证据关系；
视觉端只负责 OCR / YOLO 补证据；
Decision Head 负责把概念 + 结构化证据转成 L1 final decision。
```

硬规则：

- `claimed_identity_candidates` 只是候选，不是最终冒充判断。
- 品牌库只是 optional enhancement，不是主路径。
- `action surface != threat action`。
- `payload not observed != automatic benign`。
- V1 malicious 需要同时满足 `ManipulativeContext` 与 `InducedHighRiskAction` 的充分证据。
- `unknown relation is not malicious`。
- Rule Router 不是 classifier。
- Text tower 不拥有 final decision。
- 本文所有 JSON 示例都是 draft / conceptual，不是 official runtime schema。

## English Version

> AI note: This English section is authoritative. This document is a documentation contract only. It does not change runtime behavior, labels, official schemas, manifests, splits, samples, training code, inference code, or distillation runner behavior.

# Warden L1 Text Semantic Concepts And Relation Judgments V1

## 1. Purpose

This document defines Warden's draft L1 text semantic concept and relation judgment contract.

It specifies what a future small BERT-like / encoder-based text tower should learn as structured intermediate targets, and how those targets should feed the future L1 Decision Head.

This document is a draft contract for:

- teacher prompt / distillation target design;
- future text tower multi-task heads;
- Decision Head input design;
- concept-level evaluation;
- L1 error analysis;
- future schema-freeze discussion.

It is not:

- an implementation task;
- a model-training task;
- a teacher-distillation run;
- a final runtime schema;
- a label-enum change.

## 2. Responsibility Split

Warden L1 uses this responsibility split:

```text
Structured extraction finds candidate evidence.
Text tower models semantic concepts and evidence relations.
Vision path recovers OCR / YOLO evidence only.
Decision Head combines concepts + structured evidence into the L1 final decision.
```

The text tower must not output hidden chain-of-thought and must not own final L1 decision semantics.

## 3. Claimed Identity Candidate Extraction

`claimed_identity_candidates` is a structured evidence-preparation layer.

It finds possible claimed identities. It does not decide impersonation, does not prove brand abuse, and does not require a closed brand library.

Candidate sources include:

- `title`;
- h1 / h2 / heading;
- meta title / meta description;
- `visible_text` beginning / prominent text;
- logo `alt`, image `alt`, `aria-label`;
- copyright / footer;
- form legend / button text / input labels;
- URL subdomain / path tokens;
- OCR text if L1 vision is triggered later.

Draft candidate shape:

```json
{
  "claimed_identity_candidates": [
    {
      "raw_name": "ExampleBank",
      "normalized_name": "examplebank",
      "source_fields": ["title", "h1", "url_path"],
      "source_count": 3,
      "surface_confidence": 0.72,
      "notes": "candidate only; not final brand judgment"
    }
  ]
}
```

Hard rules:

- Candidate extraction only finds possible claimed identities.
- It must not decide impersonation.
- It must not require a closed brand library.
- A brand library may be optional enhancement, not the primary path.

## 4. `text_semantic_concepts` Top-Level Shape

The future text tower should emit bounded concept groups, not free-form reasoning and not a final label.

Draft conceptual shape:

```json
{
  "text_semantic_concepts": {
    "status": "ran",
    "schema_version": "warden_l1_text_semantic_concepts_v1_draft",
    "claimed_identity_candidates": [],
    "identity_claim_concepts": {},
    "action_surface_concepts": {},
    "behavior_context_concepts": {},
    "relation_judgments": {},
    "evidence_state_concepts": {},
    "threat_action_candidate_concepts": {},
    "concept_level_evidence_ids": []
  }
}
```

This shape is draft / conceptual. It is not official runtime schema.

## 5. Identity Claim Concepts

Identity claim concepts judge whether a candidate is an actual self-claimed identity.

Required targets:

- `claimed_identity_present`;
- `claimed_identity_strength`: `none | weak | medium | strong`;
- `claimed_identity_type`: `financial_service | exchange | wallet | saas | government | education | ecommerce | support_service | media | unknown`;
- `claim_source_type`: `title | heading | visible_text | url | meta | footer | ocr | html_attr | mixed`;
- `self_claim_vs_reference`: `self_claim | reference_or_news | third_party_login | ad_or_link | footer_only | unknown`.

Draft shape:

```json
{
  "identity_claim_concepts": {
    "claimed_identity_present": true,
    "claimed_identity_strength": "strong",
    "claimed_identity_type": "financial_service",
    "claim_source_type": "mixed",
    "self_claim_vs_reference": "self_claim",
    "evidence_ids": ["txt_001", "url_001"]
  }
}
```

## 6. Action Surface Concepts

Action surfaces are interactive or user-action-related surfaces. They are not threat actions by themselves.

Required targets:

- `login_surface`;
- `otp_mfa_surface`;
- `payment_surface`;
- `wallet_connect_surface`;
- `seed_private_key_surface`;
- `download_surface`;
- `support_contact_surface`;
- `kyc_pii_surface`;
- `qr_code_surface`;
- `third_party_redirect_surface`.

Hard rule:

```text
action surface != threat action
```

A normal login, download, payment, KYC, support, or wallet page may be a benign hard negative when business context supports it.

Draft shape:

```json
{
  "action_surface_concepts": {
    "login_surface": {"present": true, "confidence": 0.86, "evidence_ids": ["form_001"]},
    "download_surface": {"present": false, "confidence": 0.04, "evidence_ids": []}
  }
}
```

## 7. Behavior Context Concepts

Behavior context concepts identify high-risk deceptive, manipulative, or abnormal framing.

Required targets:

- `identity_impersonation_context`;
- `authority_impersonation_context`;
- `fake_security_context`;
- `account_problem_or_lock_context`;
- `fake_support_context`;
- `reward_or_claim_context`;
- `airdrop_or_giveaway_context`;
- `fake_update_context`;
- `investment_or_profit_lure_context`;
- `urgency_or_pressure_context`;
- `bypass_normal_process_context`;
- `business_legitimacy_weak_context`.

Draft shape:

```json
{
  "behavior_context_concepts": {
    "fake_security_context": {"present": true, "confidence": 0.78, "evidence_ids": ["txt_004"]},
    "urgency_or_pressure_context": {"present": true, "confidence": 0.64, "evidence_ids": ["txt_005"]}
  }
}
```

## 8. Relation Judgment Concepts

Relation judgments connect evidence pieces. This is the core bridge between structured extraction and final adjudication.

Required relation targets:

| target | allowed values |
|---|---|
| `identity_domain_relation` | `aligned | weakly_aligned | conflict_candidate | unknown` |
| `identity_url_relation` | `aligned | suspicious_modifier | conflict_candidate | unknown` |
| `identity_action_relation` | `business_consistent | sensitive_but_plausible | suspicious_context | unknown` |
| `action_target_relation` | `same_origin_or_expected | third_party_but_plausible | off_domain_suspicious | unknown` |
| `business_legitimacy_hint` | `supported | weak | conflict_candidate | unknown` |
| `hosted_platform_context` | `present | absent | unknown` |
| `text_html_consistency` | `consistent | partial_conflict | conflict | insufficient` |
| `url_text_consistency` | `consistent | partial_conflict | conflict | insufficient` |

Hard rule:

```text
unknown relation is not malicious.
```

Draft shape:

```json
{
  "relation_judgments": {
    "identity_domain_relation": {
      "value": "conflict_candidate",
      "confidence": 0.71,
      "evidence_ids": ["url_001", "txt_001"]
    },
    "business_legitimacy_hint": {
      "value": "weak",
      "confidence": 0.58,
      "evidence_ids": ["url_001", "net_001"]
    }
  }
}
```

Interpretation:

- `conflict_candidate` means a relation should be weighed by the Decision Head with supporting evidence. It is not a final malicious label.
- `unknown` means evidence is unavailable or inconclusive. It should not be forced into malicious or benign.
- Hosted platform context can reduce false positives when the page is plausibly a legitimate SSO, OAuth, marketplace, CDN, documentation, or app-hosted flow.

## 9. Evidence State Concepts

Evidence state concepts prevent overclaiming.

Required targets:

- `payload_observed`: `true | false | unknown`;
- `payload_type`: `credential | payment | wallet_authorization | seed_private_key | download | pii_kyc | support_contact | none | unknown`;
- `evidence_sufficiency`: `sufficient | partial | insufficient`;
- `needs_vision_evidence`: `true | false`;
- `needs_human_review`: `true | false`;
- `do_not_train_as_gold`: `true | false`.

Hard rules:

- `payload not observed` is not automatic benign.
- `evidence insufficient` should lead to `unknown / review`, not forced malicious or benign.

Draft shape:

```json
{
  "evidence_state_concepts": {
    "payload_observed": false,
    "payload_type": "none",
    "evidence_sufficiency": "partial",
    "needs_vision_evidence": true,
    "needs_human_review": true,
    "do_not_train_as_gold": true
  }
}
```

## 10. Threat Action Candidate Concepts

Threat action candidate concepts define when action surfaces may be upgraded for Decision Head consideration.

Required targets:

- `threat_action_candidate_present`;
- `threat_action_candidate_type`;
- `upgrade_reason`;
- `supporting_behavior_contexts`;
- `supporting_relation_conflicts`.

Rule:

```text
ManipulativeContext + (DirectAction or RoutedAction or ActionPreparation) + EvidenceSufficient(...)
=> Web-SE Threat candidate
```

Final decision remains owned by the Decision Head.

Draft shape:

```json
{
  "threat_action_candidate_concepts": {
    "threat_action_candidate_present": true,
    "threat_action_candidate_type": "credential_collection",
    "upgrade_reason": "login surface with strong fake security context and identity-domain conflict candidate",
    "supporting_behavior_contexts": ["fake_security_context"],
    "supporting_relation_conflicts": ["identity_domain_relation"]
  }
}
```

## 11. Decision Head Input Contract Refinement

The future L1 Decision Head should consume:

```text
text_semantic_concepts
+ claimed_identity_candidates
+ URL/domain features
+ actionable HTML features
+ forms/network features
+ OCR text evidence
+ YOLO UI evidence
+ rule_router diagnostics
-> L1 final decision
```

The Decision Head must not consume raw hidden chain-of-thought.

It may consume:

- concept logits / probabilities;
- structured evidence features;
- candidate lists;
- relation judgment outputs;
- evidence sufficiency flags;
- OCR / YOLO evidence if triggered;
- Rule Router diagnostics.

It outputs future final fields, not current Rule Router fields:

- `final_label`;
- `malicious_basis`;
- `payload_observed`;
- `risk_score`;
- `confidence`;
- `reason_codes`;
- `evidence_summary`;
- `needs_review`.

These future fields remain conceptual / draft unless a later schema-freeze task explicitly promotes them.

## 12. Concept-Level Evaluation Requirements

Future training evaluation must report more than final-label metrics.

Required evaluation buckets:

- `identity_claim_head`;
- `action_surface_head`;
- `behavior_context_head`;
- `relation_consistency_head`;
- `evidence_state_head`;
- `threat_action_candidate_head`;
- `Decision Head final label`;
- `T00 false positive rate`;
- `T01 hard negative false positive rate`;
- `manipulative-context head recall`;
- `direct-action malicious recall`;
- `routed-action / action-preparation malicious recall`.

Why concept-level evaluation is required:

- to know whether errors come from concept extraction, relation judgment, or Decision Head weighting;
- to prevent small text models from learning shortcuts like `login = malicious` or `download = malicious`;
- to preserve benign hard negative control;
- to distinguish manipulative-context misses from direct-action, routed-action, and action-preparation misses.

## 13. Distillation Alignment

Teacher outputs should provide advisory targets for these concept groups:

- `claimed_identity_candidates`;
- identity claim concepts;
- action surface concepts;
- behavior context concepts;
- relation judgments;
- evidence state concepts;
- threat action candidate concepts;
- Decision Head auxiliary targets.

Teacher outputs remain advisory and must not override human gold labels. Pilot or mock outputs must keep `do_not_train_as_gold = true` when required by the distillation workflow.

## 14. Non-Goals And Compatibility

This document does not:

- train any model;
- run teacher distillation;
- call external model APIs;
- implement text tower model code;
- implement Decision Head model code;
- implement OCR / YOLO / CLIP / SNet / SpecularNet-like;
- modify runtime official schema;
- change label enums;
- move or modify samples;
- modify manifests or splits;
- change production inference behavior;
- add third-party dependencies;
- freeze final schema.

Compatibility:

- Existing runtime schemas remain unchanged.
- Existing label enums remain unchanged.
- Existing distillation schemas remain draft / advisory unless separately frozen.
- This document refines documentation and target semantics only.

## 15. Counter-Review Checklist

Before using this contract downstream, verify:

- brand-library matching is not the primary path;
- action surfaces are not equivalent to threat actions;
- Rule Router is not a classifier;
- text tower does not own final decision;
- production schema and runtime behavior remain unchanged;
- final dataset freeze or teacher API calls are not required by this contract.
