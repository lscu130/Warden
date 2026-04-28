# Warden Threat Definition Alignment Task V1

## 中文摘要（给人快速阅读）

本任务用于让 Codex 在 Warden 仓库内统一修改“社会工程威胁”的项目定义。

核心变更：

- 旧口径容易把 Warden 威胁定义压缩成“网页是否诱导用户执行高风险动作”。
- 新口径必须明确：**社会工程威胁 = 高危欺骗行为 和/或 高危诱导动作**。
- 页面即使暂时没有登录框、支付框、钱包授权、下载按钮、POST 提交等高危动作，只要已经出现高危欺骗行为，也可以构成 malicious。
- 高危欺骗行为包括但不限于：品牌仿冒、机构/权威身份冒充、伪安全上下文、伪金融上下文、伪客服上下文、伪奖励/空投上下文、欺骗性 gate/evasion。
- 高危诱导动作包括但不限于：凭证收集、OTP 收集、支付信息收集、钱包连接/助记词索取、PII/KYC 收集、恶意下载、假客服引流、攻击链跳转。
- 本任务只修改文档和项目定义，不修改代码、schema、CLI、数据文件、训练脚本或机器可读标签枚举。

Codex 执行时应先全文搜索仓库内旧定义，再做最小文档补丁，并输出 alignment report 与 handoff。

---

## English Version

> Authoritative section for AI execution. The Chinese section above is a human-readable summary only.

# Task Metadata

- Task ID: `TASK-20260427-THREAT-DEFINITION-BEHAVIOR-ACTION-V1`
- Task Title: Align Warden Threat Definition Around High-Risk Behavior and High-Risk Action
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: Project / Docs / Labeling / Inference
- Related Issue / ADR / Doc: `AGENTS.md`, `PROJECT.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, `docs/templates/HANDOFF_TEMPLATE.md`
- Created At: 2026-04-27
- Requested By: Project owner

---

## 1. Background

Warden is a webpage social-engineering threat judgment system. Current project wording in several places emphasizes whether a webpage induces the user to perform high-risk actions, such as credential entry, payment, wallet authorization, download, or personal-information submission.

That wording is incomplete for Warden's threat model.

A webpage can already be malicious when it performs high-risk deceptive behavior, even if a high-risk user action has not yet been observed in the captured evidence. For example, a page that strongly impersonates a bank or trusted service through visual layout, text, brand claim, and URL/domain context may already be executing a deceptive identity setup. The later credential/payment/wallet/download action may appear only after recrawl, interaction, delayed deployment, geofencing, device switching, or a later attack-chain step.

Therefore, Warden's project-level threat definition must be updated from an action-only framing to a behavior-and/or-action framing.

---

## 2. Goal

Update all relevant Warden project definitions so that Warden consistently defines a social-engineering threat as a webpage that exhibits high-risk deceptive behavior and/or induces, prepares, or routes the user toward high-risk actions.

The updated definition must preserve Warden's intent-driven, multimodal, staged design while avoiding two errors:

1. falsely treating "no observed sensitive form/action" as "not malicious";
2. reducing Warden to a simple brand-phishing or logo-matching detector.

---

## 3. Normative Definition To Apply

Use the following definition as the canonical project wording, with minor local wording adjustments allowed for readability:

> Warden defines a webpage social-engineering threat as a webpage that exhibits high-risk deceptive behavior and/or induces, prepares, or routes the user toward high-risk actions. High-risk deceptive behavior includes false or misleading identity, brand, authority, institution, security, financial, support, reward, or access-control context construction. Such behavior may be malicious even when no credential form, payment form, wallet flow, download, POST submission, or other high-risk action is currently observed. High-risk actions include attempts to collect credentials, OTP codes, payment details, wallet approvals or seed phrases, PII/KYC data, malicious downloads, fake-support contact diversion, or attack-chain redirects.

Short form:

> Social-engineering threat = high-risk deceptive behavior and/or high-risk induced action.

Required distinctions:

- `high-risk behavior`: the page constructs a deceptive identity, trust context, scenario, authority, brand surface, or access-control context.
- `high-risk action`: the page asks, routes, pressures, or enables the user to enter, approve, pay, download, contact, authorize, or otherwise perform a dangerous action.
- `payload not observed`: no currently captured form, POST, wallet flow, payment flow, download flow, or other high-risk action component is observed.
- `malicious by behavior`: the page is malicious because high-risk deceptive behavior is observed, even if payload/action is not yet observed.

---

## 4. Scope In

This task is allowed to touch documentation only.

Codex must search the repository and update relevant Markdown documentation that defines or summarizes Warden's threat model. Likely files include, but are not limited to:

- `README.md`
- `AGENTS.md`
- `PROJECT.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/MODULE_LABELING.md`
- `docs/modules/MODULE_TRAIN.md`
- `docs/modules/MODULE_DATA.md`
- `docs/data/TRAINSET_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- any existing L0/L1/L2 design documents that define Warden's threat target
- any existing label-policy documents that describe malicious / phishing / social-engineering semantics

This task is allowed to create one new documentation file if useful:

- `docs/frozen/Warden_Threat_Definition_V1.md`

This task is allowed to create a short alignment report:

- `docs/reports/20260427_threat_definition_alignment_report.md`

This task is allowed to create a handoff:

- `docs/handoff/20260427_threat_definition_behavior_action_v1.md`

---

## 5. Scope Out

This task must NOT do the following:

- Do not edit Python code.
- Do not edit dataset samples.
- Do not edit generated manifests.
- Do not rename frozen schema fields.
- Do not add, remove, or rename machine-readable label enums.
- Do not change CLI commands.
- Do not change training, inference, capture, labeling, or evaluation behavior.
- Do not modify JSON output formats.
- Do not merge Gate / Evasion auxiliary set into TrainSet V1 primary.
- Do not redefine benign taxonomy or malicious taxonomy as machine-readable schema in this task.
- Do not treat brand impersonation as the only kind of threat.
- Do not claim validation commands were run unless they were actually run.

If Codex finds that a code or schema change is needed to fully implement the new definition, it must document that as follow-up work only.

---

## 6. Inputs

### Docs

Codex must read these files before editing:

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Codex should then search for relevant definitions across all Markdown files.

### Search Terms

Use `rg` or equivalent repository search for at least the following terms:

```bash
rg -n "social-engineering|social engineering|phishing|brand phishing|threat judgment|high-risk action|high risk action|高风险动作|社会工程|社工|钓鱼|品牌钓鱼|诱导用户|高危动作|高危行为|仿冒|冒充" .
```

Also search for wording that implies action-only threat definitions:

```bash
rg -n "whether .* perform|whether .* execute|诱导.*执行|诱导.*输入|索取密码|wallet authorization|payment details|credential" .
```

### Prior Context

The project owner has decided that Warden's threat definition must include both:

- high-risk deceptive behavior;
- high-risk induced action.

The Easybank-like case is the motivating example: a page may lack credential/payment/wallet payload in the current capture, but still be malicious when it strongly constructs deceptive brand identity and trust context.

---

## 7. Required Outputs

This task must produce:

1. Updated documentation files with aligned threat definitions.
2. If created, `docs/frozen/Warden_Threat_Definition_V1.md` containing the canonical definition.
3. `docs/reports/20260427_threat_definition_alignment_report.md`, listing:
   - files searched;
   - files changed;
   - old wording pattern found;
   - new wording pattern applied;
   - files intentionally not changed and why.
4. `docs/handoff/20260427_threat_definition_behavior_action_v1.md`, aligned with `HANDOFF_TEMPLATE.md`.
5. Final Codex response with:
   - Summary;
   - Files Changed;
   - Key Definition Changes;
   - Validation Performed;
   - Compatibility Impact;
   - Risks / Caveats;
   - Recommended Next Step.

---

## 8. Hard Constraints

Must obey all of the following:

- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Use `docs/templates/TASK_TEMPLATE.md` boundaries.
- Produce handoff content aligned with `docs/templates/HANDOFF_TEMPLATE.md`.
- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output formats.
- Do not add third-party dependencies.
- Prefer minimal documentation patches over broad rewrites.
- If a Markdown document has Chinese and English sections, update both sections.
- English remains authoritative for exact project semantics.
- Preserve the staged L0 / L1 / L2 system view.
- Preserve the distinction between raw evidence, weak labels, manual labels, model outputs, and project definitions.
- Preserve the principle that brand evidence is important support evidence but not the entire Warden task.
- Do not make "brand mismatch alone" an automatic universal malicious rule without context.

Task-specific constraints:

- Replace action-only definitions with behavior-and/or-action definitions.
- Keep the definition broad enough for non-brand social-engineering threats.
- Explicitly state that high-risk deceptive behavior can be malicious even when high-risk action/payload is not observed.
- Explicitly state that absence of observed payload should be represented as `payload not observed`, not as automatic benign.
- Treat deceptive identity / brand / authority / institution / security / financial / support / reward context construction as high-risk behavior categories.
- Treat credential / OTP / payment / wallet / PII/KYC / download / fake-support diversion / attack-chain redirect as high-risk action categories.

---

## 9. Interface / Schema Constraints

Public interfaces that must remain stable:

- Existing CLI commands.
- Existing JSON output schemas.
- Existing manifest fields.
- Existing label field names.
- Existing machine-readable enum names unless a future schema task explicitly changes them.

Schema / field constraints:

- Schema changed allowed: NO
- Machine-readable label enum changed allowed: NO
- Public output format changed allowed: NO
- Documentation wording changed allowed: YES

Downstream consumers to watch:

- manifest generation scripts;
- label backfill scripts;
- TrainSet V1 admission logic;
- inference routing logic;
- L1 training/evaluation documentation;
- future teacher-label prompt documents.

Compatibility plan:

- This task updates project definitions only.
- Any required machine-readable schema addition, such as `malicious_basis`, `high_risk_behavior_type`, or `high_risk_action_type`, must be documented as a future task, not implemented here.

---

## 10. Suggested Execution Plan

Recommended order:

1. Read the governing docs:
   - `AGENTS.md`
   - `PROJECT.md`
   - `docs/workflow/GPT_CODEX_WORKFLOW.md`
   - `docs/templates/TASK_TEMPLATE.md`
   - `docs/templates/HANDOFF_TEMPLATE.md`
2. Run repository-wide `rg` searches for old threat definitions and action-only wording.
3. Create a short list of files that actually contain threat-definition wording.
4. Update the most authoritative docs first:
   - `PROJECT.md`
   - `AGENTS.md`
   - `README.md`
5. Update relevant module/data/label/infer docs where they repeat or depend on the old definition.
6. If useful, create `docs/frozen/Warden_Threat_Definition_V1.md`.
7. Add an alignment report under `docs/reports/`.
8. Add a handoff under `docs/handoff/`.
9. Run validation searches to confirm no old action-only definition remains as the sole definition.
10. Report any unresolved documents, ambiguous wording, or follow-up schema needs.

---

## 11. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] The canonical threat definition includes high-risk deceptive behavior and high-risk induced action.
- [ ] Documentation no longer frames Warden threats solely as high-risk user actions.
- [ ] Documentation explicitly states that high-risk deceptive behavior may be malicious even when payload/action is not currently observed.
- [ ] Documentation preserves the role of high-risk actions such as credential, OTP, payment, wallet, PII/KYC, download, support diversion, and attack-chain redirects.
- [ ] Documentation preserves Warden's broader scope beyond narrow brand phishing.
- [ ] Documentation does not turn brand mismatch into a universal one-factor rule.
- [ ] No code was edited.
- [ ] No schema or machine-readable label enum was changed.
- [ ] No CLI or output format was changed.
- [ ] Chinese and English sections are both updated when a bilingual file is touched.
- [ ] `docs/reports/20260427_threat_definition_alignment_report.md` exists and lists searched / changed / unchanged files.
- [ ] `docs/handoff/20260427_threat_definition_behavior_action_v1.md` exists and states validation actually performed.
- [ ] Final Codex response includes compatibility impact and risks.

---

## 12. Validation Checklist

Minimum validation commands:

```bash
git status --short
```

Search for old action-only definitions:

```bash
rg -n "high-risk action|high risk action|高风险动作|高危动作|诱导用户执行|诱导.*高风险|诱导.*高危" README.md AGENTS.md PROJECT.md docs
```

Search for required new concepts:

```bash
rg -n "high-risk deceptive behavior|high-risk induced action|behavior and/or action|deceptive identity|payload not observed|高危欺骗行为|高危诱导动作|高危行为" README.md AGENTS.md PROJECT.md docs
```

Confirm no non-doc files changed:

```bash
git diff --name-only
```

The diff should only include Markdown documentation files unless the project owner explicitly approves otherwise.

Optional Markdown sanity check if a markdown linter already exists in the repo:

```bash
# Only run if already configured in the repository.
# Do not add a new dependency for this task.
```

---

## 13. Expected Definition Examples

Use these examples to guide wording. Do not necessarily paste all examples into every document.

### Example A: Malicious by behavior, payload not observed

A page strongly impersonates a bank or trusted brand through visual layout, text, logo/header context, and URL/domain context. No login form, payment form, wallet flow, download link, POST submission, or suspicious redirect is currently observed.

Expected wording:

- malicious basis: high-risk deceptive behavior observed;
- high-risk action: not observed;
- page role: brand/institution impersonation landing shell without payload observed;
- not ordinary benign;
- may require recrawl or L2 depending on policy.

### Example B: Malicious by behavior and action

A page impersonates Microsoft, PayPal, a bank, a wallet, or a government service and asks for password, OTP, payment details, wallet approval, seed phrase, PII/KYC, fake support contact, or download.

Expected wording:

- malicious basis: both high-risk behavior and high-risk action observed;
- page role: credential/payment/wallet/download/fake-support threat page;
- action/payload risk is high.

### Example C: Benign high-risk action surface

A legitimate official service has login, MFA, payment, checkout, account recovery, or support forms on an aligned official domain and normal flow.

Expected wording:

- high-risk action surface may exist;
- malicious behavior is not observed;
- domain/action/context alignment matters;
- do not treat login/payment/support alone as malicious.

---

## 14. Follow-Up Work To Document, Not Implement

If relevant docs mention future schemas or teacher outputs, Codex may add TODO notes for future tasks, but must not implement them in this task.

Possible future task items:

- Add conceptual or machine-readable fields such as:
  - `malicious_basis`
  - `high_risk_behavior_type`
  - `high_risk_action_type`
  - `payload_observed`
  - `deceptive_identity_risk`
- Update teacher-label prompt templates to output behavior/action split.
- Update L1 evaluation buckets to include:
  - malicious by behavior only;
  - malicious by action only;
  - malicious by both behavior and action;
  - benign high-risk action surface;
  - suspicious unresolved / recrawl-needed.
- Update benign and malicious folder taxonomy docs after the definition is frozen.

These are out of scope for the current task unless explicitly approved later.

---

## 15. Codex Final Delivery Format

Codex must finish with this structure:

```text
Summary
- ...

Files Changed
- ...

Key Definition Changes
- ...

Validation Performed
- ...

Compatibility Impact
- ...

Risks / Caveats
- ...

Recommended Next Step
- ...
```

For non-trivial changes, Codex must also provide the handoff file path and confirm whether it follows `HANDOFF_TEMPLATE.md`.
