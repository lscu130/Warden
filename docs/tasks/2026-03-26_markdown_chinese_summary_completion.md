# 2026-03-26_markdown_chinese_summary_completion

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Markdown 中文摘要补齐任务的任务定义。
- 若涉及精确文件清单、判定口径、验证命令或交付边界，以英文版为准。

## 1. 背景

仓库当前已有仓库内 Markdown 结构检查脚本，且最新检查结果显示仍有一批业务文档不合规：

- `12` 份 task / handoff 文档缺少 `## 中文版`
- `1` 份 handoff 文档已有中文外壳，但中文摘要过薄

这些问题集中在近期新增的执行任务和交接文档上，已经偏离仓库既定的“中文在前、英文在后、英文权威”约束。

## 2. 目标

把当前检查脚本报出的 `13` 份不合规业务 Markdown 补齐为统一的双语结构：

- 为缺失项补上合规的中文摘要区块
- 为过薄项补足可读的中文导览内容
- 保留英文正文事实、字段、命令、验证和结论不变
- 完成后用仓库现有检查脚本复验，并补一份 handoff

## 3. 范围

- 纳入：本轮检查脚本报出的 `13` 份 task / handoff 文档
- 新增：本次修复任务对应的 repo task / handoff 文档
- 排除：其余业务文档、脚本逻辑、schema、CLI、输出工件

## 4. 结果要求

- 中文采用压缩摘要策略，不做逐段镜像翻译
- 不改英文正文事实与历史记录
- 不改任何 Python 逻辑或检查规则
- 最终 handoff 必须写清修复文件清单、验证结果和剩余风险

## English Version

# Task Metadata

- Task ID: WARDEN-MARKDOWN-CN-SUMMARY-COMPLETION-V1
- Task Title: Complete the missing or too-thin Chinese summary sections across the currently failing Markdown business docs
- Owner Role: Codex execution engineer
- Priority: High
- Status: TODO
- Related Module: Documentation / cross-module
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `scripts/maintenance/check_markdown_bilingual_structure.py`; `docs/tasks/2026-03-23_markdown_chinese_summary_repair.md`; `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`
- Created At: 2026-03-26
- Requested By: user

---

## 1. Background

The repository already has a local Markdown bilingual-structure checker, and the current scan still reports a small set of business docs as non-compliant:

- `12` task/handoff docs are missing the `## 中文版` section entirely
- `1` handoff doc has a Chinese wrapper but its summary is too thin for the current repository threshold

These defects are concentrated in newer execution-task and handoff docs and need to be brought back into line with the repository rule of Chinese summary first, English authoritative section second.

---

## 2. Goal

Repair the `13` currently failing business Markdown docs so they all pass the existing bilingual-structure checker.

This pass must:

- add compliant Chinese summary blocks where missing
- strengthen the one too-thin Chinese summary block
- preserve English facts, fields, commands, validation claims, and historical conclusions
- rerun the repository-local checker and produce a handoff

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-03-25_dataset_target_resize_40k.md`
- `docs/tasks/2026-03-25_plan_a_batch_capture_day2_execution_task.md`
- `docs/tasks/2026-03-25_skip_only_operator_guidance.md`
- `docs/tasks/2026-03-26_plan_a_batch_capture_day3_execution_task.md`
- `docs/tasks/2026-03-26_tranco_supplement_batch_split.md`
- `docs/tasks/2026-03-27_plan_a_batch_capture_day4_execution_task.md`
- `docs/handoff/2026-03-25_benign_hang_skip_control.md`
- `docs/handoff/2026-03-25_dataset_target_resize_40k.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_day2_vm_prep.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`
- `docs/handoff/2026-03-26_plan_a_batch_capture_day3_vm_prep.md`
- `docs/handoff/2026-03-26_tranco_supplement_batch_split.md`
- `docs/handoff/2026-03-27_plan_a_batch_capture_day4_vm_prep.md`
- `docs/tasks/2026-03-26_markdown_chinese_summary_completion.md`
- `docs/handoff/2026-03-26_markdown_chinese_summary_completion.md`

This task is allowed to change:

- additive Chinese summary sections
- Chinese-side usage notes and compressed summary bullets
- documentation-only handoff/task artifacts for this repair pass

If a file is not listed here, treat it as out of scope.

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite English authoritative sections for style
- do not modify Python logic or the checker thresholds
- do not change schema, labels, CLI, outputs, or capture behavior
- do not silently repair unrelated Markdown files outside the failing set

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-23_markdown_chinese_summary_repair.md`
- `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`

### Code / Scripts

- `scripts/maintenance/check_markdown_bilingual_structure.py`

### Data / Artifacts

- current checker output showing `13` failing business Markdown docs

### Prior Handoff

- `docs/handoff/2026-03-23_markdown_chinese_summary_repair.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- repaired Chinese summary sections in the `13` failing business Markdown docs
- a repo task doc for this repair pass
- a repo handoff doc for this repair pass
- a checker rerun result showing the remaining failure count

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

- Keep English as the authoritative version.
- Keep Chinese content at the compressed-summary level, not full mirrored translation.
- Preserve existing dates, statuses, commands, and validation claims.
- Limit edits to the scoped failing docs plus this task/handoff pair.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/maintenance/check_markdown_bilingual_structure.py` CLI and defaults
- existing Markdown English authoritative sections
- repository doc-path layout

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden`

Downstream consumers to watch:

- human readers of task and handoff docs
- future doc-maintenance passes that rely on the current checker output

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the failing docs plus the prior Chinese-summary repair task/handoff.
2. Add compliant Chinese summary sections to missing files.
3. Strengthen the too-thin Chinese handoff summary.
4. Rerun the repository-local checker.
5. Record scope, validation, and remaining risk in a new handoff.

Task-specific execution notes:

- Reuse the repository's existing Chinese-summary style rather than inventing a new structure.
- Keep claims short, factual, and traceable to the English section below.
- Do not touch unrelated unstaged or user-owned changes in the worktree.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] all `13` currently failing scoped docs have compliant Chinese summary sections
- [ ] the prior too-thin handoff now passes the checker threshold
- [ ] English authoritative sections remain intact
- [ ] the repository-local checker was rerun
- [ ] the final response follows required engineering format
- [ ] a repo handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] rerun the Markdown bilingual-structure checker
- [ ] confirm the previously failing file list no longer appears
- [ ] spot-check at least one repaired task doc and one repaired handoff doc

Commands to run if applicable:

```bash
python E:\Warden\scripts\maintenance\check_markdown_bilingual_structure.py --root E:\Warden
Get-Content -Raw E:\Warden\docs\tasks\2026-03-25_dataset_target_resize_40k.md
Get-Content -Raw E:\Warden\docs\handoff\2026-03-26_tranco_supplement_batch_split.md
```

Expected evidence to capture:

- checker summary with failed file count
- repaired doc spot checks

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-03-26_markdown_chinese_summary_completion.md`

---

## 13. Open Questions / Blocking Issues

- none
