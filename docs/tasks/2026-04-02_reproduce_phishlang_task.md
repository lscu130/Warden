# 2026-04-02 Reproduce PhishLang Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是交给 Codex 的**执行任务单**，用于复现上游公开项目 **PhishLang**。
- 本任务聚焦于：
  1. 官方仓库获取；
  2. 环境搭建；
  3. 数据准备核对；
  4. 训练 / 推理路径打通；
  5. 结果与阻塞项留档。
- 本任务**不是** Warden 训练任务，也**不是**把 PhishLang 接入 Warden 主线。
- 若上游仓库说明与实际代码不一致，Codex 必须显式记录差异，不得静默脑补。

## 1. 背景

PhishLang 是一个公开的轻量级反钓鱼项目，仓库说明其核心模型基于 MobileBERT，并同时提供了一个 Chromium-based client-side app / browser extension 方向。公开仓库 README 当前给出的核心复现路径包括：

- 安装 `src/requirements.txt` 中依赖；
- 在 `training_data/` 中将 `parsed_samples_part_*` 合并为单一文件；
- 运行 `python3 training.py full` 开始训练；
- 可选运行 `python3 training.py full chunk` 做 128-token chunked training；
- 可选运行 `patched_parser_prediction.py` 与 adversarial scripts；
- 另有 `.deb` client-side service 与 Chromium 扩展安装路径，标明测试于 Ubuntu 22.04 / 24.04。

同时，源码显示训练脚本直接使用 `google/mobilebert-uncased` 作为基础模型，并默认读取 `phish_samples/` 与 `benign_samples/` 两类文本样本目录，训练完成后将模型保存到 `./model`。因此本任务的关键不是“只 clone 下仓库”，而是要把：

1. 环境；
2. 数据拼接 / 落盘逻辑；
3. 训练入口；
4. 推理入口；
5. 结果证据；

这一整条链路至少跑到 smoke-repro 级别。

## 2. 目标

在不修改上游方法定义、不将其改写成 Warden 版本、不引入额外训练目标的前提下，完成一轮 **PhishLang 官方仓库 baseline reproduction**，至少包括：

- 官方仓库获取与版本记录；
- 可复现环境搭建；
- 数据准备路径核实；
- 官方训练脚本或其最小等价入口跑通；
- 官方推理脚本或最小 smoke inference 跑通；
- 对 client-side app / extension 路径是否可行给出明确结论；
- 形成 handoff。

## 3. Scope In

This task is allowed to touch:

- repro workspace outside the main Warden production path
- `docs/tasks/`
- `docs/handoff/`
- external baseline repro directory if maintained in the repo, e.g.:
  - `external_baselines/phishlang/`
  - `third_party/phishlang/`
  - equivalent repo-local repro directory
- environment files strictly required for this task
- wrapper scripts strictly required for running the upstream baseline
- notes / README / handoff files strictly required for this task

This task is allowed to do:

- clone the upstream PhishLang repository
- create an isolated environment for PhishLang
- inspect and document upstream code / README mismatches
- add minimal wrapper scripts for reproducible execution
- create small helper scripts for data assembly if the upstream README is underspecified
- produce smoke training / inference evidence
- document blockers precisely

## 4. Scope Out

This task must NOT do the following:

- do not modify Warden frozen dataset schema
- do not integrate PhishLang into Warden training or inference
- do not redesign the upstream model architecture
- do not silently replace MobileBERT with another model
- do not convert the task into a paper-style reimplementation from scratch
- do not add unapproved benchmark claims
- do not mix PhishLang reproduction with Phishpedia / PhishIntention tasks
- do not change unrelated Warden modules for cleanup

## 5. Inputs

Relevant inputs for this task:

### Governing Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Upstream Public Sources

- official public repository: `UTA-SPRLab/phishlang`
- upstream README and source files under `src/`
- paper / abstract page if needed for method naming consistency

### Missing Inputs

- if upstream training data is incomplete or ambiguous, Codex must record that explicitly
- if client-side `.deb` assets or extension artifacts are not runnable on the current host, Codex must state that explicitly rather than pretending full extension reproduction succeeded

## 6. Required Outputs

This task should produce:

- a reproducible PhishLang environment setup record
- a pinned upstream commit hash / branch record
- a step-by-step reproduction note
- a log of how training data parts were assembled and used
- at least one of the following:
  - successful smoke training run
  - successful smoke inference run using upstream saved model or newly trained model
- explicit evidence for anything not run
- a non-trivial handoff document

Concrete expected artifacts may include something functionally equivalent to:

- `external_baselines/phishlang/README_repro.md`
- `external_baselines/phishlang/run_train.sh` or `.bat`
- `external_baselines/phishlang/run_predict.sh` or `.bat`
- `external_baselines/phishlang/env/requirements_locked.txt`
- `docs/handoff/<date>_phishlang_repro_v1.md`

Names may vary if repo-local conventions require it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve Warden mainline contracts.
- Keep PhishLang isolated as an external baseline reproduction.
- Prefer upstream-faithful execution over local reinvention.
- Prefer minimal wrappers over deep source edits.
- Record upstream commit hash.
- Record exact environment creation steps.
- Record exact commands actually run.
- If validation was not run, say so explicitly.
- If README and code diverge, record the divergence.

Task-specific constraints:

- Reproduction priority order:
  1. upstream core model training / inference path under `src/`
  2. upstream client-side app / extension path only if host platform makes it feasible
- The default target is **core model reproduction first**, not browser packaging first.
- `google/mobilebert-uncased` must remain the default backbone unless upstream code itself is changed and that change is explicitly justified and documented.
- Do not claim “full reproduction complete” if only environment creation succeeded.
- Do not claim “browser extension reproduced” unless the service and extension were actually installed and functionally verified.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Warden frozen dataset contracts
- Warden capture outputs
- Warden TrainSet V1 semantics

Schema / field constraints:

- Schema changed allowed: `NO` for Warden frozen contracts
- Compatibility plan: `N/A`

External baseline isolation constraints:

- Any PhishLang-specific sample layout, training files, checkpoints, or prediction CSVs must stay inside the external baseline repro area.
- No PhishLang-specific assumptions should leak into Warden data loaders or Warden runtime.

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs.
2. Clone the official upstream repository into an isolated repro area.
3. Record branch, commit hash, and repo status.
4. Inspect upstream README, `src/requirements.txt`, `src/training.py`, and `src/patched_parser_prediction.py`.
5. Build the runtime environment exactly or as close as possible to upstream.
6. Inspect `training_data/` and determine how `parsed_samples_part_*` must be assembled.
7. Validate whether the assembled data is sufficient for training.
8. Run the smallest meaningful training reproduction.
9. Run the smallest meaningful prediction / inference reproduction.
10. Optionally inspect the `.deb` client-side path if host OS makes it realistic.
11. Write handoff.

Task-specific notes:

- If the current host is not Ubuntu, client-side `.deb` installation should be treated as optional / likely blocked rather than forcing a fake completion.
- If training the full upstream dataset is too heavy for the current host or time budget, a bounded smoke-training path is acceptable, but it must be labeled as smoke reproduction rather than full-result reproduction.
- If the upstream training data is insufficiently documented, add a small helper note or wrapper, not a hidden data rewrite.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met to the stated reproduction level
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No Warden schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks and blockers are documented
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for this non-trivial change

Task-specific acceptance checks:

- [ ] Upstream repo URL and commit hash are recorded
- [ ] Environment creation steps are recorded
- [ ] `src/requirements.txt` was actually inspected and used or consciously adapted with explanation
- [ ] `src/training.py` was actually inspected and its assumptions were documented
- [ ] Data assembly from `training_data/parsed_samples_part_*` was either completed or explicitly blocked with evidence
- [ ] At least one meaningful execution path was run:
  - training smoke run, or
  - inference smoke run
- [ ] If client-side app / extension was not reproduced, the reason is stated explicitly
- [ ] Handoff clearly distinguishes “full reproduction”, “partial reproduction”, and “blocked attempt”

## 11. Validation Checklist

Minimum validation expected:

- [ ] clone success and commit hash capture
- [ ] environment import sanity
- [ ] upstream dependency install evidence
- [ ] training data assembly evidence
- [ ] one actual command run for training or prediction
- [ ] output artifact spot-check

Representative commands to run if applicable:

```bash
cd <PHISHLANG_REPO>/src
python -m pip install -r requirements.txt
python training.py full
python training.py test
python patched_parser_prediction.py
```

If bounded smoke runs are needed, document exactly how and why they differ from full upstream expectations.

Expected evidence to capture:

- environment creation log
- pip install output summary
- commit hash
- data assembly command transcript
- training / inference stdout snippets
- saved model path or prediction CSV path

## 12. Handoff Requirements

This task must end with handoff coverage matching `HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- upstream repo and commit pinned
- files touched
- reproduction level achieved
- behavior impact on Warden mainline (should be none)
- validation performed
- blockers / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_phishlang_repro_v1.md`

## 13. Open Questions / Known Risks

List unresolved items before execution if they exist:

- whether `training_data/parsed_samples_part_*` is complete and directly usable as-is
- whether upstream training on the full dataset is feasible on the current machine
- whether `patched_parser_prediction.py` expects a pre-existing `./model` directory from a completed train
- whether the client-side `.deb` path can realistically be validated on the current host

---

## English Version

> AI note: Codex and other models must treat the English section below as the authoritative version. The Chinese section above is for human readers and quick orientation.

# 2026-04-02 Reproduce PhishLang Task

## 1. Background

PhishLang is a public lightweight anti-phishing project whose repository describes a MobileBERT-based core model and a Chromium-oriented client-side deployment path.
The current upstream README describes the following main actions:

- install dependencies from `src/requirements.txt`
- combine `training_data/parsed_samples_part_*` into a single file
- run `python3 training.py full`
- optionally run `python3 training.py full chunk`
- optionally run `patched_parser_prediction.py` and adversarial scripts
- optionally install a `.deb` client-side service and Chromium extension on Ubuntu 22.04 / 24.04

The upstream code also shows that the training script directly uses `google/mobilebert-uncased`, reads samples from `phish_samples/` and `benign_samples/`, and saves the trained model to `./model`.
Therefore, this task is not just a clone task. It is a bounded baseline-reproduction task covering environment, data preparation, training or inference execution, and evidence capture.

## 2. Goal

Reproduce the public PhishLang baseline in a bounded but real way, without rewriting it into a Warden-native method and without silently changing the upstream method definition.
The task must cover at least:

- upstream repo acquisition and version pinning
- reproducible environment setup
- training-data preparation clarification
- upstream training-path or closest faithful equivalent
- upstream prediction-path or closest faithful equivalent
- explicit statement on whether the client-side app / extension path was actually reproduced
- non-trivial handoff

## 3. Scope In

This task is allowed to touch:

- repro workspace outside the main Warden production path
- `docs/tasks/`
- `docs/handoff/`
- external baseline repro directory if maintained in the repo, such as:
  - `external_baselines/phishlang/`
  - `third_party/phishlang/`
  - equivalent repo-local repro directory
- environment files strictly required for this task
- wrapper scripts strictly required for reproducible execution
- notes / README / handoff files strictly required for this task

This task is allowed to do:

- clone the upstream PhishLang repository
- create an isolated environment for PhishLang
- inspect and document upstream code / README mismatches
- add minimal wrapper scripts for reproducible execution
- create small helper scripts for data assembly if the upstream README is underspecified
- produce smoke training / inference evidence
- document blockers precisely

## 4. Scope Out

This task must NOT:

- modify Warden frozen dataset schema
- integrate PhishLang into Warden training or inference
- redesign the upstream model architecture
- silently replace MobileBERT with another backbone
- convert the task into a from-scratch reimplementation
- add unapproved benchmark claims
- mix this task with Phishpedia / PhishIntention tasks
- touch unrelated Warden modules for cleanup

## 5. Inputs

Relevant inputs for this task:

### Governing Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### Upstream Public Sources

- official public repository: `UTA-SPRLab/phishlang`
- upstream README and source files under `src/`
- paper / abstract page if needed for naming consistency

### Missing Inputs

- if upstream training data is incomplete or ambiguous, record that explicitly
- if client-side `.deb` assets or extension artifacts are not runnable on the current host, state that explicitly rather than pretending full extension reproduction succeeded

## 6. Required Outputs

This task should produce:

- a reproducible PhishLang environment setup record
- a pinned upstream commit hash / branch record
- a step-by-step reproduction note
- a log of how training data parts were assembled and used
- at least one of the following:
  - successful smoke training run
  - successful smoke inference run using an upstream saved model or a newly trained model
- explicit evidence for anything not run
- a non-trivial handoff document

Concrete expected artifacts may include something functionally equivalent to:

- `external_baselines/phishlang/README_repro.md`
- `external_baselines/phishlang/run_train.sh` or `.bat`
- `external_baselines/phishlang/run_predict.sh` or `.bat`
- `external_baselines/phishlang/env/requirements_locked.txt`
- `docs/handoff/<date>_phishlang_repro_v1.md`

Names may vary if repo-local conventions require it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve Warden mainline contracts.
- Keep PhishLang isolated as an external baseline reproduction.
- Prefer upstream-faithful execution over local reinvention.
- Prefer minimal wrappers over deep source edits.
- Record upstream commit hash.
- Record exact environment creation steps.
- Record exact commands actually run.
- If validation was not run, say so explicitly.
- If README and code diverge, record the divergence.

Task-specific constraints:

- Reproduction priority order:
  1. upstream core model training / inference path under `src/`
  2. upstream client-side app / extension path only if the host platform makes it feasible
- The default target is core model reproduction first, not browser packaging first.
- `google/mobilebert-uncased` must remain the default backbone unless the upstream code itself is changed and that change is explicitly justified and documented.
- Do not claim “full reproduction complete” if only environment creation succeeded.
- Do not claim “browser extension reproduced” unless the service and extension were actually installed and functionally verified.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Warden frozen dataset contracts
- Warden capture outputs
- Warden TrainSet V1 semantics

Schema / field constraints:

- Schema changed allowed: `NO` for Warden frozen contracts
- Compatibility plan: `N/A`

External baseline isolation constraints:

- Any PhishLang-specific sample layout, training files, checkpoints, or prediction CSVs must stay inside the external baseline repro area.
- No PhishLang-specific assumptions should leak into Warden data loaders or Warden runtime.

## 9. Suggested Execution Plan

Recommended order:

1. Read governing docs.
2. Clone the official upstream repository into an isolated repro area.
3. Record branch, commit hash, and repo status.
4. Inspect upstream README, `src/requirements.txt`, `src/training.py`, and `src/patched_parser_prediction.py`.
5. Build the runtime environment exactly or as close as possible to upstream.
6. Inspect `training_data/` and determine how `parsed_samples_part_*` must be assembled.
7. Validate whether the assembled data is sufficient for training.
8. Run the smallest meaningful training reproduction.
9. Run the smallest meaningful prediction / inference reproduction.
10. Optionally inspect the `.deb` client-side path if the host OS makes it realistic.
11. Write handoff.

Task-specific notes:

- If the current host is not Ubuntu, client-side `.deb` installation should be treated as optional / likely blocked rather than forcing a fake completion.
- If training the full upstream dataset is too heavy for the current host or time budget, a bounded smoke-training path is acceptable, but it must be labeled as smoke reproduction rather than full-result reproduction.
- If the upstream training data is insufficiently documented, add a small helper note or wrapper, not a hidden data rewrite.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met to the stated reproduction level
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No Warden schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks and blockers are documented
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for this non-trivial change

Task-specific acceptance checks:

- [ ] Upstream repo URL and commit hash are recorded
- [ ] Environment creation steps are recorded
- [ ] `src/requirements.txt` was actually inspected and used or consciously adapted with explanation
- [ ] `src/training.py` was actually inspected and its assumptions were documented
- [ ] Data assembly from `training_data/parsed_samples_part_*` was either completed or explicitly blocked with evidence
- [ ] At least one meaningful execution path was run:
  - training smoke run, or
  - inference smoke run
- [ ] If client-side app / extension was not reproduced, the reason is stated explicitly
- [ ] Handoff clearly distinguishes “full reproduction”, “partial reproduction”, and “blocked attempt”

## 11. Validation Checklist

Minimum validation expected:

- [ ] clone success and commit hash capture
- [ ] environment import sanity
- [ ] upstream dependency install evidence
- [ ] training data assembly evidence
- [ ] one actual command run for training or prediction
- [ ] output artifact spot-check

Representative commands to run if applicable:

```bash
cd <PHISHLANG_REPO>/src
python -m pip install -r requirements.txt
python training.py full
python training.py test
python patched_parser_prediction.py
```

If bounded smoke runs are needed, document exactly how and why they differ from full upstream expectations.

Expected evidence to capture:

- environment creation log
- pip install output summary
- commit hash
- data assembly command transcript
- training / inference stdout snippets
- saved model path or prediction CSV path

## 12. Handoff Requirements

This task must end with handoff coverage matching `HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- upstream repo and commit pinned
- files touched
- reproduction level achieved
- behavior impact on Warden mainline (should be none)
- validation performed
- blockers / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_phishlang_repro_v1.md`

## 13. Open Questions / Known Risks

List unresolved items before execution if they exist:

- whether `training_data/parsed_samples_part_*` is complete and directly usable as-is
- whether upstream training on the full dataset is feasible on the current machine
- whether `patched_parser_prediction.py` expects a pre-existing `./model` directory from a completed train
- whether the client-side `.deb` path can realistically be validated on the current host
