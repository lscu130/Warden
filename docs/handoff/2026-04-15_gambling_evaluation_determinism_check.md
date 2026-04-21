# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-15-gambling-evaluation-determinism-check`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-EVALUATION-DETERMINISM-CHECK`
- Task Title: `检查并修复 gambling evaluation determinism`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

这次交付收口了 `gambling` 评估里的 determinism 问题。

结论有两点：

- 没看到同一样本在重复调用时发生共享状态漂移
- 当前更直接的根因是样本遍历顺序未冻结，`iter_sample_dirs()` 之前依赖 `rglob()` 的未排序返回顺序

本次修复很小，只把样本遍历改成稳定排序。修复后，固定数据和固定 seed 下的三次独立聚合运行给出了完全一致的样本切片 hash、赌博池顺序 hash 和命中数。

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- changed `iter_sample_dirs()` to sort `root.rglob("meta.json")` results by lowercase path before yielding sample directories
- added a short code comment explaining that traversal is kept deterministic for repeatable evaluation and auditing

### Doc Changes

- updated `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- added `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`
- none

### Output / Artifact Changes

- evaluation traversal order is now deterministic
- repeated validation output is now reproducible for the same code, same data, and same seed
- no schema or CLI artifact changed

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `iter_sample_dirs()` now yields sample directories in a stable path-sorted order
- evaluation snippets that build a pool from `iter_sample_dirs()` and then apply a fixed seed now produce stable slices and stable aggregate counts
- repeated gambling evaluation runs on the same local data no longer depend on filesystem traversal order

### Preserved Behavior

- labeling business logic for `possible_gambling_lure` was not changed
- `adult` and `gate` logic was not changed
- current CLI and sample-dir labeling entrypoints still behave the same from the caller perspective

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

- `iter_sample_dirs()`
- current sample-dir labeling flow
- downstream evaluation snippets that iterate sample pools

Compatibility notes:

This change only freezes traversal order for evaluation repeatability. It does not add, remove, or rename any schema field. It does not change the CLI, labeling output structure, or public field semantics.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- run the same aggregate quantification three times in separate Python processes over:
  - `E:\Warden\data\raw\benign\hard benign\gambling`
  - a reproducible `ordinary_benign = 800` slice sampled from `E:\Warden\data\raw\benign\benign`
- repeat the same single-sample labeling call five times on:
  - `E:\Warden\data\raw\benign\hard benign\gambling\67toto.xyz_20260407T032641Z`
```

### Result

- syntax validation passed
- three independent aggregate runs produced identical values:
  - `gambling_total = 843`
  - `gambling_hits = 565`
  - `gambling_order_hash = e61b106af078ac04e0b6ff75e95eefe026064ff643b0c8af415590ce19ee9d55`
  - `benign_total = 14797`
  - `benign_slice_hits = 12`
  - `benign_slice_hash = d25cc58546eed34baf3840604041cde26bd63980cdc3692e02e0ace1703097bb`
- the same-sample repeated labeling call stayed stable across five iterations:
  - `possible_gambling_lure = true`
  - `gambling_weighted_score = 2`
  - `brand_candidates = []`
- current evidence supports an order-sensitivity root cause and does not support a shared mutable-state drift hypothesis for the tested sample

### Not Run

- a repo-wide mixed-batch re-evaluation across gambling, adult, gate, and benign
- a broader audit of every ad hoc evaluation snippet outside `iter_sample_dirs()`
- any gambling recall tuning

Reason:

This task was scoped to determinism repair only. The minimal fix was sufficient to stabilize the targeted evaluation path, so broader reruns and unrelated recall work were intentionally left out.

---

## 7. Risks / Caveats

- ad hoc one-off analysis snippets outside `iter_sample_dirs()` can still reintroduce drift if they build sample pools without sorting
- this task stabilizes traversal order for the current labeling helper path; it does not audit every historical notebook or shell snippet used in prior threads
- the repeated single-sample check ruled out one shared-state failure mode for the tested sample, but it does not prove that every possible helper path is mutation-free

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- standardize future evaluation snippets on `iter_sample_dirs()` plus explicit fixed-seed sampling
- if broader confidence is needed, run one refreshed mixed-batch regression using the stabilized traversal helper
- if drift is seen again outside this path, audit the specific snippet first before changing labeling logic

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-15-gambling-evaluation-determinism-check`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-EVALUATION-DETERMINISM-CHECK`
- Task Title: `Check and fix gambling evaluation determinism`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

This delivery closed the determinism issue in the `gambling` evaluation path.

The result has two parts:

- there is no evidence of shared-state drift when the same sample is labeled repeatedly
- the more direct root cause is unfrozen sample traversal order, because `iter_sample_dirs()` previously relied on the unsorted return order of `rglob()`

The fix is intentionally small: sample traversal is now explicitly sorted. After the fix, three independent aggregate runs with the same data and same seed produced identical slice hashes, identical gambling-pool order hashes, and identical hit counts.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- changed `iter_sample_dirs()` to sort `root.rglob("meta.json")` results by lowercase path before yielding sample directories
- added a short code comment explaining that traversal is kept deterministic for repeatable evaluation and auditing

### Doc Changes

- updated `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- added `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`
- none

### Output / Artifact Changes

- evaluation traversal order is now deterministic
- repeated validation output is now reproducible for the same code, same data, and same seed
- no schema or CLI artifact changed

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `iter_sample_dirs()` now yields sample directories in a stable path-sorted order
- evaluation snippets that build a pool from `iter_sample_dirs()` and then apply a fixed seed now produce stable slices and stable aggregate counts
- repeated gambling evaluation runs on the same local data no longer depend on filesystem traversal order

### Preserved Behavior

- labeling business logic for `possible_gambling_lure` was not changed
- `adult` and `gate` logic was not changed
- current CLI and sample-dir labeling entrypoints still behave the same from the caller perspective

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

- `iter_sample_dirs()`
- current sample-dir labeling flow
- downstream evaluation snippets that iterate sample pools

Compatibility notes:

This change only freezes traversal order for evaluation repeatability. It does not add, remove, or rename any schema field. It does not change the CLI, labeling output structure, or public field semantics.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- run the same aggregate quantification three times in separate Python processes over:
  - `E:\Warden\data\raw\benign\hard benign\gambling`
  - a reproducible `ordinary_benign = 800` slice sampled from `E:\Warden\data\raw\benign\benign`
- repeat the same single-sample labeling call five times on:
  - `E:\Warden\data\raw\benign\hard benign\gambling\67toto.xyz_20260407T032641Z`
```

### Result

- syntax validation passed
- three independent aggregate runs produced identical values:
  - `gambling_total = 843`
  - `gambling_hits = 565`
  - `gambling_order_hash = e61b106af078ac04e0b6ff75e95eefe026064ff643b0c8af415590ce19ee9d55`
  - `benign_total = 14797`
  - `benign_slice_hits = 12`
  - `benign_slice_hash = d25cc58546eed34baf3840604041cde26bd63980cdc3692e02e0ace1703097bb`
- the same-sample repeated labeling call stayed stable across five iterations:
  - `possible_gambling_lure = true`
  - `gambling_weighted_score = 2`
  - `brand_candidates = []`
- current evidence supports an order-sensitivity root cause and does not support a shared mutable-state drift hypothesis for the tested sample

### Not Run

- a repo-wide mixed-batch re-evaluation across gambling, adult, gate, and benign
- a broader audit of every ad hoc evaluation snippet outside `iter_sample_dirs()`
- any gambling recall tuning

Reason:

This task was scoped to determinism repair only. The minimal fix was sufficient to stabilize the targeted evaluation path, so broader reruns and unrelated recall work were intentionally left out.

---

## 7. Risks / Caveats

- ad hoc one-off analysis snippets outside `iter_sample_dirs()` can still reintroduce drift if they build sample pools without sorting
- this task stabilizes traversal order for the current labeling helper path; it does not audit every historical notebook or shell snippet used in prior threads
- the repeated single-sample check ruled out one shared-state failure mode for the tested sample, but it does not prove that every possible helper path is mutation-free

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_evaluation_determinism_check.md`
- `docs/handoff/2026-04-15_gambling_evaluation_determinism_check.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- standardize future evaluation snippets on `iter_sample_dirs()` plus explicit fixed-seed sampling
- if broader confidence is needed, run one refreshed mixed-batch regression using the stabilized traversal helper
- if drift is seen again outside this path, audit the specific snippet first before changing labeling logic
