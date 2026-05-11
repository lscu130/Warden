# T01 Hard Negative Candidate Mining V1

## 中文摘要

本文档说明 `scripts/data/benign/mine_t01_hard_negative_candidates.py` 的用途和运行方式。

该脚本从已经人工 triage 的 Tranco benign 目录中读取轻量 artifact，生成 `T01_benign_hard_negative` 候选复核队列。默认主来源是 `T00_clear_benign`，可显式加入 `T90_uncertain_or_suspicious` 作为单独复核来源。

脚本只生成候选 CSV、Markdown 报告和可选 per-bucket path list，不移动、不删除、不重命名、不覆盖原样本目录，也不自动修改人工标签。

推荐命令：

```powershell
python scripts\data\benign\mine_t01_hard_negative_candidates.py `
  --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" `
  --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1" `
  --include-labels T00_clear_benign `
  --optional-review-source T90_uncertain_or_suspicious `
  --min-score 3 `
  --write-review-folders `
  --dry-run
```

主要输出：

- `t01_candidate_manifest_v1.csv`
- `t01_candidate_report_v1.md`
- `t01_candidate_review_v1/`，仅在传入 `--write-review-folders` 时生成

人工复核仍是最终 authority。该输出不是最终 label manifest，也不是 T00 到 T01 的自动迁移结果。

---

# T01 Hard Negative Candidate Mining V1

## Purpose

`scripts/data/benign/mine_t01_hard_negative_candidates.py` mines review-only `T01_benign_hard_negative` candidates from already triaged Tranco benign sample folders.

The utility is intended to increase human-review efficiency before any future explicit relabel/apply task. It does not mutate the triage pool.

## Source Data

Default source root:

```text
E:\WardenData\manifests\tranco_benign_triage_v1
```

Default included source folder:

```text
T00_clear_benign
```

Optional review source:

```text
T90_uncertain_or_suspicious
```

T90 rows remain review-only and must not be silently promoted to T01.

## Artifacts Read

For each sample directory, the script reads these lightweight files when present:

- `visible_text.txt`
- `url.json`
- `forms.json`
- `net_summary.json`
- screenshot existence flags for `screenshot_viewport.png`, `screenshot_view.png`, and `screenshot_full.png`

Missing files and JSON parse failures are recorded per row. Missing or malformed artifacts do not stop the whole run unless a configured source folder is missing.

## Outputs

The script writes:

```text
t01_candidate_manifest_v1.csv
t01_candidate_report_v1.md
```

When `--write-review-folders` is passed, it also writes:

```text
t01_candidate_review_v1\
  C01_login_auth\
  C02_payment_checkout\
  C03_finance_banking\
  C04_crypto_web3_wallet\
  C05_download_app\
  C06_support_contact\
  C07_ai_api_token_dashboard\
  C08_donation_charity\
  C09_domain_hosting_telecom\
  C99_mixed_or_uncertain\
```

Each bucket folder contains `paths.txt` and `candidates.csv`. These are pointer/review files only. Original sample folders are not moved.

## CLI

```powershell
python scripts\data\benign\mine_t01_hard_negative_candidates.py `
  --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" `
  --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1" `
  --include-labels T00_clear_benign `
  --optional-review-source T90_uncertain_or_suspicious `
  --min-score 3 `
  --write-review-folders `
  --dry-run
```

`--dry-run` is accepted for operator clarity. The script is always read-only with respect to source samples; there is no apply, move, delete, or relabel mode.

Use `--limit <N>` for smoke validation on a bounded number of sample directories. The default `--limit 0` scans all configured source folders.

## Candidate Buckets

The manifest uses these candidate buckets:

- `C01_login_auth`
- `C02_payment_checkout`
- `C03_finance_banking`
- `C04_crypto_web3_wallet`
- `C05_download_app`
- `C06_support_contact`
- `C07_ai_api_token_dashboard`
- `C08_donation_charity`
- `C09_domain_hosting_telecom`
- `C99_mixed_or_uncertain`

## Compatibility Notes

- Schema changed: no.
- Frozen labels changed: no.
- Source samples mutated: no.
- CSV output is a utility review manifest, not a frozen project-wide schema.
- Any future label mutation must be a separate explicit task.
