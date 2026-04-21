# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
- Handoff ID: `2026-04-21-l0-latency-small-test-50`
- Related Task ID: `TASK-L0-2026-04-21-LATENCY-SMALL-TEST-50`
- Task Title: `运行 50 样本 L0 小范围时延测试并统计平均处理时间`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

这次交付对当前 working tree 的 L0 样本判断路径做了一次 `50` 样本小范围时延测试，样本构成为：

- `30` benign
- `10` adult
- `10` gambling

计时口径分两层：

- `auto_ms`: `derive_auto_labels_from_sample_dir(...)`
- `full_ms`: `derive_auto_labels_from_sample_dir(...) + derive_rule_labels(...)`

当前结果显示，两者几乎相同，说明当前 `derive_rule_labels(...)` 的时间占比很小。50 样本整体均值为：

- `auto_ms` 平均：`117.876 ms / sample`
- `full_ms` 平均：`117.912 ms / sample`

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- added `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- added `docs/handoff/2026-04-21_l0_latency_small_test_50.md`
- updated the task status to `DONE`

### Output / Artifact Changes

- none

This task only ran measurement and documentation. It did not modify L0 logic.

---

## 3. Files Touched

- `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

Optional notes per file:

- the task doc freezes the sample mix and timing scope
- the handoff records the measured timing distribution and caveats

---

## 4. Behavior Impact

### Expected New Behavior

- no code behavior changed
- the only new outcome is a measured timing snapshot for the current local L0 path

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` was not modified
- schema was not modified
- CLI and sample-dir entry behavior were not modified

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

- none

Compatibility notes:

This delivery only measured the current local L0 path. It did not modify fields, function signatures, CLI behavior, or output contracts.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- import `iter_sample_dirs`, `derive_auto_labels_from_sample_dir`, and `derive_rule_labels`
- fix random seed to `20260421`
- sample `30` benign from `E:\Warden\data\raw\benign\benign`
- sample `10` adult from `E:\Warden\data\raw\benign\hard benign\adult`
- sample `10` gambling from `E:\Warden\data\raw\benign\hard benign\gambling`
- warm one sample once outside the measured loop
- measure per-sample `auto_ms` and `full_ms`
- aggregate mean / median / p90 / p95 / min / max
```

### Result

Pool sizes at measurement time:

- benign: `17632`
- adult: `813`
- gambling: `945`

Selected counts:

- benign: `30`
- adult: `10`
- gambling: `10`
- total: `50`

All-sample timing summary:

- `auto_ms`
  - mean: `117.876`
  - median: `101.746`
  - p90: `244.455`
  - p95: `290.788`
  - min: `7.004`
  - max: `493.090`

- `full_ms`
  - mean: `117.912`
  - median: `101.802`
  - p90: `244.500`
  - p95: `290.826`
  - min: `7.031`
  - max: `493.130`

Per-group `full_ms` means:

- benign: `127.873 ms`
- adult: `102.349 ms`
- gambling: `103.592 ms`

Slowest overall samples:

- `worldofprintables.com_20260402T023119Z`: `493.130 ms`
- `flashscore.gr_20260401T094819Z`: `408.089 ms`
- `bp.org.br_20260403T094918Z`: `305.532 ms`
- `stape.st_20260414T074354Z`: `272.852 ms`
- `ttbsuper19.com_20260326T121403Z`: `244.883 ms`

Interpretation:

- current local L0 cost is about `118 ms / sample` on this 50-sample slice
- `derive_rule_labels(...)` adds almost no visible overhead beyond `derive_auto_labels_from_sample_dir(...)`
- benign pages in this slice were slower on average than adult and gambling pages

### Not Run

- no repeated multi-round benchmark for stability variance
- no hardware-isolated benchmark harness
- no code patch

Reason:

This task only asked for one bounded 50-sample local timing run.

---

## 7. Risks / Caveats

- this is a local working-tree timing snapshot, not a hardware-independent benchmark claim
- pool sizes changed over time, so later comparisons should reuse the same sampling and timing method
- only one warmup sample was excluded; broader repeated runs may shift the exact mean slightly

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- if you want a more stable latency number, run a repeated 3-5 round benchmark on the same 50-sample slice and report variance
- if you want deployment-relevant latency, rerun the same benchmark under the target runtime/hardware profile
- if you want to understand why some benign pages are much slower, open a small profiling task against the top slow outliers

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-21-l0-latency-small-test-50`
- Related Task ID: `TASK-L0-2026-04-21-LATENCY-SMALL-TEST-50`
- Task Title: `Run a 50-sample L0 latency spot test and report the average processing time`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

This delivery ran a bounded 50-sample latency spot test for the current working-tree L0 sample-judgment path with the requested mix:

- `30` benign
- `10` adult
- `10` gambling

The timing scope was measured in two layers:

- `auto_ms`: `derive_auto_labels_from_sample_dir(...)`
- `full_ms`: `derive_auto_labels_from_sample_dir(...) + derive_rule_labels(...)`

The two numbers are effectively the same in this run, which means the current `derive_rule_labels(...)` step adds negligible overhead. The overall 50-sample averages are:

- average `auto_ms`: `117.876 ms / sample`
- average `full_ms`: `117.912 ms / sample`

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- added `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- added `docs/handoff/2026-04-21_l0_latency_small_test_50.md`
- updated the task status to `DONE`

### Output / Artifact Changes

- none

This task only ran measurement and documentation. It did not modify L0 logic.

---

## 3. Files Touched

- `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

Optional notes per file:

- the task doc freezes the sample mix and timing scope
- the handoff records the measured timing distribution and caveats

---

## 4. Behavior Impact

### Expected New Behavior

- no code behavior changed
- the only new outcome is a measured timing snapshot for the current local L0 path

### Preserved Behavior

- `scripts/labeling/Warden_auto_label_utils_brandlex.py` was not modified
- schema was not modified
- CLI and sample-dir entry behavior were not modified

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

- none

Compatibility notes:

This delivery only measured the current local L0 path. It did not modify fields, function signatures, CLI behavior, or output contracts.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- import `iter_sample_dirs`, `derive_auto_labels_from_sample_dir`, and `derive_rule_labels`
- fix the random seed to `20260421`
- sample `30` benign from `E:\Warden\data\raw\benign\benign`
- sample `10` adult from `E:\Warden\data\raw\benign\hard benign\adult`
- sample `10` gambling from `E:\Warden\data\raw\benign\hard benign\gambling`
- warm one sample once outside the measured loop
- measure per-sample `auto_ms` and `full_ms`
- aggregate mean / median / p90 / p95 / min / max
```

### Result

Pool sizes at measurement time:

- benign: `17632`
- adult: `813`
- gambling: `945`

Selected counts:

- benign: `30`
- adult: `10`
- gambling: `10`
- total: `50`

All-sample timing summary:

- `auto_ms`
  - mean: `117.876`
  - median: `101.746`
  - p90: `244.455`
  - p95: `290.788`
  - min: `7.004`
  - max: `493.090`

- `full_ms`
  - mean: `117.912`
  - median: `101.802`
  - p90: `244.500`
  - p95: `290.826`
  - min: `7.031`
  - max: `493.130`

Per-group `full_ms` means:

- benign: `127.873 ms`
- adult: `102.349 ms`
- gambling: `103.592 ms`

Slowest overall samples:

- `worldofprintables.com_20260402T023119Z`: `493.130 ms`
- `flashscore.gr_20260401T094819Z`: `408.089 ms`
- `bp.org.br_20260403T094918Z`: `305.532 ms`
- `stape.st_20260414T074354Z`: `272.852 ms`
- `ttbsuper19.com_20260326T121403Z`: `244.883 ms`

Interpretation:

- the current local L0 cost is about `118 ms / sample` on this 50-sample slice
- `derive_rule_labels(...)` adds almost no visible overhead beyond `derive_auto_labels_from_sample_dir(...)`
- benign pages in this slice were slower on average than adult and gambling pages

### Not Run

- no repeated multi-round benchmark for stability variance
- no hardware-isolated benchmark harness
- no code patch

Reason:

This task only asked for one bounded 50-sample local timing run.

---

## 7. Risks / Caveats

- this is a local working-tree timing snapshot, not a hardware-independent benchmark claim
- pool sizes changed over time, so later comparisons should reuse the same sampling and timing method
- only one warmup sample was excluded; broader repeated runs may shift the exact mean slightly

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- if you want a more stable latency number, run a repeated 3-5 round benchmark on the same 50-sample slice and report variance
- if you want deployment-relevant latency, rerun the same benchmark under the target runtime/hardware profile
- if you want to understand why some benign pages are much slower, open a small profiling task against the top slow outliers
