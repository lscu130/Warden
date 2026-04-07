# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次数据集目标下调到 `40K` 的正式 handoff。
- 若涉及精确文件清单、验证结果、兼容性或后续建议，以英文版为准。

### 摘要

- 对应任务：`WARDEN-DATASET-TARGET-RESIZE-40K-V1`
- 任务主题：把当前成对 benign / malicious 规划目标从 `50K` 下调到 `40K`
- 当前状态：`DONE`
- 所属模块：Data module / dataset planning docs

### 当前交付要点

- 当前有效规划目标已明确写成 benign `20K` + malicious train-pool `20K`。
- 本次只改规划文档，不改 capture、label、training 或任何 schema / CLI。
- 下调原因被明确表述为公开恶意来源约束下的现实规划决定，而不是通用最优值宣告。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-25-dataset-target-resize-40k
- Related Task ID: WARDEN-DATASET-TARGET-RESIZE-40K-V1
- Task Title: Reduce the current V1 paired benign-malicious dataset target from 50K total to 40K total under public-source constraints
- Module: Data module / dataset planning docs
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

Updated the current dataset-planning docs to reduce the paired benign-malicious target from 50K total to 40K total.
The active planning target is now 20K benign plus 20K malicious train-pool samples.
This was documented as a practical constraint-driven adjustment under the current public malicious-source baseline rather than as a universal methodological claim.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Updated `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md` to reduce the regular benign target from 25K to 20K and adjust the quota breakdown proportionally.
- Updated `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` to state that the current malicious train-pool planning target is 20K under the public-source baseline.
- Added this task/handoff pair to freeze the target-size change explicitly in the repo.

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-03-25_dataset_target_resize_40k.md`
- `docs/handoff/2026-03-25_dataset_target_resize_40k.md`

Optional notes per file:

- The benign strategy doc carries the explicit quota numbers and therefore required direct numeric updates.
- The malicious source policy previously described the source and pool policy without an explicit fixed planning total, so the current 20K target was added there as an operational planning note.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a documented paired planning target of 40K total samples rather than 50K total.
- Regular benign planning now targets 20K samples instead of 25K.
- Malicious planning now explicitly targets 20K train-pool samples under the current public-source baseline.

### Preserved Behavior

- OpenPhish Community + PhishTank remain the public malicious baseline.
- Capture, clustering, reserve routing, and family-share-cap logic remain unchanged.
- Raw malicious capture still needs to exceed the final train-pool target because deduplication and reserve routing are still applied.

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

- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`

Compatibility notes:

This step changes planning/documentation targets only.
It does not modify capture outputs, train-pool outputs, or any CLI/interface contract.

---

## 6. Validation Performed

### Commands Run

```bash
rg -n "25,000|20,000|40K|40,000|50K|50,000" docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md docs/tasks/2026-03-25_dataset_target_resize_40k.md docs/handoff/2026-03-25_dataset_target_resize_40k.md
```

### Result

- Confirmed the benign strategy doc now reflects the reduced 20K benign target and updated quota split.
- Confirmed the malicious source policy now documents the current 20K malicious train-pool planning target.
- Confirmed the new task and handoff docs exist and describe the 40K total paired target.

### Not Run

- code execution tests
- capture tests
- clustering/pool tests

Reason:

This step is a documentation-only planning update.
No code behavior changed.

---

## 7. Risks / Caveats

- Reducing the planning target does not guarantee that 20K malicious train-pool samples will be easy to obtain from public sources; it only makes the target more realistic.
- Because malicious train-pool size is post-dedup and post-reserve, raw capture volume still needs to stay above 20K by a meaningful margin.
- Older discussion or external notes may still mention the prior 50K total planning target until they are refreshed.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-03-25_dataset_target_resize_40k.md`
- `docs/handoff/2026-03-25_dataset_target_resize_40k.md`

Doc debt still remaining:

- If any external planning note or off-repo checklist still references the old 50K total, it should be updated separately.
- If the team later gains reliable higher-tier malicious sources, the target can be revisited in a new explicit planning task.

---

## 9. Recommended Next Step

- Use 20K benign plus 20K malicious train-pool samples as the active planning target.
- Continue to budget raw malicious capture above 20K because deduplication, reserve routing, and rejects still reduce the final train-pool count.
- If the source baseline changes in the future, revisit the target in a new explicit task instead of silently inflating it again.
