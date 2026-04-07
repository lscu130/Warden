# Warden 自动标签策略 V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于冻结 `auto_labels.json` 的 **角色定位、边界、允许输出族与非目标**。
- 本文档 **不重写** `Warden_Dataset_Output_Frozen_Spec_v1.1.md` 中已经冻结的精确字段名、枚举或落盘结构。
- 若涉及精确字段名、枚举、生成来源、兼容性或历史事实，以英文版与冻结规格为准。
- 本文档的目标不是再造一份 schema 表，而是防止 `auto / rule / manual` 三层职责漂移。
- 当前 repo 活跃版本为 `Warden_AUTO_LABEL_POLICY_V1.md`，并与 `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`、`Warden_RULE_LABEL_POLICY_V1_CORE.md`、`Warden_MANUAL_LABEL_POLICY_V1_CORE.md` 保持对齐。

# Warden 自动标签策略 V1

## 1. 文档目的

本文件用于回答以下问题：

1. `auto_labels.json` 在 Warden 中到底是什么；
2. `auto` 负责什么，不负责什么；
3. `auto` 与 `rule_labels.json`、`manual_labels.json` 的边界是什么；
4. `auto` 允许输出哪些类型的弱标签；
5. 后续补标、训练、推理和人工审核应如何理解 `auto`。

本文件是 **角色与边界文档**，不是新的字段冻结总表。精确字段和枚举仍以冻结规格为准。
当前 repo 内以本文件作为 `auto` 层活跃版本，不再并行保留独立 `_ALIGNED` 活跃副本。

## 2. 定位

### 2.1 `auto_labels.json` 的定位

`auto_labels.json` 是：

- 建立在当前 capture 输出之上的 **evidence-first weak layer**；
- 默认由 crawler inline 或 offline backfill 生成的自动弱标签层；
- 用于把 **当前页面状态下** 的已观察证据组织成统一的机器可读结构；
- 服务于：
  - TrainSet V1 的默认弱标签输入；
  - L0/L1 的低成本证据读取；
  - 离线 rule backfill；
  - 样本分桶、统计、manifest 派生与错误分析。

它不是：

- 人工金标层；
- 最终真值层；
- 处理建议层；
- 页面角色最终裁决层；
- `threat_taxonomy_v1` 的最终承载层。

### 2.2 与 `rule_labels.json` 的区别

默认理解：

- `auto` = **what was observed on the page**
- `rule` = **given those observations, what does the sample more likely represent and how should it be handled**
- `manual` = **final adjudication**

也就是说：

- `auto` 负责“观察到什么”；
- `rule` 负责“这些观察组合起来更像什么、该怎么处理”；
- `manual` 负责“最终到底是什么”。

### 2.3 与 `manual_labels.json` 的区别

`manual_labels.json` 负责：

- 最终判断；
- 最终高风险动作类；
- 最终页面角色；
- 最终品牌伪装认定；
- 最终是否纳入 training / evaluation / auxiliary。

`auto_labels.json` 不负责这些最终裁决。

## 3. 设计原则

### 3.1 `auto` 先回答“观察”，再允许有限的弱候选

`auto` 的第一职责是表达页面观察证据。

因此 `auto` 的主体应优先围绕：

- URL 结构；
- 表单结构；
- HTML / JS / captcha / download 证据；
- 品牌相关弱信号；
- 页面当前状态下的 intent / evasion 弱候选；
- 轻量网络摘要；
- 弱风险输出。

### 3.2 `auto` 可以有 candidate，但 candidate 仍然属于弱语义

`auto` 可以输出例如：

- `page_stage_candidate`
- `language_candidate`
- `credential_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `needs_interaction_candidate`

但这些 candidate 仍然只是：

- 页面级弱候选；
- 观察导向的启发式结果；
- 不是最终 threat class；
- 不是最终路由结论。

### 3.3 `auto` 不能越界成 `rule`

以下做法应被视为越界：

- 在 `auto` 中引入 `page_role_hint`；
- 在 `auto` 中引入 `review_priority`；
- 在 `auto` 中引入 `needs_manual_review_candidate`；
- 在 `auto` 中引入 `guardrail_*` / `conflict_*` 家族；
- 在 `auto` 中直接承载 `threat_taxonomy_v1`；
- 在 `auto` 中把观察事实直接包装成最终处理建议。

### 3.4 `auto` 不能替代人工真值

`auto` 允许：

- 弱候选；
- 弱风险分数；
- 启发式 reasons；
- 页面阶段与语言的粗候选。

但默认不允许：

- 把 `label_hint` 当人工真值；
- 把 `risk_level_weak` 当最终恶意判定；
- 把 candidate 字段提升为默认 gold label；
- 用 `auto` 直接替代 `manual`。

## 4. 默认输入来源

`auto_labels.json` 的生成可读取以下冻结上游工件：

- `meta.json`
- `url.json`
- `forms.json`
- `net_summary.json`
- `visible_text.txt`
- `html_rendered.html`
- `html_raw.html`（必要时回退）
- `diff_summary.json`（若存在，可用于部分 evasion 相关候选）

说明：

- `auto` 不应依赖未来的人工作业作为默认前置条件；
- `auto` 的默认输入应始终优先基于当前成功样本目录中的冻结工件；
- 若某些增强工件不存在，应降级输出，而不是静默伪造事实。

## 5. 顶层输出族

本文件不重新冻结精确 schema，但确认 `auto` 的顶层输出族应保持以下角色分层：

### 5.1 元信息与生成元数据

例如：

- `schema_version`
- `generated_at_utc`
- `source`
- `label_hint`
- `page_stage_candidate`
- `language_candidate`

### 5.2 观察型特征族

例如：

- `url_features`
- `form_features`
- `html_features`
- `network_features`

这些字段的目标是：

- 记录当前页面状态下可解析的事实；
- 服务于后续训练、统计、manifest 与 rule backfill；
- 尽量避免把高层结论直接塞进低层观察族。

### 5.3 弱信号族

例如：

- `brand_signals`
- `intent_signals`
- `evasion_signals`

这些字段的目标是：

- 表达页面当前状态下的弱候选；
- 明确这些结论仍是 candidate / heuristic；
- 为 rule 层提供稳定输入，而不是替代 rule 层。

### 5.4 弱风险输出族

例如：

- `risk_outputs`

这层的目标是：

- 汇总低成本弱风险信号；
- 提供统一的可排序可筛选输出；
- 为 manifest、抽样、人工队列和 rule 层提供参考。

## 6. `auto` 允许表达什么

### 6.1 当前页面状态下的观察事实

允许。

例如：

- host 是否为 IP；
- path 是否 login-like；
- 是否存在 password / otp / card 表单证据；
- 是否存在 captcha/download 证据；
- 第三方域、POST 目标、网络异常数量；
- 文本与 URL 中的品牌 token 命中。

### 6.2 当前页面状态下的弱意图候选

允许。

例如：

- `credential_intent_candidate`
- `otp_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `personal_info_intent_candidate`
- `download_intent_candidate`

### 6.3 当前页面状态下的弱规避候选

允许。

例如：

- `captcha_present_candidate`
- `dynamic_redirect_candidate`
- `cloak_suspected_candidate`
- `anti_bot_or_cloaking_candidate`
- `variant_failed_candidate`
- `needs_interaction_candidate`

### 6.4 轻量弱风险分数与原因

允许。

例如：

- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`

但必须明确：

- 这是弱风险输出；
- 不是最终恶意裁决；
- 不能机械替代 review priority 或 final label。

## 7. `auto` 明确不负责什么

`auto_labels.json` 默认不负责：

- `page_role_hint`
- `review_priority`
- `rule_reasons`
- `guardrail_*`
- `conflict_*`
- `needs_l2_candidate`
- `needs_manual_review_candidate`
- `hard_negative_candidate`
- `hard_positive_candidate`
- `threat_taxonomy_v1`
- 最终 high-risk action class
- 最终 scenario label
- 最终 page role
- 最终 dataset admission decision

这些属于 `rule` 或 `manual` 的职责范围。

## 8. 与 `rule_labels.json` 的接口边界

### 8.1 `rule` 可以读取 `auto`，但不应简单重命名 `auto`

无效的 rule 设计包括：

- 仅把 `risk_level_weak` 离散成 `review_priority`；
- 仅把 `claimed_brands` 改写成 `primary_threat_label_candidate`；
- 仅按 `auto` 总分做二次包装，不看证据结构。

### 8.2 `rule` 应在 `auto` 之上新增组合解释

`rule` 应重点表达：

- guardrails
- conflicts
- page role
- escalation routing
- weak candidate taxonomy

这意味着：

- `auto` 保持 observation-first；
- `rule` 保持 decision-support；
- 两层不应互相复制等价字段。

### 8.3 `threat_taxonomy_v1` 留在 `rule`

当前项目方向下：

- `threat_taxonomy_v1` 应保留在 `rule_labels.json` 中；
- 它是长期活跃的弱标签命名空间；
- 但仍保持 candidate / weak-candidate-only 语义；
- 默认不直接写入 TrainSet V1 primary manifest 核心字段。

## 9. 与 TrainSet V1 的关系

### 9.1 `auto` 是 TrainSet V1 默认弱标签来源

TrainSet V1 的默认 label layer 是 `auto_labels.json`。

因此：

- `auto` 需要保持稳定、统一、可批量生成；
- `auto` 的缺失会直接影响主训练样本纳入；
- `auto` 应优先保证全量成功样本的一致覆盖。

### 9.2 `rule` 是增强层，不是主训练前置要求

`rule_labels.json`：

- 不是 TrainSet V1 primary 的必需文件；
- 推荐通过 unified offline backfill 统一补齐；
- 适合承担 review、routing、page role 和 candidate taxonomy。

### 9.3 `manual` 是增强层，而非默认前置

`manual_labels.json`：

- 可用于高质量子集、验证集、hard-case 分析；
- 但不应阻塞主训练集生产。

## 10. 生成策略

### 10.1 默认生成路径

`auto_labels.json` 默认应由：

- crawler inline
- 或 offline backfill

统一生成。

### 10.2 统一覆盖优先于局部新花样

若新功能只覆盖新样本、却让旧样本长期没有对应 `auto` 结构，应优先考虑：

- 是否需要统一 backfill；
- 是否会破坏全量统计、manifest、训练与 review 的一致性。

### 10.3 当前实现即数据真相

若旧草稿与当前真实输出不一致，以当前实现和冻结规格为准。

## 11. 当前非目标

以下内容不属于本文件冻结范围：

- `auto_labels.json` 全字段实现细节的逐项重写；
- 新 threat ontology 的完整枚举；
- 最终人工标签体系的完整冻结；
- rule 层的完整 guardrail / conflict 规则表；
- 训练 target 的最终映射。

## 12. 演进规则

### 12.1 允许后续扩展的方向

后续允许扩展：

- 更稳的 observed feature extraction
- 更稳的 candidate signals
- 更细但仍然弱语义的 risk reasons
- 更统一的 offline backfill 一致性

### 12.2 当前应保持稳定的边界

当前应保持稳定：

- `auto = evidence-first weak layer`
- `rule = decision-support weak layer`
- `manual = final adjudication layer`
- `threat_taxonomy_v1` 留在 `rule` 而不是 `auto`
- `page_role_hint` / `review_priority` 留在 `rule` 而不是 `auto`
- `auto` 不直接替代 final truth

## 13. Definition of Done

`Warden_AUTO_LABEL_POLICY_V1.md` 可以视为完成，当且仅当：

- `auto` 的核心定位明确；
- 与 `rule` / `manual` 的边界明确；
- `auto` 允许输出的字段族与语义层级明确；
- `auto` 当前非目标明确；
- 与 frozen spec、TrainSet V1、rule policy 不冲突。

### 原始中文说明

中文内容保留在前，供人工协作与快速导览。英文版为权威版本。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Auto Label Policy V1

## 1. Purpose

This document defines the **role, boundary, allowed output families, and non-goals** of `auto_labels.json` in Warden.
It is the active in-repo `auto` policy doc and stays aligned with `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`, `Warden_RULE_LABEL_POLICY_V1_CORE.md`, and `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`.

It answers the following questions:

1. what `auto_labels.json` is supposed to be;
2. what `auto` is responsible for and what it is not;
3. how `auto` differs from `rule_labels.json` and `manual_labels.json`;
4. what kinds of weak outputs `auto` is allowed to emit;
5. how later backfill, training, inference, and review should interpret `auto`.

This document is a **role-and-boundary policy**, not a replacement schema specification. Exact field names, enums, and on-disk structure remain governed by the frozen dataset-output specification.

## 2. Role

### 2.1 Role of `auto_labels.json`

`auto_labels.json` is:

- an **evidence-first weak layer** built on top of the frozen capture outputs;
- the automatically generated weak-label artifact produced by crawler inline generation or offline backfill;
- the layer that organizes observations from the **current page state** into a stable machine-readable structure;
- intended to support:
  - TrainSet V1 as the default weak-label source;
  - low-cost L0/L1 evidence consumption;
  - offline rule backfill;
  - sample bucketing, statistics, manifest derivation, and error analysis.

It is not:

- a human gold-label layer;
- a final truth layer;
- a handling-hint layer;
- a final page-role layer;
- the primary home of `threat_taxonomy_v1`.

### 2.2 Difference from `rule_labels.json`

Default interpretation:

- `auto` = **what was observed on the page**
- `rule` = **given those observations, what does the sample more likely represent and how should it be handled**
- `manual` = **final adjudication**

In practice:

- `auto` describes what was observed;
- `rule` adds higher-level handling interpretation;
- `manual` performs the final decision.

### 2.3 Difference from `manual_labels.json`

`manual_labels.json` is responsible for:

- final judgment;
- final high-risk action class;
- final page role;
- final brand-impersonation decision;
- final admission into training / evaluation / auxiliary subsets.

`auto_labels.json` is not responsible for those final decisions.

## 3. Design Principles

### 3.1 Observation first, limited candidates second

The first job of `auto` is to encode page observations.

Therefore the center of `auto` should remain focused on:

- URL structure;
- form structure;
- HTML / JS / CAPTCHA / download evidence;
- weak brand-related evidence;
- current-page-state intent and evasion candidates;
- lightweight network summary;
- weak risk outputs.

### 3.2 Candidates are allowed, but they remain weak semantics

`auto` may emit fields such as:

- `page_stage_candidate`
- `language_candidate`
- `credential_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `needs_interaction_candidate`

These fields are still:

- page-level weak candidates;
- heuristic outputs;
- not final threat classes;
- not final routing decisions.

### 3.3 `auto` must not expand into `rule`

The following should be treated as out of scope for `auto`:

- `page_role_hint`
- `review_priority`
- `rule_reasons`
- `guardrail_*`
- `conflict_*`
- `needs_l2_candidate`
- `needs_manual_review_candidate`
- `hard_negative_candidate`
- `hard_positive_candidate`
- `threat_taxonomy_v1`
- final high-risk action labels
- final scenario labels
- final page-role labels
- final dataset-admission decisions

### 3.4 `auto` must not replace human truth

`auto` may contain:

- weak candidates;
- weak risk scores;
- heuristic reasons;
- coarse stage and language candidates.

But it must not, by default:

- treat `label_hint` as human truth;
- treat `risk_level_weak` as the final malicious verdict;
- promote candidate fields into gold labels;
- replace the `manual` layer.

## 4. Default Input Sources

`auto_labels.json` may read from the following frozen upstream artifacts:

- `meta.json`
- `url.json`
- `forms.json`
- `net_summary.json`
- `visible_text.txt`
- `html_rendered.html`
- `html_raw.html` as fallback
- `diff_summary.json` when present for some evasion-related candidates

Important implications:

- `auto` should not depend on future manual work as a default precondition;
- `auto` should prefer the current successful-sample frozen artifacts as its upstream inputs;
- if enhancement artifacts are missing, `auto` should degrade gracefully rather than fabricate observations.

## 5. Output Families

This document does not re-freeze the exact schema, but it freezes the semantic output families that `auto` is allowed to contain.

### 5.1 Metadata and generation metadata

Examples include:

- `schema_version`
- `generated_at_utc`
- `source`
- `label_hint`
- `page_stage_candidate`
- `language_candidate`

### 5.2 Observation-oriented feature families

Examples include:

- `url_features`
- `form_features`
- `html_features`
- `network_features`

These families exist to:

- record parseable facts from the current page state;
- support training, statistics, manifest generation, and rule backfill;
- avoid pushing higher-level handling conclusions into low-level observation families.

### 5.3 Weak signal families

Examples include:

- `brand_signals`
- `intent_signals`
- `evasion_signals`

These families exist to:

- express weak page-state candidates;
- keep those outputs explicitly heuristic;
- provide stable inputs to `rule` rather than replacing `rule`.

### 5.4 Weak risk output family

Example:

- `risk_outputs`

This family exists to:

- summarize low-cost weak risk signals;
- provide sortable and filterable weak outputs;
- support manifest derivation, sample triage, review ordering, and later rule derivation.

## 6. What `auto` Is Allowed To Express

### 6.1 Current-page-state observed facts

Allowed.

Examples include:

- whether the host is an IP;
- whether the path is login-like;
- whether password / OTP / card-related form evidence exists;
- whether CAPTCHA or download evidence exists;
- third-party domains, POST targets, and network anomalies;
- brand-token hits from text and URL.

### 6.2 Current-page-state weak intent candidates

Allowed.

Examples include:

- `credential_intent_candidate`
- `otp_intent_candidate`
- `payment_intent_candidate`
- `wallet_connect_intent_candidate`
- `personal_info_intent_candidate`
- `download_intent_candidate`

### 6.3 Current-page-state weak evasion candidates

Allowed.

Examples include:

- `captcha_present_candidate`
- `dynamic_redirect_candidate`
- `cloak_suspected_candidate`
- `anti_bot_or_cloaking_candidate`
- `variant_failed_candidate`
- `needs_interaction_candidate`

### 6.4 Lightweight weak risk scores and reasons

Allowed.

Examples include:

- `risk_score_weak`
- `risk_level_weak`
- `risk_reasons`

But these must remain:

- weak risk outputs;
- not final malicious verdicts;
- not direct substitutes for review priority or final labels.

## 7. What `auto` Is Explicitly Not Responsible For

`auto_labels.json` is not responsible for:

- `page_role_hint`
- `review_priority`
- `rule_reasons`
- `guardrail_*`
- `conflict_*`
- `needs_l2_candidate`
- `needs_manual_review_candidate`
- `hard_negative_candidate`
- `hard_positive_candidate`
- `threat_taxonomy_v1`
- final high-risk action classes
- final scenario labels
- final page-role labels
- final dataset-admission decisions

Those belong to `rule` or `manual`.

## 8. Interface Boundary With `rule_labels.json`

### 8.1 `rule` may read `auto`, but must not merely rename it

Invalid rule design includes:

- mapping `risk_level_weak` directly into `review_priority`;
- converting `claimed_brands` directly into `primary_threat_label_candidate`;
- re-packaging the auto weak score without looking at evidence structure.

### 8.2 `rule` must add combination-level interpretation

`rule` should primarily express:

- guardrails
- conflicts
- page role
- escalation routing
- weak candidate taxonomy

That means:

- `auto` remains observation-first;
- `rule` remains decision-support;
- the two layers should not duplicate semantically equivalent fields.

### 8.3 `threat_taxonomy_v1` stays in `rule`

Under the current project direction:

- `threat_taxonomy_v1` should remain inside `rule_labels.json`;
- it is a long-lived active weak-label namespace;
- it still keeps candidate / weak-candidate-only semantics;
- it should not be inlined into the TrainSet V1 primary manifest by default.

## 9. Relationship With TrainSet V1

### 9.1 `auto` is the default weak-label source

TrainSet V1 uses `auto_labels.json` as the default label layer.

Therefore:

- `auto` should remain stable, unified, and batch-producible;
- missing `auto` directly affects primary train-set admission;
- `auto` should prioritize broad and consistent coverage across the successful corpus.

### 9.2 `rule` is an enhancement layer

`rule_labels.json`:

- is not a required TrainSet V1 primary dependency;
- is recommended as a unified offline backfill artifact;
- is a natural home for review, routing, page-role, and candidate-taxonomy logic.

### 9.3 `manual` is an enhancement layer, not a default prerequisite

`manual_labels.json`:

- may support high-quality subsets, validation sets, and hard-case analysis;
- should not block production of the main training set.

## 10. Generation Policy

### 10.1 Default generation path

`auto_labels.json` should be generated by:

- crawler inline generation;
- or unified offline backfill.

### 10.2 Unified coverage matters more than isolated new features

If a new `auto` improvement only covers new samples while older samples remain structurally behind, the project should first ask:

- whether unified backfill is needed;
- whether inconsistent coverage will break statistics, manifest generation, training, or review.

### 10.3 Current implementation remains the data truth

If older drafts differ from the real current output, the current implementation and frozen spec win.

## 11. Current Non-Goals

The following are not goals of this policy:

- re-listing every exact implementation field of `auto_labels.json`;
- freezing a new threat ontology here;
- fully freezing the final human-label schema;
- freezing the full rule-layer guardrail and conflict table;
- defining the final training-target mapping.

## 12. Evolution Rules

### 12.1 Directions that may expand later

Later expansion is allowed for:

- more robust observed feature extraction;
- more stable candidate signals;
- richer but still weak-semantic risk reasons;
- more unified offline-backfill consistency.

### 12.2 Boundaries that should remain stable now

The following boundaries should remain stable:

- `auto = evidence-first weak layer`
- `rule = decision-support weak layer`
- `manual = final adjudication layer`
- `threat_taxonomy_v1` stays in `rule`, not `auto`
- `page_role_hint` / `review_priority` stay in `rule`, not `auto`
- `auto` does not directly replace final truth

## 13. Definition of Done

`Warden_AUTO_LABEL_POLICY_V1.md` can be treated as complete only if:

- the core role of `auto` is explicit;
- the boundary with `rule` and `manual` is explicit;
- the allowed semantic output families of `auto` are explicit;
- the current non-goals are explicit;
- the policy does not conflict with the frozen dataset-output spec, TrainSet V1, or rule policy.
