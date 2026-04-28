# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

本次交付完成了 Warden 社会工程威胁定义对齐：项目定义现在明确包含“高危欺骗行为”和“高危诱导动作”两类依据。页面即使当前未观察到 payload / action，也可能因高危欺骗行为构成 malicious。本次只修改 Markdown 文档，没有改代码、schema、CLI、输出格式或机器可读枚举。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version.

# Handoff Metadata

- Handoff ID: 20260427-threat-definition-behavior-action-v1
- Related Task ID: TASK-20260427-THREAT-DEFINITION-BEHAVIOR-ACTION-V1
- Task Title: Align Warden Threat Definition Around High-Risk Behavior and High-Risk Action
- Module: Project / Docs / Labeling / Inference
- Author: Codex
- Date: 2026-04-27
- Status: PARTIAL_ACCEPTED_PENDING_DIFF_REVIEW

---

## 1. Executive Summary

Aligned Warden's project-level threat definition around high-risk deceptive behavior and/or high-risk induced action.

The change clarifies that a page can be malicious by high-risk deceptive behavior even when no current credential form, payment form, wallet flow, download, POST submission, or other direct payload is observed.

Acceptance note:

- User/GPT web review status: accept partial.
- Reason: direction and handoff scope are acceptable, but final acceptance needs actual diff review and more detailed alignment-report evidence.
- Follow-up performed in this handoff: added diff-stat evidence and residual search-hit classification to `docs/reports/20260427_threat_definition_alignment_report.md`.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added the canonical frozen threat definition document.
- Updated project entry and governance docs to include the behavior/action definition.
- Updated inference and label-policy docs so `payload not observed` is not treated as automatic benign.
- Added a repository copy of the externally provided task document.
- Added this handoff and the alignment report.

### Output / Artifact Changes

- none

---

## 3. Files Touched

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

---

## 4. Behavior Impact

### Expected New Behavior

- Documentation now defines social-engineering threat as high-risk deceptive behavior and/or high-risk induced action.
- Documentation now states that `payload not observed` is not automatic benign.
- Label-policy docs preserve existing schemas while describing how behavior-only cases should be handled conceptually.

### Preserved Behavior

- No Python behavior changed.
- No CLI behavior changed.
- No schema, field name, or machine-readable enum changed.
- L0 / L1 / L2 staged design remains preserved.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The change is documentation-only. Future fields such as `malicious_basis`, `high_risk_behavior_type`, `high_risk_action_type`, or `payload_observed` were documented as possible follow-up work, not implemented.

---

## 6. Validation Performed

### Commands Run

```bash
rg -n "social-engineering|social engineering|phishing|brand phishing|threat judgment|high-risk action|high risk action|高风险动作|社会工程|社工|钓鱼|品牌钓鱼|诱导用户|高危动作|高危行为|仿冒|冒充" --glob "*.md" .
rg -n "whether .* perform|whether .* execute|诱导.*执行|诱导.*输入|索取密码|wallet authorization|payment details|credential" --glob "*.md" .
git status --short
rg -n "high-risk action|high risk action|高风险动作|高危动作|诱导用户执行|诱导.*高风险|诱导.*高危" README.md AGENTS.md PROJECT.md docs
rg -n "high-risk deceptive behavior|high-risk induced action|behavior and/or action|deceptive identity|payload not observed|高危欺骗行为|高危诱导动作|高危行为" README.md AGENTS.md PROJECT.md docs
git diff --name-only
git diff --stat
git status --short --untracked-files=all
```

### Result

- Repository definition searches were run before edits.
- Post-edit validation searches were run and recorded in the final response.
- `git diff --name-only` was checked to confirm only tracked Markdown documentation files changed.
- `git diff --stat` was checked for tracked-file edit scale.
- `git status --short --untracked-files=all` was checked because new task/report/handoff/frozen docs are untracked before staging and therefore do not appear in `git diff --name-only`.
- Residual old-wording hits were classified in the alignment report as compatibility-preserved fields, historical records, canonical action-category references, or out-of-scope source-policy wording.

### Not Run

- code tests
- schema validation
- CLI smoke tests

Reason:

This task was documentation-only and explicitly forbade code, schema, CLI, dataset, and output-format changes.

---

## 7. Risks / Caveats

- Some historical tasks and handoffs still contain old action-only wording as historical records.
- Existing machine-readable schemas do not yet have explicit fields for behavior/action split or payload-observed state.
- Some bilingual legacy files contain mojibake in older Chinese sections; this task added readable Chinese update summaries where direct full Chinese rewrite would have created unnecessary churn.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- listed in Section 3

Doc debt still remaining:

- future schema or teacher-prompt docs may need updates if behavior/action split becomes machine-readable.

---

## 9. Recommended Next Step

- Run GPT web or human review against the task acceptance checklist.
- Create a separate schema task if Warden should add machine-readable fields for `malicious_basis`, `high_risk_behavior_type`, `high_risk_action_type`, or `payload_observed`.
