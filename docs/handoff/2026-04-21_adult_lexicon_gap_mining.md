# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
- Handoff ID: `2026-04-21-adult-lexicon-gap-mining`
- Related Task ID: `TASK-L0-2026-04-21-ADULT-LEXICON-GAP-MINING`
- Task Title: `Adult mixed low-support 词缺口挖掘与低成本特化`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

这次交付只针对 adult 的 `mixed low-support` miss 桶做了词缺口挖掘，并落了一条保守特化：

- 把 `colmek` 加入 adult 文本词
- 把 `bokep` 加入 adult host/domain hint

我没有重开 broad adult recall recovery，也没有碰 `gambling` / `gate`。当前池上，用同一套旧规则 vs 新规则口径重算后：

- adult `possible_adult_lure`: `622 / 772 -> 627 / 772`
- benign `possible_adult_lure`: `2 / 17138 -> 2 / 17138`
- precision proxy: `0.996795 -> 0.996820`

结论是：这条本地化词缺口补丁带来了小幅 recall 提升，同时没有新增 benign 反弹。

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added the localized adult text token `colmek` to `ADULT_KEYWORDS`
- added the localized adult domain-hint token `bokep` to `ADULT_DOMAIN_HINT_TOKENS`

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- added `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

### Output / Artifact Changes

- no dataset directories moved
- no schema fields changed
- no CLI surface changed

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

Optional notes per file:

- the code change is limited to one localized text token and one localized domain-hint token
- the doc update explicitly states that localized lexicon-gap refinements must remain narrow and evidence-backed

---

## 4. Behavior Impact

### Expected New Behavior

- adult pages containing the localized text token `colmek` can now contribute one strong adult text hit
- hosts or URLs containing `bokep` can now contribute adult-domain support
- some Indonesian/localized adult pages that previously stayed in the mixed low-support miss bucket now rise into `possible_adult_lure`

### Preserved Behavior

- the existing adult trigger framework is unchanged
- no broad semantic relaxation was added
- `gambling` and `gate` logic are unchanged
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

Compatibility notes:

This task only refines adult detection inputs inside the existing detector. No field, key, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- re-mine the current mixed low-support miss bucket
- compare repeated localized tokens against the benign pool
- simulate several minimal localized-adult refinements
- rerun current-pool old-rule vs new-rule adult/benign quantification
```

### Result

Current pool sizes used in this task:

- adult total: `772`
- benign total: `17138`

Mixed low-support mining summary:

- current mixed low-support bucket size: `52`
- repeated localized adult-like tokens included:
  - `bokep`
  - `colmek`
  - `jilbab`
  - `hijab`
  - `ngewe`
  - `tante`

Shortlist screen against the current full pools:

- `bokep`: adult `34`, benign `4`
- `colmek`: adult `17`, benign `1`
- `jilbab`: adult `22`, benign `3`
- `hijab`: adult `47`, benign `9`
- `ngewe`: adult `15`, benign `29`
- `tante`: adult `34`, benign `518`

Selection conclusion:

- `colmek` is the cleanest localized text token in this pass
- `bokep` is acceptable as a domain-hint token
- `ngewe`, `tante`, and `ero` are too noisy for this task boundary
- `jilbab` / `hijab` still carry contextual ambiguity and were not added

Current-pool old-rule vs new-rule comparison after the patch:

- adult `possible_adult_lure`: `622 / 772 = 80.57%` -> `627 / 772 = 81.22%`
- benign `possible_adult_lure`: `2 / 17138 = 0.0117%` -> `2 / 17138 = 0.0117%`
- adult `possible_age_gate_surface`: `307 / 772 = 39.77%`
- precision proxy: `0.996795 -> 0.996820`

Representative newly recovered adult samples:

- `bebasindi.pro_20260325T150938Z`
- `bokepcrot.ws_20260414T065146Z`
- `drbokep.page_20260401T093715Z`
- `njav.org_20260414T082227Z`
- `pasarbokep.com_20260325T071619Z`

New benign rebound samples:

- none

### Not Run

- no mixed vertical regression across gambling / adult / gate / benign bundles
- no screenshot- or OCR-based adult validation
- no manual relabel pass over the newly enlarged adult and benign pools

Reason:

This task was explicitly scoped to one low-cost localized adult lexicon refinement only.

---

## 7. Risks / Caveats

- the gain is modest; this is a conservative lexicon-gap recovery, not a broad adult recall reopen
- the current pool sizes changed relative to earlier tasks, so this handoff should only be compared directly against runs using the same current-pool method
- `bokep` was added only as a domain-hint token; if it is later promoted to a full adult text token, benign rebound should be re-measured carefully

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- continue adult recall work only through the remaining mixed low-support subpatterns
- if another localized mining pass is opened, prioritize candidates with adult-heavy counts like `colmek`, not broad ambiguous words
- if pool quality matters for later reporting, separately audit why the current benign pool already contains `2` baseline adult hits

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-21-adult-lexicon-gap-mining`
- Related Task ID: `TASK-L0-2026-04-21-ADULT-LEXICON-GAP-MINING`
- Task Title: `Mine the adult mixed low-support vocabulary gaps and add one low-cost refinement`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-21`
- Status: `DONE`

---

## 1. Executive Summary

This delivery only mined the adult `mixed low-support` miss bucket for vocabulary gaps and implemented one conservative localized refinement:

- add `colmek` as an adult text token
- add `bokep` as an adult host/domain-hint token

I did not reopen a broad adult recall recovery, and I did not touch `gambling` or `gate`. On the current pools, using one consistent old-rule vs new-rule comparison, the result is:

- adult `possible_adult_lure`: `622 / 772 -> 627 / 772`
- benign `possible_adult_lure`: `2 / 17138 -> 2 / 17138`
- precision proxy: `0.996795 -> 0.996820`

The result is a small recall improvement with no new benign rebound under the current evaluation method.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added the localized adult text token `colmek` to `ADULT_KEYWORDS`
- added the localized adult domain-hint token `bokep` to `ADULT_DOMAIN_HINT_TOKENS`

### Doc Changes

- updated `L0_DESIGN_V1.md`
- updated `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- added `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

### Output / Artifact Changes

- no dataset directories were moved
- no schema fields changed
- no CLI surface changed

---

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

Optional notes per file:

- the code change is limited to one localized text token and one localized domain-hint token
- the doc update now states explicitly that localized lexicon-gap refinements must remain narrow and evidence-backed

---

## 4. Behavior Impact

### Expected New Behavior

- adult pages containing the localized text token `colmek` can now contribute one strong adult text hit
- hosts or URLs containing `bokep` can now contribute adult-domain support
- some Indonesian/localized adult pages that previously remained in the mixed low-support miss bucket now rise into `possible_adult_lure`

### Preserved Behavior

- the existing adult trigger framework is unchanged
- no broad semantic relaxation was added
- `gambling` and `gate` logic are unchanged
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

Compatibility notes:

This task only refines adult detection inputs inside the existing detector. No field, key, CLI flag, or output structure was renamed or removed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- re-mine the current mixed low-support miss bucket
- compare repeated localized tokens against the benign pool
- simulate several minimal localized-adult refinements
- rerun current-pool old-rule vs new-rule adult/benign quantification
```

### Result

Current pool sizes used in this task:

- adult total: `772`
- benign total: `17138`

Mixed low-support mining summary:

- current mixed low-support bucket size: `52`
- repeated localized adult-like tokens included:
  - `bokep`
  - `colmek`
  - `jilbab`
  - `hijab`
  - `ngewe`
  - `tante`

Shortlist screen against the current full pools:

- `bokep`: adult `34`, benign `4`
- `colmek`: adult `17`, benign `1`
- `jilbab`: adult `22`, benign `3`
- `hijab`: adult `47`, benign `9`
- `ngewe`: adult `15`, benign `29`
- `tante`: adult `34`, benign `518`

Selection conclusion:

- `colmek` is the cleanest localized text token in this pass
- `bokep` is acceptable as a domain-hint token
- `ngewe`, `tante`, and `ero` are too noisy for this task boundary
- `jilbab` / `hijab` still carry contextual ambiguity and were not added

Current-pool old-rule vs new-rule comparison after the patch:

- adult `possible_adult_lure`: `622 / 772 = 80.57%` -> `627 / 772 = 81.22%`
- benign `possible_adult_lure`: `2 / 17138 = 0.0117%` -> `2 / 17138 = 0.0117%`
- adult `possible_age_gate_surface`: `307 / 772 = 39.77%`
- precision proxy: `0.996795 -> 0.996820`

Representative newly recovered adult samples:

- `bebasindi.pro_20260325T150938Z`
- `bokepcrot.ws_20260414T065146Z`
- `drbokep.page_20260401T093715Z`
- `njav.org_20260414T082227Z`
- `pasarbokep.com_20260325T071619Z`

New benign rebound samples:

- none

### Not Run

- no mixed-vertical regression across gambling / adult / gate / benign bundles
- no screenshot- or OCR-based adult validation
- no manual relabel pass over the newly enlarged adult and benign pools

Reason:

This task was explicitly scoped to one low-cost localized adult lexicon refinement only.

---

## 7. Risks / Caveats

- the gain is modest; this is a conservative lexicon-gap recovery, not a broad adult recall reopen
- the current pool sizes changed relative to earlier tasks, so this handoff should only be compared directly against runs using the same current-pool method
- `bokep` was added only as a domain-hint token; if it is later promoted to a full adult text token, benign rebound should be re-measured carefully

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- continue adult recall work only through the remaining mixed low-support subpatterns
- if another localized mining pass is opened, prioritize candidates with adult-heavy counts like `colmek`, not broad ambiguous words
- if pool quality matters for later reporting, separately audit why the current benign pool already contains `2` baseline adult hits
