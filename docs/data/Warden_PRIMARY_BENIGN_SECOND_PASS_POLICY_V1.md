<!-- operator: Codex; task: primary-benign-second-pass-policy; date: 2026-04-24 -->

# 中文定义对齐摘要

本文档按 `Warden_Threat_Definition_V1` 对齐：Warden 的威胁判断覆盖高危欺骗行为和/或高危诱导动作。未在当前采集中观察到 payload 或直接动作入口，只能记为 `payload not observed` 一类证据状态，不能自动推出 benign 结论。

# 中文摘要

## 1. 文档目的

本文件冻结 Warden 对“剩余 `primary benign candidates`”的二筛口径。

这里的二筛，指的是：

- 第一轮已先行分出 `adult`、`gambling`、`gate`、`evasion`；
- 剩余样本仍表现为 benign-like，但其中可能混入：
  - 真正的高危欺骗行为和/或高危诱导动作 threat 页；
  - 尚未切干净的 `adult` / `gambling` 残留；
  - gate / evasion 残留；
  - 文本稀疏、截图依赖、模板混淆、内容残缺等高混淆 hard cases。

本文件只定义 second-pass review policy。
它不重写：

- `TRAINSET_V1.md`
- `GATA_EVASION_AUXILIARY_SET_V1.md`
- `Warden_AUTO_LABEL_POLICY_V1.md`
- `Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- 恶意 taxonomy 顶层设计

## 2. 冻结边界

本文件采用以下冻结边界：

- `adult` / `gambling` 按高风险内容样本处理；
- 真正的 `malicious` 指高危欺骗行为和/或高危诱导动作样本；
- `gate` / `evasion` 按辅助数据处理，不进入 `TrainSet V1 primary`；
- weak labels 不是 manual gold labels；
- second-pass 输出是 routing / review 建议，不是 final truth。

## 3. second-pass 处理对象

`remaining primary benign candidates` 指：

- 已通过 capture 成功目录和基础质量门槛；
- 第一轮未被明确切到 `adult` / `gambling` / `gate` / `evasion`；
- 当前仍准备作为 benign 主池候选继续清洗的样本。

本集合不是：

- 已最终确认可进 `TrainSet V1 primary` 的 gold benign 集；
- final malicious 集；
- gate/evasion auxiliary set；
- manual 层最终裁决结果。

## 4. second-pass 必须分开的 4 条判断轴

### 4.1 Benign Purity 轴

问的是：该样本是否仍像正常网页，且没有足够强的高危欺骗行为或高危诱导动作证据把它踢出 primary benign 主池。

### 4.2 Content Warning 轴

问的是：该样本是否属于 `adult` / `gambling` 等高风险内容壳。

这条轴与最终 threat judgment 分离，不得把它提升成第三个主 threat class。

### 4.3 Threat Behavior / Action 轴

问的是：该样本是否更像高危欺骗行为和/或高危诱导动作页，例如：

- deceptive identity / authority / institution / security / financial / support / reward / access-control construction with payload not observed
- credential collection
- payment collection
- wallet / approval / seed phrase induced action
- fake support / contact diversion
- download lure / install lure

### 4.4 Auxiliary Routing 轴

问的是：该样本是否更像：

- gate / challenge shell
- evasion / cloaking shell
- 严重残缺、严重稀疏、当前证据不足且不适合直接并入 primary 的辅助样本

## 5. second-pass 默认读取层级

推荐按以下顺序读取：

1. `url.json`
2. `auto_labels.json`
3. `rule_labels.json` 如果存在
4. `forms.json`
5. `net_summary.json`
6. `visible_text.txt`
7. `screenshot_viewport.png`
8. 只有冲突时再看 `html_rendered.json` / `html_raw.json`

该顺序用于平衡准确度与效率，不改变现有 upstream contract。

## 6. second-pass 路由输出

本策略不新增 frozen on-disk schema。
它只冻结 second-pass 应输出的三类建议：

### 6.1 Dataset Routing Suggestion

建议只使用现有 `manual_dataset_admission` 家族对应的路由语义：

- `train_main`
- `eval_main`
- `aux_only`
- `exclude`
- `uncertain`

在 second-pass 语境下，它们表示“建议进入的后续池”，不是 final adjudication。

默认解释：

- `train_main`：当前证据下可继续保留为 primary benign 主池候选；
- `eval_main`：当前证据下不适合默认进 train main，但可作为保守 benign eval / reserve 使用；
- `aux_only`：更适合保留在辅助池，不进入 primary benign 主线；
- `exclude`：当前证据下不应进入 major benign usage pools；
- `uncertain`：当前证据不足，不能稳定给出路由。

### 6.2 Manual Review Queue Suggestion

second-pass 可并行给出：

- `needs_manual_review = yes / no`

它不是 final label。
它只表示是否应进入人工复核队列。

默认规则：

- unresolved benign-like hard cases 默认先进 `manual review`
- 不直接因为低信息量就自动并入 `aux_only`

### 6.3 Content Warning Suggestion

second-pass 可并行给出：

- `content_warning_candidate = none / adult / gambling / adult_and_gambling`

该建议只服务内容 warning / scenario axis，不替代 threat judgment。

## 7. 保留到 primary benign 候选的条件

样本可继续保留在 primary benign 主池候选，仅当以下条件同时成立：

1. 未出现明确高危欺骗行为或高危诱导动作证据；
2. 未出现足够强的 gate / evasion shell 证据；
3. 未命中需要单独处理的 `adult` / `gambling` 内容警示；
4. 页面质量、内容完整性和基本可解释性达标；
5. 即使属于 hard-benign / confusion-benign，也更像真实 benign，而不是 benign-like threat。

典型可保留样本包括：

- 正常服务页
- 正常内容页
- 正常品牌页
- benign OAuth / third-party auth delegate pattern
- 明确 demo / clone 但无 threat-behavior 或 induced-action 证据的 benign-like 页面

## 8. 必须踢出 primary benign 主池候选的情形

### 8.1 Route to content warning axis

若样本本质上属于 `adult` / `gambling` 内容壳，则：

- 不保留在 regular primary benign 主池；
- 应转入独立 content-warning 处理口径；
- 不把它改写成第三主 threat class。

### 8.2 Route to auxiliary

若样本更像：

- gate / challenge shell
- evasion / cloaking shell
- 严重残缺、严重 blank、当前无法代表标准页面级 benign 样本

则默认建议：

- `aux_only`

### 8.3 Route to exclude

若样本已出现足够强的 threat-behavior 或 induced-action 证据，或已明显不应被当作 benign 使用，则默认建议：

- `exclude`

例如：

- strong deceptive identity / authority / institution / security / financial / support / reward / access-control construction, even when direct payload is not observed in the current capture
- password / OTP / credential collection
- payment collection / fee demand
- wallet connect / approve / seed phrase request
- fake support contact diversion
- confirmed download lure / install lure

## 9. 必须进入 manual review 的情形

以下样本默认优先进入人工复核，而不是 second-pass 自动裁决：

- benign-like 但带强 threat-like surface signals 的 hard negatives
- low-signal / sparse / screenshot-dependent 页面
- 品牌外壳与行为信号冲突的页面
- clone / demo 与真实 hosted lure 边界不清的页面
- web3 / download / login / payment 混杂页
- `forms.json`、文本、截图、HTML 之间存在明显冲突的页面
- hosted / intermediary / trusted platform shell 上承载的高混淆样本

## 10. 与现有文档的接口边界

### 10.1 与 `TRAINSET_V1.md`

本文件不修改 `TrainSet V1 primary` 定义。
second-pass 是 primary admission 之前的清洗 / 路由策略，不等于 final admission truth。

### 10.2 与 `GATA_EVASION_AUXILIARY_SET_V1.md`

本文件明确继承该文档边界：

- `gate` / `evasion` 不自动进入 `TrainSet V1 primary`
- second-pass 只负责把残留 gate/evasion 样本重新路由回 auxiliary

### 10.3 与 `Warden_AUTO_LABEL_POLICY_V1.md`

`auto` 只提供 evidence-first weak layer。
second-pass 不把 `auto` 当 gold truth。

### 10.4 与 `Warden_RULE_LABEL_POLICY_V1_CORE.md`

本文件可参考 `rule` 层的：

- `hard_negative_candidate`
- `hard_positive_candidate`
- `gate_or_evasion_candidate`
- `needs_manual_review_candidate`
- `page_role_hint`

但不把 rule outputs 直接提升为 final judgment。

### 10.5 与 `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`

本文件只输出 review / routing suggestion。
final judgment、final page role、final dataset admission 仍属于 manual 层。

## 11. 当前执行口径

当前推荐口径如下：

- 第一轮先切出 `adult` / `gambling` / `gate` / `evasion`
- 第二轮只处理剩余 `primary benign candidates`
- second-pass 输出：
  - dataset routing suggestion
  - manual review suggestion
  - content warning suggestion
- unresolved benign-like hard cases 默认先进 `manual review`
- 只有确认属于 gate/evasion 或严重残缺时，才优先落到 `aux_only`

## 12. 非目标

本文件不负责：

- 冻结新的 JSON schema
- 重新定义恶意 taxonomy
- full-corpus manual annotation
- 替代 `manual_labels.json`
- 定义最终 split 策略
- 定义训练脚本如何具体实现 second-pass

---

# English Version

# Warden Primary Benign Second-Pass Policy V1

## 1. Purpose

This document freezes Warden's second-pass review policy for the remaining `primary benign candidates`.

Here, second-pass means:

- a first-pass rough split has already separated `adult`, `gambling`, `gate`, and `evasion`;
- the remaining pool is still benign-like, but may contain:
  - true high-risk behavior pages,
  - leftover `adult` / `gambling` samples,
  - leftover gate / evasion samples,
  - sparse, screenshot-dependent, broken, or highly confusing hard cases.

This file defines only the second-pass review policy.
It does not rewrite:

- `TRAINSET_V1.md`
- `GATA_EVASION_AUXILIARY_SET_V1.md`
- `Warden_AUTO_LABEL_POLICY_V1.md`
- `Warden_RULE_LABEL_POLICY_V1_CORE.md`
- `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`
- the top-level malicious-taxonomy design

## 2. Frozen Boundary

This policy adopts the following frozen boundary:

- `adult` / `gambling` are handled as high-risk content samples;
- true `malicious` can mean high-risk deceptive-behavior samples and/or high-risk induced-action samples;
- `gate` / `evasion` are handled as auxiliary data and do not enter `TrainSet V1 primary`;
- weak labels are not manual gold labels;
- second-pass outputs are routing and review suggestions, not final truth.

## 3. What The Second Pass Operates On

`remaining primary benign candidates` means samples that:

- already passed successful-capture and basic quality gates,
- were not clearly routed to `adult`, `gambling`, `gate`, or `evasion` during the first pass,
- are still being considered for the main benign pool.

This set is not:

- a final gold benign set already admitted into `TrainSet V1 primary`,
- a final malicious set,
- the gate/evasion auxiliary set,
- the manual layer's final adjudication result.

## 4. Four Axes That Must Stay Separate In The Second Pass

### 4.1 Benign Purity Axis

This asks whether the sample still looks like a normal webpage and whether there is insufficient high-risk deceptive-behavior or induced-action evidence to remove it from the primary benign pool.

### 4.2 Content Warning Axis

This asks whether the sample belongs to a high-risk content shell such as `adult` or `gambling`.

This axis must stay separate from final threat judgment. It must not become a third main threat class.

### 4.3 Threat Behavior / Action Axis

This asks whether the sample is better explained as a high-risk deceptive-behavior page and/or high-risk induced-action page, for example:

- deceptive identity / authority / institution / security / financial / support / reward / access-control construction with payload not observed
- credential collection
- payment collection
- wallet / approval / seed-phrase induced action
- fake support or contact diversion
- download or install lure

### 4.4 Auxiliary Routing Axis

This asks whether the sample is better explained as:

- a gate or challenge shell
- an evasion or cloaking shell
- a severely broken, severely sparse, or currently insufficient-evidence sample that should not go directly into primary

## 5. Default Read Order For The Second Pass

Recommended read order:

1. `url.json`
2. `auto_labels.json`
3. `rule_labels.json` if present
4. `forms.json`
5. `net_summary.json`
6. `visible_text.txt`
7. `screenshot_viewport.png`
8. `html_rendered.json` / `html_raw.json` only when there is a conflict

This order is meant to balance accuracy and efficiency without changing the upstream contract.

## 6. Second-Pass Outputs

This policy does not freeze a new on-disk schema.
It freezes three kinds of second-pass suggestions only.

### 6.1 Dataset Routing Suggestion

The routing semantics should stay anchored to the existing `manual_dataset_admission` family:

- `train_main`
- `eval_main`
- `aux_only`
- `exclude`
- `uncertain`

Inside second-pass review, these mean suggested downstream routing, not final adjudication.

Default interpretation:

- `train_main`: may remain in the main primary-benign candidate pool under the current evidence;
- `eval_main`: not ideal for default train-main use, but still acceptable for conservative benign evaluation or reserve usage;
- `aux_only`: better preserved in an auxiliary pool rather than the main primary-benign path;
- `exclude`: should not enter major benign usage pools under the current evidence;
- `uncertain`: the current evidence is not stable enough for routing.

### 6.2 Manual Review Queue Suggestion

The second pass may also emit:

- `needs_manual_review = yes / no`

This is not a final label.
It only states whether the sample should enter a manual-review queue.

Default rule:

- unresolved benign-like hard cases should go to `manual review` by default;
- low-information samples should not be auto-routed into `aux_only` unless they also match auxiliary criteria clearly.

### 6.3 Content Warning Suggestion

The second pass may also emit:

- `content_warning_candidate = none / adult / gambling / adult_and_gambling`

This suggestion serves the content-warning and scenario axis only. It does not replace threat judgment.

## 7. Conditions For Keeping A Sample In The Primary-Benign Candidate Pool

A sample may remain in the primary-benign candidate pool only if all of the following hold:

1. it does not show clear high-risk deceptive-behavior or induced-action evidence;
2. it does not show sufficiently strong gate/evasion-shell evidence;
3. it does not hit a content-warning condition that must be separated out as `adult` / `gambling`;
4. page quality, content completeness, and minimum interpretability remain acceptable;
5. even if it is a hard-benign or confusion-benign case, it still looks more like a real benign page than a benign-like threat.

Typical keep cases include:

- normal service pages
- normal content pages
- normal brand pages
- benign OAuth or third-party auth delegate patterns
- clearly demo or clone pages without threat-behavior or induced-action evidence

## 8. Conditions That Remove A Sample From The Main Primary-Benign Candidate Pool

### 8.1 Route to the content-warning axis

If a sample is fundamentally an `adult` / `gambling` content shell, then:

- it should not remain in the regular primary-benign pool;
- it should move into a separate content-warning handling path;
- it must not be rewritten into a third main threat class.

### 8.2 Route to auxiliary

If a sample is better explained as:

- a gate or challenge shell
- an evasion or cloaking shell
- a severely broken or severely blank sample that cannot represent a standard page-level benign sample

then the default suggestion is:

- `aux_only`

### 8.3 Route to exclude

If a sample already shows sufficiently strong threat-behavior or induced-action evidence, or clearly should not be used as benign, then the default suggestion is:

- `exclude`

Examples include:

- strong deceptive identity / authority / institution / security / financial / support / reward / access-control construction, even when direct payload is not observed in the current capture
- password, OTP, or credential collection
- payment collection or fee-demand behavior
- wallet connect, approve, or seed-phrase requests
- fake support contact diversion
- confirmed download or install lures

## 9. Cases That Must Go To Manual Review

The following cases should go to manual review by default instead of being auto-resolved by the second pass:

- benign-like hard negatives with strong threat-like surface signals
- low-signal, sparse, or screenshot-dependent pages
- pages whose brand shell conflicts with their behavior signals
- clone/demo vs. real hosted-lure boundary cases
- mixed web3 / download / login / payment pages
- pages where `forms.json`, text, screenshot, and HTML conflict materially
- high-confusion samples hosted on trusted platforms, intermediary carriers, or benign-looking shells

## 10. Interface Boundary With Existing Docs

### 10.1 With `TRAINSET_V1.md`

This file does not modify the meaning of `TrainSet V1 primary`.
The second pass is a cleaning and routing policy that happens before final primary admission. It is not the same thing as final admission truth.

### 10.2 With `GATA_EVASION_AUXILIARY_SET_V1.md`

This file inherits that boundary explicitly:

- `gate` / `evasion` do not auto-enter `TrainSet V1 primary`
- the second pass only routes leftover gate/evasion samples back into auxiliary handling

### 10.3 With `Warden_AUTO_LABEL_POLICY_V1.md`

`auto` remains an evidence-first weak layer.
The second pass must not treat `auto` as gold truth.

### 10.4 With `Warden_RULE_LABEL_POLICY_V1_CORE.md`

This file may consult rule-layer signals such as:

- `hard_negative_candidate`
- `hard_positive_candidate`
- `gate_or_evasion_candidate`
- `needs_manual_review_candidate`
- `page_role_hint`

But it must not promote rule outputs directly into final judgment.

### 10.5 With `Warden_MANUAL_LABEL_POLICY_V1_CORE.md`

This file produces review and routing suggestions only.
Final judgment, final page role, and final dataset admission still belong to the manual layer.

## 11. Current Execution Stance

The current recommended stance is:

- first pass separates `adult`, `gambling`, `gate`, and `evasion`
- second pass processes only the remaining `primary benign candidates`
- second-pass outputs consist of:
  - dataset routing suggestion
  - manual-review suggestion
  - content-warning suggestion
- unresolved benign-like hard cases should go to `manual review` by default
- only clearly gate/evasion or severely broken samples should default toward `aux_only`

## 12. Non-Goals

This file does not:

- freeze a new JSON schema
- redefine the malicious taxonomy
- require full-corpus manual annotation
- replace `manual_labels.json`
- define the final split strategy
- define how training scripts must implement second-pass execution
