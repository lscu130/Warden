# 2026-03-23_markdown_chinese_summary_repair

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Markdown 中文摘要修复任务的任务定义。
- 若涉及精确统计口径、纳入范围、排除范围或验证标准，以英文版为准。

## 1. 背景

仓库内一批业务 Markdown 虽然已经采用“中文在前、英文在后”的结构，但中文区块仍有两类问题：

- 部分文件中文正文损坏为 `???` 或大片 `?`
- 部分文件只有中文壳，没有实质中文摘要，用户观感上接近单英文文档

此外，近期新增的 task、handoff 和 operator README 也进入了业务文档集合，必须按同一口径一起检查，而不是只看旧核心规范文档。

## 2. 目标

对全量业务文档做一次中文摘要修复与补全：

- 修复明显损坏的中文区块
- 为薄中文文档补上可读中文摘要
- 保留英文版为 AI 权威版本
- 统计最终覆盖情况并输出 handoff

## 3. 范围

- 纳入：根目录业务 Markdown、`docs/**`、operator README
- 排除：`data/processed/**` 运行产物报告、结构草图 `docs/STRUCTION.md`

## 4. 结果要求

- 不改任何 Python 逻辑
- 不改 schema、CLI、输出路径或英文正文事实
- 中文采用压缩摘要策略，不做逐段完整镜像翻译
- 最终补一份 handoff，明确写清统计口径、修复内容和剩余风险

## English Version

# Task Metadata

- Task ID: WARDEN-MARKDOWN-CN-SUMMARY-REPAIR-V1
- Task Title: Repair garbled or missing Chinese summaries across business Markdown documents
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Documentation / cross-module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`
- Created At: 2026-03-23
- Requested By: user

## 1. Background

A set of business Markdown documents in the repo already follows the "Chinese first, English second" structure, but the Chinese sections still had two classes of defects:

- some were visibly garbled as `???` or repeated `?`
- others contained only a thin wrapper and left the actual body effectively English-only

The newer task, handoff, and operator README documents also had to be included in the same audit scope rather than being treated as exceptions.

## 2. Goal

Repair the Chinese-side summaries across the scoped business-document set while preserving the English section as the authoritative version.

The pass must:

- repair visibly garbled Chinese sections
- add substantive Chinese summaries to thin documents
- preserve English facts, fields, commands, and conclusions
- record final stats and a repo handoff

## 3. Scope

- Included: root business docs, `docs/**`, and operator README files
- Excluded: `data/processed/**` runtime reports and the structure sketch `docs/STRUCTION.md`

## 4. Required Result

- repair damaged Chinese sections
- add readable Chinese summary blocks where the Chinese side was too thin
- keep the Chinese strategy at the "compressed summary" level rather than line-by-line mirrored translation
- avoid Python/script/schema/CLI/output changes
- produce a final handoff with explicit scope and validation coverage
