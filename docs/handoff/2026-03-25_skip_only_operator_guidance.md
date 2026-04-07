# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“skip-only operator guidance”调整的正式 handoff。
- 若涉及精确文档变更、验证结果、兼容性和剩余风险，以英文版为准。

### 摘要

- 对应任务：`WARDEN-SKIP-ONLY-OPERATOR-GUIDANCE-V1`
- 任务主题：把 skip 固化为当前批次卡住时的主操作流
- 当前状态：`DONE`
- 所属模块：Data module / capture operations / operator docs

### 当前交付要点

- 当前推荐操作流已经收敛为：URL 卡住时优先 `skip`，benign 数量不足时扩新批次。
- 仓库中的 benign recovery helper 没被删除，但不再作为默认推荐操作路径。
- 这一步是文档策略同步，不涉及 capture 代码行为变化。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-skip-only-operator-guidance
- Related Task ID: WARDEN-SKIP-ONLY-OPERATOR-GUIDANCE-V1
- Task Title: De-scope recovery from current operator guidance and keep skip as the active batch-stall workflow
- Module: Data module / capture operations / operator docs
- Author: Codex
- Date: 2026-03-25
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Updated the current operator-facing documentation so the active workflow is now skip-first for stalled URLs and expand-new-batches for benign shortfall.
This handoff does not remove the existing benign recovery helper from the repository, but it does remove recovery-based second-pass recapture from the recommended operator path.
No capture code behavior changed in this step; the delivery is a documentation strategy sync only.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` so benign operators are told to use supervised `skip` for stalled URLs and to expand with more Tranco batches if final benign volume is still short.
- Updated `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md` so the 2026-03-25 prep reference no longer presents benign recovery commands as part of the normal workflow.
- Added this task/handoff pair to freeze the strategy change explicitly in the repo.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- `docs/tasks/2026-03-25_skip_only_operator_guidance.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

Optional notes per file:

- The runbook is the main day-to-day operator reference.
- The 2026-03-25 VM prep handoff remains the preferred prep reference for the unfinished Day 1 queue.
- The new task/handoff pair records that this was a workflow-policy sync, not a code change.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators are now guided to use supervised `skip` when a benign or malicious URL stalls.
- Operators are now guided to treat benign sample shortfall as a coverage problem and expand with fresh Tranco batches.
- Operators are no longer told to treat recovery-based second-pass benign recapture as the default continuation path.

### Preserved Behavior

- Existing benign and malicious runner behavior is unchanged.
- Existing supervised skip CLI flags remain unchanged.
- The existing benign recovery helper code remains in the repo unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- current benign and malicious supervised CLI flags as documented interfaces

Compatibility notes:

This step changes operator guidance only.
It does not modify sample schema, runner CLI behavior, batch summary schema, or on-disk output structure.

---

## 6. Validation Performed

### Commands Run

```bash
rg -n "recover_benign_batch|inventory_only|quarantine_partial_dirs" docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md docs/tasks/2026-03-25_skip_only_operator_guidance.md docs/handoff/2026-03-25_skip_only_operator_guidance.md
```

### Result

- Confirmed the touched runbook no longer presents benign recovery commands as part of the default operator path.
- Confirmed the touched 2026-03-25 VM prep handoff no longer presents benign recovery commands.
- Confirmed the new task and handoff docs exist and reflect the skip-only operator strategy.

### Not Run

- code execution tests
- CLI help checks
- live browser probes

Reason:

This step is a documentation-only strategy sync.
The underlying skip behavior had already been validated earlier in the thread and was not changed here.

---

## 7. Risks / Caveats

- The benign recovery helper still exists in the repo, so an operator reading older docs may still discover it unless they use the current runbook and 2026-03-25 VM prep handoff.
- Benign `skip` can still leave partial sample directories on disk; this strategy change intentionally chooses not to make leftover recovery part of the normal workflow.
- If benign shortfall becomes severe, the team still needs enough additional Tranco batches prepared locally for expansion.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/handoff/2026-03-25_plan_a_batch_capture_vm_prep.md`
- `docs/tasks/2026-03-25_skip_only_operator_guidance.md`
- `docs/handoff/2026-03-25_skip_only_operator_guidance.md`

Doc debt still remaining:

- Older historical handoffs that describe the recovery helper as part of the feature work remain in the repo and are still factually correct as historical records.
- If the team wants to fully retire the helper later, that should be a separate code-and-doc task.

---

## 9. Recommended Next Step

- Continue using supervised `skip` on both benign and malicious lanes whenever a single URL stalls.
- If benign volume is still short after a run, prepare and run more Tranco batches instead of planning recovery-based second-pass recapture.
- If the helper script itself should be removed from the repo later, open a separate explicit task for code removal and cleanup.
