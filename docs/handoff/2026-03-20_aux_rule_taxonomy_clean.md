# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF-2026-03-20-AUX-RULE-TAXONOMY-CLEAN
- Related Task ID: TASK-2026-03-20-AUX-RULE-TAXONOMY-CLEAN
- Task Title: Extend rule_labels.json to emit threat_taxonomy_v1 candidate fields without changing TrainSet V1 primary
- Module: labeling / weak-labeling
- Author: Codex
- Date: 2026-03-20
- Status: DONE

---

## 1. Executive Summary

Extended `derive_rule_labels()` so `rule_labels.json` now emits a `threat_taxonomy_v1` candidate namespace while keeping existing `rule_flags` and `review_priority` behavior intact.
This was done to map current auto-label signals into the frozen taxonomy draft while freezing `threat_taxonomy_v1` as a long-term active weak-label namespace, without changing TrainSet V1 primary, manifest defaults, capture-script behavior, or `auto_labels.json`.
Current completion state: done.

---

## 2. What Changed

### Code Changes

- Added additive taxonomy derivation logic inside `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- Added candidate scoring / rule-source aggregation for primary threat and scenario labels
- Added derived candidate tag emission for narrative, evidence, evasion, and ecosystem fields

### Doc Changes

- Marked the active task doc as `DONE`
- Added this handoff document
- Updated formal docs to state that `threat_taxonomy_v1` is a long-term active weak-label output under `rule_labels.json`
- Documented that it must not be treated as TrainSet V1 primary default gold labels and must not be default-written into primary manifest core fields

### Output / Artifact Changes

- `rule_labels.json` can now include `threat_taxonomy_v1`
- Existing `rule_flags` and `review_priority` outputs remain present

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-03-20_aux_rule_taxonomy_clean_task.md`
- `docs/handoff/2026-03-20_aux_rule_taxonomy_clean.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: only additive weak-label rule logic was changed
- capture script and manifest / consistency scripts were intentionally left untouched

---

## 4. Behavior Impact

### Expected New Behavior

- `derive_rule_labels()` now emits `threat_taxonomy_v1` under `rule_labels.json`
- taxonomy fields carry candidate semantics only, with confidence and rule-source lists
- existing backfill flow can generate the new taxonomy structure through `--emit-rule-labels`
- `threat_taxonomy_v1` is now documented as a long-term active weak-label namespace rather than a temporary experiment field

### Preserved Behavior

- `auto_labels.json` structure remains unchanged
- capture script default behavior remains unchanged
- existing `rule_flags` and `review_priority` remain unchanged
- TrainSet V1 primary and manifest default core fields remain unchanged

### User-facing / CLI Impact

- no new CLI flags were added
- `Warden_dataset_backfill_labels_brandlex.py --emit-rule-labels` continues to work through the same interface

### Output Format Impact

- `rule_labels.json` gains a new additive namespace: `threat_taxonomy_v1`
- no other default output file format was changed

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `rule_labels.json -> threat_taxonomy_v1.primary_threat_label_candidate`
- `rule_labels.json -> threat_taxonomy_v1.primary_threat_label_confidence`
- `rule_labels.json -> threat_taxonomy_v1.primary_threat_label_rules`
- `rule_labels.json -> threat_taxonomy_v1.scenario_label_candidate`
- `rule_labels.json -> threat_taxonomy_v1.scenario_label_confidence`
- `rule_labels.json -> threat_taxonomy_v1.scenario_label_rules`
- `rule_labels.json -> threat_taxonomy_v1.narrative_tags_candidate`
- `rule_labels.json -> threat_taxonomy_v1.evidence_tags_candidate`
- `rule_labels.json -> threat_taxonomy_v1.evasion_tags_candidate`
- `rule_labels.json -> threat_taxonomy_v1.ecosystem_tags_candidate`
- `rule_labels.json -> threat_taxonomy_v1.taxonomy_source`
- `rule_labels.json -> threat_taxonomy_v1.taxonomy_review_status`

Compatibility notes:

All new fields are additive and nested only under `threat_taxonomy_v1`.
Existing capture and backfill entry points still work without argument or workflow changes.
The new fields remain explicitly weak-label-safe through candidate naming and `taxonomy_review_status = weak_candidate_only`.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py --roots E:\Warden\tmp\taxonomy_smoke\sample_a E:\Warden\tmp\taxonomy_smoke\sample_b --workers 2 --emit-rule-labels --limit 2
Get-Content -Path E:\Warden\tmp\taxonomy_smoke\sample_a\rule_labels.json
Get-Content -Path E:\Warden\tmp\taxonomy_smoke\sample_b\rule_labels.json
python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py --roots E:\Warden\data\raw\phish\www.whatsapp-my.eu.cc_20260126T153839Z E:\Warden\data\raw\benign\shopifysite.cn_article_tag_shopify_E5_BC_80_E5_BA_97_E6_B5_81_E7_A8_8B_20260206T163032Z --workers 2 --emit-rule-labels --limit 2
Get-Content -Path E:\Warden\data\raw\phish\www.whatsapp-my.eu.cc_20260126T153839Z\rule_labels.json
Get-Content -Path E:\Warden\data\raw\benign\shopifysite.cn_article_tag_shopify_E5_BC_80_E5_BA_97_E6_B5_81_E7_A8_8B_20260206T163032Z\rule_labels.json
```

### Result

- `py_compile`: passed
- backfill `--emit-rule-labels` smoke test: passed
- both generated `rule_labels.json` files contained the full frozen `threat_taxonomy_v1` field set
- candidate wording and review status remained weak-label-safe
- rerun on two different real source samples: passed at file-generation level
- real phish sample mapped to `credential_theft`
- current real benign sample still over-triggered to `payment_fraud`, confirming the namespace should remain weak-label-only and should not be promoted directly to TrainSet V1 default gold labels

### Not Run

- capture-script online generation test
- manifest / consistency integration test

Reason:

Temporary-copy smoke validation was run first because the repository initially exposed only one usable source sample.
After the user added one real phish sample and one real benign sample, real-sample backfill validation was rerun and recorded above.
The task scope explicitly excluded capture-script and manifest-path changes.

---

## 7. Risks / Caveats

- Some taxonomy classes remain conservatively under-triggered because current auto-label inputs do not expose strong contact-redirect or QR-specific evidence.
- `fake_support_or_contact_diversion` and some narrative / ecosystem tags are only weakly inferable from current signals and may need richer upstream evidence later.
- Confidence values are deterministic heuristics, not calibrated probabilities.
- The current benign smoke sample still triggers `payment_fraud`, so `threat_taxonomy_v1` is not ready to be treated as default gold supervision.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-20_aux_rule_taxonomy_clean_task.md`
- `docs/handoff/2026-03-20_aux_rule_taxonomy_clean.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`

Doc debt still remaining:

- labeling-module-specific documentation could still be added later if you want a dedicated module-level taxonomy maintenance spec

---

## 9. Recommended Next Step

- continue raising `threat_taxonomy_v1` coverage through unified offline backfill
- prioritize manual review for high-value, high-conflict, and high-uncertainty subsets
- extend upstream auto-label evidence only when you want stronger coverage for `fake_support_or_contact_diversion`, `contact_redirect_present`, or `qr_present`
