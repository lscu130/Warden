# CODEX_MEMORY.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# CODEX_MEMORY.md

# Codex Execution Memory

## 1. External Artifact Localization

### Trigger

If the user provides a task file, handoff file, spec file, or other active project artifact from a path outside the repository, such as:

- `Downloads`
- `Desktop`
- chat-export temp paths
- any non-repo absolute path

and that artifact will be reused in later Warden collaboration, review, or execution steps.

### Required action

Codex must not assume the artifact is already part of the repository.

Codex must:

1. verify whether a repo-local copy already exists
2. if not, create a repo-local copy under the appropriate project directory
3. explicitly return the repo-local path to the user
4. prefer the repo-local path in all later references

### Preferred destinations

- task artifacts: `docs/tasks/`
- handoff artifacts: `docs/handoff/`
- workflow notes: `docs/workflow/`

### Why this exists

This rule is here because a prior Warden task file existed only in `Downloads`, was referenced successfully once, but was not available in the repository when the user later tried to find it.

That is a collaboration failure, not a user failure.

## 2. Near-Full Context Handoff

### Trigger

If the current background/context window is estimated to be near 90% full, or the conversation is already showing signs of overload:

- slower responses
- more repeated material
- rising risk of mixing old and new tasks
- rising risk of factual drift

### Required action

Codex must proactively remind the user to switch to a new window and continue there.

Before asking the user to switch, Codex must summarize the current state and explicitly list the files that should be handed off to the next window.

### Required handoff contents

The summary must include:

1. current task status
2. what has already been changed
3. what is still pending
4. current frozen constraints
5. recommended next step
6. files that should be passed into the next GPT-web or Codex window

### Why this exists

This rule exists to prevent long-context degradation from silently causing boundary mistakes, forgotten constraints, or duplicated work.
