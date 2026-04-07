# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 `AGENTS.md` 仓库级规则补充任务的任务定义。
- 本次只补充 Markdown 交付格式约束，不顺手改 workflow、template 或检查脚本。
- 若涉及精确范围、约束、验收和兼容性结论，以英文版为准。

## 1. 背景

用户要求把一条新的仓库级文档交付规则写入 `AGENTS.md`：

- 交付给用户的 Markdown 文档必须是中英文双语
- 中文摘要放前面，供人工快速阅读
- 英文全文放后面，供 AI 作为权威版本读取

这会修改仓库级工程契约，属于非 trivial 文档约束变更，因此需要显式 task 与 handoff。

## 2. 目标

在 `AGENTS.md` 中新增明确、可执行的 Markdown 双语交付规则，并保持现有“英文对 AI 权威、中文用于人工导览”的总体口径不变。
本次改动应只更新 `AGENTS.md` 及本次任务/交接文档，不改 workflow、模板、脚本或其他历史文档。

## 3. 范围

- 纳入：`AGENTS.md`；本次 task 文档；本次 handoff 文档
- 允许：补充 Markdown 双语交付规则；补充中文摘要中的对应提示
- 排除：`docs/workflow/`、`docs/templates/`、检查脚本、其他业务 Markdown 文档

## 4. 结果要求

- `AGENTS.md` 明确要求：给用户的 Markdown 文档必须双语，中文摘要在前，英文全文在后
- 保持英文版为 AI 权威版本
- 不改 schema、CLI、代码行为或其他仓库接口
- 最终补齐 repo handoff 并写清兼容性结论

## English Version

# Task Metadata

- Task ID: 2026-03-27-agents-markdown-bilingual-delivery-rule
- Task Title: Add a repository-level rule in AGENTS.md requiring bilingual Markdown delivery with Chinese summary first and English full text second
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: project-documentation
- Related Issue / ADR / Doc: `E:\Warden\AGENTS.md`; `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`; `E:\Warden\docs\templates\TASK_TEMPLATE.md`; `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`
- Created At: 2026-03-27
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.

---

## 1. Background

The user requested a new repository-level documentation delivery rule to be added to `AGENTS.md`.

The new rule is:

- Markdown documents delivered to the user must be bilingual
- a Chinese summary must appear first for human reading
- a full English section must appear afterward for AI reading

Because `AGENTS.md` is a top-level engineering contract, updating it changes project process expectations and is therefore non-trivial under the repository rules.

---

## 2. Goal

Update `AGENTS.md` so it explicitly requires bilingual Markdown delivery in the format requested by the user, while preserving the existing interpretation rule that English remains the authoritative version for AI agents.

The change must stay tightly scoped to `AGENTS.md` and the task/handoff artifacts for this specific edit.

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\tasks\2026-03-27_agents_markdown_bilingual_delivery_rule.md`
- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

This task is allowed to change:

- repository-level Markdown delivery rules in `AGENTS.md`
- Chinese summary bullets in `AGENTS.md` that reflect the new rule
- task/handoff documentation for this change

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify `docs/workflow/GPT_CODEX_WORKFLOW.md`
- modify `docs/templates/*.md`
- update Markdown checker scripts or add enforcement automation
- rewrite unrelated repository Markdown files

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`

### Code / Scripts

- none
- none
- none

### Data / Artifacts

- user request in the current thread requiring bilingual Markdown delivery
- existing repository bilingual documentation convention already visible in governance docs
- current date `2026-03-27`

### Prior Handoff

- none

### Missing Inputs

- none
- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- an updated `AGENTS.md` with the new Markdown bilingual delivery rule
- a repo task document for this change
- a repo handoff document for this change

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Keep the new rule limited to Markdown document delivery requirements.
- Preserve the existing English-authoritative interpretation rule for AI.
- Do not expand scope into workflow/template synchronization in this task.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- repository file paths
- existing workflow/template filenames
- existing AI-authoritative interpretation rule

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - none
  - none
  - none

Downstream consumers to watch:

- human readers of repository governance docs
- AI agents relying on `AGENTS.md` as an active contract

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Make minimal code or doc changes.
4. Run the smallest meaningful validation.
5. Summarize compatibility impact.
6. Prepare handoff.

Task-specific execution notes:

- Add the new rule where future engineering work is most likely to see it.
- Keep the wording explicit and operational rather than advisory.
- Avoid duplicating the same rule in many sections unless needed for clarity.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] `AGENTS.md` explicitly requires bilingual Markdown delivery with Chinese summary first and English full text second
- [ ] `AGENTS.md` still states that English is authoritative for AI agents
- [ ] No files outside scoped paths were modified

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] file content spot-check
- [ ] rule-presence search
- [ ] worktree scope check
- [ ] handoff creation check

Commands to run if applicable:

```bash
rg -n "bilingual|Markdown|中文摘要|English full text|authoritative" E:\Warden\AGENTS.md
Get-Content -Raw E:\Warden\AGENTS.md
git status --short
```

Expected evidence to capture:

- the new rule is visible in `AGENTS.md`
- git status only shows the scoped documentation files

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
- none
- none

If none, write `none`.
