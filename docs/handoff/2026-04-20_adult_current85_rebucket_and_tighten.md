# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-20-adult-current85-rebucket-and-tighten`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-CURRENT85-REBUCKET-AND-TIGHTEN`
- Task Title: `重挖当前 85 个 benign adult hits 并继续收紧 adult`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

这次交付分三步完成：

- 重挖当前 `85` 个 ordinary-benign `possible_adult_lure` 命中；
- 把重新确认更像成人污染样本的两批目录移出 `E:\Warden\data\raw\benign\benign`；
- 只对最后剩下的 true-rule-noise 桶做一轮更窄的 `adult` L0 收紧。

最终结果：

- 一共移走 `55` 个更像成人污染的样本目录
- 当前 ordinary benign 样本总量：`16620`
- 当前 adult 样本总量：`734`
- patch 后 ordinary benign `possible_adult_lure`: `0 / 16620`
- patch 后 adult `possible_adult_lure`: `591 / 734 = 80.52%`

当前这版的取舍很明确：

- benign 侧当前噪音被清到 `0`
- adult 侧 recall proxy 从清理后 patch 前的 `86.51%` 降到 `80.52%`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `ADULT_DOMAIN_HINT_TOKENS`
- added `has_adult_domain_hint(...)`
- tightened `possible_adult_lure` from a broad `2-token` path to a narrower set:
  - strong adult URL hit
  - high-confidence adult hit
  - at least `3` strong adult text hits
  - at least `2` strong adult text hits with adult domain / host hint
  - strong adult text with strong age-gate support

### Doc Changes

- updated `L0_DESIGN_V1.md`
- added `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- added `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

### Output / Artifact Changes

- moved `31` sample directories from `E:\Warden\data\raw\benign\benign` to `E:\Warden\data\raw\benign\hard benign\adult`
- moved another `24` sample directories from `E:\Warden\data\raw\benign\benign` to `E:\Warden\data\raw\benign\hard benign\adult`
- total cleanup move this task: `55` sample directories

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `E:\Warden\data\raw\benign\benign\<55 moved sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<55 moved sample_dirs>`

Optional notes per file:

- the 55 moved sample dirs were split into a first `31`-sample contamination bucket and a second `24`-sample stricter-triage contamination bucket
- no `gambling` or `gate` code was touched
- no schema or CLI file was touched

---

## 4. Behavior Impact

### Expected New Behavior

- ordinary-benign pages that previously triggered `possible_adult_lure` through weak or unsupported `2-token` adult paths are now suppressed more aggressively
- adult pages now need stronger text density, stronger host support, stronger age-gate support, or higher-confidence evidence to stay in the L0 adult surface bucket
- more adult-looking contamination samples are now physically outside the ordinary-benign pool

### Preserved Behavior

- strong adult URL hits still trigger adult surfaces
- high-confidence adult hits still trigger adult surfaces
- current `gambling` and `gate` behavior is unchanged
- schema, field names, CLI, and output format remain unchanged

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
- `specialized_surface_signals.matched_keywords.adult_*`

Compatibility notes:

This task tightens existing adult detection behavior and relocates selected dataset directories. No schema field, runtime interface, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- re-extract the current `85` ordinary-benign `possible_adult_lure` hits
- run a corrected-field rebucketing pass using `specialized_surface_signals.matched_keywords`
- first split result:
  - `31` contamination
  - `54` true-rule-noise
- verify and move the `31` contamination sample dirs
- run a stricter second triage on the remaining `54`
- second split result:
  - `24` additional contamination
  - `30` remaining true-rule-noise
- verify and move the additional `24` contamination sample dirs

python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- count current sample dirs under:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- rerun post-patch adult metrics across the full adult root
- rerun post-patch metrics across the current remaining `30` true-rule-noise benign samples
- verify post-patch remaining benign noise hits are `0`
```

### Result

- first rebucket:
  - current benign adult hits: `85`
  - first contamination bucket: `31`
  - first true-rule-noise bucket: `54`
- first move:
  - moved: `31`
  - remaining in source: `0`
  - present in destination: `31`
- second stricter rebucket over the remaining `54`:
  - additional contamination: `24`
  - final true-rule-noise bucket: `30`
- second move:
  - moved: `24`
  - remaining in source: `0`
  - present in destination: `24`

Current dataset counts after both moves:

- adult total: `734`
- benign total: `16620`

Pre-patch baseline after the second move:

- adult `possible_adult_lure`: `635 / 734 = 86.51%`
- benign `possible_adult_lure`: `30 / 16620 = 0.18%`
- precision proxy: `635 / (635 + 30) = 95.49%`

Post-patch metrics:

- adult `possible_adult_lure`: `591 / 734 = 80.52%`
- adult `possible_age_gate_surface`: `293 / 734 = 39.92%`
- remaining benign true-rule-noise `possible_adult_lure`: `0 / 30`
- remaining benign true-rule-noise `possible_age_gate_surface`: `0 / 30`

Inference from the tightened predicate:

- the new `possible_adult_lure` logic only removes previous trigger paths; it does not add any new positive path
- after both contamination moves, the only known current benign positives were the remaining `30` noise samples
- those `30` all evaluate false after the patch
- therefore current benign `possible_adult_lure` is `0 / 16620`

### Not Run

- no full mixed-batch regression across adult / gambling / gate / benign
- no screenshot- or OCR-based adult analysis
- no manual human review of every moved sample

Reason:

This task was scoped to current-root rebucketing, dataset cleanup, and one low-cost adult tightening pass only.

---

## 7. Risks / Caveats

- the contamination split remains heuristic triage, not manual gold labeling
- this patch improves benign precision aggressively, but it reduces adult recall proxy by about `6.00` absolute points from the post-cleanup pre-patch baseline (`86.51% -> 80.52%`)
- adult pages that expose only `1-2` strong adult text hits without host support or age-gate support are now more likely to fall through L0

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- spot-check a focused sample of the `55` moved contamination pages to confirm the rebucketing quality
- inspect the `44` adult pages that dropped out under the new tighter rule and decide whether a very small adult-domain recovery is justified
- only after that, decide whether to keep this `adult` precision-first setting or re-open a small recall-recovery task

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-20-adult-current85-rebucket-and-tighten`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-CURRENT85-REBUCKET-AND-TIGHTEN`
- Task Title: `Rebucket the current 85 benign adult hits and continue adult tightening`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

This delivery completed three bounded steps:

- re-mine the current `85` ordinary-benign `possible_adult_lure` hits;
- move the samples that now look more like adult-pool contamination out of `E:\Warden\data\raw\benign\benign`;
- tighten `adult` L0 logic only against the final true-rule-noise bucket.

Final result:

- `55` adult-contamination sample directories were moved in total
- current ordinary-benign sample count: `16620`
- current adult sample count: `734`
- post-patch ordinary-benign `possible_adult_lure`: `0 / 16620`
- post-patch adult `possible_adult_lure`: `591 / 734 = 80.52%`

The tradeoff of this version is explicit:

- current benign noise is reduced to `0`
- adult recall proxy falls from the post-cleanup pre-patch baseline of `86.51%` to `80.52%`

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `ADULT_DOMAIN_HINT_TOKENS`
- added `has_adult_domain_hint(...)`
- tightened `possible_adult_lure` from a broad `2-token` path to a narrower set:
  - strong adult URL hit
  - high-confidence adult hit
  - at least `3` strong adult text hits
  - at least `2` strong adult text hits with adult domain / host hint
  - strong adult text with strong age-gate support

### Doc Changes

- updated `L0_DESIGN_V1.md`
- added `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- added `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

### Output / Artifact Changes

- moved `31` sample directories from `E:\Warden\data\raw\benign\benign` to `E:\Warden\data\raw\benign\hard benign\adult`
- moved another `24` sample directories from `E:\Warden\data\raw\benign\benign` to `E:\Warden\data\raw\benign\hard benign\adult`
- total cleanup move in this task: `55` sample directories

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `E:\Warden\data\raw\benign\benign\<55 moved sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<55 moved sample_dirs>`

Optional notes per file:

- the 55 moved sample dirs were split into a first `31`-sample contamination bucket and a second `24`-sample stricter-triage contamination bucket
- no `gambling` or `gate` code was touched
- no schema or CLI file was touched

---

## 4. Behavior Impact

### Expected New Behavior

- ordinary-benign pages that previously triggered `possible_adult_lure` through weak or unsupported `2-token` adult paths are now suppressed more aggressively
- adult pages now need stronger text density, stronger host support, stronger age-gate support, or higher-confidence evidence to remain in the L0 adult surface bucket
- more adult-looking contamination samples are now physically outside the ordinary-benign pool

### Preserved Behavior

- strong adult URL hits still trigger adult surfaces
- high-confidence adult hits still trigger adult surfaces
- current `gambling` and `gate` behavior is unchanged
- schema, field names, CLI, and output format remain unchanged

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
- `specialized_surface_signals.matched_keywords.adult_*`

Compatibility notes:

This task tightens existing adult detection behavior and relocates selected dataset directories. No schema field, runtime interface, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- re-extract the current `85` ordinary-benign `possible_adult_lure` hits
- run a corrected-field rebucketing pass using `specialized_surface_signals.matched_keywords`
- first split result:
  - `31` contamination
  - `54` true-rule-noise
- verify and move the `31` contamination sample dirs
- run a stricter second triage on the remaining `54`
- second split result:
  - `24` additional contamination
  - `30` remaining true-rule-noise
- verify and move the additional `24` contamination sample dirs

python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- count current sample dirs under:
  - `E:\Warden\data\raw\benign\hard benign\adult`
  - `E:\Warden\data\raw\benign\benign`
- rerun post-patch adult metrics across the full adult root
- rerun post-patch metrics across the current remaining `30` true-rule-noise benign samples
- verify post-patch remaining benign noise hits are `0`
```

### Result

- first rebucket:
  - current benign adult hits: `85`
  - first contamination bucket: `31`
  - first true-rule-noise bucket: `54`
- first move:
  - moved: `31`
  - remaining in source: `0`
  - present in destination: `31`
- second stricter rebucket over the remaining `54`:
  - additional contamination: `24`
  - final true-rule-noise bucket: `30`
- second move:
  - moved: `24`
  - remaining in source: `0`
  - present in destination: `24`

Current dataset counts after both moves:

- adult total: `734`
- benign total: `16620`

Pre-patch baseline after the second move:

- adult `possible_adult_lure`: `635 / 734 = 86.51%`
- benign `possible_adult_lure`: `30 / 16620 = 0.18%`
- precision proxy: `635 / (635 + 30) = 95.49%`

Post-patch metrics:

- adult `possible_adult_lure`: `591 / 734 = 80.52%`
- adult `possible_age_gate_surface`: `293 / 734 = 39.92%`
- remaining benign true-rule-noise `possible_adult_lure`: `0 / 30`
- remaining benign true-rule-noise `possible_age_gate_surface`: `0 / 30`

Inference from the tightened predicate:

- the new `possible_adult_lure` logic only removes previous trigger paths; it does not add any new positive path
- after both contamination moves, the only known current benign positives were the remaining `30` noise samples
- those `30` all evaluate false after the patch
- therefore current benign `possible_adult_lure` is `0 / 16620`

### Not Run

- no full mixed-batch regression across adult / gambling / gate / benign
- no screenshot- or OCR-based adult analysis
- no manual human review of every moved sample

Reason:

This task was scoped to current-root rebucketing, dataset cleanup, and one low-cost adult tightening pass only.

---

## 7. Risks / Caveats

- the contamination split remains heuristic triage, not manual gold labeling
- this patch improves benign precision aggressively, but it reduces adult recall proxy by about `6.00` absolute points from the post-cleanup pre-patch baseline (`86.51% -> 80.52%`)
- adult pages that expose only `1-2` strong adult text hits without host support or age-gate support are now more likely to fall through L0

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- spot-check a focused sample of the `55` moved contamination pages to confirm the rebucketing quality
- inspect the `44` adult pages that dropped out under the new tighter rule and decide whether a very small adult-domain recovery is justified
- only after that, decide whether to keep this `adult` precision-first setting or reopen a small recall-recovery task
