# 2026-05-11 L0 / L1 Definition Realignment Report

## 中文摘要

本报告记录 `TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1` 的文档定义范围执行结果。

结论：

- 当前在线架构定义已收敛为 `L0 + L1`。
- `L0` 定义为最低成本规则热路径、低成本筛查与路由层。
- `L1` 定义为主判断层，包含 evidence pack builder、text branch、vision branch、structured / joint-signal branch、fusion、evidence ledger 与 deterministic explanation renderer。
- 当前任务不定义在线 `L2` 架构。未来更重复核或升级路径需要单独任务定义。
- `CLIP` / `MobileCLIP` 已从默认在线 L1 路径移出，仅保留为离线截图聚类、模板发现、ablation baseline、research-only visual-prior experiments，或未来另行批准的 optional feature flag。
- `SNet` / `SpecularNet`-like 路线已明确不属于 Warden V1 默认在线 L1 路径，仅保留为离线研究、ablation 或未来可选实验。
- OCR 与 YOLO / detector 保持 trigger-based、atomic evidence recovery / localization 职责。

## English Version

## 1. Scope

This report records the documentation-definition execution for `TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1`.
No code, schema, label, CLI, training, model, dataset, OCR, YOLO, CLIP, or SNet execution was performed.

## 2. Definition Outcome

The current online architecture definition now uses `L0 + L1` only:

- `L0`: cheapest rule hot path, cheap screening, and low-cost routing.
- `L1`: main judgment layer, including evidence pack builder, text branch, vision branch, structured / joint-signal branch, fusion, evidence ledger, and deterministic explanation renderer.
- Future heavier review or escalation may be defined later, but no current online L2 architecture is defined by this task.

## 3. CLIP / MobileCLIP Scope

`CLIP` / `MobileCLIP` are no longer described as default online Warden V1 L1 components.
They are allowed only for:

- offline screenshot clustering;
- template discovery;
- ablation baselines;
- research-only visual-prior experiments;
- a future optional feature flag separately approved by a later task.

## 4. SNet / SpecularNet-Like Scope

`SNet` / `SpecularNet`-like routes are not part of the Warden V1 default online L1 path.
They remain allowed only for offline research, ablation, or future optional experiments.

## 5. OCR / YOLO Scope

OCR and YOLO / detector responsibilities remain atomic:

- OCR recovers screenshot-visible text when triggered.
- YOLO / detector localizes atomic UI / form / element evidence when triggered.
- Neither path is a standalone final threat classifier.

## 6. Action Surface And Legitimacy

The text and L1 framework docs preserve the distinction between action surfaces and threat actions.
Action surfaces become threat-relevant only with deceptive identity, manipulative narrative, suspicious destination, abnormal submission, missing business legitimacy, missing context legitimacy, or another high-risk behavior context.

## 7. ADR And Future-L2 Residual Classification

Residual references were classified as follows:

- `docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md`: retained as historical research / ablation context, explicitly superseded and rejected for the default online Warden V1 path.
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`: retained only as a future heavier review / security reference; it does not define a current online L2 architecture, schema, routing contract, or implementation requirement.
- `docs/modules/L0_DESIGN_V1.md`: legacy `need_l2_candidate` / `need_l2` compatibility terms remain as field-name / routing-hint references and are documented as review / recrawl / future-escalation hints, not current L2 architecture.
- `docs/modules/Warden_FRONTIER_TECH_WATCHLIST_2026.md`: SpecularNet references are watchlist / future-candidate references and do not make it default online L1.
- Task and report files mention `L2`, `L1-fast`, `CLIP`, `MobileCLIP`, `SNet`, and `SpecularNet` as scope terms or rejected / restricted terms.

## 8. Validation Summary

Validation performed:

- Read the user task file and governing files.
- Ran focused `rg` search over `AGENTS.md`, `PROJECT.md`, `docs/modules`, `docs/frozen`, `docs/adr`, and the new task file for required terms.
- Ran `git diff --stat`.
- Ran focused diff-stat against the modified definition files.
- Ran `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md`.
- Ran `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`.

Residual search result:

- No active updated definition doc now presents `CLIP + SNet`, CLIP, MobileCLIP, SNet, or SpecularNet-like routes as the default online Warden V1 L1 path.
- No active updated definition doc now presents CLIP as a final classifier.
- Residual `L2` references are either explicit negative / future wording, superseded ADR content, future reference content, or legacy compatibility field-name mentions.
- Task checker initially failed on missing legacy metadata fields, then passed after adding those fields.
- Handoff checker passed.

Not run:

- No runtime tests.
- No model, OCR, YOLO, CLIP, SNet, or dataset execution.
- No schema validation beyond documentation checks.

## 9. Compatibility Impact

- Schema changed: no.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.
- Runtime behavior changed: no code was changed.
