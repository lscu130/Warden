# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-16-adult-false-positive-tightening`
- Related Task ID: `TASK-L0-2026-04-16-ADULT-FALSE-POSITIVE-TIGHTENING`
- Task Title: `压缩 adult 误触并收紧当前策略`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-16`
- Status: `DONE`

---

## 1. Executive Summary

这次交付先处理了当前 `adult` 在 ordinary benign 上的误触，再验证对当前 adult 池的召回影响。

核心收口是：

- 把 `nsfw`、`av`、`erotic`、`nude`、`nudity`、`anal` 视为弱 adult 文本信号
- 把 `nsfw`、`age verification`、`adult only`、`not safe for work` 视为弱 age-gate 信号
- 要求这些弱信号默认必须和更强 adult 上下文一起出现，才进入 `possible_adult_lure` 或 `possible_age_gate_surface`

在同一批当前样本上的同口径 before/after 对比里：

- adult recall proxy 保持不变：`481 / 580 = 82.93%`
- ordinary benign 上的 adult false positives：`182 -> 144`
- precision proxy：`72.55% -> 76.96%`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added weak adult-signal sets:
  - `ADULT_WEAK_TEXT_KEYWORDS`
  - `ADULT_WEAK_URL_KEYWORDS`
  - `ADULT_WEAK_AGE_GATE_KEYWORDS`
- tightened adult triggering so weak adult text and weak age-gate wording no longer trigger adult surfaces on their own

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- added `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Output / Artifact Changes

- `possible_adult_lure` is now stricter for weak adult wording on ordinary benign pages
- `possible_age_gate_surface` is now stricter for weak age-gate wording
- no schema fields were added or removed

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

---

## 4. Behavior Impact

### Expected New Behavior

- weak content-rating cues like `nsfw` and weak adult abbreviations like `av` no longer trigger `possible_adult_lure` by themselves
- weaker adult-description terms like `erotic`, `nude`, `nudity`, and `anal` now require stronger adult context before contributing to adult-surface detection
- `possible_age_gate_surface` now ignores weak age-gate wording unless stronger adult support is also present

### Preserved Behavior

- strong adult pages with high-confidence adult wording, strong adult text density, or strong URL evidence still trigger adult surfaces
- current `gambling` and `gate` logic was not changed
- current CLI and schema remain unchanged

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

- `specialized_surface_signals.possible_adult_lure`
- `specialized_surface_signals.possible_age_gate_surface`
- `l0_routing_hints.need_vision_candidate`

Compatibility notes:

This change tightens existing adult detection behavior without renaming any fields or changing output structure. Downstream consumers should expect fewer weak adult hits on ordinary benign pages, but the field names and interfaces are unchanged.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine current adult false-positive patterns from `E:\Warden\data\raw\benign\benign`
- compare trigger-path categories across:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- rerun current adult / ordinary-benign quantification after the patch
- run a same-pool old-vs-new comparison on the current roots
```

### Result

Current dominant benign-side false-positive modes before the patch:

- `text_ge2`: `92`
- `high_confidence_text`: `50`
- `text_plus_age_gate`: `38`
- `url_hit`: `2`

High-noise signals identified before the patch:

- weak text-side signals with poor adult-vs-benign separation:
  - `nsfw`
  - `av`
  - `erotic`
  - `nude`
  - `nudity`
  - `anal`
- weak age-gate signals with poor separation:
  - `nsfw`
  - `age verification`
  - `adult only`
  - `not safe for work`

Same-pool before/after comparison on the current roots:

- adult pool:
  - old `possible_adult_lure`: `481 / 580`
  - new `possible_adult_lure`: `481 / 580`
  - old `possible_age_gate_surface`: `222 / 580`
  - new `possible_age_gate_surface`: `220 / 580`
- ordinary benign pool:
  - old `possible_adult_lure`: `182 / 16339`
  - new `possible_adult_lure`: `144 / 16339`
  - old `possible_age_gate_surface`: `92 / 16339`
  - new `possible_age_gate_surface`: `56 / 16339`

Proxy metrics on the same current pools:

- precision proxy:
  - `72.55% -> 76.96%`
- recall proxy:
  - `82.93% -> 82.93%`

Representative benign-side drops:

- `9gag.com_20260401T064843Z` with `nsfw`
- `distrowatch.com_20260325T093100Z` with `av` + `age verification`
- `addic7ed.com_20260414T093019Z` with `erotic` + `av`
- `fann.sk_20260407T020947Z` with `anal` + `nude`

### Not Run

- a full mixed-batch regression across adult / gambling / gate / benign
- any screenshot- or OCR-based adult analysis
- any gate or gambling retuning

Reason:

This task was scoped to low-cost adult tightening only.

---

## 7. Risks / Caveats

- the ordinary-benign pool still appears to contain some adult-like pages, so the proxy precision remains a noisy lower bound rather than a clean gold-label precision
- tightening weak adult wording improves benign precision, but it may still miss edge adult pages that rely only on weak descriptors
- this task did not rebalance `gate` or `gambling`, so cross-vertical consistency work is still separate

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- inspect the remaining `144` benign adult hits and split them into likely pool contamination vs true rule noise
- if you want higher precision next, tighten the remaining high-noise adult tokens further only where adult recall stays stable
- after adult stabilizes, move to the `gate` contract and tightening path

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-16-adult-false-positive-tightening`
- Related Task ID: `TASK-L0-2026-04-16-ADULT-FALSE-POSITIVE-TIGHTENING`
- Task Title: `Tighten adult false positives and refine the current strategy`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-16`
- Status: `DONE`

---

## 1. Executive Summary

This delivery first handled the current `adult` false positives on ordinary benign pages, then measured the recall impact on the current adult pool.

The core tightening is:

- treat `nsfw`, `av`, `erotic`, `nude`, `nudity`, and `anal` as weak adult text signals
- treat `nsfw`, `age verification`, `adult only`, and `not safe for work` as weak age-gate signals
- require those weak signals to appear with stronger adult context before they can contribute to `possible_adult_lure` or `possible_age_gate_surface`

On a same-pool before/after comparison over the current sample roots:

- adult recall proxy stayed unchanged: `481 / 580 = 82.93%`
- ordinary-benign adult false positives went from `182 -> 144`
- precision proxy improved from `72.55% -> 76.96%`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added weak adult-signal sets:
  - `ADULT_WEAK_TEXT_KEYWORDS`
  - `ADULT_WEAK_URL_KEYWORDS`
  - `ADULT_WEAK_AGE_GATE_KEYWORDS`
- tightened adult triggering so weak adult text and weak age-gate wording no longer trigger adult surfaces on their own

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- added `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Output / Artifact Changes

- `possible_adult_lure` is now stricter for weak adult wording on ordinary benign pages
- `possible_age_gate_surface` is now stricter for weak age-gate wording
- no schema fields were added or removed

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

---

## 4. Behavior Impact

### Expected New Behavior

- weak content-rating cues like `nsfw` and weak adult abbreviations like `av` no longer trigger `possible_adult_lure` by themselves
- weaker adult-description terms like `erotic`, `nude`, `nudity`, and `anal` now require stronger adult context before contributing to adult-surface detection
- `possible_age_gate_surface` now ignores weak age-gate wording unless stronger adult support is also present

### Preserved Behavior

- strong adult pages with high-confidence adult wording, strong adult text density, or strong URL evidence still trigger adult surfaces
- current `gambling` and `gate` logic was not changed
- current CLI and schema remain unchanged

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

- `specialized_surface_signals.possible_adult_lure`
- `specialized_surface_signals.possible_age_gate_surface`
- `l0_routing_hints.need_vision_candidate`

Compatibility notes:

This change tightens existing adult detection behavior without renaming any fields or changing output structure. Downstream consumers should expect fewer weak adult hits on ordinary benign pages, but the field names and interfaces are unchanged.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine current adult false-positive patterns from `E:\Warden\data\raw\benign\benign`
- compare trigger-path categories across:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- rerun current adult / ordinary-benign quantification after the patch
- run a same-pool old-vs-new comparison on the current roots
```

### Result

Current dominant benign-side false-positive modes before the patch:

- `text_ge2`: `92`
- `high_confidence_text`: `50`
- `text_plus_age_gate`: `38`
- `url_hit`: `2`

High-noise signals identified before the patch:

- weak text-side signals with poor adult-vs-benign separation:
  - `nsfw`
  - `av`
  - `erotic`
  - `nude`
  - `nudity`
  - `anal`
- weak age-gate signals with poor separation:
  - `nsfw`
  - `age verification`
  - `adult only`
  - `not safe for work`

Same-pool before/after comparison on the current roots:

- adult pool:
  - old `possible_adult_lure`: `481 / 580`
  - new `possible_adult_lure`: `481 / 580`
  - old `possible_age_gate_surface`: `222 / 580`
  - new `possible_age_gate_surface`: `220 / 580`
- ordinary benign pool:
  - old `possible_adult_lure`: `182 / 16339`
  - new `possible_adult_lure`: `144 / 16339`
  - old `possible_age_gate_surface`: `92 / 16339`
  - new `possible_age_gate_surface`: `56 / 16339`

Proxy metrics on the same current pools:

- precision proxy:
  - `72.55% -> 76.96%`
- recall proxy:
  - `82.93% -> 82.93%`

Representative benign-side drops:

- `9gag.com_20260401T064843Z` with `nsfw`
- `distrowatch.com_20260325T093100Z` with `av` + `age verification`
- `addic7ed.com_20260414T093019Z` with `erotic` + `av`
- `fann.sk_20260407T020947Z` with `anal` + `nude`

### Not Run

- a full mixed-batch regression across adult / gambling / gate / benign
- any screenshot- or OCR-based adult analysis
- any gate or gambling retuning

Reason:

This task was scoped to low-cost adult tightening only.

---

## 7. Risks / Caveats

- the ordinary-benign pool still appears to contain some adult-like pages, so the proxy precision remains a noisy lower bound rather than a clean gold-label precision
- tightening weak adult wording improves benign precision, but it may still miss edge adult pages that rely only on weak descriptors
- this task did not rebalance `gate` or `gambling`, so cross-vertical consistency work is still separate

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-16_adult_false_positive_tightening.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- inspect the remaining `144` benign adult hits and split them into likely pool contamination vs true rule noise
- if you want higher precision next, tighten the remaining high-noise adult tokens further only where adult recall stays stable
- after adult stabilizes, move to the `gate` contract and tightening path
