# Warden_RULE_LABEL_POLICY_V1_CORE.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于冻结 **Warden `rule_labels.json` 的 v1-core 框架**。
- 当前目标不是一次性定义全部长尾威胁子类，而是先稳定 **护栏、冲突、页面角色、升级提示** 这四类核心规则层。
- 本文档不定义 `manual_labels.json` 的最终人工金标语义，也不重写 `auto_labels.json` 的既有字段。
- 若涉及精确字段名、枚举、边界或演进规则，以英文版为准。
- 当前 repo 活跃版本为 `Warden_RULE_LABEL_POLICY_V1_CORE.md`，并以 `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md` 为对齐锚点；不再并行保留独立 `_ALIGNED` 活跃副本。

# Warden Rule Label Policy V1 Core

## 1. 文档目的

本文件用于冻结 `rule_labels.json` 的 **第一阶段核心框架**，解决以下问题：

1. `auto_labels.json` 只能表达“观察到什么”，但不足以稳定表达“该如何处理”。
2. 当前已出现 hard negative / hard positive 误差模式，需要统一的规则层来承载：
   - 误报护栏
   - 证据冲突
   - 页面角色候选
   - 升级与复核提示
3. `rule_labels.json` 需要先有稳定骨架，后续才能统一离线 backfill，而不是在数据收集后期一边补历史样本、一边继续改 schema。

本文件冻结的是 **`rule_label v1-core`**，而不是最终全量威胁本体。
当前 repo 内以本文件作为 `rule` 层活跃版本；本次对齐继续保留稳定文件名，并把 shared threat/scenario/page-role family 与 `manual` 明确对齐。

## 2. 定位与边界

### 2.1 `rule_labels.json` 的定位

`rule_labels.json` 是：

- 建立在 `auto_labels.json` 与冻结上游工件之上的 **规则派生层**；
- 面向 **处理动作、升级提示、冲突表达、页面角色候选** 的弱标签层；
- 服务于：
  - L1 的更稳判断
  - L2 的升级路由
  - 人工复核队列
  - 后续错误分析与标签治理

它不是：

- 人工金标层；
- 最终真值层；
- 可以替代 `manual_labels.json` 的最终裁决层。

### 2.2 与 `auto_labels.json` 的区别

- `auto_labels.json` 回答：**页面里观察到了什么**。
- `rule_labels.json` 回答：**这些观察组合起来，更像什么、该怎么处理**。

默认理解：

- `auto` = evidence-first weak layer
- `rule` = decision-support weak layer
- `manual` = final adjudication layer

### 2.3 与 `manual_labels.json` 的区别

`manual_labels.json` 负责：

- 最终裁决
- 最终高风险动作类
- 最终页面角色
- 最终品牌伪装认定
- 最终是否纳入训练 / 评估 / auxiliary

`rule_labels.json` 不负责这些最终裁决，只负责 **候选、护栏、冲突、优先级、升级提示**。

## 3. 设计原则

### 3.1 先冻结骨架，不追求一次定全

当前只冻结以下四类核心字段：

1. `guardrail_*`：误报护栏
2. `conflict_*`：证据冲突
3. `page_role_hint`：页面角色候选
4. `routing / review`：升级与复核提示

长尾场景、超细行业子类、复杂 narrative taxonomy 后续再扩，不在 v1-core 一次性写死。

### 3.2 `rule` 不能只是 `auto` 的重命名版

禁止把以下做法当成有效 rule：

- 仅把 `risk_level_weak` 映射成 `review_priority`
- 仅把 `claimed_brands` 改写成 `primary_threat_label_candidate`
- 仅根据 `auto` 总分二次包装，而不看证据结构

有效的 rule 必须体现：

- 冲突
- 护栏
- 页面角色
- 升级路由

### 3.3 `rule` 应允许“压误报”和“升高风险”同时存在

`rule_labels.json` 既要能：

- 压住 benign third-party auth / OAuth / trusted platform 的误报

也要能：

- 把 hosted lure / intermediary carrier / off-page attack chain 从低分样本中捞出来

### 3.4 默认通过脚本统一离线 backfill 产出

`rule_labels.json` 的默认生产路径应为：

1. 按冻结采集规范产生主样本目录；
2. 离线批量回读冻结工件与 `auto_labels.json`；
3. 统一生成 `rule_labels.json`。

不建议在人工逐条处理时手工编写 rule 文件。

## 4. 输入来源

`rule_labels.json` 的生成允许读取：

- `auto_labels.json`
- `meta.json`
- `url.json`
- `forms.json`
- `net_summary.json`
- `visible_text.txt`
- `html_rendered.json`
- `html_raw.json`（必要时回退）
- `diff_summary.json`（若存在）

因此，`rule` 不应被理解为“只吃 `auto.risk_score_weak` 的二次包装层”。

## 5. v1-core 顶层结构

推荐冻结为：

```json
{
  "schema_version": "warden_rule_v1_core",
  "generated_at_utc": "2026-03-26T00:00:00Z",
  "source": "offline_rule_backfill",
  "rule_flags": {
    "guardrail_trusted_idp_flow_candidate": false,
    "guardrail_third_party_auth_delegate_candidate": false,
    "guardrail_brand_surface_not_equal_brand_spoof_candidate": false,
    "guardrail_sensitive_collection_absent_on_page_candidate": false,

    "hosted_lure_candidate": false,
    "intermediary_platform_page_candidate": false,
    "offpage_attack_chain_candidate": false,
    "gate_or_evasion_candidate": false,
    "download_lure_candidate": false,

    "conflict_brand_high_but_spoof_not_established": false,
    "conflict_sensitive_intent_low_but_lure_signal_high": false,
    "conflict_visual_risk_high_text_risk_low": false,
    "conflict_hosted_platform_and_attack_chain_signal": false,

    "needs_l2_candidate": false,
    "needs_manual_review_candidate": false,
    "hard_negative_candidate": false,
    "hard_positive_candidate": false
  },
  "page_role_hint": "other",
  "review_priority": "p3",
  "rule_reasons": ["..."],
  "threat_taxonomy_v1": {
    "primary_threat_label_candidate": "uncertain",
    "primary_threat_label_confidence": 0.0,
    "primary_threat_label_rules": [],
    "scenario_label_candidate": "other",
    "scenario_label_confidence": 0.0,
    "scenario_label_rules": [],
    "narrative_tags_candidate": [],
    "evidence_tags_candidate": [],
    "evasion_tags_candidate": [],
    "ecosystem_tags_candidate": [],
    "taxonomy_source": "rule_derived_from_auto_and_frozen_artifacts",
    "taxonomy_review_status": "weak_candidate_only"
  }
}
```

说明：

- `threat_taxonomy_v1` 当前保留为长期活跃弱标签命名空间；
- 但 v1-core 不要求现在扩充所有长尾 taxonomy 枚举；
- v1-core 的重点是 `rule_flags + page_role_hint + review_priority + rule_reasons`。

## 6. `rule_flags` 冻结字段

### 6.1 护栏类

#### `guardrail_trusted_idp_flow_candidate`
含义：页面更像可信身份提供方托管的合法认证 / 授权流程，而不是品牌伪造页。

#### `guardrail_third_party_auth_delegate_candidate`
含义：页面核心动作更像第三方认证委托 / SSO / OAuth 跳转，而不是站内伪装索权。

#### `guardrail_brand_surface_not_equal_brand_spoof_candidate`
含义：页面出现品牌表面元素，不足以推出“品牌伪造已成立”。

#### `guardrail_sensitive_collection_absent_on_page_candidate`
含义：本页缺少直接敏感信息收集证据，不能仅因品牌与流程表象直接推升终判。

### 6.2 hosted / intermediary / lure 类

#### `hosted_lure_candidate`
含义：页面托管在可信或常见平台上，但承担明显的社工诱导 / 跳转 / 引流作用。

#### `intermediary_platform_page_candidate`
含义：页面更像攻击链中的中介承载页，而不是直接收集敏感信息的终态攻击页。

#### `offpage_attack_chain_candidate`
含义：当前页的主要威胁不在本页直接完成，而在后续跳转、下载或外链动作中完成。

#### `gate_or_evasion_candidate`
含义：页面更像 gate / captcha / anti-bot / evasion shell，需要更高层判断。

#### `download_lure_candidate`
含义：页面存在明显的诱导下载 / 假更新 / payload delivery 特征。

### 6.3 冲突类

#### `conflict_brand_high_but_spoof_not_established`
含义：品牌相关信号高，但尚不能证明存在品牌伪造或品牌欺骗成立。

#### `conflict_sensitive_intent_low_but_lure_signal_high`
含义：直接收集敏感信息的证据弱，但社工诱导 / 引流 / hosted lure 信号高。

#### `conflict_visual_risk_high_text_risk_low`
含义：视觉侧风险较高，但文本或表单侧风险较弱，需更高层复核。

#### `conflict_hosted_platform_and_attack_chain_signal`
含义：页面承载平台具有合法外壳，但攻击链信号明显，不能草率按 benign 处理。

### 6.4 路由与难例类

#### `needs_l2_candidate`
含义：样本应升级到 L2 或更高成本复核路径。

#### `needs_manual_review_candidate`
含义：样本应进入人工复核队列。

#### `hard_negative_candidate`
含义：样本表现为 benign-like，但包含容易被模型错判为威胁的强混淆特征。

#### `hard_positive_candidate`
含义：样本表现为 low-signal / benign-like，但实际更可能是社工威胁或攻击链关键页面。

## 7. `page_role_hint` 冻结枚举

`page_role_hint` 当前冻结为以下小枚举：

- `benign_service_page`
- `benign_idp_redirect`
- `direct_attack_page`
- `hosted_lure`
- `intermediary_carrier`
- `gate_or_evasion_shell`
- `download_lure`
- `other`
- `uncertain`

设计原则：

- 枚举保持小而硬；
- 先覆盖当前已知 hard negative / hard positive；
- 更细粒度的页面角色后续通过版本扩展。
- 与 `manual_labels.json -> manual_page_role` 共享同一对齐 page-role family。

## 8. `review_priority` 冻结枚举

当前冻结为：

- `p0`
- `p1`
- `p2`
- `p3`

推荐含义：

- `p0`：高风险且冲突复杂，优先人工复核或进 L2
- `p1`：高价值难例或 hosted/intermediary/gate 类样本
- `p2`：一般可疑样本，需要后续 review
- `p3`：普通样本，当前不优先处理

### 8.1 禁止直接按 `auto.risk_level_weak` 机械映射

`review_priority` 可以参考 `auto` 风险输出，但不得仅按弱分数直接离散化。应综合考虑：

- 是否存在护栏
- 是否存在冲突
- 是否是 hosted / intermediary / gate 页面
- 是否命中 hard candidate
- 是否应升级到 L2 或人工

## 9. `rule_reasons` 的用途

`rule_reasons` 用于记录：

- 触发了哪些规则
- 为什么得到当前 `page_role_hint`
- 为什么给了当前 `review_priority`
- 为什么建议 L2 / manual

要求：

- 以可审计的短规则名为主
- 不写自由叙事长文本
- 便于后续统计、错误分析和规则回看

推荐示例：

- `trusted_idp_pattern_detected`
- `third_party_auth_delegate_pattern`
- `brand_surface_without_spoof_proof`
- `hosted_platform_with_lure_cta`
- `offpage_chain_signal_detected`
- `visual_text_conflict_detected`
- `gate_or_evasion_shell_detected`

## 10. 与 `threat_taxonomy_v1` 的关系

当前 `threat_taxonomy_v1`：

- 继续保留在 `rule_labels.json` 中；
- 作为长期活跃弱标签命名空间；
- 用于后续多威胁任务扩展；
- 不在 v1-core 阶段继续做大规模枚举膨胀。

当前建议：

- 保留既有顶层结构；
- 暂不大改主 threat / scenario / narrative 的全量枚举体系；
- 优先把护栏、冲突、页面角色、升级提示做稳。

### 10.1 当前对齐的一阶 primary threat candidate family

`rule -> threat_taxonomy_v1 -> primary_threat_label_candidate` 当前与 `manual -> manual_primary_threat_label` 对齐为：

- `credential_theft`
- `payment_fraud`
- `wallet_drain_or_web3_approval_fraud`
- `pii_kyc_harvesting`
- `fake_support_or_contact_diversion`
- `malware_or_fake_download`
- `benign`
- `uncertain`

这些标签在 `rule` 中仍然只是 weak candidates，不是 final truth。

### 10.2 当前对齐的 scenario candidate family

`rule -> threat_taxonomy_v1 -> scenario_label_candidate` 当前对齐为：

- `finance_banking`
- `ecommerce_retail`
- `payment_platform`
- `logistics_delivery`
- `enterprise_mail_cloud`
- `social_media`
- `government_public_service`
- `crypto_web3`
- `gaming`
- `telecom_utility`
- `tech_support`
- `job_recruitment`
- `adult`
- `gambling`
- `other`
- `uncertain`

这些标签表达外层行业/场景壳，不替代最终 harmful-action judgment。

### 10.3 当前对齐关系

- `page_role_hint` 与 `manual_page_role` 共享同一对齐 page-role family；
- `threat_taxonomy_v1` 继续留在 `rule`，不得下沉到 `auto`；
- 长尾 ontology 扩展继续后置，不在本次对齐任务中扩写。

## 11. 生成方式

### 11.1 默认生成方式

`rule_labels.json` 应默认通过脚本统一离线 backfill 生成。

### 11.2 人工不直接编写 rule 文件

人工职责应是：

- 审核 hard cases
- 发现系统性误差模式
- 修正规则设计
- 审批 schema 变化

人工不应逐条手写 `rule_labels.json` 作为主生产方式。

## 12. 与 `manual_labels.json` 的接口边界

`rule_labels.json` 输出的是：

- 弱候选
- 处理建议
- 页面角色提示
- 复核优先级

`manual_labels.json` 才负责：

- 最终判断
- 最终高风险动作类
- 最终页面角色
- 最终品牌伪装认定
- 最终是否纳入主训练 / 评估 / auxiliary

默认原则：

- `rule` 不能替代 `manual`
- `manual` 也不应回写成 `rule` 的生产逻辑

## 13. v1-core 当前非目标

以下内容不在本次冻结范围：

- 所有长尾诈骗子类的一次性全量枚举
- 所有 narrative / ecosystem tags 的最终全集
- `manual_labels.json` 终态 schema 的完整冻结
- 端到端训练 target 的最终映射
- L2 全量判定本体

## 14. 演进规则

### 14.1 当前可扩展项

后续允许扩展：

- `threat_taxonomy_v1` 的 tags 列表
- 更多 hosted / lure / carrier 子类
- 更细行业场景枚举
- 更细 narrative / ecosystem tags

### 14.2 当前冻结项

以下内容当前冻结为 v1-core 稳定骨架：

- `rule_flags` 现有字段名
- `page_role_hint` 小枚举
- `review_priority` 小枚举
- `rule_reasons` 的可审计短规则名风格
- `rule` 作为脚本统一离线 backfill 生成的默认路径

## 15. Definition of Done

`rule_label v1-core` 可以视为冻结完成，当且仅当：

- `rule_labels.json` 的核心定位明确；
- 与 `auto` / `manual` 的边界明确；
- 护栏、冲突、页面角色、升级提示四类核心字段明确；
- 小枚举已冻结；
- 默认生成路径明确；
- 后续扩展项与当前非目标明确；
- 与现有冻结数据结构契约不冲突。

### 原始中文说明

中文内容保留在前，供人工协作与快速导览。英文版为权威版本。

## 2026-04-27 Chinese Definition Update Summary

- `rule` 应支持“高危欺骗行为已观察到，但 payload / action 未观察到”的处理语义。
- `guardrail_sensitive_collection_absent_on_page_candidate` 不能被理解为自动 benign；它只表示当前页缺少直接敏感收集证据。
- 本次不新增或重命名 `rule_labels.json` 字段、枚举或 schema。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Rule Label Policy V1 Core

## 1. Purpose

This document freezes the **v1-core framework** of `rule_labels.json` for Warden.

Its purpose is to solve the following problems:

1. `auto_labels.json` can describe what was observed, but it is not sufficient to consistently express what should be done with the sample.
2. Real hard-negative and hard-positive failure modes already exist, so a stable rule layer is needed to carry:
   - guardrails
   - evidence conflicts
   - page-role hints
   - escalation and review routing hints
3. `rule_labels.json` should gain a stable skeleton now, so later offline backfill can remain unified instead of rewriting schema while historical samples continue to accumulate.

This document freezes **`rule_label v1-core`**, not the final full threat ontology.
This is the active in-repo `rule` policy doc. This alignment keeps the stable filename and makes the shared threat/scenario/page-role families explicit with `manual`.

## 2. Role and Boundary

### 2.1 Role of `rule_labels.json`

`rule_labels.json` is:

- a **rule-derived layer** built on top of `auto_labels.json` and frozen upstream artifacts;
- a weak-label layer focused on **handling hints, escalation hints, conflicts, and page-role candidates**;
- intended to support:
  - more stable L1 judgment
  - L2 escalation routing
  - manual-review queues
  - later error analysis and label governance

It is not:

- a human gold-label layer;
- a final truth layer;
- a replacement for `manual_labels.json`.

Under the project-level definition, `rule` should be able to represent cases where high-risk deceptive behavior is present while direct action payload is not observed. Such cases may require escalation or manual review instead of being treated as automatic benign.

### 2.2 Difference from `auto_labels.json`

- `auto_labels.json` answers: **what was observed on the page**.
- `rule_labels.json` answers: **given those observations, what does the sample more likely represent and how should it be handled**.

Default interpretation:

- `auto` = evidence-first weak layer
- `rule` = decision-support weak layer
- `manual` = final adjudication layer

### 2.3 Difference from `manual_labels.json`

`manual_labels.json` is responsible for:

- final judgment
- final high-risk action class
- final page role
- final brand-impersonation decision
- final admission into training / evaluation / auxiliary subsets

`rule_labels.json` is not responsible for those final decisions. It is responsible for **candidates, guardrails, conflicts, priority, and escalation hints**.

## 3. Design Principles

### 3.1 Freeze the skeleton first, not the full ontology

At the current stage, only the following four core families are frozen:

1. `guardrail_*`: false-positive guardrails
2. `conflict_*`: evidence conflicts
3. `page_role_hint`: page-role candidate
4. `routing / review`: escalation and review hints

Long-tail scenarios, ultra-fine industry subtypes, and full narrative taxonomy are future extensions and are intentionally not frozen exhaustively in v1-core.

### 3.2 `rule` must not be a renamed copy of `auto`

The following are not valid rule design:

- mapping `risk_level_weak` directly into `review_priority`
- converting `claimed_brands` directly into `primary_threat_label_candidate`
- re-packaging the auto weak score without examining evidence structure

A valid rule layer must express:

- conflicts
- guardrails
- page role
- escalation routing

### 3.3 `rule` must support both de-escalation and escalation

`rule_labels.json` must be able to:

- suppress false positives on benign third-party auth / OAuth / trusted-platform pages;
- recover hosted lures / intermediary carriers / off-page attack-chain pages from deceptively low-risk auto outputs.

### 3.4 Default generation should be unified offline backfill

The recommended production path is:

1. capture samples under the frozen dataset contract;
2. read frozen artifacts and `auto_labels.json` offline in batch;
3. produce `rule_labels.json` in a unified backfill step.

Manual writing of rule files should not be the primary path.

## 4. Allowed Input Sources

`rule_labels.json` generation may read from:

- `auto_labels.json`
- `meta.json`
- `url.json`
- `forms.json`
- `net_summary.json`
- `visible_text.txt`
- `html_rendered.json`
- `html_raw.json` as fallback
- `diff_summary.json` when present

Therefore rule generation must not be interpreted as “repackaging `auto.risk_score_weak` only.”

## 5. Frozen v1-core Top-Level Shape

The recommended frozen shape is:

```json
{
  "schema_version": "warden_rule_v1_core",
  "generated_at_utc": "2026-03-26T00:00:00Z",
  "source": "offline_rule_backfill",
  "rule_flags": {
    "guardrail_trusted_idp_flow_candidate": false,
    "guardrail_third_party_auth_delegate_candidate": false,
    "guardrail_brand_surface_not_equal_brand_spoof_candidate": false,
    "guardrail_sensitive_collection_absent_on_page_candidate": false,

    "hosted_lure_candidate": false,
    "intermediary_platform_page_candidate": false,
    "offpage_attack_chain_candidate": false,
    "gate_or_evasion_candidate": false,
    "download_lure_candidate": false,

    "conflict_brand_high_but_spoof_not_established": false,
    "conflict_sensitive_intent_low_but_lure_signal_high": false,
    "conflict_visual_risk_high_text_risk_low": false,
    "conflict_hosted_platform_and_attack_chain_signal": false,

    "needs_l2_candidate": false,
    "needs_manual_review_candidate": false,
    "hard_negative_candidate": false,
    "hard_positive_candidate": false
  },
  "page_role_hint": "other",
  "review_priority": "p3",
  "rule_reasons": ["..."],
  "threat_taxonomy_v1": {
    "primary_threat_label_candidate": "uncertain",
    "primary_threat_label_confidence": 0.0,
    "primary_threat_label_rules": [],
    "scenario_label_candidate": "other",
    "scenario_label_confidence": 0.0,
    "scenario_label_rules": [],
    "narrative_tags_candidate": [],
    "evidence_tags_candidate": [],
    "evasion_tags_candidate": [],
    "ecosystem_tags_candidate": [],
    "taxonomy_source": "rule_derived_from_auto_and_frozen_artifacts",
    "taxonomy_review_status": "weak_candidate_only"
  }
}
```

Notes:

- `threat_taxonomy_v1` remains a long-lived weak-label namespace;
- v1-core does not require exhaustive threat-taxonomy expansion now;
- the core focus of v1-core is `rule_flags + page_role_hint + review_priority + rule_reasons`.

## 6. Frozen `rule_flags`

### 6.1 Guardrail Flags

#### `guardrail_trusted_idp_flow_candidate`
Meaning: the page more likely resembles a legitimate provider-hosted identity/auth flow rather than a brand-spoofing page.

#### `guardrail_third_party_auth_delegate_candidate`
Meaning: the core interaction resembles delegated third-party authentication / SSO / OAuth flow rather than a self-claimed phishing surface.

#### `guardrail_brand_surface_not_equal_brand_spoof_candidate`
Meaning: surface-level brand presence is insufficient to establish brand impersonation.

#### `guardrail_sensitive_collection_absent_on_page_candidate`
Meaning: direct sensitive collection evidence is absent on the current page. This is a `payload not observed` state, not a benign verdict. The page should not be escalated solely by weak brand or workflow surface appearance, but strong deceptive identity, authority, institution, security, financial, support, reward, access-control, hosted-lure, or attack-chain context may still justify escalation or review.

### 6.2 Hosted / Intermediary / Lure Flags

#### `hosted_lure_candidate`
Meaning: the page is hosted on a trusted or common platform but serves an obvious social-engineering lure / redirect / user-push role.

#### `intermediary_platform_page_candidate`
Meaning: the page resembles an intermediate carrier page in the attack chain rather than the final direct collection page.

#### `offpage_attack_chain_candidate`
Meaning: the main threat is completed off-page through later redirection, download, or follow-up action.

#### `gate_or_evasion_candidate`
Meaning: the page resembles a gate / captcha / anti-bot / evasion shell and should be treated as a higher-cost case.

#### `download_lure_candidate`
Meaning: the page contains strong download-lure / fake-update / payload-delivery characteristics.

### 6.3 Conflict Flags

#### `conflict_brand_high_but_spoof_not_established`
Meaning: brand-related evidence is strong, but brand spoofing is not actually established.

#### `conflict_sensitive_intent_low_but_lure_signal_high`
Meaning: direct on-page sensitive-collection evidence is weak, but lure / redirection / hosted-page signals are strong.

This conflict is the main v1-core place to preserve behavior-only or payload-not-observed risk without changing the schema.

#### `conflict_visual_risk_high_text_risk_low`
Meaning: visual risk appears elevated while text/form evidence remains weak, so stronger review is needed.

#### `conflict_hosted_platform_and_attack_chain_signal`
Meaning: the page sits on a legitimate-looking host platform while also showing strong attack-chain cues.

### 6.4 Routing and Hard-Case Flags

#### `needs_l2_candidate`
Meaning: the sample should be escalated into L2 or another higher-cost review path.

#### `needs_manual_review_candidate`
Meaning: the sample should enter a manual-review queue.

#### `hard_negative_candidate`
Meaning: the sample is benign-like but contains strong confusing features likely to trigger false positives.

#### `hard_positive_candidate`
Meaning: the sample is low-signal or benign-like on the surface but is more likely to be a real social-engineering threat or attack-chain-critical page.

## 7. Frozen `page_role_hint` Enumeration

`page_role_hint` is frozen to the following compact enum:

- `benign_service_page`
- `benign_idp_redirect`
- `direct_attack_page`
- `hosted_lure`
- `intermediary_carrier`
- `gate_or_evasion_shell`
- `download_lure`
- `other`
- `uncertain`

Design rule:

- keep it compact and hard;
- cover current real hard-negative and hard-positive patterns first;
- add finer page-role granularity only in later versioned extensions.
- keep it aligned with `manual_labels.json -> manual_page_role`.

## 8. Frozen `review_priority` Enumeration

The frozen enum is:

- `p0`
- `p1`
- `p2`
- `p3`

Recommended meaning:

- `p0`: high-risk and conflict-heavy cases that should be reviewed or escalated first
- `p1`: valuable hard cases or hosted/intermediary/gate pages
- `p2`: generally suspicious samples worth later review
- `p3`: ordinary samples not currently prioritized

### 8.1 Direct mapping from auto weak score is forbidden

`review_priority` may reference auto outputs, but it must not be a direct discretization of `risk_level_weak` alone. It should combine:

- presence of guardrails
- presence of conflicts
- hosted / intermediary / gate role
- hard-case flags
- need for L2 or manual review

## 9. Purpose of `rule_reasons`

`rule_reasons` stores:

- which rules fired
- why the current `page_role_hint` was assigned
- why the current `review_priority` was assigned
- why escalation to L2 or manual review was suggested

Requirements:

- use auditable short rule names
- do not use free-form long narrative text
- keep it easy to analyze later in statistics and rule audits

Recommended examples:

- `trusted_idp_pattern_detected`
- `third_party_auth_delegate_pattern`
- `brand_surface_without_spoof_proof`
- `hosted_platform_with_lure_cta`
- `offpage_chain_signal_detected`
- `visual_text_conflict_detected`
- `gate_or_evasion_shell_detected`

## 10. Relationship with `threat_taxonomy_v1`

At the current stage, `threat_taxonomy_v1` should:

- remain inside `rule_labels.json`;
- remain a long-lived active weak-label namespace;
- support future multi-threat expansion;
- not be heavily expanded in v1-core.

Current recommendation:

- preserve the existing top-level shape;
- avoid large ontology expansion now;
- prioritize stable guardrails, conflicts, page roles, and escalation hints first.

### 10.1 Current aligned primary threat candidate family

`rule -> threat_taxonomy_v1 -> primary_threat_label_candidate` is currently aligned with `manual -> manual_primary_threat_label` as:

- `credential_theft`
- `payment_fraud`
- `wallet_drain_or_web3_approval_fraud`
- `pii_kyc_harvesting`
- `fake_support_or_contact_diversion`
- `malware_or_fake_download`
- `benign`
- `uncertain`

These remain weak candidates inside `rule`, not final truth.

### 10.2 Current aligned scenario candidate family

`rule -> threat_taxonomy_v1 -> scenario_label_candidate` is currently aligned as:

- `finance_banking`
- `ecommerce_retail`
- `payment_platform`
- `logistics_delivery`
- `enterprise_mail_cloud`
- `social_media`
- `government_public_service`
- `crypto_web3`
- `gaming`
- `telecom_utility`
- `tech_support`
- `job_recruitment`
- `adult`
- `gambling`
- `other`
- `uncertain`

These labels describe the outer industry/scenario shell rather than the final harmful action.

### 10.3 Current alignment relationship

- `page_role_hint` shares the same aligned page-role family as `manual_page_role`;
- `threat_taxonomy_v1` stays in `rule` and must not be pushed down into `auto`;
- long-tail ontology expansion remains deferred and is not part of this alignment task.

## 11. Generation Policy

### 11.1 Default generation path

`rule_labels.json` should be generated by unified offline backfill by default.

### 11.2 Manual writing is not the default production path

Human responsibility should be:

- reviewing hard cases
- discovering systematic error patterns
- correcting rule design
- approving schema changes

Humans should not manually write per-sample `rule_labels.json` as the main production path.

## 12. Interface Boundary with `manual_labels.json`

`rule_labels.json` outputs:

- weak candidates
- handling hints
- page-role hints
- review priority

`manual_labels.json` is responsible for:

- final judgment
- final high-risk action class
- final page role
- final brand-impersonation decision
- final admission into main training / evaluation / auxiliary subsets

Default rule:

- `rule` must not replace `manual`
- `manual` should not be back-written into rule production semantics

## 13. Current Non-Goals

The following are out of scope for this freeze:

- exhaustive one-shot enumeration of all long-tail fraud subtypes
- final full narrative / ecosystem tag universe
- full final freeze of `manual_labels.json`
- final end-to-end training target mapping
- full L2 ontology

## 14. Evolution Rules

### 14.1 Items that may expand later

Later expansion is allowed for:

- `threat_taxonomy_v1` tag lists
- more hosted / lure / carrier subtypes
- finer industry-scene enums
- finer narrative / ecosystem tags

### 14.2 Items frozen now

The following are frozen as the stable v1-core skeleton:

- the current `rule_flags` field names
- the compact `page_role_hint` enum
- the compact `review_priority` enum
- the auditable short-rule style of `rule_reasons`
- the default production path of rule labels through unified offline backfill

## 15. Definition of Done

`rule_label v1-core` can be treated as frozen only if:

- the core role of `rule_labels.json` is explicit;
- the boundary with `auto` and `manual` is explicit;
- the four core families (guardrails, conflicts, page roles, escalation hints) are explicit;
- the compact enums are frozen;
- the default generation path is explicit;
- the current non-goals and later extension path are explicit;
- the policy does not conflict with the current frozen dataset-output contract.

