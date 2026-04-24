<!-- operator: Codex; task: primary-benign-second-pass-review-manifest; date: 2026-04-24 -->

# 中文摘要

本任务把已冻结的 `primary benign candidates` 二筛策略落成可执行的 review manifest 生成流程。

执行边界：

- 只扫描候选 benign 样本并输出 routing / review suggestion。
- 不移动、不删除、不重写任何原始样本目录。
- 不把 `auto_labels.json` / `rule_labels.json` 等 weak labels 当作 manual gold labels。
- `adult` / `gambling` 按高风险内容样本处理。
- 真正的 `malicious` 仅指高危行为样本。
- `gate` / `evasion` 只按辅助数据路由。

本任务对应用户要求的五步：冻结边界、二筛剩余 primary benign candidates、做轻量一致性统计、给出用途桶建议、产出 train-ready 前置 review manifest。

---

# English Version

# Task Metadata

- Task ID: 2026-04-24_primary_benign_second_pass_review_manifest
- Task Title: Primary Benign Second-Pass Review Manifest
- Owner Role: Codex
- Priority: P1
- Status: DONE
- Related Module: Data / Labeling
- Related Issue / ADR / Doc:
  - `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
  - `docs/data/TRAINSET_V1.md`
  - `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
  - `docs/data/Warden_AUTO_LABEL_POLICY_V1.md`
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
- Created At: 2026-04-24
- Requested By: User

Use this task to execute the approved second-pass cleanup flow for remaining primary benign candidates.

---

## 1. Background

The first pass already separated obvious `adult`, `gambling`, `gate`, and `evasion` samples. The remaining benign-like pool still contains visible residues such as high-risk content, web3, download, clone, login, payment, gate, evasion, sparse, and screenshot-dependent hard cases.

The project now needs a repeatable review-manifest path that can triage this remaining pool without changing raw samples or promoting weak labels into manual gold labels.

---

## 2. Goal

Create and validate a bounded second-pass manifest builder that reads existing capture artifacts from primary benign candidate roots and emits review/routing suggestions for downstream cleaning, manual review, and train-main eligibility decisions.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/data/benign/`
- `docs/tasks/2026-04-24_primary_benign_second_pass_review_manifest.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_review_manifest.md`
- `E:\WardenData\reviewed\benign_second_pass\`

This task is allowed to change:

- Add a new read-only second-pass review manifest script.
- Add task and handoff documentation.
- Generate review manifest and summary artifacts under the active external data root.

---

## 4. Scope Out

This task must NOT do the following:

- Do not move, delete, rename, or rewrite raw sample directories.
- Do not modify `manual_labels.json`.
- Do not treat `auto_labels.json`, `rule_labels.json`, or model output as final truth.
- Do not redefine the malicious taxonomy.
- Do not change TrainSet V1 schema.
- Do not modify training, inference, or capture behavior.
- Do not run destructive deduplication.
- Do not add third-party dependencies.

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`

### Code / Scripts

- `scripts/data/common/runtime_data_root.py`
- `scripts/data/common/io_utils.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

### Data / Artifacts

- `E:\WardenData\raw\benign\benign`
- Optional operator-specified input roots via CLI.

### Prior Handoff

- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

### Missing Inputs

- No manual gold-label file is assumed to exist for the target samples.
- No full manual acceptance decision is expected from this task.

---

## 6. Required Outputs

This task should produce:

- A new second-pass review manifest builder script.
- A JSONL review manifest with per-sample routing suggestions.
- A JSON summary with aggregate counts and reason distributions.
- A repo handoff document.

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format of existing scripts.
- Do not add third-party dependencies.
- Prefer minimal patch over broad refactor.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial task.
- Weak labels are evidence only, not manual gold labels.
- `adult` / `gambling` are high-risk content samples.
- True `malicious` means high-risk behavior samples.
- `gate` / `evasion` route to auxiliary handling.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Existing `build_manifest.py` CLI.
- Existing `check_dataset_consistency.py` CLI.
- Existing capture artifact filenames.

Schema / field constraints:

- Schema changed allowed: No.
- If yes, required compatibility plan: not applicable.
- Frozen field names involved: existing capture artifact keys must not be renamed.

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/build_manifest.py`
  - `python scripts/data/check_dataset_consistency.py`

The new script may define a new review-manifest output structure because it is an additive artifact, but it must describe suggestions as non-final review routing.

---

## 9. Acceptance Criteria

- A new script can scan at least a limited sample slice from `E:\WardenData\raw\benign\benign`.
- The script emits JSONL records with per-sample route suggestion, manual-review flag, content-warning candidate, reason codes, and key evidence.
- The script emits an aggregate summary JSON.
- The script can be syntax-checked with `py_compile`.
- The handoff states validation honestly and does not claim final dataset admission.

---

## 10. Validation Checklist

- Run `python -m py_compile` on the new script.
- Run the script on a bounded sample slice before any larger run.
- Verify the output manifest is valid JSONL.
- Verify the summary file exists and contains counts.
- Report any skipped large-corpus validation explicitly.
