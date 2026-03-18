# HANDOFF_TEMPLATE.md

# Handoff Metadata

- Handoff ID: HANDOFF-2026-03-18-REPO-ALIGNMENT-SMOKE-FREEZE
- Related Task ID: TASK-2026-03-18-REPO-ALIGNMENT
- Task Title: Align repo to TRAINSET_V1 and freeze smoke-validation stage
- Module: data / labeling / workflow-doc
- Author: Codex
- Date: 2026-03-18
- Status: DONE

---

## 1. Executive Summary

Aligned the active repo paths and docs to current Warden naming for TRAINSET_V1, restored formal data entry scripts for manifest build and consistency check, and completed a small smoke validation on the currently available sample set.

This stage is now frozen at smoke-validation level only.

Deferred until data collection is sufficiently complete:

- full-dataset manifest build
- full-dataset consistency check
- rule-label backfill at larger scale
- split generation execution

---

## 2. What Changed

### Code Changes
- Added formal data entry script `scripts/data/build_manifest.py`
- Added formal data entry script `scripts/data/check_dataset_consistency.py`
- Updated `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py` usage examples to Warden naming
- Updated `scripts/labeling/Warden_auto_label_utils_brandlex.py` so active lexicon discovery prefers `WARDEN_BRAND_LEXICON` and Warden-style filenames before EVT fallback

### Doc Changes
- Updated `docs/data/TRAINSET_V1.md` to use Warden active script names and explicit manifest/check workflow
- Added `docs/modules/MODULE_DATA.md` as the current data-module contract entry
- Added `data/README.md` as the practical data workflow note for current stage
- Updated `docs/workflow/GPT_CODEX_WORKFLOW.md` to require Codex to remind the user when a task should return to GPT web

### Output / Artifact Changes
- Smoke outputs generated under `data/processed/trainset_v1_smoke/`
- Consistency reports generated under `data/processed/trainset_v1_smoke/consistency_check/`

---

## 3. Files Touched

- `docs/data/TRAINSET_V1.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/modules/MODULE_DATA.md`
- `docs/handoff/2026-03-18_repo_alignment_smoke_freeze.md`
- `data/README.md`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

Optional notes per file:

- `docs/modules/MODULE_DATA.md`: new module specification file
- `data/README.md`: operational note, not a frozen schema spec

---

## 4. Behavior Impact

### Expected New Behavior
- Active docs and paths now point to Warden-named backfill/label utilities instead of EVT names
- Data-module formal entry points now exist for manifest build and consistency check
- Default brand lexicon discovery now prefers Warden naming first, while preserving EVT fallback compatibility

### Preserved Behavior
- Frozen sample directory structure is unchanged
- Existing top-level JSON key semantics are unchanged
- Weak labels remain weak labels; no gold-label reinterpretation was introduced

### User-facing / CLI Impact
- New formal commands are available:
  - `python scripts/data/build_manifest.py ...`
  - `python scripts/data/check_dataset_consistency.py ...`

### Output Format Impact
- `build_manifest.py` produces `manifest.jsonl`, `manifest_rejected.jsonl`, and `build_summary.json`
- `check_dataset_consistency.py` produces JSON and Markdown consistency reports plus summary JSON

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- brand lexicon discovery environment variable priority

Compatibility notes:

No frozen sample-file names or top-level JSON key semantics were changed.
`auto_labels.json` / `rule_labels.json` schema version strings remain unchanged.
The new public script interfaces are additive.
EVT lexicon discovery remains as fallback for compatibility with older setups.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py E:\Warden\scripts\data\build_manifest.py E:\Warden\scripts\data\check_dataset_consistency.py
python E:\Warden\scripts\data\build_manifest.py --data-root E:\Warden\data --input-roots E:\Warden\data\raw\benign E:\Warden\data\raw\phish --out-dir E:\Warden\data\processed\trainset_v1_smoke
python E:\Warden\scripts\data\check_dataset_consistency.py --data-root E:\Warden\data --manifest E:\Warden\data\processed\trainset_v1_smoke\manifest.jsonl --out-dir E:\Warden\data\processed\trainset_v1_smoke\consistency_check
```

### Result

- `py_compile`: passed
- smoke manifest build: passed on current available sample set
- smoke consistency check: passed with `errors=0`, `warnings=0`

### Not Run

- full-dataset manifest build
- full-dataset consistency check
- full rule-label backfill
- split generation

Reason:

Current project stage is still data collection. Those steps are intentionally deferred until collection is sufficiently complete.
