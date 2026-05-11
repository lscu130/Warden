# Handoff Metadata

- Handoff ID: HANDOFF_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1
- Related Task ID: TASK_20260511_WARDEN_L0_L1_DEFINITION_REALIGN_V1
- Task Title: Warden L0 / L1 Definition Realignment V1
- Module: docs / architecture definition
- Author: Codex
- Date: 2026-05-11
- Status: Complete

## 中文版

### 1. 执行摘要

本次按用户任务把 Warden 当前在线定义收敛为 `L0 + L1`。`L0` 是最低成本筛查与路由层；`L1` 是主判断层，包含 evidence pack、text、vision evidence recovery、structured / joint signals、fusion、evidence ledger 和 deterministic explanation renderer。当前任务不定义在线 `L2`。

### 2. 变更内容

- 更新顶层和模块文档中的当前阶段定义。
- 将 `CLIP` / `MobileCLIP` 从默认在线 L1 路径移出，限制为离线 / research / ablation / 未来单独批准 optional feature flag。
- 将 `SNet` / `SpecularNet`-like 路线限制为离线研究、ablation 或未来可选实验。
- 保持 OCR 和 YOLO / detector 的 trigger-based 原子证据职责。
- 将 2026-05-08 L1-fast / L2-semantic ADR 标记为已废止且不适用于默认在线路径。
- 将现有 L2 安全参考文档标记为未来更重复核参考，不定义当前在线 L2。

### 3. 触及文件

- `AGENTS.md`
- `PROJECT.md`
- `docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `docs/modules/Warden_MINICONDA_ENV_SETUP_V1.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_PAPER.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md`
- `docs/reports/20260511_l0_l1_definition_realign_report.md`
- `docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`

### 4. 行为影响

无代码行为变化。本文档批次只修改定义与任务/报告/交接文档。

### 5. Schema / 接口影响

- Schema changed: no.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.
- Backward compatible: yes for runtime/code behavior, because no code path was changed.

### 6. 验证

已执行：

- 读取用户任务和治理文件。
- 对任务要求关键词执行 focused search。
- 执行 `git diff --stat`。
- 执行 focused diff-stat。

未执行：

- 未运行 runtime tests。
- 未运行模型、OCR、YOLO、CLIP、SNet 或数据集任务。

### 7. 风险 / 注意事项

- 仓库存在与本任务无关的既有 dirty / staged changes；本次未回退。
- 2026-05-08 ADR 内容保留为历史文本，因此搜索仍会命中 L1-fast / L2-semantic / SpecularNet / CLIP；顶部 supersession note 明确其不再适用于默认在线路径。
- `L0_DESIGN_V1.md` 中 legacy `need_l2_candidate` / `need_l2` 作为兼容字段名保留，并已说明只表示 review / recrawl / future-escalation hint。

### 8. 推荐下一步

如要继续推进，应拆成单独任务定义最终 L1 输出模式、精确文本多任务训练目标、OCR / YOLO / CLIP 触发阈值、教师蒸馏模式、评估桶和基准验证。

## English Version

## 1. Executive Summary

This task realigned the current online Warden architecture definition to `L0 + L1`.
`L0` is the cheapest screening and routing layer.
`L1` is the main judgment layer, including evidence-pack construction, text judgment, trigger-based vision evidence recovery, structured / joint signals, fusion, evidence ledger, and deterministic explanation rendering.
This task does not define a current online `L2` architecture.

## 2. What Changed

- Updated top-level and module docs to use the current `L0 + L1` stage definition.
- Removed `CLIP` / `MobileCLIP` from the default online L1 path and limited them to offline / research / ablation / separately approved optional feature-flag uses.
- Limited `SNet` / `SpecularNet`-like routes to offline research, ablation, or future optional experiments.
- Preserved trigger-based OCR and YOLO / detector atomic evidence responsibilities.
- Marked the 2026-05-08 L1-fast / L2-semantic ADR as superseded and rejected for the default online path.
- Marked the L2 security reference as a future heavier review reference that does not define current online L2.

## 3. Files Touched

- `AGENTS.md`
- `PROJECT.md`
- `docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md`
- `docs/modules/Warden_MINICONDA_ENV_SETUP_V1.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/MODULE_PAPER.md`
- `docs/modules/Warden_L2_API_REVIEW_SECURITY_REFERENCE_V1.md`
- `docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md`
- `docs/reports/20260511_l0_l1_definition_realign_report.md`
- `docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md`

## 4. Behavior Impact

### Expected New Behavior

No runtime behavior changes. The expected new behavior is documentation interpretation: current online Warden V1 is `L0 + L1` only.

### Preserved Behavior

Existing code, runtime paths, schema fields, labels, CLI flags, and public output formats are unchanged.

### User-facing / CLI Impact

None.

### Output Format Impact

None.

## 5. Schema / Interface Impact

- Schema changed: no.
- Labels changed: no.
- CLI changed: no.
- Public output format changed: no.
- Backward compatible: yes for runtime/code behavior, because no code path was changed.

## 6. Validation Performed

### Commands Run

- `rg "L2|L1-fast|CLIP|MobileCLIP|SNet|SpecularNet|OCR|YOLO|vision path|visual prior|action surface|threat action|business legitimacy|context legitimacy" AGENTS.md PROJECT.md docs/modules docs/frozen docs/adr docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md`
- `git diff --stat`
- `git diff -- AGENTS.md PROJECT.md docs/modules/MODULE_INFER.md docs/modules/Warden_TEXT_PIPELINE_V1.md docs/modules/Warden_VISION_PIPELINE_V1.md docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md docs/frozen/Warden_L1_FRAMEWORK_V0.1.md docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md docs/modules/Warden_RUNTIME_DEPLOYMENT_TASK_V1.md docs/modules/Warden_MINICONDA_ENV_SETUP_V1.md docs/modules/L0_DESIGN_V1.md docs/modules/MODULE_PAPER.md --stat`

### Result

- Search residuals are classified in `docs/reports/20260511_l0_l1_definition_realign_report.md`.
- No updated active definition doc presents `CLIP + SNet`, CLIP, MobileCLIP, SNet, or SpecularNet-like routes as the default online Warden V1 L1 path.
- No updated active definition doc presents CLIP as a final classifier.
- Residual `L2` references are explicit negative / future wording, superseded ADR text, future reference text, or legacy compatibility field-name mentions.

### Not Run

- Runtime tests were not run because this was a documentation-definition task.
- Model, OCR, YOLO, CLIP, SNet, and dataset executions were not run by scope.
- `python scripts/ci/check_task_doc.py docs/tasks/2026-05-11_warden_l0_l1_definition_realign_v1.md` initially failed because the repo-native task wrapper was missing legacy checker metadata fields. Those fields were added and the checker was rerun.
- `python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-11_warden_l0_l1_definition_realign_v1.md` passed.

## 7. Risks / Caveats

- The workspace already had unrelated dirty and staged changes. They were not reverted.
- The 2026-05-08 ADR keeps historical proposal text, so keyword search still finds `L1-fast`, `L2-semantic`, `SpecularNet`, and `CLIP`; the supersession note at the top is the active status.
- `L0_DESIGN_V1.md` still contains legacy `need_l2_candidate` / `need_l2` compatibility names. The new note classifies them as review / recrawl / future-escalation hints, not current L2 architecture.

## 8. Docs Impact

Docs updated: yes.
Code updated: no.

## 9. Recommended Next Step

Open separate tasks for final L1 output schema, exact text multi-task training targets, OCR / YOLO / CLIP trigger thresholds, teacher distillation mode, and evaluation buckets / benchmark validation.
