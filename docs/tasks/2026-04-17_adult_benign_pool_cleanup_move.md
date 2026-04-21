# Adult benign-pool cleanup move task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于清理当前 `ordinary benign` 池里被上一条 triage 明确归为 `likely screening miss / pool contamination` 的 `78` 个样本。
- 本任务只做数据池移动，不做规则调参，不做 schema / CLI / 输出变更。
- 默认把样本从 `E:\Warden\data\raw\benign\benign` 移到 `E:\Warden\data\raw\benign\hard benign\adult`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-17-ADULT-BENIGN-POOL-CLEANUP-MOVE`
- 任务标题：`清理 adult likely contamination 样本出 ordinary benign 池`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Data`
- 相关文档：`AGENTS.md`；`docs/workflow/GPT_CODEX_WORKFLOW.md`；`docs/templates/TASK_TEMPLATE.md`；`docs/templates/HANDOFF_TEMPLATE.md`；`docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- 创建日期：`2026-04-17`
- 提出人：`User`

## 1. 背景

上一条 adult 剩余 benign 命中拆分任务，把当前 `ordinary benign` 里剩余的 `144` 个 `possible_adult_lure` 命中拆成两份：

- `likely screening miss / pool contamination`: `78`
- `true rule false positive`: `66`

这次只处理前一份。目标是把这 `78` 个更像成人站 / 成人聚合页 / 初筛漏检页的样本移出 `ordinary benign`，避免继续污染 benign 池。

## 2. 目标

把上一条 split handoff 中列出的 `78` 个 `likely screening miss / pool contamination` 样本，从 `E:\Warden\data\raw\benign\benign` 移动到 `E:\Warden\data\raw\benign\hard benign\adult`，并记录这次数据池清理的实际移动结果、验证结果和兼容性结论。

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\data\raw\benign\benign\<sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<sample_dirs>`
- `docs/tasks/2026-04-17_adult_benign_pool_cleanup_move.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

This task is allowed to change:

- sample directory location for the approved 78-sample cleanup list
- task / handoff documentation for this cleanup
- none

## 4. Scope Out

This task must NOT do the following:

- modify any labeling or inference code
- retune `adult`, `gambling`, or `gate` rules
- rename files, schema fields, or CLI flags
- delete sample content
- move any sample outside the approved 78-sample list

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Code / Scripts

- none
- none
- none

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- the `10.1 Likely Screening Miss / Pool Contamination (78)` list from `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Prior Handoff

- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a repo task doc for this cleanup move
- the actual relocation of the approved 78 sample directories
- a validation summary showing source/destination counts after the move
- a repo handoff document

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- move only the approved 78 sample directories
- keep all moves inside `E:\Warden\data\raw\benign`
- do not overwrite destination directories silently
- treat this as data-pool cleanup, not relabeling logic redesign

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current labeling schema
- current runtime outputs
- current CLI and scripts

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `none`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current sample-dir labeling flow
  - current adult evaluation snippets
  - current downstream readers of existing manifests and metadata

Downstream consumers to watch:

- future benign-pool sampling
- future adult precision evaluation

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the exact 78-sample list from the prior split handoff
- verify source paths and destination root before moving
- validate that no sample outside the approved list was moved

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] all 78 approved sample directories were verified before the move
- [x] the approved sample directories now live under `hard benign\adult`
- [x] the approved sample directories no longer remain under `benign`
- [x] no code, schema, or CLI change was mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [x] source existence check for the approved 78 samples
- [x] destination non-conflict check
- [x] post-move existence check under `hard benign\adult`
- [x] repo handoff produced

Commands to run if applicable:

```bash
PowerShell:
- verify the 78 source directories exist under `E:\Warden\data\raw\benign\benign`
- move them to `E:\Warden\data\raw\benign\hard benign\adult`
- verify the source is empty for those samples and destination contains all moved samples
```

Expected evidence to capture:

- count of approved source samples found before the move
- count of destination samples present after the move
- count of missing or conflicting paths, if any

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-17-ADULT-BENIGN-POOL-CLEANUP-MOVE`
- Task Title: `Move likely adult contamination samples out of the ordinary benign pool`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Data`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- Created At: `2026-04-17`
- Requested By: `User`

Use this task to clean the ordinary-benign pool by relocating the `78` samples that were already triaged as `likely screening miss / pool contamination` in the prior adult remaining-hit split.

## 1. Background

The previous adult remaining-benign-hit split task divided the current `144` remaining ordinary-benign `possible_adult_lure` hits into two buckets:

- `likely screening miss / pool contamination`: `78`
- `true rule false positive`: `66`

This task only handles the first bucket. The goal is to remove those `78` samples, which look more like adult sites, adult aggregators, or earlier screening misses, from the ordinary-benign pool so they stop contaminating benign-side evaluation.

## 2. Goal

Move the `78` samples listed under `10.1 Likely Screening Miss / Pool Contamination (78)` in `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md` from `E:\Warden\data\raw\benign\benign` to `E:\Warden\data\raw\benign\hard benign\adult`, then record the actual move result, validation result, and compatibility impact for this pool-cleanup action.

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\data\raw\benign\benign\<sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<sample_dirs>`
- `docs/tasks/2026-04-17_adult_benign_pool_cleanup_move.md`
- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

This task is allowed to change:

- sample directory location for the approved 78-sample cleanup list
- task / handoff documentation for this cleanup
- none

## 4. Scope Out

This task must NOT do the following:

- modify any labeling or inference code
- retune `adult`, `gambling`, or `gate` rules
- rename files, schema fields, or CLI flags
- delete sample content
- move any sample outside the approved 78-sample list

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Code / Scripts

- none
- none
- none

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- the `10.1 Likely Screening Miss / Pool Contamination (78)` list from `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Prior Handoff

- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a repo task doc for this cleanup move
- the actual relocation of the approved 78 sample directories
- a validation summary showing source/destination counts after the move
- a repo handoff document

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- move only the approved 78 sample directories
- keep all moves inside `E:\Warden\data\raw\benign`
- do not overwrite destination directories silently
- treat this as data-pool cleanup, not relabeling logic redesign

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current labeling schema
- current runtime outputs
- current CLI and scripts

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `none`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current sample-dir labeling flow
  - current adult evaluation snippets
  - current downstream readers of existing manifests and metadata

Downstream consumers to watch:

- future benign-pool sampling
- future adult precision evaluation

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the exact 78-sample list from the prior split handoff
- verify source paths and destination root before moving
- validate that no sample outside the approved list was moved

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] all 78 approved sample directories were verified before the move
- [ ] the approved sample directories now live under `hard benign\adult`
- [ ] the approved sample directories no longer remain under `benign`
- [ ] no code, schema, or CLI change was mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [ ] source existence check for the approved 78 samples
- [ ] destination non-conflict check
- [ ] post-move existence check under `hard benign\adult`
- [ ] repo handoff produced

Commands to run if applicable:

```bash
PowerShell:
- verify the 78 source directories exist under `E:\Warden\data\raw\benign\benign`
- move them to `E:\Warden\data\raw\benign\hard benign\adult`
- verify the source is empty for those samples and destination contains all moved samples
```

Expected evidence to capture:

- count of approved source samples found before the move
- count of destination samples present after the move
- count of missing or conflicting paths, if any

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-17_adult_benign_pool_cleanup_move.md`

## 13. Open Questions / Blocking Issues

- none
