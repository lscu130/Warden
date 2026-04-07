# 2026-04-02 Reproduce PhishIntention Task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是交给 Codex 的**执行任务单**，目标是复现 **PhishIntention** 当前官方公开仓库的一条可运行基线。
- 本任务至少覆盖：**环境搭建、依赖安装、模型文件准备、最小命令行复现、结果留档**。
- 本任务默认按 **“先官方路径、后兼容兜底”** 执行：优先遵循官方 README / setup 脚本 / Dockerfile / pixi 配置，不要先发散重写。
- 本任务是 **baseline reproduction task**，不是 Warden 主线训练任务，也不是对 PhishIntention 方法学进行重构或增强。

## 1. 背景

PhishIntention 是公开的官方实现仓库，README 当前已经给出：

- 项目是 “Inferring Phishing Intention via Webpage Appearance and Dynamics: A Deep Vision-Based Approach” 的官方实现；
- 输入是网页截图，输出是 `Phish / Benign` 和目标品牌；
- 运行流程包括 Abstract Layout detector、Siamese logo comparison、CRP classifier、CRP locator；
- 官方当前提供 Docker 路线和非 Docker 路线；
- 非 Docker 路线默认使用 `pixi install`，再执行 `setup.sh` / `setup.bat`；
- `setup.sh` / `setup.bat` 会自动安装 PyTorch + Detectron2，并下载模型权重与 reference list；
- 命令行入口是 `pixi run python phishintention.py --folder <test folder> --output_fn <json>`；
- 测试目录最小结构为每个样本子目录包含 `info.txt` 与 `shot.png`，`html.txt` 可选。  

本任务的目标不是去改写 PhishIntention，而是把它**按当前官方实现先复现出来**，并形成 Warden 可审计、可交接的 baseline 记录。

## 2. 目标

在不干扰 Warden 主线冻结契约、不修改 Warden 现有 schema、不引入与本任务无关重构的前提下，完成 **PhishIntention 官方仓库的可审计复现**，至少包括：

1. 获取并固定 upstream 源；
2. 记录被复现的 upstream commit / branch / tag；
3. 按官方路径完成环境搭建；
4. 完成模型文件与 reference list 下载；
5. 运行最小命令行 smoke reproduction；
6. 记录实际命令、实际结果、实际问题与兜底策略；
7. 将复现结果组织成 Warden 可继续使用的 baseline 工件与 handoff。

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `environment/` (create if missing)
- `baselines/phishintention/` (create if missing)
- `scripts/reproduce/` (create if missing)
- repo-level markdown docs directly required by this task only

This task is allowed to do:

- clone or vendor the official PhishIntention repo into a clearly isolated baseline path
- add reproduction helper docs
- add environment setup artifacts
- add wrapper scripts strictly for reproduction convenience
- add notes for official-path vs fallback-path differences
- run minimal reproduction validation

## 4. Scope Out

This task must NOT do the following:

- do not modify Warden frozen sample schema
- do not modify Warden capture output file names
- do not change Warden label semantics
- do not integrate PhishIntention outputs into Warden main inference path
- do not re-train PhishIntention models
- do not replace official PhishIntention logic with a home-made reimplementation
- do not silently upgrade or refactor unrelated Warden modules
- do not fabricate successful reproduction if commands were not actually run
- do not claim paper-exact artifact reproduction unless exact evidence exists

## 5. Inputs

Relevant inputs for this task:

### Governing Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### External Upstream Source

- official repository: `https://github.com/lindsey98/PhishIntention`
- upstream README
- upstream `setup.sh`
- upstream `setup.bat`
- upstream `pixi.toml`
- upstream `Dockerfile`

### Optional Supporting Sources

- official paper PDF for pipeline understanding

### Missing Inputs Policy

If a required upstream file is unavailable, changed materially, or fails to download, state that explicitly and continue with the safest compatible interpretation instead of silently guessing.

## 6. Required Outputs

This task should produce all of the following:

- a repo-local baseline reproduction folder for PhishIntention
- a repo-local reproduction README or notes file
- an environment definition or setup note for the chosen path
- an explicit upstream version record (commit hash or equivalent)
- a recorded smoke reproduction result
- a handoff document

Concrete target outputs are expected to include something functionally equivalent to:

- `baselines/phishintention/README.md`
- `baselines/phishintention/UPSTREAM_VERSION.txt`
- `environment/phishintention_repro.md` or equivalent
- `scripts/reproduce/run_phishintention_smoke.*` (optional helper)
- `docs/handoff/<date>_reproduce_phishintention.md`

Names may vary slightly only if repository-local naming requires it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve Warden mainline boundaries.
- Keep this work isolated as an external-baseline reproduction.
- Prefer the official upstream route first.
- Record what actually happened.
- Prefer minimal, reversible, testable changes.
- Do not add unrelated dependencies to Warden runtime unless strictly required for this baseline reproduction.
- Do not pretend a fallback path is the official path.
- If fallback is used, label it clearly as fallback.

Task-specific hard constraints:

- Primary route: use the official PhishIntention setup path first.
- Official-path priority order:
  1. non-Docker pixi path
  2. Docker path if the host route is blocked and Docker is available
  3. manual fallback only if the official paths fail and the failure is documented
- Record the exact upstream commit that was reproduced.
- Keep external baseline artifacts isolated under a dedicated folder.
- If browser / chromedriver steps are required, document the exact version situation encountered.
- If GPU auto-detection is triggered by upstream scripts, record whether GPU or CPU path was actually selected.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Warden frozen sample contracts
- Warden existing CLI and output contracts
- Warden module boundaries

Schema / field constraints:

- Schema changed allowed: `NO` for Warden frozen schema
- Backward compatibility required: `YES`

Compatibility notes:

- This task may add new isolated baseline files and docs.
- This task must not silently change existing Warden outputs.
- If any wrapper script is added, it must be clearly baseline-only.

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing docs.
2. Inspect whether a baseline area already exists in the Warden repo.
3. Create the smallest isolated `baselines/phishintention/` structure if needed.
4. Clone the official upstream repo into the isolated baseline area or record an equivalent pinned external fetch path.
5. Record upstream commit / branch / tag.
6. Attempt the official non-Docker pixi setup path.
7. Run upstream `setup.sh` or `setup.bat` as appropriate.
8. Confirm model files and reference list are actually present.
9. Prepare the minimal test folder expected by upstream command-line interface.
10. Run the official smoke inference command.
11. If the official host path fails, document the failure and attempt Docker if available.
12. If Docker also fails or is unavailable, document a manual fallback path without pretending it is official.
13. Write reproduction notes and handoff.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Official upstream source is explicitly identified
- [ ] Upstream version is explicitly recorded
- [ ] Environment setup steps are documented
- [ ] Model file preparation is documented
- [ ] At least one smoke reproduction command was actually run, or failure was explicitly documented
- [ ] Validation claims are honest
- [ ] Risks / caveats are documented
- [ ] Handoff is provided

Task-specific acceptance checks:

- [ ] Official repo path used is `lindsey98/PhishIntention`
- [ ] The task records whether pixi route, Docker route, or manual fallback was used
- [ ] The task records whether GPU or CPU install path was actually selected by upstream installer
- [ ] The task records whether the following upstream assets were obtained:
  - `layout_detector.pth`
  - `crp_classifier.pth.tar`
  - `crp_locator.pth`
  - `ocr_pretrained.pth.tar`
  - `ocr_siamese.pth.tar`
  - `expand_targetlist.zip`
  - `domain_map.pkl`
- [ ] The task runs or explicitly fails the official CLI form:
  `pixi run python phishintention.py --folder <folder> --output_fn <json>`
- [ ] The test folder structure matches upstream expectation:
  `info.txt`, `shot.png`, optional `html.txt`

## 11. Validation Checklist

Minimum validation expected:

- [ ] clone / source retrieval sanity
- [ ] upstream version captured
- [ ] setup command actually executed
- [ ] key model files observed after setup
- [ ] smoke inference attempted on at least one valid sample folder
- [ ] output artifact or error trace captured

Commands to run if applicable:

```bash
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
pixi install
chmod +x setup.sh
./setup.sh
pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Windows-equivalent route if applicable:

```powershell
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
pixi install
.\setup.bat
pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Docker fallback if applicable:

```bash
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
docker build -t phishintention .
docker run --rm phishintention pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Expected evidence to capture:

- upstream commit hash
- actual setup command output
- actual model download evidence
- actual smoke-run output or failure trace
- produced `test.json` or equivalent output file if success

## 12. Handoff Requirements

This task must end with handoff coverage matching `HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- source and version reproduced
- environment path used
- actual commands run
- actual success / failure state
- files added under Warden repo
- compatibility impact on Warden mainline
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_reproduce_phishintention.md`

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- whether Codex host has Docker available
- whether Chrome / chromedriver path works on the target OS
- whether upstream auto-install logic still works unchanged on the current host
- whether paper-exact artifact reproduction is required later as a separate task

---

## English Version

> AI note: Codex and other models must treat the English section below as the authoritative version. The Chinese section above is for human readers and quick orientation.

# 2026-04-02 Reproduce PhishIntention Task

## 1. Background

PhishIntention is the official implementation of *Inferring Phishing Intention via Webpage Appearance and Dynamics: A Deep Vision-Based Approach*.
The current upstream README states that:

- the input is a webpage screenshot and the output is `Phish / Benign` plus target brand;
- the pipeline includes an Abstract Layout detector, Siamese logo comparison, CRP classifier, and CRP locator;
- both Docker and non-Docker setup routes are provided;
- the non-Docker route uses `pixi install` followed by `setup.sh` or `setup.bat`;
- the setup scripts automatically install PyTorch and Detectron2 and download the required model weights and reference list;
- the CLI entrypoint is `pixi run python phishintention.py --folder <folder> --output_fn <json>`;
- the minimal test folder structure is one subfolder per sample containing `info.txt` and `shot.png`, with optional `html.txt`.

The purpose of this task is not to redesign PhishIntention.
The purpose is to reproduce the current official implementation in an auditable way and preserve the result as a Warden baseline artifact.

## 2. Goal

Reproduce the current official PhishIntention repository as an auditable external baseline without disturbing Warden mainline contracts.
The task must at minimum cover:

1. upstream source acquisition and pinning;
2. environment setup;
3. model and reference-list preparation;
4. minimal CLI smoke reproduction;
5. explicit recording of what actually worked or failed;
6. a baseline handoff usable by later Warden work.

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- `environment/` (create if missing)
- `baselines/phishintention/` (create if missing)
- `scripts/reproduce/` (create if missing)
- repo-level markdown docs directly required by this task only

This task is allowed to do:

- clone or vendor the official PhishIntention repo into a clearly isolated baseline path
- add reproduction helper docs
- add environment setup artifacts
- add wrapper scripts strictly for reproduction convenience
- add notes for official-path vs fallback-path differences
- run minimal reproduction validation

## 4. Scope Out

This task must NOT:

- modify Warden frozen sample schema
- modify Warden capture output filenames
- change Warden label semantics
- integrate PhishIntention outputs into Warden main inference path
- retrain PhishIntention models
- replace official PhishIntention logic with a home-made reimplementation
- silently upgrade or refactor unrelated Warden modules
- fabricate successful reproduction if commands were not actually run
- claim paper-exact artifact reproduction unless exact evidence exists

## 5. Inputs

Relevant inputs for this task:

### Governing Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`

### External Upstream Source

- official repository: `https://github.com/lindsey98/PhishIntention`
- upstream README
- upstream `setup.sh`
- upstream `setup.bat`
- upstream `pixi.toml`
- upstream `Dockerfile`

### Optional Supporting Source

- official paper PDF for pipeline understanding

### Missing Inputs Policy

If a required upstream file is unavailable, changed materially, or fails to download, state that explicitly and continue with the safest compatible interpretation rather than silently guessing.

## 6. Required Outputs

This task should produce all of the following:

- a repo-local baseline reproduction folder for PhishIntention
- a repo-local reproduction README or notes file
- an environment definition or setup note for the chosen path
- an explicit upstream version record (commit hash or equivalent)
- a recorded smoke reproduction result
- a handoff document

Concrete target outputs are expected to include something functionally equivalent to:

- `baselines/phishintention/README.md`
- `baselines/phishintention/UPSTREAM_VERSION.txt`
- `environment/phishintention_repro.md` or equivalent
- `scripts/reproduce/run_phishintention_smoke.*` (optional helper)
- `docs/handoff/<date>_reproduce_phishintention.md`

Names may vary slightly only if repository-local naming requires it.

## 7. Hard Constraints

Must obey all of the following:

- Preserve Warden mainline boundaries.
- Keep this work isolated as an external-baseline reproduction.
- Prefer the official upstream route first.
- Record what actually happened.
- Prefer minimal, reversible, testable changes.
- Do not add unrelated dependencies to Warden runtime unless strictly required for this baseline reproduction.
- Do not pretend a fallback path is the official path.
- If fallback is used, label it clearly as fallback.

Task-specific hard constraints:

- Primary route: use the official PhishIntention setup path first.
- Official-path priority order:
  1. non-Docker pixi path
  2. Docker path if the host route is blocked and Docker is available
  3. manual fallback only if the official paths fail and the failure is documented
- Record the exact upstream commit that was reproduced.
- Keep external baseline artifacts isolated under a dedicated folder.
- If browser / chromedriver steps are required, document the exact version situation encountered.
- If GPU auto-detection is triggered by upstream scripts, record whether GPU or CPU path was actually selected.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- Warden frozen sample contracts
- Warden existing CLI and output contracts
- Warden module boundaries

Schema / field constraints:

- Schema changed allowed: `NO` for Warden frozen schema
- Backward compatibility required: `YES`

Compatibility notes:

- This task may add new isolated baseline files and docs.
- This task must not silently change existing Warden outputs.
- If any wrapper script is added, it must be clearly baseline-only.

## 9. Suggested Execution Plan

Recommended order:

1. Read the governing docs.
2. Inspect whether a baseline area already exists in the Warden repo.
3. Create the smallest isolated `baselines/phishintention/` structure if needed.
4. Clone the official upstream repo into the isolated baseline area or record an equivalent pinned external fetch path.
5. Record upstream commit / branch / tag.
6. Attempt the official non-Docker pixi setup path.
7. Run upstream `setup.sh` or `setup.bat` as appropriate.
8. Confirm model files and reference list are actually present.
9. Prepare the minimal test folder expected by the upstream CLI.
10. Run the official smoke inference command.
11. If the official host path fails, document the failure and attempt Docker if available.
12. If Docker also fails or is unavailable, document a manual fallback path without pretending it is official.
13. Write reproduction notes and handoff.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Official upstream source is explicitly identified
- [ ] Upstream version is explicitly recorded
- [ ] Environment setup steps are documented
- [ ] Model file preparation is documented
- [ ] At least one smoke reproduction command was actually run, or failure was explicitly documented
- [ ] Validation claims are honest
- [ ] Risks / caveats are documented
- [ ] Handoff is provided

Task-specific acceptance checks:

- [ ] Official repo path used is `lindsey98/PhishIntention`
- [ ] The task records whether the pixi route, Docker route, or manual fallback was used
- [ ] The task records whether the upstream installer selected GPU or CPU path
- [ ] The task records whether the following upstream assets were obtained:
  - `layout_detector.pth`
  - `crp_classifier.pth.tar`
  - `crp_locator.pth`
  - `ocr_pretrained.pth.tar`
  - `ocr_siamese.pth.tar`
  - `expand_targetlist.zip`
  - `domain_map.pkl`
- [ ] The task runs or explicitly fails the official CLI form:
  `pixi run python phishintention.py --folder <folder> --output_fn <json>`
- [ ] The test folder structure matches upstream expectation:
  `info.txt`, `shot.png`, optional `html.txt`

## 11. Validation Checklist

Minimum validation expected:

- [ ] clone / source retrieval sanity
- [ ] upstream version captured
- [ ] setup command actually executed
- [ ] key model files observed after setup
- [ ] smoke inference attempted on at least one valid sample folder
- [ ] output artifact or error trace captured

Commands to run if applicable:

```bash
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
pixi install
chmod +x setup.sh
./setup.sh
pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Windows-equivalent route if applicable:

```powershell
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
pixi install
.\setup.bat
pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Docker fallback if applicable:

```bash
git clone https://github.com/lindsey98/PhishIntention.git
cd PhishIntention
docker build -t phishintention .
docker run --rm phishintention pixi run python phishintention.py --folder datasets/test_sites --output_fn test.json
```

Expected evidence to capture:

- upstream commit hash
- actual setup command output
- actual model download evidence
- actual smoke-run output or failure trace
- produced `test.json` or equivalent output file if success

## 12. Handoff Requirements

This task must end with handoff coverage matching `HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- source and version reproduced
- environment path used
- actual commands run
- actual success / failure state
- files added under Warden repo
- compatibility impact on Warden mainline
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/<date>_reproduce_phishintention.md`

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- whether the Codex host has Docker available
- whether the Chrome / chromedriver path works on the target OS
- whether upstream auto-install logic still works unchanged on the current host
- whether paper-exact artifact reproduction is required later as a separate task
