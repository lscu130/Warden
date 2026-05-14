# Invalid Capture Residual Grep Report V1

## 中文摘要

本报告记录 `invalid capture / blank / 404 / pure-color / broken render / insufficient-observability / recrawl` 相关 residual grep 的分类结果。

分类结论：

- Active aligned：当前 active 合同中保留的命中，已明确写成数据清洗阶段移除对象或未来可选采集基础设施说明。
- Active patched：本任务已修正的 active 文档旧语义。
- Historical / superseded：旧 ADR、旧 task、旧 handoff、旧 report 中的历史语境，按任务要求不重写。
- Numeric / unrelated：`500` 行批次、timeout 数值、计划批次编号等非语义命中。
- Operational capture：capture runbook 中关于 timeout / HTTP status 的操作说明，不构成 threat-label 或 L1 routing 语义。

## English Version

> AI note: The English section is authoritative for exact residual classification.

# Invalid Capture Residual Grep Report V1

## 1. Command Pattern

Focused residual search pattern:

```powershell
rg -n "bad capture|bad_capture|blank|404|403|500|pure-color|pure color|empty page|broken render|render failed|invalid capture|insufficient observability|insufficient_observability|need_recrawl|route_to_recrawl|recrawl|QA queue|exclude queue|auxiliary capture" docs AGENTS.md PROJECT.md README.md
```

## 2. Active Patched Hits

The following active documents were patched:

- `docs/data/TRAIN_LABEL_DERIVATION_V1.md`
  - Removed blank-page wording from future heavier-review examples.
  - Replaced `blank_or_sparse_initial_page` with `sparse_initial_page`.
  - Added explicit dataset-quality / observability failure boundary.

- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
  - Removed broken / blank samples from second-pass auxiliary routing semantics.
  - Added explicit statement that invalid captures and insufficient-observability pages are outside second-pass review.

- `docs/data/Warden_MALICIOUS_SOURCE_POLICY_V1.md`
  - Added explicit statement that rejected / invalid page-validity cases are removed before formal train / validation / test construction and are not threat labels.

- `docs/data/GATA_EVASION_AUXILIARY_SET_V1.md`
  - Removed `blank` from gate / evasion auxiliary sample framing.
  - Added explicit statement that pure blank, HTTP error, pure-color, severe broken render, and insufficient-observability pages are not part of the auxiliary set.

- `docs/modules/MODULE_INFER.md`
  - Removed current recrawl hint semantics from active L0 / L1 inference wording.
  - Reframed future recrawl as separately defined capture infrastructure only.

- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
  - Removed current recrawl reason-code wording from L1 fallback / future path description.

- `docs/modules/Warden_TEXT_PIPELINE_V1.md`
  - Removed `need recrawl` as a current routing head.

- `docs/modules/Warden_VISION_PIPELINE_V1.md`
  - Removed `recrawl` as a current vision-path routing hint and reframed it as future capture infrastructure.

- `docs/modules/L0_DESIGN_V1.md`
  - Removed `recrawl` from the active legacy `need_l2_candidate` / `need_l2` compatibility note.
  - Replaced L0 abnormal-state wording so `blank` no longer looks like an L0 routing category.

## 3. Active Aligned Hits

Expected aligned hits remain in:

- `AGENTS.md`
- `PROJECT.md`
- `docs/frozen/Warden_Threat_Definition_V1.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/L0_DESIGN_V1.md`
- `docs/modules/Warden_RUNTIME_DATAFLOW_FREEZE_SPEC_V0.1.md`
- `docs/l1/WARDEN_L1_DECISION_HEAD_CONTRACT_V0.1.md`

These hits state that invalid captures, HTTP error pages, blank pages, pure-color renders, severe broken renders, and insufficient-observability pages are removed during dataset cleaning and are not benign / malicious / suspicious threat labels.

## 4. Historical / Superseded Hits

Residuals in historical records were not rewritten:

- `docs/adr/ADR_20260508_Warden_L1_Fast_L2_Semantic_Refactor_V0_1.md`
- previous task docs under `docs/tasks/**`
- previous handoff docs under `docs/handoff/**`
- previous reports under `docs/reports/**`

These files document previous decisions, previous implementation states, benchmark outputs, or prior review comments. They do not override the current active contracts.

## 5. Numeric / Unrelated Hits

Residual grep also matches unrelated numeric text, including:

- `500` row batch sizes in PhishTank / Tranco batch tasks and handoffs.
- `25000` timeout values in capture docs.
- Tranco rank buckets such as `100001_500000`.

These are false positives for the invalid-capture cleanup.

## 6. Operational Capture Hits

`docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md` still mentions timeout and HTTP status buckets as operator-facing capture-run notes.

Classification: operational capture documentation, not a threat-label, L0 routing, L1 routing, recrawl queue, exclude queue, or QA queue definition.

## 7. Residual Risk

The repository still contains historical wording in old ADR, task, handoff, and report files. This is expected under the task boundary. If the project later wants historical docs to carry superseded banners, that should be a separate governance task.
