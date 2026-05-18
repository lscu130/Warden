# WARDEN_DISTILLATION_WORKFLOW_V0.3

## 中文版

### 摘要

本文档定义 Warden distillation V0.3 的公式对齐工作流。V0.3 在当前 Warden V1 语义下 supersede V0.2：V0.2 的 JSON-only、非 chain-of-thought、非 gold、train-only、val/test diagnostic-only、视觉证据恢复等安全原则继续保留；威胁语义从宽泛的“恶意感”收缩到 V1 公式。

核心公式：

```text
Web-SE Threat := EvidenceSufficient(
  ManipulativeContext ∧ RiskBearingEngagement
)

RiskBearingEngagement :=
  DirectHighRiskAction
  ∨ RoutedHighRiskAction
  ∨ ActionPreparation
  ∨ DeceptiveFunnelPriming
```

当前离线实验默认链路是：

```text
Processed Valid Dataset -> Evidence Pack Builder -> L1
```

`rule_router_context` 仅作为 legacy optional 兼容字段，不是 label source、teacher label source 或 final judgment。V0.3 默认 teacher-visible context 应来自 Evidence Pack Builder 的 `pre_l1_context`，且只表达 evidence availability。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Workflow V0.3

## 1. Status And Supersession

V0.3 supersedes V0.2 for current Warden V1 formula semantics.

V0.2 remains a historical and compatibility reference for safe distillation principles:

- JSON-only output;
- no hidden chain-of-thought;
- concise evidence quotes only;
- weak labels are evidence, not gold labels;
- payload not observed is not automatic benign;
- unknown relation is not malicious;
- text-only fallback must not claim screenshot-pixel inspection;
- OCR / YOLO are conditional evidence recovery only;
- visual evidence is not a standalone malicious / benign classifier;
- official teacher distillation is train split only by default;
- val/test teacher output is diagnostic-only and must not be used for training, prompt tuning, threshold selection, model selection, acceptance metrics, or final claims.

This document is documentation only. It does not modify runner implementation, model API calls, training ingestion, runtime schemas, label enums, manifests, datasets, or JSON/YAML production contracts.

## 2. Formula-Aligned Objective

Teacher outputs must align to the Warden V1 threat formula:

```text
Web-SE Threat := EvidenceSufficient(
  ManipulativeContext ∧ RiskBearingEngagement
)

RiskBearingEngagement :=
  DirectHighRiskAction
  ∨ RoutedHighRiskAction
  ∨ ActionPreparation
  ∨ DeceptiveFunnelPriming
```

The teacher must not teach a broad "malicious-looking page" target. It must teach whether observable evidence supports:

- `ManipulativeContext`;
- `RiskBearingEngagement`;
- `DirectHighRiskAction`;
- `RoutedHighRiskAction`;
- `ActionPreparation`;
- `DeceptiveFunnelPriming`;
- the evidence-supported relation between context and risk-bearing engagement;
- evidence sufficiency for the formula.

## 3. Required Teacher Target Groups

V0.3 teacher outputs must include these primary concept groups:

```json
{
  "manipulative_context": {
    "present": "boolean",
    "context_types": [],
    "evidence_quotes": [],
    "confidence": "number"
  },
  "action_surface": {
    "present": "boolean",
    "surface_types": [],
    "evidence_quotes": [],
    "not_threat_by_itself": true
  },
  "risk_bearing_engagement": {
    "present": "boolean",
    "direct_high_risk_action": {},
    "routed_high_risk_action": {},
    "action_preparation": {},
    "deceptive_funnel_priming": {},
    "evidence_quotes": [],
    "confidence": "number",
    "action_surface_is_not_automatically_risk_bearing_engagement": true
  },
  "induced_high_risk_action": {
    "compatibility_only": true,
    "use_risk_bearing_engagement_instead": true
  },
  "context_engagement_relation": {
    "relation_supported": "boolean",
    "relation_type": "context_supports_risk_bearing_engagement | relation_unclear | no_relation_observed",
    "evidence_quotes": [],
    "unknown_relation_is_not_malicious": true
  },
  "url_claim_analysis": {
    "url_only_brand_claim_is_not_v1_positive": true
  },
  "visible_impersonation_analysis": {
    "visible_impersonation_without_funnel_affordance_is_not_strong_positive": true
  },
  "funnel_affordance_analysis": {
    "visible_impersonation_with_funnel_affordance_may_support_engagement": true
  },
  "risk_outcome_axes": {
    "credential_or_sensitive_disclosure": "boolean",
    "payment_or_wallet_authorization": "boolean",
    "download_or_installation": "boolean",
    "support_contact_or_recovery_flow": "boolean"
  },
  "evidence_sufficiency": {
    "sufficient_for_web_se_threat": "boolean",
    "missing_evidence": [],
    "conflicts": [],
    "confidence": "number"
  },
  "formula_result": {
    "web_se_threat_formula_satisfied": "boolean",
    "formula_basis": "string"
  }
}
```

Compatibility fields such as `claimed_identity_candidates`, `identity_claim`, `behavior_context`, `relation_judgments`, `evidence_state`, `threat_action_candidate`, `induced_high_risk_action`, and `decision_head_auxiliary_targets` may remain, but they must map into the V0.3 formula groups rather than define a separate broad-maliciousness target. `induced_high_risk_action` is compatibility / child concept only and must not be used as the second top-level formula term.

## 4. Action Surface Discipline

Required rule:

```text
action_surface != risk_bearing_engagement
```

`action_surface` means that a page contains an interaction surface such as a login form, payment button, download button, wallet-connect button, support contact route, PII form, OTP field, account recovery flow, QR code, or similar interaction element.

An action surface is not risk-bearing engagement by itself. It may enter `risk_bearing_engagement` only when observable evidence supports direct high-risk action, routed high-risk action, action preparation, or deceptive funnel priming.

Additional boundaries:

- URL-only brand claim is not sufficient for a V1 positive.
- Visible impersonation without a funnel affordance is not a strong positive by itself.
- Visible impersonation with a funnel affordance may support `DeceptiveFunnelPriming`, `RoutedHighRiskAction`, or `ActionPreparation`.

Calibration examples:

| Scenario | V0.3 treatment |
| --- | --- |
| Domain contains a bank brand string but page has no observable brand UI, action surface, or funnel | `url_claim_only_insufficient_page_evidence`; not V1 positive |
| Page visibly mimics a service logo but offers no login, routing CTA, form, support route, payment, wallet, download, or recovery path | `visible_impersonation_without_funnel_affordance`; not strong positive |
| Page visibly mimics an account-security portal and shows a continue / verify CTA that routes toward login or recovery | Candidate `DeceptiveFunnelPriming` or `RoutedHighRiskAction`; review relation evidence |
| Page uses urgency / account-lock language plus credential, payment, wallet, PII, download, or support-contact affordance | Candidate `RiskBearingEngagement`; formula still requires sufficient `ManipulativeContext` |

## 5. Rule Router And Pre-L1 Context

The current Warden V1 offline experiment path is:

```text
Processed Valid Dataset -> Evidence Pack Builder -> L1
```

Therefore `rule_router_context` is not a default V1 distillation teacher-visible input.

If retained for backward compatibility, `rule_router_context` must be marked:

```text
legacy_optional
not_a_label_source
not_a_teacher_label_source
not_final_judgment
```

Preferred V0.3 context field:

```json
{
  "pre_l1_context": {
    "source": "evidence_pack_builder",
    "scope": "evidence_availability_only",
    "not_a_label_source": true
  }
}
```

Weak labels, directory names, split metadata, human gold labels, and legacy router output must not be included as teacher-visible evidence unless the prompt is explicitly diagnostic-only.

## 6. V1 Out-Of-Scope Rule

Warden V1 excludes adult-content-only, gambling-content-only, guns/drugs/high-risk-content-only, gate-only, CAPTCHA-only, challenge-only, evasion-only, cloaking-only, redirect-only, and trusted-sink-only samples from the main training target.

If such content is observed without downstream observable evidence satisfying the V1 Web-SE formula, do not classify it as Web-SE threat. Mark:

```json
{
  "out_of_v1_scope_candidate": true,
  "do_not_train_as_gold": true,
  "needs_human_review": true
}
```

These values are diagnostic / review routing signals, not gold labels and not training targets.

## 7. QC Flags

V0.3 deprecates normal use of `possible_cloak_or_gate` as a V1 assessment flag.

Use precise diagnostic / out-of-scope flags instead:

```text
out_of_v1_scope_candidate
gate_or_evasion_excluded_v1
redirect_only_excluded_v1
regulated_content_only_excluded_v1
formula_relation_unclear
action_surface_without_risk_bearing_engagement
manipulative_context_only
risk_bearing_engagement_unclear
downstream_risk_unclear
evidence_sufficiency_low
```

These flags are not gold labels and not direct training targets.

## 8. Decision Head Advisory Targets

V0.3 advisory basis values:

```text
no_web_se_evidence_observed
manipulative_context_only
action_surface_only
risk_bearing_engagement_observed
manipulative_context_and_risk_bearing_engagement_observed
web_se_formula_satisfied
url_claim_only
visible_impersonation_without_funnel_affordance
out_of_v1_scope
insufficient_evidence
```

Only `web_se_formula_satisfied` can be a future safe training-target candidate, and even that remains advisory until a separate approved training-ingestion task consumes it.

Training-target language may allow only:

```text
benign
malicious
```

Diagnostic-only values may include:

```text
unknown_diagnostic_only
out_of_v1_scope_diagnostic_only
```

Any diagnostic-only value must set:

```json
{
  "do_not_train_as_gold": true,
  "diagnostic_only": true
}
```

`suspicious` is not a V1 training target in V0.3.

## 9. OCR / YOLO / CLIP Discipline

OCR / YOLO are conditional evidence recovery primitives only. They may support:

- `manipulative_context`;
- `risk_bearing_engagement`;
- `context_engagement_relation`;
- `evidence_sufficiency`.

They must not emit:

```json
{
  "visual_malicious": true
}
```

CLIP / MobileCLIP / SNet / SpecularNet-like paths are outside the V1 default distillation path. They may be discussed only as separate future, auxiliary, clustering, ablation, or research-only work.

## 10. Split Safety

Official teacher distillation remains train-only by default.

Val/test teacher outputs are diagnostic-only. They must not be used for:

- training;
- prompt tuning;
- threshold selection;
- model selection;
- final metrics;
- acceptance claims.

Before final dataset freeze, all pilot outputs must set `do_not_train_as_gold=true`.

## 11. Review Queue Reasons

V0.3 review queue reason taxonomy should include:

```text
url_claim_only_insufficient_page_evidence
visible_impersonation_without_funnel_affordance
visible_impersonation_with_funnel_affordance
deceptive_funnel_priming_candidate
risk_bearing_engagement_unclear
downstream_risk_unclear
action_surface_without_risk_bearing_engagement
formula_relation_unclear
evidence_sufficiency_low
visual_text_conflict
fallback_modality_loss
out_of_v1_scope_candidate
gate_or_evasion_excluded_v1
redirect_only_excluded_v1
teacher_human_label_conflict
schema_or_grounding_failure
```

## 12. Stop Conditions

Stop after V0.3 documentation and prompt templates define formula-aligned teacher targets and validation confirms no runtime, schema, training, data, model-call, OCR, YOLO, CLIP, or evaluation work was performed.

## 13. Record Contract And Adapter-Readiness Baseline

The current V0.3 mock record contract is a no-network adapter-readiness baseline only. It can support a future small live-provider pilot approval task because it records:

- sample and evidence provenance;
- teacher and prompt provenance;
- modality guard status;
- prompt snapshot placeholder path;
- raw output placeholder path;
- repair and validation status;
- token, cost, latency, provider request, failure, retry, and rollback placeholders;
- attempt, validation, audit, report, and review-queue links.

It is not sufficient to claim:

- live real-teacher adapter approval;
- training-ingestion approval;
- teacher quality validation;
- large-scale distillation readiness;
- provider budget or network approval.

Allowed conclusion:

```text
V0.3 mock record contract has been reviewed and adapter-readiness fields are present.
No-network dry-run readiness checks passed.
The system is ready for a separate live-provider pilot approval task.
```
