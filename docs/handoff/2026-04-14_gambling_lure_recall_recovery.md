# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-14-gambling-lure-recall-recovery`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-RECALL-RECOVERY`
- Task Title: `基于 explainable score 回收 gambling lure recall`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

这次交付继续围绕 `possible_gambling_lure` 做 recall recovery，没有扩到 `adult / gate`，也没有重写 induction。

核心结论：

- 当前 weighted-score fallback 从 `10` 放宽到 `8`
- 但 support 仍然收得很窄，只允许：
  - `domain_hint`
  - `bet_digit_host`
  - `high_confidence`
  - `strong_text>=2 + transactional_surface`
- 用这条最小 patch，在可复现实验切片上把：
  - `gambling` 从 `525 / 804` 提升到 `534 / 804`
  - `ordinary_benign` 从 `11 / 800` 提升到 `12 / 800`

这是一次偏稳的 recall recovery：多回收了 9 个博彩样本，只多带起 1 个 benign 边界样本。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 将 `GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD` 从 `10` 下调到 `8`
- 新增 `gambling_score_fallback_support`，只允许这几类 support 进入 score recovery：
  - `gambling_domain_hint`
  - `gambling_bet_digit_host`
  - `gambling_high_confidence_hit`
  - `len(gambling_strong_text_hits) >= 2 and gambling_transactional_surface`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- 新增 handoff：`docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

### Output / Artifact Changes

- 无新增 schema 字段
- 变化只体现在 `possible_gambling_lure` 的内部形成逻辑

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `bet+digits host + domain_hint` 这类强结构证据页现在更容易直接留在 `L0`
- 被 `editorial:-4` 压掉、但仍带强博彩正文和交易面支撑的页，现在有更高概率被 score 补回
- fallback 仍然不是任意 `score >= 8` 就放行，必须带窄 support

### Preserved Behavior

- `possible_gambling_lure` 字段名未改
- `gambling_weighted_score` / `gambling_weighted_score_reasons` 未改
- `possible_bonus_or_betting_induction` 未重写
- `adult / gate` specialized contract 未改
- `evt_v1.2` 总体结构未改

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

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_reason_codes.gambling_weighted_score_recovery`

Compatibility notes:

这次没有新增字段、删字段、改字段名、改 CLI。
下游如果只消费字段存在性和结构，不需要改；如果依赖历史 trigger-rate 分布，需要重新看统计。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- build a reproducible benign slice by:
  - sorting directory names
  - then applying random seed `20260414`
  - then taking `800` samples
- evaluate the full gambling pool: `804`
- inspect representative recovered, still-missed, and benign-edge samples
```

### Result

Important validation note:

- this task normalized the harness to `sorted(...)` before shuffle
- the earlier weighted-scoring handoff used the same seed but not a sorted directory list
- for this task, all before/after comparisons use the reproducible sorted baseline

Reproducible baseline before patch:

- `ordinary_benign`: `possible_gambling_lure = 11 / 800`
- `gambling`: `possible_gambling_lure = 525 / 804`
- true `gambling_weighted_score_recovery = 12 / 804`

Final after patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 534 / 804`
- true `gambling_weighted_score_recovery = 21 / 804`

Net change on the reproducible baseline:

- benign: `+1`
- gambling: `+9`
- true score recoveries: `+9`

Representative recovered samples:

- `bet36511.vip_20260101T111002Z`
  - score: `9`
  - reasons: `bet_digit_host:+5`, `domain_hint:+4`
  - now recovered
- `betking.com_20260327T020942Z`
  - score: `8`
  - reasons include `domain_hint`, `strong_text`, `transactional`, `editorial:-4`
  - now recovered

Representative still-missed samples:

- `casinoneoport.us_20260407T143903Z`
  - score: `7`
  - still below threshold
- `casinonovabase.us_20260403T100907Z`
  - score: `7`
  - still below threshold
- `exch-market.in_20260413T092146Z`
  - score: `7`
  - no domain hint / host hint / high-confidence support

Benign edge sample added by this patch:

- `fruitparty-slot.com_20260325T175621Z`
  - score: `9`
  - recovered via `domain_hint + url_hit + text/bet surface`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

这条任务只做 `gambling lure` recall recovery，并用同一套可复现切片做前后对比，没有扩成更大范围回归。

---

## 7. Risks / Caveats

- 这次放宽阈值后，确实多带起了 1 个 benign 边界样本 `fruitparty-slot.com`
- 剩余的主要 miss 现在集中在 `score = 7` 这档
- 其中有两类：
  - 有 `domain_hint`，但被 `editorial:-4` 压住
  - 没有 `domain_hint` / `high_confidence` / `bet_digit_host`，虽然正文很博彩，但 support 不够
- 当前任务没有处理 evaluation harness 的根因级顺序敏感问题，只是把本次对比统一到 sorted baseline

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有明确写入 fallback 阈值从 `10` 到 `8` 的当前实现口径
- evaluation harness 的顺序敏感问题，后续应单独记录或修复

---

## 9. Recommended Next Step

- 如果继续追 recall，下一条建议只盯 `score = 7` 且 `domain_hint = true` 的剩余 miss
- 如果要先补工程质量，下一条建议单开 `gambling evaluation determinism check`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-14-gambling-lure-recall-recovery`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-RECALL-RECOVERY`
- Task Title: `Recover gambling lure recall using the explainable score baseline`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

This delivery continued working on `possible_gambling_lure` recall only. It did not expand into `adult / gate`, and it did not redesign induction.

Core result:

- the weighted-score fallback threshold was relaxed from `10` to `8`
- but fallback support stayed narrow and only allows:
  - `domain_hint`
  - `bet_digit_host`
  - `high_confidence`
  - `strong_text>=2 + transactional_surface`
- with this minimal patch, on the reproducible evaluation baseline:
  - `gambling` improved from `525 / 804` to `534 / 804`
  - `ordinary_benign` moved from `11 / 800` to `12 / 800`

This is a conservative recall-recovery round: 9 more gambling samples were recovered at the cost of 1 additional benign edge sample.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- lowered `GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD` from `10` to `8`
- added `gambling_score_fallback_support`, limiting score recovery to these support types:
  - `gambling_domain_hint`
  - `gambling_bet_digit_host`
  - `gambling_high_confidence_hit`
  - `len(gambling_strong_text_hits) >= 2 and gambling_transactional_surface`

### Doc Changes

- updated task: `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- added handoff: `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

### Output / Artifact Changes

- no schema fields were added
- the change is limited to the internal formation logic of `possible_gambling_lure`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- pages with strong structural evidence such as `bet+digits host + domain_hint` are now more likely to finish in `L0`
- pages that were suppressed by `editorial:-4` but still carry strong gambling text and transactional support are now more likely to be recovered by score
- fallback is still not a plain `score >= 8` rule; narrow support is still required

### Preserved Behavior

- the `possible_gambling_lure` field name was not changed
- `gambling_weighted_score` and `gambling_weighted_score_reasons` were not changed
- `possible_bonus_or_betting_induction` was not redesigned
- the `adult` and `gate` specialized contracts were not changed
- the overall `evt_v1.2` structure was not changed

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

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_reason_codes.gambling_weighted_score_recovery`

Compatibility notes:

This change did not add fields, remove fields, rename fields, or change CLI.
Downstream consumers that rely on field structure do not need code changes.
Downstream consumers that rely on prior trigger-rate distributions should revisit the stats.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- build a reproducible benign slice by:
  - sorting directory names
  - then applying random seed `20260414`
  - then taking `800` samples
- evaluate the full gambling pool: `804`
- inspect representative recovered, still-missed, and benign-edge samples
```

### Result

Important validation note:

- this task normalized the harness to `sorted(...)` before shuffle
- the earlier weighted-scoring handoff used the same seed but not a sorted directory list
- for this task, all before/after comparisons use the reproducible sorted baseline

Reproducible baseline before patch:

- `ordinary_benign`: `possible_gambling_lure = 11 / 800`
- `gambling`: `possible_gambling_lure = 525 / 804`
- true `gambling_weighted_score_recovery = 12 / 804`

Final after patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 534 / 804`
- true `gambling_weighted_score_recovery = 21 / 804`

Net change on the reproducible baseline:

- benign: `+1`
- gambling: `+9`
- true score recoveries: `+9`

Representative recovered samples:

- `bet36511.vip_20260101T111002Z`
  - score: `9`
  - reasons: `bet_digit_host:+5`, `domain_hint:+4`
  - now recovered
- `betking.com_20260327T020942Z`
  - score: `8`
  - reasons include `domain_hint`, `strong_text`, `transactional`, and `editorial:-4`
  - now recovered

Representative still-missed samples:

- `casinoneoport.us_20260407T143903Z`
  - score: `7`
  - still below threshold
- `casinonovabase.us_20260403T100907Z`
  - score: `7`
  - still below threshold
- `exch-market.in_20260413T092146Z`
  - score: `7`
  - lacks domain, host, or high-confidence support

Benign edge sample added by this patch:

- `fruitparty-slot.com_20260325T175621Z`
  - score: `9`
  - recovered via `domain_hint + url_hit + text/bet surface`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

This task only targeted `gambling lure` recall recovery and compared before/after on one reproducible evaluation slice.
It did not expand into broader regression work.

---

## 7. Risks / Caveats

- the relaxed threshold does add 1 benign edge sample: `fruitparty-slot.com`
- the remaining main miss bucket is now concentrated at `score = 7`
- those misses split into two groups:
  - pages with `domain_hint` that are still suppressed by `editorial:-4`
  - pages with strong gambling text but without domain, host, or high-confidence support
- this task did not solve the root cause of order sensitivity in the evaluation harness; it only normalized this comparison onto a sorted baseline

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_lure_recall_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_recall_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document the current fallback threshold change from `10` to `8`
- the evaluation-harness order-sensitivity issue should be documented or fixed in a separate task

---

## 9. Recommended Next Step

- if you want to keep pushing recall, the next task should isolate the remaining `score = 7` misses where `domain_hint = true`
- if you want to improve engineering quality first, the next task should be `gambling evaluation determinism check`
