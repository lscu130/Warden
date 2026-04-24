# Warden_EDGE_DEPLOYMENT_PROFILE_V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档冻结 Warden V1 的默认边缘部署画像。
- 涉及硬件假设、运行时默认值和部署姿态时，以英文版为准。

## 1. 文档作用

本文档用于说明 Warden V1 在边缘侧部署时的现实约束、目标硬件范围和默认运行取舍。
重点不是追求所有硬件的一致性能，而是明确“默认支持什么级别的部署环境”。

## 2. 核心摘要

- 目标对象包括普通个人设备、小微企业主机和预算有限的边缘节点。
- 设计原则偏向可部署、可解释、可维护，而不是单纯追求最重模型。
- 任何偏离默认画像的部署方案，都应视为额外配置而不是默认主线。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden_EDGE_DEPLOYMENT_PROFILE_V1

## 1. Document Purpose

This document defines the default V1 deployment profile for Warden under practical edge-oriented constraints.

The target deployment audience is:

- individual users
- small and micro businesses
- ordinary desktop or laptop PCs
- modest x86 edge hosts
- ordinary enterprise gateway-class hardware where CPU budget is limited but not negligible

This document does not attempt to guarantee identical performance on all hardware classes.
Its purpose is to freeze the intended V1 deployment posture and runtime defaults.

---

## 2. Deployment Assumptions

Warden V1 assumes deployment environments roughly comparable to:

- ordinary PC-class CPUs from the last several years
- modest enterprise gateway or mini-PC class x86 devices
- software-router-style environments where CPU inference is possible but not abundant

V1 does not assume:

- dedicated accelerator hardware
- strong discrete GPU availability
- cloud-only dependency for core runtime judgment
- mandatory online teacher-model access

---

## 3. System Positioning Under This Profile

Under the V1 default deployment profile, Warden should behave as follows:

- lightweight staged inference remains mandatory
- text-side evidence remains cheap enough to run broadly
- vision-side evidence remains bounded and selective
- OCR must remain trigger-based rather than always-on
- detector remains present, but bounded by lightweight architecture choice
- no component may silently assume server-class compute

The practical goal is not to match heavy multi-modal LLM systems.
The practical goal is to remain meaningfully deployable on modest hardware while still providing useful social-engineering threat evidence.

---

## 4. Default V1 Runtime Stack

### 4.1 Text-side default

- primary source: `visible_text.txt`
- encoder: `multilingual-e5-small`
- runtime style: embedding plus lightweight fusion

### 4.2 Vision-side default

- primary image input: `screenshot_viewport.png`
- image-text encoder: `MobileCLIP2-S2`
- OCR: `PP-OCRv4 mobile`, trigger-based
- detector: `YOLO26n`

### 4.3 Offline-only teacher tools

- `GroundingDINO`
- `Florence-2`
- other stronger calibration or pseudo-label tools as needed

These are not required for the default online runtime path.

---

## 5. Why This Default Profile Is Chosen

### 5.1 Text-side rationale

The default text path must satisfy all of the following at once:

- multilingual support
- off-the-shelf usability
- bounded runtime cost
- compatibility with ordinary CPU deployment
- no dependency on large generative runtime models

### 5.2 Vision-side rationale

The default vision path keeps three complementary roles:

- page-level visual scenario scoring
- localized visual evidence detection
- screenshot text recovery only when needed

The selected components are intended to keep the runtime cost bounded while still preserving multimodal usefulness.

### 5.3 Why detector remains in the default profile

Detector remains in the default profile because localization of atomic UI evidence is still valuable for:

- QR-code-bearing pages
- password and OTP collection pages
- wallet-modal-like pages
- captcha and gate pages
- single-CTA conversion flows

However, detector must remain lightweight and class design must stay atomic.

---

## 6. Runtime Execution Policy

Recommended default runtime order:

1. run the L0 cheap screening hot path from URL, visible-text/title, form-summary, network-summary, raw visible-text observability, and existing compact diff/evasion hints
2. prepare text-side evidence from `visible_text.txt` and side features for L1 when needed
3. run text encoder and lightweight text fusion when L1 is entered
4. load `screenshot_viewport.png` only when the active path requests visual evidence
5. run image-text similarity encoder when visual follow-up is enabled
6. run lightweight detector when the active deployment profile enables it
7. decide whether OCR is needed
8. run OCR only if trigger conditions are met
9. package evidence and pass to staged fusion and routing

This execution order reflects a bounded-cost bias.
It keeps L0 before screenshot/OCR/model-heavy work, avoids making OCR the default bottleneck, and preserves detector usage for the later visual path rather than for the default L0 hot path.

---

## 7. OCR Trigger Policy in the Default Profile

OCR should not run unconditionally.
It should be triggered when one or more of the following hold:

- `visible_text.txt` is sparse
- screenshot appears text-heavy
- detector indicates suspicious local regions
- image-text similarity suggests a risky scenario but text evidence is weak
- full-page screenshot exists and visual ambiguity remains high

---

## 8. Fine-Tuning Policy Under the Default Profile

Warden V1 default deployment must work without mandatory task-specific tuning.
At the same time, the profile explicitly retains fine-tuning as an allowed path.

Recommended priority order:

1. deploy off-the-shelf defaults first
2. measure real runtime and false positive or false negative behavior
3. fine-tune detector and concept calibration on Warden-owned data where justified
4. avoid broad, uncontrolled end-to-end tuning before atomic evidence stability is verified

In practice, the most reasonable first fine-tuning target is the detector or concept-layer calibration, not an immediate full-pipeline monolithic rewrite.

---

## 9. Performance Positioning

### 9.1 What this profile targets

This profile targets:

- ordinary PCs
- modest x86 edge hosts
- bounded CPU deployment
- clearly lighter runtime than heavy multimodal LLM-style systems

### 9.2 What this profile does not promise

This profile does not promise:

- identical runtime on all routers or gateway appliances
- fixed universal latency values
- parity with pure-text systems once the full multimodal path runs
- comfortable deployment on very weak consumer router hardware without reduction

### 9.3 Correct engineering stance

Performance should be discussed in terms of:

- concrete benchmark hardware
- concrete input size and text length
- backend and export format
- whether OCR ran
- whether detector ran

---

## 10. Reduction Policy for Weaker Devices

If deployment hardware is weaker than the intended default profile, reduction should proceed in this order:

1. tighten OCR trigger thresholds
2. reduce detector input size or switch detector to tighter-budget fallback
3. switch image-text encoder from `MobileCLIP2-S2` to `MobileCLIP2-S0`
4. if necessary, fall back to a text-dominant path for the weakest hardware tiers

The default profile itself remains unchanged.
This section only defines reduction strategy when hardware cannot comfortably sustain the default stack.

---

## 11. Default V1 Profile Freeze

The following decisions are frozen for the V1 default deployment profile:

- text default: `multilingual-e5-small`
- vision similarity default: `MobileCLIP2-S2`
- OCR default: `PP-OCRv4 mobile`, trigger-based
- detector default: `YOLO26n`
- detector remains in V1
- off-the-shelf deployment is supported
- fine-tuning remains allowed
- runtime remains CPU-conscious and stage-disciplined

---

## 12. What This Profile Intentionally Leaves Open

The following remain open for later benchmark-driven refinement:

- exact quantization policy
- exact detector input size
- exact OCR trigger thresholds
- exact fusion latency budget by hardware tier
- whether a separate router-only reduced profile should be frozen later
- whether the stronger text encoder profile becomes worth standardizing for PC-only deployment

---

## 13. Practical One-Sentence Summary

Warden V1 default deployment is a bounded-cost multimodal profile for ordinary PC-class and modest x86 edge environments: multilingual text encoding is always available, vision similarity and lightweight detection remain part of the default path, OCR stays trigger-based, and later Warden-specific fine-tuning is allowed without making fine-tuning a prerequisite for initial deployment.

