# Task Metadata

- Task ID: TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1
- Task Title: Warden L0 / L1 Definition Realignment V1
- Owner Role: Codex
- Priority: High
- Related Module: docs / architecture definition
- Related Issue / ADR / Doc: C:\Users\20516\Downloads\TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1.md; docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md
- Created At: 2026-05-11
- Requester: User
- Requested By: User
- Date: 2026-05-11
- Status: In Progress

## 中文版

### 1. 背景

本任务采用用户提供的 `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1.md` 作为执行边界。此前部分文档仍把 Warden 当前在线架构描述为 `L0 / L1 / L2`，并把 `CLIP` / `MobileCLIP`、`SNet` / `SpecularNet`-like 路线表述为可进入默认在线 L1 或 L1-fast 路径。本任务要求将当前定义严格收敛为 `L0 + L1`。

### 2. 目标

将 Warden 当前在线架构定义调整为：

- `L0`：最低成本规则热路径、低成本筛查与路由层。
- `L1`：主判断层，包含 evidence pack builder、text branch、vision branch、structured / joint-signal branch、fusion、evidence ledger 与 deterministic explanation renderer。
- 当前任务不定义在线 `L2` 架构。未来更重复核或升级路径必须另行定义。

### 3. 范围内

- 更新当前 active docs 中的 L0 / L1 / L2、L1-fast、CLIP、MobileCLIP、SNet、SpecularNet-like 相关定义。
- 将 `CLIP` / `MobileCLIP` 限定为离线截图聚类、模板发现、ablation baseline、research-only visual-prior experiments，或未来另行批准的 optional feature flag。
- 将 `SNet` / `SpecularNet`-like 路线限定为离线研究、ablation 或未来可选实验。
- 更新 2026-05-08 ADR，使其明确为 rejected / deferred / research-only，不作为默认在线路径。
- 新增 alignment report 与 handoff。

### 4. 范围外

- 不改代码。
- 不改 schema、labels、CLI 或公共输出格式。
- 不运行训练、模型推理、OCR、YOLO、CLIP、SNet 或数据集任务。
- 不新增依赖。
- 不创建当前 `L2` 架构定义。

### 5. 输入

- User task file: `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1.md`
- Repository governing files: `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, `docs/templates/HANDOFF_TEMPLATE.md`
- Current active architecture/module/frozen docs.

### 6. 需要输出

- Updated active docs.
- Updated or superseded ADR for the 2026-05-08 L1-fast / L2-semantic proposal.
- `docs/reports/20260511_l0_l1_definition_realign_report.md`
- `docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`

### 7. 硬约束

- 文档定义任务，不代表架构或实现验收。
- 只做文档范围内的定义重排。
- 不把 action surface 自动等同于 malicious；必须保留 business legitimacy 与 context legitimacy 判断。
- 不把 CLIP、MobileCLIP、SNet 或 SpecularNet-like 路线写成默认在线 L1 路径。

### 8. 接口 / Schema 约束

- Schema changed: no.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.

### 9. 执行计划

- Read task and governing files.
- Patch active docs to define current architecture as L0 + L1.
- Mark the 2026-05-08 ADR as superseded / rejected for default online Warden V1 path.
- Run focused residual searches and checker scripts where available.
- Summarize results in report and handoff.

### 10. 验收标准

- Active docs no longer imply current L2 is required or defined.
- Active docs no longer imply `CLIP + SNet` is accepted as Warden V1 default online L1 path.
- Active docs no longer imply CLIP is a final classifier.
- Active docs no longer imply SNet is the default L1 decision layer.
- Active docs preserve OCR / YOLO as trigger-based atomic evidence recovery paths.
- Active docs preserve action-surface context and business-legitimacy distinction.

### 11. 验证清单

- Search for `L2`, `L1-fast`, `CLIP`, `MobileCLIP`, `SNet`, `SpecularNet`, `OCR`, `YOLO`, `vision path`, `visual prior`, `action surface`, `threat action`, `business legitimacy`, `context legitimacy`.
- Run `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md` if available.
- Run `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md` if available.
- Provide `git diff --stat` and focused diff summary.

## English Version

## 1. Background

This task adopts the user-provided file `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1.md` as the execution boundary. Some active Warden documents still describe the current online architecture as `L0 / L1 / L2` and describe `CLIP` / `MobileCLIP` or `SNet` / `SpecularNet`-like routes as potentially entering the default online L1 or L1-fast path. This task realigns the current definition to `L0 + L1` only.

## 2. Goal

Realign Warden's current online architecture definition to:

- `L0`: cheapest rule hot path, cheap screening, and low-cost routing.
- `L1`: main judgment layer, including evidence pack builder, text branch, vision branch, structured / joint-signal branch, fusion, evidence ledger, and deterministic explanation renderer.
- No current online `L2` architecture is defined by this task. Future heavier review or escalation must be defined separately.

## 3. Scope In

- Update current active docs that define or imply L0 / L1 / L2, L1-fast, CLIP, MobileCLIP, SNet, or SpecularNet-like default behavior.
- Restrict `CLIP` / `MobileCLIP` to offline screenshot clustering, template discovery, ablation baselines, research-only visual-prior experiments, or a separately approved future optional feature flag.
- Restrict `SNet` / `SpecularNet`-like routes to offline research, ablation, or future optional experiments.
- Update the 2026-05-08 ADR so it is clearly rejected / deferred / research-only for the default online path.
- Add an alignment report and handoff.

## 4. Scope Out

- No code changes.
- No schema, label, CLI, or public output-format changes.
- No training, model inference, OCR, YOLO, CLIP, SNet, or dataset execution.
- No new dependencies.
- No current `L2` architecture definition.

## 5. Inputs

- User task file: `C:\Users\20516\Downloads\TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1.md`
- Repository governing files: `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, `docs/templates/HANDOFF_TEMPLATE.md`
- Current active architecture/module/frozen docs.

## 6. Required Outputs

- Updated active docs.
- Updated or superseded ADR for the 2026-05-08 L1-fast / L2-semantic proposal.
- `docs/reports/20260511_l0_l1_definition_realign_report.md`
- `docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`

## 7. Hard Constraints

- This is documentation-definition work only and is not architecture or implementation acceptance.
- Keep the change inside documentation definition scope.
- Do not make action surfaces automatically malicious; preserve business-legitimacy and context-legitimacy judgment.
- Do not write CLIP, MobileCLIP, SNet, or SpecularNet-like routes as the default online L1 path.

## 8. Interface / Schema Constraints

- Schema changed: no.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.

## 9. Execution Plan

- Read the task and governing files.
- Patch active docs to define the current architecture as L0 + L1.
- Mark the 2026-05-08 ADR as superseded / rejected for the default online Warden V1 path.
- Run focused residual searches and checker scripts where available.
- Summarize results in the report and handoff.

## 10. Acceptance Criteria

- Active docs no longer imply current L2 is required or defined.
- Active docs no longer imply `CLIP + SNet` is accepted as Warden V1 default online L1 path.
- Active docs no longer imply CLIP is a final classifier.
- Active docs no longer imply SNet is the default L1 decision layer.
- Active docs preserve OCR / YOLO as trigger-based atomic evidence recovery paths.
- Active docs preserve action-surface context and business-legitimacy distinction.

## 11. Validation Checklist

- Search for `L2`, `L1-fast`, `CLIP`, `MobileCLIP`, `SNet`, `SpecularNet`, `OCR`, `YOLO`, `vision path`, `visual prior`, `action surface`, `threat action`, `business legitimacy`, `context legitimacy`.
- Run `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md` if available.
- Run `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md` if available.
- Provide `git diff --stat` and focused diff summary.
