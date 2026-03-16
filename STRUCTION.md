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