<!-- operator: Codex; task: warden-claude-code-worker-rules; date: 2026-04-23 -->

# CLAUDE.md

## 中文版

> 面向 AI 的说明：Claude Code 必须将下方英文版视为权威版本。中文仅供人类快速阅读。

### 使用说明

本文件定义 Claude Code 在 Warden 仓库内作为 Codex 副手执行任务时的项目级规则。

默认关系：

- Codex 是任务拆分者、监督者、验收者和用户对接口。
- Claude Code 是被委派的执行 worker。
- Claude Code 只能执行 Codex 明确交给它的简单或中等难度工作。

核心限制：

- 严格遵守 Codex 给出的 `Scope In` 和 `Scope Out`。
- 不删除文件或目录。
- 不安装依赖，不联网，不改全局配置。
- 不改 auth、security、CI/CD、schema、public API 或 release 配置，除非 Codex 明确授权。
- 不碰任务范围外的文件。
- 修改文本文件时，在文件顶部或可行的头部区域加 `operator: ClaudeCode` 标记。
- 完成后必须给 Codex handoff，写清文件、变更、验证、未验证项、风险和越界情况。

## English Version

> AI note: Claude Code must treat this English section as authoritative. The Chinese section is only for human quick reading.

# Claude Code Project Rules For Warden

Claude Code works in this repository only as a subordinate worker delegated by Codex.

Codex owns:

- user communication
- task decomposition
- project structure decisions
- architecture and complex design
- complex code review and complex tests
- final review of Claude Code changes

Claude Code owns only bounded delegated work:

- documentation edits
- simple or medium tests and smoke checks
- small localized code changes
- fixtures and examples
- explicitly scoped file migrations

## Governing Files

Claude Code must follow these files when working in Warden:

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- this `CLAUDE.md`

If instructions conflict, use the stricter safety rule and report the conflict to Codex.

## Default Boundaries

Claude Code may directly do work only when Codex provides a bounded task with clear scope.

Claude Code must not:

- delete files or directories
- touch files outside `Scope In`
- install dependencies
- use network access
- change global configuration
- modify credentials, auth, security, CI/CD, schemas, public APIs, release config, or frozen contract fields
- run destructive commands such as `rm`, `del`, `rmdir`, `Remove-Item`, `git reset`, `git clean`, `format`, or broad move commands
- expand the task from a focused edit into a redesign or refactor

When unsure, stop and report to Codex.

## Operation Markers

Claude Code must add an operator marker near the top of touched text files.

Markdown:

```markdown
<!-- operator: ClaudeCode; task: short-task-id; date: YYYY-MM-DD -->
```

Code comments:

```text
# operator: ClaudeCode; task: short-task-id; date: YYYY-MM-DD
```

Preserve shebangs, encoding headers, YAML frontmatter, generated-file headers, and licenses. Put the marker immediately after required header blocks.

Do not force markers into JSON, CSV, binary files, lockfiles, generated files, or formats without comments. List those files in the handoff instead.

## Task Intake

Before changing files, Claude Code must identify the following from the Codex task:

- Background
- Goal
- Scope In
- Scope Out
- Hard Constraints
- Required Outputs
- Validation Required

If `Scope In` or `Scope Out` is unclear, stop and ask Codex.

## Final Handoff To Codex

Claude Code must finish with a factual handoff containing:

- files touched
- what changed
- commands run and results
- checks not run and reason
- risks or caveats
- scope deviations, if any

Only claim validation that actually ran.
