# TRAINSET_V1.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden TrainSet V1 Specification

This document defines the admission criteria, exclusion rules, manifest rules, and split baseline for Warden TrainSet V1.

It does not define model architecture, loss design, or inference thresholds. It answers a narrower set of questions:

1. Which captured samples may enter the training set.
2. Which files are the minimum dependency set.
3. Which files are recommended enhancements rather than primary requirements.
4. How the manifest should express sample usability for text, vision, and multimodal baselines.
5. How later text / vision / multimodal training can share the same upstream dataset contract.

## 1. Purpose

TrainSet V1 exists to define a stable dataset baseline for training-oriented consumption of Warden capture outputs.

Its job is to freeze:

- what counts as an admissible sample;
- what the primary dependency set is;
- what a manifest must record;
- how downstream training subsets are derived.

## 2. Upstream Baseline

TrainSet V1 is built strictly on top of the frozen capture-output contract.

That means:

- current script outputs are the upstream truth;
- successful sample directory structure follows the frozen spec;
- model changes must not silently rewrite upstream data fields;
- training convenience must not silently change the sample layout.

If the frozen capture specification changes, this TrainSet spec should be revised explicitly.

## 3. Data Source Scope

The allowed TrainSet V1 source pool consists of:

- successful sample directories produced by the current capture pipeline;
- label artifacts supplemented by later offline backfill;
- optional manual labels as an enhancement layer rather than a mandatory precondition.

The intended script chain is aligned with the current capture and backfill pipeline, including the capture script, the dataset backfill script, and the shared brand-lexicon labeling utilities.

## 4. Sample Admission Principles

### 4.1 Only Successful Sample Directories Are Considered

Under the current capture rules, failed or obviously unusable samples do not become successful sample directories. Therefore, TrainSet V1 starts from successful sample directories only.

### 4.2 Not Every Enhancement Artifact Is Required

TrainSet V1 is a primary training set, not a full forensic archive.

Therefore it does not require the following to exist:

- `rule_labels.json`
- `manual_labels.json`
- `actions.jsonl`
- `after_action/`
- `variants/`
- `diff_summary.json`
- `network.har`

### 4.3 The Sample Directory Must Remain Intact

TrainSet construction should:

- scan samples;
- read their information;
- generate a manifest;
- generate splits.

It should not rewrite the sample directory, rename upstream fields, or mutate the source capture artifacts.

## 5. Required Files For TrainSet V1

A sample must have at least the following files to enter TrainSet V1:

- `meta.json`
- `url.json`
- `env.json`
- `redirect_chain.json`
- `screenshot_viewport.png`
- `net_summary.json`
- `auto_labels.json`

Together these files provide minimum metadata, visual input, network summary, and weak-label coverage for a trainable sample.

If any of them are missing, the sample should be excluded from the TrainSet V1 primary set.

## 6. Strongly Recommended Files

The following files are not absolute requirements, but they are strongly recommended:

- `visible_text.txt`
- `forms.json`
- `html_rendered.html`

Why they matter:

- the text tower depends on `visible_text.txt`;
- form-structure features depend on `forms.json`;
- HTML fallback and additional parsing often depend on `html_rendered.html`.

If they are missing, the sample may still remain in the overall manifest, but the usability fields should reflect the limitation so downstream training can filter appropriately.

## 7. Optional Enhancement Files

The following files may exist, but they are not primary TrainSet V1 dependencies:

- `html_raw.html`
- `screenshot_full.png`
- `rule_labels.json`
- `manual_labels.json`

Their intended roles are:

- `html_raw.html` for supplemental analysis;
- `screenshot_full.png` for later visual experiments beyond the first baseline;
- `rule_labels.json` as a unified offline backfill artifact;
- `manual_labels.json` as an enhancement source for high-quality subsets or later evaluation.

If `rule_labels.json` contains `threat_taxonomy_v1`, that namespace should be treated as a long-lived active weak-label output, not a disposable temporary experiment field.

## 8. Files That Are Not Primary Training Dependencies

The following should not be part of the TrainSet V1 primary dependency set:

- `network.har`
- `actions.jsonl`
- `after_action/`
- `variants/`
- `diff_summary.json`

They remain useful for:

- hard-case diagnosis;
- cloaking and evasion analysis;
- interaction-heavy page studies;
- L2 research;
- case studies.

### 8.1 Boundary With The Gate / Evasion Auxiliary Set

The auxiliary protocol for gate / evasion samples is defined separately in `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`.

That auxiliary set:

- does not replace TrainSet V1;
- does not expand primary admission by default;
- does not change the core meaning of the primary manifest.

The default manifest path remains focused on TrainSet V1 primary samples.

## 9. Label-Layer Policy

### 9.1 Default Label Layer

TrainSet V1 uses `auto_labels.json` as the default weak-label source.

### 9.2 Policy For `rule_labels.json`

`rule_labels.json` is not required during online capture.

The recommended path is:

1. capture the main data under the frozen spec;
2. run offline backfill over the full successful corpus;
3. emit `rule_labels.json` in a unified way.

This avoids inconsistent coverage where new samples have rule labels but older samples do not.

If `rule_labels.json` contains `threat_taxonomy_v1`, the current boundary is:

- it is an active weak-label namespace aligned with Warden's multi-threat problem definition;
- it may remain long-lived and improve through unified offline backfill;
- it does not automatically become the TrainSet V1 human gold-label layer;
- the primary manifest does not need to inline this namespace by default.

### 9.3 Policy For `manual_labels.json`

`manual_labels.json` is not a default prerequisite for TrainSet V1.

If present, it may support:

- high-quality validation subsets;
- smaller manually reviewed subsets;
- later weak-supervision correction or hard-case analysis.

It should not block production of the main training set.

## 10. Manifest Rules

TrainSet V1 should not be consumed by raw directory traversal alone. It should first be materialized into a unified manifest.

The recommended format is:

- `manifest.jsonl`

That format is preferred because it keeps one sample per line, supports streaming reads, supports later filtering for text / vision / multimodal subsets, and scales better for larger corpora and compressed storage.

## 11. Minimum Manifest Fields

Each sample record should include at least:

- `sample_id`
- `sample_dir`
- `label_hint`
- `crawl_time_utc`
- `http_status`
- `input_url`
- `final_url`

File-presence fields:

- `has_visible_text`
- `has_forms`
- `has_html_rendered`
- `has_html_raw`
- `has_screenshot_full`
- `has_rule_labels`
- `has_manual_labels`

Training-usability fields:

- `usable_for_text`
- `usable_for_vision`
- `usable_for_multimodal`

Optional enhancement fields:

- `page_stage_candidate`
- `risk_level_weak`
- `review_priority`
- `domain_etld1`
- `split`

## 12. Usability Rules

### 12.1 `usable_for_text`

The default value should be `true` only when:

- required files are complete;
- `visible_text.txt` exists;
- text reading succeeded.

### 12.2 `usable_for_vision`

The default value should be `true` only when:

- required files are complete;
- `screenshot_viewport.png` exists.

### 12.3 `usable_for_multimodal`

The default value should be `true` only when:

- `usable_for_text == true`;
- `usable_for_vision == true`;
- `forms.json` exists.

The first multimodal baseline does not need to require `screenshot_full.png`.

## 13. Exclusion Conditions

The following should exclude a sample from the TrainSet V1 primary manifest by default:

- missing required files;
- unreadable `meta.json` or `url.json`;
- an obvious mismatch between `sample_id` and the directory name;
- missing or corrupted `auto_labels.json`;
- missing or corrupted `net_summary.json`;
- missing viewport screenshot.

The following should not force exclusion, but should be reflected in manifest flags:

- missing `visible_text.txt`;
- missing `forms.json`;
- missing `html_rendered.html`;
- missing `rule_labels.json`;
- missing `manual_labels.json`.

## 14. Split Principles

Splits should be created only after the full manifest is generated.

The split design should ensure:

- clear `train / val / test` separation;
- leakage control for same-source or near-duplicate samples;
- no silent sample dropping before split accounting;
- reproducible split rules.

The recommended order is:

1. generate a full `manifest.jsonl`;
2. use a separate split script to derive:
   - `train_manifest.jsonl`
   - `val_manifest.jsonl`
   - `test_manifest.jsonl`

## 15. Relationship To Model Choice

TrainSet V1 is intentionally decoupled from any specific backbone.

Backbone changes such as:

- TinyBERT versus DistilBERT;
- MobileNetV3-Small versus MobileNetV4;
- later student / teacher / distillation strategies

should not change the upstream TrainSet V1 data contract.

Model changes may affect:

- which fields are read;
- which subset filters are applied;
- which modalities are enabled.

They should not change the frozen TrainSet baseline itself.

## 16. Recommended Current Workflow

The current recommended workflow is:

1. keep capturing data under the frozen output contract;
2. run unified offline backfill;
3. run `build_manifest.py` to generate `manifest.jsonl`;
4. run `check_dataset_consistency.py` for consistency checking;
5. generate splits;
6. start text / vision / multimodal baseline training.

## 17. Definition Of Done

TrainSet V1 can be considered defined when:

- admission rules are explicit;
- exclusion rules are explicit;
- required files are explicit;
- optional enhancement files are explicit;
- manifest fields are explicit;
- split principles are explicit;
- the boundary with model choice is explicit;
- the spec does not conflict with the frozen capture contract.

### Original Chinese Source

The original Chinese source text is kept below for human readers and traceability.

# TRAINSET_V1.md

# Warden TrainSet V1 Specification

版本：v1.0-draft  
状态：草案（Draft）  
适用阶段：Warden 第一阶段训练集定稿与训练通路打通  
上游冻结依据：`EVT Dataset Output Frozen Spec v1.1` :contentReference[oaicite:1]{index=1}

---

## 1. 目的

本文件用于定义 **Warden TrainSet V1** 的纳入标准、排除标准、目录读取基线、manifest 规则与后续 split 基线。

本文件不负责定义模型结构，不负责定义 loss，不负责定义推理阈值。
本文件只负责回答以下问题：

1. 什么样本可以进入训练集；
2. 训练集最少依赖哪些文件；
3. 哪些文件是增强项，哪些不是主训练依赖；
4. manifest 应该如何表达样本可用性；
5. 后续 text / vision / multimodal 基线如何共用同一份训练集清单。

---

## 2. 上游基线

TrainSet V1 严格建立在当前冻结数据结构之上。

即：

- 以当前脚本真实落盘为准
- 成功样本目录结构以冻结规范为准
- 不因为模型变化而修改上游冻结字段
- 不因为训练便利而偷偷改数据目录结构

若冻结规范升级，则本文件应显式升版本或修订。

---

## 3. 数据来源范围

TrainSet V1 的来源是：

- 当前抓取脚本产生的成功样本目录
- 后续离线补标脚本补齐后的标签文件
- 人工标注文件（若存在）仅作为增强层，不作为默认前置条件

适用脚本链路：

- `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `Warden_dataset_backfill_labels_brandlex.py`
- `Warden_auto_label_utils_brandlex.py`

---

## 4. 样本纳入原则

### 4.1 只纳入成功样本目录

由于当前采集规则中，失败 / 不可访问 / 状态码不允许 / 明显拦截页 / 截图质量失败样本不会创建成功样本目录，因此 TrainSet V1 默认只从成功样本目录中筛选。:contentReference[oaicite:2]{index=2}

### 4.2 不要求所有增强文件都存在

TrainSet V1 是“主训练集”，不是“全功能取证集”。

因此不要求以下增强文件必须存在：

- `rule_labels.json`
- `manual_labels.json`
- `actions.jsonl`
- `after_action/`
- `variants/`
- `diff_summary.json`
- `network.har`

### 4.3 必须保持目录原样

TrainSet V1 的构建方式是：

- 扫描样本
- 读取信息
- 生成 manifest
- 生成 split

不修改样本目录本体，不重写上游文件，不重命名字段。

---

## 5. TrainSet V1 必须文件

一个样本要进入 TrainSet V1，必须至少具备以下文件：

- `meta.json`
- `url.json`
- `env.json`
- `redirect_chain.json`
- `screenshot_viewport.png`
- `net_summary.json`
- `auto_labels.json`

说明：

- 这些文件共同构成最小可训练样本的基础元信息、视觉输入、网络摘要与弱标签层。
- 若上述任一文件缺失，则该样本默认不进入 TrainSet V1 主清单。

---

## 6. TrainSet V1 强烈建议文件

以下文件不是绝对必需，但强烈建议存在：

- `visible_text.txt`
- `forms.json`
- `html_rendered.html`

原因：

- 文本塔依赖 `visible_text.txt`
- 表单结构特征依赖 `forms.json`
- HTML 补充解析与部分文本回退分析依赖 `html_rendered.html`

若它们缺失，样本仍可进入总 manifest，但应在可用性字段中明确标记，供 text / multimodal 训练时过滤。

---

## 7. 可选增强文件

以下文件可存在，但不作为 TrainSet V1 主依赖：

- `html_raw.html`
- `screenshot_full.png`
- `rule_labels.json`
- `manual_labels.json`

说明：

- `html_raw.html` 可用于补充分析，但不是主读取依赖
- `screenshot_full.png` 可用于后续增强视觉实验，但首版视觉基线不强依赖
- `rule_labels.json` 建议通过后续统一离线 backfill 补齐
- 若 `rule_labels.json` 含 `threat_taxonomy_v1`，应视为长期保留的活跃弱标签输出，而不是临时实验字段
- `manual_labels.json` 若存在，可作为后续高质量子集或 eval 集增强来源

---

## 8. 不纳入主训练依赖的文件

以下内容不应作为 TrainSet V1 主训练依赖：

- `network.har`
- `actions.jsonl`
- `after_action/`
- `variants/`
- `diff_summary.json`

这些内容可用于：

- hard case 诊断
- cloaking 研究
- 交互式页面研究
- L2 难例分析
- case study

但不应成为 TrainSet V1 基线训练的前置要求。

### 8.1 与 gate / evasion auxiliary set 的边界

gate / evasion 类样本的辅助协议由 `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md` 单独定义。  
该集合不替代 TrainSet V1，不扩大 TrainSet V1 primary 的默认 admission，也不改变当前 primary manifest 的核心语义。  
当前 `build_manifest.py` 的默认行为仍仅面向 TrainSet V1 primary。

---

## 9. 标签层策略

### 9.1 默认标签层

TrainSet V1 默认使用：

- `auto_labels.json`

作为弱标签层来源。

### 9.2 `rule_labels.json` 策略

`rule_labels.json` 不要求在线抓取阶段默认存在。  
建议做法是：

1. 先按当前冻结生产档采集主数据；
2. 对全量成功样本统一运行离线 backfill；
3. 用 `--emit-rule-labels` 补齐 `rule_labels.json`。

这样可以避免“旧样本没有、新样本有”的不一致。

若 `rule_labels.json` 中存在 `threat_taxonomy_v1`，当前默认边界是：

- 它是 Warden 多威胁主问题定义对应的活跃弱标签命名空间
- 它可以长期保留并持续通过统一离线 backfill 提高覆盖率
- 它不直接提升为 TrainSet V1 primary 的默认金标
- 当前 primary manifest 核心字段不默认展开写入该命名空间

### 9.3 `manual_labels.json` 策略

`manual_labels.json` 不是 TrainSet V1 默认前置条件。  
若存在：

- 可用于构建高质量验证集 / 小规模精标集
- 可作为后续弱监督修正或 hard-case 分析来源

但不应阻塞主训练集生产。

---

## 10. TrainSet V1 Manifest 规则

TrainSet V1 不直接靠目录遍历训练，必须先生成统一 manifest。

manifest 推荐格式：

- `manifest.jsonl`

推荐原因：

- 每行一个样本对象
- 便于流式读取与后续拼接
- 便于按条件筛选 text / vision / multimodal 子集
- 便于大规模样本处理与后续压缩存储 `.jsonl.gz` :contentReference[oaicite:3]{index=3}

---

## 11. Manifest 最小字段

每个样本至少应记录以下字段：

- `sample_id`
- `sample_dir`
- `label_hint`
- `crawl_time_utc`
- `http_status`
- `input_url`
- `final_url`

文件存在性字段：

- `has_visible_text`
- `has_forms`
- `has_html_rendered`
- `has_html_raw`
- `has_screenshot_full`
- `has_rule_labels`
- `has_manual_labels`

训练可用性字段：

- `usable_for_text`
- `usable_for_vision`
- `usable_for_multimodal`

可选增强字段：

- `page_stage_candidate`
- `risk_level_weak`
- `review_priority`
- `domain_etld1`
- `split`

---

## 12. 可用性判定规则

### 12.1 `usable_for_text`

默认判定为 true 的条件：

- 必须文件完整
- `visible_text.txt` 存在
- 文本读取成功

### 12.2 `usable_for_vision`

默认判定为 true 的条件：

- 必须文件完整
- `screenshot_viewport.png` 存在

### 12.3 `usable_for_multimodal`

默认判定为 true 的条件：

- `usable_for_text == true`
- `usable_for_vision == true`
- `forms.json` 存在

说明：
multimodal 首版不强制要求 `screenshot_full.png`。

---

## 13. 排除条件

以下样本默认排除出 TrainSet V1 主清单：

- 必须文件缺失
- `meta.json` 或 `url.json` 无法解析
- `sample_id` 与目录名明显不一致
- `auto_labels.json` 缺失或损坏
- `net_summary.json` 缺失或损坏
- 首屏截图缺失

以下样本不直接排除，但需在 manifest 标记：

- 无 `visible_text.txt`
- 无 `forms.json`
- 无 `html_rendered.html`
- 无 `rule_labels.json`
- 无 `manual_labels.json`

---

## 14. Split 原则

TrainSet V1 在 manifest 完成后再做 split。

split 设计要求：

- train / val / test 分离
- 尽量避免同源或近重复泄漏
- 不在 split 前偷偷丢弃样本而不记录
- split 规则必须可复现

当前建议：

- 先生成全量 `manifest.jsonl`
- 再通过单独脚本生成：
  - `train_manifest.jsonl`
  - `val_manifest.jsonl`
  - `test_manifest.jsonl`

---

## 15. 与模型选择的关系

TrainSet V1 与具体 backbone 解耦。

即：

- TinyBERT / DistilBERT
- MobileNetV3-Small / MobileNetV4
- 后续 student / teacher / distillation 方案

都不改变 TrainSet V1 的上游数据契约。

模型变化只会影响：

- 哪些字段会被读取
- 哪些样本子集会被筛选
- 哪些模态会被启用

不会改变 TrainSet V1 的冻结基线。

---

## 16. 当前阶段建议工作流

1. 继续按当前冻结生产档采集主数据
2. 统一运行离线 backfill
3. 运行 `build_manifest.py` 生成 `manifest.jsonl`
4. 运行 `check_dataset_consistency.py` 做数据一致性检查
5. 生成 split
6. 再做 text / vision / multimodal 基线训练

---

## 17. Definition of Done

TrainSet V1 定稿的完成条件：

- 纳入标准明确
- 排除标准明确
- 必须文件明确
- 可选增强文件明确
- manifest 字段明确
- split 原则明确
- 与模型选择的边界明确
- 与冻结规范不冲突
