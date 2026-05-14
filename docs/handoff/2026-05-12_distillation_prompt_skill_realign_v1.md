# HANDOFF_20260512_WARDEN_DISTILLATION_PROMPT_SKILL_REALIGN_V1

## 中文版

### 摘要

本次交付创建 Warden distillation prompt / Claude Code Skill V0.2 包，并对齐当前 L1 语义。交付只涉及文档和 Skill 模板：没有实现 runner，没有调用模型 API，没有运行 teacher distillation，没有修改数据、标签、manifest、split、训练、推理、采集或 official schema。

V0.2 明确：`rule_router` 只做路由和证据充分性诊断；`text_semantic_concepts` 是主要蒸馏目标；`vision_evidence` 只做证据恢复；`decision_head` 只接收 advisory auxiliary targets；`weak labels are evidence`；`payload not observed` 不能自动等同于 benign。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF_20260512_WARDEN_DISTILLATION_PROMPT_SKILL_REALIGN_V1
- Related Task ID: TASK-20260512-WARDEN-DISTILLATION-PROMPT-SKILL-REALIGN-V1
- Task Title: Realign Warden Distillation Prompt Pack And Claude Code Skill With Current L1 Semantics
- Module: Distillation / Prompting / Skill / Data Quality
- Author: Codex
- Date: 2026-05-12
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

## 1. Executive Summary

Created a documentation-only V0.2 distillation workflow, prompt pack, project Claude Code Skill, prompt templates, draft schema reference, active task doc, and handoff. The package realigns distillation outputs with the current Warden L1 draft semantics: router diagnostics, text semantic concepts, evidence-only visual observations, and future Decision Head auxiliary targets. The task reached the document-generation stage; validation results are recorded below.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md`.
- Added `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`.
- Added `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`.
- Added `.claude/skills/warden-distillation/SKILL.md`.
- Added `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`.
- Added five prompt template files under `.claude/skills/warden-distillation/templates/`.
- Added this handoff.

### Output / Artifact Changes

- New repository-local documentation and Skill artifacts only.

## 3. Files Touched

- `docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`
- `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`
- `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`
- `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`

## 4. Behavior Impact

### Expected New Behavior

- No runtime behavior changes.
- Future Warden distillation prompt / Skill work has a V0.2 repository-local contract aligned with current L1 semantics.
- The project Skill can guide future Claude Code sessions that work on Warden distillation prompts or teacher-output review.

### Preserved Behavior

- Existing code behavior remains unchanged.
- Existing schema, labels, manifests, samples, splits, and CLI behavior remain unchanged.
- Existing V0.1 / older distillation artifacts were preserved if present.

### User-facing / CLI Impact

- none

### Output Format Impact

- none for production runtime or training outputs
- `warden_distill_v0.2` is documented as draft distillation-output schema only

## 5. Schema / Interface Impact

- Schema changed: NO for existing schemas
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

`warden_distill_v0.2` is documentation-only draft schema for future teacher outputs. It does not replace Warden manifests, labels, runtime results, traces, or training schema.

## 6. Validation Performed

### Commands Run

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md
python -c "from pathlib import Path; required=['docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md','docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md','docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md','.claude/skills/warden-distillation/SKILL.md','.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md','.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md','.claude/skills/warden-distillation/templates/judge_teacher_prompt.md','.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md','.claude/skills/warden-distillation/templates/schema_repair_prompt.md','.claude/skills/warden-distillation/templates/human_review_packet_prompt.md','docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md']; missing=[p for p in required if not Path(p).exists()]; raise SystemExit('Missing files:\n' + '\n'.join(missing)) if missing else print('All required files exist.')"
python -c "from pathlib import Path; p=Path('.claude/skills/warden-distillation/SKILL.md'); text=p.read_text(encoding='utf-8'); assert text.startswith('---\n'), 'SKILL.md missing opening YAML frontmatter'; end=text.find('\n---\n',4); assert end!=-1, 'SKILL.md missing closing YAML frontmatter'; front=text[4:end]; [(_ for _ in ()).throw(SystemExit(f'SKILL.md missing {key}')) for key in ['name:','description:'] if key not in front]; print('SKILL.md frontmatter sanity passed.')"
rg -n "warden_distill_v0.2|rule_router|text_semantic_concepts|vision_evidence|decision_head|action surface is not automatically threat action|payload not observed|weak labels are evidence|do_not_train_as_gold|needs_human_review|DeepSeek-V4 fallback" docs/distillation .claude/skills/warden-distillation
git diff --name-only
```

### Result

- Task doc checker:
  - `[task-doc] OK   docs\tasks\2026-05-12_distillation_prompt_skill_realign_v1.md`
- Handoff checker:
  - `[handoff-doc] OK   docs\handoff\2026-05-12_distillation_prompt_skill_realign_v1.md`
- Corrected file existence check:
  - `All required files exist.`
- SKILL frontmatter sanity check:
  - `SKILL.md frontmatter sanity passed.`
- Required-term grep:
  - matched required terms including `warden_distill_v0.2`, `rule_router`, `text_semantic_concepts`, `vision_evidence`, `decision_head`, `action surface is not automatically threat action`, `payload not observed`, `weak labels are evidence`, `do_not_train_as_gold`, `needs_human_review`, and `DeepSeek-V4 fallback`.
- Scope check:
  - `git diff --name-only` reported pre-existing tracked worktree changes outside this task.
  - Targeted status for this task's scope showed only the 11 scoped files as new untracked files.

Validation note:

An initial one-line file existence check printed `All required files exist.` but exited with `TypeError` because the Python one-liner attempted to raise a non-exception value. It was not counted as passed. The corrected equivalent command was rerun and passed with exit code 0.

### Not Run

- production distillation runner
- MiMo, DeepSeek, OpenAI, Claude, or other model API calls
- teacher distillation batches
- training
- runtime smoke
- OCR, YOLO, CLIP, MobileCLIP, SNet, or SpecularNet-like inference

Reason:

These actions are explicitly out of scope for this documentation / Skill realignment task.

Next best check:

Before any production teacher run, verify the exact configured MiMo / DeepSeek endpoints and add runner-level schema validation in a separate approved task.

## 7. Risks / Caveats

- Prompt quality has not been empirically validated.
- Exact local MiMo invocation method remains unverified.
- Exact DeepSeek endpoint configuration and image-input capability remain unverified.
- DeepSeek-V4 fallback is therefore limited to text / metadata / judge / schema repair until endpoint modality is verified.
- Future runner implementation must add real JSON schema validation and split-policy enforcement.
- Counter-review residual risk: future implementation may refine schema field names before a formal schema freeze.
- Karpathy guardrail residual risk: this task validates documents and prompt contents only, not teacher quality.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md`
- `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
- `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
- `.claude/skills/warden-distillation/SKILL.md`
- `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
- `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`
- `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`
- `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`
- `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`
- `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`

Doc debt still remaining:

- Future implementation tasks should add runner docs only when runner work is explicitly approved.
- Future schema-freeze work should occur only after dataset freeze and pilot validation.

## 9. Recommended Next Step

- Review V0.2 prompt and schema semantics.
- If accepted, create a separate runner implementation task with explicit API, storage, schema validation, resume, and split-policy enforcement requirements.
- Verify MiMo and DeepSeek endpoint details again before any production teacher run.

## 10. Evidence / Retrieval Performed

Evidence sources actually checked:

- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_DISTILLATION_PROMPT_SKILL_REALIGN_V1.md`
- `C:\Users\20516\Downloads\TASK_DISTILLATION_PROMPT_SKILL_V0_1.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/modules/Warden_DISTILLATION_INFRASTRUCTURE_TASK_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- official MiMo website: `https://mimo.mi.com/`
- official DeepSeek API docs: `https://api-docs.deepseek.com/quick_start/pricing/`, `https://api-docs.deepseek.com/guides/json_mode/`
- official Claude Code Skills docs: `https://code.claude.com/docs/en/skills`

Retrieval / reading performed:

- checked old V0.1 task to preserve useful prompt / fallback intent while revising L1 semantics
- checked current L1 Decision Head contract and latest L1 router handoff
- checked official external docs for MiMo, DeepSeek, and Claude Code Skill claims

Claims supported by evidence:

- Current Warden L1 separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`.
- MiMo official website states Token Plan support for V2.5 models and Claude Code ecosystem compatibility.
- DeepSeek official docs list DeepSeek-V4 model IDs and JSON Output support.
- Claude Code official docs describe project Skills under `.claude/skills/<skill-name>/SKILL.md` and frontmatter.

Claims left unsupported or assumed:

- exact local MiMo invocation method in this repo
- exact user DeepSeek endpoint modality support
- empirical prompt validity

Retrieval stopped because:

- required workflow, prompt, Skill, and schema docs could be produced without additional unsupported production claims.

## 10.1 Counter-Review Performed

Original framing reviewed:

Realign Warden distillation prompt / Skill package with current L1 semantics without implementing runner behavior or changing production contracts.

Assumptions checked:

- V0.2 can supersede V0.1 semantically while preserving historical files.
- Rule-router context can be included as diagnostic input only.
- DeepSeek fallback can be documented safely when modality limits are explicit.

Failure modes considered:

- router output becoming teacher label source
- text-only fallback claiming screenshot observation
- advisory labels overriding human labels
- teacher outputs contaminating val/test
- CLIP / SNet becoming implied default online L1 components

Counterexamples or contradictory evidence found:

- none blocking

Alternative routes considered:

- keep V0.1 unchanged
- create V0.2 docs / Skill package only
- implement runner now

Framing changed: NO

If changed, what changed:

none

Claims left unsupported or assumed after counter-review:

- exact production model endpoint details remain unverified

Residual risks after counter-review:

- future runner task may need stricter machine-readable schema validation

Decision after counter-review:

- ACCEPT_ORIGINAL

## 10.2 Karpathy Guardrail Check

### Think Before Acting

Assumptions surfaced before or during execution:

- This is documentation / Skill work only.
- Any runner, API call, data change, training change, or schema freeze is out of scope.

Ambiguities resolved or escalated:

- No blocker. The user-provided task fixed exact file paths and validation requirements.

### Simplicity First

Simplest acceptable route used:

- Add only the 11 scoped files and run required documentation / grep / scope validations.

Larger or more speculative routes rejected:

- runner implementation
- API integration
- pilot teacher batch
- training or runtime edits
- schema freeze

### Surgical Changes

Touched-file to task-scope mapping:

- task doc -> active task artifact
- distillation workflow and prompt docs -> required documentation outputs
- `.claude/skills/warden-distillation/**` -> required Skill, schema reference, and prompt templates
- handoff -> required delivery record

Adjacent cleanup or formatting-only changes:

- none

### Goal-Driven Verification

Verification loop:

- task doc checker -> passed
- handoff checker -> passed
- file existence check -> passed after corrected rerun
- Skill frontmatter check -> passed
- required-term grep -> passed
- scope check -> targeted task scope passed; full `git diff --name-only` contains pre-existing unrelated tracked changes
