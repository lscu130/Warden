# Warden Distillation Adapter Readiness Report

## 中文版

本报告只说明 no-network adapter-readiness baseline。没有真实 provider/API/OCR/YOLO/CLIP 调用，也不代表 live teacher 已获批准。

## English Version

This report documents no-network adapter-readiness only. It is not live-teacher approval.

## Status

- `adapter_readiness_status`: ready_for_no_network_dry_run
- `live_teacher_readiness`: not_ready_for_live_teacher
- `schema_version`: warden_distill_v0.3_mock
- `prompt_template_versions`: {'warden_distill_v0.3': 1}
- `teacher_profiles`: {'mock_v0_3_formula': 1}

## Counts

- `attempt_count`: 1
- `repair_count`: 0
- `validation_pass_count`: 1
- `validation_fail_count`: 0
- `review_reason_counts`: {'action_surface_without_risk_bearing_engagement': 1, 'formula_relation_unclear': 1, 'risk_bearing_engagement_unclear': 1}

## Call Counters

- `teacher_calls`: 0
- `real_teacher_calls`: 0
- `external_api_calls`: 0
- `ocr_calls`: 0
- `yolo_calls`: 0
- `clip_calls`: 0

## Output Path Inventory

- `output_path_inventory`: {'distillation_records': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\distillation_records.jsonl', 'review_queue': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\review_queue.jsonl', 'attempts': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\attempts.jsonl', 'validation_summaries': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\validation_summaries.jsonl', 'run_audit': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_audit.json', 'run_report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\run_report.md', 'adapter_readiness_report': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\adapter_readiness_report.md', 'errors': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\errors.jsonl', 'prompt_snapshots': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\prompt_snapshots', 'raw_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\raw_outputs', 'repaired_outputs': '.codex_tmp\\distillation_v03_adapter_readiness_smoke\\out\\repaired_outputs'}

## Guardrails

- `ready_for_live_teacher`: false
- `ready_for_training_ingestion`: false
- `provider_budget_approved`: false
