# MODULE_INFER.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Inference 模块的默认职责。
- 涉及阶段路由、阈值和部署输出时，以英文版为准。
- 当前 V1 离线实验口径是 `Processed Valid Dataset -> Evidence Pack Builder -> L1`。旧 `L0` / `L0-fast` 只作为 runtime compatibility 或 future online/wild-test 的 cheap screening / scope admission 辅助，不是当前 V1 模型主线。
- 当前 auto-label 参考实现的活动 L0 逻辑位于 `src/warden/module/l0.py`，`scripts/labeling/Warden_auto_label_utils_brandlex.py` 保留兼容入口与顶层编排职责。
- 当前 auto-label 参考实现的默认 L0 热路径已收窄：默认不做完整 `HTML` 特征提取，也不做默认 `brand` 提取；相关字段保留为兼容默认值，非 specialized 页面默认继续交给 `L1`。

## 1. 模块作用

Inference 模块负责运行期判断流程，包括阶段路由、阈值应用、运行时输出、导出与性能相关路径。
它的关注点是线上或准线上推理行为，而不是训练阶段的数据重标或 schema 改写。
本模块采用项目级 V1 公式：`Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)`，其中 `InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation`。未观察到 payload / action 应表达为 `payload not observed`，不应在推理文档中自动等同于 benign；该状态本身也不足以构成 V1 malicious。

## 2. 责任边界

- 拥有：runtime pipeline、stage routing、threshold application、export / benchmark / deployment path。
- 不拥有：训练集重标、训练期目标定义和数据层结构重构。
- 当前推荐 V1 离线实验流：`Processed Valid Dataset` 进入 `Evidence Pack Builder`，再进入 `L1` 主判断、训练和评估。未来 online / wild-test 流保留 `Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1`。OCR / YOLO 只作为 L1 内部 evidence-insufficient 时的 trigger-based visual evidence recovery。Future heavier review or escalation may be defined later，但本文档不定义当前在线 `L2` 架构。
- `early low-risk exit` 只是路由结果，不是真值安全结论；运行时输出应显式保留这种 routing outcome 语义。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# MODULE_INFER.md

# Warden Inference Module Specification

## 1. Module Purpose

The Inference module defines how Warden performs runtime webpage social-engineering threat judgment
using staged logic, bounded cost, explicit routing, and auditable outputs.

This module is responsible for online or offline inference-time decision flow.
It must preserve the current V1 model/dataflow refocus and must not silently absorb training-time assumptions as runtime truth.

At the project-definition level, Warden V1 uses `Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)`, where `InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation`. Inference documentation and outputs should avoid treating "no payload observed" as automatic benign. When manipulative context is present but no credential/payment/wallet/download/POST/action payload is observed, the state should be represented as `payload not observed` and routed according to evidence sufficiency and stage rules; that state alone is not sufficient for a V1 malicious judgment.

---

## 2. Core Responsibility

The Inference module owns:

- runtime input preparation
- evidence-pack construction and L1 execution policy
- threshold application
- review / routing policy
- inference-time structured output
- runtime evidence packaging
- model/runtime loading
- benchmark and deployment entrypoints
- export / packaging logic for deployment targets where applicable

The Inference module does not own:

- raw sample collection policy
- dataset schema redesign
- weak-label ontology redesign
- training loss design
- paper result narration

---

## 3. Inference Philosophy

### 3.1 Evidence-pack-first L1 judgment, not monolithic guessing

Warden V1 inference and experiments are evidence-pack-first by design.

Default expectation:

- Current offline experiment: `Processed Valid Dataset -> Evidence Pack Builder -> L1 Main Judgment / L1 Training / L1 Evaluation -> Metrics / Evidence Ledger / Ablation`
- Future wild-test / online inference: `Raw URL -> Capture Pipeline -> Capture QA / V1 Scope Admission -> Evidence Pack Builder -> L1 Main Judgment -> Wild-Test Report`
- L1: main judgment layer, including evidence-pack construction, text / HTML / URL / forms first pass, trigger-based vision evidence recovery, structured / joint signals, fusion, evidence ledger, and deterministic explanation rendering
- Future heavier review or escalation may be defined later; this document does not define a current online L2 architecture.
- Legacy L0 code paths, if present, are compatibility screening / routing support and not the current V1 default model/dataflow mainline.

### 3.2 Runtime cost discipline

Inference is constrained by runtime cost.
Expensive logic must not be silently pushed into early stages.

### 3.3 Explicit routing

Stage transitions must remain explainable.
A sample should be able to answer:

- why it stayed at L0
- why it escalated to L1
- why L1 requested trigger-based vision evidence recovery or later review
- what evidence or threshold triggered routing

### 3.4 Auditable outputs

Inference outputs must remain inspectable and not collapse into opaque single-value mystery decisions.

### 3.4.1 Behavior/action distinction

Inference reasoning should preserve the distinction between:

- ManipulativeContext: deceptive identity, trust, authority, institution, security, financial, support, reward, brand, or access-control context construction;
- InducedHighRiskAction: direct action, routed action, or action-preparation evidence involving credential, OTP, payment, wallet, PII/KYC, download, fake-support diversion, account verification, or attack-chain redirect behavior;
- payload not observed: no current evidence of a form, POST, wallet flow, payment flow, download flow, or other direct action component.

This distinction is conceptual in this task. It does not introduce new output fields or change existing runtime schemas.

### 3.5 Current runtime-flow interpretation

The current recommended V1 flow starts with evidence-pack construction for processed valid samples. This does not implement new runtime behavior in this documentation task.

At the module-contract level, the intended flow is:

1. current offline experiments read from `Processed Valid Dataset`;
2. build a source-aware evidence pack;
3. run `L1`, with text / HTML / URL / forms first;
4. trigger OCR / YOLO only when L1 evidence is insufficient;
5. preserve future online / wild-test flow as `Raw URL -> Capture -> QA / Scope Admission -> Evidence Pack Builder -> L1`.

Legacy `L0-fast` or L0 router terminology may remain in current code and compatibility docs, but it is not the V1 default model/dataflow entrypoint after this refocus.

For the current auto-label-backed reference path, the active L0 implementation lives in `src/warden/module/l0.py`, while `scripts/labeling/Warden_auto_label_utils_brandlex.py` remains the compatibility entrypoint and top-level orchestration layer.

In the current narrowed default hot path for that reference implementation:

- full `HTML` feature extraction is skipped by default;
- default `brand` extraction is skipped by default;
- `html_features` and `brand_signals` remain present with compatibility-safe default values;
- non-specialized pages should normally continue toward evidence-pack construction and `L1`, while legacy L0 code stays focused on cheap `gambling / adult / gate` specialized screening, exclusion, and routing hints. These hints are not V1 primary threat classes.

---

## 4. Allowed Runtime Inputs

Depending on deployment mode, inference may use some or all of the following:

- runtime screenshot input
- visible text input
- URL input
- form-structure-derived runtime features
- network summary or lightweight network features when supported
- cached or precomputed structured features
- model outputs from lower stages

The runtime input contract must be explicit for each inference path.

---

## 5. Stage Responsibility Rules

### 5.1 L0 rules

L0 is the cheapest stage.
It may be implemented as an embedded `L0-fast` runtime sub-path inside the broader pipeline, but it still remains the official `L0` stage in module semantics.

Default responsibilities:

- obvious `gambling / adult / gate` specialized-surface recall for auxiliary routing, exclusion, or future-scope handling
- obvious benign filtering only if policy explicitly allows
- simple structured/rule signals
- cheap URL, visible-text/title, form-summary, network-summary, and existing cheap diff/evasion-observability evidence
- initial escalation candidate generation
- observability-aware routing when cheap evidence is missing, including raw visible-text missing cases
- early low-risk exit only as an explicit routing outcome under sufficient low-risk evidence

Strict rules:

- do not make full `HTML` feature extraction part of the default L0 hot path
- do not make default `brand` extraction part of the default L0 hot path
- do not make screenshot/OCR or image-lite evidence a default L0 prerequisite
- do not perform gate solving, click-through recovery, or interaction recovery inside L0
- do not silently add heavy model inference to L0
- do not bury most of the system cost in L0
- do not make L0 routing opaque
- do not reinterpret embedded `L0-fast` as `L1-fast`
- do not treat `early_stop_low_risk` as a ground-truth safety claim

### 5.2 L1 rules

L1 is the stronger middle stage and the current main judgment layer.
Its current framework definition is maintained in `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`.
At the module level, L1 should be treated as a staged main-judgment shell rather than a monolithic model.

Default responsibilities:

- text-first main judgment by default
- stronger semantic/structural judgment
- source-aware evidence bundle construction from `SampleContext`
- structured semantic concept and relation-judgment outputs for downstream fusion
- conditional multimodal supplementation when text-only judgment is insufficient
- visual evidence recovery and localization when cheap/text/HTML/action evidence is sparse, conflicting, or low-confidence
- fusion over text concepts, structured features, joint signals, OCR-recovered text, and YOLO-localized UI evidence
- deterministic explanation rendering from evidence ledger entries and reason codes
- richer consistency checks
- more reliable main-stage judgment for samples that stop at L1
- review or future-escalation hinting without defining a current L2 stage

Strict rules:

- keep L1 purpose distinct from L0
- do not let L1 become a copy of L0 with different thresholds
- do not let L1 become effectively “always final” unless explicitly intended
- do not reinterpret conditional multimodal supplementation as a separate official stage
- do not treat CLIP or any page-level visual similarity encoder as a standalone malicious / benign judge
- do not put CLIP, MobileCLIP, SNet, or SpecularNet-like routes into the Warden V1 default path
- do not treat action surfaces such as login, download, payment, wallet, support, or redirect as automatically malicious without risky behavior context or inherently high-risk action patterns
- do not document draft L1 output terms as frozen machine-readable schema without a later explicit schema task

### 5.3 Future heavier review or escalation

Future heavier review or escalation may be defined later in a separate accepted task.
This module does not define a current online L2 architecture, L2 schema, L2 routing contract, or L2 implementation requirement.

Until such a task exists, hard gate, evasion, interaction-heavy, high-ambiguity, or signal-conflict valid webpage cases should be represented through explicit review / future-escalation hints and evidence-ledger reason codes. Recrawl must not be emitted as a current L0 / L1 threat-model route.

---

## 6. Routing Rules

### 6.1 Routing must be explicit

Every inference path must have a documented routing rule, threshold, or trigger family.

### 6.2 Routing trigger families

Possible trigger families include:

- low confidence
- conflicting signals
- high-risk rule flags
- sensitive intent + mismatch indicators
- evasion/cloaking indicators
- quality issues requiring stronger stage
- empty or missing raw visible-text observability that prevents a trustworthy cheap-stage stop

The exact triggers may vary by implementation, but they must be explicit.

### 6.3 No silent routing drift

Do not silently change routing thresholds, escalation logic, or trigger families without reporting it.

### 6.4 Routing output expectations

The inference result should be able to expose at least:

- final stage reached
- whether escalation happened
- why escalation happened
- final risk output
- optional intermediate stage summary

### 6.5 Early exit semantics

Any early low-risk stop at `L0` remains a routing decision under the currently observed evidence and active policy thresholds.
It must not be documented or exposed as a final ground-truth safety statement.
Downstream output should preserve this distinction explicitly.

---

## 7. Threshold Rules

### 7.1 Thresholds are policy, not hidden magic

Thresholds used for:

- benign / risk decision
- escalation
- review recommendation
- confidence gating

must be explicit and documented.

### 7.2 Threshold change control

Any threshold change that affects behavior materially must be reported.

Do not hide threshold changes inside code defaults.

### 7.3 Calibration awareness

If calibrated scores are not guaranteed, do not overstate confidence semantics.
Use language appropriate to actual model behavior.

---

## 8. Runtime Output Rules

### 8.1 Output purpose

Inference outputs must support:

- downstream product logic
- offline audit
- error analysis
- benchmarking
- optional human review routing

### 8.2 Output requirements

A non-trivial inference output should be able to express:

- sample or request identifier
- final risk decision or risk level
- routing outcome/status, especially when distinguishing an `early low-risk exit` from a stronger final benign judgment
- score or confidence if available
- final stage
- escalation path
- evidence summary or reason codes
- optional review recommendation
- optional model/runtime metadata

### 8.3 Explainability discipline

Do not reduce all behavior to a single opaque scalar if reason codes or stage reasoning exist.

### 8.4 Stable output contract

If inference output is consumed by downstream tooling, its contract must remain stable unless explicitly versioned.

---

## 9. Runtime Feature Preparation Rules

### 9.1 Runtime feature extraction must remain bounded

Feature extraction at inference time must be cost-aware and explicit.

### 9.2 No hidden dependency explosion

Do not silently add heavyweight preprocessing or unsupported runtime dependencies to a deployment path.

### 9.3 Missing feature handling

If a runtime feature is unavailable:

- fallback behavior must be explicit
- degraded mode must be explicit
- stage-routing consequences must be explicit

Silent fallback is not allowed.

When raw visible text is empty or materially missing, the default safe behavior is to treat that as a routing-quality problem.
By default, `L0` should avoid low-risk early stop and prefer sending the sample to `L1` for fuller-content judgment.
This remains a routing semantic rather than a direct risk label.

---

## 10. Deployment and Packaging Rules

### 10.1 Deployment target awareness

Inference code may support multiple deployment forms, for example:

- local Python runtime
- exportable model artifact
- ONNX / TensorRT / mobile/edge variant where explicitly supported

The deployment target must be explicit.

### 10.2 Packaging discipline

Export or packaging code must not silently change model behavior or preprocessing semantics.

### 10.3 Resource constraint discipline

If a deployment target has constraints such as:

- memory
- latency
- CPU-only
- mobile/edge runtime
- batch-size limitations

those constraints must be documented and respected.

---

## 11. Benchmark Rules

### 11.1 Benchmark purpose

Benchmarking exists to measure runtime behavior, not to fabricate pretty numbers.

### 11.2 Benchmark dimensions

Where relevant, benchmark reporting should separate:

- latency
- throughput
- memory usage
- stage distribution
- escalation rate
- accuracy / recall tradeoff at policy thresholds

### 11.3 No mixed-condition benchmark claims

Do not compare incompatible runtime settings without stating the differences.

Examples:

- different hardware
- different precision modes
- different batch sizes
- different routing thresholds
- different preprocessing pipelines

---

## 12. Inference Module Non-Goals

This module must not:

- redesign frozen dataset schema
- silently redefine label semantics
- silently import training-only assumptions as runtime truth
- silently collapse staged routing into one opaque branch
- silently change public output contract
- silently change deployment dependencies
- fabricate benchmark results

---

## 13. Validation Requirements

For any non-trivial Inference module change, validate at least:

1. runtime input preparation works on a smoke sample
2. L0 path works if touched
3. L1 path works if touched
4. routing behavior works on at least a small representative set if routing changed
5. output structure matches documented expectations
6. deployment/export path works if export logic changed
8. benchmark command still runs if benchmark logic changed

If any validation is not run, state exactly what was not run and why.

---

## 14. Compatibility Rules

The Inference module must explicitly report compatibility impact when changing:

- runtime input assumptions
- routing logic
- thresholds
- output schema
- export format
- deployment dependency requirements

Breaking changes require:

- explicit approval
- versioning or migration plan
- downstream consumer impact note

---

## 15. Required Reporting for Inference Changes

Every non-trivial change must explicitly state:

- what stage behavior changed
- whether routing changed
- whether thresholds changed
- whether output contract changed
- whether deployment assumptions changed
- whether benchmark semantics changed
- whether docs need update

---

## 16. Definition of Done

An Inference module task is Done only if:

- requested runtime behavior is implemented
- staged responsibility remains clear
- routing/threshold impact is stated
- validation is stated honestly
- compatibility impact is stated
- risks are stated
- documentation impact is stated

