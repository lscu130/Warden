# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-15-gambling-multilingual-title-token-recovery`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-MULTILINGUAL-TITLE-TOKEN-RECOVERY`
- Task Title: `补 multilingual title-token 的低成本 gambling recovery`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

这次交付继续补 `gambling` 的低成本证据，目标是 multilingual title-token recovery。

我最终没有做“大扩词表”，只加了一条窄的 title-only recovery：

- 只看 `page_title`
- 只看印尼系组合词
- 必须 `score < 4`
- 必须至少命中 3 个 token
- 必须包含 `togel` 或 `bandar`

这条规则的直接效果很清楚：

- `gambling_multilingual_title_token_recovery` 命中了 `10` 个赌博页
- benign 命中 `0`

当前跑出来的总量是：

- `ordinary_benign`: `12 / 800`
- `gambling`: `562 / 804`

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增 `GAMBLING_INDONESIAN_TITLE_TOKENS`
  - `togel`
  - `bandar`
  - `situs`
  - `terpercaya`
  - `resmi`
- 给 `derive_specialized_surface_signals(...)` 新增 `title_text` 输入
- multilingual recovery 改成只吃 `title_text`，不再吃 `page_title + visible_text` 混合文本
- 新增窄 recovery：
  - `gambling_multilingual_title_token_recovery`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- 新增 handoff：`docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

### Output / Artifact Changes

- 无新增 schema 字段
- `specialized_reason_codes` 新增一个 additive reason code

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- 标题里带强印尼系博彩组合词的页，现在可以在 `L0` 直接完成
- 这条恢复不看完整 HTML，不看 OCR，不看截图语义
- 这条恢复只吃 `page_title`，不会因为正文里碰巧有相关词而误抬

### Preserved Behavior

- `possible_gambling_lure` 字段名未改
- 之前的 `score7 domain_hint` recovery 未改
- 之前的 `xbet landing` recovery 未改
- `adult / gate` 未改
- `possible_bonus_or_betting_induction` 未改

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
- internal call path of `derive_specialized_surface_signals(...)`

Compatibility notes:

这次没有新增字段、删字段、改字段名、改 CLI。
`derive_specialized_surface_signals(...)` 的签名变了，但它是内部调用点，不是外部公共接口。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine multilingual title-token combinations on the reproducible baseline
- compare the target combinations against:
  - `ordinary_benign = 800`
  - `gambling = 804`
- validate the final title-only recovery patch
```

### Result

Title-token mining findings:

- benign pages with any of the target Indonesian tokens in title: `1`
- `score < 4` gambling misses with any of those tokens in title: `31`
- benign pages with `>= 3` target title tokens: `0`
- `score < 4` gambling misses with `>= 3` target title tokens: `10`

The final rule fired on:

- `gambling`: `10`
- `ordinary_benign`: `0`

Recovered gambling samples:

- `babylemonademusic.com_20260306T083346Z`
- `dolantaring.com_20260402T132541Z`
- `hermantoto1544.shop_20260326T191650Z`
- `koiturki.com_20260403T013331Z`
- `kokitotofive.com_20260407T120300Z`
- `lakupendiri.com_20260326T144427Z`
- `larisjav.com_20260407T130449Z`
- `podtoto.org_20260407T051621Z`
- `polototo7.site_20260326T144452Z`
- `toto9.monster_20260403T082840Z`

Benign recovered by the new reason code:

- `none`

Final current totals on the reproducible baseline:

- `ordinary_benign`: `12 / 800`
- `gambling`: `562 / 804`

### Not Run

- full-repo regression
- broad multilingual keyword expansion beyond the narrow title combo
- evaluation-determinism root-cause fix

Reason:

这条任务只收窄的 title-token 组合 recovery，不做更大范围的低成本扩词。

---

## 7. Risks / Caveats

- 这条 recovery 很像“高特异性 title pattern”补丁，不是通用 multilingual 赌博识别器
- 剩余 miss 仍然大量存在，尤其是：
  - 证据过少的页
  - title 不够强的页
  - 非印尼系模式的页
- evaluation harness 的顺序敏感根因还没独立修复

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有记录 `gambling_multilingual_title_token_recovery`
- 如果继续做低成本回收，下一条应明确下一个语言簇或模式边界

---

## 9. Recommended Next Step

- 如果继续追 recall，下一条建议开：
  - `gambling low-cost toto/togel host recovery`
  - 或 `gambling low-cost vietnamese title-token recovery`
- 如果先补工程质量，下一条仍建议：
  - `gambling evaluation determinism check`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-15-gambling-multilingual-title-token-recovery`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-MULTILINGUAL-TITLE-TOKEN-RECOVERY`
- Task Title: `Recover gambling misses using low-cost multilingual title-token patterns`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

This delivery continued low-cost `gambling` evidence recovery through multilingual title-token patterns.

I did not do a broad keyword expansion. I added one narrow title-only recovery:

- title-only evidence
- Indonesian token cluster only
- `score < 4`
- at least 3 target tokens
- must include `togel` or `bandar`

The direct effect is clear:

- `gambling_multilingual_title_token_recovery` fired on `10` gambling pages
- benign hits by the new reason code: `0`

Current totals on the reproducible run are:

- `ordinary_benign`: `12 / 800`
- `gambling`: `562 / 804`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `GAMBLING_INDONESIAN_TITLE_TOKENS`
  - `togel`
  - `bandar`
  - `situs`
  - `terpercaya`
  - `resmi`
- added `title_text` as an input to `derive_specialized_surface_signals(...)`
- moved multilingual recovery to title-only evidence instead of mixed `page_title + visible_text`
- added a narrow recovery:
  - `gambling_multilingual_title_token_recovery`

### Doc Changes

- updated task: `docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- added handoff: `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

### Output / Artifact Changes

- no schema fields were added
- one additive reason code was added under `specialized_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- pages whose titles carry strong Indonesian gambling token combinations can now finish in `L0`
- this recovery does not use full HTML, OCR, or screenshot semantics
- this recovery uses title-only evidence, so incidental body-text token collisions do not lift pages by themselves

### Preserved Behavior

- the `possible_gambling_lure` field name was not changed
- the prior `score7 domain_hint` recovery remains unchanged
- the prior `xbet landing` recovery remains unchanged
- `adult` and `gate` remain unchanged
- `possible_bonus_or_betting_induction` remains unchanged

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
- internal call path of `derive_specialized_surface_signals(...)`

Compatibility notes:

This task did not add fields, remove fields, rename fields, or change CLI.
The signature of `derive_specialized_surface_signals(...)` changed, but it is an internal call path, not a public external interface.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- mine multilingual title-token combinations on the reproducible baseline
- compare the target combinations against:
  - `ordinary_benign = 800`
  - `gambling = 804`
- validate the final title-only recovery patch
```

### Result

Title-token mining findings:

- benign pages with any of the target Indonesian tokens in title: `1`
- `score < 4` gambling misses with any of those tokens in title: `31`
- benign pages with `>= 3` target title tokens: `0`
- `score < 4` gambling misses with `>= 3` target title tokens: `10`

The final rule fired on:

- `gambling`: `10`
- `ordinary_benign`: `0`

Recovered gambling samples:

- `babylemonademusic.com_20260306T083346Z`
- `dolantaring.com_20260402T132541Z`
- `hermantoto1544.shop_20260326T191650Z`
- `koiturki.com_20260403T013331Z`
- `kokitotofive.com_20260407T120300Z`
- `lakupendiri.com_20260326T144427Z`
- `larisjav.com_20260407T130449Z`
- `podtoto.org_20260407T051621Z`
- `polototo7.site_20260326T144452Z`
- `toto9.monster_20260403T082840Z`

Benign recovered by the new reason code:

- `none`

Final current totals on the reproducible baseline:

- `ordinary_benign`: `12 / 800`
- `gambling`: `562 / 804`

### Not Run

- full-repo regression
- broad multilingual keyword expansion beyond the narrow title combo
- evaluation-determinism root-cause fix

Reason:

This task only landed a narrow title-token combination recovery and did not broaden low-cost keyword coverage further.

---

## 7. Risks / Caveats

- this recovery is best described as a high-specificity title-pattern patch, not a general multilingual gambling detector
- a large remaining miss set still exists, especially:
  - sparse-evidence pages
  - pages without strong titles
  - non-Indonesian patterns
- the root cause of evaluation-harness order sensitivity is still not separately fixed

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_multilingual_title_token_recovery.md`
- `docs/handoff/2026-04-15_gambling_multilingual_title_token_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document `gambling_multilingual_title_token_recovery`
- if low-cost recovery continues, the next task should explicitly freeze the next language cluster or pattern boundary

---

## 9. Recommended Next Step

- if recall work continues, the next task should be:
  - `gambling low-cost toto/togel host recovery`
  - or `gambling low-cost vietnamese title-token recovery`
- if engineering quality comes first, the next task should still be:
  - `gambling evaluation determinism check`
