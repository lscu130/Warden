# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-13-gate-fn-mining
- Related Task ID: TASK-L0-2026-04-13-GATE-FN-MINING
- Task Title: 专项挖掘 gate false negative，聚焦 matched_keywords 为空的漏检页
- Module: Inference
- Author: Codex
- Date: 2026-04-13
- Status: DONE

---

## 1. Executive Summary

本次交付专门处理 `gate` specialized detector 的 false negative，范围严格收紧到 `matched_keywords = []` 的 gate 漏检页。  
先做了漏检样本分型，再补最小 patch。

这轮 false-negative mining 的核心发现：

- 旧版本 gate full recall 约 `59.3%`
- 漏检里有 `74` 个 `matched_keywords = []` 样本
- 其中约 `46` 个是 `visible_text` 基本为空的捕获空洞页
- 其余约 `28` 个有文本，但属于当前词表没覆盖的 gate 语义

本次 patch 只补了第二类，也就是“有文本但漏词”的 gate FN。  
结果：

- `gate` full recall 从 `59.3%` 提升到 `72.5%`
- `ordinary_benign` 200 样本切片上的 gate 触发率保持在 `2.5%`
- `adult` / `gambling` 切片上的 gate cross-trigger 仍接近零

剩余未解决的 FN 现在主要是截图里有 challenge 文本、但 `visible_text.txt` 为空的捕获空洞页。

---

## 2. What Changed

### Code Changes

- 更新 `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- 扩展 gate 词表，补入这轮 false-negative mining 找到的未覆盖模式：
  - `idp verification`
  - `protected by idp`
  - `solve the equation`
  - `enter the code below`
  - `code refreshes`
  - `verificando`
  - `please prove that you are human`
  - `sicherheitsüberprüfung wird durchgeführt`
  - `ich bin kein roboter`
  - `humancheck`
  - `select the box to continue`
  - `tap the box to verify`
  - `privacy-friendly check`
  - `verify to sign`
  - `verify your identity`
  - `verification code`
  - `copy code`
  - `secure portal`
  - `click here to continue`
  - `click to continue`
  - `点击继续访问`
- 增加 `gate_short_flow_hit`，用于短文本、低表单密度、带 loading / continue / secure-portal 语义的 gate 页
- 增加 `gate_identity_flow_hit`，用于短文本、低表单密度、带 verification-code / verify-identity / verify-to-sign 语义的 gate 页
- 保持现有 gate 主路径不变：仍然优先依赖强 gate/challenge 文本和带文本支撑的 runtime/provider support

### Doc Changes

- 更新 task：`docs/tasks/2026-04-13_gate_fn_mining.md`
- 新增 handoff：`docs/handoff/2026-04-13_gate_fn_mining.md`
- 未修改 `L0_DESIGN_V1.md`，因为 specialized contract 和字段集合没有变化

### Output / Artifact Changes

- 字段集合没有变化
- 输出 schema 没变化
- 新增的是 gate false-negative pattern summary 和这轮 focused validation 结果

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: 只补 gate FN 挖出来的模式，不碰 `adult` / `gambling`
- `docs/tasks/2026-04-13_gate_fn_mining.md`: 仅将状态更新为 `DONE`
- `docs/handoff/2026-04-13_gate_fn_mining.md`: 记录 false-negative pattern、实现 patch 和验证结果

---

## 4. Behavior Impact

### Expected New Behavior

- 旧版本漏掉的 `IDP Verification`、`Verificando`、`HumanCheck`、`Please prove that you are human`、德语验证码确认页、DocuSign / Microsoft verification-code gate 页，现在会稳定打出 `possible_gate_or_evasion`
- gate 现在对短文本 challenge/interstitial 页更敏感，只要文本里有明确 verification / continue / box / code 语义，并且页面没有明显敏感表单，就更容易命中
- 剩余 gate miss 主要集中到 capture failure / empty visible-text 这类文本缺失页

### Preserved Behavior

- 不重新引入 `possible_fake_verification`
- 不重新引入 `possible_interaction_required`
- 不修改 `gambling` / `adult` specialized family
- `specialized_surface_signals` 和 `l0_routing_hints` 的字段集合保持不变

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

- none

Compatibility notes:

本次只改已有 gate 弱信号的形成逻辑，没加字段、没删字段、没改字段名、没改函数签名、没改 CLI。  
下游如果依赖的是 schema presence 或 `evt_v1.2`，不需要改。  
变化体现在 gate 触发率和 reason path，而不是接口。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- enumerate `E:\Warden\data\raw\benign\gate`
- collect current misses where:
  - `possible_gate_or_evasion = false`
  - `matched_keywords.gate_text = []`
- classify them by:
  - empty visible text
  - filename / URL hint
  - loading-like text
  - credential-like text

PowerShell heredoc piped to `python -`:
- run focused smoke on representative misses:
  - `burraqtechnologies.com_statement_20260401T005758Z`
  - `crmcupoflb.web.app_20260318T072401Z`
  - `cuonet.com_20260402T175831Z`
  - `prevengo3.netsons.org_master_20260129T151639Z`
  - `pub-5f42dfaab80a4e1583ad07d911dd504d.r2.dev_...`
  - `docusign-auth-docusign-com.dporozok.workers.dev_...`
  - `secure-device-auth-office-com.dporozok.workers.dev_...`
- run benign controls:
  - `cp.pt_20260408T071621Z`
  - `talksport.com_20260401T091722Z`
  - `autoscout24.pl_20260403T023010Z`

PowerShell heredoc piped to `python -`:
- run gate-focused regression on:
  - full `gate` pool
  - `ordinary_benign` random slice of 200
  - `adult` random slice of 200
  - `gambling` random slice of 200
- random seed: `20260413`
```

### Result

- 语法检查通过
- false-negative mining 结果：
  - `74` 个 `matched_keywords = []` gate miss
  - 其中 `46` 个是 `empty_visible_text`
  - 其余 `28` 个有文本，可继续挖词
- 代表样本 smoke：
  - `burraqtechnologies...` 现在命中：
    - `idp verification`
    - `protected by idp`
    - `solve the equation`
  - `crmcupoflb.web.app...` 现在命中：
    - `verificando`
  - `cuonet.com...` 现在命中：
    - `please prove that you are human`
  - `prevengo3.netsons...` 现在命中：
    - `sicherheitsüberprüfung wird durchgeführt`
    - `ich bin kein roboter`
  - `pub-...r2.dev...` 现在命中：
    - `humancheck`
    - `tap the box to verify`
    - `privacy-friendly check`
  - `docusign-auth...` / `secure-device-auth...` 现在命中：
    - `verify your identity`
    - `verification code`
    - `copy code`
  - `cp.pt`、`talksport.com`、`autoscout24.pl` 仍不触发 gate
- gate-focused regression：
  - `gate` full pool:
    - `possible_gate_or_evasion`: `72.5%`
    - 旧基线约 `59.3%`
  - `ordinary_benign` 200:
    - `possible_gate_or_evasion`: `2.5%`
  - `adult` 200:
    - `possible_gate_or_evasion`: `0.5%`
  - `gambling` 200:
    - `possible_gate_or_evasion`: `0.0%`

### Not Run

- 全量普通 benign 全集回归
- 人工金标复审
- 任何训练或部署流程

Reason:

本次任务只要求 gate FN mining、focused validation 和 gate-oriented regression，不要求重跑全仓库全集或进入训练/部署阶段。

---

## 7. Risks / Caveats

- 当前剩余 gate miss 的主力已经不是漏词，主力是 `visible_text.txt` 为空的 capture failure 页
- 这些空白页里有一批从截图上看确实是真 gate，但当前脚本没有 OCR 或截图语义能力，单靠现有文本工件无法稳妥补
- `ordinary_benign` 上 gate 触发率在这轮 200 切片里是 `2.5%`，没有明显回弹，但 `challenge` / `captcha` 一类词仍然是主要 benign gate 噪音来源

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

Doc debt still remaining:

- 如果后续继续追 gate recall，建议单开一条 `empty visible-text gate capture gap` 任务
- 如果后续要引入截图级语义或 OCR，需要单独冻结新输入能力和兼容性边界

---

## 9. Recommended Next Step

- 单开一条 `empty visible-text gate capture gap` 任务，专门处理截图里可见、但 `visible_text.txt` 缺失的 gate 页
- 在那条任务里先确认是否允许使用截图 OCR 或截图级 lightweight semantics
- 当前这条 gate FN mining 可以视为完成，下一步不该再继续放宽纯文本 gate 条件

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# Handoff Metadata

- Handoff ID: 2026-04-13-gate-fn-mining
- Related Task ID: TASK-L0-2026-04-13-GATE-FN-MINING
- Task Title: Mine gate false negatives with a strict focus on pages whose matched_keywords are empty
- Module: Inference
- Author: Codex
- Date: 2026-04-13
- Status: DONE

---

## 1. Executive Summary

This delivery focused specifically on `gate` specialized-detector false negatives, with the scope tightly restricted to gate misses whose `matched_keywords` were empty.  
The work started with false-negative classification and then applied the smallest valid implementation patch.

The core findings from this false-negative mining pass were:

- the previous full-pool gate recall was about `59.3%`
- there were `74` gate misses with `matched_keywords = []`
- about `46` of those were capture-gap pages with almost empty `visible_text`
- the remaining `28` had visible text but represented uncovered gate semantics

This patch addressed only the second class: text-visible gate false negatives caused by missing lexicon coverage.  
The results were:

- full-pool gate recall improved from `59.3%` to `72.5%`
- the gate trigger rate on a 200-sample `ordinary_benign` slice stayed at `2.5%`
- gate cross-triggering on `adult` and `gambling` control slices remained near zero

The dominant remaining false-negative family is now capture-gap pages where challenge text is visible in the screenshot but absent from `visible_text.txt`.

---

## 2. What Changed

### Code Changes

- updated `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- expanded the gate lexicon with the uncovered patterns found during false-negative mining:
  - `idp verification`
  - `protected by idp`
  - `solve the equation`
  - `enter the code below`
  - `code refreshes`
  - `verificando`
  - `please prove that you are human`
  - `sicherheitsüberprüfung wird durchgeführt`
  - `ich bin kein roboter`
  - `humancheck`
  - `select the box to continue`
  - `tap the box to verify`
  - `privacy-friendly check`
  - `verify to sign`
  - `verify your identity`
  - `verification code`
  - `copy code`
  - `secure portal`
  - `click here to continue`
  - `click to continue`
  - `点击继续访问`
- added `gate_short_flow_hit` for short-text, low-form-density pages with loading / continue / secure-portal semantics
- added `gate_identity_flow_hit` for short-text, low-form-density pages with verification-code / verify-identity / verify-to-sign semantics
- preserved the existing primary gate path: strong gate/challenge text and runtime/provider support that is backed by text remain the main route

### Doc Changes

- updated task doc: `docs/tasks/2026-04-13_gate_fn_mining.md`
- added handoff doc: `docs/handoff/2026-04-13_gate_fn_mining.md`
- did not modify `L0_DESIGN_V1.md` because the specialized contract and field set were unchanged

### Output / Artifact Changes

- no field-set change
- no output-schema change
- the new artifacts are the gate false-negative pattern summary and the focused validation results

---

## 3. Files Touched

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

Optional notes per file:

- `scripts/labeling/Warden_auto_label_utils_brandlex.py`: only gate false-negative patterns were added; `adult` and `gambling` were left unchanged
- `docs/tasks/2026-04-13_gate_fn_mining.md`: only the status was updated to `DONE`
- `docs/handoff/2026-04-13_gate_fn_mining.md`: records the false-negative patterns, implementation patch, and validation results

---

## 4. Behavior Impact

### Expected New Behavior

- the previously missed patterns such as `IDP Verification`, `Verificando`, `HumanCheck`, `Please prove that you are human`, the German bot-check pages, and the DocuSign / Microsoft verification-code gate pages now emit `possible_gate_or_evasion`
- the gate detector is now more sensitive to short challenge/interstitial pages when they contain clear verification / continue / box / code semantics and do not expose obvious sensitive forms
- the remaining gate misses are now concentrated mainly in capture-gap / empty-visible-text pages

### Preserved Behavior

- `possible_fake_verification` was not reintroduced
- `possible_interaction_required` was not reintroduced
- the `gambling` and `adult` specialized families were not modified
- the field sets of `specialized_surface_signals` and `l0_routing_hints` remain unchanged

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

- none

Compatibility notes:

This task only changed how existing gate weak signals are formed. It did not add fields, remove fields, rename fields, change function signatures, or change CLI behavior.  
Downstream consumers that depend on schema presence or `evt_v1.2` remain compatible.  
The changes are behavioral in trigger rates and reason paths rather than interface-level.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile "E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py"

PowerShell heredoc piped to `python -`:
- enumerate `E:\Warden\data\raw\benign\gate`
- collect current misses where:
  - `possible_gate_or_evasion = false`
  - `matched_keywords.gate_text = []`
- classify them by:
  - empty visible text
  - filename / URL hint
  - loading-like text
  - credential-like text

PowerShell heredoc piped to `python -`:
- run focused smoke on representative misses:
  - `burraqtechnologies.com_statement_20260401T005758Z`
  - `crmcupoflb.web.app_20260318T072401Z`
  - `cuonet.com_20260402T175831Z`
  - `prevengo3.netsons.org_master_20260129T151639Z`
  - `pub-5f42dfaab80a4e1583ad07d911dd504d.r2.dev_...`
  - `docusign-auth-docusign-com.dporozok.workers.dev_...`
  - `secure-device-auth-office-com.dporozok.workers.dev_...`
- run benign controls:
  - `cp.pt_20260408T071621Z`
  - `talksport.com_20260401T091722Z`
  - `autoscout24.pl_20260403T023010Z`

PowerShell heredoc piped to `python -`:
- run gate-focused regression on:
  - the full `gate` pool
  - a 200-sample `ordinary_benign` slice
  - a 200-sample `adult` slice
  - a 200-sample `gambling` slice
- random seed: `20260413`
```

### Result

- syntax check passed
- false-negative mining results:
  - `74` gate misses with `matched_keywords = []`
  - `46` of them were `empty_visible_text`
  - the remaining `28` had visible text and were therefore still mineable through lexicon / rule work
- representative smoke:
  - `burraqtechnologies...` now matches:
    - `idp verification`
    - `protected by idp`
    - `solve the equation`
  - `crmcupoflb.web.app...` now matches:
    - `verificando`
  - `cuonet.com...` now matches:
    - `please prove that you are human`
  - `prevengo3.netsons...` now matches:
    - `sicherheitsüberprüfung wird durchgeführt`
    - `ich bin kein roboter`
  - `pub-...r2.dev...` now matches:
    - `humancheck`
    - `tap the box to verify`
    - `privacy-friendly check`
  - `docusign-auth...` and `secure-device-auth...` now match:
    - `verify your identity`
    - `verification code`
    - `copy code`
  - `cp.pt`, `talksport.com`, and `autoscout24.pl` still do not trigger as gate
- gate-focused regression:
  - full `gate` pool:
    - `possible_gate_or_evasion`: `72.5%`
    - previous baseline was about `59.3%`
  - `ordinary_benign` 200:
    - `possible_gate_or_evasion`: `2.5%`
  - `adult` 200:
    - `possible_gate_or_evasion`: `0.5%`
  - `gambling` 200:
    - `possible_gate_or_evasion`: `0.0%`

### Not Run

- a full ordinary-benign dataset rerun
- manual gold-label review
- any training or deployment workflow

Reason:

This task was scoped to gate false-negative mining, focused validation, and a gate-oriented regression slice rather than a full-repo rerun or training/deployment work.

---

## 7. Risks / Caveats

- the dominant remaining gate false-negative family is no longer lexicon coverage; it is capture-gap pages where `visible_text.txt` is empty
- a subset of those empty-text pages still appear to be real gate pages in screenshots, but the current script has no OCR or screenshot-semantic capability, so those pages cannot be repaired safely through the current text-only path alone
- the gate trigger rate on the `ordinary_benign` 200-sample slice stayed at `2.5%` without a clear rebound, but `challenge` / `captcha` wording remains the main benign source of gate noise

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/tasks/2026-04-13_gate_fn_mining.md`
- `docs/handoff/2026-04-13_gate_fn_mining.md`

Doc debt still remaining:

- if gate recall is pushed further, a dedicated `empty visible-text gate capture gap` task is recommended
- if screenshot-level OCR or lightweight screenshot semantics are considered later, the new input capability and compatibility boundary should be frozen in a separate task

---

## 9. Recommended Next Step

- open a dedicated `empty visible-text gate capture gap` task for gate pages that are visually obvious in screenshots but missing from `visible_text.txt`
- in that task, decide explicitly whether screenshot OCR or lightweight screenshot semantics are allowed
- this gate false-negative mining task should stop here rather than further loosening the pure-text gate rules
