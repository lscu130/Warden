# Warden L1 Draft Mixed Runtime Benchmark V1

## 中文版

> 面向人类阅读的摘要版。英文版为权威执行版本；若精确范围、字段、验收或验证要求有冲突，以英文版为准。

## 1. 背景

`warden.l1` draft sidecar 已通过 `WARDEN_ENABLE_L1_DRAFT=1` 接入 runtime，默认关闭时不新增 `debug_sidecars`，开启时只追加 draft/debug sidecar。前置任务只完成了单样本 smoke，因此需要一个有界 mixed runtime benchmark 来验证混合样本上的接线稳定性、sidecar 完整性、规则路由 sanity 和延迟。

## 2. 目标

新增只读 benchmark 脚本，从 bounded mixed sample set 采样并运行 flag-off / flag-on runtime 对照，输出 JSONL、summary CSV、Markdown report 和 errors CSV。该任务不是最终模型准确率评估，不训练、不改标签、不移动样本、不改 frozen schema。

## 3. Scope In

允许触碰：

- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`

允许生成输出：

- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_results_v1.jsonl`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_summary_v1.csv`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_report_v1.md`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_errors_v1.csv`
- runtime smoke subdirectories under the same output root.

## 4. Scope Out

不得：

- 训练模型；
- 跑 teacher distillation；
- 跑 OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like inference；
- 修改 frozen schema；
- 修改正式 runtime output contract；
- 修改人工标签；
- 移动、删除或重命名样本；
- 重新切分 train/val/test；
- 把 L1 draft 当最终模型指标；
- 把 L1 draft 输出写入训练标签。

## 5. Inputs

相关输入：

- `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_DRAFT_MIXED_RUNTIME_BENCHMARK_V1.md`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `src/warden/runtime/pipeline.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`

缺失项：

- 未提供 malicious manifest。本任务允许 malicious buckets 为空，并先完成 benign T00/T01 coverage。

## 6. Required Outputs

- Benchmark script。
- Focused pytest。
- Benchmark JSONL。
- Benchmark summary CSV。
- Benchmark Markdown report。
- Error samples CSV，即使无错误也生成空 CSV。
- Repo-local task doc。
- Repo-local handoff doc。

## 7. Hard Constraints

- Benchmark 必须以 `WARDEN_ENABLE_L1_DRAFT=1` 运行 flag-on runtime。
- 至少验证 flag-off 无 `debug_sidecars`。
- 至少验证 flag-on 有 `debug_sidecars.l1_draft`。
- 必须对比 flag-on / flag-off 官方字段：`final_stage`、`terminal_routing`、`routing_outcome`、`stage_sequence`。
- Runtime error 必须写入结果，不得中断整个 benchmark。
- 不修改样本、标签、split 或正式 runtime schema。

## 8. Interface / Schema Constraints

- Schema changed: `NO official runtime schema change`
- Benchmark artifacts are new output files only.
- `debug_sidecars.l1_draft` remains draft/debug and not frozen schema.
- Existing runtime CLI default behavior remains unchanged.

## 9. Execution Notes

- 默认使用 `benign_val_manifest_v1.csv`。
- `T00_clear_benign` 映射到 `B00_benign_clear`。
- `T01_benign_hard_negative` 映射到 `B01_benign_hard_negative`。
- malicious buckets may be empty if no malicious manifest is supplied.

## 10. Acceptance Criteria

- Benchmark script exists and passes `py_compile`.
- Script can sample and run benign T00/T01 samples.
- Flag-on runtime produces `debug_sidecars.l1_draft`.
- Sidecar has `draft=true` and `not_final_schema=true`.
- JSONL / CSV / Markdown report are generated.
- Report includes bucket counts, runtime success/error, duration summary, routing counts, and reason-code summary.
- Runtime errors are recorded without aborting the whole benchmark.
- No official runtime schema is changed.
- No labels/samples/splits are modified.
- Handoff states this is a runtime/routing smoke benchmark, not final accuracy evaluation.

## 11. Validation Checklist

- `python -m py_compile scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `pytest tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q`
- `python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_mixed_benchmark_v1" --limit-per-bucket 25 --seed 42`
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative execution contract.

# Task Metadata

- Task ID: `TASK-20260511-WARDEN-L1-DRAFT-MIXED-RUNTIME-BENCHMARK-V1`
- Task Title: `Run Bounded Mixed Runtime Benchmark For L1 Draft Sidecar`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Runtime / L1 / Benchmark / Smoke`
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_DRAFT_MIXED_RUNTIME_BENCHMARK_V1.md`; `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`; `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- Created At: `2026-05-11`
- Requested By: `User`
- Karpathy Guardrails Required: `YES`

## 1. Background

The `warden.l1` draft sidecar has been integrated into runtime behind `WARDEN_ENABLE_L1_DRAFT=1`. The previous integration task only ran a single-sample smoke. This task adds a bounded mixed runtime benchmark to verify integration stability, draft sidecar completeness, rule-routing sanity, and latency.

## 2. Goal

Add a read-only benchmark script that samples a bounded mixed sample set, runs flag-off / flag-on runtime comparisons, and writes JSONL, summary CSV, Markdown report, and errors CSV. This is not a final model accuracy evaluation, and it must not train models, modify labels, move samples, or change frozen runtime schema.

## 3. Scope In

This task is allowed to touch:

- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`

This task is allowed to generate:

- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_results_v1.jsonl`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_summary_v1.csv`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_report_v1.md`
- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1\l1_draft_mixed_runtime_errors_v1.csv`
- runtime smoke subdirectories under the same output root.

## 4. Scope Out

This task must not:

- train models;
- run teacher distillation;
- run OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference;
- modify frozen schema;
- modify official runtime output contract;
- change manual labels;
- move, delete, or rename samples;
- re-split train/val/test;
- treat L1 draft as final model metric;
- write L1 draft output into training labels.

## 5. Inputs

Relevant inputs:

- `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_DRAFT_MIXED_RUNTIME_BENCHMARK_V1.md`
- `docs/tasks/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `docs/handoff/2026-05-11_warden_l1_runtime_draft_integration_v1.md`
- `src/warden/runtime/pipeline.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`

Missing inputs:

- No malicious manifest was supplied. This task allows malicious buckets to remain empty and first validates benign T00/T01 coverage.

## 6. Required Outputs

- Benchmark script.
- Focused pytest.
- Benchmark JSONL.
- Benchmark summary CSV.
- Benchmark Markdown report.
- Error samples CSV, even when empty.
- Repo-local task document.
- Repo-local handoff document.

## 7. Hard Constraints

- Benchmark must run flag-on runtime with `WARDEN_ENABLE_L1_DRAFT=1`.
- Benchmark must verify flag-off output has no `debug_sidecars`.
- Benchmark must verify flag-on output has `debug_sidecars.l1_draft`.
- Benchmark must compare official flag-on / flag-off fields: `final_stage`, `terminal_routing`, `routing_outcome`, and `stage_sequence`.
- Runtime errors must be recorded without aborting the benchmark.
- Do not modify samples, labels, splits, or official runtime schema.

## 8. Interface / Schema Constraints

- Schema changed: `NO official runtime schema change`.
- Benchmark artifacts are new output files only.
- `debug_sidecars.l1_draft` remains draft/debug and not frozen schema.
- Existing runtime CLI default behavior remains unchanged.

## 9. Execution Notes

- Default input is `benign_val_manifest_v1.csv`.
- `T00_clear_benign` maps to `B00_benign_clear`.
- `T01_benign_hard_negative` maps to `B01_benign_hard_negative`.
- Malicious buckets may be empty when no malicious manifest is supplied.

## 10. Acceptance Criteria

- Benchmark script exists and passes `py_compile`.
- It can sample and run benign T00/T01 samples.
- Flag-on runtime produces `debug_sidecars.l1_draft`.
- Sidecar has `draft=true` and `not_final_schema=true`.
- JSONL, CSV, and Markdown report are generated.
- Report includes bucket counts, runtime success/error, duration summary, routing counts, and reason-code summary.
- Runtime errors are recorded without aborting the whole benchmark.
- No official runtime schema is changed.
- No labels/samples/splits are modified.
- Handoff states this is a runtime/routing smoke benchmark, not final accuracy evaluation.

## 11. Validation Checklist

- `python -m py_compile scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `pytest tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q`
- `python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_mixed_benchmark_v1" --limit-per-bucket 25 --seed 42`
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
