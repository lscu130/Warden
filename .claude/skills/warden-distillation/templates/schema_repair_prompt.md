# SCHEMA_REPAIR_PROMPT_V0_2

## 中文版

### 摘要

这是 schema repair 模板。只能修复 JSON shape、缺失必需 key、类型和明显格式错误。不得改写语义，不得发明证据。

---

## English Version

> AI note: This English section is authoritative. The prompt below is the template body.

# Schema Repair Prompt

You repair Warden distillation JSON shape only.

Return JSON only. Do not reveal hidden chain-of-thought. Do not add new evidence. Do not change semantic content unless the caller explicitly instructs a semantic correction.

Required rules:

- Preserve the sample's semantic meaning.
- Preserve `needs_human_review` and `do_not_train_as_gold` if present.
- Preserve modality limitations.
- Preserve `weak labels are evidence`.
- Preserve `payload not observed`.
- Preserve `action surface is not automatically threat action`.
- Preserve `rule_router_context` as context only.

Input:

```json
{
  "target_schema_version": "warden_distill_v0.2",
  "invalid_json_or_object": {{invalid_json_or_object}},
  "repair_notes": {{repair_notes}}
}
```

Output JSON:

```json
{
  "schema_version": "warden_distill_v0.2",
  "repair_metadata": {
    "repair_type": "json_shape_only",
    "semantic_content_changed": false,
    "fields_added_as_empty_defaults": []
  },
  "repaired_object": {}
}
```
