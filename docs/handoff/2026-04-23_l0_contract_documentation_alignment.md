# L0 Contract Documentation Alignment Handoff

## 中文摘要

### 元数据

- Task ID: `TASK-L0-2026-04-23-CONTRACT-DOCUMENTATION-ALIGNMENT`
- Task doc: `docs/tasks/2026-04-23_l0_contract_documentation_alignment.md`
- Date: `2026-04-23`
- Scope type: documentation-only
- Status: completed pending user acceptance

### 执行摘要

本次交付把 active 文档中的 L0 口径统一到当前基本定型的合同：L0 是低成本、快速、可解释的 screening / routing 层，默认热路径只围绕 URL、可见文本/标题、表单摘要、网络摘要、raw visible-text 可观测性、已有低成本 diff/evasion 摘要，以及 `gambling / adult / gate` 三类专项表面信号工作。

本次未修改代码、schema、字段名、CLI、历史 task 或历史 handoff。

### 主要变化

- README 只做短说明，按用户要求不展开成完整 L0 模块规格。
- `PROJECT.md` 新增当前 L0 合同摘要。
- `MODULE_INFER.md` 收紧 L0 responsibilities / strict rules。
- `L0_DESIGN_V1.md` 同步 L0 职责、输入、禁止项、`html_features` / `brand_signals` 兼容说明、`diff_summary` 读取边界。
- runtime/dataflow、vision、edge、gate/evasion、auto-label、train-label derivation 相关文档同步了 L0 与 L1/L2 的边界。

### 兼容性影响

- Schema changed: no
- Backward compatible: yes
- Docs updated: yes
- Code changed: no
- Python files changed: no
- Historical task/handoff changed: no

`html_features` 和 `brand_signals` 仍作为兼容字段保留；文档明确它们不属于当前 L0 默认热路径的主动计算结果。

### 验证

已执行：

- `git diff --name-only`
- `git diff --check`
- `git diff --name-only | Select-String -Pattern '\.py$'`
- `rg` 检查旧式 L0 默认输入表述残留
- `rg` 检查 HTML / brand / screenshot / OCR / L0 hot path 相关表述
- 只读 subagent post-edit review

验证结论：

- 未发现 Python 文件变更。
- 未发现旧式 `basic visual signals`、`URL / DOM`、`URL、文本、表单、HTML`、`品牌 token 不一致` 等 active 表述残留。
- 剩余 HTML / brand / screenshot / OCR 命中均为负向边界、兼容字段、或历史 task/handoff 证据。
- 只读 reviewer 未发现阻塞问题；其指出的 `brand` no-early-stop wording 歧义已收紧为“显式预计算或兼容输入提供的 brand signals”。

### 风险 / caveats

- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md` 和 `docs/frozen/SCHEMA_REGISTRY.md` 保持未改，因为本次没有 schema 或 artifact contract 变更。
- 一些历史 task/handoff 仍包含旧阶段过程描述，按用户要求未修改。
- 后续如果 L0 因新增样本继续调参，应只更新 L0 策略/阈值相关段落，不应重新打开 HTML / brand / screenshot/OCR 默认热路径。

### 推荐下一步

后续 L0 若只做样本驱动微调，建议单开小任务处理阈值、词表或 score policy，并继续保持 no schema change / no heavy evidence in L0 的边界。

## English Version

> AI note: The English section is authoritative for exact scope, compatibility, validation, and follow-up boundaries.

# L0 Contract Documentation Alignment Handoff

## 1. Metadata

- Task ID: `TASK-L0-2026-04-23-CONTRACT-DOCUMENTATION-ALIGNMENT`
- Task doc: `docs/tasks/2026-04-23_l0_contract_documentation_alignment.md`
- Date: `2026-04-23`
- Scope type: documentation-only
- Status: completed pending user acceptance

## 2. Executive Summary

This delivery aligns active L0-related documentation with the current near-final L0 contract.

The current contract is:

- L0 is a fast, low-cost, auditable screening and routing layer.
- The default L0 hot path consumes cheap URL evidence, visible text/title, form summaries, network summaries, raw visible-text observability, and already available compact diff/evasion hints.
- L0 currently specializes in `gambling / adult / gate` surface signals.
- L0 does not default to full HTML scanning, default brand extraction, screenshot/OCR, image-lite evidence, heavy model inference, gate solving, click-through recovery, or interaction recovery.
- `html_features` and `brand_signals` remain compatibility fields.

No code, schema, field names, CLI flags, historical task documents, or historical handoffs were changed.

## 3. Files Changed

- `README.md`
- `PROJECT.md`
- `docs/tasks/2026-04-23_l0_contract_documentation_alignment.md`
- `docs/modules/MODULE_INFER.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/modules/Warden_EDGE_DEPLOYMENT_PROFILE_V1.md`
- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/handoff/2026-04-23_l0_contract_documentation_alignment.md`

## 4. Key Logic Changes

- `README.md` now contains only a short high-level L0 correction, as requested.
- `PROJECT.md` now records the current project-level L0 contract.
- `MODULE_INFER.md` now states L0 responsibilities and strict prohibitions in the narrowed hot-path form.
- `L0_DESIGN_V1.md` now defines the active L0 role, default inputs, prohibited default inputs, compatibility fields, `diff_summary` consumption boundary, and specialized detector role.
- Runtime/dataflow documentation now states that L0 must not eagerly request heavy HTML, screenshot/OCR, default brand extraction, heavy models, or interaction recovery.
- Vision and edge deployment docs now place screenshot/OCR/model-heavy work after L0 rather than in the default L0 hot path.
- Gate/evasion and train-label docs now treat L0 as detect-and-route, not gate solving, final labeling, or heavy evidence recovery.
- Auto-label policy now distinguishes the broader `auto_labels.json` compatibility contract from the narrowed standalone L0 hot path.

## 5. Validation Performed

Commands run:

```bash
git diff --name-only
git diff --check
git diff --name-only | Select-String -Pattern '\.py$'
rg -n --glob "*.md" "basic visual signals|URL / DOM|DOM / text|URL、文本、表单、HTML|品牌 token 不一致|品牌仿冒、紧迫性用语、二维码|quickly extract URL, DOM" README.md PROJECT.md docs/modules docs/data docs/frozen
rg -n --glob "*.md" "full HTML|default brand extraction|screenshots/OCR|screenshot/OCR|image-lite evidence|L0 hot path|gambling / adult / gate" README.md PROJECT.md docs/modules docs/data docs/frozen
```

Result:

- No Python files were changed.
- `git diff --check` reported no whitespace errors; PowerShell/Git emitted normal CRLF warnings only.
- No active old wording remained for `basic visual signals`, `URL / DOM`, `URL、文本、表单、HTML`, or brand-token mismatch as an L0 default input.
- Remaining HTML / brand / screenshot / OCR matches are boundary statements, compatibility-field statements, or historical task/handoff evidence.
- A read-only post-edit subagent review completed with no blocking findings.
- The reviewer's non-blocking brand no-early-stop wording caveat was addressed by scoping those lines to explicitly precomputed or compatibility-provided brand inputs.

## 6. Compatibility Impact

- Schema changed: no
- Backward compatible: yes
- Docs updated: yes
- Code changed: no
- CLI changed: no
- Output format changed: no
- Labels changed: no

Compatibility fields:

- `html_features` remains documented.
- `brand_signals` remains documented.
- The current default L0 path is documented as not actively computing full HTML features or default brand extraction.
- Existing compact `diff_summary.json` may be consumed when already present, but generating variants or producing `diff_summary.json` is not an L0 responsibility.

## 7. Risks / Caveats

- Frozen schema documents were reviewed but not edited, because this delivery did not change schema or artifact contracts.
- Historical task and handoff documents still contain process history and older boundary statements; they were intentionally left unchanged per user instruction.
- Future sample-driven L0 tuning should update only the affected strategy, threshold, or lexicon sections and should not reintroduce heavy evidence into L0 by default.

## 8. Recommended Next Step

For future L0 work, open narrow tuning tasks for sample-driven threshold, score-policy, or lexicon changes. Keep the same hard boundary: no default full HTML, no default brand extraction, no screenshot/OCR, no heavy model path, and no interaction recovery in L0.
