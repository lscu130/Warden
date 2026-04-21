# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
- Handoff ID: `2026-04-21-l0-latency-breakdown-analysis`
- Related Task ID: `TASK-L0-2026-04-21-LATENCY-BREAKDOWN-ANALYSIS`
- Task Title: `拆解当前 L0 样本判断时延并定位主要耗时来源`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

这次交付没有修改代码，只对当前本地 L0 路径做了阶段级时延拆解。结论很清楚：

- 最大耗时来自 `html_features`
- 第二大耗时来自 `specialized_surface_signals + intent + page_stage`
- 第三大耗时来自品牌提取

在当前 `50` 样本切片上，平均总时延约为 `111.786 ms / sample`。平均阶段占比为：

- `html_features`: `47.71%`
- `specialized_intent_stage`: `29.64%`
- `brand`: `18.22%`

三者合计约占总时延的 `95.57%`。其余阶段都很小。

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- updated `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- added `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

### Output / Artifact Changes

- none

This task only ran profiling and documentation. It did not modify L0 logic.

---

## 3. Files Touched

- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

Optional notes per file:

- the task doc freezes this as an analysis-only task
- the handoff records measured stage-level timing shares and optimization guidance

---

## 4. Behavior Impact

### Expected New Behavior

- no code behavior changed
- the new outcome is a stage-level latency explanation for the current local L0 path

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` was not modified
- schema was not modified
- CLI and sample-dir entry behavior were not modified

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- none

Compatibility notes:

This delivery only profiled the current path. It did not modify fields, function signatures, CLI behavior, or output contracts.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- reuse the same deterministic 50-sample mix as the prior latency task
- manually replay the current `derive_auto_labels_from_sample_dir(...)` path in stages
- measure:
  - sample I/O
  - prep
  - url/forms/network summarization
  - html feature summarization
  - brand extraction / brand consistency
  - evasion + text observability
  - specialized surface + intent + page stage
  - routing + weak-risk + language
  - rule-label derivation
- aggregate mean / median / p90 / p95 / min / max
```

### Result

All-sample stage means on the 50-sample slice:

- `sample_io_ms`: `2.515`
- `prep_ms`: `0.346`
- `url_forms_net_ms`: `0.262`
- `html_features_ms`: `53.337`
- `brand_ms`: `20.362`
- `evasion_textobs_ms`: `1.120`
- `specialized_intent_stage_ms`: `33.129`
- `routing_risk_lang_ms`: `0.682`
- `rule_labels_ms`: `0.034`
- `full_ms`: `111.786`

Mean stage-share percentages:

- `html_features_ms`: `47.71%`
- `specialized_intent_stage_ms`: `29.64%`
- `brand_ms`: `18.22%`
- `sample_io_ms`: `2.25%`
- `evasion_textobs_ms`: `1.00%`
- `routing_risk_lang_ms`: `0.61%`
- `prep_ms`: `0.31%`
- `url_forms_net_ms`: `0.23%`
- `rule_labels_ms`: `0.03%`

Per-group `full_ms` means:

- benign: `122.476 ms`
- adult: `91.185 ms`
- gambling: `100.320 ms`

Why those stages are expensive in the current code:

- `html_features`
  - `summarize_html_features(...)` scans the HTML blob for script sources, known JS library aliases, version patterns, obfuscation-like strings, captcha evidence, and download evidence
  - this stage scales with HTML payload size and repeated string scanning
- `brand`
  - `extract_claimed_brands(...)` loops through every brand and alias in the lexicon, then runs `_kw_match(...)` repeatedly against the full visible text
  - this is effectively repeated text scanning across the whole lexicon
- `specialized_intent_stage`
  - `derive_specialized_surface_signals(...)` runs many `hit_keywords(...)` passes over the same `text_low` / `url_blob`
  - gambling, adult, and gate detectors each rescan keyword families separately, and `derive_intent_signals(...)` and `derive_page_stage(...)` add more scans

Slowest outlier patterns:

- the slowest samples were mostly benign pages with large HTML and heavy brand/specialized scanning
- the top outlier `worldofprintables.com_20260402T023119Z` spent about:
  - `80.070 ms` in `html_features`
  - `159.765 ms` in `brand`
  - `225.788 ms` in `specialized_intent_stage`

### Not Run

- no implementation patch
- no repeated multi-round profiling variance study
- no hardware-isolated benchmark harness

Reason:

This task was explicitly scoped to latency-source analysis only.

---

## 7. Risks / Caveats

- this is still a local working-tree profiling snapshot, not a hardware-general benchmark statement
- stage timings were measured by replaying the current function path in a profiling script, so they are very close to the real path but still not a CPython profiler trace
- optimization savings discussed below are directional unless separately measured in an implementation task

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- if you want the safest latency reduction first, open an implementation task for `html_features` gating or cheap-mode narrowing inside L0
- after that, open a second task for keyword-scan consolidation inside `derive_specialized_surface_signals(...)`
- only then consider brand-stage optimization, because that stage is meaningful but also tied to useful risk evidence

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-21-l0-latency-breakdown-analysis`
- Related Task ID: `TASK-L0-2026-04-21-LATENCY-BREAKDOWN-ANALYSIS`
- Task Title: `Break down the current L0 latency and identify the main cost sources`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

This delivery did not modify code. It only decomposed the current local L0 path by stage. The result is clear:

- the largest cost source is `html_features`
- the second-largest cost source is `specialized_surface_signals + intent + page_stage`
- the third-largest cost source is brand extraction

On the current 50-sample slice, the average total latency is about `111.786 ms / sample`. The average stage shares are:

- `html_features`: `47.71%`
- `specialized_intent_stage`: `29.64%`
- `brand`: `18.22%`

Together, those three stages account for about `95.57%` of the current total latency. Everything else is small.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- updated `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- added `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

### Output / Artifact Changes

- none

This task only ran profiling and documentation. It did not modify L0 logic.

---

## 3. Files Touched

- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

Optional notes per file:

- the task doc freezes this as an analysis-only task
- the handoff records measured stage-level timing shares and optimization guidance

---

## 4. Behavior Impact

### Expected New Behavior

- no code behavior changed
- the new outcome is a stage-level latency explanation for the current local L0 path

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` was not modified
- schema was not modified
- CLI and sample-dir entry behavior were not modified

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- none

Compatibility notes:

This delivery only profiled the current path. It did not modify fields, function signatures, CLI behavior, or output contracts.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- reuse the same deterministic 50-sample mix as the prior latency task
- manually replay the current `derive_auto_labels_from_sample_dir(...)` path in stages
- measure:
  - sample I/O
  - prep
  - url/forms/network summarization
  - html feature summarization
  - brand extraction / brand consistency
  - evasion + text observability
  - specialized surface + intent + page stage
  - routing + weak-risk + language
  - rule-label derivation
- aggregate mean / median / p90 / p95 / min / max
```

### Result

All-sample stage means on the 50-sample slice:

- `sample_io_ms`: `2.515`
- `prep_ms`: `0.346`
- `url_forms_net_ms`: `0.262`
- `html_features_ms`: `53.337`
- `brand_ms`: `20.362`
- `evasion_textobs_ms`: `1.120`
- `specialized_intent_stage_ms`: `33.129`
- `routing_risk_lang_ms`: `0.682`
- `rule_labels_ms`: `0.034`
- `full_ms`: `111.786`

Mean stage-share percentages:

- `html_features_ms`: `47.71%`
- `specialized_intent_stage_ms`: `29.64%`
- `brand_ms`: `18.22%`
- `sample_io_ms`: `2.25%`
- `evasion_textobs_ms`: `1.00%`
- `routing_risk_lang_ms`: `0.61%`
- `prep_ms`: `0.31%`
- `url_forms_net_ms`: `0.23%`
- `rule_labels_ms`: `0.03%`

Per-group `full_ms` means:

- benign: `122.476 ms`
- adult: `91.185 ms`
- gambling: `100.320 ms`

Why those stages are expensive in the current code:

- `html_features`
  - `summarize_html_features(...)` scans the HTML blob for script sources, known JS library aliases, version patterns, obfuscation-like strings, captcha evidence, and download evidence
  - this stage scales with HTML payload size and repeated string scanning
- `brand`
  - `extract_claimed_brands(...)` loops through every brand and alias in the lexicon, then runs `_kw_match(...)` repeatedly against the full visible text
  - this is effectively repeated text scanning across the whole lexicon
- `specialized_intent_stage`
  - `derive_specialized_surface_signals(...)` runs many `hit_keywords(...)` passes over the same `text_low` / `url_blob`
  - gambling, adult, and gate detectors each rescan keyword families separately, and `derive_intent_signals(...)` and `derive_page_stage(...)` add more scans

Slowest outlier patterns:

- the slowest samples were mostly benign pages with large HTML and heavy brand/specialized scanning
- the top outlier `worldofprintables.com_20260402T023119Z` spent about:
  - `80.070 ms` in `html_features`
  - `159.765 ms` in `brand`
  - `225.788 ms` in `specialized_intent_stage`

### Not Run

- no implementation patch
- no repeated multi-round profiling variance study
- no hardware-isolated benchmark harness

Reason:

This task was explicitly scoped to latency-source analysis only.

---

## 7. Risks / Caveats

- this is still a local working-tree profiling snapshot, not a hardware-general benchmark statement
- stage timings were measured by replaying the current function path in a profiling script, so they are very close to the real path but still not a CPython profiler trace
- optimization savings discussed here are directional unless they are separately measured in an implementation task

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- if you want the safest latency reduction first, open an implementation task for `html_features` gating or cheap-mode narrowing inside L0
- after that, open a second task for keyword-scan consolidation inside `derive_specialized_surface_signals(...)`
- only then consider brand-stage optimization, because that stage is meaningful but also tied to useful risk evidence
