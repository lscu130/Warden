# Warden 人工标签策略 V1 Core

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于冻结 `manual_labels.json` 的 **v1-core 框架**。
- 当前目标不是一次性定义全部长尾威胁本体，也不是要求对全量数据做人工标注，而是先稳定 **最终裁决、最终高风险动作类、最终页面角色、最终品牌伪装认定、最终数据集去向** 这五类核心人工字段。
- 本文档不重写 `Warden_Dataset_Output_Frozen_Spec_v1.1.md` 中已经冻结的样本目录结构，也不重写 `auto_labels.json` 与 `rule_labels.json` 的既有角色边界。
- 若涉及精确字段名、枚举、边界、生产方式或演进规则，以英文版为准。
- 当前 repo 活跃版本为 `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`，并与 `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`、`Warden_AUTO_LABEL_POLICY_V1.md`、`Warden_RULE_LABEL_POLICY_V1_CORE.md` 保持对齐；不再并行保留独立 `_ALIGNED` 活跃副本。

# Warden Manual Label Policy V1 Core

## 1. 文档目的

本文件用于冻结 `manual_labels.json` 的 **第一阶段核心框架**，回答以下问题：

1. `manual_labels.json` 在 Warden 中到底负责什么；
2. `manual` 与 `auto_labels.json`、`rule_labels.json` 的边界是什么；
3. 人工最终应该裁决哪些信息，而不是重复 `auto` / `rule` 的低层观察；
4. `manual` 是否需要全量覆盖数据集；
5. 当前阶段最小可用的人工标签字段应包含什么。

本文件冻结的是 **`manual_label v1-core`**，而不是最终全量本体、最终训练映射、或未来全部长尾场景。
当前 repo 内以本文件作为 `manual` 层活跃版本，并按 suite alignment note 与 `auto/rule` 共享 family 对齐。

## 2. 定位与边界

### 2.1 `manual_labels.json` 的定位

`manual_labels.json` 是：

- Warden 的 **final adjudication layer**；
- 人工最终裁决层；
- 用于承载：
  - 最终判断
  - 最终高风险动作类
  - 最终页面角色
  - 最终品牌伪装认定
  - 最终数据集纳入去向

它不是：

- 低层观察证据层；
- 规则护栏/冲突表达层；
- 默认全量覆盖要求；
- 用来替代 `auto_labels.json` 和 `rule_labels.json` 的重复抄写层。

### 2.2 与 `auto_labels.json` 的区别

默认理解：

- `auto` = **what was observed on the page**
- `rule` = **given those observations, what does the sample more likely represent and how should it be handled**
- `manual` = **final adjudication**

也就是说：

- `auto` 负责“观察到什么”；
- `rule` 负责“这些观察组合起来更像什么、该怎么处理”；
- `manual` 负责“最终到底是什么”。

### 2.3 与 `rule_labels.json` 的区别

`rule_labels.json` 负责：

- guardrails
- conflicts
- page-role hints
- escalation hints
- review priority
- weak candidate taxonomy

`manual_labels.json` 才负责：

- final judgment
- final high-risk action class
- final page role
- final brand-impersonation decision
- final dataset-admission decision

## 3. 设计原则

### 3.1 `manual` 不重复低层观察

`manual` 不应该复制以下内容作为主体：

- `url_features`
- `form_features`
- `html_features`
- `network_features`
- `risk_score_weak`
- `risk_level_weak`
- `guardrail_*`
- `conflict_*`
- `review_priority`
- `needs_l2_candidate`
- `needs_manual_review_candidate`

这些属于 `auto` 或 `rule` 的职责层。

### 3.2 `manual` 优先回答最终裁决问题

`manual` 需要回答的是：

1. 最终是否是社会工程威胁；
2. 观察到什么高危欺骗行为，以及最终想诱导、准备或路由用户执行什么高风险动作；
3. 当前页在攻击链里扮演什么角色；
4. 品牌伪装是否真的成立；
5. 该样本最终应进入哪个数据使用桶。

### 3.3 `manual` 默认不是全量前置要求

当前阶段，`manual_labels.json` 不应成为全量数据集的默认前置条件。

原因：

- 当前项目仍处于 foundation / contract-freezing stage；
- `auto` 和 `rule` 已承担全量弱标签与处理提示职责；
- manual final adjudication 成本高；
- hard cases、gold eval 与冲突样本优先级远高于全量重复样本；
- 若 cluster/subcluster 已存在，应优先人工确认 representative / canonical 样本，而不是默认逐个重复页全量人工标。

### 3.4 一级主类保持兼容，同时最终裁决覆盖行为和动作

`manual` 的主类继续围绕稳定的 **最终高风险动作 / 最终危害目标** 枚举，以保持兼容；但 `manual_final_label` 的最终裁决应同时考虑高危欺骗行为和高危诱导动作。

行业/场景、内容警示、hard-case 属性等应作为辅助字段保留，而不应覆盖最终威胁主类。

## 4. 当前覆盖策略

### 4.1 当前默认不是全量人工标注

`manual_labels.json` 当前默认不要求对全部成功样本全量覆盖。

### 4.2 推荐优先人工标注的子集

当前阶段建议优先覆盖：

1. **gold evaluation subset**
   - 用于模型评测、误差分析、基准对照。

2. **hard cases**
   - hard negative
   - hard positive
   - hosted lure
   - intermediary carrier
   - gate / evasion shell
   - evidence-conflict samples

3. **高价值 / 高争议样本**
   - web3 wallet approval / seed phrase pages
   - trusted-platform hosted lures
   - strong brand-surface but spoof-not-established pages
   - adult / gambling / sensitive-vertical samples where product warning and threat judgment must be separated

4. **规则失败样本**
   - `auto` 明显失败
   - `rule` 明显失败
   - `auto` 与 `rule` 冲突显著
   - 当前系统性误报 / 漏报模式样本

### 4.3 与 cluster / subcluster 的关系

若数据管线已有 cluster / subcluster：

- 优先人工审核 canonical / representative 样本；
- 默认不要求对同簇近重复页逐页全量人工重复标注；
- 若同一子簇内存在明确时间差异、页面状态差异或动作差异，可额外补少量人工标注。

## 5. v1-core 顶层结构

推荐冻结为：

```json
{
  "schema_version": "warden_manual_v1_core",
  "manual_final_label": "se_threat",
  "manual_primary_threat_label": "credential_theft",
  "manual_action_variant": "password_and_otp",
  "manual_scenario_label": "enterprise_mail_cloud",
  "manual_page_role": "direct_attack_page",
  "manual_brand_impersonation": "deceptive_brand_claim_present",
  "manual_content_warning": "none",
  "manual_hard_case_type": "hard_positive",
  "manual_dataset_admission": "train_main",
  "manual_reason_codes": [
    "direct_credential_collection",
    "brand_claim_established"
  ],
  "manual_review_status": "reviewed",
  "manual_reviewer": "annotator_01",
  "manual_reviewed_at_utc": "2026-04-07T00:00:00Z",
  "manual_notes": "short note"
}
```

说明：

- `manual_action_variant` 用于在不破坏主 threat label 稳定性的前提下，保留更细的动作差异；
- `manual_content_warning` 用于表达 adult / gambling 等独立警示轴，不替代主 threat judgment；
- `manual_dataset_admission` 用于把人工最终裁决直接落到训练/评测/auxiliary 路由上。

## 6. 冻结字段

### 6.1 `manual_final_label`

冻结枚举：

- `benign`
- `se_threat`
- `uncertain`
- `auxiliary`

含义：

- `benign`：正常页面，不构成社会工程威胁；
- `se_threat`：明确社会工程威胁页面；
- `uncertain`：证据不足、证据冲突、当前无法稳定裁决；
- `auxiliary`：具有研究或复核价值，但不适合直接纳入主训练集。

### 6.2 `manual_primary_threat_label`

冻结枚举：

- `credential_theft`
- `payment_fraud`
- `wallet_drain_or_web3_approval_fraud`
- `pii_kyc_harvesting`
- `fake_support_or_contact_diversion`
- `malware_or_fake_download`
- `benign`
- `uncertain`

设计说明：

- 与 `rule -> threat_taxonomy_v1 -> primary_threat_label_candidate` 保持对齐；
- 主类优先保持小而稳；
- 更细动作差异通过 `manual_action_variant` 表达。

### 6.3 `manual_action_variant`

冻结枚举：

- `none`
- `password_only`
- `otp_only`
- `password_and_otp`
- `card_payment`
- `wallet_approval`
- `seed_phrase`
- `pii_form`
- `fake_support_contact`
- `remote_tool_download`
- `fake_software_download`
- `other`
- `uncertain`

设计说明：

- 该字段用于保留主类内部更细的动作差异；
- 不应反向取代主类；
- 对非 threat 或不适用情况，使用 `none`。

### 6.4 `manual_scenario_label`

冻结枚举：

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

说明：

- 与 `rule -> threat_taxonomy_v1 -> scenario_label_candidate` 共享同一对齐 scenario family；
- 表达行业壳 / 场景壳；
- 不替代主 threat 类；
- adult / gambling 放在场景和警示轴中，不直接提升为 threat 主类。

### 6.5 `manual_page_role`

冻结枚举：

- `benign_service_page`
- `benign_idp_redirect`
- `direct_attack_page`
- `hosted_lure`
- `intermediary_carrier`
- `gate_or_evasion_shell`
- `download_lure`
- `other`
- `uncertain`

说明：

- `manual_page_role` 是对 `rule.page_role_hint` 的最终人工确认版本；
- 用于稳定区分 benign OAuth / hosted lure / intermediary / direct collection 等关键模式。

### 6.6 `manual_brand_impersonation`

冻结枚举：

- `none`
- `supportive_brand_reference_only`
- `deceptive_brand_claim_present`
- `uncertain`

说明：

- 用于把“品牌表面出现”与“品牌伪装成立”分开；
- 不能因为品牌 token 命中就机械判定 `deceptive_brand_claim_present`。

### 6.7 `manual_content_warning`

冻结枚举：

- `none`
- `adult_content`
- `gambling`
- `adult_and_gambling`
- `uncertain`

说明：

- 这是独立 warning axis；
- 不与 `manual_final_label` 并列为第三主类；
- 其作用是保留产品/审计/分析所需的内容警示信息，而不是取代 threat judgment。

### 6.8 `manual_hard_case_type`

冻结枚举：

- `none`
- `hard_negative`
- `hard_positive`
- `both`
- `uncertain`

说明：

- `hard_negative` = 实际 benign，但表面具有强 threat-like signals；
- `hard_positive` = 实际 threat，但表面 benign-like / low-signal；
- `both` 仅在多重冲突极强时使用。

### 6.9 `manual_dataset_admission`

冻结枚举：

- `train_main`
- `eval_main`
- `aux_only`
- `exclude`
- `uncertain`

说明：

- `train_main`：可进入主训练池；
- `eval_main`：适合主评测集，但不默认进训练；
- `aux_only`：仅进入辅助集 / hard-case 集 / 保留集；
- `exclude`：不建议进入主要使用池；
- `uncertain`：当前未稳定决定最终路由。

### 6.10 `manual_reason_codes`

要求：

- 必须是可审计、可统计的短代码列表；
- 不应写成长篇自由叙事；
- 可多选；
- 后续允许扩展，但 v1-core 保持“短代码 + 可统计”风格冻结。

推荐示例：

- `benign_oauth_flow`
- `trusted_platform_hosted_lure`
- `direct_credential_collection`
- `brand_claim_established`
- `brand_surface_not_spoof`
- `offpage_attack_chain`
- `seed_phrase_request`
- `wallet_approval_request`
- `payment_collection`
- `support_contact_diversion`
- `download_lure_confirmed`
- `evidence_insufficient`

### 6.11 审核元数据

冻结字段：

- `manual_review_status`
- `manual_reviewer`
- `manual_reviewed_at_utc`
- `manual_notes`

其中：

#### `manual_review_status`
冻结枚举：

- `unreviewed`
- `reviewed`
- `disputed`

#### `manual_notes`
- 允许短自由文本；
- 不应用作主要机器统计字段；
- 不应用来替代 `manual_reason_codes`。

## 7. 生成方式

### 7.1 默认由人工产生

`manual_labels.json` 的默认生产方式是：

- 人工审核
- 人工最终裁决
- 人工确认数据集去向

### 7.2 脚本可辅助，但不能自动写 final adjudication

允许的脚本辅助包括：

- 生成 review queue
- 汇总 `auto` / `rule` / upstream evidence
- 预填建议模板
- 导出待审 JSON 草稿

不允许的默认路径包括：

- 脚本直接替代人工生成最终 `manual_labels.json`
- 把 `rule` 自动升格为 `manual`
- 把 `auto` 或 `rule` 当 final truth 直接写入人工层

## 8. 与 `auto` / `rule` 的接口边界

### 8.1 `manual` 可以参考 `auto` 和 `rule`

人工审核时允许参考：

- `auto_labels.json`
- `rule_labels.json`
- 冻结上游工件
- cluster / subcluster / review manifest

### 8.2 `manual` 不能退化成“复制 auto/rule”

无效的 manual 设计包括：

- 直接把 `auto.risk_level_weak` 作为 `manual_final_label`
- 直接把 `rule.page_role_hint` 复制成 `manual_page_role`
- 直接把 `rule.primary_threat_label_candidate` 复制成 `manual_primary_threat_label`

### 8.3 `manual` 与 TrainSet V1 的关系

`manual`：

- 不是 TrainSet V1 全量前置要求；
- 适合 gold eval subset、hard-case subset、冲突样本、策略敏感样本；
- 不应阻塞主训练集在 `auto` / `rule` 驱动下的持续生产。

## 9. 当前非目标

以下内容不在本次 v1-core 冻结范围：

- 全量 manual 标注要求
- 全部长尾场景和 narrative tags 的一次性冻结
- 最终训练 target 的全量映射
- 人工审核工作台 / UI 设计
- 多人协同标注协议的完整治理

## 10. 演进规则

### 10.1 后续允许扩展

后续允许扩展：

- `manual_reason_codes` 词表
- `manual_action_variant` 更细子类
- 更细场景壳枚举
- 更细内容警示 / 生态警示轴
- 多人审核一致性字段

### 10.2 当前冻结项

以下内容当前冻结为 v1-core 稳定骨架：

- `manual_final_label`
- `manual_primary_threat_label`
- `manual_action_variant`
- `manual_scenario_label`
- `manual_page_role`
- `manual_brand_impersonation`
- `manual_content_warning`
- `manual_hard_case_type`
- `manual_dataset_admission`
- `manual_reason_codes` 的短代码风格
- 审核元数据字段
- “manual 默认不是全量前置要求”的策略边界

## 11. Definition of Done

`manual_label v1-core` 可以视为冻结完成，当且仅当：

- `manual` 的核心定位明确；
- 与 `auto` / `rule` 的边界明确；
- 最终裁决、主 threat 类、页面角色、品牌伪装、数据集去向等核心字段明确；
- 当前建议覆盖策略明确；
- 默认生成方式明确；
- 当前非目标与扩展规则明确；
- 与现有 frozen spec、auto policy、rule policy、TrainSet V1 不冲突。

### 原始中文说明

中文内容保留在前，供人工协作与快速导览。英文版为权威版本。

## 2026-04-27 Chinese Definition Update Summary

- `manual` 的最终裁决应同时考虑高危欺骗行为和高危诱导动作。
- 未观察到 payload / action 时，应记录为 `payload not observed`，不能自动判为 benign。
- 本次只更新文档口径，不新增或重命名 `manual_labels.json` 字段、枚举或 schema。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Manual Label Policy V1 Core

## 1. Purpose

This document freezes the **v1-core framework** of `manual_labels.json` for Warden.
It is the active in-repo `manual` policy doc and stays aligned with `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`, `Warden_AUTO_LABEL_POLICY_V1.md`, and `Warden_RULE_LABEL_POLICY_V1_CORE.md`.

It answers the following questions:

1. what `manual_labels.json` is supposed to do in Warden;
2. how `manual` differs from `auto_labels.json` and `rule_labels.json`;
3. which final decisions should be made by human adjudication instead of repeating low-level evidence layers;
4. whether `manual` is expected to cover the full dataset;
5. what the minimum viable manual-label fields should be at the current stage.

This document freezes **`manual_label v1-core`**, not the final full ontology, not the final training-target mapping, and not all future long-tail scene definitions.

## 2. Role and Boundary

### 2.1 Role of `manual_labels.json`

`manual_labels.json` is:

- Warden's **final adjudication layer**;
- the human final-decision layer;
- intended to carry:
  - final judgment,
  - final high-risk action class,
  - final page role,
  - final brand-impersonation decision,
  - final dataset-admission routing.

It is not:

- a low-level observation layer;
- a guardrail/conflict layer;
- a default full-corpus requirement;
- a place to duplicate `auto_labels.json` or `rule_labels.json`.

### 2.2 Difference from `auto_labels.json`

Default interpretation:

- `auto` = **what was observed on the page**
- `rule` = **given those observations, what does the sample more likely represent and how should it be handled**
- `manual` = **final adjudication**

In practice:

- `auto` records observations;
- `rule` provides handling-oriented weak interpretation;
- `manual` makes the final decision.

### 2.3 Difference from `rule_labels.json`

`rule_labels.json` is responsible for:

- guardrails,
- conflicts,
- page-role hints,
- escalation hints,
- review priority,
- weak candidate taxonomy.

`manual_labels.json` is responsible for:

- final judgment,
- final high-risk action class,
- final page role,
- final brand-impersonation decision,
- final dataset-admission decision.

The final judgment must consider high-risk deceptive behavior and/or high-risk induced action. A page can be `se_threat` because it constructs a deceptive identity, brand, authority, institution, security, financial, support, reward, or access-control context even when no direct credential, payment, wallet, download, POST, or other action payload is currently observed.

## 3. Design Principles

### 3.1 `manual` must not duplicate low-level observations

The following should not form the core of `manual`:

- `url_features`
- `form_features`
- `html_features`
- `network_features`
- `risk_score_weak`
- `risk_level_weak`
- `guardrail_*`
- `conflict_*`
- `review_priority`
- `needs_l2_candidate`
- `needs_manual_review_candidate`

These belong to `auto` or `rule`.

### 3.2 `manual` should answer final adjudication questions

`manual` should answer:

1. whether the page is finally judged benign, social-engineering threat, uncertain, or auxiliary;
2. what high-risk deceptive behavior is observed, and what harmful action it is ultimately trying to induce, prepare, or route toward if any;
3. what role the current page plays in the attack chain;
4. whether brand impersonation is actually established;
5. where the sample should finally be routed in dataset usage.

If high-risk deceptive behavior is established but the direct payload/action is absent in the current capture, reviewers should treat that as a `payload not observed` evidence state rather than as automatic benign.

### 3.3 `manual` is not a default full-corpus prerequisite

At the current stage, `manual_labels.json` should not be treated as a full-corpus requirement.

Reasons:

- Warden is still in the foundation / contract-freezing stage;
- `auto` and `rule` already cover full-corpus weak labeling and handling hints;
- manual adjudication is expensive;
- gold-eval, hard-case, and conflict-heavy samples are more valuable than exhaustively annotating near-duplicate ordinary pages;
- when cluster/subcluster structures exist, manual review should prioritize canonical/representative samples rather than per-page exhaustive duplication.

### 3.4 Primary classes remain stable while final judgment covers behavior and action

The manual primary label remains aligned with the stable **final harmful action / induced harm goal** family for compatibility. The final `manual_final_label` should still consider both high-risk deceptive behavior and high-risk induced action.

Industry, content warning, and hard-case attributes should remain secondary fields rather than replacing the main threat class.
When the final judgment is malicious by behavior but no direct action payload is observed, preserve the stable enum contract and use existing page-role, brand-impersonation, scenario, hard-case, and reason-code fields to document the basis. Any dedicated future fields such as `malicious_basis`, `high_risk_behavior_type`, or `payload_observed` require a separate schema task.

## 4. Current Coverage Strategy

### 4.1 Full-corpus manual coverage is not required by default

`manual_labels.json` is not required to cover the full successful corpus by default.

### 4.2 Recommended subsets to prioritize

The current stage should prioritize manual coverage for:

1. **gold evaluation subsets**
   - used for model evaluation, error analysis, and benchmark comparison;

2. **hard cases**
   - hard negative,
   - hard positive,
   - hosted lure,
   - intermediary carrier,
   - gate / evasion shell,
   - evidence-conflict cases;

3. **high-value / high-dispute samples**
   - web3 wallet approval / seed phrase pages,
   - trusted-platform hosted lures,
   - strong brand-surface but spoof-not-established pages,
   - adult / gambling / sensitive-vertical samples where warning and threat judgment must remain separated;

4. **rule-failure samples**
   - clear `auto` failure,
   - clear `rule` failure,
   - strong `auto` / `rule` disagreement,
   - recurring systematic false-positive or false-negative patterns.

### 4.3 Relationship with cluster / subcluster

When cluster/subcluster structures exist:

- review canonical / representative samples first;
- do not require exhaustive manual annotation for every near-duplicate page by default;
- add a small number of extra manual annotations only when time, page-state, or action differences are meaningful within the subcluster.

## 5. Frozen v1-core Top-Level Shape

The recommended frozen shape is:

```json
{
  "schema_version": "warden_manual_v1_core",
  "manual_final_label": "se_threat",
  "manual_primary_threat_label": "credential_theft",
  "manual_action_variant": "password_and_otp",
  "manual_scenario_label": "enterprise_mail_cloud",
  "manual_page_role": "direct_attack_page",
  "manual_brand_impersonation": "deceptive_brand_claim_present",
  "manual_content_warning": "none",
  "manual_hard_case_type": "hard_positive",
  "manual_dataset_admission": "train_main",
  "manual_reason_codes": [
    "direct_credential_collection",
    "brand_claim_established"
  ],
  "manual_review_status": "reviewed",
  "manual_reviewer": "annotator_01",
  "manual_reviewed_at_utc": "2026-04-07T00:00:00Z",
  "manual_notes": "short note"
}
```

Notes:

- `manual_action_variant` preserves finer-grained action differences without destabilizing the main threat-class layer;
- `manual_content_warning` preserves adult / gambling warning signals as a separate axis instead of replacing the main threat judgment;
- `manual_dataset_admission` is meant to connect human adjudication directly to training / evaluation / auxiliary routing.

## 6. Frozen Fields

### 6.1 `manual_final_label`

Frozen enum:

- `benign`
- `se_threat`
- `uncertain`
- `auxiliary`

Meaning:

- `benign`: the page is judged benign and not a meaningful social-engineering threat;
- `se_threat`: the page is judged to be a real social-engineering threat;
- `uncertain`: evidence is insufficient or conflicting;
- `auxiliary`: the sample remains valuable for research or review but should not directly enter the main training set.

### 6.2 `manual_primary_threat_label`

Frozen enum:

- `credential_theft`
- `payment_fraud`
- `wallet_drain_or_web3_approval_fraud`
- `pii_kyc_harvesting`
- `fake_support_or_contact_diversion`
- `malware_or_fake_download`
- `benign`
- `uncertain`

Design rule:

- stay aligned with `rule -> threat_taxonomy_v1 -> primary_threat_label_candidate`;
- keep the primary set compact and stable;
- express finer action differences through `manual_action_variant`.

### 6.3 `manual_action_variant`

Frozen enum:

- `none`
- `password_only`
- `otp_only`
- `password_and_otp`
- `card_payment`
- `wallet_approval`
- `seed_phrase`
- `pii_form`
- `fake_support_contact`
- `remote_tool_download`
- `fake_software_download`
- `other`
- `uncertain`

Design rule:

- preserve finer action differences inside a stable main-class system;
- do not let this field replace the primary threat class;
- use `none` when not applicable.

### 6.4 `manual_scenario_label`

Frozen enum:

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

Meaning:

- share the same aligned scenario family as `rule -> threat_taxonomy_v1 -> scenario_label_candidate`;
- describes the industry shell / context shell;
- does not replace the primary threat class;
- `adult` / `gambling` stay on the scenario and warning axes rather than becoming primary threat classes.

### 6.5 `manual_page_role`

Frozen enum:

- `benign_service_page`
- `benign_idp_redirect`
- `direct_attack_page`
- `hosted_lure`
- `intermediary_carrier`
- `gate_or_evasion_shell`
- `download_lure`
- `other`
- `uncertain`

Meaning:

- final human-confirmed version of the page role;
- used to separate benign OAuth-like pages from hosted lures, intermediary carriers, and direct collection pages.

### 6.6 `manual_brand_impersonation`

Frozen enum:

- `none`
- `supportive_brand_reference_only`
- `deceptive_brand_claim_present`
- `uncertain`

Meaning:

- separates surface-level brand reference from actually established brand impersonation;
- the presence of brand tokens alone is not enough to force `deceptive_brand_claim_present`.

### 6.7 `manual_content_warning`

Frozen enum:

- `none`
- `adult_content`
- `gambling`
- `adult_and_gambling`
- `uncertain`

Meaning:

- this is a separate warning axis;
- it must not become a third main class parallel to `benign` and `se_threat`;
- it exists for product, auditing, and analysis needs without replacing threat judgment.

### 6.8 `manual_hard_case_type`

Frozen enum:

- `none`
- `hard_negative`
- `hard_positive`
- `both`
- `uncertain`

Meaning:

- `hard_negative` = actually benign, but with strong threat-like surface signals;
- `hard_positive` = actually threatening, but benign-like or low-signal on the surface;
- `both` is reserved for highly conflicted and unusual cases.

### 6.9 `manual_dataset_admission`

Frozen enum:

- `train_main`
- `eval_main`
- `aux_only`
- `exclude`
- `uncertain`

Meaning:

- `train_main`: suitable for the main training pool;
- `eval_main`: suitable for evaluation but not necessarily default training;
- `aux_only`: only for auxiliary / hard-case / reserve-style usage;
- `exclude`: should not enter major usage pools;
- `uncertain`: routing is not yet stable.

### 6.10 `manual_reason_codes`

Requirements:

- must be a list of short auditable reason codes;
- must not become long free-form essays;
- multi-select is allowed;
- later expansion is allowed, but the v1-core style stays frozen as short analyzable codes.

Recommended examples:

- `benign_oauth_flow`
- `trusted_platform_hosted_lure`
- `direct_credential_collection`
- `brand_claim_established`
- `brand_surface_not_spoof`
- `offpage_attack_chain`
- `seed_phrase_request`
- `wallet_approval_request`
- `payment_collection`
- `support_contact_diversion`
- `download_lure_confirmed`
- `evidence_insufficient`

### 6.11 Review Metadata

Frozen fields:

- `manual_review_status`
- `manual_reviewer`
- `manual_reviewed_at_utc`
- `manual_notes`

#### `manual_review_status`

Frozen enum:

- `unreviewed`
- `reviewed`
- `disputed`

#### `manual_notes`

- may contain short free text;
- should not replace reason-code fields;
- should not be treated as the main machine-readable analysis field.

## 7. Generation Policy

### 7.1 Default generation is human-driven

`manual_labels.json` should be produced through:

- human review,
- human final adjudication,
- human final dataset-routing decisions.

### 7.2 Scripts may assist, but may not auto-produce final adjudication

Allowed assistance includes:

- generating review queues,
- aggregating `auto` / `rule` / upstream evidence,
- pre-filling suggestion templates,
- exporting draft review JSON.

Disallowed default behavior includes:

- scripts replacing humans for final `manual_labels.json`,
- auto-promoting `rule` into `manual`,
- treating `auto` or `rule` as final truth inside the manual layer.

## 8. Interface Boundary with `auto` / `rule`

### 8.1 `manual` may reference `auto` and `rule`

Human reviewers may consult:

- `auto_labels.json`,
- `rule_labels.json`,
- frozen upstream artifacts,
- cluster / subcluster / review-manifest outputs.

### 8.2 `manual` must not degrade into copying `auto` or `rule`

Invalid manual behavior includes:

- copying `auto.risk_level_weak` into `manual_final_label`,
- copying `rule.page_role_hint` into `manual_page_role`,
- copying `rule.primary_threat_label_candidate` into `manual_primary_threat_label`.

### 8.3 Relationship to TrainSet V1

`manual`:

- is not a full-corpus TrainSet V1 prerequisite;
- is appropriate for gold evaluation subsets, hard-case subsets, conflict-heavy subsets, and policy-sensitive subsets;
- should not block ongoing production of the main training set driven by `auto` and `rule`.

## 9. Current Non-Goals

The following are out of scope for v1-core:

- full-corpus manual-annotation requirement,
- one-shot freezing of every long-tail scenario or narrative tag,
- the final full training-target mapping,
- a manual-review UI or workflow application,
- a full multi-reviewer governance protocol.

## 10. Evolution Rules

### 10.1 Later extensions are allowed for:

- `manual_reason_codes`,
- finer `manual_action_variant` subtypes,
- finer scenario enums,
- finer warning or ecosystem-risk axes,
- multi-reviewer consistency fields.

### 10.2 Frozen now as the stable v1-core skeleton:

- `manual_final_label`
- `manual_primary_threat_label`
- `manual_action_variant`
- `manual_scenario_label`
- `manual_page_role`
- `manual_brand_impersonation`
- `manual_content_warning`
- `manual_hard_case_type`
- `manual_dataset_admission`
- the short-code style of `manual_reason_codes`
- review metadata fields
- the policy boundary that manual is not a default full-corpus prerequisite

## 11. Definition of Done

`manual_label v1-core` can be treated as frozen only if:

- the core role of `manual` is explicit;
- the boundary with `auto` and `rule` is explicit;
- the core final-adjudication fields are explicit;
- the current recommended coverage strategy is explicit;
- the default generation mode is explicit;
- the current non-goals and future-extension rules are explicit;
- the policy does not conflict with the frozen spec, auto policy, rule policy, or TrainSet V1.
