<!-- operator: Codex; task: warden-snet-l1-fast-reproduction; date: 2026-05-08 -->

# Warden SNet L1-fast Reproduction Handoff

## 中文版

本次交付完成了 SNet 最小复现 smoke：read-only split builder、dataset adapter、DOM parser、纯 PyTorch SNet、train/eval CLI、per-sample score export、10 个 targeted tests，以及 64 条样本的 train/val/test smoke。

状态是 `PARTIAL`。原因是未找到现有 CLIP/MobileCLIP 输出，不能执行 CLIP-only 或 SNet+CLIP fusion；SNet-only smoke 的 p95 latency 为 `273.5284 ms/sample`，高于任务建议的 `<100ms/sample` 初始预算。

推荐结论：`keep exploratory`。不要从这次 smoke 直接进入 L1-fast ADR 接受状态。

## English Version

> AI note: English is authoritative for exact validation, compatibility, and status statements.

# Handoff Metadata

- Handoff ID: `HANDOFF-WARDEN-SNET-001-20260508`
- Related Task ID: `TASK-WARDEN-SNET-001`
- Task Title: `Reproduce SpecularNet-style SNet and evaluate SNet+CLIP for L1-fast`
- Module: `Warden L1-fast / model research / inference pipeline`
- Author: `Codex`
- Date: `2026-05-08`
- Status: `PARTIAL`
- Quota Mode: `CODEX_QUOTA_SUFFICIENT`
- Task Difficulty: `HIGH`
- Executor: `CODEX`
- Required Reviewer: `GPT_WEB`
- Codex Review Required: `NO`
- Codex Review Performed: `NOT_APPLICABLE`

---

## 1. Executive Summary

Implemented and smoke-tested a minimal SpecularNet-style SNet branch for Warden. The implementation reads Warden manifest records, requires rendered HTML, maps weak `label_hint` values to internal `benign=1` / `phish=0`, parses tag/attribute DOM structure while ignoring text and attribute values, trains a pure PyTorch SNet model, and exports test scores.

The task is partial because CLIP outputs were not found, so CLIP-only and SNet+CLIP fusion were not run. The SNet-only smoke also does not meet the initial latency budget.

Stop condition reached: SNet-only reproduction smoke completed; fusion blocked by missing CLIP outputs.

---

## 2. What Changed

### Code Changes

- Added `src/warden/models/snet/` with dataset adapter, DOM parser, vocab, and model modules.
- Added `scripts/build_snet_splits.py`.
- Added `scripts/train_snet.py`.
- Added `scripts/eval_snet.py`.
- Added targeted SNet tests under `tests/train/snet/`.

### Doc Changes

- Added task document: `docs/tasks/2026-05-08_warden_snet_l1_fast_reproduction.md`.
- Added research report: `docs/research/2026-05-08_warden_snet_l1_fast_reproduction_report.md`.
- Added this handoff document.

### Output / Artifact Changes

- Generated local ignored smoke artifacts under `E:\Warden\tmp\snet_l1_fast_smoke`.
- No raw dataset artifacts were mutated.

---

## 3. Files Touched

- `configs/train/snet_l1_fast_smoke.yaml`
- `docs/handoff/2026-05-08_warden_snet_l1_fast_reproduction.md`
- `docs/research/2026-05-08_warden_snet_l1_fast_reproduction_report.md`
- `docs/tasks/2026-05-08_warden_snet_l1_fast_reproduction.md`
- `scripts/build_snet_splits.py`
- `scripts/eval_snet.py`
- `scripts/train_snet.py`
- `src/warden/models/__init__.py`
- `src/warden/models/snet/__init__.py`
- `src/warden/models/snet/data.py`
- `src/warden/models/snet/dom.py`
- `src/warden/models/snet/model.py`
- `src/warden/models/snet/vocab.py`
- `tests/train/snet/test_attr_nodes_are_children.py`
- `tests/train/snet/test_domain_char_vocab.py`
- `tests/train/snet/test_dom_parser_ignores_text_and_values.py`
- `tests/train/snet/test_label_direction.py`
- `tests/train/snet/test_phish_score_equals_one_minus_benign_prob.py`
- `tests/train/snet/test_root_preserved_after_topk.py`
- `tests/train/snet/test_snet_forward_output_keys.py`
- `tests/train/snet/test_tree_reconnect_connects_to_retained_ancestor.py`

---

## 4. Behavior Impact

### Expected New Behavior

- Operators can build SNet split JSONL files from existing Warden manifests.
- Operators can train a minimal SNet checkpoint on Warden rendered-DOM samples.
- Operators can evaluate SNet and export per-sample SNet scores.

### Preserved Behavior

- Existing Warden L0/L1/L2 runtime behavior is unchanged.
- Existing labels, schema fields, and capture artifacts are unchanged.
- Existing CLIP / vision path behavior is unchanged.

### User-facing / CLI Impact

New optional research CLIs were added. No existing CLI was modified.

### Output Format Impact

New research outputs are JSON / JSONL under the user-provided output directory. Existing output schemas were not changed.

---

## 5. Schema / Interface Impact

- Schema changed: no.
- Backward compatible: yes.
- Public interface changed: no for existing interfaces; new research CLIs were added.
- Existing CLI still valid: yes.

Affected schema fields / interfaces:

- none

Compatibility notes:

The SNet score JSONL uses new `snet_*` fields only in research outputs. These are not wired into Warden runtime schema or production L1 outputs.

---

## 6. Validation Performed

### Commands Run

```powershell
python -m py_compile src\warden\models\snet\dom.py src\warden\models\snet\data.py src\warden\models\snet\vocab.py src\warden\models\snet\model.py scripts\build_snet_splits.py scripts\train_snet.py scripts\eval_snet.py
pytest tests\train\snet -q
python scripts\build_snet_splits.py --manifest E:\WardenData\processed\trainset_v1_externalization_smoke\manifest.jsonl --manifest E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup\manifest.jsonl --out-dir E:\Warden\tmp\snet_l1_fast_smoke --max-per-label 32 --seed 20260508
python scripts\train_snet.py --config configs\train\snet_l1_fast_smoke.yaml --train-split E:\Warden\tmp\snet_l1_fast_smoke\snet_train.jsonl --val-split E:\Warden\tmp\snet_l1_fast_smoke\snet_val.jsonl --out E:\Warden\tmp\snet_l1_fast_smoke\run --epochs 1
python scripts\eval_snet.py --checkpoint E:\Warden\tmp\snet_l1_fast_smoke\run\best.pt --split E:\Warden\tmp\snet_l1_fast_smoke\snet_test.jsonl --out E:\Warden\tmp\snet_l1_fast_smoke\run\eval_test.json --scores-out E:\Warden\tmp\snet_l1_fast_smoke\run\snet_scores_test.jsonl
```

### Result

- `py_compile`: passed.
- `pytest tests\train\snet -q`: `10 passed`.
- Split builder selected 64 samples: 32 benign and 32 phish.
- Train smoke completed 1 epoch.
- Eval smoke completed on 12 test samples.

SNet-only test smoke:

| Metric | Value |
|---|---:|
| test total | 12 |
| skipped | 0 |
| accuracy | 0.4166666666666667 |
| precision_phishing | 0.4444444444444444 |
| recall_phishing | 0.6666666666666666 |
| f1_phishing | 0.5333333333333333 |
| AUROC | 0.5555555555555556 |
| AUPRC | 0.7066498316498316 |

Latency, including DOM parse:

| Latency | ms/sample |
|---|---:|
| p50 | 244.01049999960378 |
| p95 | 273.528400000032 |
| p99 | 405.7066000004852 |

### Not Run

- CLIP-only evaluation was not run because no reusable CLIP/MobileCLIP per-sample outputs were found.
- SNet+CLIP fusion was not run because CLIP outputs were missing.
- Full corpus evaluation was not run; this was a 64-sample smoke.

Validation caveat:

- Pytest emitted a cache warning because `.pytest_cache` could not be created in the current Windows environment. Tests still passed.

---

## 7. Risks / Caveats

- The smoke set is too small for model-quality conclusions.
- The current implementation is a minimal pure-PyTorch research POC, not an optimized inference path.
- `gensim` was unavailable, so Word2Vec was not reproduced.
- CLIP-only and fusion comparisons were not run because no CLIP outputs were found.
- Weak `label_hint` values are not human gold labels.
- The measured p95 latency is above the initial budget.

---

## 8. Docs Impact

- Added repo-local task, research report, and handoff.
- No existing governing docs were modified by this task.
- No production runtime docs were updated because production behavior did not change.

---

## 9. Recommended Next Step

Keep SNet exploratory. The next task should first produce or locate CLIP/MobileCLIP per-sample outputs on the same split, then run a larger hard-negative evaluation and a simple logistic-regression fusion baseline. Do not wire SNet into L1-fast production routing from this smoke.
