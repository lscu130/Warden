# Warden 标签策略套件对齐交接单

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 交付摘要

- 状态：DONE
- 相关任务：`TASK-2026-04-07-LABEL-POLICY-SUITE-REPO-ALIGNMENT`
- 本次交付把 repo 内活跃 label-policy suite 收敛到稳定文件名：
  - 最小合并：
    - `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
    - `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
    - `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
    - `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
  - 替换/收敛移除：
    - `docs/data/Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md`
    - `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md`
    - `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md`
- suite alignment note：保留，且已改为指向稳定活跃文件名
- Schema changed：no
- Backward compatible：yes
- Docs updated：yes

### 关键变化

- `auto` 活跃文档增加了显式对齐锚点，明确当前 repo 使用稳定文件名而非独立 `_ALIGNED` 活跃副本。
- `rule` 活跃文档补齐了与 `manual` 对齐的 primary threat candidate family、scenario candidate family，并把 `page_role_hint` 的活跃枚举补到包含 `uncertain`。
- `manual` 活跃文档补了与 `rule` 的 primary/scenario family 对齐锚点，继续保留“final adjudication + selective coverage”口径。
- suite alignment note 保留，并改为说明当前活跃套件就是稳定文件名版本。

### 验证摘要

- 已检查四份活跃文档存在。
- 已检查三份 `_ALIGNED` 并行副本不存在。
- 已检查四份活跃文档具备 `## 中文版` / `## English Version` 双语结构标头。
- 已检查活跃文档内能 grep 到对齐锚点、shared family 和 page-role 对齐语句。

### 风险 / 备注

- 本次触达的四份活跃 label-policy 文档在当前 worktree 中是未跟踪文件，无法基于已提交版本做 `git diff` 基线比对，只能做文件内容级验证。
- 仓库外历史材料如果仍引用 `_ALIGNED` 文件名，需要后续人工在跨窗口提示词或外部笔记中改为稳定文件名。
- 本次严格限制在 task `scope_in` 内，没有扩写 ontology，也没有传播改动到无关模块文档。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: HANDOFF-2026-04-07-LABEL-POLICY-SUITE-REPO-ALIGNMENT
- Related Task ID: TASK-2026-04-07-LABEL-POLICY-SUITE-REPO-ALIGNMENT
- Task Title: Replace or merge repo label-policy docs to the aligned auto/rule/manual suite
- Module: labeling / docs / governance
- Author: Codex
- Date: 2026-04-07
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

---

## 1. Executive Summary

The active in-repo label-policy suite was aligned onto the stable non-`_ALIGNED` filenames under `docs/data/`.

`Warden_AUTO_LABEL_POLICY_V1.md`, `Warden_RULE_LABEL_POLICY_V1_CORE.md`, and `Warden_MANUAL_LABEL_POLICY_V1_CORE.md` were minimally merged in place using the supplied aligned suite as the semantic baseline. `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md` was retained as the suite-level alignment note and updated to point at the stable active filenames. The three per-layer `_ALIGNED` copies were removed so the repo no longer presents multiple competing active versions of the same policy layer.

Current completion state is `DONE` for the scope defined in the task doc.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Minimally merged `docs/data/Warden_AUTO_LABEL_POLICY_V1.md` to mark it as the active aligned repo copy and keep its relationship to the suite note explicit.
- Minimally merged `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md` to add the aligned primary threat candidate family, aligned scenario candidate family, and the `uncertain` page-role member needed by the approved aligned suite.
- Minimally merged `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md` to make the shared primary/scenario-family alignment with `rule` explicit while preserving the existing final-adjudication semantics.
- Updated `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md` so the retained suite note points to the stable active filenames and explicitly states that per-layer `_ALIGNED` copies should not remain as parallel active docs.

### Output / Artifact Changes

- Removed `docs/data/Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md`.
- Removed `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md`.
- Removed `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md`.

---

## 3. Files Touched

- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `docs/data/Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md`
- `docs/handoff/2026-04-07_label_policy_suite_repo_alignment.md`

Optional notes per file:

- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`: minimal merge only; no ontology expansion.
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`: minimal merge plus the approved aligned `uncertain` page-role member.
- `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`: retained as the suite alignment note.

---

## 4. Behavior Impact

### Expected New Behavior

- The active repo label-policy suite now resolves to the stable non-`_ALIGNED` filenames only.
- The active `rule` policy doc now explicitly aligns its primary threat candidate family, scenario candidate family, and page-role family with the approved suite baseline.
- The suite alignment note is preserved as the supporting cross-layer anchor instead of leaving three parallel `_ALIGNED` policy copies active.

### Preserved Behavior

- `auto` remains the evidence-first weak layer.
- `rule` remains the decision-support weak layer with unified offline backfill as the default production path whenever practical.
- `manual` remains the final adjudication layer and selective high-value annotation remains the default coverage policy instead of a full-corpus prerequisite.

### User-facing / CLI Impact

- none

### Output Format Impact

- Markdown doc content only; no runtime output, CLI output, or dataset-output format was changed.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `rule -> threat_taxonomy_v1 -> primary_threat_label_candidate`
- `rule -> threat_taxonomy_v1 -> scenario_label_candidate`
- `rule.page_role_hint` / `manual.manual_page_role` documentation alignment

Compatibility notes:

This task updated active documentation semantics and active-doc selection only. No dataset-output field names, sample on-disk schema, training code, inference logic, or CLI entry points were modified.

The only enum-level alignment change made in the active repo policy docs was adding `uncertain` to the active `rule.page_role_hint` family so it matches the approved aligned suite and the existing manual counterpart. That change was explicitly required by the task's aligned baseline and was not a speculative redesign.

---

## 6. Validation Performed

### Commands Run

```bash
@( 'docs/data/Warden_AUTO_LABEL_POLICY_V1.md','docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md','docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md','docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md' ) | ForEach-Object { if (Test-Path $_) { "OK`t$_" } else { "MISSING`t$_" } }

@( 'docs/data/Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md','docs/data/Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md','docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md' ) | ForEach-Object { if (Test-Path $_) { "EXISTS`t$_" } else { "MISSING`t$_" } }

rg -n "^## 中文版$|^## English Version$" docs/data/Warden_AUTO_LABEL_POLICY_V1.md docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md

rg -n "活跃版本|active in-repo|当前对齐的一阶 primary threat candidate family|Current aligned primary threat candidate family|当前对齐的 scenario candidate family|Current aligned scenario candidate family|manual_page_role|manual_primary_threat_label" docs/data/Warden_AUTO_LABEL_POLICY_V1.md docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md
```

### Result

- All four active suite docs exist at the expected repo paths.
- All three per-layer `_ALIGNED` copies are absent after alignment.
- All four active suite docs expose bilingual section headings.
- Alignment anchors, shared-family markers, and page-role alignment lines are present in the touched docs.

### Not Run

- full repo-wide markdown bilingual scan
- tracked diff review against a committed Git baseline
- downstream validation in training/inference/manual-review tooling

Reason:

The touched suite docs are currently untracked in this worktree, so validation was limited to direct file-presence and content-sanity checks within the task scope. Broader repo-wide scans were not necessary for this minimal documentation alignment and could introduce unrelated noise.

---

## 7. Risks / Caveats

- The four active suite docs are currently untracked in this worktree, so this handoff cannot compare the result against a committed baseline using Git history.
- External notes, prompts, or off-repo artifacts may still mention the removed `_ALIGNED` filenames as source docs; the active in-repo suite now uses the stable non-`_ALIGNED` filenames.
- No unrelated docs were updated because no in-repo active references requiring path correction were found within `scope_in`; if external references exist outside the repo, they still need manual cleanup.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
- `docs/data/Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- `docs/data/Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `docs/handoff/2026-04-07_label_policy_suite_repo_alignment.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- Stage the four active suite docs plus this handoff if you want the stable non-`_ALIGNED` suite to become the repo baseline.
- If you want a secondary review, take this handoff plus the touched docs back to GPT web for acceptance against the task checklist.
- Keep future label-policy edits on the stable filenames and update the suite note in the same change whenever one layer's semantics shifts.
