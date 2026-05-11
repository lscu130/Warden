# HANDOFF_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1

## 中文版

### 摘要

本次交付新增了 Warden L1 管线骨架与规则基线 V1。新增内容包括 `src/warden/l1/**` 包、模型 adapter stub、只读 smoke CLI、基础 pytest 覆盖、repo task doc 和本 handoff。实现保持为隔离式内部 draft 路径，未接入现有 runtime 输出契约，未修改冻结 schema、标签、样本、manifest 或训练切分。

实际验证结果：

- 新增 pytest：`7 passed`
- 核心 L1 模块和 CLI：`py_compile` 通过
- 真实 manifest smoke：从 `E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv` 读取 100 行，写出 `E:\WardenData\manifests\l1_smoke_v1\l1_baseline_smoke_results.jsonl`
- 任务文档 checker：通过

明确未运行训练、teacher、OCR、YOLO、CLIP、MobileCLIP、SNet 或 SpecularNet-like 路径。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1
- Related Task ID: TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1
- Task Title: Build Warden L1 Pipeline Skeleton And Rule Baseline V1
- Module: Inference / L1
- Author: Codex
- Date: 2026-05-11
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

Added an isolated Warden L1 skeleton and conservative rule baseline. The new package reads evidence from sample directories or manifest rows, extracts URL / visible text / actionable HTML / forms / network features, derives joint signals, emits reason codes, builds an evidence ledger, renders deterministic explanations, and writes internal draft L1 result JSONL through a read-only smoke CLI. The task stop condition was reached for the requested skeleton and validation scope.

## 2. What Changed

### Code Changes

- Added `src/warden/l1/evidence_pack.py` for source-aware sample evidence loading with missing-artifact and bad-JSON issue recording.
- Added URL, visible-text, actionable-HTML, forms, network, joint-signal, reason-code, evidence-ledger, explanation-renderer, rule-baseline, and runner modules under `src/warden/l1/`.
- Added `TextTowerAdapterStub`, `FusionAdapterStub`, and `VisionEvidenceAdapterStub`; stubs do not load models, access network, run OCR / YOLO / CLIP, or generate explanations.
- Added read-only CLI `scripts/l1/run_l1_baseline_smoke.py` that reads manifest `current_path` rows and writes JSONL draft results.
- Added `tests/infer/test_l1_pipeline_skeleton.py` with coverage for missing files, bad JSON, actionable HTML, forms, reason codes, deterministic explanation, manifest-row input isolation, and CLI smoke.

### Doc Changes

- Added `docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`.
- Added this handoff at `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`.

### Output / Artifact Changes

- Generated smoke output outside the repo at `E:\WardenData\manifests\l1_smoke_v1\l1_baseline_smoke_results.jsonl`.

## 3. Files Touched

- `docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`
- `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`
- `scripts/l1/run_l1_baseline_smoke.py`
- `src/warden/l1/__init__.py`
- `src/warden/l1/evidence_pack.py`
- `src/warden/l1/url_features.py`
- `src/warden/l1/text_features.py`
- `src/warden/l1/html_action_extractor.py`
- `src/warden/l1/form_features.py`
- `src/warden/l1/network_features.py`
- `src/warden/l1/joint_signals.py`
- `src/warden/l1/evidence_ledger.py`
- `src/warden/l1/reason_codes.py`
- `src/warden/l1/explanation_renderer.py`
- `src/warden/l1/rule_baseline.py`
- `src/warden/l1/l1_runner.py`
- `src/warden/l1/model_adapters/__init__.py`
- `src/warden/l1/model_adapters/text_tower_stub.py`
- `src/warden/l1/model_adapters/fusion_stub.py`
- `src/warden/l1/model_adapters/vision_stub.py`
- `tests/infer/test_l1_pipeline_skeleton.py`

## 4. Behavior Impact

### Expected New Behavior

- `warden.l1.run_l1_baseline_for_sample(path)` returns an internal draft L1 result dict.
- `warden.l1.run_l1_baseline_for_manifest_row(row)` reads only `current_path` from manifest rows and does not place labels or split metadata into evidence text.
- The smoke CLI writes one draft L1 result JSON object per processed manifest row.
- Missing files, bad JSON, and malformed HTML are tolerated and recorded through `missing_artifacts` and `issues`.
- Actionable HTML extraction supports `form`, `input`, `button`, `a`, `iframe`, `script`, `select`, `textarea`, `title`, `meta`, and heading tags.

### Preserved Behavior

- Existing runtime pipeline files were not edited.
- Existing schemas, labels, manifests, source samples, and train / val / test splits were not edited.
- Existing CLI behavior was not changed.

### User-facing / CLI Impact

- New CLI added: `python scripts/l1/run_l1_baseline_smoke.py --manifest <csv> --limit <n> --output <jsonl>`.
- No existing CLI was modified.

### Output Format Impact

- New output only: internal draft JSONL result from the new smoke CLI.
- Draft fields include `label`, `risk_score`, `confidence`, `malicious_basis`, `payload_observed`, `page_role`, `risk_axes`, `routing`, `reason_codes`, `evidence_ledger`, and `explanation`.
- This delivery does not freeze a final project output schema.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The new `warden.l1` package is isolated. It introduces a new internal draft result shape and a new smoke CLI output, while preserving current runtime result / trace contracts and existing manifests.

## 6. Validation Performed

### Commands Run

```bash
pytest tests/infer/test_l1_pipeline_skeleton.py -q
python -m py_compile src/warden/l1/evidence_pack.py
python -m py_compile src/warden/l1/html_action_extractor.py
python -m py_compile src/warden/l1/l1_runner.py
python -m py_compile scripts/l1/run_l1_baseline_smoke.py
python scripts/l1/run_l1_baseline_smoke.py --manifest "E:\WardenData\manifests\benign_clean_v1\benign_val_manifest_v1.csv" --limit 100 --output "E:\WardenData\manifests\l1_smoke_v1\l1_baseline_smoke_results.jsonl"
python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md
```

### Result

- `pytest tests/infer/test_l1_pipeline_skeleton.py -q`: `7 passed in 0.17s`.
- `py_compile` commands exited 0.
- Real manifest smoke wrote `100` rows to `E:\WardenData\manifests\l1_smoke_v1\l1_baseline_smoke_results.jsonl`.
- Smoke output spot-check parsed the first JSONL row and confirmed draft result, features, evidence ledger, and explanation are present.
- Task doc checker returned `[task-doc] OK`.
- Handoff checker returned `[handoff-doc] OK`.

### Not Run

- Full repository pytest.
- Training, teacher distillation, OCR, YOLO, CLIP, MobileCLIP, SNet, and SpecularNet-like inference.

Reason:

Full repository pytest is broader than the task's targeted validation scope and the worktree already contains many unrelated user changes. Heavy model, teacher, OCR, detector, and training paths are explicitly out of scope.

Next best check:

For broader regression confidence, run full repository pytest in a clean worktree or isolated CI job.

## 7. Risks / Caveats

- The rule baseline is heuristic and conservative. It must not be treated as ground-truth labeling or final production judgment.
- `registrable_domain_approx` is a standard-library approximation and does not use the public suffix list.
- HTML parsing is tolerant and non-rendering. Browser-rendered behavior, SPA state, OCR text, and detector-localized UI remain future work.
- The generated smoke output is outside the repository under `E:\WardenData`; it is a runtime artifact and was not added to git.
- Counter-review residual risk: future schema freeze may rename or reshape the draft result fields.
- Karpathy guardrail residual risk: full repo tests were not run because the required stop rule was targeted validation plus smoke.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`
- `docs/handoff/2026-05-11_warden_l1_pipeline_skeleton_rule_baseline_v1.md`

Doc debt still remaining:

- A later task should update module docs if this skeleton becomes the active runtime L1 path.
- A later schema task should freeze final L1 output fields before downstream consumers depend on them.

## 9. Recommended Next Step

- Run a review pass against the new isolated `warden.l1` package and this handoff.
- If accepted, create a follow-up task to wire the L1 skeleton into the existing runtime pipeline behind an explicit compatibility boundary.
- Later tasks can integrate a real text tower, a real fusion head, OCR / YOLO adapters, teacher distillation after dataset freeze, final L1 output schema freeze, and latency profiling.

## 10. Evidence / Retrieval Performed

Evidence sources actually checked:

- user-provided task document from `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L1_PIPELINE_SKELETON_RULE_BASELINE_V1.md`
- `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `src/warden/runtime/core.py`, `src/warden/runtime/pipeline.py`, `src/warden/module/l1.py`
- `scripts/data/common/html_payload_utils.py`, `scripts/data/common/io_utils.py`
- `scripts/ci/check_task_doc.py`, `scripts/ci/check_handoff_doc.py`
- local command outputs listed in validation

Retrieval / reading performed:

- confirmed existing `src/warden` package layout
- confirmed current project rule excluding default online CLIP / SNet path
- confirmed current `SampleContext` and runtime dataflow context
- confirmed checkers' required markers

Claims supported by evidence:

- `src/warden/l1` fits the existing package style.
- Current docs define L1 as a staged main judgment layer with evidence ledger and deterministic explanation rendering.
- Current task explicitly prohibits training, teacher, OCR, YOLO, CLIP, SNet, schema, label, sample, manifest, and split changes.

Claims left unsupported or assumed:

- Full-repo regression safety beyond the targeted tests was not established.
- Rule baseline quality on malicious samples was not measured.

Retrieval stopped because:

- Required implementation and validation evidence for the task scope was available.

## 10.1 Counter-Review Performed

Original framing reviewed:

Build an L1 skeleton and rule baseline now, keeping heavy models, training, final schema freeze, and runtime integration for later tasks.

Assumptions checked:

- `src/warden/l1` is compatible with current repository package layout.
- Internal draft result fields can exist without changing frozen schema.
- Smoke CLI can read manifest rows and write JSONL without modifying samples or manifests.

Failure modes considered:

- one-factor rules treating login, download, wallet, support, or brand tokens as malicious
- label or folder metadata entering evidence text
- model stubs generating explanations or invoking heavy routes
- draft output being misrepresented as final schema

Counterexamples or contradictory evidence found:

- The first benign smoke row contained a form and many actionable HTML nodes, yet the baseline produced `benign`, showing login/form presence alone was not used as a malicious rule.
- No repository evidence required changing existing runtime output contracts.

Alternative routes considered:

- docs-only delivery
- direct existing-runtime integration
- isolated skeleton package with separate smoke CLI

Framing changed: NO

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- final thresholds are provisional
- malicious detection quality remains unevaluated

Residual risks after counter-review:

- future runtime integration may require interface tightening
- a final schema task may change draft field names

Decision after counter-review:

- ACCEPT_ORIGINAL

## 10.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- The new package should stay isolated from existing runtime to avoid changing current contracts.
- Draft fields are internal to this task and are not final frozen schema.

Ambiguities resolved or escalated:

- No need to clarify because the external task gave explicit scope, out-of-scope list, acceptance criteria, and validation commands.

### Simplicity First

Simplest acceptable route used:

- Standard-library feature extractors, deterministic rule baseline, model stubs, focused tests, and a read-only CSV-to-JSONL CLI.

Larger or more speculative routes rejected:

- direct runtime integration
- dependency additions
- browser rendering
- model loading or training

### Surgical Changes

Touched-file to task-scope mapping:

- `src/warden/l1/**`: L1 skeleton package
- `scripts/l1/run_l1_baseline_smoke.py`: smoke CLI
- `tests/infer/test_l1_pipeline_skeleton.py`: required tests
- `docs/tasks/**` and `docs/handoff/**`: required workflow artifacts

Adjacent cleanup or formatting-only changes:

- none outside newly added files

### Goal-Driven Verification

Verification loop:

- L1 skeleton imports and core modules compile -> `py_compile` exited 0
- required behavior coverage -> targeted pytest reported `7 passed`
- real manifest smoke -> wrote 100 JSONL rows and first-row spot-check parsed
- workflow artifacts -> task checker passed; handoff checker pending immediately after file creation
