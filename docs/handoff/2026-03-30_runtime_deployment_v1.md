# 交接摘要 / Handoff Summary

## 中文摘要

- Handoff ID: HANDOFF-2026-03-30-RUNTIME-DEPLOYMENT-V1
- Related Task ID: Warden_RUNTIME_DEPLOYMENT_TASK_V1
- Task Title: Warden Runtime Deployment Task V1
- Module: inference / runtime / environment
- Author: Codex
- Date: 2026-03-30
- Status: DONE

### Executive Summary

已将外部任务文档复制进仓库，并在 `F:\Warden` 完成 Git 初始化与远端 `origin` 关联。基于 `Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`，已落地一套可运行的 Warden V1 runtime baseline：包含 Miniconda 环境定义、runtime 配置、模型预加载脚本、smoke inference 入口与使用说明。`warden_runtime` 环境已确认存在且关键依赖可导入，`multilingual-e5-small` 已成功缓存并完成 live text embedding；`MobileCLIP2-S2` 已通过官方 `ml-mobileclip` adapter 在 smoke run 中成功输出相似度，`YOLO26n` 仍需手动放置权重。

### What Changed

- 复制了外部工件到仓库：
  - `docs/tasks/Warden_MINICONDA_ENV_SETUP_V1.md`
  - `docs/tasks/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
  - `environment/warden_runtime_env_example.yml`
- 新增 runtime baseline 文件：
  - `environment/warden_runtime_miniconda.yml`
  - `configs/runtime/runtime_default.yaml`
  - `scripts/infer/preload_models.py`
  - `scripts/infer/run_smoke_infer.py`
  - `docs/tasks/2026-03-30_runtime_deployment_usage.md`
- 更新 `scripts/infer/README.md`
- 初始化 Git 仓库并关联 `origin`
- 安装官方 `ml-mobileclip` 到 `warden_runtime`
- 在 `model_cache/` 下预下载：
  - `intfloat/multilingual-e5-small`
  - `apple/MobileCLIP2-S2`

### Runtime Behavior Impact

- 现在仓库内已有可执行的 smoke inference CLI
- smoke inference 默认输出组件级证据，不输出伪造的最终融合风险分数
- OCR 保持 trigger-based，当前验证样本上正确跳过
- text encoder 已可在本地缓存模型上实际运行
- vision similarity 已可通过 `ml-mobileclip` adapter 在本地 checkpoint 上实际运行
- detector 目前保留为本地权重路径约定，不伪造自动下载

### Dependency Impact

- `warden_runtime` 环境已存在，Python 版本为 3.10.20
- 关键包均已可导入：`torch`、`transformers`、`huggingface_hub`、`sentence_transformers`、`ultralytics`、`yaml`、`paddle`、`paddleocr`
- `ml-mobileclip` 已安装到 `warden_runtime`
- 当前未新增仓库级 Python packaging 元数据，仅新增环境文件

### Schema / Interface Impact

- Schema changed: no
- Backward compatible: yes
- Public interface changed: no
- Existing CLI still valid: yes

### Validation Performed

- `git fetch origin` 成功
- `git remote -v` 正确显示远端
- `python scripts/infer/preload_models.py --help`
- `python scripts/infer/run_smoke_infer.py --help`
- 运行 smoke inference：
  - 默认模式
  - `--run-live-models` 模式
- `multilingual-e5-small` live embedding 成功，输出 384 维 embedding
- `MobileCLIP2-S2` live similarity 成功，输出 prompt-bank 相似度分布
- `ast.parse` 对两份 infer 脚本通过
- 输出工件已落地：
  - `outputs/smoke/runtime/model_preload_manifest.json`
  - `outputs/smoke/runtime/<sample>/runtime_summary.json`

### Risks / Caveats

- 当前 `F:\Warden` 是在已有快照目录上 `git init` 的本地仓库，不是直接 `clone` 的仓库；已关联并可 fetch，但本地尚无提交历史
- `YOLO26n` 权重仍需用户手动放置到配置路径
- OCR 在本次 smoke 样本上未被触发，因此未做 live OCR 结果验证
- `compileall` 因 `.pyc` 写入权限问题未作为最终语法校验手段；改用实际脚本执行和 `ast.parse`

### Docs Impact

- Docs updated: yes
- Docs touched:
  - `docs/tasks/Warden_MINICONDA_ENV_SETUP_V1.md`
  - `docs/tasks/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
  - `docs/tasks/2026-03-30_runtime_deployment_usage.md`
  - `docs/handoff/2026-03-30_runtime_deployment_v1.md`
  - `scripts/infer/README.md`

### Recommended Next Step

- 为 `MobileCLIP2-S2` 补一个最小 adapter，或明确切换到可直接由当前 runtime stack 加载的 image-text encoder
- 放置 `YOLO26n` 权重后补一次 detector smoke run
- 如需长期 Git 协作，下一步应创建首个本地提交并决定是否与 `origin/main` 做历史对齐

## English Version

# Handoff Metadata

- Handoff ID: HANDOFF-2026-03-30-RUNTIME-DEPLOYMENT-V1
- Related Task ID: Warden_RUNTIME_DEPLOYMENT_TASK_V1
- Task Title: Warden Runtime Deployment Task V1
- Module: inference / runtime / environment
- Author: Codex
- Date: 2026-03-30
- Status: DONE

## 1. Executive Summary

The external runtime task artifacts were copied into the repository, `F:\Warden` was initialized as a Git repository and associated with `origin`, and a first Warden V1 runtime deployment baseline was implemented. The baseline now includes a Miniconda environment definition, a runtime config template, a model preload script, a smoke inference entrypoint, and a runtime usage document. The existing `warden_runtime` environment was verified to contain the key dependencies, `multilingual-e5-small` was downloaded and executed successfully for live text embedding, `MobileCLIP2-S2` was downloaded and is now executed successfully through the official `ml-mobileclip` adapter, `YOLO26n` was downloaded into the local cache and executed successfully in the detector path, and the live PaddleOCR path was validated with a forced-OCR smoke run against the localized external sample `tmp/ocr_smoke_external/rylkngdm.com_20260325T045413Z`.

## 2. What Changed

### Code Changes

- added `environment/warden_runtime_miniconda.yml`
- added `configs/runtime/runtime_default.yaml`
- added `scripts/infer/preload_models.py`
- added `scripts/infer/run_smoke_infer.py`
- updated `scripts/infer/README.md`
- installed official `ml-mobileclip` into `warden_runtime`

### Doc Changes

- copied the user-provided runtime task docs into the repo:
  - `F:\Warden\docs\tasks\Warden_MINICONDA_ENV_SETUP_V1.md`
  - `F:\Warden\docs\tasks\Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- copied the environment example into:
  - `F:\Warden\environment\warden_runtime_env_example.yml`
- added:
  - `F:\Warden\docs\tasks\2026-03-30_runtime_deployment_usage.md`
  - `F:\Warden\docs\handoff\2026-03-30_runtime_deployment_v1.md`

### Output / Artifact Changes

- created `F:\Warden\model_cache\hf\intfloat__multilingual-e5-small`
- created `F:\Warden\model_cache\hf\apple__MobileCLIP2-S2`
- created `F:\Warden\model_cache\paddle`
- created `F:\Warden\model_cache\paddle\paddlex_runtime\official_models\PP-OCRv4_mobile_det`
- created `F:\Warden\model_cache\paddle\paddlex_runtime\official_models\en_PP-OCRv4_mobile_rec`
- created `F:\Warden\model_cache\ultralytics\YOLO26n\weights\best.pt`
- created `F:\Warden\outputs\smoke\runtime\model_preload_manifest.json`
- created `F:\Warden\outputs\smoke\runtime\www.whatsapp-my.eu.cc_20260126T153839Z\runtime_summary.json`
- created `F:\Warden\outputs\smoke\runtime\rylkngdm_external_forced_ocr.json`

## 3. Files Touched

- `F:\Warden\docs\tasks\Warden_MINICONDA_ENV_SETUP_V1.md`
- `F:\Warden\docs\tasks\Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `F:\Warden\environment\warden_runtime_env_example.yml`
- `F:\Warden\environment\warden_runtime_miniconda.yml`
- `F:\Warden\configs\runtime\runtime_default.yaml`
- `F:\Warden\scripts\infer\preload_models.py`
- `F:\Warden\scripts\infer\run_smoke_infer.py`
- `F:\Warden\scripts\infer\README.md`
- `F:\Warden\docs\tasks\2026-03-30_runtime_deployment_usage.md`
- `F:\Warden\docs\handoff\2026-03-30_runtime_deployment_v1.md`
- `.git/` metadata under `F:\Warden`
- `F:\Warden\model_cache\...`
- `F:\Warden\outputs\smoke\runtime\...`

Optional notes per file:

- Git metadata was created by local repository initialization, not by a clean clone
- the copied Desktop artifacts were localized into repo paths for continuity

## 4. Behavior Impact

### Expected New Behavior

- the repository now has a runnable smoke inference CLI for the current frozen sample contract
- the runtime baseline now supports explicit local model caching
- the default runtime now emits component-level evidence bundles without inventing a fused final decision
- the live vision similarity path now works for `MobileCLIP2-S2` through the official adapter
- the detector path now auto-downloads and uses local `YOLO26n` weights
- the OCR path now supports explicit `--force-ocr` execution for smoke/debug runs and uses a repo-local Paddle cache root

### Preserved Behavior

- frozen dataset filenames and sample contracts were not changed
- existing capture/data-manifest/consistency scripts were not modified
- OCR remains trigger-based by default

### User-facing / CLI Impact

- new CLI added: `scripts/infer/preload_models.py`
- new CLI added: `scripts/infer/run_smoke_infer.py`
- existing CLIs were not intentionally changed

### Output Format Impact

- new runtime smoke outputs were added under `outputs/smoke/runtime/`
- no existing output format was changed

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The runtime baseline was added without changing the frozen successful-sample contract. The main operational caveat is repository state, not schema: `F:\Warden` is now Git-associated, but it was initialized locally on top of an existing snapshot directory, so it does not yet share commit history with `origin/main`.

## 6. Validation Performed

### Commands Run

```bash
git fetch origin
git remote -v
python F:\Warden\scripts\infer\preload_models.py --help
python F:\Warden\scripts\infer\run_smoke_infer.py --help
python F:\Warden\scripts\infer\run_smoke_infer.py --sample-dir F:\Warden\data\raw\phish\www.whatsapp-my.eu.cc_20260126T153839Z --config F:\Warden\configs\runtime\runtime_default.yaml
C:\Users\20516\miniconda3\Scripts\conda.exe run -n warden_runtime python F:\Warden\scripts\infer\preload_models.py --config F:\Warden\configs\runtime\runtime_default.yaml --components text vision_similarity ocr detector
C:\Users\20516\miniconda3\Scripts\conda.exe run -n warden_runtime python F:\Warden\scripts\infer\run_smoke_infer.py --sample-dir F:\Warden\data\raw\phish\www.whatsapp-my.eu.cc_20260126T153839Z --config F:\Warden\configs\runtime\runtime_default.yaml --run-live-models
python -c "from pathlib import Path; import ast; files=[Path(r'F:\Warden\scripts\infer\preload_models.py'), Path(r'F:\Warden\scripts\infer\run_smoke_infer.py')]; [ast.parse(p.read_text(encoding='utf-8')) for p in files]; print('ast_ok')"
C:\Users\20516\miniconda3\envs\warden_runtime\python.exe F:\Warden\scripts\infer\preload_models.py --components ocr
C:\Users\20516\miniconda3\envs\warden_runtime\python.exe F:\Warden\scripts\infer\run_smoke_infer.py --sample-dir F:\Warden\tmp\ocr_smoke_external\rylkngdm.com_20260325T045413Z --force-ocr --output F:\Warden\outputs\smoke\runtime\rylkngdm_external_forced_ocr.json
```

### Result

- `origin` was configured and `git fetch origin` succeeded
- `warden_runtime` already existed and key dependencies were importable
- text and vision model artifacts were cached locally
- smoke inference ran successfully in default mode
- live text embedding ran successfully in `warden_runtime`
- live vision similarity ran successfully in `warden_runtime` through the `ml-mobileclip` adapter
- live detector execution ran successfully in `warden_runtime` with local `YOLO26n` weights
- OCR model preload succeeded into `model_cache/paddle/paddlex_runtime/official_models/`
- forced live OCR execution succeeded on the localized external sample and extracted viewport text correctly
- output artifacts were generated under `outputs/smoke/runtime/`
- syntax sanity passed via `ast.parse`

### Not Run

- history alignment between local `main` and `origin/main`

Reason:

the chosen external sample required `--force-ocr` because it is not naturally sparse under the current trigger threshold, and the current repository was initialized locally rather than cloned directly from the remote history.

## 7. Risks / Caveats

- the repo is Git-associated but still has no local commits and no shared history with `origin/main`
- OCR has been validated only via `--force-ocr`; a naturally triggering sparse-text sample is still preferable
- `compileall` could not be used as the final syntax check because `.pyc` writes were denied in this environment

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `F:\Warden\docs\tasks\Warden_MINICONDA_ENV_SETUP_V1.md`
- `F:\Warden\docs\tasks\Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `F:\Warden\docs\tasks\2026-03-30_runtime_deployment_usage.md`
- `F:\Warden\docs\handoff\2026-03-30_runtime_deployment_v1.md`
- `F:\Warden\scripts\infer\README.md`

Doc debt still remaining:

- a dedicated runtime contract document if the evidence bundle schema needs to be frozen later
- a small runtime note documenting the exact `ml-mobileclip` adapter assumptions for later maintenance

## 9. Recommended Next Step

- collect one naturally sparse-text sample to validate trigger-based OCR without `--force-ocr`
- if long-term Git collaboration is required, create the first local commit and decide how to align local history with `origin/main`
