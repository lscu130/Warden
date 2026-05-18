# WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1_ADDENDUM_V1_SCOPE

## 中文版

### 摘要

本文档是 runner design V0.1 的 V1 scope addendum。它不修改 runner 实现，只补充 V0.3 distillation 所需的 Evidence Pack 可见性、`rule_router_context` 降级、V1 out-of-scope、OCR / YOLO / CLIP 边界和 split safety 规则。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Runner Design V0.1 Addendum: V1 Scope

## 1. Status

This addendum updates the documentation contract for V0.3 formula-aligned distillation.

It does not implement a runner, call teacher models, run OCR / YOLO / CLIP, change schemas, alter manifests, or modify training/runtime code.

## 2. Current Offline Path

Current Warden V1 offline experiment path:

```text
Processed Valid Dataset -> Evidence Pack Builder -> L1
```

The future online / wild-test path remains:

```text
Raw URL -> Capture Pipeline -> Capture QA / V1 Scope Admission -> Evidence Pack Builder -> L1
```

L0 is not part of the current V1 offline distillation default path.

## 3. Formula

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ RiskBearingEngagement)

RiskBearingEngagement := DirectHighRiskAction ∨ RoutedHighRiskAction ∨ ActionPreparation ∨ DeceptiveFunnelPriming
```

The runner's prompt packet builder should support formula-aligned teacher-visible evidence, but this addendum does not implement that builder.

## 4. Evidence Pack Visibility

Prompt packets should distinguish:

```json
{
  "teacher_visible_evidence": {},
  "teacher_visible_context": {
    "v1_scope": "observable_web_se_threat",
    "threat_formula": "EvidenceSufficient(ManipulativeContext AND RiskBearingEngagement)"
  },
  "metadata_not_for_prompt": {
    "weak_label": "...",
    "legacy_router_output": "...",
    "split": "...",
    "source_manifest": "...",
    "human_gold_label": "..."
  }
}
```

Weak labels, directory names, split metadata, human gold labels, and legacy router outputs must not be teacher-visible prompt input by default.

Boundary hints are teacher-visible only as formula discipline:

- URL-only brand claim is not sufficient for V1 positive.
- Visible impersonation without funnel affordance is not a strong positive.
- Visible impersonation with funnel affordance may support `DeceptiveFunnelPriming`, `RoutedHighRiskAction`, or `ActionPreparation`.

## 5. Router Context

`rule_router_context` is legacy optional and must be marked:

```text
legacy_optional
not_a_label_source
not_a_teacher_label_source
not_final_judgment
```

Preferred V0.3 context:

```json
{
  "pre_l1_context": {
    "source": "evidence_pack_builder",
    "scope": "evidence_availability_only",
    "not_a_label_source": true
  }
}
```

## 6. V1 Out-Of-Scope Handling

Adult-content-only, gambling-content-only, guns/drugs/high-risk-content-only, gate-only, CAPTCHA-only, challenge-only, evasion-only, cloaking-only, redirect-only, and trusted-sink-only samples are not V1 main training targets unless downstream observable evidence satisfies the formula.

Use diagnostic flags:

```text
out_of_v1_scope_candidate
gate_or_evasion_excluded_v1
redirect_only_excluded_v1
regulated_content_only_excluded_v1
```

Set `do_not_train_as_gold=true` and `needs_human_review=true`.

## 7. OCR / YOLO / CLIP

OCR and YOLO remain conditional evidence recovery only. They may support formula evidence groups but must not emit standalone malicious / benign classification.

CLIP / MobileCLIP / SNet / SpecularNet-like paths are outside the V1 default distillation path and require separate future or auxiliary tasks.

## 8. Split Safety

Official teacher distillation remains train-only by default.

Val/test outputs are diagnostic-only and must not be used for training, prompt tuning, threshold selection, model selection, final metrics, or acceptance claims.

## 9. No-Network Adapter-Readiness Layout

The mock runner may prepare real-teacher adapter readiness placeholders, but it must not call any provider. A no-network readiness run should create:

```text
attempts.jsonl
validation_summaries.jsonl
prompt_snapshots/
raw_outputs/
repaired_outputs/
adapter_readiness_report.md
```

Each attempt / validation record must make the mock boundary explicit:

```json
{
  "mock_only": true,
  "real_teacher_call": false,
  "external_api_call": false,
  "repair_attempted": false,
  "validation_status": "passed"
}
```

`raw_outputs/` contains placeholder raw-output files only. It must not contain real provider responses in this task class.

Required audit status:

```text
adapter_readiness_status = ready_for_no_network_dry_run
live_teacher_readiness = not_ready_for_live_teacher
```

The addendum does not approve live teacher calls, provider billing, training ingestion, model evaluation, or production runtime schema changes.
