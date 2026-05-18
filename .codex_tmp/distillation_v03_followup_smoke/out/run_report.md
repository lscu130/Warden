# Warden Distillation Skeleton Run Report

## 中文版

本报告来自 dry-run / mock distillation runner skeleton。没有真实 teacher call，输出不得作为 gold label 或训练标签。

## English Version

This report was produced by the dry-run / mock distillation runner skeleton.

- No real teacher calls were made.
- Outputs are mock/dry-run only.
- All records must keep `do_not_train_as_gold=true`.
- All records must keep `diagnostic_only=true`.

## Counts

- `run_id`: distill_skeleton_9b498c78fb2450f2
- `teacher_run_id`: distill_skeleton_9b498c78fb2450f2
- `schema_version`: warden_distill_v0.3_mock
- `prompt_template_version`: warden_distill_v0.3
- `source_manifest`: E:\Warden\.codex_tmp\distillation_v03_followup_smoke\manifest.csv
- `source_split`: train
- `total_rows_seen`: 1
- `processed_count`: 1
- `skipped_existing_count`: 0
- `error_count`: 0
- `review_queue_count`: 1
- `schema_valid_count`: 1
- `schema_invalid_count`: 0
- `records_written`: 1
- `records_valid`: 1
- `records_invalid`: 0
- `attempt_count`: 1
- `mock_teacher_calls`: 1
- `real_teacher_calls`: 0
- `external_api_calls`: 0
- `teacher_calls`: 0
- `ocr_calls`: 0
- `yolo_calls`: 0
- `clip_calls`: 0
- `do_not_train_as_gold_failures`: 0
- `diagnostic_only_failures`: 0

## Readiness Summary

- `missing_required_readiness_fields`: {}
- `missing_required_concept_fields`: {}
- `concept_level_readiness`: {'records_with_formula_concepts': 1, 'records_with_context_action_relation': 1, 'records_with_evidence_sufficiency': 1, 'records_with_formula_result': 1, 'records_with_claimed_identity_candidates': 1, 'records_with_relation_judgments': 1, 'records_with_evidence_state': 1, 'records_with_threat_action_candidate': 1}
- `schema_validation_errors_by_type`: {}
- `review_reason_counts`: {'action_surface_without_context': 1, 'formula_relation_unclear': 1}
- `duplicate_record_ids`: []
- `duplicate_sample_keys`: []
- `output_files`: {'records': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\distillation_records.jsonl', 'review': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\review_queue.jsonl', 'attempts': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\attempts.jsonl', 'audit': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\run_audit.json', 'report': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\run_report.md', 'errors': 'E:\\Warden\\.codex_tmp\\distillation_v03_followup_smoke\\out\\errors.jsonl'}
