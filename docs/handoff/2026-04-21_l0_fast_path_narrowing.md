# L0 fast-path narrowing handoff

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-FAST-PATH-NARROWING`
- Related Task ID: `TASK-L0-2026-04-21-FAST-PATH-NARROWING`
- Task Title: `Narrow L0 into a gambling/adult/gate fast path and remove HTML and brand from the default hot path`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

## 1. Executive Summary

这次交付把默认 L0 热路径收窄成更明确的 `gambling / adult / gate` specialized fast path。  
默认热路径里已经去掉完整 `HTML` 特征提取和默认 `brand` 提取，但 `html_features` / `brand_signals` 字段仍保留兼容默认值。  
在固定 `50` 样本切片上，均值延迟从 `84.424 ms / sample` 降到 `21.391 ms / sample`，同时 adult / gambling / gate 主 specialized 触发保持稳定。

## 2. What Changed

### Code Changes

- 在 `src/warden/module/l0.py` 中让默认热路径不再扫描 `html_rendered/html_raw`，`html_features` 直接走兼容默认值。
- 在 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中让默认热路径不再做 `extract_claimed_brands(...)` / `extract_claimed_brands_from_url(...)`，`brand_signals` 直接输出兼容默认值。
- 调整 `derive_l0_routing_hints(...)`，让普通非 specialized 页面默认带上 `need_text_semantic_candidate`，更明确地继续交给 `L1`。
- 补了 `src/warden/module/l0.py` 内部的 specialized 常量 fallback 和本地 `has_adult_domain_hint(...)`，修掉当前 working tree 下 active L0 导入会炸的问题。

### Doc Changes

- 更新任务文档边界和完成状态：`docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- 更新模块文档：`docs/modules/MODULE_INFER.md`
- 更新 L0 设计文档：`docs/modules/L0_DESIGN_V1.md`

### Output / Artifact Changes

- none
- none
- none

## 3. Files Touched

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

Optional notes per file:

- `src/warden/module/l0.py`: active L0 hot-path narrowing and routing changes live here.
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: only compatibility-layer hot-path wiring changed.
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`: task boundary aligned to current active module location and real gate sample path.

## 4. Behavior Impact

### Expected New Behavior

- 默认 L0 不再做完整 `HTML` 扫描。
- 默认 L0 不再做 `brand` 提取。
- 普通非 specialized 页面默认更明确地带着 `need_text_semantic_candidate` 继续到 `L1`。
- `gambling / adult / gate` 的 specialized surface 仍然只靠低成本 URL / text / form / net-summary 路径触发。

### Preserved Behavior

- `derive_auto_labels(...)` 和 `derive_auto_labels_from_sample_dir(...)` 入口未改。
- `html_features`、`brand_signals`、`specialized_surface_signals`、`l0_routing_hints` 等冻结字段仍然存在。
- 这次没有改 `L1` / `L2` 逻辑，也没有改下游 backfill CLI。

### User-facing / CLI Impact

- 无新增 CLI；现有 sample-dir labeling 和 backfill 调用方式保持不变。

### Output Format Impact

- 输出字段未删；`html_features` 和 `brand_signals` 现在在默认热路径上会更常见地呈现为空/默认值结构。

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `html_features`
- `brand_signals`
- `l0_routing_hints.need_text_semantic_candidate`

Compatibility notes:

字段名和接口名都没有变。  
兼容方式是保留原字段存在性，但让默认热路径输出默认值结构。  
这意味着任何依赖 “字段存在” 的下游不需要改，但如果有下游隐式依赖 “L0 默认会产出 brand claim 或 HTML 特征内容”，它的行为预期需要同步更新。

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python - <<'PY'
import sys
sys.path.insert(0, r'E:\Warden\src')
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as auto
from warden.module import l0
print("IMPORT_OK")
PY
python - <<'PY'
# deterministic 50-sample before/after latency and trigger regression
# seed=20260421
# 20 benign + 10 adult + 10 gambling + 10 gate
PY
python - <<'PY'
# one smoke sample to verify html_features default zeros,
# brand_signals default no_brand_claim,
# and need_text_semantic_candidate behavior
PY
```

### Result

- `py_compile` 通过。
- import smoke 通过。
- 固定切片 before / after 延迟：
  - before mean: `84.424 ms / sample`
  - after mean: `21.391 ms / sample`
  - absolute reduction: `63.033 ms`
  - relative reduction: about `74.66%`
- 分组均值 before / after：
  - benign: `98.699 -> 26.135 ms`
  - adult: `105.954 -> 24.963 ms`
  - gambling: `109.066 -> 27.211 ms`
  - gate: `9.705 -> 2.513 ms`
- specialized trigger 对比：
  - benign:
    - `possible_gambling_lure`: `0 / 20 -> 0 / 20`
    - `possible_adult_lure`: `0 / 20 -> 0 / 20`
    - `possible_age_gate_surface`: `0 / 20 -> 0 / 20`
    - `possible_gate_or_evasion`: `0 / 20 -> 0 / 20`
  - adult:
    - `possible_adult_lure`: `7 / 10 -> 7 / 10`
    - `possible_age_gate_surface`: `2 / 10 -> 2 / 10`
  - gambling:
    - `possible_gambling_lure`: `5 / 10 -> 5 / 10`
  - gate:
    - `possible_gate_or_evasion`: `3 / 10 -> 3 / 10`
- after 切片上的新增路由表现：
  - benign `need_text_semantic_candidate`: `20 / 20`
  - adult `need_text_semantic_candidate`: `9 / 10`
  - gambling `need_text_semantic_candidate`: `6 / 10`
  - gate `need_text_semantic_candidate`: `9 / 10`
- smoke sample 显示：
  - `html_features` 为全默认零值结构
  - `brand_signals.domain_brand_consistency_candidate = "no_brand_claim"`
  - `need_text_semantic_candidate = True`

### Not Run

- full dataset rerun
- full benchmark harness
- downstream consumer audit beyond compile/smoke

Reason:

这条 task 的边界是窄实现加 bounded regression，不是全量重跑或更大范围的联调任务。

## 7. Risks / Caveats

- 去掉默认热路径 `brand` 后，L0 不再利用 brand mismatch 作为默认弱风险来源；这会把更多 brand-sensitive 判断压力留给 `L1` 或后续路径。
- 去掉默认热路径 `HTML` 后，依赖 HTML 中 captcha/download/JS 结构的廉价线索默认也不再参与；当前 gate specialized 更依赖文本、URL 和低成本网络摘要。
- 为了跑通当前 working tree，这次顺手补了 specialized 常量 fallback；说明旧脚本与新模块之间仍有一部分共享常量债务。

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

Doc debt still remaining:

- 如果后续要把 specialized keyword scanning 本身继续提速，需要单开下一条 task，不能再混进本条 task。
- shared specialized constants 仍有进一步整理价值，但那是单独的 stabilization 任务。

## 9. Recommended Next Step

- 下一条建议开 `specialized keyword scan consolidation`，只盯 `derive_specialized_surface_signals(...)` 的重复扫描。
- 如果后续确认 brand 仍然要在某些路径保留，建议做显式 gated brand path，而不是回到默认热路径。
- 如果要继续做可比 benchmark，复用同一个 `seed=20260421` 的 `50` 样本切片。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-FAST-PATH-NARROWING`
- Related Task ID: `TASK-L0-2026-04-21-FAST-PATH-NARROWING`
- Task Title: `Narrow L0 into a gambling/adult/gate fast path and remove HTML and brand from the default hot path`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

This delivery narrowed the default L0 hot path into a more explicit `gambling / adult / gate` specialized fast path.  
The default hot path no longer performs full `HTML` feature extraction or default `brand` extraction, while `html_features` and `brand_signals` remain present with compatibility-safe default values.  
On the fixed `50`-sample slice, mean latency dropped from `84.424 ms / sample` to `21.391 ms / sample`, while the primary adult / gambling / gate specialized trigger behavior remained stable.

## 2. What Changed

### Code Changes

- Changed `src/warden/module/l0.py` so the default hot path no longer scans `html_rendered/html_raw`; `html_features` now uses compatibility-safe default values.
- Changed `scripts/labeling/Warden_auto_label_utils_brandlex.py` so the default hot path no longer runs `extract_claimed_brands(...)` or `extract_claimed_brands_from_url(...)`; `brand_signals` now uses compatibility-safe default values.
- Adjusted `derive_l0_routing_hints(...)` so ordinary non-specialized pages default more explicitly toward `L1` via `need_text_semantic_candidate`.
- Added internal fallback constants and a local `has_adult_domain_hint(...)` implementation in `src/warden/module/l0.py` so the active L0 path no longer fails to import when the legacy script lacks some specialized constant definitions.

### Doc Changes

- Updated task boundary and completion state in `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`.
- Updated `docs/modules/MODULE_INFER.md`.
- Updated `docs/modules/L0_DESIGN_V1.md`.

### Output / Artifact Changes

- none
- none
- none

## 3. Files Touched

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

Optional notes per file:

- `src/warden/module/l0.py`: active L0 hot-path narrowing and routing changes live here.
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: only compatibility-layer hot-path wiring changed.
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`: task scope was aligned to the actual active module location and the real gate sample directory.

## 4. Behavior Impact

### Expected New Behavior

- The default L0 path no longer performs full `HTML` scanning.
- The default L0 path no longer performs `brand` extraction.
- Ordinary non-specialized pages now more explicitly carry `need_text_semantic_candidate` and continue toward `L1`.
- `gambling / adult / gate` specialized surfaces still trigger from cheap URL / text / form / net-summary evidence only.

### Preserved Behavior

- The `derive_auto_labels(...)` and `derive_auto_labels_from_sample_dir(...)` entrypoints did not change.
- Frozen output fields such as `html_features`, `brand_signals`, `specialized_surface_signals`, and `l0_routing_hints` still exist.
- This task did not modify `L1` / `L2` logic and did not modify the downstream backfill CLI.

### User-facing / CLI Impact

- No new CLI was added; existing sample-dir labeling and backfill call paths remain valid.

### Output Format Impact

- No fields were removed; `html_features` and `brand_signals` now more often carry empty/default structures on the default hot path.

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `html_features`
- `brand_signals`
- `l0_routing_hints.need_text_semantic_candidate`

Compatibility notes:

Field names and public entrypoints did not change.  
Compatibility is preserved by keeping the same fields present while populating them with default structures on the narrowed hot path.  
Any downstream consumer that only relies on field presence should remain compatible, but any downstream logic that implicitly expects default L0 execution to produce brand claims or rich HTML-derived features should update its expectations.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python - <<'PY'
import sys
sys.path.insert(0, r'E:\Warden\src')
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as auto
from warden.module import l0
print("IMPORT_OK")
PY
python - <<'PY'
# deterministic 50-sample before/after latency and trigger regression
# seed=20260421
# 20 benign + 10 adult + 10 gambling + 10 gate
PY
python - <<'PY'
# one smoke sample to verify html_features default zeros,
# brand_signals default no_brand_claim,
# and need_text_semantic_candidate behavior
PY
```

### Result

- `py_compile` passed.
- Import smoke passed.
- Fixed-slice before / after latency:
  - before mean: `84.424 ms / sample`
  - after mean: `21.391 ms / sample`
  - absolute reduction: `63.033 ms`
  - relative reduction: about `74.66%`
- Per-group means before / after:
  - benign: `98.699 -> 26.135 ms`
  - adult: `105.954 -> 24.963 ms`
  - gambling: `109.066 -> 27.211 ms`
  - gate: `9.705 -> 2.513 ms`
- Specialized trigger comparison:
  - benign:
    - `possible_gambling_lure`: `0 / 20 -> 0 / 20`
    - `possible_adult_lure`: `0 / 20 -> 0 / 20`
    - `possible_age_gate_surface`: `0 / 20 -> 0 / 20`
    - `possible_gate_or_evasion`: `0 / 20 -> 0 / 20`
  - adult:
    - `possible_adult_lure`: `7 / 10 -> 7 / 10`
    - `possible_age_gate_surface`: `2 / 10 -> 2 / 10`
  - gambling:
    - `possible_gambling_lure`: `5 / 10 -> 5 / 10`
  - gate:
    - `possible_gate_or_evasion`: `3 / 10 -> 3 / 10`
- New routing behavior on the after slice:
  - benign `need_text_semantic_candidate`: `20 / 20`
  - adult `need_text_semantic_candidate`: `9 / 10`
  - gambling `need_text_semantic_candidate`: `6 / 10`
  - gate `need_text_semantic_candidate`: `9 / 10`
- The smoke sample confirmed:
  - `html_features` is now an all-default zero-value structure
  - `brand_signals.domain_brand_consistency_candidate = "no_brand_claim"`
  - `need_text_semantic_candidate = True`

### Not Run

- full dataset rerun
- full benchmark harness
- downstream consumer audit beyond compile/smoke

Reason:

This task was intentionally scoped as a narrow implementation plus bounded regression, not a full rerun or broader integration task.

## 7. Risks / Caveats

- With default-path `brand` removed, L0 no longer uses brand mismatch as a default weak-risk source; more brand-sensitive judgment now shifts to `L1` or later paths.
- With default-path `HTML` removed, cheap cues derived from HTML-side captcha/download/JS structure no longer participate by default; current gate specialized behavior therefore depends more on text, URL, and cheap network summary evidence.
- To make the current working tree runnable, this task also restored missing specialized constant coverage via fallbacks; that indicates there is still shared-constant debt between the legacy script and the active L0 module.

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

Doc debt still remaining:

- If specialized keyword scanning itself should be accelerated next, that needs a separate task and should not be folded back into this one.
- The shared specialized-constant layer still has cleanup value, but that is a separate stabilization task.

## 9. Recommended Next Step

- Open the next task for `specialized keyword scan consolidation`, focused only on repeated scanning inside `derive_specialized_surface_signals(...)`.
- If brand evidence must remain available on some paths, introduce an explicit gated brand path instead of putting it back into the default hot path.
- If you want future benchmark comparisons to stay clean, reuse the same `seed=20260421` `50`-sample slice.
