# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-17-adult-post-cleanup-metrics-rerun`
- Related Task ID: `TASK-L0-2026-04-17-ADULT-POST-CLEANUP-METRICS-RERUN`
- Task Title: `重跑 adult 在清理后 benign 池上的误触统计`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-17`
- Status: `DONE`

---

## 1. Executive Summary

这次交付没有改代码，也没有改数据池位置。它基于当前工作树下的 `adult` 规则，对清理后的 `E:\Warden\data\raw\benign\benign` 和当前 `E:\Warden\data\raw\benign\hard benign\adult` 重跑了一轮池级统计。

当前结果：

- ordinary benign: `85 / 17748 = 0.48%`
- adult pool recall proxy: `580 / 679 = 85.42%`
- precision proxy: `580 / (580 + 85) = 87.22%`

需要注意一点：当前 benign / adult 根目录总量已经比上一次报告时更大，所以这轮结果是“当前真实状态”，但不是只隔离 cleanup 这一件事的纯净 A/B。

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- added `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- added `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- updated task status in `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md` to `DONE`

### Output / Artifact Changes

- recomputed current adult pool counts on `E:\Warden\data\raw\benign\hard benign\adult`
- recomputed current cleaned ordinary-benign counts on `E:\Warden\data\raw\benign\benign`
- refreshed the current proxy metrics for `possible_adult_lure`

---

## 3. Files Touched

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

Optional notes per file:

- no code file was touched
- no dataset directory was moved in this task
- this task only refreshes metrics using the current working-tree labeling logic

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task refreshes the current adult proxy metrics after the benign-pool cleanup
- downstream discussions can now use the current cleaned-pool statistics instead of the stale pre-cleanup numbers

### Preserved Behavior

- no `adult`, `gambling`, or `gate` logic changed
- no schema, field, CLI, or output format changed
- no dataset contents or dataset locations changed in this task

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

- `specialized_surface_signals.possible_adult_lure`
- `specialized_surface_signals.possible_age_gate_surface`
- `matched_keywords.adult_text`

Compatibility notes:

This delivery only refreshes statistics. No runtime interface, schema field, CLI, or output structure changed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- import `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- verify `derive_auto_labels_from_sample_dir`, `derive_rule_labels`, and `iter_sample_dirs` exist
- run a concurrent full-pool metric pass over:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- count:
  - pool total
  - `possible_adult_lure` hits
  - `possible_age_gate_surface` hits
- derive:
  - ordinary-benign false-positive rate
  - adult recall proxy
  - precision proxy
- verify the moved 78-sample cleanup bucket still yields `78` current `possible_adult_lure` hits under the adult pool
```

### Result

- current adult pool:
  - total: `679`
  - `possible_adult_lure`: `580`
  - `possible_age_gate_surface`: `262`
- current ordinary benign pool:
  - total: `17748`
  - `possible_adult_lure`: `85`
  - `possible_age_gate_surface`: `31`
- derived metrics:
  - ordinary-benign false-positive rate: `85 / 17748 = 0.48%`
  - adult recall proxy: `580 / 679 = 85.42%`
  - precision proxy: `580 / (580 + 85) = 87.22%`
- cleanup relation check:
  - moved 78-sample bucket still yields `78` current `possible_adult_lure` hits in the adult pool

Relative to the last reported stale baseline from `docs/handoff/2026-04-16_adult_false_positive_tightening.md`:

- previous ordinary-benign false positives: `144 / 16339 = 0.88%`
- previous adult recall proxy: `481 / 580 = 82.93%`
- previous precision proxy: `76.96%`

Current numbers are directionally better, but the pool sizes changed:

- ordinary benign total: `16339 -> 17748`
- adult total: `580 -> 679`

So this is a current-state rerun, not a pure isolated cleanup-only delta.

### Not Run

- no runtime patch
- no manual human review of the current `85` benign hits
- no new adult precision-tightening pass

Reason:

This task was scoped to metric refresh only.

---

## 7. Risks / Caveats

- the current rerun mixes cleanup effects with later pool growth, because both `ordinary benign` and `hard benign\adult` roots are larger than in the last reported baseline
- these are still proxy metrics tied to current pool composition, not manual gold precision / recall
- the remaining `85` ordinary-benign hits should be re-mined before the next adult tightening pass, because the current root now contains newer adult-like samples that were not in the earlier `66` bucket

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- mine the current remaining `85` ordinary-benign adult hits again on today's root
- split those `85` hits into pool-contamination vs true-rule-noise using the updated current root
- then continue the next adult precision-tightening pass only on the current true-rule-noise bucket

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-17-adult-post-cleanup-metrics-rerun`
- Related Task ID: `TASK-L0-2026-04-17-ADULT-POST-CLEANUP-METRICS-RERUN`
- Task Title: `Rerun adult false-positive statistics on the cleaned benign pool`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-17`
- Status: `DONE`

---

## 1. Executive Summary

This delivery did not change code or dataset placement. It reran pool-level statistics with the current working-tree `adult` logic over the cleaned `E:\Warden\data\raw\benign\benign` root and the current `E:\Warden\data\raw\benign\hard benign\adult` root.

Current results:

- ordinary benign: `85 / 17748 = 0.48%`
- adult recall proxy: `580 / 679 = 85.42%`
- precision proxy: `580 / (580 + 85) = 87.22%`

One caveat matters: both the current benign root and the current adult root are larger than they were in the last reported baseline, so this rerun is the current true state, but it is not a perfectly isolated cleanup-only A/B.

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- added `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- added `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- updated task status in `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md` to `DONE`

### Output / Artifact Changes

- recomputed current adult pool counts on `E:\Warden\data\raw\benign\hard benign\adult`
- recomputed current cleaned ordinary-benign counts on `E:\Warden\data\raw\benign\benign`
- refreshed the current proxy metrics for `possible_adult_lure`

---

## 3. Files Touched

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

Optional notes per file:

- no code file was touched
- no dataset directory was moved in this task
- this task only refreshes metrics using the current working-tree labeling logic

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task refreshes the current adult proxy metrics after the benign-pool cleanup
- downstream discussions can now use the current cleaned-pool statistics instead of the stale pre-cleanup numbers

### Preserved Behavior

- no `adult`, `gambling`, or `gate` logic changed
- no schema, field, CLI, or output format changed
- no dataset contents or dataset locations changed in this task

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

- `specialized_surface_signals.possible_adult_lure`
- `specialized_surface_signals.possible_age_gate_surface`
- `matched_keywords.adult_text`

Compatibility notes:

This delivery only refreshes statistics. No runtime interface, schema field, CLI, or output structure changed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- import `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- verify `derive_auto_labels_from_sample_dir`, `derive_rule_labels`, and `iter_sample_dirs` exist
- run a concurrent full-pool metric pass over:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- count:
  - pool total
  - `possible_adult_lure` hits
  - `possible_age_gate_surface` hits
- derive:
  - ordinary-benign false-positive rate
  - adult recall proxy
  - precision proxy
- verify the moved 78-sample cleanup bucket still yields `78` current `possible_adult_lure` hits under the adult pool
```

### Result

- current adult pool:
  - total: `679`
  - `possible_adult_lure`: `580`
  - `possible_age_gate_surface`: `262`
- current ordinary benign pool:
  - total: `17748`
  - `possible_adult_lure`: `85`
  - `possible_age_gate_surface`: `31`
- derived metrics:
  - ordinary-benign false-positive rate: `85 / 17748 = 0.48%`
  - adult recall proxy: `580 / 679 = 85.42%`
  - precision proxy: `580 / (580 + 85) = 87.22%`
- cleanup relation check:
  - moved 78-sample bucket still yields `78` current `possible_adult_lure` hits in the adult pool

Relative to the last reported stale baseline from `docs/handoff/2026-04-16_adult_false_positive_tightening.md`:

- previous ordinary-benign false positives: `144 / 16339 = 0.88%`
- previous adult recall proxy: `481 / 580 = 82.93%`
- previous precision proxy: `76.96%`

Current numbers are directionally better, but the pool sizes changed:

- ordinary benign total: `16339 -> 17748`
- adult total: `580 -> 679`

So this is a current-state rerun, not a pure isolated cleanup-only delta.

### Not Run

- no runtime patch
- no manual human review of the current `85` benign hits
- no new adult precision-tightening pass

Reason:

This task was scoped to metric refresh only.

---

## 7. Risks / Caveats

- the current rerun mixes cleanup effects with later pool growth, because both `ordinary benign` and `hard benign\adult` roots are larger than in the last reported baseline
- these are still proxy metrics tied to current pool composition, not manual gold precision / recall
- the remaining `85` ordinary-benign hits should be re-mined before the next adult tightening pass, because the current root now contains newer adult-like samples that were not in the earlier `66` bucket

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- mine the current remaining `85` ordinary-benign adult hits again on today's root
- split those `85` hits into pool-contamination vs true-rule-noise using the updated current root
- then continue the next adult precision-tightening pass only on the current true-rule-noise bucket
