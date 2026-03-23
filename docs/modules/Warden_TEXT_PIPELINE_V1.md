# Warden_TEXT_PIPELINE_V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden_TEXT_PIPELINE_V1

## 1. Module Purpose

This document defines the V1 text-side pipeline for Warden.

The Text pipeline is responsible for converting webpage-visible language and near-text structural signals into auditable, deployment-friendly textual evidence for Warden L1 fusion.

The Text pipeline is not a standalone final judge and must remain consistent with Warden's staged inference philosophy.

---

## 2. Scope

This document defines:

- text-side runtime inputs
- V1 default text encoder selection
- text evidence construction policy
- structured side-feature usage
- deployment and performance positioning
- what V1 explicitly freezes
- what V1 intentionally leaves open

This document does not define:

- dataset schema redesign
- label ontology redesign
- final risk decision thresholds
- L2 heavy reasoning logic
- paper-facing result narration

---

## 3. Alignment with Current Repository Data Contract

The Text pipeline must be built around text and structured files already produced by current Warden samples.

### 3.1 Primary text input

- `visible_text.txt`

This is the default text-side primary source and should be treated as the main runtime textual channel.

### 3.2 Auxiliary text-capable inputs

- OCR output from screenshots
- `html_raw.html`
- `html_rendered.html`

These are useful, but they should not automatically replace the primary text channel.

### 3.3 Structured side inputs

- `forms.json`
- `url.json`
- `redirect_chain.json`
- `net_summary.json`
- selected metadata fields where applicable

### 3.4 Practical consequence

The V1 Text pipeline is designed as:

- visible-text-first
- OCR-aware, but not OCR-dependent
- structure-aware
- multilingual by default
- embedding-plus-fusion oriented

---

## 4. Design Principles

### 4.1 Evidence extraction, not chat-style interpretation

The Text pipeline should extract bounded textual evidence, not produce free-form agent-like narration at runtime.

Typical outputs include:

- text embeddings
- bounded concept scores
- source-aware token statistics
- high-risk phrase flags
- text quality and sparsity flags
- escalation hints

### 4.2 Multilingual-first default

Warden V1 should assume real deployment may encounter multilingual webpages.
The default text encoder should therefore be multilingual by default rather than English-only.

### 4.3 Source-aware text handling

Different text sources must not be flattened carelessly into one undifferentiated string.

At minimum, the pipeline should preserve the distinction between:

- visible DOM-derived text
- OCR-recovered screenshot text
- URL and redirect textual signals
- form and network-derived structured evidence

### 4.4 Bounded runtime cost

The Text pipeline must be compatible with ordinary PCs and modest enterprise or x86 edge environments.
It should not rely on a large autoregressive LLM in the default runtime path.

### 4.5 Default deployability with fine-tuning retained

Warden V1 should be deployable with an off-the-shelf multilingual encoder.
At the same time, the design keeps task-specific fine-tuning and calibration available for later Warden-owned data.

This means:

- the default path works without mandatory fine-tuning
- Warden-specific fine-tuning remains allowed
- concept-layer calibration and task adaptation remain first-class extensions, not forbidden changes

---

## 5. V1 Runtime Inputs

### 5.1 Primary runtime text

- `visible_text.txt`

### 5.2 Auxiliary text

- OCR output from the Vision pipeline
- selected HTML-derived snippets when needed

### 5.3 Structured side evidence used downstream

- URL tokens and domain features
- redirect chain features
- form-sensitive-input features
- lightweight network summary features

The Text pipeline is not expected to infer all structural context from free text alone.
It is designed to cooperate with structured side features and visual evidence downstream.

---

## 6. V1 Architecture

The V1 text pipeline uses a layered design:

1. primary text preparation
2. optional OCR-aware merge or side-channel handling
3. multilingual sentence or page embedding
4. bounded concept and side-feature fusion
5. evidence packaging for L1 downstream fusion

The default path uses an embedding-style encoder rather than a generative LLM.

---

## 7. Component 1: Text Preparation

### 7.1 Purpose

The text preparation stage normalizes runtime text evidence before encoding.
Its purpose is to keep the input compact, source-aware, and stable enough for downstream embedding and concept scoring.

### 7.2 Preferred source priority

Recommended V1 source priority:

1. `visible_text.txt`
2. OCR text from the Vision pipeline, if present
3. selected compact HTML-derived snippets only when clearly useful
4. structured text fragments from forms, URL, and redirect chain

### 7.3 Merge policy

OCR text should not be blindly concatenated into the primary visible text without source control.

Preferred V1 merge policy:

- keep `visible_text` as the primary channel
- keep OCR text as an auxiliary channel or prefixed merge block
- keep URL and structure-derived text as side features or separately tagged fragments

### 7.4 Preparation outputs

Examples:

- normalized primary text string
- OCR-auxiliary text string
- source-aware token counts
- text sparsity flags
- truncated-length indicators
- language-confidence hints when available

---

## 8. Component 2: Multilingual Text Encoder

### 8.1 Purpose

This component converts prepared text into compact semantic representations suitable for low-cost downstream fusion.

### 8.2 V1 default selection

#### Default configuration

- `multilingual-e5-small`

#### Stronger optional configuration

- `BGE-M3` for stronger multi-language and longer-context deployments when runtime budget is wider

#### English-biased optional lightweight alternative

- `bge-small-en-v1.5`

### 8.3 Why this policy

The default choice should optimize for:

- multilingual coverage
- bounded model size
- bounded sequence length and runtime cost
- deployment realism on ordinary PC-class hardware
- no mandatory fine-tuning requirement for initial deployment

### 8.4 Usage mode

The encoder is used as a non-generative semantic encoder.

Recommended runtime pattern:

- prepare bounded text input
- encode text into one or more fixed-size embeddings
- pass embeddings and side features to a lightweight fusion model

### 8.5 Fine-tuning policy

Warden V1 allows later task-specific fine-tuning, adapter tuning, or calibration on Warden-owned data.
However, the default V1 deployment profile must remain functional without mandatory task-specific tuning.

### 8.6 Output examples

- page-level embedding
- auxiliary OCR embedding where applicable
- pooled text quality indicators
- cross-source consistency hints

---

## 9. Component 3: Concept and Side-Feature Fusion

### 9.1 Purpose

This stage converts text embeddings and structured side evidence into bounded, auditable semantic signals that are useful for L1 fusion.

### 9.2 Why this stage exists

Embeddings alone are not sufficiently interpretable.
The system needs compact concept-level evidence such as:

- credential-seeking tendency
- payment-seeking tendency
- wallet-connection tendency
- account-verification tendency
- urgency or coercion tendency
- brand-mimic language tendency

### 9.3 V1 default implementation pattern

Use a lightweight tabular or tree-based fusion layer over:

- text embeddings
- OCR-derived text indicators
- URL features
- form-sensitive-input indicators
- redirect and network summary features

### 9.4 Fine-tuning and teacher support

This stage may be improved later by:

- teacher-generated concept supervision
- small Warden-specific calibration sets
- task-specific fusion tuning

This remains allowed in V1, but the default runtime should not depend on a large online teacher.

### 9.5 Output examples

- `score_credential_seek`
- `score_payment_seek`
- `score_wallet_connect`
- `score_verification_gate`
- `score_brand_mimic_language`
- `score_urgency_language`
- text-side escalation hint

These are bounded evidence outputs, not final Warden decisions.

---

## 10. Teacher Models and Supervision Strategy

Warden V1 allows stronger offline teacher models or rule-assisted labeling to supervise concept learning, calibration, and later fine-tuning.

Recommended V1 stance:

- runtime stays lightweight
- stronger teachers remain offline only
- concept supervision is preferred over long free-form teacher narration
- Warden-owned correction loops remain necessary

### Rules

- teacher labels are not gold labels
- manual spot-check remains required
- calibration data should emphasize hard cases and cross-language cases
- source-aware text supervision is preferred over naïve merged text supervision

---

## 11. Recommended Execution Order

A practical V1 execution order is:

1. load `visible_text.txt`
2. collect OCR text if Vision pipeline produced it
3. collect compact URL, redirect, form, and network side evidence
4. build source-aware prepared text input
5. run multilingual text encoder
6. run lightweight concept and side-feature fusion
7. package text evidence for downstream multimodal fusion

This order is chosen to preserve a text-first default while still benefiting from OCR and structural evidence when present.

---

## 12. Evidence Packaging

The Text pipeline should package outputs into a structured bundle.

A conceptual example:

    {
      "text_component_status": {
        "primary_text_loaded": true,
        "ocr_text_used": true,
        "encoder_ran": true,
        "concept_fusion_ran": true
      },
      "text_features": {
        "primary_token_count": 312,
        "ocr_token_count": 21,
        "text_sparse": false
      },
      "text_concepts": {
        "score_credential_seek": 0.88,
        "score_payment_seek": 0.10,
        "score_wallet_connect": 0.05,
        "score_verification_gate": 0.72,
        "score_brand_mimic_language": 0.64,
        "score_urgency_language": 0.41
      },
      "text_flags": {
        "ocr_aux_used": true,
        "language_mixed": true,
        "needs_higher_review": false
      }
    }

Field names above are illustrative.
The exact output schema may be finalized in the inference module or an adjacent runtime contract document.

---

## 13. Performance Policy

### 13.1 No hard-coded universal latency promises

V1 must not claim fixed numbers such as:

- “all text inference always under X ms”
- “embedding always under Y ms on any CPU”
- “full text pipeline always matches pure-text benchmark latency”

Those statements are too hardware-dependent and too sensitive to sequence length, backend, preprocessing, and fusion implementation.

### 13.2 Correct engineering wording

Performance statements must be written as:

- benchmark targets
- measured under specified hardware
- measured under specified sequence length
- measured under specified backend
- measured with clear inclusion or exclusion of side-feature preparation

### 13.3 What V1 should optimize for

- multilingual coverage under bounded cost
- deployability on ordinary PCs and modest x86 edge environments
- graceful degradation when OCR text is absent
- no silent dependency on a large autoregressive model

---

## 14. Security Positioning

### 14.1 What V1 does

Warden V1 does not use a large instruction-following autoregressive LLM as the default text runtime path.

This reduces the attack surface associated with direct prompt-following runtime behavior.

### 14.2 What V1 does not claim

V1 does not claim that this fully eliminates:

- adversarial wording
- evasion phrasing
- poisoned supervision effects
- encoder blind spots
- concept-layer calibration errors

Those concerns remain relevant and should be handled as part of later robustness evaluation and L2 or security testing work.

---

## 15. Final V1 Selection Summary

### 15.1 Default V1 runtime selection

- primary text source: `visible_text.txt`
- default encoder: `multilingual-e5-small`
- default runtime style: embedding plus lightweight fusion

### 15.2 Optional stronger selection

- stronger multilingual encoder: `BGE-M3`
- intended only for wider runtime budgets

### 15.3 Optional English-biased selection

- `bge-small-en-v1.5`

---

## 16. What V1 Explicitly Freezes

This document freezes the following high-level decisions for V1:

- Text pipeline remains evidence-oriented, not chat-style
- `visible_text.txt` remains the primary text input
- OCR text remains auxiliary by default
- multilingual support is part of the default design
- default text runtime uses an encoder, not a large autoregressive LLM
- embeddings and side features flow into lightweight fusion
- default deployment must work without mandatory fine-tuning
- Warden-specific fine-tuning remains allowed

---

## 17. What V1 Intentionally Leaves Open

The following items are intentionally left open for later benchmark-driven refinement:

- exact source-aware merge format
- exact concept inventory
- exact side-feature schema at code level
- exact calibration method
- exact hardware benchmark targets
- whether adapter tuning becomes the preferred fine-tuning path
- whether longer-context multilingual encoder variants are needed for later profiles

---

## 18. Practical One-Sentence Summary

Warden V1 Text is a visible-text-first, multilingual, evidence-oriented pipeline:
it uses a compact encoder to represent webpage language under bounded runtime cost, preserves OCR and structural evidence as auxiliary signals, and emits auditable concept-level outputs for downstream multimodal fusion instead of producing a standalone chat-style final judgment.
