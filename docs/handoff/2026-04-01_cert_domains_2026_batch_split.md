# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 CERT 域名 CSV 过滤与分批导出的正式 handoff。
- 若涉及精确列名、计数结果、输出文件名模式或兼容性，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CERT-DOMAINS-2026-BATCH-SPLIT-V1`
- 任务主题：保留 `2026` 年内 CERT 域名并按 `500` 一批导出 TXT
- 当前状态：`DONE`
- 所属模块：Data / External Feed Utility

### 当前交付要点

- 已从 `C:\Users\20516\Downloads\domains.csv` 中筛出 `2026` 年数据。
- 只保留了 `AdresDomeny`，没有改源 CSV。
- 已在 `E:\Warden\cert csv\` 下生成带 `CERT` 前缀的批次 TXT。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-01-cert-domains-2026-batch-split
- Related Task ID: WARDEN-CERT-DOMAINS-2026-BATCH-SPLIT-V1
- Task Title: Filter the provided CERT domains CSV to 2026-only rows and split domains into 500-line TXT batches with CERT in the filenames
- Module: Data / External Feed Utility
- Author: Codex
- Date: 2026-04-01
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.
- Write this Markdown handoff in bilingual form by default: Chinese summary first, full English version second, with English authoritative for exact facts, commands, validation, and compatibility statements.

---

## 1. Executive Summary

Processed the provided `domains.csv` file and kept only rows whose `DataWpisu` falls in calendar year `2026`.

Extracted only the `AdresDomeny` values from those rows and split them into `500`-line TXT batches under `E:\Warden\cert csv\`.
All generated filenames include `CERT` to make the source explicit.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_batch_split.md`.
- Added `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_batch_split.md`.

### Output / Artifact Changes

- Created `130` TXT batch files under `E:\Warden\cert csv\`.
- Output filename pattern:
  - `CERT_2026_only_batch_0001_domains.txt`
  - ...
  - `CERT_2026_only_batch_0130_domains.txt`

---

## 3. Files Touched

- `E:\Warden\cert csv\CERT_2026_only_batch_0001_domains.txt`
- `E:\Warden\cert csv\CERT_2026_only_batch_0130_domains.txt`
- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_batch_split.md`

Optional notes per file:

- The `cert csv` directory now contains the full batch set for this run.
- The generated TXT files contain domains only, one per line.

---

## 4. Behavior Impact

### Expected New Behavior

- There is now a repo-local set of CERT batch TXT files ready for later manual review or downstream use.
- Each file contains at most `500` domains from `2026` rows only.

### Preserved Behavior

- The source CSV was not modified.
- No downstream crawling or capture was run in this task.

### User-facing / CLI Impact

- none

### Output Format Impact

- TXT output only
- one domain per line
- no header row

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This task generated new artifacts only.
It did not modify the source CSV schema or any existing script interface.

---

## 6. Validation Performed

### Commands Run

```bash
Get-Content -Path C:\Users\20516\Downloads\domains.csv -TotalCount 8
python - <<'PY'
import csv
from datetime import datetime
from pathlib import Path

input_path = Path(r'C:\Users\20516\Downloads\domains.csv')
output_dir = Path(r'E:\Warden\cert csv')
batch_size = 500

def parse_year(raw: str) -> int | None:
    value = (raw or '').strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).year
    except ValueError:
        return None

rows = []
with input_path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for record in reader:
        if parse_year(record.get('DataWpisu', '')) != 2026:
            continue
        domain = (record.get('AdresDomeny') or '').strip()
        if not domain:
            continue
        rows.append(domain)

output_dir.mkdir(parents=True, exist_ok=True)
for old in output_dir.glob('CERT_2026_only_batch_*_domains.txt'):
    old.unlink()

batch_count = 0
for idx in range(0, len(rows), batch_size):
    batch_count += 1
    chunk = rows[idx:idx + batch_size]
    path = output_dir / f'CERT_2026_only_batch_{batch_count:04d}_domains.txt'
    path.write_text('\n'.join(chunk) + '\n', encoding='utf-8', newline='\n')

print(f'total_2026_domains={len(rows)}')
print(f'batch_count={batch_count}')
PY
python - <<'PY'
from pathlib import Path
paths = sorted(Path(r'E:\Warden\cert csv').glob('CERT_2026_only_batch_*_domains.txt'))
line_counts = [(p.name, sum(1 for _ in p.open('r', encoding='utf-8'))) for p in paths]
print(f'file_count={len(line_counts)}')
print(f'max_lines={max(c for _, c in line_counts) if line_counts else 0}')
print(f'last_file={line_counts[-1][0] if line_counts else "none"}')
print(f'last_file_lines={line_counts[-1][1] if line_counts else 0}')
PY
```

### Result

- Confirmed the relevant source columns are `AdresDomeny` and `DataWpisu`.
- Kept `64716` domains from rows whose `DataWpisu` year is `2026`.
- Generated `130` batch TXT files.
- Verified the maximum line count per batch is `500`.
- Verified the last batch file is `CERT_2026_only_batch_0130_domains.txt` with `216` lines.

### Not Run

- downstream crawling
- duplicate-domain review
- semantic validation of the source feed itself

Reason:

The task was limited to time filtering, domain extraction, and batch export only.

---

## 7. Risks / Caveats

- The exported TXT files preserve source order and do not deduplicate repeated domains.
- Rows with unparseable or empty `DataWpisu` were excluded by the year filter logic.
- If a future consumer expects URLs rather than bare domains, these TXT files will need a separate conversion step.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_batch_split.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If you want to run capture on these batches, decide first whether downstream tools should consume bare domains or prepend a scheme such as `http://` or `https://`.
- If you want a deduplicated CERT export as well, do that in a separate bounded task instead of silently altering these current batches.
