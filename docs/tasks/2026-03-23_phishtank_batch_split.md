# 2026-03-23_phishtank_batch_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次任务定义文档的中文摘要版。
- 若涉及精确字段名、状态、路径、命令或约束，以英文版为准。

### 摘要

- 任务 ID：WARDEN-PHISHTANK-BATCH-SPLIT-V1
- 任务主题：把用户提供的 PhishTank CSV 切成仓库内 `500` 行一批的本地批次，并补上使用说明
- 当前状态：DONE
- 相关模块：Data module

### 当前任务要点

- 输入文件是 `C:\Users\20516\phishtank_2026_only.csv`
- 输出目录固定为 `E:\Warden\phishtank csv`
- 除了批次 CSV 外，还需要生成每批对应的 `*_urls.txt`、`split_summary.json` 和本地 `README.md`
- 本任务不改 ingest / capture 逻辑，只生成可直接操作的批次数据和说明文档

## English Version

# Task Metadata

- Task ID: WARDEN-PHISHTANK-BATCH-SPLIT-V1
- Task Title: Split the user-provided PhishTank CSV into 500-row local batches under the repository and document how to use them
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- Created At: 2026-03-23
- Requested By: user

## 1. Background

The user provided a local PhishTank CSV file at `C:\Users\20516\phishtank_2026_only.csv` and requested deterministic batch splitting into 500-row chunks.
The split artifacts had to be stored inside the repository under `E:\Warden\phishtank csv`, and the delivery also had to explain concrete script usage for these batches.

## 2. Goal

Produce repository-local PhishTank batch files in 500-row chunks, keep the source rows intact, generate operator-friendly companion files, and document the practical ways to use those batches with the current ingest scripts.

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\phishtank csv\`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- repository-local batch artifacts
- operational README content for the batch folder
- task and handoff documentation

## 4. Scope Out

This task must NOT do the following:

- modify the original source CSV in place
- modify ingest script logic
- redesign pipeline behavior
- add dependencies

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`

### Data / Artifacts

- `C:\Users\20516\phishtank_2026_only.csv`

## 6. Required Outputs

This task should produce:

- 500-row PhishTank batch CSV files under `E:\Warden\phishtank csv`
- companion URL TXT files for each batch
- a small README in the output folder
- a task document and handoff document

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.

Task-specific constraints:

- Keep the original CSV row order.
- Use fixed batch size `500`.
- Keep the split artifacts inside `E:\Warden\phishtank csv`.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current ingest script CLIs
- current PhishTank CSV column names used by the scripts

Schema / field constraints:

- Schema changed allowed: NO
- Frozen field names involved: `url`, `target`

## 9. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Source CSV was split into 500-row batches
- [x] Companion TXT files were generated
- [x] Local usage instructions were provided
- [x] No ingest or capture logic was changed

## 10. Validation Checklist

Minimum validation expected:

- inspect source header and row count
- inspect representative split CSV and TXT files
- inspect `split_summary.json`
- confirm final batch counts and short-tail final batch size
