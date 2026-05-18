# WARDEN_DISTILLATION_PROMPTS_V0.3

## 中文版

### 摘要

本文档定义 Warden distillation prompt pack V0.3。V0.3 prompt 必须输出 JSON-only，不输出 hidden chain-of-thought，只给短证据摘录，并围绕 Warden V1 公式生成结构化 teacher targets。

核心公式：

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Prompt Pack V0.3

## 1. Global Prompt Contract

All Warden distillation prompts must enforce:

- JSON-only output.
- No hidden chain-of-thought disclosure.
- Concise evidence quotes only.
- No unsupported visual claims.
- `weak labels are evidence`, never gold labels.
- `payload not observed` is not automatic benign.
- `action_surface != risk_bearing_engagement`.
- `induced_high_risk_action` is compatibility / child concept only, not the second top-level formula term.
- URL-only brand claim is not a V1 positive.
- Visible impersonation without funnel affordance is not a strong positive.
- Visible impersonation with funnel affordance may satisfy `DeceptiveFunnelPriming`, `RoutedHighRiskAction`, or `ActionPreparation`.
- `unknown relation is not malicious`.
- `rule_router_context` is legacy optional context only, not a label source, not a teacher label source, and not final judgment.
- Advisory labels do not override human gold labels.
- `needs_human_review`, `do_not_train_as_gold`, and diagnostic-only safeguards are required when evidence is incomplete, out of V1 scope, or non-train.

The target documentation schema is `warden_distill_v0.3`. It is not official runtime schema.

## 2. Formula

Every V0.3 prompt must include:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

The teacher must decide whether observable evidence is sufficient for both `ManipulativeContext` and `RiskBearingEngagement`, and whether the relation between them is supported.

## 3. Teacher-Visible Evidence

Preferred teacher-visible structure:

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
  },
  "metadata_not_for_prompt": {
    "weak_label": "...",
    "legacy_router_output": "...",
    "split": "...",
    "source_manifest": "..."
  }
}
```

Weak labels, folder names, split metadata, human gold labels, and legacy router outputs are not teacher-visible prompt evidence unless the role is explicitly diagnostic-only.

## 4. Required Output Groups

Prompt templates must request:

```json
{
  "manipulative_context": {},
  "action_surface": {
    "not_threat_by_itself": true
  },
  "risk_bearing_engagement": {
    "direct_high_risk_action": {},
    "routed_high_risk_action": {},
    "action_preparation": {},
    "deceptive_funnel_priming": {},
    "action_surface_is_not_automatically_risk_bearing_engagement": true
  },
  "induced_high_risk_action": {
    "compatibility_only": true,
    "use_risk_bearing_engagement_instead": true
  },
  "context_engagement_relation": {
    "unknown_relation_is_not_malicious": true
  },
  "url_claim_analysis": {
    "url_only_brand_claim_is_not_v1_positive": true
  },
  "visible_impersonation_analysis": {
    "visible_impersonation_without_funnel_affordance_is_not_strong_positive": true
  },
  "funnel_affordance_analysis": {},
  "risk_outcome_axes": {},
  "evidence_sufficiency": {},
  "formula_result": {}
}
```

`threat_action_candidate` and `induced_high_risk_action` may remain as legacy compatibility fields only when mapped to `risk_bearing_engagement`.

## 5. Primary MLLM Teacher Prompt

Template file:

- `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`

Purpose:

- Produce the full `warden_distill_v0.3` JSON draft.
- Extract formula-aligned target groups.
- Record OCR / YOLO / screenshot evidence only when such evidence is actually provided.
- Produce Decision Head auxiliary targets as advisory, non-gold signals.

## 6. Judge Teacher Prompt

Template file:

- `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`

Purpose:

- Audit formula alignment, schema shape, evidence grounding, split safety, modality honesty, and legacy-router misuse.
- Flag action-surface overreach, context/engagement relation gaps, URL-only overreach, visible-impersonation-without-funnel overreach, out-of-V1-scope leakage, and diagnostic-only violations.

## 7. DeepSeek-V4 Fallback Prompt

Template file:

- `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`

Purpose:

- Provide text / metadata / judge / schema repair fallback with modality limits.
- Must not claim direct visual inspection unless image support is verified and image input is actually passed.

## 8. Schema Repair Prompt

Template file:

- `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`

Purpose:

- Repair JSON shape only.
- Preserve semantic content.
- Do not invent formula evidence, labels, visual observations, context-action relations, or evidence sufficiency.

## 9. Human Review Packet Prompt

Template file:

- `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`

Purpose:

- Compress evidence, conflicts, formula relation gaps, diagnostic-only reasons, and review queue reasons for manual review.

## 10. Updated QC Flags

Required V0.3 flags:

```text
needs_human_review
do_not_train_as_gold
diagnostic_only
teacher_confidence_low
fallback_modality_loss
visual_text_conflict
formula_relation_unclear
action_surface_without_risk_bearing_engagement
risk_bearing_engagement_unclear
downstream_risk_unclear
url_claim_only_insufficient_page_evidence
visible_impersonation_without_funnel_affordance
visible_impersonation_with_funnel_affordance
deceptive_funnel_priming_candidate
evidence_sufficiency_low
out_of_v1_scope_candidate
gate_or_evasion_excluded_v1
redirect_only_excluded_v1
regulated_content_only_excluded_v1
schema_or_grounding_failure
```

`possible_cloak_or_gate` is deprecated for normal V1 assessment.

## 11. Advisory Values

Use:

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

Do not use `suspicious` as a V1 training target. Diagnostic-only values must set `do_not_train_as_gold=true` and `diagnostic_only=true`.

## 12. Adapter-Readiness Prompt And Output Placeholders

Prompt templates may include no-network adapter-readiness placeholders for auditability:

```json
{
  "teacher_provider": "mock",
  "teacher_profile": "mock_v0_3_formula",
  "teacher_run_id": "...",
  "prompt_template_id": "warden_distill_v0.3.primary_mock",
  "prompt_template_version": "warden_distill_v0.3",
  "prompt_snapshot_path": "prompt_snapshots/<attempt_id>.json",
  "image_input_expected": false,
  "image_input_passed_to_teacher": false,
  "modality_guard_status": "mock_no_image_input",
  "raw_output_path": "raw_outputs/<attempt_id>.json",
  "repaired_output_path": null,
  "validation_status": "passed",
  "validation_errors": [],
  "token_usage_placeholder": {"mock_only": true},
  "cost_placeholder": {"mock_only": true},
  "provider_request_id_placeholder": null,
  "failure_category": null,
  "retry_allowed": false,
  "rollback_required": false
}
```

These fields are audit placeholders only. They do not permit provider calls, do not validate teacher quality, and do not approve training ingestion.
