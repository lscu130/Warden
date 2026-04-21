# Handoff Metadata

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若精确字段、路径、命令、兼容性结论有冲突，以英文版为准。

- Handoff ID: `2026-04-17-adult-remaining-benign-hit-split`
- Related Task ID: `TASK-L0-2026-04-17-ADULT-REMAINING-BENIGN-HIT-SPLIT`
- Task Title: `拆分 adult 剩余 benign 命中样本`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-17`
- Status: `DONE`

---

## 1. Executive Summary

这次交付没有改代码，只把当前 `adult` 收紧后 ordinary benign 池里剩余的 `144` 个 `possible_adult_lure` 命中拆成了两份：

- `likely screening miss / pool contamination`: `78`
- `true rule false positive`: `66`

当前分桶依据是低成本、可审计的 triage 规则：

- 命中高置信 adult 词
- 命中非弱化的 adult URL 词
- 或强 adult 文本密度明显过高

则归入更像“初筛漏掉的成人页 / 数据池污染”；其余归入更像“当前规则仍然带出来的真噪音页”。

这次分桶是 triage split，不是人工 gold label。

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- updated `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- added `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- none

### Output / Artifact Changes

- produced one `likely screening miss / pool contamination` bucket
- produced one `true rule false positive` bucket
- documented representative examples and full sample-name lists in this handoff

---

## 3. Files Touched

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task is analysis-only and does not change runtime behavior
- future adult precision work can now separate likely data-pool contamination from rule noise

### Preserved Behavior

- no adult trigger logic changed
- no `gambling` or `gate` logic changed
- no CLI, schema, or output structure changed

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
- `matched_keywords.adult_text`
- `matched_keywords.adult_url`

Compatibility notes:

This task only classifies current samples into two triage buckets. No runtime field, schema, or interface changed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- extract the current remaining ordinary-benign `possible_adult_lure` hits
- rank them by strong adult evidence density
- split them into:
  - `likely screening miss / pool contamination`
  - `true rule false positive`
```

### Result

- remaining ordinary-benign adult hits after the latest adult tightening: `144`
- bucket counts:
  - `likely screening miss / pool contamination`: `78`
  - `true rule false positive`: `66`

Current split heuristic:

- put a sample into `likely screening miss / pool contamination` if any of the following is true:
  - it contains at least one high-confidence adult token
  - it contains at least one non-weak adult URL token
  - it contains at least 5 strong adult text hits
  - it contains at least 4 strong adult text hits and also has age-gate support
- otherwise, put it into `true rule false positive`

Representative `likely screening miss / pool contamination` examples:

- `91porna.com_20260327T063219Z`
- `fuckmoral.com_20260401T082010Z`
- `hugesex.tv_20260403T021827Z`
- `theporndude.vip_20260416T053656Z`
- `bestpornsites.tv_20260407T120048Z`
- `faphouse.tv_20260325T031305Z`
- `hindiporn.rodeo_20260410T044541Z`
- `cartoonporn.pro_20260401T125444Z`

Representative `true rule false positive` examples:

- `androidrus.ru_20260325T175430Z`
- `anishcollegehyd.org_20260327T053616Z`
- `atsu.moe_20260403T034930Z`
- `bdsmsutra.com_20260414T080514Z`
- `besthookupswebsites.com_20260416T012037Z`
- `osnews.com_20260401T143628Z`
- `thepleasurechest.com_20260407T133920Z`
- `telegramlinksgroup.xyz_20260326T202732Z`

### Not Run

- any runtime patch
- any adult metric rerun beyond the current remaining-hit split
- any manual human review

Reason:

This task was scoped to split the current remaining hits only.

---

## 7. Risks / Caveats

- this split is heuristic triage, not human gold labeling
- some samples in the `likely screening miss` bucket can still be borderline, especially when the domain looks adult-like but the current artifact is sparse
- some samples in the `true rule false positive` bucket may still be weak adult pages; they only look less certain under the current low-cost evidence

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- use the `likely screening miss / pool contamination` bucket to clean the benign pool first
- use the `true rule false positive` bucket as the next target for adult precision tightening
- if human review time is available, spot-check the top 20 samples in each bucket before using the split as a hard cleanup source

## 10. Bucket Lists

### 10.1 Likely Screening Miss / Pool Contamination (`78`)

- `91porna.com_20260327T063219Z`
- `fuckmoral.com_20260401T082010Z`
- `hugesex.tv_20260403T021827Z`
- `tophdsex.com_20260415T133649Z`
- `faphouse.tv_20260325T031305Z`
- `hindiporn.rodeo_20260410T044541Z`
- `mon-bouledogue.com_20260330T110932Z`
- `theporndude.vip_20260416T053656Z`
- `cartoonporn.pro_20260401T125444Z`
- `fantasyasianp.com_20260330T080845Z`
- `horseporntube.fun_20260326T154155Z`
- `javmov.com_20260413T020513Z`
- `pornproxy.art_20260415T095008Z`
- `amatori.info_20260330T081827Z`
- `crazysexstory.com_20260414T070400Z`
- `kandavideos.com_20260416T010826Z`
- `desifakes.com_20260327T092532Z`
- `pervtube.net_20260325T143527Z`
- `qbm281.com_20260413T025249Z`
- `xxxn.onl_20260415T044257Z`
- `kanhuji.com_20260402T171537Z`
- `kanhuji.com_20260410T032923Z`
- `arabx.tv_20260327T093354Z`
- `arbnaar.com_20260327T053245Z`
- `hentailoop.com_20260407T070558Z`
- `thebongacams.com_20260330T092814Z`
- `av-wiki.net_20260327T092211Z`
- `maxsiu.com_20260413T014412Z`
- `mxseries.com.co_20260414T071214Z`
- `stripol.com_20260330T110545Z`
- `zettai-ero.com_20260414T070922Z`
- `zone-mp3.com_20260325T153832Z`
- `101.ru_20260327T075659Z`
- `24pdd.kz_20260326T181105Z`
- `amyelise.net_20260416T024955Z`
- `babyplan.ru_20260416T052916Z`
- `cyberleninka.ru_20260327T073309Z`
- `dzen.ru_20260327T010123Z`
- `eborus.top_20260330T072834Z`
- `erokan.net_20260415T145745Z`
- `girla.me_20260415T121623Z`
- `ixbt.com_20260327T015030Z`
- `lb.ua_20260326T094619Z`
- `lenta.ru_20260327T031729Z`
- `massaggioit.com_20260330T023935Z`
- `mostbet94620.help_20260413T030336Z`
- `pravdaurfo.ru_20260416T045407Z`
- `sexchatters.com_20260325T082015Z`
- `siza.tv_20260330T101953Z`
- `terfit.ru_20260415T040038Z`
- `xn--hhr917d3fecva.xyz_20260416T023156Z`
- `yadongred1.org_20260403T082921Z`
- `bestpornsites.tv_20260407T120048Z`
- `glam0ur.net_20260402T120605Z`
- `iceporn.tube_20260416T023717Z`
- `s-forum.biz_20260402T114102Z`
- `smokinmovies.com_20260326T144147Z`
- `prehistorictube.com_20260330T085831Z`
- `videosz.com_20260408T083407Z`
- `dadyporn.mobi_20260330T072606Z`
- `privatehomeclips.com_20260327T083241Z`
- `txxx.com_20260326T024624Z`
- `usbxh.life_20260326T105459Z`
- `xfantazy.org_20260325T112452Z`
- `xhinvestments.world_20260410T053936Z`
- `cuckold69.com_20260403T074132Z`
- `ersties.com_20260325T114913Z`
- `lemmecheck.com_20260403T090502Z`
- `lesbian8.com_20260408T074913Z`
- `turkifsalar6.space_20260413T010717Z`
- `adultgameson.com_20260330T061956Z`
- `babeuniversum.com_20260402T133814Z`
- `damplips.com_20260327T082537Z`
- `giantessa.net_20260414T113844Z`
- `xmissy.nl_20260325T144940Z`
- `xxxcom.cam_20260413T012127Z`
- `newanonib.com_20260414T113814Z`
- `nudeindians2.net_20260326T053011Z`

### 10.2 True Rule False Positive (`66`)

- `androidrus.ru_20260325T175430Z`
- `anishcollegehyd.org_20260327T053616Z`
- `atsu.moe_20260403T034930Z`
- `bdsmsutra.com_20260414T080514Z`
- `besthookupswebsites.com_20260416T012037Z`
- `clubsextury21.com_20260326T074954Z`
- `cuckold.net_20260326T073710Z`
- `escortaccess.net_20260414T130907Z`
- `familydogs.cz_20260325T131823Z`
- `hobbyladies.de_20260413T031928Z`
- `ladyxena.com_20260326T052927Z`
- `mlivevip.com_20260416T011649Z`
- `motosvet.com_20260326T172622Z`
- `mtp88.com_20260325T182632Z`
- `mundosexanuncio.com_20260325T093147Z`
- `net9ja.com.ng_20260326T073302Z`
- `nonshy.com_20260415T090200Z`
- `osnews.com_20260401T143628Z`
- `pincobet.top_20260413T015429Z`
- `rosstab.com_20260403T064335Z`
- `sexwanderer.com_20260325T171821Z`
- `telegramlinksgroup.xyz_20260326T202732Z`
- `tellyquelz.com_20260415T145934Z`
- `thepleasurechest.com_20260407T133920Z`
- `tkor099.com_20260402T064706Z`
- `tkor099.com_20260408T071703Z`
- `torrentdownloads.pro_20260326T084350Z`
- `uptodater.net_20260403T084914Z`
- `wilfmovies.com_20260413T102700Z`
- `wowgirls.com_20260416T051339Z`
- `badassdownloader.com_20260325T164642Z`
- `blikk.hu_20260401T083500Z`
- `cduniverse.com_20260403T022648Z`
- `cloudns.uk_20260326T092408Z`
- `cupidbaba.com_20260407T143450Z`
- `darazcenter.pk_20260326T185325Z`
- `engadget.com_20260327T022541Z`
- `familystrokes.com_20260415T103220Z`
- `hookupplan.com_20260413T032218Z`
- `hugepornhole.com_20260413T045432Z`
- `kodpornx.com_20260402T063235Z`
- `krx18.com_20260401T092332Z`
- `lovehub.com_20260415T123726Z`
- `mandygirls.com_20260330T083330Z`
- `mangakakalot.gg_20260326T041317Z`
- `manganato.gg_20260325T094010Z`
- `moreshemales.com_20260330T035104Z`
- `natomanga.com_20260326T041309Z`
- `pharmgf.online_20260414T124043Z`
- `redquill.net_20260414T071258Z`
- `reru.ac.th_20260402T193153Z`
- `simply-adult.com_20260402T165301Z`
- `simply-adult.com_20260410T030426Z`
- `swingersplein.nl_20260330T103222Z`
- `thefappeningblog.com_20260401T125133Z`
- `xchat.cz_20260413T101540Z`
- `zygrib.org_20260407T120548Z`
- `brazzers.com_20260326T084639Z`
- `gostosavip.com_20260330T035745Z`
- `hdporncomics.com_20260327T030126Z`
- `ladyboygold.com_20260402T135333Z`
- `nic.xxx_20260402T090003Z`
- `phimxxx.ai_20260327T021140Z`
- `yfm307.com_20260330T074527Z`
- `247pantyhose.com_20260402T110647Z`
- `eroticity.net_20260416T052003Z`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: `2026-04-17-adult-remaining-benign-hit-split`
- Related Task ID: `TASK-L0-2026-04-17-ADULT-REMAINING-BENIGN-HIT-SPLIT`
- Task Title: `Split the remaining benign adult hits into two handling buckets`
- Module: `Inference`
- Author: `Codex`
- Date: `2026-04-17`
- Status: `DONE`

---

## 1. Executive Summary

This delivery did not change code. It split the current `144` remaining ordinary-benign `possible_adult_lure` hits into two handling buckets:

- `likely screening miss / pool contamination`: `78`
- `true rule false positive`: `66`

The split uses an auditable low-cost triage rule:

- if a sample has high-confidence adult tokens
- or non-weak adult URL hits
- or clearly high strong-adult-text density

then it is placed into the more likely `screening miss / pool contamination` bucket; otherwise it is placed into the more likely `true rule false positive` bucket.

This is a triage split, not human gold labeling.

---

## 2. What Changed

### Code Changes

- none
- none
- none

### Doc Changes

- updated `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- added `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- none

### Output / Artifact Changes

- produced one `likely screening miss / pool contamination` bucket
- produced one `true rule false positive` bucket
- documented representative examples and full sample-name lists in this handoff

---

## 3. Files Touched

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

---

## 4. Behavior Impact

### Expected New Behavior

- none
- this task is analysis-only and does not change runtime behavior
- future adult precision work can now separate likely data-pool contamination from rule noise

### Preserved Behavior

- no adult trigger logic changed
- no `gambling` or `gate` logic changed
- no CLI, schema, or output structure changed

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
- `matched_keywords.adult_text`
- `matched_keywords.adult_url`

Compatibility notes:

This task only classifies current samples into two triage buckets. No runtime field, schema, or interface changed.

---

## 6. Validation Performed

### Commands Run

```bash
PowerShell inline Python:
- extract the current remaining ordinary-benign `possible_adult_lure` hits
- rank them by strong adult evidence density
- split them into:
  - `likely screening miss / pool contamination`
  - `true rule false positive`
```

### Result

- remaining ordinary-benign adult hits after the latest adult tightening: `144`
- bucket counts:
  - `likely screening miss / pool contamination`: `78`
  - `true rule false positive`: `66`

Current split heuristic:

- put a sample into `likely screening miss / pool contamination` if any of the following is true:
  - it contains at least one high-confidence adult token
  - it contains at least one non-weak adult URL token
  - it contains at least 5 strong adult text hits
  - it contains at least 4 strong adult text hits and also has age-gate support
- otherwise, put it into `true rule false positive`

Representative `likely screening miss / pool contamination` examples:

- `91porna.com_20260327T063219Z`
- `fuckmoral.com_20260401T082010Z`
- `hugesex.tv_20260403T021827Z`
- `theporndude.vip_20260416T053656Z`
- `bestpornsites.tv_20260407T120048Z`
- `faphouse.tv_20260325T031305Z`
- `hindiporn.rodeo_20260410T044541Z`
- `cartoonporn.pro_20260401T125444Z`

Representative `true rule false positive` examples:

- `androidrus.ru_20260325T175430Z`
- `anishcollegehyd.org_20260327T053616Z`
- `atsu.moe_20260403T034930Z`
- `bdsmsutra.com_20260414T080514Z`
- `besthookupswebsites.com_20260416T012037Z`
- `osnews.com_20260401T143628Z`
- `thepleasurechest.com_20260407T133920Z`
- `telegramlinksgroup.xyz_20260326T202732Z`

### Not Run

- any runtime patch
- any adult metric rerun beyond the current remaining-hit split
- any manual human review

Reason:

This task was scoped to split the current remaining hits only.

---

## 7. Risks / Caveats

- this split is heuristic triage, not human gold labeling
- some samples in the `likely screening miss` bucket can still be borderline, especially when the domain looks adult-like but the current artifact is sparse
- some samples in the `true rule false positive` bucket may still be weak adult pages; they only look less certain under the current low-cost evidence

---

## 8. Docs Impact

- Docs updated: `YES`

Docs touched:

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

Doc debt still remaining:

- `none`

---

## 9. Recommended Next Step

- use the `likely screening miss / pool contamination` bucket to clean the benign pool first
- use the `true rule false positive` bucket as the next target for adult precision tightening
- if human review time is available, spot-check the top 20 samples in each bucket before using the split as a hard cleanup source
