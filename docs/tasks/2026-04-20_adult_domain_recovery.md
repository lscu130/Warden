# Adult narrow domain recovery task

## 中文版

> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务只做一条非常窄的 `adult` recall recovery。
- 范围只允许覆盖上一条 review 里确认的 `single_strong_token_with_domain_only` 模式。
- 不允许顺手放宽其他 adult 路径，也不允许碰 `gambling` / `gate`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-20-ADULT-DOMAIN-RECOVERY`
- 任务标题：`恢复 adult 的窄域名支撑单强词路径`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`TODO`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`；`docs/workflow/GPT_CODEX_WORKFLOW.md`；`docs/templates/TASK_TEMPLATE.md`；`docs/templates/HANDOFF_TEMPLATE.md`；`docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- 创建日期：`2026-04-20`
- 提出人：`User`

## 1. 背景

上一条 review 的结论是：

- 不建议重开 broad adult recall recovery
- 如果要恢复，只建议恢复非常窄的 `adult-domain` 类
- 当前最值得单独看的模式是 `single_strong_token_with_domain_only`

这类样本的共同点是：

- 只有 `1` 个强成人词
- 但 URL / host 本身带明显 adult domain 提示
- 当前 stricter rule 下被压掉

## 2. 目标

对 `single_strong_token_with_domain_only` 做一条最小、可审计、低成本的 adult recall recovery，要求它尽量只回收当前 adult 池里这类被压掉的窄子集，同时保持当前 benign 池不明显回弹。

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-20_adult_domain_recovery.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

This task is allowed to change:

- one narrow adult recall-recovery rule
- adult contract wording if behavior changes
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- broaden adult logic outside the target pattern
- modify `gambling` or `gate`
- add heavy evidence, OCR, screenshot semantics, or dependencies
- rename schema fields or CLI flags
- move more dataset directories

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\benign`
- the current dropped-adult subpattern `single_strong_token_with_domain_only`

### Prior Handoff

- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one narrow adult-domain recovery patch
- updated adult contract text if needed
- before/after quantification on the current adult and benign pools
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

- recovery must stay inside `single_strong_token_with_domain_only` or a strictly narrower equivalent
- recovery must remain low-cost and L0-compatible
- quantify adult gain and benign rebound explicitly
- do not turn this into a general `2-token` rollback

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
- future adult recall / precision tuning

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- evaluate the recovery candidate before committing the patch
- prefer a token allowlist or equivalent narrow gate if needed
- rerun both adult and benign metrics after the patch

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

- [x] one narrow adult-domain recovery is implemented
- [x] adult gain is measured
- [x] benign rebound is measured
- [x] no broad adult rollback is introduced

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted candidate evaluation before patch
- [x] after-patch adult vs benign quantification
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# evaluate narrow adult-domain recovery and rerun metrics
PY
```

Expected evidence to capture:

- recovered adult sample count
- benign rebound count
- updated precision / recall proxies

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

- `docs/handoff/2026-04-20_adult_domain_recovery.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-20-ADULT-DOMAIN-RECOVERY`
- Task Title: `Recover the narrow adult domain-supported single-strong-token path`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- Created At: `2026-04-20`
- Requested By: `User`

Use this task to implement one very narrow `adult` recall recovery restricted to the `single_strong_token_with_domain_only` pattern identified in the previous review.

## 1. Background

The previous review concluded:

- do not reopen a broad adult recall recovery
- if recovery is reopened at all, it should only target a very narrow adult-domain path
- the most justified subpattern is `single_strong_token_with_domain_only`

Those samples share a common structure:

- only `1` strong adult token
- but the URL / host still carries an obvious adult-domain hint
- they are currently suppressed by the stricter rule

## 2. Goal

Implement a minimal auditable low-cost adult recall recovery for `single_strong_token_with_domain_only`, aiming to recover that narrow subset from the current adult pool while keeping the current benign pool from materially rebounding.
