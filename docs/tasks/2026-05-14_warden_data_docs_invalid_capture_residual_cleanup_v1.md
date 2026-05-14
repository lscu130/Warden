# Task Metadata

- Task ID: TASK_20260514_WARDEN_DATA_DOCS_INVALID_CAPTURE_RESIDUAL_CLEANUP_V1
- Task Title: Warden Data Docs Invalid Capture Residual Cleanup V1
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: docs / data / infer / runtime
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260514_WARDEN_DATA_DOCS_INVALID_CAPTURE_RESIDUAL_CLEANUP_V1.md
- Created At: 2026-05-14
- Requested By: User
- Karpathy Guardrails Required: YES

## 中文版

### 1. 背景

本任务按用户提供的 `TASK_20260514_WARDEN_DATA_DOCS_INVALID_CAPTURE_RESIDUAL_CLEANUP_V1.md` 执行，范围限定为文档清理。

目标是清理 active 文档中关于 invalid capture、404 / blank / pure-color / broken render / insufficient-observability、recrawl 路由、auxiliary bucket 的旧口径，使其统一为：

- 无效采集、错误页、空白页、纯色渲染、严重渲染失败和证据不可观测页面是数据质量 / 可观测性失败；
- 这些对象在正式 train / validation / test 构建前由数据集构建 / 清洗流程移除；
- 它们不进入 benign / malicious / suspicious / uncertain 或 auxiliary 威胁标签体系；
- 当前在线架构只定义 `L0` 和 `L1`，当前 L1 / Rule Router 不输出 recrawl 路由；
- recrawl 若未来出现，只能作为另行定义的采集基础设施能力，不能作为当前威胁模型输出。

本任务不修改代码、schema、manifest、split、数据文件或运行时行为。

## English Version

> AI note: The English section is authoritative for exact scope, constraints, validation, and acceptance criteria.

# Warden Data Docs Invalid Capture Residual Cleanup V1

## 1. Background

The previous L0-to-L1 realignment accepted the core behavior and routing direction but left residual wording in active data and module documentation. Those residuals can still imply that invalid captures, blank pages, broken renders, or insufficient-observability states belong in benign, malicious, suspicious, uncertain, auxiliary, recrawl, or QA routing systems.

The current project definition is:

- Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, structure-corruption pages, and insufficient-observability pages are dataset-quality / observability failures.
- They are removed during dataset construction and cleaning before formal train / validation / test construction.
- They are not Warden threat-model samples.
- They must not be labeled as benign, malicious, suspicious, uncertain, or auxiliary threat samples.
- L0 handles only a small set of high-confidence cheap terminal or auxiliary buckets such as adult, gambling, and obvious gate / challenge / verification.
- Every valid non-terminal webpage sample must route to L1 by default.
- L1 is the main judgment layer; Rule Router may provide evidence-sufficiency diagnostics and review routing, but must not emit final labels or recrawl routing.

## 2. Goal

Clean active documentation residuals so the data, L0, L1, runtime, and text-pipeline documentation no longer preserve the old invalid-capture / recrawl / auxiliary semantics.

## 3. Scope In

- Active documentation under `docs/data/**` that discusses blank pages, broken renders, invalid captures, gate / evasion auxiliary samples, second-pass benign review, malicious source validity, or label derivation.
- Active module documentation under `docs/modules/**` when it describes current L0 / L1 routing, recrawl hints, or routing heads.
- Residual grep report covering `docs`, `AGENTS.md`, `PROJECT.md`, and `README.md`.
- Repo-local task document and formal handoff document.

## 4. Scope Out

- No code changes.
- No runtime, inference, crawler, model, OCR, YOLO, CLIP, SNet, schema, label, manifest, split, or dataset changes.
- No recrawl / exclude / QA queue implementation.
- No new active L2 architecture.
- No rewrite of historical ADR, old task, old handoff, or old report documents unless the current task explicitly identifies them as active contracts.

## 5. Inputs

- User-provided task file: `C:\Users\20516\Downloads\TASK_20260514_WARDEN_DATA_DOCS_INVALID_CAPTURE_RESIDUAL_CLEANUP_V1.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- Current active docs found by residual grep.

## 6. Required Outputs

- `docs/tasks/2026-05-14_warden_data_docs_invalid_capture_residual_cleanup_v1.md`
- `docs/reports/2026-05-14_invalid_capture_residual_grep_report_v1.md`
- `docs/handoff/2026-05-14_warden_data_docs_invalid_capture_residual_cleanup_v1.md`
- Minimal wording patches to active docs only.

## 7. Hard Constraints

- Preserve existing schema and interface contracts.
- Do not invent new labels or routing states.
- Do not convert invalid captures into any threat label, auxiliary threat bucket, recrawl route, exclude queue, or QA queue.
- Preserve historical records; classify them in the residual report instead of rewriting them.
- Keep all edits minimal and directly traceable to this task.

## 8. Interface / Schema Constraints

Schema changed: no.

Output format changed: no.

Routing output changed: no implementation changed in this task.

Label semantics changed: active documentation is clarified to preserve the already accepted project definition; no new label is introduced.

## 9. Evidence Rules

- Read the external task document before editing.
- Read mandatory Warden governing files before editing.
- Run focused residual grep before and after edits.
- Classify remaining residual hits into active aligned, historical / superseded, numeric false-positive, or out-of-scope operational capture references.

## 10. Acceptance Criteria

- Active docs no longer imply that invalid capture / blank / 404 / pure-color / broken render / insufficient-observability pages are benign, malicious, suspicious, uncertain, or auxiliary threat labels.
- Active docs no longer describe recrawl as current L0 / L1 threat-model output.
- Historical residuals are classified instead of rewritten.
- No code, schema, label, manifest, split, or dataset files are changed by this task.
- Task and handoff checkers pass.

## 11. Validation Checklist

- [x] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_data_docs_invalid_capture_residual_cleanup_v1.md`
- [x] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_data_docs_invalid_capture_residual_cleanup_v1.md`
- [x] Focused residual grep over `docs`, `AGENTS.md`, `PROJECT.md`, and `README.md`.
- [x] Scope check with `git diff --name-only`.

## 12. Stop Rules

Stop as done when active doc wording is aligned, residuals are classified, required artifacts exist, and required validation has been run or honestly reported.

Stop as blocked if checker failures require changes outside the documented scope, or if residual cleanup would require code/schema/data changes.
