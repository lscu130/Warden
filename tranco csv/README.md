# Tranco Batch Usage

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读与快速操作参考。

### 这是什么

- 这里是 `C:/Users/20516/Desktop/tranco_NN99W.csv` 的策略对齐切分结果。
- 源文件本身没有表头，原始格式是 `rank,domain`。
- 这里不是把 `1,000,000` 行全切成 `1,000` 批，而是按 `Warden_BENIGN_SAMPLING_STRATEGY_V1.md` 的 Tranco 主榜单配额先抽 `20,000` 条，再按 `1000` 一批切成 `20` 个批次。
- 每个批次 `*.csv` 都规范化成了三列：`rank,domain,url`。
- 每个 `*_urls.txt` 都是一行一个 URL，可直接用于 benign 抓取。
- `split_summary.json` 记录了总行数、bucket 配额、批次数和每个批次的路径。

### 当前采用的配额

- `top_1_10000`：`2000`
- `top_10001_100000`：`7000`
- `top_100001_500000`：`8000`
- `top_500001_1000000`：`3000`

### 最常用的两种用法

#### 用法 A：按 TXT 直接抓取，最省事

```powershell
python E:/Warden/scripts/data/benign/run_benign_capture.py `
  --input_path "E:/Warden/tranco csv/tranco_top_1_10000_batch_0001_urls.txt" `
  --output_root E:/Warden/data/raw/benign/2026-03-23_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en
```

#### 用法 B：按 CSV 直接抓取

```powershell
python E:/Warden/scripts/data/benign/run_benign_capture.py `
  --input_path "E:/Warden/tranco csv/tranco_top_1_10000_batch_0001.csv" `
  --input_format csv `
  --csv_url_column url `
  --output_root E:/Warden/data/raw/benign/2026-03-23_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en
```

### 说明

- 当前切分只实现了 rank-bucket 配额层。
- page type、category、language、quality filtering、safety veto 和 hard-benign 仍属于后续抓取与筛选阶段。

## English Version

## What This Folder Contains

- This folder contains the strategy-aligned split outputs from `C:\Users\20516\Desktop\tranco_NN99W.csv`.
- The source file itself had no header and used raw `rank,domain` rows.
- This is not a naive full split of all `1,000,000` source rows.
- Instead, it first selects `20,000` Tranco main-pool candidates according to `Warden_BENIGN_SAMPLING_STRATEGY_V1.md`, and then writes them as `20` batches of `1000`.
- Each batch `*.csv` has been normalized into `rank,domain,url`.
- Each `*_urls.txt` contains one benign URL per line for direct capture usage.
- `split_summary.json` is the authoritative summary of quotas, batch counts, and paths.

## Current Quotas

- `top_1_10000`: `2000`
- `top_10001_100000`: `7000`
- `top_100001_500000`: `8000`
- `top_500001_1000000`: `3000`

## Current Batch Count

- total selected samples: `20000`
- total batches: `20`
- batch size: `1000`

## The Two Most Useful Workflows

### Workflow A: Direct benign capture from TXT, simplest path

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0001_urls.txt" `
  --output_root E:\Warden\data\raw\benign\2026-03-23_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en
```

### Workflow B: Direct benign capture from CSV

The batch CSV files already include a `url` column, so they can be used directly:

```powershell
python E:\Warden\scripts\data\benign\run_benign_capture.py `
  --input_path "E:\Warden\tranco csv\tranco_top_1_10000_batch_0001.csv" `
  --input_format csv `
  --csv_url_column url `
  --output_root E:\Warden\data\raw\benign\2026-03-23_tranco_top_1_10000_batch_0001 `
  --source tranco `
  --rank_bucket top_1_10000 `
  --page_type homepage `
  --language en
```

## How To Set `rank_bucket`

- `tranco_top_1_10000_batch_0001.*` -> `top_1_10000`
- `tranco_top_10001_100000_batch_0001.*` -> `top_10001_100000`
- `tranco_top_100001_500000_batch_0001.*` -> `top_100001_500000`
- `tranco_top_500001_1000000_batch_0001.*` -> `top_500001_1000000`

## Important Note

- This split only implements the rank-bucket quota layer.
- The secondary stratification requirements in the strategy doc, such as page type, category, language, and hard-benign handling, still belong to later capture and filtering stages.

