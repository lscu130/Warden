# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Warden Harness P0.1 任务的正式交接文档。
- 若命令、验证结果、兼容性结论或状态说明存在冲突，以英文版为准。

### 摘要

- 对应任务：WARDEN-HARNESS-P0-1-NEGATIVE-FIXTURES-AND-PORTABILITY
- 任务主题：Warden Harness P0.1 Negative Fixtures and Portability Cleanup
- 当前状态：DONE
- 所属模块：documentation maintenance / harness baseline

### 当前交付要点

- 为 3 个 checker 分别补齐了最小 positive / negative fixtures。
- 新增了统一本地入口 `run_harness_checks.py`。
- 清理了 baseline 文档和 schema guard 中的硬编码 `E:\Warden...` 路径。
- `check_task_doc.py` 已补齐缺失的 metadata marker 检查。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-14-warden-harness-p0-1-negative-fixtures-and-portability-handoff
- Related Task ID: WARDEN-HARNESS-P0-1-NEGATIVE-FIXTURES-AND-PORTABILITY
- Task Title: Warden Harness P0.1 Negative Fixtures and Portability Cleanup
- Module: documentation maintenance / harness baseline
- Author: Codex
- Date: 2026-04-20
- Status: DONE

## 1. Executive Summary

Completed the planned narrow P0.1 reinforcement on top of the existing Warden harness baseline without changing training, inference, capture outputs, or frozen schema semantics.

This delivery added checked-in positive and negative fixtures for all three harness checkers, a thin unified local runner, portability cleanup for repo-path handling, and stricter task-doc metadata marker enforcement.

## 2. What Changed

### Code Changes

- Updated `scripts/ci/check_task_doc.py` to require the missing task metadata markers.
- Kept `scripts/ci/check_handoff_doc.py` structurally narrow and made its marker handling explicit and stable.
- Updated `scripts/ci/check_schema_compat.py` to derive repo-local paths from the script location instead of using a hardcoded `E:\Warden...` registry path.
- Added `scripts/ci/run_harness_checks.py` as a thin unified local runner over the existing three checkers.

### Doc Changes

- Added the formal P0.1 task doc.
- Updated `docs/harness/WARDEN_HARNESS_BASELINE.md` to document the P0.1 delta, fixture layout, unified runner, and repo-relative commands.
- Added this handoff document.

### Output / Artifact Changes

- Added positive and negative fixtures under `tests/fixtures/harness/task_doc/`.
- Added positive and negative fixtures under `tests/fixtures/harness/handoff_doc/`.
- Added positive and negative manifest-record fixtures under `tests/fixtures/harness/schema/`.

## 3. Files Touched

- `docs/tasks/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- `docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- `docs/harness/WARDEN_HARNESS_BASELINE.md`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`
- `scripts/ci/check_schema_compat.py`
- `scripts/ci/run_harness_checks.py`
- `tests/fixtures/harness/task_doc/positive_minimal.md`
- `tests/fixtures/harness/task_doc/negative_missing_requested_by.md`
- `tests/fixtures/harness/handoff_doc/positive_minimal.md`
- `tests/fixtures/harness/handoff_doc/negative_missing_not_run.md`
- `tests/fixtures/harness/schema/positive_manifest_record.json`
- `tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json`

Optional notes per file:

- The new fixtures are intentionally small and checker-specific.
- The unified runner uses a fixed checked-in fixture map rather than dynamic discovery.
- `README.md` was not changed because the updated harness doc already provides a discoverable local entrypoint.

## 4. Behavior Impact

### Expected New Behavior

- The task-doc checker now fails if `Related Module`, `Related Issue / ADR / Doc`, `Created At`, or `Requested By` are missing.
- The harness now has checked-in positive and negative fixtures for all three checkers.
- Operators can run `python scripts/ci/run_harness_checks.py` for a default positive suite and `python scripts/ci/run_harness_checks.py --suite negative` for a failing negative suite.
- The schema guard now resolves repo-relative input paths and reports the schema-registry reference without a hardcoded Windows repo path.

### Preserved Behavior

- No training logic changed.
- No inference routing logic changed.
- No capture output structure changed.
- No TrainSet V1 semantics changed.
- No Gate / Evasion semantics changed.
- The task-doc and handoff-doc checkers remain structure-only checks.
- The schema guard remains a top-level-only baseline guard.

### User-facing / CLI Impact

- Existing CLI remains valid:
  - `python scripts/ci/check_task_doc.py ...`
  - `python scripts/ci/check_handoff_doc.py ...`
  - `python scripts/ci/check_schema_compat.py --kind ... --path ...`
- New additive CLI:
  - `python scripts/ci/run_harness_checks.py`
  - `python scripts/ci/run_harness_checks.py --suite negative`
  - `python scripts/ci/run_harness_checks.py --only task_doc|handoff_doc|schema`

### Output Format Impact

- Additive only:
  - new checked-in harness fixtures
  - a new thin local runner
  - updated harness baseline documentation
- No existing public output format changed.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- task-doc metadata marker enforcement in `check_task_doc.py`
- repo-relative path handling in `check_schema_compat.py`
- new additive local runner `run_harness_checks.py`

Compatibility notes:

This task is additive only.
It does not rename frozen fields, change manifest field semantics, or change the supported `--kind` values in the schema guard.
The machine-readable registry gap still exists by design in P0.1.

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/ci/check_task_doc.py
python -m py_compile scripts/ci/check_handoff_doc.py
python -m py_compile scripts/ci/check_schema_compat.py
python -m py_compile scripts/ci/run_harness_checks.py
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/positive_minimal.md
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/negative_missing_requested_by.md
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/positive_minimal.md
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/negative_missing_not_run.md
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/positive_manifest_record.json
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json
python scripts/ci/run_harness_checks.py
python scripts/ci/run_harness_checks.py --suite negative
Select-String -Path docs/harness/WARDEN_HARNESS_BASELINE.md -Pattern "E:\\Warden|run_harness_checks.py|tests/fixtures/harness" -Context 0,0
python scripts/ci/check_task_doc.py docs/tasks/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md
Select-String -Path scripts/ci/check_schema_compat.py -Pattern "E:\\Warden|docs/frozen/SCHEMA_REGISTRY.md|resolve_user_path|REPO_ROOT" -Context 0,0
```

### Result

- All four scripts passed `py_compile`.
- The task-doc positive fixture passed.
- The task-doc negative fixture failed with `missing marker: - Requested By:`.
- The handoff-doc positive fixture passed.
- The handoff-doc negative fixture failed with `missing marker: ### Not Run`.
- The schema positive fixture passed.
- The schema negative fixture failed with `field must be boolean: usable_for_multimodal`.
- The unified runner positive suite passed with three PASS lines.
- The unified runner negative suite failed with non-zero and three FAIL lines.
- The new P0.1 task doc passed the updated task-doc lint.
- The new P0.1 handoff doc passed the handoff-doc lint.
- The harness baseline doc no longer contains hardcoded `E:\Warden...` command examples and documents the fixture paths and unified runner.
- The schema guard shows repo-root-derived path logic through `REPO_ROOT`, `resolve_user_path`, and the relative registry reference `docs/frozen/SCHEMA_REGISTRY.md`.

### Not Run

- README entrypoint update
- corpus-level schema validation beyond the checked-in manifest-record fixtures

Reason:

README was intentionally left unchanged because the updated harness baseline doc already provides the local entrypoint.
Corpus-level schema validation remains out of scope for this narrow P0.1 task.

## 7. Risks / Caveats

- The unified runner does not depend on manually chosen fixture paths by default, but it still depends on a fixed checked-in fixture mapping embedded in the script.
- The machine-readable registry gap still exists.
- The schema guard still does not cover nested schema shape, enum semantics, or cross-field semantic validation.
- The doc lints still perform structure-only checks.
- `tests/smoke/README.md` still contains older absolute-path examples because this task only required portability cleanup in the harness baseline doc and schema guard.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- `docs/handoff/2026-04-14_warden_harness_p0_1_negative_fixtures_and_portability.md`
- `docs/harness/WARDEN_HARNESS_BASELINE.md`

Doc debt still remaining:

- `tests/smoke/README.md` still has older absolute-path command examples if the project later wants full harness-doc consistency
- a machine-readable registry is still absent by design

## 9. Recommended Next Step

- If you want full harness-doc consistency, update `tests/smoke/README.md` in a narrow follow-up so all harness-facing docs use repo-relative commands.
- If stricter schema enforcement becomes necessary, freeze additional nested surfaces before expanding the guard.
- If the fixture set grows, keep the unified runner thin and explicit instead of turning it into dynamic discovery or a larger test framework.
