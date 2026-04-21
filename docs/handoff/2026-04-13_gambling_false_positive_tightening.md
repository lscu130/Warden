# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: `2026-04-13-gambling-false-positive-tightening`
- Related Task ID: `TASK-L0-2026-04-13-GAMBLING-FALSE-POSITIVE-TIGHTENING`
- Task Title: `收紧 gambling false positive，聚焦普通内容站和 affiliate/news 页面`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-13`
- Status: `DONE`

---

## 1. Executive Summary

这次交付专门收紧 `gambling` specialized detector 的误触发，范围只限 `gambling`。  
核心动作有三件：

- 去掉把普通内容站表单误当成赌博交易面的逻辑
- 把赌博导购 / 评测 / 资讯页明确压到编辑态抑制路径
- 补一个更窄的 host-level gambling domain hint，回收真实赌博站点的召回

最终固定切片结果：

- `ordinary_benign` 400 样本里，`possible_gambling_lure` 从 `15` 降到 `3`
- `gambling` 200 样本里，`possible_gambling_lure` 从 `138` 变为 `132`

这轮 tradeoff 明显偏向降低普通内容页误触发，但没有改 schema，也没有碰 `adult / gate` 契约。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 收紧 `GAMBLING_ACTION_KEYWORDS`，去掉 `deposit / withdraw / customer service / online service` 这类容易在资讯页出现的动作词
- 新增 `has_gambling_domain_hint(...)`，直接从 host token 提取窄域名赌博提示
- 调整 `gambling_transactional_surface`：
  - 不再使用 `form_count > 0`
  - 改为依赖 `has_sensitive_form` 或 `action_hits + domain/strong support`
- 调整 `gambling_editorial_context`：
  - 对高编辑态页面做显式抑制
- 调整 `possible_gambling_lure`：
  - 不再由任意 `gambling_url_hits` 直接触发
  - 改为依赖高置信文本、交易面、或更窄的 domain hint 组合

### Doc Changes

- 更新 task：`docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- 新增 handoff：`docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- `L0_DESIGN_V1.md` 未修改；这轮只是 trigger tuning，没有改契约字段和语义边界

### Output / Artifact Changes

- 输出 schema 无变化
- 变化只体现在 `possible_gambling_lure` 的触发行为

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: 只改 `gambling` specialized trigger，不碰 `adult / gate`
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`: 仅将状态更新为 `DONE`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`: 记录实现、回归和当前触发策略

---

## 4. Behavior Impact

### Expected New Behavior

- 普通资讯站、博彩评测页、SEO 聚合页不再因为 `deposit / withdrawal / payout / search form / download app` 这类弱词或普通表单被轻易打成 `possible_gambling_lure`
- `casino.guide`、`zamsino`、`modernline`、`solitaire.org` 这类代表误触发页，现在不会再打出 `possible_gambling_lure`
- `gbetclub.io`、`premierbet.co.ao`、`thescore.bet`、`5500bet.com`、`wjcasino.com`、`pinnbet.rs` 这类真实赌博域名页，现在可以通过 host-level domain hint 回收命中

### Preserved Behavior

- `possible_bonus_or_betting_induction` 仍然保留，内容型赌博资讯页仍可能打出这个弱信号
- `adult` / `gate` specialized trigger 未修改
- `evt_v1.2` 字段集合和现有函数调用方式未修改

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
- `specialized_surface_signals.possible_bonus_or_betting_induction`
- `specialized_surface_signals.matched_keywords`

Compatibility notes:

这次没有新增字段、删除字段、改字段名、改 CLI 或改函数签名。  
变化只在 `possible_gambling_lure` 的内部形成逻辑。下游如果依赖的是字段存在性和输出结构，不需要改。  
下游如果依赖的是旧的触发率分布，需要重新看统计。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- inspect representative benign false positives:
  - `casino.guide_20260402T011614Z`
  - `zamsino.com_20260326T125628Z`
  - `modernline.us_20260325T153055Z`
  - `solitaire.org_20260410T033750Z`
  - `sportszion.com_20260413T020813Z`
- inspect representative gambling recovery samples:
  - `gbetclub.io_20260326T190910Z`
  - `premierbet.co.ao_20260326T045734Z`
  - `thescore.bet_20260408T072233Z`
  - `5500bet.com_20260325T182307Z`
  - `wjcasino.com_20260407T131953Z`
  - `pinnbet.rs_20260407T120003Z`

PowerShell heredoc piped to `python -`:
- rerun fixed-slice regression
- `ordinary_benign` sample size: `400`
- `gambling` sample size: `200`
- random seed: `20260413`
```

### Result

- Python 语法检查通过
- 代表 benign false-positive 样本现在都不再触发 `possible_gambling_lure`
- 代表赌博站点样本中，`gbetclub / premierbet / thescore.bet / 5500bet / wjcasino / pinnbet` 已恢复命中
- 固定切片结果：
  - pre-final-patch baseline:
    - `ordinary_benign`: `15 / 400`
    - `gambling`: `138 / 200`
  - final patch:
    - `ordinary_benign`: `3 / 400`
    - `gambling`: `132 / 200`
- 仍然命中的 `ordinary_benign` 3 个样本是：
  - `live4d2u.net_20260326T073921Z`
  - `oranum.com_20260330T045511Z`
  - `brfcs.com_20260403T085010Z`

### Not Run

- 全量仓库回归
- 之前 `3 x 200 mixed batches` 的整套重跑
- 人工金标复审

Reason:

这条任务只要求 `gambling` false-positive tightening。  
这次验证已经覆盖代表样本和固定随机切片，但没有再重跑更大的全量回归或人工复核流程。

---

## 7. Risks / Caveats

- `gambling` 200 切片命中率从 `138` 降到 `132`，有可见召回代价
- 剩余 miss 里还有一批带赌博 host 的弱文本页，后续如果继续回收，容易把 SEO / affiliate 页重新带回来
- `possible_bonus_or_betting_induction` 仍然偏宽，资讯页和导购页依然可能打这个弱信号

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 里还没有展开写这轮更细的 `gambling` editorial-vs-landing trigger 细节
- 如果后续继续调 `possible_bonus_or_betting_induction`，需要单独开 task 和记录新的统计

---

## 9. Recommended Next Step

- 单开一条 `gambling induction narrowing`，专门收紧 `possible_bonus_or_betting_induction`
- 对当前 `ordinary_benign` 仅剩的 3 个命中样本做人工复核，判断它们是残余误触发还是本来就应保留的赌博表面页
- 下一次大回归时，把这轮 `gambling` 规则放回 `3 x 200 mixed batches` 重新量化整体影响

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-13-gambling-false-positive-tightening`
- Related Task ID: `TASK-L0-2026-04-13-GAMBLING-FALSE-POSITIVE-TIGHTENING`
- Task Title: `Tighten gambling false positives with a focus on ordinary content sites and affiliate/news pages`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-13`
- Status: `DONE`

---

## 1. Executive Summary

This delivery tightened `gambling` specialized-detector false positives, with scope restricted to `gambling` only.  
The implementation made three concrete changes:

- removed logic that treated ordinary content-site forms as gambling-transaction evidence
- pushed gambling guide / review / news pages into an explicit editorial-suppression path
- added a narrower host-level gambling-domain hint to recover true gambling-site recall

Final fixed-slice results:

- in `ordinary_benign` 400 samples, `possible_gambling_lure` dropped from `15` to `3`
- in `gambling` 200 samples, `possible_gambling_lure` moved from `138` to `132`

This tradeoff clearly favors reducing ordinary-content false positives, while leaving schema unchanged and avoiding any changes to the `adult` or `gate` contracts.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- tightened `GAMBLING_ACTION_KEYWORDS` by removing weak action terms such as `deposit`, `withdraw`, `customer service`, and `online service`, which often appear on editorial pages
- added `has_gambling_domain_hint(...)` to extract a narrow host-level gambling-domain hint directly from host tokens
- changed `gambling_transactional_surface`:
  - it no longer uses `form_count > 0`
  - it now depends on `has_sensitive_form` or `action_hits + domain/strong support`
- changed `gambling_editorial_context`:
  - high-editorial pages now go through an explicit suppression path
- changed `possible_gambling_lure`:
  - arbitrary `gambling_url_hits` no longer trigger it directly
  - it now depends on high-confidence text, transactional evidence, or narrower domain-hint combinations

### Doc Changes

- updated task doc: `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- added handoff doc: `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`
- `L0_DESIGN_V1.md` was not updated; this round only tuned trigger behavior and did not change contract fields or semantic boundaries

### Output / Artifact Changes

- no output-schema change
- the change is limited to `possible_gambling_lure` trigger behavior

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: changed `gambling` specialized trigger only; did not touch `adult` or `gate`
- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`: updated status to `DONE`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`: records implementation, regression results, and the current trigger strategy

---

## 4. Behavior Impact

### Expected New Behavior

- ordinary news pages, gambling-review pages, and SEO aggregation pages no longer fire `possible_gambling_lure` as easily because of weak terms such as `deposit`, `withdrawal`, `payout`, search forms, or `download app`
- representative false-positive pages such as `casino.guide`, `zamsino`, `modernline`, and `solitaire.org` no longer emit `possible_gambling_lure`
- representative true gambling-domain pages such as `gbetclub.io`, `premierbet.co.ao`, `thescore.bet`, `5500bet.com`, `wjcasino.com`, and `pinnbet.rs` are recovered through the host-level domain hint path

### Preserved Behavior

- `possible_bonus_or_betting_induction` is still preserved, so content-oriented gambling information pages may still emit that weak signal
- `adult` and `gate` specialized triggers were not changed
- the `evt_v1.2` field set and existing function call shapes were not changed

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
- `specialized_surface_signals.possible_bonus_or_betting_induction`
- `specialized_surface_signals.matched_keywords`

Compatibility notes:

This round did not add fields, remove fields, rename fields, change CLI flags, or change function signatures.  
The only change is the internal formation logic of `possible_gambling_lure`. Downstream consumers that rely on field presence or output structure do not need code changes.  
Downstream consumers that rely on prior trigger-rate distributions should revisit their statistics.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- inspect representative benign false positives:
  - `casino.guide_20260402T011614Z`
  - `zamsino.com_20260326T125628Z`
  - `modernline.us_20260325T153055Z`
  - `solitaire.org_20260410T033750Z`
  - `sportszion.com_20260413T020813Z`
- inspect representative gambling recovery samples:
  - `gbetclub.io_20260326T190910Z`
  - `premierbet.co.ao_20260326T045734Z`
  - `thescore.bet_20260408T072233Z`
  - `5500bet.com_20260325T182307Z`
  - `wjcasino.com_20260407T131953Z`
  - `pinnbet.rs_20260407T120003Z`

PowerShell heredoc piped to `python -`:
- rerun fixed-slice regression
- `ordinary_benign` sample size: `400`
- `gambling` sample size: `200`
- random seed: `20260413`
```

### Result

- Python syntax check passed
- representative benign false-positive pages no longer emit `possible_gambling_lure`
- representative gambling-domain pages `gbetclub`, `premierbet`, `thescore.bet`, `5500bet`, `wjcasino`, and `pinnbet` now emit `possible_gambling_lure`
- fixed-slice results:
  - pre-final-patch baseline:
    - `ordinary_benign`: `15 / 400`
    - `gambling`: `138 / 200`
  - final patch:
    - `ordinary_benign`: `3 / 400`
    - `gambling`: `132 / 200`
- the remaining `ordinary_benign` hits are:
  - `live4d2u.net_20260326T073921Z`
  - `oranum.com_20260330T045511Z`
  - `brfcs.com_20260403T085010Z`

### Not Run

- full-repo regression
- a full rerun of the previous `3 x 200 mixed batches`
- manual gold-label review

Reason:

This task only required `gambling` false-positive tightening.  
The validation here covers representative samples and fixed random slices, but it does not rerun larger full-repo evaluations or manual-review workflows.

---

## 7. Risks / Caveats

- the `gambling` 200-sample slice still dropped from `138` to `132`, so there is a visible recall cost
- some remaining misses are weak-text pages on gambling-looking hosts; pushing further recall recovery could easily reintroduce SEO / affiliate false positives
- `possible_bonus_or_betting_induction` is still broad, so informational and review pages may still emit that weak signal

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-13_gambling_false_positive_tightening.md`
- `docs/handoff/2026-04-13_gambling_false_positive_tightening.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet spell out the finer editorial-vs-landing trigger details from this gambling tuning round
- if `possible_bonus_or_betting_induction` is tuned next, that work should get its own task doc and new stats

---

## 9. Recommended Next Step

- open a dedicated `gambling induction narrowing` task to tighten `possible_bonus_or_betting_induction`
- manually review the remaining 3 `ordinary_benign` hits to determine whether they are residual false positives or intentional gambling-surface keeps
- in the next larger regression pass, rerun the earlier `3 x 200 mixed batches` with this gambling logic to quantify broader impact
