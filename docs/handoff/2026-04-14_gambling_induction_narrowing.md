# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: `2026-04-14-gambling-induction-narrowing`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-INDUCTION-NARROWING`
- Task Title: `收紧 possible_bonus_or_betting_induction，并完成一轮量化`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

这次交付只处理 `possible_bonus_or_betting_induction`。  
核心改动是把它从“任意 bonus 词命中就触发”收紧成“bonus 词 + 赌博上下文/落地页支撑”。

固定切片结果：

- `ordinary_benign` 400 样本：`36 -> 3`
- `gambling` 200 样本：`145 -> 54`

误触发下降非常明显，但代价也很明确：`gambling` 侧的 induction 命中率掉得很大。  
这次还顺手修复了脚本里被误解码弄坏的常量块；这部分是恢复性修复，不是新的功能扩 scope。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增 `GAMBLING_STRONG_BONUS_KEYWORDS`
- 调整 `possible_bonus_or_betting_induction` 形成逻辑：
  - 纯 `bonus / promotion / cashback / deposit / withdrawal / payout` 不再单独触发
  - 现在要求 `bonus_hits` 同时带下列支撑之一：
    - `possible_gambling_lure`
    - `gambling_domain_hint + strong_bonus_hits`
    - `strong_bonus_hits + (strong_text_hits or action_hits)`
- editorial 抑制改成更窄版本：
  - 有赌博域名支撑时，不会被 editorial 抑制直接压掉
- 修复了常量块和内建 brand lexicon 的编码损坏，恢复脚本可编译状态

### Doc Changes

- 更新 task：`docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- 新增 handoff：`docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- `L0_DESIGN_V1.md` 未修改；这轮没有改字段契约和阶段语义

### Output / Artifact Changes

- 输出 schema 无变化
- 变化只体现在 `possible_bonus_or_betting_induction` 的触发行为

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: 包含 induction 逻辑收紧，以及一次恢复性编码修复
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`: 仅将状态更新为 `DONE`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`: 记录这轮 trigger 变化和量化结果

---

## 4. Behavior Impact

### Expected New Behavior

- 普通内容页现在不会再因为单独出现 `bonus / promotion / cashback / deposit / withdrawal / payout` 就触发 `possible_bonus_or_betting_induction`
- 博彩资讯/affiliate/SEO 页如果只有讲解语义，没有落地页支撑，也更难再触发 induction
- 带真实赌博域名支撑且带强 bonus 话术的页面，仍可触发 induction
- `download1xbet.com` 这类有 host 支撑 + 强 bonus 话术的样本现在可以保留 induction

### Preserved Behavior

- `possible_gambling_lure` 字段集合和字段名未改
- `adult` / `gate` specialized contract 未改
- `evt_v1.2` 输出结构未改

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

- `specialized_surface_signals.possible_bonus_or_betting_induction`
- `specialized_surface_signals.matched_keywords`

Compatibility notes:

这次没有新增字段、删字段、改字段名、改 CLI、改函数签名。  
变化只在 `possible_bonus_or_betting_induction` 的内部形成逻辑。  
下游如果依赖字段存在性和输出结构，不需要改。下游如果依赖旧的 induction 触发率分布，需要重新看统计。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- inspect representative benign induction false positives:
  - `macquarie.com.au_20260403T050232Z`
  - `tower-rush.org_20260402T164731Z`
  - `cbssports.com_20260327T032849Z`
  - `vegasparlor.us_20260403T092519Z`
- inspect representative gambling samples:
  - `download1xbet.com_20260413T092342Z`
  - `msport.com_20260326T031207Z`
  - `eliteslots.ro_20260407T144932Z`
  - `m.51570066.com_20260317T075129Z`

PowerShell heredoc piped to `python -`:
- run fixed-slice quantification
- `ordinary_benign` sample size: `400`
- `gambling` sample size: `200`
- random seed: `20260414`
```

### Result

- Python 语法检查通过
- 代表 benign induction false positives 现在都不再触发：
  - `macquarie`
  - `tower-rush`
  - `cbssports`
  - `vegasparlor`
- 代表 gambling 样本：
  - `download1xbet` 触发 induction
  - `msport` 触发 induction
  - `eliteslots` 触发 induction
  - `m.51570066.com` 不触发 induction，因为没有 bonus 命中
- fixed-slice 结果：
  - baseline:
    - `ordinary_benign`: `36 / 400`
    - `gambling`: `145 / 200`
  - final:
    - `ordinary_benign`: `3 / 400`
    - `gambling`: `54 / 200`
- 最终剩余的 `ordinary_benign` induction 命中样本：
  - `wayan62.com_20260330T071457Z`
  - `onenote.com_20260327T035500Z`
  - `slotsbeatbuzz.co.uk_20260407T115126Z`

### Not Run

- 全量仓库回归
- `3 x 200 mixed batches` 重跑
- 人工金标复审

Reason:

这条任务只要求收紧 induction 字段并做一轮量化。  
本次验证覆盖了代表样本 smoke 和固定随机切片，没有扩到更大规模回归。

---

## 7. Risks / Caveats

- 这轮收得很干净，但 `gambling` 侧 induction 命中率从 `145` 掉到 `54`，代价很大
- 当前结果更像“高 precision 版本”的 induction，不再像之前那样偏 recall
- 这次包含了一次恢复性编码修复；虽然脚本已重新可编译，但后续如果继续改这份文件，建议避免再用会改写整文件编码的 PowerShell 文本写法

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有展开写 induction 的强弱 bonus 分层规则
- 如果要继续调这个字段，下一条任务需要先明确 induction 是偏 precision 还是偏 recall

---

## 9. Recommended Next Step

- 先不要继续细调，先决定 `possible_bonus_or_betting_induction` 的目标定位到底偏 recall 还是偏 precision
- 如果要保留现在的低误触发方向，下一条就专看剩余 3 个 benign hit
- 如果要回收赌博侧 induction，下一条就单独做 `gambling induction recall recovery`，只看当前 `145 -> 54` 掉掉的那批页

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-14-gambling-induction-narrowing`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-INDUCTION-NARROWING`
- Task Title: `Tighten possible_bonus_or_betting_induction and run one quantification round`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

This delivery handled `possible_bonus_or_betting_induction` only.  
The core change was to tighten it from “any bonus-related term triggers it” into “bonus terms plus gambling-context or landing-page support”.

Fixed-slice results:

- `ordinary_benign` 400 samples: `36 -> 3`
- `gambling` 200 samples: `145 -> 54`

False positives dropped sharply, but the cost is explicit: induction hit-rate on the gambling slice also dropped sharply.  
This round also included a recovery repair for a mis-decoded constant block in the script; that part was a restoration fix, not new feature scope.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `GAMBLING_STRONG_BONUS_KEYWORDS`
- changed the formation logic of `possible_bonus_or_betting_induction`:
  - plain `bonus`, `promotion`, `cashback`, `deposit`, `withdrawal`, and `payout` no longer trigger it by themselves
  - the field now requires `bonus_hits` plus one of:
    - `possible_gambling_lure`
    - `gambling_domain_hint + strong_bonus_hits`
    - `strong_bonus_hits + (strong_text_hits or action_hits)`
- narrowed editorial suppression:
  - pages with real gambling-domain support are no longer suppressed automatically by editorial-context logic
- repaired the corrupted constant block and built-in brand lexicon so the script compiles again

### Doc Changes

- updated task doc: `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- added handoff doc: `docs/handoff/2026-04-14_gambling_induction_narrowing.md`
- `L0_DESIGN_V1.md` was not updated; this round did not change field contracts or stage semantics

### Output / Artifact Changes

- no output-schema change
- the change is limited to `possible_bonus_or_betting_induction` trigger behavior

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: includes the induction tightening plus a recovery encoding fix
- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`: updated status to `DONE`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`: records trigger changes and quantification results

---

## 4. Behavior Impact

### Expected New Behavior

- ordinary content pages no longer emit `possible_bonus_or_betting_induction` just because they contain `bonus`, `promotion`, `cashback`, `deposit`, `withdrawal`, or `payout`
- gambling-news, affiliate, and SEO pages with explanatory content but no landing-page support are much less likely to emit induction
- pages with real gambling-domain support plus strong bonus language can still emit induction
- samples such as `download1xbet.com` now keep induction through the host-support path

### Preserved Behavior

- the `possible_gambling_lure` field set and field names were not changed
- the `adult` and `gate` specialized contracts were not changed
- the `evt_v1.2` output structure was not changed

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

- `specialized_surface_signals.possible_bonus_or_betting_induction`
- `specialized_surface_signals.matched_keywords`

Compatibility notes:

This round did not add fields, remove fields, rename fields, change CLI, or change function signatures.  
The only behavior change is the internal formation logic of `possible_bonus_or_betting_induction`.  
Downstream consumers that rely on field presence or output shape do not need code changes. Downstream consumers that rely on the prior induction trigger-rate distribution should revisit their stats.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- inspect representative benign induction false positives:
  - `macquarie.com.au_20260403T050232Z`
  - `tower-rush.org_20260402T164731Z`
  - `cbssports.com_20260327T032849Z`
  - `vegasparlor.us_20260403T092519Z`
- inspect representative gambling samples:
  - `download1xbet.com_20260413T092342Z`
  - `msport.com_20260326T031207Z`
  - `eliteslots.ro_20260407T144932Z`
  - `m.51570066.com_20260317T075129Z`

PowerShell heredoc piped to `python -`:
- run fixed-slice quantification
- `ordinary_benign` sample size: `400`
- `gambling` sample size: `200`
- random seed: `20260414`
```

### Result

- Python syntax check passed
- representative benign induction false positives no longer emit induction:
  - `macquarie`
  - `tower-rush`
  - `cbssports`
  - `vegasparlor`
- representative gambling samples:
  - `download1xbet` emits induction
  - `msport` emits induction
  - `eliteslots` emits induction
  - `m.51570066.com` does not emit induction because there is no bonus hit
- fixed-slice results:
  - baseline:
    - `ordinary_benign`: `36 / 400`
    - `gambling`: `145 / 200`
  - final:
    - `ordinary_benign`: `3 / 400`
    - `gambling`: `54 / 200`
- remaining `ordinary_benign` induction hits:
  - `wayan62.com_20260330T071457Z`
  - `onenote.com_20260327T035500Z`
  - `slotsbeatbuzz.co.uk_20260407T115126Z`

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

This task only required tightening the induction field and running one quantification pass.  
The validation here covers representative sample smoke checks and fixed random slices, but it does not expand to larger full-repo regressions.

---

## 7. Risks / Caveats

- this round is much cleaner on false positives, but the gambling-side induction hit-rate dropped from `145` to `54`, which is a large cost
- the current outcome is closer to a high-precision induction variant than a recall-oriented one
- this round included a recovery encoding fix; the script compiles again, but future edits to this file should avoid whole-file PowerShell text rewrites that can rewrite encoding

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_induction_narrowing.md`
- `docs/handoff/2026-04-14_gambling_induction_narrowing.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet describe the strong-vs-weak bonus split for induction
- if this field is tuned further, the next task should first freeze whether induction is meant to optimize for precision or recall

---

## 9. Recommended Next Step

- do not keep tuning blindly; first decide whether `possible_bonus_or_betting_induction` is meant to optimize for recall or precision
- if you want to keep the current low-false-positive direction, the next task should focus on the remaining 3 benign hits
- if you want to recover gambling-side induction, the next task should be a dedicated `gambling induction recall recovery` pass over the pages that dropped in the `145 -> 54` reduction
