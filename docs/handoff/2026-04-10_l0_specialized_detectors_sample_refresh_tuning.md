# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-10-l0-specialized-detectors-sample-refresh-tuning
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SAMPLE-REFRESH-TUNING
- Task Title: 基于补充样本继续优化 L0 gambling / adult / gate specialized triggers
- Module: Inference
- Author: Codex
- Date: 2026-04-13
- Status: DONE

---

## 1. Executive Summary

本次交付基于补充后的 `gambling / adult / gate` 样本，继续收紧并补强了 L0 specialized trigger 逻辑。  
实现上，重点做了三件事：

- 给 keyword matching 补了轻量 normalization，解决弯引号、省略号等文本变体带来的漏检
- 给 `gate` 增加了更强的 challenge / verification 文本覆盖，并把触发条件收紧到“强语义命中”或“带文本支撑的 runtime support”
- 给 `gambling` / `adult` 补了补充样本里高频出现的多语种和高显著词，改善单页纯文本触发

验证上，除了代表样本 smoke，还跑了三批混合回归。每批 200，`ordinary benign` 固定占 `20%`，其余由 `gambling / adult / gate` 均分。  
结果显示：

- `adult` 主信号在混合回归中稳定在 `87.4%`
- `gambling` 主信号在混合回归中稳定在 `81.5%`
- `gate` 主信号提升到 `62.9%`
- `adult` / `gambling` 的 cross-gate 误触发已基本清掉
- `ordinary benign` 上的 `possible_gate_or_evasion` 降到 `0.8%`

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 给 `_kw_match(...)` 增加轻量文本 normalization，统一处理弯引号、全角空格、省略号和长横线
- 扩展 `GATE_SURFACE_KEYWORDS` 与 `GATE_STRONG_KEYWORDS`，覆盖 `human check`、`not a robot`、`verify you're not a bot`、`please wait while your request is being verified`、`请稍候`、`正在验证您的请求` 等真实 gate 话术
- 收紧 `possible_gate_or_evasion` / `possible_challenge_surface` 形成条件，去掉“裸 `captcha_present_candidate` 就打 gate”的路径
- 扩展 `GAMBLING_KEYWORDS` / `GAMBLING_HIGH_CONFIDENCE_KEYWORDS`，补入 `bet365`、`slot`、`投注`、`彩票`、`真人`、`棋牌`、`捕鱼`、`线路中心`
- 扩展 `ADULT_KEYWORDS` / `ADULT_HIGH_CONFIDENCE_KEYWORDS`，补入 `theporndude`、`91porn`、`порно`、`成人社区`、`约炮`、`口交`、`内射`、`啪啪`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- 新增 handoff：`docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- 未修改 `L0_DESIGN_V1.md`，因为本次没有改 contract 字段集合和阶段语义

### Output / Artifact Changes

- `specialized_surface_signals` 字段集合未变化
- `l0_routing_hints` 字段集合未变化
- 新增的是这轮 tuned implementation 与 mixed-batch regression 结果

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: 只调整 `gambling / adult / gate` 相关关键词与 specialized trigger 逻辑
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`: 仅将状态更新为 `DONE`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`: 记录本次实现与三批混合回归结果

---

## 4. Behavior Impact

### Expected New Behavior

- `gate` 现在优先依赖强 verification / challenge 文本，或“文本支撑 + provider/runtime support”，不再因为普通站点嵌了 captcha/turnstile 就直接命中 gate
- `adult` 和 `gambling` 对补充样本里的中文、俄文和高显著品牌词覆盖更好，单页纯文本样本更容易打出主 specialized signal
- `adult` / `gambling` 样本上的 gate cross-trigger 显著下降

### Preserved Behavior

- 仍只保留三类 specialized families：`gambling`、`adult`、`gate`
- 没有重新引入 `possible_fake_verification` 或 `possible_interaction_required`
- `evt_v1.2` contract、CLI 调用方式、输出字段名、routing-hint 字段名都未变化

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

本次只调整已有弱信号形成逻辑，没有新增字段、删字段、改字段名，也没有修改函数签名、CLI 参数或输出路径。  
下游如果依赖的是字段存在性或 schema version，不需要改。  
下游如果依赖的是具体触发率或 reason path，则行为会变化，这是预期的 detector tuning 影响。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir`
- run representative smoke on refreshed gate / adult / gambling / benign samples
- print `specialized_surface_signals` and `l0_routing_hints`

PowerShell heredoc piped to `python -`:
- run 3 mixed regression batches with seeds:
  - `20260413`
  - `20260414`
  - `20260415`
- per batch size: `200`
- composition per batch:
  - `gambling`: `54`
  - `adult`: `53`
  - `gate`: `53`
  - `ordinary_benign`: `40`
- summarize trigger rates for:
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
```

### Result

- 语法检查通过
- 代表样本 smoke 表现符合预期：
  - 新增 gate 文本模式可命中 `yktex.cn...`、`ycj.rhn...`、`www.tragetlocax...`
  - `yuvideos.com...` 和 `autoscout24.pl...` 不再被 gate 误触发
  - `avjb.com...` 能稳定打出 `possible_adult_lure`
  - `1036m.com...`、`0140.ee...`、`1777sz.com...` 能稳定打出 `possible_gambling_lure`
- 三批混合回归 aggregate 结果：
  - `gambling`:
    - `possible_gambling_lure`: `81.5%`
    - `possible_bonus_or_betting_induction`: `71.6%`
    - `possible_gate_or_evasion`: `0.6%`
  - `adult`:
    - `possible_adult_lure`: `87.4%`
    - `possible_age_gate_surface`: `39.6%`
    - `possible_gate_or_evasion`: `0.6%`
  - `gate`:
    - `possible_gate_or_evasion`: `62.9%`
    - `possible_challenge_surface`: `62.9%`
  - `ordinary_benign`:
    - `possible_gambling_lure`: `3.3%`
    - `possible_adult_lure`: `1.7%`
    - `possible_gate_or_evasion`: `0.8%`

### Not Run

- 全量仓库全样本回归
- 人工金标校验
- 任何训练或部署流程

Reason:

本次任务只要求基于补充样本继续做 detector tuning 和 regression validation，没有要求重跑完整数据集或训练流程。

---

## 7. Risks / Caveats

- `gate` 虽然明显提升，但 mixed-batch aggregate 仍只有 `62.9%`，剩余漏检样本大多 `matched_keywords` 全空，说明还有一批 gate 页面没有稳定文本证据
- `ordinary_benign` 上的 `gambling` 误触发仍有 `3.3%`，主要来自博彩资讯、联盟页或带博彩术语的内容站
- `adult` 仍有一批 miss 只打出单个弱词，如 `milf`、`bdsm`、`xxx`，当前规则没有把这类单弱词直接升级为主 adult signal

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

Doc debt still remaining:

- 如果后续继续调 gate，建议补一份专门的 false-negative pattern note
- 如果后续继续压 gambling false positive，建议补一份博彩资讯 / affiliate 页面误触发说明

---

## 9. Recommended Next Step

- 单开一条 `gate FN mining` 任务，专门处理 `matched_keywords` 全空的 gate 漏检页
- 单开一条 `gambling false-positive tightening` 任务，压普通资讯站和 affiliate 内容页的博彩误触发
- 若后续要继续提升 adult recall，可单独评估“单高显著 adult 词是否足够升级为主信号”

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-10-l0-specialized-detectors-sample-refresh-tuning
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SAMPLE-REFRESH-TUNING
- Task Title: Continue optimizing L0 gambling/adult/gate specialized triggers using the supplemented samples
- Module: Inference
- Author: Codex
- Date: 2026-04-13
- Status: DONE

---

## 1. Executive Summary

This delivery further tuned the L0 `gambling` / `adult` / `gate` specialized triggers against the supplemented sample pools.  
The implementation focused on three concrete changes:

- adding lightweight text normalization to keyword matching so curly quotes, ellipses, and similar text variants stop causing avoidable misses
- expanding `gate` challenge / verification text coverage while tightening gate formation to require either strong semantics or runtime/provider support that is backed by text
- expanding `gambling` / `adult` keyword coverage with multilingual and high-salience terms repeatedly observed in the refreshed samples

Validation included representative smoke checks plus three mixed regression batches. Each batch size was 200, with `ordinary_benign` fixed at `20%` and the remaining `80%` split across `gambling` / `adult` / `gate`.  
The mixed-batch aggregate results showed:

- `adult` main-signal recall at `87.4%`
- `gambling` main-signal recall at `81.5%`
- `gate` main-signal recall improved to `62.9%`
- cross-gate triggering on `adult` / `gambling` became near-zero
- `possible_gate_or_evasion` on `ordinary_benign` dropped to `0.8%`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added lightweight normalization inside `_kw_match(...)` to normalize curly quotes, non-breaking spaces, ellipses, and long dashes before keyword matching
- expanded `GATE_SURFACE_KEYWORDS` and `GATE_STRONG_KEYWORDS` to cover real gate phrasing such as `human check`, `not a robot`, `verify you're not a bot`, `please wait while your request is being verified`, `请稍候`, and `正在验证您的请求`
- tightened `possible_gate_or_evasion` and `possible_challenge_surface` so bare `captcha_present_candidate` no longer triggers a gate hit by itself
- expanded `GAMBLING_KEYWORDS` and `GAMBLING_HIGH_CONFIDENCE_KEYWORDS` with `bet365`, `slot`, `投注`, `彩票`, `真人`, `棋牌`, `捕鱼`, and `线路中心`
- expanded `ADULT_KEYWORDS` and `ADULT_HIGH_CONFIDENCE_KEYWORDS` with `theporndude`, `91porn`, `порно`, `成人社区`, `约炮`, `口交`, `内射`, and `啪啪`

### Doc Changes

- updated task doc: `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- added handoff doc: `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- did not modify `L0_DESIGN_V1.md` because this task did not change the field set or stage semantics

### Output / Artifact Changes

- no field-set change in `specialized_surface_signals`
- no field-set change in `l0_routing_hints`
- the new artifacts are the tuned implementation and the mixed-batch regression results

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: only `gambling` / `adult` / `gate` keyword families and specialized-trigger logic were changed
- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`: only the status was updated to `DONE`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`: records the implementation change and the three mixed regression batches

---

## 4. Behavior Impact

### Expected New Behavior

- `gate` now depends primarily on strong verification / challenge semantics, or on runtime/provider support that is backed by gate-like text, instead of firing on ordinary pages just because they embed captcha/turnstile
- `adult` and `gambling` now cover more of the refreshed multilingual and high-salience sample patterns, especially text-only pages
- gate cross-triggering on `adult` and `gambling` samples is substantially reduced

### Preserved Behavior

- the specialized detector still exposes only the three families `gambling`, `adult`, and `gate`
- `possible_fake_verification` and `possible_interaction_required` were not reintroduced
- the `evt_v1.2` contract, CLI usage, output field names, and routing-hint field names all remain unchanged

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This task only adjusted how existing weak signals are formed. It did not add fields, remove fields, rename fields, change function signatures, change CLI parameters, or change output paths.  
Any downstream consumer that depends on schema presence or schema version should remain compatible.  
Any downstream consumer that depends on exact trigger rates or reason paths should expect detector-tuning behavior changes.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir`
- run representative smoke checks on refreshed gate / adult / gambling / benign samples
- print `specialized_surface_signals` and `l0_routing_hints`

PowerShell heredoc piped to `python -`:
- run 3 mixed regression batches with seeds:
  - `20260413`
  - `20260414`
  - `20260415`
- per-batch size: `200`
- per-batch composition:
  - `gambling`: `54`
  - `adult`: `53`
  - `gate`: `53`
  - `ordinary_benign`: `40`
- summarize trigger rates for:
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
```

### Result

- syntax check passed
- representative smoke behavior matched the intended direction:
  - the new gate phrases now catch `yktex.cn...`, `ycj.rhn...`, and `www.tragetlocax...`
  - `yuvideos.com...` and `autoscout24.pl...` no longer cross-trigger as gate
  - `avjb.com...` now emits `possible_adult_lure`
  - `1036m.com...`, `0140.ee...`, and `1777sz.com...` now emit `possible_gambling_lure`
- mixed-batch aggregate results:
  - `gambling`:
    - `possible_gambling_lure`: `81.5%`
    - `possible_bonus_or_betting_induction`: `71.6%`
    - `possible_gate_or_evasion`: `0.6%`
  - `adult`:
    - `possible_adult_lure`: `87.4%`
    - `possible_age_gate_surface`: `39.6%`
    - `possible_gate_or_evasion`: `0.6%`
  - `gate`:
    - `possible_gate_or_evasion`: `62.9%`
    - `possible_challenge_surface`: `62.9%`
  - `ordinary_benign`:
    - `possible_gambling_lure`: `3.3%`
    - `possible_adult_lure`: `1.7%`
    - `possible_gate_or_evasion`: `0.8%`

### Not Run

- full-repo full-sample regression
- manual gold-label review
- any training or deployment workflow

Reason:

This task was scoped to detector tuning plus refreshed-sample regression validation rather than full-dataset reruns or training/deployment work.

---

## 7. Risks / Caveats

- although `gate` improved materially, mixed-batch aggregate recall is still only `62.9%`, and many remaining misses have completely empty `matched_keywords`, which means there is still a family of gate pages with weak or missing text evidence
- `ordinary_benign` still shows `3.3%` gambling false positives, mostly from gambling-news, affiliate, or term-heavy content pages
- `adult` still misses a subset of pages that only expose one weak token such as `milf`, `bdsm`, or `xxx`, and the current rules do not upgrade that single weak token into the main adult signal

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_sample_refresh_tuning.md`

Doc debt still remaining:

- if gate tuning continues, a dedicated false-negative pattern note would help
- if gambling false positives are tightened further, a short note about gambling-news / affiliate false-trigger patterns would help

---

## 9. Recommended Next Step

- open a dedicated `gate FN mining` task for the remaining gate misses with empty `matched_keywords`
- open a dedicated `gambling false-positive tightening` task to reduce gambling-news and affiliate-page false positives
- if adult recall is pushed further, explicitly evaluate whether a single high-salience adult token should ever be allowed to promote the main adult signal
