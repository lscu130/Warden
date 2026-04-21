# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-14-gambling-score-lt4-low-cost-evidence-gap-mining`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-SCORE-LT4-LOW-COST-EVIDENCE-GAP-MINING`
- Task Title: `挖 score<4 的 gambling miss，并只补低成本 L0 证据`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

这次交付只做 `score < 4` 的低成本 evidence-gap mining，不碰重证据。

先说结论：

- `score < 4` 的剩余 miss 里，最大的低成本可补模式不是“再扫更多内容”
- 最干净的一档是 `1xbet / 1xbt` affiliate-landing pattern
- 我只对这档做了一个窄 recovery patch

结果在可复现实验切片上是：

- `ordinary_benign`: `12 / 800 -> 12 / 800`
- `gambling`: `536 / 804 -> 544 / 804`

也就是：

- benign 没有回弹
- 赌博样本额外补回了 `8` 个

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增一个极窄的低成本 recovery 条件：
  - `not possible_gambling_lure_before_score`
  - `gambling_weighted_score == 2`
  - `gambling_transactional_surface`
  - text 里包含 `1xbet`
  - URL blob 里包含 `1xbt` 或 `1xbet`
- 新增 explainability reason code：
  - `gambling_xbet_landing_recovery`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- 新增 handoff：`docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

### Output / Artifact Changes

- 无新增 schema 字段
- `specialized_reason_codes` 里新增一个 additive reason code

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `1xbet / 1xbt` 这类低成本 affiliate / landing 页，现在只要同时带：
  - `transactional_surface`
  - title/text 中的 `1xbet`
  - URL/path 中的 `1xbt` 或 `1xbet`
  就会被直接补成 `possible_gambling_lure`

### Preserved Behavior

- 没有扩大到完整 HTML、OCR、截图语义
- 没有改 `adult / gate`
- 没有重写 `possible_bonus_or_betting_induction`
- 全局 score 阈值和之前的 recovery 逻辑未改

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
只有一个 additive reason code；不消费它的下游不受影响。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine `score < 4` gambling misses on the reproducible baseline
- compare low-cost host / URL / title patterns
- validate the narrow `1xbet / 1xbt` recovery rule on:
  - `ordinary_benign = 800`
  - `gambling = 804`
```

### Result

Low-cost mining findings:

- `score < 4` gambling miss count: `222`
- the cleanest low-cost subgroup was:
  - `1xbet / 1xbt` title-or-path pattern with `transactional_surface`
- this subgroup size in `score < 4` gambling misses: `8`
- this subgroup size in the benign control slice: `0`

Before patch on the reproducible baseline:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 536 / 804`

After patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 544 / 804`

Recovered by the new reason code:

- `7000-landing.com_l_687a7dbc10e46e6ab1083af9_20260401T005621Z`
- `7000-landings.com_l_68b3f4ade511822d3306a79f_20260403T013311Z`
- `7000partpromo.com_l_687a7dbc10e46e6ab1083af9_20260402T124250Z`
- `7kpartners-best.com_1xbt_20260403T013320Z`
- `fastthemegaplay.com_landingpages_1xbt_20260408T014625Z`
- `sevenkpartners.com_l_687a7dbc10e46e6ab1083af9_20260330T150052Z`
- `totalbestpromo.com_l_687a7dbc10e46e6ab1083af9_20260203T120747Z`
- `totalbestpromo.com_landingpages_1xbt_20260131T140308Z`

Benign recovered by the new reason code:

- `none`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- broad multilingual keyword expansion

Reason:

这条任务的目标是先找最干净的低成本模式并做最小 patch，不是把全部 `score<4` miss 一次性清完。

---

## 7. Risks / Caveats

- 这次补回的是一个非常窄的 `1xbet / 1xbt` 子模式，不代表 `score<4` 的主问题已经解决
- 其余大部分 `score<4` miss 仍然是证据过少、或词表覆盖不足
- multilingual title 词表还有可扩空间，但这次故意没直接大扩，避免把 benign 一起带起来

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有记录 `gambling_xbet_landing_recovery`
- 如果继续做低成本回收，下一条要单独冻结“多语种 title 词表扩展”的边界

---

## 9. Recommended Next Step

- 如果继续追 recall，下一条建议开：
  - `gambling multilingual title-token recovery`
- 如果先补工程质量，下一条建议还是：
  - `gambling evaluation determinism check`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-14-gambling-score-lt4-low-cost-evidence-gap-mining`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-SCORE-LT4-LOW-COST-EVIDENCE-GAP-MINING`
- Task Title: `Mine score<4 gambling misses and add only low-cost L0 evidence`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

This delivery handled `score < 4` evidence-gap mining using low-cost evidence only. It did not introduce heavy evidence.

The conclusion is straightforward:

- the strongest low-cost recoverable subgroup in the remaining `score < 4` misses was not “read more content”
- the cleanest subgroup was a narrow `1xbet / 1xbt` affiliate-landing pattern
- I implemented only that narrow recovery patch

Results on the reproducible evaluation baseline:

- `ordinary_benign`: `12 / 800 -> 12 / 800`
- `gambling`: `536 / 804 -> 544 / 804`

So:

- no benign regression
- 8 additional gambling samples were recovered

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added one extremely narrow low-cost recovery condition:
  - `not possible_gambling_lure_before_score`
  - `gambling_weighted_score == 2`
  - `gambling_transactional_surface`
  - `1xbet` present in text
  - `1xbt` or `1xbet` present in the URL blob
- added one explainability reason code:
  - `gambling_xbet_landing_recovery`

### Doc Changes

- updated task: `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- added handoff: `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

### Output / Artifact Changes

- no schema fields were added
- one additive reason code was added under `specialized_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `1xbet / 1xbt` affiliate or landing pages can now be directly recovered as `possible_gambling_lure` when they carry:
  - `transactional_surface`
  - `1xbet` in text/title
  - `1xbt` or `1xbet` in URL/path

### Preserved Behavior

- no expansion into full HTML, OCR, or screenshot semantics
- no changes to `adult` or `gate`
- no redesign of `possible_bonus_or_betting_induction`
- the global score threshold and prior recovery logic remain unchanged

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
The only additive change is one reason code; downstream consumers that ignore it are unaffected.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine `score < 4` gambling misses on the reproducible baseline
- compare low-cost host / URL / title patterns
- validate the narrow `1xbet / 1xbt` recovery rule on:
  - `ordinary_benign = 800`
  - `gambling = 804`
```

### Result

Low-cost mining findings:

- `score < 4` gambling miss count: `222`
- the cleanest low-cost subgroup was:
  - `1xbet / 1xbt` title-or-path pattern with `transactional_surface`
- subgroup size in `score < 4` gambling misses: `8`
- subgroup size in the benign control slice: `0`

Before patch on the reproducible baseline:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 536 / 804`

After patch:

- `ordinary_benign`: `possible_gambling_lure = 12 / 800`
- `gambling`: `possible_gambling_lure = 544 / 804`

Recovered by the new reason code:

- `7000-landing.com_l_687a7dbc10e46e6ab1083af9_20260401T005621Z`
- `7000-landings.com_l_68b3f4ade511822d3306a79f_20260403T013311Z`
- `7000partpromo.com_l_687a7dbc10e46e6ab1083af9_20260402T124250Z`
- `7kpartners-best.com_1xbt_20260403T013320Z`
- `fastthemegaplay.com_landingpages_1xbt_20260408T014625Z`
- `sevenkpartners.com_l_687a7dbc10e46e6ab1083af9_20260330T150052Z`
- `totalbestpromo.com_l_687a7dbc10e46e6ab1083af9_20260203T120747Z`
- `totalbestpromo.com_landingpages_1xbt_20260131T140308Z`

Benign recovered by the new reason code:

- `none`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- broad multilingual keyword expansion

Reason:

This task aimed to find the cleanest low-cost subgroup and implement one minimal patch, not to clear the entire `score < 4` miss bucket in one pass.

---

## 7. Risks / Caveats

- this patch only recovers one very narrow `1xbet / 1xbt` subgroup and does not solve the broader `score < 4` problem
- most remaining `score < 4` misses are still caused by sparse evidence or missing keyword coverage
- multilingual title-token expansion still has room, but this task intentionally did not broaden keyword coverage yet in order to avoid benign regression

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`
- `docs/handoff/2026-04-14_gambling_score_lt4_low_cost_evidence_gap_mining.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document `gambling_xbet_landing_recovery`
- if low-cost recall work continues, the next task should explicitly freeze the boundary for multilingual title-token expansion

---

## 9. Recommended Next Step

- if recall work continues, the next task should be:
  - `gambling multilingual title-token recovery`
- if engineering quality comes first, the next task should still be:
  - `gambling evaluation determinism check`
