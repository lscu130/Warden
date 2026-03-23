# Warden_DATA_INGEST_RUNBOOK_V1

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档是日常采样抓取的操作手册，不是架构设计文档。
- 文中命令使用绝对路径占位符，你只需要把 `<WARDEN_ROOT>`、`<RUN_DATE>`、`<BATCH_NAME>` 之类占位符替换成你自己的实际路径和批次名。
- 若中英内容冲突，以英文版为准。

## 1. 目的

这份 runbook 解决的是“平常怎么用”。
重点覆盖：

- 小规模 benign 抓取
- 每日 malicious 批量抓取，尤其是大约 300 条
- 抓取完成后的 cluster / train-reserve / review / exclusion 产物生成
- Windows 下常见坑

## 2. 相关脚本

- benign 抓取入口：`scripts/data/benign/run_benign_capture.py`
- 恶意 feed 导入：`scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious 抓取入口：`scripts/data/malicious/run_malicious_capture.py`
- 恶意聚类：`scripts/data/malicious/build_malicious_clusters.py`
- train / reserve 划分：`scripts/data/malicious/build_malicious_train_pool.py`
- review manifest：`scripts/data/maintenance/build_dedup_review_manifest.py`
- exclusion list：`scripts/data/maintenance/build_training_exclusion_lists.py`

## 3. 前置条件

- 可以正常运行 `python`
- 抓取环境中已经安装并可用 `playwright`
- 在仓库根目录执行命令最省事
- 例子里的绝对路径要替换成你自己的真实路径

建议先跑：

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py --help
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py --help
```

## 4. 路径约定

建议每次运行都单独建一个批次目录，不要把每天的临时中间结果全混在一起。

示例占位：

- `<WARDEN_ROOT>`：例如 `E:\Warden`
- `<RUN_DATE>`：例如 `2026-03-24`
- `<BATCH_NAME>`：例如 `daily300`

建议目录：

- benign 输入：`<WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\`
- malicious feed 中间产物：`<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\`
- malicious cluster 中间产物：`<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool 中间产物：`<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\`
- malicious review / exclusion：`<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_review\`、`<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_exclusions\`
- benign 输出根：`<WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious 输出根：`<WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. 常用场景 A：小规模 benign 抓取

### 5.1 准备 URL 文本

准备一个 UTF-8 文本文件，例如：

`<WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt`

每行一个 URL。

### 5.2 运行命令

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

### 5.3 成功后会看到什么

- 输出根目录下生成样本子目录
- 输出根目录下生成 `benign_capture_run.json`
- 每个样本目录里仍然是原 capture 引擎的标准输出
- `meta.json` 里会多一个 `ingest_metadata` 字段

## 6. 常用场景 B：每天抓大约 300 条 malicious

这是最常用的操作流程。

### 6.1 先拉公共 feed

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed
```

生成的关键文件：

- `malicious_feed_candidates.jsonl`
- `malicious_feed_candidates.txt`
- `malicious_feed_summary.json`

### 6.2 从候选里切一个 daily 300 manifest

不要用 `Get-Content | Set-Content` 直接切 JSONL，Windows 下容易把 BOM 带进第一行。

用下面这个 Python 片段最稳：

```powershell
@'
import json
import random
from pathlib import Path

src = Path(r"<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates.jsonl")
dst = Path(r"<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl")

rows = []
with src.open("r", encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        text = line.lstrip("\ufeff").strip()
        if not text:
            continue
        rows.append(json.loads(text))

random.seed(12345)
if len(rows) > 300:
    rows = random.sample(rows, 300)

with dst.open("w", encoding="utf-8", newline="\n") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("selected_rows =", len(rows))
print("output =", dst)
'@ | python -
```

如果你不想随机抽样，也可以把 `random.sample(rows, 300)` 改成 `rows[:300]`。

### 6.3 跑 malicious 抓取

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 6.4 成功后先检查什么

先看：

- `<WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json`

重点字段：

- `all_success`
- `returncodes`

如果 `all_success` 为 `true`，说明这批 capture 进程级别是成功的。

### 6.5 对这批 malicious 样本做 cluster

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_clusters.py `
  --input_roots <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters
```

生成：

- `malicious_cluster_records.jsonl`
- `malicious_cluster_summary.json`

### 6.6 构建 train / reserve pool

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool `
  --family_share_cap 0.10
```

生成：

- `pool_decisions.jsonl`
- `train_pool_manifest.jsonl`
- `reserve_pool_manifest.jsonl`
- `pool_summary.json`

### 6.7 生成 review / exclusion 产物

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_dedup_review_manifest.py `
  --clusters_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_review
```

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_exclusions
```

## 7. 常用场景 C：只想手工抓一小批 malicious URL

如果你已经有一个恶意 URL 文本文件，不想先走 feed ingest，也可以直接跑：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

## 8. 每次运行后建议人工检查的文件

- benign：`benign_capture_run.json`
- malicious：`malicious_capture_run.json`
- cluster：`malicious_cluster_summary.json`
- pool：`pool_summary.json`
- 任取一个样本目录里的 `meta.json`

重点看：

- `returncode` / `all_success`
- `ingest_metadata`
- `total_records`
- `train_count` / `reserve_count`
- `family_share_cap`

## 9. 常见问题

### 9.1 `playwright` 导入失败

说明运行环境没准备好，不是上层脚本参数错了。先修环境，再重跑。

### 9.2 JSONL 首行 BOM 导致 “line 1 is not valid JSON”

这通常是手工切文件时用了：

```powershell
Get-Content ... | Set-Content ...
```

处理方式：

- 优先用上面的 Python 片段切 JSONL
- 不要用 shell 文本管道硬切 JSONL

### 9.3 输出目录写错

最常见问题不是脚本坏了，而是 `--output_root` 指到了旧目录，结果你在错误的地方找产物。

## 10. 最小日常命令清单

### 每天抓 300 malicious

1. `ingest_public_malicious_feeds.py`
2. Python 片段切 300 条 manifest
3. `run_malicious_capture.py`
4. `build_malicious_clusters.py`
5. `build_malicious_train_pool.py`
6. `build_dedup_review_manifest.py`
7. `build_training_exclusion_lists.py`

### 偶尔补一批 benign

1. 准备 `benign_urls.txt`
2. `run_benign_capture.py`
3. 检查 `benign_capture_run.json`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat this English section as the authoritative version. The Chinese section above is for human readers and quick orientation.

## 1. Purpose

This document is an operational runbook, not an architecture document.
It explains normal day-to-day usage of the current ingest scripts, especially:

- small benign capture runs,
- daily malicious batch capture, especially a roughly 300-URL batch,
- post-capture cluster / pool / review / exclusion generation,
- common Windows pitfalls.

## 2. Relevant Scripts

- benign capture entry: `scripts/data/benign/run_benign_capture.py`
- malicious public-feed ingest: `scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious capture entry: `scripts/data/malicious/run_malicious_capture.py`
- malicious clustering: `scripts/data/malicious/build_malicious_clusters.py`
- train/reserve routing: `scripts/data/malicious/build_malicious_train_pool.py`
- dedup review manifest: `scripts/data/maintenance/build_dedup_review_manifest.py`
- training exclusion list: `scripts/data/maintenance/build_training_exclusion_lists.py`

## 3. Preconditions

- `python` must be available.
- `playwright` must already be installed and usable in the capture environment.
- It is simplest to run commands from the repository root.
- Replace all absolute-path placeholders with your real paths before running commands.

Recommended quick checks:

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py --help
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py --help
```

## 4. Suggested Path Convention

Use a separate batch directory for each operational run instead of mixing all temporary artifacts together.

Suggested placeholders:

- `<WARDEN_ROOT>`: for example `E:\Warden`
- `<RUN_DATE>`: for example `2026-03-24`
- `<BATCH_NAME>`: for example `daily300`

Suggested directories:

- benign input: `<WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\`
- malicious feed intermediates: `<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\`
- malicious clustering outputs: `<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool outputs: `<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\`
- malicious review / exclusion outputs: `<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_review\` and `<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_exclusions\`
- benign output root: `<WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious output root: `<WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. Common Scenario A: Small Benign Capture

### 5.1 Prepare a UTF-8 URL file

Example path:

`<WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt`

One URL per line.

### 5.2 Run the benign capture command

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

### 5.3 Expected outputs

- sample subdirectories under the output root,
- `benign_capture_run.json` under the output root,
- the normal capture-engine files inside each sample directory,
- an additive `ingest_metadata` object inside `meta.json`.

## 6. Common Scenario B: Daily Malicious Batch of Roughly 300 URLs

This is the main operational workflow.

### 6.1 Ingest public malicious feeds

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed
```

Key outputs:

- `malicious_feed_candidates.jsonl`
- `malicious_feed_candidates.txt`
- `malicious_feed_summary.json`

### 6.2 Create a daily-300 manifest

Do not slice JSONL with `Get-Content | Set-Content`.
On Windows, that often injects a BOM into the first line and breaks JSONL parsing.

Use this Python snippet instead:

```powershell
@'
import json
import random
from pathlib import Path

src = Path(r"<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates.jsonl")
dst = Path(r"<WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl")

rows = []
with src.open("r", encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        text = line.lstrip("\ufeff").strip()
        if not text:
            continue
        rows.append(json.loads(text))

random.seed(12345)
if len(rows) > 300:
    rows = random.sample(rows, 300)

with dst.open("w", encoding="utf-8", newline="\n") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("selected_rows =", len(rows))
print("output =", dst)
'@ | python -
```

If you want a deterministic head-300 instead of random sampling, replace `random.sample(rows, 300)` with `rows[:300]`.

### 6.3 Run the malicious capture

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 6.4 First artifact to inspect

Inspect:

`<WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json`

Key fields:

- `all_success`
- `returncodes`

If `all_success` is `true`, the batch-level capture process succeeded.

### 6.5 Build malicious clusters

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_clusters.py `
  --input_roots <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters
```

Outputs:

- `malicious_cluster_records.jsonl`
- `malicious_cluster_summary.json`

### 6.6 Build train/reserve pool decisions

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool `
  --family_share_cap 0.10
```

Outputs:

- `pool_decisions.jsonl`
- `train_pool_manifest.jsonl`
- `reserve_pool_manifest.jsonl`
- `pool_summary.json`

### 6.7 Build review and exclusion artifacts

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_dedup_review_manifest.py `
  --clusters_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_review
```

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_exclusions
```

## 7. Common Scenario C: Manual Small Malicious URL Set

If you already have a text file of malicious URLs and do not want to ingest public feeds first:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

## 8. Files To Inspect After Each Run

- benign: `benign_capture_run.json`
- malicious: `malicious_capture_run.json`
- clustering: `malicious_cluster_summary.json`
- pool routing: `pool_summary.json`
- at least one sample `meta.json`

Key fields to inspect:

- `returncode` / `all_success`
- `ingest_metadata`
- `total_records`
- `train_count` / `reserve_count`
- `family_share_cap`

## 9. Common Problems

### 9.1 `playwright` import failure

This is an environment problem, not an upper-layer CLI problem.
Fix the runtime environment first, then rerun the capture command.

### 9.2 JSONL first-line BOM causing `line 1 is not valid JSON`

This usually happens when a JSONL file was sliced with:

```powershell
Get-Content ... | Set-Content ...
```

Preferred fix:

- use the Python snippet above to create the subset manifest,
- do not slice JSONL with shell text piping.

### 9.3 Wrong output root

One of the most common operational mistakes is simply checking the wrong directory because `--output_root` pointed somewhere else than expected.

## 10. Minimal Daily Command Checklist

### Daily malicious batch of about 300 URLs

1. `ingest_public_malicious_feeds.py`
2. Python snippet to create a 300-row manifest
3. `run_malicious_capture.py`
4. `build_malicious_clusters.py`
5. `build_malicious_train_pool.py`
6. `build_dedup_review_manifest.py`
7. `build_training_exclusion_lists.py`

### Occasional benign batch

1. prepare `benign_urls.txt`
2. `run_benign_capture.py`
3. inspect `benign_capture_run.json`
