# Module infer stage-flow update task

## 中文版

> 面向人类阅读的摘要版，英文版为权威执行版本。若精确字段、边界、兼容性结论有冲突，以英文版为准。

### 使用说明

- 本任务只允许做文档级修改，不写推理代码。
- 目标是把 `MODULE_INFER.md` 的阶段流表述补齐到当前口径，不改官方 `L0 / L1 / L2` 语义。
- 本任务工件名称已统一到仓库现有 `docs/tasks/` 命名风格。

## 任务元信息

- 任务 ID：`TASK-MODULE-INFER-2026-04-09-STAGE-FLOW-UPDATE`
- 任务标题：`更新 MODULE_INFER.md 以反映内嵌式 L0-fast 阶段流`
- 执行角色：`Codex 执行工程师`
- 优先级：`高`
- 状态：`DONE`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`PROJECT.md`、`MODULE_INFER.md`、`GPT_CODEX_WORKFLOW.md`、`TASK_TEMPLATE.md`、`HANDOFF_TEMPLATE.md`、`L0_DESIGN_V1.md`、`GATA_EVASION_AUXILIARY_SET_V1.md`
- 创建日期：`2026-04-09`
- 提出人：`用户`

## 背景

当前仓库里的 `MODULE_INFER.md` 已经定义了推理模块的职责、阶段路由、阈值治理、输出要求等高层约束，但项目目前对运行时主链的口径已经进一步收敛：

- 保留官方阶段命名 `L0 / L1 / L2`
- 允许 L0 以内嵌式 `L0-fast` 筛查/路由子路径的形式存在于总 runtime pipeline 中
- 不能把它语义上改叫 `L1-fast`
- `L1` 仍然是主判断层
- `L1` 可以包含 text-first 主路径和 conditional multimodal supplementation
- `L2` 仍然负责 gate / evasion / hard ambiguous / interaction-heavy 升级处理

本任务只改文档，不写代码。

## 目标

补充修改 `docs/modules/MODULE_INFER.md`，让它明确表达当前运行流设计：

- `L0` 仍然是官方 cheap screening stage
- `L0` 可以以内嵌方式存在于总 pipeline 中
- `L1` 是主判断层
- `L1-mm` 属于 `L1` 下的补证子路径，不是新 stage
- `L2` 是升级复核层
- early low-risk exit 只是路由语义，不是真实安全结论

## 允许修改范围

允许触碰：

- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-09_module_infer_stage_flow_update.md`
- `docs/handoff/2026-04-09_module_infer_stage_flow_update.md`

允许修改：

- `MODULE_INFER.md` 的措辞
- 分层责任说明
- runtime flow 说明
- early exit / routing 语义澄清
- 如有必要，在 `MODULE_INFER.md` 中增加一个紧凑的新小节说明当前建议运行流

## 禁止修改范围

不得：

- 写 L0 代码
- 改 inference 脚本
- 重写整个 staged architecture
- 改官方 stage 命名
- 把 `MODULE_INFER.md` 变成实现细则文档
- 塞入训练设计或模型设计细节
- 改数据 schema / label 语义 / TrainSet 规则
- 改 `GATA_EVASION_AUXILIARY_SET_V1.md`
- 顺手重构其他 module doc

## 输入

需要阅读：

- `AGENTS.md`
- `PROJECT.md`
- `MODULE_INFER.md`
- `L0_DESIGN_V1.md`
- `GATA_EVASION_AUXILIARY_SET_V1.md`
- workflow / template 文档

当前缺失项：

- `none`

## 输出

必须产出：

- 更新后的 `docs/modules/MODULE_INFER.md`
- 明确保留 `L0 / L1 / L2` 命名
- 明确 `L0` 可内嵌但不能语义改名
- 明确 `L1` 是主判断层
- 明确 `L1-mm` 属于 `L1` 的补证子路径
- 明确 `L2` 是 gate / evasion / hard ambiguous / interaction-heavy 的升级层
- 明确 early exit 只是路由语义
- handoff 文档

## 硬约束

- 只做文档修改
- 不改代码
- 不改 schema
- 不改官方 stage naming
- 文档仍必须保持模块级规范定位
- 新增 runtime-flow 内容必须兼容现有治理文档与 gate/evasion 协议

## 接口 / 兼容性约束

- `MODULE_INFER.md` 仍必须是模块契约文档
- 官方 stage 名必须保持 `L0 / L1 / L2`
- 不得通过文档措辞引入接口/语义漂移

## 建议执行顺序

1. 阅读治理文档和 `MODULE_INFER.md`
2. 找到现有文档中关于 stage responsibility / routing / output semantics 的位置
3. 做最小必要修改
4. 明确加入：
   - shared evidence preparation
   - embedded L0-fast router semantics
   - L1 text-first + conditional multimodal supplementation
   - L2 escalation semantics
5. 检查文档没有越界成实现说明
6. 输出 handoff

## 验收条件

必须满足：

- `MODULE_INFER.md` 明确保留 `L0 / L1 / L2`
- 明确允许内嵌式 `L0-fast` 运行流，但不改名
- 明确 `L1` 仍为主判断层
- 明确 `L1-mm` 归属 `L1`
- 明确 `L2` 的升级职责
- 明确 early low-risk exit 只是路由结果
- 文档与现有项目契约一致
- 有 handoff

## 最低验证要求

至少做：

- 文档一致性检查
- governing docs 对齐检查
- 中英双语格式检查
- diff 越界检查

## 交接要求

交付时必须补：

- `docs/handoff/2026-04-09_module_infer_stage_flow_update.md`

## 执行前开放问题

- `L0_DESIGN_V1.md` 已位于仓库根目录 `E:\Warden\L0_DESIGN_V1.md`
- runtime-flow 补充是作为 `MODULE_INFER.md` 新小节加入，还是并入现有 stage sections；若无额外要求，优先最小干净修改

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-MODULE-INFER-2026-04-09-STAGE-FLOW-UPDATE`
- Task Title: `Update MODULE_INFER.md to reflect the embedded L0-fast stage flow`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md; PROJECT.md; MODULE_INFER.md; GPT_CODEX_WORKFLOW.md; TASK_TEMPLATE.md; HANDOFF_TEMPLATE.md; L0_DESIGN_V1.md; GATA_EVASION_AUXILIARY_SET_V1.md`
- Created At: `2026-04-09`
- Requested By: `User`

Use this task for the non-trivial documentation update that aligns `MODULE_INFER.md` with the clarified embedded-L0-fast runtime flow while preserving official L0 / L1 / L2 semantics.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.
- If the task will produce Markdown deliverables, define them as bilingual by default: Chinese summary first, full English version second, with English authoritative for exact facts and contract wording.

---

## 1. Background

`docs/modules/MODULE_INFER.md` already defines the Inference module at the module-contract level, including staged judgment, routing discipline, threshold governance, output expectations, and compatibility rules. However, the current project discussion has further clarified the intended runtime flow: Warden should keep the official **L0 / L1 / L2** staged semantics while allowing an **embedded L0-fast screening/router path** inside the overall runtime pipeline rather than treating L0 as a separate heavyweight subsystem.

The current clarified direction is:

- shared evidence preparation happens first
- L0 remains the cheap, fast, high-recall screening/router stage
- L0 may be implemented as an embedded runtime sub-path, but it must not be renamed to L1 or semantically collapsed into L1
- L1 remains the current main judgment layer
- L1 may include a text-first default path and a multimodal supplementary path
- L2 remains reserved for escalated gate / evasion / hard ambiguous / interaction-heavy cases

This task is **documentation-only**. It updates `MODULE_INFER.md` so that the module contract explicitly reflects the clarified runtime stage flow and naming discipline, without implementing L0 itself and without redesigning the broader project architecture.

---

## 2. Goal

Revise `docs/modules/MODULE_INFER.md` so that it explicitly documents the current intended Warden runtime flow under the existing staged contract. The updated document must make clear that:

- Warden keeps the official stage naming of **L0 / L1 / L2**
- L0 may be embedded in the overall runtime pipeline as a fast screening/router sub-path
- L0 remains a routing-oriented cheap stage rather than the main semantic judgment stage
- L1 remains the main judgment stage and may use text-first judgment plus conditional multimodal supplementation
- L2 remains the escalation stage for gate / evasion / interaction-heavy / hard ambiguous cases
- early exit semantics remain routing semantics rather than ground-truth safety semantics

The revision must preserve the current module-level role of `MODULE_INFER.md` and must not turn it into an implementation spec or replace the separate L0 design document.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/MODULE_INFER.md`
- `docs/tasks/2026-04-09_module_infer_stage_flow_update.md`
- `docs/handoff/2026-04-09_module_infer_stage_flow_update.md`

This task is allowed to change:

- wording in `MODULE_INFER.md`
- stage-responsibility explanations in `MODULE_INFER.md`
- runtime-flow wording in `MODULE_INFER.md`
- clarifications around routing semantics, early exit semantics, and the relationship among embedded L0-fast, L1-text, L1-mm, and L2
- minimal document-structure reorganization inside `MODULE_INFER.md` if needed for clarity

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not implement L0 runtime code
- do not create or modify inference scripts
- do not redesign the whole staged architecture beyond documentation clarification
- do not rename official stages from L0 / L1 / L2 to other names
- do not rewrite `PROJECT.md`, `AGENTS.md`, or other governing docs unless a conflict must be reported
- do not convert `MODULE_INFER.md` into a low-level implementation spec
- do not define final L0 feature schemas or code interfaces here
- do not add machine-learning design content or training-method content into `MODULE_INFER.md`
- do not modify dataset schema, label semantics, or TrainSet rules
- do not change `GATA_EVASION_AUXILIARY_SET_V1.md`
- do not create opportunistic broad doc refactors in unrelated module docs

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_INFER.md`
- `L0_DESIGN_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`

### Code / Scripts

- `none`

### Data / Artifacts

- `none`

### Prior Handoff

- `none`

### Missing Inputs

- `none`

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- an updated `docs/modules/MODULE_INFER.md`
- explicit wording clarifying that L0 may be embedded in the runtime flow while preserving official L0 semantics
- explicit wording clarifying that L1 remains the main judgment stage
- explicit wording clarifying that conditional multimodal supplementation belongs under L1 rather than silently creating a new stage
- explicit wording clarifying that L2 is for escalated gate / evasion / hard ambiguous / interaction-heavy review
- explicit wording clarifying that early low-risk exit remains a routing outcome rather than a ground-truth safety claim
- a handoff aligned with `HANDOFF_TEMPLATE.md`

Optional but allowed if truly needed:

- a short added subsection illustrating the current recommended runtime flow in prose or compact bullet form inside `MODULE_INFER.md`

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- Preserve `MODULE_INFER.md` as a module-level specification, not an implementation playbook.
- Keep official stage naming as `L0`, `L1`, and `L2`.
- Explicitly forbid reinterpreting embedded L0-fast as `L1-fast` in module semantics.
- Do not silently redefine L1 or L2 responsibilities.
- Do not over-specify exact model backbones in `MODULE_INFER.md`.
- Any added runtime-flow wording must remain compatible with `PROJECT.md`, `AGENTS.md`, and the gate/evasion auxiliary protocol.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `MODULE_INFER.md` must remain a module-contract document for the Inference module
- official stage naming must remain `L0 / L1 / L2`
- documented staged-routing semantics must remain compatible with existing project contracts

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `none at dataset-schema level; do not introduce schema renaming through module-doc wording`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `none; this is a documentation-only task`

Downstream consumers to watch:

- future L0 implementation tasks
- future L1/L2 design tasks
- future inference runtime output-contract tasks
- future benchmark/reporting tasks that rely on stage naming discipline

---

## 9. Suggested Execution Plan

Recommended order:

1. Read `AGENTS.md`, `PROJECT.md`, `MODULE_INFER.md`, `L0_DESIGN_V1.md`, and `GATA_EVASION_AUXILIARY_SET_V1.md`.
2. Identify where `MODULE_INFER.md` currently defines stage purposes, routing, and output semantics.
3. Make the smallest wording changes needed to reflect the clarified runtime structure.
4. Add or revise wording to distinguish:
   - shared evidence preparation
   - embedded L0-fast screening/router behavior
   - L1 as the main judgment stage
   - L1 text-first and conditional multimodal supplementation
   - L2 escalation role
5. Explicitly preserve early-exit semantics as routing semantics.
6. Verify the final document still reads as a module-contract doc rather than an implementation spec.
7. Produce the handoff.

Task-specific execution notes:

- Prefer localized edits over full-document rewrites.
- Keep the document general enough to remain stable across near-term implementation changes.
- If adding a runtime-flow subsection, keep it compact and contract-level rather than code-level.

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [ ] `MODULE_INFER.md` explicitly preserves official `L0 / L1 / L2` naming
- [ ] `MODULE_INFER.md` explicitly allows embedded L0-fast runtime flow without semantically renaming L0
- [ ] `MODULE_INFER.md` clearly preserves L1 as the main judgment stage
- [ ] `MODULE_INFER.md` clearly positions conditional multimodal supplementation under L1
- [ ] `MODULE_INFER.md` clearly preserves L2 as escalation for gate / evasion / hard ambiguous / interaction-heavy cases
- [ ] `MODULE_INFER.md` clearly states that early low-risk exit is a routing outcome, not a ground-truth safety claim
- [ ] the revised wording remains compatible with project-level staged semantics

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] document sanity review
- [ ] consistency check against governing docs
- [ ] bilingual-format sanity check
- [ ] diff review for scope control

Commands to run if applicable:

```bash
none required for code execution
```

Expected evidence to capture:

- updated `MODULE_INFER.md` excerpt or summary showing the revised stage-flow wording
- explicit note in the handoff confirming no code, schema, or CLI change occurred

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-09_module_infer_stage_flow_update.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- `L0_DESIGN_V1.md` is available at `E:\Warden\L0_DESIGN_V1.md`
- whether the runtime-flow clarification should be inserted as a dedicated subsection or integrated into existing stage-responsibility sections; choose the smallest clean edit if not otherwise specified

If none, write `none`.
