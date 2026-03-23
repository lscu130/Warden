# Warden Vision Pipeline Specification (V1)

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档已按“中文在前，英文在后”整理。
- 若涉及精确字段名、命令、模板或历史事实，以英文版为准。
- 对历史 task、handoff、report 文档，本次改造只调整呈现，不应改变原始结论、状态或验证记录。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Vision Pipeline Specification (V1)

## 1. Module Purpose

The Vision Pipeline defines how Warden extracts runtime visual evidence from webpage screenshots for L1 social-engineering threat judgment.

This module is not a standalone final judge and is not a traditional logo-matching subsystem.
Its purpose is to produce bounded-cost, deployment-friendly, auditable visual evidence that can be fused with visible text, URL features, form features, and lightweight network features downstream.

The Vision Pipeline must preserve the current Warden project direction:

- Warden targets **web social-engineering threat judgment**, not narrow phishing-logo matching.
- Vision evidence must support staged L0 / L1 / L2 inference rather than collapsing the system into a monolithic black-box path.
- Runtime cost must remain bounded and explicit.
- Outputs must remain inspectable and suitable for downstream audit and review.

---

## 2. Core Responsibility

The Vision Pipeline owns:

- runtime screenshot preparation for the visual path
- visual evidence extraction from the current sample contract
- image-side OCR policy
- page-level visual scenario similarity extraction
- local suspicious component detection
- visual evidence packaging for downstream fusion
- missing-input and degraded-mode handling for the visual path
- benchmark-facing runtime configuration discipline for the vision path

The Vision Pipeline does not own:

- raw collection policy redesign
- frozen dataset schema redesign
- weak-label ontology redesign
- final L1 fusion thresholds
- final risk decision policy
- L2 heavy review logic
- paper-level result narration

---

## 3. Alignment with Current Repository Contracts

### 3.1 Project alignment

Warden currently defines its main problem as webpage social-engineering threat judgment under staged, lightweight, and explainable constraints.
The vision path therefore focuses on visual evidence of risk-inducing page structure, visual mimicry, credential collection surfaces, payment or wallet-inducing interfaces, and suspicious gating flows.

### 3.2 Dataset alignment

Under the current frozen output contract, the Vision Pipeline must operate against the files that already exist in successful samples.

Primary visual input:

- `screenshot_viewport.png`

Optional visual enhancement input:

- `screenshot_full.png`

Parallel non-visual evidence already available in the repository:

- `visible_text.txt`
- `forms.json`
- `url.json`
- `net_summary.json`

Therefore:

- the visual path must be **viewport-first**
- the visual path must be **visible-text-aware**
- the visual path must treat full-page screenshots as **optional enhancement**, not as a hard dependency
- OCR must not be treated as the only text source

### 3.3 Practical implication

The V1 visual path is designed as an evidence module that complements existing structured and textual inputs.
It is not responsible for reconstructing all non-visual semantics from screenshots alone.

---

## 4. Vision Inference Philosophy

### 4.1 Evidence extraction, not opaque final judgment

The vision path must output structured evidence such as:

- OCR text summaries
- image-text similarity scores
- local detector presence flags and counts
- image quality or uncertainty flags
- escalation hints when visual evidence quality is weak or conflicting

The vision path must not silently convert all behavior into one opaque scalar if richer evidence is available.

### 4.2 Stage discipline

The visual path supports L1 judgment and may provide cheap image-lite evidence to L0 only where explicitly allowed by inference policy.
It must not silently move L2-class heavy logic into early stages.

### 4.3 Stable primitives before broad semantics

V1 should first learn stable, visually grounded primitives rather than broad, weakly defined semantic classes.
Examples of preferred primitives include:

- password-like field presence
- OTP-like field presence
- QR code presence
- wallet-modal-like region presence
- captcha-like region presence
- fullscreen overlay presence
- strong single-CTA region presence

V1 should avoid directly training detectors on broad concepts such as:

- `urgent_scam_page`
- `brand_mimic_page`
- globally defined `fake_captcha` truth labels
- broad maliciousness concepts that require text, URL, or policy context to interpret

### 4.4 Missing-tolerant operation

Any one visual submodule may fail, be skipped, or be unavailable.
The pipeline must still produce a usable partial evidence package and make degraded operation explicit.

---

## 5. Runtime Inputs

### 5.1 Required visual input

- `screenshot_viewport.png`

### 5.2 Optional visual input

- `screenshot_full.png`

### 5.3 Parallel structured inputs used downstream

- `visible_text.txt`
- `forms.json`
- `url.json`
- `net_summary.json`

### 5.4 Input discipline

The runtime input contract for the visual path must remain explicit.
If optional inputs are missing, fallback behavior must be explicit and auditable.
Silent dependency expansion is not allowed.

---

## 6. High-Level Architecture

The V1 Vision Pipeline uses a decoupled three-component design:

1. OCR component
2. image-text similarity encoder
3. lightweight local detector

Outputs from these components are packed into a structured visual evidence bundle and passed to downstream fusion.

This design is preferred over a monolithic end-to-end generative visual-language runtime path because it provides:

- bounded deployment cost
- clearer module boundaries
- better interpretability
- easier fallback handling
- simpler component replacement or benchmarking

---

## 7. Component A: OCR

## 7.1 Purpose

The OCR component recovers screenshot-visible text that may be absent, incomplete, or poorly represented in DOM-derived text extraction.

Typical use cases include:

- image-rendered warning banners
- modal text not cleanly present in `visible_text.txt`
- QR-side labels
- wallet / payment / verification prompt text embedded in images
- anti-DOM or screenshot-heavy presentation styles

## 7.2 V1 selection policy

Default path:

- `PP-OCRv4 mobile`

Enhanced path:

- language-specific `PP-OCRv5` recognition variants when justified by sample language profile or benchmark results
- full `PP-OCRv5 mobile` only for explicitly enabled stronger OCR paths

## 7.3 Selection rationale

V1 does not assume that the newest OCR pipeline is automatically the best default for bounded-cost runtime.
The default OCR path should prioritize deployment stability and controlled latency.
Stronger OCR paths remain allowed, but they should be benchmark-driven and opt-in rather than silently always-on.

## 7.4 Invocation policy

OCR should be trigger-based rather than unconditionally executed on every sample.

Recommended trigger families include:

- `visible_text.txt` is sparse or abnormally short
- image-heavy text presentation is suspected
- the detector identifies suspicious local panels, overlays, captcha-like regions, or wallet-like regions
- the page appears text-rich visually but DOM text is weak
- the full-page screenshot exists and viewport evidence is insufficient

## 7.5 Typical output fields

Examples:

- OCR text string or normalized excerpt
- OCR token count
- OCR region count
- OCR confidence summary
- OCR-heavy-image flag
- OCR-executed flag

---

## 8. Component B: Image-Text Similarity Encoder

## 8.1 Purpose

The image-text similarity encoder captures page-level visual scenario similarity.
It is used as a non-generative dual-encoder-style module rather than a runtime instruction-following visual-language model.

Its purpose is to map screenshots against a fixed prompt bank representing social-engineering-relevant visual scenarios and produce numeric similarity features for downstream fusion.

## 8.2 V1 selection policy

Standard configuration:

- `MobileCLIP2-S2`

Tight-budget configuration:

- `MobileCLIP2-S0`

Research backup option:

- another extremely small CLIP-family alternative only if later Warden-specific benchmarking shows a materially better accuracy / latency / deployment trade-off

## 8.3 Selection rationale

The default image-text encoder should optimize for:

- mobile or edge-friendly deployment profile
- low-latency image-text encoding
- practical parameter size
- easier expansion through prompt-bank updates

V1 does not choose a larger general-purpose visual-language encoder as the default runtime path.

## 8.4 Runtime usage mode

The encoder should be used in non-generative similarity mode.

Recommended runtime pattern:

- maintain a fixed prompt bank
- precompute and cache prompt embeddings offline
- compute image embeddings at runtime
- emit similarity scores as numeric features

## 8.5 Prompt-bank discipline

The prompt bank should describe visual social-engineering scenarios, not final legal, policy, or maliciousness conclusions.

Suitable prompt themes include:

- login or re-login panel
- payment confirmation page
- wallet connection modal
- wallet recovery or seed phrase page
- verification or human-check gate
- single-primary-CTA conversion page
- brand-like account verification interface

## 8.6 Typical output fields

Examples:

- `sim_login_panel`
- `sim_payment_page`
- `sim_wallet_connect_modal`
- `sim_seed_phrase_recovery`
- `sim_verification_gate`
- `sim_single_cta_page`
- `sim_brand_mimic_ui`

These are scenario-similarity features, not final maliciousness labels.

---

## 9. Component C: Lightweight Local Detector

## 9.1 Purpose

The local detector provides spatially grounded evidence that page-level similarity alone cannot express precisely.
Its job is to detect a small number of high-value visual primitives and suspicious interaction regions.

## 9.2 V1 selection policy

Standard configuration:

- `YOLO26n`

Tight-budget / extreme edge alternative:

- `PicoDet-S`
- `PicoDet-XS`

Optional backup:

- another lightweight detector only if later internal benchmarking shows a materially better export and deployment trade-off

## 9.3 Selection rationale

V1 prefers:

- one default detector with a mature training and export ecosystem
- one tighter-budget fallback for CPU-heavy or memory-constrained deployment cases

## 9.4 Class design rule

Detector classes must remain atomic and visually grounded.
They should not embed final semantic interpretation that requires broader textual, URL, or policy context.

Preferred V1 classes include:

- `qr_code`
- `password_field`
- `otp_field`
- `seed_phrase_grid`
- `wallet_modal_region`
- `checkbox_captcha`
- `puzzle_captcha`
- `fullscreen_overlay`
- `single_primary_cta_region`

## 9.5 Typical output fields

Examples:

- per-class presence flags
- per-class counts
- per-class maximum confidence
- suspicious-region area ratios
- simple spatial distribution summaries

---

## 10. Teacher Models and Pseudo-Labeling

V1 allows stronger offline teacher models to support pseudo-label generation and annotation acceleration.

Recommended teacher-family usage:

- `GroundingDINO` for phrase-guided region grounding and open-set assistance
- `Florence-2` for broader prompt-based visual-task assistance

These teacher models are offline tooling and are not default Warden runtime dependencies.

### 10.1 Rules

- pseudo-labels are not gold labels
- human spot-check remains required
- hard cases must be manually corrected
- teacher-generated labels should primarily target atomic visual evidence classes

---

## 11. Recommended Execution Order

A practical V1 execution order is:

1. load `screenshot_viewport.png`
2. run the image-text similarity encoder
3. run the lightweight local detector
4. decide whether OCR is necessary
5. run OCR only if trigger conditions are met
6. package visual evidence
7. send the visual evidence bundle to downstream fusion together with:
   - `visible_text.txt`
   - `forms.json`
   - `url.json`
   - `net_summary.json`

This order avoids making OCR an unconditional always-on bottleneck.

---

## 12. Visual Evidence Packaging

The visual path should package outputs into a structured bundle suitable for downstream fusion and audit.

An example conceptual structure is shown below.
Field names are illustrative only; the exact runtime contract may be finalized in the Inference module or an adjacent runtime contract document.

```json
{
  "vision_component_status": {
    "clip_encoder_ran": true,
    "detector_ran": true,
    "ocr_ran": false
  },
  "vision_similarity": {
    "sim_login_panel": 0.81,
    "sim_wallet_connect_modal": 0.23,
    "sim_verification_gate": 0.74
  },
  "vision_detection": {
    "has_qr_code": false,
    "password_field_count": 1,
    "otp_field_count": 0,
    "wallet_modal_region_count": 0,
    "captcha_region_count": 1
  },
  "vision_ocr": {
    "ocr_text": "",
    "ocr_token_count": 0
  },
  "vision_flags": {
    "fullpage_missing": true,
    "ocr_skipped": true,
    "needs_higher_review": false
  }
}
```

The visual output contract must remain stable if consumed by downstream tooling.
If the contract changes materially, that change must be versioned or explicitly reported.

---

## 13. Performance Policy

### 13.1 No hard-coded universal latency promises

V1 must not claim fixed numbers such as:

- “OCR always 50 ms”
- “detector always 10 ms”
- “full pipeline always under X ms”
- “always under 100 MB total memory”

Those numbers are too hardware-dependent and too sensitive to runtime backend, input size, preprocessing, postprocessing, and export format.

### 13.2 Correct engineering wording

Performance statements must be written as measured benchmark targets under specified conditions, including where relevant:

- hardware
- input size
- runtime backend
- precision mode
- batch size
- whether preprocessing and postprocessing are included

### 13.3 What V1 should optimize for

- bounded runtime cost
- predictable CPU deployment profile
- graceful degradation when optional inputs are absent
- no silent dependency on full-page screenshots
- no silent dependency on heavy always-on OCR

---

## 14. Security Positioning

### 14.1 What V1 does

Warden V1 does not use an instruction-following generative visual-language model as the default edge runtime path.
This reduces the attack surface associated with direct multimodal instruction-following behavior in the runtime path.

### 14.2 What V1 does not claim

V1 does not claim that this fully eliminates:

- image-based prompt injection risk in all contexts
- adversarial image attacks
- transfer attacks on vision encoders
- detector evasion by crafted layouts

Those concerns remain relevant and belong to later robustness evaluation, security testing, and L2-facing escalation work.

---

## 15. Validation Requirements

For any non-trivial Vision Pipeline change, validate at least:

1. viewport-only path works on a smoke sample
2. missing-fullpage path works if full-page handling is touched
3. OCR trigger behavior works on at least a small representative set if OCR logic changed
4. detector path works on a smoke sample if detector logic changed
5. similarity-encoder path works on a smoke sample if encoder logic changed
6. evidence packaging matches documented expectations if output fields changed
7. degraded-mode behavior is explicit if optional inputs are missing
8. benchmark command or benchmark script still runs if benchmark logic changed

If any validation is not run, state exactly what was not run and why.

---

## 16. Compatibility Rules

The Vision Pipeline must explicitly report compatibility impact when changing:

- visual input assumptions
- OCR trigger policy
- detector class definitions
- similarity feature definitions
- output schema
- deployment dependencies
- benchmark semantics

Breaking changes require:

- explicit approval
- versioning or migration plan
- downstream consumer impact note

---

## 17. Vision Module Non-Goals

This module must not:

- redesign the frozen dataset schema
- silently redefine label semantics
- silently collapse staged routing into one opaque branch
- silently change runtime dependencies
- silently claim benchmark numbers not actually measured
- silently treat optional inputs as mandatory
- silently turn offline teacher models into runtime hard dependencies

---

## 18. Final V1 Selection Summary

### 18.1 Standard configuration

- OCR: `PP-OCRv4 mobile`
- image-text encoder: `MobileCLIP2-S2`
- local detector: `YOLO26n`

### 18.2 Tight-budget configuration

- OCR: `PP-OCRv4 mobile`, trigger-based only
- image-text encoder: `MobileCLIP2-S0`
- local detector: `PicoDet-S` or `PicoDet-XS`

### 18.3 Offline teacher tools

- `GroundingDINO`
- `Florence-2`

---

## 19. What V1 Explicitly Freezes

This document freezes the following high-level decisions for V1:

- the vision pipeline remains decoupled rather than monolithic
- OCR, similarity encoding, and local detection remain separate components
- the vision path emits evidence rather than final judgment
- `screenshot_viewport.png` remains the primary visual input
- `screenshot_full.png` remains optional
- OCR remains trigger-based by default
- detector classes should remain atomic and visually grounded
- offline teacher models are allowed for pseudo-labeling but are not required at runtime

---

## 20. What V1 Intentionally Leaves Open

The following items remain open for later benchmark-driven refinement:

- exact prompt-bank contents
- exact detector class list after pilot labeling
- exact OCR trigger thresholds
- exact runtime field names at code level
- exact fusion feature schema
- exact hardware benchmark targets
- whether quantized export becomes the default deployment form

---

## 21. Definition of Done

A Vision Pipeline V1 task is done only if:

- requested visual behavior is implemented
- stage responsibility remains clear
- runtime cost assumptions remain explicit
- evidence packaging remains auditable
- validation is stated honestly
- compatibility impact is stated
- risks are stated
- documentation impact is stated

---

## 22. Practical One-Sentence Summary

Warden Vision V1 is a viewport-first, evidence-oriented, decoupled visual pipeline: it uses lightweight OCR to fill screenshot text blind spots, a mobile-friendly image-text encoder to score page-level social-engineering visual scenarios, and a lightweight detector to locate atomic high-risk components, then passes those outputs into downstream multimodal fusion rather than making a standalone black-box final decision.
