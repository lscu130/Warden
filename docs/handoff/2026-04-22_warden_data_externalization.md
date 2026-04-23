# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是一份 `data` 外迁任务的实际执行 handoff。
- 本次已经完成代码默认根更新、活跃文档更新、物理目录迁移和小规模烟测。
- repo 内 `E:\Warden\data` 现在只保留 `README.md`，运行期目录已经迁到 `E:\WardenData`。

### 摘要

- 统一把活跃脚本的默认运行期数据根切到 `E:\WardenData`。
- 把 `raw/ processed/ manifests/ reviewed/ stats/` 从 repo 内 `data/` 挪到了 `E:\WardenData`。
- 用 `E:\WardenData` 跑通了 `build_manifest.py` 和 `check_dataset_consistency.py` 的小规模烟测。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-22-warden-data-externalization
- Related Task ID: WARDEN-DATA-ROOT-EXTERNALIZATION-V1
- Task Title: Externalize Warden runtime data root from repo-local `E:\Warden\data` to external `E:\WardenData`
- Module: Data module / repo portability / local operations
- Author: Codex
- Date: 2026-04-22
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.
- Write this Markdown handoff in bilingual form by default: Chinese summary first, full English version second, with English authoritative for exact facts, commands, validation, and compatibility statements.

---

## 1. Executive Summary

Completed the Warden runtime data-root externalization to `E:\WardenData`.
Active scripts that previously defaulted to repo-local `data/` now default to the external root through a shared helper.
Active operational docs and command examples that are still meant to be reused were updated to point to `E:\WardenData`.
The runtime directories `raw`, `processed`, `manifests`, `reviewed`, and `stats` were moved out of `E:\Warden\data`, while `E:\Warden\data\README.md` remained in the repository as documentation.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/common/runtime_data_root.py` as the shared helper for the active runtime data root.
- Updated active manifest, consistency, capture, malicious-processing, and backfill scripts so their default runtime paths resolve to `E:\WardenData`.
- Preserved CLI override behavior: callers can still pass explicit paths when needed.

### Doc Changes

- Updated `data/README.md`, `docs/modules/MODULE_DATA.md`, `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`, `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`, `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`, `tests/smoke/README.md`, `tests/smoke/golden_manifest.example.json`, and `tranco csv/README.md` to reflect the externalized runtime root where those docs still serve as active operational references.
- Updated `docs/tasks/2026-04-21_warden_data_externalization_task.md` to remove the already-resolved target-path naming blocker.

### Output / Artifact Changes

- Moved `E:\Warden\data\raw` to `E:\WardenData\raw`
- Moved `E:\Warden\data\processed` to `E:\WardenData\processed`
- Moved `E:\Warden\data\manifests` to `E:\WardenData\manifests`
- Moved `E:\Warden\data\reviewed` to `E:\WardenData\reviewed`
- Moved `E:\Warden\data\stats` to `E:\WardenData\stats`

---

## 3. Files Touched

- `.gitignore`
- `data/README.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/tasks/2026-04-21_warden_data_externalization_task.md`
- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- `docs/handoff/2026-04-22_warden_data_externalization.md`
- `scripts/data/common/runtime_data_root.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/malicious/export_phishtank_verified_urls.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `tests/smoke/README.md`
- `tests/smoke/golden_manifest.example.json`
- `tranco csv/README.md`

Optional notes per file:

- `.gitignore` already had the earlier repo-local data/tranco/tmp ignore cleanup from the preceding turn.
- The migration left `E:\Warden\data\README.md` in place on purpose so the repo still carries a local documentation anchor.

---

## 4. Behavior Impact

### Expected New Behavior

- Active scripts that used repo-local `data/` defaults now resolve to `E:\WardenData` by default.
- New runtime artifacts are expected under `E:\WardenData\raw\...`, `E:\WardenData\processed\...`, and related external-root paths.
- Repo-local `E:\Warden\data` is no longer the steady-state runtime storage location.

### Preserved Behavior

- Sample directory internal structure remains unchanged.
- Schema, label semantics, manifest field names, and capture output semantics remain unchanged.
- CLI callers can still provide explicit path arguments instead of relying on the default root.

### User-facing / CLI Impact

- Default path behavior changed for active scripts that previously defaulted to repo-local `data/`.
- Explicit CLI arguments still override the defaults.

### Output Format Impact

- none

Do not hand-wave here.
If behavior did not change, say so explicitly.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- runtime default data-root contract
- manifest and consistency CLI defaults
- capture runner default output-root behavior

Compatibility notes:

The change affects only default filesystem locations.
It does not rename schema fields, modify sample contents, or alter manifest core columns.
Users who still need repo-local or custom paths can continue to pass explicit CLI arguments.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\build_manifest.py --help
python E:\Warden\scripts\data\check_dataset_consistency.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
@' 
from scripts.data.common.runtime_data_root import get_data_root
print(get_data_root())
'@ | python -
@'
import scripts.data.build_manifest as m
print(m.CONFIG_DATA_ROOT)
print(m.CONFIG_INPUT_ROOTS)
print(m.CONFIG_OUTPUT_DIR)
'@ | python -
python E:\Warden\scripts\data\build_manifest.py --data-root E:\WardenData --input-roots E:\WardenData\raw\phish E:\WardenData\raw\benign --out-dir E:\WardenData\processed\trainset_v1_externalization_smoke --limit 5
python E:\Warden\scripts\data\check_dataset_consistency.py --data-root E:\WardenData --manifest E:\WardenData\processed\trainset_v1_externalization_smoke\manifest.jsonl --out-dir E:\WardenData\processed\trainset_v1_externalization_smoke\consistency_check --strict
```

### Result

- Confirmed the active runtime data root resolves to `E:\WardenData`.
- Confirmed `build_manifest.py` now defaults to `E:\WardenData` and external-root input/output paths.
- Confirmed capture entry scripts still load and expose their CLI help normally after the default-root change.
- Successfully built a 5-sample smoke manifest from `E:\WardenData`.
- Successfully ran the matching strict consistency check with `0` errors and `0` warnings.

### Not Run

- full-dataset manifest build
- full-dataset consistency sweep
- live benign capture after migration
- live malicious capture after migration

Reason:

This turn used the smallest meaningful validation path.
Full-dataset processing and live capture runs would be heavier than needed for confirming the migration contract.

---

## 7. Risks / Caveats

- Historical handoffs and older archived docs still contain factual repo-local `E:\Warden\data\...` paths. Those were intentionally not bulk-rewritten.
- The remaining repo-wide old-path hits are concentrated in historical task and handoff records, so a blind full-repo replacement would risk damaging factual audit trails.
- Operators who have local automation or shell history that assumed repo-local defaults may still need to refresh their commands.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `data/README.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/modules/Warden_PLAN_A_BATCH_TRACKER.md`
- `docs/tasks/2026-04-21_warden_data_externalization_task.md`
- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- `tests/smoke/README.md`
- `tests/smoke/golden_manifest.example.json`
- `tranco csv/README.md`
- `docs/handoff/2026-04-22_warden_data_externalization.md`

Doc debt still remaining:

- archived handoffs and older historical records still reference repo-local `E:\Warden\data\...`

---

## 9. Recommended Next Step

- When you are ready, do one live benign or malicious post-migration run and write a short receipt handoff that confirms the new external-root outputs are being produced in normal operation.
