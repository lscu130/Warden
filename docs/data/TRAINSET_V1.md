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
