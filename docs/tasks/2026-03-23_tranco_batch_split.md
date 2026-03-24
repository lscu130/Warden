# 2026-03-23_tranco_batch_split

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次任务定义文档的中文摘要版。
- 若涉及精确字段名、状态、路径、命令或约束，以英文版为准。

### 摘要

- 任务 ID：WARDEN-TRANCO-BATCH-SPLIT-V1
- 任务主题：按良性采样策略，把用户提供的 Tranco CSV 处理成仓库内 `1000` 条一批的本地批次，并补上使用说明
- 当前状态：DONE
- 相关模块：Data module

### 当前任务要点

- 输入文件是 `C:\Users\20516\Desktop\tranco_NN99W.csv`
- 切分不能粗暴按一百万行全量平均分，而是要先按 `Warden_BENIGN_SAMPLING_STRATEGY_V1.md` 的 Tranco 配额抽样
- 输出目录固定为 `E:\Warden\tranco csv`
- 每个批次既要保留规范化后的 CSV，也要生成可直接用于 benign 抓取的 `*_urls.txt`

## English Version

# Task Metadata

- Task ID: WARDEN-TRANCO-BATCH-SPLIT-V1
- Task Title: Split the user-provided Tranco benign CSV into 1000-row strategy-aligned repository-local batches and document how to use them
- Owner Role: Codex execution engineer
- Priority: Medium
- Status: DONE
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- Created At: 2026-03-23
- Requested By: user

## 1. Background

The user provided a Tranco benign source file at `C:\Users\20516\Desktop\tranco_NN99W.csv` and asked for 1000-row batching.
The later clarification added a hard constraint: the split had to follow the Tranco main-pool quotas defined in `Warden_BENIGN_SAMPLING_STRATEGY_V1.md` rather than performing a naive full one-million-row partition.

## 2. Goal

Produce repository-local, strategy-aligned benign Tranco batches by:

- reading the headerless `rank,domain` source
- applying the frozen Tranco quota buckets
- emitting normalized batch CSV files with `rank,domain,url`
- emitting companion TXT URL files
- documenting direct benign-capture usage

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\tranco csv\`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- repository-local Tranco batch artifacts
- operator README content for the batch folder
- task and handoff documentation

## 4. Scope Out

This task must NOT do the following:

- modify the source Tranco CSV in place
- modify benign ingest script logic
- redesign benign pipeline behavior
- add dependencies

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`

### Data / Artifacts

- `C:\Users\20516\Desktop\tranco_NN99W.csv`

## 6. Required Outputs

This task should produce:

- strategy-aligned Tranco CSV batch files under `E:\Warden\tranco csv`
- companion URL TXT files for each batch
- `split_summary.json`
- a local README with benign-capture usage examples
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

- Apply the frozen Tranco quota buckets before batching.
- Use batch size `1000` after quota selection.
- Keep the split artifacts inside `E:\Warden\tranco csv`.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current benign capture CLI
- current benign capture output format

Schema / field constraints:

- Schema changed allowed: NO
- Frozen field names involved: `rank`, `domain`, `url`

## 9. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Strategy-aligned quota selection was applied
- [x] Selected candidates were emitted as 1000-row batches
- [x] Companion TXT files were generated
- [x] Local usage instructions were provided
- [x] No benign ingest or capture logic was changed

## 10. Validation Checklist

Minimum validation expected:

- inspect source file shape and row count
- inspect selected quota counts
- inspect `split_summary.json`
- inspect representative split CSV and TXT files
- confirm final total selected count and batch count
