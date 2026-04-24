# L0 contract documentation alignment task

## 中文版

> 面向人工阅读的摘要版。英文版为权威版本；若文件范围、字段名、验证要求、执行顺序或兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务用于把仓库内与 `L0` 相关的项目级、模块级、runtime 级、数据/标签说明文档统一到当前基本定型的 L0 合同。
- 当前 L0 合同重点是：低成本、快速、可解释、以 `gambling / adult / gate` 三类 specialized surface 为主的筛查与路由层。
- 当前 L0 默认热路径不吃完整 HTML，不做默认 brand extraction，不吃 screenshot；这些能力应归入 L1、L2、heavy artifact、gated fallback 或后续显式任务。
- 本任务是文档对齐任务，不允许改代码、不允许改 schema 字段、不允许重写 L1/L2 最终业务逻辑。
- 因涉及 Markdown 文件较多，本任务必须包含 review / conflict check / handoff。

## 任务元信息

- Task ID: `TASK-L0-2026-04-23-CONTRACT-DOCUMENTATION-ALIGNMENT`
- Task Title: `Align project documentation with the finalized L0 contract`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `COMPLETED`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`; `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`; `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`; `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- Created At: `2026-04-23`
- Requested By: `User`

## 1. Background

L0 has now mostly stabilized through the recent narrowing and consolidation work. The active implementation lives in `src/warden/module/l0.py`, with legacy-compatible orchestration still exposed through `scripts/labeling/Warden_auto_label_utils_brandlex.py`.

The current L0 hot path has an intentionally narrow role:

- focus on cheap `gambling / adult / gate` specialized surface screening;
- consume cheap URL, visible text/title, raw visible-text observability, form summary, network summary, and cheap diff/evasion hints where available;
- preserve compatibility fields such as `html_features` and `brand_signals` with default-safe structures;
- avoid default full HTML scanning, default brand extraction, screenshot/OCR, heavy vision, LLM inference, or interaction recovery;
- route non-specialized or evidence-light pages toward L1 instead of expanding L0 into a general judgment layer.

However, older project and module documents still contain broader or outdated descriptions of L0, including references to HTML, brand, DOM/basic visual signals, and more general weak-risk logic as if they were part of the default L0 path. This creates a documentation-contract mismatch.

This task freezes a broad documentation-alignment pass so those documents can be updated consistently, with explicit review, without drifting into code changes or schema rewrites.

## 2. Goal

Align all active project documentation that defines or materially describes L0 so it consistently states the current L0 contract: L0 is a fast, low-cost, auditable specialized screening and routing layer centered on `gambling / adult / gate`; its default hot path consumes only cheap URL/text/title/form/network/diff-observability evidence; it does not default to HTML, brand extraction, screenshot/OCR, heavy model inference, or interaction recovery; and all non-specialized or insufficient-evidence cases should continue to L1 or L2 according to explicit routing semantics.

## 3. Scope In

This task is allowed to touch:

- `README.md`
- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/tasks/2026-04-23_l0_contract_documentation_alignment.md`
- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

This task is allowed to change:

- L0 responsibility descriptions
- L0 input boundary descriptions
- L0 prohibited input / prohibited implementation descriptions
- wording around `HTML`, `brand`, `screenshot`, `OCR`, heavy artifacts, and L1/L2 routing boundaries
- compatibility notes explaining that `html_features` and `brand_signals` may remain present as fields while no longer being populated by the default L0 hot path
- document cross-references to the active L0 implementation and recent handoffs
- review notes or conflict-resolution tables inside the task/handoff

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- modify Python code
- change `src/warden/module/l0.py`
- change `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- rename schema fields, label fields, JSON keys, CLI flags, files, or folders
- remove documented compatibility fields such as `html_features` or `brand_signals`
- change label semantics or weak-label ontology
- redefine L1 or L2 final business logic
- rewrite historical task or handoff conclusions
- add new dependencies, databases, matching engines, or runtime infrastructure
- convert L0 into a final adjudication stage
- claim full-dataset validation when only documentation review was performed

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`

### Code / Scripts

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- no new dataset artifact is required
- recent L0 benchmark summaries may be cited only if already recorded in handoffs

### Prior Handoff

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`
- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

### Missing Inputs

- `none required to create the task`
- Optional user decision before execution: whether to also update lower-priority historical notes that are not active specs. Default answer should be `NO`; historical task/handoff documents should remain unchanged except this task's own handoff.

## 6. Required Outputs

This task should produce:

- updated active Markdown docs that consistently describe the current L0 contract
- a documented review pass listing changed files and conflict checks
- explicit compatibility notes for `html_features`, `brand_signals`, `diff_summary`, `visible_text`, screenshot/OCR, and heavy artifacts
- no code changes
- a repo handoff document at `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

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

- Treat English sections as authoritative when editing bilingual Markdown.
- Preserve current file names, headings, and historical context unless a heading is directly misleading.
- Historical task/handoff docs are review evidence, not active specs to rewrite.
- Keep `L0 / L1 / L2` as the official stage names.
- `L0-fast` may remain a local implementation form only; it must not become a renamed official stage.
- Current default L0 hot path must be documented as no default full `HTML`, no default `brand` extraction, no screenshot/OCR, no heavy model inference.
- Current default L0 inputs must be documented as cheap URL, visible text/title, raw visible-text observability, forms summary, network summary, and cheap diff/evasion hints where present.
- `html_features` and `brand_signals` must be described as compatibility fields that may carry default-safe structures in the default L0 hot path.
- `diff_summary` must be described carefully: cheap existing summary may inform evasion/routing; heavy variant generation is not an L0 responsibility.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `prepare_l0_inputs(...)`
- `derive_l0_outputs(...)`
- `derive_specialized_surface_signals(...)`
- existing runtime stage names `L0`, `L1`, `L2`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `html_features`; `brand_signals`; `specialized_surface_signals`; `matched_keywords`; `l0_routing_hints`; `routing_reason_codes`; `possible_gambling_lure`; `possible_adult_lure`; `possible_gate_or_evasion`; `possible_age_gate_surface`; `possible_challenge_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - existing sample-dir auto-label/backfill flows
  - current runtime/dataflow skeleton smoke commands if referenced by docs

Downstream consumers to watch:

- dataset backfill readers of `auto_labels.json`
- runtime/dataflow skeleton readers of L0 outputs
- documentation users relying on `README.md`, `PROJECT.md`, `MODULE_INFER.md`, and `L0_DESIGN_V1.md`

## 9. Suggested Execution Plan

Recommended order:

1. Build an inventory of active docs that materially define or describe L0.
2. Classify each doc as `must update`, `likely update`, `review only`, or `historical do not edit`.
3. Update the most authoritative active docs first: `PROJECT.md`, `MODULE_INFER.md`, and `L0_DESIGN_V1.md`.
4. Update supporting docs only where they currently contradict the new L0 input/role boundary.
5. Run a text review using `rg` for outdated L0 references.
6. Run a diff review to ensure only scoped Markdown files changed.
7. Produce handoff with changed-file list, compatibility impact, unresolved caveats, and recommended next step.

Task-specific execution notes:

- Do not make every occurrence of `HTML` or `brand` disappear. The correct distinction is default L0 hot path versus L1/L2/heavy/gated paths.
- Do not rewrite broad Warden multimodal positioning. Warden remains multimodal overall; only L0 default hot-path inputs are narrower.
- Do not state that L0 never uses `diff_summary`; state that existing cheap diff/evasion summary may be consumed when present, while generating heavy variants is outside L0.
- Do not overstate L0 as final. L0 remains a screening and routing layer.
- Treat `docs/modules/Warden_TEXT_PIPELINE_V1.md`, `docs/modules/Warden_VISION_PIPELINE_V1.md`, `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`, `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`, `docs/data/TRAINSET_V1.md`, and `docs/data/TRAIN_LABEL_DERIVATION_V1.md` as review-first files: edit them only when a direct L0 contradiction is found.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] active docs consistently state current L0 responsibilities
- [x] active docs consistently state current L0 default inputs
- [x] active docs consistently state L0 prohibited default inputs and implementation forms
- [x] `HTML` and `brand` wording distinguishes field compatibility from default hot-path computation
- [x] `screenshot`, `OCR`, and heavy artifacts are assigned to L1/L2 or lazy heavy paths, not L0 default
- [x] gate/evasion docs preserve L0's detect-and-route role without assigning gate solving to L0
- [x] review pass identifies any remaining contradictory L0 references or explicitly marks them as historical

## 11. Validation Checklist

Minimum validation expected:

- [x] Markdown scope review via `git diff --name-only`
- [x] text search review for outdated L0 phrases
- [x] cross-doc consistency review across `README.md`, `PROJECT.md`, `MODULE_INFER.md`, `L0_DESIGN_V1.md`, runtime/dataflow spec, and gate/evasion protocol
- [x] no Python files changed
- [x] handoff produced

Commands to run if applicable:

```bash
rg -n --glob "*.md" "\bL0\b|L0-fast|html_features|brand_signals|HTML|brand|screenshot|OCR|diff_summary|early_stop_low_risk" README.md PROJECT.md docs
git diff --name-only
git diff -- README.md PROJECT.md docs/modules/MODULE_INFER.md docs/modules/L0_DESIGN_V1.md docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs/modules/Warden_TEXT_PIPELINE_V1.md docs/modules/Warden_VISION_PIPELINE_V1.md docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md docs/data/GATA_EVASION_AUXILIARY_SET_V1.md docs/data/TRAINSET_V1.md docs/data/TRAIN_LABEL_DERIVATION_V1.md docs/data/Warden_AUTO_LABEL_POLICY_V1.md docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md docs/frozen/SCHEMA_REGISTRY.md
```

Expected evidence to capture:

- changed-file list
- summary of L0 contract statements after edit
- list of reviewed but intentionally unchanged historical docs
- remaining risks or doc debt

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- active L0 contract now documented
- files touched
- docs reviewed but not edited
- compatibility impact
- validation performed
- remaining contradictions or caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

## 13. Open Questions / Blocking Issues

- No blocking user input is required to start the documentation alignment using the current L0 implementation and recent handoffs as the source of truth.
- User decision: `README.md` should receive only a short high-level correction for now, because the L0 contract may still be tuned later.
- User decision: historical task and handoff documents must not be edited; they may only be used as evidence.
- Optional decision: whether to run this with subagents. Recommended execution setup is one read-only explorer for doc inventory and one read-only reviewer for post-edit conflict review; Codex should own all file edits directly.
- Subagent inventory note: one read-only explorer was already used during task creation and found the same priority split. For execution, use subagents only for read-only inventory/review or disjoint worker edits with explicit ownership.

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-23-CONTRACT-DOCUMENTATION-ALIGNMENT`
- Task Title: `Align project documentation with the finalized L0 contract`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `COMPLETED`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_INFER.md`; `docs/modules/L0_DESIGN_V1.md`; `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`; `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`; `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- Created At: `2026-04-23`
- Requested By: `User`

Use this task to align active Warden documentation with the current, mostly finalized L0 contract. This is a broad documentation task, not a code task.

## 1. Background

L0 has now mostly stabilized through the recent narrowing and consolidation work. The active implementation lives in `src/warden/module/l0.py`, with legacy-compatible orchestration still exposed through `scripts/labeling/Warden_auto_label_utils_brandlex.py`.

The current L0 hot path has an intentionally narrow role:

- focus on cheap `gambling / adult / gate` specialized surface screening;
- consume cheap URL, visible text/title, raw visible-text observability, form summary, network summary, and cheap diff/evasion hints where available;
- preserve compatibility fields such as `html_features` and `brand_signals` with default-safe structures;
- avoid default full HTML scanning, default brand extraction, screenshot/OCR, heavy vision, LLM inference, or interaction recovery;
- route non-specialized or evidence-light pages toward L1 instead of expanding L0 into a general judgment layer.

However, older project and module documents still contain broader or outdated descriptions of L0, including references to HTML, brand, DOM/basic visual signals, and more general weak-risk logic as if they were part of the default L0 path. This creates a documentation-contract mismatch.

This task freezes a broad documentation-alignment pass so those documents can be updated consistently, with explicit review, without drifting into code changes or schema rewrites.

## 2. Goal

Align all active project documentation that defines or materially describes L0 so it consistently states the current L0 contract: L0 is a fast, low-cost, auditable specialized screening and routing layer centered on `gambling / adult / gate`; its default hot path consumes only cheap URL/text/title/form/network/diff-observability evidence; it does not default to HTML, brand extraction, screenshot/OCR, heavy model inference, or interaction recovery; and all non-specialized or insufficient-evidence cases should continue to L1 or L2 according to explicit routing semantics.

## 3. Scope In

This task is allowed to touch:

- `README.md`
- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/tasks/2026-04-23_l0_contract_documentation_alignment.md`
- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

This task is allowed to change:

- L0 responsibility descriptions
- L0 input boundary descriptions
- L0 prohibited input / prohibited implementation descriptions
- wording around `HTML`, `brand`, `screenshot`, `OCR`, heavy artifacts, and L1/L2 routing boundaries
- compatibility notes explaining that `html_features` and `brand_signals` may remain present as fields while no longer being populated by the default L0 hot path
- document cross-references to the active L0 implementation and recent handoffs
- review notes or conflict-resolution tables inside the task/handoff

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

## 4. Scope Out

This task must NOT do the following:

- modify Python code
- change `src/warden/module/l0.py`
- change `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- rename schema fields, label fields, JSON keys, CLI flags, files, or folders
- remove documented compatibility fields such as `html_features` or `brand_signals`
- change label semantics or weak-label ontology
- redefine L1 or L2 final business logic
- rewrite historical task or handoff conclusions
- add new dependencies, databases, matching engines, or runtime infrastructure
- convert L0 into a final adjudication stage
- claim full-dataset validation when only documentation review was performed

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`

### Code / Scripts

- `src/warden/module/l0.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- no new dataset artifact is required
- recent L0 benchmark summaries may be cited only if already recorded in handoffs

### Prior Handoff

- `docs/handoff/2026-04-21_l0_fast_path_narrowing.md`
- `docs/handoff/2026-04-21_l0_specialized_keyword_scan_consolidation.md`
- `docs/handoff/2026-04-22_runtime_dataflow_freeze_spec_v0_1.md`
- `docs/handoff/2026-04-22_runtime_dataflow_skeleton_v0_1.md`
- `docs/handoff/2026-04-22_runtime_l1_l2_contract_refinement.md`

### Missing Inputs

- `none required to create the task`
- Optional user decision before execution: whether to also update lower-priority historical notes that are not active specs. Default answer should be `NO`; historical task/handoff documents should remain unchanged except this task's own handoff.

## 6. Required Outputs

This task should produce:

- updated active Markdown docs that consistently describe the current L0 contract
- a documented review pass listing changed files and conflict checks
- explicit compatibility notes for `html_features`, `brand_signals`, `diff_summary`, `visible_text`, screenshot/OCR, and heavy artifacts
- no code changes
- a repo handoff document at `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

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

- Treat English sections as authoritative when editing bilingual Markdown.
- Preserve current file names, headings, and historical context unless a heading is directly misleading.
- Historical task/handoff docs are review evidence, not active specs to rewrite.
- Keep `L0 / L1 / L2` as the official stage names.
- `L0-fast` may remain a local implementation form only; it must not become a renamed official stage.
- Current default L0 hot path must be documented as no default full `HTML`, no default `brand` extraction, no screenshot/OCR, no heavy model inference.
- Current default L0 inputs must be documented as cheap URL, visible text/title, raw visible-text observability, forms summary, network summary, and cheap diff/evasion hints where present.
- `html_features` and `brand_signals` must be described as compatibility fields that may carry default-safe structures in the default L0 hot path.
- `diff_summary` must be described carefully: cheap existing summary may inform evasion/routing; heavy variant generation is not an L0 responsibility.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels(...)`
- `derive_auto_labels_from_sample_dir(...)`
- `prepare_l0_inputs(...)`
- `derive_l0_outputs(...)`
- `derive_specialized_surface_signals(...)`
- existing runtime stage names `L0`, `L1`, `L2`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `html_features`; `brand_signals`; `specialized_surface_signals`; `matched_keywords`; `l0_routing_hints`; `routing_reason_codes`; `possible_gambling_lure`; `possible_adult_lure`; `possible_gate_or_evasion`; `possible_age_gate_surface`; `possible_challenge_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py ...`
  - existing sample-dir auto-label/backfill flows
  - current runtime/dataflow skeleton smoke commands if referenced by docs

Downstream consumers to watch:

- dataset backfill readers of `auto_labels.json`
- runtime/dataflow skeleton readers of L0 outputs
- documentation users relying on `README.md`, `PROJECT.md`, `MODULE_INFER.md`, and `L0_DESIGN_V1.md`

## 9. Suggested Execution Plan

Recommended order:

1. Build an inventory of active docs that materially define or describe L0.
2. Classify each doc as `must update`, `likely update`, `review only`, or `historical do not edit`.
3. Update the most authoritative active docs first: `PROJECT.md`, `MODULE_INFER.md`, and `L0_DESIGN_V1.md`.
4. Update supporting docs only where they currently contradict the new L0 input/role boundary.
5. Run a text review using `rg` for outdated L0 references.
6. Run a diff review to ensure only scoped Markdown files changed.
7. Produce handoff with changed-file list, compatibility impact, unresolved caveats, and recommended next step.

Task-specific execution notes:

- Do not make every occurrence of `HTML` or `brand` disappear. The correct distinction is default L0 hot path versus L1/L2/heavy/gated paths.
- Do not rewrite broad Warden multimodal positioning. Warden remains multimodal overall; only L0 default hot-path inputs are narrower.
- Do not state that L0 never uses `diff_summary`; state that existing cheap diff/evasion summary may be consumed when present, while generating heavy variants is outside L0.
- Do not overstate L0 as final. L0 remains a screening and routing layer.
- Treat `docs/modules/Warden_TEXT_PIPELINE_V1.md`, `docs/modules/Warden_VISION_PIPELINE_V1.md`, `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`, `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`, `docs/data/TRAINSET_V1.md`, and `docs/data/TRAIN_LABEL_DERIVATION_V1.md` as review-first files: edit them only when a direct L0 contradiction is found.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] active docs consistently state current L0 responsibilities
- [x] active docs consistently state current L0 default inputs
- [x] active docs consistently state L0 prohibited default inputs and implementation forms
- [x] `HTML` and `brand` wording distinguishes field compatibility from default hot-path computation
- [x] `screenshot`, `OCR`, and heavy artifacts are assigned to L1/L2 or lazy heavy paths, not L0 default
- [x] gate/evasion docs preserve L0's detect-and-route role without assigning gate solving to L0
- [x] review pass identifies any remaining contradictory L0 references or explicitly marks them as historical

## 11. Validation Checklist

Minimum validation expected:

- [x] Markdown scope review via `git diff --name-only`
- [x] text search review for outdated L0 phrases
- [x] cross-doc consistency review across `README.md`, `PROJECT.md`, `MODULE_INFER.md`, `L0_DESIGN_V1.md`, runtime/dataflow spec, and gate/evasion protocol
- [x] no Python files changed
- [x] handoff produced

Commands to run if applicable:

```bash
rg -n --glob "*.md" "\bL0\b|L0-fast|html_features|brand_signals|HTML|brand|screenshot|OCR|diff_summary|early_stop_low_risk" README.md PROJECT.md docs
git diff --name-only
git diff -- README.md PROJECT.md docs/modules/MODULE_INFER.md docs/modules/L0_DESIGN_V1.md docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs/modules/Warden_TEXT_PIPELINE_V1.md docs/modules/Warden_VISION_PIPELINE_V1.md docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md docs/data/GATA_EVASION_AUXILIARY_SET_V1.md docs/data/TRAINSET_V1.md docs/data/TRAIN_LABEL_DERIVATION_V1.md docs/data/Warden_AUTO_LABEL_POLICY_V1.md docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md docs/frozen/SCHEMA_REGISTRY.md
```

Expected evidence to capture:

- changed-file list
- summary of L0 contract statements after edit
- list of reviewed but intentionally unchanged historical docs
- remaining risks or doc debt

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- active L0 contract now documented
- files touched
- docs reviewed but not edited
- compatibility impact
- validation performed
- remaining contradictions or caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

## 13. Open Questions / Blocking Issues

- No blocking user input is required to start the documentation alignment using the current L0 implementation and recent handoffs as the source of truth.
- User decision: `README.md` should receive only a short high-level correction for now, because the L0 contract may still be tuned later.
- User decision: historical task and handoff documents must not be edited; they may only be used as evidence.
- Optional decision: whether to run this with subagents. Recommended execution setup is one read-only explorer for doc inventory and one read-only reviewer for post-edit conflict review; Codex should own all file edits directly.
- Subagent inventory note: one read-only explorer was already used during task creation and found the same priority split. For execution, use subagents only for read-only inventory/review or disjoint worker edits with explicit ownership.
