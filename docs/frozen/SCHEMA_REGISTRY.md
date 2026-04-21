# SCHEMA_REGISTRY.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档用于汇总 Warden 当前已冻结或应视为冻结的公开契约表面。
- 若字段名、文件名、CLI 参数、输出名或兼容性结论存在歧义，以英文版为准。
- 不能从现有冻结文档或仓库现状直接证明的内容，必须标为 `uncertain / needs confirmation`。

### 摘要

- 当前最强的冻结来源是 `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md` 和 `docs/data/TRAINSET_V1.md`。
- 本 registry 只记录当前能从冻结文档和仓库现状确认的 public schema / top-level keys / file names / CLI surfaces / output artifacts。
- 推理侧 CLI、深层嵌套 schema、枚举语义细节和未文档化接口，当前不在本次 P0 registry 的确定覆盖范围内。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# SCHEMA_REGISTRY.md

This document is the first repo-native human-readable registry of Warden public contract surfaces that should be treated as frozen or functionally frozen.

It is intentionally conservative.
Only surfaces supported by current frozen docs or direct repository observation are listed as confirmed.
Anything that cannot be proven from those sources is marked `uncertain / needs confirmation`.

## 1. Source Priority Used For This Registry

Confirmed sources used here:

- `AGENTS.md`
- `PROJECT.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/data/TRAINSET_V1.md`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- direct read-only observation of one current real sample directory under `data/raw/...`

Interpretation rules:

- frozen docs outrank inferred behavior
- current script reality may confirm a surface that the docs already imply
- undocumented public surfaces are not upgraded to confirmed status by guesswork

## 2. Frozen Sample-Directory Output Artifacts

Confirmed from `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`:

Core sample artifacts that a successful sample directory may contain:

- `meta.json`
- `url.json`
- `env.json`
- `redirect_chain.json`
- `html_raw.json`
- `html_rendered.json`
- `visible_text.txt`
- `forms.json`
- `screenshot_viewport.png`
- `screenshot_full.png`
- `net_summary.json`
- `auto_labels.json`
- `rule_labels.json`
- `manual_labels.json`

Mode-dependent or optional artifacts:

- `actions.jsonl`
- `after_action/`
- `variants/`
- `diff_summary.json`
- `network.har`

Confirmed compatibility note:

- file names above should be treated as frozen unless the spec is explicitly version-bumped
- as of the 2026-04-10 capture-contract update, HTML payload artifacts are stored as JSON wrappers such as `html_raw.json` and `html_rendered.json`
- legacy sample directories may still contain old `.html` artifacts during migration, so compatibility readers may need to support both forms temporarily

## 3. Confirmed Top-Level JSON Keys

### 3.1 `meta.json`

Confirmed by direct observation of one current real sample:

- `sample_id`
- `label`
- `crawl_time_utc`
- `http_status`
- `page_title`
- `etld1_mode`
- `ingest_metadata`

Confirmed by frozen doc semantics:

- `sample_id`
- `label`
- `crawl_time_utc`
- `http_status`

Registry decision:

- the full observed top-level key set above is treated as the current baseline top-level surface for P0 checks
- nested structure under `ingest_metadata` is `uncertain / needs confirmation` for this registry

### 3.2 `url.json`

Confirmed by direct observation of one current real sample:

- `input_url`
- `final_url`
- `redirect_chain`

Registry decision:

- these top-level keys are confirmed for P0 compatibility checks
- nested redirect entry structure is `uncertain / needs confirmation` in this registry

### 3.3 `auto_labels.json`

Confirmed by frozen doc and direct observation:

- `schema_version`
- `generated_at_utc`
- `source`
- `label_hint`
- `page_stage_candidate`
- `language_candidate`
- `url_features`
- `form_features`
- `html_features`
- `brand_signals`
- `intent_signals`
- `evasion_signals`
- `network_features`
- `risk_outputs`

Confirmed compatibility note:

- these top-level fields are part of the current frozen weak-label surface

Registry decision:

- nested key structure under each field family is only partially documented here
- nested shape remains `uncertain / needs confirmation` unless separately frozen

## 4. TrainSet V1 Manifest Surface

Confirmed from `docs/data/TRAINSET_V1.md`.

### 4.1 Minimum Manifest Fields

- `sample_id`
- `sample_dir`
- `label_hint`
- `crawl_time_utc`
- `http_status`
- `input_url`
- `final_url`

File-presence fields:

- `has_visible_text`
- `has_forms`
- `has_html_rendered`
- `has_html_raw`
- `has_screenshot_full`
- `has_rule_labels`
- `has_manual_labels`

Training-usability fields:

- `usable_for_text`
- `usable_for_vision`
- `usable_for_multimodal`

Optional enhancement fields explicitly named by the spec:

- `page_stage_candidate`
- `risk_level_weak`
- `review_priority`
- `domain_etld1`
- `split`

### 4.2 Required Sample-Directory Files For TrainSet V1 Admission

- `meta.json`
- `url.json`
- `env.json`
- `redirect_chain.json`
- `screenshot_viewport.png`
- `net_summary.json`
- `auto_labels.json`

Compatibility note:

- TrainSet V1 admission and manifest generation should remain additive to current frozen sample outputs
- the manifest should not rewrite upstream files or rename upstream fields

## 5. Known Script Output Artifact Names

Confirmed from `scripts/data/build_manifest.py`:

- `manifest.jsonl`
- `manifest_rejected.jsonl`
- `build_summary.json`

Confirmed from `scripts/data/check_dataset_consistency.py`:

- `consistency_report.json`
- `consistency_report.md`
- `summary.json`

Registry decision:

- these names are current known public output artifacts for the documented data-manifest path

## 6. Known Stable CLI Surfaces

Confirmed from `scripts/data/build_manifest.py`:

- `--data-root`
- `--input-roots`
- `--out-dir`
- `--manifest-name`
- `--rejected-name`
- `--summary-name`
- `--limit`

Confirmed from `scripts/data/check_dataset_consistency.py`:

- `--data-root`
- `--manifest`
- `--out-dir`
- `--report-json-name`
- `--report-md-name`
- `--summary-name`
- `--example-limit`
- `--strict`

Registry decision:

- the data-manifest and consistency-check CLI surfaces above should be treated as current stable public script surfaces

## 7. Uncertain / Needs Confirmation

The following surfaces are intentionally not promoted to confirmed frozen status by this registry:

- inference-side CLI surfaces beyond what current frozen docs explicitly define
- nested schemas inside `env.json`, `forms.json`, `net_summary.json`, `rule_labels.json`, and `manual_labels.json`
- exact allowed enumerations for all weak-label fields beyond what the frozen docs state narratively
- capture-script CLI stability as a frozen public contract
- nested structure under `ingest_metadata`
- nested redirect-entry schema inside `redirect_chain`
- any public artifact produced only by local habit, chat context, or undocumented operator convention

Default rule:

- if a later task needs one of these surfaces to become enforceable, freeze it explicitly in a dedicated doc or versioned spec before adding stricter automated checks

## 8. P0 Harness Enforcement Boundary

The P0 harness checks introduced in this phase should enforce only:

- selected required file names for a sample directory
- selected top-level keys for `meta.json`, `url.json`, and `auto_labels.json`
- TrainSet V1 minimum manifest fields and boolean presence/usability flags
- structural completeness of task and handoff docs

The P0 harness should not claim to enforce:

- full semantic schema validity
- nested object compatibility
- enum-level compatibility across all fields
- training or inference behavior correctness
- capture pipeline correctness

