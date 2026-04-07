# Warden Distillation Infrastructure Task (V1)

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是给 Codex 的**执行任务单**，目标是落地 Warden 的蒸馏基础设施，而不是冻结最终蒸馏策略。
- 若涉及精确字段名、目录、CLI、输出格式、验收条件或缺失输入，以英文版为准。
- 本任务默认属于 **non-trivial engineering task**，必须遵守 `AGENTS.md`、`GPT_CODEX_WORKFLOW.md`、`TASK_TEMPLATE.md`、`HANDOFF_TEMPLATE.md`。
- 若本任务继续协作，需将本文件复制进仓库路径，例如：`docs/tasks/2026-03-30_distillation_infrastructure_v1.md`。

## 1. 背景摘要

Warden 当前已冻结项目级方向、文本/视觉/边缘部署主线，但蒸馏相关内容仍处于“可开工基础设施、暂不冻结最终标签空间”的阶段。
当前更适合先搭 teacher 推理、teacher 输出缓存、pseudo-label 存储、student 数据读取、基础训练入口和 smoke 验证骨架，
不适合现在就把最终 detector class list、最终 concept inventory、最终 loss 权重、最终 benchmark 阈值写死。

## 2. 任务目标摘要

本任务只构建蒸馏基础设施，使仓库具备：
- 离线 teacher 产出缓存能力；
- 蒸馏样本读取与统一 artifact 存储能力；
- student 训练入口与最小 smoke 跑通能力；
- 明确的占位配置与版本化输出；
- 文档化的接口与缺失项声明。

本任务**不**要求完成最终 teacher 选择定稿、最终标签语义冻结、最终蒸馏指标达标、最终大规模训练结果。

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Warden Distillation Infrastructure Task (V1)

# Task Metadata

- Task ID: WD-DISTILL-INFRA-V1
- Task Title: Build distillation infrastructure skeleton for Warden without freezing final label space
- Owner Role: GPT Web task drafter for Codex execution
- Priority: High
- Status: TODO
- Related Module: Training / Inference / Data Interface / Docs
- Related Issue / ADR / Doc: `PROJECT.md`, `Warden_VISION_PIPELINE_V1.md`, `Warden_TEXT_PIPELINE_V1.md`, `Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- Created At: 2026-03-30
- Requested By: Human project owner

Use this task for non-trivial distillation infrastructure work only.

---

## 1. Background

Warden already has project-level direction, staged inference positioning, and default text / vision / edge deployment profiles.
However, the repository does not yet have a stable distillation infrastructure layer that supports:

- offline teacher execution,
- cached teacher outputs,
- pseudo-label persistence,
- student-ready dataset readers,
- basic distillation training entrypoints,
- smoke validation for the teacher-student path.

At the current project stage, the correct target is **infrastructure-first distillation**, not **final label-aligned distillation**.
This means the repository should gain a bounded, auditable distillation skeleton now, while leaving final detector classes, final concept inventory, final threshold policy, and final benchmark targets open.

This task is needed now because:

1. the owner currently has time to prepare deployment / training infrastructure while data work continues;
2. the project already allows stronger offline teacher tools while keeping runtime lightweight;
3. distillation infrastructure can be built against the existing sample contract without waiting for every final label to be frozen;
4. delaying all distillation work until full label completion would unnecessarily postpone executable prototype work.

---

## 2. Goal

Build a repository-ready distillation infrastructure skeleton that can ingest current Warden sample artifacts, run or mock offline teacher export, persist teacher outputs in a versioned format, read those outputs for student-side distillation, and execute at least a minimal smoke path. The implementation must remain label-space-flexible, backward compatible with current repository contracts, documentation-first, and explicit about what is placeholder versus what is already runnable.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`
- `scripts/`
- `configs/` if it does not already exist and is needed for distillation config skeletons

This task is allowed to change or add:

- a new distillation module spec doc;
- a new active repo task doc copied from this task artifact;
- distillation infrastructure scripts and configs;
- teacher-output cache schema that is **new and additive**;
- smoke-entry CLI or script entrypoint for distillation;
- minimal documentation links needed to explain the new infrastructure.

Preferred repo targets include, but are not limited to:

- `docs/modules/Warden_DISTILLATION_PIPELINE_V1.md`
- `docs/tasks/2026-03-30_distillation_infrastructure_v1.md`
- `docs/handoff/2026-03-30_distillation_infrastructure_v1.md`
- `scripts/distill/` or another narrowly scoped equivalent path
- `configs/distill/` or another narrowly scoped equivalent path

If the exact target path differs, keep it minimal and explicit.

---

## 4. Scope Out

This task must NOT do the following:

- do not freeze or redesign the final label ontology;
- do not redesign TrainSet V1 primary schema;
- do not rename frozen fields, filenames, or enumerations;
- do not silently change current runtime sample contracts;
- do not replace the current text or vision runtime with teacher-heavy online inference;
- do not claim large-scale distillation results or benchmark numbers that were not actually run;
- do not build a monolithic end-to-end training system if a smaller skeleton suffices;
- do not add new third-party dependencies unless explicitly required and approved;
- do not modify unrelated capture, labeling, or deployment logic outside explicit distillation needs;
- do not treat pseudo-labels as human gold labels.

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- any existing training / inference module docs relevant to student-side integration

### Code / Scripts

- existing sample readers, dataset scripts, or manifest scripts already present in repo;
- any current runtime packaging utilities that can be reused safely;
- any current benchmark or smoke-test entrypoint that can be reused safely.

### Data / Artifacts

- current successful sample contract files, especially:
  - `screenshot_viewport.png`
  - optional `screenshot_full.png`
  - `visible_text.txt`
  - `forms.json`
  - `url.json`
  - `redirect_chain.json` when present
  - `net_summary.json`
- any current manifest or consistency outputs already used in repo workflows.

### Prior Handoff

- latest relevant deployment / pipeline handoff if available;
- otherwise write `none` explicitly.

### Missing Inputs

The following are intentionally not frozen yet and must be treated as open inputs, not blockers for infrastructure work:

- exact final detector class inventory;
- exact final text concept inventory;
- exact final teacher set per subtask;
- exact final distillation loss weighting;
- exact final acceptance benchmark thresholds by hardware tier.

If any additional required repo input is missing, state it explicitly before editing.

---

## 6. Required Outputs

This task should produce:

- one distillation module spec markdown document inside the repo;
- one repo task document copied from this task artifact;
- one repo handoff document after implementation;
- one minimal distillation config skeleton or config directory;
- one teacher-output artifact contract definition (doc and/or schema stub);
- one student-side dataset reader or loader skeleton for distillation inputs;
- one smoke-run entrypoint or script that proves the infrastructure path is wired;
- one explicit statement of which parts are runnable now versus placeholder or mock.

Concrete examples of acceptable outputs:

- `docs/modules/Warden_DISTILLATION_PIPELINE_V1.md`
- `scripts/distill/export_teacher_outputs.py`
- `scripts/distill/train_student_smoke.py`
- `scripts/distill/common_io.py`
- `configs/distill/base_distill.yaml`
- `docs/handoff/2026-03-30_distillation_infrastructure_v1.md`

These file names are examples, not mandatory exact names, unless the implementer chooses them.

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format for existing modules.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial task.
- Keep the distillation design **label-space-flexible**.
- Separate **observed teacher output** from **final project judgment labels**.
- Keep teacher tools offline-only by default; do not make them default online runtime dependencies.
- Mark any placeholder / mock teacher path explicitly.
- Keep staged-system discipline: distillation infrastructure must not silently collapse L0/L1/L2 boundaries.

Task-specific constraints:

- teacher output storage must be versioned or explicitly schema-tagged;
- student input readers must tolerate partially missing teacher outputs;
- smoke validation must be honest and minimal;
- documentation must clearly distinguish runnable baseline vs future extensions.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current successful sample directory contract;
- current frozen output file names for sample artifacts;
- current default runtime path for text / vision / deployment docs;
- current staged-system interpretation.

Schema / field constraints:

- Schema changed allowed: YES, but only for **new additive distillation artifacts**.
- If yes, required compatibility plan: all new distillation outputs must live under new files / new paths and must not overwrite existing frozen sample files.
- Frozen field names involved: existing sample contract file names and existing documented manifest / label fields are frozen unless explicitly approved otherwise.

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - current capture workflows
  - current labeling workflows
  - current manifest / consistency workflows unless explicitly untouched
- New distillation commands must be additive rather than replacing current entrypoints.

Downstream consumers to watch:

- future student training scripts;
- future evaluation scripts;
- docs that may reference distillation as part of training or deployment planning.

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and confirm stable contracts.
2. Identify the minimal repo paths needed for distillation infrastructure.
3. Draft or add the distillation module spec doc first.
4. Add common artifact IO utilities for teacher outputs.
5. Add a minimal teacher export path:
   - real export if safely feasible with current dependencies, or
   - explicit mock export path if full teacher execution is not yet appropriate.
6. Add a student-side reader / dataloader skeleton that consumes the distillation artifacts.
7. Add a minimal train-smoke entrypoint or config-driven smoke path.
8. Run the smallest meaningful validation.
9. Produce a repo handoff doc.

Task-specific execution notes:

- if a real teacher model is too heavy or dependency-risky at this stage, prefer a clearly marked mock or stub path over speculative dependency expansion;
- if a final label mapping is unclear, use extensible field naming and document the open mapping rather than inventing final semantics;
- if no training script structure exists yet, create the smallest isolated skeleton rather than refactoring the whole repo into a new framework.

---

## 10. Acceptance Criteria

This task is accepted only if all of the following hold:

1. A distillation module spec doc is added to the repo.
2. The active task doc is copied into the repo under `docs/tasks/` or equivalent tracked path.
3. The implementation creates an isolated distillation infrastructure path without breaking existing sample contracts.
4. New teacher-output artifacts are additive and versioned or schema-tagged.
5. A student-side reader or loader skeleton exists and can consume the new artifacts.
6. A minimal smoke path exists and is actually run if feasible.
7. If any part could not be run, the missing execution is stated explicitly.
8. The implementation does not freeze final label ontology prematurely.
9. The implementation does not make teacher models mandatory online runtime dependencies.
10. A repo handoff doc is produced and matches `HANDOFF_TEMPLATE.md` expectations.
11. Compatibility impact is stated explicitly.
12. Risks and open items are stated explicitly.

---

## 11. Validation Checklist

Minimum required validation:

- doc path exists and is readable;
- new script entrypoints import successfully or pass syntax sanity;
- new config files parse if configs are added;
- a smoke path is exercised on at least one tiny representative sample or one explicit mock sample path;
- teacher-output write/read roundtrip is sanity-checked;
- missing-teacher-output degraded mode is sanity-checked if such logic is implemented;
- any newly introduced CLI flag or command is documented.

If anything was not run, report exactly:

- what was not run;
- why it was not run;
- what should be run next.

---

## 12. Risks / Caveats

Known risks at task-definition time:

- final label mapping may still change;
- teacher choice may differ across text vs vision subpaths;
- dependency expansion pressure may appear if the implementation tries to run heavy teachers immediately;
- overly ambitious refactor could drift beyond infrastructure-first scope;
- a fake sense of completion may appear if mock export is mistaken for full distillation readiness.

Required handling:

- keep scope narrow;
- document placeholders;
- separate runnable now vs future work;
- preserve backward compatibility;
- explicitly state open items.

---

## 13. Doc Updates Needed

At minimum, check whether the following docs need update or cross-reference:

- `PROJECT.md`
- training-related module docs
- inference-related module docs if new artifact assumptions affect them
- any deployment doc that references future distilled students

If no update is made to a potentially relevant doc, state whether it is unnecessary now or still needed later.

---

## 14. Fixed Execution Instruction For Codex

Use the following execution instruction when handing this task to Codex:

```text
You are the execution engineer for the Warden project.
Read AGENTS.md, PROJECT.md, relevant module docs, and this task doc before editing.

Execution requirements:
1. State which files you will modify before editing.
2. Edit only inside scope_in.
3. Do not touch scope_out.
4. Do not rename frozen fields, frozen file names, or frozen enumerations.
5. Prefer the smallest valid patch.
6. Run the minimum necessary validation.
7. Produce final output in this format:
   - Summary
   - Files Changed
   - Key Logic Changes
   - Validation Performed
   - Compatibility Impact
   - Risks / Caveats
   - Recommended Next Step
8. Because this task is non-trivial, also produce a handoff aligned with HANDOFF_TEMPLATE.md.
9. If any critical input is missing, stop and state exactly what is missing instead of guessing.
```

---

## 15. Practical One-Sentence Summary

This task builds Warden's **distillation infrastructure skeleton now** without pretending that the project's **final distillation label space, threshold policy, or benchmark targets are already frozen**.
