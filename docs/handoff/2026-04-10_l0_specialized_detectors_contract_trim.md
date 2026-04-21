# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-10-l0-specialized-detectors-contract-trim
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-CONTRACT-TRIM
- Task Title: 收紧 L0 specialized detectors 契约并移除 fake verification 与 interaction required 输出
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

本次交付把 L0 specialized detectors 的契约收紧到了三类：

- `gambling`
- `adult`
- `gate`

并明确移除了两个 L0 输出：

- `possible_fake_verification`
- `possible_interaction_required`

实现上，这两个字段已经从 `specialized_surface_signals` 中删除，对应的独立关键词族和 reason code 也已移除。  
文档上，`L0_DESIGN_V1.md` 已同步改成只保留 `gambling / adult / gate / challenge / CAPTCHA` 的 L0 specialized contract。  
这次同时进一步收紧了三类触发逻辑，尤其把 gate 的触发重新收口到验证语义、challenge 提示、provider 线索和运行期支持信号，而不是保留单独的 fake-verification / interaction-required 语义。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 删除 `FAKE_VERIFICATION_KEYWORDS`
- 删除 `PERMISSION_INDUCEMENT_KEYWORDS`
- 将部分原本属于 fake-verification 的明显 gate 语义词并入 `GATE_SURFACE_KEYWORDS`
- 在 `derive_specialized_surface_signals(...)` 中删除：
  - `possible_fake_verification`
  - `possible_interaction_required`
  - 对应 `matched_keywords` 项
  - 对应 reason codes
- 收紧 `possible_gate_or_evasion` / `possible_challenge_surface` 的形成条件
- 将 `schema_version` 从 `evt_v1.1` 提升到 `evt_v1.2`
- 删除 `derive_rule_labels(...)` 中与 `possible_fake_verification` 相关的 evasion tag 逻辑

### Doc Changes

- 更新 `L0_DESIGN_V1.md`
- 新增 task：`docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- 新增 handoff：`docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

### Output / Artifact Changes

- `auto_labels.specialized_surface_signals` 删除：
  - `possible_fake_verification`
  - `possible_interaction_required`
- `auto_labels.specialized_surface_signals.matched_keywords` 删除：
  - `fake_verification`
  - `permission_inducement`
- `auto_labels.schema_version` 改为 `evt_v1.2`
- `rule_labels.schema_version` 改为 `evt_v1.2`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

---

## 4. Behavior Impact

### Expected New Behavior

- L0 specialized outputs 现在只保留：
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
- `possible_fake_verification` 不再是 L0 字段
- `possible_interaction_required` 不再是 L0 字段
- gate 相关触发现在主要依赖：
  - 强 gate / challenge 语义
  - captcha / anti-bot / cloaking / variant-failed / dynamic-redirect 一类支持信号
- gambling / adult / gate 的代表样本仍能正常打出对应 specialized signal

### Preserved Behavior

- `no_early_stop_candidate`、`need_text_semantic_candidate`、`need_vision_candidate`、`need_l2_candidate` 仍保留
- `gambling` / `adult` / `gate` 三类 specialized family 仍保留
- capture 侧调用方式未改

### User-facing / CLI Impact

- 无 CLI 变更

### Output Format Impact

- 有 breaking schema 变化，删除了两个 specialized fields

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: NO
- Public interface changed: PARTIALLY
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- removed `auto_labels.specialized_surface_signals.possible_fake_verification`
- removed `auto_labels.specialized_surface_signals.possible_interaction_required`
- removed `auto_labels.specialized_surface_signals.matched_keywords.fake_verification`
- removed `auto_labels.specialized_surface_signals.matched_keywords.permission_inducement`
- bumped `schema_version` from `evt_v1.1` to `evt_v1.2`

Compatibility notes:

如果下游脚本显式读取这两个被删除字段，会直接受到影响。  
这次是用户明确要求的 contract trim，不是向后兼容改动。  
CLI 入口没变，但输出 schema 发生了删字段变更。

---

## 6. Validation Performed

### Commands Run

```bash
Select-String -Path "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py","E:\Warden\L0_DESIGN_V1.md" -Pattern "possible_fake_verification|possible_interaction_required|FAKE_VERIFICATION_KEYWORDS|PERMISSION_INDUCEMENT_KEYWORDS"
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
```

```bash
PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir` and `derive_rule_labels`
- run smoke checks on:
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
  - `E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- print:
  - `specialized_surface_signals`
  - `l0_routing_hints`
  - `rule_flags`
  - `primary_label`
```

### Result

- 残留词检查为空，说明代码和 `L0_DESIGN_V1.md` 中已无这两个 L0 字段
- 语法检查通过
- 赌博样本仍输出：
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
- 成人样本仍输出：
  - `possible_adult_lure`
- gate 样本仍输出：
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
- 三个代表样本的 `specialized_surface_signals` 中都不再包含：
  - `possible_fake_verification`
  - `possible_interaction_required`

### Not Run

- 100 样本回归重跑
- 全量数据集回归

Reason:

这次先做 contract trim 和 focused validation，未重复跑完整回归切片。

---

## 7. Risks / Caveats

- 这次是删字段，不向后兼容；任何显式依赖旧字段的下游都需要同步
- 虽然保留了 `gate`，但普通 benign 上的 gate 误触发问题并没有在这次任务里系统性解决
- `need_l2_candidate` 仍保留在 routing hints 中，因此 gate / adult / gambling 的升级提示逻辑还在
- 历史 handoff / regression 文档仍会出现旧字段名，那些文档保留的是当时事实，不代表当前契约

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

Doc debt still remaining:

- 建议后续再开一条 task，对 gate 误触发做专门收紧

---

## 9. Recommended Next Step

- 跑一轮新的小批量回归，重新测量删掉两个字段后的 `gate` / `adult` / `gambling` 区分度
- 单开一个 `gate tightening` task，继续压普通 benign 上的 gate 误触发率

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-10-l0-specialized-detectors-contract-trim
- Related Task ID: TASK-L0-2026-04-10-SPECIALIZED-DETECTORS-CONTRACT-TRIM
- Task Title: Tighten the L0 specialized-detector contract and remove fake-verification and interaction-required outputs
- Module: Inference
- Author: Codex
- Date: 2026-04-10
- Status: DONE

---

## 1. Executive Summary

This delivery tightened the L0 specialized-detector contract down to three families:

- `gambling`
- `adult`
- `gate`

and explicitly removed two L0 outputs:

- `possible_fake_verification`
- `possible_interaction_required`

In code, those two fields are now deleted from `specialized_surface_signals`, and their dedicated keyword families and reason codes are removed as well.  
In docs, `L0_DESIGN_V1.md` now records an L0 specialized contract that keeps only `gambling / adult / gate / challenge / CAPTCHA`.  
This change also further tightened the three trigger families, especially by collapsing gate triggering back to verification semantics, challenge prompts, provider hints, and runtime support signals rather than keeping separate fake-verification / interaction-required semantics.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- removed `FAKE_VERIFICATION_KEYWORDS`
- removed `PERMISSION_INDUCEMENT_KEYWORDS`
- folded some previously fake-verification-like gate wording into `GATE_SURFACE_KEYWORDS`
- removed from `derive_specialized_surface_signals(...)`:
  - `possible_fake_verification`
  - `possible_interaction_required`
  - the corresponding `matched_keywords` entries
  - the corresponding reason codes
- tightened the formation rules for `possible_gate_or_evasion` and `possible_challenge_surface`
- bumped `schema_version` from `evt_v1.1` to `evt_v1.2`
- removed the `derive_rule_labels(...)` evasion-tag branch that depended on `possible_fake_verification`

### Doc Changes

- updated `L0_DESIGN_V1.md`
- added task doc: `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- added handoff doc: `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

### Output / Artifact Changes

- removed from `auto_labels.specialized_surface_signals`:
  - `possible_fake_verification`
  - `possible_interaction_required`
- removed from `auto_labels.specialized_surface_signals.matched_keywords`:
  - `fake_verification`
  - `permission_inducement`
- changed `auto_labels.schema_version` to `evt_v1.2`
- changed `rule_labels.schema_version` to `evt_v1.2`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

---

## 4. Behavior Impact

### Expected New Behavior

- L0 specialized outputs now keep only:
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
  - `possible_adult_lure`
  - `possible_age_gate_surface`
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
- `possible_fake_verification` is no longer an L0 field
- `possible_interaction_required` is no longer an L0 field
- gate triggering now depends primarily on:
  - strong gate / challenge semantics
  - captcha / anti-bot / cloaking / variant-failed / dynamic-redirect support signals
- representative gambling / adult / gate samples still emit the expected specialized signals

### Preserved Behavior

- `no_early_stop_candidate`, `need_text_semantic_candidate`, `need_vision_candidate`, and `need_l2_candidate` remain present
- the three specialized families `gambling` / `adult` / `gate` remain present
- capture-side call patterns are unchanged

### User-facing / CLI Impact

- no CLI change

### Output Format Impact

- there is a breaking schema change because two specialized fields were removed

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: NO
- Public interface changed: PARTIALLY
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- removed `auto_labels.specialized_surface_signals.possible_fake_verification`
- removed `auto_labels.specialized_surface_signals.possible_interaction_required`
- removed `auto_labels.specialized_surface_signals.matched_keywords.fake_verification`
- removed `auto_labels.specialized_surface_signals.matched_keywords.permission_inducement`
- bumped `schema_version` from `evt_v1.1` to `evt_v1.2`

Compatibility notes:

Any downstream script that explicitly reads those removed fields will break.  
This is a user-requested contract trim rather than a backward-compatible extension.  
CLI entrypoints are unchanged, but the output schema is not backward compatible.

---

## 6. Validation Performed

### Commands Run

```bash
Select-String -Path "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py","E:\Warden\L0_DESIGN_V1.md" -Pattern "possible_fake_verification|possible_interaction_required|FAKE_VERIFICATION_KEYWORDS|PERMISSION_INDUCEMENT_KEYWORDS"
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
```

```bash
PowerShell heredoc piped to `python -`:
- import `derive_auto_labels_from_sample_dir` and `derive_rule_labels`
- run smoke checks on:
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\cobbercasino.org_20260408T093616Z`
  - `E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\pornamateur.net_20260408T073300Z`
  - `E:\Warden\data\raw\benign\gate\kill-bot.net_20260402T164619Z`
- print:
  - `specialized_surface_signals`
  - `l0_routing_hints`
  - `rule_flags`
  - `primary_label`
```

### Result

- the residual-string check returned empty, which confirms that the removed L0 fields no longer appear in the implementation or in `L0_DESIGN_V1.md`
- syntax check passed
- the gambling sample still emitted:
  - `possible_gambling_lure`
  - `possible_bonus_or_betting_induction`
- the adult sample still emitted:
  - `possible_adult_lure`
- the gate sample still emitted:
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
- none of the three representative samples contained:
  - `possible_fake_verification`
  - `possible_interaction_required`

### Not Run

- rerunning the 100-sample regression
- full-dataset regression

Reason:

This task prioritized the contract trim and focused validation rather than repeating the broader regression slice immediately.

---

## 7. Risks / Caveats

- this is a field-removal change and is not backward compatible; any downstream code that depends on the removed fields must be updated
- although `gate` remains present, this task did not systematically solve the gate false-trigger issue on ordinary benign pages
- `need_l2_candidate` still remains inside the routing hints, so the escalation-hint path for gate / adult / gambling is still active
- historical handoff and regression docs still mention the old fields because they record past state rather than the current contract

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-10_l0_specialized_detectors_contract_trim.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_contract_trim.md`

Doc debt still remaining:

- a future task should still tighten gate false triggers further

---

## 9. Recommended Next Step

- rerun a small-batch regression to measure gambling / adult / gate separation after the two-field removal
- open a dedicated `gate tightening` task to reduce gate false triggers on ordinary benign pages
