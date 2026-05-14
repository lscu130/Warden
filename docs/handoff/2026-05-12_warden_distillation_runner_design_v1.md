# HANDOFF_20260512_WARDEN_DISTILLATION_RUNNER_DESIGN_V1

## 中文版

### 摘要

本次交付新增 Warden distillation runner design contract V0.1。交付只包含 3 个文档：task doc、runner design、handoff。未实现 runner，未调用模型 API，未运行 teacher distillation，未生成 teacher labels，未修改数据、标签、manifest、split、训练、推理、runtime schema 或 CLI。

设计文档定义了未来 runner 的 CLI/API 形状、manifest 输入、evidence pack、teacher routing、DeepSeek-V4 fallback 限制、JSONL 输出、schema validation / schema repair、train-only 官方蒸馏策略、val/test diagnostic-only 策略、review queue、resume/idempotency、logging/audit 和 pilot plan。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF_20260512_WARDEN_DISTILLATION_RUNNER_DESIGN_V1
- Related Task ID: TASK-20260512-WARDEN-DISTILLATION-RUNNER-DESIGN-V1
- Task Title: Design Warden Distillation Runner Contract V1
- Module: Distillation / Labeling / Data Quality / Runner Design
- Author: Codex
- Date: 2026-05-12
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

Added a documentation-only Warden distillation runner design contract. The design defines future CLI/API shape, input manifest handling, evidence pack rules, teacher routing and fallback logging, JSONL outputs, schema validation and repair, split-policy enforcement, review queue generation, resume/idempotency, logging/audit, and pilot stages. The task reached its design stop condition without implementing a runner or changing production behavior.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`.
- Added `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`.
- Added `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`.

### Output / Artifact Changes

- none outside repository documentation

## 3. Files Touched

- `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- No runtime behavior changes.
- Future runner implementation now has a design contract to follow.
- Future distillation work has explicit train-only, diagnostic-only, JSONL, schema repair, review queue, resume, and audit requirements.

### Preserved Behavior

- Existing Warden code behavior remains unchanged.
- Existing schemas, labels, manifests, samples, splits, training, inference, runtime outputs, and CLIs remain unchanged.
- Existing distillation V0.2 prompt / Skill files remain unchanged.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for production outputs
- draft future JSONL shapes are documented only

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The runner design references `warden_distill_v0.2` as draft distillation-output schema only. It does not freeze production schema or change official Warden runtime schema.

## 6. Validation Performed

### Commands Run

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md
rg -n "warden_distill_v0.2|rule_router|text_semantic_concepts|vision_evidence|decision_head|train split|diagnostic_only|do_not_train_as_gold|needs_human_review|resume|JSONL|schema repair|fallback_reason|DeepSeek-V4 fallback|payload not observed|weak labels are evidence" docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md
git status --short --untracked-files=all -- docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md
```

### Result

- Task doc checker:
  - `[task-doc] OK   docs\tasks\2026-05-12_warden_distillation_runner_design_v1.md`
- Handoff checker:
  - `[handoff-doc] OK   docs\handoff\2026-05-12_warden_distillation_runner_design_v1.md`
- Required-term grep:
  - matched required terms including `warden_distill_v0.2`, `rule_router`, `text_semantic_concepts`, `vision_evidence`, `decision_head`, `train split`, `diagnostic_only`, `do_not_train_as_gold`, `needs_human_review`, `resume`, `JSONL`, `schema repair`, `fallback_reason`, `DeepSeek-V4 fallback`, `payload not observed`, and `weak labels are evidence`.
- Targeted scope status:
  - only the three task-scoped files were reported as new untracked files.

### Not Run

- production distillation runner
- MiMo, DeepSeek, OpenAI, Claude, or other model API calls
- teacher distillation
- teacher label generation
- training
- runtime smoke
- OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference

Reason:

These actions are explicitly outside this design-only task.

Next best check:

Review the design contract before creating any implementation task.

## 7. Risks / Caveats

- This is a design contract, not implementation.
- `warden_distill_v0.2` remains draft.
- Exact future runner CLI names may be refined in an implementation task.
- Exact MiMo / DeepSeek endpoint behavior remains unverified for production execution.
- Split-safety depends on future implementation enforcing fail-closed checks.
- Counter-review residual risk: future implementation may expose edge cases in manifest split fields or sample-key generation.
- Karpathy guardrail residual risk: validation checks document structure and required terms only.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`
- `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`

Doc debt still remaining:

- Future runner implementation task should add implementation docs only after code is approved.
- Future schema-freeze task should occur only after pilot validation and dataset freeze.

## 9. Recommended Next Step

- Review the runner design contract.
- If accepted, create a separate implementation task for dry-run prompt building, schema validation, append-only JSONL writing, and split-policy enforcement.
- Keep teacher API calls and pilot distillation behind a later explicit approval.

## 10. Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_DISTILLATION_RUNNER_DESIGN_V1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

Retrieval / reading performed:

- confirmed current `warden_distill_v0.2` target groups and split policy
- confirmed current L1 semantics and Decision Head draft status
- confirmed prior distillation realignment caveats and validation
- confirmed exact runner design requirements from the user-provided task

Claims supported by evidence:

- Current distillation docs define `warden_distill_v0.2`.
- Current L1 docs separate `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`.
- The task requires design-only runner contract work.

Claims left unsupported or assumed:

- exact future production teacher endpoint behavior
- exact final frozen manifest field names for all future train manifests
- empirical prompt or teacher-output quality

Retrieval stopped because:

- the design scope and required validation commands were clear.

## 10.1 Counter-Review Performed

Original framing reviewed:

Create a runner design contract before implementing the production runner.

Assumptions checked:

- A documentation-only design can freeze safety and split-policy requirements.
- Runner implementation can remain a later task.
- `warden_distill_v0.2` can be referenced as draft without freezing production schema.

Failure modes considered:

- design implying production schema freeze
- val/test contamination
- router output used as teacher label
- schema repair inventing evidence
- text-only fallback claiming visual inspection
- resume overwriting successful JSONL records

Counterexamples or contradictory evidence found:

- none blocking

Alternative routes considered:

- implement runner now
- keep prompt docs only
- create focused runner design contract

Framing changed: NO

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- exact production endpoint details remain future implementation inputs

Residual risks after counter-review:

- future implementation may need to refine sample-key hashing and manifest split resolution

Decision after counter-review:

- ACCEPT_ORIGINAL

## 10.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- This is a design-only task.
- Optional `docs/distillation/README.md` is unnecessary because required cross-links fit in the design document.

Ambiguities resolved or escalated:

- No blocker. The task provided exact files and validation requirements.

### Simplicity First

Simplest acceptable route used:

- Add the three required Markdown files only.

Larger or more speculative routes rejected:

- runner implementation
- model API integration
- pilot distillation
- code-level schema validator
- data or manifest mutation

### Surgical Changes

Touched-file to task-scope mapping:

- `docs/tasks/2026-05-12_warden_distillation_runner_design_v1.md`: active task doc
- `docs/distillation/WARDEN_DISTILLATION_RUNNER_DESIGN_V0.1.md`: required runner design contract
- `docs/handoff/2026-05-12_warden_distillation_runner_design_v1.md`: required handoff

Adjacent cleanup or formatting-only changes:

- none

### Goal-Driven Verification

Verification loop:

- task doc checker -> passed
- handoff checker -> passed
- required-term grep -> passed
- targeted scope status -> passed
