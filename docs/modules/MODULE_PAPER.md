# MODULE_PAPER.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Paper / experiment support 模块的边界。
- 涉及实验归档、结果汇总和复现说明时，以英文版为准。

## 1. 模块作用

Paper 模块负责实验支持和论文侧产物整理，包括配置归档、结果汇总、表格图表辅助和复现备注。
它的目标是让实验结果可追踪，而不是未经说明地重写方法逻辑。

## 2. 责任边界

- 拥有：experiment configs archive、result aggregation、tables / figures helpers、reproducibility notes。
- 不拥有：未文档化的方法改写和核心工程逻辑的静默替换。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# MODULE_PAPER.md

# Warden Paper / Experiment Support Module Specification

## 1. Module Purpose

The Paper module defines how Warden research outputs are organized, justified, and exported
for paper writing, experiment reporting, rebuttal support, and reproducibility packaging.

This module is responsible for turning engineering artifacts and experiment results
into auditable scientific deliverables.

It does not own model execution, raw capture, or runtime inference behavior directly.
It owns how those results are documented, aggregated, cross-checked, and presented.

---

## 2. Core Responsibility

The Paper module owns:

- experiment registry for paper-facing runs
- result aggregation for tables and figures
- ablation organization
- error analysis packaging
- case study packaging
- method description support
- dataset description support
- evaluation protocol description support
- reproducibility appendix support
- rebuttal / response note support

The Paper module does not own:

- raw sample collection
- weak-label generation logic
- training-loop implementation
- inference runtime implementation
- silent reinterpretation of engineering outputs

---

## 3. Paper Philosophy

### 3.1 Paper follows project truth

The paper must describe the actual implemented and validated system,
not an idealized fantasy version.

### 3.2 No retrospective mythology

Do not rewrite project history to make the method sound cleaner than it is.

Examples of forbidden behavior:

- claiming a modality was used when it was not
- claiming manual labels existed for all samples when they did not
- claiming a benchmark was controlled if settings differed materially
- presenting weak-label supervision as clean gold truth

### 3.3 Reproducibility is part of the paper contract

A result used in the paper should be traceable to:

- code version
- config
- data subset / split
- checkpoint if applicable
- metric definition
- export script or notebook path if applicable

---

## 4. Paper-Facing Assets

The Paper module may consume:

- frozen data specification docs
- module docs
- experiment configs
- run logs
- checkpoint metadata
- evaluation outputs
- benchmark outputs
- error analysis exports
- case-study exports
- tables / figures intermediate files

It may also read curated notes from handoff or ADR records.

---

## 5. What Counts as a Paper Result

A result is paper-eligible only if the following are known:

- which model/run produced it
- which data split/subset it used
- which metric definition produced it
- whether thresholds were fixed or tuned
- whether the result is single-run or aggregated
- whether randomness / seed policy is known

If any of these are unknown, the result is not paper-ready.

---

## 6. Dataset Description Rules

### 6.1 Dataset description must follow frozen contracts

When describing dataset artifacts, the paper must align with the frozen data specification.

### 6.2 Do not overclaim label quality

If weak labels are used:

- call them weak labels, rule labels, or automated labels as appropriate
- do not present them as manual gold truth

If manual labels are used:

- specify subset scope and review status clearly

### 6.3 Dataset structure claims must match actual outputs

If the paper says the dataset includes screenshots, visible text, forms, URL, and network summary,
those claims must match the frozen output contract and actual data availability.

---

## 7. Method Description Rules

### 7.1 Method must match implementation family

The method section must reflect the actual system family in use.

Examples:

- text-only baseline
- vision-only baseline
- multimodal staged model
- teacher-student distillation path
- rule-assisted routing

Do not describe an imagined grand unified model if the implementation is staged or modular.

### 7.2 Staged-system honesty

If Warden is evaluated as an L0 / L1 / L2 staged system, that staging must be explicitly described.

Do not flatten the architecture in writing just because it looks cleaner.

### 7.3 Auxiliary signals must be described honestly

If rule flags, weak features, or review priorities are used:

- specify whether they are inputs, auxiliary targets, routing signals, or analysis aids
- do not mix these roles casually in the write-up

---

## 8. Experiment Design Rules

### 8.1 Every headline experiment needs a purpose

Each experiment included in the paper should answer a concrete question.

Examples:

- Does multimodal fusion outperform text-only or image-only baselines?
- Does staged routing improve efficiency under a fixed recall target?
- Does brand-aware evidence improve performance on impersonation-heavy subsets?
- Does evasion-aware routing help on hard cases?

### 8.2 Ablations must isolate one change at a time

Avoid soup ablations where multiple variables change together.

### 8.3 Baselines must be comparable

If comparing baselines, control for:

- data split
- supervision source
- evaluation subset
- threshold policy where relevant
- metric definitions

Do not compare apples to hovercraft.

---

## 9. Metric Reporting Rules

### 9.1 Metrics must match the task

Use metrics appropriate to the actual task formulation.

Examples:

- binary risk classification
- multi-class page stage classification
- escalation / routing efficiency
- review prioritization utility

### 9.2 Threshold reporting discipline

If metrics depend on thresholds, the threshold policy must be stated.

### 9.3 No selective metric inflation

Do not cherry-pick only the metric that looks pretty.

At minimum, report enough to show tradeoffs.

### 9.4 Efficiency claims must include runtime conditions

If claiming efficiency, include relevant conditions such as:

- hardware
- batch size
- precision
- input resolution
- stage-routing policy

---

## 10. Table Rules

### 10.1 Tables must be traceable

Every table row should be mappable to a run or aggregation source.

### 10.2 Consistent naming

Model names, data subsets, and settings must be named consistently across all tables.

### 10.3 No hidden setting drift

If one row differs in threshold, preprocessing, or supervision source, state it.

---

## 11. Figure Rules

### 11.1 Figures must be reproducible

A figure should ideally be regeneratable from a script and a known input artifact.

### 11.2 Figure semantics must be explicit

Axes, units, subset names, and threshold conditions must be explicit.

### 11.3 Case-study figures must preserve evidence honesty

If presenting page examples or risk cases:

- preserve what evidence was actually present
- do not annotate as if the model saw information it did not actually use

---

## 12. Error Analysis Rules

### 12.1 Error analysis is mandatory for non-trivial claims

If a method claim is important, the paper should include supporting error analysis.

### 12.2 Error categories should be explicit

Examples:

- brand mismatch false positives
- no-brand social-engineering misses
- CAPTCHA / cloaking hard cases
- multi-step interaction misses
- noisy visible-text extraction cases

### 12.3 Error analysis must use identifiable samples

At minimum, error exports should preserve sample_id or equivalent traceable identity.

---

## 13. Case Study Rules

### 13.1 Case studies must be representative

Do not choose only theatrical examples.

### 13.2 Case studies must state why they matter

Each case study should explain:

- what evidence was present
- what the model or pipeline decided
- why the case is interesting
- what it says about the system

### 13.3 Hard-case honesty

If a case is ambiguous, say it is ambiguous.
Do not force certainty because the prose wants drama.

---

## 14. Rebuttal / Response Support Rules

The Paper module should support later rebuttal by making the following easy to retrieve:

- run config
- split definition
- metric script
- threshold policy
- key handoff notes
- known limitations already documented

Do not wait until rebuttal week to discover your experiment lineage is vapor.

---

## 15. Limitations Section Rules

The paper must state real limitations where they exist.

Examples:

- weak-label noise
- incomplete brand coverage
- interaction-heavy pages not fully captured
- network-evidence mode variability
- deployment-budget constraints
- open-world generalization limits

A limitations section that says nothing is usually a decorative lie.

---

## 16. Non-Goals

This module must not:

- fabricate results
- round inconvenient facts into silence
- hide weak supervision under stronger wording
- merge incompatible runs into one number without note
- silently rewrite dataset semantics
- silently rewrite system scope

---

## 17. Validation Requirements

For any non-trivial Paper module task, validate at least:

1. table sources are traceable
2. figure sources are traceable
3. metric names match actual implementations
4. subset names match actual split definitions
5. method description matches current implementation family
6. claims about dataset outputs match frozen docs

If validation cannot be completed, say exactly what remains unchecked.

---

## 18. Required Reporting for Paper Changes

Every non-trivial paper-facing change must explicitly state:

- which section or artifact changed
- which experiment/run supports it
- whether terminology changed
- whether result interpretation changed
- whether tables/figures need regeneration
- whether limitations or caveats need update

---

## 19. Definition of Done

A Paper module task is Done only if:

- the requested paper-facing artifact is produced
- supporting experiment lineage is traceable
- terminology is honest
- limitations are not hidden
- validation is stated honestly
- doc/update impact is stated

