# Data README

This directory stores Warden dataset artifacts and derived dataset-preparation outputs.

Current stage note:

- data collection is still in progress
- smoke validation for manifest build and consistency check is frozen as complete
- full-dataset processing is intentionally deferred until collection is sufficiently complete

---

## Current Relevant Paths

- raw samples: `data/raw/`
- smoke manifest outputs: `data/processed/trainset_v1_smoke/`

Formal data entry scripts:

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

Auxiliary-set note:

- gate / evasion auxiliary-set protocol is documented in `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- it is separate from TrainSet V1 primary
- current data scripts do not default-admit that auxiliary set into primary manifest output

---

## Minimal Workflow For Current Stage

1. Continue collecting raw samples under `data/raw/phish` and `data/raw/benign`
2. Use `build_manifest.py` only for smoke checks or spot checks
3. Use `check_dataset_consistency.py` only for smoke checks or spot checks
4. Defer full manifest build, full consistency sweep, and large-scale rule backfill until data collection is sufficiently complete

---

## Minimal Commands

Build smoke manifest:

```bash
python scripts/data/build_manifest.py --data-root ./data --input-roots ./data/raw/phish ./data/raw/benign --out-dir ./data/processed/trainset_v1_smoke
```

Check smoke manifest consistency:

```bash
python scripts/data/check_dataset_consistency.py --data-root ./data --manifest ./data/processed/trainset_v1_smoke/manifest.jsonl --out-dir ./data/processed/trainset_v1_smoke/consistency_check
```

---

## Deferred Until Later

- full manifest generation over the full collected dataset
- full consistency report over the full collected dataset
- large-scale `rule_labels.json` backfill
- split execution for training use
- any auxiliary-set-specific script interface, unless a later task explicitly adds an opt-in default-off path

`split_dataset.py` should be handled only after the next task is frozen via GPT web review.
