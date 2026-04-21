# Handoff Metadata

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-15-gambling-low-cost-toto-togel-host-recovery`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-LOW-COST-TOTO-TOGEL-HOST-RECOVERY`
- Task Title: `补 toto/togel host 的低成本 gambling recovery`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

这次交付继续补 `gambling` 的低成本结构证据，目标是 `toto/togel` host recovery。

结果先说清楚：

- `toto/togel` host 模式在当前 full gambling pool 里一共 `10` 个样本
- 其中原本已命中 `8`
- 剩余 miss 只有 `2`
- full benign root 里匹配到 `toto/togel` host 的样本有 `6`

所以这条任务不适合做“host 里有 toto/togel 就直接放行”的宽规则。

最后落地的是一条极窄 recovery：

- `score < 4`
- URL/host 含 `toto` 或 `togel`
- `page_title` 同时含 `bandar` 和 `togel`
- 且必须是前面 recovery 都没补到的页

这条规则最后只补回了 `1` 个真正增量样本：

- `67toto.xyz_20260407T032641Z`

benign 增量是 `0`。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 新增窄 recovery：
  - `gambling_toto_togel_host_recovery`
- 条件是：
  - `not` already recovered by previous gambling recovery paths
  - `gambling_weighted_score < 4`
  - final URL 中有 `toto` 或 `togel`
  - `title_text` 中同时有 `bandar` 和 `togel`
- 新增 explainability reason code：
  - `gambling_toto_togel_host_recovery`

### Doc Changes

- 更新 task：`docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- 新增 handoff：`docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

### Output / Artifact Changes

- 无新增 schema 字段
- `specialized_reason_codes` 新增一个 additive reason code

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `toto/togel` host 只有在标题也明确呈现博彩语义时，才会被补成 `possible_gambling_lure`
- 这条规则不会把 `toto/togel` host 本身当成充分条件
- 这条规则只吃低成本 `host + title + current score`，不碰重证据

### Preserved Behavior

- 之前的 score fallback 未改
- `score=7 + domain_hint` recovery 未改
- `1xbet / 1xbt` landing recovery 未改
- multilingual title-token recovery 未改
- `adult / gate` 未改

### User-facing / CLI Impact

- none

### Output Format Impact

- `specialized_reason_codes` 里新增一个可选 reason code

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_surface_signals.specialized_reason_codes`

Compatibility notes:

这次没有新增字段、删字段、改字段名、改 CLI。
唯一新增的是一个 additive reason code。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- scan the current full gambling pool for `toto/togel` hosts
- scan the full benign root for `toto/togel` hosts
- validate the narrow host recovery on:
  - reproducible `ordinary_benign = 800`
  - current full `gambling` pool
```

### Result

Pattern mining:

- current full gambling pool `toto/togel` host count: `10`
- already hit before this patch: `8`
- remaining host misses: `2`
  - `67toto.xyz_20260407T032641Z`
  - `pilartoto.org_20260325T131715Z`
- full benign root `toto/togel` host count: `6`

Why the rule stayed narrow:

- `67toto.xyz` title is explicitly gambling:
  - contains both `bandar` and `togel`
- `pilartoto.org` title does not provide the same level of direct gambling evidence
- several benign `toto/togel` hosts exist, so host-only recovery is unsafe

Direct incremental effect of the new reason code:

- `gambling_toto_togel_host_recovery` on gambling: `1`
- `gambling_toto_togel_host_recovery` on benign: `0`

Recovered gambling sample:

- `67toto.xyz_20260407T032641Z`

Not recovered by this rule:

- `pilartoto.org_20260325T131715Z`

Current totals after this patch:

- `ordinary_benign`: `possible_gambling_lure = 10 / 800`
- `gambling`: `possible_gambling_lure = 564 / 842`

### Not Run

- full mixed-batch rerun
- broad `toto/togel` host token expansion
- evaluation-determinism root-cause fix

Reason:

这条任务只做窄 host recovery，不做更大范围结构词扩展。

---

## 7. Risks / Caveats

- 这条 recovery 只补回了 `67toto` 这一档，非常窄
- `pilartoto` 仍然没收，因为当前 title 证据不够干净
- full benign root 已经证明 `toto/togel` host 本身会带来噪音，所以这条规则不能轻易继续放宽
- 当前 reproducible benign baseline 的总命中数与前面某些线程内统计不完全一致，说明评估环境仍有漂移风险；这也是为什么这次 handoff 重点报告直接增量 reason-code 效果

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` 还没有记录 `gambling_toto_togel_host_recovery`
- evaluation determinism 仍需单开任务收口

---

## 9. Recommended Next Step

- 如果继续追 recall，下一条建议开：
  - `gambling low-cost pilartoto-style title clarification`
  - 或 `gambling low-cost vietnamese title-token recovery`
- 如果先补工程质量，下一条仍建议：
  - `gambling evaluation determinism check`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-15-gambling-low-cost-toto-togel-host-recovery`
- Related Task ID: `TASK-L0-2026-04-15-GAMBLING-LOW-COST-TOTO-TOGEL-HOST-RECOVERY`
- Task Title: `Recover gambling misses using low-cost toto/togel host patterns`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-15`
- Status: `DONE`

---

## 1. Executive Summary

This delivery continued low-cost structural recovery for `gambling`, focusing on `toto/togel` host patterns.

The outcome is straightforward:

- there are `10` `toto/togel` host samples in the current full gambling pool
- `8` were already detected before this patch
- only `2` remained missed
- there are `6` `toto/togel` host samples in the full benign root

That means this task is not a good place for a broad “host contains toto/togel -> allow” rule.

The final implementation is one extremely narrow recovery:

- `score < 4`
- final URL / host contains `toto` or `togel`
- `page_title` contains both `bandar` and `togel`
- and no earlier gambling recovery path already handled the sample

This rule recovers exactly `1` true incremental sample:

- `67toto.xyz_20260407T032641Z`

Incremental benign effect is `0`.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- added a narrow recovery:
  - `gambling_toto_togel_host_recovery`
- the condition requires:
  - not already recovered by prior gambling recovery paths
  - `gambling_weighted_score < 4`
  - final URL contains `toto` or `togel`
  - `title_text` contains both `bandar` and `togel`
- added one explainability reason code:
  - `gambling_toto_togel_host_recovery`

### Doc Changes

- updated task: `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- added handoff: `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

### Output / Artifact Changes

- no schema fields were added
- one additive reason code was added under `specialized_reason_codes`

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

---

## 4. Behavior Impact

### Expected New Behavior

- `toto/togel` hosts are only recovered when the title also presents direct gambling semantics
- this rule does not treat the host token alone as sufficient evidence
- this rule uses only low-cost `host + title + current score` evidence and does not introduce heavy evidence

### Preserved Behavior

- the existing score fallback is unchanged
- the `score=7 + domain_hint` recovery is unchanged
- the `1xbet / 1xbt` landing recovery is unchanged
- the multilingual title-token recovery is unchanged
- `adult` and `gate` remain unchanged

### User-facing / CLI Impact

- none

### Output Format Impact

- one optional reason code was added under `specialized_reason_codes`

---

## 5. Schema / Interface Impact

- Schema changed: `NO`
- Backward compatible: `YES`
- Public interface changed: `NO`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- `specialized_surface_signals.possible_gambling_lure`
- `specialized_surface_signals.specialized_reason_codes`

Compatibility notes:

This task did not add fields, remove fields, rename fields, or change CLI.
The only additive change is one reason code.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell inline Python:
- scan the current full gambling pool for `toto/togel` hosts
- scan the full benign root for `toto/togel` hosts
- validate the narrow host recovery on:
  - reproducible `ordinary_benign = 800`
  - the current full `gambling` pool
```

### Result

Pattern mining:

- current full gambling pool `toto/togel` host count: `10`
- already hit before this patch: `8`
- remaining host misses: `2`
  - `67toto.xyz_20260407T032641Z`
  - `pilartoto.org_20260325T131715Z`
- full benign root `toto/togel` host count: `6`

Why the rule stayed narrow:

- `67toto.xyz` has an explicitly gambling title:
  - contains both `bandar` and `togel`
- `pilartoto.org` does not present the same level of direct gambling title evidence
- several benign `toto/togel` hosts already exist, so host-only recovery is unsafe

Direct incremental effect of the new reason code:

- `gambling_toto_togel_host_recovery` on gambling: `1`
- `gambling_toto_togel_host_recovery` on benign: `0`

Recovered gambling sample:

- `67toto.xyz_20260407T032641Z`

Not recovered by this rule:

- `pilartoto.org_20260325T131715Z`

Current totals after this patch:

- `ordinary_benign`: `possible_gambling_lure = 10 / 800`
- `gambling`: `possible_gambling_lure = 564 / 842`

### Not Run

- full mixed-batch rerun
- broad `toto/togel` host token expansion
- evaluation-determinism root-cause fix

Reason:

This task only lands a narrow host recovery and does not broaden structural token coverage further.

---

## 7. Risks / Caveats

- this recovery adds only one sample, which is intentionally narrow
- `pilartoto` is still not recovered because the current title evidence is not clean enough
- the full benign root already proves that `toto/togel` host tokens alone are noisy, so this rule should not be broadened casually
- the reproducible benign baseline still appears to drift relative to some earlier thread-local numbers, which is why this handoff emphasizes direct incremental reason-code effect

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`
- `docs/handoff/2026-04-15_gambling_low_cost_toto_togel_host_recovery.md`

Doc debt still remaining:

- `L0_DESIGN_V1.md` does not yet document `gambling_toto_togel_host_recovery`
- evaluation determinism still needs a dedicated cleanup task

---

## 9. Recommended Next Step

- if recall work continues, the next task should be:
  - `gambling low-cost pilartoto-style title clarification`
  - or `gambling low-cost vietnamese title-token recovery`
- if engineering quality comes first, the next task should still be:
  - `gambling evaluation determinism check`
