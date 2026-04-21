# Adult remaining benign-hit split task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前 `adult` 收紧后仍然留在 ordinary benign 池里的命中样本分成两份：
  - `likely screening miss / pool contamination`
  - `true rule false positive`
- 本任务重点是分桶和交付清单，不继续改成人规则。
- 本任务默认遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-17-ADULT-REMAINING-BENIGN-HIT-SPLIT`
- 任务标题：`拆分 adult 剩余 benign 命中样本`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`
- 创建日期：`2026-04-17`
- 提出人：`用户`

## 1. 背景

在 `adult false-positive tightening` 之后，ordinary benign 池上的 `possible_adult_lure` 已从 `182` 压到 `144`。  
这 `144` 个剩余命中里混着两类东西：

- 看起来像初筛漏进 ordinary benign 池的成人站或成人聚合页
- 真正由当前规则仍然带出来的噪音页

如果不把这两类拆开，后续的 precision 判断和进一步调规则都会失真。

## 2. 目标

从当前剩余的 `144` 个 ordinary-benign adult hits 中，显式拆出两份样本清单：

- `likely screening miss / pool contamination`
- `true rule false positive`

并给出当前分桶依据，让后续能分别走数据池修正或规则继续收紧两条路径。

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

This task is allowed to change:

- task / handoff docs
- repo-facing triage split content inside the handoff
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue adult tuning
- modify `gambling` / `gate`
- add dependencies
- change CLI or schema

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current remaining ordinary-benign `possible_adult_lure` hits after the latest adult-tightening patch
- matched-keyword output from `specialized_surface_signals`
- none

### Prior Handoff

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one explicit `likely screening miss / pool contamination` list
- one explicit `true rule false positive` list
- a short explanation of the split heuristics
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

- do not patch rules in this task
- keep the split auditable from current matched keywords and sample names
- state clearly that this is a triage split, not human gold labeling

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`
  - current adult evaluation snippets

Downstream consumers to watch:

- future adult precision analysis
- future benign-pool cleanup work

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the current tightened adult outputs
- rank likely pool contamination by strong adult evidence density
- keep clearly weak/noisy pages in the true-rule-false-positive bucket

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

- [ ] the remaining adult hits are split into two explicit lists
- [ ] the split rationale is documented
- [ ] no code or schema changes are mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [ ] remaining-hit extraction
- [ ] bucket split review
- [ ] handoff produced
- [ ] final summary reflects the two-bucket split

Commands to run if applicable:

```bash
python - <<'PY'
# extract remaining benign adult hits and split them into two buckets
PY
```

Expected evidence to capture:

- count of remaining hits
- bucket counts
- representative samples per bucket

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

- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-17-ADULT-REMAINING-BENIGN-HIT-SPLIT`
- Task Title: `Split the remaining benign adult hits into two handling buckets`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`
- Created At: `2026-04-17`
- Requested By: `User`

Use this task to split the current remaining ordinary-benign `adult` hits into two explicit buckets:

- `likely screening miss / pool contamination`
- `true rule false positive`

## 1. Background

After the latest `adult false-positive tightening`, ordinary-benign `possible_adult_lure` hits dropped from `182` to `144`.

Those `144` remaining hits contain two different populations:

- pages that look like adult sites or adult aggregators that likely slipped into the ordinary-benign pool during earlier screening
- pages that still look like genuine rule noise under the current strategy

If those two populations are not separated, later precision analysis and further rule tuning will stay distorted.

## 2. Goal

Produce two explicit lists from the current remaining `144` ordinary-benign adult hits:

- `likely screening miss / pool contamination`
- `true rule false positive`

and document the split rationale so that follow-up work can separately address data-pool cleanup versus further rule tightening.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

This task is allowed to change:

- task / handoff docs
- repo-facing triage split content inside the handoff
- none

## 4. Scope Out

This task must NOT do the following:

- modify `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- continue adult tuning
- modify `gambling` / `gate`
- add dependencies
- change CLI or schema

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- current remaining ordinary-benign `possible_adult_lure` hits after the latest adult-tightening patch
- matched-keyword output from `specialized_surface_signals`
- none

### Prior Handoff

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one explicit `likely screening miss / pool contamination` list
- one explicit `true rule false positive` list
- a short explanation of the split heuristics
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

- do not patch rules in this task
- keep the split auditable from current matched keywords and sample names
- state clearly that this is a triage split, not human gold labeling

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `matched_keywords`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`
  - current adult evaluation snippets

Downstream consumers to watch:

- future adult precision analysis
- future benign-pool cleanup work

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- reuse the current tightened adult outputs
- rank likely pool contamination by strong adult evidence density
- keep clearly weak/noisy pages in the true-rule-false-positive bucket

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

- [x] the remaining adult hits are split into two explicit lists
- [x] the split rationale is documented
- [x] no code or schema changes are mixed into this task

## 11. Validation Checklist

Minimum validation expected:

- [x] remaining-hit extraction
- [x] bucket split review
- [x] handoff produced
- [x] final summary reflects the two-bucket split

Commands to run if applicable:

```bash
python - <<'PY'
# extract remaining benign adult hits and split them into two buckets
PY
```

Expected evidence to capture:

- count of remaining hits
- bucket counts
- representative samples per bucket

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

- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`

## 13. Open Questions / Blocking Issues

- `none`
