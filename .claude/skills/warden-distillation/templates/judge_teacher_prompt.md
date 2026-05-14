# JUDGE_TEACHER_PROMPT_V0_2

## 中文版

### 摘要

这是 judge / audit teacher 模板，用于比较 teacher output、raw evidence、可选 human label 和 `rule_router_context`。输出 JSON-only，不输出 hidden chain-of-thought。

---

## English Version

> AI note: This English section is authoritative. The prompt below is the template body.

# Judge Teacher Prompt

You are auditing a Warden draft teacher output for schema compliance, evidence support, split safety, and L1 semantic alignment.

Return JSON only. Do not reveal hidden chain-of-thought. Use short evidence quotes only.

Audit rules:

- `rule_router` outputs are routing / evidence sufficiency diagnostics only.
- `rule_router` is not a gold label, not a teacher label, and not final model judgment.
- `weak labels are evidence`, not gold labels.
- `payload not observed` is not automatic benign.
- `action surface is not automatically threat action`.
- `vision_evidence` is evidence recovery, not classifier output.
- Advisory Decision Head fields must not override human labels.
- Val/test teacher outputs must not be used as training targets.
- DeepSeek-V4 fallback must not claim direct visual inspection unless image input support and actual image input are verified.

Input packet:

```json
{
  "sample_id": "{{sample_id}}",
  "source_split": "{{source_split}}",
  "raw_evidence": {{raw_evidence}},
  "teacher_output": {{teacher_output}},
  "human_label_if_available": {{human_label_if_available}},
  "rule_router_context": {{rule_router_context}}
}
```

Output JSON:

```json
{
  "schema_version": "warden_distill_judge_v0.2",
  "sample_id": "{{sample_id}}",
  "audit_result": {
    "schema_valid": false,
    "json_repair_needed": false,
    "semantic_repair_needed": false,
    "unsupported_visual_claims": [],
    "weak_label_overreach": false,
    "rule_router_label_misuse": false,
    "advisory_label_overreach": false,
    "split_policy_violation": false
  },
  "quality_control": {
    "needs_human_review": true,
    "do_not_train_as_gold": true,
    "teacher_disagrees_with_human_label": false,
    "teacher_confidence_low": false,
    "fallback_modality_loss": false,
    "visual_text_conflict": false,
    "rule_router_teacher_conflict": false,
    "evidence_incomplete": false,
    "possible_cloak_or_gate": false
  },
  "repair_recommendations": [],
  "human_review_reasons": [],
  "concise_evidence_notes": []
}
```
