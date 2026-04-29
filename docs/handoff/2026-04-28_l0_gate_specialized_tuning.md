# L0 Gate Specialized Tuning Handoff

## 中文版

> 面向人工阅读的摘要版。英文版为权威版本；若数值、验证命令、兼容性结论或状态表述有冲突，以英文版为准。

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- Related Task ID: `TASK-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- Task Title: `L0 gate specialized tuning with score-guided low-cost evidence`
- Module: `Inference / L0`
- Author: `Codex`
- Date: `2026-04-28`
- Status: `DONE`

## 1. Executive Summary

本次交付把 L0 gate detector 从基础 keyword / routing signal 推进到可解释 score-guided gate specialization。实现保持当前 L0 低成本边界：未启用 full HTML、default brand extraction、screenshot/OCR、heavy model、interaction recovery 或 gate solving。

baseline 显示 gate recall 偏低：malicious gate `65.29%`，benign gate `57.07%`，combined gate `62.11%`。调参后，malicious gate 提升到 `71.34%`，benign gate 提升到 `69.19%`，combined gate 提升到 `70.51%`。后续按 recommended next step 执行了更大的 900-sample/control 回归：adult gate hit `3 / 900 = 0.33%`，gambling gate hit `4 / 900 = 0.44%`，Tranco gate hit `7 / 900 = 0.78%`。

## 2. What Changed

### Code Changes

- 在 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中稳定 gate 词族：
  - `GATE_URL_KEYWORDS`
  - `GATE_SHORT_FLOW_KEYWORDS`
  - `GATE_IDENTITY_FLOW_KEYWORDS`
- 扩展 `GATE_SURFACE_KEYWORDS` / `GATE_STRONG_KEYWORDS`，覆盖 IDP verification、算术验证、humancheck、box-to-verify、Incapsula、prove-human 等低成本 gate evidence。
- 在 `src/warden/module/l0.py` 中新增 additive gate explainability fields：
  - `gate_weighted_score`
  - `gate_weighted_score_reasons`
  - `gate_score_evidence`
- 用 gate score 参与 `possible_challenge_surface` / `possible_gate_or_evasion`，同时收紧判定，避免仅凭 `short_loading_flow + needs_interaction` 或无文本 `captcha_or_antibot` 单独大面积触发。

### Doc Changes

- 更新 `docs/modules/L0_DESIGN_V1.md`，补充 gate score 字段和 gate routing-support 语义。
- 更新 `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md` 状态为 `DONE`。
- 新增本 handoff 文档。

### Output / Artifact Changes

- 无新增数据 artifact。
- 本 handoff 记录 baseline / after 小批量回归结果。

## 3. Files Touched

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

## 4. Behavior Impact

### Expected New Behavior

- Gate detector now emits explainable gate score fields.
- IDP verification / equation-code verification / Incapsula / humancheck / prove-human patterns are more likely to trigger gate.
- Gate recall improves on both malicious gate and benign gate pools.

### Preserved Behavior

- Existing gate fields remain:
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - `specialized_fast_resolution_candidate`
- Gate output remains weak-signal / routing-hint oriented.
- `specialized_fast_resolution_candidate` is not redefined as final judgment.
- No default full HTML, brand extraction, screenshot/OCR, heavy model, or interaction path was added.

### User-facing / CLI Impact

- No CLI changed.

### Output Format Impact

- Additive output fields were added under `specialized_surface_signals`.

## 5. Schema / Interface Impact

- Schema changed: `YES, additive only`
- Backward compatible: `YES`
- Public interface changed: `YES, additive fields only`
- Existing CLI still valid: `YES`

Added fields:

- `specialized_surface_signals.gate_weighted_score`
- `specialized_surface_signals.gate_weighted_score_reasons`
- `specialized_surface_signals.gate_score_evidence`

Compatibility notes:

No existing fields were removed or renamed. Existing consumers that ignore unknown fields remain compatible.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py

# Baseline and after regression were run with a fixed seed:
# seed = 20260428
# malicious_gate: E:\WardenData\raw\phish\gate, full 314
# benign_gate: E:\WardenData\raw\benign\gate, full 198
# adult_control: E:\WardenData\raw\benign\adult, sampled 300
# gambling_control: E:\WardenData\raw\benign\gambling, sampled 300
# tranco_control: E:\WardenData\raw\benign\tranco, sampled 300

# Larger mixed regression follow-up was run with the same fixed seed:
# seed = 20260428
# malicious_gate: E:\WardenData\raw\phish\gate, full 314
# benign_gate: E:\WardenData\raw\benign\gate, full 198
# adult_control_large: E:\WardenData\raw\benign\adult, sampled 900
# gambling_control_large: E:\WardenData\raw\benign\gambling, sampled 900
# tranco_control_large: E:\WardenData\raw\benign\tranco, sampled 900
```

### Result

Baseline:

- malicious gate: `205 / 314 = 65.29%`
- benign gate: `113 / 198 = 57.07%`
- combined gate: `318 / 512 = 62.11%`
- adult control gate hit: `1 / 300 = 0.33%`
- gambling control gate hit: `1 / 300 = 0.33%`
- Tranco control gate hit: `1 / 300 = 0.33%`

After tuning:

- malicious gate: `224 / 314 = 71.34%`
- benign gate: `137 / 198 = 69.19%`
- combined gate: `361 / 512 = 70.51%`
- adult control gate hit: `2 / 300 = 0.67%`
- gambling control gate hit: `2 / 300 = 0.67%`
- Tranco control gate hit: `1 / 300 = 0.33%`

Remaining miss bucket:

- malicious gate misses: `90`, including `86` with no gate keywords
- benign gate misses: `61`, including `59` with no gate keywords
- Main residual cause: truly empty or near-empty visible text/title-only login shells without cheap gate wording. These remain better suited for L1 under the current L0 no-heavy-evidence boundary.

Latency spot check:

- malicious gate mean: `3.989 ms -> 4.364 ms`
- benign gate mean: `4.029 ms -> 3.929 ms`
- adult control mean: `38.610 ms -> 59.819 ms`
- gambling control mean: `42.578 ms -> 62.342 ms`
- Tranco control mean: `35.435 ms -> 55.713 ms`

The added gate score emits many nonzero explainability scores on control pools, but tightened trigger logic keeps actual gate hits low.

Larger mixed regression follow-up:

- malicious gate: `224 / 314 = 71.34%`; mean `4.185 ms`, p95 `6.015 ms`
- benign gate: `137 / 198 = 69.19%`; mean `3.983 ms`, p95 `5.820 ms`
- combined gate: `361 / 512 = 70.51%`
- adult control gate hit: `3 / 900 = 0.33%`; mean `57.034 ms`, p95 `132.324 ms`
- gambling control gate hit: `4 / 900 = 0.44%`; mean `46.379 ms`, p95 `115.455 ms`
- Tranco control gate hit: `7 / 900 = 0.78%`; mean `51.512 ms`, p95 `128.507 ms`

Large-run FP notes:

- Adult control hits were dominated by `needs_interaction_support` with Cloudflare/CAPTCHA or one identity-flow case.
- Gambling control hits were dominated by Cloudflare/CAPTCHA, security verification, or notification-gate wording; some co-occurred with gambling surface evidence.
- Tranco control hits were all CAPTCHA / anti-bot surfaces, mainly Cloudflare, Turnstile, or generic CAPTCHA.

Large-run miss notes:

- malicious gate misses: `90`, including `86` with no gate keywords
- benign gate misses: `61`, including `59` with no gate keywords
- The larger run confirms the same residual limit: most misses have no cheap visible-text gate keyword evidence.

### Not Run

- No full-dataset rerun across all adult/gambling/Tranco pools.
- No downstream training/evaluation pipeline run.
- No schema registry update.

Reason:

The task was scoped to L0 gate tuning and bounded regression over the specified gate/control pools.

## 7. Risks / Caveats

- The new score fields are additive schema surface. Downstream scripts that assume a fixed exact key set may need a spot check.
- Remaining misses are mostly no-keyword / empty-visible-text cases. Recovering them inside L0 would require broader heuristics or heavier evidence, which conflicts with the current L0 boundary.
- The latency spot check shows higher mean time on sampled control pools. The added explainability scoring is still low-cost, but further performance work should be a separate task if needed.
- The larger mixed regression shows low cross-family gate hit rates, but the Tranco control rate increased to `7 / 900 = 0.78%`; these examples are mostly real CAPTCHA / anti-bot surfaces and should be treated as gate-surface routing signals, not malicious judgments.

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

Doc debt still remaining:

- If additive score fields are later promoted into a frozen schema registry, update frozen schema docs in a separate task.

## 9. Recommended Next Step

- Larger mixed regression has been completed. Do not loosen the current gate threshold inside this task; the remaining misses are mostly no-keyword / empty-visible-text cases.
- If recall must go beyond about `70%` under L0, open a separate `empty-visible-text gate recovery` task and explicitly decide whether the added latency / FP risk is acceptable.
- If latency becomes the priority, open a separate L0 scoring profiler task focused on control-pool mean/p95 time rather than adding more gate evidence.

## English Version

> AI note: The English section is authoritative for exact validation, compatibility, and follow-up boundaries.

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- Related Task ID: `TASK-L0-2026-04-28-GATE-SPECIALIZED-TUNING`
- Task Title: `L0 gate specialized tuning with score-guided low-cost evidence`
- Module: `Inference / L0`
- Author: `Codex`
- Date: `2026-04-28`
- Status: `DONE`

## 1. Executive Summary

This delivery moves the L0 gate detector from basic keyword / routing signals to an explainable score-guided gate specialization. It preserves the current low-cost L0 boundary: no default full HTML, default brand extraction, screenshot/OCR, heavy model, interaction recovery, or gate solving was added.

Baseline gate recall was low: malicious gate `65.29%`, benign gate `57.07%`, combined gate `62.11%`. After tuning, malicious gate improved to `71.34%`, benign gate improved to `69.19%`, and combined gate improved to `70.51%`. A larger 900-sample/control follow-up was run per the recommended next step: adult gate hit `3 / 900 = 0.33%`, gambling gate hit `4 / 900 = 0.44%`, and Tranco gate hit `7 / 900 = 0.78%`.

## 2. What Changed

### Code Changes

- Stabilized gate keyword families in `scripts/labeling/Warden_auto_label_utils_brandlex.py`:
  - `GATE_URL_KEYWORDS`
  - `GATE_SHORT_FLOW_KEYWORDS`
  - `GATE_IDENTITY_FLOW_KEYWORDS`
- Expanded `GATE_SURFACE_KEYWORDS` / `GATE_STRONG_KEYWORDS` to cover low-cost evidence for IDP verification, equation-code verification, humancheck, box-to-verify wording, Incapsula, and prove-human wording.
- Added additive gate explainability fields in `src/warden/module/l0.py`:
  - `gate_weighted_score`
  - `gate_weighted_score_reasons`
  - `gate_score_evidence`
- Used gate score as support for `possible_challenge_surface` / `possible_gate_or_evasion`, while keeping trigger logic tight enough that `short_loading_flow + needs_interaction` or textless `captcha_or_antibot` alone does not broadly trigger gate.

### Doc Changes

- Updated `docs/modules/L0_DESIGN_V1.md` with gate score fields and gate routing-support semantics.
- Updated `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md` to `DONE`.
- Added this handoff document.

### Output / Artifact Changes

- No data artifact was added.
- This handoff records the baseline / after bounded regression results.

## 3. Files Touched

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

## 4. Behavior Impact

### Expected New Behavior

- The gate detector now emits explainable gate score fields.
- IDP verification / equation-code verification / Incapsula / humancheck / prove-human patterns are more likely to trigger gate.
- Gate recall improves on both malicious gate and benign gate pools.

### Preserved Behavior

- Existing gate fields remain:
  - `possible_gate_or_evasion`
  - `possible_challenge_surface`
  - `matched_keywords.gate_text`
  - `matched_keywords.gate_url`
  - `specialized_fast_resolution_candidate`
- Gate output remains weak-signal / routing-hint oriented.
- `specialized_fast_resolution_candidate` is not redefined as final judgment.
- No default full HTML, brand extraction, screenshot/OCR, heavy model, or interaction path was added.

### User-facing / CLI Impact

- No CLI changed.

### Output Format Impact

- Additive output fields were added under `specialized_surface_signals`.

## 5. Schema / Interface Impact

- Schema changed: `YES, additive only`
- Backward compatible: `YES`
- Public interface changed: `YES, additive fields only`
- Existing CLI still valid: `YES`

Added fields:

- `specialized_surface_signals.gate_weighted_score`
- `specialized_surface_signals.gate_weighted_score_reasons`
- `specialized_surface_signals.gate_score_evidence`

Compatibility notes:

No existing fields were removed or renamed. Existing consumers that ignore unknown fields remain compatible.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py

# Baseline and after regression were run with a fixed seed:
# seed = 20260428
# malicious_gate: E:\WardenData\raw\phish\gate, full 314
# benign_gate: E:\WardenData\raw\benign\gate, full 198
# adult_control: E:\WardenData\raw\benign\adult, sampled 300
# gambling_control: E:\WardenData\raw\benign\gambling, sampled 300
# tranco_control: E:\WardenData\raw\benign\tranco, sampled 300

# Larger mixed regression follow-up was run with the same fixed seed:
# seed = 20260428
# malicious_gate: E:\WardenData\raw\phish\gate, full 314
# benign_gate: E:\WardenData\raw\benign\gate, full 198
# adult_control_large: E:\WardenData\raw\benign\adult, sampled 900
# gambling_control_large: E:\WardenData\raw\benign\gambling, sampled 900
# tranco_control_large: E:\WardenData\raw\benign\tranco, sampled 900
```

### Result

Baseline:

- malicious gate: `205 / 314 = 65.29%`
- benign gate: `113 / 198 = 57.07%`
- combined gate: `318 / 512 = 62.11%`
- adult control gate hit: `1 / 300 = 0.33%`
- gambling control gate hit: `1 / 300 = 0.33%`
- Tranco control gate hit: `1 / 300 = 0.33%`

After tuning:

- malicious gate: `224 / 314 = 71.34%`
- benign gate: `137 / 198 = 69.19%`
- combined gate: `361 / 512 = 70.51%`
- adult control gate hit: `2 / 300 = 0.67%`
- gambling control gate hit: `2 / 300 = 0.67%`
- Tranco control gate hit: `1 / 300 = 0.33%`

Remaining miss bucket:

- malicious gate misses: `90`, including `86` with no gate keywords
- benign gate misses: `61`, including `59` with no gate keywords
- Main residual cause: truly empty or near-empty visible text/title-only login shells without cheap gate wording. These remain better suited for L1 under the current L0 no-heavy-evidence boundary.

Latency spot check:

- malicious gate mean: `3.989 ms -> 4.364 ms`
- benign gate mean: `4.029 ms -> 3.929 ms`
- adult control mean: `38.610 ms -> 59.819 ms`
- gambling control mean: `42.578 ms -> 62.342 ms`
- Tranco control mean: `35.435 ms -> 55.713 ms`

The added gate score emits many nonzero explainability scores on control pools, but tightened trigger logic keeps actual gate hits low.

Larger mixed regression follow-up:

- malicious gate: `224 / 314 = 71.34%`; mean `4.185 ms`, p95 `6.015 ms`
- benign gate: `137 / 198 = 69.19%`; mean `3.983 ms`, p95 `5.820 ms`
- combined gate: `361 / 512 = 70.51%`
- adult control gate hit: `3 / 900 = 0.33%`; mean `57.034 ms`, p95 `132.324 ms`
- gambling control gate hit: `4 / 900 = 0.44%`; mean `46.379 ms`, p95 `115.455 ms`
- Tranco control gate hit: `7 / 900 = 0.78%`; mean `51.512 ms`, p95 `128.507 ms`

Large-run FP notes:

- Adult control hits were dominated by `needs_interaction_support` with Cloudflare/CAPTCHA or one identity-flow case.
- Gambling control hits were dominated by Cloudflare/CAPTCHA, security verification, or notification-gate wording; some co-occurred with gambling surface evidence.
- Tranco control hits were all CAPTCHA / anti-bot surfaces, mainly Cloudflare, Turnstile, or generic CAPTCHA.

Large-run miss notes:

- malicious gate misses: `90`, including `86` with no gate keywords
- benign gate misses: `61`, including `59` with no gate keywords
- The larger run confirms the same residual limit: most misses have no cheap visible-text gate keyword evidence.

### Not Run

- No full-dataset rerun across all adult/gambling/Tranco pools.
- No downstream training/evaluation pipeline run.
- No schema registry update.

Reason:

The task was scoped to L0 gate tuning and bounded regression over the specified gate/control pools.

## 7. Risks / Caveats

- The new score fields are additive schema surface. Downstream scripts that assume a fixed exact key set may need a spot check.
- Remaining misses are mostly no-keyword / empty-visible-text cases. Recovering them inside L0 would require broader heuristics or heavier evidence, which conflicts with the current L0 boundary.
- The latency spot check shows higher mean time on sampled control pools. The added explainability scoring is still low-cost, but further performance work should be a separate task if needed.
- The larger mixed regression shows low cross-family gate hit rates, but the Tranco control rate increased to `7 / 900 = 0.78%`; these examples are mostly real CAPTCHA / anti-bot surfaces and should be treated as gate-surface routing signals, not malicious judgments.

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-28_l0_gate_specialized_tuning.md`
- `docs/handoff/2026-04-28_l0_gate_specialized_tuning.md`

Doc debt still remaining:

- If additive score fields are later promoted into a frozen schema registry, update frozen schema docs in a separate task.

## 9. Recommended Next Step

- The larger mixed regression has been completed. Do not loosen the current gate threshold inside this task; remaining misses are mostly no-keyword / empty-visible-text cases.
- If recall must go beyond about `70%` under L0, open a separate `empty-visible-text gate recovery` task and explicitly decide whether the added latency / FP risk is acceptable.
- If latency becomes the priority, open a separate L0 scoring profiler task focused on control-pool mean/p95 time rather than adding more gate evidence.
