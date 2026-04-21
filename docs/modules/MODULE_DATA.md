# MODULE_DATA.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Data 模块的责任和边界。
- 涉及冻结样本结构、入口脚本和输入契约时，以英文版为准。

## 1. 模块作用

Data 模块负责读取冻结样本目录、生成 manifest、做一致性检查，并为后续 split、训练和评估提供可审计的输入。
它的重点是让数据摄取可复现，而不是重写上游 capture 或下游训练逻辑。

## 2. 责任边界

Data 模块拥有：目录扫描、manifest 生成、数据一致性检查、样本可用性标记和摘要输出。
Data 模块不拥有：capture 行为重构、标签本体重写、训练目标定义和推理阈值策略。

补充边界说明：

- 默认正式入口脚本应保持只读，不修改上游样本目录。
- 若存在数据维护脚本，它们必须明确标注为 maintenance utility，而不是默认 intake 流程。
- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py` 属于显式 opt-in 维护工具：按目录名中的 URL 键去重，默认 dry-run，仅在显式 `--delete` 时删除较新的重复目录。

## 3. 阅读重点

优先看英文版的 `Core Responsibility`、`Current Active Entry Points` 和 `Input Contract`。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# MODULE_DATA.md

# Warden Data Module Specification

## 1. Module Purpose

The Data module defines how Warden reads frozen sample directories, builds derived manifests, and checks dataset consistency without mutating upstream sample artifacts.

This module is responsible for making dataset intake reproducible and auditable before later split, training, and evaluation steps.

This module must not silently redefine sample schema, label semantics, or training behavior.

---

## 2. Core Responsibility

The Data module owns:

- dataset directory scanning
- manifest generation
- dataset consistency checks
- sample availability flags for later text / vision / multimodal filtering
- summary artifacts for later split or training preparation

The Data module does not own:

- raw capture behavior redesign
- weak-label ontology redesign
- training target definition
- inference threshold policy

---

## 3. Current Active Entry Points

Current formal data entry scripts are:

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

They operate on the current TRAINSET_V1 frozen sample layout and are intentionally read-only with respect to sample directories.

Separate opt-in maintenance utilities may exist under `scripts/data/maintenance/`, but they are not part of the default manifest-intake path.

Current maintenance utility explicitly added for channel hygiene:

- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`

This utility:

- scans direct child sample directories under a channel root,
- groups directories by the URL key encoded in `<url_key>_<YYYYMMDDTHHMMSSZ>`,
- keeps the oldest timestamped directory for each URL key,
- defaults to dry-run and only deletes duplicates when `--delete` is explicitly provided.

Current default boundary:

- they target TrainSet V1 primary intake
- they do not default-admit gate / evasion auxiliary-set samples into primary manifest output
- they do not default-project `rule_labels.json -> threat_taxonomy_v1` into primary manifest core fields
- any future auxiliary-set interface must be opt-in, default-off, and backward compatible

---

## 4. Input Contract

### 4.1 Frozen sample structure

The Data module currently assumes the TRAINSET_V1 directory baseline:

- required: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `screenshot_viewport.png`, `net_summary.json`, `auto_labels.json`
- recommended: `visible_text.txt`, `forms.json`, `html_rendered.json`
- optional: `html_raw.json`, `screenshot_full.png`, `rule_labels.json`, `manual_labels.json`

### 4.2 Label discipline

- directory-level `phish/benign` is only a hint source
- weak label priority comes from `auto_labels.json`
- `rule_labels.json -> threat_taxonomy_v1` is an active weak-label namespace when present, not a gold-label layer
- this module must not promote weak labels into gold labels

### 4.3 Auxiliary-set boundary

The gate / evasion auxiliary-set protocol is documented separately in `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`.

For the current stage:

- the Data module may document or report this boundary
- the Data module must not silently widen TrainSet V1 primary admission
- current default manifest flow remains primary-oriented unless a later task adds an explicit opt-in auxiliary interface

---

## 5. Script Responsibilities

### 5.1 `build_manifest.py`

Owns:

- sample discovery
- required-file validation for manifest admission
- per-sample availability flags
- `usable_for_text` / `usable_for_vision` / `usable_for_multimodal`
- `manifest.jsonl` export
- rejected-sample export and build summary

Must not:

- rewrite sample files
- rename frozen fields
- infer new schema semantics

### 5.2 `check_dataset_consistency.py`

Owns:

- manifest field validation
- sample path existence checks
- required-file presence verification against manifest rows
- `has_*` and `usable_*` flag verification
- JSON and Markdown report export

Must not:

- modify sample directories
- rewrite manifest rows
- auto-heal broken data silently

---

## 6. Current Stage Policy

At the current project stage:

- smoke validation is allowed and recommended
- full-dataset manifest build is deferred until data collection is sufficiently complete
- full consistency check is deferred until data collection is sufficiently complete
- unified offline `rule_labels.json` backfill remains the preferred path for raising `threat_taxonomy_v1` coverage as sample collection grows

This is an intentional scheduling decision, not an omission.

---

## 7. Minimal Commands

Smoke-level manifest build:

```bash
python scripts/data/build_manifest.py --data-root ./data --input-roots ./data/raw/phish ./data/raw/benign --out-dir ./data/processed/trainset_v1_smoke
```

Smoke-level consistency check:

```bash
python scripts/data/check_dataset_consistency.py --data-root ./data --manifest ./data/processed/trainset_v1_smoke/manifest.jsonl --out-dir ./data/processed/trainset_v1_smoke/consistency_check
```

---

## 8. When To Run / Not Run

Run now:

- when validating that scripts still match current frozen structure
- when checking a small sample subset or newly collected spot sample
- when preparing GPT-web review material for current repo state

Do not run now:

- full-dataset manifest build before data collection stabilizes
- full consistency sweep before data collection stabilizes
- full downstream split execution before the GPT-web task for `split_dataset.py` is frozen

---

## 9. Compatibility Rules

Any Data module change must explicitly state:

- whether schema changed
- whether output compatibility was preserved
- whether downstream scripts may be affected

Breaking changes to sample schema, manifest core fields, or output expectations require explicit approval and doc updates.

---

## 10. Definition of Done

A non-trivial Data module task is Done only if:

- requested data behavior is implemented
- frozen sample contracts are respected
- output artifacts are clearly described
- validation is stated honestly
- compatibility impact is stated
- doc impact is stated


