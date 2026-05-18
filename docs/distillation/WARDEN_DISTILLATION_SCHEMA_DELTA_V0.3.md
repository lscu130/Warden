# WARDEN_DISTILLATION_SCHEMA_DELTA_V0.3

## 中文版

### 摘要

本文档是 documentation-only schema delta。它不修改 official runtime schema、label enum、JSON/YAML 输出合同或训练 ingestion。它只说明 V0.3 distillation teacher output 相对 V0.2 的公式对齐字段。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Schema Delta V0.3

## 1. Status

This is a documentation-only schema delta for distillation teacher outputs.

It does not modify:

- official Warden runtime schema;
- label enums;
- manifest fields;
- JSON/YAML production output contracts;
- training ingestion code;
- inference/runtime code.

## 2. Formula

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

## 3. New Primary Formula Groups

V0.3 adds or promotes:

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

## 4. Compatibility Mapping

V0.2 field | V0.3 treatment
--- | ---
`rule_router_context` | `legacy_optional`, `not_a_label_source`, `not_a_teacher_label_source`, `not_final_judgment`
`threat_action_candidate` | compatibility alias only; map to `risk_bearing_engagement`
`induced_high_risk_action` | compatibility / child concept only; not the second top-level formula term
`behavior_context` | map into `manipulative_context`
`relation_judgments` | map into `context_engagement_relation`
`evidence_state` | map into `evidence_sufficiency`
`vision_evidence_observations` | conditional evidence recovery only
`decision_head_auxiliary_targets` | advisory only, non-gold

Required invariant:

```text
action_surface != risk_bearing_engagement
```

Boundary rules:

- URL-only brand claim is not sufficient for V1 positive.
- Visible impersonation without funnel affordance is not a strong positive.
- Visible impersonation with funnel affordance may support `DeceptiveFunnelPriming`, `RoutedHighRiskAction`, or `ActionPreparation`.

## 5. Evidence Pack Visibility

Teacher-visible:

```json
{
  "teacher_visible_evidence": {},
  "teacher_visible_context": {
    "v1_scope": "observable_web_se_threat",
    "threat_formula": "EvidenceSufficient(ManipulativeContext AND RiskBearingEngagement)"
  },
  "pre_l1_context": {
    "source": "evidence_pack_builder",
    "scope": "evidence_availability_only",
    "not_a_label_source": true
  }
}
```

Not teacher-visible by default:

```json
{
  "metadata_not_for_prompt": {
    "weak_label": "...",
    "legacy_router_output": "...",
    "split": "...",
    "source_manifest": "...",
    "human_gold_label": "..."
  }
}
```

## 6. Advisory Values

Replace or extend `malicious_basis_advisory` with:

```text
no_web_se_evidence_observed
manipulative_context_only
action_surface_only
risk_bearing_engagement_observed
manipulative_context_and_risk_bearing_engagement_observed
url_claim_only
visible_impersonation_without_funnel_affordance
web_se_formula_satisfied
out_of_v1_scope
insufficient_evidence
```

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

Diagnostic-only values must set:

```json
{
  "do_not_train_as_gold": true,
  "diagnostic_only": true
}
```

`suspicious` is not a V1 training target.

## 7. QC And Review Reasons

V0.3 flags:

```text
out_of_v1_scope_candidate
gate_or_evasion_excluded_v1
redirect_only_excluded_v1
regulated_content_only_excluded_v1
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
teacher_human_label_conflict
schema_or_grounding_failure
```

`possible_cloak_or_gate` is deprecated for normal V1 assessment.

## 8. Out-Of-Scope Values

Adult-content-only, gambling-content-only, guns/drugs/high-risk-content-only, gate-only, CAPTCHA-only, challenge-only, evasion-only, cloaking-only, redirect-only, and trusted-sink-only samples must not become Web-SE threats unless downstream observable evidence satisfies the formula.

Use:

```json
{
  "out_of_v1_scope_candidate": true,
  "do_not_train_as_gold": true,
  "needs_human_review": true
}
```

## 9. Record Contract Review And Adapter-Readiness Fields

Current `warden_distill_v0.3_mock` records are a candidate no-network record contract baseline for a future small live-provider pilot. They are sufficient for adapter dry-run readiness when they include:

- stable sample provenance: `sample_key`, `sample_id`, `source_manifest`, `source_split`, `source_url`, `canonical_url`, `capture_id`, `evidence_pack_id`;
- teacher provenance: `teacher_provider`, `teacher_model`, `teacher_role`, `teacher_profile`, `teacher_run_id`;
- prompt provenance: `prompt_template_id`, `prompt_template_version`, `prompt_snapshot_path`;
- modality guard fields: `image_input_expected`, `image_input_passed_to_teacher`, `image_input_policy`, `modality_guard_status`, `visual_evidence_source`;
- raw / repair / validation placeholders: `raw_output_path`, `repaired_output_path`, `validation_status`, `validation_errors`;
- attempt audit fields: `attempt_id`, `attempt_index`, `attempt_status`, `repair_attempted`, `repair_reason`;
- cost / provider placeholders: `token_usage_placeholder`, `cost_placeholder`, `latency_ms_placeholder`, `provider_request_id_placeholder`;
- failure and rollback fields: `failure_category`, `retry_allowed`, `rollback_required`.

All fields above are readiness / audit placeholders in mock mode. They must not trigger real provider calls and must not be treated as training gold labels.

Mock-only fields:

- `teacher_provider = mock`;
- `teacher_model = mock_teacher_v0`;
- `image_input_expected = false`;
- `image_input_passed_to_teacher = false`;
- `modality_guard_status = mock_no_image_input`;
- `raw_output_path` points to a placeholder file, not a provider response;
- `repaired_output_path = null` unless a later repair task explicitly creates one;
- `token_usage_placeholder` and `cost_placeholder` contain no real token or billing data.

Fields that must never authorize training ingestion by themselves:

- `decision_head_auxiliary_targets`;
- `review_reasons`;
- `formula_result`;
- `risk_score_hint`;
- `confidence_hint`;
- any mock-only teacher advisory or adapter-readiness placeholder.

## 10. Output Layout For No-Network Adapter Readiness

A compliant mock readiness run should write:

```text
distillation_records.jsonl
review_queue.jsonl
attempts.jsonl
validation_summaries.jsonl
run_audit.json
run_report.md
adapter_readiness_report.md
errors.jsonl
prompt_snapshots/
raw_outputs/
repaired_outputs/
```

Required readiness status values:

```text
adapter_readiness_status = ready_for_no_network_dry_run
live_teacher_readiness = not_ready_for_live_teacher
```

Do not output or imply `ready_for_live_teacher=true`.
