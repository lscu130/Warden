# Warden 标签策略对齐版落仓任务单

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务单用于把 repo 内现有旧版 `auto / rule / manual` 标签策略文档统一到本轮已对齐的一组口径。
- 本任务单是 **文档替换/合并任务**，不是新的标签体系发散设计任务。
- 本任务单不要求顺手扩展长尾 ontology，不要求改动训练逻辑，也不要求改动 frozen dataset-output schema。
- 若交付物为 Markdown，默认采用“中文摘要在前、英文全文在后、英文权威”。

## English Version

> AI note: GPT, Gemini, Codex, Grok, Claude, and other model agents must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-04-07-LABEL-POLICY-SUITE-REPO-ALIGNMENT
- Task Title: Replace or merge repo label-policy docs to the aligned auto/rule/manual suite
- Owner Role: GPT web task drafter / human owner freezes scope / Codex executes
- Priority: High
- Status: TODO
- Related Module: labeling / docs / governance
- Related Issue / ADR / Doc:
  - `AGENTS.md`
  - `PROJECT.md`
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
  - `docs/templates/TASK_TEMPLATE.md`
  - `docs/templates/HANDOFF_TEMPLATE.md`
  - current repo copies of label-policy docs
  - aligned source docs supplied with this task
- Created At: 2026-04-07
- Requested By: user

Use this task for the non-trivial repo documentation alignment of the Warden label-policy suite.

---

## 1. Background

Warden now has an aligned label-policy suite prepared outside the repo, covering:

- the shared interpretation of the three labeling layers;
- the aligned primary threat family;
- the aligned scenario family;
- the aligned page-role family;
- the aligned policy that:
  - `auto` remains the evidence-first weak layer,
  - `rule` remains the decision-support weak layer,
  - `manual` remains the final adjudication layer,
  - `rule` should be unified offline backfill whenever practical,
  - `manual` should remain selective high-value annotation rather than a default full-corpus requirement.

The repo may already contain older versions, partial drafts, or differently named copies of these label-policy docs. Those repo copies now need to be replaced or merged into one aligned suite without expanding scope into unrelated redesign.

The aligned source documents for this task are:

- `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md`
- `Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md`
- `Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md`

This task is not asking for a new ontology redesign. It is asking for the repo to be brought into alignment with this already-prepared suite.

---

## 2. Goal

Update the repository so that the active label-policy docs reflect one coherent aligned suite for `auto / rule / manual`, using the supplied aligned docs as the source baseline.

The result must ensure that:

- repo copies of the relevant label-policy docs are replaced or merged to match the aligned suite;
- the three layers do not drift semantically;
- the shared primary threat family, scenario family, and page-role family are consistent across the suite;
- the repo reflects the current policy that:
  - `auto` is evidence-first,
  - `rule` is decision-support,
  - `manual` is final adjudication,
  - `rule` is broad unified backfill whenever practical,
  - `manual` is selective and not a default full-corpus prerequisite;
- documentation remains bilingual and English remains authoritative.

---

## 3. Scope In

This task is allowed to touch:

- repo copies of the current label-policy docs, including whichever files currently serve as the active policy docs for:
  - auto labels
  - rule labels
  - manual labels
- repo path(s) where a suite-level alignment note should live, if appropriate
- references in nearby docs only if strictly required to keep naming/path consistency after replacement or merge
- one repo handoff document

This task is allowed to change:

- document content
- document names only if the repo currently uses clearly obsolete draft names and a rename is necessary for consistency
- document cross-references
- wording that defines layer boundaries, shared families, coverage strategy, and generation strategy
- repo insertion of the suite-alignment note as a supporting doc

If a file is not directly part of the label-policy suite or required doc-link consistency, treat it as out of scope.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the label ontology beyond the aligned suite
- do not invent new primary threat classes
- do not expand long-tail scenario or narrative taxonomy
- do not change TrainSet V1 schema
- do not change frozen sample-output field names
- do not modify training code
- do not modify inference logic
- do not modify data-ingest logic
- do not silently rewrite README or unrelated module docs
- do not add new dependencies
- do not turn this into a broad repo cleanup task

---

## 5. Inputs

Relevant inputs for this task:

### Governing Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Source Alignment Docs

- `Warden_LABEL_POLICY_SUITE_ALIGNMENT_V1.md`
- `Warden_AUTO_LABEL_POLICY_V1_ALIGNED.md`
- `Warden_RULE_LABEL_POLICY_V1_CORE_ALIGNED.md`
- `Warden_MANUAL_LABEL_POLICY_V1_CORE_ALIGNED.md`

### Existing Repo Docs To Inspect

- current repo copies of any label-policy docs
- any repo docs that currently reference those policy docs

### Missing Inputs

- exact repo-relative target paths if the aligned docs are not yet copied into the repo
- exact current repo filenames if they differ from the aligned source names

If any required repo path is missing or ambiguous, state that explicitly before modifying files.

---

## 6. Required Outputs

This task should produce:

- updated repo copy of the auto-label policy doc aligned to the new suite
- updated repo copy of the rule-label policy doc aligned to the new suite
- updated repo copy of the manual-label policy doc aligned to the new suite
- repo copy of the suite-alignment note if that is the chosen minimal integration path
- updated doc references if necessary
- a non-trivial handoff document

If the repo already contains older docs with overlapping content, the result should either:

- replace them cleanly with the aligned versions, or
- merge them minimally while preserving the aligned semantics.

Be explicit in the handoff about which strategy was used.

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
- Markdown deliverables must be bilingual by default, with English authoritative.

Task-specific constraints:

- Treat the supplied aligned docs as the semantic baseline.
- Do not expand the aligned suite into a new redesign task.
- Keep the three-layer interpretation fixed:
  - `auto` = evidence-first weak layer
  - `rule` = decision-support weak layer
  - `manual` = final adjudication layer
- Keep the aligned shared primary threat family fixed:
  - `credential_theft`
  - `payment_fraud`
  - `wallet_drain_or_web3_approval_fraud`
  - `pii_kyc_harvesting`
  - `fake_support_or_contact_diversion`
  - `malware_or_fake_download`
  - `benign`
  - `uncertain`
- Keep the aligned page-role family fixed:
  - `benign_service_page`
  - `benign_idp_redirect`
  - `direct_attack_page`
  - `hosted_lure`
  - `intermediary_carrier`
  - `gate_or_evasion_shell`
  - `download_lure`
  - `other`
  - `uncertain`
- Keep the policy that `rule` is broad backfill whenever practical and `manual` is selective, not full-corpus by default.
- Do not silently downgrade or remove existing important content unless it conflicts with the aligned suite and must be replaced.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- frozen dataset-output contract
- TrainSet V1 admission semantics unless only doc wording clarification is required
- current meaning that weak labels are not human gold labels
- current meaning that brand evidence is supportive rather than sole truth

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none should be renamed in this task

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - not applicable to code execution behavior in this task
- If any doc examples mention commands, preserve their factual meaning unless they are being explicitly corrected by aligned docs.

Downstream consumers to watch:

- future labeling tasks
- future training-label mapping tasks
- future manual-review tooling tasks
- any repo doc that references label-layer responsibilities

---

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs.
2. Inspect current repo label-policy docs and identify the active repo targets.
3. Compare repo copies against the supplied aligned docs.
4. Choose the smallest valid merge strategy:
   - direct replacement where safe, or
   - minimal merge where repo-specific context must be preserved.
5. Update cross-references only as needed.
6. Run light validation on doc presence and consistency.
7. Produce handoff.

Task-specific execution notes:

- Prefer replacement over creative merging when older drafts are clearly outdated.
- If repo naming conventions strongly prefer a different filename, keep the semantic content aligned and document the naming decision clearly.
- Preserve bilingual format.
- Keep English authoritative.
- Do not create multiple competing active versions after this task if a clear single active version can be maintained.

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

- [ ] repo active auto-label policy doc matches the aligned `auto` role and boundaries
- [ ] repo active rule-label policy doc matches the aligned `rule` role and boundaries
- [ ] repo active manual-label policy doc matches the aligned `manual` role and boundaries
- [ ] the shared primary threat family is aligned across `rule` and `manual`
- [ ] the shared scenario family is aligned where both docs reference it
- [ ] the shared page-role family is aligned across `rule` and `manual`
- [ ] repo docs clearly preserve the policy that `rule` is broad unified backfill whenever practical
- [ ] repo docs clearly preserve the policy that `manual` is selective high-value annotation rather than full-corpus by default
- [ ] no extra ontology expansion was introduced

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] doc presence check
- [ ] targeted diff / content sanity
- [ ] cross-reference sanity
- [ ] bilingual structure spot-check

Commands to run if applicable:

```bash
# example only; use the repo's actual path structure
git diff --stat
git diff -- [target_doc_paths]
```

Expected evidence to capture:

- which repo docs were replaced or merged
- whether any filenames changed
- whether aligned families and layer boundaries now match across the suite
- whether any doc debt remains

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
- docs impact
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-07_label_policy_suite_repo_alignment.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- exact repo target paths for the active label-policy docs
- whether older repo docs should be replaced in place or superseded by new filenames
- whether the suite-alignment note should become an active supporting doc in the repo or remain external

If none remain after repo inspection, write `none`.
