# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-09-l0-specialized-detectors
- Related Task ID: TASK-L0-2026-04-09-SPECIALIZED-DETECTORS
- Task Title: 实现 L0 博彩 / 成人 / gate 专项探测器并接入现有弱信号链路
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

本次交付没有去虚构新的 `src/infer` runtime baseline，而是把 specialized detector families 落在仓库里当前真实可运行的 cheap-evidence / weak-signal 路径：`scripts/labeling/Warden_auto_label_utils_brandlex.py`。  
实现内容包括三类专项表面识别：`gambling`、`adult`、`gate / challenge / fake verification`，并新增 additive 的 `specialized_surface_signals` 与 `l0_routing_hints` 输出，用于表达弱信号、`no_early_stop` 倾向、`need_text_semantic_candidate`、`need_vision_candidate`、`need_l2_candidate`。  
同时补了若干最小抑制逻辑，避免博彩页或 gate 页仅因静态说明文本里的 `verify`、`deposit`、`wallet`、`download` 等词就被通用 intent 规则过度拉成高风险主标签。

---

## 2. What Changed

### Code Changes

- 在 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中新增 specialized keyword families：
  `GAMBLING_KEYWORDS`、`GAMBLING_BONUS_KEYWORDS`、`ADULT_KEYWORDS`、`ADULT_AGE_GATE_KEYWORDS`、`GATE_SURFACE_KEYWORDS`、`FAKE_VERIFICATION_KEYWORDS`、`PERMISSION_INDUCEMENT_KEYWORDS`
- 新增 `derive_specialized_surface_signals(...)`
- 新增 `derive_l0_routing_hints(...)`
- 收紧 `wallet` 相关 intent，新增更保守的 `WEB3_WALLET_KEYWORDS`
- 在 `derive_auto_labels(...)` 中新增：
  - `specialized_surface_signals`
  - `l0_routing_hints`
- 在 `derive_intent_signals(...)` 中加入垂类感知抑制：
  - 博彩 / 成人文本页默认不再仅靠静态 `login / verify / payment / pii` 文案触发高敏 intent
  - gate 文本页默认不再仅靠“验证中”文案触发 `otp_intent_candidate`
- 在 `derive_rule_labels(...)` 中把 `no_early_stop_candidate`、`need_text_semantic_candidate`、`need_vision_candidate`、`need_l2_candidate` 接进 `rule_flags`
- 在 `derive_rule_labels(...)` 中对博彩 / gate 的 text-only generic intent 做了保守抑制，降低误把垂类内容写成 `payment_fraud`、`credential_theft`、`malware_or_fake_download` 的概率

### Doc Changes

- 新增 repo task：`docs/tasks/2026-04-09_l0_specialized_detectors.md`
- 新增本 handoff：`docs/handoff/2026-04-09_l0_specialized_detectors.md`
- 将 task 状态统一到 `DONE`

### Output / Artifact Changes

- `derive_auto_labels(...)` 输出新增两个 additive 顶层字段：
  - `specialized_surface_signals`
  - `l0_routing_hints`
- `derive_rule_labels(...)` 的 `rule_flags` 新增 additive 字段：
  - `no_early_stop_candidate`
  - `need_text_semantic_candidate`
  - `need_vision_candidate`
  - `need_l2_candidate`
  - `specialized_surface_family_candidates`
  - `specialized_routing_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` 是本次真正的实现落点；`scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` 没改，因为它已经消费该脚本输出
- task 文档由用户给的外部 task 收进仓库并按 repo 风格对齐

---

## 4. Behavior Impact

### Expected New Behavior

- 赌博页可输出 `possible_gambling_lure` 与 `possible_bonus_or_betting_induction`
- 成人页可输出 `possible_adult_lure`
- gate 页可输出 `possible_gate_or_evasion`、`possible_challenge_surface`
- 这些专项信号会同步产出 `l0_routing_hints`
- `rule_flags` 现在显式暴露 `no_early_stop_candidate`、`need_text_semantic_candidate`、`need_vision_candidate`、`need_l2_candidate`
- gate / fake-verification 类页面不再只靠通用 `otp` 词命中就被写成 `credential_theft`
- 成人页在没有其他高敏证据时，不再走 `benign` 低风险回退；会保留为 `uncertain` 并带专项路由提示
- 博彩文本页对 `wallet`、`payment`、`otp`、`pii`、`download` 的误触发被收紧，避免仅凭注册说明或 app 下载文案就直接投到错误主标签

### Preserved Behavior

- 现有 `derive_auto_labels(...)` / `derive_rule_labels(...)` 调用方式保持不变
- 现有字段名都没重命名
- `scripts/capture/...plus_labels_brandlex.py` 现有调用链保持可运行
- 现有风险分数、taxonomy、rule-flags 结构仍保留原有字段，只做 additive 扩展和保守抑制

### User-facing / CLI Impact

- 无新增 CLI
- 无新增依赖

### Output Format Impact

- `auto_labels` 和 `rule_labels` 存在 additive 字段扩展
- 旧字段仍保留

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `auto_labels.specialized_surface_signals`
- `auto_labels.l0_routing_hints`
- `rule_labels.rule_flags.no_early_stop_candidate`
- `rule_labels.rule_flags.need_text_semantic_candidate`
- `rule_labels.rule_flags.need_vision_candidate`
- `rule_labels.rule_flags.need_l2_candidate`
- `rule_labels.rule_flags.specialized_surface_family_candidates`
- `rule_labels.rule_flags.specialized_routing_reason_codes`

Compatibility notes:

所有新增字段都是 additive。  
现有函数签名对外调用方式未改，既有字段没有删除或重命名。  
本次没有改 stage naming、CLI、采集脚本入口或下游文件路径。

---

## 6. Validation Performed

### Sample Observation Before Hardening

- 赌博样本 `cobbercasino.org_20260408T093616Z` 与 `thescore.bet_20260408T072233Z` 明显包含 `casino / sportsbook / jackpot / bonus / deposit / payout / play now` 一类高显著词
- 成人样本 `pornamateur.net_20260408T073300Z` 与 `avxxxmini.com_20260408T071508Z` 明显包含 `porn / xxx / cumshot / bdsm / anal / jav / avxxx` 一类高显著词
- gate 样本 `kill-bot.net_20260402T164619Z` 明显包含 `用户验证 / 验证中` 一类 gate 文案；`hertz.com_20260401T082852Z` 返回 `Incapsula incident`，说明 gate / challenge 表面真实存在

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
```

```bash
PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir` and `derive_rule_labels`
- run smoke checks on:
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
  - `E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- print `intent_signals`, `specialized_surface_signals`, `l0_routing_hints`, `risk_outputs`, `rule_flags`, `primary_label`, `scenario_label`
```

### Result

- 语法检查通过
- 赌博样本成功输出 `possible_gambling_lure` / `possible_bonus_or_betting_induction`
- 成人样本成功输出 `possible_adult_lure`
- gate 样本成功输出 `possible_gate_or_evasion` / `possible_challenge_surface`
- 三类样本都成功输出 `no_early_stop_candidate`
- gate 样本成功输出 `need_l2_candidate`
- gate 样本的 `primary_label` 从原先受 `otp` 文案拖动的 `credential_theft` 收敛为 `uncertain`
- 成人样本不再走 `benign` 低风险回退，而是保留 `uncertain` 并携带专项路由提示
- 博彩样本的 generic `wallet / payment / otp / pii` 误触发已显著下降，主标签不再被这些 text-only generic intents 直接带偏

### Not Run

- capture 端到端整链回归
- 大批量样本统计回归
- 下游消费脚本兼容性批量扫描

Reason:

本次改动聚焦在单文件弱信号逻辑；先做了语法检查和代表样本 smoke，未扩到批量回归。

---

## 7. Risks / Caveats

- 仓库里现有 brand / scenario 规则本来就比较粗，仍会在部分垂类样本上给出偏粗的 `scenario_label`，例如赌博样本里仍可能受 app-store / brand alias 误命中影响
- 这次没有重写整套 `brand_signals` 或 `scenario_label` 逻辑；相关误报只做了与本任务强相关的最小抑制
- `download_intent_candidate` 在部分博彩页面仍可能保留，因为页面确实存在 app 下载语义；当前实现只阻止它直接把页面写成 fake-download 主标签
- 还没做批量样本统计，因此这次收口结果主要由代表样本 smoke 支撑

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

Doc debt still remaining:

- `none`

说明：

`L0_DESIGN_V1.md` 与 `MODULE_INFER.md` 已经有这类 specialized detector 的契约表述，这次实现没有再改模块文档 wording。

---

## 9. Recommended Next Step

- 做一次小批量回归，统计这几个新字段在博彩 / 成人 / gate / 普通 benign 样本上的触发率
- 单独开一个 brand / scenario 去噪任务，收掉 `google / apple / ups` 这类短 alias 或 app-store 语义带来的垂类误导

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-09-l0-specialized-detectors
- Related Task ID: TASK-L0-2026-04-09-SPECIALIZED-DETECTORS
- Task Title: Implement L0 specialized detectors for gambling, adult, and gate surfaces on the existing weak-signal path
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

This delivery did not invent a new `src/infer` runtime baseline. It implemented the specialized detector families inside the real cheap-evidence / weak-signal path that already exists and runs in the repo: `scripts/labeling/Warden_auto_label_utils_brandlex.py`.  
The implementation adds specialized surface recognition for `gambling`, `adult`, and `gate / challenge / fake verification`, plus additive `specialized_surface_signals` and `l0_routing_hints` outputs for weak signals, `no_early_stop` tendency, `need_text_semantic_candidate`, `need_vision_candidate`, and `need_l2_candidate`.  
It also adds a small amount of context-aware suppression so gambling pages or gate pages are not over-pulled into high-risk primary labels purely because static page copy contains generic words such as `verify`, `deposit`, `wallet`, or `download`.

---

## 2. What Changed

### Code Changes

- added specialized keyword families in `scripts/labeling/Warden_auto_label_utils_brandlex.py`:
  `GAMBLING_KEYWORDS`, `GAMBLING_BONUS_KEYWORDS`, `ADULT_KEYWORDS`, `ADULT_AGE_GATE_KEYWORDS`, `GATE_SURFACE_KEYWORDS`, `FAKE_VERIFICATION_KEYWORDS`, `PERMISSION_INDUCEMENT_KEYWORDS`
- added `derive_specialized_surface_signals(...)`
- added `derive_l0_routing_hints(...)`
- narrowed wallet-related intent with a more conservative `WEB3_WALLET_KEYWORDS`
- extended `derive_auto_labels(...)` with:
  - `specialized_surface_signals`
  - `l0_routing_hints`
- added vertical-aware suppression inside `derive_intent_signals(...)`:
  - gambling / adult text pages no longer trigger sensitive intent as easily from static `login / verify / payment / pii` wording alone
  - gate text pages no longer trigger `otp_intent_candidate` purely from “verification in progress” copy
- wired `no_early_stop_candidate`, `need_text_semantic_candidate`, `need_vision_candidate`, and `need_l2_candidate` into `derive_rule_labels(...).rule_flags`
- added conservative suppression in `derive_rule_labels(...)` so gambling / gate text-only generic intents are less likely to become `payment_fraud`, `credential_theft`, or `malware_or_fake_download`

### Doc Changes

- added repo task doc: `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- added this handoff: `docs/handoff/2026-04-09_l0_specialized_detectors.md`
- normalized the task status to `DONE`

### Output / Artifact Changes

- `derive_auto_labels(...)` now emits two additive top-level fields:
  - `specialized_surface_signals`
  - `l0_routing_hints`
- `derive_rule_labels(...).rule_flags` now emits additive fields:
  - `no_early_stop_candidate`
  - `need_text_semantic_candidate`
  - `need_vision_candidate`
  - `need_l2_candidate`
  - `specialized_surface_family_candidates`
  - `specialized_routing_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` is the actual implementation target for this task; `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` did not need changes because it already consumes this script’s outputs
- the task doc was adopted from the user-provided external task and normalized into the repo task format

---

## 4. Behavior Impact

### Expected New Behavior

- gambling pages can emit `possible_gambling_lure` and `possible_bonus_or_betting_induction`
- adult pages can emit `possible_adult_lure`
- gate pages can emit `possible_gate_or_evasion` and `possible_challenge_surface`
- those specialized signals now produce `l0_routing_hints`
- `rule_flags` now explicitly expose `no_early_stop_candidate`, `need_text_semantic_candidate`, `need_vision_candidate`, and `need_l2_candidate`
- gate / fake-verification pages are no longer pushed into `credential_theft` purely by generic `otp` wording
- adult pages no longer fall through the low-risk `benign` fallback when no other strong signal exists; they now stay `uncertain` with specialized routing hints
- gambling text pages now suppress several generic `wallet`, `payment`, `otp`, `pii`, and `download` false triggers so registration prose or app-download copy does not immediately force the wrong primary label

### Preserved Behavior

- the current `derive_auto_labels(...)` / `derive_rule_labels(...)` call pattern is unchanged
- no existing field names were renamed
- the current `scripts/capture/...plus_labels_brandlex.py` call chain stays runnable
- the existing risk-score, taxonomy, and rule-flag structure remains intact, with only additive extensions and conservative suppressions

### User-facing / CLI Impact

- no new CLI
- no new dependency

### Output Format Impact

- `auto_labels` and `rule_labels` receive additive field extensions
- old fields remain present

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `auto_labels.specialized_surface_signals`
- `auto_labels.l0_routing_hints`
- `rule_labels.rule_flags.no_early_stop_candidate`
- `rule_labels.rule_flags.need_text_semantic_candidate`
- `rule_labels.rule_flags.need_vision_candidate`
- `rule_labels.rule_flags.need_l2_candidate`
- `rule_labels.rule_flags.specialized_surface_family_candidates`
- `rule_labels.rule_flags.specialized_routing_reason_codes`

Compatibility notes:

All new fields are additive.  
The external call pattern of the existing functions is unchanged, and no existing field was removed or renamed.  
This change does not touch stage naming, CLI entrypoints, capture entrypoints, or downstream file paths.

---

## 6. Validation Performed

### Sample Observation Before Hardening

- the gambling samples `cobbercasino.org_20260408T093616Z` and `thescore.bet_20260408T072233Z` clearly contained high-salience wording such as `casino / sportsbook / jackpot / bonus / deposit / payout / play now`
- the adult samples `pornamateur.net_20260408T073300Z` and `avxxxmini.com_20260408T071508Z` clearly contained high-salience wording such as `porn / xxx / cumshot / bdsm / anal / jav / avxxx`
- the gate sample `kill-bot.net_20260402T164619Z` clearly contained `用户验证 / 验证中`; `hertz.com_20260401T082852Z` returned an `Incapsula incident`, confirming that gate / challenge surfaces exist in the dataset

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
```

```bash
PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir` and `derive_rule_labels`
- run smoke checks on:
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
  - `E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- print `intent_signals`, `specialized_surface_signals`, `l0_routing_hints`, `risk_outputs`, `rule_flags`, `primary_label`, and `scenario_label`
```

### Result

- syntax check passed
- the gambling sample emitted `possible_gambling_lure` and `possible_bonus_or_betting_induction`
- the adult sample emitted `possible_adult_lure`
- the gate sample emitted `possible_gate_or_evasion` and `possible_challenge_surface`
- all three sample families emitted `no_early_stop_candidate`
- the gate sample emitted `need_l2_candidate`
- the gate sample primary label collapsed from the earlier generic `otp`-driven `credential_theft` outcome to `uncertain`
- the adult sample no longer falls through the low-risk `benign` fallback; it now stays `uncertain` with specialized routing hints
- the gambling sample’s generic `wallet / payment / otp / pii` false triggers were materially reduced, and those text-only generic intents no longer directly dictate the primary label

### Not Run

- end-to-end capture regression
- batch-scale statistical regression
- broad downstream consumer compatibility scan

Reason:

This change is concentrated in one weak-signal file. I prioritized syntax sanity and representative-sample smoke tests before any larger regression sweep.

---

## 7. Risks / Caveats

- the repo’s existing brand / scenario rules are still coarse and can still produce rough `scenario_label` outcomes on some vertical pages
- this task did not rewrite the full `brand_signals` or `scenario_label` logic; it only added the smallest suppressions directly relevant to the specialized-detector task
- `download_intent_candidate` can still remain true on some gambling pages when the page genuinely contains app-download semantics; the current change only prevents that signal from directly forcing a fake-download primary label in the normal gambling flow
- no batch-scale statistics were run yet, so the current confidence comes mainly from representative sample smoke checks

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-09_l0_specialized_detectors.md`
- `docs/handoff/2026-04-09_l0_specialized_detectors.md`

Doc debt still remaining:

- `none`

Note:

`L0_DESIGN_V1.md` and `MODULE_INFER.md` already contained the specialized-detector contract wording, so this implementation did not need an extra wording sync there.

---

## 9. Recommended Next Step

- run a small-batch regression to measure the trigger rate of the new fields across gambling / adult / gate / ordinary benign samples
- open a separate brand / scenario denoising task to clean up short alias and app-store related false guidance such as `google / apple / ups`
