# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是本次 CERT 域名 CSV 缩窄到 `2026-03` 月份的重新分批 handoff。
- 若涉及精确时间边界、文件名模式、数量或兼容性，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CERT-DOMAINS-2026-03-ONLY-BATCH-SPLIT-V1`
- 任务主题：只保留 `2026-03` 月份的数据并重新分批
- 当前状态：`DONE`
- 所属模块：Data / External Feed Utility

### 当前交付要点

- 已新增一套 3 月专用的 CERT 批次，不覆盖旧的全年版和 2 月起版。
- 保留范围是 `2026-03-01T00:00:00+00:00` 到 `2026-04-01T00:00:00+00:00` 之前。
- 仍然只导出 domain，一行一个，`500` 一批。

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-01-cert-domains-2026-03-only-batch-split
- Related Task ID: WARDEN-CERT-DOMAINS-2026-03-ONLY-BATCH-SPLIT-V1
- Task Title: Filter the provided CERT domains CSV to March 2026 only and split domains into 500-line TXT batches
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

Generated a March-2026-only CERT batch set from `C:\Users\20516\Downloads\domains.csv`.

The retained range is:

- inclusive lower bound: `2026-03-01T00:00:00+00:00`
- exclusive upper bound: `2026-04-01T00:00:00+00:00`

Only `AdresDomeny` values were exported, split into `500`-line TXT batches, and written as a separate artifact set so the earlier broader CERT exports remain untouched.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_03_only_batch_split.md`.
- Added `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_03_only_batch_split.md`.

### Output / Artifact Changes

- Created a March-only CERT batch set under `E:\Warden\cert csv\`.
- Output filename pattern:
  - `CERT_2026_03_only_batch_0001_domains.txt`
  - ...
  - `CERT_2026_03_only_batch_0060_domains.txt`

---

## 3. Files Touched

- `E:\Warden\cert csv\CERT_2026_03_only_batch_0001_domains.txt`
- `E:\Warden\cert csv\CERT_2026_03_only_batch_0060_domains.txt`
- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_03_only_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_03_only_batch_split.md`

Optional notes per file:

- The earlier `CERT_2026_only_...` and `CERT_2026_02_01_to_2026_04_01_...` artifact sets still exist unchanged.
- The new March-only files contain domains only, one per line.

---

## 4. Behavior Impact

### Expected New Behavior

- There is now a smaller CERT batch set limited to March 2026 only.
- Operators can use the March-only set instead of the broader sets when they want a smaller working volume.

### Preserved Behavior

- The source CSV was not modified.
- Earlier broader CERT batch sets were not deleted.
- Output remains TXT with one domain per line.

### User-facing / CLI Impact

- none

### Output Format Impact

- TXT only
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

This task added a third artifact set only.
It did not modify the source CSV, and it did not remove the earlier broader CERT exports.

---

## 6. Validation Performed

### Commands Run

```bash
python - <<'PY'
import csv
from datetime import datetime
from pathlib import Path

input_path = Path(r'C:\Users\20516\Downloads\domains.csv')
output_dir = Path(r'E:\Warden\cert csv')
batch_size = 500
lower_bound = datetime.fromisoformat('2026-03-01T00:00:00+00:00')
upper_bound = datetime.fromisoformat('2026-04-01T00:00:00+00:00')
prefix = 'CERT_2026_03_only'

def parse_dt(raw: str):
    value = (raw or '').strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None

rows = []
latest_retained = None
with input_path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for record in reader:
        dt = parse_dt(record.get('DataWpisu', ''))
        if dt is None or dt < lower_bound or dt >= upper_bound:
            continue
        domain = (record.get('AdresDomeny') or '').strip()
        if not domain:
            continue
        rows.append(domain)
        if latest_retained is None or dt > latest_retained:
            latest_retained = dt

output_dir.mkdir(parents=True, exist_ok=True)
for old in output_dir.glob(f'{prefix}_batch_*_domains.txt'):
    old.unlink()

batch_count = 0
for idx in range(0, len(rows), batch_size):
    batch_count += 1
    chunk = rows[idx:idx + batch_size]
    path = output_dir / f'{prefix}_batch_{batch_count:04d}_domains.txt'
    path.write_text('\n'.join(chunk) + '\n', encoding='utf-8', newline='\n')

print(f'total_domains={len(rows)}')
print(f'batch_count={batch_count}')
print(f'latest_retained={latest_retained.isoformat() if latest_retained else "none"}')
PY
python - <<'PY'
from pathlib import Path
paths = sorted(Path(r'E:\Warden\cert csv').glob('CERT_2026_03_only_batch_*_domains.txt'))
line_counts = [(p.name, sum(1 for _ in p.open('r', encoding='utf-8'))) for p in paths]
print(f'file_count={len(line_counts)}')
print(f'max_lines={max(c for _, c in line_counts) if line_counts else 0}')
print(f'first_file={line_counts[0][0] if line_counts else "none"}')
print(f'last_file={line_counts[-1][0] if line_counts else "none"}')
print(f'last_file_lines={line_counts[-1][1] if line_counts else 0}')
PY
Get-ChildItem 'E:\Warden\cert csv\CERT_2026_only_batch_0001_domains.txt','E:\Warden\cert csv\CERT_2026_02_01_to_2026_04_01_batch_0001_domains.txt','E:\Warden\cert csv\CERT_2026_03_only_batch_0001_domains.txt' | Select-Object Name,Length
```

### Result

- Confirmed `29521` domains were retained in March 2026.
- Confirmed the latest retained timestamp is `2026-03-31T23:56:11+00:00`.
- Generated `60` March-only batch files.
- Verified the maximum line count per batch is `500`.
- Verified the last batch file is `CERT_2026_03_only_batch_0060_domains.txt` with `21` lines.
- Verified that the year-wide, Feb-onward, and March-only CERT batch sets all coexist.

### Not Run

- downstream crawling
- duplicate-domain review
- semantic validation of the feed contents

Reason:

The task was limited to a March-only export.

---

## 7. Risks / Caveats

- The March-only output still preserves source order and does not deduplicate repeated domains.
- The retained March range is based on UTC timestamps parsed from `DataWpisu`.
- If you later want only part of March, that would require another narrower export.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\tasks\2026-04-01_cert_domains_2026_03_only_batch_split.md`
- `E:\Warden\docs\handoff\2026-04-01_cert_domains_2026_03_only_batch_split.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If this March-only set is the one you actually plan to use, work from `CERT_2026_03_only_batch_*.txt` and ignore the broader sets.
- If you no longer need the broader exports, delete them in a separate explicit cleanup task rather than mixing cleanup into this export task.
