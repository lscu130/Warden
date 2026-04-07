# 2026-03-31 Reproduce Phishpedia Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 Warden 内部正式采用的 Phishpedia baseline 复现任务单。
- 本任务属于 non-trivial task，必须遵守 `AGENTS.md`、`docs/workflow/GPT_CODEX_WORKFLOW.md`、`docs/templates/TASK_TEMPLATE.md`、`docs/templates/HANDOFF_TEMPLATE.md`。
- 中文是压缩摘要。英文版为权威执行版本。

## English Version

> AI note: Codex and other models must treat the English section below as the authoritative version. The Chinese section above is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-2026-03-31-PHISHPEDIA-REPRO
- Task Title: Reproduce Official Phishpedia Baseline On The Local Host
- Owner Role: Codex execution engineer
- Priority: High
- Status: BLOCKED
- Related Module: Paper / experiment support, external baseline reproduction
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`
- Created At: 2026-03-31
- Requested By: Human owner

Use this template-backed task for the bounded reproduction of the official Phishpedia baseline.

---

## 1. Background

The user wants one controlled reproduction of the official public Phishpedia baseline on this physical Windows host so that later comparisons, engineering tradeoff analysis, and error analysis can refer to a runnable external baseline rather than to paper-only claims.

This task is not to merge Phishpedia into Warden mainline, not to rewrite its algorithm, and not to claim full paper-level benchmark reproduction.

The upstream facts that anchor this task are:

- the official repository is `https://github.com/lindsey98/Phishpedia`;
- the current README requires `Pixi`;
- the Windows route is `pixi install` then `setup.bat`;
- the command-line entry point is `pixi run python phishpedia.py --folder <test folder>`;
- the test folder contract is one subfolder per sample containing `info.txt` and `shot.png`;
- the documented `models/` layout includes `rcnn_bet365.pth`, `faster_rcnn.yaml`, `resnetv2_rgb_new.pth.tar`, `expand_targetlist/`, and `domain_map.pkl`;
- `setup.bat` installs detectron2 and downloads the model files using `gdown`.

---

## 2. Goal

Produce one auditable, bounded, and documented local reproduction attempt of the official Phishpedia command-line baseline on this machine, preserving Warden frozen schema and interfaces, preserving Warden mainline boundaries, and either:

- running at least one real `phishpedia.py --folder ...` command successfully; or
- documenting the exact blocking failure after actually attempting the official path.

Minimum success conditions:

1. create or prepare an isolated user-scoped environment path for the upstream toolchain;
2. obtain and pin the actual upstream code revision used;
3. attempt the official Pixi route first;
4. attempt model setup and record required-file presence or exact failure;
5. execute at least one real command-line inference or preserve the blocking failure;
6. record environment facts, commands run, outputs, risks, and handoff.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-03-31_reproduce_phishpedia_task.md`
- `docs/baselines/`
- `docs/handoff/`
- `environment/`
- `scripts/repro/phishpedia/`
- `outputs/repro/phishpedia/`
- `third_party/Phishpedia/`

This task is allowed to change:

- repo-local documentation for this external baseline reproduction;
- a dedicated PowerShell wrapper or helper script for this external baseline reproduction;
- repo-local environment notes and reproducibility records;
- external baseline checkout and its user-scoped setup under `third_party/`.

---

## 4. Scope Out

This task must NOT do the following:

- modify Warden frozen schema, labels, CLI, or training-set contracts;
- integrate Phishpedia into Warden mainline runtime;
- modify Warden training, inference, capture, data, or labeling modules unless only for documentation paths;
- rewrite the Phishpedia algorithm;
- turn compatibility workarounds into a broad fork;
- silently upgrade shared Warden dependencies;
- claim reproduction success if the run did not actually complete;
- treat unrun validation as passed validation;
- turn this task into full benchmark reproduction.

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Code / Scripts

- official upstream `README.md`
- official upstream `pixi.toml`
- official upstream `setup.bat`
- official upstream `phishpedia.py`

### Data / Artifacts

- one upstream sample directory if available;
- otherwise one repo-local smoke sample directory satisfying the upstream input contract;
- repo-local logs and output artifacts under `outputs/repro/phishpedia/`.

### Prior Handoff

- none

### Missing Inputs

- whether external network access, Pixi installation, detectron2 build, and Google Drive downloads will work on this host remains to be validated by actual execution.

---

## 6. Required Outputs

This task should produce:

- `docs/baselines/PHISHPEDIA_REPRO_V1.md`
- `environment/phishpedia_repro_environment.md`
- `scripts/repro/phishpedia/run_phishpedia_repro.ps1`
- one reproducibility record under `outputs/repro/phishpedia/<run_id>/`
- one handoff under `docs/handoff/2026-04-01_phishpedia_repro_v1.md`

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies to Warden without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for this non-trivial task.

Task-specific constraints:

- Use the official upstream reproduction path first.
- Try the official Pixi route before any fallback.
- Record the actual upstream commit hash used.
- Record actual OS, PowerShell, Python, Git, Pixi, Torch, Detectron2, and proxy-related facts when available.
- State explicitly whether CPU or GPU was used.
- If a local workaround is required, keep it minimal and label it clearly as local-only.
- Do not claim paper-level reproduction unless those experiments were actually run.
- Markdown deliverables must be bilingual, Chinese-summary-first and full-English-second, with English authoritative.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- all existing Warden CLI entry points
- all frozen Warden schema fields
- all current Warden module boundaries

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - all current Warden commands
  - all current Warden scripts under `scripts/train/`, `scripts/infer/`, and data tooling
  - the new wrapper must not masquerade as a Warden main entry point

Downstream consumers to watch:

- any later Warden baseline comparison workflow
- any later Warden experiment-support docs that refer to this reproduction

---

## 9. Suggested Execution Plan

Recommended order:

1. Read relevant docs and target files.
2. Freeze repo-local task and artifact paths.
3. Attempt upstream retrieval with process-local proxy correction.
4. Pin and record the actual upstream commit.
5. Attempt Pixi preparation using user-scoped or portable installation.
6. Attempt official setup and only use the PowerShell unzip workaround if the official path is blocked by missing `unzip`.
7. Prepare one smoke sample folder matching the upstream input contract.
8. Run one real `pixi run python phishpedia.py --folder ...` command.
9. Save logs, environment notes, outputs, and exact failure points if blocked.
10. Write final guide and handoff.

Task-specific execution notes:

- External network and setup actions should be performed in explicitly separated permission phases.
- `ALL_PROXY` should be corrected per-process to the same proxy as `HTTP_PROXY` and `HTTPS_PROXY` during external steps.
- If `git clone` remains blocked, use a pinned GitHub archive fallback and record the exact failure point.

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
- [ ] Handoff is provided

Task-specific acceptance checks:

- [ ] the official upstream source and commit hash are pinned
- [ ] the actual environment summary is recorded
- [ ] the official Pixi path was attempted
- [ ] model-file presence or explicit missing-file state is recorded
- [ ] at least one real `phishpedia.py --folder ...` command was executed or its exact blocking failure was preserved
- [ ] output result files or failure logs were preserved

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity where applicable
- [ ] `pixi --version`
- [ ] `pixi install`
- [ ] actual execution of `setup.bat` or the documented local unzip workaround path
- [ ] required-files spot-check under `models/`
- [ ] at least one command-line inference execution
- [ ] stdout / stderr summary capture

Commands to run if applicable:

```powershell
git clone https://github.com/lindsey98/Phishpedia.git third_party/Phishpedia
git -C third_party/Phishpedia rev-parse HEAD
pixi --version
pixi install
.\setup.bat
pixi run python phishpedia.py --folder <SMOKE_SAMPLE_DIR>
```

Expected evidence to capture:

- upstream commit hash and retrieval method
- output artifact path and command logs

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

- `docs/handoff/2026-04-01_phishpedia_repro_v1.md`

---

## 13. Open Questions / Blocking Issues

- whether user-scoped or portable Pixi installation will succeed on this host
- whether detectron2 can be built successfully on this host
- whether Google Drive model downloads succeed on this host
- whether the official setup is blocked only by missing `unzip` or by deeper Windows/toolchain incompatibilities
