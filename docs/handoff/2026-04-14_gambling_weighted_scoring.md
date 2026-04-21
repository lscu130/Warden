# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-14-gambling-weighted-scoring`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-WEIGHTED-SCORING`
- Task Title: `分析 gambling 特征区分度，并实现 explainable weighted score`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

这次交付把 `gambling` specialized detector 从纯布尔组合往“可解释的加权证据”方向推进了一步。

核心做法有两部分：

- 先用真实样本统计 `URL / host / text / bonus / editorial` 证据的区分度
- 再把区分度高的证据做成一个低成本、可解释的 `gambling_weighted_score`

当前结论很明确：

- `high_confidence`、`domain_hint`、`bet+digits host`、`strong text` 是强正向证据
- `editorial context`、`bonus_without_text` 是有效负向证据
- 泛化动作词本身区分力弱，不适合单独抬高博彩判断

这次没有把 weighted score 变成新的主判定器。它现在承担两件事：

- 给 `L0` 输出更可解释的量化证据
- 在保守阈值下，补回一小批被布尔规则漏掉但博彩证据足够强的页面

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增一组 explainable gambling score 常量：
  - `GAMBLING_SCORE_HIGH_CONFIDENCE = 8`
  - `GAMBLING_SCORE_BET_DIGIT_HOST = 5`
  - `GAMBLING_SCORE_DOMAIN_HINT = 4`
  - `GAMBLING_SCORE_URL_HIT = 2`
  - `GAMBLING_SCORE_TEXT_GE2 = 2`
  - `GAMBLING_SCORE_TEXT_GE3 = 1`
  - `GAMBLING_SCORE_TRANSACTIONAL = 2`
  - `GAMBLING_SCORE_EDITORIAL_SUPPRESSION = -4`
  - `GAMBLING_SCORE_BONUS_WITHOUT_TEXT = -3`
  - `GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD = 10`
- 新增 `has_bet_digit_host_pattern(final_url)`，用于抓 `bet36511.vip` 这类 host pattern
- 在 `derive_specialized_surface_signals(...)` 里新增 `gambling_weighted_score` 及原因分解
- `possible_gambling_lure` 新增一个保守 fallback：
  - 只有当 `score >= 10`
  - 且同时有 `domain_hint`、`bet_digit_host`、`high_confidence` 之一
  - 才允许 score 把页面补成 `possible_gambling_lure`
- `gambling_weighted_score_recovery` 已收紧为真正的 recovery 语义：
  - 只有 score 实际把页面从 `False` 拉成 `True` 时才输出

### Doc Changes

- 更新 task：`docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- 新增 handoff：`docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- 同时修复了 task 中文区块的乱码，避免继续把坏编码留在仓库里

### Output / Artifact Changes

- `specialized_surface_signals` 新增：
  - `gambling_weighted_score`
  - `gambling_weighted_score_reasons`
- 这是 additive schema change，没有删字段、改字段名、改 CLI

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `gambling` 判断现在会同时产出一个可解释分数，而不是只给布尔结果
- URL / host 级证据的权重高于正文弱词
- `bonus` 这类弱词如果没有正文博彩证据，会被负向项压制
- 一小批具备强博彩结构证据、但没有穿过旧布尔逻辑的页面，现在会被 score 保守补回

### Preserved Behavior

- `possible_gambling_lure` 仍是现有字段，没有改名
- `possible_bonus_or_betting_induction` 字段仍保留，逻辑未在本任务内重写
- `adult` / `gate` specialized contract 未改
- `evt_v1.2` 总体结构未改

### User-facing / CLI Impact

- none

### Output Format Impact

- `specialized_surface_signals` 新增 2 个可选字段

---

## 5. Schema / Interface Impact

- Schema changed: `YES`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.gambling_weighted_score`
- `specialized_surface_signals.gambling_weighted_score_reasons`
- `specialized_reason_codes.gambling_weighted_score_recovery`

Compatibility notes:

这次是 additive 变更。旧字段都还在，旧调用方式也不需要改。
下游如果只读既有字段，不会被破坏；下游如果愿意，可以开始消费 score 和 reason list 做更细的分析。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- analyze feature separability on:
  - ordinary benign: 800 samples
  - gambling pool: 804 samples
- sweep score thresholds on the same pools
- inspect representative benign and gambling samples
- quantify final lure / induction / score hit-rates on the same pools
```

### Result

Feature separability on `ordinary_benign = 800` vs `gambling = 804`:

- `high_confidence`
  - benign: `0.0013`
  - gambling: `0.4204`
  - lift: `336.32`
- `domain_hint`
  - benign: `0.0125`
  - gambling: `0.2674`
  - lift: `21.39`
- `bet_digit_host`
  - benign: `0.0000`
  - gambling: `0.0883`
- `strong_text_ge1`
  - benign: `0.0100`
  - gambling: `0.5012`
  - lift: `50.12`
- `text_ge2`
  - benign: `0.0563`
  - gambling: `0.4241`
  - lift: `7.54`
- `transactional_surface`
  - benign: `0.1113`
  - gambling: `0.4104`
  - lift: `3.69`
- `editorial_ge2`
  - benign: `0.5363`
  - gambling: `0.1368`
  - lift: `0.26`
- `bonus_without_text`
  - benign: `0.0462`
  - gambling: `0.0211`
  - lift: `0.46`

Current score-threshold sweep on the same pools:

- `score >= 7`
  - benign: `8 / 800`
  - gambling: `447 / 804`
- `score >= 8`
  - benign: `6 / 800`
  - gambling: `419 / 804`
- `score >= 9`
  - benign: `6 / 800`
  - gambling: `386 / 804`
- `score >= 10`
  - benign: `5 / 800`
  - gambling: `371 / 804`

Current post-change pool quantification:

- `possible_gambling_lure`
  - benign: `11 / 800`
  - gambling: `513 / 804`
- `possible_bonus_or_betting_induction`
  - benign: `12 / 800`
  - gambling: `196 / 804`
- true `gambling_weighted_score_recovery`
  - benign: `0 / 800`
  - gambling: `12 / 804`

Representative samples:

- benign
  - `macquarie.com.au_20260403T050232Z`
    - lure: `False`
    - induction: `False`
    - score: `-7`
    - reasons: `editorial:-4`, `bonus_without_text:-3`
- gambling
  - `21luckybets.net_20260326T131611Z`
    - lure: `True`
    - score: `11`
    - true score-recovery path
  - `casino.guide_20260402T011614Z`
    - lure: `True`
    - score: `16`
  - `download1xbet.com_20260413T092342Z`
    - lure: `True`
    - score: `14`
  - `bet36511.vip_20260101T111002Z`
    - lure: `False`
    - score: `9`
    - below conservative fallback threshold

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

本任务目标是解释型 score 建模与一轮定量验证，不是仓库级回归清场。

---

## 7. Risks / Caveats

- 这版 weighted score 目前更适合做 explainability 和保守 recovery，不适合直接替代全部布尔逻辑
- `slotscapital.org` 这类域名会被保守 fallback 拉起；这说明 URL / host 权重确实强，但也意味着 host 级误导仍需继续看
- 当前 score 主要针对 `possible_gambling_lure`，并没有解决 `possible_bonus_or_betting_induction` 的 recall 平衡问题
- 这次只量化了 `gambling` 对 `ordinary benign` 的区分，没有同步扩到 `adult / gate`

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有记录 `gambling_weighted_score` 这两个 explainability 输出
- 如果后续决定把 score 提升为更核心的 L0 完成条件，需要补正式 contract

---

## 9. Recommended Next Step

- 先用这套 score 对当前博彩样本再做一轮“增量恢复样本”清单，只看真正被 score 补回的页面
- 再决定要不要把 `possible_bonus_or_betting_induction` 也改成类似的 explainable weighted path
- 如果目标是让更多高特征博彩页留在 `L0` 完成，下一条应做 `gambling lure recall recovery with score-guided tuning`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-14-gambling-weighted-scoring`
- Related Task ID: `TASK-L0-2026-04-14-GAMBLING-WEIGHTED-SCORING`
- Task Title: `Analyze gambling feature separability and implement an explainable weighted score`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-14`
- Status: `DONE`

---

## 1. Executive Summary

This delivery moved the `gambling` specialized detector one step away from pure boolean composition and toward explainable weighted evidence.

The work had two parts:

- quantify feature separability on real gambling and ordinary-benign samples
- convert the strongest evidence buckets into a low-cost, explainable `gambling_weighted_score`

The outcome is clear:

- `high_confidence`, `domain_hint`, `bet+digits host`, and `strong text` are strong positive evidence
- `editorial context` and `bonus_without_text` are useful negative evidence
- generic action words are weak by themselves and should not heavily raise gambling confidence

The weighted score does not replace the main boolean detector.
It currently serves two purposes:

- provide a more quantitative and explainable L0 output
- conservatively recover a small set of pages whose gambling evidence is strong but that were missed by the previous boolean combinations

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added a set of explainable gambling score constants:
  - `GAMBLING_SCORE_HIGH_CONFIDENCE = 8`
  - `GAMBLING_SCORE_BET_DIGIT_HOST = 5`
  - `GAMBLING_SCORE_DOMAIN_HINT = 4`
  - `GAMBLING_SCORE_URL_HIT = 2`
  - `GAMBLING_SCORE_TEXT_GE2 = 2`
  - `GAMBLING_SCORE_TEXT_GE3 = 1`
  - `GAMBLING_SCORE_TRANSACTIONAL = 2`
  - `GAMBLING_SCORE_EDITORIAL_SUPPRESSION = -4`
  - `GAMBLING_SCORE_BONUS_WITHOUT_TEXT = -3`
  - `GAMBLING_SCORE_LURE_FALLBACK_THRESHOLD = 10`
- added `has_bet_digit_host_pattern(final_url)` to capture host patterns such as `bet36511.vip`
- added `gambling_weighted_score` and explicit score-reason breakdown inside `derive_specialized_surface_signals(...)`
- added a conservative fallback path for `possible_gambling_lure`:
  - only when `score >= 10`
  - and at least one of `domain_hint`, `bet_digit_host`, or `high_confidence_hit` is present
- tightened `gambling_weighted_score_recovery` to true recovery semantics:
  - the reason code is emitted only when the score actually changes the page from `False` to `True`

### Doc Changes

- updated task: `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- added handoff: `docs/handoff/2026-04-14_gambling_weighted_scoring.md`
- repaired the corrupted Chinese task section so the repo does not keep carrying that broken encoding forward

### Output / Artifact Changes

- added two fields under `specialized_surface_signals`:
  - `gambling_weighted_score`
  - `gambling_weighted_score_reasons`
- this is an additive schema change only; no field removals, field renames, or CLI changes

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `gambling` detection now emits an explainable score in addition to the boolean result
- URL / host evidence carries more weight than weak body-text terms
- weak `bonus` terms without gambling-text support are explicitly penalized
- a small set of pages with strong gambling structure but missed by the old boolean logic can now be conservatively recovered by score

### Preserved Behavior

- `possible_gambling_lure` remains the existing field and is not renamed
- `possible_bonus_or_betting_induction` is preserved and was not redesigned in this task
- the `adult` and `gate` specialized contracts were not changed
- the overall `evt_v1.2` structure was not changed

### User-facing / CLI Impact

- none

### Output Format Impact

- `specialized_surface_signals` now includes 2 additional optional fields

---

## 5. Schema / Interface Impact

- Schema changed: `YES`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.gambling_weighted_score`
- `specialized_surface_signals.gambling_weighted_score_reasons`
- `specialized_reason_codes.gambling_weighted_score_recovery`

Compatibility notes:

This is an additive change only.
All prior fields remain present and existing calling patterns remain valid.
Downstream readers that only consume the old fields should continue to work unchanged.
Downstream readers that want more granular analysis can start consuming the score and reason list.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- analyze feature separability on:
  - ordinary benign: 800 samples
  - gambling pool: 804 samples
- sweep score thresholds on the same pools
- inspect representative benign and gambling samples
- quantify final lure / induction / score hit-rates on the same pools
```

### Result

Feature separability on `ordinary_benign = 800` vs `gambling = 804`:

- `high_confidence`
  - benign: `0.0013`
  - gambling: `0.4204`
  - lift: `336.32`
- `domain_hint`
  - benign: `0.0125`
  - gambling: `0.2674`
  - lift: `21.39`
- `bet_digit_host`
  - benign: `0.0000`
  - gambling: `0.0883`
- `strong_text_ge1`
  - benign: `0.0100`
  - gambling: `0.5012`
  - lift: `50.12`
- `text_ge2`
  - benign: `0.0563`
  - gambling: `0.4241`
  - lift: `7.54`
- `transactional_surface`
  - benign: `0.1113`
  - gambling: `0.4104`
  - lift: `3.69`
- `editorial_ge2`
  - benign: `0.5363`
  - gambling: `0.1368`
  - lift: `0.26`
- `bonus_without_text`
  - benign: `0.0462`
  - gambling: `0.0211`
  - lift: `0.46`

Current score-threshold sweep on the same pools:

- `score >= 7`
  - benign: `8 / 800`
  - gambling: `447 / 804`
- `score >= 8`
  - benign: `6 / 800`
  - gambling: `419 / 804`
- `score >= 9`
  - benign: `6 / 800`
  - gambling: `386 / 804`
- `score >= 10`
  - benign: `5 / 800`
  - gambling: `371 / 804`

Current post-change pool quantification:

- `possible_gambling_lure`
  - benign: `11 / 800`
  - gambling: `513 / 804`
- `possible_bonus_or_betting_induction`
  - benign: `12 / 800`
  - gambling: `196 / 804`
- true `gambling_weighted_score_recovery`
  - benign: `0 / 800`
  - gambling: `12 / 804`

Representative samples:

- benign
  - `macquarie.com.au_20260403T050232Z`
    - lure: `False`
    - induction: `False`
    - score: `-7`
    - reasons: `editorial:-4`, `bonus_without_text:-3`
- gambling
  - `21luckybets.net_20260326T131611Z`
    - lure: `True`
    - score: `11`
    - true score-recovery path
  - `casino.guide_20260402T011614Z`
    - lure: `True`
    - score: `16`
  - `download1xbet.com_20260413T092342Z`
    - lure: `True`
    - score: `14`
  - `bet36511.vip_20260101T111002Z`
    - lure: `False`
    - score: `9`
    - below the conservative fallback threshold

### Not Run

- full-repo regression
- rerun of the earlier `3 x 200 mixed batches`
- manual gold-label review

Reason:

This task targeted explainable score construction and one quantitative validation round.
It was not intended to close out repo-wide regression work.

---

## 7. Risks / Caveats

- the current weighted score is better suited for explainability and conservative recovery than for fully replacing the boolean detector
- domains such as `slotscapital.org` can still be lifted by host-weighted evidence; that is useful signal, but it also means host-level noise still needs continued review
- this score currently strengthens `possible_gambling_lure` only and does not solve the recall balance problem for `possible_bonus_or_betting_induction`
- this quantification focused on gambling vs ordinary benign and did not extend to `adult` or `gate`

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-14_gambling_weighted_scoring.md`
- `docs/handoff/2026-04-14_gambling_weighted_scoring.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document the two new gambling explainability outputs
- if the score is later promoted into a more central L0 completion rule, a formal contract update will still be needed

---

## 9. Recommended Next Step

- first generate an incremental-recovery list using this score, restricted to pages that were truly recovered by score
- then decide whether `possible_bonus_or_betting_induction` should also move toward an explainable weighted path
- if the goal is to keep more high-feature gambling pages completed in `L0`, the next task should be `gambling lure recall recovery with score-guided tuning`
