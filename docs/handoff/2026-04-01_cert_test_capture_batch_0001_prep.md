# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 CERT 第一个 3 月批次 test capture 的 prep handoff。
- 若涉及精确输入批次、输出目录、命令或兼容性说明，以英文版为准。

### 摘要

- 对应任务：`WARDEN-CERT-TEST-CAPTURE-BATCH-0001-V1`
- 任务主题：冻结 CERT 第一个 3 月批次的 test 抓取命令与输出根目录
- 当前状态：`DONE`
- 所属模块：Data module / capture operations

### 当前交付要点

- test 输入固定为 `CERT_2026_03_only_batch_0001_domains.txt`
- 推荐命令沿用当前 malicious supervised 默认风格
- 输入是裸域名，但仓库 capture 脚本会自动补 `https://`

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-01-cert-test-capture-batch-0001-prep
- Related Task ID: WARDEN-CERT-TEST-CAPTURE-BATCH-0001-V1
- Task Title: Freeze an execution-ready test capture task for the first March-only CERT batch so the feed quality can be inspected
- Module: Data module / capture operations
- Author: Codex
- Date: 2026-04-01
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Added a new execution-prep handoff for a CERT test capture that uses only the first March-only CERT batch.

The purpose of this prep artifact is to freeze a small, bounded test run so the practical quality of the CERT feed can be inspected before any broader CERT capture plan is attempted.
The test input batch contains `500` bare-domain lines, and the current capture script implementation normalizes scheme-less inputs by prepending `https://`, so the batch can be passed directly to the existing malicious runner.

---

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-04-01_cert_test_capture_batch_0001_execution_task.md`.
- Added `docs/handoff/2026-04-01_cert_test_capture_batch_0001_prep.md`.
- Froze the CERT test queue as:
  - malicious test input `CERT_2026_03_only_batch_0001_domains.txt`
  - output root `E:\Warden\data\raw\phish\2026-04-01_cert_test_batch_0001`

### Output / Artifact Changes

- none

---

## 3. Files Touched

- `docs/tasks/2026-04-01_cert_test_capture_batch_0001_execution_task.md`
- `docs/handoff/2026-04-01_cert_test_capture_batch_0001_prep.md`

Optional notes per file:

- These docs define a test-capture boundary only.
- They do not claim the CERT test capture already ran.

---

## 4. Behavior Impact

### Expected New Behavior

- Operators now have a separate prep artifact for a bounded CERT feed test.
- The test uses only the first March-only CERT batch.
- The resulting capture output will land in its own output root so feed quality can be reviewed cleanly.
- The test uses the current supervised malicious-runner defaults.

### Preserved Behavior

- No capture code changed.
- Current malicious runner CLI behavior remains unchanged.
- Earlier CERT batch generation artifacts remain untouched.

### User-facing / CLI Impact

- none

### Output Format Impact

- none

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

Compatibility notes:

This prep artifact changes only execution planning for a new test queue.
It does not change any runner or capture interface.
The only important operational assumption is that bare domains from the CERT batch are accepted because the capture script normalizes scheme-less inputs to `https://...`.

---

## 6. Validation Performed

### Commands Run

```bash
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python - <<'PY'
from pathlib import Path
path = Path(r'E:\Warden\cert csv\CERT_2026_03_only_batch_0001_domains.txt')
print(f'line_count={sum(1 for _ in path.open("r", encoding="utf-8"))}')
PY
Select-String -Path E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py -Pattern 'def normalize_url|if not RE_URL_SCHEME.match\(u\)|u = "https://" \+ u'
```

### Result

- Confirmed the current malicious runner still exposes:
  - `--input_path`
  - `--source`
  - `--output_root`
  - `--disable_route_intercept`
  - `--interactive_skip`
  - `--url_hard_timeout_ms`
  - `--nav_timeout_ms`
  - `--goto_wait_until {load,domcontentloaded,commit,networkidle}`
- Confirmed `CERT_2026_03_only_batch_0001_domains.txt` exists and contains `500` lines.
- Confirmed the capture script includes:
  - `def normalize_url(u: str)`
  - `if not RE_URL_SCHEME.match(u):`
  - `u = "https://" + u`

### Not Run

- live CERT test capture itself
- feed-quality review of actual returned artifacts

Reason:

This handoff is an execution-prep artifact only.
Actual quality assessment must wait for the real capture output.

---

## 7. Risks / Caveats

- Because the input is domain-only, some sites may require `http://` rather than `https://`; the current normalization behavior assumes `https://` first.
- A `500`-domain test batch can still be non-trivial in runtime and operator burden.
- This doc does not prove anything about CERT feed quality yet; it only freezes the test plan.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-01_cert_test_capture_batch_0001_execution_task.md`
- `docs/handoff/2026-04-01_cert_test_capture_batch_0001_prep.md`

Doc debt still remaining:

- a later run-result handoff is still needed after the actual CERT test capture is executed

---

## 9. Recommended Next Step

- Use this exact output root for the CERT test queue:
  - `E:\Warden\data\raw\phish\2026-04-01_cert_test_batch_0001`
- Run this preflight first:

```powershell
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --help
```

- Use this exact test command:

```powershell
New-Item -ItemType Directory -Force E:\Warden\data\raw\phish\2026-04-01_cert_test_batch_0001 | Out-Null
python E:\Warden\scripts\data\malicious\run_malicious_capture.py `
  --input_path "E:\Warden\cert csv\CERT_2026_03_only_batch_0001_domains.txt" `
  --source cert `
  --output_root E:\Warden\data\raw\phish\2026-04-01_cert_test_batch_0001 `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

- After the run finishes, inspect:
  - how many samples are actually reachable
  - how many are clearly malicious vs dead/benign/parking
  - how much usable train-eligible content remains in this feed
