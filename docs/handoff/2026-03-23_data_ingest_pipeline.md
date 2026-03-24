# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次交接文档的中文摘要版。
- 若涉及精确命令、字段、状态、验证结果或兼容性结论，以英文版为准。

### 摘要

- 对应任务：WARDEN-DATA-INGEST-V1
- 任务主题：Split benign/malicious ingest pipelines, preserve the current capture engine, and implement malicious cluster/subcluster train-pool construction
- 当前状态：DONE
- 所属模块：Data module

### 当前交付要点

- 英文版记录了本次交付的变更、影响、验证、风险和建议下一步。
- 阅读时建议先看 Executive Summary，再看 Behavior Impact、Validation Performed 和 Risks / Caveats。
- 中文区块只保留压缩摘要，不改写原始结论和状态。

## English Version

# Handoff Metadata

- Handoff ID: 2026-03-23-data-ingest-pipeline-handoff
- Related Task ID: WARDEN-DATA-INGEST-V1
- Task Title: Split benign/malicious ingest pipelines, preserve the current capture engine, and implement malicious cluster/subcluster train-pool construction
- Module: Data module
- Author: Codex
- Date: 2026-03-23
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Synced the repository first and confirmed that the latest upstream commit (`036ba5c`, dated 2026-03-23) mainly added the new ingest-policy / architecture documentation and this task doc, but did not yet implement the pipeline scripts.
Implemented the first-pass data-ingest code layer: non-interactive capture orchestration hooks, separate benign and malicious upper-layer entrypoints, malicious feed ingest, malicious cluster/subcluster construction, train/reserve-pool construction, and legacy-data review/exclusion maintenance scripts.
The delivery is now marked `DONE`: local implementation and offline validation were completed in this workspace, and the missing live benign/malicious capture smoke was later executed in the user's VM and confirmed via returned validation artifacts.

---

## 2. What Changed

Describe the actual changes.

### Code Changes

- Updated `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` so upper-layer scripts can call it non-interactively via `--label`, `--output_root`, `--ingest_metadata_json`, and `--dry_run`, while preserving the existing capture logic and frozen output filenames.
- Added shared data-ingest helper modules under `scripts/data/common/` for JSON/JSONL IO, URL normalization, sample fingerprinting, and pool-decision logic.
- Added separate benign / malicious / maintenance scripts under `scripts/data/` for benign capture orchestration, OpenPhish/PhishTank ingest, malicious capture orchestration, malicious cluster/subcluster building, train/reserve pool construction, legacy-data backfill, dedup review manifest generation, and training exclusion-list generation.

### Doc Changes

- Updated `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md` with an implementation mapping section that points to the new script entrypoints and the capture CLI orchestration hooks.
- Updated `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md` with a current benign implementation mapping section.
- Updated `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` with a current malicious implementation mapping section.

### Output / Artifact Changes

- Added this handoff document under `docs/handoff/`.
- Generated smoke-test artifacts during validation and removed them afterward so they do not remain as repo outputs.

---

## 3. Files Touched

List only files actually touched.

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/common/io_utils.py`
- `scripts/data/common/url_utils.py`
- `scripts/data/common/fingerprint_utils.py`
- `scripts/data/common/pool_utils.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`
- `docs/handoff/2026-03-23_data_ingest_pipeline.md`

Optional notes per file:

- The capture script received minimal orchestration-facing changes rather than a full rewrite.
- The new `scripts/data/` tree is the main implementation payload of this task.
- The task doc is now marked `DONE` because the previously missing live-capture validation was completed in the user's VM and the resulting artifacts were reviewed.

---

## 4. Behavior Impact

Describe what behavior is now different.

### Expected New Behavior

- Capture can now be invoked from upper-layer scripts without interactive label selection.
- Benign and malicious now have separate upper-layer entrypoints instead of relying on one mixed strategy script.
- Malicious ingestion now has explicit script paths for public-feed ingest, cluster/subcluster construction, train/reserve decisions, and legacy-data review/exclusion outputs.

### Preserved Behavior

- The core capture logic was not rewritten.
- Frozen top-level sample filenames remain unchanged.
- Historical malicious sample directories are not physically deleted by default.

### User-facing / CLI Impact

- New upper-layer CLI entrypoints exist under `scripts/data/benign/`, `scripts/data/malicious/`, and `scripts/data/maintenance/`.
- The capture CLI now supports `--label`, `--output_root`, `--ingest_metadata_json`, and `--dry_run`.

### Output Format Impact

- Existing capture output filenames remain unchanged.
- New helper outputs are additive and include feed manifests, cluster records, pool decisions, review manifests, and exclusion lists.

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` CLI
- new upper-layer script entrypoints under `scripts/data/`
- additive `meta.json -> ingest_metadata` field when upper-layer metadata is provided

Compatibility notes:

The frozen capture output filenames were preserved.
The capture CLI remains backward compatible for existing `--input_path` / `--input_format` / `--csv_url_column` usage, but it now also exposes non-interactive orchestration flags.
The only additive output-structure change inside a sample is the optional `meta.json.ingest_metadata` field when upper-layer pipelines pass ingest metadata.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

List what was actually checked.

### Commands Run

```bash
git log --oneline --decorate -n 8
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
python E:\Warden\scripts\data\malicious\build_malicious_clusters.py --input_roots E:\Warden\data\raw\phish --output_dir E:\Warden\data\processed\malicious_clusters_smoke
python E:\Warden\scripts\data\maintenance\backfill_existing_sample_fingerprints.py --input_roots E:\Warden\data\raw\phish --output_dir E:\Warden\data\processed\malicious_backfill_smoke --emit_clusters --emit_review_manifest --emit_exclusion_list
python E:\Warden\scripts\data\malicious\build_malicious_train_pool.py --clusters_path E:\Warden\data\processed\malicious_clusters_smoke\malicious_cluster_records.jsonl --output_dir E:\Warden\data\processed\malicious_train_pool_smoke
python E:\Warden\scripts\data\maintenance\build_dedup_review_manifest.py --clusters_path E:\Warden\data\processed\malicious_clusters_smoke\malicious_cluster_records.jsonl --pool_decisions_path E:\Warden\data\processed\malicious_train_pool_smoke\pool_decisions.jsonl --output_dir E:\Warden\data\processed\malicious_review_smoke
python E:\Warden\scripts\data\maintenance\build_training_exclusion_lists.py --pool_decisions_path E:\Warden\data\processed\malicious_train_pool_smoke\pool_decisions.jsonl --output_dir E:\Warden\data\processed\malicious_exclusions_smoke
python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py --output_dir E:\Warden\data\processed\malicious_feed_smoke --openphish_input_path E:\Warden\data\processed\malicious_feed_smoke\openphish.txt --phishtank_input_path E:\Warden\data\processed\malicious_feed_smoke\phishtank.csv
python E:\Warden\scripts\data\benign\run_benign_capture.py --input_path E:\Warden\data\processed\benign_pipeline_smoke\urls.txt --output_root E:\Warden\data\processed\benign_pipeline_smoke --source tranco --rank_bucket top_1_10000 --dry_run
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --input_path E:\Warden\data\processed\malicious_pipeline_smoke\urls.txt --source openphish_community --output_root E:\Warden\data\processed\malicious_pipeline_smoke --dry_run
```

### Result

- Confirmed that the latest repo sync state was a clean worktree on top of commit `036ba5c`, where docs had been added but ingest implementation was still missing.
- Confirmed Python syntax/import sanity for the new and modified scripts via `py_compile`, and confirmed the capture CLI help now works without crashing at import time.
- Confirmed legacy malicious sample backfill, cluster/subcluster construction, train-pool/reserve-pool decisions, review-manifest generation, exclusion-list generation, and local feed-ingest smoke all run successfully on the available local sample / local feed fixtures.
- Reviewed user-provided VM live-capture artifacts:
  - `benign_capture_run.json`: `returncode = 0`, with `ingest_metadata.pipeline = "benign"`, `source = "vm_benign_smoke"`, `rank_bucket = "manual_smoke"`, `page_type = "homepage"`, and `language_hint = "en"`.
  - `malicious_capture_run.json`: `all_success = true`, `returncodes = [0]`, confirming a successful live malicious capture run from the VM feed subset manifest.
  - `malicious_cluster_summary.json`: `total_records = 11`, `valid_records = 11`, `invalid_records = 0`, `cluster_count = 11`, `subcluster_count = 11`, `family_count = 8`.
  - `pool_summary.json`: `total_records = 11`, `train_count = 8`, `reserve_count = 3`, `reject_count = 0`, `family_share_cap = 0.1`.
  - `malicious_cluster_records.jsonl`: reviewed representative records and confirmed populated sample-level fields for normalized/final URLs, fingerprints, cluster IDs, subcluster IDs, validity status, and forms summaries.

### Not Run

- direct local rerun of the VM live-capture commands inside this workspace

Reason:

The live-capture validation was executed in the user's VM rather than duplicated in this workspace.
This workspace still lacks a runnable `playwright` environment, so the final acceptance evidence is based on the returned VM artifacts instead of a redundant local rerun.

---

## 7. Risks / Caveats

- The current malicious clustering logic is deterministic and auditable, but still heuristic; it is a first-pass implementation, not a paper-grade final clustering algorithm.
- Feed-ingest dedup is normalized-URL based within the ingest script, while deeper cross-feed family/template dedup is deferred to the later cluster/subcluster stage by design.
- On Windows, ad hoc JSONL slicing with `Get-Content | Set-Content` can introduce a UTF-8 BOM at the first line; the IO layer now tolerates BOM-marked files, but JSONL subset creation should still prefer a script-based rewrite instead of shell text piping.

If there are no meaningful risks, say `none`.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`

Doc debt still remaining:

- none

If none, say `none`.

---

## 9. Recommended Next Step

- Run a somewhat larger OpenPhish/PhishTank end-to-end ingest sample next and inspect whether the current heuristic family/grouping outputs remain stable as sample diversity increases.
- Spot-check a few produced `meta.json.ingest_metadata` records and downstream pool decisions together to confirm that source attribution and reserve routing remain aligned on less clean malicious pages.
- If the first-pass malicious clustering heuristics prove too coarse on larger data, refine the cluster/subcluster seeds while preserving the same auditable output interfaces.


