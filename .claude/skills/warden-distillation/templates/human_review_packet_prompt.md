# HUMAN_REVIEW_PACKET_PROMPT_V0_2

## 中文版

### 摘要

这是 human-review packet 模板，用于压缩证据、teacher 分歧和 QC flags，方便人工快速审查。输出 JSON-only。

---

## English Version

> AI note: This English section is authoritative. The prompt below is the template body.

# Human Review Packet Prompt

You create a concise human-review packet for a Warden distillation output.

Return JSON only. Do not reveal hidden chain-of-thought. Use short evidence quotes only.

Rules:

- `weak labels are evidence`.
- `payload not observed` is not automatic benign.
- `action surface is not automatically threat action`.
- `rule_router` output is context only.
- Teacher advisory labels do not override human gold labels.
- Do not claim visual evidence if image input was unavailable.

Input:

```json
{
  "sample_id": "{{sample_id}}",
  "raw_evidence_summary": {{raw_evidence_summary}},
  "teacher_output": {{teacher_output}},
  "judge_output_if_available": {{judge_output_if_available}},
  "human_label_if_available": {{human_label_if_available}},
  "rule_router_context": {{rule_router_context}}
}
```

Output JSON:

```json
{
  "schema_version": "warden_human_review_packet_v0.2",
  "sample_id": "{{sample_id}}",
  "review_priority": "medium",
  "review_reasons": [],
  "evidence_snapshot": {
    "url_domain": "",
    "visible_text_quotes": [],
    "action_surfaces": [],
    "network_notes": [],
    "visual_notes": []
  },
  "conflicts": {
    "teacher_vs_human": null,
    "teacher_vs_rule_router": null,
    "visual_vs_text": null,
    "weak_label_conflict": null
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
  "recommended_manual_action": "inspect_before_training_use"
}
```
