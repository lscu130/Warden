# Roblox+Netflix+Trezor+Ledger malicious cluster/pool scope and cap relaxation task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务单用于把当前活动执行范围从“仅 Roblox + Netflix families 默认进入高级 cluster / subcluster / train-reserve 流程”收口调整为“仅 Roblox + Netflix + Trezor + Ledger families 默认进入该高级流程”。
- 本任务单同时用于把当前默认 `family_share_cap` 从过于激进的 `0.10` 放宽到更温和、但仍保留 family 压缩边界的默认值。
- 本任务单不推翻 `Warden_DATA_INGEST_ARCHITECTURE_V1` 与 `Warden_MALICIOUS_SOURCE_POLICY_V1` 的 V1 通用能力边界，只调整当前活动 rollout 范围与默认保留强度。
- 本文档是 Markdown 交付物，按项目规则采用“中文摘要在前、英文全文在后、英文权威”。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-04-22-FOUR-FAMILY-CLUSTER-POOL-SCOPE-AND-CAP-RELAXATION
- Task Title: Expand the current malicious advanced cluster/pool scope to Roblox, Netflix, Trezor, and Ledger, and relax the default family share cap
- Owner Role: GPT web task drafter / human owner freezes scope / Codex executes
- Priority: High
- Status: TODO
- Related Module: data / malicious-ingest / maintenance / docs
- Related Issue / ADR / Doc: `PROJECT.md`; `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`; `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`; `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`; `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- Created At: 2026-04-22
- Requested By: user

Use this task for the non-trivial follow-up that widens the current default advanced malicious scope from two families to four families and loosens the current default family-share compression.

---

## 1. Background

Warden V1 already keeps a broader malicious advanced capability boundary of cluster -> subcluster -> train/reserve handling, while the current active rollout scope was previously tightened to Roblox+Netflix-only by default.

The current user request is a narrow follow-up:
- Roblox and Netflix should stay enabled for the advanced path,
- Trezor and Ledger should now also be enabled for that same default path,
- all other malicious families should remain on the basic ingest/archive path by default,
- the current default `family_share_cap = 0.10` is considered too aggressive for the observed duplicate-heavy data and should be relaxed somewhat.

This is still a bounded rollout-scope and default-parameter change.
It is not a request to redesign malicious clustering globally, remove family compression, or reopen all-family advanced handling by default.

---

## 2. Goal

Make the current malicious advanced cluster / subcluster / train-reserve execution path explicitly scoped by default to the Roblox, Netflix, Trezor, and Ledger families, while preserving the broader V1 architecture as a general capability boundary and keeping all other malicious families on the basic path by default. In the same task, relax the default family-share compression so train-pool retention is less aggressive on duplicate-heavy data, while still retaining a bounded per-family cap and additive CLI override.

---

## 3. Scope In

This task is allowed to touch:

- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`
- one new repo task doc
- one new repo handoff doc

This task is allowed to change:

- current rollout-scope wording in the two active malicious-ingest policy docs
- the default advanced family list for the current active cluster/pool scripts
- the default `family_share_cap` value for the current active train-pool / maintenance paths
- additive CLI help text only as needed to reflect the updated defaults
- documentation wording that distinguishes:
  - general V1 capability boundary,
  - current active rollout scope,
  - current default compression strength

If a file is not listed here, treat it as out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the full malicious-ingest architecture
- do not convert the current implementation into all-family advanced clustering by default
- do not remove the archive / train / reserve three-pool concept
- do not remove family-share control entirely
- do not rewrite clustering into a global fuzzy template-matching system
- do not rewrite the capture engine
- do not rewrite the benign pipeline
- do not rename frozen schema fields, frozen file names, or frozen directory contracts
- do not add third-party dependencies
- do not modify unrelated data-externalization work or other dirty files already in the worktree

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`

### Code / Scripts

- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- `scripts/data/maintenance/backfill_existing_sample_fingerprints.py`

### Data / Artifacts

- current observed malicious-capture batches indicating Roblox / Netflix / Trezor / Ledger duplication pressure
- any current cluster / pool outputs if needed for smoke checking
- synthetic sample directories if real Trezor/Ledger samples are not available locally

### Prior Handoff

- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

### Missing Inputs

- real local Trezor-tagged malicious samples, if absent
- real local Ledger-tagged malicious samples, if absent
- an explicitly approved numeric target for the relaxed default family-share cap beyond the user request to loosen it

If required inputs are missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- updated wording in `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md` that explicitly distinguishes the broader V1 capability boundary from the current Roblox+Netflix+Trezor+Ledger rollout scope
- updated wording in `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md` with the same four-family current-scope statement
- minimal code changes so the default advanced family scope becomes Roblox + Netflix + Trezor + Ledger
- minimal code changes so the default `family_share_cap` is relaxed while remaining additive and bounded
- consistent default behavior across the cluster, train-pool, review, exclusion, and backfill maintenance paths that expose the active advanced path or the family-share cap
- a repo handoff document

Be concrete and keep the patch minimal.

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
- Markdown deliverables must remain bilingual, with English authoritative.

Task-specific constraints:

- Clearly distinguish the broader V1 capability boundary from the current active rollout scope.
- Other malicious families must still stay out of advanced cluster / subcluster / train-reserve handling by default.
- Do not silently remove the explicit `--advanced_family_brands all` escape hatch.
- Do not turn this task into a global malicious cluster/pool rewrite.
- Keep the cap relaxation moderate and auditable rather than removing the cap or making it effectively meaningless.
- If an exact relaxed default cap is chosen by implementation judgment, state it explicitly in the handoff and explain why that default was selected.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current frozen sample-output structure
- current archive / train / reserve conceptual separation
- existing malicious-ingest script entrypoints, unless a new optional parameter is added compatibly
- existing `--advanced_family_brands` parameter name
- existing `--family_share_cap` parameter name

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none should be renamed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing malicious cluster/train-pool scripts
  - existing review-manifest and exclusion-list scripts
  - existing maintenance backfill script
- If default behavior changes, keep it additive, document it, and keep the explicit override path available.

Downstream consumers to watch:

- train-pool summary outputs
- review manifest generation
- training exclusion-list generation
- any current docs that describe the active advanced scope

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing docs, the prior Roblox+Netflix task/handoff, and the active malicious-ingest policy docs.
2. Inspect the current family-scope and family-share-cap defaults.
3. Create a new task doc that freezes the four-family scope and cap-relaxation boundary.
4. Apply the smallest code changes that:
   - expand the active default advanced family list,
   - relax the default `family_share_cap`,
   - preserve additive CLI overrides.
5. Update the two active malicious-ingest docs to reflect the current four-family rollout scope.
6. Run targeted validation, using synthetic smoke if real Trezor/Ledger samples are unavailable.
7. Prepare handoff.

Task-specific execution notes:

- Reuse the existing family-scope mechanism instead of inventing a new routing layer.
- Keep all non-listed families on the basic path by default.
- Use the same relaxed default cap consistently across train-pool and backfill maintenance paths that expose it.
- If real Trezor/Ledger samples are not locally available, use the smallest auditable synthetic smoke input and say so explicitly.

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

- [ ] the active implementation defaults now target Roblox, Netflix, Trezor, and Ledger for advanced cluster/pool handling
- [ ] all other malicious families still remain outside the broader advanced cluster/pool path by default
- [ ] the default family-share compression is relaxed from `0.10` to the chosen higher value without removing the cap entirely
- [ ] the same relaxed default cap is used consistently in the active train-pool and maintenance path that exposes it
- [ ] docs clearly distinguish V1 general capability from the current four-family rollout scope
- [ ] handoff explicitly states the chosen relaxed cap value and its compatibility impact

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py scripts/data/maintenance/backfill_existing_sample_fingerprints.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
python scripts/data/maintenance/backfill_existing_sample_fingerprints.py --help
```

Targeted smoke behavior to verify, if runnable with available sample data/config:

```bash
# Default four-family scope
python scripts/data/malicious/build_malicious_clusters.py [existing args...]

# All-family control run
python scripts/data/malicious/build_malicious_clusters.py [existing args...] --advanced_family_brands all

# Default train-pool run with the relaxed cap
python scripts/data/malicious/build_malicious_train_pool.py [existing args...]
```

Expected evidence to capture:

- docs now distinguish general architecture from the current four-family rollout scope
- Roblox / Netflix / Trezor / Ledger enter the advanced path by default
- a non-listed family stays out of the default advanced path
- the reported `family_share_cap` in output summaries reflects the new relaxed default

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

- `docs/handoff/2026-04-22_roblox_netflix_trezor_ledger_cluster_pool_scope_and_cap_relaxation.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- what exact relaxed default cap should replace `0.10` in the absence of a user-specified number
- whether real local Trezor-tagged malicious samples are available for smoke validation
- whether real local Ledger-tagged malicious samples are available for smoke validation

If none remain after code inspection, write `none`.
