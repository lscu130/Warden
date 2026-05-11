# Warden L1 Framework Definition Update Execution Task

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分供人工快速阅读。

### 摘要

本任务是 repo-native execution wrapper，用于承接用户提供的外部任务单：

- `docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md`

本 wrapper 不改变原始任务边界，只把本轮执行压缩成仓库 checker 可识别的任务格式。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260507-L1-FRAMEWORK-DEFINITION-EXECUTION
- Task Title: Execute L1 Framework Definition Documentation Update
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: MODULE_INFER / MODULE_TRAIN / runtime-dataflow / edge deployment / L1 architecture
- Related Issue / ADR / Doc: docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md; docs/frozen/Warden_L1_FRAMEWORK_V0.1.md
- Created At: 2026-05-07
- Requested By: project owner

## 1. Background

The project owner provided a detailed external task document to update Warden L1 framework definitions.
That document was copied into the repository as `docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md`.

The task affects architecture documentation, so it is non-trivial and requires task/handoff coverage.

## 2. Goal

Update repository documentation so Warden L1 is consistently defined as a staged main-judgment shell with a text/structured main evidence path, conditional visual evidence recovery, OCR/YOLO/CLIP responsibility separation, fusion, and deterministic explanation rendering.

## 3. Scope In

Allowed files and directories:

- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/frozen/`
- `docs/reports/`
- `docs/tasks/`
- `docs/handoff/`

Allowed changes:

- documentation-only L1 definition updates;
- new L1 framework definition document;
- repo-local task copy and execution wrapper;
- alignment report;
- handoff document.

## 4. Scope Out

This task must not:

- modify Python code;
- modify model training or inference runtime logic;
- modify dataset files;
- modify label JSON files;
- rename frozen schema fields;
- rename labels or enums;
- add dependencies;
- change CLI behavior;
- change machine-readable output schema;
- remove `MobileCLIP2-S2`, trigger-based `PP-OCRv4 mobile`, or `YOLO26n` from the default edge profile;
- claim runtime, latency, accuracy, or model-performance validation.

## 5. Inputs

Docs:

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`

Code / Scripts:

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

Data / Artifacts:

- none

Prior Handoff:

- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

Missing Inputs:

- none blocking

## 6. Required Outputs

This task should produce:

- updated documentation files inside repository scope;
- a new L1 framework definition document;
- a concise alignment report;
- this repo-native execution task wrapper;
- a handoff matching repository template expectations.

## 7. Hard Constraints

- Preserve existing schema, CLI, labels, output formats, and deployment defaults.
- Keep all L1 output field names as draft / proposed / conceptual unless already frozen elsewhere.
- Preserve official `L0 / L1 / L2` stage naming.
- Preserve trigger-based OCR.
- Preserve CLIP / MobileCLIP as weak page-level visual prior and routing helper.
- Do not treat login, download, payment, wallet, support, or redirect surfaces as automatically malicious.
- Follow `AGENTS.md` and `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff coverage for this non-trivial documentation task.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- frozen sample artifact filenames;
- current stable data CLI surfaces;
- official `L0 / L1 / L2` stage names;
- current default edge components.

Schema / field constraints:

- Schema changed allowed: No
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none changed

CLI / output compatibility constraints:

- Existing commands must keep working.
- No CLI or machine-readable output schema change is allowed.

Downstream consumers to watch:

- future L1 implementation;
- future training target definition;
- future output schema freeze;
- future benchmark/evaluation work.

## 9. Suggested Execution Notes

Recommended order:

1. Read governing docs and task input.
2. Search active L1 / text / vision / CLIP / OCR / YOLO / fusion docs.
3. Create or update documentation only.
4. Run repository search validation and diff checks.
5. Run available task/handoff structural checks where applicable.
6. Produce handoff.

## 10. Acceptance Criteria

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Evidence rules were followed or caveats were stated
- [x] Counter-review was performed
- [x] Validation was run or caveats were stated
- [x] Stop rules were satisfied
- [x] Risks are documented
- [x] Required docs were updated
- [x] Handoff is provided for this non-trivial change

## 11. Validation Checklist

Minimum validation expected:

- [x] repository search for L1 / text / vision / CLIP / OCR / YOLO / fusion terms
- [x] search for risky contradictory wording patterns
- [x] focused diff check for touched docs
- [x] task document checker for this wrapper
- [ ] handoff checker after handoff creation

Commands:

```powershell
Get-ChildItem -Path 'E:\Warden\docs' -File -Recurse | Select-String -Pattern 'L1|text tower|vision tower|CLIP|MobileCLIP|OCR|YOLO|fusion|XGBoost|evidence ledger|reason code|explanation renderer'
Get-ChildItem -Path 'E:\Warden\docs' -File -Recurse | Select-String -Pattern 'CLIP.*malicious|CLIP.*benign|vision.*final|vision.*judge|OCR.*always|brand.*domain.*malicious|login.*malicious'
git diff --stat -- PROJECT.md docs/modules/MODULE_INFER.md docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md docs/modules/Warden_TEXT_PIPELINE_V1.md docs/modules/Warden_VISION_PIPELINE_V1.md docs/frozen/Warden_L1_FRAMEWORK_V0.1.md docs/reports/20260507_l1_framework_alignment_report.md docs/tasks/2026-05-07_warden_l1_framework_definition_update_v0_1.md
python scripts/ci/check_task_doc.py docs/tasks/2026-05-07_warden_l1_framework_definition_update_execution.md
```
