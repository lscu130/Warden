# HANDOFF_20260512_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1

## 中文版

### 摘要

本次交付把 L1 rule baseline 从临时 classifier 语义改为 rule router / evidence sufficiency diagnostic。当前 L1 draft 不再在顶层输出 `label / risk_score / confidence / malicious_basis / payload_observed`。这些 final-like 字段只保留在 `decision_head` stub 内，并且值为 `null`，状态为 `not_run`。

已同步更新 benchmark 统计口径：报告 `rule_assessment distribution`、routing counts、candidate counts、latency、official field mismatch 和 final-like label leakage warning count；不再报告 `benign / suspicious / malicious` label distribution。

验证结果：targeted pytest 18 passed；必跑 py_compile 通过；task checker 通过；bounded benign smoke 跑 50 个样本，runtime success 50，L1 draft ok 50，official mismatch 0，final-like label leakage warning count 为 0。

明确未运行训练、teacher、OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like 路径。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF_20260512_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1
- Related Task ID: TASK_20260511_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1
- Task Title: Realign Warden L1 Rule Router And Decision Head Semantics V1
- Module: Inference / L1
- Author: Codex
- Date: 2026-05-12
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

Realigned the L1 draft skeleton so the rule-only component is a routing and evidence-sufficiency diagnostic component, not a final classifier. The L1 draft result now separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`. The `decision_head` is explicit `not_run` with final-like fields set to `null`. Benchmark reporting now uses rule-assessment and routing metrics, with final-like label leakage detection.

## 2. What Changed

### Code Changes

- Updated `src/warden/l1/rule_baseline.py` to return `rule_assessment`, `routing_assessment`, `routing_hints`, `risk_hints`, `evidence_sufficiency`, `risk_axes`, and `reason_codes`.
- Updated `src/warden/l1/l1_runner.py` to emit the new draft shape with `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`.
- Updated `src/warden/l1/explanation_renderer.py` so explanations are `routing_diagnostic` summaries and do not claim final malicious or benign judgment.
- Updated `src/warden/l1/evidence_ledger.py` wording from rule-baseline decision confidence to rule-router routing confidence.
- Updated `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py` to report routing/assessment distributions and final-like label leakage warnings.
- Updated targeted tests for L1 skeleton, runtime draft integration, and mixed runtime benchmark semantics.

### Doc Changes

- Added `docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`.
- Added this handoff.

### Output / Artifact Changes

- Generated bounded smoke output under `E:\WardenData\manifests\l1_draft_routing_semantics_v1`.

If nothing changed in one category, say `none`.

## 3. Files Touched

- `docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `scripts/l1/run_l1_baseline_smoke.py`
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- `src/warden/l1/__init__.py`
- `src/warden/l1/evidence_ledger.py`
- `src/warden/l1/explanation_renderer.py`
- `src/warden/l1/form_features.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/rule_baseline.py`
- `tests/infer/test_l1_pipeline_skeleton.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_draft_mixed_runtime_benchmark.py`

## 4. Behavior Impact

### Expected New Behavior

- Rule baseline no longer emits top-level `label`, `risk_score`, `confidence`, `malicious_basis`, or `payload_observed`.
- Rule baseline emits routing diagnostics through `rule_router`.
- L1 draft result has `decision_head.status = "not_run"` and null final-like decision fields.
- Explanation renderer emits routing diagnostic text.
- Benchmark reports `rule_assessment_distribution`, routing counts, candidate counts, latency, official mismatch count, and final-like label leakage warning count.

### Preserved Behavior

- `WARDEN_ENABLE_L1_DRAFT` remains default-off.
- Runtime bridge failures remain sidecar errors and do not interrupt official runtime output.
- Official runtime fields remain unchanged under flag-on versus flag-off runs.
- No samples, manifests, labels, or splits were modified.

### User-facing / CLI Impact

- Existing benchmark CLI flags remain valid.
- Benchmark summary/report metric names changed from final-like label distributions to routing/assessment diagnostics.

### Output Format Impact

- L1 draft sidecar shape changed because it is explicitly draft and not final schema.
- Official runtime output schema did not change.

## 5. Schema / Interface Impact

- Schema changed: NO for official runtime schema
- Backward compatible: YES for official runtime output
- Public interface changed: NO for official runtime fields
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- L1 draft debug sidecar only: `rule_router`, `text_semantic_concepts`, `vision_evidence`, `decision_head`

Compatibility notes:

The draft sidecar is marked `draft=true` and `not_final_schema=true`. Any consumer of the old draft-only top-level `label` fields must move to `rule_router` and `decision_head`.

## 6. Validation Performed

### Commands Run

```bash
pytest tests/infer/test_l1_pipeline_skeleton.py tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_draft_mixed_runtime_benchmark.py -q
python -m py_compile src/warden/l1/rule_baseline.py src/warden/l1/l1_runner.py src/warden/l1/explanation_renderer.py src/warden/runtime/l1_draft_bridge.py scripts/l1/run_l1_draft_mixed_runtime_benchmark.py
python scripts/l1/run_l1_draft_mixed_runtime_benchmark.py --benign-val "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --output-dir "E:\WardenData\manifests\l1_draft_routing_semantics_v1" --limit-per-bucket 25 --seed 42
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md
rg -n "label distribution|B00 label|B01 label|suspicious/malicious|final-like label leakage warning count|rule_assessment distribution|routing_need_text_tower_count" "E:\WardenData\manifests\l1_draft_routing_semantics_v1\l1_draft_mixed_runtime_report_v1.md"
```

### Result

- Targeted pytest: `18 passed in 0.37s`.
- Required `py_compile`: exit 0.
- Task doc checker: `[task-doc] OK`.
- Handoff checker: `[handoff-doc] OK`.
- Bounded benign smoke:
  - `total_samples`: 50
  - `runtime_success_count`: 50
  - `runtime_error_count`: 0
  - `l1_draft_ok_count`: 50
  - `official_fields_mismatch_count`: 0
  - `flag_off_debug_sidecar_count`: 0
  - `final_like_label_leakage_warning_count`: 0
  - `rule_assessment_distribution`: `needs_review=26`, `benign_hard_negative_candidate=7`, `needs_text_model_judgment=9`, `low_risk_candidate=3`, `high_risk_candidate=5`
  - routing counts: `need_text_tower=47`, `need_ocr=2`, `need_yolo=14`, `need_review=31`, `need_recrawl=0`
  - latency: `avg_l1_draft_duration_ms=6.246`, `p50=3.584`, `p95=16.603`, `p99=22.791`
- Generated report contains required `rule_assessment distribution`, routing counts, and `final-like label leakage warning count: 0`; no old label-distribution lines were found by the focused report check.

### Not Run

- Full repository pytest.
- Training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SNet, and SpecularNet-like inference.

Reason:

Full repository pytest is broader than the task's required targeted validation. Heavy model, teacher, OCR, detector, and training paths are explicitly out of scope.

Next best check:

Run full repository pytest in a clean worktree or CI job if broader regression confidence is required.

## 7. Risks / Caveats

- The rule router is still heuristic and should not be treated as final model judgment.
- Draft sidecar consumers that expected top-level `label` need to migrate to `rule_router.rule_assessment` or wait for future `decision_head`.
- `high_risk_candidate` remains a routing/review candidate signal, not a final malicious label.
- Bounded smoke used benign validation buckets only; it does not establish malicious coverage.
- Counter-review residual risk: future Decision Head integration may require another draft shape update before final schema freeze.
- Karpathy guardrail residual risk: full repository regression was not run.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`

Doc debt still remaining:

- Historical handoffs from the previous benchmark still record the old result. They were not rewritten because they describe a past run.
- Future active module docs should be updated when L1 Decision Head integration is designed.

## 9. Recommended Next Step

- Review the new draft sidecar shape and benchmark report semantics.
- If accepted, open a separate task for L1 Decision Head interface design or text semantic concept stub contract.
- Keep future calibration tasks focused on router thresholds and avoid treating router output as accuracy.

## 10. Evidence / Retrieval Performed

Evidence sources actually checked:

- user-provided task file from `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_RULE_ROUTER_DECISION_HEAD_REALIGN_V1.md`
- `src/warden/l1/rule_baseline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/explanation_renderer.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/runtime/pipeline.py`
- `scripts/l1/run_l1_draft_mixed_runtime_benchmark.py`
- targeted tests under `tests/infer/`
- bounded smoke outputs under `E:\WardenData\manifests\l1_draft_routing_semantics_v1`

Retrieval / reading performed:

- confirmed existing old final-like rule fields
- confirmed benchmark old label-distribution logic
- confirmed runtime sidecar bridge keeps draft flagging and non-fatal error behavior
- confirmed generated report routing metrics and leakage count

Claims supported by evidence:

- Rule router no longer emits top-level final-like labels in targeted tests and smoke output.
- Runtime official fields matched flag-off outputs in the bounded smoke run.
- Benchmark reports routing semantics and final-like label leakage warning count.

Claims left unsupported or assumed:

- Full repository regression safety remains untested.
- Malicious-sample behavior was not evaluated.

Retrieval stopped because:

- Required task acceptance checks had direct validation evidence.

## 10.1 Counter-Review Performed

Original framing reviewed:

Demote rule baseline from temporary classifier to router / evidence-sufficiency diagnostic, with future final label owned by L1 Decision Head.

Assumptions checked:

- Draft sidecar shape can change because it is marked `not_final_schema`.
- Official runtime fields must remain unchanged.
- Benchmark can report routing metrics without accuracy-like label distributions.

Failure modes considered:

- hidden `label` leakage in nested draft output
- report still containing old label distribution lines
- explanations implying final judgment
- decision head populated from rule-router heuristics

Counterexamples or contradictory evidence found:

- Benign smoke buckets still produce high-risk candidates, which supports keeping these as candidate/routing signals.
- Official field mismatch count was 0, so the sidecar change did not alter official runtime fields in the bounded run.

Alternative routes considered:

- keep old top-level fields with null values
- remove top-level fields and place null final-like fields only under `decision_head`
- defer benchmark changes

Framing changed: NO

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- final Decision Head contract remains future work

Residual risks after counter-review:

- downstream draft consumers may need migration

Decision after counter-review:

- ACCEPT_ORIGINAL

## 10.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- L1 draft sidecar is allowed to change because it is not final schema.
- Official runtime fields must remain stable.

Ambiguities resolved or escalated:

- No blocker. The user-provided task fixed scope, validation, and out-of-scope items.

### Simplicity First

Simplest acceptable route used:

- Update existing rule-router output, runner shape, explanation text, benchmark metrics, and targeted tests without adding dependencies or model paths.

Larger or more speculative routes rejected:

- training a Decision Head
- adding a new model adapter implementation
- changing official runtime schema
- rewriting historical handoffs

### Surgical Changes

Touched-file to task-scope mapping:

- `src/warden/l1/**`: rule router, draft shape, explanation, narrow docstrings
- `scripts/l1/**`: smoke/benchmark wording and routing metrics
- `tests/infer/**`: targeted behavior checks
- `docs/tasks/**` and `docs/handoff/**`: workflow artifacts

Adjacent cleanup or formatting-only changes:

- none outside task scope

### Goal-Driven Verification

Verification loop:

- final-like labels removed from rule baseline output -> targeted pytest and JSONL spot-check
- decision head not run -> targeted pytest
- benchmark routing metrics -> targeted pytest, smoke summary, report grep
- official runtime fields unchanged -> targeted runtime integration pytest and bounded smoke mismatch count 0
