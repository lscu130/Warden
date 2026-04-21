# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次“抓取 HTML 改为 JSON 存储并补旧样本转换脚本”的正式交接文档。
- 本次改动属于输出契约变更，已同步补下游兼容读取和文档更新。
- 若涉及精确文件名、兼容性、CLI、验证命令或风险结论，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CAPTURE-HTML-JSON-STORAGE-V1`
- 当前状态：`DONE`
- 新抓取样本不再把 HTML 落成裸 `.html` 文件，改为 `html_raw.json` / `html_rendered.json` 这类 JSON 封装。
- 下游读取侧已补新旧双读，旧样本仍可读。
- 新增 `scripts/data/maintenance/convert_legacy_html_to_json.py`，用于把老旧样本目录迁移到 JSON 形式。
- 仓库当前存在与本任务无关的已有脏改动；本 handoff 只覆盖下方明确列出的文件和行为。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-10-capture-html-json-storage
- Related Task ID: WARDEN-CAPTURE-HTML-JSON-STORAGE-V1
- Task Title: Store captured HTML payloads as JSON wrappers, keep downstream readers migration-compatible, and add a legacy HTML-to-JSON conversion utility
- Module: Data module / capture operations / labeling compatibility
- Author: Codex
- Date: 2026-04-10
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

Updated the capture path so newly emitted HTML artifacts are stored as JSON wrappers instead of raw `.html` files.
Added compatibility helpers so downstream readers now support both the new JSON HTML artifacts and legacy `.html` artifacts during migration.
Added a new maintenance utility, `scripts/data/maintenance/convert_legacy_html_to_json.py`, and updated the active docs/specs that describe the sample-output contract.

---

## 2. What Changed

### Code Changes

- Updated `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` to write `html_raw.json`, `html_rendered.json`, `after_action/step1_html_rendered.json`, and variant `html_rendered.json` via a shared JSON-wrapper helper.
- Added `scripts/data/common/html_payload_utils.py` for HTML JSON write/read, legacy `.html` fallback reads, and legacy-file conversion.
- Updated downstream readers and presence checks in `scripts/data/build_manifest.py`, `scripts/data/check_dataset_consistency.py`, `scripts/data/common/fingerprint_utils.py`, `scripts/data/benign/recover_benign_batch.py`, and `scripts/labeling/Warden_auto_label_utils_brandlex.py` to read the new JSON HTML artifacts while still accepting legacy `.html`.
- Added `scripts/data/maintenance/convert_legacy_html_to_json.py` as the explicit migration utility for older sample directories.

### Doc Changes

- Added the active task doc and this handoff doc.
- Updated current active data/spec/module docs so they now name `html_rendered.json` / `html_raw.json` instead of the old `.html` artifact names.
- Updated the runbook to include the new legacy conversion utility and operational notes about JSON HTML artifacts.

### Output / Artifact Changes

- New captures now write HTML payload wrappers as JSON files instead of raw `.html` files.
- Legacy sample directories are still readable by updated repo consumers.
- The migration utility can optionally convert older `.html` artifacts to JSON wrappers and optionally delete the old `.html` files.

---

## 3. Files Touched

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/common/html_payload_utils.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/common/fingerprint_utils.py`
- `scripts/data/benign/recover_benign_batch.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/data/maintenance/convert_legacy_html_to_json.py`
- `docs/tasks/2026-04-10_capture_html_json_storage.md`
- `docs/handoff/2026-04-10_capture_html_json_storage.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

Optional notes per file:

- The worktree already contained unrelated local changes and deletions outside this list; those were not reverted.
- `scripts/labeling/Warden_auto_label_utils_brandlex.py` already had pre-existing local modifications in the worktree; this task only layered the HTML JSON read-path compatibility on top of that file’s current state.
- `docs/frozen/SCHEMA_REGISTRY.md` is included because the active contract registry also needed to reflect the new HTML artifact naming.

---

## 4. Behavior Impact

### Expected New Behavior

- Successful new captures now persist HTML payloads as JSON wrappers such as `html_raw.json` and `html_rendered.json`.
- `after_action` and variant capture paths now store rendered HTML in JSON form as well.
- Repo consumers that read HTML payloads now accept the new JSON wrappers and fall back to legacy `.html` files when needed.
- Operators can convert older sample directories with `scripts/data/maintenance/convert_legacy_html_to_json.py`.

### Preserved Behavior

- Existing capture runner commands remain valid.
- Non-HTML sample artifacts such as `meta.json`, `url.json`, `visible_text.txt`, `forms.json`, screenshots, and `net_summary.json` keep their current names and meanings.
- Manifest booleans such as `has_html_rendered` and `has_html_raw` keep their existing semantic meaning.

### User-facing / CLI Impact

- Existing benign/malicious/capture CLIs remain valid without new required flags.
- New additive CLI:
  - `python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots ...`

### Output Format Impact

- HTML artifact file names changed from raw `.html` payload files to JSON wrappers for newly captured samples.
- Updated repo readers preserve migration compatibility by supporting both new and legacy forms.

Do not hand-wave here.

---

## 5. Schema / Interface Impact

- Schema changed: YES
- Backward compatible: PARTIAL
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- sample HTML artifact names: `html_raw.json`, `html_rendered.json`, `step1_html_rendered.json`
- manifest presence semantics for `has_html_rendered` / `has_html_raw`
- new maintenance CLI: `convert_legacy_html_to_json.py`

Compatibility notes:

This change is intentionally contract-changing for HTML artifact filenames in newly captured samples because the user explicitly requested JSON storage to reduce Windows security-tool quarantine risk.
Compatibility is preserved inside the repository by updating current readers to support both the new JSON wrappers and legacy `.html` files.
External tooling that still hardcodes raw `.html` file reads outside the updated repo consumers will need migration to the new JSON artifact names or must use the new helper/legacy fallback pattern.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py scripts/data/common/html_payload_utils.py scripts/data/build_manifest.py scripts/data/check_dataset_consistency.py scripts/data/common/fingerprint_utils.py scripts/data/benign/recover_benign_batch.py scripts/labeling/Warden_auto_label_utils_brandlex.py scripts/data/maintenance/convert_legacy_html_to_json.py
python scripts/data/maintenance/convert_legacy_html_to_json.py --help
python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots E:\Warden\temp\html_json_validation --dry_run --summary_path E:\Warden\temp\html_json_validation\dry_run_summary.json
python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots E:\Warden\temp\html_json_validation --summary_path E:\Warden\temp\html_json_validation\convert_summary.json
python scripts/data/build_manifest.py --help
python scripts/data/check_dataset_consistency.py --help
python -c "from pathlib import Path; from scripts.data.common.html_payload_utils import read_html_payload_text; text = read_html_payload_text(Path(r'E:\\Warden\\temp\\html_json_validation\\sample_a'), 'html_rendered.json'); print(text)"
```

### Result

- Confirmed all touched Python files pass `py_compile`.
- Confirmed the new conversion utility help output renders correctly and exposes `--dry_run`, `--overwrite`, `--delete_original_html`, `--summary_path`, and `--limit`.
- Confirmed a temporary sample directory with legacy `html_raw.html` and `html_rendered.html` converts successfully to `html_raw.json` and `html_rendered.json`.
- Confirmed `build_manifest.py --help` and `check_dataset_consistency.py --help` still import cleanly after the new helper-module dependency.
- Confirmed `read_html_payload_text(...)` can read the converted JSON payload back as HTML text.

### Not Run

- live browser capture against real URLs after the storage-format change
- full-dataset manifest rebuild
- full consistency sweep on the current dataset
- destructive-path validation for `--delete_original_html`

Reason:

This task was scoped to contract migration, compatibility reads, and utility-level validation.
Live capture and full-dataset sweeps are heavier operational checks and were not required to verify the correctness of the local code changes in this turn.

---

## 7. Risks / Caveats

- Newly captured samples no longer emit raw `.html` files for the migrated HTML artifacts, so any external non-repo tooling that still hardcodes `.html` paths will break until migrated.
- The repo worktree already contained unrelated local changes and deletions, including data directories and other module files; this handoff does not claim ownership of those unrelated changes.
- `--delete_original_html` was exposed by the migration utility but was not smoke-tested in this turn.
- Some existing docs outside the explicitly updated active contract set may still mention old `.html` names if they are historical records rather than current specs.

If there are no meaningful risks, say `none`.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-10_capture_html_json_storage.md`
- `docs/handoff/2026-04-10_capture_html_json_storage.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

Doc debt still remaining:

- Chinese runbook sections were not exhaustively expanded with the same new operational detail that was added to the English runbook section.
- Historical task/handoff docs that mention the old `.html` artifact names were intentionally left unchanged because they are historical records, not current active specs.

If none, say `none`.

---

## 9. Recommended Next Step

- Run one small real capture batch in the target VM and confirm new sample directories now emit `html_raw.json` / `html_rendered.json` without downstream breakage.
- Run `convert_legacy_html_to_json.py --dry_run` against the real legacy sample roots to estimate migration volume before deciding whether to use `--delete_original_html`.
- If any external tooling outside the updated repo still depends on raw `.html` artifact paths, migrate that tooling explicitly before treating the old filenames as retired.
