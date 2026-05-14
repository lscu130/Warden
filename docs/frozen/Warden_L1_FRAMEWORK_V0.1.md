# Warden L1 Framework Definition V0.1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 摘要

本文档把 Warden 当前 L1 定义收敛为一个可实现但尚未实现的框架合同：

- L1 是主判断层，但不是单一模型的一锤定音。
- L1 消费从 `SampleContext` 派生的 source-aware evidence bundle。
- 所有有效且未被 L0 终止的网页样本都进入 L1；文本 / HTML / URL / forms / network / structured signals 是 L1 默认主证据路径。
- 文本塔学习结构化语义概念识别和关系判断，通过多任务头输出中间概念，而不是生成自由推理文本。
- 视觉路径是证据恢复和局部证据定位路径，不是独立最终威胁判断器。
- OCR 用于恢复截图文字；YOLO 用于定位原子 UI 证据；CLIP / MobileCLIP 不属于 Warden V1 默认在线 L1 路径，仅允许离线截图聚类、模板发现、ablation baseline、research-only visual-prior experiments，或未来另行批准的 optional feature flag。
- Fusion 把概念输出、结构化特征、joint signals 和视觉恢复证据合并成 L1 机器判断。
- L1 解释来自 evidence ledger、reason codes 和 deterministic explanation renderer，不来自 BERT、CLIP 或 XGBoost 的自由生成。

### 兼容性说明

本文档是定义更新，不是实现任务。它不改变代码、训练逻辑、CLI、冻结 schema、标签枚举或机器可读输出格式。本文档中列出的 L1 输出项和 head 名称均为 draft / proposed / conceptual terms，除非未来任务显式冻结 schema。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other execution agents must treat the English section below as authoritative. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden L1 Framework Definition V0.1

## 1. Purpose

This document defines the current Warden L1 framework direction for future implementation, data-labeling, distillation, evaluation, and documentation alignment.

It is a documentation definition update. It is not an implementation task and not a machine-readable schema freeze.

This document must stay compatible with:

- the official current `L0 / L1` staged runtime contract;
- `SampleContext` and lazy heavy-artifact discipline from the runtime/dataflow spec;
- the edge deployment profile that keeps trigger-based `PP-OCRv4 mobile` and `YOLO26n` in the default V1 online profile while excluding CLIP / MobileCLIP from that default path;
- the project threat definition: social-engineering threat equals high-risk deceptive behavior and/or high-risk induced action.

Routing precondition:

- Every valid webpage sample not terminated by L0 must route to L1.
- L1 text judgment is the default path.
- L1 vision is evidence recovery, not a parallel final classifier.
- Invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are removed during dataset cleaning before formal train / validation / test construction; they are not L1 threat labels.

## 2. L1 Position

L1 is Warden's main judgment stage.
It is not a monolithic classifier and should not be described as a single model that directly reads all raw artifacts and emits a final threat verdict.

Conceptual structure:

```text
L1 main judgment shell
  -> source-aware evidence pack builder
  -> text / HTML / URL / form / network main path
  -> structured feature and joint-signal branch
  -> visual evidence recovery path, requested only when needed
  -> fusion head or heads
  -> deterministic explanation renderer
```

L1 consumes a source-aware evidence bundle derived from `SampleContext`.
It may reference heavy artifacts lazily, but the default L1 contract should not embed full heavy payload bodies or make screenshot/OCR execution unconditional.

## 3. Text Tower Role

The L1 text tower is not expected to perform complete free-form human-like reasoning.
It should learn structured semantic concept recognition and relation judgments through multi-task heads.

The intended pattern is an implicit reasoning scaffold:

- the model does not output chain-of-thought;
- it outputs bounded intermediate concepts, relation judgments, risk axes, page roles, and routing hints;
- fusion combines those outputs with structured and visual evidence into the final L1 machine judgment.

The text path remains source-aware. It should preserve distinctions among visible text, selected HTML/DOM text, URL and redirect signals, forms, network summaries, and OCR-recovered auxiliary text when present.

## 4. Draft Text Multi-Task Head Groups

The following groups are draft design terms, not frozen schema fields.

### 4.1 Action Surface Heads

- `login_surface`
- `signup_surface`
- `payment_surface`
- `wallet_connect_surface`
- `download_surface`
- `support_contact_surface`
- `pii_collection_surface`
- `third_party_redirect_surface`

Action surfaces are not automatically threat actions.
A login form, download button, payment button, wallet connection button, support contact, or third-party redirect becomes threat-relevant only when combined with deceptive identity, manipulative narrative, suspicious destination, abnormal submission behavior, missing business legitimacy, missing context legitimacy, or another high-risk behavior context.

Some action patterns are inherently high-risk in untrusted contexts, including seed phrase or private key collection, remote-control installation lures, requests to disable security protections, and OTP collection in an untrusted context.

### 4.2 Behavior Context Heads

- `brand_impersonation_context`
- `authority_impersonation_context`
- `institution_impersonation_context`
- `fake_security_context`
- `fake_financial_context`
- `fake_reward_or_prize_context`
- `fake_support_context`
- `urgency_or_threat_context`
- `deceptive_hosted_brand_shell`

### 4.3 Relation / Consistency Heads

- `brand_domain_alignment`
- `brand_url_token_consistency`
- `claimed_brand_officiality`
- `action_target_alignment`
- `form_action_alignment`
- `download_target_alignment`
- `redirect_chain_reasonableness`
- `hosted_platform_context`

These heads should reduce false positives from one-factor rules. Brand-domain mismatch, visual similarity, login presence, download presence, or wallet presence must not become a universal malicious rule without supporting context.

### 4.4 Risk Axis Heads

- `human_exposure_risk`
- `deceptive_identity_risk`
- `observed_action_risk`
- `payload_deployment_risk`
- `brand_domain_conflict_risk`
- `evidence_incompleteness_risk`
- `evasion_or_gate_risk`

### 4.5 Page Role Heads

- `benign_clear`
- `benign_hard_negative`
- `brand_impersonation_landing_shell_without_payload_observed`
- `credential_collection_page`
- `payment_collection_page`
- `wallet_drain_or_web3_abuse_page`
- `fake_download_lure_page`
- `fake_support_page`
- `gate_or_evasion_shell`
- `intermediary_or_redirector`
- `unknown`

### 4.6 Routing Heads

- `need_vision`
- `need_human_review`
- `future_escalation_hint`

Routing heads are routing support signals. They are not final acceptance or ground-truth safety statements.

## 5. Visual Evidence Recovery Path

The L1 visual path is an evidence recovery and evidence localization path.
It is not an independent visual threat-judgment path and must not be treated as a standalone final malicious / benign judge.

The visual path should be requested when the active L1 path needs it, for example when:

- `visible_text.txt` is missing, empty, or sparse;
- effective visible text is below the active policy threshold, with V0.1 examples around `< 300` effective characters;
- HTML actionable structure is sparse;
- forms summary is missing but the screenshot appears interactive;
- SPA / React / Vue extraction is weak;
- L1 text confidence is low;
- text, URL, HTML, forms, or network evidence conflicts;
- L0 marks possible gate, evasion, or brand-surface conflict.

This trigger list is conceptual. Exact thresholds and trigger logic remain future implementation work.

## 6. OCR / YOLO / CLIP Responsibility Split

### 6.1 OCR

OCR recovers screenshot text when visible text and HTML-derived text are missing, sparse, image-rendered, or incomplete.
OCR remains trigger-based by default and must not become an unconditional bottleneck for every L1 sample.

### 6.2 YOLO

YOLO detects and localizes atomic UI evidence, such as:

- input boxes;
- password fields;
- OTP or code fields;
- card or payment fields;
- wallet/connect buttons;
- download buttons;
- QR codes;
- captcha or verify widgets;
- popups and modals;
- primary CTA buttons.

Detector classes should remain atomic and visually grounded.
They should not encode broad final concepts that require text, URL, destination, or policy context to interpret.

### 6.3 CLIP / MobileCLIP

CLIP-family image-text encoders, including MobileCLIP variants, are not part of the Warden V1 default online L1 path.

They are allowed only for:

- offline screenshot clustering;
- template discovery;
- ablation baselines;
- research-only visual-prior experiments;
- a future optional feature flag separately approved by a later task.

They must not:

- output the final `malicious / benign` judgment;
- act as a standalone visual threat classifier;
- replace OCR for text recovery;
- replace YOLO for local UI evidence localization;
- become a default online L1 input;
- treat page-level visual similarity as sufficient malicious evidence by itself.

## 7. Fusion

Fusion combines:

- text tower concept logits;
- relation, risk-axis, page-role, and routing logits;
- structured features;
- joint signals;
- OCR-recovered text evidence;
- YOLO-localized UI evidence.

If XGBoost is used as a fusion head, it should consume concept outputs, structured features, and joint signals.
It should not consume raw webpage text or raw screenshot pixels directly.

Draft / proposed / conceptual L1 machine outputs include:

```text
final_label:
  - benign
  - malicious
  - suspicious
  - unknown

malicious_basis:
  - no_malicious_evidence_observed
  - high_risk_behavior_observed
  - high_risk_action_observed
  - both_behavior_and_action_observed
  - insufficient_evidence

other outputs:
  - risk_score
  - confidence
  - payload_observed
  - page_role
  - risk_axes
  - routing decision
```

These terms are draft / proposed / conceptual, not frozen machine-readable schema.
A later schema task is required before these names become output-contract fields.

## 8. Explanation

L1 explanations are produced from an evidence ledger, reason codes, and a deterministic explanation renderer.

Student models such as BERT-style text encoders, CLIP-family visual encoders, YOLO detectors, and XGBoost fusion heads do not generate free-form explanations.
They activate concepts, scores, detections, and reason-code candidates.
The renderer converts evidence-grounded concepts into auditable summaries.

Preferred architecture:

```text
Evidence Pack Builder
  -> evidence ledger

Text / Vision / Structured branches
  -> concept outputs and reason-code candidates

Fusion
  -> final label, risk axes, page role, routing, top contributors

Explanation Renderer
  -> deterministic, evidence-grounded explanation
```

Evidence ledger entries should be able to record:

- source;
- claim;
- value;
- confidence when available;
- evidence ID;
- reason code;
- whether the evidence supports, limits, or conflicts with the final decision.

## 9. Compatibility And Non-Implementation Statement

This document changes documentation only.
It does not:

- modify Python code;
- modify model training logic;
- modify inference runtime logic;
- modify dataset files;
- modify label JSON files;
- rename frozen schema fields;
- rename labels or enums;
- add dependencies;
- change CLI behavior;
- change output JSON schema as an implemented contract;
- remove trigger-based `PP-OCRv4 mobile` or `YOLO26n` from the default online edge profile;
- claim runtime, accuracy, latency, or model-performance validation.

Future work is still required for:

- exact text multi-task training targets;
- exact OCR / YOLO trigger thresholds and any separately approved optional CLIP / MobileCLIP feature-flag threshold;
- final output schema;
- evaluation buckets;
- teacher distillation schema;
- implementation and benchmark validation.
