# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 harness smoke README 路径清理任务的正式交接文档。
- 若命令、验证结果、兼容性结论或状态说明存在冲突，以英文版为准。

### 摘要

- 对应任务：WARDEN-HARNESS-SMOKE-README-PORTABILITY-CLEANUP
- 任务主题：只修 smoke README 的旧绝对路径示例，并检查其他 harness-facing 文档残留
- 当前状态：DONE
- 所属模块：documentation maintenance / harness baseline

### 当前交付要点

- 已把 `tests/smoke/README.md` 中两条 `E:\Warden...` 命令改成 repo-relative 写法。
- 已重新扫描 `docs/harness/*.md` 和 `tests/smoke/*.md`，当前没有残留 `E:\Warden...`。
- 没有修改脚本逻辑、schema 和 runner。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-20-harness-smoke-readme-portability-cleanup-handoff
- Related Task ID: WARDEN-HARNESS-SMOKE-README-PORTABILITY-CLEANUP
- Task Title: Harness smoke README portability cleanup
- Module: documentation maintenance / harness baseline
- Author: Codex
- Date: 2026-04-20
- Status: DONE

## 1. Executive Summary

Updated the old absolute-path command examples in `tests/smoke/README.md` to repo-relative form and re-scanned harness-facing Markdown docs for any remaining `E:\Warden...` path references.

No script logic, schema logic, or runner behavior was changed.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `tests/smoke/README.md` to replace the remaining absolute-path examples with repo-relative commands.
- Added the formal task doc for this scoped cleanup.
- Added this handoff document.

### Output / Artifact Changes

- none

## 3. Files Touched

- `docs/tasks/2026-04-20_harness_smoke_readme_portability_cleanup.md`
- `docs/handoff/2026-04-20_harness_smoke_readme_portability_cleanup.md`
- `tests/smoke/README.md`

Optional notes per file:

- The smoke README change was limited to the two old command examples.
- No harness scripts were edited.

## 4. Behavior Impact

### Expected New Behavior

- Readers of `tests/smoke/README.md` now see repo-relative commands instead of `E:\Warden...` absolute-path examples.
- Harness-facing Markdown docs now present a consistent portable command style across `docs/harness/*.md` and `tests/smoke/*.md`.

### Preserved Behavior

- No checker logic changed.
- No schema or contract semantics changed.
- No runner behavior changed.

### User-facing / CLI Impact

- Documentation-only change:
  - `python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/smoke/golden_manifest.example.json`
  - `python scripts/ci/check_schema_compat.py --kind sample_dir --path data/raw/benign/2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010/0x7c0.com_20260408T092757Z`

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

This task changed documentation examples only.
No script interface or schema surface was changed.

## 6. Validation Performed

### Commands Run

```bash
Select-String -Path tests/smoke/README.md -Pattern "E:\\Warden" -Context 2,2
Select-String -Path docs/harness/*.md,tests/smoke/*.md -Pattern "E:\\Warden" -CaseSensitive:$false | Select-Object Path, LineNumber, Line
python scripts/ci/check_task_doc.py docs/tasks/2026-04-20_harness_smoke_readme_portability_cleanup.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-04-20_harness_smoke_readme_portability_cleanup.md
```

### Result

- The initial scan confirmed two `E:\Warden...` examples in `tests/smoke/README.md`.
- After the edit, `tests/smoke/README.md` no longer contains `E:\Warden...`.
- After the edit, the harness-facing Markdown set under `docs/harness/*.md` and `tests/smoke/*.md` no longer contains `E:\Warden...`.
- The new task doc passed `check_task_doc.py`.
- The new handoff doc passed `check_handoff_doc.py`.

### Not Run

- script execution checks
- schema guard execution
- unified runner execution

Reason:

The user explicitly constrained this follow-up to documentation cleanup only and asked not to touch scripts, schema, or runner behavior.
Those validations were unnecessary for this scoped task.

## 7. Risks / Caveats

- This cleanup only covered harness-facing Markdown docs under `docs/harness/*.md` and `tests/smoke/*.md`.
- Other unrelated repository docs may still contain absolute repo paths; they were not in scope for this task.
- The Chinese sections in some existing docs still display as mojibake in the terminal output, but this task did not attempt any encoding cleanup.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `tests/smoke/README.md`
- `docs/tasks/2026-04-20_harness_smoke_readme_portability_cleanup.md`
- `docs/handoff/2026-04-20_harness_smoke_readme_portability_cleanup.md`

Doc debt still remaining:

- none for the scoped harness-facing absolute-path cleanup

## 9. Recommended Next Step

- If you want broader documentation portability cleanup, run the same absolute-path scan across other doc areas under a separate task boundary.
- If you later want encoding cleanup for mojibake in terminal views, treat that as a separate documentation-maintenance task.
