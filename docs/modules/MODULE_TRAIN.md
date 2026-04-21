# MODULE_TRAIN.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 Training 模块的默认职责和非职责。
- 涉及 loader、训练循环、loss 和评估实现时，以英文版为准。

## 1. 模块作用

Training 模块负责训练相关实现，包括数据加载、配置、训练循环、loss、checkpoint 和评估指标。
它的重点是训练阶段的工程闭环，而不是原始数据 schema 的重新设计。

## 2. 责任边界

- 拥有：loaders、configs、training loop、loss logic、checkpointing、eval metrics。
- 不拥有：raw data schema redesign 和与数据层无关的上游结构变更。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# MODULE_TRAIN.md

# Warden Training Module Specification

## 1. Module Purpose

The Training module defines how Warden consumes frozen dataset outputs and labeling outputs
to perform model training, evaluation, ablation, and reproducible experiment execution.

This module is responsible for turning frozen, documented sample artifacts into
stable, auditable training/evaluation pipelines.

This module must not silently redefine data schema, label semantics, or inference policy.

---

## 2. Core Responsibility

The Training module owns:

- dataset reading for training / validation / test
- sample filtering for training use
- feature loading and preprocessing
- model config loading
- training loop
- evaluation loop
- checkpoint save / load
- metrics computation
- experiment config recording
- ablation support
- result export for later paper use

The Training module does not own:

- raw data capture
- sample directory generation
- weak-label ontology redesign
- manual-label semantic redesign
- runtime deployment routing logic

---

## 3. Training Philosophy

### 3.1 Frozen input, controlled transformation

Training must consume documented, frozen upstream outputs.
It may transform them into model inputs, but must not silently redefine their meaning.

### 3.2 Reproducibility first

Training must be rerunnable under the same config, seed policy, and data split assumptions.

### 3.3 Separation of concerns

Training logic must not back-write into frozen dataset artifacts.
Training may read data and labels, but must not mutate sample directories.

### 3.4 Transparent experiment behavior

Every experiment must be explainable in terms of:

- input data subset
- label source used
- model configuration
- loss configuration
- seed and run settings
- evaluation protocol

---

## 4. Allowed Training Inputs

The Training module may read from frozen sample artifacts and derived label artifacts, including:

- `meta.json`
- `url.json`
- `visible_text.txt`
- `forms.json`
- `html_rendered.json`
- `html_raw.json` where explicitly needed
- `screenshot_viewport.png`
- `screenshot_full.png` where available
- `net_summary.json`
- `auto_labels.json`
- `rule_labels.json` when explicitly enabled
- `manual_labels.json` when available and approved for the task

It may also read project-level split manifests, config files, and experiment metadata.

---

## 5. Input Contract Rules

### 5.1 Upstream schema is not owned here

The Training module must treat upstream data and label contracts as external frozen contracts.

Strict rules:

- do not rename upstream field names from training code
- do not silently reinterpret field semantics
- do not infer schema changes and then code around them without reporting it
- do not “fix” broken upstream outputs by silently patching semantics in the training loader

If upstream inconsistency is discovered, report it explicitly.

### 5.2 Weak labels vs manual labels

If weak labels are used:

- they must be treated as weak supervisory signals
- they must not be described as gold truth

If manual labels are used:

- the source and subset policy must be explicit
- the training task must clearly state whether manual labels override weak labels

### 5.3 Optional upstream artifacts

The Training module must handle optional artifact absence safely.

Examples:

- absence of `screenshot_full.png` must not crash the pipeline if viewport screenshot is sufficient
- absence of `rule_labels.json` must not break baseline training unless the run explicitly requires it
- absence of `manual_labels.json` must not break default training

---

## 6. Data Split Rules

### 6.1 Split ownership

The Training module may consume split definitions, but split policy must be explicit and reproducible.

### 6.2 Reproducibility requirement

A training run must be able to answer:

- what samples were in train / val / test
- whether grouping by domain / etld1 / campaign was used
- whether weak labels or manual labels defined the target
- whether any filtering was applied before split or after split

### 6.3 No silent leakage

Strict rules:

- do not allow silent train / test leakage
- do not allow near-duplicate variants across train / test unless explicitly part of the experiment
- do not silently merge or reshuffle splits during resume logic
- do not silently change split rules between runs

If leakage prevention logic changes, document it.

---

## 7. Model Input Rules

### 7.1 Supported evidence families

Depending on experiment scope, model inputs may include:

- screenshot image input
- visible text input
- form-structure-derived input
- URL-derived input
- weak structured features
- network summary features

### 7.2 Modality discipline

If a modality is absent from a given run, that must be explicit in config and reporting.

Examples:

- image-only
- text-only
- text + URL
- image + text + structured features
- staged distillation setups

### 7.3 No hidden modality change

Do not silently add or remove an evidence family from a training pipeline without config and doc updates.

---

## 8. Label Target Rules

### 8.1 Target source must be explicit

For every train/eval run, the target source must be explicitly known.

Examples:

- weak binary risk target from `auto_labels.json`
- weak multi-class target from derived mapping
- manual final label from `manual_labels.json`
- review-priority auxiliary task
- page-stage auxiliary task

### 8.2 Multi-task discipline

If multi-task training is used, each target must specify:

- source file
- source field
- task type
- missing-label handling
- loss weighting

Do not hide multi-task complexity inside ad hoc code branches.

### 8.3 Missing target handling

Missing targets must be handled explicitly.

Allowed explicit strategies include:

- drop sample for that task
- mask loss for that task
- fallback to alternative target only if documented

Silent fallback is not allowed.

---

## 9. Config and Experiment Control

### 9.1 Config-driven execution

Training runs must be primarily config-driven, not hidden-constant-driven.

A run should be reproducible from:

- code revision
- config
- seed
- run command
- split definition
- checkpoint if resumed

### 9.2 Required config transparency

A training config should make the following explicit:

- model family
- input modalities
- target definition
- loss setup
- optimizer
- scheduler
- batch size
- precision mode
- seed policy
- checkpoint policy
- evaluation cadence
- save policy

### 9.3 No silent default drift

If default config values change, report that change.
Do not silently drift experiment meaning by editing hidden defaults.

---

## 10. Checkpoint Rules

### 10.1 Checkpoint contents

A checkpoint should preserve enough information to resume or audit a run, including where applicable:

- model state
- optimizer state
- scheduler state
- epoch / step
- config snapshot or config reference
- seed metadata if supported

### 10.2 Resume discipline

Resume behavior must be explicit:

- true resume
- fine-tune from checkpoint
- evaluation-only load

Do not mix them silently.

### 10.3 Compatibility handling

If checkpoint compatibility breaks due to architectural change, report it explicitly.
Do not pretend old checkpoints remain valid.

---

## 11. Evaluation Rules

### 11.1 Evaluation must be separated from training metrics

Training loss and evaluation metrics are not interchangeable.

### 11.2 Metrics must match task type

Examples:

- binary classification: precision / recall / F1 / ROC-AUC / PR-AUC as appropriate
- multi-class classification: macro / weighted metrics as appropriate
- ranking / staged routing: routing accuracy or escalation efficiency where applicable

### 11.3 Threshold discipline

If a thresholded metric is reported, the threshold policy must be stated.

Do not silently change thresholds between runs without recording it.

### 11.4 Error analysis support

Non-trivial experiments should support later error analysis, including at minimum:

- sample identifiers for mistakes
- predicted output
- target
- optional confidence / score
- optional contributing evidence summary

---

## 12. Distillation / Teacher-Student Rules

If distillation is used, the Training module must make explicit:

- teacher source
- teacher output type
- student target type
- distillation loss terms
- temperature if used
- balance with supervised loss
- dataset subset used for distillation

Do not bury distillation behavior inside undocumented helper code.

---

## 13. Training Module Non-Goals

This module must not:

- redesign frozen data schema
- silently redefine label semantics
- silently change inference routing semantics
- silently rewrite dataset directories
- overwrite manual labels
- fabricate experiment outcomes
- claim reproducibility without config/run trace

---

## 14. Validation Requirements

For any non-trivial Training module change, validate at least:

1. dataset loader can read a small sample batch
2. config parsing works
3. model forward pass works on a smoke batch
4. training step works on a smoke batch
5. evaluation step works on a smoke batch if evaluation logic changed
6. checkpoint save/load works if checkpoint logic changed
7. metric computation works if metric logic changed

If any validation is not run, state exactly what was not run and why.

---

## 15. Compatibility Rules

The Training module must explicitly report compatibility impact when changing:

- dataset reader expectations
- config schema
- checkpoint layout
- metric output format
- result export format

Breaking changes require:

- explicit approval
- migration note
- downstream experiment impact note

---

## 16. Required Reporting for Training Changes

Every non-trivial change must explicitly state:

- what training path changed
- what config behavior changed
- whether dataset assumptions changed
- whether label target assumptions changed
- whether checkpoint compatibility changed
- whether metric output changed
- whether docs need update

---

## 17. Definition of Done

A Training module task is Done only if:

- requested training behavior is implemented
- upstream frozen contracts are respected
- config impact is clear
- validation is stated honestly
- compatibility impact is stated
- risks are stated
- documentation impact is stated


