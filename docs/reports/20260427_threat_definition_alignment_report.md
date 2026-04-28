# Threat Definition Alignment Report

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

本次对齐把 Warden 的项目定义从偏“高危动作”补充为“高危欺骗行为和/或高危诱导动作”。本次只改 Markdown 文档，不改代码、schema、CLI、JSON 输出或机器可读枚举。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version.

# 20260427 Threat Definition Alignment Report

## 1. Files Searched

Required governing docs read:

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Repository searches run:

- `rg -n "social-engineering|social engineering|phishing|brand phishing|threat judgment|high-risk action|high risk action|高风险动作|社会工程|社工|钓鱼|品牌钓鱼|诱导用户|高危动作|高危行为|仿冒|冒充" --glob "*.md" .`
- `rg -n "whether .* perform|whether .* execute|诱导.*执行|诱导.*输入|索取密码|wallet authorization|payment details|credential" --glob "*.md" .`

Focused files reviewed:

- `README.md`
- `PROJECT.md`
- `AGENTS.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`

## 2. Files Changed

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/modules/MODULE_INFER.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/tasks/20260427_warden_threat_definition_behavior_action_v1.md`
- `docs/reports/20260427_threat_definition_alignment_report.md`
- `docs/handoff/20260427_threat_definition_behavior_action_v1.md`

## 3. Actual Diff Evidence

Tracked-file diff summary from `git diff --stat`:

- `AGENTS.md`: 6 added lines
- `PROJECT.md`: 17 changed lines
- `README.md`: 29 changed lines
- `docs/modules/MODULE_INFER.md`: 13 added lines
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`: 10 added lines
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`: 36 changed lines
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`: 10 added lines
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`: 23 changed lines
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`: 38 changed lines
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`: 12 changed lines

Repository-local new files are untracked until staged, so they do not appear in `git diff --stat`:

- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/tasks/20260427_warden_threat_definition_behavior_action_v1.md`
- `docs/reports/20260427_threat_definition_alignment_report.md`
- `docs/handoff/20260427_threat_definition_behavior_action_v1.md`

`git status --short --untracked-files=all` confirms the changed set is Markdown-only.

## 4. Old Wording Pattern Found

The main old pattern was action-only or action-dominant wording:

- Warden as judging whether a page induces a dangerous user action.
- Primary threat labels described only through final high-risk action.
- Missing sensitive-collection evidence described in ways that could be misread as a benign guardrail.

## 5. New Wording Pattern Applied

The canonical definition now states:

**Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.**

The docs now explicitly state that:

- high-risk deceptive behavior can itself be malicious;
- payload/action absence should be represented as `payload not observed`;
- `payload not observed` is not automatic benign;
- brand evidence is supportive and contextual, not a universal one-factor rule;
- existing schemas and enum names remain unchanged.

## 6. Residual Search Hits Classification

Post-edit searches still find `high-risk action` / `高风险动作` style text. These are not all defects. They fall into four categories:

- Current canonical definition and entry docs: action wording is now paired with high-risk deceptive behavior, for example `PROJECT.md`, `README.md`, `AGENTS.md`, and `docs/frozen/Warden_Threat_Definition_V1.md`.
- Compatibility-preserved label fields and enum descriptions: `final high-risk action class`, `最终高风险动作类`, and action-oriented primary label wording remain in `Warden_AUTO_LABEL_POLICY_V1.md`, `Warden_RULE_LABEL_POLICY_V1_CORE.md`, `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`, `TRAIN_LABEL_DERIVATION_V1.md`, and `L0_DESIGN_V1.md` because this task explicitly forbids schema / enum changes.
- Historical records: older `docs/tasks/**` and `docs/handoff/**` hits are retained as historical task scopes or validation transcripts.
- Out-of-scope policy docs: `Warden_MALICIOUS_SOURCE_POLICY_V1.md` uses `high-risk actions` to describe source-feed diversity rather than the project-level threat definition, so it was not rewritten.

Active docs that previously risked action-only interpretation were updated to include one or more of:

- high-risk deceptive behavior;
- high-risk induced action;
- `payload not observed`;
- no automatic benign conclusion from missing payload.

## 7. Files Intentionally Not Changed

- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`: not changed because it freezes output structure and machine-readable schema examples. This task did not approve schema or enum edits.
- `docs/modules/MODULE_TRAIN.md`: reviewed, but it defines training module boundaries rather than threat semantics.
- `docs/data/TRAINSET_V1.md`: reviewed, but it defines dataset admission and manifest dependencies rather than project threat definition.
- Historical `docs/tasks/**` and `docs/handoff/**`: not bulk-edited because many hits are historical records, validation transcripts, or prior task scopes.
- Python files and JSON artifacts: not changed because they are outside scope.

## 8. Follow-Up Work

Potential future schema work should be handled in a separate task if desired:

- `malicious_basis`
- `high_risk_behavior_type`
- `high_risk_action_type`
- `payload_observed`
- teacher-label prompt updates for explicit behavior/action split
- evaluation buckets for behavior-only, action-only, both, benign high-risk action surface, and unresolved recrawl-needed cases
