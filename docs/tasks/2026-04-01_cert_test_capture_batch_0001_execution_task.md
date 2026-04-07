# 2026-04-01_cert_test_capture_batch_0001_execution_task

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 这是 CERT 3 月批次首批 test 抓取的任务定义。
- 若涉及精确输入批次、输出目录、推荐命令或执行边界，以英文版为准。

## 1. 背景

用户希望先拿 CERT 3 月批次的第一个 batch 做一次小规模抓取测试，用来判断这个 feed 的实际质量。当前已有的 March-only CERT 批次是 domain-only TXT，不是完整 URL，但仓库 capture 脚本会自动为无协议输入补 `https://`，因此该 batch 可以直接用于 test capture。

## 2. 目标

冻结一份 execution-ready task：使用 `CERT_2026_03_only_batch_0001_domains.txt` 作为输入，跑一次 malicious capture test，输出到独立目录，便于后续人工检查这个 feed 的有效性与页面质量。

## 3. 范围

- 纳入：test capture task、prep handoff、精确输入输出与命令
- 排除：capture 核心逻辑修改、批次重切分、全量 CERT 抓取执行、结果质量结论伪造

## English Version

# Task Metadata

- Task ID: WARDEN-CERT-TEST-CAPTURE-BATCH-0001-V1
- Task Title: Freeze an execution-ready test capture task for the first March-only CERT batch so the feed quality can be inspected
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`; `scripts/data/malicious/run_malicious_capture.py`; `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`; `cert csv/CERT_2026_03_only_batch_0001_domains.txt`; `docs/handoff/2026-04-01_cert_domains_2026_03_only_batch_split.md`
- Created At: 2026-04-01
- Requested By: user

---

## 1. Background

The user wants a small test capture from the CERT feed so the practical feed quality can be inspected before committing to broader capture work.

The newly generated March-only CERT export provides a convenient bounded input:

- `E:\Warden\cert csv\CERT_2026_03_only_batch_0001_domains.txt`

That batch contains `500` lines and is domain-only rather than full URLs.
However, the current capture script implementation normalizes scheme-less inputs by prepending `https://`, so this batch can still be used directly for a test capture run.

The immediate need is not a feed-quality conclusion yet.
The immediate need is an execution-ready task boundary and prep artifact that freeze:

- the exact test input batch
- the exact output root
- the exact runner command
- the assumptions and validation relevant to domain-only input

---

## 2. Goal

Create an execution-ready task definition for a CERT test capture that uses only the first March-only CERT batch.

The task should freeze the exact input path, output root, runner command, and operational assumptions so the later test run can be executed consistently and then reviewed for feed quality.

---

## 3. Scope In

This task is allowed to touch:

- `docs/tasks/`
- `docs/handoff/`
- current CERT batch artifacts for reference only

This task is allowed to change:

- execution-boundary docs for the CERT test capture
- exact command and output-root recommendations for this test

---

## 4. Scope Out

This task must NOT do the following:

- do not change capture code or runner behavior
- do not regenerate or rename the CERT batch files
- do not claim the test capture already ran
- do not fabricate any feed-quality conclusion before actual results exist

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/handoff/2026-03-28_plan_a_batch_capture_day5_vm_prep.md`
- `docs/handoff/2026-04-01_cert_domains_2026_03_only_batch_split.md`

### Code / Scripts

- `scripts/data/malicious/run_malicious_capture.py`
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`

### Data / Artifacts

- `cert csv/CERT_2026_03_only_batch_0001_domains.txt`

### Prior Handoff

- `docs/handoff/2026-04-01_cert_domains_2026_03_only_batch_split.md`

### Missing Inputs

- actual capture results do not exist yet and must not be invented

---

## 6. Required Outputs

This task should produce:

- a repo task doc for the CERT batch-0001 test capture
- a repo prep/handoff doc with exact command and output root for the test run

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.

Task-specific constraints:

- Use only `CERT_2026_03_only_batch_0001_domains.txt` as the test input batch.
- Keep the output root separate from other capture runs.
- Use the existing supervised malicious runner command shape.
- Document explicitly that the input file is domain-only and relies on the capture script's scheme normalization behavior.
- Do not claim any test result until the actual capture is executed.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `scripts/data/malicious/run_malicious_capture.py` CLI
- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` URL normalization behavior
- current output-root naming discipline

Schema / field constraints:

- Schema changed allowed: NO
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/malicious/run_malicious_capture.py --help`
  - current malicious runner flags

Downstream consumers to watch:

- operator review of the CERT feed quality
- later result handoff for this test batch

---

## 9. Suggested Execution Plan

Recommended order:

1. Freeze the CERT batch-0001 test boundary in a repo task doc.
2. Freeze the exact output root and exact command in a prep handoff.
3. Reuse current supervised malicious-runner defaults.
4. Let the later operator run the test and then assess the resulting sample quality.

Task-specific execution notes:

- input batch size is `500`
- input lines are bare domains
- the capture script normalizes scheme-less inputs to `https://...`
- recommended source tag for this test is `cert`

---

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] the CERT test has its own repo task doc
- [ ] the doc freezes `CERT_2026_03_only_batch_0001_domains.txt` as the only test input
- [ ] the doc freezes an exact output root and exact command
- [ ] the doc documents the bare-domain input assumption correctly
- [ ] no code behavior changed
- [ ] docs were updated
- [ ] final response follows required engineering format
- [ ] prep/handoff is provided

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] the local batch filename exists
- [ ] the batch line count was checked
- [ ] the malicious runner still exposes the required flags
- [ ] the capture script normalization behavior was verified in code

Commands to run if applicable:

```bash
python E:\Warden\scripts\data\malicious\run_malicious_capture.py --help
```

Expected evidence to capture:

- confirmed input filename and line count for the CERT test batch
- exact output root for the CERT test
- exact supervised command for the CERT test
- evidence that scheme-less inputs are normalized to `https://...`

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Repo handoff path if one should be created:

- `docs/handoff/2026-04-01_cert_test_capture_batch_0001_prep.md`

---

## 13. Open Questions / Blocking Issues

List unresolved items before execution if they exist:

- none
