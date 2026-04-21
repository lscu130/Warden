# 2026-04-10_warden_harness_p0_guardrails

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 Warden Harness P0 Guardrails 任务的正式任务单。
- 若中英文存在冲突，以英文版为准。
- 本任务涉及的 Markdown 交付默认采用中文摘要在前、英文全文在后。

### 摘要

- 任务 ID：WARDEN-HARNESS-P0-GUARDRAILS
- 任务主题：建立第一版 repo-native harness 基础护栏
- 当前状态：DONE
- 相关模块：documentation maintenance / harness baseline

### 当前任务要点

- 目标是在不改变训练、推理、capture 输出和主数据协议行为的前提下，补齐 task/handoff lint、schema compatibility guard 和 smoke baseline skeleton。
- 本任务只允许修改任务范围内的 docs、scripts/ci 和 tests/smoke 路径。
- 不能确认的公共契约必须显式标记为 `uncertain / needs confirmation`，不能猜。

## English Version

# Task Metadata

- Task ID: WARDEN-HARNESS-P0-GUARDRAILS
- Task Title: Warden Harness P0 Guardrails
- Owner Role: Codex execution engineer
- Priority: P0
- Status: DONE
- Related Module: documentation maintenance / harness baseline
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`; `docs/data/TRAINSET_V1.md`
- Created At: 2026-04-10
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.
- If the task will produce Markdown deliverables, define them as bilingual by default: Chinese summary first, full English version second, with English authoritative for exact facts and contract wording.

---

## 1. Background

Warden already has frozen workflow, task, handoff, and dataset-contract documentation, but it does not yet have a repo-native harness baseline that can check whether non-trivial execution artifacts and selected schema surfaces remain structurally compliant.

The current repository state confirms:

- governing workflow and template docs exist and are active contracts;
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md` and `docs/data/TRAINSET_V1.md` provide the strongest current frozen schema truth for sample outputs and manifest fields;
- there is no existing `tests/smoke/` baseline;
- there is no checked-in `manifest.jsonl` under `data/processed/`;
- real sample artifacts exist under `data/raw/...` and can support read-only baseline validation.

This task is needed now to create a minimal auditable starting point for task doc lint, handoff lint, schema compatibility checking, and smoke-baseline documentation without changing the current training, inference, or data mainline behavior.

---

## 2. Goal

Add the first repo-native harness guardrail layer for Warden so that task documents, handoff documents, selected schema surfaces, and a minimal smoke baseline become locally checkable, handoff-friendly, and reproducible, while preserving all current public training, inference, capture-output, and data-protocol behavior.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `docs/frozen/`
- `docs/harness/`
- `scripts/ci/`
- `tests/smoke/`
- `README.md` or a related docs index only if a minimal reference is required

This task is allowed to change:

- a new formal task doc for this delivery
- a new formal handoff for this delivery
- a new bilingual schema / contract registry doc
- a new bilingual harness baseline doc
- three additive read-only checker scripts
- a smoke baseline README and example manifest skeleton

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- modify training logic
- modify inference routing logic
- modify capture output structure
- rename any frozen field, file name, CLI surface, or enumeration
- add third-party dependencies
- perform broad refactors
- change TrainSet V1 semantics
- change Gate / Evasion auxiliary-set semantics
- build a full benchmark platform instead of a minimal smoke-baseline skeleton

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/data/TRAINSET_V1.md`

### Code / Scripts

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/maintenance/check_markdown_bilingual_structure.py`

### Data / Artifacts

- one existing real sample directory under `data/raw/...` for read-only validation
- current repository task and handoff docs for structure reference
- `tests/smoke/golden_manifest.example.json` to be created in this task

### Prior Handoff

- `none required`

### Missing Inputs

- a machine-readable existing schema registry does not exist
- checked-in `manifest.jsonl` baseline data under `data/processed/` is missing
- undocumented public interfaces beyond current frozen docs will be treated as `uncertain / needs confirmation`

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- `docs/tasks/2026-04-10_warden_harness_p0_guardrails.md`
- `docs/handoff/2026-04-10_warden_harness_p0_guardrails.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/harness/WARDEN_HARNESS_BASELINE.md`
- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`
- `scripts/ci/check_schema_compat.py`
- `tests/smoke/README.md`
- `tests/smoke/golden_manifest.example.json`

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- Do not change existing training, inference, capture, or data-mainline behavior.
- Mark any unconfirmed contract surface as `uncertain / needs confirmation` instead of guessing.
- Keep the schema guard baseline executable but limited to minimal compatibility checks.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen sample-output file names and top-level keys
- existing TrainSet V1 manifest field names
- existing data-script CLI surfaces and main output artifact names

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `meta.json`, `url.json`, `auto_labels.json`, TrainSet V1 manifest minimum fields, existing output artifact names from `build_manifest.py`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\data\build_manifest.py --help`
  - `python E:\Warden\scripts\data\check_dataset_consistency.py --help`
  - `python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help`

Downstream consumers to watch:

- operators relying on current Warden dataset and manifest contracts
- future automation or CI jobs that may call the new checker scripts

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Create the formal task doc before implementation.
4. Add the three minimal checker scripts.
5. Add the schema registry, harness baseline doc, and smoke baseline files.
6. Run the smallest meaningful validation.
7. Update the task doc status and validation evidence.
8. Prepare the repo handoff last.

Task-specific execution notes:

- Keep the task and handoff lint scripts structural only.
- Keep the schema guard focused on selected top-level keys and required files.
- Use real sample artifacts only for read-only positive validation, not as committed fixtures.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Handoff is provided for non-trivial changes
- [x] `docs/frozen/SCHEMA_REGISTRY.md` exists and marks unknown contract surfaces explicitly
- [x] `docs/harness/WARDEN_HARNESS_BASELINE.md` exists and documents the P0 harness purpose and commands
- [x] the three additive checker scripts run with no third-party dependencies
- [x] `tests/smoke/README.md` and `tests/smoke/golden_manifest.example.json` exist as a minimal smoke skeleton

---

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity for all new Python scripts
- [x] positive task-doc check on this task doc
- [x] positive handoff-doc check on the new handoff doc
- [x] positive schema-guard check on the example manifest record
- [x] positive schema-guard check on one real sample directory
- [x] optional positive schema-guard checks on one real `meta.json`, `url.json`, and `auto_labels.json`
- [x] smoke-baseline file existence and format spot-check

Commands to run if applicable:

```bash
python -m py_compile E:\Warden\scripts\ci\check_task_doc.py
python -m py_compile E:\Warden\scripts\ci\check_handoff_doc.py
python -m py_compile E:\Warden\scripts\ci\check_schema_compat.py
python E:\Warden\scripts\ci\check_task_doc.py E:\Warden\docs\tasks\2026-04-10_warden_harness_p0_guardrails.md
python E:\Warden\scripts\ci\check_handoff_doc.py E:\Warden\docs\handoff\2026-04-10_warden_harness_p0_guardrails.md
python E:\Warden\scripts\ci\check_schema_compat.py --kind manifest_record --path E:\Warden\tests\smoke\golden_manifest.example.json
python E:\Warden\scripts\ci\check_schema_compat.py --kind sample_dir --path E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\0x7c0.com_20260408T092757Z
python E:\Warden\scripts\ci\check_schema_compat.py --kind meta_json --path E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\0x7c0.com_20260408T092757Z\meta.json
python E:\Warden\scripts\ci\check_schema_compat.py --kind url_json --path E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\0x7c0.com_20260408T092757Z\url.json
python E:\Warden\scripts\ci\check_schema_compat.py --kind auto_labels_json --path E:\Warden\data\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\0x7c0.com_20260408T092757Z\auto_labels.json
```

Expected evidence to capture:

- successful `py_compile` runs for all new scripts
- successful task-doc lint on this task doc
- successful handoff-doc lint on the new handoff doc
- successful schema-guard checks on the example manifest record and one real sample directory
- confirmation that the smoke-baseline files exist and align with `TRAINSET_V1.md`

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-10_warden_harness_p0_guardrails.md`
