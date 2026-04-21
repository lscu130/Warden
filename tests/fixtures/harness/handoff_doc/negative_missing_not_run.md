# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

- 这是 handoff checker 的负例 fixture。

## English Version

# Handoff Metadata

- Handoff ID: FIXTURE-HANDOFF-NEGATIVE
- Related Task ID: FIXTURE-TASK-DOC-NEGATIVE
- Task Title: Negative handoff fixture missing not run section
- Module: harness fixtures
- Author: Codex
- Date: 2026-04-20
- Status: DONE

## 1. Executive Summary

Minimal negative fixture for the handoff-doc checker.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- this fixture

### Output / Artifact Changes

- none

## 3. Files Touched

- `tests/fixtures/harness/handoff_doc/negative_missing_not_run.md`

Optional notes per file:

- minimal failing fixture

## 4. Behavior Impact

### Expected New Behavior

- The checker should fail.

### Preserved Behavior

- No production behavior changes.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

none

## 6. Validation Performed

### Commands Run

```bash
python scripts/ci/check_handoff_doc.py tests/fixtures/harness/handoff_doc/negative_missing_not_run.md
```

### Result

- expected to fail

## 7. Risks / Caveats

- none

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `tests/fixtures/harness/handoff_doc/negative_missing_not_run.md`

Doc debt still remaining:

- none

## 9. Recommended Next Step

- keep this fixture minimal
