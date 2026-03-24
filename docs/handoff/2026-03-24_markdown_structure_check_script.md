# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Markdown 结构检查脚本任务的交接文档。
- 若涉及精确 CLI 参数、返回码、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：WARDEN-MARKDOWN-STRUCTURE-CHECK-V1
- 任务主题：新增一个仓库内 Markdown 双语结构检查脚本
- 当前状态：DONE
- 所属模块：documentation maintenance

### 当前交付要点

- 新增了只读检查脚本 [check_markdown_bilingual_structure.py](E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py)。
- 默认检查双语分区、中文乱码标题、中文占位符和中文摘要过薄四类问题。
- 当前仓库实扫结果为通过，脚本在故意构造的坏样本上能正确返回非零。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-24-markdown-structure-check-script-handoff
- Related Task ID: WARDEN-MARKDOWN-STRUCTURE-CHECK-V1
- Task Title: Add a repository-local Markdown bilingual-structure checking script
- Module: documentation maintenance
- Author: Codex
- Date: 2026-03-24
- Status: DONE

## 1. Executive Summary

Added a new read-only maintenance script at `scripts/maintenance/check_markdown_bilingual_structure.py`.
The script scans scoped business Markdown files, checks bilingual-section structure and Chinese-side quality heuristics, prints a human-readable summary, optionally writes a JSON report, and exits non-zero on violations.

The script was validated on:

- `--help`
- `py_compile`
- a full repo run on the current repaired Warden state
- targeted smoke tests for missing English-section markers and Chinese placeholder-variable detection

## 2. What Changed

### Code Changes

- Added `scripts/maintenance/check_markdown_bilingual_structure.py`.

### Doc Changes

- Added the task doc for this checker.
- Added this handoff document.
- Updated the task doc status and validation checklist after implementation.

### Output / Artifact Changes

- none committed

## 3. Files Touched

- `scripts/maintenance/check_markdown_bilingual_structure.py`
- `docs/tasks/2026-03-24_markdown_structure_check_script.md`
- `docs/handoff/2026-03-24_markdown_structure_check_script.md`

Optional notes per file:

- The new script is read-only and does not modify repo Markdown files.
- The task doc now records the completed validation evidence.
- No existing runtime scripts were edited.

## 4. Behavior Impact

### Expected New Behavior

- Operators can now run a single local command to validate bilingual Markdown structure across the repo.
- The checker can catch missing `## 中文版` / `## English Version` markers, garbled Chinese headings, unresolved Chinese placeholders, and too-thin Chinese summaries.
- The checker can emit an optional JSON report for later automation or CI-style use.

### Preserved Behavior

- No existing capture, data, labeling, training, inference, or paper-support scripts changed.
- No Markdown files are auto-fixed by this script.
- Existing repo CLI behavior remains unchanged.

### User-facing / CLI Impact

- New additive CLI:
  - `python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden`

### Output Format Impact

- Additive only: optional JSON report when `--report-json` is provided.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- new maintenance CLI under `scripts/maintenance/`

Compatibility notes:

This task added a new script only.
It did not alter any existing schema, output format, or CLI surface outside the new checker.

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --help
python -m py_compile E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden\tmp\markdown_structure_check_smoke --report-json E:\Warden\tmp\markdown_structure_check_smoke\report.json
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden\tmp\markdown_structure_check_placeholder_smoke
```

### Result

- `--help` rendered correctly.
- `py_compile` passed.
- Repo run passed with `0` failing files on the current Warden state.
- Missing-English-marker smoke failed as expected with exit code `1` and produced a JSON report.
- Placeholder-variable smoke failed as expected with exit code `1`.

### Not Run

- CI integration
- scheduled automation integration
- rendered Markdown viewer pass

Reason:

This task only added the local checker itself.
Automation and CI wiring were intentionally left out of scope.

## 7. Risks / Caveats

- The thin-summary check is heuristic, not semantic truth; thresholds may need adjustment later if doc style changes.
- The default exclusions intentionally skip `data/processed/**`, `docs/STRUCTION.md`, and `STRUCTION.md`.
- The script currently reports issues but does not auto-fix them.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-03-24_markdown_structure_check_script.md`
- `docs/handoff/2026-03-24_markdown_structure_check_script.md`

Doc debt still remaining:

- none required for this scoped additive checker

## 9. Recommended Next Step

- If you want this to become part of routine maintenance, add a small wrapper command or automation that runs the checker after future Markdown batch edits.
- If threshold tuning becomes necessary, adjust `--min-cn-chars`, `--min-non-usage-headings`, and `--min-bullet-lines` based on actual doc drift rather than guessing.
- Keep future scope separate if you later want an auto-fix mode; do not mix repair logic into this checker without a new task boundary.
