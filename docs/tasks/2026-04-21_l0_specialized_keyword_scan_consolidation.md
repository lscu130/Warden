# L0 specialized keyword scan consolidation task

## 中文版

> 面向人工阅读的摘要版。英文版为权威版本；若字段、范围、兼容性、命令或验收条件有冲突，以英文版为准。

### 使用说明

- 本任务单独冻结 `src/warden/module/l0.py` 中 specialized detectors 的 repeated keyword scanning 优化。
- 本任务只处理扫描重复，不处理 HTML、brand、阈值调参、词表扩写、L1/L2 路由重设计。
- 目标是先把可重复扫描的低成本热点整合掉，再做小范围延迟与行为回归验证。

## 任务元信息

- Task ID: `TASK-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Task Title: `Consolidate repeated specialized keyword scanning inside src/warden/module/l0.py`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`; `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

## 1. Background

上一条 `l0_fast_path_narrowing` 任务已经把默认热路径收窄到 `gambling / adult / gate` 三类 specialized signals，并从默认 L0 热路径中移除了 `HTML` 与 `brand` 的主成本项。

当前剩余的 L0 内部热点之一，是 `src/warden/module/l0.py` 中 `derive_specialized_surface_signals(...)` 对同一份 `text_low`、`title_low`、`url_blob` 做多轮 `hit_keywords(...)` 扫描。`gambling`、`adult`、`gate` 三组逻辑各自重复扫描，导致同一输入被多次线性遍历。

需要把这个问题冻结为一条单独窄任务，避免在执行时把范围漂移到词表改写、策略重调、HTML 回归或其他模块。

## 2. Goal

在不改变现有 specialized 输出字段、规则语义和默认 L0 职责边界的前提下，对 `src/warden/module/l0.py` 内部 repeated keyword scanning 做最小 consolidation：减少对相同文本和 URL blob 的重复扫描次数，保留当前 `gambling / adult / gate` 专项触发的可解释性，并通过一个小范围、可重复的延迟与行为回归确认变更没有引入明显退化。

## 3. Scope In

This task is allowed to touch:

- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

This task is allowed to change:

- internal keyword-scan orchestration inside `derive_specialized_surface_signals(...)`
- shared low-cost helper structure inside `src/warden/module/l0.py` if it only serves repeated specialized keyword scan consolidation
- local benchmark or smoke-validation notes captured for this task

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- reintroduce `HTML` or `brand` work into the default L0 hot path
- retune thresholds, labels, routing policy, or specialized trigger semantics
- rewrite lexicons, add new keyword families, or broaden detector coverage
- touch `scripts/labeling/Warden_auto_label_utils_brandlex.py` unless a separate approval is given
- modify L1 or L2 behavior
- add third-party dependencies, databases, FTS, or external indexing infrastructure

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`

### Code / Scripts

- `src/warden/module/l0.py`

### Data / Artifacts

- the same deterministic small-slice benchmark composition used for recent L0 latency spot checks, or an explicitly documented equivalent slice
- current local sample pools for `benign`, `adult`, `gambling`, and `gate`

### Prior Handoff

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a minimal code patch that consolidates repeated specialized keyword scanning in `src/warden/module/l0.py`
- a bounded latency comparison before and after the consolidation
- a bounded behavior regression summary on `benign`, `adult`, `gambling`, and `gate`
- a repo handoff document at `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

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

- keep all work inside `src/warden/module/l0.py`
- preserve current specialized field names and meaning
- optimize scan reuse before considering any lexicon or rule changes
- keep the resulting logic auditable and easy to trace back to detector-specific evidence
- do not collapse distinct evidence buckets if that would hide current detector explainability

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `prepare_l0_inputs(...)`
- `derive_specialized_surface_signals(...)`
- `derive_l0_routing_hints(...)`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_bonus_or_betting_induction`; `possible_adult_lure`; `possible_age_gate_surface`; `possible_gate_or_evasion`; `matched_keywords`; `routing_reason_codes`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current inference-side imports of `src/warden/module/l0.py`
  - current dataset backfill flows that consume the same specialized outputs indirectly through the L0 module boundary
  - current local benchmark entry points already used for recent L0 latency checks

Downstream consumers to watch:

- L0 callers expecting current specialized output keys
- evaluation scripts that compare trigger rates across `benign`, `adult`, `gambling`, and `gate`

## 9. Suggested Execution Plan

Recommended order:

1. Read the current repeated scan sites inside `derive_specialized_surface_signals(...)`.
2. Freeze which scans are logically distinct and which can be consolidated safely.
3. Apply the smallest internal refactor that reuses scanning results without changing output semantics.
4. Run syntax sanity and one bounded before/after benchmark.
5. Run one bounded behavior regression and prepare handoff.

Task-specific execution notes:

- prioritize consolidation around repeated `hit_keywords(...)` passes over the same `text_low` and `url_blob`
- avoid speculative abstractions that spread detector logic across multiple modules
- if a consolidation changes evidence ordering or tie behavior, record it explicitly in the handoff

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

- [x] repeated specialized keyword scans in `src/warden/module/l0.py` are materially consolidated
- [x] current specialized outputs remain field-compatible
- [x] detector-specific evidence remains explainable after consolidation
- [x] bounded latency is improved, and the observed gain is explicitly documented
- [x] bounded trigger behavior does not show unexplained regression

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax or import sanity on touched Python files
- [x] one deterministic small-slice latency spot check before and after
- [x] one bounded behavior regression on `benign`, `adult`, `gambling`, and `gate`
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py
python ...
python ...
```

Expected evidence to capture:

- before and after mean latency on the bounded slice
- whether per-class specialized trigger counts changed
- whether any compatibility caveat remains for current L0 callers

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- repeated-scan hotspots consolidated
- behavior impact
- schema or interface impact
- validation performed
- risks or caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-SPECIALIZED-KEYWORD-SCAN-CONSOLIDATION`
- Task Title: `Consolidate repeated specialized keyword scanning inside src/warden/module/l0.py`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`; `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to isolate and optimize repeated keyword scanning inside `src/warden/module/l0.py` only. This task is intentionally narrow and should not expand into HTML, brand, threshold, lexicon, or routing redesign work.

## 1. Background

The previous `l0_fast_path_narrowing` task already narrowed the default hot path to the three specialized surfaces `gambling / adult / gate` and removed `HTML` and `brand` from the default L0 hot path.

One of the remaining internal L0 hotspots is that `derive_specialized_surface_signals(...)` in `src/warden/module/l0.py` performs multiple `hit_keywords(...)` passes over the same `text_low`, `title_low`, and `url_blob`. The `gambling`, `adult`, and `gate` branches each rescan overlapping inputs, which means the same strings are traversed multiple times.

This task is needed to freeze that problem into a separate narrow execution unit so the implementation does not drift into lexicon rewrites, threshold retuning, HTML reintroduction, or other module changes.

## 2. Goal

Consolidate repeated keyword scanning inside `src/warden/module/l0.py` with the smallest internal refactor that reduces duplicate scans over the same text and URL blobs, while preserving current specialized output fields, rule semantics, explainability, and the narrowed L0 responsibility boundary. Validate the change with one bounded latency comparison and one bounded behavior regression.

## 3. Scope In

This task is allowed to touch:

- `src/warden/module/l0.py`
- `docs/tasks/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

This task is allowed to change:

- internal keyword-scan orchestration inside `derive_specialized_surface_signals(...)`
- shared low-cost helper structure inside `src/warden/module/l0.py` when it exists only to support repeated specialized keyword scan consolidation
- local benchmark or smoke-validation notes captured for this task

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- reintroduce `HTML` or `brand` work into the default L0 hot path
- retune thresholds, labels, routing policy, or specialized trigger semantics
- rewrite lexicons, add new keyword families, or broaden detector coverage
- touch `scripts/labeling/Warden_auto_label_utils_brandlex.py` unless separate approval is given
- modify L1 or L2 behavior
- add third-party dependencies, databases, FTS, or external indexing infrastructure

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`

### Code / Scripts

- `src/warden/module/l0.py`

### Data / Artifacts

- the same deterministic small-slice benchmark composition used for recent L0 latency spot checks, or an explicitly documented equivalent slice
- current local sample pools for `benign`, `adult`, `gambling`, and `gate`

### Prior Handoff

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a minimal code patch that consolidates repeated specialized keyword scanning in `src/warden/module/l0.py`
- a bounded latency comparison before and after the consolidation
- a bounded behavior regression summary on `benign`, `adult`, `gambling`, and `gate`
- a repo handoff document at `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

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

- keep all work inside `src/warden/module/l0.py`
- preserve current specialized field names and meanings
- optimize scan reuse before considering any lexicon or rule changes
- keep the resulting logic auditable and easy to trace back to detector-specific evidence
- do not collapse distinct evidence buckets if that would hide current detector explainability

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `prepare_l0_inputs(...)`
- `derive_specialized_surface_signals(...)`
- `derive_l0_routing_hints(...)`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_gambling_lure`; `possible_bonus_or_betting_induction`; `possible_adult_lure`; `possible_age_gate_surface`; `possible_gate_or_evasion`; `matched_keywords`; `routing_reason_codes`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current inference-side imports of `src/warden/module/l0.py`
  - current dataset backfill flows that consume the same specialized outputs indirectly through the L0 module boundary
  - current local benchmark entry points already used for recent L0 latency checks

Downstream consumers to watch:

- L0 callers expecting current specialized output keys
- evaluation scripts that compare trigger rates across `benign`, `adult`, `gambling`, and `gate`

## 9. Suggested Execution Plan

Recommended order:

1. Read the current repeated scan sites inside `derive_specialized_surface_signals(...)`.
2. Freeze which scans are logically distinct and which can be consolidated safely.
3. Apply the smallest internal refactor that reuses scanning results without changing output semantics.
4. Run syntax sanity and one bounded before/after benchmark.
5. Run one bounded behavior regression and prepare handoff.

Task-specific execution notes:

- prioritize consolidation around repeated `hit_keywords(...)` passes over the same `text_low` and `url_blob`
- avoid speculative abstractions that spread detector logic across multiple modules
- if a consolidation changes evidence ordering or tie behavior, record it explicitly in the handoff

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

- [x] repeated specialized keyword scans in `src/warden/module/l0.py` are materially consolidated
- [x] current specialized outputs remain field-compatible
- [x] detector-specific evidence remains explainable after consolidation
- [x] bounded latency is improved, and the observed gain is explicitly documented
- [x] bounded trigger behavior does not show unexplained regression

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax or import sanity on touched Python files
- [x] one deterministic small-slice latency spot check before and after
- [x] one bounded behavior regression on `benign`, `adult`, `gambling`, and `gate`
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\src\warden\module\l0.py
python ...
python ...
```

Expected evidence to capture:

- before and after mean latency on the bounded slice
- whether per-class specialized trigger counts changed
- whether any compatibility caveat remains for current L0 callers

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- repeated-scan hotspots consolidated
- behavior impact
- schema or interface impact
- validation performed
- risks or caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`

## 13. Open Questions / Blocking Issues

- none
