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
- 抓取环境中已经安装并可用 `playwright-stealth`
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

### 5.2 ????

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

### 5.3 ????????
- ?????????????
- ???????? `benign_capture_run.json`
- ?????????? capture ???????
- `meta.json` ????? `ingest_metadata` ??

### 5.4 benign ?????????

???? recovery ??????????????
????? benign ?????????????????????? Tranco ???????????????????????? URL ?????

???????

- ?? URL ????? supervised ??????? `skip`
- ?????????????????????????
- ???? benign ??????????? Tranco ??
- ?????????????????? recovery ????????

### 5.5 benign 单 URL 卡住时的 supervised 模式

默认 benign runner 还是“一次拉起一个 capture 子进程跑完整批次”。
只有在你显式加了下面这两个参数之一时，runner 才会切到 supervised 模式：

- `--interactive_skip`
- `--url_hard_timeout_ms <毫秒>`

supervised 模式下，runner 会按 URL 逐条拉起 capture 子进程。
这样当前 URL 如果卡住，你可以在终端输入：

```text
skip
```

然后只终止当前 URL，继续后面的站点。

如果你还想给每条 URL 一个硬上限，可以再加：

```powershell
--url_hard_timeout_ms 120000
```

示例：

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000
```

批次结束后，`benign_capture_run.json` 会额外记录：

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `all_success`
- `skipped_urls`
- `timed_out_urls`
- `results`

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

### 7.1 PT `verified_online.csv` 按确认时间导出 URL-only CSV

如果你的输入不是 feed，而是本地的 PT `verified_online.csv`，并且你只想先按 `verification_time` 截出某一天及之后的 URL，再单独抓取，可以用：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv
```

脚本启动后会先提示你输入：

```text
2026/3/27
```

规则：

- 按 `verification_time` 的 UTC 日期做过滤
- 选中范围是“输入日期当天及之后”
- 一次运行同时输出：
  - 一份 URL-only CSV，只有 `url` 列
  - 一份一行一个 URL 的 TXT
- 默认输出到 `<WARDEN_ROOT>\data\processed\pt_csv_exports\`

如果你想指定输出路径：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

如果你不显式给 `--output_txt`，默认会在 CSV 同目录生成同名 `.txt` 文件。

拿到 TXT 后直接抓：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt `
  --source phishtank `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

也就是完整 PT 本地流程是：

1. `export_phishtank_verified_urls.py`
2. `run_malicious_capture.py --input_path ...`

如果你手头已经有旧的 URL-only CSV，没有对应 TXT，再用备用脚本补转：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\convert_url_csv_to_txt.py `
  --input_csv <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
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

### 9.1 `playwright` 或 `playwright-stealth` 导入失败

说明运行环境没准备好，不是上层脚本参数错了。先修环境，再重跑。

常见修法：

```powershell
python -m pip install playwright
python -m pip install playwright-stealth
playwright install
```

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

### 9.4 `Timeout 25000ms exceeded` 但浏览器里看起来又能打开

这通常不代表页面真的完全打不开，更常见的是：

- 旧版 `page.goto(..., wait_until="load")` 太苛刻，而页面主体其实已经出来了
- 当前抓取环境的 IP / 区域 / 网络路径比你手工打开网页时更慢
- 抓取浏览器和手工浏览器并不在同一条网络路径上
- Google / consent.google 这类站点还可能先卡在 consent 或 bot 检测前置页

当前默认 hardening 已内建：

- 默认导航超时已放宽到 `60000ms`
- 默认 `goto_wait_until` 已改为 `commit`
- 导航后会再等一次 `domcontentloaded` 和短暂 hydration
- Google 域名会自动尝试 consent 处理
- 浏览器页创建后默认启用 stealth

当前 runner 和 capture 脚本仍支持以下可选参数：

- `--nav_timeout_ms`
- `--proxy_server`
- `--proxy_username`
- `--proxy_password`
- `--disable_route_intercept`
- `--goto_wait_until`

建议顺序：

1. 先直接用新的默认配置重试，不要先改一堆参数
2. 如果报的是 `net::ERR_ABORTED` 且卡在 `wait_until="commit"`，先做一个极小批次对照并加 `--disable_route_intercept`
3. 如果同类站点还是持续 timeout，再显式指定 `--goto_wait_until domcontentloaded` 或 `--goto_wait_until networkidle` 做小批对照
4. 再考虑只放宽超时
5. 代理保持可选开关，不要直接改成默认强制开启

示例：malicious

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000
```

如果你要直接改成显式的更宽松导航等待模式：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000 `
  --goto_wait_until networkidle
```

如果你看到的是 `net::ERR_ABORTED`，先优先做这个对照：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept
```

示例：benign

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --nav_timeout_ms 60000 `
  --proxy_server http://127.0.0.1:7890
```

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
- `playwright-stealth` must already be installed and usable in the capture environment.
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

### 5.4 What to do if benign sample count is still short

Do not treat recovery-based second-pass recapture as the default operator workflow.
For the current Warden operator path, if benign sample count is still short after a run, prefer preparing another fresh benign input batch and continuing capture.

In practice this means:

- keep the current batch outputs as they are,
- use supervised benign mode with `skip` if a single site stalls,
- if the final benign count is still not enough, expand with more Tranco batches instead of trying to salvage every missing URL from the interrupted batch.

This keeps the workflow simple and auditable:

- stalled URLs do not block the whole batch,
- operators do not need to classify every failure into timeout / 403 / 404 / partial-leftover buckets before continuing,
- additional benign volume comes from fresh Tranco coverage rather than uncertain second-pass retries.

### 5.5 Supervised benign mode for stuck URLs

The default benign runner still uses one capture subprocess for the full batch.
It switches into supervised mode only when you explicitly enable one of these flags:

- `--interactive_skip`
- `--url_hard_timeout_ms <milliseconds>`

In supervised mode, the benign runner launches one capture worker per URL.
If the current URL gets stuck, type this in the terminal:

```text
skip
```

That aborts only the current URL and continues with the remaining URLs.
If the worker was killed while it was already writing sample files, a partial sample directory may remain under `output_root`.
Current operator guidance is still to continue the batch with `skip`, and if benign volume remains short after the run, add more Tranco input batches rather than treating leftover partial directories as a default recovery workflow.

If you also want a hard ceiling per URL, add:

```powershell
--url_hard_timeout_ms 120000
```

Example:

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000
```

When supervised mode is used, `benign_capture_run.json` records these additive fields:

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `all_success`
- `skipped_urls`
- `timed_out_urls`
- `results`

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

### 6.4A Supervised malicious mode for stuck URLs

The default malicious runner still uses the current grouped-subprocess batch mode.
It switches into supervised mode only when you explicitly enable one of these flags:

- `--interactive_skip`
- `--url_hard_timeout_ms <milliseconds>`

In supervised mode, the malicious runner launches one capture worker per URL.
If the current URL gets stuck, type this in the terminal:

```text
skip
```

That aborts only the current malicious URL and continues with the remaining malicious URLs.

If you also want a hard ceiling per URL, add:

```powershell
--url_hard_timeout_ms 120000
```

Unlike the benign recovery path, malicious does not preserve partial leftovers for later recovery.
If the current malicious URL is skipped, times out, or fails, any sample directories newly created during that URL attempt are deleted immediately.

Example:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

When supervised mode is used, `malicious_capture_run.json` records these additive fields:

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `skipped_urls`
- `timed_out_urls`
- `deleted_partial_sample_dirs`
- `results`

Important note:

- In supervised malicious runs, `results[*].status = "success"` only means the child capture process exited with code `0` and was not operator-aborted or hard-timed-out.
- Do not treat supervised `malicious_capture_run.json` as the authoritative malicious sample-count source for later experiments. Authoritative malicious counting must come from discovered sample directories and downstream cluster records.

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

### 7.1 PT `verified_online.csv` to URL-only CSV by verification date

If your input is not a public feed but a local PT `verified_online.csv`, and you first want a URL-only CSV filtered by PT confirmation time before later capture, use:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv
```

The script will first prompt for a date such as:

```text
2026/3/27
```

Rules:

- filtering is based on the UTC calendar date of `verification_time`
- the selected range is inclusive of the entered date
- one run writes both:
  - a URL-only CSV with one column: `url`
  - a one-URL-per-line TXT file for direct capture
- the default output directory is `<WARDEN_ROOT>\data\processed\pt_csv_exports\`

If you want an explicit output path:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

If you do not pass `--output_txt`, the script will create a sibling `.txt` path next to the CSV automatically.

Then run capture directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt `
  --source phishtank `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

That means the full local PT workflow is:

1. `export_phishtank_verified_urls.py`
2. `run_malicious_capture.py --input_path ...`

If you already have an older URL-only CSV without a matching TXT, the fallback helper still exists:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\convert_url_csv_to_txt.py `
  --input_csv <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
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

### 9.1 `playwright` or `playwright-stealth` import failure

This is an environment problem, not an upper-layer CLI problem.
Fix the runtime environment first, then rerun the capture command.

Typical recovery commands:

```powershell
python -m pip install playwright
python -m pip install playwright-stealth
playwright install
```

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

### 9.4 `Timeout 25000ms exceeded` even though the page seems to open manually

This does not necessarily mean the site is truly unreachable.
The more common cases are:

- the older `page.goto(..., wait_until="load")` criterion was too strict even though the page body was already usable,
- the site is slower on the current IP / region / network path used by the capture environment,
- the capture browser and your manual browser are not using the same network path,
- Google / consent.google may insert a consent or anti-bot front page before the useful content.

The default hardening path is now built in:

- default navigation timeout is `60000ms`,
- default `goto_wait_until` is `commit`,
- the browser waits for `domcontentloaded` plus a short hydration delay after navigation,
- Google domains attempt consent handling automatically,
- stealth is applied by default on page creation.

The current runners and capture script still support these optional flags:

- `--nav_timeout_ms`
- `--proxy_server`
- `--proxy_username`
- `--proxy_password`
- `--disable_route_intercept`
- `--goto_wait_until`

Recommended order of operations:

1. first retry with the new built-in defaults before adding more overrides,
2. if the failure is `net::ERR_ABORTED` while waiting for `commit`, first run a tiny comparison batch with `--disable_route_intercept`,
3. if timeouts still cluster on the same sites, explicitly test `--goto_wait_until domcontentloaded` or `--goto_wait_until networkidle` on a small batch,
4. only then extend timeouts further if needed,
5. keep proxy usage optional instead of switching the whole pipeline to proxy-by-default.

Example: malicious

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000
```

If you want to force an even looser navigation mode directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000 `
  --goto_wait_until networkidle
```

If the specific failure is `net::ERR_ABORTED`, try this before changing more knobs:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_ROOT>\data\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept
```

Example: benign

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_ROOT>\data\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_ROOT>\data\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --nav_timeout_ms 60000 `
  --proxy_server http://127.0.0.1:7890
```

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
