# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-10-l0-specialized-detectors-small-batch-regression
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SMALL-BATCH-REGRESSION
- Task Title: 运行 L0 specialized detectors 约 100 样本小批量回归并统计触发率
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

本次交付对当前 working tree 中的 specialized-detector 版本做了一轮 100 样本回归。实际分组为：

- `gate`: 14
- `gambling`: 29
- `adult`: 29
- `ordinary benign`: 28

关键结果：

- `gambling` 信号区分度最好，`possible_gambling_lure` 在赌博组触发率 `96.6%`，在普通 benign 组为 `0%`
- `adult` 信号也有明显区分度，`possible_adult_lure` 在成人组触发率 `79.3%`，在普通 benign 组为 `0%`
- `gate` 信号能覆盖大部分 gate 组，`possible_gate_or_evasion` 在 gate 组触发率 `78.6%`
- 但 `gate` 相关信号在普通 benign 组仍然偏高，`possible_gate_or_evasion` 为 `25.0%`，`need_l2_candidate` 也为 `25.0%`
- `possible_interaction_required` 过宽，100 样本总体触发率 `93.0%`，普通 benign 组也有 `85.7%`
- `possible_fake_verification` 在这 100 样本中完全没有触发，说明当前样本切片没有覆盖到，或者关键词还偏窄

结论：当前 specialized detectors 对 `gambling` / `adult` 已经有实用区分度；`gate` 路由和 `interaction_required` 还需要单独收紧。

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- 新增 task：`docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- 新增 handoff：`docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- 将 task 状态更新为 `DONE`

### Output / Artifact Changes

- none

本次只运行统计，不修改 detector 实现。

---

## 3. Files Touched

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

---

## 4. Behavior Impact

### Expected New Behavior

- 无代码行为变化
- 新增的是对当前 specialized-detector 行为的统计认知，不是实现变更

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` 未修改
- schema 未修改
- CLI / 调用方式未修改

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

本次交付只读取当前输出并做统计，没有改字段、函数签名、CLI 或路径约定。

---

## 6. Validation Performed

### Sampling Method

- 数据根目录：`E:\Warden\data\raw\benign`
- gate 组：直接使用 `E:\Warden\data\raw\benign\gate` 下全部 14 个样本
- gambling / adult / ordinary benign：
  使用固定随机种子 `20260410`，基于“域名强词 + 文本强词”规则建立候选池，再随机抽样
- 最终总量：100

Candidate pool sizes:

- gate: 14
- gambling: 683
- adult: 447
- ordinary benign: 9094

Selected counts:

- gate: 14
- gambling: 29
- adult: 29
- ordinary benign: 28

### Commands Run

使用 PowerShell heredoc 管道到 `python -`：

- 从 `E:\Warden\data\raw\benign` 遍历样本目录
- 固定随机种子为 `20260410`
- 导入：
  - `derive_auto_labels_from_sample_dir`
  - `derive_rule_labels`
- 对 100 个选中样本运行当前弱信号链路
- 统计以下字段触发率：
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `possible_fake_verification`
  - `possible_interaction_required`
  - `no_early_stop_candidate`
  - `need_text_semantic_candidate`
  - `need_vision_candidate`
  - `need_l2_candidate`
  - `escalate_to_l2_candidate`

### Result

Per-group trigger rates:

- `gate`
  - `possible_gate_or_evasion`: `78.6%`
  - `possible_challenge_surface`: `78.6%`
  - `no_early_stop_candidate`: `85.7%`
  - `need_l2_candidate`: `42.9%`
  - obvious misses: `alz.co.uk_20260402T023734Z`, `cuonet.com_20260402T175831Z`

- `gambling`
  - `possible_gambling_lure`: `96.6%`
  - `possible_bonus_or_betting_induction`: `79.3%`
  - `no_early_stop_candidate`: `100.0%`
  - `need_l2_candidate`: `69.0%`
  - cross-gate trigger: `24.1%`
  - only one miss on main signal: `gbetclub.io_20260326T190910Z`

- `adult`
  - `possible_adult_lure`: `79.3%`
  - `possible_age_gate_surface`: `37.9%`
  - `no_early_stop_candidate`: `82.8%`
  - `need_l2_candidate`: `62.1%`
  - cross-gate trigger: `13.8%`
  - missed adult signal examples include `codespaces.com_20260402T184547Z`, `trackjs.com_20260326T050957Z`, `ai.google_20260325T092919Z`

- `ordinary benign`
  - `possible_gambling_lure`: `0.0%`
  - `possible_adult_lure`: `0.0%`
  - `possible_gate_or_evasion`: `25.0%`
  - `no_early_stop_candidate`: `25.0%`
  - `need_l2_candidate`: `25.0%`
  - false-trigger examples are mostly gate-like benign pages such as `autoscout24.pl_20260403T023010Z`, `mastersofwine.org_20260402T190135Z`, `nachi.org_20260408T063852Z`

Overall rates across all 100:

- `possible_gambling_lure`: `29.0%`
- `possible_bonus_or_betting_induction`: `27.0%`
- `possible_adult_lure`: `24.0%`
- `possible_age_gate_surface`: `12.0%`
- `possible_gate_or_evasion`: `29.0%`
- `possible_challenge_surface`: `29.0%`
- `possible_fake_verification`: `0.0%`
- `possible_interaction_required`: `93.0%`
- `no_early_stop_candidate`: `72.0%`
- `need_text_semantic_candidate`: `72.0%`
- `need_vision_candidate`: `0.0%`
- `need_l2_candidate`: `51.0%`
- `escalate_to_l2_candidate`: `90.0%`

Primary-label top distribution across all 100:

- `uncertain`: 53
- `credential_theft`: 21
- `payment_fraud`: 12
- `malware_or_fake_download`: 7
- `benign`: 4

### Not Run

- 全量数据集回归
- detector 代码改动后的再训练或重部署
- 任何代码级 patch

Reason:

本次任务只要求一轮约 100 样本的小批量回归统计。

---

## 7. Risks / Caveats

- `adult` 和 `gambling` 候选池已做收紧，但仍是启发式抽样，不是人工金标集合
- `gate` 在普通 benign 组上的 `25%` 误触发率很高，说明 benign anti-bot / challenge 页面会明显污染当前 gate 路由
- `possible_interaction_required` 的区分度很差，当前几乎对所有组都高触发
- `need_vision_candidate` 在这轮 100 样本中完全没有触发，当前逻辑没有被这批样本覆盖到
- `possible_fake_verification` 也完全没有触发，当前还缺专门的 fake-verification 样本切片

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 单开一个 `gate tightening` 任务，优先降低普通 benign 上的 gate 误触发率
- 单开一个 `interaction_required narrowing` 任务，把 `possible_interaction_required` 从当前近乎全量触发的状态收紧
- 追加一组专门的 `fake verification` 样本回归，因为这轮 100 样本没有覆盖到该路径

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-10-l0-specialized-detectors-small-batch-regression
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-SMALL-BATCH-REGRESSION
- Task Title: Run an approximately 100-sample small-batch regression for L0 specialized detectors and summarize trigger rates
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

This delivery ran a 100-sample regression against the current specialized-detector version in the working tree. The actual group sizes were:

- `gate`: 14
- `gambling`: 29
- `adult`: 29
- `ordinary benign`: 28

Key findings:

- the `gambling` signal is the strongest separator; `possible_gambling_lure` fired on `96.6%` of the gambling group and `0%` of the ordinary-benign group
- the `adult` signal also shows clear separation; `possible_adult_lure` fired on `79.3%` of the adult group and `0%` of the ordinary-benign group
- the `gate` signal covers most curated gate pages; `possible_gate_or_evasion` fired on `78.6%` of the gate group
- but gate-related signals remain too broad on ordinary benign pages, where `possible_gate_or_evasion` still fired on `25.0%` and `need_l2_candidate` also fired on `25.0%`
- `possible_interaction_required` is too broad; it fired on `93.0%` of the full 100-sample slice and `85.7%` of the ordinary-benign group
- `possible_fake_verification` never fired in this 100-sample run, which means either this slice did not exercise that path or the keywords remain too narrow

Conclusion: the current specialized detectors already have practical separation for `gambling` and `adult`, while the `gate` routing and `interaction_required` logic still need a dedicated tightening pass.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- added task doc: `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- added handoff doc: `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- updated the task status to `DONE`

### Output / Artifact Changes

- none

This task only ran measurement and documentation. It did not modify the detector implementation.

---

## 3. Files Touched

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

---

## 4. Behavior Impact

### Expected New Behavior

- no code behavior changed
- the new outcome is measurement clarity for the current specialized-detector implementation, not an implementation change

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` was not modified
- schema was not modified
- CLI and call patterns were not modified

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

This delivery only read the current outputs and summarized them. It did not modify fields, function signatures, CLI behavior, or path conventions.

---

## 6. Validation Performed

### Sampling Method

- dataset root: `E:\Warden\data\raw\benign`
- gate group: all 14 available samples under `E:\Warden\data\raw\benign\gate`
- gambling / adult / ordinary benign:
  candidate pools were built with a fixed random seed `20260410` using “strong host token + strong visible-text token” heuristics, then sampled randomly
- final total: 100

Candidate pool sizes:

- gate: 14
- gambling: 683
- adult: 447
- ordinary benign: 9094

Selected counts:

- gate: 14
- gambling: 29
- adult: 29
- ordinary benign: 28

### Commands Run

A PowerShell heredoc was piped into `python -` to:

- walk sample directories under `E:\Warden\data\raw\benign`
- fix the random seed to `20260410`
- import:
  - `derive_auto_labels_from_sample_dir`
  - `derive_rule_labels`
- run the current weak-signal path on the 100 selected samples
- summarize trigger rates for:
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `possible_fake_verification`
  - `possible_interaction_required`
  - `no_early_stop_candidate`
  - `need_text_semantic_candidate`
  - `need_vision_candidate`
  - `need_l2_candidate`
  - `escalate_to_l2_candidate`

### Result

Per-group trigger rates:

- `gate`
  - `possible_gate_or_evasion`: `78.6%`
  - `possible_challenge_surface`: `78.6%`
  - `no_early_stop_candidate`: `85.7%`
  - `need_l2_candidate`: `42.9%`
  - obvious misses: `alz.co.uk_20260402T023734Z`, `cuonet.com_20260402T175831Z`

- `gambling`
  - `possible_gambling_lure`: `96.6%`
  - `possible_bonus_or_betting_induction`: `79.3%`
  - `no_early_stop_candidate`: `100.0%`
  - `need_l2_candidate`: `69.0%`
  - cross-gate trigger: `24.1%`
  - only one main-signal miss: `gbetclub.io_20260326T190910Z`

- `adult`
  - `possible_adult_lure`: `79.3%`
  - `possible_age_gate_surface`: `37.9%`
  - `no_early_stop_candidate`: `82.8%`
  - `need_l2_candidate`: `62.1%`
  - cross-gate trigger: `13.8%`
  - missed-adult examples include `codespaces.com_20260402T184547Z`, `trackjs.com_20260326T050957Z`, and `ai.google_20260325T092919Z`

- `ordinary benign`
  - `possible_gambling_lure`: `0.0%`
  - `possible_adult_lure`: `0.0%`
  - `possible_gate_or_evasion`: `25.0%`
  - `no_early_stop_candidate`: `25.0%`
  - `need_l2_candidate`: `25.0%`
  - false-trigger examples were mostly gate-like benign pages such as `autoscout24.pl_20260403T023010Z`, `mastersofwine.org_20260402T190135Z`, and `nachi.org_20260408T063852Z`

Overall rates across the 100 samples:

- `possible_gambling_lure`: `29.0%`
- `possible_bonus_or_betting_induction`: `27.0%`
- `possible_adult_lure`: `24.0%`
- `possible_age_gate_surface`: `12.0%`
- `possible_gate_or_evasion`: `29.0%`
- `possible_challenge_surface`: `29.0%`
- `possible_fake_verification`: `0.0%`
- `possible_interaction_required`: `93.0%`
- `no_early_stop_candidate`: `72.0%`
- `need_text_semantic_candidate`: `72.0%`
- `need_vision_candidate`: `0.0%`
- `need_l2_candidate`: `51.0%`
- `escalate_to_l2_candidate`: `90.0%`

Top primary-label distribution across all 100:

- `uncertain`: 53
- `credential_theft`: 21
- `payment_fraud`: 12
- `malware_or_fake_download`: 7
- `benign`: 4

### Not Run

- full-dataset regression
- retraining or redeployment
- any code patch

Reason:

The task only asked for an approximately 100-sample small-batch regression.

---

## 7. Risks / Caveats

- the `adult` and `gambling` pools were tightened, but they are still heuristic sample pools rather than a manually curated gold set
- the `gate` false-trigger rate of `25%` on ordinary benign pages is still high, which means benign anti-bot / challenge surfaces strongly contaminate the current gate routing
- `possible_interaction_required` has very weak discrimination right now and fires on nearly every group
- `need_vision_candidate` never fired in this 100-sample run, so that path was not exercised by this slice
- `possible_fake_verification` also never fired, so the current regression still lacks a dedicated fake-verification slice

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- open a dedicated `gate tightening` task to reduce the gate false-trigger rate on ordinary benign pages
- open a dedicated `interaction_required narrowing` task to reduce the current near-global firing of `possible_interaction_required`
- add a regression slice specifically for fake-verification pages, because this 100-sample run did not exercise that path
