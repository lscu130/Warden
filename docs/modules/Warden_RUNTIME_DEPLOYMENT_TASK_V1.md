# Warden Runtime Deployment Task V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是交给 Codex 的**执行任务单**，用于在当前 Warden 阶段先落地一套可运行、可下载模型、可做 smoke inference 的运行时基线。
- 本任务**不是**训练任务、也不是完整生产发布任务。
- 若仓库中对应目录不存在，允许在 `scope_in` 范围内按本文创建。
- 若关键输入缺失，Codex 必须先明确指出，再按最安全兼容解释继续，而不是静默发散。

## 1. 背景

Warden 当前已经冻结了项目级协作规则、Vision Pipeline V1、Text Pipeline V1、Edge Deployment Profile V1，以及 PROJECT.md 主规格。
当前默认运行画像已经足够支持一版**离线可缓存模型、边缘可运行、以 smoke inference 为目标**的运行时部署基线：

- text default: `multilingual-e5-small`
- vision similarity default: `MobileCLIP2-S2`
- OCR default: `PP-OCRv4 mobile`, trigger-based
- detector default: `YOLO26n`
- offline teacher tools are not part of the default online runtime path

当前用户仍在处理数据，因此本任务目标不是追求最终精度或 benchmark 封版，而是优先落地：

1. 模型获取与本地缓存路径
2. 运行时环境定义
3. 最小可运行推理入口
4. 组件级 smoke validation

## 2. 目标

在不改动冻结数据契约、不引入训练逻辑、不要求 fine-tuning 的前提下，为 Warden 落地一套 **V1 runtime deployment baseline**。该基线必须支持：使用当前默认模块选型完成 text / vision / OCR / detector 的最小可运行集成；支持本地预下载模型权重并从本地加载；支持在普通 PC / modest x86 edge profile 上先运行 smoke inference；并为后续 benchmark 与更强融合实现保留清晰扩展边界。

## 3. Scope In

This task is allowed to touch:

- `AGENTS.md`
- `PROJECT.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/tasks/`
- `docs/handoff/`
- `scripts/infer/` (create if missing)
- `configs/runtime/` (create if missing)
- `environment/` (create if missing)
- repo-level runtime helper files directly related to this task only

This task is allowed to change:

- add a minimal runtime inference entrypoint
- add model-download / model-cache helper scripts
- add runtime config templates
- add Miniconda environment definition(s)
- add deployment-facing documentation strictly required by this task
- add smoke validation commands and notes

## 4. Scope Out

This task must NOT do the following:

- do not redesign TrainSet V1 or frozen sample schema
- do not modify capture output fields or file names
- do not add training, fine-tuning, pseudo-labeling, or eval-pipeline logic
- do not convert teacher models into runtime hard dependencies
- do not redesign detector ontology or text concept ontology
- do not add a monolithic generative VLM runtime path
- do not silently add server-only assumptions
- do not claim benchmark numbers not actually measured
- do not touch unrelated modules for cleanup

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`

### Code / Scripts

- existing repo runtime / inference related files if any
- existing repo config helpers if any
- any currently existing smoke-test or demo entrypoints if any

### Data / Artifacts

- current frozen successful-sample contract with at least:
  - `screenshot_viewport.png`
  - `visible_text.txt`
  - `forms.json`
  - `url.json`
  - `net_summary.json`
- optional:
  - `screenshot_full.png`

### Prior Handoff

- latest relevant deployment/runtime handoff if one exists

### Missing Inputs

- if no current inference directory exists, state that explicitly and create the smallest needed structure
- if no representative smoke sample path is available, state that explicitly and provide a dummy/sample-compatible CLI contract anyway

## 6. Required Outputs

This task should produce:

- a minimal runtime entry script for Warden V1 smoke inference
- a model-preload / model-cache helper script or command wrapper
- a runtime config template documenting model paths and toggles
- a Miniconda environment definition for runtime deployment
- a short deployment readme or runtime usage doc
- a smoke validation summary
- a non-trivial handoff document

Concrete target outputs are expected to include something functionally equivalent to:

- `scripts/infer/run_smoke_infer.py`
- `scripts/infer/preload_models.py`
- `configs/runtime/runtime_default.yaml`
- `environment/warden_runtime_miniconda.yml`
- `docs/handoff/<date>_runtime_deployment_v1.md`

Names may differ slightly only if repository-local conventions require it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format of existing scripts.
- No new third-party dependency beyond what is strictly required for this approved runtime task.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.

Task-specific constraints:

- Runtime must remain **off-the-shelf first**; no mandatory fine-tuning.
- Default runtime must remain **CPU-conscious** and consistent with edge deployment profile.
- OCR must remain **trigger-based by default**, not always-on.
- `screenshot_viewport.png` remains primary visual input.
- `screenshot_full.png` remains optional.
- `visible_text.txt` remains primary text input.
- Teacher models remain offline-only and must not be required by default runtime.
- If GPU acceleration is optional, CPU path must still be runnable.
- Model downloads must support **local cache / local path reuse** after initial retrieval.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current frozen successful-sample file contract
- existing data and capture file naming used by TrainSet V1
- current stage discipline of L0 / L1 / L2

Schema / field constraints:

- Schema changed allowed: `NO` for frozen sample output
- If yes, required compatibility plan: `N/A`
- Frozen field names involved: sample output filenames and documented frozen contract fields

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing capture commands
  - existing data-manifest commands
  - existing consistency-check commands
- New runtime commands may be added, but they must not break existing commands.

Downstream consumers to watch:

- future fusion-layer implementation
- future benchmark scripts
- future deployment packaging

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing files and module specs.
2. Inspect whether repo already has runtime/infer/config directories.
3. Freeze the smallest runtime directory layout.
4. Add environment definition.
5. Add model preload / local cache logic.
6. Add smoke inference script using off-the-shelf defaults.
7. Add runtime config template.
8. Run smallest meaningful validation.
9. Prepare handoff.

Task-specific execution notes:

- Prefer local model path parameters over implicit online-only fetch.
- If a model API is unstable, wrap it behind a minimal adapter instead of spreading model-specific logic everywhere.
- Keep OCR, text encoder, image-text encoder, and detector as decoupled components.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for this non-trivial change

Task-specific acceptance checks:

- [ ] There is a runnable runtime entrypoint for smoke inference
- [ ] There is a documented local model cache / preload path
- [ ] Default runtime stack matches current module specs:
  - text: `multilingual-e5-small`
  - vision similarity: `MobileCLIP2-S2`
  - OCR: `PP-OCRv4 mobile`, trigger-based
  - detector: `YOLO26n`
- [ ] Missing optional full-page screenshot is handled explicitly
- [ ] OCR can be skipped when trigger conditions are not met
- [ ] Runtime can run without teacher models
- [ ] Environment definition is present and human-readable

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test on at least one representative sample path or mocked-equivalent path
- [ ] backward compatibility spot-check for unrelated existing commands
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m compileall scripts/infer
python scripts/infer/preload_models.py --help
python scripts/infer/run_smoke_infer.py --help
python scripts/infer/run_smoke_infer.py --sample-dir <SMOKE_SAMPLE_DIR> --config configs/runtime/runtime_default.yaml
```

Expected evidence to capture:

- command output snippets
- model cache path behavior
- generated evidence bundle or runtime summary

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- runtime behavior impact
- dependency impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_runtime_deployment_v1.md`

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- whether runtime should emit only component evidence or also a temporary fused placeholder score
- whether repo already contains a preferred inference entry directory
- whether Windows-specific Paddle GPU path should be attempted now or deferred in favor of CPU OCR first

---

## English Version

> AI note: Codex and other models must treat the English section below as the authoritative version. The Chinese section above is for human readers and quick orientation.

# Warden Runtime Deployment Task V1

## 1. Background

Warden already has active governing contracts, pipeline specifications, and a project-level specification.
The current repository state is sufficient to support a first runtime deployment baseline focused on **local model caching, smoke inference, and bounded-cost component integration** rather than final production benchmarking.

The current default runtime profile is:

- text default: `multilingual-e5-small`
- vision similarity default: `MobileCLIP2-S2`
- OCR default: `PP-OCRv4 mobile`, trigger-based
- detector default: `YOLO26n`
- offline teacher tools are not part of the default online runtime path

The user is still processing data.
Therefore this task is not a final training or release task.
It is a runtime deployment task intended to make the default stack runnable early.

## 2. Goal

Implement a bounded, off-the-shelf-first Warden V1 runtime deployment baseline that supports local model preloading and local reuse, smoke inference on current sample-contract inputs, and minimal runtime packaging without changing frozen dataset contracts or requiring task-specific fine-tuning.

## 3. Scope In

This task is allowed to touch:

- `AGENTS.md`
- `PROJECT.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/tasks/`
- `docs/handoff/`
- `scripts/infer/` (create if missing)
- `configs/runtime/` (create if missing)
- `environment/` (create if missing)
- repo-level runtime helper files directly related to this task only

This task is allowed to change:

- add a minimal runtime inference entrypoint
- add model-preload / model-cache helper scripts
- add runtime config templates
- add Miniconda environment definition(s)
- add deployment-facing documentation strictly required by this task
- add smoke validation commands and notes

## 4. Scope Out

This task must NOT:

- redesign TrainSet V1 or the frozen sample schema
- modify capture output fields or frozen filenames
- add training, fine-tuning, pseudo-labeling, or evaluation-pipeline logic
- convert teacher models into runtime hard dependencies
- redesign detector ontology or text concept ontology
- add a monolithic generative VLM runtime path
- silently add server-only assumptions
- claim benchmark numbers that were not actually measured
- touch unrelated modules for cleanup

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`

### Code / Scripts

- existing repo runtime / inference related files if any
- existing repo config helpers if any
- any currently existing smoke-test or demo entrypoints if any

### Data / Artifacts

- current frozen successful-sample contract with at least:
  - `screenshot_viewport.png`
  - `visible_text.txt`
  - `forms.json`
  - `url.json`
  - `net_summary.json`
- optional:
  - `screenshot_full.png`

### Prior Handoff

- latest relevant deployment/runtime handoff if one exists

### Missing Inputs

- if no current inference directory exists, state that explicitly and create the smallest needed structure
- if no representative smoke sample path is available, state that explicitly and still provide a sample-compatible CLI contract

## 6. Required Outputs

This task should produce:

- a minimal runtime entry script for Warden V1 smoke inference
- a model-preload / model-cache helper script or command wrapper
- a runtime config template documenting model paths and toggles
- a Miniconda environment definition for runtime deployment
- a short deployment readme or runtime usage doc
- a smoke validation summary
- a non-trivial handoff document

Concrete target outputs are expected to include something functionally equivalent to:

- `scripts/infer/run_smoke_infer.py`
- `scripts/infer/preload_models.py`
- `configs/runtime/runtime_default.yaml`
- `environment/warden_runtime_miniconda.yml`
- `docs/handoff/<date>_runtime_deployment_v1.md`

Names may differ slightly only if repository-local conventions require it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format of existing scripts.
- No third-party dependency beyond what is strictly required for this approved runtime task.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.

Task-specific constraints:

- Runtime must remain **off-the-shelf first**; no mandatory fine-tuning.
- Default runtime must remain **CPU-conscious** and consistent with the edge deployment profile.
- OCR must remain **trigger-based by default**, not always-on.
- `screenshot_viewport.png` remains the primary visual input.
- `screenshot_full.png` remains optional.
- `visible_text.txt` remains the primary text input.
- Teacher models remain offline-only and must not be required by the default runtime.
- If GPU acceleration is optional, the CPU path must still be runnable.
- Model downloads must support **local cache / local path reuse** after initial retrieval.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current frozen successful-sample file contract
- existing data and capture file naming used by TrainSet V1
- current stage discipline of L0 / L1 / L2

Schema / field constraints:

- Schema changed allowed: `NO` for frozen sample output
- Compatibility plan: `N/A`
- Frozen field names involved: sample output filenames and documented frozen contract fields

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing capture commands
  - existing data-manifest commands
  - existing consistency-check commands
- New runtime commands may be added, but they must not break existing commands.

Downstream consumers to watch:

- future fusion-layer implementation
- future benchmark scripts
- future deployment packaging

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing files and module specs.
2. Inspect whether the repo already has runtime/infer/config directories.
3. Freeze the smallest runtime directory layout.
4. Add the environment definition.
5. Add model preload / local cache logic.
6. Add the smoke inference script using off-the-shelf defaults.
7. Add the runtime config template.
8. Run the smallest meaningful validation.
9. Prepare handoff.

Task-specific execution notes:

- Prefer local model path parameters over implicit online-only fetch.
- If a model API is unstable, wrap it behind a minimal adapter instead of spreading model-specific logic.
- Keep OCR, text encoder, image-text encoder, and detector as decoupled components.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for this non-trivial change

Task-specific acceptance checks:

- [ ] There is a runnable runtime entrypoint for smoke inference
- [ ] There is a documented local model cache / preload path
- [ ] The default runtime stack matches current module specs:
  - text: `multilingual-e5-small`
  - vision similarity: `MobileCLIP2-S2`
  - OCR: `PP-OCRv4 mobile`, trigger-based
  - detector: `YOLO26n`
- [ ] Missing optional full-page screenshot is handled explicitly
- [ ] OCR can be skipped when trigger conditions are not met
- [ ] Runtime can run without teacher models
- [ ] Environment definition is present and human-readable

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test on at least one representative sample path or mocked-equivalent path
- [ ] backward compatibility spot-check for unrelated existing commands
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m compileall scripts/infer
python scripts/infer/preload_models.py --help
python scripts/infer/run_smoke_infer.py --help
python scripts/infer/run_smoke_infer.py --sample-dir <SMOKE_SAMPLE_DIR> --config configs/runtime/runtime_default.yaml
```

Expected evidence to capture:

- command output snippets
- model cache path behavior
- generated evidence bundle or runtime summary

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- runtime behavior impact
- dependency impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_runtime_deployment_v1.md`

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- whether runtime should emit only component evidence or also a temporary fused placeholder score
- whether the repo already contains a preferred inference entry directory
- whether Windows-specific Paddle GPU path should be attempted now or deferred in favor of CPU OCR first
