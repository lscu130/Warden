# WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1

## 中文版

### 摘要

本文档定义 Warden 蒸馏 runner 的设计合同 V0.1。它只冻结未来实现必须满足的工程边界，不实现 runner，不调用模型 API，不运行 teacher distillation，不生成 teacher labels。

当前设计对齐 Warden L1：

- `rule_router` outputs are routing / evidence sufficiency diagnostics only. They are not gold labels, not teacher labels, and not final model judgments.
- `text_semantic_concepts` 是主要蒸馏目标。
- `vision_evidence` 只记录 OCR / YOLO 证据观察，不能作为视觉分类塔输出最终恶意判断。
- `decision_head_auxiliary_targets` 是未来 Decision Head advisory targets，不能覆盖 human gold label。
- `warden_distill_v0.2` 是 draft distillation-output schema，不是 official runtime schema。
- 正式蒸馏默认只处理 train split。
- val/test 只允许 `diagnostic_only=true` 的诊断性 teacher run，输出必须 `do_not_train_as_gold=true`，不得用于训练、调 prompt、阈值选择、模型选择或最终验收指标。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Runner Design V0.1

## 1. Purpose And Non-Goals

This document defines a design contract for a future Warden distillation runner. It is a draft engineering contract for later implementation.

It defines:

- future runner CLI contract;
- future Python API shape;
- input manifest contract;
- evidence pack contract;
- teacher routing and fallback policy;
- output directory layout;
- JSONL record draft;
- schema validation and schema repair policy;
- split policy and contamination prevention;
- review queue policy;
- resume and idempotency;
- logging and audit;
- pilot plan;
- future implementation checklist.

Non-goals:

- no production runner implementation;
- no model API call;
- no teacher distillation run;
- no generated teacher labels;
- no data, label, manifest, split, sample, training, inference, runtime schema, or CLI changes;
- no dependency additions;
- no schema freeze for `warden_distill_v0.2`.

## 2. Current L1 Alignment

The future runner must align with current Warden L1 semantics:

- `rule_router`: routing and evidence-sufficiency diagnostic only.
- `text_semantic_concepts`: future text-tower structured semantic concept outputs and the primary distillation target area.
- `vision_evidence`: OCR / YOLO evidence observations only, not a standalone visual classifier.
- `decision_head`: future L1 final decision component; distillation may produce `decision_head_auxiliary_targets` only as advisory non-gold targets.

Required rule-router statement:

```text
rule_router outputs are routing / evidence sufficiency diagnostics only.
They are not gold labels, not teacher labels, and not final model judgments.
```

Required evidence statements:

```text
payload not observed != benign
weak labels are evidence, not gold labels
action surface is not automatically threat action
```

`warden_distill_v0.2` remains a draft distillation-output schema. It is not official Warden runtime schema.

## 3. Runner High-Level Flow

Draft flow:

```text
run config
  -> manifest scan
  -> split policy gate
  -> per-sample evidence pack build
  -> prompt packet build
  -> teacher routing decision
  -> teacher call or dry-run prompt output
  -> JSON parse validation
  -> schema validation
  -> optional schema repair
  -> final validation
  -> JSONL output append
  -> review queue generation
  -> run manifest and summary update
```

The implementation must support a dry-run / prompt-only mode that builds prompt packets and audit metadata without calling a teacher model.

## 4. Runner CLI Contract

Draft future CLI:

```bash
python scripts/distillation/run_warden_distillation.py \
  --manifest <path-to-warden_train_manifest_v1.csv> \
  --split train \
  --output-dir <path-to-distillation-output-dir> \
  --schema-version warden_distill_v0.2 \
  --teacher-profile mimo_v2_5_primary \
  --limit <n> \
  --resume \
  --dry-run
```

Implementation may adjust names in a future approved task, but it must preserve these concepts:

- manifest input;
- split enforcement;
- output directory;
- schema version;
- teacher profile;
- resume / idempotency;
- dry run / prompt-only mode;
- bounded pilot mode;
- audit logs.

Suggested additional future flags:

```text
--diagnostic-only
--assume-split train
--prompt-template-version <version>
--judge-profile <profile>
--fallback-profile <profile>
--max-attempts <n>
--repair-json
--review-queue
--write-prompts
--seed <n>
```

`--assume-split train` must be available only in controlled pilot mode and must be logged.

## 5. Python API Contract

Draft internal API names:

```python
DistillationRunConfig
DistillationSampleRecord
DistillationEvidencePack
DistillationPromptPacket
TeacherRoutingDecision
TeacherCallRecord
DistillationOutputRecord
DistillationValidationResult
DistillationReviewQueueRecord
DistillationRunner
```

Draft responsibilities:

- `DistillationRunConfig`: immutable run-level config snapshot.
- `DistillationSampleRecord`: manifest row plus resolved sample paths and split metadata.
- `DistillationEvidencePack`: source-aware evidence prepared for prompts.
- `DistillationPromptPacket`: prompt template version, filled prompt, model role, and modality metadata.
- `TeacherRoutingDecision`: teacher profile, fallback profile, modality support, and fallback reason.
- `TeacherCallRecord`: attempt metadata, latency, token / cost estimate if available, raw response path.
- `DistillationOutputRecord`: final validated `warden_distill_v0.2` draft output.
- `DistillationValidationResult`: parse, schema, enum, modality, split, grounding, and leakage checks.
- `DistillationReviewQueueRecord`: compact review item with reasons and evidence pointers.
- `DistillationRunner`: orchestrates the above objects.

These names are draft API contract terms only. This document does not add code.

## 6. Input Manifest Contract

The future runner must read a frozen manifest and must not mutate it.

Minimum expected manifest concepts:

- sample identifier;
- current sample path;
- URL or resolved artifact path fields;
- split;
- artifact availability indicators when present;
- optional weak-label metadata.

Split handling:

- official distillation requires `--split train`;
- if the manifest row has split metadata, it must match the requested split;
- if the row lacks split metadata, the runner must fail closed;
- `--assume-split train` is allowed only for controlled pilot mode and must set `do_not_train_as_gold=true` unless a later approved task says otherwise.

Forbidden prompt input:

- no hidden ground-truth label fields;
- no val/test labels as prompt hints;
- no human folder names as evidence text;
- no `triage_label` or split metadata as model input text;
- no dataset-management labels promoted into evidence claims.

## 7. Evidence Pack Contract

The future runner must prepare a source-aware evidence pack. It should preserve source provenance and keep metadata separate from teacher-visible evidence.

Core evidence:

- URL / final URL / host / eTLD+1;
- redirect chain summary if available;
- visible text;
- title / selected DOM text;
- actionable HTML summary: forms, inputs, buttons, anchors, iframes, scripts, select, textarea, title, meta, headings;
- forms summary;
- network summary;
- screenshot path or screenshot summary if available;
- OCR / YOLO evidence only if already generated by a prior allowed step;
- weak labels and rule-router outputs as evidence only, never gold.

Evidence pack fields should distinguish:

- `teacher_visible_evidence`;
- `routing_context`;
- `metadata_not_for_prompt`;
- `human_label_for_audit_only`;
- `artifact_paths`;
- `missing_artifacts`.

The runner must not run OCR or YOLO as part of this design unless a future implementation task explicitly allows that step.

## 8. Teacher Routing And Fallback Policy

Draft profiles:

- primary teacher profile: MiMo-V2.5 family when available;
- judge / audit teacher profile: MiMo-V2.5-Pro when available;
- fallback teacher profile: DeepSeek-V4 family within verified modality limits.

DeepSeek-V4 fallback policy:

```text
DeepSeek-V4 fallback is allowed for text / metadata / judge / schema repair roles.
It must not claim direct visual inspection unless the configured endpoint is verified to support image input and image input is actually passed.
```

Every output record must include:

- `teacher_model`;
- `teacher_role`;
- `teacher_profile`;
- `input_modalities`;
- `fallback_reason`;
- `schema_version`;
- `teacher_run_id`;
- `prompt_template_version`;
- `image_input_passed_to_teacher`.

Fallback reasons should include:

- `primary_quota_exhausted`;
- `primary_unavailable`;
- `primary_timeout`;
- `primary_schema_failure`;
- `modality_not_supported`;
- `manual_fallback_requested`;
- `dry_run_no_teacher_call`.

## 9. Output Directory Layout

Draft layout:

```text
<output-dir>/
  distillation_run_manifest.json
  distillation_summary.md
  distillation_outputs.jsonl
  distillation_errors.jsonl
  distillation_attempts.jsonl
  distillation_review_queue.jsonl
  prompts/
    <sample_key>.primary.prompt.json
    <sample_key>.judge.prompt.json
  raw_teacher_outputs/
    <sample_key>.<attempt>.raw.txt
  repairs/
    <sample_key>.<attempt>.repair.json
  audit/
    config_snapshot.json
    prompt_template_versions.json
    validation_summary.json
```

Successful records go to `distillation_outputs.jsonl`.

Failed records go to `distillation_errors.jsonl`.

Each attempt, including dry-run and repair attempts, goes to `distillation_attempts.jsonl`.

Review items go to `distillation_review_queue.jsonl`.

## 10. JSONL Record Draft

Draft successful record:

```json
{
  "schema_version": "warden_distill_v0.2",
  "sample_id": "...",
  "sample_key": "...",
  "source_manifest": "...",
  "source_split": "train",
  "teacher_model": "...",
  "teacher_role": "primary_teacher",
  "teacher_profile": "...",
  "teacher_run_id": "...",
  "prompt_template_version": "...",
  "input_modalities": ["url", "visible_text", "html_action_summary", "forms", "network", "screenshot_summary"],
  "fallback_reason": null,
  "diagnostic_only": false,
  "do_not_train_as_gold": true,
  "needs_human_review": false,
  "rule_router_observation": {},
  "text_semantic_concepts": {},
  "vision_evidence_observations": {},
  "decision_head_auxiliary_targets": {},
  "evidence_summary": [],
  "quality_flags": [],
  "validation": {
    "json_parse_ok": true,
    "schema_valid": true,
    "repair_attempted": false,
    "split_policy_ok": true,
    "modality_consistency_ok": true,
    "chain_of_thought_leakage_detected": false
  }
}
```

Draft error record:

```json
{
  "sample_id": "...",
  "sample_key": "...",
  "source_manifest": "...",
  "source_split": "train",
  "attempt": 1,
  "teacher_profile": "...",
  "teacher_role": "primary_teacher",
  "error_type": "schema_validation_failed",
  "error_message": "...",
  "raw_output_path": "raw_teacher_outputs/<sample_key>.1.raw.txt",
  "retryable": true,
  "do_not_train_as_gold": true,
  "needs_human_review": true
}
```

This is a draft distillation-output record and not official Warden runtime schema.

## 11. Schema Validation And Repair Policy

Staged validation:

1. JSON parse check.
2. Required field check.
3. Enum value check.
4. Modality consistency check.
5. Split-policy check.
6. Evidence-grounding check.
7. No forbidden final-label override check.
8. No chain-of-thought leakage check.

Schema repair may fix:

- JSON syntax;
- field names when mapping is unambiguous;
- enum normalization;
- missing nullable fields;
- missing empty object defaults.

Schema repair must not:

- invent evidence;
- upgrade uncertainty into certainty;
- create visual observations for text-only fallback outputs;
- convert weak labels into gold labels;
- convert `rule_router` into teacher label;
- alter human labels;
- hide val/test contamination.

Repair must preserve:

- original raw output;
- repair prompt version;
- repair audit record;
- validation status before and after repair.

## 12. Split Policy And Contamination Prevention

Official distillation policy:

- process `train split` only by default;
- require final frozen benign + malicious manifests before full official run;
- write training-eligible outputs only from train split after final approval;
- keep `do_not_train_as_gold=true` until a later approved training-ingestion task explicitly consumes safe teacher fields.

Val/test policy:

- val/test teacher runs require `diagnostic_only=true`;
- diagnostic outputs must be written to a separate diagnostic directory;
- diagnostic outputs must set `do_not_train_as_gold=true`;
- diagnostic outputs must not be used for training, prompt tuning, threshold selection, model selection, acceptance metrics, or final claims.

Fail-closed rules:

- if a manifest row lacks split information, fail closed;
- if requested split and row split disagree, fail closed;
- if diagnostic mode is missing for val/test, fail closed;
- if prompt packet includes hidden label metadata, fail closed.

## 13. Review Queue Policy

Generate `distillation_review_queue.jsonl` records when any of these happen:

- teacher conflict;
- judge disagreement;
- fallback modality loss;
- visual/text evidence conflict;
- rule-router conflict;
- weak-label conflict;
- high-impact uncertainty;
- suspected cloak/gate;
- payload not observed but high-risk behavior suggested;
- business legitimacy ambiguity;
- schema repair required;
- repeated teacher failure;
- val/test diagnostic output attempted outside diagnostic mode;
- `needs_human_review=true`;
- `do_not_train_as_gold=true` with high-value sample priority.

Review queue records should include:

- `sample_id`;
- `sample_key`;
- `review_priority`;
- `review_reasons`;
- `quality_flags`;
- short evidence quotes;
- raw output path;
- suggested manual action.

## 14. Resume And Idempotency

The future runner must define:

- stable run id;
- stable sample key;
- per-sample status;
- attempt counter;
- raw teacher output preservation;
- atomic write or temp-file rename strategy;
- skip already successful samples when `--resume` is enabled;
- retry failed samples only under explicit policy;
- never overwrite existing successful JSONL records silently.

Stable `sample_key` should be derived from stable source fields such as manifest path, sample id, current path, and schema version. The exact hash rule should be frozen in the implementation task.

Append-only JSONL is preferred. If deduplication is needed, write a separate index or summary instead of editing historical successful lines.

## 15. Logging And Audit

Required run-level audit:

- config snapshot;
- prompt template version;
- schema version;
- teacher routing decision;
- fallback reason;
- token / cost estimate if available;
- latency if available;
- validation result;
- repair result;
- review queue reason;
- run-level summary.

Required per-attempt audit:

- sample id and sample key;
- teacher role and profile;
- input modalities;
- prompt path if written;
- raw output path if any;
- parse / validation status;
- retryability;
- error category;
- timestamp.

`distillation_summary.md` should report:

- total rows inspected;
- rows skipped by split policy;
- dry-run prompt count;
- successful output count;
- error count;
- repair count;
- review queue count;
- fallback count by reason;
- `needs_human_review` count;
- `do_not_train_as_gold` count.

## 16. Pilot Plan

Pilot stages:

1. Dry-run prompt build only.
2. Local schema validation only.
3. Tiny teacher pilot on train split only, for example 10 to 30 samples.
4. Judge / audit pilot.
5. Human review of pilot outputs.
6. Prompt / schema revision.
7. Bounded train-only pilot.
8. Full train distillation only after final dataset freeze and human approval.

Pilot outputs before final dataset freeze must set:

```json
{
  "do_not_train_as_gold": true
}
```

## 17. Risks And Caveats

- This document is design-only.
- `warden_distill_v0.2` is still draft.
- Prompt quality has not been empirically validated.
- Exact MiMo and DeepSeek endpoint behavior remains a future implementation concern.
- Split safety depends on the future runner enforcing fail-closed checks.
- Schema repair can damage data quality if allowed to change semantics.
- Review queue generation requires downstream human review capacity.

## 18. Future Implementation Checklist

Before runner implementation:

- freeze exact CLI names and storage root;
- implement a typed run config;
- implement manifest row reader without mutating manifests;
- implement split-policy fail-closed checks;
- implement evidence pack construction without hidden labels;
- implement prompt packet writing;
- implement dry-run mode first;
- implement teacher routing logs before API calls;
- implement JSON parse and schema validation;
- implement schema repair audit before repair is enabled;
- implement append-only JSONL writes;
- implement resume / idempotency index;
- implement review queue generation;
- implement summary reporting;
- run a train-only dry-run;
- run a tiny train-only pilot only after separate approval.
