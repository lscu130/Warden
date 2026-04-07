# Warden Miniconda Environment Setup V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于**人工或 Codex** 在 Miniconda 下配置 Warden V1 运行时环境。
- 本文档服务的目标是：先让默认 runtime stack 可运行、可缓存模型、可做 smoke inference。
- 这不是最终 benchmark 环境，也不是训练环境。
- 默认优先落地 **CPU-conscious baseline**；GPU 是加速选项，不是前置要求。

## 1. 目标环境

建议先固定为以下姿态：

- Python: `3.10`
- 包管理：`conda + pip`
- 目标：普通 PC / modest x86 edge 可运行
- 默认 runtime stack:
  - text encoder: `multilingual-e5-small`
  - image-text encoder: `MobileCLIP2-S2`
  - OCR: `PP-OCRv4 mobile`（trigger-based）
  - detector: `YOLO26n`

为什么先用 Python 3.10：

- PyTorch 当前 stable 要求 Python 3.10+；
- Sentence Transformers 官方也推荐 Python 3.10+；
- 这样能减少 Torch / Transformers / Sentence Transformers / Paddle 之间的兼容噪音。

## 2. 推荐环境策略

### 2.1 先做一个“稳定可跑”的 baseline

先让下面这件事成立：

- 可以建环境
- 可以导入 torch / transformers / sentence-transformers / ultralytics / paddleocr
- 可以本地缓存 HF 模型
- 可以执行 smoke inference

不要在第一步就追求：

- 最优 CUDA 版本
- 最快 OCR GPU 路径
- 量化优化
- ONNX/TensorRT 全套部署

### 2.2 OCR 先走 CPU 更稳

如果你当前主机是 Windows + NVIDIA 50 系显卡，Paddle 官方文档已经给出专门 wheel，同时注明该路径仍有已知问题与适配中的功能。对 Warden 当前阶段，更稳妥的默认策略是：

- 文本塔、视觉 encoder、detector 可走 PyTorch GPU（若你后续确认可用）
- OCR 先使用 Paddle CPU 路径
- 等 smoke runtime 稳定后，再单独评估 Paddle GPU OCR 是否值得接入

## 3. 目录约定

建议把模型缓存放到仓库外或仓库下单独目录，例如：

- `E:\Warden\model_cache\hf`
- `E:\Warden\model_cache\paddle`
- `E:\Warden\model_cache\ultralytics`

并设置环境变量：

- `HF_HOME`
- `TRANSFORMERS_CACHE`（如仍需要兼容旧逻辑）
- `TORCH_HOME`
- 可选：自定义 `WARDEN_MODEL_CACHE`

## 4. Miniconda 创建环境

```bash
conda create -n warden_runtime python=3.10 -y
conda activate warden_runtime
python -m pip install --upgrade pip setuptools wheel
```

## 5. PyTorch 安装策略

### 5.1 最稳默认：先装 CPU 版或默认官方 stable

如果你只是要先让 Codex 把 runtime 跑起来，先用官方 stable 命令即可。
如果当前机器 GPU 路径不确定，先不要把环境卡死在某个 CUDA wheel URL 上。

```bash
pip install torch torchvision torchaudio
```

### 5.2 若要 GPU，加速路径按官方 selector 选

你后续若要 GPU，请去 PyTorch 官方 selector 复制**当前系统对应命令**，不要在文档里硬编码一个可能过期的 CUDA index-url。

建议顺序：

1. 先确认 `nvidia-smi` 正常
2. 再去 PyTorch 官方安装页复制当前命令
3. 安装后执行：

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## 6. 基础运行依赖安装

```bash
pip install -U transformers huggingface_hub sentence-transformers ultralytics pillow opencv-python pyyaml tqdm numpy scipy requests
```

可选：如果你计划直接用 BGE 风格封装而不是只走 sentence-transformers：

```bash
pip install -U FlagEmbedding
```

## 7. Paddle / OCR 安装

### 7.1 默认建议：CPU Paddle

```bash
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
python -m pip install "paddleocr[all]"
```

### 7.2 若只需轻量 OCR 功能，可后续再缩依赖

第一版先不要过度优化安装体积。先让功能稳定，再决定是否裁剪 PaddleOCR 依赖组。

### 7.3 Paddle 验证

```bash
python -c "import paddle; print(paddle.__version__)"
python -c "from paddleocr import PaddleOCR; print('paddleocr_ok')"
```

## 8. Hugging Face 模型缓存建议

建议预下载并固定 revision，不要把“首次联网下载”混进正式 smoke inference 命令。

### 8.1 基础依赖

```bash
pip install -U huggingface_hub
```

### 8.2 设置缓存目录（Windows PowerShell 示例）

```powershell
$env:HF_HOME="E:\Warden\model_cache\hf"
$env:TORCH_HOME="E:\Warden\model_cache\torch"
```

### 8.3 预下载建议对象

- `intfloat/multilingual-e5-small`
- `apple/MobileCLIP2-S2`
- 紧预算可选：`apple/MobileCLIP2-S0`
- 若要更强文本备选：`BAAI/bge-m3`

建议由 Codex 写一个 `preload_models.py`，统一执行模型下载与本地路径登记。

## 9. 建议的最小导入检查

```bash
python -c "import torch; print('torch_ok')"
python -c "import transformers; print('transformers_ok')"
python -c "import sentence_transformers; print('sentence_transformers_ok')"
python -c "from ultralytics import YOLO; print('ultralytics_ok')"
python -c "from paddleocr import PaddleOCR; print('paddleocr_ok')"
```

## 10. 推荐给 Codex 的环境落地顺序

1. 建 `warden_runtime` conda 环境
2. 装 PyTorch stable
3. 装 transformers / sentence-transformers / ultralytics / huggingface_hub
4. 装 Paddle CPU + PaddleOCR
5. 写模型预下载脚本
6. 写 smoke inference 入口
7. 在一个样本目录上做最小验证

## 11. 不要现在就做的事

- 不要一开始就把 OCR GPU、Torch GPU、ONNX、量化、TensorRT 全部一起上
- 不要现在就把 GroundingDINO / Florence-2 做成默认 runtime 依赖
- 不要把 benchmark 还没测的数字写进部署文档
- 不要把环境成功创建和模型成功运行混为一件事

## 12. 失败时优先排查顺序

1. `python --version`
2. `pip --version`
3. `torch.cuda.is_available()`
4. `paddle` 能否导入
5. `ultralytics` 能否导入
6. `sentence_transformers` 能否导入
7. HF 缓存目录是否可写
8. 模型下载是否成功
9. smoke sample 路径是否满足当前输入契约

---

## English Version

> AI note: Codex and other models must treat the English section below as the authoritative version. The Chinese section above is for human readers and quick orientation.

# Warden Miniconda Environment Setup V1

## 1. Intended Environment

This document defines a practical Miniconda-based setup for the current Warden V1 runtime baseline.
It is intended for **smoke deployment and local model caching**, not for final benchmarking or full training.

Recommended baseline:

- Python: `3.10`
- package management: `conda + pip`
- runtime posture: CPU-conscious baseline first
- default runtime stack:
  - text encoder: `multilingual-e5-small`
  - image-text encoder: `MobileCLIP2-S2`
  - OCR: `PP-OCRv4 mobile`, trigger-based
  - detector: `YOLO26n`

## 2. Why Python 3.10

Use Python 3.10 as the initial baseline because it is a stable overlap point for:

- current PyTorch stable usage
- Sentence Transformers recommended versions
- modern Transformers usage
- Ultralytics runtime usage
- Paddle / PaddleOCR support

Do not optimize for the newest possible Python version first.
Optimize for compatibility and reduced environment noise.

## 3. Deployment Strategy

The correct order is:

1. make the baseline runtime importable
2. make the baseline models locally cacheable
3. make smoke inference runnable
4. benchmark and optimize later

Do not attempt all of the following at once in the first pass:

- GPU OCR
- Torch GPU tuning
- ONNX export
- quantization
- TensorRT
- benchmark locking

## 4. Windows + NVIDIA 50-series Note

If the host is Windows with an NVIDIA 50-series GPU, Paddle currently documents a special Windows wheel path for this hardware family and notes known issues for some functionality.
For the current Warden phase, the safer default is:

- allow PyTorch GPU later if confirmed
- keep OCR on Paddle CPU first
- stabilize runtime behavior before experimenting with Paddle GPU OCR

## 5. Directory and Cache Policy

Recommended cache directories:

- `E:\Warden\model_cache\hf`
- `E:\Warden\model_cache\paddle`
- `E:\Warden\model_cache\ultralytics`

Recommended environment variables:

- `HF_HOME`
- `TRANSFORMERS_CACHE` if needed for legacy compatibility
- `TORCH_HOME`
- optional `WARDEN_MODEL_CACHE`

## 6. Create the Miniconda Environment

```bash
conda create -n warden_runtime python=3.10 -y
conda activate warden_runtime
python -m pip install --upgrade pip setuptools wheel
```

## 7. PyTorch Installation Policy

### 7.1 Safe baseline

For the first deployment pass, install official stable PyTorch without hard-coding an environment-specific CUDA index in this document:

```bash
pip install torch torchvision torchaudio
```

### 7.2 GPU path

If GPU acceleration is desired, use the **current official PyTorch selector** for the exact host OS and driver situation.
Do not hard-code a possibly stale CUDA wheel URL into the first-pass environment spec.

Verify after install:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## 8. Core Runtime Dependencies

```bash
pip install -U transformers huggingface_hub sentence-transformers ultralytics pillow opencv-python pyyaml tqdm numpy scipy requests
```

Optional if the runtime or later tuning path explicitly wants BGE-native wrappers:

```bash
pip install -U FlagEmbedding
```

## 9. Paddle / OCR Installation

### 9.1 Default recommendation: Paddle CPU first

```bash
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
python -m pip install "paddleocr[all]"
```

This is the recommended first-pass path for Warden V1 runtime stabilization.

### 9.2 Validation

```bash
python -c "import paddle; print(paddle.__version__)"
python -c "from paddleocr import PaddleOCR; print('paddleocr_ok')"
```

## 10. Hugging Face Model Caching

Do not treat first-time online download as the same thing as stable runtime behavior.
Pre-download models and reuse local paths.

Recommended preload targets:

- `intfloat/multilingual-e5-small`
- `apple/MobileCLIP2-S2`
- optional tight-budget fallback: `apple/MobileCLIP2-S0`
- optional stronger text fallback: `BAAI/bge-m3`

Recommended approach:

- install `huggingface_hub`
- use a preload helper script
- pin model paths or model ids in runtime config
- keep local cache paths explicit

## 11. Minimal Import Checks

```bash
python -c "import torch; print('torch_ok')"
python -c "import transformers; print('transformers_ok')"
python -c "import sentence_transformers; print('sentence_transformers_ok')"
python -c "from ultralytics import YOLO; print('ultralytics_ok')"
python -c "from paddleocr import PaddleOCR; print('paddleocr_ok')"
```

## 12. Recommended Setup Order For Codex

1. create `warden_runtime`
2. install stable PyTorch
3. install Transformers / Sentence Transformers / Ultralytics / HF Hub
4. install Paddle CPU + PaddleOCR
5. implement model preload script
6. implement smoke inference entrypoint
7. validate on one sample directory

## 13. Not For This Phase

Do not do the following in the first pass:

- enable all acceleration paths at once
- make GroundingDINO or Florence-2 runtime dependencies
- write unmeasured benchmark numbers into deployment docs
- confuse environment creation with successful runtime execution

## 14. Debugging Order

When setup fails, debug in this order:

1. `python --version`
2. `pip --version`
3. `torch.cuda.is_available()`
4. whether `paddle` imports
5. whether `ultralytics` imports
6. whether `sentence_transformers` imports
7. whether the HF cache path is writable
8. whether model downloads completed
9. whether the smoke sample path matches the current input contract
