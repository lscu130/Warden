<!-- operator: ClaudeCode; task: AGENTOPS-V0-DOC; date: 2026-04-29 -->

# Warden AgentOps V0 Workflow

---

## 中文版

> 面向人类维护者：本文档说明 Warden AgentOps V0 的当前工作流、能力边界与安全规则。

### 1. 概述

Warden AgentOps V0 是一个以文档为中心的 AI Agent 工作流，旨在让 Claude Code 安全地协助维护项目文档。当前版本聚焦于 `docs/` 目录内的只读与编辑操作，所有变更必须经过人工审查和显式批准后方可提交到任务分支。

### 2. 当前 V0 能力

#### 2.1 已完成的任务

| 任务编号 | 描述 |
|---------|------|
| **TASK-CLAUDE-001** | Claude Code 可执行只读任务，并通过飞书向维护者汇报结果。 |
| **TASK-CLAUDE-002** | Claude Code 可在 `docs/` 范围内修改文件，并生成 report / diff / 飞书汇报。 |
| **TASK-CLAUDE-003** | `agentctl.py` 支持 `list` / `status` / `diff` / `approve` / `reject` 命令，用于审查和管理 Agent 任务。 |

#### 2.2 能力边界

- **读写范围**：仅限 `docs/` 目录内的 Markdown 及文本文件。
- **禁止操作**：不得修改源码、数据文件、配置文件、README.md（除非任务明确要求）。
- **网络与依赖**：不得安装依赖、联网或修改全局配置。
- **版本控制**：不得自动 push、merge 或执行破坏性 Git 操作（如 `git reset`、`git clean`）。

### 3. 执行流程

1. **任务下发**：Codex 在任务分支（如 `agent/TASK-CLAUDE-00X`）上创建任务，并将明确的工作范围（Scope In / Scope Out）交给 Claude Code。
2. **Agent 执行**：Claude Code 在任务分支上执行文档编辑，严格限定在 `docs/` 目录内。
3. **生成报告**：Claude Code 生成执行报告（含变更文件列表、diff 摘要），并默认以中文通过飞书汇报。
4. **人工审查**：维护者使用 `agentctl.py` 查看任务状态与 diff，确认变更是否符合预期。
5. **批准或拒绝**：
   - `approve`：将变更提交到当前任务分支。
   - `reject`：默认执行 dry-run，仅展示将被撤销的改动；加 `--force` 才会实际丢弃 `docs/` 内的修改。

### 4. 安全边界

| 规则 | 说明 |
|------|------|
| **不自动 push** | Agent 不会将任何提交推送到远程仓库。 |
| **不自动 merge 到 main** | 所有变更保留在任务分支，merge 操作必须由人工在 PR 流程中完成。 |
| **approve 只在任务分支提交** | `agentctl.py approve` 仅在当前任务分支创建 commit，不影响 main 分支。 |
| **reject 默认 dry-run** | `agentctl.py reject` 默认只展示会被撤销的改动，加 `--force` 才实际丢弃 `docs/` 修改。 |
| **敏感文件禁止入仓** | `.agentops/`、`.env`、Webhook URL、Secret/Token 等禁止进入 Git 追踪。 |

### 5. 推荐使用方式

- **Claude Doc Agent 只处理 docs/ 文档任务**：目前仅用于文档编辑、整理和说明撰写。
- **代码任务暂时不交给该 Agent**：涉及源码、架构、复杂设计的任务仍由 Codex 或其他专项 Agent 负责。
- **所有变更先走任务分支，再审查，再 approve**：不要直接在 main 分支上运行 Agent 任务。
- **汇报语言**：Agent 的执行总结和飞书汇报默认使用中文，便于国内团队阅读。

### 6. 后续扩展方向

- **扩大安全编辑范围**：在验证安全性后，逐步开放 `tests/`、`fixtures/`、`examples/` 等低风险目录。
- **增强审查能力**：在 `agentctl.py` 中集成 Markdown 规范检查、链接有效性校验等自动化审查。
- **引入多 Agent 协作**：探索 Review Agent、Test Agent、Localization Agent 等角色分工。
- **CI/CD 预检查**：在 Agent 提交后触发轻量级 CI 检查（如文档构建、拼写检查），提升自动化水平。

---

## English Version

> For AI agents / Codex / Claude Code: This section serves as the authoritative workflow context for Warden AgentOps V0.

### 1. Overview

Warden AgentOps V0 is a documentation-centric AI Agent workflow. It allows Claude Code to assist with project documentation safely. The current scope is limited to read-only and editing operations within the `docs/` directory. All changes require human review and explicit approval before being committed to a task branch.

### 2. Current V0 Capabilities

#### 2.1 Completed Tasks

| Task ID | Description |
|---------|-------------|
| **TASK-CLAUDE-001** | Claude Code executes read-only tasks and reports results to maintainers via Feishu. |
| **TASK-CLAUDE-002** | Claude Code can modify files within `docs/`, generating reports, diffs, and Feishu summaries. |
| **TASK-CLAUDE-003** | `agentctl.py` supports `list`, `status`, `diff`, `approve`, and `reject` commands for task review and management. |

#### 2.2 Capability Boundaries

- **Read/Write Scope**: Only Markdown and text files under `docs/`.
- **Prohibited Operations**: No modification of source code, data files, configuration files, or README.md unless explicitly required.
- **Network & Dependencies**: No installing dependencies, network access, or global configuration changes.
- **Version Control**: No automatic push, merge, or destructive Git operations (e.g., `git reset`, `git clean`).

### 3. Execution Workflow

1. **Task Delegation**: Codex creates a task branch (e.g., `agent/TASK-CLAUDE-00X`) and delegates a clearly scoped task to Claude Code.
2. **Agent Execution**: Claude Code performs documentation edits strictly within the `docs/` directory on the task branch.
3. **Report Generation**: Claude Code produces an execution report (file list, diff summary) and reports via Feishu in Chinese by default.
4. **Human Review**: Maintainers use `agentctl.py` to inspect task status and diffs, verifying that changes meet expectations.
5. **Approve or Reject**:
   - `approve`: Commits the changes to the current task branch.
   - `reject`: Defaults to dry-run, showing what would be discarded; use `--force` to actually discard changes in `docs/`.

### 4. Security Boundaries

| Rule | Description |
|------|-------------|
| **No automatic push** | The agent never pushes commits to the remote repository. |
| **No automatic merge to main** | All changes remain on task branches; merging must be done manually via PR. |
| **Approve commits only to task branch** | `agentctl.py approve` creates a commit only on the current task branch, never on `main`. |
| **Reject defaults to dry-run** | `agentctl.py reject` shows changes to be discarded by default; `--force` is required to actually drop `docs/` modifications. |
| **Sensitive files must not enter Git** | `.agentops/`, `.env`, Webhook URLs, secrets, and tokens are forbidden from Git tracking. |

### 5. Recommended Usage

- **Claude Doc Agent handles docs/ only**: Use it solely for documentation editing, organization, and writing.
- **Do not delegate source code tasks**: Tasks involving source code, architecture, or complex design remain with Codex or specialized agents.
- **Task branch → Review → Approve**: Always run agent tasks on a dedicated branch, review changes, and approve before considering them final.
- **Reporting Language**: Agent execution summaries and Feishu reports default to Chinese for team readability.

### 6. Future Extensions

- **Expand safe edit scope**: After safety validation, gradually open `tests/`, `fixtures/`, `examples/`, and other low-risk directories.
- **Enhanced review capabilities**: Integrate Markdown linting, link validation, and other automated checks into `agentctl.py`.
- **Multi-agent collaboration**: Introduce specialized roles such as Review Agent, Test Agent, and Localization Agent.
- **CI/CD pre-checks**: Trigger lightweight CI checks (e.g., doc build, spell check) after agent commits to increase automation.
