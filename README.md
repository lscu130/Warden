<p align="center">
  <img src="assets/Warden_logo_full.png" alt="Warden Logo" width="520">
</p>

# Warden

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本 README 是仓库入口和当前阶段导览。
- 精确定义、字段、任务边界、接口和验收标准以英文版、`PROJECT.md`、模块文档、任务单和 handoff 为准。
- 当前 README 反映 Warden 最新主线：网页社会工程威胁判断、L0 + L1、文本/结构优先、视觉补证据、CLIP/SNet 不进默认在线主线。

## 1. 项目概览

Warden 是一个 **网页社会工程威胁判断系统**。

它关注网页是否存在高危欺骗行为，和/或是否诱导、准备、路由用户执行高危动作，例如：

- 账号、密码、OTP、支付信息、钱包授权、助记词索取；
- 品牌、平台、机构、客服、安全、金融、奖励、访问控制等身份或信任上下文伪造；
- 假客服引流、恶意下载、假验证、假奖励、Web3 钱包滥用；
- 通过文案、布局、跳转、表单、按钮或视觉伪装推动用户执行危险操作。

规范短句：

**社会工程威胁 = 高危欺骗行为 和/或 高危诱导动作。**

页面即使当前没有观察到登录框、支付框、钱包流程、下载、POST 提交或其他 payload，也可能因高危欺骗行为构成 malicious。这类证据状态应记录为 `payload not observed`，不能自动视为 benign。

## 2. 当前系统主线

当前在线系统只定义 **L0 + L1**。未来更重的复核或升级层可以另行设计；当前阶段不把 L2 作为在线主线契约。

```text
Raw sample
  -> CheapEvidenceSnapshot
  -> L0Router
  -> if L0 terminal: stop / auxiliary terminal
  -> else: L1EvidencePack.expand(cheap_snapshot)
  -> L1 text branch
  -> Rule Router diagnostics
  -> optional OCR / YOLO evidence recovery
  -> L1 Decision Head
  -> Evidence Renderer
```

### 2.1 CheapEvidenceSnapshot

L0 前先构建极轻量证据快照，用于避免重复读取基础文件。它包含 URL、title、visible_text 统计、forms/network 轻量统计、artifact presence、adult/gambling/gate cheap hints 等。

### 2.2 L0

L0 是 cheap screening / specialized terminal router。

它只处理少数高置信低成本 bucket：

- adult；
- gambling；
- obvious gate / challenge / verification。

所有有效且未被 L0 terminal 的网页默认进入 L1。L0 不判断普通网页的 benign / malicious 状态。

### 2.3 L1

L1 是当前主判断层，但不是单体模型。

L1 包含：

- `L1EvidencePack`：在 `CheapEvidenceSnapshot` 基础上增量补全完整证据；
- `L1-text`：默认运行的文本与结构化语义主路径；
- `Rule Router`：路由和证据充分性诊断器，不是分类器；
- `L1-vision`：按需 OCR / YOLO 视觉补证据端；
- `L1 Decision Head`：未来负责 L1 final decision；
- `Evidence Renderer`：基于 evidence ledger 与 reason codes 的确定性解释器。

## 3. 视觉端定位

视觉端当前只负责补充证据：

- OCR 用于 visible_text 缺失、稀疏或文字图片化时恢复截图文字；
- YOLO / detector 用于定位输入框、密码框、OTP、二维码、下载按钮、钱包按钮、验证码、弹窗、主 CTA 等 UI 组件。

视觉端不负责最终 malicious / benign 判断。

CLIP / MobileCLIP 不进入默认在线 L1 主线。SNet / SpecularNet-like 也不进入默认在线 L1 主线。它们仅保留为离线聚类、模板发现、ablation、研究实验或未来另行批准的可选功能。

## 4. 数据与训练状态

当前重点仍是数据、契约和工程骨架，而不是最终模型分数。

当前状态：

- benign clean v1 可用于开发、loader smoke、pipeline 联调和初步误报观察；
- final full Warden dataset 仍需等待 malicious clean pool、统一 manifest、split、审计；
- 正式蒸馏必须等待 benign + malicious 最终数据集冻结；
- 正式 teacher distillation 默认只跑 train split；
- val/test 不得被 teacher 输出污染；
- text tower、Decision Head、OCR / YOLO adapter 还未作为最终模型接入。

## 5. 无效采集说明

HTTP 错误页、404、空白页、纯色页、严重渲染失败、结构严重错乱、证据不可观测页面属于数据质量或可观测性失败。

这些样本不进入 Warden 的 benign / malicious / suspicious 威胁标签体系。项目负责人在数据集构建与清洗阶段直接移除。

## 6. 当前非目标

当前默认不做：

- 把 invalid capture 当威胁样本；
- 让 L0 判断普通网页 benign / malicious；
- 让 Rule Router 输出 final label；
- 让视觉端承担最终判断；
- 让 CLIP / SNet 进入默认在线主线；
- 在 malicious clean pool 完成前训练正式 L1；
- 在最终数据集冻结前正式蒸馏；
- 当前阶段定义在线 L2。

## 7. 当前工程状态

Warden 已经建立或正在建立：

- L0 / L1 runtime skeleton；
- CheapEvidenceSnapshot；
- L1 evidence pack skeleton；
- Rule Router draft；
- L1 draft sidecar；
- Decision Head draft contract；
- distillation prompt / skill / runner skeleton；
- handoff / task / review 纪律。

当前最重要的主线是继续完成 malicious clean pool，然后冻结 full dataset，之后再进入正式蒸馏、文本塔训练和 Decision Head 训练。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden

Warden is a **webpage social-engineering threat judgment system**.

It is broader than narrow brand-phishing detection. Warden judges whether a real webpage presents high-risk deceptive behavior and/or high-risk induced action.

Canonical short form:

**Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.**

High-risk deceptive behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other payload is currently observed. That state should be recorded as `payload not observed`; it is not automatic benign.

## 1. What Warden Looks For

Warden focuses on evidence such as:

- credential, OTP, payment, wallet-approval, or seed-phrase collection;
- false or misleading identity, brand, institution, authority, security, finance, support, reward, or access-control context;
- fake-support diversion, malicious downloads, fake verification, fake rewards, Web3 wallet abuse, and attack-chain redirects;
- wording, layout, redirects, forms, buttons, or visual disguise that push users toward dangerous actions.

Warden distinguishes:

- action surfaces;
- threat actions;
- business / context legitimacy;
- payload observed versus payload not observed;
- evidence sufficiency.

Action surface alone is not malicious. A login form, download button, payment page, wallet button, or support page must be interpreted with page context, URL/domain relation, business legitimacy, form/network targets, and other evidence.

## 2. Current Online Mainline: L0 + L1

The current online architecture defines **L0 + L1 only**. Future heavier review or escalation may be designed later; the current online architecture does not define L2.

```text
Raw sample
  -> CheapEvidenceSnapshot
  -> L0Router
  -> if L0 terminal: stop / auxiliary terminal
  -> else: L1EvidencePack.expand(cheap_snapshot)
  -> L1 text branch
  -> Rule Router diagnostics
  -> optional OCR / YOLO evidence recovery
  -> L1 Decision Head
  -> Evidence Renderer
```

### 2.1 CheapEvidenceSnapshot

`CheapEvidenceSnapshot` is a lightweight evidence snapshot built before L0. It reads and caches only cheap evidence:

- URL / final URL / host;
- title;
- visible-text presence, length, prefix snippets, and keyword hits;
- lightweight forms / network counts;
- artifact presence;
- adult / gambling / gate hints.

L1 should reuse this snapshot rather than rereading and reparsing the same cheap evidence.

### 2.2 L0

L0 is a cheap screening / specialized terminal router.

It handles only a few high-confidence, low-cost terminal or auxiliary buckets:

- adult;
- gambling;
- obvious gate / challenge / verification.

Every valid webpage sample not terminated by L0 routes to L1 by default. L0 does not decide ordinary webpage benign / malicious status.

### 2.3 L1

L1 is the current main judgment layer, but it is not a monolithic model.

L1 includes:

- `L1EvidencePack`: incrementally expands full structured evidence from `CheapEvidenceSnapshot`;
- `L1-text`: the default text and structured-semantic main path;
- `Rule Router`: routing and evidence-sufficiency diagnostics, not a classifier;
- `L1-vision`: optional OCR / YOLO evidence recovery;
- `L1 Decision Head`: the future owner of the final L1 decision;
- `Evidence Renderer`: deterministic explanation from evidence ledger and reason codes.

## 3. Visual Branch Position

The visual branch recovers evidence. It does not make the final malicious / benign decision.

Current default visual evidence recovery consists of:

- OCR for screenshot text recovery when visible text is missing, sparse, or image-rendered;
- YOLO / detector for UI-component evidence such as input boxes, password fields, OTP fields, QR codes, download buttons, wallet buttons, captcha widgets, modals, and primary CTAs.

CLIP / MobileCLIP are not part of the Warden V1 default online L1 path. SNet / SpecularNet-like routes are not part of the Warden V1 default online L1 path. They may be used only for offline clustering, template discovery, ablation, research experiments, or a separately approved future optional feature flag.

## 4. Current Data And Training State

The project is still in a foundation and contract-freezing stage.

Current status:

- `benign_clean_v1` is usable for development, loader smoke, pipeline integration, and preliminary false-positive observation;
- the final full Warden dataset still depends on malicious clean pool construction, unified manifests, split, and audit;
- official distillation must wait for the final benign + malicious dataset freeze;
- official teacher distillation defaults to train split only;
- validation / test must not be polluted by teacher outputs;
- the text tower, Decision Head, and OCR / YOLO adapters have not been integrated as final trained models.

## 5. Invalid Captures

HTTP error pages, 404 pages, blank pages, pure-color pages, severe broken renders, structurally unusable pages, and insufficient-observability pages are data-quality or observability failures.

They are not Warden benign / malicious / suspicious threat-label samples. The project owner removes them during dataset construction and cleaning.

## 6. Current Non-Goals

The current default scope does not include:

- treating invalid captures as threat samples;
- letting L0 decide ordinary webpage benign / malicious status;
- letting Rule Router output final labels;
- letting the visual branch make final judgments;
- putting CLIP / SNet into the default online mainline;
- training official L1 before malicious clean pool completion;
- running official distillation before the final dataset freeze;
- defining an online L2 at the current stage.

## 7. Current Engineering State

Warden currently has or is building:

- L0 / L1 runtime skeleton;
- CheapEvidenceSnapshot;
- L1 evidence-pack skeleton;
- Rule Router draft;
- L1 draft sidecar;
- Decision Head draft contract;
- distillation prompt / skill / runner skeleton;
- task / handoff / review discipline.

The most important next mainline is malicious clean pool construction. After benign + malicious data are frozen into a full dataset, Warden can proceed to official distillation, text-tower training, and Decision Head training.

## 8. Recommended Current Use Of This README

Use this README as:

- the repository front-page overview;
- a current-stage explanation for collaborators and model agents;
- a quick orientation document before reading `PROJECT.md`, module docs, task docs, and handoffs.

For exact task boundaries, use the active task document. For project-level authority, use `PROJECT.md`. For delivery truth, use the matching handoff.
