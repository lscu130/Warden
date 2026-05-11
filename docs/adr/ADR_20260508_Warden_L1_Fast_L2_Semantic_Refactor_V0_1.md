# ADR 2026-05-08: Warden L1-fast / L2-semantic Cascade Refactor V0.1

> Supersession status, 2026-05-11:
> This ADR is superseded and rejected for the default online Warden V1 architecture by `TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1`.
> It is retained only as historical research / ablation context.
> The current online architecture defines `L0` and `L1` only. It does not define current online `L2`, `L1-fast`, CLIP / MobileCLIP default routing, or SNet / SpecularNet-like default decision layers.

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分供人工快速阅读与任务交接。

> 2026-05-11 废止说明：
> 本 ADR 对默认在线 Warden V1 架构已被 `TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1` 废止并拒绝。
> 本文件仅保留为历史研究 / ablation 背景。
> 当前在线架构只定义 `L0` 和 `L1`，不定义当前在线 `L2`、`L1-fast`、CLIP / MobileCLIP 默认路由或 SNet / SpecularNet-like 默认决策层。

### 摘要

本 ADR 记录一个架构方向调整：保留 Warden 当前 `L0 / L1 / L2` 三层，不新增 L3；把此前讨论的“完整 L1”（文本塔多任务头 + OCR + YOLO + fusion + evidence ledger + explanation renderer）上移为 **L2-semantic full judgment**；新增一个更轻的 **L1-fast structural-visual triage/router**。

新的层级意图：

```text
L0 = 规则热路径 / cheap screening
L1-fast = 轻量结构 + 视觉先验路由层
L2-semantic = 完整语义裁决与解释层
```

L1-fast 不负责完整解释，也不负责最终复杂威胁归因。它只做低成本候选判断与路由：

- 使用 SpecularNet-like DOM/domain structural scorer 捕捉 phishing-kit / template / DOM 结构风险；
- 使用 CLIP / MobileCLIP 作为视觉场景先验和 OCR / YOLO / L2 的路由辅助；
- 使用 cheap structured features 做低成本补充；
- 输出 early benign candidate、structural malicious candidate、need L2、need OCR、need YOLO、need recrawl 等路由信号。

L2-semantic 承接此前完整 L1 设计，负责最终 `benign / malicious / suspicious / unknown` 判断、`malicious_basis`、`payload_observed`、风险轴、页面角色、证据账本和确定性解释。

本 ADR 是架构决策草案，不是实现任务，不改代码，不改 schema，不改 CLI，不冻结机器可读输出字段。

---

## 1. 背景

此前 Warden 已形成一份 `Warden_L1_FRAMEWORK_V0.1.md`，其中 L1 被定义为主判断层：文本 / HTML / URL / forms / network / structured signals 是主证据路径；文本塔学习结构化语义概念识别和关系判断；视觉路径是证据恢复和局部证据定位路径；OCR、YOLO、CLIP 职责分离；fusion 形成 L1 机器判断；解释由 evidence ledger 和 reason codes 确定性渲染。

经过进一步反审，当前“完整 L1”仍然偏重：它包含文本塔、多任务头、OCR、YOLO、fusion、解释器和复杂路由。对于 Warden 的级联架构，它更像一个深层语义裁决层，而不是轻量 L1。

同时，SpecularNet-like 结构模型提供了一个可作为前置层的方向：只依赖 domain + DOM/HTML structure，目标是低成本 CPU inference，适合在复杂语义层之前提供结构风险评分和路由信号。CLIP / MobileCLIP 也更适合做视觉场景先验和路由，而不是最终威胁分类器。

因此，本 ADR 提出将当前架构调整为更明确的倒三角级联：

```text
轻量规则
  ↓
轻量结构/视觉先验筛选与路由
  ↓
完整语义证据裁决与解释
```

---

## 2. 决策

### 2.1 保留三层命名，不新增 L3

Warden V0.1 继续采用：

```text
L0
L1
L2
```

不新增 L3，避免当前阶段系统复杂度继续膨胀。

### 2.2 重新定义 L1

L1 改为：

```text
L1-fast structural-visual triage/router
```

职责：

- 轻量结构风险判断；
- 视觉敏感场景路由；
- cheap structured signal 汇总；
- early benign candidate；
- structural malicious candidate；
- 决定是否进入 L2-semantic；
- 决定是否请求 L2 中 OCR / YOLO / recrawl。

L1 不负责：

- 完整社会工程语义判断；
- 完整高危行为 / 威胁动作归因；
- 完整 evidence ledger 解释；
- 最终复杂 malicious basis 输出；
- 生成自然语言解释。

### 2.3 将当前完整 L1 上移为 L2-semantic

原先完整 L1 设计改为：

```text
L2-semantic full judgment
```

职责：

- 文本塔多任务头；
- source-aware visible_text / OCR text / HTML actionable summary；
- URL/domain/forms/network/redirect 关系判断；
- YOLO 局部 UI 证据；
- OCR 截图文字证据；
- fusion；
- evidence ledger；
- reason codes；
- deterministic explanation renderer；
- 最终 `benign / malicious / suspicious / unknown` 判断。

---

## 3. 新级联结构

```text
L0 Rule Hot Path
  - adult / gambling / obvious gate / obvious bad capture
  - cheap URL/text/form/network flags
  - obvious allow/block/review candidates

        ↓

L1-fast Structural-Visual Triage
  - SpecularNet-like DOM/domain structural scorer
  - CLIP / MobileCLIP visual-prior router
  - cheap structured features
  - outputs:
      early_benign_candidate
      structural_malicious_candidate
      visual_sensitive_surface
      need_L2_semantic
      need_OCR
      need_YOLO
      need_recrawl
      low_applicability / insufficient_structure

        ↓

L2-semantic Full Judgment
  - text tower multi-task concept heads
  - source-aware visible_text / OCR text / HTML action summary
  - URL/domain/form/network relation judgment
  - YOLO localized UI evidence
  - OCR recovered screenshot text
  - fusion head
  - evidence ledger + deterministic explanation renderer
  - final label / basis / risk axes / page role / explanation
```

---

## 4. L1-fast 组件定义

### 4.1 SpecularNet-like structural scorer

输入候选：

```text
final_domain / host / eTLD+1
rendered DOM tree or captured HTML structure
HTML tag sequence
HTML attributes
basic DOM statistics
optional compact action-structure hints
```

输出候选：

```json
{
  "structural_applicability": "high | medium | low",
  "structural_phish_score": 0.0,
  "structural_confidence": 0.0,
  "structural_reason_codes": [
    "dom_template_like",
    "phishing_kit_structural_pattern",
    "sparse_or_abnormal_dom",
    "domain_dom_structural_mismatch"
  ]
}
```

关键约束：

- SpecularNet-like scorer 不能替代文本塔；
- 它不看完整 visible_text 语义，不看截图，不看 OCR，不看品牌官方性；
- 它对纯图片页、HTML 很少页、SPA 初始结构空页可能 `structural_applicability=low`；
- 低适用性不能当作 benign；
- 高分样本默认进入 L2-semantic 做最终裁决和解释。

### 4.2 CLIP / MobileCLIP visual-prior router

输入候选：

```text
screenshot_viewport.png
optional fixed crops
```

输出候选：

```json
{
  "visual_prior_applicability": "high | medium | low",
  "visual_scene": "content | login | wallet | payment | download | support | reward | finance | gate | brand_landing | unknown",
  "visual_sensitive_surface": "low | medium | high",
  "route_hints": [
    "need_ocr",
    "need_yolo",
    "need_l2_semantic"
  ]
}
```

关键约束：

- CLIP 不输出 final malicious / benign；
- CLIP 不负责品牌和 URL 是否官方匹配；
- CLIP 不负责 payload_observed 判断；
- CLIP 只提供页面级视觉先验、敏感场景提示和路由辅助；
- CLIP 高风险只代表“值得继续看”，不代表 confirmed malicious。

### 4.3 Cheap structured features

L1-fast 可使用轻量结构特征：

```text
visible_text_len
effective_visible_text_len
html_actionable_node_count
form_count
input_count
has_password
has_download_link
has_wallet_keyword
redirect_count
third_party_domain_count
hosted_platform_domain
brand_token_in_url
l0_flags
```

这些特征不能单独作为一条规则判恶意，应与结构评分、视觉先验和后续 L2 语义裁决配合使用。

---

## 5. L1-fast 输出与路由

### 5.1 Early benign candidate

仅当下列条件同时满足时，L1-fast 才能输出 early benign candidate：

```text
structural_phish_score low
structural_confidence sufficient
visual_sensitive_surface low
visible_text not sparse
HTML actionable structure not suspicious
no sensitive action surface
no strong brand/domain conflict
no L0 risk flag
no evidence conflict
```

输出示例：

```json
{
  "stage": "L1_fast",
  "decision": "early_benign_candidate",
  "confidence": 0.0,
  "route": "stop_or_optional_L2_sampled_audit"
}
```

注意：早停 benign 必须保守。L1-fast 低风险不应默认覆盖明显的文本 / URL / form / network 冲突。

### 5.2 Structural malicious candidate

如果 structural scorer 高置信认为 DOM/domain 结构符合 phishing-kit/template 风险，且 cheap structured features 也有支撑，则输出：

```json
{
  "stage": "L1_fast",
  "decision": "structural_malicious_candidate",
  "confidence": 0.0,
  "route": "L2_semantic_for_basis_and_explanation"
}
```

默认不直接作为最终恶意结论。L2-semantic 负责最终 basis、payload、行为/动作拆分和解释。

### 5.3 Need L2-semantic

进入 L2-semantic 的典型条件：

```text
SpecularNet-like structural score high
SpecularNet-like applicability low but page not clearly benign
CLIP sees login / wallet / payment / reward / download / support / gate / finance
visible_text < active threshold, e.g. around 300 effective chars
HTML actionable structure sparse
SPA / React / Vue extraction weak
sensitive action surface present
brand/domain or evidence conflict
text or structure confidence low
L0 possible gate/evasion/brand-surface conflict
```

L1-fast 可以同时请求：

```json
{
  "need_l2_semantic": true,
  "l2_requests": {
    "run_text_tower": true,
    "run_yolo": true,
    "run_ocr": true,
    "ocr_scope": "yolo_crops_or_viewport_regions",
    "need_recrawl": false
  }
}
```

---

## 6. L2-semantic 定义

L2-semantic 是完整裁决层，承接之前完整 L1 设计。

输入：

```text
visible_text
OCR recovered text
HTML actionable summary
URL/domain/redirect evidence
forms/network summary
L1-fast structural scores
L1-fast visual prior
YOLO localized evidence
joint signals
```

输出：

```text
final_label:
  benign | malicious | suspicious | unknown

malicious_basis:
  no_malicious_evidence_observed
  high_risk_behavior_observed
  high_risk_action_observed
  both_behavior_and_action_observed
  insufficient_evidence

other outputs:
  risk_score
  confidence
  payload_observed
  high_risk_behavior
  high_risk_action
  page_role
  risk_axes
  routing
  evidence ledger
  reason codes
  deterministic explanation
```

这些输出项在本 ADR 中仍为 conceptual / proposed terms，不冻结为机器可读 schema。

---

## 7. 为什么这样更合理

### 7.1 更符合级联触发

原设计中完整 L1 偏重，包含深语义、多模态证据恢复和解释。新设计把轻重分离：

```text
L1-fast = 轻量筛选 / 路由
L2-semantic = 重量裁决 / 解释
```

### 7.2 给 L2 找到了明确位置

此前 L2 定义不够清楚。现在 L2 不再是模糊的“更强模型”，而是原完整 L1 的语义裁决层。

### 7.3 CLIP 定位更稳

CLIP 不再被要求判断威胁，只负责视觉场景先验和路由。这符合其能力边界。

### 7.4 SpecularNet-like 模型填补结构筛选空位

SpecularNet-like 结构模型适合捕捉 phishing-kit / template / DOM structural risk，可作为 L2 之前的轻量候选层。

---

## 8. 风险与约束

### 8.1 SpecularNet 论文结果不能直接等同于 Warden 效果

SpecularNet 的威胁范围偏 classic phishing / phishing-kit。Warden 的目标是更宽的社会工程威胁。必须在 Warden 自有数据上复现和验证。

### 8.2 L1-fast 早停不能激进

如果 L1-fast 早停 benign 过宽，会漏掉图片型、SPA 型、文本稀疏型、品牌壳型和行为-only 威胁。

### 8.3 Structural scorer 可能误伤 benign hard negatives

正常登录页、SaaS、Web3、交易所、支付页、下载页也可能有类似结构。必须用 Tranco benign hard negative 验证 false positive。

### 8.4 CLIP 仍然是弱证据

CLIP 的 high sensitive surface 只表示“需要继续检查”，不能作为 malicious basis。

### 8.5 纯图片页仍需 L2 OCR/YOLO

SpecularNet-like structural scorer 对纯图片或 HTML 极少页面不适用。必须通过 CLIP / cheap evidence 路由到 L2 的 OCR / YOLO。

---

## 9. 实验与验收要求

本 ADR 不要求立刻实现。未来冻结前必须做 ablation：

```text
A. current full semantic path only
B. SpecularNet-like structural scorer only
C. CLIP router only
D. SpecularNet-like + CLIP router
E. L1-fast + L2-semantic cascade
```

关键评估 buckets：

```text
ordinary benign
benign hard negative
text-sparse login
text-sparse brand landing
pure image page
image-text page
SPA / React / Vue weak extraction
wallet / exchange
download / gate
reward / prize / fake support
behavior-only malicious
action-observed malicious
both behavior and action malicious
```

关键指标：

```text
early benign false negative rate
L1-fast route-to-L2 recall
structural malicious candidate precision
benign hard negative false positive rate
L2 load reduction
final L2 F1 / precision / recall
latency by hardware tier
OCR / YOLO trigger correctness
```

冻结条件：

```text
1. L1-fast 不能显著提高漏报风险；
2. L1-fast 能减少不必要的 L2 调用；
3. SpecularNet-like scorer 对 template / phishing-kit 样本有稳定增益；
4. CLIP router 对 OCR / YOLO / L2 路由有稳定增益；
5. benign hard negative FPR 可控；
6. 所有结果按 grouped split 或独立时间/来源测试集验证。
```

---

## 10. 对现有文档的影响建议

本 ADR 被接受后，后续 Codex 文档任务应：

```text
1. 新增本 ADR 到 docs/adr/ 或 docs/frozen/decision/。
2. 不直接删除 Warden_L1_FRAMEWORK_V0.1.md。
3. 新增一个 compatibility note：当前 L1 framework 可能升级为 L2-semantic full judgment。
4. 更新 PROJECT.md 中 L0/L1/L2 的概念摘要。
5. 更新 MODULE_INFER.md 中 L1 和 L2 的阶段职责。
6. 更新 Warden_VISION_PIPELINE_V1.md：CLIP 主要属于 L1-fast router，OCR/YOLO 主要在 L2 evidence recovery 中执行。
7. 明确本 ADR 不改 schema、CLI、runtime、训练逻辑。
```

---

## 11. 当前决策状态

```text
Status: Superseded / Rejected for default online Warden V1 path by TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1
Decision type: Architecture refactor proposal
Implementation status: Not implemented
Schema status: Not changed
Runtime status: Not changed
Training status: Not changed
```

本 ADR 只冻结一个设计方向：

```text
把 Warden 当前完整 L1 设计上移为 L2-semantic；
新增 L1-fast 作为 SpecularNet-like + CLIP-router + cheap structured features 的轻量结构/视觉先验路由层；
保持 Warden 只有 L0 / L1 / L2 三层，不新增 L3。
```

---

# English Version

> AI note: This English section is authoritative. The Chinese section is for human readers, collaboration, and quick orientation.

# ADR 2026-05-08: Warden L1-fast / L2-semantic Cascade Refactor V0.1

## Status

Proposed.

This ADR is an architecture proposal. It is not an implementation task, not a schema freeze, and not a runtime behavior change.

## Context

Warden previously defined `Warden_L1_FRAMEWORK_V0.1.md` as a main-judgment framework where:

- text / HTML / URL / forms / network / structured signals are the main evidence path;
- the text tower learns structured semantic concepts and relation judgments through multi-task heads;
- the visual path is evidence recovery and localization rather than an independent threat judge;
- OCR, YOLO, and CLIP / MobileCLIP have separated responsibilities;
- fusion produces the machine judgment;
- explanations are rendered deterministically from evidence ledger entries and reason codes.

After further counter-review, the previous full L1 design is still heavy for a first semantic stage. It includes semantic multi-task heads, OCR, YOLO, fusion, evidence ledger, and explanation rendering. In a staged cascade, that design fits better as a deeper full semantic adjudication stage.

At the same time, a SpecularNet-like structural model offers a plausible lightweight layer before full semantic judgment. SpecularNet is a reference-free phishing detector operating on domain name and DOM / HTML structure. It is designed for CPU-oriented inference and structural phishing-kit detection. CLIP / MobileCLIP also fits better as a visual-prior and routing module than as a final threat classifier.

This ADR therefore proposes a narrower cascade:

```text
L0 = rule hot path / cheap screening
L1-fast = lightweight structural + visual-prior triage/router
L2-semantic = full semantic judgment and explanation
```

Warden should not add L3 at this stage.

## Decision

### 1. Keep only L0 / L1 / L2

Warden V0.1 keeps the three-stage structure:

```text
L0
L1
L2
```

No L3 stage is introduced in this ADR.

### 2. Redefine L1 as L1-fast

L1 becomes:

```text
L1-fast structural-visual triage/router
```

L1-fast responsibilities:

- lightweight DOM/domain structural risk scoring;
- page-level visual-prior routing;
- cheap structured feature aggregation;
- early benign candidate identification;
- structural malicious candidate identification;
- routing to L2-semantic;
- requesting L2 OCR, YOLO, or recrawl where needed.

L1-fast must not be responsible for:

- complete social-engineering semantic adjudication;
- full high-risk behavior / threat-action attribution;
- final evidence-ledger explanation;
- final complex malicious basis output;
- free-form natural-language explanation.

### 3. Promote the previous full L1 design into L2-semantic

The previous full L1 design becomes:

```text
L2-semantic full judgment
```

L2-semantic responsibilities:

- text tower multi-task concept heads;
- source-aware visible text / OCR text / HTML actionable summary;
- URL / domain / forms / network / redirect relation judgments;
- YOLO localized UI evidence;
- OCR recovered screenshot text;
- fusion;
- evidence ledger;
- reason codes;
- deterministic explanation rendering;
- final `benign / malicious / suspicious / unknown` machine judgment.

## New Cascade

```text
L0 Rule Hot Path
  - adult / gambling / obvious gate / obvious bad capture
  - cheap URL/text/form/network flags
  - obvious allow/block/review candidates

        ↓

L1-fast Structural-Visual Triage
  - SpecularNet-like DOM/domain structural scorer
  - CLIP / MobileCLIP visual-prior router
  - cheap structured features
  - outputs:
      early_benign_candidate
      structural_malicious_candidate
      visual_sensitive_surface
      need_L2_semantic
      need_OCR
      need_YOLO
      need_recrawl
      low_applicability / insufficient_structure

        ↓

L2-semantic Full Judgment
  - text tower multi-task concept heads
  - source-aware visible_text / OCR text / HTML action summary
  - URL/domain/form/network relation judgment
  - YOLO localized UI evidence
  - OCR recovered screenshot text
  - fusion head
  - evidence ledger + deterministic explanation renderer
  - final label / basis / risk axes / page role / explanation
```

## L1-fast Components

### SpecularNet-like structural scorer

Candidate inputs:

```text
final_domain / host / eTLD+1
rendered DOM tree or captured HTML structure
HTML tag sequence
HTML attributes
basic DOM statistics
optional compact action-structure hints
```

Candidate outputs:

```json
{
  "structural_applicability": "high | medium | low",
  "structural_phish_score": 0.0,
  "structural_confidence": 0.0,
  "structural_reason_codes": [
    "dom_template_like",
    "phishing_kit_structural_pattern",
    "sparse_or_abnormal_dom",
    "domain_dom_structural_mismatch"
  ]
}
```

Constraints:

- The structural scorer does not replace the semantic text tower.
- It does not inspect full visible-text semantics, screenshots, OCR, or brand officiality.
- It may have low applicability on pure-image pages, sparse HTML pages, and weak SPA extraction pages.
- Low applicability must not be treated as benign.
- High structural risk should usually route to L2-semantic for final basis and explanation.

### CLIP / MobileCLIP visual-prior router

Candidate inputs:

```text
screenshot_viewport.png
optional fixed crops
```

Candidate outputs:

```json
{
  "visual_prior_applicability": "high | medium | low",
  "visual_scene": "content | login | wallet | payment | download | support | reward | finance | gate | brand_landing | unknown",
  "visual_sensitive_surface": "low | medium | high",
  "route_hints": [
    "need_ocr",
    "need_yolo",
    "need_l2_semantic"
  ]
}
```

Constraints:

- CLIP must not output final malicious / benign.
- CLIP must not determine brand-domain officiality.
- CLIP must not determine `payload_observed`.
- CLIP only provides page-level visual prior, sensitive-scene hints, and routing assistance.
- High visual risk means “inspect further,” not confirmed malicious.

### Cheap structured features

L1-fast may consume cheap structured signals such as:

```text
visible_text_len
effective_visible_text_len
html_actionable_node_count
form_count
input_count
has_password
has_download_link
has_wallet_keyword
redirect_count
third_party_domain_count
hosted_platform_domain
brand_token_in_url
l0_flags
```

These features must not become one-factor malicious rules.

## L1-fast Outputs And Routing

### Early benign candidate

L1-fast may produce an early benign candidate only when all of the following hold:

```text
structural_phish_score is low
structural_confidence is sufficient
visual_sensitive_surface is low
visible_text is not sparse
HTML actionable structure is not suspicious
no sensitive action surface exists
no strong brand/domain conflict exists
no L0 risk flag exists
no evidence conflict exists
```

Example:

```json
{
  "stage": "L1_fast",
  "decision": "early_benign_candidate",
  "confidence": 0.0,
  "route": "stop_or_optional_L2_sampled_audit"
}
```

Early benign must be conservative.

### Structural malicious candidate

When the structural scorer reports high-confidence phishing-kit or template-like risk and cheap structured features support it, L1-fast may output:

```json
{
  "stage": "L1_fast",
  "decision": "structural_malicious_candidate",
  "confidence": 0.0,
  "route": "L2_semantic_for_basis_and_explanation"
}
```

This should not become the default final malicious verdict before Warden-specific validation.

### Need L2-semantic

Typical L2-semantic routing conditions:

```text
SpecularNet-like structural score is high
SpecularNet-like applicability is low and the page is not clearly benign
CLIP sees login / wallet / payment / reward / download / support / gate / finance
visible_text is below the active threshold, e.g. around 300 effective characters
HTML actionable structure is sparse
SPA / React / Vue extraction is weak
sensitive action surface is present
brand/domain or evidence conflict exists
text or structure confidence is low
L0 marks possible gate / evasion / brand-surface conflict
```

Example L2 request:

```json
{
  "need_l2_semantic": true,
  "l2_requests": {
    "run_text_tower": true,
    "run_yolo": true,
    "run_ocr": true,
    "ocr_scope": "yolo_crops_or_viewport_regions",
    "need_recrawl": false
  }
}
```

## L2-semantic Definition

L2-semantic consumes:

```text
visible_text
OCR recovered text
HTML actionable summary
URL/domain/redirect evidence
forms/network summary
L1-fast structural scores
L1-fast visual prior
YOLO localized evidence
joint signals
```

L2-semantic produces conceptual outputs such as:

```text
final_label:
  benign | malicious | suspicious | unknown

malicious_basis:
  no_malicious_evidence_observed
  high_risk_behavior_observed
  high_risk_action_observed
  both_behavior_and_action_observed
  insufficient_evidence

other outputs:
  risk_score
  confidence
  payload_observed
  high_risk_behavior
  high_risk_action
  page_role
  risk_axes
  routing
  evidence ledger
  reason codes
  deterministic explanation
```

These names are conceptual / proposed terms in this ADR. They are not frozen machine-readable schema fields.

## Rationale

### Better staged cascade

The previous full L1 was heavy. The proposed split makes the cascade more coherent:

```text
L1-fast = lightweight screening and routing
L2-semantic = heavier semantic judgment and explanation
```

### Clearer L2 purpose

Previously, L2 had no stable role. In this proposal, L2 becomes the full semantic adjudication stage.

### Safer CLIP role

CLIP no longer has to judge maliciousness. It acts as a visual-prior router.

### SpecularNet-like scorer fills the structural gap

A SpecularNet-like structural scorer can cover DOM/template/phishing-kit risk before the semantic layer.

## Risks

### SpecularNet paper results do not directly transfer to Warden

SpecularNet is evaluated mainly under classic phishing / phishing-kit conditions. Warden targets broader social-engineering threats. Warden-owned validation is required.

### L1-fast early benign can cause false negatives

Early benign must be conservative and should not override evidence conflict.

### Structural scorer may hurt benign hard negatives

Normal login, SaaS, Web3, exchange, payment, and download pages can share structural features with malicious pages.

### CLIP remains weak evidence

High CLIP visual risk should route to inspection. It must not become malicious basis.

### Pure-image pages still require L2 OCR / YOLO

The structural scorer has low applicability when DOM/HTML evidence is absent.

## Required Future Evaluation

Before implementation freeze, run ablations:

```text
A. current full semantic path only
B. SpecularNet-like structural scorer only
C. CLIP router only
D. SpecularNet-like + CLIP router
E. L1-fast + L2-semantic cascade
```

Required buckets:

```text
ordinary benign
benign hard negative
text-sparse login
text-sparse brand landing
pure image page
image-text page
SPA / React / Vue weak extraction
wallet / exchange
download / gate
reward / prize / fake support
behavior-only malicious
action-observed malicious
both behavior and action malicious
```

Required metrics:

```text
early benign false negative rate
L1-fast route-to-L2 recall
structural malicious candidate precision
benign hard negative false positive rate
L2 load reduction
final L2 F1 / precision / recall
latency by hardware tier
OCR / YOLO trigger correctness
```

## Documentation Impact If Accepted

If this ADR is accepted, a later documentation task should:

```text
1. Add this ADR under docs/adr/ or docs/frozen/decision/.
2. Keep Warden_L1_FRAMEWORK_V0.1.md; do not delete it immediately.
3. Add a compatibility note that the current L1 framework may become L2-semantic full judgment.
4. Update PROJECT.md with the revised L0/L1/L2 summary.
5. Update MODULE_INFER.md with revised stage responsibilities.
6. Update Warden_VISION_PIPELINE_V1.md so CLIP primarily belongs to L1-fast routing, while OCR/YOLO are primarily executed under L2 evidence recovery.
7. State explicitly that this ADR does not change schema, CLI, runtime, or training logic.
```

## Current Decision State

```text
Status: Proposed
Decision type: Architecture refactor proposal
Implementation status: Not implemented
Schema status: Not changed
Runtime status: Not changed
Training status: Not changed
```

This ADR proposes the following direction:

```text
Promote Warden's current full L1 framework into L2-semantic.
Introduce L1-fast as a lightweight structural/visual-prior router using a SpecularNet-like scorer, CLIP-router, and cheap structured features.
Keep Warden limited to L0 / L1 / L2 for now.
```
