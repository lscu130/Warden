# Warden_DATA_INGEST_RUNBOOK_V1

## 中文版（摘要）

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文区块供人类快速阅读和日常操作导览。涉及精确命令、路径、字段、接口或历史事实时，以英文版为准。

### 使用说明

- 本文档是日常采样抓取的操作手册，覆盖 benign 抓取、malicious feed 导入、malicious 抓取、聚类、train/reserve、review 和 exclusion 产物生成。
- 命令中的 `<WARDEN_ROOT>`、`<WARDEN_DATA_ROOT>`、`<RUN_DATE>`、`<BATCH_NAME>` 都是占位符，执行前要替换成实际路径和批次名。
- 当前本地运行期数据根默认是 `E:\WardenData`；repo 内 `E:\Warden\data\README.md` 只保留说明文档。
- 如果旧 handoff 或旧命令里仍写着 `<WARDEN_ROOT>\data\...`，当前执行时应替换成 `<WARDEN_DATA_ROOT>\...`。

## 1. 目的

这份 runbook 解决日常数据抓取怎么跑、跑完看什么、卡住时怎么处理。
重点覆盖：

- 小规模 benign URL 抓取。
- 每日 malicious 批量抓取，常见目标量级约 300 条 URL。
- OpenPhish Community / PhishTank public feed 导入。
- 抓取完成后的 cluster、train/reserve、review、exclusion 产物生成。
- Windows 下 JSONL、BOM、timeout、supervised skip 等常见坑。

## 2. 相关脚本

- benign 抓取入口：`scripts/data/benign/run_benign_capture.py`
- 恶意 public feed 导入：`scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious 抓取入口：`scripts/data/malicious/run_malicious_capture.py`
- PhishTank verified CSV URL 导出：`scripts/data/malicious/export_phishtank_verified_urls.py`
- URL-only CSV 转 TXT：`scripts/data/malicious/convert_url_csv_to_txt.py`
- 旧 HTML 转 JSON：`scripts/data/maintenance/convert_legacy_html_to_json.py`
- malicious 聚类：`scripts/data/malicious/build_malicious_clusters.py`
- train / reserve 划分：`scripts/data/malicious/build_malicious_train_pool.py`
- review manifest：`scripts/data/maintenance/build_dedup_review_manifest.py`
- exclusion list：`scripts/data/maintenance/build_training_exclusion_lists.py`

## 3. 前置条件

- `python` 可以正常运行。
- 抓取环境已经安装并可用 `playwright`。
- 抓取环境已经安装并可用 `playwright-stealth`。
- 建议在仓库根目录执行命令。
- 所有示例路径都要替换成当前机器上的真实路径。

建议先跑：

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py --help
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py --help
```

## 4. 路径约定

建议每次运行都建立独立批次目录，不要把每天的中间产物混在一起。

占位符：

- `<WARDEN_ROOT>`：例如 `E:\Warden`
- `<WARDEN_DATA_ROOT>`：例如 `E:\WardenData`
- `<RUN_DATE>`：例如 `2026-03-24`
- `<BATCH_NAME>`：例如 `daily300`

当前目录约定：

- benign 输入：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\`
- malicious feed 中间产物：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\`
- malicious cluster 中间产物：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool 中间产物：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\`
- malicious review 产物：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review\`
- malicious exclusion 产物：`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions\`
- benign 输出根：`<WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious 输出根：`<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. 小规模 benign 抓取

准备 URL 文本：

```text
<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt
```

每行一个 URL。运行：

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

输出后优先检查：

- `<WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME>\benign_capture_run.json`
- 每个样本目录中的 `meta.json`、HTML JSON wrapper、截图和 trace 类产物。

如果单个 benign URL 卡住，可以显式启用 supervised 模式：

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000
```

运行时输入 `skip` 只跳过当前 URL，后续 URL 继续。

## 6. 每日 malicious public feed 流程

先导入 public malicious feeds：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed
```

该脚本默认拉取：

- OpenPhish Community：`https://openphish.com/feed.txt`
- PhishTank：`https://data.phishtank.com/data/online-valid.csv`

关键输出：

- `malicious_feed_candidates.jsonl`
- `malicious_feed_candidates.txt`
- `malicious_feed_summary.json`

不要用 `Get-Content | Set-Content` 直接切 JSONL。Windows 下容易把 BOM 写进第一行。需要抽取 daily-300 manifest 时，按英文版 `Create a daily-300 manifest` 小节里的 Python 片段执行。

运行 malicious 抓取：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

先检查：

```text
<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json
```

重点字段：`all_success`、`returncodes`、`skipped_urls`、`timed_out_urls`、`results`。

## 7. malicious 后处理

聚类：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_clusters.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters
```

构建 train / reserve pool：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool `
  --family_share_cap 0.10
```

生成 review manifest：

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_dedup_review_manifest.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review
```

生成 exclusion list：

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions
```

## 8. 手工 malicious URL 和 PhishTank 本地 CSV

如果已有 URL 文本，可跳过 feed ingest 直接抓取：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

如果输入是本地 PhishTank `verified_online.csv`，先按 `verification_time` 导出 URL-only CSV / TXT：

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

再把 TXT 交给 `run_malicious_capture.py --input_path`。

## 9. 常见问题

- JSONL 切分不要用 PowerShell `Get-Content | Set-Content`，优先用 Python 读写并显式指定 `encoding="utf-8"`。
- 如果 `Timeout 25000ms exceeded` 但手工浏览器能打开，先用当前默认配置重试；再小批量对照 `--disable_route_intercept`、`--goto_wait_until domcontentloaded` 或 `--goto_wait_until networkidle`。
- 代理保持可选开关，不要直接改成默认强制开启。
- 旧 `.html` 样本目录需要转换时，用 `scripts/data/maintenance/convert_legacy_html_to_json.py`，具体命令以英文版为准。
- 批次结束后优先检查 `*_capture_run.json`、cluster summary、pool summary、review manifest 和 exclusion 输出。

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
- legacy HTML-to-JSON conversion: `scripts/data/maintenance/convert_legacy_html_to_json.py`
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
- `<WARDEN_DATA_ROOT>`: for example `E:\WardenData`
- `<RUN_DATE>`: for example `2026-03-24`
- `<BATCH_NAME>`: for example `daily300`

Current local default contract:

- the runtime data root is `E:\WardenData`
- `E:\Warden\data\README.md` remains repo-local documentation only
- if an older handoff or older command still shows `<WARDEN_ROOT>\data\...`, replace that path with `<WARDEN_DATA_ROOT>\...` when you actually run it

Suggested directories:

- benign input: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\`
- malicious feed intermediates: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\`
- malicious clustering outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\`
- malicious review / exclusion outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review\` and `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions\`
- benign output root: `<WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious output root: `<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. Common Scenario A: Small Benign Capture

### 5.1 Prepare a UTF-8 URL file

Example path:

`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt`

One URL per line.

### 5.2 Run the benign capture command

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
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

HTML payload note:

- newly captured HTML payloads are stored as JSON wrappers such as `html_rendered.json` and `html_raw.json`
- older sample directories may still contain legacy `.html` files until they are migrated
- use `scripts/data/maintenance/convert_legacy_html_to_json.py` when you need to convert old sample directories

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
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
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
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed
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

src = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates.jsonl")
dst = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl")

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
  --feed_manifest <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 6.4 First artifact to inspect

Inspect:

`<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json`

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
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
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
  --input_roots <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters
```

Outputs:

- `malicious_cluster_records.jsonl`
- `malicious_cluster_summary.json`

### 6.6 Build train/reserve pool decisions

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool `
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
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review
```

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions
```

## 7. Common Scenario C: Manual Small Malicious URL Set

If you already have a text file of malicious URLs and do not want to ingest public feeds first:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
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
- the default output directory is `<WARDEN_DATA_ROOT>\processed\pt_csv_exports\`

If you want an explicit output path:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

If you do not pass `--output_txt`, the script will create a sibling `.txt` path next to the CSV automatically.

Then run capture directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt `
  --source phishtank `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

That means the full local PT workflow is:

1. `export_phishtank_verified_urls.py`
2. `run_malicious_capture.py --input_path ...`

If you already have an older URL-only CSV without a matching TXT, the fallback helper still exists:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\convert_url_csv_to_txt.py `
  --input_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

### 7.2 Convert legacy sample HTML files to JSON wrappers

If you have older sample directories that still contain legacy `.html` capture artifacts, convert them with:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign
```

If you want a report only without writing files:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign `
  --dry_run
```

In this mode the script only reports `would_convert` / `would_overwrite` style counts.
It does not write any JSON files.

If you want to remove the legacy `.html` files after successful conversion:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign `
  --delete_original_html
```

If you run the conversion without `--delete_original_html`, the new JSON wrappers are written and the old `.html` files are intentionally kept.

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
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000
```

If you want to force an even looser navigation mode directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000 `
  --goto_wait_until networkidle
```

If the specific failure is `net::ERR_ABORTED`, try this before changing more knobs:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept
```

Example: benign

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
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

