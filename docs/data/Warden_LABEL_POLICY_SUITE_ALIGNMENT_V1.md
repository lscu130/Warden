# Warden 标签策略对齐说明 V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文件用于把 `auto / rule / manual` 三份策略文档对齐成一组。
- 本文件不是字段冻结总表，也不替代单份 policy 文档。
- 若涉及精确字段名、枚举、角色边界或覆盖策略，以英文版和各对应 policy 正文为准。
- 当前 repo 活跃套件为 `Warden_AUTO_LABEL_POLICY_V1.md`、`Warden_RULE_LABEL_POLICY_V1_CORE.md`、`Warden_MANUAL_LABEL_POLICY_V1_CORE.md`。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Label Policy Suite Alignment V1

## 1. Purpose

This document aligns the current Warden label-policy suite:

- `Warden_AUTO_LABEL_POLICY_V1.md`
- `Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`

The goal is to make sure the three layers do not drift semantically.
These are the active in-repo policy docs after repository alignment.
The temporary per-layer `_ALIGNED` source copies should not remain as separate active versions once this suite note has been merged into the stable filenames.

## 2. Frozen Layer Interpretation

The suite freezes the following layer interpretation:

- `auto` = **evidence-first weak layer**
- `rule` = **decision-support weak layer**
- `manual` = **final adjudication layer**

This means:

- `auto` answers: what was observed on the page;
- `rule` answers: given those observations, what does the sample more likely represent and how should it be handled;
- `manual` answers: what the sample is finally judged to be.

## 3. Shared Primary Threat Family

The aligned primary threat family shared across:
- `rule -> threat_taxonomy_v1 -> primary_threat_label_candidate`
- `manual -> manual_primary_threat_label`

is:

- `credential_theft`
- `payment_fraud`
- `wallet_drain_or_web3_approval_fraud`
- `pii_kyc_harvesting`
- `fake_support_or_contact_diversion`
- `malware_or_fake_download`
- `benign`
- `uncertain`

Rule keeps these as weak candidates.
Manual keeps these as final adjudicated primary threat labels.

## 4. Shared Scenario Family

The aligned scenario family is:

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

These describe outer shell / vertical, not the final harmful action.

## 5. Shared Page-Role Family

The aligned page-role family shared across:
- `rule -> page_role_hint`
- `manual -> manual_page_role`

is:

- `benign_service_page`
- `benign_idp_redirect`
- `direct_attack_page`
- `hosted_lure`
- `intermediary_carrier`
- `gate_or_evasion_shell`
- `download_lure`
- `other`
- `uncertain`

`auto` must not directly own page-role fields.

## 6. Coverage Strategy Alignment

The suite freezes the following coverage strategy:

- `auto_labels.json` should remain broad and consistent across the successful corpus whenever practical;
- `rule_labels.json` should be produced as unified offline backfill for the successful corpus whenever practical;
- `manual_labels.json` is **not** a default full-corpus requirement.

Manual coverage should prioritize:

- gold evaluation subsets,
- hard cases,
- conflict-heavy samples,
- policy-sensitive samples,
- representative/canonical samples when cluster/subcluster exists.

## 7. Final-Judgment vs Warning Separation

The suite freezes the separation between:

- final threat judgment, and
- content warning / sensitive-vertical warning.

At the current stage:

- adult / gambling should not become a third main threat class;
- content warning remains a separate warning axis in `manual`;
- `rule` may later support candidate-level warning tags, but this is not required in the current frozen v1-core set.

## 8. Non-Goals

This alignment document does not:
- redefine the frozen dataset-output contract,
- fully enumerate long-tail scenario or narrative ontologies,
- require full-corpus manual annotation,
- turn rule into final truth,
- move `threat_taxonomy_v1` into `auto`.

## 9. Conclusion

The suite should be interpreted as one coherent stack:

- `auto` provides the broad observed evidence layer,
- `rule` adds handling-oriented weak interpretation at corpus scale,
- `manual` provides selective high-value final adjudication.

The three documents should be reviewed and edited together whenever one layer's semantics changes.
