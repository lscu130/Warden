# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
- Handoff ID: `2026-04-20-adult-domain-recovery`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-DOMAIN-RECOVERY`
- Task Title: `恢复 adult 的窄域名支持单强词路径`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

这次交付只做了一条非常窄的 adult recall recovery：

- 只针对 `single_strong_token_with_domain_only`
- 只允许显式白名单 token：`jav`、`porno`、`avxxx`
- 只在 URL / host 同时带有显著 adult domain hint 时生效

当前池上，用同一套评估口径得到的结果是：

- adult pool: `591 / 734 -> 594 / 734`
- benign pool: `0 / 16623 -> 0 / 16623`
- precision proxy: `1.0000 -> 1.0000`
- 净新增 adult 回收样本：`3`

净新增回收样本为：

- `avxxxmini.com_20260408T071508Z`
- `kangenjav.com_20260413T103704Z`
- `njav.org_20260414T082227Z`

另有 `onejav.com_20260403T024535Z` 命中了 recovery pattern，但它原本已通过 age-gate 路径命中，不构成净新增。

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKENS`
- added `adult_domain_single_strong_recovery`
- extended `possible_adult_lure` with one narrow allowlisted recovery path

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-20_adult_domain_recovery.md`
- added `docs/handoff/2026-04-20_adult_domain_recovery.md`

### Output / Artifact Changes

- no dataset directories moved
- no schema fields changed
- no CLI surface changed

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_domain_recovery.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` received one additive narrow adult recovery path only
- `L0_DESIGN_V1.md` now documents the allowlisted single-strong-token recovery constraint in both Chinese and English

---

## 4. Behavior Impact

### Expected New Behavior

- pages with exactly one strong adult text token may now trigger `possible_adult_lure` when:
  - the page also has an adult domain / host hint
  - the strong token is in the explicit allowlist
- the recovery stays inside the narrow pattern chosen by the prior review

### Preserved Behavior

- all previously documented adult paths remain unchanged
- `gambling` and `gate` logic remain unchanged
- schema, field names, CLI, and output format remain unchanged
- generic hosts and ambiguous single-token pages still do not enter through this path

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

Compatibility notes:

This task only adds and documents one additional detection path inside the existing adult detector. No field, key, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- evaluate current-pool adult / benign metrics with one consistent pre-patch vs post-patch comparator
- enumerate net-new recovered adult samples
- verify benign rebound on the current full benign root
```

### Result

Current pool sizes:

- adult total: `734`
- benign total: `16623`

Current-pool pre-patch vs post-patch comparison:

- adult `possible_adult_lure`: `591 / 734 = 80.52%` -> `594 / 734 = 80.93%`
- benign `possible_adult_lure`: `0 / 16623 = 0.00%` -> `0 / 16623 = 0.00%`
- adult net-new recovered samples: `3`
- adult recovery-pattern overlap samples already covered by another path: `1`
- adult `possible_age_gate_surface`: `294 / 734 = 40.05%`
- precision proxy: `1.0000 -> 1.0000`

Net-new recovered adult samples:

- `avxxxmini.com_20260408T071508Z`
- `kangenjav.com_20260413T103704Z`
- `njav.org_20260414T082227Z`

Recovery-pattern overlap sample:

- `onejav.com_20260403T024535Z`
  - this sample already hit through the strong age-gate path before the recovery patch

### Not Run

- no mixed vertical regression across gambling / adult / gate / benign
- no screenshot or OCR-based adult validation
- no manual review of the entire adult pool

Reason:

This task was explicitly scoped to one low-cost adult-domain recovery only.

---

## 7. Risks / Caveats

- the gain is intentionally small; this is a precision-preserving recovery, not a broad adult recall reopening
- current evaluation is based on the local text-root scan used in this task; it should be compared against future runs only when the same evaluation method is reused
- `porno` stayed in the allowlist for compatibility with the earlier candidate screen, but the current-pool net-new recoveries came from `jav` and `avxxx`

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_domain_recovery.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- keep this narrow adult-domain recovery as the current adult precision/recall compromise
- if adult recall is still considered insufficient, mine the remaining missed adult pages by subpattern again instead of reopening a broad rollback
- if future pool quality work continues, separately review the new `16623` benign-root composition before using it as a publication-grade baseline

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-20-adult-domain-recovery`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-DOMAIN-RECOVERY`
- Task Title: `Recover the narrow adult domain-supported single-strong-token path`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

This delivery implemented one very narrow adult recall-recovery path only:

- restricted to `single_strong_token_with_domain_only`
- restricted to the explicit allowlist tokens `jav`, `porno`, and `avxxx`
- restricted to pages where the URL / host also carries a salient adult-domain hint

On the current pools, using one consistent evaluation method, the result is:

- adult pool: `591 / 734 -> 594 / 734`
- benign pool: `0 / 16623 -> 0 / 16623`
- precision proxy: `1.0000 -> 1.0000`
- net-new adult recoveries: `3`

The net-new recovered adult samples are:

- `avxxxmini.com_20260408T071508Z`
- `kangenjav.com_20260413T103704Z`
- `njav.org_20260414T082227Z`

There is also one overlap case, `onejav.com_20260403T024535Z`, which matches the recovery pattern but was already covered by the age-gate path before this patch, so it does not count as a net-new recovery.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added `ADULT_DOMAIN_SINGLE_STRONG_RECOVERY_TOKENS`
- added `adult_domain_single_strong_recovery`
- extended `possible_adult_lure` with one narrow allowlisted recovery path

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-20_adult_domain_recovery.md`
- added `docs/handoff/2026-04-20_adult_domain_recovery.md`

### Output / Artifact Changes

- no dataset directories were moved
- no schema fields changed
- no CLI surface changed

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_domain_recovery.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` received one additive narrow adult recovery path only
- `L0_DESIGN_V1.md` now documents the allowlisted single-strong-token recovery constraint in both Chinese and English

---

## 4. Behavior Impact

### Expected New Behavior

- pages with exactly one strong adult text token may now trigger `possible_adult_lure` when:
  - the page also has an adult domain / host hint
  - the strong token is inside the explicit allowlist
- the recovery remains inside the narrow pattern recommended by the prior review

### Preserved Behavior

- all previously documented adult trigger paths remain unchanged
- `gambling` and `gate` logic remain unchanged
- schema, field names, CLI, and output format remain unchanged
- generic hosts and ambiguous single-token pages still do not enter through this path

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

Compatibility notes:

This task only adds and documents one additional detection path inside the existing adult detector. No field, key, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- evaluate current-pool adult / benign metrics with one consistent pre-patch vs post-patch comparator
- enumerate net-new recovered adult samples
- verify benign rebound on the current full benign root
```

### Result

Current pool sizes:

- adult total: `734`
- benign total: `16623`

Current-pool pre-patch vs post-patch comparison:

- adult `possible_adult_lure`: `591 / 734 = 80.52%` -> `594 / 734 = 80.93%`
- benign `possible_adult_lure`: `0 / 16623 = 0.00%` -> `0 / 16623 = 0.00%`
- adult net-new recovered samples: `3`
- adult recovery-pattern overlap samples already covered by another path: `1`
- adult `possible_age_gate_surface`: `294 / 734 = 40.05%`
- precision proxy: `1.0000 -> 1.0000`

Net-new recovered adult samples:

- `avxxxmini.com_20260408T071508Z`
- `kangenjav.com_20260413T103704Z`
- `njav.org_20260414T082227Z`

Recovery-pattern overlap sample:

- `onejav.com_20260403T024535Z`
  - this sample already hit through the strong age-gate path before the recovery patch

### Not Run

- no mixed-vertical regression across gambling / adult / gate / benign
- no screenshot- or OCR-based adult validation
- no manual review of the entire adult pool

Reason:

This task was explicitly scoped to one low-cost adult-domain recovery only.

---

## 7. Risks / Caveats

- the gain is intentionally small; this is a precision-preserving recovery, not a broad adult recall reopening
- the current evaluation is based on the local text-root scan used in this task; it should only be compared to future runs that reuse the same evaluation method
- `porno` remains in the allowlist for compatibility with the earlier candidate screen, but the current-pool net-new recoveries came from `jav` and `avxxx`

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_domain_recovery.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- keep this narrow adult-domain recovery as the current adult precision/recall compromise
- if adult recall is still considered insufficient, mine the remaining missed adult pages by subpattern again instead of reopening a broad rollback
- if future pool-quality work continues, separately review the new `16623` benign-root composition before using it as a publication-grade baseline
