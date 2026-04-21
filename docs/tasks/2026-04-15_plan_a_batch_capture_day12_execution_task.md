# 2026-04-15_plan_a_batch_capture_day12_execution_task

## 涓枃鐗?> 闈㈠悜 AI 鐨勮鏄庯細GPT銆丟emini銆丆odex銆丟rok銆丆laude 浠呭皢涓嬫柟鑻辨枃鐗堣涓烘潈濞佺増鏈€備腑鏂囦粎渚涗汉绫婚槄璇汇€佸崗浣滀笌蹇€熷瑙堛€?
### 浣跨敤璇存槑

- 杩欐槸 `2026-04-15` Plan A Day 12 鎶撳彇闃熷垪鐨勪换鍔″畾涔夈€?- 褰撳墠鏃ュ父鍙ｅ緞缁х画鏄?benign-only銆佹瘡澶?3 鎵广€?- 鑻ユ秹鍙婄簿纭壒娆°€佽緭鍑烘牴鐩綍銆佸懡浠ゅ弬鏁版垨鏃ユ湡杈圭晫锛屼互鑻辨枃鐗堜负鍑嗐€?
## 1. 鑳屾櫙

Day 7 鍒?Day 11 宸茬粡杩涘叆 benign-only銆佹瘡澶?3 鎵圭殑鍥哄畾妯″紡銆?鐜板湪 Day 11 宸茬粡鍙互鎸夊洖浼?JSON 鏀跺彛锛屽洜姝?Day 12 闇€瑕佺户缁部鐫€鍓╀綑鍙敤 benign tranche 寰€鍚庢帓銆?
褰撳墠浠撳簱鏈湴 split 浠嶇劧缂哄皯 `tranco_top_1_10000_batch_0005_urls.txt`銆?鍚屾椂 `top_10001_100000` 宸茬粡鍦?Day 11 鐢ㄥ埌 `batch_0014`锛宍top_500001_1000000` 宸茬粡鍦?Day 10 鐢ㄥ埌 `batch_0006`銆?鍥犳 Day 12 鍙兘缁х画浣跨敤褰撳墠浠嶆湁鍓╀綑鐨?`top_100001_500000`銆?
## 2. 鐩爣

鍐荤粨 `2026-04-15` Day 12 鐨?benign-only 鎶撳彇闃熷垪锛岀粰鍑哄彲鐩存帴鎵ц鐨?3 涓?benign 鎵规銆佽緭鍑烘牴鐩綍鍜屾帹鑽愬懡浠わ紝骞跺悓姝ユ洿鏂?tracker銆?
## 3. 鑼冨洿

- 绾冲叆锛欴ay 12 闃熷垪浠诲姟瀹氫箟銆佸搴?vm prep / handoff銆乼racker 鍚屾
- 鎺掗櫎锛歝apture 浠ｇ爜閫昏緫銆丏ay 11 缁撴灉澶嶇洏銆乵alicious 闃熷垪銆乧luster / pool銆佸巻鍙叉牱鏈噸绠?
## English Version

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-DAY12-V1
- Task Title: Freeze the 2026-04-15 Plan A Day 12 benign-only queue at three batches per day
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`; `docs/tasks/2026-04-08_plan_a_batch_capture_day11_execution_task.md`; `docs/handoff/2026-04-08_plan_a_batch_capture_day11_vm_prep.md`; `docs/tasks/2026-04-15_plan_a_batch_capture_day11_result_receipt_task.md`; `docs/handoff/2026-04-15_plan_a_batch_capture_day11_result_receipt.md`
- Created At: 2026-04-15
- Requested By: user

---

## 1. Background

Day 7 through Day 11 already established the benign-only steady-state with exactly `3` benign batches per day.
Day 11 has now been closed from `selected` to `results_received` based on the returned Day 11 JSON package, so Day 12 can be queued from a clean continuity baseline.

Within the currently available repo-local Tranco split, `tranco_top_1_10000_batch_0005_urls.txt` is still absent.
Also, `top_10001_100000` has now been consumed through `batch_0014`, and `top_500001_1000000` was already exhausted at `batch_0006`.
That means Day 12 must continue with the next `3` available benign batches from `top_100001_500000`.

---

## 2. Goal

Create an execution-ready task definition for the 2026-04-15 Plan A Day 12 queue.
This task must freeze:

- the exact `3` benign batches assigned to Day 12,
- the exact output roots for each batch,
- the exact supervised skip-capable commands that remain the recommended default commands,
- and the matching tracker update while preserving benign-only daily planning semantics.

The intended 2026-04-15 Day 12 queue is:

- benign:
  - `tranco_top_100001_500000_batch_0009`
  - `tranco_top_100001_500000_batch_0010`
  - `tranco_top_100001_500000_batch_0011`

No malicious batches are assigned to Day 12.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/modules/`

This task is allowed to change:

- daily execution-boundary docs
- exact batch-to-output-root mapping for Day 12
- tracker continuity docs
- operator command examples for Day 12

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not reopen Day 11 receipt closure
- do not schedule malicious batches for Day 12
- do not rename frozen schema fields, outputs, or CLI flags
- do not claim that the 2026-04-15 queue has already been executed

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/tasks/2026-04-08_plan_a_batch_capture_day11_execution_task.md`
- `docs/handoff/2026-04-08_plan_a_batch_capture_day11_vm_prep.md`
- `docs/tasks/2026-04-15_plan_a_batch_capture_day11_result_receipt_task.md`
- `docs/handoff/2026-04-15_plan_a_batch_capture_day11_result_receipt.md`

### Code / Scripts

- `scripts/data/benign/run_benign_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `tranco csv/tranco_top_100001_500000_batch_0009_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0010_urls.txt`
- `tranco csv/tranco_top_100001_500000_batch_0011_urls.txt`

### Missing Inputs

- no new malicious artifacts are required for Day 12 because malicious is intentionally out of scope for this day
- no `tranco_top_1_10000_batch_0005_urls.txt` exists in the current repo-local split
- no new `top_10001_100000` batch remains after `tranco_top_10001_100000_batch_0014_urls.txt`
- no new `top_500001_1000000` batch remains after `tranco_top_500001_1000000_batch_0006_urls.txt`

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the 2026-04-15 Day 12 queue
- a repo prep/handoff doc with exact commands and output roots for Day 12
- a tracker update row for Day 12 in `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`

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

- Day 12 must be benign-only.
- Day 12 must contain exactly `3` benign batches.
- Use the current supervised skip-capable commands as the recommended default commands for Day 12.
- Be explicit that Day 12 still cannot use `top_1_10000_batch_0005` because that file remains absent in the current split.
- Be explicit that Day 12 cannot use a new `top_10001_100000` batch because that local tranche is now exhausted through `batch_0014`.
- Be explicit that Day 12 cannot use a new `top_500001_1000000` batch because that bucket is exhausted in the current local split.
- Keep rank priority explicit: continue with the highest-value remaining benign batches rather than introducing a new source or a gap.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/benign/run_benign_capture.py` CLI
- current output-root naming discipline

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current benign runner commands
  - current capture script commands

Downstream consumers to watch:

- operators resuming or auditing Plan A batch lineage
- later benign run-result handoff writing
- the Plan A batch tracker

---

## 9. Suggested Execution Plan

Recommended order:

1. Preserve Day 11 as `results_received` based on the returned JSON package.
2. Create a new 2026-04-15 task boundary for Day 12.
3. Freeze the `3`-batch benign-only queue for Day 12.
4. Freeze exact supervised commands and output roots for Day 12.
5. Update the Plan A batch tracker in the same turn.

Task-specific execution notes:

- Day 12 uses no malicious batches.
- Day 12 selects `3` benign batches in rank-priority order from the remaining non-exhausted buckets.
- `top_100001_500000_batch_0009` through `batch_0011` are selected because that tranche is the highest-priority remaining benign source still available in the local split.
- `top_1_10000`, `top_10001_100000`, and `top_500001_1000000` contribute no Day 12 batch under the current local inventory.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the 2026-04-15 Day 12 queue has its own repo task doc
- [ ] the doc freezes the exact `3` benign batches listed above
- [ ] the doc states that Day 12 has no malicious queue
- [ ] the doc explains why no `top_1_10000` batch is used
- [ ] the doc explains why no `top_10001_100000` batch is used
- [ ] the doc explains why no `top_500001_1000000` batch is used
- [ ] the doc provides exact output roots and exact commands
- [ ] the tracker is updated in the same turn
- [ ] Day 11 remains `results_received`
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] local batch filenames exist and match the doc
- [ ] referenced runner scripts still expose the required supervised flags
- [ ] tracker row for Day 12 was added
- [ ] Day 11 tracker status now reads `results_received`

Commands to run if applicable:

```bash
python scripts/data/benign/run_benign_capture.py --help
python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

Expected evidence to capture:

- confirmed input filenames for the Day 12 queue
- exact output roots for the Day 12 queue
- exact supervised commands for the Day 12 queue
- tracker update evidence

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

- `docs/handoff/2026-04-15_plan_a_batch_capture_day12_vm_prep.md`

---

## 13. Open Questions / Blocking Issues

- none


