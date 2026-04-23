# 2026-04-21_warden_data_externalization_task

## 中文版
> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是一个用于将 Warden 大体量 `data/` 目录外迁出仓库根目录的正式任务单。
- 当前默认目标外部数据根为 `E:\WardenData`。若执行前目标路径变化，必须先更新英文版任务字段再执行。
- 若涉及精确路径、兼容策略、CLI 约束、验收标准或验证命令，以英文版为准。

## 1. 背景

- 当前 `E:\Warden` 仓库根内包含大体量 `data/` 目录，导致工作区扫描、Git 观察、桌面端索引和文件监听压力明显升高。
- 近期 Codex Windows 桌面端已多次出现 `Application Hang / MoAppHangXProc`，而工作区内大规模 `data/` 文件集合是当前最可疑的放大因素之一。
- 仓库中的脚本、模块文档、runbook、smoke README 与部分维护脚本，当前仍大量把 `data/` 视为 repo 内默认路径。

## 2. 目标

- 产出并执行一条可审计、可回退、可验证的 `data` 外迁路径：
  - 将运行期数据根从 repo 内 `E:\Warden\data` 外迁到 repo 外 `E:\WardenData`；
  - 保持 `data` 根内部既有 `raw/`、`processed/` 等子结构语义不变；
  - 让当前活跃脚本与活跃文档改为使用显式数据根配置，而不再把 repo 内 `data/` 当作唯一默认位置；
  - 在不改样本 schema、不改标签语义、不改输出目录内部结构的前提下，降低工作区体积和桌面端后台扫描压力。

## 3. 范围

- 纳入：
  - 活跃脚本中的数据根解析与默认路径策略
  - 活跃模块文档 / runbook / smoke 文档中的数据根说明
  - 一次性迁移步骤、验证步骤与回退说明
  - 任务交付所需的 handoff
- 排除：
  - 历史 task / handoff 文档批量改写
  - 样本目录内部 JSON/PNG/TXT 内容修改
  - 冻结 sample schema、label schema、manifest core 字段语义修改
  - `channel/`、`outputs/`、`tranco csv/` 等非本任务明确纳入目录的外迁

## English Version

# Task Metadata

- Task ID: WARDEN-DATA-ROOT-EXTERNALIZATION-V1
- Task Title: Externalize Warden runtime data root from repo-local `E:\Warden\data` to external `E:\WardenData`
- Owner Role: Codex execution engineer
- Priority: High
- Status: TODO
- Related Module: Data module / repo portability / local operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_DATA.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`
- Created At: 2026-04-21
- Requested By: user

Use this template for any non-trivial engineering task in Warden.

Rules:

- Fill it before execution, not after.
- Replace every placeholder or explicitly write `none`, `not applicable`, or `missing`.
- If scope is unclear, stop and clarify before implementation.
- If the task is trivial enough to skip a formal task doc, say why in the thread explicitly.
- If the task will produce Markdown deliverables, define them as bilingual by default: Chinese summary first, full English version second, with English authoritative for exact facts and contract wording.

---

## 1. Background

The current Warden repo root at `E:\Warden` contains a large in-repo `data/` tree with substantial `raw/` and `processed/` contents.
This increases worktree size, background file watching cost, Git-status pressure, and desktop-tool indexing overhead.

Recent local Codex Desktop hangs on Windows were recorded as `Application Hang / MoAppHangXProc`.
The hang evidence does not prove that the in-repo `data/` tree is the sole root cause, but it is currently one of the most credible amplifiers because:

- the repo is large mainly due to `data/`,
- multiple active scripts and docs still assume repo-local `data/`,
- and current local tooling frequently scans workspace roots rather than only edited files.

The project therefore needs a controlled externalization path that moves the runtime data root out of the repo while preserving Warden's frozen sample structure, schema discipline, labeling discipline, and documented operational commands.

The default target external data root for this task is:

- `E:\WardenData`

If that target path changes before execution, this task doc must be updated explicitly before implementation starts.

---

## 2. Goal

Move Warden's runtime data root from repo-local `E:\Warden\data` to external `E:\WardenData` in a way that is explicit, auditable, minimally disruptive, and reversible.

The intended outcome is:

- active scripts no longer hardcode repo-local `./data` as the only default runtime data location;
- active docs describe the externalized data-root contract clearly;
- the repo root no longer needs to host the large working `data/` tree in its steady state;
- sample directory internal structure under the data root remains unchanged;
- frozen schema, labels, manifest semantics, and current capture output contracts remain untouched.

This task is complete only when the externalized layout is usable for current active workflows and the migration path is documented with validation and rollback notes.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/`
- `scripts/labeling/`
- `scripts/ci/`
- `tests/smoke/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`
- `.gitignore`

This task is allowed to change:

- active script data-root resolution logic
- active script CLI defaults or config defaults related to the runtime data root
- active module and runbook docs that currently describe repo-local `data/`
- migration instructions and rollback instructions
- repo-local ignore rules or lightweight placeholders needed after externalization

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not rewrite historical sample artifacts under `raw/` or `processed/`
- do not rename frozen sample fields, manifest fields, or label fields
- do not redesign capture logic, training logic, or inference policy
- do not bulk-rewrite old archived task docs or old archived handoff docs just to replace historical paths
- do not externalize `channel/`, `outputs/`, `assets/`, `tranco csv/`, or unrelated directories in the same task
- do not add third-party dependencies
- do not leave a permanent repo-root `data` junction / symlink as the final steady-state solution unless the task is explicitly revised to allow that

Examples:

- do not redesign the whole pipeline
- do not rename frozen fields
- do not add new dependencies
- do not modify training logic if this is a labeling task

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
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `tests/smoke/README.md`
- `tests/smoke/golden_manifest.example.json`
- `tranco csv/README.md`
- `STRUCTION.md`

### Code / Scripts

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/benign/run_benign_capture.py`
- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/data/malicious/ingest_public_malicious_feeds.py`
- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- any other active script under `scripts/data/` or `scripts/ci/` that still assumes repo-local `data/`

### Data / Artifacts

- current repo-local data root `E:\Warden\data`
- target external data root `E:\WardenData`
- current workspace evidence showing large repo size and desktop instability

### Prior Handoff

- `docs/handoff/2026-04-21_plan_a_batch_capture_day15_vm_prep.md`

### Missing Inputs

- a pre-approved exact rollback trigger threshold, if the migration validation is only partially successful

If any required input is missing, state that explicitly before execution.

---

## 6. Required Outputs

This task should produce:

- updated active scripts that resolve the runtime data root explicitly and support the external root
- updated active docs that describe the externalized data-root contract and operator usage
- a completed one-time migration from `E:\Warden\data` to `E:\WardenData`, or a clearly documented partial/block status if not completed
- a repo handoff document covering the migration result, validation, compatibility impact, and rollback notes

Be concrete.

Examples:

- updated Python script
- new CLI flag with backward compatibility
- markdown doc update
- conflict report JSON
- smoke-test summary
- repo handoff document

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

- The external target root for this task is `E:\WardenData`.
- Preserve the internal directory layout beneath the data root, including `raw/` and `processed/` semantics.
- Do not modify sample artifact contents just to support migration.
- Do not rewrite historical archived docs solely to normalize old path references.
- Active scripts must use explicit data-root resolution rather than hidden path guessing across multiple unrelated roots.
- The steady-state repo root should not continue to host the large working data tree.
- Do not overwrite or silently revert unrelated in-progress work already present in the dirty working tree.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- frozen sample directory structure and sample-file expectations documented in `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- Data-module manifest and consistency-check semantics documented in `docs/data/TRAINSET_V1.md` and `docs/modules/MODULE_DATA.md`
- current capture runner CLI surface except for explicitly approved data-root related compatibility additions

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/build_manifest.py --help`
  - `python scripts/data/check_dataset_consistency.py --help`
  - `python scripts/data/benign/run_benign_capture.py --help`
  - `python scripts/data/malicious/run_malicious_capture.py --help`
  - current active labeling backfill CLI help entrypoints

Downstream consumers to watch:

- operator runbooks and local capture workflows
- active smoke tests under `tests/smoke/`
- labeling and manifest utilities that currently default to repo-local `data/`

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Inventory active script and doc references that assume repo-local `data/`.
3. Define one explicit runtime data-root contract centered on `E:\WardenData`.
4. Make minimal code changes to support that contract.
5. Update active docs and operator commands.
6. Move the actual data root out of the repo.
7. Run the smallest meaningful validation against the externalized root.
8. Summarize compatibility impact and rollback notes.
9. Prepare handoff.

Task-specific execution notes:

- Historical docs may keep historical `E:\Warden\data\...` references when they record past facts rather than active instructions.
- Prefer a single explicit contract over many ad hoc path exceptions.
- If a temporary compatibility shim is needed during cutover, document it explicitly and remove it before declaring the task fully done, unless the task is revised.
- Current review already confirmed repo-local data-root/default-output assumptions in:
  - `scripts/data/build_manifest.py`
  - `scripts/data/check_dataset_consistency.py`
  - `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
  - `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
  - `scripts/data/malicious/ingest_public_malicious_feeds.py`
  - `tests/smoke/README.md`
  - `tranco csv/README.md`
  - `docs/modules/MODULE_DATA.md`
  - `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`

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

- [ ] active scripts no longer rely on repo-local `./data` as the only runtime default
- [ ] active docs explain the external root `E:\WardenData` clearly
- [ ] the large working data tree is no longer hosted under `E:\Warden\data` in steady state
- [ ] no sample artifact contents were rewritten
- [ ] frozen schema and label semantics remain unchanged
- [ ] rollback notes are documented
- [ ] the final approved target path name is explicitly consistent across user request, task doc, and implementation

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\build_manifest.py --help
python E:\Warden\scripts\data\check_dataset_consistency.py --help
python E:\Warden\scripts\data\benign\run_benign_capture.py --help
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\labeling\Warden_dataset_backfill_labels_brandlex.py --help
python E:\Warden\scripts\ci\check_schema_compat.py --kind sample_dir --path E:\WardenData\raw\benign\2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010\0x7c0.com_20260408T092757Z
python E:\Warden\scripts\data\build_manifest.py --data-root E:\WardenData --input-roots E:\WardenData\raw\phish E:\WardenData\raw\benign --out-dir E:\WardenData\processed\trainset_v1_externalization_smoke
python E:\Warden\scripts\data\check_dataset_consistency.py --data-root E:\WardenData --manifest E:\WardenData\processed\trainset_v1_externalization_smoke\manifest.jsonl --out-dir E:\WardenData\processed\trainset_v1_externalization_smoke\consistency_check
```

Expected evidence to capture:

- post-migration script help output
- successful explicit-root smoke manifest build and consistency check
- proof that at least one real sample path under `E:\WardenData` remains readable and schema-compatible
- evidence that the repo root no longer hosts the large runtime data tree in its steady state

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

- `docs/handoff/2026-04-21_warden_data_externalization.md`

---

## 13. Open Questions / Blocking Issues

- Should the final steady-state repo root keep an empty placeholder `data/` directory, or should `data/` disappear entirely from the repo root?
- If any active operator workflow still requires repo-local relative commands, should that workflow be updated now or explicitly deferred as doc debt?
- If `E:\WardenData` already exists with partial content, what exact merge policy should be applied before file move execution?
