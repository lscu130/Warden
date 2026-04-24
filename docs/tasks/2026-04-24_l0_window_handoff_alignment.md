# 2026-04-24 L0 Window Handoff Alignment Task

## 中文摘要

### 任务元数据
- Task ID: `TASK-L0-2026-04-24-WINDOW-HANDOFF-ALIGNMENT`
- Task Title: `Align GPT-Web Window Handoff With Current L0 Contract`
- Owner Role: `Codex`
- Priority: `P1`
- Status: `DONE`
- Related Module: `inference-docs`
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\Warden_window_handoff_summary_2026-04-24.md`; `docs/modules/L0_DESIGN_V1.md`; `docs/modules/MODULE_INFER.md`; `PROJECT.md`
- Created At: `2026-04-24`
- Requested By: `user`

### 背景
用户提供了一份给 GPT 网页端继续使用的窗口交接文档，但其 L0 表述与仓库当前冻结口径存在漂移，包括仍保留 `fake verification` 作为 L0 特化家族、继续使用 `L0-fast / L1-text / L1-mm` 作为主合同命名、以及把 L0 说成默认可直接完成广义 resolution。该文档若继续原样流转，会让 GPT 网页端和 repo 内 active docs 使用不同定义。

### 目标
把这份窗口交接材料对齐到当前仓库内的 L0 合同，并在 repo 内落一份可持续引用的正式版本，供后续 GPT 网页端窗口继续使用。输出内容需明确当前 L0 的职责、输入、禁止事项、实现状态和 continuation 边界，避免继续传播旧口径。

### Scope In
本任务允许修改：

- `docs/tasks/2026-04-24_l0_window_handoff_alignment.md`
- `docs/handoff/2026-04-24_l0_window_handoff_alignment.md`
- `docs/handoff/2026-04-24_window_handoff_summary_for_gpt_web.md`

本任务允许变更：

- repo 内 task / handoff 文档
- GPT 网页端用的窗口交接 Markdown 内容
- 文档中的 L0 合同表述与 continuation 提示

### Scope Out
本任务禁止：

- 修改任何 Python 代码或 runtime 逻辑
- 重新打开已收紧的 L0 合同边界
- 修改历史 task / handoff 或当前其他 active module docs

### 输入

#### Docs
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

#### Data / Artifacts
- `C:\Users\20516\Downloads\Warden_window_handoff_summary_2026-04-24.md`

#### Missing Inputs
- `none`

### Required Outputs
- repo 内对齐后的 GPT 网页端窗口交接文档
- repo 内 task doc
- repo 内 handoff doc

### Hard Constraints
- 不修改 schema、CLI、字段名或代码行为
- 窗口交接文档按双语结构交付，英文权威
- 文档内容必须以 repo 当前 active L0 合同为准
- 明确指出旧口径中已经失效或不再默认成立的部分

### Interface / Schema Constraints
- Schema changed allowed: `no`
- Frozen field names involved: `html_features`, `brand_signals`, `specialized_fast_resolution_candidate`
- Existing commands that must keep working:
  - `none`
  - `none`
  - `none`

### Suggested Execution Plan
1. 读取外部窗口交接文档和当前 repo L0 合同文档。
2. 标出旧口径与当前口径的冲突点。
3. 在 repo 内落对齐版窗口交接文档。
4. 生成对应 task 和 handoff。
5. 做最小内容校验与兼容性说明。

### Acceptance Criteria
- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes
- [x] 新窗口交接文档明确当前 L0 专注 `gambling / adult / gate`
- [x] 新窗口交接文档明确默认禁止 full HTML / default brand extraction / screenshot-OCR / heavy model / interaction recovery
- [x] 新窗口交接文档明确 `fake verification` 不再作为当前 L0 的独立 active family

### Validation Checklist
- [x] content sanity check
- [x] targeted grep spot-check
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

```bash
Get-Content -LiteralPath 'E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md'
rg -n "fake verification|L0-fast|L1-text|L1-mm|full HTML|brand extraction|screenshot/OCR|gambling / adult / gate" E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md
git diff -- E:\Warden\docs\tasks\2026-04-24_l0_window_handoff_alignment.md E:\Warden\docs\handoff\2026-04-24_l0_window_handoff_alignment.md E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md
```

### Handoff Requirements
- `docs/handoff/2026-04-24_l0_window_handoff_alignment.md`

### Open Questions / Blocking Issues
- `Writing back to the external Downloads file requires escalation approval.`

## English Version

> AI note: The English section is authoritative for exact scope and acceptance.

# 2026-04-24 L0 Window Handoff Alignment Task

# Task Metadata

- Task ID: `TASK-L0-2026-04-24-WINDOW-HANDOFF-ALIGNMENT`
- Task Title: `Align GPT-Web Window Handoff With Current L0 Contract`
- Owner Role: `Codex`
- Priority: `P1`
- Status: DONE
- Related Module: `inference-docs`
- Related Issue / ADR / Doc: `C:\Users\20516\Downloads\Warden_window_handoff_summary_2026-04-24.md`; `docs/modules/L0_DESIGN_V1.md`; `docs/modules/MODULE_INFER.md`; `PROJECT.md`
- Created At: `2026-04-24`
- Requested By: `user`

Use this task to align the GPT-web continuation handoff with the current repository L0 contract.

## 1. Background

The user provided a window handoff document for GPT web continuation. Its L0 wording has drifted away from the current repository contract. The old handoff still treats `fake verification` as an active L0 specialized family, still uses `L0-fast / L1-text / L1-mm` as public top-level contract naming, and still frames L0 as broadly able to directly resolve samples by default. If that document continues to circulate unchanged, GPT web and repo-active docs will operate from different L0 definitions.

## 2. Goal

Align the handoff material with the repository's current L0 contract and persist a repo-local continuation document that GPT web can safely use in the next window. The output must clearly state current L0 responsibilities, inputs, prohibitions, implementation status, and continuation boundaries.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-04-24_l0_window_handoff_alignment.md`
- `docs/handoff/2026-04-24_l0_window_handoff_alignment.md`
- `docs/handoff/2026-04-24_window_handoff_summary_for_gpt_web.md`

This task is allowed to change:

- repo-local task and handoff docs
- the GPT-web continuation Markdown content
- L0 contract wording and continuation guidance inside that handoff

## 4. Scope Out

This task must NOT do the following:

- modify any Python code or runtime logic
- reopen the narrowed L0 contract boundary
- modify historical task documents, historical handoffs, or other active module docs

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

### Data / Artifacts

- `C:\Users\20516\Downloads\Warden_window_handoff_summary_2026-04-24.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- a repo-local aligned GPT-web window handoff document
- a repo-local task doc
- a repo-local handoff doc

## 7. Hard Constraints

Must obey all of the following:

- no schema, CLI, field-name, or behavior change
- the continuation document must be bilingual, with English authoritative
- all wording must match the current repo-active L0 contract
- older assumptions that are no longer valid must be called out explicitly

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `html_features`
- `brand_signals`
- `specialized_fast_resolution_candidate`

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `html_features`, `brand_signals`, `specialized_fast_resolution_candidate`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `none`
  - `none`
  - `none`

Downstream consumers to watch:

- GPT web continuation windows
- future repo-local task drafting based on this handoff

## 9. Suggested Execution Plan

Recommended order:

1. Read the external handoff and the current repo L0 contract docs.
2. Mark the conflicts between old wording and current wording.
3. Write an aligned repo-local continuation handoff.
4. Produce the corresponding task and handoff docs.
5. Run minimal content and compatibility checks.

Task-specific execution notes:

- Preserve the purpose of a GPT-web continuation handoff.
- Remove drift around `fake verification` and old public stage naming.
- Keep the document concise enough to be used in a fresh web window.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes
- [x] The new continuation handoff states that current L0 specializes in `gambling / adult / gate`
- [x] The new continuation handoff states the default prohibitions: full HTML, default brand extraction, screenshot/OCR, heavy model path, interaction recovery
- [x] The new continuation handoff states that `fake verification` is no longer a standalone active L0 family

## 11. Validation Checklist

Minimum validation expected:

- [x] content sanity check
- [x] targeted grep spot-check
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

```bash
Get-Content -LiteralPath 'E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md'
rg -n "fake verification|L0-fast|L1-text|L1-mm|full HTML|brand extraction|screenshot/OCR|gambling / adult / gate" E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md
git diff -- E:\Warden\docs\tasks\2026-04-24_l0_window_handoff_alignment.md E:\Warden\docs\handoff\2026-04-24_l0_window_handoff_alignment.md E:\Warden\docs\handoff\2026-04-24_window_handoff_summary_for_gpt_web.md
```

Expected evidence to capture:

- the aligned handoff content
- grep evidence showing old drift wording removed or explicitly scoped

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

- `docs/handoff/2026-04-24_l0_window_handoff_alignment.md`

## 13. Open Questions / Blocking Issues

- Writing back to the external Downloads file requires escalation approval.
