# Task Metadata

- Task ID: WARDEN-TASK-20260518-V1-MODEL-DATAFLOW-REFOCUS
- Task Title: Refocus Warden V1 model structure and data flow around Evidence Pack Builder -> L1
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Warden architecture / data pipeline / L1 inference design
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_MODEL_DATAFLOW_REFOCUS.md
- Created At: 2026-05-18
- Requested By: Cao yong
- Karpathy Guardrails Required: YES

## 中文版

本任务按用户提供的外部任务单执行，目标是把 Warden V1 模型结构与数据流聚焦到：

```text
Current offline experiment:
Processed Valid Dataset
  -> Evidence Pack Builder
  -> L1 Main Judgment / L1 Training / L1 Evaluation
  -> Metrics / Evidence Ledger / Ablation

Future wild-test / online inference:
Raw URL
  -> Capture Pipeline
  -> Capture QA / V1 Scope Admission
  -> Evidence Pack Builder
  -> L1 Main Judgment
  -> Wild-Test Report
```

本任务只做文档与 specification refocus，不修改 L1 代码、训练逻辑、runtime 行为、schema、label enum、CLI、manifest 字段或 JSON 输出。

## English Version

AI note: English is authoritative for exact scope, constraints, validation, and compatibility.

## 1. Background

The user provided an external execution task at `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_MODEL_DATAFLOW_REFOCUS.md`.

Warden V1 has just been narrowed around observable web-based social-engineering threat detection. The next documentation gap is model/dataflow scope: some active docs still describe legacy L0, default L2, default CLIP, adult/gambling/gate/evasion, or always-on multimodal paths in ways that can be confused with the current V1 main experiment.

## 2. Goal

Refocus Warden V1 architecture/dataflow/model-structure documentation so the current default experiment path is:

```text
Processed Valid Dataset -> Evidence Pack Builder -> L1
```

and the future online / wild-test path is preserved as:

```text
Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1
```

L1 must be documented as text / HTML / URL / forms first, with OCR / YOLO as conditional evidence recovery only when evidence is insufficient.

## 3. Scope In

This task is allowed to touch:

- top-level docs that describe Warden architecture, V1 scope, model structure, dataflow, runtime, and inference
- Markdown docs under `docs/` related to architecture, runtime, L1, text pipeline, model design, training/evaluation, or paper framing
- one minimal design note under `docs/architecture/`
- repo task and handoff documents

This task is allowed to change:

- architecture and dataflow diagrams in Markdown
- V1 vs V2+ scope boundaries
- OCR / YOLO / CLIP role descriptions
- offline experiment and future online/wild-test path descriptions
- statements that Warden V1 has no default L0 model entrypoint and no default L2 judgment path

## 4. Scope Out

This task must not:

- modify L1 model code
- add or change model training logic
- implement OCR / YOLO calls
- implement wild testing
- implement online capture
- delete code files
- modify label enums, schema fields, manifest fields, CLI flags, or JSON output formats
- reintroduce adult / gambling / gate / evasion into Warden V1
- define CLIP as a default visual tower
- define L2 as a default V1 path
- perform drive-by cleanup, repository-wide formatting, unrelated renames, or dependency changes

## 5. Inputs

Relevant inputs for this task:

### Docs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_MODEL_DATAFLOW_REFOCUS.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`
- `README.md`
- relevant active docs under `docs/modules/`, `docs/frozen/`, and `docs/l1/`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- `docs/handoff/2026-05-18_v1_threat_formula_focus.md`

### Missing Inputs

- none

## 6. Required Outputs

This task should produce:

- updated architecture/dataflow/model-structure documentation
- a minimal V1 model/dataflow refocus design note
- a repo-local task document
- a repo-local handoff document
- validation evidence covering residual old-reference search, changed-file scope, and checker status

## 7. Hard Constraints

Must obey all of the following:

- Do not modify code, runtime behavior, training behavior, schemas, label enums, CLI flags, manifest fields, or JSON outputs.
- Do not keep CLIP as a V1 default path.
- Do not keep L2 as a V1 default path.
- Do not treat adult/gambling/gate/evasion/redirect-only as V1 main tasks.
- Preserve future online/wild-test architecture as documentation only.
- Preserve compatibility names by classifying them when deletion would imply implementation/schema change.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing CLI commands
- existing schema versions and fields
- existing output file names and JSON/YAML structures
- existing label/enumeration values
- existing runtime and training code behavior

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none may be renamed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - not changed by this documentation-only task

Downstream consumers to watch:

- runtime pipeline docs and code that still contain L0/L2 names
- L1 evidence-pack and Decision Head draft docs
- future online/wild-test planning docs

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- where old L0/L2/CLIP/adult/gambling/gate/evasion references remain
- whether current code still contains L0/L2 compatibility paths
- whether JSON/YAML/schema/runtime files changed
- whether task and handoff docs satisfy repo checker structure

Allowed evidence sources:

- user-provided external task document
- repository governing docs and active docs
- targeted `rg`, `git diff`, `git status`, and checker command outputs

Retrieval budget:

- Initial retrieval: governing docs plus active docs and code paths likely to contain model/dataflow references.
- Additional retrieval is allowed only when targeted search shows unresolved conflicting wording.
- Stop retrieval when active-doc residual hits are either patched or classified as legacy, V2+, future online/wild-test, historical, or out-of-scope.

Missing-evidence behavior:

- Report unknown or unverified status explicitly; do not infer implementation behavior from documentation edits.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Current offline experiment path is documented as `Processed Valid Dataset -> Evidence Pack Builder -> L1`.
- [ ] Future online/wild-test path is preserved as `Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1`.
- [ ] OCR / YOLO are documented as conditional L1 evidence recovery, not always-on dataflow stages.
- [ ] CLIP is documented as outside the Warden V1 default path.
- [ ] Warden V1 is documented as having no default L2.
- [ ] Adult / gambling / gate / evasion / redirect-only handling is documented as outside V1 main tasks.
- [ ] No code/schema/label/CLI/JSON/training/runtime behavior changes are made.
- [ ] Residual old-reference search is performed and classified.
- [ ] Handoff is created.
- [ ] Task and handoff checker scripts are run or failures are reported honestly.

## 11. Validation Checklist

Minimum validation expected:

- [ ] targeted `rg` for `L0|L2|CLIP|adult|gambling|gate|evasion`
- [ ] targeted `rg` for `Processed Valid Dataset|Evidence Pack Builder|Capture QA|V1 Scope Admission|Wild-Test|OCR|YOLO`
- [ ] code search for L0/L2/CLIP compatibility risks, read-only
- [ ] `git diff --stat` scoped to task-touched docs
- [ ] changed-file check confirming no JSON/YAML/Python files in task scope changed
- [ ] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-18_v1_model_dataflow_refocus.md`
- [ ] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-18_v1_model_dataflow_refocus.md`

## 12. Stop Rules

Stop when:

- V1 model/dataflow docs are updated or residuals classified.
- Future online/wild-test path remains documented.
- OCR / YOLO conditional trigger semantics are documented.
- Validation commands are run and recorded.
- Handoff is completed.

Stop and escalate if:

- implementation, schema, label, CLI, manifest, training, or L1 interface changes become necessary.
