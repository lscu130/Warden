# L0 module extraction handoff

## 中文版

> 面向人类阅读的摘要版。英文版是权威版本；若事实、命令、兼容性结论有冲突，以英文版为准。

## 1. Executive Summary

本次交付把当前 auto-label 路径里的活动 L0 逻辑独立到了 `src/warden/module/l0.py`，同时在 `src/warden/module/` 下新增了 `l1.py` 与 `l2.py` 作为明确阶段占位模块。

`scripts/labeling/Warden_auto_label_utils_brandlex.py` 的对外入口 `derive_auto_labels(...)` 与 `derive_auto_labels_from_sample_dir(...)` 保持不变，现已改为委托新模块执行活动中的 L0 特征准备与阶段输出拼装。一次真实样本烟测显示输出 schema 关键字段保持存在。

## 2. What Changed

### Code Changes

- 新增 `src/warden/module/` 包，并建立 `l0.py`、`l1.py`、`l2.py`。
- 将活动中的 L0 特征准备与阶段输出逻辑收敛到 `src/warden/module/l0.py`。
- `scripts/labeling/Warden_auto_label_utils_brandlex.py` 的 `derive_auto_labels(...)` 改为在运行时导入并调用 `warden.module.l0`。
- 新增 `src/warden/__init__.py` 与 `src/warden/module/__init__.py` 以支持包导入。
- 在 `Warden_auto_label_utils_brandlex.py` 顶部补充 `src` 路径注入，确保新包可被现有脚本入口加载。

### Doc Changes

- 更新 `docs/modules/MODULE_INFER.md`，标注当前 auto-label 参考路径的活动 L0 代码位置。
- 更新 `docs/modules/L0_DESIGN_V1.md`，标注当前活动 L0 实现在 `src/warden/module/l0.py`。
- 新增 repo task 与 handoff 文档。

### Output / Artifact Changes

- `none`

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\src\warden\__init__.py`
- `E:\Warden\src\warden\module\__init__.py`
- `E:\Warden\src\warden\module\l0.py`
- `E:\Warden\src\warden\module\l1.py`
- `E:\Warden\src\warden\module\l2.py`
- `E:\Warden\docs\modules\MODULE_INFER.md`
- `E:\Warden\docs\modules\L0_DESIGN_V1.md`
- `E:\Warden\docs\tasks\2026-04-21_l0_module_extraction.md`
- `E:\Warden\docs\handoff\2026-04-21_l0_module_extraction.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` 仍保留兼容入口和 brand / rule-label / sample-dir 逻辑。
- `src/warden/module/l1.py` 与 `src/warden/module/l2.py` 当前是明确占位模块，没有引入新阶段逻辑。

## 4. Behavior Impact

### Expected New Behavior

- 当前 active L0 执行路径由 `derive_auto_labels(...)` 委托到 `src/warden/module/l0.py`。
- 现有脚本入口和调用方式保持不变。
- 仓库内已有明确的 `L0 / L1 / L2` 代码落点，不再只有一个大脚本承载阶段语义。

### Preserved Behavior

- `derive_auto_labels(...)` 仍从原脚本路径导出。
- `derive_auto_labels_from_sample_dir(...)` 仍从原脚本路径导出。
- smoke 样本上关键输出字段仍存在，`possible_adult_lure` 等 specialized 字段仍可触发。

### User-facing / CLI Impact

- 无新的 CLI。
- 现有 backfill / capture 侧入口保持原路径可用。

### Output Format Impact

- 输出结构未改。
- 本次未新增或重命名 schema 字段。

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- `specialized_surface_signals`
- `l0_routing_hints`

Compatibility notes:

本次属于内部重构。调用方仍从原脚本导入入口函数，输出 key 在 smoke 验证中保持存在。

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\src\warden\module\l1.py
python -m py_compile E:\Warden\src\warden\module\l2.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python - <<'PY'
import sys
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as m
from warden.module import l0, l1, l2
print('derive_auto_labels' in dir(m))
print('derive_auto_labels_from_sample_dir' in dir(m))
print(l0.__name__)
print(l1.module_name())
print(l2.module_name())
PY
python - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as m
sample = Path(r'E:\Warden\data\raw\benign\hard benign\adult\101.ru_20260327T075659Z')
out = m.derive_auto_labels_from_sample_dir(sample, source='smoke')
keys = ['schema_version','page_stage_candidate','language_candidate','url_features','form_features','html_features','brand_signals','intent_signals','evasion_signals','specialized_surface_signals','l0_routing_hints','network_features','risk_outputs']
print(json.dumps({
  'has_all_keys': all(k in out for k in keys),
  'missing': [k for k in keys if k not in out],
  'page_stage_candidate': out.get('page_stage_candidate'),
  'possible_adult_lure': ((out.get('specialized_surface_signals') or {}).get('possible_adult_lure')),
  'module_path': 'warden.module.l0'
}, ensure_ascii=False, indent=2))
PY
```

### Result

- 所有 `py_compile` 成功。
- 现有 auto-label 入口导入成功。
- `warden.module.l0`、`l1`、`l2` 均可导入。
- 真实样本烟测中关键 schema keys 全部存在。
- 真实样本烟测中 `possible_adult_lure = true`，说明 specialized 输出仍在 active 路径上工作。

### Not Run

- 大范围数据回填回归
- 大样本 before/after 输出逐字段 diff
- L1/L2 行为验证

Reason:

本次任务边界是代码组织重构与低成本烟测，不包含大规模行为回归。

## 7. Risks / Caveats

- `Warden_auto_label_utils_brandlex.py` 里仍保留一份旧的内联 L0 helper / stage 实现，当前 active 路径已改走 `src/warden/module/l0.py`，但旧实现尚未做二次清理。这是代码债，不是行为变更。
- `src/warden/module/l1.py` 与 `src/warden/module/l2.py` 当前仅为占位模块，尚未承载真实阶段实现。
- 本次只做了 smoke 验证，没有做大批量 before/after diff，理论上仍存在低概率细节漂移风险。

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\modules\MODULE_INFER.md`
- `E:\Warden\docs\modules\L0_DESIGN_V1.md`
- `E:\Warden\docs\tasks\2026-04-21_l0_module_extraction.md`

Doc debt still remaining:

- 如果后续继续清理 `Warden_auto_label_utils_brandlex.py` 中的 legacy L0 实现，需要再次同步文档，明确“兼容层”边界。

## 9. Recommended Next Step

- 做第二轮窄重构，删除 `Warden_auto_label_utils_brandlex.py` 中不再走 active path 的 legacy L0 内联实现，只保留兼容入口和 brand / I/O 逻辑。
- 如果你下一步要继续做性能收紧，就在 `src/warden/module/l0.py` 上推进，不再在旧脚本里加新 L0 逻辑。
- 如果要真正落地阶段化 runtime，再逐步把 L1 / L2 真实实现接入 `src/warden/module/l1.py` 与 `src/warden/module/l2.py`。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-MODULE-EXTRACTION`
- Related Task ID: `TASK-L0-2026-04-21-MODULE-EXTRACTION`
- Task Title: `Extract L0 into a dedicated warden module package while keeping auto_label behavior unchanged`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

## 1. Executive Summary

This delivery extracted the active L0 logic used by the current auto-label path into `src/warden/module/l0.py` and added `src/warden/module/l1.py` and `src/warden/module/l2.py` as explicit stage placeholder modules.

The external entrypoints in `scripts/labeling/Warden_auto_label_utils_brandlex.py`, including `derive_auto_labels(...)` and `derive_auto_labels_from_sample_dir(...)`, remain unchanged from the caller perspective. The active `derive_auto_labels(...)` path now delegates L0 preparation and stage-output assembly to the new module. A real sample smoke run confirmed that the expected schema keys still exist.

## 2. What Changed

### Code Changes

- Added a new `src/warden/module/` package with `l0.py`, `l1.py`, and `l2.py`.
- Moved the active L0 preparation and stage-output logic into `src/warden/module/l0.py`.
- Updated `scripts/labeling/Warden_auto_label_utils_brandlex.py` so `derive_auto_labels(...)` imports and calls `warden.module.l0` at runtime.
- Added `src/warden/__init__.py` and `src/warden/module/__init__.py` to support package imports.
- Added `src` path injection at the top of `Warden_auto_label_utils_brandlex.py` so existing script entrypoints can load the new package.

### Doc Changes

- Updated `docs/modules/MODULE_INFER.md` to state where the active L0 implementation now lives for the current auto-label-backed reference path.
- Updated `docs/modules/L0_DESIGN_V1.md` with the new active L0 implementation location.
- Added the repo task and handoff documents for this refactor.

### Output / Artifact Changes

- none

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\src\warden\__init__.py`
- `E:\Warden\src\warden\module\__init__.py`
- `E:\Warden\src\warden\module\l0.py`
- `E:\Warden\src\warden\module\l1.py`
- `E:\Warden\src\warden\module\l2.py`
- `E:\Warden\docs\modules\MODULE_INFER.md`
- `E:\Warden\docs\modules\L0_DESIGN_V1.md`
- `E:\Warden\docs\tasks\2026-04-21_l0_module_extraction.md`
- `E:\Warden\docs\handoff\2026-04-21_l0_module_extraction.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` still owns the compatibility entrypoints plus brand, rule-label, and sample-dir logic.
- `src/warden/module/l1.py` and `src/warden/module/l2.py` are explicit placeholders in this round and do not introduce new stage logic yet.

## 4. Behavior Impact

### Expected New Behavior

- The active L0 execution path used by `derive_auto_labels(...)` now delegates into `src/warden/module/l0.py`.
- Existing script entrypoints and caller import paths remain unchanged.
- The repository now has explicit `L0 / L1 / L2` code locations instead of relying only on a monolithic script for stage semantics.

### Preserved Behavior

- `derive_auto_labels(...)` is still exported from the same legacy script path.
- `derive_auto_labels_from_sample_dir(...)` is still exported from the same legacy script path.
- On the smoke sample, key output fields still existed and specialized signals such as `possible_adult_lure` still fired.

### User-facing / CLI Impact

- No new CLI was added.
- Existing backfill and capture-side entrypoints remain callable from their current paths.

### Output Format Impact

- No output structure was changed.
- No schema field was added or renamed in this task.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`
- `specialized_surface_signals`
- `l0_routing_hints`

Compatibility notes:

This was an internal code-organization refactor. Callers still import the same entrypoints from the same script path, and the smoke validation confirmed the expected schema keys are still present.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\src\warden\module\l0.py
python -m py_compile E:\Warden\src\warden\module\l1.py
python -m py_compile E:\Warden\src\warden\module\l2.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python -m py_compile E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python - <<'PY'
import sys
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as m
from warden.module import l0, l1, l2
print('derive_auto_labels' in dir(m))
print('derive_auto_labels_from_sample_dir' in dir(m))
print(l0.__name__)
print(l1.module_name())
print(l2.module_name())
PY
python - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as m
sample = Path(r'E:\Warden\data\raw\benign\hard benign\adult\101.ru_20260327T075659Z')
out = m.derive_auto_labels_from_sample_dir(sample, source='smoke')
keys = ['schema_version','page_stage_candidate','language_candidate','url_features','form_features','html_features','brand_signals','intent_signals','evasion_signals','specialized_surface_signals','l0_routing_hints','network_features','risk_outputs']
print(json.dumps({
  'has_all_keys': all(k in out for k in keys),
  'missing': [k for k in keys if k not in out],
  'page_stage_candidate': out.get('page_stage_candidate'),
  'possible_adult_lure': ((out.get('specialized_surface_signals') or {}).get('possible_adult_lure')),
  'module_path': 'warden.module.l0'
}, ensure_ascii=False, indent=2))
PY
```

### Result

- All `py_compile` checks succeeded.
- The existing auto-label entrypoints still imported successfully.
- `warden.module.l0`, `warden.module.l1`, and `warden.module.l2` imported successfully.
- On a real sample smoke run, all expected schema keys were still present.
- On that smoke run, `possible_adult_lure = true`, confirming that specialized outputs are still active on the new L0 path.

### Not Run

- large-scale dataset backfill regression
- broad before/after output diff across many samples
- L1/L2 behavior validation

Reason:

This task boundary was a code-organization refactor plus low-cost smoke validation, not a large-scale behavior regression.

## 7. Risks / Caveats

- `Warden_auto_label_utils_brandlex.py` still contains the older inline L0 helper and stage implementations. The active path now uses `src/warden/module/l0.py`, but the older inline implementations have not yet been removed. This is code debt rather than an intended behavior change.
- `src/warden/module/l1.py` and `src/warden/module/l2.py` are placeholders only in this round and do not yet contain real stage logic.
- Only smoke validation was run. There is still a low-probability risk of detail-level drift that would only show up in a broader before/after regression.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\modules\MODULE_INFER.md`
- `E:\Warden\docs\modules\L0_DESIGN_V1.md`
- `E:\Warden\docs\tasks\2026-04-21_l0_module_extraction.md`

Doc debt still remaining:

- If the legacy inline L0 code is removed from `Warden_auto_label_utils_brandlex.py` in a follow-up cleanup round, the docs should be updated again to make the compatibility-layer boundary explicit.

## 9. Recommended Next Step

- Run a second narrow refactor to delete the legacy inline L0 implementation still sitting in `Warden_auto_label_utils_brandlex.py`, leaving only the compatibility entrypoints plus brand and I/O logic.
- If the next goal is performance tightening, continue on top of `src/warden/module/l0.py` rather than adding new L0 logic back into the legacy script.
- If you want true staged runtime ownership next, start wiring real L1 and L2 implementations into `src/warden/module/l1.py` and `src/warden/module/l2.py`.
