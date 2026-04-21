# Channel URL keep-oldest dedup task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于在 `channel/` 目录下新增一个按目录名中的 URL 分组去重的维护脚本。
- 目标是对同一 URL 的重复样本，仅保留最老时间戳对应的目录，其余目录输出删除计划，并在显式参数下执行删除。
- 本任务不修改冻结样本字段名，不重写 manifest 主流程，不扩展到训练或推理模块。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: TASK-2026-04-08-CHANNEL-URL-KEEP-OLDEST-DEDUP
- Task Title: Add a low-memory maintenance script to deduplicate channel sample directories by URL and keep the oldest sample
- Owner Role: Codex executes under active repo contracts
- Priority: High
- Status: TODO
- Related Module: data / maintenance / dataset hygiene
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_DATA.md`
- Created At: 2026-04-08
- Requested By: user

Use this task for the non-trivial addition of a channel-directory URL dedup maintenance utility.

---

## 1. Background

The repository contains a `channel/` directory with sample directories named in the form:

- `<url_key>_<YYYYMMDDTHHMMSSZ>`

Observed duplicates exist where the URL portion is identical and only the timestamp suffix differs. The requested behavior is to scan such sample directories, group them by URL key, and keep only the oldest timestamped sample for each URL.

This is a data-maintenance task with compatibility and safety implications because the implementation may delete directories when explicitly requested. The tool must therefore remain:

- low-memory,
- fast,
- auditable,
- default-safe.

---

## 2. Goal

Add an opt-in maintenance script under `scripts/data/maintenance/` that scans a channel root, groups sample directories by the URL key encoded in the directory name, keeps the oldest timestamped directory for each URL key, emits auditable keep/delete artifacts, defaults to dry-run mode, and only deletes duplicate directories when an explicit delete flag is supplied. The implementation must preserve existing schema and manifest behavior and must not silently affect current data-ingest entrypoints.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/maintenance/`
- `docs/modules/MODULE_DATA.md`
- one new repo task doc
- one new repo handoff doc

This task is allowed to change:

- data-maintenance utility coverage for channel URL deduplication
- module documentation that clarifies this utility is an opt-in maintenance path rather than a default formal data-entry script
- maintenance output artifacts for dedup review

If a file or directory is not listed here, treat it as out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not rename frozen sample fields, file names, or manifest fields
- do not modify `scripts/data/build_manifest.py`
- do not modify `scripts/data/check_dataset_consistency.py`
- do not redesign the dataset layout
- do not add new third-party dependencies
- do not automatically delete anything unless the operator explicitly passes a delete flag
- do not touch training, inference, or labeling logic

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_DATA.md`

### Code / Scripts

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/common/io_utils.py`
- `scripts/data/maintenance/build_dedup_review_manifest.py`

### Data / Artifacts

- `channel/`
- sample directories such as `channel/1-easybank-landing-page-master.vercel.app_20251230T075649Z`
- sample directories such as `channel/1-easybank-landing-page-master.vercel.app_20260306T075237Z`

### Prior Handoff

- none

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- a new maintenance script for channel URL deduplication that keeps the oldest timestamped sample per URL key
- dry-run keep/delete artifacts suitable for review
- explicit delete mode guarded by a flag
- a small doc update that clarifies the utility's maintenance-only role
- a repo handoff document

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

- The script must default to dry-run.
- The script must not read per-sample JSON files during normal grouping unless necessary; directory-name grouping is the intended fast path.
- Memory usage should scale with the number of unique URL keys, not with all duplicate sample files loaded into memory.
- Actual deletion must verify the target directory remains within the requested input root before recursive removal.
- The script must be direct and auditable rather than clever.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing frozen sample directory contents
- existing manifest script CLI and output behavior
- existing consistency-check CLI and output behavior

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/build_manifest.py --help`
  - `python scripts/data/check_dataset_consistency.py --help`
- New dedup behavior must be additive via a new maintenance script rather than a behavior change to an existing entrypoint.

Downstream consumers to watch:

- dataset operators using `channel/` as raw sample storage
- any later scripts that expect only one kept directory per URL after hygiene cleanup

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing docs and relevant data scripts.
2. Inspect the observed `channel/` directory layout and duplicate pattern.
3. Add the smallest safe maintenance script under `scripts/data/maintenance/`.
4. Update the data module doc to clarify the maintenance-only boundary.
5. Run syntax/help checks and a targeted smoke validation.
6. Prepare handoff.

Task-specific execution notes:

- Prefer two-pass scanning so the tool only retains the current oldest candidate per URL key in memory.
- Prefer `os.scandir()`-style directory iteration for speed.
- Emit explicit summary counts for kept, duplicate, skipped, and deleted directories.

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

- [ ] the new script groups channel sample directories by directory-name URL key
- [ ] the oldest timestamped directory is kept for each URL key
- [ ] dry-run outputs explicitly show which directories would be deleted
- [ ] actual deletion requires an explicit flag
- [ ] deletion paths are verified to remain under the requested input root
- [ ] validation covers the observed `channel/` example and at least one controlled smoke test

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py
python scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py --help
python scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py --input-root E:\Warden\channel --output-dir E:\Warden\tmp\channel_url_dedup_real_check
```

Expected evidence to capture:

- the real `channel/` example reports one kept directory and one duplicate delete candidate for the same URL key
- a controlled temp-data smoke run shows delete mode removes only the newer duplicate directory
- no existing manifest or consistency-check entrypoint behavior was changed

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

- `docs/handoff/2026-04-08_channel_url_keep_oldest_dedup.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
