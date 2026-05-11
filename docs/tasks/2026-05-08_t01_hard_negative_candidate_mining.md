# TASK_20260508_T01_Hard_Negative_Candidate_Mining_V1

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分供人工快速阅读与执行确认。

### 任务摘要

当前 Tranco benign 数据已经完成 T00/T01 粗筛，usable benign 总量满足 20K 要求，但 `T01_benign_hard_negative` 目前约 800 个，偏少。后续如果直接做 train/val/test split，val/test 中 T01 的绝对数量可能不足，hard negative 误报评估会偏弱。

本任务要求新增一个**候选挖掘脚本**，从已经人工标好的 benign pool 中，尤其是 `T00_clear_benign`，自动挖掘可能应该归入 T01 的 benign hard negative 候选。脚本只负责候选发现、分桶、排序、报告和复核队列生成；**不得自动覆盖人工标签，不得默认移动原始样本**。

### 核心原则

- 脚本负责：挖候选、打分、分桶、生成 CSV / 报告 / 可选复核目录。
- 人工负责：最终确认候选是否从 T00 调整为 T01。
- 默认只读，不移动、不删除、不改标签。
- 不跑模型，不跑 OCR / YOLO / CLIP，不做 teacher distillation。
- 目标是把 T01 从约 800 补到至少 1500，理想 2000 左右，但本任务只生成候选队列，不直接完成最终补标。

### 推荐候选桶

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

### 交付重点

最终应得到：

- `t01_candidate_manifest_v1.csv`
- `t01_candidate_report_v1.md`
- 可选复核目录树，例如 `t01_candidate_review_v1/`
- 明确说明脚本是否只读、扫描了多少样本、找到多少候选、各桶数量、排除/疑似数量。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: `TASK-20260508-T01-HARD-NEGATIVE-CANDIDATE-MINING-V1`
- Task Title: Mine T01 Benign Hard Negative Candidates From Existing Tranco Benign Pool
- Owner Role: Codex
- Priority: High
- Status: TODO
- Related Module: dataset cleaning / benign pool / label manifest utilities
- Related Issue / ADR / Doc: `docs/data/Warden_T01_HARD_NEGATIVE_CANDIDATE_MINING_V1.md`
- Related Docs:
  - `AGENTS.md`
  - `docs/workflow/GPT_CODEX_WORKFLOW.md`
  - `docs/templates/TASK_TEMPLATE.md`
  - `docs/templates/HANDOFF_TEMPLATE.md`
  - `docs/frozen/Warden_L1_FRAMEWORK_V0.1.md` if present
  - `docs/frozen/Warden_Threat_Definition_V1.md` if present
- Created At: 2026-05-08
- Requested By: project owner

Use this task to build a reproducible, read-only candidate-mining utility for expanding the `T01_benign_hard_negative` pool from already triaged Tranco benign data.

---

## 1. Background

The Tranco benign data has already been manually triaged into usable benign categories.

Current state:

- `T00_clear_benign` and `T01_benign_hard_negative` together satisfy the 20K usable benign requirement.
- `T01_benign_hard_negative` currently has roughly 800 samples.
- This is usable for a pilot but weak for hard-negative false-positive evaluation, especially after train/validation/test splitting.
- We need a reproducible way to mine additional T01 candidates from the existing triaged benign pool, especially from `T00_clear_benign`, before final clean-pool manifest generation and group-based split.

Important semantic rule:

- A login form, payment surface, wallet/connect button, download button, support contact, or third-party redirect is not automatically malicious.
- In a benign official or non-deceptive context, these are valuable benign hard negatives.
- The script must therefore surface candidates for human review rather than overwrite labels automatically.

---

## 2. Goal

Build a local script that scans the already triaged benign sample folders and generates a reviewable queue of possible `T01_benign_hard_negative` candidates.

The script should detect benign pages with risk-relevant action surfaces or sensitive benign contexts, assign candidate buckets and scores, produce a CSV manifest and Markdown report, and optionally create review folders or path lists for GUI-based manual review.

The script must be read-only by default and must not mutate final human labels unless a future, explicitly approved apply task is created.

---

## 3. Expected Outcome And Success Criteria

Expected outcome:

- A reproducible script exists for mining T01 candidates from existing T00/T90/T01 triage data.
- The script produces a candidate CSV, a report, and optional review-folder organization.
- The script does not move, delete, relabel, or overwrite samples by default.
- Human reviewers can use the output to efficiently confirm additional T01 samples.

Success criteria:

- The script scans configured input directories and recognizes at least `T00_clear_benign` as the main candidate source.
- The script can optionally include `T90_uncertain_or_suspicious` as a separate review source, but never silently promotes T90 to T01.
- The script reads available lightweight artifacts only: `visible_text.txt`, `url.json`, `forms.json`, `net_summary.json`, screenshot existence flags, and optional title/html summary if already present.
- The script outputs `t01_candidate_manifest_v1.csv` with the required columns listed below.
- The script outputs `t01_candidate_report_v1.md` summarizing counts, buckets, score bands, and exclusion/suspicion flags.
- The script supports a dry-run/read-only default mode.
- If review folders are created, they must contain copies, shortcuts, symlinks, or manifest references only; original sample folders must not be moved by default.
- The script has clear CLI help text and sane defaults for Windows paths.
- Validation demonstrates that counts in the report match the CSV rows.

---

## 4. Scope In

This task is allowed to touch:

- Add a new dataset utility script under the existing project scripts/tools location appropriate for dataset manifest utilities.
- Add lightweight helper functions if needed in the same utility area.
- Add or update documentation for how to run this script.
- Add a task handoff under `docs/handoff/`.
- Add generated example output paths only if they are small and appropriate for version control; otherwise document where runtime outputs are written.

This task is allowed to change:

- Dataset utility code for candidate mining.
- CLI options for the new script only.
- Documentation related to this candidate-mining workflow.

Preferred output paths should be configurable, for example:

```text
E:\WardenData\manifests\t01_candidate_mining_v1\
  t01_candidate_manifest_v1.csv
  t01_candidate_report_v1.md
  t01_candidate_review_v1\
```

---

## 5. Scope Out

This task must NOT do the following:

- Do not train any model.
- Do not run teacher distillation.
- Do not use external web lookup.
- Do not run OCR, YOLO, CLIP, SpecularNet, BERT, or any other ML model.
- Do not change L1/L2 schema.
- Do not modify frozen labels or enums.
- Do not edit threat-definition semantics.
- Do not overwrite human labels.
- Do not move samples from T00 to T01 by default.
- Do not delete, rename, or mutate original sample directories.
- Do not make train/val/test split in this task.
- Do not generate final clean-pool manifests in this task unless explicitly approved as an extension.
- Do not add third-party dependencies unless explicitly approved.

If any apply/move/relabel behavior is requested later, it must be implemented as a separate explicit task or protected by a disabled-by-default `--apply` mode with strong confirmation checks.

---

## 6. Inputs

Relevant inputs for this task:

### Expected triage folders

The script should support configurable paths and should not hard-code a single environment. Expected examples:

```text
E:\WardenData\manifests\tranco_benign_triage_v1\
  T00_clear_benign\
  T01_benign_hard_negative\
  T90_uncertain_or_suspicious\
  T99_bad_capture_or_unusable\
```

### Sample artifacts to scan

For each sample directory, read these if present:

- `visible_text.txt`
- `url.json`
- `forms.json`
- `net_summary.json`
- `meta.json` only if needed for sample ID or path metadata; do not use feed labels as model-like judgment input
- `screenshot_viewport.png`, `screenshot_view.png`, `screenshot_full.png` existence only
- optional existing HTML/title summary if already present in the sample folder

### Missing inputs behavior

- Missing lightweight artifacts should be recorded in the output manifest.
- Missing artifacts should not crash the whole run.
- Bad or unreadable JSON should be recorded as a parsing warning for that sample.

---

## 7. Evidence / Retrieval Rules

Facts or claims that require support:

- Any claim about existing repository scripts or docs must be based on reading/searching the repository.
- Any claim about generated counts must be based on actual script output.
- Any claim that the script is read-only must be supported by code review and a dry-run validation.

Allowed evidence sources:

- Repository files.
- Local sample directories provided by the owner.
- Script output generated during validation.
- Handoff command output.

Retrieval budget:

- Read the required governing docs first if they are present: `AGENTS.md`, workflow, task template, handoff template.
- Search existing dataset/manifest utility scripts before adding a new script.
- Reuse existing conventions where reasonable.
- Stop repository retrieval once the correct script location, CLI style, and output conventions are clear.

Missing-evidence behavior:

- If the expected data path is missing, stop and report blocked.
- If a specific artifact type is missing for some samples, continue and record per-sample missing flags.
- Do not invent sample counts.

---

## 7.1 Counter-Review Requirements

Current proposed framing:

- Use a rule-based local script to mine possible T01 hard-negative candidates from existing T00/T90 benign triage data.

Hidden assumptions to check:

- T00 contains a meaningful number of missed T01-like benign hard negatives.
- Lightweight artifacts contain enough information to identify candidate action surfaces.
- Rule-based keyword and artifact matching can produce a useful review queue without too many false candidates.
- Human review remains the final authority.

Failure modes to consider:

- Too many low-quality candidates, wasting manual review time.
- Missing multilingual keywords, causing under-recall.
- Overfitting to English keywords only.
- Accidentally moving or relabeling original samples.
- Treating suspicious/malicious-looking pages as T01 candidates.
- Treating action surfaces as final benign evidence without context.

Counterexamples or contradictory cases:

- Normal article pages containing words like “account” or “support” but not actually hard negatives.
- Suspicious pages containing “login” or “wallet” that should remain T90, not T01.
- Bad captures with login words in browser error pages.
- Web3 pages with seed phrase/private key terms that must not become benign hard negatives.

Alternative routes to compare:

- Manual-only review of all T00 again.
- Teacher LLM review of sampled candidates.
- New crawling targeted at official login/payment/download/Web3 pages.

Decision rule:

- Accept the script if it is read-only, review-oriented, reproducible, and produces useful candidate buckets.
- Revise the rule set if candidate quality is poor or too broad.
- Stop and escalate if implementation would mutate labels or require schema changes.

---

## 8. Candidate Buckets

The script should assign one primary candidate bucket and may add secondary buckets when applicable.

Required buckets:

```text
C01_login_auth
C02_payment_checkout
C03_finance_banking
C04_crypto_web3_wallet
C05_download_app
C06_support_contact
C07_ai_api_token_dashboard
C08_donation_charity
C09_domain_hosting_telecom
C99_mixed_or_uncertain
```

Bucket intent:

- `C01_login_auth`: login, sign-in, signup, account, password, MFA, OTP, verify, SSO, OAuth.
- `C02_payment_checkout`: checkout, payment, billing, invoice, card, subscription, renew, order confirmation.
- `C03_finance_banking`: banking, fintech, investment platform, insurance, loan, account finance surface.
- `C04_crypto_web3_wallet`: exchange, crypto, wallet, connect wallet, KYC, deposit, withdraw, staking, NFT, bridge.
- `C05_download_app`: download, install, app, extension, plugin, APK, EXE, launcher, software update, document download.
- `C06_support_contact`: support, help center, contact, chat, customer service, ticket, call support.
- `C07_ai_api_token_dashboard`: AI platform, API key, token, credits, model dashboard, playground, billing dashboard.
- `C08_donation_charity`: donate, donation, charity, church/nonprofit support, fundraiser, support us.
- `C09_domain_hosting_telecom`: domain, hosting, VPS, server, SSL, CDN, DNS, broadband, data plan, telecom service.
- `C99_mixed_or_uncertain`: multiple weak signals, ambiguous evidence, or candidate needs cautious review.

---

## 9. Candidate Detection Rules

### 9.1 Positive candidate signals

Use keyword and artifact signals from `visible_text`, URL/title/path, `forms.json`, and `net_summary.json`.

High-score examples:

- `has_password = true`
- `form_count > 0`
- `input_count > 0`
- login/sign in/account/password/MFA/OTP/verify language
- checkout/payment/billing/card/invoice/renew/subscription language
- bank/finance/loan/insurance/investment/fintech language
- wallet/connect wallet/KYC/deposit/withdraw/staking/NFT/bridge language
- download/install/app/extension/plugin/apk/exe/launcher language
- support/help/contact/chat/customer service/ticket language
- API key/token/credits/dashboard/playground/model billing language
- donate/donation/charity/fundraiser/support us language
- domain/hosting/VPS/server/SSL/CDN/DNS/broadband/data plan language
- URL/title/path includes login/signin/account/checkout/support/download/billing/wallet

### 9.2 Medium-score signals

- `pricing`, `plans`, `subscription`, `upgrade`
- third-party redirect exists but appears to be a normal platform indicator
- links to App Store, Google Play, GitHub, Microsoft Store, official CDN-like hosts
- dashboard/account/console language
- language indicating official product onboarding

### 9.3 Negative / exclusion signals

These should not become direct T01 candidates. Mark as suspicious/exclude/review instead:

- gambling/adult/gray-service terms
- prize, quick-rich, high-return investment manipulation, guaranteed profit
- seed phrase, private key, recovery phrase, keystore upload
- obvious brand impersonation
- severe brand-domain mismatch combined with sensitive action surface
- unknown EXE/APK download with deceptive or urgent language
- browser error page, 403/404/500, Cloudflare/challenge/captcha-only bad capture
- empty/blank/parked/for-sale pages unless separately intended for T99/T14-like handling

The script should record exclusion reasons separately from positive candidate reasons.

---

## 10. Scoring Requirements

Implement a transparent score that is easy to inspect.

Recommended approach:

- High-confidence artifact signals, such as password field or form inputs, should carry more weight than generic keywords.
- Bucket-specific keywords should add score to their bucket.
- Negative/exclusion signals should reduce candidate confidence or set `needs_review = true`.
- Multiple independent signals should increase confidence.

Required score fields:

```text
candidate_score
score_band: high | medium | low
candidate_bucket
secondary_buckets
reasons
exclude_reasons
needs_review
```

Do not make score thresholds opaque. Put threshold constants near the top of the script or in a small config object.

---

## 11. Required Outputs

### 11.1 Candidate manifest

Output file:

```text
t01_candidate_manifest_v1.csv
```

Required columns:

```csv
sample_id,current_label,candidate_score,score_band,candidate_bucket,secondary_buckets,reasons,exclude_reasons,current_path,final_url,final_host,etld1,visible_text_chars,effective_visible_text_chars,form_count,input_count,has_password,has_login_hint,has_payment_hint,has_finance_hint,has_wallet_hint,has_download_hint,has_support_hint,has_ai_token_hint,has_donation_hint,has_hosting_hint,has_screenshot_viewport,has_screenshot_view,has_screenshot_full,missing_artifacts,parse_warnings,needs_review
```

### 11.2 Candidate report

Output file:

```text
t01_candidate_report_v1.md
```

Report must include:

- total scanned samples
- total scanned by current label/source folder
- total candidates found
- candidates by bucket
- candidates by score band
- candidates with exclusion/suspicious flags
- missing artifact counts
- parse warning counts
- recommended manual review order
- reminder that output is candidate-only and does not overwrite labels

### 11.3 Optional review folder tree

If implemented, create an optional review tree under a configured output directory:

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

By default, review folders must not move original samples. Acceptable options:

- write per-bucket CSV files;
- write `.txt` path lists;
- copy lightweight pointer files;
- create shortcuts if the repo already uses a safe Windows shortcut approach;
- copy sample folders only if explicitly configured and documented as a copy operation.

---

## 12. CLI Requirements

The script should expose a clear CLI.

Suggested options:

```powershell
python <script_path> ^
  --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" ^
  --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1" ^
  --include-labels T00_clear_benign ^
  --optional-review-source T90_uncertain_or_suspicious ^
  --min-score 3 ^
  --write-review-folders ^
  --dry-run
```

Behavior requirements:

- `--dry-run` or read-only behavior must be the default.
- The script must print summary counts.
- The script must fail safely when paths are invalid.
- The script must not require network access.

---

## 13. Hard Constraints

Must obey all of the following:

- Follow `AGENTS.md` and the Warden workflow docs if present.
- Prefer minimal, testable, reversible changes.
- Do not rename frozen fields, folders, or labels.
- Do not silently change output formats.
- Do not add third-party dependencies without approval.
- Keep this as a candidate-mining tool, not a label mutation tool.
- Preserve human label authority.
- Record missing artifacts and parse failures instead of crashing the whole run.
- Keep generated output outside the repository unless small sample fixtures are explicitly needed.

---

## 14. Interface / Schema Constraints

Schema changed allowed: NO.

This task must not freeze or modify:

- final dataset schema;
- L1/L2 output schema;
- label enums;
- threat taxonomy;
- teacher distillation schema;
- model training targets.

The CSV output is a utility manifest for review, not a frozen project-wide schema unless a future task promotes it.

---

## 15. Validation Checklist

Minimum validation:

- Run the script on a small subset first.
- Confirm it does not move, delete, rename, or relabel original samples by default.
- Confirm the CSV opens correctly and contains required columns.
- Confirm the report counts match the CSV counts.
- Confirm candidates appear in expected buckets.
- Confirm suspicious/exclusion terms do not silently become clean T01 candidates.
- Confirm missing artifacts are recorded.
- Confirm parse warnings are recorded.
- Confirm running the script twice produces stable outputs for the same input.

Suggested validation commands:

```powershell
python <script_path> --help
python <script_path> --triage-root "E:\WardenData\manifests\tranco_benign_triage_v1" --output-dir "E:\WardenData\manifests\t01_candidate_mining_v1_test" --include-labels T00_clear_benign --min-score 3 --dry-run
```

If repository tests/checkers exist for scripts or docs, run the relevant targeted checks and report results.

---

## 16. Acceptance

Accept this task if:

- A reproducible script generates a reviewable T01 candidate queue from the existing triaged benign pool.
- It is read-only by default.
- It produces the required CSV and report.
- It records candidate reasons and exclusion reasons.
- It supports efficient human review without overwriting labels.
- Validation confirms output consistency and non-mutating behavior.

Reject or mark partial if:

- It silently relabels or moves samples.
- It requires ML models or external APIs.
- It changes schemas or label definitions.
- It lacks reason columns, making manual review inefficient.
- It cannot handle missing artifacts robustly.

---

## 17. Required Handoff

After execution, produce a handoff under `docs/handoff/` using the project handoff template.

The handoff must include:

- files touched;
- script path;
- exact commands run;
- output paths;
- counts from validation run;
- whether any samples were moved or mutated;
- validation result;
- not-run items;
- known risks;
- recommended next step.

---

## Repo Template Compatibility Index

This repo-local copy preserves the external task wording above. The markers below keep the current structural checker aligned with the active task sections:

## 3. Scope In

See `## 4. Scope In` above.

## 4. Scope Out

See `## 5. Scope Out` above.

## 5. Inputs

See `## 6. Inputs` above.

## 6. Required Outputs

See `## 11. Required Outputs` above.

## 7. Hard Constraints

See `## 13. Hard Constraints` above.

## 8. Interface / Schema Constraints

See `## 14. Interface / Schema Constraints` above.

## 10. Acceptance Criteria

See `## 16. Acceptance` above.

## 11. Validation Checklist

See `## 15. Validation Checklist` above.
