# PhishTank Batch Usage

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读与快速操作参考。

### 这是什么

- 这里是 `C:\Users\20516\phishtank_2026_only.csv` 的本地切分结果。
- 每个 `*.csv` 批次都是 `500` 行一批，最后一批不足 `500`。
- 每个 `*_urls.txt` 是对应批次的 URL 文本版，一行一个 URL。
- `openphish_empty.txt` 是给 PhishTank-only 本地 ingest 用的空文件。
- `split_summary.json` 记录了总行数、总批次数和每个批次的路径。

### 你最常用的两种用法

#### 用法 A：按 TXT 直接抓取，最省事

如果你就是想抓这一批 PhishTank URL，直接用对应的 `*_urls.txt`：

```powershell
python E:\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "E:\Warden\phishtank csv\phishtank_2026_only_batch_0001_urls.txt" `
  --source phishtank `
  --output_root E:\Warden\data\raw\phish\2026-03-23_phishtank_batch_0001
```

#### 用法 B：按 CSV 走本地 ingest，再抓取

先把这一批 CSV 转成 feed manifest：

```powershell
python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir E:\Warden\data\processed\2026-03-23_phishtank_batch_0001_feed `
  --openphish_input_path "E:\Warden\phishtank csv\openphish_empty.txt" `
  --phishtank_input_path "E:\Warden\phishtank csv\phishtank_2026_only_batch_0001.csv"
```

然后再抓：

```powershell
python E:\Warden\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest E:\Warden\data\processed\2026-03-23_phishtank_batch_0001_feed\malicious_feed_candidates.jsonl `
  --output_root E:\Warden\data\raw\phish\2026-03-23_phishtank_batch_0001
```

### 哪个更适合你

- 只想快点抓：用法 A
- 想保留 feed manifest 和中间产物：用法 B

### 批次数量

- 总数据行数：`15913`
- 总批次数：`32`
- 前 `31` 批每批 `500`
- 第 `32` 批 `413`

## English Version

## What This Folder Contains

- This folder contains the local split outputs from `C:\Users\20516\phishtank_2026_only.csv`.
- Each `*.csv` batch contains `500` rows, except the final short batch.
- Each `*_urls.txt` file contains the same batch as one URL per line.
- `openphish_empty.txt` is an empty file intended for PhishTank-only local ingest.
- `split_summary.json` is the authoritative count and path summary.

## The Two Most Useful Workflows

### Workflow A: Direct capture from TXT, simplest path

If you simply want to capture that batch of PhishTank URLs directly, use the matching `*_urls.txt` file:

```powershell
python E:\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "E:\Warden\phishtank csv\phishtank_2026_only_batch_0001_urls.txt" `
  --source phishtank `
  --output_root E:\Warden\data\raw\phish\2026-03-23_phishtank_batch_0001
```

### Workflow B: Local ingest from CSV first, then capture

First build a local feed manifest from the CSV batch:

```powershell
python E:\Warden\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir E:\Warden\data\processed\2026-03-23_phishtank_batch_0001_feed `
  --openphish_input_path "E:\Warden\phishtank csv\openphish_empty.txt" `
  --phishtank_input_path "E:\Warden\phishtank csv\phishtank_2026_only_batch_0001.csv"
```

Then run capture:

```powershell
python E:\Warden\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest E:\Warden\data\processed\2026-03-23_phishtank_batch_0001_feed\malicious_feed_candidates.jsonl `
  --output_root E:\Warden\data\raw\phish\2026-03-23_phishtank_batch_0001
```

## Which Workflow To Prefer

- Use Workflow A if speed and simplicity matter more than retaining intermediate feed artifacts.
- Use Workflow B if you want the local feed manifest and summary files as auditable intermediates.

## Batch Count

- Total data rows: `15913`
- Total batches: `32`
- First `31` batches: `500` rows each
- Final batch: `413` rows
