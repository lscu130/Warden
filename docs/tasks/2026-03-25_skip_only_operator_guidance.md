# 2026-03-25_skip_only_operator_guidance

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“只保留 skip 为主操作流”的任务定义。
- 若涉及精确操作建议、文档路径、兼容性结论或验证口径，以英文版为准。

## 1. 背景

仓库里虽然已经有 supervised skip 和 benign recovery helper，但当前操作成本评估后，用户明确决定：

- 正常操作流以 `skip` 处理单个卡住 URL
- 不再把 recovery-based second-pass benign recapture 作为默认推荐路径
- 若 benign 数量不足，优先扩充新的 Tranco 批次

这意味着 operator 文档必须同步，不应继续把 recovery 写成常规主路径。

## 2. 目标

把当前面向操作员的文档更新为“skip-first，benign 不足就扩新批次”的口径，同时保留已有 recovery helper 作为仓库中的辅助工具，而不是日常默认流程。

## 3. 范围

- 纳入：operator-facing 文档与对应 task / handoff
- 排除：capture 代码行为修改、删除 recovery helper、schema / CLI 结构改动

## English Version

# Task Metadata

- Task ID: WARDEN-SKIP-ONLY-OPERATOR-GUIDANCE-V1
- Task Title: De-scope recovery from current operator guidance and keep skip as the active batch-stall workflow
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations / operator docs
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`; `docs/handoff/2026-03-25_benign_hang_skip_control.md`; `docs/handoff/2026-03-25_malicious_hang_skip_control.md`
- Created At: 2026-03-25
- Requested By: user

---

## 1. Background

The repository currently contains both supervised skip support and a benign recovery helper.
After review of the operational cost, the user explicitly decided that recovery-based second-pass benign recapture should not remain part of the normal operator workflow.
The active workflow should instead be:

- use supervised `skip` when a single benign or malicious URL stalls,
- preserve existing sample outputs without trying to recover every interrupted benign URL,
- if benign sample count is still insufficient, expand with more Tranco batches.

This requires syncing the current docs so operators stop treating recovery as a recommended default path.

---

## 2. Goal

Update the current operator-facing documentation so the active workflow is "skip-first, expand-new-benign-batches when short" rather than "skip plus recovery-based second-pass recapture".
This task should not change the capture code path itself, should not remove the helper script from the repo, and should not change sample schema, label semantics, or runner CLI behavior.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- operator guidance wording
- recommended command examples
- explicit next-step strategy for benign sample shortfall
- task / handoff continuity artifacts for this strategy update

---

## 4. Scope Out

This task must NOT do the following:

- do not remove existing recovery helper code from `scripts/data/benign/recover_benign_batch.py`
- do not modify benign or malicious runner behavior
- do not change sample sidecar schema, labels, training logic, or inference logic
- do not rewrite older historical handoffs as if the recovery helper never existed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/benign/recover_benign_batch.py`

### Data / Artifacts

- prior supervised benign and malicious skip probe results already generated under `E:\Warden\tmp\`

### Prior Handoff

- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- `docs/handoff/2026-03-25_benign_hang_skip_control.md`
- `docs/handoff/2026-03-25_malicious_hang_skip_control.md`

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated operator-facing docs that recommend skip without recovery as the normal workflow
- an explicit repo task doc for this strategy change
- an explicit repo handoff for this strategy change

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

- Keep the skip-based workflow intact for both benign and malicious.
- Do not present recovery-based second-pass recapture as the default path for benign shortfall.
- Preserve factual historical statements where needed, but make the current recommended operator path unambiguous.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `python scripts/data/benign/run_benign_capture.py --input_path ...`
- `python scripts/data/malicious/run_malicious_capture.py --input_path ...`
- current supervised CLI flags for benign and malicious runners

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --help`
  - `python scripts/data/malicious/run_malicious_capture.py --help`
  - `python scripts/data/benign/recover_benign_batch.py --help`

Downstream consumers to watch:

- operators reading the runbook
- operators using the 2026-03-25 VM prep handoff

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current operator-facing docs that mention recovery.
2. Write a narrow task definition for the strategy update.
3. Update runbook and VM prep to remove recovery as recommended operator guidance.
4. Add a handoff summarizing the doc-only strategy change.
5. Run lightweight validation on the touched markdown files.

Task-specific execution notes:

- Keep the recovery helper code untouched.
- Prefer operator wording like "expand fresh Tranco batches" over vague "retry if needed".
- Preserve the 2026-03-24 Day 1 naming freeze in the VM prep doc.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] current operator docs no longer recommend benign recovery as the default path
- [ ] runbook clearly says to use skip for stalls and expand new Tranco batches if benign volume is still short
- [ ] 2026-03-25 VM prep no longer instructs operators to use benign recovery commands
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] validation was run, or inability to run was explicitly stated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] markdown content spot-check
- [ ] search for stale recovery instructions in touched operator docs

Commands to run if applicable:

```bash
rg -n "recover_benign_batch|inventory_only|quarantine_partial_dirs" docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md docs/tasks/2026-03-25_skip_only_operator_guidance.md docs/handoff/2026-03-25_skip_only_operator_guidance.md
```

Expected evidence to capture:

- runbook no longer presents recovery as the default benign workflow
- VM prep no longer presents benign recovery commands
- new task and handoff docs exist in the repo
