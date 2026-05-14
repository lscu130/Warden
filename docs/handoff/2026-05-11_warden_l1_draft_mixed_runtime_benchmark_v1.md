# Warden L1 Draft Mixed Runtime Benchmark V1 Handoff

## 中文版

> 面向人类阅读的摘要版。英文版为权威执行记录；若精确命令、验证结果、兼容性结论或未运行项有冲突，以英文版为准。

# Handoff Metadata

- Handoff ID: `HANDOFF-20260511-WARDEN-L1-DRAFT-MIXED-RUNTIME-BENCHMARK-V1`
- Related Task ID: `TASK-20260511-WARDEN-L1-DRAFT-MIXED-RUNTIME-BENCHMARK-V1`
- Task Title: `Run Bounded Mixed Runtime Benchmark For L1 Draft Sidecar`
- Module: `Runtime / L1 / Benchmark / Smoke`
- Author: `Codex`
- Date: `2026-05-11`
- Status: `DONE`

## 1. Executive Summary

本次交付新增并运行了只读 L1 draft mixed runtime benchmark。实际输入为 `benign_val_manifest_v1.csv`，按 `seed=42` 和 `limit-per-bucket=25` 抽取 `B00_benign_clear=25` 与 `B01_benign_hard_negative=25`，共 `50` 条。未提供 malicious manifest，因此 malicious buckets 为空。

结果显示 runtime 接线稳定：`runtime_success_count=50`，`runtime_error_count=0`，`l1_draft_ok_count=50`，`missing_sidecar_count=0`，flag-on / flag-off 官方字段 mismatch 为 `0`。规则路由 sanity 方面，当前 L1 draft rule baseline 对 benign 样本偏激进：`B00` 中 `18/25` 为 suspicious，`B01` 中 `18/25` 为 suspicious、`5/25` 为 malicious。该结果是规则基线校准信号，不是最终模型准确率结论。

## 2. What Changed

### Code Changes

- 新增 `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`。
- 新增 `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`。

### Doc Changes

- 新增 `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`。
- 新增 `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`。

### Output / Artifact Changes

新增输出目录：

- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`

生成文件：

- `l1_draft_mixed_runtime_results_v1.jsonl`
- `l1_draft_mixed_runtime_summary_v1.csv`
- `l1_draft_mixed_runtime_report_v1.md`
- `l1_draft_mixed_runtime_errors_v1.csv`

## 3. Files Touched

- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- 可以通过 benchmark 脚本对 bounded mixed sample set 执行 flag-off / flag-on runtime 对照。
- 每条样本记录 official runtime 字段、L1 draft sidecar 状态、duration、label/routing/reason/evidence summary。
- Runtime 或 sidecar error 会被记录到结果中，不中断整个 benchmark。

### Preserved Behavior

- 未修改 runtime pipeline 行为。
- 未修改正式 runtime schema。
- 未修改样本、标签或 split。
- L1 draft 仍然是 draft/debug sidecar，不作为 final judgment、training label 或 benchmark metric。

### User-facing / CLI Impact

- 新增只读 CLI：`python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py ...`
- 现有 runtime CLI 默认行为不变。

### Output Format Impact

- 官方 runtime output contract 未改变。
- 新增 benchmark artifact schema，仅用于本次 smoke/report。

## 5. Schema / Interface Impact

- Schema changed: `NO official runtime schema change`
- Backward compatible: `YES`
- Public interface changed: `YES, new benchmark CLI only`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- 新增 benchmark JSONL/CSV/report 输出字段。
- 未新增或修改正式 runtime result/trace 字段。

Compatibility notes:

Benchmark artifacts are external report artifacts. They must not be treated as frozen runtime schema.

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile scripts/l1/run_l1_draft_mixed_runtime_benchmark.py
pytest tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q
python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_mixed_benchmark_v1" --limit-per-bucket 25 --seed 42
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md
```

### Result

- `py_compile`: passed.
- Targeted pytest: `4 passed in 0.11s`.
- Task doc checker: passed.
- Handoff doc checker: passed.
- Actual input manifest: `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`.
- Output directory: `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`.
- Actual sampled buckets: `B00_benign_clear=25`, `B01_benign_hard_negative=25`.
- `total_samples=50`.
- `runtime_success_count=50`.
- `runtime_error_count=0`.
- `l1_draft_ok_count=50`.
- `l1_draft_error_count=0`.
- `missing_sidecar_count=0`.
- `official_fields_mismatch_count=0`.
- `flag_off_debug_sidecar_count=0`.
- `avg_l1_draft_duration_ms=5.760`.
- `p50_l1_draft_duration_ms=3.230`.
- `p95_l1_draft_duration_ms=17.375`.
- `p99_l1_draft_duration_ms=22.078`.
- `avg_total_runtime_duration_ms=49.767`.
- `routing_need_ocr_count=2`.
- `routing_need_yolo_count=14`.
- `routing_need_review_count=28`.
- `routing_need_recrawl_count=0`.
- `B00 label distribution`: `suspicious=18`, `benign=7`.
- `B00 high risk count`: `0`.
- `B01 label distribution`: `suspicious=18`, `benign=2`, `malicious=5`.
- `B01 high risk count`: `5`.
- `B01 need_review count`: `13`.
- `B01 need_ocr count`: `2`.

Top reason codes:

- `payload_not_observed=43`
- `support_surface_present=34`
- `download_surface_present=30`
- `need_review_for_conflict=28`
- `html_action_sparse=23`
- `benign_hard_negative_candidate=20`
- `financial_context_present=18`
- `security_urgency_context_present=15`
- `login_surface_present=15`
- `need_yolo_for_ui_localization=14`

Rule-routing review:

- No one-factor final-accuracy claim was made.
- The current rule baseline pushes many benign pages to suspicious and pushes `5/25` B01 hard-negative samples to malicious.
- Treat this as calibration evidence for the L1 rule baseline. It is not final accuracy and should not be used as a model metric.

### Not Run

- Training was not run.
- Teacher distillation was not run.
- OCR was not run.
- YOLO was not run.
- CLIP / MobileCLIP was not run.
- SNet / SpecularNet-like inference was not run.
- Malicious benchmark coverage was not run because no malicious manifest was supplied.
- Full dataset benchmark was not run.
- Frozen schema promotion was not run.

## 7. Risks / Caveats

- This benchmark measures runtime wiring, sidecar completeness, rule-routing sanity, and latency. It is not a final model accuracy benchmark.
- Current L1 draft output is not frozen schema.
- Malicious buckets are empty in this run.
- Current rule baseline appears too aggressive on benign hard negatives and also marks many B00 samples suspicious; this should be handled in a separate rule calibration task.
- The repository had a large dirty worktree before this task started. This handoff only claims the files listed above and the benchmark output directory.

## 8. Docs Impact

- Docs updated: `YES`
- Task doc added.
- Handoff doc added.
- Benchmark report generated under `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`.

## 9. Recommended Next Step

- Open a narrow `L1 rule baseline calibration` task focused on reducing benign hard-negative over-triggering without using draft output as final accuracy.
- If malicious manifests become available, rerun the same benchmark with malicious buckets enabled.

## English Version

> AI note: The English section is authoritative for exact validation, compatibility, and follow-up boundaries.

# Handoff Metadata

- Handoff ID: `HANDOFF-20260511-WARDEN-L1-DRAFT-MIXED-RUNTIME-BENCHMARK-V1`
- Related Task ID: `TASK-20260511-WARDEN-L1-DRAFT-MIXED-RUNTIME-BENCHMARK-V1`
- Task Title: `Run Bounded Mixed Runtime Benchmark For L1 Draft Sidecar`
- Module: `Runtime / L1 / Benchmark / Smoke`
- Author: `Codex`
- Date: `2026-05-11`
- Status: `DONE`

## 1. Executive Summary

This delivery adds and runs a read-only L1 draft mixed runtime benchmark. The actual input was `benign_val_manifest_v1.csv`, sampled with `seed=42` and `limit-per-bucket=25`, producing `B00_benign_clear=25` and `B01_benign_hard_negative=25`, for `50` total samples. No malicious manifest was supplied, so malicious buckets are empty.

Runtime wiring was stable: `runtime_success_count=50`, `runtime_error_count=0`, `l1_draft_ok_count=50`, `missing_sidecar_count=0`, and flag-on / flag-off official field mismatch count was `0`. Rule-routing sanity showed that the current L1 draft rule baseline is too aggressive on benign samples: `B00` had `18/25` suspicious, and `B01` had `18/25` suspicious plus `5/25` malicious. This is rule-baseline calibration evidence, not a final model accuracy result.

## 2. What Changed

### Code Changes

- Added `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`.
- Added `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`.

### Doc Changes

- Added `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`.
- Added `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`.

### Output / Artifact Changes

Added output directory:

- `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`

Generated files:

- `l1_draft_mixed_runtime_results_v1.jsonl`
- `l1_draft_mixed_runtime_summary_v1.csv`
- `l1_draft_mixed_runtime_report_v1.md`
- `l1_draft_mixed_runtime_errors_v1.csv`

## 3. Files Touched

- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`
- `docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`
- `docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- The benchmark script can run flag-off / flag-on runtime comparisons over a bounded mixed sample set.
- Each sample records official runtime fields, L1 draft sidecar status, duration, label/routing/reason/evidence summary.
- Runtime or sidecar errors are recorded in the results and do not abort the whole benchmark.

### Preserved Behavior

- Runtime pipeline behavior was not modified.
- Official runtime schema was not modified.
- Samples, labels, and splits were not modified.
- L1 draft remains a draft/debug sidecar and is not used as final judgment, training label, or benchmark metric.

### User-facing / CLI Impact

- Added read-only CLI: `python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py ...`
- Existing runtime CLI default behavior remains unchanged.

### Output Format Impact

- Official runtime output contract was not changed.
- New benchmark artifact schema exists only for this smoke/report output.

## 5. Schema / Interface Impact

- Schema changed: `NO official runtime schema change`
- Backward compatible: `YES`
- Public interface changed: `YES, new benchmark CLI only`
- Existing CLI still valid: `YES`

Affected schema fields / interfaces:

- New benchmark JSONL/CSV/report output fields.
- No official runtime result/trace fields were added or modified.

Compatibility notes:

Benchmark artifacts are external report artifacts. They must not be treated as frozen runtime schema.

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile scripts/l1/run_l1_draft_mixed_runtime_benchmark.py
pytest tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q
python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_mixed_benchmark_v1" --limit-per-bucket 25 --seed 42
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_draft_mixed_runtime_benchmark_v1.md
```

### Result

- `py_compile`: passed.
- Targeted pytest: `4 passed in 0.11s`.
- Task doc checker: passed.
- Handoff doc checker: passed.
- Actual input manifest: `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv`.
- Output directory: `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`.
- Actual sampled buckets: `B00_benign_clear=25`, `B01_benign_hard_negative=25`.
- `total_samples=50`.
- `runtime_success_count=50`.
- `runtime_error_count=0`.
- `l1_draft_ok_count=50`.
- `l1_draft_error_count=0`.
- `missing_sidecar_count=0`.
- `official_fields_mismatch_count=0`.
- `flag_off_debug_sidecar_count=0`.
- `avg_l1_draft_duration_ms=5.760`.
- `p50_l1_draft_duration_ms=3.230`.
- `p95_l1_draft_duration_ms=17.375`.
- `p99_l1_draft_duration_ms=22.078`.
- `avg_total_runtime_duration_ms=49.767`.
- `routing_need_ocr_count=2`.
- `routing_need_yolo_count=14`.
- `routing_need_review_count=28`.
- `routing_need_recrawl_count=0`.
- `B00 label distribution`: `suspicious=18`, `benign=7`.
- `B00 high risk count`: `0`.
- `B01 label distribution`: `suspicious=18`, `benign=2`, `malicious=5`.
- `B01 high risk count`: `5`.
- `B01 need_review count`: `13`.
- `B01 need_ocr count`: `2`.

Top reason codes:

- `payload_not_observed=43`
- `support_surface_present=34`
- `download_surface_present=30`
- `need_review_for_conflict=28`
- `html_action_sparse=23`
- `benign_hard_negative_candidate=20`
- `financial_context_present=18`
- `security_urgency_context_present=15`
- `login_surface_present=15`
- `need_yolo_for_ui_localization=14`

Rule-routing review:

- No one-factor final-accuracy claim was made.
- The current rule baseline pushes many benign pages to suspicious and pushes `5/25` B01 hard-negative samples to malicious.
- Treat this as calibration evidence for the L1 rule baseline. It is not final accuracy and should not be used as a model metric.

### Not Run

- Training was not run.
- Teacher distillation was not run.
- OCR was not run.
- YOLO was not run.
- CLIP / MobileCLIP was not run.
- SNet / SpecularNet-like inference was not run.
- Malicious benchmark coverage was not run because no malicious manifest was supplied.
- Full dataset benchmark was not run.
- Frozen schema promotion was not run.

## 7. Risks / Caveats

- This benchmark measures runtime wiring, sidecar completeness, rule-routing sanity, and latency. It is not a final model accuracy benchmark.
- Current L1 draft output is not frozen schema.
- Malicious buckets are empty in this run.
- Current rule baseline appears too aggressive on benign hard negatives and also marks many B00 samples suspicious; this should be handled in a separate rule calibration task.
- The repository had a large dirty worktree before this task started. This handoff only claims the files listed above and the benchmark output directory.

## 8. Docs Impact

- Docs updated: `YES`
- Task doc added.
- Handoff doc added.
- Benchmark report generated under `E:\WardenData\manifests\l1_draft_mixed_benchmark_v1`.

## 9. Recommended Next Step

- Open a narrow `L1 rule baseline calibration` task focused on reducing benign hard-negative over-triggering without using draft output as final accuracy.
- If malicious manifests become available, rerun the same benchmark with malicious buckets enabled.
