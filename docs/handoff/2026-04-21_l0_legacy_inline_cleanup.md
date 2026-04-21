# L0 legacy inline cleanup handoff

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Related Task ID: `TASK-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Task Title: `Delete the legacy inline L0 implementation from the old auto-label script while keeping compatibility entrypoints`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

## 1. Executive Summary

本次交付把 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中已经失活的 legacy L0 内联实现删除，只保留兼容入口、brand 相关 helper 和样本目录 I/O 编排。  
活跃 L0 逻辑继续集中在 `src/warden/module/l0.py`。  
清理后补做了编译、导入和真实样本 smoke；发现并修复了两个兼容问题：历史坏编码字符串导致的语法错误，以及 brand helper 被误删导致的运行时 `NameError`。

## 2. What Changed

### Code Changes

- 删除旧脚本中的 legacy L0 内联 helper 和风险/路由/阶段判断实现。
- 在 `src/warden/module/l0.py` 内补齐 L0 仍需自有的 prep helper：`summarize_forms(...)`、`summarize_url(...)`、`summarize_network(...)`、`summarize_html_features(...)`。
- 在旧脚本中保留并补回 brand 兼容 helper：`extract_claimed_brands(...)`、`extract_claimed_brands_from_url(...)`、`classify_domain_brand_consistency(...)`。
- 清理旧脚本中一批历史损坏的 keyword/alias 字面量，消除语法错误。

### Doc Changes

- 更新任务文档状态并勾选验收项：`docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- 新增本次 handoff：`docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`
- none

### Output / Artifact Changes

- none
- none
- none

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: 旧脚本现在主要承担兼容入口、brand helper、规则标签和 sample-dir 编排。
- `src/warden/module/l0.py`: 现在独立持有 active L0 的 prep 和输出逻辑。
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`: 任务状态从 `TODO` 更新为 `DONE`。

## 4. Behavior Impact

### Expected New Behavior

- 旧脚本不再保留第二份 legacy L0 实现，避免双份逻辑漂移。
- `derive_auto_labels(...)` 继续从旧路径可调，但 active L0 计算只走 `src/warden/module/l0.py`。
- 旧脚本中的 brand claim 和域名一致性判断继续可用。

### Preserved Behavior

- `derive_auto_labels(...)`、`derive_auto_labels_from_sample_dir(...)`、`derive_rule_labels(...)` 入口名未变。
- 顶层输出 schema key 未变。
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py` 和 capture 侧脚本仍可编译。

### User-facing / CLI Impact

- 无新增 CLI；现有调用路径保持不变。

### Output Format Impact

- 无输出格式变更。

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `brand_signals.domain_brand_consistency_candidate`

Compatibility notes:

本次仅调整实现归属，不改字段名、不改入口名、不改下游脚本调用方式。  
review 期间确认旧脚本已删除的 L0 helper 在当前 `scripts/` 与 `src/` 范围内没有外部调用残留，剩余命中只在 `src/warden/module/l0.py` 和 capture 侧自有 diff helper。

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\src\warden\module\l0.py E:\Warden\src\warden\module\l1.py E:\Warden\src\warden\module\l2.py E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, r'E:\Warden\src')
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as auto
from warden.module import l0
sample = Path(r'E:\Warden\data\raw\benign\hard benign\adult\101.ru_20260327T075659Z')
result = auto.derive_auto_labels_from_sample_dir(sample)
print(result.get("page_stage_candidate"), (result.get("risk_outputs") or {}).get("risk_level_weak"))
PY
rg -n --glob '!docs/**' "extract_claimed_brands\(|classify_domain_brand_consistency\(|summarize_forms|summarize_url|summarize_network|summarize_html_features|derive_specialized_surface_signals|derive_text_observability_signals|derive_l0_routing_hints|derive_intent_signals|derive_page_stage|derive_evasion_signals|derive_safe_int|compute_weak_risk|risk_level_from_score" E:\Warden\scripts E:\Warden\src
```

### Result

- `py_compile` 通过，触达旧脚本、新 L0 模块、L1/L2 占位模块、backfill 调用方、capture 调用方。
- 导入和真实样本 smoke 通过；样本输出未丢失预期顶层 key。
- review 过程中发现并修复一个运行时冲突：`extract_claimed_brands(...)` 与 `classify_domain_brand_consistency(...)` 被误删，已补回。

### Not Run

- full dataset rerun
- benchmark rerun
- capture end-to-end execution

Reason:

这次任务边界是窄 cleanup，目标是删除 dead inline L0 并验证兼容入口未坏；全量回归和性能复测不属于本 task 的最小验证面。

## 7. Risks / Caveats

- 旧脚本的 keyword 常量里仍有部分历史乱码 token，只是当前已修到可编译、可运行的安全状态，没有做词表质量重建。
- `classify_domain_brand_consistency(...)` 是按现有冻结输出值补回的最小兼容实现，不是新的 brand 研究任务。
- 仓库当前工作树本身很脏，存在大量与本任务无关的删除/新增/修改；本次未处理那些内容。

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

Doc debt still remaining:

- 如果后续要系统清理历史乱码 lexicon，需要单开 task 和记 handoff。
- `none`

## 9. Recommended Next Step

- 单开一条 brand helper stabilization 小任务，专门核对旧脚本里剩余 brand/keyword 常量的编码质量。
- 如果你要继续推进 L0 提速，再开下一条 task 做 keyword scan consolidation，不要把它混进这条 cleanup。
- 在下一轮相关任务前，先基于当前工作树做一次更干净的变更隔离。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Related Task ID: `TASK-L0-2026-04-21-LEGACY-INLINE-CLEANUP`
- Task Title: `Delete the legacy inline L0 implementation from the old auto-label script while keeping compatibility entrypoints`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

This delivery removed the now-dead legacy inline L0 implementation from `scripts/labeling/Warden_auto_label_utils_brandlex.py` and left that script as a compatibility layer containing entrypoints, brand helpers, rule-label logic, and sample-dir I/O orchestration.  
The active L0 implementation remains centralized in `src/warden/module/l0.py`.  
After the cleanup, compile/import/sample validation exposed two real compatibility issues: malformed historical string literals that broke parsing, and accidental removal of brand helpers that caused a runtime `NameError`. Both were fixed in this task.

## 2. What Changed

### Code Changes

- Deleted the legacy inline L0 helper block plus its stage/risk/routing logic from the old script.
- Completed L0-owned helper relocation into `src/warden/module/l0.py` by making that module own `summarize_forms(...)`, `summarize_url(...)`, `summarize_network(...)`, and `summarize_html_features(...)`.
- Restored the required brand compatibility helpers inside the old script: `extract_claimed_brands(...)`, `extract_claimed_brands_from_url(...)`, and `classify_domain_brand_consistency(...)`.
- Cleaned a narrow set of malformed historical keyword and alias literals so the old script compiles again.

### Doc Changes

- Updated task status and acceptance checks in `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`.
- Added this handoff file at `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`.
- none

### Output / Artifact Changes

- none
- none
- none

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: now acts primarily as a compatibility-layer script.
- `src/warden/module/l0.py`: now owns the active L0 prep/output helpers directly.
- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`: status moved from `TODO` to `DONE`.

## 4. Behavior Impact

### Expected New Behavior

- The old script no longer carries a second legacy inline L0 implementation.
- `derive_auto_labels(...)` remains callable from the legacy script path, but active L0 computation now lives only in `src/warden/module/l0.py`.
- Brand-claim extraction and domain-consistency classification continue to work from the old script.

### Preserved Behavior

- `derive_auto_labels(...)`, `derive_auto_labels_from_sample_dir(...)`, and `derive_rule_labels(...)` remain callable under the same names.
- The top-level output schema remains unchanged.
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py` and the capture-side script still compile.

### User-facing / CLI Impact

- No new CLI was introduced; existing call paths remain valid.

### Output Format Impact

- No output-format change.

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `brand_signals.domain_brand_consistency_candidate`

Compatibility notes:

This task changed implementation ownership only. It did not rename frozen fields, change entrypoint names, or alter downstream caller usage.  
The conflict review confirmed that the deleted L0 helper names no longer have external caller references inside the current `scripts/` and `src/` trees; remaining matches are the new L0 module itself and capture-side diff-specific helpers.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\src\warden\module\l0.py E:\Warden\src\warden\module\l1.py E:\Warden\src\warden\module\l2.py E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
python - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, r'E:\Warden\src')
sys.path.insert(0, r'E:\Warden\scripts\labeling')
import Warden_auto_label_utils_brandlex as auto
from warden.module import l0
sample = Path(r'E:\Warden\data\raw\benign\hard benign\adult\101.ru_20260327T075659Z')
result = auto.derive_auto_labels_from_sample_dir(sample)
print(result.get("page_stage_candidate"), (result.get("risk_outputs") or {}).get("risk_level_weak"))
PY
rg -n --glob '!docs/**' "extract_claimed_brands\(|classify_domain_brand_consistency\(|summarize_forms|summarize_url|summarize_network|summarize_html_features|derive_specialized_surface_signals|derive_text_observability_signals|derive_l0_routing_hints|derive_intent_signals|derive_page_stage|derive_evasion_signals|derive_safe_int|compute_weak_risk|risk_level_from_score" E:\Warden\scripts E:\Warden\src
```

### Result

- `py_compile` passed for the old script, the new L0/L1/L2 module files, the backfill caller, and the capture caller.
- Import and real-sample smoke passed; the smoke output retained all expected top-level keys.
- The review found and fixed one real runtime conflict: `extract_claimed_brands(...)` and `classify_domain_brand_consistency(...)` had been removed accidentally and were restored.

### Not Run

- full dataset rerun
- benchmark rerun
- capture end-to-end execution

Reason:

This task was intentionally scoped as a narrow cleanup. The required validation boundary was compile/import/sample compatibility, not a full regression or performance rerun.

## 7. Risks / Caveats

- The old script still contains some historically corrupted keyword tokens; this task only cleaned enough malformed literals to restore safe parsing/runtime behavior.
- `classify_domain_brand_consistency(...)` was restored as a minimal compatibility implementation using the existing frozen output values, not as a redesigned brand-analysis module.
- The repository worktree is already very dirty with many unrelated changes; this task did not attempt to normalize that state.

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_legacy_inline_cleanup.md`
- `docs/handoff/2026-04-21_l0_legacy_inline_cleanup.md`

Doc debt still remaining:

- If the remaining historical corrupted lexicon content should be normalized systematically, that should be handled in a separate task and handoff.
- none

## 9. Recommended Next Step

- Open a small brand-helper stabilization task to review remaining keyword and alias encoding quality in the old script.
- If you want to continue L0 latency work, open the next task for keyword-scan consolidation and keep it separate from this cleanup.
- Before the next related change, isolate work more cleanly from the already-dirty repository state.
