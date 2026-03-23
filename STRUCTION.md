# STRUCTION

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Suggested Repository Structure

This file gives a suggested repository structure for Warden and explains the intended responsibility of the major directories.

## Repository-Structure Guidance

The main design ideas are:

- keep governance and long-lived contracts under `docs/`;
- keep configs, scripts, source code, experiments, outputs, tests, and datasets separated;
- preserve explicit module boundaries for data, labeling, training, inference, and paper support;
- keep raw capture outputs, reviewed data, and derived subsets under `data/` instead of mixing them into code folders.

## Top-Level Layout

At the top level, the repository should expose the project identity and the core contracts, for example:

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- package metadata such as `requirements.txt` or `pyproject.toml`

This layer should stay small and stable. It should not become a dumping ground for unrelated scripts.

## `docs/`

`docs/` is the governance and specification area.

It should hold:

- frozen specifications under `docs/frozen/`;
- module-boundary documents under `docs/modules/`;
- workflow contracts under `docs/workflow/`;
- task and handoff templates under `docs/templates/`;
- ADRs under `docs/adr/`;
- task records under `docs/tasks/`;
- handoff records under `docs/handoff/`.

In short, `docs/` is where project contracts live.

## `configs/`

`configs/` should keep configuration files organized by responsibility, for example:

- `configs/data/` for capture, backfill, and split settings;
- `configs/train/` for model and experiment settings;
- `configs/infer/` for runtime and export settings.

The goal is to keep behavior reproducible and prevent configuration sprawl.

## `src/` And `scripts/`

`src/` should own reusable implementation modules. `scripts/` should own operational entry points, execution helpers, and task-oriented utilities.

This split matters because:

- reusable logic belongs in modules;
- execution wrappers belong in scripts;
- later refactoring is easier when library code is not hidden in ad hoc entry files.

## `data/`

`data/` should hold captured samples, derived datasets, reviewed subsets, and dataset-management artifacts.

A healthy layout keeps apart:

- raw or near-raw captured outputs;
- processed manifests and splits;
- reviewed or curated subsets;
- smoke-test subsets and consistency reports.

This is how reproducibility remains auditable.

## `experiments/`, `outputs/`, And `tests/`

`experiments/` should keep experiment definitions, archived runs, and result metadata.

`outputs/` should hold generated reports, exports, and other produced artifacts that should not be confused with source data.

`tests/` should stay focused on sanity checks, unit tests, smoke tests, and regression protection.

## Practical Intent

This structure is a recommendation, not a guarantee that every listed folder already exists exactly as shown.

Its value is practical:

- contracts become easy to find;
- ownership stays clearer;
- data and code are not mixed carelessly;
- future growth is less likely to collapse into path and naming chaos.

### Original Chinese Source

The original Chinese source text is kept below for human readers and traceability.

Warden/
├─ AGENTS.md
├─ PROJECT.md
├─ README.md
├─ requirements.txt
├─ pyproject.toml                     # 可选；有就保留一个主入口
├─ .gitignore
│
├─ docs/
│  ├─ frozen/
│  │  └─ Warden_Dataset_Output_Frozen_Spec_v1.1.md
│  │
│  ├─ modules/
│  │  ├─ MODULE_DATA.md
│  │  ├─ MODULE_LABELING.md
│  │  ├─ MODULE_TRAIN.md
│  │  ├─ MODULE_INFER.md
│  │  └─ MODULE_PAPER.md
│  │
│  ├─ workflow/
│  │  └─ GEMINI_CODEX_WORKFLOW.md
│  │
│  ├─ templates/
│  │  ├─ TASK_TEMPLATE.md
│  │  └─ HANDOFF_TEMPLATE.md
│  │
│  ├─ adr/
│  │  ├─ ADR-0001-project-scope.md
│  │  ├─ ADR-0002-data-freeze-policy.md
│  │  ├─ ADR-0003-labeling-policy.md
│  │  └─ ADR-0004-model-stack.md
│  │
│  ├─ tasks/
│  │  ├─ active/
│  │  ├─ done/
│  │  └─ blocked/
│  │
│  └─ handoff/
│     ├─ 2026-03/
│     └─ archive/
│
├─ configs/
│  ├─ data/
│  │  ├─ capture/
│  │  ├─ backfill/
│  │  └─ splits/
│  │
│  ├─ train/
│  │  ├─ text/
│  │  ├─ vision/
│  │  ├─ multimodal/
│  │  └─ distill/
│  │
│  └─ infer/
│     ├─ l0/
│     ├─ l1/
│     ├─ l2/
│     └─ export/
│
├─ scripts/
│  ├─ capture/
│  │  ├─ capture_url_v6_optimized_v6_2_plus_labels_brandlex.py
│  │  ├─ capture_smoke_test.py
│  │  └─ capture_validate_outputs.py
│  │
│  ├─ labeling/
│  │  ├─ evt_dataset_backfill_labels_brandlex.py
│  │  ├─ evt_auto_label_utils_brandlex.py
│  │  ├─ build_rule_labels.py
│  │  └─ labeling_smoke_test.py
│  │
│  ├─ data/
│  │  ├─ build_manifest.py
│  │  ├─ check_dataset_consistency.py
│  │  ├─ split_dataset.py
│  │  └─ export_stats.py
│  │
│  ├─ train/
│  │  ├─ train_text.py
│  │  ├─ train_vision.py
│  │  ├─ train_multimodal.py
│  │  ├─ train_distill.py
│  │  └─ eval_model.py
│  │
│  ├─ infer/
│  │  ├─ run_l0.py
│  │  ├─ run_l1.py
│  │  ├─ run_l2.py
│  │  ├─ run_pipeline.py
│  │  ├─ benchmark_infer.py
│  │  └─ export_model.py
│  │
│  └─ paper/
│     ├─ collect_results.py
│     ├─ build_tables.py
│     ├─ build_figures.py
│     └─ export_casebook.py
│
├─ src/
│  └─ warden/
│     ├─ __init__.py
│     ├─ common/
│     │  ├─ io.py
│     │  ├─ paths.py
│     │  ├─ logging.py
│     │  ├─ schema_checks.py
│     │  └─ constants.py
│     │
│     ├─ data/
│     │  ├─ dataset_reader.py
│     │  ├─ manifest.py
│     │  ├─ sample_parser.py
│     │  └─ validators.py
│     │
│     ├─ labeling/
│     │  ├─ brand_lexicon.py
│     │  ├─ weak_rules.py
│     │  ├─ rule_labels.py
│     │  └─ manual_label_io.py
│     │
│     ├─ train/
│     │  ├─ loaders/
│     │  ├─ losses/
│     │  ├─ models/
│     │  │  ├─ text/
│     │  │  ├─ vision/
│     │  │  ├─ fusion/
│     │  │  └─ distill/
│     │  ├─ engine.py
│     │  ├─ eval.py
│     │  └─ metrics.py
│     │
│     ├─ infer/
│     │  ├─ l0/
│     │  ├─ l1/
│     │  ├─ l2/
│     │  ├─ routing.py
│     │  ├─ thresholds.py
│     │  ├─ outputs.py
│     │  └─ benchmark.py
│     │
│     └─ paper/
│        ├─ tables.py
│        ├─ figures.py
│        └─ error_analysis.py
│
├─ assets/
│  ├─ brand_lexicon/
│  │  ├─ evt_brand_lexicon_v1.json
│  │  └─ README.md
│  │
│  ├─ prompts/
│  └─ examples/
│
├─ experiments/
│  ├─ registry/
│  ├─ runs/
│  ├─ ablations/
│  └─ exports/
│
├─ outputs/
│  ├─ smoke/
│  ├─ eval/
│  ├─ benchmark/
│  └─ paper/
│
├─ tests/
│  ├─ data/
│  ├─ labeling/
│  ├─ train/
│  ├─ infer/
│  └─ fixtures/
│
└─ data/
   ├─ raw/
   │  ├─ phish/
   │  ├─ benign/
   │  └─ quarantine/
   │
   ├─ reviewed/
   │  ├─ train/
   │  ├─ val/
   │  └─ test/
   │
   ├─ manifests/
   ├─ stats/
   └─ README.md
