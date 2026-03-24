# Data README

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档解释 `data/` 目录的职责和边界。
- 涉及精确目录、文件名和派生物命名时，以英文版为准。

## 1. 目录作用

`data/` 用于承载 Warden 的原始样本、派生产物、中间检查结果以及与数据相关的可复现实验输入。
重点不是“存文件”，而是保证数据流可追踪、可审计、可回放。

## 2. 关键边界

- 原始样本与派生产物应尽量分层管理。
- 运行期中间结果不应冒充冻结规格或长期契约。
- 与训练、标注、推理相关的下游步骤都应尊重这里定义的数据边界。

## 3. 阅读重点

建议优先查看英文版中关于目录职责、输入输出边界和长期保留规则的部分。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

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

