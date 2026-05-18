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

- `run_id`: distill_skeleton_0741f559f2b4a766
- `teacher_run_id`: distill_skeleton_0741f559f2b4a766
- `schema_version`: warden_distill_v0.3_mock
- `prompt_template_version`: warden_distill_v0.3
- `source_manifest`: .codex_tmp\distillation_v03_adapter_readiness_smoke\manifest.csv
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
- `repair_count`: 0
- `validation_summary_count`: 1
- `validation_pass_count`: 1
- `validation_fail_count`: 0
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
- `concept_level_readiness`: {'records_with_formula_concepts': 1, 'records_with_context_engagement_relation': 1, 'records_with_evidence_sufficiency': 1, 'records_with_formula_result': 1, 'records_with_claimed_identity_candidates': 1, 'records_with_relation_judgments': 1, 'records_with_evidence_state': 1, 'records_with_threat_action_candidate': 1}
- `schema_validation_errors_by_type`: {}
- `review_reason_counts`: {'action_surface_without_risk_bearing_engagement': 1, 'formula_relation_unclear': 1, 'risk_bearing_engagement_unclear': 1}
- `duplicate_record_ids`: []
- `duplicate_sample_keys`: []
- `output_path_inventory`: {'distillation_records': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\distillation_records.jsonl', 'review_queue': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\review_queue.jsonl', 'attempts': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\attempts.jsonl', 'validation_summaries': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\validation_summaries.jsonl', 'run_audit': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_audit.json', 'run_report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_report.md', 'adapter_readiness_report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\adapter_readiness_report.md', 'errors': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\errors.jsonl', 'prompt_snapshots': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\prompt_snapshots', 'raw_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\raw_outputs', 'repaired_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\repaired_outputs'}
- `output_files`: {'records': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\distillation_records.jsonl', 'review': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\review_queue.jsonl', 'attempts': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\attempts.jsonl', 'validation_summaries': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\validation_summaries.jsonl', 'audit': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_audit.json', 'report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_report.md', 'adapter_readiness_report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\adapter_readiness_report.md', 'errors': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\errors.jsonl', 'prompt_snapshots': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\prompt_snapshots', 'raw_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\raw_outputs', 'repaired_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\repaired_outputs'}
- `cost_token_placeholders`: {'mock_only': True, 'token_usage_available': False, 'cost_available': False}
- `adapter_readiness_status`: ready_for_no_network_dry_run
- `live_teacher_readiness`: not_ready_for_live_teacher
