# MODULE_INFER.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Inference 模块的默认职责。
- 涉及阶段路由、阈值和部署输出时，以英文版为准。

## 1. 模块作用

Inference 模块负责运行期判断流程，包括阶段路由、阈值应用、运行时输出、导出与性能相关路径。
它的关注点是线上或准线上推理行为，而不是训练阶段的数据重标或 schema 改写。

## 2. 责任边界

- 拥有：runtime pipeline、stage routing、threshold application、export / benchmark / deployment path。
- 不拥有：训练集重标、训练期目标定义和数据层结构重构。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# MODULE_INFER.md

# Warden Inference Module Specification

## 1. Module Purpose

The Inference module defines how Warden performs runtime webpage social-engineering threat judgment
using staged logic, bounded cost, explicit routing, and auditable outputs.

This module is responsible for online or offline inference-time decision flow.
It must preserve the staged L0 / L1 / L2 philosophy and must not silently absorb training-time assumptions as runtime truth.

---

## 2. Core Responsibility

The Inference module owns:

- runtime input preparation
- stage routing
- L0 / L1 / L2 execution policy
- threshold application
- escalation policy
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

### 3.1 Staged judgment, not monolithic guessing

Warden inference is staged by design.

Default expectation:

- L0: cheap, fast, high-recall screening
- L1: stronger semantic / structural judgment
- L2: highest-cost escalation for hard or high-risk cases

### 3.2 Runtime cost discipline

Inference is constrained by runtime cost.
Expensive logic must not be silently pushed into early stages.

### 3.3 Explicit routing

Stage transitions must remain explainable.
A sample should be able to answer:

- why it stayed at L0
- why it escalated to L1
- why it escalated to L2
- what evidence or threshold triggered escalation

### 3.4 Auditable outputs

Inference outputs must remain inspectable and not collapse into opaque single-value mystery decisions.

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

Default responsibilities:

- obvious risk recall
- obvious benign filtering only if policy explicitly allows
- simple structured/rule signals
- cheap text/URL/image-lite evidence
- initial escalation candidate generation

Strict rules:

- do not silently add heavy model inference to L0
- do not bury most of the system cost in L0
- do not make L0 routing opaque

### 5.2 L1 rules

L1 is the stronger middle stage.

Default responsibilities:

- stronger semantic/structural fusion
- moderate-cost multimodal reasoning
- richer consistency checks
- more reliable intermediate judgment
- escalation filtering toward L2

Strict rules:

- keep L1 purpose distinct from both L0 and L2
- do not let L1 become a copy of L0 with different thresholds
- do not let L1 become effectively “always final” unless explicitly intended

### 5.3 L2 rules

L2 is the highest-cost stage.

Default responsibilities:

- ambiguous difficult cases
- high-risk cases needing stronger evidence
- conflict resolution across signals
- hard evasion or edge cases

Strict rules:

- do not route everything to L2 by laziness
- do not use L2 as a dumping ground for broken routing
- do not hide why escalation happened

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
4. L2 path works if touched
5. routing behavior works on at least a small representative set if routing changed
6. output structure matches documented expectations
7. deployment/export path works if export logic changed
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

