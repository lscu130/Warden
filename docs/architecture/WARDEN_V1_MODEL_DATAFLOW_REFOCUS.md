# WARDEN_V1_MODEL_DATAFLOW_REFOCUS

## 中文版

### 摘要

本文档冻结 Warden V1 当前模型结构和数据流重聚焦口径：

```text
Current offline experiment:
Processed Valid Dataset
  -> Evidence Pack Builder
  -> L1 Main Judgment / L1 Training / L1 Evaluation
  -> Metrics / Evidence Ledger / Ablation

Future wild-test / online inference:
Raw URL
  -> Capture Pipeline
  -> Capture QA / V1 Scope Admission
  -> Evidence Pack Builder
  -> L1 Main Judgment
  -> Wild-Test Report
```

L1 内部流程：

```text
Text / HTML / URL / Forms first pass
  -> if evidence insufficient, trigger OCR / YOLO
  -> Conditional Vision Evidence Recovery
  -> Fusion
  -> Evidence Ledger
```

当前 V1 不把 L0、默认 L2、默认 CLIP、adult / gambling / gate / evasion / redirect-only 作为主实验或主判断路径。旧 L0/L2 字段、代码或文档引用只作为 legacy compatibility、V2+、future online/wild-test 或 out-of-scope 说明保留。

### 当前 Warden V1 权威状态

- 威胁定义：`Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)`。
- 高风险诱导动作定义：`InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation`。
- 当前离线实验默认链路：`Processed Valid Dataset -> Evidence Pack Builder -> L1`。
- 未来 online / wild-test 链路：`Raw URL -> Capture Pipeline -> Capture QA / V1 Scope Admission -> Evidence Pack Builder -> L1`。
- L0 不是当前 V1 离线实验默认链路的一部分；现存 L0 wording 只作为 legacy/runtime compatibility、future online/wild-test support 或 scope-admission 说明。
- L2 不是当前 V1 默认判断路径；任何 heavy review / L2 路径需要单独任务定义。
- OCR / YOLO 是 L1 内部按需触发的 evidence recovery，不是 always-on 阶段，也不是独立最终判定器。
- CLIP / MobileCLIP / SNet 不属于当前 V1 默认路径，只能在单独任务中作为 auxiliary、future 或 ablation framing。
- Adult / gambling / gate / evasion / redirect-only 等捕获或内容类别，单独存在时不是 V1 malicious 成立条件。

## English Version

> AI note: English is authoritative for exact architecture, scope, and compatibility wording.

# Warden V1 Model/Dataflow Refocus

## 1. Purpose

This document defines the current Warden V1 model structure and dataflow focus.

It is a documentation contract only. It does not modify runtime behavior, model code, training behavior, schema fields, label enums, manifest fields, CLI flags, or JSON output formats.

## Current Warden V1 authoritative state

- Threat definition: `Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)`.
- Induced high-risk action definition: `InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation`.
- Current offline experiment default path: `Processed Valid Dataset -> Evidence Pack Builder -> L1`.
- Future online / wild-test path: `Raw URL -> Capture Pipeline -> Capture QA / V1 Scope Admission -> Evidence Pack Builder -> L1`.
- L0 is not part of the current V1 offline experiment default path. Existing L0 wording is legacy/runtime compatibility, future online/wild-test support, or scope-admission wording only.
- L2 is not part of the current V1 default judgment path. Any heavy review / L2 path requires a separate accepted task.
- OCR / YOLO are conditional L1 evidence recovery primitives, not always-on stages and not independent final judges.
- CLIP / MobileCLIP / SNet are outside the current V1 default path and require separate auxiliary, future, or ablation framing.
- Adult / gambling / gate / evasion / redirect-only captures or content categories are not sufficient V1 malicious conditions by themselves.

## 2. Current Offline Experiment Path

The current Warden V1 full experiment starts from already processed, valid, human-observable samples:

```text
Processed Valid Dataset
  -> Evidence Pack Builder
  -> L1 Main Judgment / L1 Training / L1 Evaluation
  -> Metrics / Evidence Ledger / Ablation
```

Implications:

- `Processed Valid Dataset` is already inside V1 scope and capture-valid enough for human-observable evidence analysis.
- `Evidence Pack Builder` is the current main experiment entrypoint.
- L1 is the current main judgment / training / evaluation layer.
- Legacy L0 screening is not the default model entrypoint for the current offline experiment.

## 3. Future Wild-Test / Online Inference Path

The future online and wild-test path remains documented:

```text
Raw URL
  -> Capture Pipeline
  -> Capture QA / V1 Scope Admission
  -> Evidence Pack Builder
  -> L1 Main Judgment
  -> Wild-Test Report
```

Implications:

- Online capture remains necessary for future wild testing.
- Capture QA / V1 Scope Admission is not a new default L0 judgment layer.
- Gate-only, redirect-only, trusted-sink-only, insufficient-observability, and evasion-only captures are handled as QA / admission / V2+ issues unless downstream content satisfies the V1 threat formula.
- This document does not implement capture, recrawl, interaction recovery, or wild testing.

## 4. L1 Internal Evidence Flow

L1 should remain text / HTML / URL / forms first:

```text
Text / HTML / URL / Forms first pass
  -> if evidence insufficient, trigger OCR / YOLO
  -> Conditional Vision Evidence Recovery
  -> Fusion
  -> Evidence Ledger
```

Rules:

- OCR is conditional screenshot text recovery.
- YOLO / detector is conditional UI-component localization.
- OCR and YOLO are not always-on dataflow stages.
- Vision evidence supports the evidence pack, fusion, and evidence ledger; it is not an independent final malicious / benign judge.

## 5. CLIP Status

CLIP / MobileCLIP is not part of the Warden V1 default path.

Allowed future or auxiliary uses require a separate task:

- offline screenshot clustering;
- template discovery;
- ablation baseline;
- research-only visual-prior experiments;
- optional feature-flag experiments.

CLIP must not be described as:

- the default visual tower;
- an always-on V1 stage;
- a final malicious / benign judge;
- a replacement for OCR text recovery or YOLO UI localization.

## 6. L0 / L2 Status

Current V1 does not define a default L0 model entrypoint or a default L2 judgment path.

Compatibility notes:

- Existing `L0`, `L0-fast`, `direct_to_L2`, or `needs_l2_candidate` names may remain in code or historical docs as legacy compatibility or future-escalation hints.
- Those names must not be interpreted as the current V1 offline experiment mainline.
- If future online/wild-test work needs cheap screening, it should be framed under Capture QA / V1 Scope Admission unless a separate accepted task redefines runtime stages.
- Any future heavy review / L2 path requires a separate architecture task.

## 7. Adult / Gambling / Gate / Evasion Scope

Adult, gambling, guns, drugs, gate-only, challenge-only, CAPTCHA-only, redirect-only, trusted-sink-only, and evasion-only captures are not Warden V1 main tasks by themselves.

They may be:

- excluded by V1 scope admission;
- kept as auxiliary or future V2+ datasets;
- used as compatibility weak signals;
- used in future wild-test QA analysis.

They must not be treated as V1 malicious solely by content category or capture pattern.

## 8. Implementation Boundary

This refocus does not:

- modify L1 model code;
- add OCR / YOLO calls;
- implement online capture;
- implement wild testing;
- change training logic;
- change runtime schemas;
- change labels or enums;
- change CLI flags;
- change manifest fields;
- change JSON output formats.

Known implementation follow-up risk:

- Existing runtime code still contains L0 and L2 stage names. That is a compatibility and implementation-alignment issue for a later task, not a change made by this documentation refocus.
