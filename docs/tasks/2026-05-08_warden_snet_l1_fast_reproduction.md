<!-- operator: Codex; task: warden-snet-l1-fast-reproduction; date: 2026-05-08 -->

# Warden SNet L1-fast Reproduction Task

## 中文版

本任务按用户提供的 `Warden_SpecularNet_SNet_L1Fast_Reproduction_Task.md` 执行首轮 repo-local 复现。目标是实现一个最小可训练的 SpecularNet-style SNet 结构分支，并用 Warden 现有 rendered DOM、URL/domain 和弱标签样本跑通 smoke。

关键边界：

- SNet 只能作为 L1-fast 候选结构/DOM 异常分支，不是 Warden 最终威胁判断器。
- 不改冻结 labels、schema、L0/L1/L2 默认运行行为。
- 不新增第三方依赖；若 Word2Vec 依赖不可用，允许记录偏差并使用 trainable embedding。
- 若找不到 rendered DOM/HTML 或标签无法映射，则停止并报告 partial/blocked。
- 若没有现有 CLIP 输出，则不做 fusion，只记录未运行原因。

## English Version

> AI note: English is authoritative for exact task scope, interfaces, success criteria, and validation rules.

# Task Metadata

- Task ID: `TASK-WARDEN-SNET-001`
- Task Title: `Reproduce SpecularNet-style SNet and evaluate SNet+CLIP for L1-fast`
- Owner Role: `Codex`
- Priority: `High`
- Status: `PARTIAL`
- Related Module: `Warden L1-fast / model research / inference pipeline`
- Related Issue / ADR / Doc:
  - `AGENTS.md`
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
  - `docs/templates/TASK_TEMPLATE.md`
  - `docs/templates/HANDOFF_TEMPLATE.md`
  - `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`
  - `docs/modules/Warden_VISION_PIPELINE_V1.md`
- Created At: `2026-05-08`
- Requested By: `佶`

---

## 1. Background

The user provided an external reproduction task for SpecularNet, renamed internally as SNet for Warden research. The task asks whether a SpecularNet-style domain + rendered DOM structural branch can support Warden L1-fast when combined with CLIP.

The source task explicitly states that SNet cannot replace Warden's broader social-engineering judgment because it ignores text, screenshots, attribute values, brand appearance, action semantics, wallet/support/investment narratives, and other Warden-critical modalities.

---

## 2. Goal

Implement and smoke-test a minimal, auditable SNet reproduction inside Warden using existing rendered DOM/HTML, URL/domain, and pilot binary weak labels. Evaluate SNet-only smoke behavior and determine whether the current evidence is sufficient to proceed toward L1-fast ADR or must remain exploratory.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/2026-05-08_warden_snet_l1_fast_reproduction.md`
- `docs/research/2026-05-08_warden_snet_l1_fast_reproduction_report.md`
- `docs/handoff/2026-05-08_warden_snet_l1_fast_reproduction.md`
- `configs/train/snet_l1_fast_smoke.yaml`
- `scripts/build_snet_splits.py`
- `scripts/train_snet.py`
- `scripts/eval_snet.py`
- `src/warden/models/snet/`
- `tests/train/snet/`
- ignored local smoke outputs under `tmp/snet_l1_fast_smoke/`

Allowed changes:

- add a read-only SNet dataset adapter;
- add deterministic DOM tag/attribute parser;
- add pure PyTorch SNet model modules;
- add split/train/eval research CLIs;
- add per-sample SNet score export;
- add tests for label direction, DOM parsing, pooling connectivity, output keys, and score direction;
- add research report and handoff.

---

## 4. Scope Out

This task must NOT do the following:

- modify frozen Warden labels or schema;
- change existing L0/L1/L2 behavior by default;
- replace existing CLIP branch;
- add SNet to production runtime routing;
- add third-party dependencies without approval;
- mutate raw dataset directories;
- relabel datasets;
- treat weak labels as human gold labels;
- train SNet on screenshots, visible text, full URL paths, reputation, WHOIS, DNS, ASN, or blacklist data;
- claim SNet+CLIP fusion results if CLIP outputs are missing.

---

## 5. Inputs

### Docs

- `AGENTS.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/data/TRAINSET_V1.md`
- `docs/modules/Warden_VISION_PIPELINE_V1.md`
- `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md`

### Code / Scripts

- existing `scripts/data/build_manifest.py`
- existing `scripts/data/common/html_payload_utils.py`
- existing `scripts/data/common/runtime_data_root.py`

### Data / Artifacts

- `E:\WardenData\processed\trainset_v1_externalization_smoke\manifest.jsonl`
- `E:\WardenData\processed\tranco_benign_triage_v1_t00_t05_consistency_20260507\post_dedup\manifest.jsonl`
- sample-level `url.json`
- sample-level `html_rendered.json`
- manifest `label_hint`

### Prior Handoff

- none required for SNet implementation; L1 framework docs were read for compatibility.

### Missing Inputs

- stable CLIP/MobileCLIP per-sample outputs were not found during inventory.
- `gensim` was not available in the current Python environment.

---

## 6. Required Outputs

- Repo-local task document.
- SNet model/data/parser implementation.
- Split builder CLI.
- Train CLI.
- Eval CLI.
- Smoke config.
- Targeted tests.
- Research report with metrics, latency, skipped counts, failure cases, and recommendation.
- Handoff document.

---

## 7. Hard Constraints

- Use rendered DOM/HTML when available.
- Ignore text nodes and attribute values in SNet.
- Preserve internal label convention: `benign = 1`, `phish/malicious/threat = 0`.
- Expose external `phish_score = 1 - benign_prob`.
- Do not add dependencies.
- If faithful Word2Vec cannot be implemented without adding dependencies, record it as a controlled deviation.
- Keep all raw data operations read-only.
- Record validation honestly.

---

## 8. Interface / Schema Constraints

- Schema changed: no.
- Existing CLI changed: no.
- Existing runtime interface changed: no.
- New research CLIs are additive only.
- New research score fields are not production schema fields unless a future task explicitly freezes them.

---

## 9. Evidence / Retrieval Rules

Before implementation, inspect:

- current repository tree;
- existing dataset sample format;
- existing model/config conventions;
- existing CLIP/L1-fast outputs if any;
- dependency availability;
- mandatory Warden workflow docs.

Stop retrieval when Phase 0 inventory can support SNet-only POC and additional search is unlikely to unblock CLIP fusion.

---

## 10. Acceptance Criteria

- SNet split builder can create train/val/test JSONL from existing Warden manifests without mutating raw data.
- SNet parser ignores text and attribute values and preserves tag/attribute structure.
- Root-preserving TopK pooling keeps root and reconnects retained nodes.
- SNet forward output includes `benign_prob`, `phish_score`, `prob_threshold`, `prob_mlp`, `recon_error`, `dom_node_count`, and `pooled_node_count`.
- Label direction tests prove `benign=1`, `phish=0`, and `phish_score = 1 - benign_prob`.
- A one-epoch smoke train/eval run completes if inputs exist.
- Fusion is run only if CLIP outputs already exist.
- Final report states go/no-go honestly.

---

## 11. Validation Checklist

- [x] Read mandatory Warden governance docs.
- [x] Inventory rendered DOM / URL / label availability.
- [x] Inventory CLIP output availability.
- [x] Check dependency availability.
- [x] Run `py_compile` over new modules and scripts.
- [x] Run targeted SNet pytest tests.
- [x] Run split-builder smoke.
- [x] Run train smoke.
- [x] Run eval smoke.
- [x] Write research report and handoff.
- [x] Report CLIP/fusion as not run if CLIP outputs are missing.
