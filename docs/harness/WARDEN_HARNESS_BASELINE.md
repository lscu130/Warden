# WARDEN_HARNESS_BASELINE.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Warden 当前 harness baseline 的最小目标、运行方式和边界。
- 若命令、路径、覆盖范围或兼容性说明存在冲突，以英文版为准。

### 摘要

- P0 已建立 task doc lint、handoff lint、schema compatibility guard 和 smoke baseline skeleton。
- P0.1 新增了 positive / negative fixtures、统一运行入口、task doc metadata 检查补齐和路径可移植性修正。
- 当前 baseline 仍然只覆盖最小结构和选定顶层 schema surface，不覆盖深层语义、运行时行为或平台级 CI。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# WARDEN_HARNESS_BASELINE.md

This document defines the current Warden harness baseline.

The goal is to keep the harness small, local, and auditable.
It is not a benchmark platform, not a CI platform, and not a deep schema-validation framework.

## 1. Current Phase Summary

### P0 Baseline

Harness P0 introduced the first repo-native guardrail set:

- task-document structure checks
- handoff-document structure checks
- a baseline schema compatibility guard
- a smoke-baseline skeleton

### P0.1 Reinforcement

Harness P0.1 adds:

- checked-in positive fixtures
- checked-in negative fixtures
- a thin local unified runner
- portable repo-relative command examples
- expanded task-doc metadata marker checks

These additions are still intentionally narrow.
They do not change training, inference, capture-output, or data-mainline behavior.

## 2. Included Checks

### 2.1 Task Doc Lint

Script:

- `python scripts/ci/check_task_doc.py <task_doc.md>`

Purpose:

- verify that a non-trivial task doc contains the required bilingual markers, key task metadata markers, and required English template headings

Current boundary:

- structure only
- does not validate whether the task content is semantically correct

### 2.2 Handoff Doc Lint

Script:

- `python scripts/ci/check_handoff_doc.py <handoff_doc.md>`

Purpose:

- verify that a non-trivial handoff doc contains the required bilingual markers, metadata markers, required section headings, and required validation/behavior subheadings

Current boundary:

- structure only
- does not validate whether validation or compatibility claims are true

### 2.3 Schema Compatibility Guard

Script:

- `python scripts/ci/check_schema_compat.py --kind <kind> --path <target>`

Supported kinds:

- `sample_dir`
- `meta_json`
- `url_json`
- `auto_labels_json`
- `manifest_record`

Purpose:

- enforce a minimal compatibility baseline for selected required file names and top-level keys

Current boundary:

- checks selected TrainSet V1 required files for sample directories
- checks selected top-level keys for `meta.json`, `url.json`, and `auto_labels.json`
- checks minimum TrainSet V1 manifest fields and boolean presence/usability flags

## 3. Checked-In Fixture Layout

Harness fixtures now live under:

- `tests/fixtures/harness/task_doc/`
- `tests/fixtures/harness/handoff_doc/`
- `tests/fixtures/harness/schema/`

Current fixture set:

- `tests/fixtures/harness/task_doc/positive_minimal.md`
- `tests/fixtures/harness/task_doc/negative_missing_requested_by.md`
- `tests/fixtures/harness/handoff_doc/positive_minimal.md`
- `tests/fixtures/harness/handoff_doc/negative_missing_not_run.md`
- `tests/fixtures/harness/schema/positive_manifest_record.json`
- `tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json`

Fixture policy:

- each checker has at least one positive fixture and one negative fixture
- negative fixtures are intentionally small and fail for one clear reason
- schema fixtures use `manifest_record` only so they stay repo-native and deterministic

## 4. Unified Local Runner

Script:

- `python scripts/ci/run_harness_checks.py`

Purpose:

- run the checked-in positive or negative harness fixture suite from one local entrypoint

Available usage:

```bash
python scripts/ci/run_harness_checks.py
python scripts/ci/run_harness_checks.py --suite negative
python scripts/ci/run_harness_checks.py --only task_doc
python scripts/ci/run_harness_checks.py --only handoff_doc
python scripts/ci/run_harness_checks.py --only schema
```

Behavior:

- the default run uses the positive fixture suite
- `--suite negative` intentionally surfaces failing checks and returns non-zero
- any failing selected subcheck causes the overall runner to return non-zero

## 5. Local Minimal Run Commands

Run syntax/import sanity:

```bash
python -m py_compile scripts/ci/check_task_doc.py
python -m py_compile scripts/ci/check_handoff_doc.py
python -m py_compile scripts/ci/check_schema_compat.py
python -m py_compile scripts/ci/run_harness_checks.py
```

Run direct positive checks:

```bash
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/positive_minimal.md
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/positive_minimal.md
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/positive_manifest_record.json
```

Run direct negative checks:

```bash
python scripts/ci/check_task_doc.py tests/fixtures/harness/task_doc/negative_missing_requested_by.md
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/negative_missing_not_run.md
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/fixtures/harness/schema/negative_manifest_record_missing_bool.json
```

Run the unified suites:

```bash
python scripts/ci/run_harness_checks.py
python scripts/ci/run_harness_checks.py --suite negative
```

## 6. Deliberately Uncovered

The current harness still does not cover:

- nested schema validation
- enum-level compatibility validation
- full manifest JSONL corpus validation
- runtime inference routing validation
- training-loop validation
- capture execution correctness
- benchmark result generation
- automatic repair or auto-fix behavior
- CI-platform integration

These omissions remain deliberate.

## 7. Known Gaps Still Remaining

- the schema registry is still human-readable only; there is no machine-readable registry yet
- the schema guard still enforces selected top-level and file-presence surfaces only
- doc lints are still structural-only checks
- the unified runner still depends on the checked-in fixture mapping embedded in the script, not dynamic discovery

## 8. Recommended Next Expansion Path

Recommended next steps after P0.1:

- add one or two more negative fixtures for edge cases only when they map to a concrete bug class
- add a machine-readable registry only if stricter schema enforcement becomes necessary
- add optional corpus-level validation over checked-in fixture data only if a later task requires it
- keep any future CI integration thin and local-first instead of turning the harness into a platform rewrite
