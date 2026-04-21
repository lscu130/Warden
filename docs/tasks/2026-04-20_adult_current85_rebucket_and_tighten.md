# Adult current-85 rebucket and tightening task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于重挖当前 `85` 个 ordinary-benign adult hits，重新拆分污染样本和真规则噪音。
- 对确认更像成人污染样本的一桶，允许从 `E:\Warden\data\raw\benign\benign` 移到 `E:\Warden\data\raw\benign\hard benign\adult`。
- 对新的 `true-rule-noise` 桶，只允许做低成本、L0 兼容的 `adult` 精度收紧。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-20-ADULT-CURRENT85-REBUCKET-AND-TIGHTEN`
- 任务标题：`重挖当前 85 个 benign adult hits 并继续收紧 adult`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`；`docs/workflow/GPT_CODEX_WORKFLOW.md`；`docs/templates/TASK_TEMPLATE.md`；`docs/templates/HANDOFF_TEMPLATE.md`；`docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- 创建日期：`2026-04-20`
- 提出人：`User`

## 1. 背景

在上一次清理 benign 池并重跑统计之后，当前 ordinary benign 根目录里仍有 `85` 个 `possible_adult_lure` 命中。

这 `85` 个命中不能直接当作同一种东西处理。里面通常混着两类样本：

- 更像成人站、成人聚合页或初筛漏入 ordinary benign 的污染样本
- 真正由当前 `adult` 规则带出来的噪音页

如果不先重新拆桶，后续 precision tightening 会继续被污染样本干扰。

## 2. 目标

基于当前工作树和当前数据根目录，重新提取当前 `85` 个 ordinary-benign adult hits，拆成新的 `pool contamination` 与 `true rule noise` 两桶；把新的污染桶移出 ordinary benign；然后只针对新的 true-rule-noise 桶继续做一轮最小、可审计、低成本的 adult precision tightening，并重跑 adult / ordinary-benign 指标。

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\data\raw\benign\benign\<selected sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<selected sample_dirs>`
- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

This task is allowed to change:

- adult-hit rebucketing output and cleanup move
- adult-specific low-cost trigger tightening
- adult contract docs if behavior changes
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `gambling` or `gate`
- add heavy HTML parsing, OCR, screenshot semantics, or new dependencies to L0
- rename frozen schema fields or CLI flags
- change dataset paths outside the approved selected sample dirs
- do broad refactor outside the adult-specific path

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- current `possible_adult_lure` hits on the cleaned benign pool

### Prior Handoff

- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one explicit split of the current `85` ordinary-benign adult hits
- one cleanup move for the newly identified contamination bucket
- one minimal adult precision-tightening patch if justified
- before/after quantification on adult and ordinary-benign pools
- one repo handoff document

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

- re-mine the current 85 hits before moving or patching anything
- keep adult tightening low-cost and L0-compatible
- do not silently expand this task into a new taxonomy or multimodal redesign
- if a sample move is performed, verify exact source and destination paths before moving

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- adult proxy metrics
- downstream routing flags derived from adult surfaces
- future benign-pool cleanup analysis

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- extract the current 85 benign hits first
- split them into new contamination vs true-rule-noise buckets
- if contamination exists, move only that bucket out of ordinary benign
- then patch adult logic only against the remaining true-rule-noise bucket
- rerun adult / ordinary-benign metrics after the move and patch

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

- [x] current 85 ordinary-benign adult hits are explicitly re-bucketed
- [x] any moved contamination samples are validated before and after the move
- [x] adult tightening is applied only to the new true-rule-noise bucket
- [x] before/after adult and ordinary-benign metrics are reported

## 11. Validation Checklist

Minimum validation expected:

- [x] current-hit extraction
- [x] rebucket review
- [x] syntax / import sanity
- [x] before/after adult vs ordinary-benign quantification
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# extract current benign adult hits, rebucket them, and rerun metrics after move/patch
PY
```

Expected evidence to capture:

- current 85-hit list and new bucket counts
- moved-sample count if cleanup move happens
- before/after ordinary-benign false positives
- before/after adult recall / precision proxies

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

- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-20-ADULT-CURRENT85-REBUCKET-AND-TIGHTEN`
- Task Title: `Rebucket the current 85 benign adult hits and continue adult tightening`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`
- Created At: `2026-04-20`
- Requested By: `User`

Use this task to re-mine the current `85` ordinary-benign `adult` hits, split them into a new contamination bucket and a new true-rule-noise bucket, move the contamination bucket out of the ordinary-benign pool if justified, and then continue one minimal low-cost adult precision-tightening pass only against the new true-rule-noise bucket.

## 1. Background

After the benign-pool cleanup and the later metrics rerun, the current ordinary-benign root still contains `85` `possible_adult_lure` hits.

Those `85` hits should not be treated as one population. They usually mix:

- pages that look more like adult sites, adult aggregators, or earlier screening misses that still contaminate the ordinary-benign pool
- pages that are genuinely being brought up by the current `adult` rules as noise

If the bucket split is not refreshed first, the next precision-tightening pass will remain distorted by contamination samples.

## 2. Goal

Using the current working tree and the current dataset roots, extract the current `85` ordinary-benign `adult` hits again, split them into a new `pool contamination` bucket and a new `true rule noise` bucket, move the new contamination bucket out of the ordinary-benign pool, then continue one minimal auditable low-cost adult precision-tightening pass only against the new true-rule-noise bucket, and finally rerun adult / ordinary-benign metrics.

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\data\raw\benign\benign\<selected sample_dirs>`
- `E:\Warden\data\raw\benign\hard benign\adult\<selected sample_dirs>`
- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`

This task is allowed to change:

- adult-hit rebucketing output and cleanup move
- adult-specific low-cost trigger tightening
- adult contract docs if behavior changes
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- modify `gambling` or `gate`
- add heavy HTML parsing, OCR, screenshot semantics, or new dependencies to L0
- rename frozen schema fields or CLI flags
- change dataset paths outside the approved selected sample dirs
- do broad refactor outside the adult-specific path

## 5. Inputs

Relevant inputs for this task:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-16_adult_false_positive_tightening.md`
- `docs/handoff/2026-04-17_adult_remaining_benign_hit_split.md`
- `docs/handoff/2026-04-17_adult_post_cleanup_metrics_rerun.md`
