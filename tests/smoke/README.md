# tests/smoke README

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本目录用于保存 Warden Harness P0 的最小 smoke baseline 骨架。
- 当前不是完整数据集，也不是 benchmark 套件。
- 若格式约定与命令说明存在冲突，以英文版为准。

### 摘要

- 当前只提交一个 example manifest record 和本说明文档。
- `golden_manifest.example.json` 是单条 JSON 对象，不是 JSONL。
- 本目录允许用 repo 里真实 sample_dir 做本地只读 spot-check，但不把真实样本固化进这里。

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Smoke Baseline Skeleton

This directory holds the minimal smoke-baseline skeleton for Warden Harness P0.

It is intentionally small.
It does not define a full benchmark dataset, a training fixture suite, or a corpus-level regression framework.

## 1. Current Contents

- `golden_manifest.example.json`
- this README

## 2. Artifact Format

`golden_manifest.example.json` is a single JSON object representing one example TrainSet V1 manifest record.

It is not JSONL.
This is intentional because the P0 schema guard validates one manifest record at a time under `--kind manifest_record`.

## 3. Expected Fields

The example record is expected to include at least:

- `sample_id`
- `sample_dir`
- `label_hint`
- `crawl_time_utc`
- `http_status`
- `input_url`
- `final_url`
- `has_visible_text`
- `has_forms`
- `has_html_rendered`
- `has_html_raw`
- `has_screenshot_full`
- `has_rule_labels`
- `has_manual_labels`
- `usable_for_text`
- `usable_for_vision`
- `usable_for_multimodal`

These fields align with the TrainSet V1 minimum manifest surface documented in `docs/data/TRAINSET_V1.md`.

## 4. How To Use It

Example command:

```bash
python scripts/ci/check_schema_compat.py --kind manifest_record --path tests/smoke/golden_manifest.example.json
```

Optional local read-only spot-check on one real sample directory:

```bash
python scripts/ci/check_schema_compat.py --kind sample_dir --path data/raw/benign/2026-04-02_planA_day8_tranco_top_10001_100000_batch_0010/0x7c0.com_20260408T092757Z
```

## 5. Current Non-Goals

This directory does not currently provide:

- a checked-in real manifest corpus
- negative fixtures
- JSONL corpus regression coverage
- training or inference runtime checks
- benchmark scoring

If stricter smoke coverage is needed later, add it under a new task boundary rather than expanding this skeleton ad hoc.
