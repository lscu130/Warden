# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-20-adult-moved55-spotcheck-and-lost44-review`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-MOVED55-SPOTCHECK-AND-LOST44-REVIEW`
- Task Title: `复核 moved 55 样本质量并审查 lost 44 adult 样本`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

这次交付没有改代码，也没有再移动样本。它做了两件事：

- 对上一条任务里 moved 的 `55` 个 contamination samples 做 focused spot-check；
- 专门看 stricter adult rule 下掉出去的 adult 样本，判断是否值得 reopen recall recovery。

当前结论：

- moved `55` 的方向整体是对的，但质量不是全干净；
- 里面有一批明显应该移走的成人站 / 成人服务页；
- 也混着少量更像“普通内容页提到成人话题”的过移样本；
- 掉出去的 adult 样本主力是低支撑的 `1-2 strong token` 页面；
- 我不建议直接整体回收这批 dropped samples；
- 如果要做 recall recovery，只建议开一条非常窄的 adult-domain recovery。

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- added `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- added `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- updated task status in `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md` to `DONE`

### Output / Artifact Changes

- produced a focused quality review of the moved `55` samples
- produced a dropped-pattern review for the lost adult samples
- produced a recommendation on whether narrow recall recovery is justified

---

## 3. Files Touched

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

Optional notes per file:

- this task is analysis-only
- no code was patched
- no dataset directories were moved

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task only adds a clearer quality read on the prior adult cleanup / tightening outcome
- future adult recall-recovery decisions now have a sharper evidence base

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

- `none`
- `none`
- `none`

Compatibility notes:

This task only reviews the prior results. No runtime interface, schema field, CLI, or output structure changed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell:
- inspect sample directory structure for representative moved samples
- read `auto_labels.json`, `meta.json`, `url.json`, and `visible_text.txt` for a focused moved-sample set
- review moved-sample evidence for:
  - title
  - final URL
  - adult matched keywords
  - age-gate hits
  - visible-text head

PowerShell inline Python:
- categorize dropped adult samples by old-rule vs new-rule mismatch
- summarize dominant lost-pattern buckets
```

### Result

Focused moved-sample spot-check set:

- `brazzers.com_20260326T084639Z`
- `theporndude.com_20260416T115045Z`
- `pornpics.com_20260416T074136Z`
- `bestxnxxvideos.com_20260417T020752Z`
- `hookupplan.com_20260413T032218Z`
- `osnews.com_20260401T143628Z`
- `engadget.com_20260327T022541Z`
- `androidrus.ru_20260325T175430Z`
- `cduniverse.com_20260403T022648Z`
- `wowgirls.com_20260416T051339Z`
- `redquill.net_20260414T071258Z`
- `nonshy.com_20260415T090200Z`

Spot-check judgment summary:

- clearly directionally correct moves:
  - `brazzers.com`
  - `theporndude.com`
  - `pornpics.com`
  - `bestxnxxvideos.com`
  - `cduniverse.com`
  - `wowgirls.com`
  - `redquill.net`
  - `nonshy.com`
- plausible / borderline moves:
  - `hookupplan.com`
    - looks more like adult-adjacent casual hookup / dating, not classic porn content
- likely over-moved or at least not clean contamination removals:
  - `osnews.com`
  - `engadget.com`
  - `androidrus.ru`
    - these look more like ordinary content pages where adult wording appears inside article or catalog text, not adult-pool contamination in the same sense as porn sites

Practical quality read on moved `55`:

- the bucket is directionally useful
- the bucket is not pure
- there is enough evidence that a subset of moved samples are clear contamination
- there is also enough evidence that some moved samples are just topical false positives rather than samples that obviously belong outside the benign pool

Dropped-adult review:

- the prior task reported `44` dropped adult samples under the stricter rule
- a strict current re-derivation over the adult root using old-rule vs new-rule mismatch reconstructed `38` unequivocal drops
- this discrepancy indicates some boundary sensitivity in how the dropped set is reconstructed, but the dominant pattern mix is stable

Dominant reconstructed drop patterns:

- `two_strong_tokens_no_domain_no_age`: `21`
- `single_strong_token_only`: `11`
- `single_strong_token_with_domain_only`: `6`

Representative dropped examples:

- `single_strong_token_only`
  - `123av.com_20260401T080704Z` -> `jav + av`
  - `osnews.com_20260401T143628Z` -> `porn + av`
  - `pururin.me_20260402T125050Z` -> `hentai + nude`
- `single_strong_token_with_domain_only`
  - `avxxxmini.com_20260408T071508Z`
  - `njav.org_20260414T082227Z`
  - `sextrungquoc69.blog_20260414T082621Z`
- `two_strong_tokens_no_domain_no_age`
  - `cached.cyou_20260330T030347Z` -> `xxx + sex video`
  - `castaway.org.uk_20260403T082215Z` -> `xxx + jav`
  - `engadget.com_20260327T022541Z` -> `pornhub + adult content`
  - `gaymenring.com_20260407T070759Z` -> `porn + bdsm`

Interpretation:

- the stricter rule is mostly dropping pages that do not have enough support beyond `1-2` strong adult tokens
- many of those dropped pages still look adult-like
- but they also fit the exact risk the new precision-first rule was designed to suppress on generic or weakly supported hosts

### Not Run

- no runtime patch
- no manual review of all `55` moved samples
- no new recall-recovery implementation

Reason:

This task was explicitly scoped to review and recommendation only.

---

## 7. Risks / Caveats

- the moved-55 review is a focused spot-check, not a complete human re-label of all `55`
- the lost-adult review has a boundary discrepancy: prior task summary said `44`, strict current recomputation reconstructed `38` unequivocal drops
- because of that discrepancy, the review should be treated as a pattern-level decision aid, not as a mathematically final count for publication

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- do not reopen a broad adult recall recovery
- if recall recovery is reopened at all, make it a very narrow adult-domain recovery for pages with:
  - `single_strong_token_with_domain_only`
  - or a very small hand-reviewed subset of `two_strong_tokens_no_domain_no_age`
- if moved-sample purity matters for evaluation, run a second human review pass on the clearly ambiguous moved samples such as `osnews.com`, `engadget.com`, and `androidrus.ru`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-20-adult-moved55-spotcheck-and-lost44-review`
- Related Task ID: `TASK-L0-2026-04-20-ADULT-MOVED55-SPOTCHECK-AND-LOST44-REVIEW`
- Task Title: `Review moved-55 sample quality and inspect the lost-44 adult samples`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-20`
- Status: `DONE`

---

## 1. Executive Summary

This delivery did not change code or move more samples. It did two things:

- run a focused spot-check over the `55` moved contamination samples from the prior adult task;
- inspect the adult samples that dropped out under the stricter adult rule and judge whether a recall-recovery task should be reopened.

Current conclusion:

- the moved-55 bucket is directionally useful, but it is not fully clean;
- a substantial part of it clearly should have been moved out as adult contamination;
- it also contains a smaller set of pages that look more like ordinary content pages discussing or listing adult topics;
- the dropped adult samples are dominated by low-support `1-2` strong-token pages;
- I do not recommend reopening a broad recall recovery;
- if recovery is reopened at all, it should be a very narrow adult-domain recovery only.

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- added `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- added `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- updated task status in `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md` to `DONE`

### Output / Artifact Changes

- produced a focused quality review of the moved `55` samples
- produced a dropped-pattern review for the lost adult samples
- produced a recommendation on whether narrow recall recovery is justified

---

## 3. Files Touched

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

Optional notes per file:

- this task is analysis-only
- no code was patched
- no dataset directories were moved

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task only adds a clearer quality read on the prior adult cleanup / tightening outcome
- future adult recall-recovery decisions now have a sharper evidence base

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

- `none`
- `none`
- `none`

Compatibility notes:

This task only reviews the prior results. No runtime interface, schema field, CLI, or output structure changed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell:
- inspect sample directory structure for representative moved samples
- read `auto_labels.json`, `meta.json`, `url.json`, and `visible_text.txt` for a focused moved-sample set
- review moved-sample evidence for:
  - title
  - final URL
  - adult matched keywords
  - age-gate hits
  - visible-text head

PowerShell inline Python:
- categorize dropped adult samples by old-rule vs new-rule mismatch
- summarize dominant lost-pattern buckets
```

### Result

Focused moved-sample spot-check set:

- `brazzers.com_20260326T084639Z`
- `theporndude.com_20260416T115045Z`
- `pornpics.com_20260416T074136Z`
- `bestxnxxvideos.com_20260417T020752Z`
- `hookupplan.com_20260413T032218Z`
- `osnews.com_20260401T143628Z`
- `engadget.com_20260327T022541Z`
- `androidrus.ru_20260325T175430Z`
- `cduniverse.com_20260403T022648Z`
- `wowgirls.com_20260416T051339Z`
- `redquill.net_20260414T071258Z`
- `nonshy.com_20260415T090200Z`

Spot-check judgment summary:

- clearly directionally correct moves:
  - `brazzers.com`
  - `theporndude.com`
  - `pornpics.com`
  - `bestxnxxvideos.com`
  - `cduniverse.com`
  - `wowgirls.com`
  - `redquill.net`
  - `nonshy.com`
- plausible / borderline moves:
  - `hookupplan.com`
    - more adult-adjacent hookup / dating than classic porn content
- likely over-moved or at least not clean contamination removals:
  - `osnews.com`
  - `engadget.com`
  - `androidrus.ru`
    - these look more like ordinary content pages where adult wording appears inside article or catalog text, not adult-pool contamination in the same sense as porn sites

Practical quality read on moved `55`:

- the bucket is directionally useful
- the bucket is not pure
- there is enough evidence that a subset of moved samples are clear contamination
- there is also enough evidence that some moved samples are topical false positives rather than samples that obviously belong outside the benign pool

Dropped-adult review:

- the prior task reported `44` dropped adult samples under the stricter rule
- a strict current re-derivation over the adult root using old-rule vs new-rule mismatch reconstructed `38` unequivocal drops
- this discrepancy indicates some boundary sensitivity in how the dropped set is reconstructed, but the dominant pattern mix is stable

Dominant reconstructed drop patterns:

- `two_strong_tokens_no_domain_no_age`: `21`
- `single_strong_token_only`: `11`
- `single_strong_token_with_domain_only`: `6`

Representative dropped examples:

- `single_strong_token_only`
  - `123av.com_20260401T080704Z` -> `jav + av`
  - `osnews.com_20260401T143628Z` -> `porn + av`
  - `pururin.me_20260402T125050Z` -> `hentai + nude`
- `single_strong_token_with_domain_only`
  - `avxxxmini.com_20260408T071508Z`
  - `njav.org_20260414T082227Z`
  - `sextrungquoc69.blog_20260414T082621Z`
- `two_strong_tokens_no_domain_no_age`
  - `cached.cyou_20260330T030347Z` -> `xxx + sex video`
  - `castaway.org.uk_20260403T082215Z` -> `xxx + jav`
  - `engadget.com_20260327T022541Z` -> `pornhub + adult content`
  - `gaymenring.com_20260407T070759Z` -> `porn + bdsm`

Interpretation:

- the stricter rule is mostly dropping pages that do not have enough support beyond `1-2` strong adult tokens
- many of those dropped pages still look adult-like
- they also fit the exact risk that the new precision-first rule was designed to suppress on generic or weakly supported hosts

### Not Run

- no runtime patch
- no manual review of all `55` moved samples
- no new recall-recovery implementation

Reason:

This task was explicitly scoped to review and recommendation only.

---

## 7. Risks / Caveats

- the moved-55 review is a focused spot-check, not a complete human relabel of all `55`
- the lost-adult review has a boundary discrepancy: the prior task summary said `44`, while strict current recomputation reconstructed `38` unequivocal drops
- because of that discrepancy, this review should be treated as a pattern-level decision aid, not as a publication-grade final count

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- do not reopen a broad adult recall recovery
- if recall recovery is reopened at all, make it a very narrow adult-domain recovery for pages with:
  - `single_strong_token_with_domain_only`
  - or a very small hand-reviewed subset of `two_strong_tokens_no_domain_no_age`
- if moved-sample purity matters for evaluation, run a second human review pass on the clearly ambiguous moved samples such as `osnews.com`, `engadget.com`, and `androidrus.ru`
