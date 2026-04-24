<!-- operator: Codex; task: primary-benign-second-pass-policy; date: 2026-04-24 -->

# 中文摘要

## 交接元数据

- Handoff ID: `handoff-primary-benign-second-pass-policy-2026-04-24`
- Related Task ID: `primary-benign-second-pass-policy-2026-04-24`
- Task Title: Freeze a primary-benign second-pass review policy
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

## 1. 执行摘要

本次交付新增了一份 repo 内 active policy，用来冻结“剩余 `primary benign candidates`”的二筛口径，并同步落了一份 task doc。

这份 policy 明确写死了：

- `adult` / `gambling` 作为高风险内容样本处理；
- 真正的 `malicious` 指高危行为样本；
- `gate` / `evasion` 保持辅助数据定位，不并入 `TrainSet V1 primary`；
- second-pass 输出只属于 routing / review suggestion，不等于 final truth。

## 2. 实际变更

### Code Changes

- none

### Doc Changes

- 新增 `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`，冻结本次文档任务边界。
- 新增 `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`，定义 primary benign second-pass policy。
- 将二筛输出明确拆成三类建议：dataset routing suggestion、manual review suggestion、content warning suggestion。
- 将 unresolved benign-like hard cases 的默认路由写成先进入 `manual review`，而不是自动并入 `aux_only`。

### Output / Artifact Changes

- 新增 repo task doc
- 新增 repo active policy doc
- 新增 repo handoff doc

## 3. Files Touched

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

Optional notes per file:

- task doc 冻结了用户给出的边界和本次文档任务的 scope。
- policy doc 只补 benign second-pass 执行口径，不重写现有 TrainSet / auxiliary / auto-rule-manual 合同。
- handoff doc 只记录本次文档交付事实。

## 4. Behavior Impact

### Expected New Behavior

- 后续执行 `primary benign candidates` 二筛时，有一份 repo 内 active doc 可直接引用。
- benign purity、content warning、threat behavior、auxiliary routing 被明确拆开，降低执行时的语义漂移。
- 后续让 Codex 或 Claude Code执行二筛时，可以把输出限制为路由建议，而不是误写成 final labels。

### Preserved Behavior

- `TrainSet V1 primary` 的定义不变。
- `gate / evasion` 仍保持 auxiliary set 定位。
- `auto / rule / manual` 三层边界不变。
- `adult / gambling` 仍不成为第三个主 threat class。

### User-facing / CLI Impact

- none; doc-only change

### Output Format Impact

- none for runtime or dataset schema; this is a documentation-policy addition only

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

本次没有新增或修改任何 on-disk JSON 字段、CLI 参数、样本目录结构或 manifest contract。新增 policy 只冻结文档层的 second-pass routing semantics，并显式要求不要把其输出当作 `manual` 最终裁决。

## 6. Validation Performed

### Commands Run

```bash
rg -n "primary benign|second pass|adult|gambling|gate|evasion|manual review|aux_only|exclude|train_main|weak labels are not manual gold labels|final truth" E:\Warden\docs\data\Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
Get-ChildItem -LiteralPath E:\Warden\docs\tasks\2026-04-24_primary_benign_second_pass_policy.md,E:\Warden\docs\data\Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
```

### Result

- 关键边界词已命中：`adult`、`gambling`、`gate`、`evasion`、`train_main`、`aux_only`、`exclude`、`manual review`、`final truth`。
- task doc 和 policy doc 已在 repo 内落库。
- 我还读取并对齐了相关 active docs，并让 Claude Code 做了一轮只读结构审查；其审查意见被吸收为 policy 里的“routing suggestion 而非 final truth”边界。

### Not Run

- no runtime tests
- no schema checks beyond document/content inspection
- no script execution against dataset directories

Reason:

This is a doc-only policy task. No code, schema, CLI, or dataset-directory mutation was made.

## 7. Risks / Caveats

- 当前 policy 冻结的是文档层口径，不是最终脚本实现；真正落 review manifest / queue 时，仍需单独冻结输出字段名。
- `manual_review` 与 `manual_dataset_admission` 的接口在本次只冻结到“语义层”，未冻结具体 JSON schema。
- 仓库当前工作树本身是 dirty 的，本次交付没有清理或回滚任何与任务无关的既有改动。

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

Doc debt still remaining:

- 后续如果要把 second-pass 真正落成 review manifest / queue 产物，需要再补一份 execution-side task doc，冻结字段名和输出路径。

## 9. Recommended Next Step

- 基于这份 policy，再起一个窄范围执行任务，把“剩余 primary benign candidates 二筛”落成 review manifest / queue。
- 执行任务里直接复用本 policy 的三条输出：dataset routing suggestion、manual review suggestion、content warning suggestion。
- 执行时优先把 high-confusion 样本送人工复核，不要让 weak labels 或单一截图结果替代 final adjudication。

---

# English Version

# Handoff Metadata

- Handoff ID: `handoff-primary-benign-second-pass-policy-2026-04-24`
- Related Task ID: `primary-benign-second-pass-policy-2026-04-24`
- Task Title: Freeze a primary-benign second-pass review policy
- Module: Data / Labeling
- Author: Codex
- Date: 2026-04-24
- Status: DONE

## 1. Executive Summary

This delivery adds an active in-repo policy for second-pass review of the remaining `primary benign candidates`, together with a task doc for the work.

The policy freezes the following boundary:

- `adult` / `gambling` are handled as high-risk content samples;
- true `malicious` means high-risk behavior samples;
- `gate` / `evasion` remain auxiliary data and do not re-enter `TrainSet V1 primary`;
- second-pass outputs remain routing and review suggestions rather than final truth.

## 2. What Changed

### Code Changes

- none

### Doc Changes

- Added `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md` to freeze the task boundary for this documentation work.
- Added `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md` as the active primary-benign second-pass policy.
- Explicitly split second-pass outputs into three suggestion families: dataset routing suggestion, manual-review suggestion, and content-warning suggestion.
- Froze unresolved benign-like hard cases to default into `manual review` rather than being auto-routed into `aux_only`.

### Output / Artifact Changes

- new repo task doc
- new repo active policy doc
- new repo handoff doc

## 3. Files Touched

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

Optional notes per file:

- the task doc freezes the user-provided boundary and scope;
- the policy doc fills only the benign second-pass execution gap and does not rewrite TrainSet / auxiliary / auto-rule-manual contracts;
- the handoff doc records this documentation delivery only.

## 4. Behavior Impact

### Expected New Behavior

- future second-pass review of `primary benign candidates` now has a dedicated active policy doc in the repo;
- benign purity, content warning, threat behavior, and auxiliary routing are explicitly separated;
- future execution by Codex or Claude Code can keep outputs at the routing-suggestion level instead of accidentally treating them as final labels.

### Preserved Behavior

- the meaning of `TrainSet V1 primary` is unchanged;
- `gate / evasion` remain auxiliary-set material;
- the `auto / rule / manual` boundary is unchanged;
- `adult / gambling` still do not become a third main threat class.

### User-facing / CLI Impact

- none; doc-only change

### Output Format Impact

- none for runtime or dataset schema; this is a documentation-policy addition only

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This change does not add or modify any on-disk JSON fields, CLI parameters, sample-directory structure, or manifest contract. It only freezes document-level second-pass routing semantics and explicitly prevents those outputs from being treated as `manual` final adjudication.

## 6. Validation Performed

### Commands Run

```bash
rg -n "primary benign|second pass|adult|gambling|gate|evasion|manual review|aux_only|exclude|train_main|weak labels are not manual gold labels|final truth" E:\Warden\docs\data\Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
Get-ChildItem -LiteralPath E:\Warden\docs\tasks\2026-04-24_primary_benign_second_pass_policy.md,E:\Warden\docs\data\Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md
```

### Result

- the key boundary terms were found in the new policy doc: `adult`, `gambling`, `gate`, `evasion`, `train_main`, `aux_only`, `exclude`, `manual review`, and `final truth`;
- the task doc and policy doc were created successfully in the repo;
- I also read the related active docs and ran one bounded read-only Claude Code structure review; its main warning about keeping second-pass outputs as routing suggestions rather than final truth was incorporated into the policy.

### Not Run

- no runtime tests
- no schema checks beyond document/content inspection
- no dataset-directory script execution

Reason:

This is a doc-only policy task. No code, schema, CLI, or dataset-directory mutation was made.

## 7. Risks / Caveats

- the current freeze is at the documentation-policy level, not the final script implementation level; a later execution task is still required to freeze actual review-manifest or queue field names;
- the interface between `manual_review` semantics and `manual_dataset_admission` remains frozen only at the semantic level in this task, not as a concrete JSON schema;
- the repository worktree is already dirty; this delivery did not clean or revert any unrelated pre-existing changes.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-24_primary_benign_second_pass_policy.md`
- `docs/data/Warden_PRIMARY_BENIGN_SECOND_PASS_POLICY_V1.md`
- `docs/handoff/2026-04-24_primary_benign_second_pass_policy.md`

Doc debt still remaining:

- if the second pass is later implemented as a real review manifest or review queue artifact, a separate execution-side task doc is still needed to freeze field names and output paths.

## 9. Recommended Next Step

- Start a narrow execution task that turns this policy into a concrete review manifest / review queue for the remaining primary-benign candidates.
- Reuse the three policy outputs directly: dataset routing suggestion, manual-review suggestion, and content-warning suggestion.
- During execution, route high-confusion samples to manual review first rather than letting weak labels or a single screenshot substitute for final adjudication.
