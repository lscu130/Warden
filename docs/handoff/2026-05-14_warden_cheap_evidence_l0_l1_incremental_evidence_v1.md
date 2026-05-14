# 2026-05-14 Warden Cheap Evidence L0/L1 Incremental Evidence V1 Handoff

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分仅用于人工快速阅读。

### 中文摘要

本次交付完成了任务要求的最小 runtime 改动：新增内部 `CheapEvidenceSnapshot`，L0 前只构建一次 cheap snapshot，L0 消费该 snapshot；只有官方 runtime 路径进入 L1 后，才允许 L1 draft sidecar 做增量 evidence pack 展开，并把 snapshot 传入 L1 draft runner 复用 URL / text / forms / network / artifact presence 等 cheap 证据。

正式 runtime result / trace schema 版本保持不变。L1 draft sidecar 仍标记为 `draft=true` 和 `not_final_schema=true`。未修改数据、manifest、split、标签、训练、蒸馏、OCR、YOLO、CLIP、SNet 或 L2 架构。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF-20260514-WARDEN-CHEAP-EVIDENCE-L0-L1-INCREMENTAL-EVIDENCE-V1
- Related Task ID: TASK-20260514-WARDEN-CHEAP-EVIDENCE-L0-L1-INCREMENTAL-EVIDENCE-V1
- Task Title: Implement CheapEvidenceSnapshot And Incremental L1 Evidence Pack Expansion
- Module: Runtime / Inference / L0 / L1 / Evidence Construction
- Author: Codex
- Date: 2026-05-14
- Status: DONE

---

## 1. Executive Summary

Implemented an internal cheap evidence snapshot and wired runtime/L1 draft evidence construction to reuse it. L0 now receives an explicit `cheap_evidence_snapshot_v1` input contract, L1 input bundles record snapshot reuse, and the L1 draft sidecar only runs after the official runtime path has entered L1. The task stop condition was reached with targeted validation passing.

---

## 2. What Changed

### Code Changes

- Added `CheapEvidenceSnapshot` to runtime core and cached it on `SampleContext`.
- Added `build_cheap_evidence_snapshot()` in the runtime pipeline and kept `prepare_shared_evidence()` as a compatibility wrapper.
- Updated L0 runtime input contract to identify the cheap snapshot and avoid full L1 extraction before L0 routing.
- Updated L1 input bundle and draft bridge to pass the cheap snapshot into L1 draft evidence construction.
- Updated L1 evidence pack and runner to accept `cheap_snapshot`, reuse cheap URL/text/forms/network/artifact fields, and expose draft-only evidence-construction metadata.
- Guarded L1 draft sidecar attachment so L0 terminal samples do not trigger full L1 draft expansion.

### Doc Changes

- Added the repo-local task doc at `docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`.
- Added this repo-local handoff doc.

### Output / Artifact Changes

- Official runtime result / trace schema versions remain unchanged.
- Draft/debug L1 sidecar can include `evidence_construction` metadata showing incremental snapshot reuse.

---

## 3. Files Touched

- `docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`
- `docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`
- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/l1/evidence_pack.py`
- `src/warden/l1/l1_runner.py`
- `tests/infer/test_l1_runtime_draft_integration.py`
- `tests/infer/test_l1_pipeline_skeleton.py`

Note: the worktree already contained unrelated dirty files before this task. They were not intentionally modified for this task.

---

## 4. Behavior Impact

### Expected New Behavior

- Runtime builds one internal `CheapEvidenceSnapshot` before L0 and caches it on `SampleContext`.
- L0 consumes cheap snapshot data and does not run full L1 evidence-pack expansion.
- L0 terminal auxiliary samples do not attach or run the L1 draft sidecar even when `WARDEN_ENABLE_L1_DRAFT=1`.
- L0 non-terminal samples enter L1, and L1 draft evidence construction reuses the cheap snapshot when the draft sidecar is enabled.

### Preserved Behavior

- `WARDEN_ENABLE_L1_DRAFT=0` still produces no L1 draft sidecar.
- L1 draft sidecar remains `draft=true` and `not_final_schema=true`.
- Rule Router remains a routing/evidence-sufficiency diagnostic path, not a final classifier.
- Invalid-capture-like samples remain diagnostic-only in targeted tests and do not receive benign/malicious/suspicious labels.

### User-facing / CLI Impact

- No CLI flag or command behavior was intentionally changed.

### Output Format Impact

- Official runtime output schema changed: no.
- Draft/debug sidecar output can include the new `evidence_construction` object. This is draft-only and not a frozen final schema.

---

## 5. Schema / Interface Impact

- Schema changed: NO for official runtime result / trace schema.
- Backward compatible: YES for official runtime result / trace schema and existing CLI behavior.
- Public interface changed: NO.
- Existing CLI still valid: YES.

Affected schema fields / interfaces:

- Internal dataclass added: `CheapEvidenceSnapshot`.
- Internal compatibility wrapper retained: `prepare_shared_evidence(context)`.
- Draft-only L1 runner signature now accepts optional keyword `cheap_snapshot`.

Compatibility notes:

Official runtime schema versions remain `warden_runtime_result_v0_2` and `warden_runtime_trace_v0_2`. The optional L1 draft sidecar is debug/draft output and remains explicitly marked as not final schema.

---

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- External task file in `C:\Users\20516\Downloads\TASK_20260514_WARDEN_CHEAP_EVIDENCE_L0_L1_INCREMENTAL_EVIDENCE_V1.md`.
- Governing docs: `AGENTS.md`, `PROJECT.md`, workflow and task/handoff templates.
- Runtime files: `src/warden/runtime/core.py`, `pipeline.py`, `l1_draft_bridge.py`.
- L1 files: `src/warden/l1/evidence_pack.py`, `l1_runner.py`.
- Targeted tests under `tests/infer/`.
- Latest related handoff context under `docs/handoff/`.

Retrieval / reading performed:

- Inspected current runtime entrypoints, stage routing, L1 draft attachment, and result/trace generation.
- Inspected current L1 evidence-pack construction and draft runner shape.
- Inspected existing runtime and L1 tests before adding targeted assertions.

Claims supported by evidence:

- `SampleContext` can carry internal per-sample state without changing official runtime output.
- Existing L1 draft evidence construction could be adapted with an optional `cheap_snapshot` input.
- Existing runtime stage trace can determine whether L1 was officially entered.

Claims left unsupported or assumed:

- No runtime speedup is claimed because no benchmark was run.
- No production readiness claim is made for final L1 decision output.

Retrieval stopped because:

- The exact edit targets and validation commands were identified, and additional search was unlikely to change the minimal implementation.

---

## 6.1 Counter-Review Performed

Original framing reviewed:

Build cheap evidence before L0 and expand into L1 evidence only after non-terminal routing.

Assumptions checked:

- `SampleContext` can carry snapshot state internally.
- L1 evidence pack can accept snapshot data without a broad refactor.
- L0 terminal/non-terminal state can guard L1 draft sidecar execution.

Failure modes considered:

- L0 accidentally triggers full L1 extraction before terminal routing.
- L1 rereads cheap evidence despite receiving snapshot data.
- Official runtime output schema changes silently.
- Recrawl routing or final-like labels return through L1 Rule Router paths.

Counterexamples or contradictory evidence found:

- The prior runtime attached L1 draft sidecar unconditionally after stage execution, which would violate the L0-terminal skip requirement when the draft flag is enabled.
- Existing direct L1 evidence-pack calls still need a direct mode for tests and scripts that do not run through runtime.

Alternative routes considered:

- Full L1 extraction before L0 was rejected because it defeats the cheap routing layer.
- Separate duplicated L0 and L1 cheap extractors were rejected because they risk drift.
- Shared `CheapEvidenceSnapshot` on `SampleContext` was selected as the minimal compatible path.

Framing changed: NO

If changed, what changed:

none.

Claims left unsupported or assumed after counter-review:

- The handoff does not claim benchmarked performance improvement.

Residual risks after counter-review:

- Existing dirty worktree contains prior changes in related L1/runtime files, so review should focus on this task's added lines before staging.
- Draft-only metadata is useful for validation but should not be treated as frozen final L1 schema.

Decision after counter-review:

- ACCEPT_ORIGINAL.

---

## 6.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- The task should stay within L0/L1 and must not expand L2.
- L1 draft sidecar changes are permitted only as draft/debug internals.

Ambiguities resolved or escalated:

- Existing unconditional L1 draft attachment was resolved by guarding it on official L1 entry.
- Existing direct L1 evidence-pack usage was preserved by making snapshot input optional.

### Simplicity First

Simplest acceptable route used:

- Reused `SampleContext`, `ArtifactPackage`, and existing L1 evidence-pack code with one internal snapshot dataclass and optional runner input.

Larger or more speculative routes rejected:

- No new evidence-builder framework.
- No dataset-level offline evidence export.
- No model, OCR, YOLO, CLIP, SNet, training, or distillation path.

### Surgical Changes

Touched-file to task-scope mapping:

- Runtime files map to cheap snapshot construction, L0 consumption, and L1 draft gating.
- L1 files map to incremental evidence-pack expansion from snapshot.
- Test files map to L0 terminal skip, non-terminal L1 expansion, and cheap snapshot reuse.
- Task/handoff docs map to workflow compliance.

Adjacent cleanup or formatting-only changes:

- none intentional.

### Goal-Driven Verification

Verification loop:

- Cheap snapshot exists and is cached -> `test_cheap_snapshot_is_cached_on_context` passed.
- L0 terminal skips full L1 draft expansion -> `test_l0_terminal_auxiliary_bucket_does_not_run_l1_draft_when_enabled` passed.
- L1 reuses snapshot -> `test_non_terminal_l1_input_bundle_reuses_cheap_snapshot` and `test_evidence_pack_reuses_cheap_snapshot_for_cheap_artifacts` passed.
- Compatibility and syntax -> py_compile and targeted pytest passed.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile src/warden/runtime/core.py src/warden/runtime/pipeline.py src/warden/runtime/l1_draft_bridge.py src/warden/l1/evidence_pack.py src/warden/l1/l1_runner.py
pytest tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_pipeline_skeleton.py -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
rg -n "need_recrawl|route_to_recrawl" src/warden tests/infer docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
git diff --name-only
```

### Result

- `python -m py_compile ...` passed with exit code 0.
- `pytest ... -q` passed: 20 tests passed.
- `check_task_doc.py` passed for the repo task doc.
- `check_handoff_doc.py` passed for this handoff: `[handoff-doc] OK   docs\handoff\2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`.
- Focused grep found only task/handoff constraint mentions and negative test assertions for `need_recrawl` / `route_to_recrawl`; no active implementation output was found in `src/warden`.
- `git diff --name-only` confirmed a dirty worktree with many pre-existing unrelated files; task-relevant touched files are listed in this handoff.

### Manual / Artifact Checks

- Inspected diffs for runtime core/pipeline, L1 draft bridge, evidence pack, L1 runner, and targeted tests.
- Checked that official runtime schema version strings were not changed.
- Checked that L1 draft remains marked as draft and not final schema.

### Not Run

- Full test suite.
- Runtime benchmark.
- External model/API calls.
- OCR / YOLO / CLIP / SNet / text tower / Decision Head inference.
- Training or distillation.

Reason:

The task required a minimal runtime/L1 evidence construction patch and targeted checks. Broader validation and model/data work were explicitly out of scope.

Next best check:

Run a small runtime smoke over existing representative sample directories after the current dirty worktree is staged or isolated, then compare result/trace schema snapshots.

---

## 8. Model / Agent Runtime Used

- Executor: CODEX
- Model or agent: GPT-5-class Codex agent
- Reasoning effort: unknown
- Verbosity: medium
- Preamble used before tool-heavy work: YES
- Progress updates provided: YES
- Tools used: PowerShell shell commands, apply_patch, pytest, py_compile, ripgrep
- Structured output used: NO
- Notes on deviations from task guidance: none.

---

## 9. Stop Condition

Completion stop condition reached: YES

Reason:

Cheap snapshot construction and incremental L1 draft expansion were implemented, targeted validation passed, official runtime compatibility was preserved, and handoff was written.

Escalation triggered: NO

If yes, escalation reason:

not applicable.

Remaining blockers:

- none for this task.

---

## 7. Risks / Caveats

- The worktree contains unrelated dirty files that predate this task; staging should be selective.
- The L1 draft `evidence_construction` metadata is debug/draft-only and must not be treated as frozen final schema.
- No benchmark was run, so performance improvement remains an engineering inference rather than a measured result.
- Counter-review residual risk: future callers of `run_l1_baseline_for_sample()` that bypass runtime will still use direct L1 evidence-pack mode unless they provide a snapshot.
- Karpathy guardrail residual risk: none identified after targeted validation.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`
- `docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`

Doc debt still remaining:

- Active module docs can optionally be updated later if the project owner wants the internal `CheapEvidenceSnapshot` contract documented outside this task/handoff.

---

## 9. Recommended Next Step

- Review this patch with focus on runtime/L1 evidence construction boundaries and draft-only metadata.
- If accepted, run a representative sample smoke after isolating this task from unrelated dirty worktree changes.
- Keep final L1 Decision Head and any high-cost review/L2 work as separate explicitly accepted tasks.
