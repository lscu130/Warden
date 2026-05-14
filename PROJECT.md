# PROJECT.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文件是 Warden 的项目级总规格，用于约束项目身份、威胁模型、当前主线、模块边界、冻结原则和近期任务方向。
- 本文件不是 README、任务单、模块文档或 handoff 的替代品。
- 涉及精确字段名、接口、命令、schema、验收标准或历史事实时，以英文版为准。
- 若本文件与当前用户任务、`AGENTS.md`、`GPT_CODEX_WORKFLOW.md`、有效任务单或冻结 schema 冲突，采用更高优先级文件。

---

# Warden 项目总规格

## 1. 项目身份

Warden 是一个 **网页社会工程威胁判断系统**。

Warden 的研究对象超出传统品牌钓鱼页识别。它关注真实网页是否通过身份、品牌、权威、机构、安全、金融、客服、奖励、访问控制等上下文构造高危欺骗行为，和/或诱导、准备、路由用户执行高危动作。

规范短句：

**社会工程威胁 = 高危欺骗行为 和/或 高危诱导动作。**

高危欺骗行为可以在没有观察到凭证表单、支付表单、钱包流程、下载、POST 提交或其他 payload 时成立。此时证据状态应记录为 `payload not observed`，不能自动归为 benign。

Warden 对普通网页的判断必须区分：

- **action surface**：页面存在登录、下载、支付、钱包、客服、跳转、表单等动作表面；
- **threat action**：动作表面处在欺骗、操纵、异常业务上下文、异常目标、异常域名关系或异常提交/下载/授权目标中，升级为威胁动作；
- **business / context legitimacy**：动作表面是否可以被正常业务上下文解释。

动作表面本身不能单独升级为恶意。

## 2. 无效采集不属于威胁模型

以下对象是数据质量或可观测性失败：

- HTTP 错误页；
- 404 / 500 等错误页；
- 空白页；
- 纯色渲染页；
- 严重渲染失败页；
- 结构严重错乱页；
- 证据不可观测页面；
- 无法支持人类基本判断的无效采集样本。

这些对象不进入 Warden 的 benign / malicious / suspicious 威胁标签体系。项目负责人在数据集构建与清洗阶段将其移除，不作为正式 train / validation / test 样本。当前项目不实现 recrawl / exclude / QA 队列作为威胁判断输出。

## 3. 当前阶段定位

Warden 处于 **基础设施、数据与主线契约冻结阶段**。

当前优先级：

- 稳定 capture 输出结构；
- 稳定 TrainSet V1 与辅助数据边界；
- 稳定 L0 / L1 分层职责；
- 稳定文本端、视觉补证据端、Decision Head 的接口；
- 稳定弱标签、人审、蒸馏、runner、handoff 流程；
- 避免在模型训练前反复改变 schema、标签和输出结构。

当前还没有进入最终模型训练和论文级 benchmark 阶段。

## 4. 当前在线主线：L0 + L1

当前在线主线只定义 **L0 + L1**。未来更重的复核或升级层可以另行设计；当前 online architecture 不定义 L2。

### 4.1 样本流

当前样本流：

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

### 4.2 CheapEvidenceSnapshot

`CheapEvidenceSnapshot` 是 L0 前的极轻量证据层。它读取和缓存低成本字段，例如：

- URL / final URL / host；
- title；
- visible_text 是否存在、长度、前缀片段、关键词命中；
- forms / network 的轻量统计；
- artifact presence；
- adult / gambling / gate 的 cheap keyword hints。

它的目标是支持 L0 快速路由，并为 L1 提供可复用基础证据。L1 不应重复读取和重复解析这些 cheap evidence。

### 4.3 L0 合同

L0 是 cheap screening / specialized terminal router。

L0 只处理少量高置信、低成本 terminal 或 auxiliary bucket，例如：

- adult；
- gambling；
- obvious gate / challenge / verification。

L0 不做普通网页的 benign / malicious 判断。所有有效且未被 L0 terminal 的网页样本必须默认进入 L1。

L0 默认不加载：

- full HTML deep extraction；
- screenshots / OCR；
- YOLO / detector；
- CLIP / MobileCLIP；
- SNet / SpecularNet-like；
- 文本塔；
- Decision Head；
- teacher / LLM。

### 4.4 L1 合同

L1 是当前主判断层，但不是单体模型。

L1 包含：

- `L1EvidencePack`：在 `CheapEvidenceSnapshot` 上增量补全完整结构化证据；
- `L1-text`：默认运行的文本与结构化语义主判断分支；
- `Rule Router`：路由与证据充分性诊断器，不是 classifier；
- `L1-vision`：按需视觉补证据端，只包含 OCR / YOLO 类型证据恢复；
- `L1 Decision Head`：未来负责 final decision 的结构化证据裁决头；
- `Evidence Renderer`：基于 evidence ledger 与 reason codes 生成确定性解释。

L1 主证据路径：

- visible_text；
- URL / domain / redirect；
- actionable HTML；
- forms；
- network summary；
- structured / joint signals；
- OCR 补充文字；
- YOLO / detector 补充 UI 组件证据。

L1 视觉端只负责补证据，不负责最终判断。恶意判断主要依赖文本端结构化语义概念、业务上下文、关系一致性、结构化证据，以及 Decision Head 的裁决。

## 5. 当前模型路线原则

### 5.1 文本端

文本端是 L1 的主语义判断路径。它未来应输出结构化语义概念，而不是自由文本推理。

目标概念包括：

- action surface；
- behavior context；
- relation consistency；
- business / context legitimacy；
- risk axes；
- page role；
- payload observed / payload not observed；
- evidence sufficiency。

### 5.2 视觉端

视觉端是 evidence recovery path。

当前默认主线允许：

- OCR：在 visible_text 缺失、稀疏或截图文字化时恢复文字证据；
- YOLO / detector：定位输入框、密码框、OTP、二维码、下载按钮、钱包按钮、验证码、弹窗、主 CTA 等 UI 组件证据。

视觉端不输出 final malicious / benign。

### 5.3 Decision Head

`L1 Decision Head` 是把结构化 JSON 与结构化证据转成 L1 final decision 的模块。

它未来接收：

- text_semantic_concepts；
- URL/domain features；
- actionable HTML features；
- forms/network features；
- OCR text features；
- YOLO UI evidence features；
- rule_router diagnostics；
- joint signals。

它未来输出：

- final label / decision；
- risk score；
- confidence；
- malicious basis；
- payload observed state；
- page role；
- routing / escalation hints；
- reason code inputs for explanation。

当前 Decision Head 尚未训练和接入，现有实现只保留 draft / stub contract。

### 5.4 CLIP / SNet 当前状态

CLIP / MobileCLIP 不进入 Warden V1 默认在线 L1 主线。允许用途：

- 离线截图聚类；
- 模板发现；
- ablation baseline；
- research-only visual-prior experiment；
- 未来另行批准的 optional feature flag。

SNet / SpecularNet-like 不进入 Warden V1 默认在线 L1 主线。允许用途：

- 离线研究；
- ablation；
- 模板/结构聚类辅助；
- 未来可选实验。

拒绝原因：它们缺少业务合法性判断，容易对 benign hard negative 产生高误报。

## 6. 数据与蒸馏原则

### 6.1 数据优先

当前正式训练与正式蒸馏必须等待 benign + malicious 两侧数据集清洗、manifest、split、审计全部完成。

benign clean v1 已可用于开发、loader smoke、pipeline 联调和初步误报观察；最终 full Warden dataset 仍需等待 malicious clean pool 和统一 train / validation / test manifest。

### 6.2 弱标签不是金标

自动规则、crawler 标签、teacher 输出、mock runner 输出、diagnostic runner 输出都不是人工 gold label。

默认原则：

- weak labels are evidence；
- `payload not observed` 不是 automatic benign；
- teacher outputs 是 advisory / distillation targets；
- `do_not_train_as_gold` 必须被下游尊重；
- val/test 不得被 teacher 输出污染。

### 6.3 蒸馏当前状态

当前已有：

- distillation prompt / skill draft；
- runner design contract；
- mock-only runner skeleton；
- real-adapter readiness fields。

当前未做：

- real teacher adapter；
- teacher API 调用；
- 正式蒸馏；
- text tower 训练；
- Decision Head 训练。

正式 teacher distillation 默认只跑 train split。validation / test 只允许 diagnostic-only 检查，不得用于训练、调参、阈值选择或模型选择。

## 7. 模块关系

### 7.1 Data

负责数据目录扫描、manifest、consistency check、样本可用性标志、训练前摘要。

不负责模型结构、推理阈值、原始 schema 重定义。

### 7.2 Labeling

负责自动补标、规则标签、品牌词典匹配、冲突报告、人审辅助输出。

不负责最终训练阈值或推理策略重定义。

### 7.3 Training

负责 loader、config、训练循环、loss、checkpoint、评估指标。

不负责 capture 输出重定义或数据 schema 改造。

### 7.4 Inference

负责 runtime 输入准备、CheapEvidenceSnapshot、L0 / L1 stage routing、L1 evidence pack、Decision Head 接入、evidence renderer、benchmark 与 deployment entrypoint。

不负责训练集重标或弱标签本体重定义。

### 7.5 Paper / Experiment Support

负责实验配置归档、结果聚合、表格图表、可复现说明。

不负责未记录的方法逻辑重写。

## 8. 当前非目标

除非当前任务明确要求，以下不是当前默认目标：

- 重写 frozen schema；
- 重命名稳定字段；
- 把 weak label 当 gold label；
- 把 invalid capture 当威胁模型样本；
- 让 Rule Router 输出 final label；
- 让 CLIP / SNet 进入默认在线主线；
- 实现真实 teacher adapter；
- 正式跑蒸馏；
- 在 malicious clean pool 完成前训练正式 L1；
- 定义当前 online L2。

## 9. 文档优先级与冲突处理

默认优先级：

1. 当前任务中的显式用户要求；
2. `AGENTS.md`；
3. `docs/workflow/GPT_CODEX_WORKFLOW.md`；
4. 当前有效任务单；
5. `PROJECT.md`；
6. module docs；
7. handoff；
8. 当前代码行为；
9. 注释或 TODO。

若冲突存在，必须显式说明，不得静默覆盖更高优先级契约。

## 10. 当前阶段完成标准

当前阶段的完成标准优先是：

**可复现、可审计、可交接。**

不是单纯追逐最终指标。

非 trivial 工作必须有：

- task doc；
- 最小有效修改；
- 最小必要验证；
- 兼容性说明；
- handoff；
- 二审或验收。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# PROJECT.md

# Warden Project Specification

## 1. Project Identity

Warden is a **webpage social-engineering threat judgment system**.

Warden is broader than narrow brand-phishing-page detection. It judges whether a real webpage constructs high-risk deceptive behavior through identity, brand, authority, institution, security, financial, support, reward, or access-control context, and/or whether it induces, prepares, or routes the user toward a high-risk action.

Canonical short form:

**Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.**

High-risk deceptive behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other payload is currently observed. In that case, the evidence state is `payload not observed`; it is not automatic benign.

Warden must distinguish:

- **action surface**: login, download, payment, wallet, support, redirect, form, or similar user-action surface;
- **threat action**: an action surface under deceptive, manipulative, abnormal-business, abnormal-target, abnormal-domain-relation, or abnormal submission / download / authorization context;
- **business / context legitimacy**: whether the action surface can be explained by legitimate business context.

An action surface alone must not be upgraded to malicious.

## 2. Invalid Captures Are Outside The Threat Model

The following are data-quality or observability failures:

- HTTP error pages;
- 404 / 500 error pages;
- blank pages;
- pure-color renders;
- severe broken renders;
- structurally unusable pages;
- insufficient-observability pages;
- invalid captures that do not support basic human judgment.

They are not Warden benign / malicious / suspicious threat-label samples. The project owner removes them during dataset construction and cleaning before formal train / validation / test construction. The current project does not implement a recrawl / exclude / QA queue as a threat-judgment output.

## 3. Current Project Stage

Warden is in a **foundation, data, and contract-freezing stage**.

Current priorities are:

- stabilize capture-output structure;
- stabilize TrainSet V1 and auxiliary data boundaries;
- stabilize L0 / L1 responsibility boundaries;
- stabilize interfaces among the text branch, visual evidence recovery, and Decision Head;
- stabilize weak-label, human-review, distillation, runner, and handoff workflows;
- avoid schema, label, and output-shape churn before model training.

Warden has not yet entered final model training or paper-grade benchmark stage.

## 4. Current Online Mainline: L0 + L1

The current online mainline defines **L0 + L1 only**. Future heavier review or escalation may be designed later; the current online architecture does not define L2.

### 4.1 Sample Flow

Current sample flow:

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

### 4.2 CheapEvidenceSnapshot

`CheapEvidenceSnapshot` is the lightweight evidence layer before L0. It reads and caches low-cost fields such as:

- URL / final URL / host;
- title;
- visible-text presence, length, prefix snippets, and keyword hits;
- lightweight forms / network counts;
- artifact presence;
- adult / gambling / gate cheap keyword hints.

Its purpose is to support fast L0 routing and provide reusable base evidence for L1. L1 should not reread or reparse the same cheap evidence.

### 4.3 L0 Contract

L0 is a cheap screening / specialized terminal router.

L0 handles only a small number of high-confidence, low-cost terminal or auxiliary buckets, such as:

- adult;
- gambling;
- obvious gate / challenge / verification.

L0 does not decide ordinary webpage benign / malicious status. Every valid webpage sample not terminated by L0 must route to L1 by default.

By default, L0 must not load:

- full HTML deep extraction;
- screenshots / OCR;
- YOLO / detector;
- CLIP / MobileCLIP;
- SNet / SpecularNet-like;
- text tower;
- Decision Head;
- teacher / LLM.

### 4.4 L1 Contract

L1 is the current main judgment layer, but it is not a monolithic model.

L1 consists of:

- `L1EvidencePack`: incrementally expands a full structured evidence pack from `CheapEvidenceSnapshot`;
- `L1-text`: the default text and structured-semantic main judgment branch;
- `Rule Router`: a routing and evidence-sufficiency diagnostic component, not a classifier;
- `L1-vision`: optional visual evidence recovery, currently OCR / YOLO style evidence recovery only;
- `L1 Decision Head`: the future structured-evidence adjudication head that owns final L1 decision;
- `Evidence Renderer`: deterministic explanation rendering from evidence ledger and reason codes.

L1 main evidence path:

- visible text;
- URL / domain / redirect;
- actionable HTML;
- forms;
- network summary;
- structured / joint signals;
- OCR-recovered text;
- YOLO / detector UI-component evidence.

The L1 visual branch only recovers evidence. It does not produce final malicious / benign judgment. Malicious judgment primarily comes from the text-side structured semantic concepts, business context, relation consistency, structured evidence, and Decision Head adjudication.

## 5. Current Model-Route Principles

### 5.1 Text Branch

The text branch is the main semantic judgment path in L1. It should output structured semantic concepts rather than free-form reasoning.

Target concepts include:

- action surface;
- behavior context;
- relation consistency;
- business / context legitimacy;
- risk axes;
- page role;
- payload observed / payload not observed;
- evidence sufficiency.

### 5.2 Visual Branch

The visual branch is an evidence recovery path.

The current default mainline allows:

- OCR: recover screenshot text when visible text is missing, sparse, or image-rendered;
- YOLO / detector: localize UI evidence such as input boxes, password fields, OTP fields, QR codes, download buttons, wallet buttons, captcha widgets, modals, and primary CTAs.

The visual branch does not output final malicious / benign.

### 5.3 Decision Head

`L1 Decision Head` converts structured JSON and structured evidence into the L1 final decision.

It will receive:

- text_semantic_concepts;
- URL/domain features;
- actionable HTML features;
- forms/network features;
- OCR text features;
- YOLO UI evidence features;
- rule_router diagnostics;
- joint signals.

It will output:

- final label / decision;
- risk score;
- confidence;
- malicious basis;
- payload observed state;
- page role;
- routing / escalation hints;
- reason-code inputs for explanation.

The Decision Head is not trained or integrated yet. Current implementation only preserves a draft / stub contract.

### 5.4 CLIP / SNet Current Status

CLIP / MobileCLIP are not part of the Warden V1 default online L1 path. Allowed uses:

- offline screenshot clustering;
- template discovery;
- ablation baseline;
- research-only visual-prior experiment;
- a separately approved future optional feature flag.

SNet / SpecularNet-like routes are not part of the Warden V1 default online L1 path. Allowed uses:

- offline research;
- ablation;
- template / structure clustering assistance;
- future optional experiments.

Reason for exclusion from the default online path: they lack business-legitimacy judgment and tend to over-trigger on benign hard negatives.

## 6. Data And Distillation Principles

### 6.1 Data First

Formal training and formal distillation must wait for both benign and malicious datasets to be cleaned, audited, and frozen into final manifests.

`benign_clean_v1` is usable for development, loader smoke, pipeline integration, and preliminary false-positive observation. The final full Warden dataset still depends on malicious clean pool construction and unified train / validation / test manifests.

### 6.2 Weak Labels Are Not Gold Labels

Automatic rules, crawler labels, teacher outputs, mock runner outputs, and diagnostic runner outputs are not human gold labels.

Default rules:

- weak labels are evidence;
- `payload not observed` is not automatic benign;
- teacher outputs are advisory / distillation targets;
- `do_not_train_as_gold` must be respected by downstream consumers;
- val/test must not be polluted by teacher outputs.

### 6.3 Current Distillation State

Current assets:

- distillation prompt / skill draft;
- runner design contract;
- mock-only runner skeleton;
- real-adapter readiness fields.

Not yet done:

- real teacher adapter;
- teacher API calls;
- official distillation;
- text tower training;
- Decision Head training.

Official teacher distillation defaults to train split only. Validation / test may be used only for diagnostic-only inspection, not for training, prompt tuning, threshold tuning, or model selection.

## 7. Module Relations

### 7.1 Data

Owns dataset directory scanning, manifest generation, consistency checks, sample availability flags, and training-preparation summaries.

Does not own model architecture, inference thresholds, or raw schema redesign.

### 7.2 Labeling

Owns auto backfill, rule labels, brand-lexicon matching, conflict reports, and manual-review support outputs.

Does not own final training thresholds or inference-policy redesign.

### 7.3 Training

Owns loaders, configs, training loops, loss, checkpointing, and evaluation metrics.

Does not own capture-output redesign or data schema redesign.

### 7.4 Inference

Owns runtime input preparation, CheapEvidenceSnapshot, L0 / L1 stage routing, L1 evidence pack, Decision Head integration, evidence rendering, benchmark, and deployment entrypoints.

Does not own training-set relabeling or weak-label ontology redesign.

### 7.5 Paper / Experiment Support

Owns experiment-configuration archiving, result aggregation, figures, tables, and reproducibility notes.

Does not own undocumented rewriting of main method logic.

## 8. Current Non-Goals

Unless an active task explicitly asks for it, the following are not default goals:

- rewrite frozen schema;
- rename stable fields;
- treat weak labels as gold labels;
- treat invalid captures as threat-model samples;
- let Rule Router output final labels;
- put CLIP / SNet into the default online mainline;
- implement real teacher adapters;
- run official distillation;
- train official L1 before malicious clean pool completion;
- define an online L2 at the current stage.

## 9. Priority And Conflict Handling

Default priority:

1. explicit user request in the current task;
2. `AGENTS.md`;
3. `docs/workflow/GPT_CODEX_WORKFLOW.md`;
4. the active approved task doc;
5. `PROJECT.md`;
6. module docs;
7. handoff;
8. current code behavior;
9. comments or TODOs.

If a conflict exists, state it explicitly and do not silently override the higher-priority contract.

## 10. Current-Stage Completion Standard

The current-stage completion standard is first:

**reproducible, auditable, and handoff-ready.**

It is not simply chasing final metrics.

Non-trivial work must have:

- a task doc;
- the smallest valid change;
- minimum necessary validation;
- compatibility notes;
- a handoff;
- review or acceptance.
