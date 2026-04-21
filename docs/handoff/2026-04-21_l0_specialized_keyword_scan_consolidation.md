# L0 specialized keyword scan consolidation handoff

## 中文版

> 面向人工阅读的摘要版。英文版为权威版本；若验证命令、兼容性结论、数值结果或状态表述有冲突，以英文版为准。

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Related Task ID: `TASK-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Task Title: `Consolidate repeated specialized keyword scanning inside src/warden/module/l0.py`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

## 1. Executive Summary

本次交付只修改了 `src/warden/module/l0.py`。目标是把 `derive_specialized_surface_signals(...)` 中对同一 `text_low` 和 `url_blob` 的多轮重复 `hit_keywords(...)` 扫描收敛为共享扫描结果，再按 detector bucket 回填已有输出结构。

实现完成后，固定 `seed=20260421` 的 `50` 样本切片上，specialized 输出零差异；函数级均值延迟从 `11.787 ms / sample` 降到 `11.479 ms / sample`，相对下降约 `2.61%`。整链路 smoke 通过。

## 2. What Changed

### Code Changes

- 在 `src/warden/module/l0.py` 中新增 module-level specialized scan specs、union lexicon 和 set 预计算。
- 新增 `collect_keyword_hits_by_bucket(...)`，将一次 union 扫描结果回填为 `gambling / adult / gate` 的原有 bucket 命中列表。
- 将 `derive_specialized_surface_signals(...)` 从多轮重复 `hit_keywords(...)` 调用改为两轮共享扫描：一轮 `text_low`，一轮 `url_blob`。
- 将若干重复 list membership 判断改为 set membership，以减少 detector 内部热路径开销。

### Doc Changes

- 更新 `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md` 状态为 `DONE` 并勾选验收项。
- 新增本 handoff 文档。

### Output / Artifact Changes

- 生成了一组固定 `50` 样本切片上的 before/after specialized function benchmark 结果。
- 生成了一次整链路 smoke 结果，用于确认 sample-dir -> auto-label 路径未报错。
- 未新增持久化数据文件或 schema artifact。

## 3. Files Touched

- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

Optional notes per file:

- `src/warden/module/l0.py`: 只做 specialized keyword scan consolidation，没有触碰字段名、阈值或 routing 逻辑。
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`: 回填执行状态与验收勾选。
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`: 记录实际改动、验证与风险。

## 4. Behavior Impact

### Expected New Behavior

- `derive_specialized_surface_signals(...)` 现在会复用共享扫描结果，而不是对同一文本和 URL blob 重复做多轮独立 `hit_keywords(...)`。
- 在固定 `50` 样本切片上，target function 的均值延迟小幅下降。

### Preserved Behavior

- `possible_gambling_lure`、`possible_bonus_or_betting_induction`、`possible_adult_lure`、`possible_age_gate_surface`、`possible_gate_or_evasion` 在固定切片上与旧实现完全一致。
- `matched_keywords` 的 bucket 结构与内容在固定切片上与旧实现完全一致。
- L0 对外公开接口、字段名和默认 L0 边界未变化。

### User-facing / CLI Impact

- 无新增 CLI，无现有 CLI 变更。

### Output Format Impact

- 输出格式无变化。

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `derive_specialized_surface_signals(...)`
- `specialized_surface_signals.matched_keywords`
- `specialized_surface_signals.possible_gambling_lure`

Compatibility notes:

本次交付只改变 `l0.py` 内部 specialized scan 的执行方式，没有改动任何字段名、bucket 名或上层入口。  
固定切片回归中，specialized 输出完全一致。当前已知兼容性风险主要是性能收益有限，不是接口破坏。

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python - <<'PY'
# deterministic specialized function before/after benchmark
# seed=20260421
# 20 benign + 10 adult + 10 gambling + 10 gate
# 30 rounds per sample
PY
python - <<'PY'
# one sample-dir derive_auto_labels_from_sample_dir(...) smoke run
PY
```

### Result

- `py_compile` passed.
- Fixed-slice specialized function benchmark:
  - before mean: `11.787 ms / sample`
  - after mean: `11.479 ms / sample`
  - absolute reduction: `0.308 ms`
  - relative reduction: about `2.61%`
- Per-group means before / after:
  - benign: `14.349 -> 13.915 ms`
  - adult: `13.094 -> 12.857 ms`
  - gambling: `16.208 -> 15.778 ms`
  - gate: `0.934 -> 0.929 ms`
- Fixed-slice behavior regression:
  - output mismatches: `0 / 50`
  - benign:
    - `possible_gambling_lure`: `0 / 20 -> 0 / 20`
    - `possible_adult_lure`: `0 / 20 -> 0 / 20`
    - `possible_gate_or_evasion`: `0 / 20 -> 0 / 20`
  - adult:
    - `possible_adult_lure`: `7 / 10 -> 7 / 10`
    - `possible_age_gate_surface`: `2 / 10 -> 2 / 10`
  - gambling:
    - `possible_gambling_lure`: `5 / 10 -> 5 / 10`
    - `possible_bonus_or_betting_induction`: `8 / 10 -> 8 / 10`
  - gate:
    - `possible_gate_or_evasion`: `3 / 10 -> 3 / 10`
- Smoke sample passed:
  - sample: `007cctv.com_20260325T163721Z`
  - `page_stage_candidate = "transition"`
  - `routing_reason_codes = ["default_non_specialized_l1_path"]`

### Not Run

- full dataset rerun
- full end-to-end latency harness
- downstream consumer audit beyond bounded slice and smoke

Reason:

This task was intentionally scoped as a narrow `l0.py` internal consolidation plus bounded regression, not a full rerun or broader integration task.

## 7. Risks / Caveats

- 当前收益存在，但幅度不大；说明 `derive_specialized_surface_signals(...)` 的重复扫描并不是现阶段 L0 的主导成本项。
- `contains_any(...)`、regex 匹配本身和其他 L0 阶段逻辑仍然存在固定开销；如果还要继续压延迟，需要单开下一条更窄任务处理 matching engine 或更激进的预处理。
- 这次回归只覆盖固定 `50` 样本切片；没有证明全量数据上一定得到同等幅度收益。

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

Doc debt still remaining:

- `none`

## 9. Recommended Next Step

- 如果继续做 L0 提速，下一条任务应单独量化 `contains_any(...)` 与其他非-specialized 阶段的占比，不要把它们混进本任务。
- 如果用户要继续追更明显收益，优先考虑 keyword matching engine 的更低成本实现路径，并继续保持字段和 bucket 解释性不变。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `HANDOFF-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Related Task ID: `TASK-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Task Title: `Consolidate repeated specialized keyword scanning inside src/warden/module/l0.py`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

## 1. Executive Summary

This delivery only changed `src/warden/module/l0.py`. The goal was to collapse repeated `hit_keywords(...)` scans over the same `text_low` and `url_blob` inside `derive_specialized_surface_signals(...)` into shared scan results while preserving the existing detector buckets and output structure.

After the change, the fixed `50`-sample slice with `seed=20260421` showed zero specialized-output mismatches; the function-level mean latency dropped from `11.787 ms / sample` to `11.479 ms / sample`, a relative reduction of about `2.61%`. A full sample-dir smoke run also passed.

## 2. What Changed

### Code Changes

- Added module-level specialized scan specs, union lexicons, and set precomputations in `src/warden/module/l0.py`.
- Added `collect_keyword_hits_by_bucket(...)` to reuse one union scan result and project it back into the existing `gambling / adult / gate` matched-keyword buckets.
- Reworked `derive_specialized_surface_signals(...)` so it now performs two shared scans, one over `text_low` and one over `url_blob`, instead of multiple repeated `hit_keywords(...)` passes.
- Replaced several repeated list-membership checks with set-membership checks in the same hot path.

### Doc Changes

- Updated `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md` to `DONE` and checked off the acceptance items.
- Added this handoff document.

### Output / Artifact Changes

- Produced a bounded before/after benchmark for the specialized function on a fixed `50`-sample slice.
- Produced a sample-dir smoke result to confirm the `sample_dir -> auto_labels` path still runs.
- No persistent data artifact or schema artifact was added.

## 3. Files Touched

- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

Optional notes per file:

- `src/warden/module/l0.py`: only specialized keyword-scan consolidation; no field, threshold, or routing redesign.
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`: execution status and acceptance checklist updated.
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`: actual implementation, validation, and risks recorded.

## 4. Behavior Impact

### Expected New Behavior

- `derive_specialized_surface_signals(...)` now reuses shared scan results instead of repeatedly scanning the same text and URL blob for each detector bucket.
- On the fixed `50`-sample slice, the target function now runs slightly faster on average.

### Preserved Behavior

- `possible_gambling_lure`, `possible_bonus_or_betting_induction`, `possible_adult_lure`, `possible_age_gate_surface`, and `possible_gate_or_evasion` matched the old implementation exactly on the fixed slice.
- The structure and contents of `matched_keywords` matched the old implementation exactly on the fixed slice.
- Public L0 interfaces, field names, and the narrowed L0 responsibility boundary did not change.

### User-facing / CLI Impact

- No new CLI was added, and no existing CLI changed.

### Output Format Impact

- No output format changed.

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `derive_specialized_surface_signals(...)`
- `specialized_surface_signals.matched_keywords`
- `specialized_surface_signals.possible_gambling_lure`

Compatibility notes:

This delivery only changes how specialized scans are executed internally inside `l0.py`; it does not change any field names, bucket names, or top-level entrypoints.  
The fixed-slice regression showed exact specialized-output parity.  
The current known risk is limited performance gain, not interface breakage.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python - <<'PY'
# deterministic specialized function before/after benchmark
# seed=20260421
# 20 benign + 10 adult + 10 gambling + 10 gate
# 30 rounds per sample
PY
python - <<'PY'
# one sample-dir derive_auto_labels_from_sample_dir(...) smoke run
PY
```

### Result

- `py_compile` passed.
- Fixed-slice specialized-function benchmark:
  - before mean: `11.787 ms / sample`
  - after mean: `11.479 ms / sample`
  - absolute reduction: `0.308 ms`
  - relative reduction: about `2.61%`
- Per-group means before / after:
  - benign: `14.349 -> 13.915 ms`
  - adult: `13.094 -> 12.857 ms`
  - gambling: `16.208 -> 15.778 ms`
  - gate: `0.934 -> 0.929 ms`
- Fixed-slice behavior regression:
  - output mismatches: `0 / 50`
  - benign:
    - `possible_gambling_lure`: `0 / 20 -> 0 / 20`
    - `possible_adult_lure`: `0 / 20 -> 0 / 20`
    - `possible_gate_or_evasion`: `0 / 20 -> 0 / 20`
  - adult:
    - `possible_adult_lure`: `7 / 10 -> 7 / 10`
    - `possible_age_gate_surface`: `2 / 10 -> 2 / 10`
  - gambling:
    - `possible_gambling_lure`: `5 / 10 -> 5 / 10`
    - `possible_bonus_or_betting_induction`: `8 / 10 -> 8 / 10`
  - gate:
    - `possible_gate_or_evasion`: `3 / 10 -> 3 / 10`
- Smoke sample passed:
  - sample: `007cctv.com_20260325T163721Z`
  - `page_stage_candidate = "transition"`
  - `routing_reason_codes = ["default_non_specialized_l1_path"]`

### Not Run

- full dataset rerun
- full end-to-end latency harness
- downstream consumer audit beyond the bounded slice and smoke

Reason:

This task was intentionally scoped as a narrow `l0.py` internal consolidation plus bounded regression, not a full rerun or broader integration task.

## 7. Risks / Caveats

- There is a real gain, but it is small; that suggests repeated scanning inside `derive_specialized_surface_signals(...)` is not the dominant L0 cost at this point.
- `contains_any(...)`, regex matching itself, and the other L0 stages still contribute fixed cost; if latency should be reduced further, that needs a separate narrow task focused on the matching engine or more aggressive preprocessing.
- This regression only covers the fixed `50`-sample slice; it does not prove the same gain magnitude across the full dataset.

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

Doc debt still remaining:

- `none`

## 9. Recommended Next Step

- If L0 acceleration should continue, the next task should isolate and quantify the cost share of `contains_any(...)` and other non-specialized stages instead of folding them into this task.
- If the user wants a more meaningful latency drop, prioritize a lower-cost keyword-matching implementation path while keeping the current fields and bucket explainability intact.
