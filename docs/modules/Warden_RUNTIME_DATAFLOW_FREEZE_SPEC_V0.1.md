# Warden Runtime/Dataflow Freeze Spec V0.1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 中文摘要

本文档用于冻结 Warden 当前最小可执行的 runtime/dataflow 合同，服务于既有 `L0 / L1 / L2` 主线。

本版本先冻结以下内容：

- `ArtifactPackage` 负责什么，不负责什么；
- `SampleContext` 负责什么，不负责什么；
- 哪些工件属于 cheap evidence，应该每个 sample 只准备一次；
- 哪些工件属于 heavy artifacts，只能按需 lazy load；
- `L0 / L1 / L2` 的最小运行期输入/输出边界；
- runtime result / trace 应保留哪些最小审计信息；
- 哪些内容现在冻结，哪些内容仍保持可配置。

本版本不冻结：

- 最终 threat logic；
- 最终阈值；
- 最终 OCR / vision / multimodal 策略；
- 最终对外 CLI 规范；
- 最终 inference output 全字段 schema。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Runtime/Dataflow Freeze Spec V0.1

## 1. Purpose

This document freezes the minimum runtime/dataflow contract needed for near-term Warden implementation work while preserving the official top-level runtime structure as `L0 / L1 / L2`.

The goal is to stabilize:

- runtime object responsibilities;
- per-sample shared-state boundaries;
- cheap-vs-heavy artifact lifecycle discipline;
- minimum stage input/output expectations;
- audit-oriented result and trace retention;
- the line between frozen items and still-configurable items.

This is a runtime/dataflow contract.
It is not a final threat-logic specification and not a replacement for `MODULE_INFER.md`.

---

## 2. Top-Level Runtime Contract

The official runtime stage framing remains:

- `L0`: cheapest screening and routing stage;
- `L1`: main judgment stage;
- `L2`: highest-cost escalation / review stage.

This document does not introduce an alternative top-level taxonomy.
Implementation-local helper sub-stages may exist internally, but they must not replace the project-level `L0 / L1 / L2` contract.

---

## 3. Runtime Objects

### 3.1 `ArtifactPackage`

`ArtifactPackage` is the immutable per-sample artifact handle.

Responsibilities:

- point to the sample directory and known runtime-relevant artifacts;
- expose stable path-level access to frozen sample artifacts;
- expose artifact-presence information;
- provide safe readers for cheap JSON/text artifacts;
- provide lazy access hooks for heavy artifacts.

Non-responsibilities:

- no final threat judgment;
- no stage-policy decisions;
- no threshold ownership;
- no mutation of upstream frozen dataset artifacts.

Minimum expected artifact families:

- required sample identity artifacts:
  - `meta.json`
  - `url.json`
- cheap structured artifacts when present:
  - `forms.json`
  - `net_summary.json`
  - `diff_summary.json`
  - `auto_labels.json`
- cheap text artifact:
  - `visible_text.txt`
- heavy artifacts:
  - `html_rendered.json` or legacy `html_rendered.html`
  - `html_raw.json` or legacy `html_raw.html`
  - `screenshot_viewport.png`
  - `screenshot_full.png`
  - other future large payloads if later approved

### 3.2 `SampleContext`

`SampleContext` is the mutable per-sample runtime state shared across stages.

Responsibilities:

- store the current sample identity and primary URLs;
- hold shared cheap evidence prepared once per sample;
- hold stage trace entries;
- hold routing state across `L0 / L1 / L2`;
- hold runtime-only caches for lazy-loaded heavy artifacts;
- hold minimal result payload state before writeback;
- support explicit heavy-cache release after processing.

Non-responsibilities:

- no ownership of frozen dataset schema redesign;
- no ownership of label-schema redesign;
- no silent conversion of routing outcomes into final truth claims.

---

## 4. Cheap Evidence vs Heavy Artifacts

### 4.1 Cheap evidence

Cheap evidence should be prepared once per sample whenever practical and then reused across stages.

Current minimum cheap-evidence families:

- sample identity:
  - `sample_id`
  - sample directory
  - capture timestamp when present
- URL family:
  - input URL
  - final URL
  - cheap URL-derived features
- page metadata:
  - page title when present
  - label hint when present
- form family:
  - raw `forms.json` payload when present
  - summarized form features
- network/diff family when present:
  - `net_summary.json`
  - `diff_summary.json`
- text family:
  - `visible_text.txt`
  - cheap text observability status
- artifact presence family:
  - which key artifacts exist
  - which key artifacts are missing
- compatibility family:
  - existing `auto_labels.json` payload when present

The cheap-evidence layer may include L0-oriented observation preparation as long as:

- it remains runtime infrastructure rather than final label logic;
- it does not silently redefine frozen dataset schema;
- it does not force heavy artifacts to load eagerly.

### 4.2 Heavy artifacts

Heavy artifacts must stay lazy-loadable by default.

Current heavy-artifact families:

- rendered HTML payload;
- raw HTML payload;
- screenshot bytes;
- future larger runtime payloads explicitly marked as heavy.

Rules:

- heavy artifacts must not be loaded eagerly just because a sample entered the runtime shell;
- heavy-artifact access must be explicit and auditable;
- stages may request heavy artifacts on demand through `SampleContext`;
- heavy caches should be releasable after result/trace writeback.

---

## 5. Minimum Stage Contracts

### 5.1 `L0`

Minimum inputs:

- `ArtifactPackage`
- `SampleContext`
- shared cheap evidence

Minimum responsibilities:

- prepare or consume cheap observation-oriented evidence;
- produce routing-oriented weak outputs and reason codes;
- decide whether the sample can stop early under current policy or must continue.

Minimum outputs:

- stage name `L0`
- stage status
- routing reason codes
- next-stage decision among `STOP`, `L1`, or `L2`
- weak risk / specialized-surface / observability outputs when available

Strict boundary:

- `L0` runtime output may support routing, but it does not freeze final threat logic in this spec.

### 5.2 `L1`

Minimum inputs:

- `SampleContext` after `L0`
- shared cheap evidence
- an explicit `L1` main-judgment input bundle derived from the current sample state
- optional heavy artifacts requested lazily

Minimum responsibilities:

- act as the main judgment shell;
- request heavier evidence only when needed;
- preserve routing trace from `L0`;
- either complete the current runtime path or escalate to `L2`.

Minimum outputs:

- stage name `L1`
- stage status
- explicit routing outcome/status
- reason codes or notes explaining why the sample stayed or escalated
- placeholder or partial main-judgment outputs when final logic is not frozen yet
- next-stage decision among `STOP` or `L2`

Strict boundary:

- `L1` remains the main judgment stage by contract, but this document does not freeze final text/vision/multimodal policy detail.

#### Minimum `L1` main-judgment input bundle

The minimum `L1` main-judgment input bundle should expose at least:

- sample identity:
  - `sample_id`
  - `input_url`
  - `final_url`
- incoming routing context from the prior stage:
  - incoming stage
  - incoming stage status
  - incoming routing outcome
  - incoming reason codes
- cheap-evidence families needed for main judgment:
  - URL family
  - visible-text family
  - form-summary family
  - network-summary family when present
  - artifact-presence family
  - current auto-label family when present
- judgment-focus flags:
  - whether text-semantic follow-up is needed
  - whether vision follow-up is needed
  - whether higher-cost escalation is already hinted
- required heavy artifacts for this stage, if any
- missing required artifacts, if any

The bundle may contain summaries and references.
It should not embed full heavy payload bodies by default.

### 5.3 `L2`

Minimum inputs:

- `SampleContext` after prior stage trace
- an explicit `L2` high-cost review contract
- optional heavy artifacts requested lazily

Minimum responsibilities:

- serve as the highest-cost escalation shell;
- preserve why escalation happened;
- emit a review/deeper-analysis placeholder result even when final logic is still deferred.

Minimum outputs:

- stage name `L2`
- stage status
- explicit routing outcome/status
- escalation reason summary
- placeholder high-cost review result
- terminal routing decision

Strict boundary:

- `L2` is the highest-cost stage, but this document does not freeze the final interaction, OCR, or multimodal review policy.

#### Minimum `L2` high-cost review contract

The minimum `L2` high-cost review contract should expose at least:

- sample identity:
  - `sample_id`
  - `input_url`
  - `final_url`
- escalation context:
  - incoming stage
  - incoming stage status
  - incoming routing outcome
  - incoming escalation reason codes
- required cheap-evidence families that must remain available to review
- required heavy artifacts for review
- missing required heavy artifacts, if any
- review targets or review focus families
- output-contract constraints stating that routing semantics must remain distinguishable from final judgment semantics

---

## 6. Result and Trace Retention

The runtime shell should preserve two logical output views:

- a result payload for per-sample terminal output;
- a trace payload for stage-by-stage auditability.

Minimum result content:

- sample identity;
- input/final URL;
- final stage reached;
- terminal routing outcome/status;
- runtime notes or placeholder judgment outputs;
- artifact-presence summary.

Minimum trace content:

- ordered stage entries;
- per-stage status;
- per-stage routing outcome/status;
- per-stage input-contract summary;
- per-stage requested heavy-artifact list;
- reason codes or notes;
- whether heavy artifacts were requested.

Rules:

- trace must preserve routing semantics distinctly from final judgment semantics;
- heavy artifacts themselves should not be copied into runtime outputs by default;
- result and trace retention may store summaries, not full heavy payload bodies.

Concrete filenames remain implementation-local in V0.1 unless later frozen explicitly.

---

## 7. Frozen Items in V0.1

The following are frozen by this document:

- the official top-level runtime structure stays `L0 / L1 / L2`;
- `ArtifactPackage` is the immutable artifact-handle layer;
- `SampleContext` is the shared mutable per-sample runtime state layer;
- cheap evidence is prepared once per sample whenever practical;
- heavy artifacts are lazy-loaded on demand by default;
- routing trace must remain explicit and auditable;
- result payload and trace payload are both first-class runtime outputs at the logical level;
- runtime orchestration must stay separable from final business judgment logic.

---

## 8. Still Configurable in V0.1

The following remain configurable and are not frozen by this document:

- final threat-decision logic inside `L0`, `L1`, or `L2`;
- exact thresholds;
- exact OCR strategy;
- exact vision or multimodal supplementation policy;
- exact concrete output field expansion beyond the minimum logical families above;
- exact CLI contract for future public inference entrypoints;
- exact deployment/export packaging shape;
- exact heavy-artifact set beyond the currently named minimum families.

---

## 9. Compatibility Notes

- This document does not rename any frozen dataset artifact names.
- This document does not change label semantics.
- This document does not redefine the project-level stage taxonomy.
- Any later runtime implementation must remain additive/backward-compatible unless an explicit migration task says otherwise.

---

## 10. Implementation Mapping for the Current V0.1 Skeleton

The current V0.1 runtime/dataflow skeleton is expected to map this contract into:

- a runtime package under `src/warden/runtime/`;
- a thin local CLI under `scripts/infer/`;
- additive result/trace writeout for smoke validation.

Those paths are implementation choices for the current task, not a project-wide commitment that all future runtime entrypoints must follow.

---

## 11. Non-Goals

This document does not:

- freeze final inference output schema;
- freeze concrete model-selection policy;
- freeze final benign / malicious decision thresholds;
- redesign dataset contracts;
- redefine label taxonomy;
- replace `MODULE_INFER.md`.
