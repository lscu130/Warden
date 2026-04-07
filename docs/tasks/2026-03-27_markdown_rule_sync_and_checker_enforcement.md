# Task Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“Markdown 双语交付规则同步与检查器补强”任务的任务定义。
- 本次只同步 workflow、template 和现有检查器，不做仓库级批量文档修复。
- 若涉及精确范围、约束、验收或验证命令，以英文版为准。

## 1. 背景

上一轮已在 `AGENTS.md` 新增仓库级规则：

- 给用户的 Markdown 文档默认必须中英双语
- 中文摘要在前，供人工快速阅读
- 英文全文在后，供 AI 读取
- 英文在精确事实、字段、命令和历史事实层面保持权威

用户现在要求单独开一个 scoped task，把这条规则同步到 workflow、相关模板，并补一个 Markdown 规则检查。

## 2. 目标

完成三件事：

- 在 `docs/workflow/GPT_CODEX_WORKFLOW.md` 明确写入这条 Markdown 双语交付规则
- 在 `docs/templates/TASK_TEMPLATE.md` 和 `docs/templates/HANDOFF_TEMPLATE.md` 中加入与之对齐的要求
- 扩展现有 `scripts/maintenance/check_markdown_bilingual_structure.py`，让它检查这条规则对应的关键结构，而不仅是中英分区壳子

## 3. 范围

- 纳入：
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
  - `docs/templates/TASK_TEMPLATE.md`
  - `docs/templates/HANDOFF_TEMPLATE.md`
  - `scripts/maintenance/check_markdown_bilingual_structure.py`
  - 本次 task / handoff 文档
- 排除：
  - `AGENTS.md`
  - 其他业务 Markdown 文档
  - 非 Markdown 检查相关脚本
  - 仓库级批量修复

## 4. 结果要求

- workflow 和模板都要显式写出 Markdown 双语交付规则
- 检查器新增规则感知，默认扫描时能发现关键结构缺失
- 不引入第三方依赖
- 不顺手修其他不在范围内的旧文档
- 最终补齐 repo handoff

## English Version

# Task Metadata

- Task ID: 2026-03-27-markdown-rule-sync-and-checker-enforcement
- Task Title: Synchronize the Markdown bilingual-delivery rule into workflow/templates and extend the Markdown checker to enforce the key rule structure
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: project-documentation
- Related Issue / ADR / Doc: `E:\Warden\AGENTS.md`; `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`; `E:\Warden\docs\templates\TASK_TEMPLATE.md`; `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`; `E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py`; `E:\Warden\docs\tasks\2026-03-24_markdown_structure_check_script.md`; `E:\Warden\docs\handoff\2026-03-24_markdown_structure_check_script.md`; `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`
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

The previous scoped task updated `AGENTS.md` to add a repository-level Markdown delivery rule:

- Markdown documents delivered to the user must be bilingual by default
- a Chinese summary must appear first for human reading
- the full English version must appear afterward for AI reading
- English remains authoritative whenever exact wording, fields, commands, priorities, or historical facts matter

The user now requested a separate scoped task to synchronize this rule into the workflow and template docs, and to add checker support for the rule instead of leaving it as a manual expectation only.

---

## 2. Goal

Complete three tightly scoped changes:

- update `docs/workflow/GPT_CODEX_WORKFLOW.md` so it explicitly states the Markdown bilingual-delivery rule
- update `docs/templates/TASK_TEMPLATE.md` and `docs/templates/HANDOFF_TEMPLATE.md` so the templates reflect the same requirement
- extend `scripts/maintenance/check_markdown_bilingual_structure.py` so it validates the key structure required by the rule, not only the presence of Chinese/English section markers

---

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\docs\workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs\templates\TASK_TEMPLATE.md`
- `E:\Warden\docs\templates\HANDOFF_TEMPLATE.md`
- `E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py`
- `E:\Warden\docs\tasks\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`
- `E:\Warden\docs\handoff\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`

This task is allowed to change:

- workflow wording for Markdown-delivery expectations
- task/handoff template wording for Markdown-delivery expectations
- checker logic, issue codes, and optional JSON output fields related to the Markdown rule
- task and handoff documentation for this scoped change

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify `AGENTS.md`
- rewrite unrelated repository Markdown documents
- batch-fix checker failures outside the scoped files
- introduce third-party dependencies

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
- `E:\Warden\docs\tasks\2026-03-24_markdown_structure_check_script.md`
- `E:\Warden\docs\handoff\2026-03-24_markdown_structure_check_script.md`
- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

### Code / Scripts

- `E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py`

### Data / Artifacts

- existing repository Markdown files scanned by the checker
- the current repository bilingual Markdown convention with `## 中文版` before `## English Version`
- the current standardized AI-authoritative note used in many governance/docs files

### Prior Handoff

- `E:\Warden\docs\handoff\2026-03-24_markdown_structure_check_script.md`
- `E:\Warden\docs\handoff\2026-03-27_agents_markdown_bilingual_delivery_rule.md`

### Missing Inputs

- none
- none

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- an updated workflow doc with the Markdown-delivery rule
- updated task and handoff templates reflecting the rule
- an updated Markdown checker that validates the new rule's key structure
- a repo task doc and a repo handoff doc for this change

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

- Keep the checker read-only.
- Extend the checker only for key structure implied by the new Markdown rule; do not turn this task into a full editorial lint.
- Avoid checker changes that would immediately require a broad repo-wide repair outside the scoped files unless the current repo already satisfies the new rule.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing workflow and template filenames
- existing checker CLI entrypoint and default root behavior
- existing bilingual section markers `## 中文版` and `## English Version`

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --help`
  - `python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden`
  - `python -m py_compile E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py`

Downstream consumers to watch:

- human operators using the workflow/templates
- future task/handoff authors
- any automation or operator reading checker issue codes or JSON output

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

- Use wording that mirrors `AGENTS.md` rather than inventing a competing phrasing.
- Keep checker additions explicit and deterministic.
- Prefer additive checks and backward-compatible output expansion over breaking the existing checker interface.

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

- [ ] `docs/workflow/GPT_CODEX_WORKFLOW.md` explicitly states the Markdown bilingual-delivery rule
- [ ] `docs/templates/TASK_TEMPLATE.md` and `docs/templates/HANDOFF_TEMPLATE.md` both reflect the rule
- [ ] the checker detects at least one new rule-aligned structural issue beyond the old marker/thin-summary checks
- [ ] the current repo passes the checker after the scoped updates, or any remaining failures are explicitly reported without silent repair

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] repo checker run
- [ ] targeted negative smoke for the new checker rule
- [ ] scoped worktree check

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root <negative-smoke-dir>
git status --short -- "docs/workflow/GPT_CODEX_WORKFLOW.md" "docs/templates/TASK_TEMPLATE.md" "docs/templates/HANDOFF_TEMPLATE.md" "scripts/maintenance/check_markdown_bilingual_structure.py" "docs/tasks/2026-03-27_markdown_rule_sync_and_checker_enforcement.md" "docs/handoff/2026-03-27_markdown_rule_sync_and_checker_enforcement.md"
```

Expected evidence to capture:

- repo-wide checker result after the scoped updates
- a negative smoke result proving the new rule check actually fires

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

- `E:\Warden\docs\handoff\2026-03-27_markdown_rule_sync_and_checker_enforcement.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
- none
- none

If none, write `none`.
