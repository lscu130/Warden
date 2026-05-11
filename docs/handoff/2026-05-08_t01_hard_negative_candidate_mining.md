# Handoff: T01 Hard Negative Candidate Mining V1

## 中文摘要

## 中文版

- 本次新增了只读候选挖掘脚本 `scripts/data/benign/mine_t01_hard_negative_candidates.py`，用于从已 triage 的 Tranco benign pool 中生成 `T01_benign_hard_negative` 候选复核队列。
- 外部任务单已复制到 repo：`docs/tasks/2026-05-08_t01_hard_negative_candidate_mining.md`。
- 新增运行说明：`docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md`。
- 正式输出写到 `E:\WardenData\manifests\t01_candidate_mining_v1`。
- 正式运行扫描 19,389 个样本，输出 12,759 个候选；CSV 与 report 候选计数一致。
- 脚本没有 apply/move/delete/relabel 模式；`--write-review-folders` 只写 per-bucket `paths.txt` 和 `candidates.csv`。
- 风险：候选量仍偏大，且 `C01_login_auth` 占绝对多数。建议人工先审 high score + exclusion rows，再根据样本质量调高阈值或细化规则。

---

## English Version

# Handoff Metadata

- Handoff ID: `HANDOFF-20260508-T01-HARD-NEGATIVE-CANDIDATE-MINING-V1`
- Related Task ID: `TASK-20260508-T01-HARD-NEGATIVE-CANDIDATE-MINING-V1`
- Task Title: Mine T01 Benign Hard Negative Candidates From Existing Tranco Benign Pool
- Module: dataset cleaning / benign pool / label manifest utilities
- Author: Codex
- Date: 2026-05-08
- Status: DONE
- Quota Mode: CODEX_QUOTA_CONSTRAINED
- Task Difficulty: HIGH
- Executor: CODEX
- Required Reviewer: GPT_WEB
- Codex Review Required: NO
- Codex Review Performed: NOT_APPLICABLE

## 1. Executive Summary

Implemented a reproducible, read-only candidate-mining utility for review-only `T01_benign_hard_negative` candidate discovery from existing Tranco benign triage folders.

The task reached the implementation and validation stop condition: the script exists, emits the required CSV/report, supports optional review folders, records missing/parse-warning evidence, and does not mutate source sample folders. Human acceptance and final relabel decisions remain outside this handoff.

## 2. What Changed

### Code Changes

- Added `scripts/data/benign/mine_t01_hard_negative_candidates.py`.
- The script scans configured triage label folders, reads lightweight artifacts, scores candidate buckets, records exclusion reasons, and writes deterministic CSV/report outputs.
- The script has no source-sample mutation mode. `--dry-run` is accepted for operator clarity and source-sample behavior is always read-only.

### Doc Changes

- Copied the external task definition into `docs/tasks/2026-05-08_t01_hard_negative_candidate_mining.md`.
- Added `docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md` with bilingual usage guidance and compatibility notes.
- Added this handoff.

### Output / Artifact Changes

- Wrote formal runtime outputs under `E:\WardenData\manifests\t01_candidate_mining_v1`.
- Generated `t01_candidate_manifest_v1.csv`.
- Generated `t01_candidate_report_v1.md`.
- Generated `t01_candidate_review_v1\` per-bucket path lists and per-bucket CSV files.

## 3. Files Touched

- `docs/tasks/2026-05-08_t01_hard_negative_candidate_mining.md`
- `scripts/data/benign/mine_t01_hard_negative_candidates.py`
- `docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md`
- `docs/handoff/2026-05-08_t01_hard_negative_candidate_mining.md`

Runtime outputs outside the repo:

- `E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_manifest_v1.csv`
- `E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_report_v1.md`
- `E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_review_v1\`

## 4. Behavior Impact

### Expected New Behavior

- Operators can run a local utility to generate T01 hard-negative candidate review queues from T00 and optional T90 triage folders.
- Candidates are scored into these buckets: `C01_login_auth`, `C02_payment_checkout`, `C03_finance_banking`, `C04_crypto_web3_wallet`, `C05_download_app`, `C06_support_contact`, `C07_ai_api_token_dashboard`, `C08_donation_charity`, `C09_domain_hosting_telecom`, and `C99_mixed_or_uncertain`.
- Missing lightweight artifacts and JSON parse warnings are recorded instead of crashing the whole run.

### Preserved Behavior

- Existing source sample folders are not moved, deleted, renamed, relabeled, or overwritten.
- Existing labels, frozen enums, L1/L2 schemas, train/val/test split logic, and final clean-pool manifest generation are unchanged.
- No third-party dependency was added.

### User-facing / CLI Impact

New CLI only:

```powershell
python scripts\data\benign\mine_t01_hard_negative_candidates.py `
  --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" `
  --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1" `
  --include-labels T00_clear_benign `
  --optional-review-source T90_uncertain_or_suspicious `
  --min-score 8 `
  --write-review-folders `
  --dry-run
```

### Output Format Impact

The new utility manifest uses the required task columns. This is a review utility output only, not a frozen project-wide schema.

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

The new script adds a standalone CLI. It does not modify existing scripts, labels, manifests, model targets, or frozen schema files.

## 6. Evidence / Retrieval Performed

Evidence sources actually checked:

- `AGENTS.md` content supplied in the current thread.
- `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- `docs/templates/TASK_TEMPLATE.md`.
- `docs/templates/HANDOFF_TEMPLATE.md`.
- External task doc from `C:\Users\20516\Downloads\TASK_20260508_T01_Hard_Negative_Candidate_Mining_V1.md`.
- Existing scripts under `scripts/data/benign/` and shared helpers under `scripts/data/common/`.
- Current triage root `E:\WardenData\manifests\tranco_benign_triage_v1`.

Retrieval / reading performed:

- Read required workflow and template docs before editing.
- Searched repository file list with `rg --files`.
- Read neighboring benign data utilities for CLI/output style.
- Inspected sample files under `T00_clear_benign` to confirm available artifact shape.
- Checked memory registry for WardenData/Tranco/manifest context; memory was used only for orientation, and current files/data were rechecked before implementation.

Claims supported by evidence:

- The expected triage root exists and contains T00, T01, T90, T99, and related bucket folders.
- The new output row count in the final run is 12,759 and the report's candidate count matches the CSV row count.
- The new script has no source-sample mutation operations and writes only output files/review lists.

Claims left unsupported or assumed:

- Candidate precision is not proven. The output is a ranked review queue, not a validated final T01 relabel set.
- Human review throughput and exact threshold needed to reach 1,500 to 2,000 accepted T01 samples remain unknown.

Retrieval stopped because:

- The script location, CLI convention, artifact shape, output requirements, and validation targets were clear enough for this task.

## 6.1 Counter-Review Performed

Original framing reviewed:

Use a rule-based local script to mine possible T01 hard-negative candidates from existing T00/T90 benign triage data.

Assumptions checked:

- T00 contains action-surface benign pages. The final output found many login/form/payment/support/hosting candidates, but this does not prove final T01 correctness.
- Lightweight artifacts are enough for candidate discovery. They were enough to produce reasons, buckets, missing flags, and parse warnings.
- Human review remains the final authority. The script does not apply labels.

Failure modes considered:

- Too many low-quality candidates.
- Multilingual under-recall.
- Accidentally mutating labels or source folders.
- Suspicious wallet/reward/error/download cases becoming clean T01 candidates.

Counterexamples or contradictory evidence found:

- The first full run with broader weak terms produced 16,385 candidates, which was too broad for efficient review.
- A synthetic validation sample with `seed phrase` / `private key` and bad JSON initially got filtered out after score penalties; the emit rule was fixed so such rows remain review-visible with exclusion reasons.
- Current final output still has a large C01 skew: 12,368 of 12,759 candidates are `C01_login_auth`.

Alternative routes considered:

- Manual-only review of all T00 again: lower engineering risk but poor reviewer efficiency.
- Teacher/LLM review: out of scope because the task forbids model use.
- New targeted crawl: out of scope because the task is limited to existing triaged benign data.

Framing changed: PARTIAL

If changed, what changed:

The implementation retained rule-based candidate mining, but tightened weak keyword scoring and used `--min-score 8` for the final output because the recommended `--min-score 3` produced a very broad queue in this local pool.

Claims left unsupported or assumed after counter-review:

- The final queue's precision is unknown until manual review.
- The best production threshold may be higher than 8 if the manual review budget is small.

Residual risks after counter-review:

- Candidate count is still high.
- Login/auth dominates the queue; bucket diversity is limited by current rules and pool content.
- Some useful multilingual candidates may still be missed.

Decision after counter-review:

- ACCEPT_ORIGINAL with a tightened operational threshold and explicit residual risk.

## 6. Validation Performed

### Commands Run

```powershell
python scripts\data\benign\mine_t01_hard_negative_candidates.py --help
python -m py_compile scripts\data\benign\mine_t01_hard_negative_candidates.py
python scripts\data\benign\mine_t01_hard_negative_candidates.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1_test" --include-labels T00_clear_benign --min-score 3 --limit 25 --dry-run
python scripts\data\benign\mine_t01_hard_negative_candidates.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1_stability_a" --include-labels T00_clear_benign --min-score 8 --limit 100 --dry-run
python scripts\data\benign\mine_t01_hard_negative_candidates.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1_stability_b" --include-labels T00_clear_benign --min-score 8 --limit 100 --dry-run
python scripts\data\benign\mine_t01_hard_negative_candidates.py --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1" --include-labels T00_clear_benign --optional-review-source T90_uncertain_or_suspicious --min-score 8 --write-review-folders --dry-run
```

Additional validation commands:

```powershell
Import-Csv -LiteralPath 'E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_manifest_v1.csv'
Get-Content -LiteralPath 'E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_report_v1.md'
Get-FileHash -Algorithm SHA256 'E:\WardenData\manifests\t01_candidate_mining_v1_stability_a\t01_candidate_manifest_v1.csv'
Get-FileHash -Algorithm SHA256 'E:\WardenData\manifests\t01_candidate_mining_v1_stability_b\t01_candidate_manifest_v1.csv'
Select-String -Path 'E:\Warden\scripts\data\benign\mine_t01_hard_negative_candidates.py' -Pattern 'rmtree|Move-Item|Remove-Item|unlink\(|rename\(|replace\(|shutil|\.write_text\(|\.open\('
```

### Search Validation Fallback

- rg attempted: YES
- rg status: SUCCEEDED
- rg failure message: none
- PowerShell fallback run: YES
- PowerShell fallback command:

```powershell
Select-String -Path 'E:\Warden\scripts\data\benign\mine_t01_hard_negative_candidates.py' -Pattern 'rmtree|Move-Item|Remove-Item|unlink\(|rename\(|replace\(|shutil|\.write_text\(|\.open\('
```

- Fallback validation evidence: only output writes were found in the new script; no source-sample mutation operations were found.

### Result

- `--help` succeeded.
- `py_compile` succeeded.
- Small subset run succeeded: scanned 25, candidates 22.
- Final run succeeded: scanned 19,389, candidates 12,759.
- CSV row count matched report count: 12,759.
- Report scanned count: 19,389.
- Candidate rows with `needs_review=True`: 4,184.
- Candidate rows with `exclude_reasons`: 4,183.
- Candidate rows with `missing_artifacts`: 3.
- Candidate rows with parse warnings in real full output: 0.
- Synthetic bad-JSON validation confirmed parse warnings and missing artifact fields are recorded when present.
- 100-sample repeated manifest hash matched: `53A54DEA2313C76684EB240F2AF553243D1F06F3336C0E0ED14A7C5069392904`.
- Review folders were created for all required buckets.

### Manual / Artifact Checks

- Confirmed required CSV columns are present: 32 columns, no missing or extra columns.
- Confirmed bucket folders exist under `t01_candidate_review_v1`.
- Confirmed suspicious/exclusion row behavior with a synthetic `seed phrase` / `private key` sample; the row was emitted with `dangerous_wallet_secret_request`, missing `net_summary.json`, and a `forms.json` parse warning.

### Not Run

- No unit test file was added.
- No model, OCR, YOLO, CLIP, teacher distillation, training, split generation, or final clean-pool manifest generation was run.
- No manual visual review of all 12,759 candidates was performed.

### Validation Caveats

- An earlier full command with broader scoring printed completion output but returned tool timeout 124. It was not treated as a clean pass and was rerun successfully with a longer timeout after rule tightening.
- The final candidate count is high and should be reviewed as a ranked queue, not as an apply list.

Reason:

The task scope is candidate mining only. Final T01 assignment requires separate human review and a future explicit apply/relabel task.

Next best check:

Manually review the top high-score `C01_login_auth` rows and all rows with `exclude_reasons`, then decide whether to tune thresholds or bucket rules before any relabel task.

## 8. Execution / Review / Agent Runtime Used

- quota_mode: CODEX_QUOTA_CONSTRAINED
- task_difficulty: HIGH
- Executor: CODEX
- Human Manual Required: NO
- Required Reviewer: GPT_WEB
- Codex Review Required: NO
- Codex Review Performed: NOT_APPLICABLE
- Codex Review Result: NOT_APPLICABLE
- Model or agent: Codex
- Reasoning effort: unknown
- Verbosity: medium
- Preamble used before tool-heavy work: YES
- Progress updates provided: YES
- Tools used: PowerShell shell commands, apply_patch
- Structured output used: NOT_APPLICABLE
- Notes on deviations from task guidance: final formal run used `--min-score 8` instead of the suggested `--min-score 3` because local validation showed score 3 was too broad.

Validation responsibility:

- Validation run by Human Manual: NO
- Validation run by Codex: YES
- Validation not run: full manual review and final relabel validation

## 9. Stop Condition

Completion stop condition reached: YES

Reason:

The required script, docs, repo task copy, runtime CSV/report/review folders, validation checks, and handoff were produced. The script remained candidate-only and read-only for source samples.

Escalation triggered: NO

If yes, escalation reason:

not applicable

Remaining blockers:

- Human review is required before any candidate becomes final T01.
- A future apply/relabel task is required if the owner wants to move accepted samples or update labels.

## 7. Risks / Caveats

- Candidate count is high: 12,759 rows from 19,389 scanned samples.
- Bucket distribution is highly skewed toward `C01_login_auth`.
- Keyword rules are transparent but heuristic; precision and recall are not established.
- Multilingual coverage is partial.
- Review folders contain pointers/review files only, not copied sample folders.
- Counter-review residual risk: broad login/auth matching may still waste manual review time unless review starts from top score bands and exclusion rows.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md`
- `docs/tasks/2026-05-08_t01_hard_negative_candidate_mining.md`
- `docs/handoff/2026-05-08_t01_hard_negative_candidate_mining.md`

Doc debt still remaining:

- none for this candidate-mining utility.

## 9. Recommended Next Step

- Review `E:\WardenData\manifests\t01_candidate_mining_v1\t01_candidate_report_v1.md` first, then start manual review from high-score candidates and rows with `exclude_reasons`.
- If the queue is too broad, rerun with a higher `--min-score` or narrow `C01_login_auth` rules before any relabel work.
- Create a separate explicit apply/relabel task only after manual acceptance criteria are frozen.
