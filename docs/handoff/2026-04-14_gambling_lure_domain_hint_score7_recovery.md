# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-14-gambling-lure-domain-hint-score7-recovery`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-DOMAIN-HINT-SCORE7-RECOVERY`
- Task Title: `回收 score=7 且 domain_hint=true 的 gambling lure miss`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

这次交付只处理最窄的一档剩余 miss：

- `score = 7`
- `domain_hint = true`
- 当前仍未触发 `possible_gambling_lure`

在可复现实验切片上，这档样本只有 2 个：

- `casinoneoport.us_20260407T143903Z`
- `casinonovabase.us_20260403T100907Z`

我加了一条极窄 recovery 子句，结果是：

- 这 2 个目标页全部补回
- `ordinary_benign` 没有新增回弹
- `gambling` 总命中从 `534 / 804` 提升到 `536 / 804`

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增 `gambling_score7_domain_editorial_recovery` 窄 recovery 条件：
  - `not possible_gambling_lure_before_score`
  - `gambling_weighted_score == 7`
  - `gambling_domain_hint`
  - `gambling_editorial_context`
  - `gambling_strong_text_hits`
  - `len(gambling_text_hits) >= 3`
  - `gambling_strong_bonus_hits`
  - `not gambling_transactional_surface`
- 新增 explainability reason code：
  - `gambling_domain_editorial_score7_recovery`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- 新增 handoff：`docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

### Output / Artifact Changes

- 无新增 schema 字段
- `specialized_reason_codes` 新增一个 additive reason code

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- 对于被 `editorial:-4` 压住、但仍然满足“`domain_hint + strong_text + strong_bonus + text>=3`”的窄档博彩页，`L0` 现在会直接完成
- 这条规则不会影响一般的 `score=7` 页，也不会影响没有 `domain_hint` 的页

### Preserved Behavior

- `possible_gambling_lure` 字段名未改
- `gambling_weighted_score` / `gambling_weighted_score_reasons` 未改
- 全局 score fallback 阈值和 support 逻辑未改
- `possible_bonus_or_betting_induction` 未重写
- `adult / gate` 未改

### User-facing / CLI Impact

- none

### Output Format Impact

- `specialized_reason_codes` 里新增一个可选 reason code

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_surface_signals.specialized_reason_codes`

Compatibility notes:

这次没有新增字段、删字段、改字段名、改 CLI。
唯一新增的是一个 additive reason code，下游如果不消费它，不受影响。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- rebuild the reproducible `ordinary_benign = 800` sorted+seeded baseline
- evaluate the full `gambling = 804` pool
- isolate the target `score=7 and domain_hint=true` misses
- verify before/after recovery and benign control impact
```

### Result

Target-bucket mining before patch:

- target miss count: `2`
- target samples:
  - `casinoneoport.us_20260407T143903Z`
  - `casinonovabase.us_20260403T100907Z`
- benign non-lure pages matching the same target bucket: `0`

Before patch on the reproducible baseline:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 534 / 804`

After patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 536 / 804`

Recovered by the new reason code:

- `casinoneoport.us_20260407T143903Z`
- `casinonovabase.us_20260403T100907Z`

Benign recovered by the new reason code:

- `none`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

这条任务只针对一个极窄 bucket 做最小 patch，不需要扩大成更大范围回归。

---

## 7. Risks / Caveats

- 这条 recovery 明显带有“针对剩余样本模式”的性质，泛化范围故意收得很窄
- 还剩下的主要 miss 已不在这档 bucket 里，继续追 recall 需要看别的模式
- 当前 evaluation harness 的顺序敏感根因仍未单独修复；这次只是继续沿用 sorted baseline

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有记这条新 recovery reason code
- 如果要继续追 recall，下一条要重新定义新的目标 bucket

---

## 9. Recommended Next Step

- 现在剩余 miss 已不再集中在 `score=7 + domain_hint` 这档
- 下一条建议二选一：
  - `gambling score<4 evidence-gap mining`
  - `gambling evaluation determinism check`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-14-gambling-lure-domain-hint-score7-recovery`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-LURE-DOMAIN-HINT-SCORE7-RECOVERY`
- Task Title: `Recover score=7 and domain_hint=true gambling lure misses`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

This delivery handled only the narrowest remaining miss bucket:

- `score = 7`
- `domain_hint = true`
- still not triggering `possible_gambling_lure`

On the reproducible evaluation baseline, this bucket contained only 2 samples:

- `casinoneoport.us_20260407T143903Z`
- `casinonovabase.us_20260403T100907Z`

I added one extremely narrow recovery clause. The result is:

- both target pages are now recovered
- `ordinary_benign` did not increase
- total `gambling` hits improved from `534 / 804` to `536 / 804`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added a narrow `gambling_score7_domain_editorial_recovery` condition:
  - `not possible_gambling_lure_before_score`
  - `gambling_weighted_score == 7`
  - `gambling_domain_hint`
  - `gambling_editorial_context`
  - `gambling_strong_text_hits`
  - `len(gambling_text_hits) >= 3`
  - `gambling_strong_bonus_hits`
  - `not gambling_transactional_surface`
- added one explainability reason code:
  - `gambling_domain_editorial_score7_recovery`

### Doc Changes

- updated task: `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- added handoff: `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

### Output / Artifact Changes

- no schema fields were added
- one additive reason code was added under `specialized_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- gambling pages suppressed by `editorial:-4` but still matching the narrow pattern `domain_hint + strong_text + strong_bonus + text>=3` can now complete in `L0`
- this rule does not affect general `score=7` pages and does not affect pages without `domain_hint`

### Preserved Behavior

- the `possible_gambling_lure` field name was not changed
- `gambling_weighted_score` and `gambling_weighted_score_reasons` were not changed
- the global score fallback threshold and support logic were not changed
- `possible_bonus_or_betting_induction` was not redesigned
- `adult` and `gate` were not changed

### User-facing / CLI Impact

- none

### Output Format Impact

- one optional reason code was added under `specialized_reason_codes`

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_surface_signals.specialized_reason_codes`

Compatibility notes:

This task did not add fields, remove fields, rename fields, or change CLI.
The only additive change is one reason code; downstream consumers that ignore it remain unaffected.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- rebuild the reproducible `ordinary_benign = 800` sorted+seeded baseline
- evaluate the full `gambling = 804` pool
- isolate the target `score=7 and domain_hint=true` misses
- verify before/after recovery and benign control impact
```

### Result

Target-bucket mining before patch:

- target miss count: `2`
- target samples:
  - `casinoneoport.us_20260407T143903Z`
  - `casinonovabase.us_20260403T100907Z`
- benign non-lure pages matching the same target bucket: `0`

Before patch on the reproducible baseline:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 534 / 804`

After patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 536 / 804`

Recovered by the new reason code:

- `casinoneoport.us_20260407T143903Z`
- `casinonovabase.us_20260403T100907Z`

Benign recovered by the new reason code:

- `none`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

This task targeted one extremely narrow bucket and used a minimal patch.
It did not require broader regression work.

---

## 7. Risks / Caveats

- this recovery is intentionally pattern-specific and very narrow
- the remaining misses are no longer concentrated in this bucket, so further recall work needs a new target pattern
- the root cause of evaluation-harness order sensitivity is still not fixed separately; this task only continues using the sorted baseline

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`
- `docs/handoff/2026-04-14_gambling_lure_domain_hint_score7_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document this new recovery reason code
- if recall work continues, the next task should redefine the next target miss bucket

---

## 9. Recommended Next Step

- the remaining misses are no longer concentrated in the `score=7 + domain_hint` bucket
- the next task should be one of:
  - `gambling score<4 evidence-gap mining`
  - `gambling evaluation determinism check`
