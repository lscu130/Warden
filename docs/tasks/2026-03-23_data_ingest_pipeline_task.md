# 2026-03-23_data_ingest_pipeline_task

## 中文版

# Task Metadata

- Task ID: WARDEN-DATA-INGEST-V1
- Task Title: Split benign/malicious ingest pipelines, preserve current capture engine, and implement malicious cluster/subcluster train-pool construction
- Owner Role: Codex execution engineer
- Priority: High
- Status: TODO
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`; `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- Created At: 2026-03-23
- Requested By: user

---

## 1. 背景

Warden 当前已有可用的 capture 引擎 `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`，但 benign 与 malicious 现在已经有不同的上层策略边界：
- benign 需要按 `Warden_BENIGN_SAMPLING_STRATEGY_V1.md` 做分层抽样、可信长尾补充与 hard-benign 采样；
- malicious 需要按 `Warden_MALICIOUS_SOURCE_POLICY_V1.md` 做公开基线来源接入、页面有效性检查、campaign/template 聚类、subcluster 抽样，以及 archive/train/reserve 三池构建。

本任务目标不是重写 capture，而是在最小改动下：
- 让 capture 成为可编排的底层引擎；
- 新增 benign / malicious 两条上层 pipeline；
- 新增 malicious 的 cluster/subcluster 训练池构建；
- 新增老数据回处理与 review 输出。

---

## 2. 目标

实现 Warden V1 数据摄取结构，使其满足：
1. benign 和 malicious 使用分开的上层入口脚本；
2. capture 引擎保持可复用，改成无交互可编排；
3. malicious 公开基线来源固定支持 **OpenPhish Community + PhishTank**；
4. malicious 不再使用“每簇最多保留固定 N 条”的硬规则，而是支持：
   - exact URL 去重
   - normalized/final URL 去重
   - campaign/template 聚类
   - subcluster 切分
   - train/reserve 分流
   - family share cap
5. 提供老数据回处理脚本，对历史 malicious 样本回填 fingerprint、cluster/subcluster、review manifest、训练排除清单；
6. 默认不物理删除历史样本目录。

---

## 3. Scope In

允许修改：
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/`
- `docs/data/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

允许新增：
- benign pipeline 脚本
- malicious pipeline 脚本
- common helper 模块
- maintenance/backfill 脚本
- 与新行为相关的文档

---

## 4. Scope Out

本任务不得：
- 重写 capture 主抓取逻辑
- 重命名冻结的 top-level 输出文件
- 修改训练逻辑
- 修改推理逻辑
- 引入新的第三方依赖
- 默认物理删除历史样本目录
- 把 benign / malicious 业务策略重新糊成一个大脚本
- 把固定 “keep 15 per cluster” 一类 magic number 写死成默认硬规则

---

## 5. 输入

### Docs
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`

### Code / Scripts
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- 现有 capture 相关 helper（若仓库中已有）

### Data / Artifacts
- 当前 benign 样本根目录
- 当前 malicious 样本根目录
- 一小批 benign URL 用于 smoke test
- 一小批 malicious URL 用于 smoke test
- 一小批历史 malicious 样本目录用于 backfill smoke test

### Missing Inputs
- `PROJECT.md` 内容若仓库中无有效内容，则不作为约束前提
- 恶性 family share cap 的具体数值默认做成配置项，不在本任务中由文档写死

---

## 6. 必须产出

本任务应产出：
1. capture 的无交互 CLI 入口
2. benign 上层 ingest path
3. malicious 上层 ingest path
4. malicious cluster / subcluster 构建脚本
5. malicious train-pool / reserve-pool 构建脚本
6. 历史数据 fingerprint 回填脚本
7. dedup review manifest 输出
8. 训练排除清单输出
9. 更新后的文档
10. 非 trivial handoff 文档

---

## 7. Hard Constraints

必须遵守：
- 保持向后兼容，除非明确做不到，并在交付中说明
- 不重命名冻结字段或 top-level 文件名
- 不静默改变输出结构
- 不新增第三方依赖
- 优先最小补丁
- 若行为变化，必须更新文档
- 遵循 `AGENTS.md`
- 遵循 `docs/workflow/GPT_CODEX_WORKFLOW.md`
- 输出 handoff 文档

任务特定约束：
- capture 必须仍然是底层 evidence-production engine
- benign 与 malicious 必须保持两条上层 pipeline
- malicious 公开基线来源默认支持 OpenPhish Community + PhishTank
- malicious 去重必须支持 exact URL、normalized/final URL、cluster、subcluster
- 训练池必须基于 cluster -> subcluster -> train/reserve 决策，而不是固定每簇保留条数
- family share cap 必须作为配置项暴露，而不是写死 magic number
- 历史数据处理默认只做“报告 + 标记”，不做物理删除

---

## 8. Interface / Schema Constraints

必须保持稳定的接口：
- 已冻结的 top-level 文件名
- 当前成功样本目录语义
- 当前 capture 输出结构

允许增加：
- 新 CLI flags，例如 `--label`
- helper manifests / review outputs / exclusion lists
- 向后兼容的新 metadata 字段

禁止：
- 重命名 `meta.json`, `url.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`
- 为了方便而改写现有字段语义

---

## 9. Acceptance Criteria

满足以下所有条件才算完成：
1. capture 可被上层脚本无交互调用
2. benign 与 malicious 入口明确分离
3. malicious 公开源至少支持 OpenPhish Community 与 PhishTank
4. malicious cluster / subcluster 输出可 review，而不是 silent drop
5. train-pool / reserve-pool 决策存在且可导出 manifest
6. 历史数据回处理脚本可生成 fingerprint、cluster/subcluster、review manifest、训练排除清单
7. 未发生禁止的 schema / filename 重命名
8. 文档同步更新
9. handoff 文档已生成

---

## 10. 最低验证清单

必须至少完成：
1. 所有修改 Python 文件的 syntax / import sanity
2. 一个小规模 benign smoke run
3. 一个小规模 malicious smoke run（OpenPhish 或 PhishTank URL 子集）
4. 一个小规模历史 malicious backfill smoke run
5. 人工检查生成的 review manifest / exclusion list / cluster outputs
6. 明确写出 capture CLI 兼容性说明

若某项无法跑，必须明确说明：
- 哪项没跑
- 为什么没跑
- 下一步应如何补验证

---

## 11. 推荐文件变更范围

保守预期：
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/common/...`
- `scripts/data/benign/...`
- `scripts/data/malicious/...`
- `scripts/data/maintenance/...`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`（若需补行为说明）
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/tasks/<date>_data_ingest_pipeline.md`
- `docs/handoff/<date>_data_ingest_pipeline.md`

---

## 12. 给 Codex 的具体实现提示

1. 先读当前 capture 脚本，不要一上来大重构。
2. 先把 capture 入口无交互化，再做上层 orchestrator。
3. benign 与 malicious 入口分开，但共用 common utils。
4. malicious 去重不要只做 exact URL；至少补 normalized/final URL + cluster + subcluster。
5. 不要把 family share cap 写成固定 15 或其他 magic number；改成配置项。
6. 历史数据脚本默认输出 review / exclusion，不默认删目录。
7. 任何不确定的地方优先保留原始数据，再输出标记与 manifest。

---

## English Version

# Task Metadata

- Task ID: WARDEN-DATA-INGEST-V1
- Task Title: Split benign/malicious ingest pipelines, preserve the current capture engine, and implement malicious cluster/subcluster train-pool construction
- Owner Role: Codex execution engineer
- Priority: High
- Status: TODO
- Related Module: Data module
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`; `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`; `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- Created At: 2026-03-23
- Requested By: user

---

## 1. Background

Warden already has a usable capture engine in `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`, but benign and malicious now have clearly different upper-layer strategy boundaries:
- benign requires stratified sampling, trusted long-tail supplementation, and hard-benign sampling according to `Warden_BENIGN_SAMPLING_STRATEGY_V1.md`,
- malicious requires public-baseline ingestion, page-validity checks, campaign/template clustering, subcluster sampling, and archive/train/reserve pool construction according to `Warden_MALICIOUS_SOURCE_POLICY_V1.md`.

The goal is not to rewrite capture. The goal is to:
- make capture an orchestratable lower-layer engine,
- add separate benign and malicious upper-layer pipelines,
- add malicious cluster/subcluster train-pool construction,
- add legacy-data backfill and review outputs.

---

## 2. Goal

Implement a Warden V1 data-ingest structure that satisfies all of the following:
1. benign and malicious use separate upper-layer entry scripts,
2. the capture engine remains reusable and non-interactive,
3. the malicious public baseline explicitly supports **OpenPhish Community + PhishTank**,
4. malicious no longer uses a hard fixed “keep at most N per cluster” rule, and instead supports:
   - exact URL dedup,
   - normalized/final URL dedup,
   - campaign/template clustering,
   - subcluster splitting,
   - train/reserve routing,
   - family share cap,
5. legacy-data backfill scripts exist for historical malicious samples and can generate fingerprints, cluster/subcluster assignments, review manifests, and training exclusion lists,
6. historical sample directories are not physically deleted by default.

---

## 3. Scope In

This task may modify:
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/`
- `docs/data/`
- `docs/modules/`
- `docs/tasks/`
- `docs/handoff/`

This task may add:
- benign pipeline scripts,
- malicious pipeline scripts,
- common helper modules,
- maintenance/backfill scripts,
- documentation required by the new behavior.

---

## 4. Scope Out

This task must NOT:
- rewrite the core capture logic,
- rename frozen top-level output files,
- modify training logic,
- modify inference logic,
- add new third-party dependencies,
- physically delete historical sample directories by default,
- collapse benign and malicious back into one monolithic strategy script,
- hardcode a fixed “keep 15 per cluster” or similar magic-number rule as the default.

---

## 5. Inputs

### Docs
- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md`
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`

### Code / Scripts
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- any existing capture-related helpers already present in the repo

### Data / Artifacts
- current benign sample root
- current malicious sample root
- a small benign URL subset for smoke testing
- a small malicious URL subset for smoke testing
- a small historical malicious subset for backfill smoke testing

### Missing Inputs
- `PROJECT.md` should not be treated as a binding source if it is empty or unavailable
- the exact family share cap numeric value should remain configurable rather than frozen in this task

---

## 6. Required Outputs

This task must produce:
1. a non-interactive capture CLI entry,
2. a benign upper-layer ingest path,
3. a malicious upper-layer ingest path,
4. a malicious cluster/subcluster builder,
5. a malicious train-pool / reserve-pool builder,
6. a legacy-data fingerprint backfill script,
7. dedup review manifests,
8. training exclusion lists,
9. updated documentation,
10. a non-trivial handoff document.

---

## 7. Hard Constraints

The implementation must obey all of the following:
- preserve backward compatibility unless clearly impossible and then report it,
- do not rename frozen schema fields or top-level filenames,
- do not silently change output format,
- do not add third-party dependencies,
- prefer minimal patching,
- update docs if behavior changes,
- follow `AGENTS.md`,
- follow `docs/workflow/GPT_CODEX_WORKFLOW.md`,
- produce a handoff document.

Task-specific constraints:
- capture must remain the lower-layer evidence-production engine,
- benign and malicious must remain separate upper-layer pipelines,
- the malicious public baseline must explicitly support OpenPhish Community + PhishTank,
- malicious dedup must support exact URL, normalized/final URL, cluster, and subcluster handling,
- train-pool decisions must be based on cluster -> subcluster -> train/reserve routing rather than a fixed per-cluster retention count,
- family share cap must be exposed as configuration rather than hardcoded as a magic number,
- historical-data handling must default to reporting and marking, not deletion.

---

## 8. Interface / Schema Constraints

The following must remain stable:
- frozen top-level sample filenames,
- current successful-sample directory semantics,
- current capture output structure.

Backward-compatible additions allowed:
- new CLI flags such as `--label`,
- helper manifests / review outputs / exclusion lists,
- new metadata fields that do not replace existing semantics.

Not allowed:
- renaming `meta.json`, `url.json`, `redirect_chain.json`, `visible_text.txt`, `forms.json`, `screenshot_viewport.png`, `screenshot_full.png`, `net_summary.json`, `auto_labels.json`,
- changing existing field semantics for convenience.

---

## 9. Acceptance Criteria

This task is complete only if all of the following are true:
1. capture can be called non-interactively by upper-layer scripts,
2. benign and malicious entrypoints are clearly separated,
3. malicious public-source ingestion supports at least OpenPhish Community and PhishTank,
4. malicious cluster/subcluster outputs are reviewable rather than silently dropped,
5. train-pool / reserve-pool routing exists and exports manifests,
6. legacy-data backfill scripts can generate fingerprints, cluster/subcluster assignments, review manifests, and training exclusion lists,
7. no forbidden schema or filename renames occurred,
8. documentation is updated,
9. a handoff document is produced.

---

## 10. Minimum Validation Checklist

At minimum, the implementation must validate:
1. syntax / import sanity for all touched Python files,
2. one small benign smoke run,
3. one small malicious smoke run using a small OpenPhish or PhishTank subset,
4. one small historical-malicious backfill smoke run,
5. manual inspection of generated review manifests / exclusion lists / cluster outputs,
6. an explicit compatibility note for the capture CLI change.

If any validation is not run, the final handoff must state:
- what was not run,
- why it was not run,
- what should be run next.

---

## 11. Recommended File Touch Set

Conservative expected set:
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/common/...`
- `scripts/data/benign/...`
- `scripts/data/malicious/...`
- `scripts/data/maintenance/...`
- `docs/modules/Warden_DATA_INGEST_ARCHITECTURE_V1.md`
- `docs/data/Warden_BENIGN_SAMPLING_STRATEGY_V1.md` if behavior notes are needed,
- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`,
- `docs/tasks/<date>_data_ingest_pipeline.md`,
- `docs/handoff/<date>_data_ingest_pipeline.md`.

---

## 12. Practical Codex Guidance

1. Read the current capture script first; do not start with a broad refactor.
2. Make capture non-interactive before adding upper-layer orchestration.
3. Keep benign and malicious entrypoints separate, but share common utilities.
4. Malicious dedup must go beyond exact URL and include normalized/final URL plus cluster and subcluster handling.
5. Do not hardcode a family-share rule such as fixed keep-15; expose it as configuration.
6. Legacy-data scripts should generate review and exclusion outputs by default, not delete directories.
7. When uncertain, preserve the raw data and emit markings/manifests rather than destructive actions.
