# WARDEN_DISTILLATION_RUNNER_OUTPUT_INSPECTION_V1

## 中文版

### 摘要

本报告审查上一轮 Warden distillation runner skeleton 在 `E:\WardenData\manifests\distillation_skeleton_v1` 生成的 mock 输出。结论分两层：

1. 当前 mock 输出作为 skeleton 工程烟测产物是安全的：文件齐全、JSONL 可解析、audit/report count 一致、10 条记录全部 `do_not_train_as_gold=true` 和 `diagnostic_only=true`，没有 forbidden field，外部/API/OCR/YOLO/CLIP call counter 全部为 0。
2. 当前输出还不能直接作为 real teacher adapter 输出合同。接真实 teacher adapter 前必须补齐稳定 sample key、source manifest/source split、teacher profile/run id、prompt template version、image modality flag、structured validation / attempt metadata 等字段。

Severity 结论：

- `BLOCKER`: 当前 mock 输出缺少 real teacher adapter 所需的关键 provenance、prompt/version、teacher routing、validation 和 modality guardrail 字段。真实 adapter 任务必须先冻结或实现这些字段。
- `HIGH`: review queue 对人工复核仍偏薄，缺少 priority、短 evidence context、reason taxonomy 和 schema-failure / high-risk-uncertainty 分类。
- `MEDIUM`: audit/report 对 mock 足够，但对真实 teacher pilot 缺少 prompt/schema version、output paths、latency、retry、repair、token/cost 和 per-attempt 摘要。
- `LOW`: 文档可进一步说明 `WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md` 是当前实际 runner design 文件名，避免任务文本里的 V1 名称造成查找歧义。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Warden Distillation Runner Output Inspection V1

## 1. Executive Summary

This report inspects the mock output produced by the Warden distillation runner skeleton under:

```text
E:\WardenData\manifests\distillation_skeleton_v1
```

The current mock output is machine-readable and safe as a skeleton smoke artifact. All expected files exist, JSONL rows parse, `run_report.md` agrees with `run_audit.json`, records are non-gold and diagnostic-only, forbidden fields are absent, and model/API/OCR/YOLO/CLIP call counters are zero.

The output is not ready to become the real teacher adapter output contract without changes. Before real teacher adapter implementation, Warden should add or freeze key provenance, prompt versioning, teacher routing, modality, structured validation, attempt, and audit fields.

## 2. Files Inspected

Repository docs and contracts checked:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_implementation_skeleton_v1.md`

Source files checked:

- `src/warden/distillation/schema.py`
- `src/warden/distillation/schema_validator.py`
- `src/warden/distillation/mock_teacher.py`
- `src/warden/distillation/runner.py`

Output files inspected:

- `E:\WardenData\manifests\distillation_skeleton_v1\distillation_records.jsonl`
- `E:\WardenData\manifests\distillation_skeleton_v1\review_queue.jsonl`
- `E:\WardenData\manifests\distillation_skeleton_v1\run_audit.json`
- `E:\WardenData\manifests\distillation_skeleton_v1\run_report.md`
- `E:\WardenData\manifests\distillation_skeleton_v1\errors.jsonl`

Helper used:

- `scripts/distillation/inspect_distillation_runner_outputs.py`

## 3. Counts Observed

Output file status:

| File | Size | Status |
| --- | ---: | --- |
| `distillation_records.jsonl` | 16986 | present |
| `review_queue.jsonl` | 2142 | present |
| `run_audit.json` | 674 | present |
| `run_report.md` | 783 | present |
| `errors.jsonl` | 0 | present and intentionally empty for this zero-error smoke |

Observed machine counts:

| Metric | Value |
| --- | ---: |
| records | 10 |
| review queue rows | 7 |
| error rows | 0 |
| `total_rows_seen` | 10 |
| `processed_count` | 10 |
| `skipped_existing_count` | 0 |
| `error_count` | 0 |
| `review_queue_count` | 7 |
| `schema_valid_count` | 10 |
| `schema_invalid_count` | 0 |
| `teacher_calls` | 0 |
| `external_api_calls` | 0 |
| `ocr_calls` | 0 |
| `yolo_calls` | 0 |
| `clip_calls` | 0 |

Record distributions:

- `schema_version`: `warden_distill_v0.2_mock` = 10
- `teacher_model`: `mock_teacher_v0` = 10
- split: `train` = 10
- duplicate `record_id`: none
- duplicate `sample_id`: none
- forbidden field hits: none
- records failing `do_not_train_as_gold=true`: 0
- records failing `diagnostic_only=true`: 0

Review queue:

- unlinked review rows: 0
- rows without reasons: 0
- rows without suggested action: 0
- review reason counts:
  - `action_surface_present_with_mock_context`: 7

## 4. File And Parse Readiness Findings

### PASS

- All expected output files exist.
- All JSONL rows are parseable.
- JSON files are UTF-8 readable.
- `errors.jsonl` exists and is empty. This is consistent with `error_count=0`.
- `run_report.md` agrees with `run_audit.json` for all reported counts.
- `run_report.md` states no real teacher calls were made and outputs are mock/dry-run only.

### Readiness Note

For mock smoke, file and parse readiness are acceptable.

For real teacher adapter work, the directory layout remains too minimal because it lacks per-attempt logs, raw teacher outputs, prompt snapshots, repair logs, and validation summaries described in the runner design contract.

Severity: `HIGH`

## 5. Schema-Readiness Findings

### Present And Stable In Current Mock Records

The records include the current skeleton-required fields:

- `schema_version`
- `record_id`
- `sample_id`
- `sample_path`
- `split`
- `diagnostic_only`
- `do_not_train_as_gold`
- `teacher_model`
- `teacher_role`
- `input_modalities`
- `fallback_reason`
- `evidence_pack_summary`
- `rule_router_observation`
- `text_semantic_concepts`
- `vision_evidence`
- `decision_head_auxiliary_targets`
- `quality_flags`
- `review_reasons`
- `created_at`

### Missing Or Ambiguous For Real Teacher Adapter

The helper found these future-readiness fields missing from all 10 records:

- `sample_key`
- `source_manifest`
- `source_split`
- `teacher_profile`
- `teacher_run_id`
- `prompt_template_version`
- `image_input_passed_to_teacher`
- `validation`
- `error_status`

These fields are not required for the mock skeleton test, but they are required or strongly implied by the runner design contract for real teacher adapter auditability.

Severity: `BLOCKER`

### Fields That Should Remain Mock-Only

- `schema_version = warden_distill_v0.2_mock`
- `teacher_model = mock_teacher_v0`
- `teacher_role = mock_skeleton`
- deterministic `created_at = 1970-01-01T00:00:00Z`

These are useful for deterministic mock validation. They must not be confused with production teacher metadata.

Severity: `HIGH`

### Fields That Must Never Be Used As Model Input

The inspection did not find hidden final labels in output records. For future prompt construction, these remain forbidden as teacher-visible input:

- human gold labels;
- val/test labels;
- `triage_label`;
- split metadata;
- folder names used as label hints;
- weak labels promoted to facts.

Severity: `BLOCKER` if violated by a future adapter.

## 6. L1 Contract Alignment Findings

The current mock output aligns with the L1 contract in the following ways:

- `rule_router_observation` is diagnostic / routing context only.
- `rule_router_observation` includes `not_teacher_label=true`.
- `rule_router` is not teacher label and not final label.
- `text_semantic_concepts` is present as the main future distillation target area.
- `vision_evidence` states `status=not_run`; it is evidence observation only and not a visual classifier.
- `decision_head_auxiliary_targets` is advisory, with `final_label_advisory=unknown`.
- `do_not_train_as_gold=true` for all mock outputs.
- The output text includes the required principle: `payload not observed` is not automatic benign.
- The output text includes the required principle: `action surface is not automatically threat action`.
- The distillation docs preserve the required principle: `weak labels are evidence`.

No L1 contract violation was found in the inspected mock outputs.

Severity: no immediate issue.

## 7. Split-Safety Findings

### Positive Findings

- All inspected records are `split=train`.
- All inspected records set `do_not_train_as_gold=true`.
- All inspected records set `diagnostic_only=true`.
- No forbidden gold-label fields were found.
- `run_audit.json` records `split=train`, `mode=mock`, and the source manifest path.

### Remaining Gaps

The inspected records use `split`, but they do not separately preserve `source_split` and requested run split. They also do not include `source_manifest` per record. This makes future auditing weaker when multiple manifests or diagnostic val/test output directories exist.

The output does not include an explicit downstream ingestion guard field beyond `do_not_train_as_gold=true` and `diagnostic_only=true`. These flags are sufficient for mock safety, but future ingestion should require a separate approved training-consumption gate and should reject these mock records by default.

Severity: `BLOCKER` before real teacher adapter output is allowed to feed any downstream training-ingestion path.

## 8. Resume / Idempotency Findings

### Positive Findings

- `record_id` is present on all records.
- No duplicate `record_id` values were found.
- No duplicate `sample_id` values were found in this 10-row smoke.
- The prior handoff reports resume/idempotency tests passed.

### Remaining Gaps

For real teacher adapter runs, `record_id` alone is not enough. The design contract calls for a stable `sample_key` derived from stable source fields and schema/version context. The current output lacks:

- `sample_key`;
- `source_manifest`;
- `source_split`;
- `teacher_run_id`;
- attempt counter;
- per-attempt raw output path;
- retry and repair metadata;
- append-only status index or validation summary.

Severity: `BLOCKER`

## 9. Review Queue Findings

### Positive Findings

- All review queue rows are parseable.
- Every review row links back to a source `record_id`.
- Every review row has at least one `review_reason`.
- Every review row has `suggested_action`.

### Usability Gaps

The review queue is usable for skeleton smoke, but too thin for real teacher pilot review. It lacks:

- review priority;
- short evidence quotes;
- source artifact references;
- human-readable context summary;
- reason taxonomy separating schema failure, evidence incompleteness, fallback modality loss, and high-risk uncertainty;
- raw teacher output path;
- prompt/attempt references.

Current review reasons are concentrated entirely in `action_surface_present_with_mock_context`, which is expected for this smoke but not enough to exercise the future review taxonomy.

Severity: `HIGH`

## 10. Audit And Reproducibility Findings

### Positive Findings

`run_audit.json` logs:

- `run_id`
- `started_at`
- `finished_at`
- `manifest`
- `output_dir`
- `split`
- `mode`
- `limit`
- `seed`
- row and validation counts
- call counters for teacher/API/OCR/YOLO/CLIP

`run_report.md` is bilingual and agrees with audit counts.

### Gaps Before Real Teacher Adapter

For real teacher adapter readiness, audit/report should additionally log:

- `schema_version`;
- `prompt_template_version`;
- teacher profile and routing decision;
- fallback reason summary;
- output file paths;
- raw teacher output paths;
- repair attempt counts;
- retry counts;
- latency;
- token/cost estimates when available;
- secure credential handling summary without secrets;
- per-attempt parse/validation status.

Severity: `MEDIUM` for mock smoke, `HIGH` before real pilot.

## 11. Real Teacher Adapter Readiness Gaps

### `BLOCKER`

1. Freeze and implement stable `sample_key`, `source_manifest`, and `source_split` fields before real teacher adapter output.
2. Add teacher provenance fields: `teacher_profile`, `teacher_run_id`, `prompt_template_version`, and `image_input_passed_to_teacher`.
3. Add structured validation fields covering JSON parse, schema validity, split policy, modality consistency, repair status, and chain-of-thought leakage detection.
4. Add attempt-level records or output paths for prompt snapshots, raw teacher output, parse failure, retry, repair, and final validation.
5. Keep `do_not_train_as_gold=true` as the default until a later approved training-ingestion task explicitly consumes safe train-only fields.

### `HIGH`

1. Expand review queue records with priority, short evidence context, artifact references, reason taxonomy, raw output paths, and suggested manual actions.
2. Add audit logging for teacher routing, fallback modality loss, prompt/schema version, retry/backoff, latency, and token/cost estimates.
3. Add explicit modality guardrails so text-only fallback cannot claim visual inspection.
4. Add separate diagnostic output location or fields for val/test teacher audits.

### `MEDIUM`

1. Add output path inventory to `run_report.md`.
2. Add review reason counts to `run_report.md`.
3. Add duplicate detection summary to audit/report.
4. Add an errors schema even when `errors.jsonl` is empty.

### `LOW`

1. Clarify that current runner design file is `WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`.
2. Consider naming consistency between mock skeleton files and future design layout, while preserving current skeleton behavior.

## 12. Blocking Issues Before Real Teacher Adapter

The current mock output has no blocker for continuing mock-only skeleton validation.

There are `BLOCKER` issues before real teacher adapter implementation:

- missing stable `sample_key` / source provenance fields;
- missing teacher profile/run/prompt version fields;
- missing image modality guard field;
- missing structured validation and per-attempt audit fields;
- missing real-adapter output layout for prompts, raw outputs, attempts, repairs, and validation summaries.

These should be fixed in a separate adapter-readiness implementation task before any MiMo / DeepSeek / OpenAI / Claude teacher adapter is allowed to emit pilot outputs.

## 13. Non-Blocking Improvements

- Add report-level review reason histogram.
- Add report-level duplicate key summary.
- Include output file path inventory in the report.
- Expand review queue context for human triage.
- Add documentation note mapping current mock names to future design names.

## 14. Recommended Next Task

Create a dedicated task:

```text
TASK-20260513-WARDEN-DISTILLATION-REAL-ADAPTER-READINESS-FIELDS-V1
```

Goal:

Extend the skeleton output contract, still without real teacher calls, to add:

- stable `sample_key`;
- `source_manifest` and `source_split`;
- `teacher_profile`, `teacher_run_id`, and `prompt_template_version`;
- `image_input_passed_to_teacher`;
- structured `validation`;
- attempt JSONL;
- prompt snapshot paths;
- raw output / repair path placeholders;
- richer review queue fields;
- expanded audit/report summaries.

Stop condition:

Run the enhanced skeleton in mock mode only, confirm all non-gold/diagnostic invariants remain true, and keep all external/model/OCR/YOLO/CLIP call counters at zero.

## 15. Evidence Summary

Facts:

- The inspected mock output directory contains all five expected output files.
- All JSONL files are parseable.
- `errors.jsonl` is empty and `error_count=0`.
- `run_report.md` agrees with `run_audit.json`.
- 10 records are present and all use `schema_version=warden_distill_v0.2_mock`.
- All 10 records set `do_not_train_as_gold=true` and `diagnostic_only=true`.
- No forbidden fields were detected.
- Call counters for teacher/API/OCR/YOLO/CLIP are all zero.

Inferences:

- The current mock output is safe for skeleton engineering validation.
- The current output needs provenance, prompt/version, modality, validation, and attempt fields before real teacher adapter output can be safely audited.

Assumptions:

- The prior handoff path `E:\WardenData\manifests\distillation_skeleton_v1` is the latest skeleton output directory for this inspection.
- Future real teacher adapter work will follow the current runner design contract unless a later approved task changes it.

Risks:

- If a future adapter reuses the current mock schema without the `BLOCKER` fixes, downstream training and audit paths may lack enough information to prevent contamination or reproduce teacher calls.
