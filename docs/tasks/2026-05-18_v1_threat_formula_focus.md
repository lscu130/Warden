# Task Metadata

- Task ID: WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS
- Task Title: Refocus Warden V1 Threat Definition Around Context Plus Induced Action Formula
- Owner Role: Codex
- Priority: P0
- Status: TODO
- Related Module: project governance / threat definition / L0-L1 documentation
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS.md
- Created At: 2026-05-18
- Requested By: user
- Karpathy Guardrails Required: YES

## 中文版

本任务按用户提供的外部任务单执行，目标是把 Warden V1 的主威胁定义收敛到：

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)
InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

本任务只做文档定义与范围校准，不修改运行时代码、schema、字段名、枚举、CLI、输出结构或数据集样本。成人、博彩、枪支、毒品等 high-risk-content-only 页面，以及 gate-only / challenge-only / CAPTCHA-only / redirect-only / trusted-sink-only / evasion-only 捕获，不作为 V1 主任务威胁类别；若下游页面满足公式，可由下游页面进入主判断。

## English Version

AI note: English is authoritative for exact scope, constraints, validation, and compatibility.

## 1. Background

The user provided an external execution task at `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS.md`.

The repository contains several active governance and module documents that still describe Warden V1 with broader wording such as behavior-only threat, high-risk-content categories, gate/evasion handling, or legacy L2-related framing. The task requires a documentation-only refocus around the final V1 threat formula while preserving existing schemas, labels, CLI flags, outputs, and runtime behavior.

## 2. Goal

Align Warden's active definition and scope documentation around the final V1 formula:

```text
Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)
InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation
```

The goal is a minimal, reviewable, reversible documentation patch that makes V1 focus on observable webpage social-engineering threat detection and lightweight local deployment, without changing implementation contracts.

## 3. Scope In

This task is allowed to touch:

- `AGENTS.md`
- `PROJECT.md`
- `README.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/threat_model/WARDEN_THREAT_ADJUDICATION_FLOW_V1.md`
- relevant active docs under `docs/data/`, `docs/modules/`, `docs/frozen/`, and `docs/l1/` that contain conflicting V1 definition wording
- `docs/tasks/2026-05-18_v1_threat_formula_focus.md`
- `docs/handoff/2026-05-18_v1_threat_formula_focus.md`

This task is allowed to change:

- wording that defines Warden V1 Web-SE Threat
- documentation that classifies phishing as a subset of Web-SE Threat
- documentation that clarifies adult/gambling/guns/drugs high-risk-content-only pages are outside V1 main objective
- documentation that clarifies gate-only/challenge-only/CAPTCHA-only/redirect-only/trusted-sink-only/evasion-only captures are excluded or auxiliary unless downstream content satisfies the formula
- documentation that clarifies no current online L2 architecture is introduced by this task

## 4. Scope Out

This task must NOT do the following:

- change runtime code
- change schemas, schema versions, frozen field names, enums, CLI flags, output structures, or dataset layout
- delete labels or fields such as adult, gambling, gate, evasion, `needs_l2_candidate`, or legacy route names
- create a new L2 architecture
- add dependencies
- rename files or broad-refactor documentation structure
- reclassify existing samples or regenerate data artifacts
- treat high-risk-content-only pages or gate-only captures as V1 malicious solely by category or capture pattern

## 5. Inputs

Relevant inputs for this task:

### Docs

- `C:\Users\20516\Downloads\WARDEN_TASK_20260518_V1_THREAT_FORMULA_FOCUS.md`
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `PROJECT.md`

### Code / Scripts

- `scripts/ci/check_task_doc.py`
- `scripts/ci/check_handoff_doc.py`

### Data / Artifacts

- none

### Prior Handoff

- none required

### Missing Inputs

- none

## 6. Required Outputs

This task should produce:

- updated active Markdown docs that express the final V1 formula consistently
- a repo-local task document at `docs/tasks/2026-05-18_v1_threat_formula_focus.md`
- a repo-local handoff document at `docs/handoff/2026-05-18_v1_threat_formula_focus.md`
- validation summary covering residual wording search, schema/JSON/YAML non-change checks, and task/handoff checker status

Output format requirements:

- Markdown deliverables must be bilingual where they are user-facing project artifacts.
- English is authoritative for exact task, validation, and compatibility wording.
- Final response must follow Warden engineering-task format.

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial documentation change.

Task-specific constraints:

- Do not modify `src/**`, tests, scripts, schemas, data manifests, or runtime behavior.
- Do not remove adult/gambling/gate/evasion labels or fields; only clarify their V1 role as auxiliary, exclusion, or future-scope.
- Do not describe manipulative context alone as sufficient for V1 malicious; V1 requires induced high-risk action evidence.
- Do not describe missing payload/action as automatic benign.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing CLI commands
- existing schema files and schema versions
- existing output file names and JSON/YAML structures
- existing label/enumeration values

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none may be renamed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - not changed by this documentation-only task

Downstream consumers to watch:

- labeling and training docs that depend on stable labels
- inference docs that depend on L0/L1 boundary language
- future review workflows that may still use legacy route names

## 9. Evidence / Retrieval Rules

Facts or claims that require support:

- which docs contain old V1 threat wording
- whether JSON/YAML/schema/runtime files were changed
- whether task and handoff docs satisfy repo checker structure

Allowed evidence sources:

- user-provided external task document
- repository governing docs and active module docs
- targeted `rg`, `git diff`, `git status`, and checker command outputs

Retrieval budget:

- Initial retrieval: governing docs plus active docs likely to contain V1 definition, L0/L1, label, or gate/evasion wording.
- Additional retrieval is allowed only when targeted search shows unresolved conflicting wording.
- Stop retrieval when active-doc residual hits are either patched or classified as compatible/historical.

Missing-evidence behavior:

- Report unknown or unverified status explicitly; do not infer implementation or data behavior from documentation edits.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Core active docs state or align with `Web-SE Threat := EvidenceSufficient(ManipulativeContext ∧ InducedHighRiskAction)`.
- [ ] `InducedHighRiskAction := DirectAction ∨ RoutedAction ∨ ActionPreparation` is documented in central definition docs.
- [ ] Phishing is described as a subset of Web-SE Threat.
- [ ] High-risk-content-only pages are excluded from V1 main objective unless they also satisfy the formula.
- [ ] Gate-only/challenge-only/CAPTCHA-only/redirect-only/trusted-sink-only/evasion-only captures are not treated as V1 malicious solely by capture pattern.
- [ ] No runtime code, schema, CLI, JSON, YAML, or output structure is changed.
- [ ] Legacy labels/fields are preserved and reclassified rather than deleted.
- [ ] Residual old-wording search is performed and classified.
- [ ] `docs/handoff/2026-05-18_v1_threat_formula_focus.md` is created.
- [ ] Task and handoff checker scripts are run or failures are reported honestly.

## 11. Validation Checklist

Minimum validation expected:

- [ ] targeted `rg` for formula terms and old behavior-only wording
- [ ] targeted `rg` for adult/gambling/gate/L2-related residual wording
- [ ] `git diff --stat` scoped to task-touched docs
- [ ] changed-file check confirming no JSON/YAML files in task scope changed
- [ ] `python scripts/ci/check_task_doc.py docs/tasks/2026-05-18_v1_threat_formula_focus.md`
- [ ] `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-18_v1_threat_formula_focus.md`

Commands to run if applicable:

```bash
rg -n "behavior-only|behavior_only|high-risk deceptive behavior and/or|Web-SE Threat|EvidenceSufficient|ManipulativeContext|InducedHighRiskAction" AGENTS.md PROJECT.md README.md docs -g "*.md"
git diff --stat -- AGENTS.md PROJECT.md README.md docs
git diff --name-only -- AGENTS.md PROJECT.md README.md docs | rg "\.(json|ya?ml)$"
python scripts/ci/check_task_doc.py docs/tasks/2026-05-18_v1_threat_formula_focus.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-18_v1_threat_formula_focus.md
```

Expected evidence to capture:

- formula terms appear in central definition docs
- old active behavior-only formula references are removed or classified as compatible residuals
- no JSON/YAML/schema/runtime files were touched by this task
- task/handoff checkers pass, or any checker mismatch is explicitly documented

## 12. Stop Rules

The executor should stop and report completion when all of the following are true:

- relevant docs have been patched or residual hits classified
- validation checklist has been run or any non-run item has an explicit reason
- handoff is created and compatibility impact is documented

The executor should stop and escalate instead of continuing when any of the following happens:

- schema, CLI, runtime, data, or label enum changes appear necessary
- active task scope requires files outside the allowed documentation scope
- residual old wording cannot be safely classified without user approval
