# 2026-04-23_plan_a_batch_capture_day15_result_receipt_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 `2026-04-23` 对 Plan A Day 15 回传结果做收口的任务定义。
- 本任务基于 `E:\WardenData\raw\benign\tranco` 下的 Day 15 `benign_capture_run.json` 文件。
- Day 15 的 `batch_0007` 是 partial artifact，不能写成完整 `1000` 条。

## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY15-RESULT-RECEIPT-V1
- Task Title: Record returned Day 15 benign Tranco artifacts from WardenData with an explicit partial caveat for batch 0007
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- Created At: 2026-04-23
- Requested By: user

---

## 1. Background

Day 15 was still recorded as `selected` in the Plan A tracker.
The returned Day 15 Tranco artifacts are present under `E:\WardenData\raw\benign\tranco`, with one `benign_capture_run.json` per batch.

The Day 15 `batch_0007` JSON contains only `565` result rows, so Day 15 must be closed with an explicit partial caveat.

---

## 2. Goal

Record the actual Day 15 `benign_capture_run.json` paths and counts, align the Day 15 prep output roots to `E:\WardenData\raw\benign\tranco`, and update the tracker so Day 15 is marked `results_received` with a partial caveat for `batch_0007`.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

This task is allowed to change:

- Day 15 result-receipt docs
- Day 15 tracker receipt state
- Day 15 prep handoff output-root references

---

## 4. Scope Out

This task must NOT do the following:

- do not modify capture code
- do not rerun Day 15 capture
- do not fabricate `batch_0007` completeness
- do not change Day 15 queue membership
- do not rename schema fields or CLI flags

---

## 5. Inputs

### Docs

- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

### Data / Artifacts

- `E:\WardenData\raw\benign\tranco\2026-04-21_planA_day15_tranco_top_10001_100000_batch_0007\benign_capture_run.json`
- `E:\WardenData\raw\benign\tranco\2026-04-21_planA_day15_tranco_top_10001_100000_batch_0008\benign_capture_run.json`
- `E:\WardenData\raw\benign\tranco\2026-04-21_planA_day15_tranco_top_10001_100000_batch_0009\benign_capture_run.json`

### Missing Inputs

- none for receipt closure

---

## 6. Required Outputs

- Day 15 result-receipt task doc
- Day 15 result-receipt handoff
- tracker update from `selected` to `results_received`

---

## 7. Hard Constraints

- Preserve backward compatibility.
- Do not change capture code.
- Do not change output schema.
- Keep `batch_0007` partial state explicit.
- Follow `AGENTS.md` and required handoff rules.

---

## 8. Interface / Schema Constraints

- Schema changed allowed: NO
- Public interface changed: NO
- Existing CLI still valid: YES

---

## 9. Suggested Execution Plan

1. Parse the three Day 15 `benign_capture_run.json` files.
2. Record counts and paths.
3. Align Day 15 prep output roots to `E:\WardenData\raw\benign\tranco`.
4. Mark Day 15 `results_received` in the tracker with a partial caveat.

---

## 10. Acceptance Criteria

- [ ] Day 15 result paths and counts are recorded
- [ ] Day 15 tracker row reads `results_received`
- [ ] Day 15 prep paths use `E:\WardenData\raw\benign\tranco`
- [ ] `batch_0007` partial state is explicit
- [ ] no code behavior changed
- [ ] handoff is provided

---

## 11. Validation Checklist

Expected evidence:

- `batch_0007`: `565` results, `554` success, `11` timed_out, `0` skipped
- `batch_0008`: `1000` results, `997` success, `3` timed_out, `0` skipped
- `batch_0009`: `1000` results, `996` success, `4` timed_out, `0` skipped

---

## 12. Handoff Requirements

- `docs/handoff/2026-04-23_plan_a_batch_capture_day15_result_receipt.md`

---

## 13. Open Questions / Blocking Issues

- none
