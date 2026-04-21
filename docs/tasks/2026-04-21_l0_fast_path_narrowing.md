# L0 fast-path narrowing task

## 中文版

> 面向人类阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把当前 L0 收窄为更快的 specialized fast path。
- 目标边界已经冻结：L0 只重点处理 `gambling`、`adult`、`gate` 三类 specialized 信号。
- 当前新增约束已经纳入：从 L0 默认热路径移除 `HTML` 和 `brand` 处理。
- 其他页面默认尽快路由到 L1，不在本任务中继续扩展 L0 证据面。

## 任务元信息

- Task ID: `TASK-L0-2026-04-21-FAST-PATH-NARROWING`
- Task Title: `Narrow L0 into a gambling/adult/gate fast path and remove HTML and brand from the default hot path`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`; `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`; `L0_DESIGN_V1.md`; `docs/modules/MODULE_INFER.md`
- Created At: `2026-04-21`
- Requested By: `User`

## 1. Background

最近的 L0 小样本延迟拆解显示，当前本地路径平均开销约 `111.8 ms / sample`，其中 `html_features`、specialized keyword scanning、brand extraction 占了绝大多数时间。

当前 specialized detector 的核心 `gambling / adult / gate` 触发本身并不依赖 `html_features`。用户已经明确要求把 L0 收窄为只做这三类快速判断，并进一步把 `HTML` 与 `brand` 从默认热路径拿掉，以降低单页判断延迟。

这个任务需要把范围冻结成一个最小实现任务，避免在执行时继续扩大 L0 职责。

## 2. Goal

将当前 L0 调整为一个更窄、更快的 fast path：默认只围绕 `possible_gambling_lure`、`possible_adult_lure`、`possible_age_gate_surface`、`possible_gate_or_evasion` 及其必要 routing hints 进行低成本判断；从默认热路径中去掉完整 `HTML` 特征提取与 `brand` 提取；让不属于这三类 specialized surface 的页面尽快交给 L1；并用小范围延迟与行为回归验证降耗结果和行为边界。

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

This task is allowed to change:

- the default L0 hot-path call order
- whether `html_features` and `claimed_brands` are computed on the default L0 path
- routing behavior that escalates non-specialized or evidence-light pages to L1 faster
- local benchmark / smoke-validation commands and their recorded summaries

## 4. Scope Out

This task must NOT do the following:

- redesign L1 or L2 behavior
- rename frozen schema fields or label keys
- add third-party dependencies or database-backed matching infrastructure
- redesign the entire inference stack beyond the L0 fast path
- weaken the existing `gambling / adult / gate` specialized outputs into unrelated generic risk logic

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`
- `L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\hard benign\gambling`
- `E:\Warden\data\raw\benign\gate`

### Prior Handoff

- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a minimal code patch that narrows the default L0 hot path
- removal of default hot-path `html_features` and `brand` extraction from the L0 path
- any necessary doc updates describing the new L0 responsibility boundary
- one bounded regression / latency summary on a small deterministic slice
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

- keep L0 focused on `gambling / adult / gate` specialization only
- remove full `HTML` feature extraction from the default L0 hot path unless a tiny explicitly-gated fallback is approved later
- remove `brand` extraction from the default L0 hot path
- prefer preserving existing field presence with empty / default-compatible values over breaking downstream readers
- do not introduce database storage, FTS, or other infrastructure changes in this task

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- current specialized output keys such as `possible_gambling_lure`, `possible_adult_lure`, `possible_age_gate_surface`, `possible_gate_or_evasion`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_adult_lure`; `possible_age_gate_surface`; `possible_gate_or_evasion`; `routing_reason_codes`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current sample-dir labeling flow
  - current downstream readers of generated label JSON

Downstream consumers to watch:

- dataset backfill runs
- any inference-side readers expecting current label key presence
- future latency comparison tasks

## 9. Suggested Execution Plan

Recommended order:

1. Read the current L0 path and freeze exactly where `html_features` and `brand` are computed.
2. Apply the smallest patch that removes them from the default L0 hot path.
3. Keep specialized gambling/adult/gate logic and L1 escalation behavior coherent.
4. Run a bounded latency spot-check and a bounded behavior regression on the specialized slices.
5. Update docs and prepare handoff.

Task-specific execution notes:

- keep non-specialized pages on the quickest path to L1
- if a field previously derived from `html_features` or `brand` must remain present, prefer a safe default over interface drift
- record any precision / recall risk introduced by removing default hot-path evidence

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

- [ ] default L0 hot path no longer computes full `html_features`
- [ ] default L0 hot path no longer computes `claimed_brands`
- [ ] specialized `gambling / adult / gate` outputs still run on the intended low-cost evidence path
- [ ] non-specialized pages escalate to L1 without expanding L0 evidence cost
- [ ] small-slice latency improves measurably versus the current baseline

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity on touched Python files
- [ ] one deterministic small-slice latency spot check
- [ ] one bounded behavior regression on `benign`, `adult`, `gambling`, and `gate` slices
- [ ] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python ...
```

Expected evidence to capture:

- before / after mean latency on the bounded slice
- whether specialized trigger rates changed on the bounded slice
- whether any downstream compatibility caveat remains

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- what changed in the L0 hot path
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-FAST-PATH-NARROWING`
- Task Title: `Narrow L0 into a gambling/adult/gate fast path and remove HTML and brand from the default hot path`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`; `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`; `L0_DESIGN_V1.md`; `docs/modules/MODULE_INFER.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to narrow the current L0 path into a faster specialized fast path focused on `gambling`, `adult`, and `gate`, while removing default hot-path `HTML` and `brand` processing and preserving documented interface stability where possible.

## 1. Background

The recent small-slice L0 latency breakdown showed an average local cost of about `111.8 ms / sample`, with `html_features`, specialized keyword scanning, and brand extraction dominating most of the runtime.

The current specialized detector core for `gambling / adult / gate` does not actually depend on `html_features` for its main trigger logic. The user has now explicitly requested that L0 be narrowed into a fast triage layer for only these three specialized surfaces and that both `HTML` and `brand` be removed from the default hot path in order to reduce per-page latency.

This task is needed to freeze that boundary into a minimal implementation scope before execution expands it again.

## 2. Goal

Refactor the current L0 path into a narrower and faster fast path that focuses by default on low-cost decisions for `possible_gambling_lure`, `possible_adult_lure`, `possible_age_gate_surface`, `possible_gate_or_evasion`, and their necessary routing hints; remove full `HTML` feature extraction and `brand` extraction from the default hot path; send pages outside these specialized surfaces to L1 quickly; and validate the change with a bounded latency and behavior regression.

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

This task is allowed to change:

- the default L0 hot-path call order
- whether `html_features` and `claimed_brands` are computed on the default L0 path
- routing behavior that escalates non-specialized or evidence-light pages to L1 faster
- local benchmark / smoke-validation commands and their recorded summaries

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- redesign L1 or L2 behavior
- rename frozen schema fields or label keys
- add third-party dependencies or database-backed matching infrastructure
- redesign the entire inference stack beyond the L0 fast path
- weaken the existing `gambling / adult / gate` specialized outputs into unrelated generic risk logic

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_latency_breakdown_analysis.md`
- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`
- `L0_DESIGN_V1.md`
- `docs/modules/MODULE_INFER.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `src/warden/module/l0.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\benign`
- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\hard benign\gambling`
- `E:\Warden\data\raw\benign\gate`

### Prior Handoff

- `docs/handoff/2026-04-21_l0_latency_breakdown_analysis.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a minimal code patch that narrows the default L0 hot path
- removal of default hot-path `html_features` and `brand` extraction from the L0 path
- any necessary doc updates describing the new L0 responsibility boundary
- one bounded regression / latency summary on a small deterministic slice
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

- keep L0 focused on `gambling / adult / gate` specialization only
- remove full `HTML` feature extraction from the default L0 hot path unless a tiny explicitly gated fallback is approved later
- remove `brand` extraction from the default L0 hot path
- prefer preserving existing field presence with empty or default-compatible values over breaking downstream readers
- do not introduce database storage, FTS, or other infrastructure changes in this task

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- current specialized output keys such as `possible_gambling_lure`, `possible_adult_lure`, `possible_age_gate_surface`, `possible_gate_or_evasion`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_adult_lure`; `possible_age_gate_surface`; `possible_gate_or_evasion`; `routing_reason_codes`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - current sample-dir labeling flow
  - current downstream readers of generated label JSON

Downstream consumers to watch:

- dataset backfill runs
- any inference-side readers expecting current label key presence
- future latency comparison tasks

## 9. Suggested Execution Plan

Recommended order:

1. Read the current L0 path and freeze exactly where `html_features` and `brand` are computed.
2. Apply the smallest patch that removes them from the default L0 hot path.
3. Keep specialized gambling/adult/gate logic and L1 escalation behavior coherent.
4. Run a bounded latency spot-check and a bounded behavior regression on the specialized slices.
5. Update docs and prepare handoff.

Task-specific execution notes:

- keep non-specialized pages on the quickest path to L1
- if a field previously derived from `html_features` or `brand` must remain present, prefer a safe default over interface drift
- record any precision or recall risk introduced by removing default hot-path evidence

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

- [x] default L0 hot path no longer computes full `html_features`
- [x] default L0 hot path no longer computes `claimed_brands`
- [x] specialized `gambling / adult / gate` outputs still run on the intended low-cost evidence path
- [x] non-specialized pages escalate to L1 without expanding L0 evidence cost
- [x] small-slice latency improves measurably versus the current baseline

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity on touched Python files
- [x] one deterministic small-slice latency spot check
- [x] one bounded behavior regression on `benign`, `adult`, `gambling`, and `gate` slices
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py
python ...
```

Expected evidence to capture:

- before / after mean latency on the bounded slice
- whether specialized trigger rates changed on the bounded slice
- whether any downstream compatibility caveat remains

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- what changed in the L0 hot path
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

## 13. Open Questions / Blocking Issues

- none
