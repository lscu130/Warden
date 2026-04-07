# 2026-03-24_plan_a_batch_capture_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档按“中文在前，英文在后”整理。
- 若涉及精确脚本路径、实际 CLI、输出目录、验证结果或兼容性结论，以英文版为准。
- 本任务单用于把既定的 **方案 A** 落地成一个 **Codex 当前即可执行** 的工程任务。
- 本任务单**不要求 Codex 假装完成未来 10 天的异步工作**；它要求 Codex 完成：
  1. 读取本地仓库与现有批次产物；
  2. 冻结并写清 Day 1 执行路径；
  3. 在本地环境允许的前提下执行 Day 1；
  4. 产出 Day 2–Day 10 的明确队列与交接信息。

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-V1
- Task Title: Execute Plan A Day 1 batch capture for current PhishTank and Tranco local batches, and prepare the remaining day-wise operator queue
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`; `docs/handoff/2026-03-23_data_ingest_pipeline.md`; `docs/tasks/2026-03-23_tranco_batch_split.md`; `docs/handoff/2026-03-23_tranco_batch_split.md`; `docs/tasks/2026-03-23_phishtank_batch_split.md`; `docs/handoff/2026-03-23_phishtank_batch_split.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. 背景

Warden 当前已经具备：

1. 本地 PhishTank malicious 批次产物，按 500 行切分，共 32 批；
2. 本地 Tranco benign 批次产物，按策略对齐后按 1000 行切分，共 20 批；
3. 已落地的数据摄取主线与 capture 编排路径；
4. 现有治理文件要求非 trivial 工作必须走 task + handoff，并且不能把未执行的未来工作写成已完成。

当前决策不是“是否分批”，而是已经明确采用 **方案 A**：

- malicious：每天 4 批；
- benign：每天 2 批；
- PhishTank 从 `batch_0001` 开始；
- Tranco 不按单一 rank bucket 连续扫完，而是优先跨 bucket 启动；
- 每个 batch 必须单独 output root，保证 lineage / review / retry 可审计。

本任务的核心不是大改代码，而是把方案 A 变成可执行的操作任务，并在本地环境允许时把 **Day 1** 真正跑起来。

---

## 2. 目标

完成以下四件事：

1. 基于本地仓库实际脚本与本地产物，确认方案 A 对应的真实执行入口，不发明不存在的脚本名或 CLI；
2. 落地 Day 1 执行：
   - malicious：执行 `batch_0001` ~ `batch_0004`；
   - benign：执行 2 个来自不同 rank bucket 的 Tranco batch；
3. 为每个 batch 使用独立 output root，并记录 batch → output root → result 的映射；
4. 产出一个 handoff，明确：
   - Day 1 实际运行了什么；
   - 哪些成功、失败、跳过；
   - Day 2–Day 10 的剩余批次队列；
   - 下一轮操作员继续执行时应从哪里接着跑。

本任务默认只要求完成 **Day 1 + 剩余天数排队信息**，不要求 Codex 在同一轮里假装完成未来多天的抓取。

---

## 3. Scope In

本任务允许触碰：

- `docs/tasks/`
- `docs/handoff/`
- 当前 benign / malicious batch 目录下的本地 README 或操作说明文档
- 当前 capture / ingest 入口相关脚本（仅当需要最小修复以支持 Day 1 执行时）
- Day 1 运行产生的 output roots、summary、review artifact

本任务允许修改或新增：

- 一份正式 task 文档（若 repo 中需落库）
- 一份正式 handoff 文档
- 一份 Day 1 运行摘要或 operator note
- 仅限支持 Day 1 正常执行所需的**最小补丁**

---

## 4. Scope Out

本任务不得：

- 假装完成 Day 2–Day 10 的异步抓取
- 大改已有 data ingest / capture pipeline
- 重命名冻结字段、冻结文件名、冻结目录契约
- 引入新第三方依赖
- 修改训练逻辑、推理逻辑或标签语义
- 为了“计划更漂亮”而重排既有 split 产物的文件名或顺序
- 将 benign 20 批或 malicious 32 批在本轮一次性全跑完

---

## 5. 输入

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`
- `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- `docs/tasks/2026-03-23_tranco_batch_split.md`
- `docs/handoff/2026-03-23_tranco_batch_split.md`
- `docs/tasks/2026-03-23_phishtank_batch_split.md`
- `docs/handoff/2026-03-23_phishtank_batch_split.md`

### Code / Scripts

- 当前本地仓库中的 benign ingest 入口
- 当前本地仓库中的 malicious ingest 入口
- 当前本地仓库中的 capture 入口
- 任何与 batch input、output root、resume/retry、review manifest 相关的 helper 脚本

### Data / Artifacts

- 本地 PhishTank 32 个 batch CSV/TXT 产物
- 本地 Tranco 20 个 batch CSV/TXT 产物
- 现有 output root 根目录
- 现有 summary / review artifact 根目录（若已存在）

### Prior Handoff

- `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- `docs/handoff/2026-03-23_tranco_batch_split.md`
- `docs/handoff/2026-03-23_phishtank_batch_split.md`

### Missing Inputs

- 当前 benign / malicious 实际 runner 文件名与 CLI 参数，必须通过阅读本地仓库确认；不得猜测
- 若本地环境缺少运行所需代理、浏览器依赖、账号状态或权限，必须在 handoff 中写明，不得伪装为脚本成功

---

## 6. 必须产出

本任务应产出：

1. 一份正式 task 文档（若当前文件尚未落库，则将其落入 repo）
2. 一份 Day 1 正式 handoff 文档
3. Day 1 批次执行记录，至少覆盖：
   - batch id
   - source type（benign / malicious）
   - input artifact path
   - output root
   - status（success / partial / failed / skipped）
   - short note
4. Day 2–Day 10 剩余批次队列清单
5. 如发生失败：明确的 retry / stop / continue 建议
6. 若为 Day 1 执行做了最小代码修复：对应最小 patch 与兼容性说明

---

## 7. Hard Constraints

必须遵守以下约束：

- 保持向后兼容，除非明确做不到，并在交付中说明
- 不重命名冻结 schema 字段或冻结 top-level 文件名
- 不静默改变 output format
- 不新增第三方依赖
- 优先最小补丁，不做机会主义重构
- 若行为变化，必须更新相关 docs
- 遵循 `AGENTS.md`
- 遵循 `docs/workflow/GPT_CODEX_WORKFLOW.md`
- 以本地仓库真实状态为准，不凭 GitHub 旧快照做判断
- 不得把未运行的 Day 2–Day 10 写成已完成

任务特定约束：

- malicious Day 1 固定为 `batch_0001` ~ `batch_0004`
- benign Day 1 固定为 **2 个来自不同 rank bucket 的 batch**，不得都来自同一 bucket
- 每个 batch 必须独立 output root
- 任何失败或中断必须保留 lineage，不得覆盖旧产物
- 若 Day 1 中途暴露系统性故障，应停止继续放量，并在 handoff 中明确说明停止点与原因

---

## 8. Interface / Schema Constraints

必须保持稳定的公共接口：

- 当前 benign ingest CLI（若存在）
- 当前 malicious ingest CLI（若存在）
- 当前 capture entrypoint CLI（若存在）
- 当前成功样本目录语义
- 当前 batch artifact 文件名与目录语义

Schema / field constraints：

- Schema changed allowed: NO（除非仅新增向后兼容的运行摘要字段或 sidecar artifact）
- If yes, required compatibility plan: not applicable by default
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints：

- Existing commands that must keep working:
  - 当前 benign batch 执行入口
  - 当前 malicious batch 执行入口
  - 当前 capture engine 直接调用入口（若已有）

Downstream consumers to watch：

- `build_manifest.py` 及后续 manifest / consistency 路径
- 后续 review / backfill / cluster / train-pool 消费路径

---

## 9. Suggested Execution Plan

建议执行顺序：

1. 读取治理文件、split handoff、data ingest handoff 与本地实际脚本。
2. 确认 benign / malicious 的真实执行入口、输入格式与 output root 组织方式。
3. 选择 benign Day 1 的 2 个 batch，要求来自不同 rank bucket，并在 task/handoff 中写明选择理由。
4. 准备 Day 1 六个 batch 的 output roots。
5. 先跑一个最小先导批次；若运行路径明显错误，先修复最小问题，不要盲目跑满全部 6 批。
6. 若先导批次通过，再完成 Day 1 剩余批次。
7. 汇总每个 batch 的状态、错误、review 比例、是否建议重跑。
8. 产出 Day 2–Day 10 队列清单与继续执行建议。
9. 写 handoff。

Day 1 固定排程：

- malicious：`batch_0001`, `batch_0002`, `batch_0003`, `batch_0004`
- benign：从不同 rank bucket 选 2 批

后续默认队列：

- Day 2：malicious `batch_0005` ~ `batch_0008`；benign 再选 2 个不同或尚未覆盖优先的 bucket batch
- Day 3：malicious `batch_0009` ~ `batch_0012`；benign 2 批
- Day 4：malicious `batch_0013` ~ `batch_0016`；benign 2 批
- Day 5：malicious `batch_0017` ~ `batch_0020`；benign 2 批
- Day 6：malicious `batch_0021` ~ `batch_0024`；benign 2 批
- Day 7：malicious `batch_0025` ~ `batch_0028`；benign 2 批
- Day 8：malicious `batch_0029` ~ `batch_0032`；benign 2 批
- Day 9：不新开 malicious 主批次；用于 retry / review / exclusion / cluster-check
- Day 10：剩余 benign 2 批 + 全局整理

---

## 10. Acceptance Criteria

本任务只有在以下条件全部满足时才算完成：

- [ ] 已确认本地仓库中的真实执行入口，而不是猜测脚本名
- [ ] Day 1 的 4 个 malicious batch 已尝试执行，或已明确写明因环境/故障无法执行的停止点
- [ ] Day 1 的 2 个 benign batch 已尝试执行，且来自不同 rank bucket，或已明确写明因环境/故障无法执行的停止点
- [ ] 每个 batch 使用独立 output root
- [ ] batch → output root → result 的映射已记录
- [ ] 未触碰 scope-out 项
- [ ] 未引入 silent schema / interface break
- [ ] 如有代码修改，已说明最小补丁与兼容性影响
- [ ] 已生成正式 handoff
- [ ] 已生成 Day 2–Day 10 剩余队列与继续执行建议

---

## 11. Validation Checklist

最低验证要求：

- [ ] 相关 Python 文件 syntax / import sanity（若修改了代码）
- [ ] Day 1 至少一个先导批次成功进入预期 output root
- [ ] Day 1 运行产物路径可被人工 spot-check
- [ ] batch 记录表与实际输出目录一致
- [ ] 若失败：失败原因、停止点、下一步建议清晰

Commands to run if applicable:

```bash
# Do not invent commands. First inspect the local repo and write the actual commands used.
# At minimum, record the exact Day 1 commands in the final handoff.
```

Expected evidence to capture:

- Day 1 实际执行命令
- 代表性 output root 路径
- 每个 batch 的状态表
- 代表性错误日志或 summary 片段（若有）

---

## 12. Handoff Requirements

本任务必须以符合 `docs/templates/HANDOFF_TEMPLATE.md` 的 handoff 结束。

本任务 handoff 必须重点覆盖：

- Day 1 实际执行了哪些 batch
- 哪些成功 / 部分成功 / 失败 / 跳过
- 使用了哪些真实 CLI / 脚本路径
- 是否做了最小代码修复
- output root 与 lineage 是否保持可审计
- Day 2–Day 10 剩余批次队列
- 若要继续跑，下一位操作员从哪里接手

建议 repo handoff path：

- `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`

---

## 13. Open Questions / Blocking Issues

- benign Day 1 具体选哪 2 个 batch，必须在读取本地 Tranco split summary 后按不同 rank bucket 决定
- 本地 benign / malicious runner 的真实脚本名与 CLI 参数，需要 Codex 先查清，不能凭记忆写
- 若本地浏览器依赖、代理或运行权限异常，Codex 应停止继续放量，并在 handoff 中明确写出 blocker
- 若 Day 1 的先导批次已经暴露系统性故障，则本任务可以以 `PARTIAL` 结束，但必须给出可继续执行的修复建议

---

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat this English section as the authoritative version. The Chinese section above is for human readers, collaboration, and quick orientation.

# Task Metadata

- Task ID: WARDEN-BATCH-CAPTURE-PLAN-A-V1
- Task Title: Execute Plan A Day 1 batch capture for current PhishTank and Tranco local batches, and prepare the remaining day-wise operator queue
- Owner Role: Codex execution engineer
- Priority: High
- Status: IN_PROGRESS
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`; `docs/handoff/2026-03-23_data_ingest_pipeline.md`; `docs/tasks/2026-03-23_tranco_batch_split.md`; `docs/handoff/2026-03-23_tranco_batch_split.md`; `docs/tasks/2026-03-23_phishtank_batch_split.md`; `docs/handoff/2026-03-23_phishtank_batch_split.md`
- Created At: 2026-03-24
- Requested By: user

---

## 1. Background

Warden already has:

1. local PhishTank malicious batch artifacts, split into 32 local 500-row batches;
2. local Tranco benign batch artifacts, strategy-aligned and split into 20 local 1000-row batches;
3. the landed data-ingest mainline and capture orchestration path;
4. active governance rules requiring task + handoff for non-trivial work, and forbidding future unexecuted work from being reported as done.

The decision is no longer whether to batch. The decision is already to use **Plan A**:

- malicious: 4 batches per day;
- benign: 2 batches per day;
- start PhishTank from `batch_0001`;
- do not run Tranco in a single-bucket contiguous sweep; prioritize cross-bucket startup;
- use one output root per batch so lineage / review / retry remains auditable.

The core purpose of this task is not a large code rewrite. It is to turn Plan A into an execution-ready operator task and, if the local environment allows, actually run **Day 1**.

Execution-environment note:

- malicious live capture for this task is executed in the user's VM;
- benign live capture for this task is executed on the user's physical machine, where local Playwright and Pillow are present and Playwright Chromium launch has been confirmed;
- the repo-side role in the current thread is to freeze the exact Day 1 commands, output roots, stop rules, dependency checks, and returned-artifact requirements per environment;
- the final Day 1 execution handoff under `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md` must only be written after the user returns the actual batch artifacts from the corresponding environment(s).

---

## 2. Goal

Complete the following four things:

1. inspect the local repository and identify the real execution entrypoints for Plan A, without inventing nonexistent script names or CLI flags;
2. land Day 1 execution:
   - malicious: run `batch_0001` through `batch_0004`;
   - benign: run 2 Tranco batches coming from different rank buckets;
3. use a dedicated output root for each batch and record the batch → output root → result mapping;
4. produce a handoff stating:
   - what was actually run on Day 1;
   - what succeeded, failed, or was skipped;
   - the remaining Day 2–Day 10 queue;
   - where the next operator should resume.

This task only requires **Day 1 + the queued remaining days**. It does not require Codex to pretend that future multi-day capture has already been completed.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- local README or operator notes under the current benign / malicious batch directories
- current capture / ingest entrypoint scripts, but only if a minimal fix is required to support Day 1 execution
- Day 1 output roots, execution summaries, and review artifacts

This task is allowed to add or modify:

- one formal task document, if it still needs to be written into the repo
- one formal handoff document
- one Day 1 execution summary or operator note
- one approved third-party dependency if it is required for the minimum viable Day 1 capture hardening patch
- only the **minimum patch** needed to support valid Day 1 execution

---

## 4. Scope Out

This task must NOT:

- pretend to complete Day 2–Day 10 asynchronous capture
- broadly redesign the current data-ingest / capture pipeline
- rename frozen fields, frozen top-level files, or frozen directory contracts
- add any third-party dependency other than the explicitly approved `playwright-stealth` hardening dependency
- modify training logic, inference logic, or label semantics
- reorder or rename existing split artifacts merely to make the schedule look cleaner
- run all 20 benign batches or all 32 malicious batches in this single task

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/tasks/2026-03-23_data_ingest_pipeline_task.md`
- `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- `docs/tasks/2026-03-23_tranco_batch_split.md`
- `docs/handoff/2026-03-23_tranco_batch_split.md`
- `docs/tasks/2026-03-23_phishtank_batch_split.md`
- `docs/handoff/2026-03-23_phishtank_batch_split.md`

### Code / Scripts

- the current benign ingest entrypoint in the local repo
- the current malicious ingest entrypoint in the local repo
- the current capture entrypoint in the local repo
- any helper scripts relevant to batch input, output roots, resume/retry, and review manifests

### Data / Artifacts

- local PhishTank batch CSV/TXT artifacts
- local Tranco batch CSV/TXT artifacts
- the current output-root base directory
- the current summary / review-artifact root, if it already exists

### Prior Handoff

- `docs/handoff/2026-03-23_data_ingest_pipeline.md`
- `docs/handoff/2026-03-23_tranco_batch_split.md`
- `docs/handoff/2026-03-23_phishtank_batch_split.md`

### Missing Inputs

- the exact current runner filenames and CLI flags for benign / malicious execution must be resolved by reading the local repo; do not guess
- if the local environment is missing required proxy, browser dependencies, account state, or permissions, that must be stated explicitly in handoff instead of being disguised as script success
- current known dependency status for the physical-machine benign lane: Python package import is available for `playwright` and `PIL`, and Playwright Chromium launch has been confirmed
- current approved hardening dependency status: `playwright-stealth` may be introduced if required for the minimum viable anti-bot capture patch and must be documented explicitly in handoff

---

## 6. Required Outputs

This task must produce:

1. one formal task document, if this file still needs to be written into the repo
2. one formal Day 1 handoff document after the physical-machine benign artifacts and VM malicious artifacts are returned
3. a Day 1 batch execution record covering at least:
   - batch id
   - source type (benign / malicious)
   - input artifact path
   - output root
   - status (success / partial / failed / skipped)
   - short note
4. a remaining Day 2–Day 10 queue list
5. explicit retry / stop / continue guidance if failures occur
6. if a minimal code fix was made for Day 1, the minimal patch plus compatibility notes

---

## 7. Hard Constraints

The following constraints are mandatory:

- preserve backward compatibility unless explicitly impossible, and explain it if so
- do not rename frozen schema fields or frozen top-level file names
- do not silently change output formats
- do not add new third-party dependencies other than the explicitly approved `playwright-stealth` capture-hardening dependency
- prefer a minimal patch over opportunistic refactor
- update docs if behavior changes
- follow `AGENTS.md`
- follow `docs/workflow/GPT_CODEX_WORKFLOW.md`
- use the local repository as the source of truth, not an older GitHub-visible snapshot
- do not report Day 2–Day 10 as completed if they were not actually run
- do not treat malicious capture as locally executable in this workspace for this task; malicious remains VM-only
- do not treat benign physical-machine execution as complete until real benign batch artifacts are returned, even though local Playwright browser readiness has now been confirmed

Task-specific constraints:

- malicious Day 1 is fixed to `batch_0001` through `batch_0004`
- benign Day 1 is fixed to **2 batches from different rank buckets**, not from the same bucket
- each batch must have a dedicated output root
- any failure or interruption must preserve lineage and must not overwrite old artifacts
- if Day 1 reveals a systemic fault, stop scaling further and state the stop point and reason clearly in handoff

---

## 8. Interface / Schema Constraints

These public interfaces must remain stable:

- the current benign ingest CLI, if it exists
- the current malicious ingest CLI, if it exists
- the current capture entrypoint CLI, if it exists
- the current successful-sample directory semantics
- the current batch-artifact file names and directory semantics

Schema / field constraints:

- Schema changed allowed: NO for this hardening patch
- If yes, required compatibility plan: not applicable
- Frozen field names involved: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - the current benign batch execution entrypoint
  - the current malicious batch execution entrypoint
  - the current direct capture-engine entrypoint, if one exists

Downstream consumers to watch:

- `build_manifest.py` and later manifest / consistency paths
- later review / backfill / cluster / train-pool consumer paths

---

## 9. Suggested Execution Plan

Recommended order:

1. read the governance files, split handoffs, data-ingest handoff, and the local repo scripts;
2. resolve the true benign / malicious execution entrypoints, input formats, and output-root structure;
3. choose the 2 benign Day 1 batches, ensuring they come from different rank buckets, and record the rationale;
4. prepare the output roots for all 6 Day 1 batches;
5. run one pilot batch first; if the execution path is clearly broken, fix only the minimum issue instead of blindly launching all 6 batches;
6. if the pilot passes, finish the remaining Day 1 batches;
7. summarize per-batch status, errors, review ratio, and rerun recommendation;
8. produce the Day 2–Day 10 remaining queue and continuation guidance;
9. write handoff.

Fixed Day 1 schedule:

- malicious: `batch_0001`, `batch_0002`, `batch_0003`, `batch_0004`
- benign: pick 2 batches from different rank buckets

Default remaining queue:

- Day 2: malicious `batch_0005` ~ `batch_0008`; benign 2 more batches from different or not-yet-covered preferred buckets
- Day 3: malicious `batch_0009` ~ `batch_0012`; benign 2 batches
- Day 4: malicious `batch_0013` ~ `batch_0016`; benign 2 batches
- Day 5: malicious `batch_0017` ~ `batch_0020`; benign 2 batches
- Day 6: malicious `batch_0021` ~ `batch_0024`; benign 2 batches
- Day 7: malicious `batch_0025` ~ `batch_0028`; benign 2 batches
- Day 8: malicious `batch_0029` ~ `batch_0032`; benign 2 batches
- Day 9: no new malicious main batches; use for retry / review / exclusion / cluster-check
- Day 10: remaining benign 2 batches + global cleanup

---

## 10. Acceptance Criteria

This task is complete only if all conditions below are satisfied:

- [ ] the actual local execution entrypoints were resolved instead of guessed
- [ ] the 4 malicious Day 1 batches were attempted, or the exact environment/system stop point was documented
- [ ] the 2 benign Day 1 batches were attempted from different rank buckets, or the exact environment/system stop point was documented
- [ ] each batch used a dedicated output root
- [ ] the batch → output root → result mapping was recorded
- [ ] no scope-out item was touched
- [ ] no silent schema / interface break was introduced
- [ ] if code changed, the minimal patch and compatibility impact were explained
- [ ] a formal handoff was produced
- [ ] the Day 2–Day 10 remaining queue and continuation guidance were produced

---

## 11. Validation Checklist

Minimum validation required:

- [ ] syntax / import sanity for any changed Python files
- [ ] at least one pilot Day 1 batch successfully entered the expected output root
- [ ] the Day 1 output paths are available for human spot-check
- [ ] the batch record table matches the actual output directories
- [ ] if failures occurred, the failure reason, stop point, and next-step advice are clear

Commands to run if applicable:

```bash
# Do not invent commands. First inspect the local repo and record the actual commands used.
# At minimum, place the exact Day 1 commands in the final handoff.
```

Expected evidence to capture:

- the actual Day 1 commands executed
- representative output-root paths
- the per-batch status table
- representative error-output or summary snippets, if any

---

## 12. Handoff Requirements

This task must end with a handoff aligned to `docs/templates/HANDOFF_TEMPLATE.md`.

The handoff must explicitly cover:

- which Day 1 batches were actually executed
- which succeeded / partially succeeded / failed / were skipped
- which real CLI / script paths were used
- whether any minimal code fix was made
- whether output roots and lineage remained auditable
- the remaining Day 2–Day 10 queue
- where the next operator should resume

Suggested repo handoff path:

- `docs/handoff/2026-03-24_plan_a_batch_capture_day1.md`

---

## 13. Open Questions / Blocking Issues

- which exact 2 benign Day 1 batches should be chosen must be decided after reading the local Tranco split summary and ensuring cross-bucket coverage
- the exact local benign / malicious runner names and CLI flags must be resolved by Codex first, not guessed from memory
- if local browser dependencies, proxy state, or execution permissions are broken, Codex should stop scaling further and state the blocker clearly in handoff
- if the pilot Day 1 batch already exposes a systemic fault, this task may end as `PARTIAL`, but it must still provide concrete repair guidance for continuation
