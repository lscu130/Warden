# Roblox+Netflix-only malicious cluster/pool scope-tightening task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务单用于把 **当前活动执行范围** 从“仅 Roblox family 默认启用高级 cluster / subcluster / train-reserve pool”调整为“仅 Roblox + Netflix families 默认启用该高级流程”。
- 本任务单不推翻 `Warden_DATA_INGEST_ARCHITECTURE_V1` 和 `Warden_MALICIOUS_SOURCE_POLICY_V1` 的 **V1 通用能力定义**，只调整 **当前活动 rollout 范围**。
- 本文档是 Markdown 交付物，按项目规则采用“中文摘要在前、英文全文在后、英文权威”。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-04-08-ROBLOX-NETFLIX-ONLY-CLUSTER-POOL-SCOPE-TIGHTENING
- Task Title: Tighten current malicious cluster/pool execution scope to Roblox and Netflix families only
- Owner Role: GPT web task drafter / human owner freezes scope / Codex executes
- Priority: High
- Status: TODO
- Related Module: data / malicious-ingest / maintenance / docs
- Related Issue / ADR / Doc: `PROJECT.md`; `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`; `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`; `Warden_DATA_INGEST_ARCHITECTURE_V1.md`; `Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- Created At: 2026-04-08
- Requested By: user

Use this task for the non-trivial tightening of the currently active malicious dedup / cluster / pool execution scope.

---

## 1. Background

Warden V1 already defines a general malicious-ingest architecture with:
- shared lower-layer capture,
- separate benign and malicious upper-layer pipelines,
- raw archive / train-eligible canonical pool / reserve pool,
- campaign / template clustering,
- subcluster splitting,
- family-share control,
- legacy-data backfill and review outputs.

The previous active rollout tightening made the advanced cluster / subcluster / train-reserve path Roblox-only by default.

The current requested rollout change is narrower than a global malicious-family expansion but broader than the previous Roblox-only scope:
- Roblox family should remain enabled for advanced handling,
- Netflix family should also become enabled for advanced handling,
- all other malicious families should remain on the basic ingest/archive path for now.

For all other malicious families, keep only:
- source recording,
- page-validity checks,
- raw archive handling,
- optional exact-URL hygiene dedup within batch/run scope,
- no broader family/template clustering by default.

This task is about tightening the **current execution scope**, not redefining the long-term V1 architecture.

---

## 2. Goal

Make the current malicious cluster / subcluster / train-reserve execution path explicitly scoped to the Roblox and Netflix families, while preserving the broader V1 architectural documents as the general capability boundary. The task must update docs and implementation so that:
- Roblox and Netflix remain the only actively enabled families for advanced cluster/pool handling at the current stage,
- all other malicious families remain on a basic ingest/archive path,
- the implementation does not silently remove the broader V1 capability from future use,
- the behavior is explicit, documented, backward compatible where reasonable, and auditable.

---

## 3. Scope In

This task is allowed to touch:

- `Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- current repo copies of those docs under the appropriate `docs/` path, if those are the actual active files
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`
- small shared helper files only if strictly required to support Roblox+Netflix-family scoping
- one new repo task doc
- one repo handoff doc

This task is allowed to change:

- current execution-scope wording in docs
- family-scope gating logic for advanced malicious cluster/pool handling
- CLI/config exposure for Roblox+Netflix-only scope control, if needed
- review-manifest / exclusion-list routing logic only as required to reflect Roblox+Netflix-only advanced handling
- documentation wording that distinguishes:
  - long-term V1 capability,
  - current-stage active rollout scope

If a file is not listed here, treat it as out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the full malicious-ingest architecture
- do not remove the archive / train / reserve three-pool concept from the V1 docs
- do not rewrite benign pipeline logic
- do not rewrite the capture engine
- do not enable advanced clustering for all malicious families
- do not redefine malicious label taxonomy
- do not change TrainSet V1 schema or frozen sample-file names
- do not add new third-party dependencies
- do not physically delete archived data
- do not change unrelated malicious-source policies beyond what is required for Roblox+Netflix-only scope tightening

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-04-02_roblox_only_cluster_pool_scope_tightening_task.md`
- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`
- `Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `Warden_MALICIOUS_SOURCE_POLICY_V1.md`

### Code / Scripts

- `scripts/data/common/pool_utils.py`
- `scripts/data/malicious/build_malicious_clusters.py`
- `scripts/data/malicious/build_malicious_train_pool.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`
- `scripts/data/maintenance/build_training_exclusion_lists.py`

### Data / Artifacts

- current observed malicious-capture batches indicating why Roblox and Netflix should remain/enter the advanced scope
- any existing cluster / subcluster / train-pool outputs if needed for smoke checking
- any current config or manifest files used by the above scripts

### Prior Handoff

- `docs/handoff/2026-04-02_roblox_only_cluster_pool_scope_tightening.md`

### Missing Inputs

- exact Netflix-family matching evidence in current malicious sample data, if local malicious samples are absent
- exact current active config surface for multi-family advanced clustering, if not already implemented

If required inputs are missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- updated doc wording in `Warden_DATA_INGEST_ARCHITECTURE_V1.md` that explicitly distinguishes general V1 architecture from the current Roblox+Netflix-only rollout scope
- updated doc wording in `Warden_MALICIOUS_SOURCE_POLICY_V1.md` that explicitly states Roblox+Netflix-only active advanced dedup/cluster/pool handling at the current stage
- minimal code changes so that advanced cluster/subcluster/train-reserve handling applies only to Roblox and Netflix families by default
- explicit behavior for all other malicious families:
  - source recording,
  - page-validity checks,
  - raw archive handling,
  - optional exact-URL hygiene dedup only,
  - no broad advanced family/template clustering by default
- a clear CLI/config description if a family-scope parameter is added or exposed
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

- Do not misstate this task as a full architecture reversal. The docs must preserve the broader V1 capability as the general design boundary.
- The current active rollout scope must be explicitly described as Roblox+Netflix-family-only advanced handling.
- Other malicious families must not silently pass through the advanced cluster/pool path by default after this task.
- Optional exact-URL hygiene dedup for non-Roblox/non-Netflix families may remain, but do not expand that into campaign/template clustering.
- Do not convert Roblox+Netflix-only rollout logic into undocumented hardcoded behavior without documenting it.
- If a default family matcher is introduced or updated, make it auditable and easy to adjust later.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- current frozen sample-output structure
- current archive / train / reserve conceptual separation
- current capture engine invocation path unless a listed script explicitly requires a compatible adjustment
- existing malicious-ingest script entrypoints, unless a new optional parameter is added compatibly

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none should be renamed

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - existing malicious ingest/capture entrypoints
  - existing legacy-data backfill entrypoints
  - existing cluster/train-pool scripts, unless a new optional flag is added compatibly
- If a new flag is introduced, it must be additive and default-safe.

Downstream consumers to watch:

- review manifest generation
- training exclusion-list generation
- any current malicious-train-pool report or summary outputs
- any docs or task/handoff text that describe cluster/pool as globally active for all families right now

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing docs, the prior Roblox task/handoff, and the two malicious-policy docs.
2. Inspect current script behavior for family-scoped clustering and pool construction.
3. Identify the smallest possible change from Roblox-only scope to Roblox+Netflix-only scope.
4. Update docs to distinguish general architecture from the current rollout scope.
5. Implement the smallest code/config change that makes Roblox+Netflix-only advanced handling explicit by default.
6. Run targeted smoke validation.
7. Prepare handoff.

Task-specific execution notes:

- Prefer a default-safe configuration path rather than structural rewrites.
- Preserve future extensibility, but do not enable more families now.
- Reuse the existing family-scope mechanism added for the Roblox-only task if possible.
- If local Netflix-tagged malicious samples are missing, use the smallest auditable synthetic smoke input and state that clearly.

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

- [ ] `Warden_DATA_INGEST_ARCHITECTURE_V1.md` explicitly states that the full V1 architecture remains valid, but the current active advanced malicious cluster/pool rollout is Roblox+Netflix-only
- [ ] `Warden_MALICIOUS_SOURCE_POLICY_V1.md` explicitly states that all other families currently remain on basic ingest/archive handling, optionally with exact-URL hygiene dedup only
- [ ] advanced cluster/subcluster/train-reserve behavior is Roblox+Netflix-only by default in the active implementation
- [ ] other families do not silently enter broad advanced family/template clustering by default
- [ ] any new CLI/config behavior is additive, documented, and backward compatible
- [ ] handoff clearly states the difference between long-term architecture and the current rollout scope

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile scripts/data/common/pool_utils.py scripts/data/malicious/build_malicious_clusters.py scripts/data/malicious/build_malicious_train_pool.py scripts/data/maintenance/build_dedup_review_manifest.py scripts/data/maintenance/build_training_exclusion_lists.py
python scripts/data/malicious/build_malicious_clusters.py --help
python scripts/data/malicious/build_malicious_train_pool.py --help
python scripts/data/maintenance/build_dedup_review_manifest.py --help
python scripts/data/maintenance/build_training_exclusion_lists.py --help
```

Targeted smoke behavior to verify, if runnable with available sample data/config:

```bash
# Default Roblox+Netflix scope
python scripts/data/malicious/build_malicious_clusters.py [existing args...]

# All-family control run
python scripts/data/malicious/build_malicious_clusters.py [existing args...] --advanced_family_brands all
```

Expected evidence to capture:

- docs now distinguish general architecture from the current rollout scope
- Roblox and Netflix families enter the advanced cluster/pool path by default
- other families do not enter broad advanced cluster/pool path by default
- existing CLI remains valid or additive compatibility is documented

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

- `docs/handoff/2026-04-08_roblox_netflix_only_cluster_pool_scope_tightening.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- what exact matcher should define the Netflix family in the active implementation: domain tokens, brand tokens, or both
- whether local malicious sample data already includes a usable Netflix-tagged case for smoke validation
- whether non-Roblox/non-Netflix exact-URL hygiene dedup is already present and should simply remain documented

If none remain after code inspection, write `none`.
