"""Constants for the mock distillation skeleton schema."""

SCHEMA_VERSION = "warden_distill_v0.2_mock"
TEACHER_MODEL = "mock_teacher_v0"
TEACHER_ROLE = "mock_skeleton"
TEACHER_PROFILE = "mock_teacher_v0"
PROMPT_TEMPLATE_VERSION = "mock_prompt_v0"
VALIDATOR_VERSION = "warden_distill_validator_v0.2"
ALLOWED_SPLITS = {"train", "val", "test", "unknown"}
ALLOWED_MODES = {"dry-run", "mock"}
FORBIDDEN_FIELDS = {
    "final_gold_label",
    "final_training_label",
    "gold_malicious_label",
    "chain_of_thought",
    "hidden_reasoning",
    "teacher_cot",
}

REQUIRED_OUTPUT_FILES = [
    "distillation_records.jsonl",
    "review_queue.jsonl",
    "attempts.jsonl",
    "run_audit.json",
    "run_report.md",
    "errors.jsonl",
]

REQUIRED_RECORD_KEYS = [
    "schema_version",
    "record_id",
    "sample_key",
    "sample_id",
    "sample_path",
    "source_manifest",
    "source_split",
    "split",
    "diagnostic_only",
    "do_not_train_as_gold",
    "teacher_model",
    "teacher_role",
    "teacher_profile",
    "teacher_run_id",
    "prompt_template_version",
    "attempt_id",
    "attempt_index",
    "created_at_utc",
    "input_modalities",
    "fallback_reason",
    "image_input_passed_to_teacher",
    "image_input_policy",
    "visual_evidence_source",
    "evidence_pack_summary",
    "rule_router_observation",
    "text_semantic_concepts",
    "vision_evidence",
    "decision_head_auxiliary_targets",
    "quality_flags",
    "review_reasons",
    "validation",
    "error_status",
    "record_hash",
    "evidence_pack_hash",
    "prompt_input_hash",
    "created_at",
]
