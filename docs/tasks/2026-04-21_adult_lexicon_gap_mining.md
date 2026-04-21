# Adult lexicon-gap mining task

## 中文版
> 面向人工阅读的摘要版。英文版是权威版本；若字段、路径、命令、兼容性结论有冲突，以英文版为准。
### 使用说明

- 本任务只处理当前 adult pool 里 `mixed low-support` miss 桶的词缺口。
- 目标是先挖出高频本地化成人词，再只做一轮低成本、可解释、可回退的特化。
- 不允许借这个任务顺手重开 broad adult recall recovery，也不允许碰 `gambling` / `gate`。

## 任务元信息

- 任务 ID：`TASK-L0-2026-04-21-ADULT-LEXICON-GAP-MINING`
- 任务标题：`Adult mixed low-support 词缺口挖掘与低成本特化`
- 执行角色：`Codex Execution Engineer`
- 优先级：`High`
- 状态：`TODO`
- 相关模块：`Inference`
- 相关文档：`AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`、`docs/handoff/2026-04-20_adult_domain_recovery.md`
- 创建日期：`2026-04-21`
- 提出人：`User`

## 1. Background

The current adult detector still misses a remaining bucket of adult-pool samples after the narrow domain-supported single-strong-token recovery. A focused mining pass showed that the remaining misses are not mainly caused by empty text. All current misses examined in that pass still had `visible_text.txt`, and the largest unresolved bucket was the mixed low-support group previously described as roughly `48` samples.

That bucket appears to contain a vocabulary-coverage problem:

- localized or transliterated adult vocabulary not covered by the current adult lexicon
- low-cost adult surfaces whose visible text does not map cleanly onto the current keyword lists
- a smaller amount of pool contamination or boundary-noisy samples

This task is needed now to see whether a small explainable lexicon refinement can recover part of that bucket without materially rebounding the benign pool.

## 2. Goal

Mine the current adult mixed low-support miss bucket for repeated local adult vocabulary gaps, then implement at most one minimal low-cost explainable adult lexicon refinement if the mined terms are clean enough. The outcome must stay inside L0-compatible lightweight text/url evidence and must explicitly quantify adult gain, benign rebound, and remaining risk.

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\L0_DESIGN_V1.md`
- `docs/tasks/2026-04-21_adult_lexicon_gap_mining.md`
- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

This task is allowed to change:

- one narrow adult lexicon refinement derived from the mixed low-support mining result
- adult detector contract wording if behavior changes
- task / handoff docs

## 4. Scope Out

This task must NOT do the following:

- reopen a broad adult recall rollback
- modify `gambling` or `gate`
- add OCR, screenshot semantics, HTML-heavy parsing, or dependencies
- rename schema fields, output keys, or CLI flags
- move dataset directories

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/handoff/2026-04-20_adult_current85_rebucket_and_tighten.md`
- `docs/handoff/2026-04-20_adult_moved55_spotcheck_and_lost44_review.md`
- `docs/handoff/2026-04-20_adult_domain_recovery.md`

### Code / Scripts

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `E:\Warden\data\raw\benign\hard benign\adult`
- `E:\Warden\data\raw\benign\benign`
- the current adult mixed low-support miss bucket

### Prior Handoff

- `docs/handoff/2026-04-20_adult_domain_recovery.md`

### Missing Inputs

- `none`

## 6. Required Outputs

This task should produce:

- one mined summary of repeated local adult vocabulary gaps in the mixed low-support bucket
- one minimal adult lexicon refinement if the mined terms are clean enough
- updated adult detector contract wording if behavior changes
- before/after adult-vs-benign quantification plus repo handoff

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

- mining must stay focused on the current mixed low-support adult misses
- any lexicon refinement must stay low-cost, explainable, and auditable
- do not admit weak or ambiguous terms unless the evidence for adult specificity is strong

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current `specialized_surface_signals`
- current `specialized_reason_codes`
- current `l0_routing_hints`

Schema / field constraints:

- Schema changed allowed: `NO`
- If yes, required compatibility plan: `not applicable`
- Frozen field names involved: `possible_adult_lure`; `possible_age_gate_surface`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python -m py_compile E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
  - current sample-dir labeling flow
  - current downstream readers of `specialized_surface_signals`

Downstream consumers to watch:

- adult proxy metrics
- future adult recall / precision tuning

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Identify stable contracts that cannot break.
3. Mine the current mixed low-support bucket and extract repeated adult vocabulary gaps.
4. Make the smallest valid code/doc change.
5. Run the smallest meaningful validation.
6. Summarize compatibility impact and prepare handoff.

Task-specific execution notes:

- quantify the current miss bucket before changing the lexicon
- prefer a tiny allowlist or tiny keyword addition over broad semantic relaxation
- rerun both adult and benign metrics after the patch

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [x] Goal is met
- [x] Scope-out items were not touched
- [x] Relevant files were updated correctly
- [x] No silent schema / interface break was introduced
- [x] Validation was run, or inability to run was explicitly stated
- [x] Risks are documented
- [x] Required docs were updated or doc debt was explicitly listed
- [x] Final response follows required engineering format
- [x] Handoff is provided for non-trivial changes

Task-specific acceptance checks:

- [x] the current mixed low-support adult misses are re-mined and summarized
- [x] any new adult lexicon refinement is explicitly justified by repeated miss evidence
- [x] adult gain and benign rebound are both measured

## 11. Validation Checklist

Minimum validation expected:

- [x] syntax / import sanity
- [x] targeted mixed low-support mining pass
- [x] after-patch adult vs benign quantification
- [x] handoff produced

Commands to run if applicable:

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"
python - <<'PY'
# mine mixed low-support adult misses and rerun adult-vs-benign metrics
PY
```

Expected evidence to capture:

- repeated local adult vocabulary gaps
- recovered adult sample count
- benign rebound count

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

- `docs/handoff/2026-04-21_adult_lexicon_gap_mining.md`

## 13. Open Questions / Blocking Issues

- none

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: `TASK-L0-2026-04-21-ADULT-LEXICON-GAP-MINING`
- Task Title: `Mine the adult mixed low-support vocabulary gaps and add one low-cost refinement`
- Owner Role: `Codex Execution Engineer`
- Priority: `High`
- Status: `DONE`
- Related Module: `Inference`
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-04-20_adult_domain_recovery.md`
- Created At: `2026-04-21`
- Requested By: `User`

Use this task to mine the current adult mixed low-support miss bucket for repeated vocabulary gaps and, only if the evidence is clean enough, add one minimal low-cost explainable adult lexicon refinement.
