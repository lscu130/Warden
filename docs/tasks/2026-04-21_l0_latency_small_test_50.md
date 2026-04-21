# L0 latency small test task

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
### 使用说明

- 本任务只做一次小范围 L0 时延测试。
- 样本固定为 `50` 个：`30` 个 benign、`10` 个 adult、`10` 个 gambling。
- 本任务只做抽样、计时、统计与文档交付，不修改 L0 实现。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-21-LATENCY-SMALL-TEST-50`
- 任务标题：`运行 50 样本 L0 小范围时延测试并统计平均处理时间`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`TODO`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- 创建日期：`2026-04-21`
- 提出人：`User`

## 1. Background

The user requested a small-scope timing measurement for the current L0 sample-judgment path. The requested mix is `50` samples total with `30` benign, `10` adult, and `10` gambling. The benchmark should reflect the current working-tree logic rather than a hypothetical deployment path.

The current repo already exposes a sample-directory entrypoint in `scripts/labeling/Warden_auto_label_utils_brandlex.py`:

- `derive_auto_labels_from_sample_dir(...)`
- `derive_rule_labels(...)`

This task is needed now to measure the current local processing cost of the L0 path on a bounded sample slice and to report the actual average time honestly.

## 2. Goal

Run a deterministic 50-sample L0 timing test using the current local sample pools, measure the average processing time per sample, and report both the end-to-end timing for `sample_dir -> auto_labels -> rule_labels` and the narrower `derive_auto_labels_from_sample_dir(...)` timing so the current L0 cost is auditable and comparable later.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-21_l0_latency_small_test_50.md`
- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

This task is allowed to change:

- repo task / handoff docs
- runtime commands
- temporary one-off timing scripts or inline commands

## 4. Scope Out

This task must NOT do the following:

- modify L0 detector or routing logic
- modify schema or field names
- move or edit sampled data
- claim production or hardware-general benchmark guarantees

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\hard benign\gambling`

### Prior Handoff

- `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one deterministic 50-sample L0 timing run
- average and percentile timing summaries
- actual sample counts per pool
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

- use the current working-tree L0 path only
- keep the sample mix at `30` benign, `10` adult, `10` gambling unless a pool is smaller
- report the exact timing scope honestly

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `l0_routing_hints`
- current `derive_auto_labels_from_sample_dir(...)`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `none`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of label outputs

Downstream consumers to watch:

- benchmark comparisons in future handoffs
- inference-side latency expectations

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Sample the three pools with a fixed seed.
4. Run the smallest meaningful timing benchmark.
5. Summarize timing, compatibility impact, and caveats.
6. Prepare handoff.

Task-specific execution notes:

- measure both `derive_auto_labels_from_sample_dir(...)` and the combined `derive_auto_labels_from_sample_dir(...) + derive_rule_labels(...)`
- keep the sample selection deterministic
- report mean plus percentile-style summaries, not just one number

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

- [x] exactly one 50-sample run was completed with the requested mix
- [x] average timing was measured and reported
- [x] timing scope and caveats were stated explicitly

## 11. Validation Checklist

Minimum validation expected:

- [x] sample-count check
- [x] successful timing execution
- [x] output spot-check
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# deterministic 50-sample L0 timing benchmark
PY
```

Expected evidence to capture:

- exact selected sample counts
- mean / p50 / p90 / p95 timing values

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

- `docs/handoff/2026-04-21_l0_latency_small_test_50.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-LATENCY-SMALL-TEST-50`
- Task Title: `Run a 50-sample L0 latency spot test and report the average processing time`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-10_l0_specialized_detectors_small_batch_regression.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to run a deterministic 50-sample latency spot test for the current local L0 path and report the average per-sample processing time honestly.
