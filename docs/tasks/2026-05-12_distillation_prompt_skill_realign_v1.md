# TASK_20260512_WARDEN_DISTILLATION_PROMPT_SKILL_REALIGN_V1

## 中文版

### 摘要

本任务把旧的 Warden distillation prompt / Claude Code Skill 方案升级为 V0.2，并对齐当前 L1 语义：`rule_router` 只做路由和证据充分性诊断，`text_semantic_concepts` 是文本语义概念目标，`vision_evidence` 是 OCR / YOLO 证据恢复，`decision_head` 是未来最终裁决组件且当前为 `not_run`。

本任务只创建文档、prompt 模板、Skill 和 draft schema reference。不得实现 runner，不调用任何模型 API，不运行 teacher distillation，不修改训练、推理、采集、标签、manifest、样本、split 或既有 schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260512-WARDEN-DISTILLATION-PROMPT-SKILL-REALIGN-V1
- Task Title: Realign Warden Distillation Prompt Pack And Claude Code Skill With Current L1 Semantics
- Owner Role: Codex executor, GPT Web reviewer, human final acceptor
- Priority: P0
- Status: TODO
- Related Module: Distillation / Prompting / Skill / Data Quality
- Related Issue / ADR / Doc: `TASK_DISTILLATION_PROMPT_SKILL_V0_1.md`, `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`, `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`, `PROJECT.md`
- Created At: 2026-05-12
- Requested By: 佶
- Karpathy Guardrails Required: YES

Use this template for any non-trivial engineering task in Warden.

## 1. Background

The earlier V0.1 distillation prompt / Skill task defined a useful teacher workflow, but Warden L1 semantics have since changed. The current L1 draft sidecar separates `rule_router`, `text_semantic_concepts`, `vision_evidence`, and `decision_head`. The `rule_router` is a routing and evidence-sufficiency diagnostic component. It must not be used as a teacher-label source. The `decision_head` is currently `not_run` and future-owned.

This task creates a V0.2 documentation and Skill package that aligns teacher outputs with current L1 semantics without implementing a runner or changing production contracts.

## 2. Goal

Create a repository-ready V0.2 Warden distillation workflow, prompt pack, Claude Code Skill, and draft schema reference that target structured semantic concepts, relation judgments, evidence observations, Decision Head auxiliary targets, and review / QC flags while preventing teacher outputs from overriding human gold labels or contaminating validation / test splits.

## 3. Scope In

This task is allowed to touch:

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

This task is allowed to change:

- distillation workflow documentation;
- prompt templates for future teacher runs;
- project-level Claude Code Skill instructions;
- draft distillation-output schema documentation only.

If older V0.1 files exist, preserve them and mark V0.2 as superseding V0.1 for current Warden L1 semantics.

## 4. Scope Out

This task must NOT do the following:

- Do not implement a production distillation runner.
- Do not call MiMo, DeepSeek, OpenAI, Claude, or any external model API.
- Do not run teacher distillation.
- Do not modify dataset files, labels, manifests, train / val / test split, or samples.
- Do not modify training code, inference code, capture code, crawler code, or labeling scripts.
- Do not change existing Warden schema fields, output schema, label enums, or CLI commands.
- Do not add third-party dependencies.
- Do not train or define a final model architecture beyond draft target semantics.
- Do not claim prompt empirical validity without a later pilot run.

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `C:\Users\20516\Downloads\TASK_20260512_WARDEN_DISTILLATION_PROMPT_SKILL_REALIGN_V1.md`
- `C:\Users\20516\Downloads\TASK_DISTILLATION_PROMPT_SKILL_V0_1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`
- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/modules/Warden_DISTILLATION_INFRASTRUCTURE_TASK_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/MODULE_TRAIN.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none; no data files may be changed by this task.

### Prior Handoff

- `docs/handoff/2026-05-12_warden_l1_rule_router_decision_head_realign_v1.md`
- `docs/handoff/2026-05-12_warden_l1_decision_head_contract_v1.md`

### Missing Inputs

- exact local MiMo invocation method inside Claude Code;
- exact DeepSeek endpoint configuration and credentials;
- empirical prompt quality results;
- final frozen benign + malicious dataset manifests.

## 6. Required Outputs

This task should produce:

1. `docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md`
2. `docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md`
3. `docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md`
4. `.claude/skills/warden-distillation/SKILL.md`
5. `.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md`
6. `.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md`
7. `.claude/skills/warden-distillation/templates/judge_teacher_prompt.md`
8. `.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md`
9. `.claude/skills/warden-distillation/templates/schema_repair_prompt.md`
10. `.claude/skills/warden-distillation/templates/human_review_packet_prompt.md`
11. `docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md`

All Markdown deliverables must be bilingual by default: Chinese summary first, English authoritative section second.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial change.
- Keep `rule_router` outputs under `rule_router_context` or routing hints when included as teacher input.
- Keep teacher outputs separate from human gold labels and dataset-management metadata.
- Keep `warden_distill_v0.2` as draft distillation-output schema only.
- Mark external model claims as source-backed or unverified.

Task-specific constraints:

- `rule_router` outputs are routing / evidence sufficiency diagnostics only.
- `text_semantic_concepts` must include action surfaces, behavior contexts, relation consistency, legitimacy hints, risk axes, page roles, and routing recommendations.
- Prompt templates must include: `action surface is not automatically threat action`.
- Prompt templates must include: `payload not observed` is not automatic benign.
- Prompt templates must include: `weak labels are evidence`.
- Vision observations are evidence only and cannot be final labels.
- CLIP / SNet / SpecularNet-like routes are not Warden V1 default online L1 assumptions.
- Formal teacher distillation waits for final benign + malicious dataset freeze and runs on train split by default.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing Warden data layout;
- existing manifests, labels, splits, and samples;
- existing training, inference, capture, crawler, labeling, and runtime CLIs;
- official runtime result / trace schema.

Schema / field constraints:

- Schema changed allowed: NO for existing schemas.
- New draft distillation-output schema allowed: YES, documentation only.
- Frozen field names involved: existing manifest / label / runtime fields must not change.

CLI / output compatibility constraints:

- Existing commands must keep working.
- No existing CLI command may be edited.

Downstream consumers to watch:

- future text semantic concept training;
- future Decision Head training;
- manual review tooling;
- dataset split and evaluation logic.

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- MiMo-V2.5 Token Plan and Claude Code ecosystem compatibility.
- DeepSeek-V4 model IDs and JSON output support.
- Claude Code project Skill path and `SKILL.md` frontmatter structure.
- Current Warden L1 semantics.

Allowed evidence sources:

- official MiMo website;
- official DeepSeek API docs;
- official Claude Code Skills docs;
- existing Warden repository docs and handoffs;
- user-provided task documents.

Missing-evidence behavior:

- Mark unresolved model invocation or modality claims as unverified.
- Do not assume DeepSeek-V4 is visual unless the configured endpoint supports image input and image input is passed.

### 9.1 Counter-Review Requirements

Current proposed framing:

Realign the prompt / Skill package so distillation trains future L1 semantic targets and Decision Head auxiliary targets without treating rule-router output or teacher advisory labels as gold labels.

Hidden assumptions to check:

- MiMo can be represented as a primary teacher without local invocation details.
- DeepSeek-V4 fallback is safe when constrained to text / metadata / judge / schema repair.
- Prompt documentation can be useful before a production runner exists.

Failure modes to consider:

- `rule_router` re-enters the workflow as a classifier.
- A text-only fallback claims visual observation.
- Advisory labels contaminate human labels or val/test split.
- Prompt outputs reveal hidden chain-of-thought.
- Prompt wording implies CLIP / SNet are default online L1 components.

Alternative routes to compare:

- keep V0.1 unchanged;
- add a narrow V0.2 superseding package;
- implement a runner now.

Decision rule:

- Accept the V0.2 documentation route if it can satisfy semantic realignment without touching code, data, schema, labels, or runtime behavior.
- Stop and escalate if implementation requires production runner behavior, schema freeze, label changes, or model API calls.

### 9.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Assume this task is documentation / Skill only because scope explicitly excludes runner and API execution.
- No ambiguity requires clarification because the scope-in file list is exact.

Simplicity boundary:

- The simplest acceptable solution is to add only the 11 scoped files and run the required validation commands.

Surgical change boundary:

- Every touched file must be one of the 11 scope-in paths.
- Adjacent cleanup is forbidden.

Goal-driven verification loop:

- Required files exist -> file existence check.
- Skill frontmatter valid -> frontmatter sanity check.
- Task and handoff conform -> Warden doc checkers.
- Required semantics present -> required-term grep.
- Scope preserved -> `git diff --name-only` review.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] All required files exist.
- [ ] Skill has valid YAML frontmatter.
- [ ] V0.2 workflow doc supersedes V0.1 for current L1 semantics.
- [ ] Prompt pack contains primary, judge, DeepSeek fallback, schema repair, and human-review packet prompts.
- [ ] Schema reference defines `warden_distill_v0.2` and marks it as draft distillation-output schema.
- [ ] Rule router is not treated as a teacher label source.
- [ ] Vision evidence is treated as evidence recovery, not classifier output.
- [ ] CLIP / SNet are not default online L1 assumptions.
- [ ] Formal distillation waits for final dataset freeze and runs on train split by default.
- [ ] Validation commands were run or inability is documented.
- [ ] No production runner, model API call, schema change, label change, data move, or training change was made.

## 11. Validation Checklist

Minimum validation expected:

```bash
python scripts/ci/check_task_doc.py docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md
```

File existence check:

```bash
python - <<'PY'
from pathlib import Path
required = [
    'docs/tasks/2026-05-12_distillation_prompt_skill_realign_v1.md',
    'docs/distillation/WARDEN_DISTILLATION_WORKFLOW_V0.2.md',
    'docs/distillation/WARDEN_DISTILLATION_PROMPTS_V0.2.md',
    '.claude/skills/warden-distillation/SKILL.md',
    '.claude/skills/warden-distillation/references/warden_distillation_schema_v0_2.md',
    '.claude/skills/warden-distillation/templates/primary_mllm_teacher_prompt.md',
    '.claude/skills/warden-distillation/templates/judge_teacher_prompt.md',
    '.claude/skills/warden-distillation/templates/deepseek_v4_fallback_prompt.md',
    '.claude/skills/warden-distillation/templates/schema_repair_prompt.md',
    '.claude/skills/warden-distillation/templates/human_review_packet_prompt.md',
    'docs/handoff/2026-05-12_distillation_prompt_skill_realign_v1.md',
]
missing = [p for p in required if not Path(p).exists()]
if missing:
    raise SystemExit('Missing files:\n' + '\n'.join(missing))
print('All required files exist.')
PY
```

SKILL frontmatter check:

```bash
python - <<'PY'
from pathlib import Path
p = Path('.claude/skills/warden-distillation/SKILL.md')
text = p.read_text(encoding='utf-8')
if not text.startswith('---\n'):
    raise SystemExit('SKILL.md missing opening YAML frontmatter')
end = text.find('\n---\n', 4)
if end == -1:
    raise SystemExit('SKILL.md missing closing YAML frontmatter')
front = text[4:end]
for key in ['name:', 'description:']:
    if key not in front:
        raise SystemExit(f'SKILL.md missing {key}')
print('SKILL.md frontmatter sanity passed.')
PY
```

Required grep check:

```bash
rg -n "warden_distill_v0.2|rule_router|text_semantic_concepts|vision_evidence|decision_head|action surface is not automatically threat action|payload not observed|weak labels are evidence|do_not_train_as_gold|needs_human_review|DeepSeek-V4 fallback" docs/distillation .claude/skills/warden-distillation
```

Scope check:

```bash
git diff --name-only
```

The relevant diff for this task must remain within Scope In.

## 12. Stop Rules

Stop and report completion when:

- the 11 scoped files exist;
- required validation has passed or unrun checks are explicitly explained;
- handoff is written;
- no out-of-scope files were intentionally modified;
- no runner, API call, data move, schema change, label change, or training change was made.

Stop and escalate if:

- a production runner becomes necessary;
- any schema / label / split / runtime output change is needed;
- external evidence contradicts the model-routing policy;
- validation fails and root cause is unclear.

## 13. Handoff Requirements

The handoff must include:

- files created / edited;
- exact external facts verified or explicitly unverified;
- validation commands and results;
- whether V0.1 files were preserved;
- risks around model modality or fallback;
- confirmation that no API calls or distillation batches were run;
- explicit note that the output schema is draft only.
