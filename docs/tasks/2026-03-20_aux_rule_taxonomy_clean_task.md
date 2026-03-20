# TASK_TEMPLATE.md

# Task Metadata

- Task ID: TASK-2026-03-18-RULE-TAXONOMY-V1
- Task Title: Extend rule_labels.json to emit threat_taxonomy_v1 candidate fields without changing TrainSet V1 primary
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: labeling / weak-labeling
- Related Issue / ADR / Doc: AGENTS.md; GPT_CODEX_WORKFLOW.md; TRAIN_LABEL_DERIVATION_V1.md; TRAINSET_V1.md; MODULE_DATA.md
- Created At: 2026-03-18
- Requested By: User

---

## 1. Background

Warden 当前已冻结新的多威胁标签结构：
- 一级主标签按最终高风险动作
- 二级标签按行业/场景
- 辅助标签按叙事、证据、规避特征

当前已决定：
- 这套新结构先不进入 TrainSet V1 primary 主定义
- 这套新结构先不改主 manifest 默认核心字段
- 这套新结构作为 `rule_labels.json` 中长期保留的活跃弱标签输出落地
- 命名空间固定为 `threat_taxonomy_v1`
- 所有新增字段必须使用候选标签语义，不得冒充人工金标

当前抓取脚本已具备：
- 生成 `auto_labels.json`
- 可选通过 `derive_rule_labels(auto_labels)` 生成 `rule_labels.json`

当前 backfill 脚本已具备：
- 批量生成 `auto_labels.json`
- 通过 `--emit-rule-labels` 批量生成 `rule_labels.json`

因此，本任务的核心不是重写抓取链路，也不是重写 backfill 流程，而是扩展 `derive_rule_labels()` 的输出结构，使其能产出冻结后的 `threat_taxonomy_v1` 字段。

---

## 2. Goal

在不改变 TrainSet V1 primary、不改变当前主 manifest 默认核心字段、不把弱标签提升为人工金标的前提下，
扩展 `derive_rule_labels()`，使 `rule_labels.json` 能稳定输出 `threat_taxonomy_v1` 命名空间下的候选标签字段，并通过现有 backfill 流程可批量落盘。

完成后应满足：

- `rule_labels.json` 可新增 `threat_taxonomy_v1`
- 新字段仅表示规则派生候选标签
- 现有 backfill 路径无需重构即可输出新增字段
- 现有抓取脚本默认行为不变

---

## 3. Scope In

This task is allowed to touch:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`（仅在必要时补帮助说明或最小兼容性注释）

This task is allowed to change:

- `derive_rule_labels()` 及其必要的内部辅助函数
- `rule_labels.json` 的新增字段输出
- backfill 脚本的帮助文本、注释、最小说明（如确有必要）

---

## 4. Scope Out

This task must NOT do the following:

- 不修改 `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` 主流程
- 不修改抓取脚本默认开关
- 不修改 `auto_labels.json` 顶层结构
- 不修改 `TRAINSET_V1.md` 主定义
- 不修改 `build_manifest.py` 默认输出
- 不修改 `check_dataset_consistency.py` 默认行为
- 不把新分类字段写入 `meta.json`、`url.json`、`env.json`
- 不新增第三方依赖
- 不把 `*_candidate` 字段写成最终标签语义
- 不新增训练逻辑
- 不新增推理逻辑

---

## 5. Inputs

Relevant inputs for this task:

- Docs:
  - `AGENTS.md`
  - `GPT_CODEX_WORKFLOW.md`
  - `TRAIN_LABEL_DERIVATION_V1.md`
  - `TRAINSET_V1.md`
  - `MODULE_DATA.md`

- Code / scripts:
  - `scripts/labeling/Warden_auto_label_utils_brandlex.py`
  - `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`

- Reference scripts:
  - current capture script structure
  - current backfill script structure

- Existing behavior:
  - `derive_auto_labels(...)`
  - `derive_rule_labels(auto_labels)`
  - `--emit-rule-labels`

If any input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- updated `derive_rule_labels()` implementation
- stable `rule_labels.json` output containing `threat_taxonomy_v1`
- if needed, minimal helper functions for rule aggregation / confidence / rule-source collection
- optional help-text update in backfill script only if needed
- doc updates that freeze `threat_taxonomy_v1` as an active weak-label namespace without promoting it into TrainSet V1 primary or primary manifest core fields
- clear handoff describing:
  - which files changed
  - whether capture script was intentionally left untouched
  - whether schema changed
  - whether backward compatibility was preserved

The task does NOT require:
- manifest integration
- consistency-check integration
- capture-script online generation changes

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format outside `rule_labels.json`.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant comments/help text if behavior changes.

Task-specific constraints:

- New fields must be nested under `threat_taxonomy_v1`
- All new label fields must use candidate semantics
- `threat_taxonomy_v1.taxonomy_source` must clearly indicate rule-derived output
- `threat_taxonomy_v1.taxonomy_review_status` default must remain weak-label-safe
- No field may imply gold-label authority
- Backfill flow should continue to work through existing `--emit-rule-labels`
- Capture script should remain untouched unless a hard blocker is found

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `Warden_dataset_backfill_labels_brandlex.py --emit-rule-labels`
- current capture script default behavior
- current `auto_labels.json` structure

Schema / field constraints:

New fields are allowed only inside:

- `rule_labels.json -> threat_taxonomy_v1`

Frozen new field set:

- `threat_taxonomy_v1.primary_threat_label_candidate`
- `threat_taxonomy_v1.primary_threat_label_confidence`
- `threat_taxonomy_v1.primary_threat_label_rules`
- `threat_taxonomy_v1.scenario_label_candidate`
- `threat_taxonomy_v1.scenario_label_confidence`
- `threat_taxonomy_v1.scenario_label_rules`
- `threat_taxonomy_v1.narrative_tags_candidate`
- `threat_taxonomy_v1.evidence_tags_candidate`
- `threat_taxonomy_v1.evasion_tags_candidate`
- `threat_taxonomy_v1.ecosystem_tags_candidate`
- `threat_taxonomy_v1.taxonomy_source`
- `threat_taxonomy_v1.taxonomy_review_status`

Allowed values must follow the already frozen label draft.
No renaming.
No collapsing candidate fields into final labels.

---

## 9. Suggested Execution Plan

Recommended order:

1. Read current `derive_rule_labels()` implementation.
2. Read frozen taxonomy definitions from project docs.
3. Map current `auto_labels` signals to:
   - primary threat label candidate
   - scenario label candidate
   - narrative / evidence / evasion / ecosystem tags
4. Add the smallest necessary helper functions inside `Warden_auto_label_utils_brandlex.py`.
5. Extend `derive_rule_labels()` to emit `threat_taxonomy_v1`.
6. Keep existing rule-label output intact unless removal is explicitly justified.
7. Verify that `Warden_dataset_backfill_labels_brandlex.py --emit-rule-labels` still works without workflow change.
8. Only if necessary, update backfill help text/comments.
9. Do not modify capture script unless a blocker is proven.

Task-specific execution notes:

- Prefer additive logic
- Prefer deterministic rule mapping
- Confidence can be heuristic but must be bounded and documented
- Rules list should record why a candidate label was emitted
- If a sample is ambiguous, use `uncertain` rather than forcing a strong class

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema/interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs/comments were updated if needed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] `derive_rule_labels()` emits `threat_taxonomy_v1`
- [x] all new fields use candidate semantics
- [x] `Warden_dataset_backfill_labels_brandlex.py --emit-rule-labels` can produce the new structure without workflow rewrite
- [x] capture script default behavior remains unchanged
- [x] no new dependency was introduced
- [x] no TrainSet V1 primary definition was changed
- [x] no manifest default field set was changed

---

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted smoke test
- [x] backward compatibility spot-check
- [x] output artifact spot-check

Commands to run if applicable:

    python -m py_compile scripts/labeling/Warden_auto_label_utils_brandlex.py scripts/labeling/Warden_dataset_backfill_labels_brandlex.py

    python scripts/labeling/Warden_dataset_backfill_labels_brandlex.py \
      --roots ./data/raw/phish ./data/raw/benign \
      --only-missing \
      --workers 2 \
      --emit-rule-labels \
      --limit 5

Additional validation for this task:

- inspect at least 2 generated `rule_labels.json` files
- confirm `threat_taxonomy_v1` exists
- confirm no gold-label wording leaked into candidate fields
- confirm old output path and CLI behavior still work
- confirm behavior on two different real source samples when available
