# PROJECT.md

## 2026-04-27 Chinese Definition Update Summary

- Warden 的社会工程威胁定义已对齐为：**高危欺骗行为和/或高危诱导动作**。
- 页面即使当前没有观察到凭证表单、支付表单、钱包流程、下载、POST 提交或其他高危动作，也可能因高危欺骗行为构成 malicious。
- `payload not observed` 不能自动等同于 benign。

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板、优先级规则或历史事实，以英文版为准。
- 本文档是 **项目级总规格**，用于定义 Warden 在当前阶段的项目目标、主线边界、冻结原则与模块关系。
- 本文档不是 `README.md` 的重复版，也不是单个模块文档或任务单的替代品。
- 若与当前任务单、`AGENTS.md` 或 `docs/workflow/GPT_CODEX_WORKFLOW.md` 冲突，以更高优先级文件为准。

# Warden 项目总规格

## 1. 文档目的

`PROJECT.md` 用于在项目级回答以下问题：

1. Warden 现在到底在做什么；
2. 当前主线是什么，不是什么；
3. 当前阶段优先收敛哪些内容；
4. 项目级冻结边界在哪里；
5. 模块之间如何分工而不互相越界；
6. 后续任务、模块文档、训练与推理实现，应围绕什么总契约展开。

它的作用是减少多窗口、多模型、多轮交接下的语义漂移，避免把 README、模块文档、任务单和聊天上下文拼接成一个不稳定的“隐式项目定义”。

## 2. 项目身份

Warden 是一个 **网页社会工程威胁判断系统**。

它的研究对象不是狭义的“品牌钓鱼页识别”，也不是单一 logo 匹配器。Warden 关注的是：

- 网页是否存在社会工程诱导；
- 网页是否索取密码、OTP、支付信息、钱包授权、助记词等敏感信息；
- 网页是否通过视觉伪装、文案、流程或跳转诱导用户执行高风险动作；
- 网页风险是否足够高，需要进入更强的复核层；
- 在轻量、边缘、成本受限的前提下，系统是否仍然可部署、可审计、可复现。

## 3. 当前阶段定位

Warden 当前处于 **基础设施与主线规格冻结阶段**。

当前优先级不是追求花哨的最终模型分数，而是优先把以下基础打稳：

- 数据采集输出结构；
- TrainSet V1 主训练集边界；
- Gate / Evasion auxiliary set 的独立定位；
- 标签字段、弱标签命名空间与回填路径；
- L0 / L1 / L2 的分层职责；
- 轻量文本 / 视觉 / 融合路线；
- 任务单、交接单与审查流程。

这意味着：

- 当前阶段允许继续补数据、补文档、补弱标签、补视觉/文本模块规格；
- 当前阶段不应无边界地大改 schema、随意重命名字段或重写整条主线；
- 任何影响公共契约的修改，都必须先显式冻结任务边界。

## 4. 当前主线

当前 Warden 主线由以下几条组成：

### 4.1 问题主线

主问题定义为：
**对真实网页进行轻量、多模态、分层式社会工程威胁判断。**

默认系统视图：

- **L0**：低成本、快路径、高召回筛查；
- **L1**：更强的语义 / 结构判断；
- **L2**：高成本升级复核层，用于高风险、歧义或困难样本。

### 4.2 数据主线

数据主线建立在当前 capture 输出冻结契约之上。

当前主训练基线为：

- `docs/data/TRAINSET_V1.md`

它定义：

- 哪些成功样本可进入训练集；
- 哪些文件是主依赖；
- 哪些文件只是增强项；
- manifest 如何表达 text / vision / multimodal 可用性。

### 4.3 辅助问题主线

Gate / Evasion 样本在当前版本中属于 **Auxiliary Set**，而非 TrainSet V1 primary。

其协议由以下文件单独定义：

- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

默认原则：

- 不自动并入 TrainSet V1 primary；
- 不默认改变主 manifest 语义；
- 若未来需要接口，必须 opt-in、default-off、backward-compatible。

### 4.4 工程主线

工程主线是 **documentation-first + contract-first + minimal-patch execution**。

默认过程不是“想到什么就改什么”，而是：

1. 先做需求整理；
2. 冻结任务边界；
3. 进行最小实现；
4. 做最小必要验证；
5. 交接；
6. 再审查与验收。

## 5. 当前非目标

除非明确要求，以下内容不是当前默认目标：

- 静默大重构；
- 任意 schema 改名；
- 随意更换公共输出格式；
- 把弱标签当成人工金标；
- 把 Gate / Evasion 问题吸收成主训练目标；
- 把所有样本都强行送进最重模型路径；
- 引入未经批准的新依赖；
- 用“模型觉得可以”替代任务验收；
- 先做宏大平台化，再回头补基础数据契约。

## 6. 冻结与变更原则

### 6.1 上游数据冻结优先

当前脚本实际产出的样本目录与字段，是数据上游真相。

下游训练、清单、统计、补标、评估和推理实现，必须围绕当前冻结输出结构工作，而不是为训练方便偷偷改上游字段。

### 6.2 字段与枚举稳定性优先

除非明确批准或显式升版本：

- 不重命名已冻结字段；
- 不修改已冻结文件名；
- 不静默改变 top-level JSON key；
- 不合并语义不同的字段；
- 不把一个稳定字段拆成多个新字段。

### 6.3 文档显式升版本

当项目级边界发生变化时，应通过文档版本或新文件明确表达，而不是依赖聊天上下文默认继承。

以下情况通常需要显式更新：

- 主问题定义变化；
- TrainSet 主契约变化；
- 新的核心模块进入主线；
- L0 / L1 / L2 职责变化；
- 公共输出、CLI、标签语义或目录规范变化。

## 7. 模块关系

Warden 默认包含以下模块层次：

### 7.1 Data

拥有：

- 数据目录扫描；
- manifest 生成；
- consistency check；
- 样本可用性标志；
- 训练前数据准备摘要。

不拥有：

- 模型结构决策；
- 推理阈值政策；
- 原始 schema 重定义。

### 7.2 Labeling

拥有：

- 自动补标；
- 规则标签；
- 品牌词典匹配；
- 冲突报告；
- 手工校正辅助输出。

不拥有：

- 最终训练阈值；
- 推理阶段策略重定义。

### 7.3 Training

拥有：

- loader；
- config；
- 训练循环；
- loss 与 checkpointing；
- 评估指标实现。

不拥有：

- 原始数据 schema 改造；
- capture 输出结构重定义。

### 7.4 Inference

拥有：

- 运行时输入准备；
- stage routing；
- 阈值应用；
- L0 / L1 / L2 执行策略；
- 运行时证据打包；
- benchmark 与 deployment entrypoints。

不拥有：

- 训练集重标；
- 弱标签本体重定义。

### 7.5 Paper / Experiment Support

拥有：

- 实验配置归档；
- 结果聚合；
- 表格与图表辅助；
- 可复现说明。

不拥有：

- 未记录的“方法逻辑重写”；
- 反向覆盖主规格。

## 8. 关键基线文档

当前项目级主线应至少与以下文档保持一致：

- `README.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/MODULE_INFER.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

解释原则：

- `README.md` 提供仓库入口和阶段背景；
- 本文件提供项目级总规格；
- `MODULE_*.md` 提供模块边界与职责；
- `TASK_TEMPLATE.md` 提供任务级执行边界；
- `HANDOFF_TEMPLATE.md` 提供交付级记录边界。

## 9. 文档优先级与冲突处理

本文件是项目级规格，但不是最高优先级文件。

默认优先级如下：

1. 当前任务中的显式用户要求；
2. `AGENTS.md`；
3. `docs/workflow/GPT_CODEX_WORKFLOW.md`；
4. 当前有效任务单；
5. `PROJECT.md`；
6. 模块文档；
7. 相关 handoff；
8. 现有代码行为；
9. 代码注释或 TODO。

若本文件与更高优先级文件冲突：

- 必须显式指出冲突；
- 不得静默覆盖更高优先级契约；
- 应采用最安全、最兼容的解释继续工作。

## 10. 当前模型路线原则

当前模型路线以 **轻量、多模态、可部署** 为前提。

项目级默认原则为：

- 文本塔优先走轻量路线；
- 视觉塔优先走轻量路线；
- 允许使用更强教师模型进行蒸馏或离线伪标；
- 融合层必须保留可审计性；
- 运行时成本从设计起点就算进约束；
- L0 不允许静默吸收重成本逻辑；
- L1 是当前主判断层；
- L2 保留给高风险、困难、开放世界和后续鲁棒性问题。

## 11. 当前数据与标签原则

### 11.1 数据优先于模型炫技

当前阶段，项目更重视：

- 数据可复现；
- 标签语义稳定；
- capture 输出稳定；
- backfill 路径可审计；
- 训练与推理共享同一上游数据契约。

### 11.2 弱标签不是金标

当前项目允许：

- 自动补标；
- 规则标签；
- 离线 backfill；
- 选择性人工修正。

但默认不允许：

- 把 auto labels 当作人工 gold labels；
- 用启发式结论伪装成最终真值；
- 让 Data 模块把弱标签提升成金标层。

### 11.3 品牌逻辑只是支持证据

品牌匹配在 Warden 中是支持证据，而不是全部判断依据。

主问题仍然是：
**网页是否正在实施具有意义的社会工程风险。**

## 12. 当前执行纪律

Warden 不是 demo 沙盒，而是实际工程项目。

所有非 trivial 工作默认遵守：

1. 先读相关文档；
2. 再整理需求；
3. 冻结任务边界；
4. 做最小有效修改；
5. 跑最小必要验证；
6. 写清兼容性影响；
7. 写 handoff；
8. 再做审查与验收。

对于跨模块、改 schema、改 labels、改 CLI、改输出格式的任务：

- 默认视为 non-trivial；
- 不得跳过任务单；
- 不得跳过 handoff；
- 不得跳过审查；
- 不得把“没跑但应该没问题”写成验证通过。

## 13. 当前阶段完成标准

以当前阶段而言，一个“完成”的子方向至少应满足：

- 有明确的项目或模块文档；
- 与冻结字段和上游契约不冲突；
- 有明确的输入与输出边界；
- 有最小验证路径；
- 能解释兼容性影响；
- 能通过 handoff 交给下一个窗口继续。

这意味着，当前阶段的完成标准首先是：
**可复现、可审计、可交接。**
而不是“看起来很先进”。

## 14. 近期主线任务方向

当前阶段最合理的近程任务方向包括：

- 继续积累与筛查高质量样本；
- 稳定 TrainSet V1 相关脚本与报告；
- 完善标签与品牌词典；
- 明确视觉与文本模块规格；
- 打通轻量训练 / 评测 / 推理基线；
- 为后续论文叙事保留稳定的工程与数据契约。

## 15. 本文件不承担的职责

本文件不直接定义：

- 某一条具体任务的 scope_in / scope_out；
- 某个脚本的详细实现；
- 某个模型配置的参数表；
- 单个任务的 acceptance checklist；
- 单个交付的 validation 结果。

这些内容应分别进入：

- 任务单；
- 模块文档；
- 配置文件；
- handoff；
- 评测或 benchmark 文档。

### 原始中文说明

中文内容保留在前，供人工协作与快速导览。英文版为权威版本。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# PROJECT.md

# Warden Project Specification

## 1. Purpose

`PROJECT.md` is the project-level specification for Warden.

It exists to answer the following questions at the project level:

1. what Warden is currently trying to build;
2. what the active mainline is and what it is not;
3. what the current-stage priorities are;
4. where the active freeze boundaries are;
5. how modules relate without silently absorbing each other's responsibility;
6. what later tasks, module docs, training work, and inference work must stay aligned with.

This file exists to reduce semantic drift across long-context chats, multi-agent collaboration, and cross-window continuation. It should prevent the project definition from being reconstructed implicitly from README notes, module docs, task docs, and partial memory.

## 2. Project Identity

Warden is a **webpage social-engineering threat judgment system**.

It is not a narrow brand-phishing detector and not a pure logo recognizer. Warden is concerned with questions such as:

- whether a webpage exhibits high-risk deceptive behavior, such as false or misleading identity, brand, authority, institution, security, financial, support, reward, or access-control context construction;
- whether a webpage induces, prepares, or routes the user toward high-risk actions;
- whether it is requesting passwords, OTP codes, payment details, wallet approvals, seed phrases, or other sensitive information;
- whether it is pushing the user toward a dangerous action through wording, layout, interaction flow, redirects, or visual disguise;
- whether the sample is risky enough to require escalation to a stronger review stage;
- whether the system remains deployable, auditable, and reproducible under lightweight and edge-constrained conditions.

Canonical short form:

**Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.**

High-risk deceptive behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other high-risk action is currently observed. In that situation, the evidence state should be described as `payload not observed`, not as automatic benign.

## 3. Current Project Stage

Warden is currently in a **foundation and contract-freezing stage**.

The priority is not flashy end metrics. The priority is to stabilize the foundations that later training, evaluation, and deployment will depend on:

- capture-output structure;
- TrainSet V1 primary boundary;
- separate positioning of the gate / evasion auxiliary set;
- label fields, weak-label namespaces, and backfill paths;
- L0 / L1 / L2 responsibility boundaries;
- lightweight text / vision / fusion route;
- workflow, task, handoff, and review discipline.

This means:

- the project should continue to improve data, docs, weak labels, and module specifications;
- it should not casually redesign shared schema, rename frozen fields, or rewrite the mainline without explicit approval;
- any change affecting a shared contract must first have an explicit task boundary.

## 4. Active Mainline

The current Warden mainline consists of the following threads.

### 4.1 Problem Mainline

The main problem is defined as:
**lightweight, multimodal, staged social-engineering threat judgment for real webpages.**

Default system view:

- **L0**: low-cost, fast-path, high-recall screening;
- **L1**: stronger semantic / structural judgment;
- **L2**: highest-cost escalation for hard, high-risk, or ambiguous cases.

Current L0 contract:

- L0 is a screening and routing layer, not a final adjudication layer.
- The default L0 hot path is intentionally narrow: it consumes cheap URL, visible-text/title, form-summary, network-summary, raw visible-text observability, and existing cheap diff/evasion hints when present.
- L0 currently specializes in fast `gambling / adult / gate` surface detection and routing hints.
- L0 must not silently make full HTML, default brand extraction, screenshots/OCR, heavy model inference, or interaction recovery part of its default path.

### 4.2 Data Mainline

The data mainline is built on top of the frozen capture-output contract.

The current primary training baseline is:

- `docs/data/TRAINSET_V1.md`

It defines:

- which successful samples are admissible;
- which files are the primary dependency set;
- which files are enhancements rather than requirements;
- how the manifest should express text / vision / multimodal usability.

### 4.3 Auxiliary-Problem Mainline

Gate / evasion samples belong to an **Auxiliary Set** rather than to TrainSet V1 primary.

Their protocol is defined separately in:

- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

Default rule:

- do not auto-admit them into TrainSet V1 primary;
- do not silently change primary-manifest semantics;
- if a future interface is added, it must be opt-in, default-off, and backward compatible.

### 4.4 Engineering Mainline

The engineering mainline is **documentation-first + contract-first + minimal-patch execution**.

The default process is not improvised free-form coding. It is:

1. clarify the requirement;
2. freeze the task boundary;
3. implement the smallest valid change;
4. run the minimum necessary validation;
5. produce handoff;
6. return for review and acceptance.

## 5. Non-Goals At The Current Stage

Unless explicitly requested, the following are not default goals:

- silent large-scale refactor;
- arbitrary schema renaming;
- casual replacement of public output formats;
- treating weak labels as human gold labels;
- absorbing gate / evasion into the primary training objective;
- routing every sample into the most expensive path by default;
- adding dependencies without explicit approval;
- treating "the model thinks it is fine" as acceptance;
- trying to build a grand platform before the data and contract foundations are stable.

## 6. Freeze And Change Principles

### 6.1 Upstream Data Freeze First

The current script-produced sample structure is upstream truth.

Downstream training, manifest, statistics, backfill, evaluation, and inference work must adapt to the active frozen output contract rather than silently changing upstream fields for downstream convenience.

### 6.2 Field And Enumeration Stability First

Unless explicitly approved or version-bumped:

- do not rename frozen fields;
- do not rename frozen files;
- do not silently change top-level JSON keys;
- do not merge semantically different fields;
- do not split a stable field into several new fields.

### 6.3 Explicit Document Versioning

When project-level boundaries change, the change should be recorded through document updates or explicit versioning rather than through chat-only context.

Typical triggers for explicit updates include:

- a change in the main problem framing;
- a change in the TrainSet primary contract;
- a new core module entering the mainline;
- a change in L0 / L1 / L2 responsibility boundaries;
- a change in shared outputs, CLI, label semantics, or directory conventions.

## 7. Module Relations

Warden currently assumes the following module structure.

### 7.1 Data

Owns:

- dataset directory scanning;
- manifest generation;
- consistency checks;
- sample availability flags;
- training-preparation summaries.

Does not own:

- model architecture decisions;
- inference threshold policy;
- raw schema redesign.

### 7.2 Labeling

Owns:

- auto backfill;
- rule labels;
- brand-lexicon matching;
- conflict reports;
- manual-review support outputs.

Does not own:

- final training thresholds;
- inference-policy redesign.

### 7.3 Training

Owns:

- loaders;
- configs;
- training loops;
- loss and checkpointing;
- evaluation-metric implementation.

Does not own:

- raw data schema redesign;
- capture-output redesign.

### 7.4 Inference

Owns:

- runtime input preparation;
- stage routing;
- threshold application;
- L0 / L1 / L2 execution policy;
- runtime evidence packaging;
- benchmark and deployment entrypoints.

Does not own:

- training-set relabeling;
- weak-label ontology redesign.

### 7.5 Paper / Experiment Support

Owns:

- experiment-configuration archiving;
- result aggregation;
- figure and table helpers;
- reproducibility notes.

Does not own:

- undocumented rewriting of main method logic;
- silent override of project contracts.

## 8. Key Baseline Documents

The active project-level mainline should stay aligned with at least the following files:

- `README.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/MODULE_INFER.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Interpretation rule:

- `README.md` is the repository entry and stage background;
- this file is the project-level specification;
- `MODULE_*.md` files define module boundaries and responsibilities;
- `TASK_TEMPLATE.md` defines execution boundaries for a concrete task;
- `HANDOFF_TEMPLATE.md` defines delivery boundaries for a concrete change.

## 9. Priority And Conflict Handling

This file is project-level authority, but it is not the highest-priority file.

Default priority order:

1. explicit user request in the current task;
2. `AGENTS.md`;
3. `docs/workflow/GPT_CODEX_WORKFLOW.md`;
4. the active approved task doc;
5. `PROJECT.md`;
6. module docs;
7. relevant handoff;
8. current code behavior;
9. comments or TODOs.

If this file conflicts with a higher-priority source:

- state the conflict explicitly;
- do not silently override the higher-priority contract;
- continue with the safest compatible interpretation.

## 10. Current Model-Route Principles

The current model route is constrained by **lightweight, multimodal, deployable-first** assumptions.

Default project-level principles:

- the text tower should stay lightweight by default;
- the vision tower should stay lightweight by default;
- stronger teacher models may be used for distillation or offline pseudo-labeling;
- fusion must preserve auditability;
- runtime cost is a first-class design constraint;
- L0 must not silently absorb heavy logic;
- L1 is the current main judgment layer;
- L2 remains reserved for high-risk, hard, open-world, and later robustness-oriented problems.

## 11. Current Data And Label Principles

### 11.1 Data Before Model Showmanship

At the current stage, the project values:

- reproducible data;
- stable label semantics;
- stable capture outputs;
- auditable backfill paths;
- shared upstream data contracts across training and inference.

### 11.2 Weak Labels Are Not Gold Labels

The project allows:

- auto backfill;
- rule-label application;
- offline weak-label generation;
- selective human correction.

The default project rule is still:

- do not treat auto labels as human gold labels;
- do not disguise heuristic judgments as final truth;
- do not let the Data module promote weak labels into a gold-label layer.

### 11.3 Brand Logic Is Supportive Evidence

Brand logic is supportive evidence inside Warden, not the whole decision basis.

The main question remains:
**is the webpage presenting meaningful social-engineering risk?**

Brand evidence is one form of high-risk deceptive-behavior evidence when it helps establish a false identity or trust context. It must still be interpreted with URL, page content, flow, authority context, and observed or missing payload evidence rather than used as a universal one-factor rule.

## 12. Execution Discipline

Warden is a real engineering project rather than a demo sandbox.

All non-trivial work should, by default:

1. read the relevant governing docs;
2. clarify the requirement;
3. freeze the task boundary;
4. make the smallest valid change;
5. run the smallest necessary validation;
6. report compatibility impact;
7. provide handoff;
8. return for review and acceptance.

For tasks that touch multiple modules, schema, labels, CLI, or public outputs:

- treat them as non-trivial by default;
- do not skip the task doc;
- do not skip the handoff;
- do not skip review;
- do not claim unrun validation as passed validation.

## 13. Current-Stage Completion Standard

At the current stage, a sub-area should be treated as "complete enough" only if it has:

- a clear project or module document;
- no conflict with frozen fields or upstream contracts;
- a defined input/output boundary;
- a minimum validation path;
- an explicit compatibility statement;
- enough handoff clarity for continuation in a fresh window.

In other words, the current-stage completion standard is first:
**reproducible, auditable, and handoff-ready**.
Not "looks advanced".

## 14. Near-Term Mainline Directions

The most reasonable near-term task directions include:

- continuing to accumulate and screen higher-quality samples;
- stabilizing TrainSet V1 related scripts and reports;
- improving labels and brand lexicons;
- freezing clearer vision and text module specifications;
- connecting lightweight training / evaluation / inference baselines;
- preserving stable engineering and data contracts for later paper framing.

## 15. What This File Does Not Define

This file does not directly define:

- the exact `scope_in` / `scope_out` of a concrete task;
- the implementation details of a specific script;
- a model-specific hyperparameter table;
- a task-level acceptance checklist;
- the validation results of a concrete delivery.

Those belong, respectively, in:

- a task document;
- module docs;
- config files;
- handoff;
- benchmark or evaluation docs.
