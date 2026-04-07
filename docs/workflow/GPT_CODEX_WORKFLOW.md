# GPT_CODEX_WORKFLOW.md

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本文档定义 GPT web、Codex 与项目负责人之间的默认协作流程。
- 涉及强制顺序、角色边界和切窗规则时，以英文版为准。
- 若交付物是 Markdown 文档，默认必须双语：中文摘要在前，英文全文在后，且英文对 AI 保持权威。

## 1. 文档作用

本工作流用于防止上下文漂移、边界失控和“模型自以为已经验证”的伪事实。
它把协作固定成四步：需求澄清、任务生成、执行交付、复核验收。

## 2. 角色摘要

- GPT web：负责长上下文综合、任务草拟、二次复核。
- Codex：负责读仓库、编辑、执行命令、验证和交付。
- 人类负责人：负责冻结边界、做最终接受和跨窗口延续。
- 若交付的是 Markdown 文档，默认按“中文摘要在前、英文全文在后、英文权威”执行。

## 3. 阅读重点

优先看英文版的：

- `Absolute Rules`
- `Standard Workflow Overview`
- `Step Two: Generate The Task Document`
- `Step Three: Hand The Work To Codex`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# GPT_CODEX_WORKFLOW.md

This workflow document defines the collaboration contract between GPT web chat, Codex, and the human project owner inside Warden.

The goal is not to let models improvise freely. The goal is:

1. GPT web handles higher-level design, long-context synthesis, task drafting, and secondary review.
2. Codex handles repository reading, execution, editing, command running, validation, and delivery.
3. The human owner freezes boundaries, decides acceptance, and makes merge or release decisions.

This is the default collaboration method, not an optional suggestion.

## 1. Purpose

This workflow exists to make Warden collaboration strict, auditable, and low-ambiguity.

It is designed to prevent common failure modes such as:

- GPT claiming local execution facts it cannot verify;
- Codex receiving vague work and expanding scope on its own;
- frozen fields or labels changing without explicit approval;
- long-context threads drifting into partial memory and unstable assumptions.

## 2. Default Roles

### 2.1 GPT Web Default Role

GPT web is the default:

- overall designer;
- specification reviewer;
- long-context summarizer;
- task-definition drafter;
- secondary reviewer;
- handoff-summary organizer.

GPT web is not the default:

- local repository executor;
- witness that tests were run;
- sole source of truth for terminal output;
- final merge or acceptance authority.

### 2.2 Codex Default Role

Codex is the default:

- execution engineer;
- repository reader;
- file editor;
- command runner;
- diff deliverer;
- first-pass self-checker.

Codex is not the default:

- final architecture approver;
- semantic approver for label redesign;
- approver for frozen-field renaming;
- final release authority.

### 2.3 Human Default Role

The human owner is the default:

- project manager;
- requirement splitter;
- boundary freezer;
- final acceptor;
- documentation merger;
- cross-window continuity coordinator.

Final judgment responsibility cannot be outsourced to the model.

## 3. Absolute Rules

The following rules are mandatory:

1. Do not send ambiguous implementation requests directly to Codex.
2. Do not let GPT web pretend it already ran local commands.
3. Do not let Codex silently refactor an entire module.
4. Do not skip `AGENTS.md`.
5. Do not skip task-definition requirements from `TASK_TEMPLATE.md`.
6. Do not skip handoff requirements from `HANDOFF_TEMPLATE.md`.
7. Do not modify frozen fields, file names, or enumerations without explicit approval.
8. Do not treat weak labels as human gold labels.
9. Do not treat "the model thinks this is fine" as acceptance.
10. Do not let two windows modify the same shared interface without freezing the contract first.
11. Do not treat GPT web output as already-verified engineering fact.
12. When a web-chat context becomes too long, slow, or hallucination-prone, summarize first and then continue in a fresh window.
13. When a task needs GPT web again for requirement clarification, secondary review, or cross-window continuation, Codex should explicitly remind the user to return there.
14. If active artifacts live outside the repository and future collaboration depends on them, copy them into the repo and return the repo path explicitly.
15. When the deliverable is a Markdown document, write it as bilingual by default: a Chinese summary first for human reading, followed by the full English version for AI reading.
16. For Markdown deliverables, English remains the authoritative version whenever exact wording, fields, commands, priorities, validation claims, or historical facts matter.

## 4. Standard Workflow Overview

The standard sequence is fixed:

1. Requirement clarification.
2. Task generation.
3. Execution and delivery.
4. Review and acceptance.

The order should not be shuffled casually.

## 5. Step One: Requirement Clarification

Requirement clarification should happen in GPT web before Codex execution when the task is broad, risky, or context-heavy.

### 5.1 When GPT Web Must Be Used First

Use GPT web first when:

- the task spans multiple modules;
- schema, labels, directory layout, CLI, or outputs may be affected;
- the context is long;
- multiple prior handoffs matter;
- the request is ambiguous;
- `PROJECT.md` or module docs may need alignment;
- the work depends on multiple prior chat windows;
- the task must first be converted into a low-ambiguity engineering scope.

### 5.2 Inputs For GPT Web

The GPT web step should receive:

- `AGENTS.md`;
- `PROJECT.md`;
- relevant module docs;
- the latest relevant handoff;
- the current target description;
- repository-tree or script excerpts when needed;
- a previous-window summary when the context comes from an older thread.

If critical inputs are missing, that fact should be stated explicitly instead of being hidden.

### 5.3 Required GPT Web Output

GPT web should return a structured task conclusion rather than vague advice.

The recommended output fields are:

- `goal`
- `scope_in`
- `scope_out`
- `constraints`
- `files_to_touch`
- `acceptance`
- `risks`
- `doc_updates_needed`

### 5.4 What GPT Web Must Not Do At This Stage

GPT web must not:

- pretend code already ran;
- pretend it already read the whole local repository;
- output a large uncontrolled refactor as if the scope were frozen;
- rename frozen fields;
- fill pages with weak "could consider" fluff;
- state unverified repository status as fact.

## 6. Step Two: Generate The Task Document

### 6.1 Who Produces It

By default, GPT web drafts the structured task content first and the human owner then places it into the task template.

### 6.2 What The Task Document Must Pin Down

The task document must explicitly define:

- background;
- goal;
- allowed scope;
- forbidden scope;
- input files;
- required outputs;
- hard constraints;
- interface or schema constraints;
- acceptance conditions;
- minimum validation requirements.

### 6.3 What The Task Document Must Avoid

Avoid weak phrases such as:

- "optimize as appropriate";
- "refactor if necessary";
- "adjust structure if needed";
- "try to stay compatible";
- "change as appropriate".

Replace them with hard statements such as:

- do not modify top-level JSON keys;
- do not add third-party dependencies;
- do not touch the training module;
- only edit files under a specific path;
- old CLI entry points must remain runnable.

## 7. Step Three: Hand The Work To Codex

### 7.1 Codex Inputs

Codex should receive at least:

- `AGENTS.md`;
- `PROJECT.md`;
- relevant module docs;
- a completed task document based on `TASK_TEMPLATE.md`.

When the task depends on prior history, also provide:

- the latest handoff;
- a relevant diff summary;
- bugs or error reports if applicable.

### 7.2 Fixed Execution Instructions For Codex

The execution instruction given to Codex should follow this shape:

1. Read relevant files before editing.
2. State which files will be changed.
3. Edit only inside `scope_in`.
4. Do not touch `scope_out`.
5. Prefer the smallest valid patch.
6. Run the minimum necessary validation.
7. Produce a handoff.
8. If the deliverable is Markdown, write it as bilingual Chinese-summary-first / full-English-second, with English authoritative.

### 7.3 Required Codex Output

Codex must finally deliver:

- Summary
- Files Changed
- Key Logic Changes
- Validation Performed
- Compatibility Impact
- Risks / Caveats
- Recommended Next Step

If the task is non-trivial, Codex must also provide a handoff aligned with `HANDOFF_TEMPLATE.md`.

### 7.4 What Codex Must Not Do

Codex must not:

- perform opportunistic large refactors;
- rename fields to match personal preference;
- silently fix extra items outside scope;
- claim "should be fine" without validation;
- omit compatibility impact;
- hide documentation-update requirements.

## 8. Step Four: Review And Acceptance

After Codex finishes, the process should return to GPT web for review and then to the human owner for final acceptance.

### 8.1 Why GPT Web Is Used Again

Codex executes the work, but it does not make the final approval decision.

GPT web is useful here for:

- checking whether the task requirements were met;
- checking whether forbidden scope was touched;
- checking interface or schema risk;
- checking whether documentation debt was missed;
- checking whether the proposed next step is coherent;
- deciding whether the work should continue in a fresh chat window.

### 8.2 Materials To Provide For Review

The review step should receive:

- Codex's final output;
- a key diff summary;
- validation results;
- the handoff content;
- updated document excerpts if docs changed.

### 8.3 Recommended GPT Web Review Output

The suggested structured review format is:

- `accept: yes / no / partial`
- `requirement_coverage`
- `interface_break_risk`
- `missing_validation`
- `missing_doc_updates`
- `notable_risks`
- `recommended_next_task`

### 8.4 What GPT Web Must Not Do In Review

GPT web must not:

- approve work only because the reasoning sounds plausible;
- treat unrun validation as passed validation;
- replace the human owner as final approver;
- downplay interface breakage;
- state unverified repository status as certain fact.

## 9. Who Performs Final Acceptance

Only the human owner performs final acceptance.

The acceptance order should be:

1. Was the goal completed?
2. Did the change cross scope boundaries?
3. Were frozen fields or outputs touched?
4. Was validation actually run?
5. Was compatibility impact stated clearly?
6. Do related docs also need updates?
7. Is the next step clear?

The model can assist, but it cannot replace final approval.

## 10. Recommended Split For Four Task Types

### 10.1 Architecture / Specification Tasks

Prefer GPT web for:

- module-boundary design;
- schema-impact analysis;
- L0 / L1 / L2 responsibility design;
- interface-contract review;
- paper-method skeleton drafting;
- cross-window synthesis;
- long-context engineering task definition.

Codex should only implement code or doc skeletons after the spec is clear.

### 10.2 Data / Labeling Tasks

GPT web should handle:

- frozen-field review;
- label-consistency review;
- brand-lexicon strategy review;
- backfill-scope definition;
- training-set admission design;
- manifest-field design.

Codex should handle:

- backfill-script changes;
- brand-matching implementation;
- report export;
- small-batch smoke tests;
- consistency / manifest / split script execution and delivery.

### 10.3 Training / Experiment Tasks

GPT web should handle:

- experiment-matrix design;
- ablation design;
- loss-design review;
- metric interpretation;
- training smoke-test decomposition.

Codex should handle:

- config implementation;
- train and eval scripts;
- log organization;
- experiment-export tooling;
- dataset-reader or dataloader implementation.

### 10.4 Documentation / Paper Tasks

GPT web should handle:

- novelty framing;
- method wording;
- related-work comparison;
- figure and table narrative structure;
- cross-window summary and relay prompts.

Codex should handle:

- table-generation scripts;
- formatting fixes inside the repo;
- document-structure normalization;
- referenceable repository artifacts.

## 11. When To Use Only GPT Web

Use only GPT web when the task is still purely about:

- requirement clarification;
- architectural comparison;
- high-level specification drafting;
- paper positioning;
- long-context synthesis;
- risk analysis without local execution.

If repository execution is not needed yet, Codex does not need to be involved.

## 12. When To Use Only Codex

Use only Codex when the task is already narrow, local, and execution-ready, for example:

- a small bug fix with clear scope;
- a focused document edit inside frozen boundaries;
- a narrow script patch with obvious validation;
- a local check that does not require upstream task synthesis.

This shortcut is acceptable only when the scope is genuinely low-risk and low-ambiguity.

## 13. Recommended Prompt Templates

### 13.1 Template For GPT Web

The GPT web prompt should include the active contracts, the relevant context, the explicit goal, the boundaries, and the required structured task output.

### 13.2 Template For Codex

The Codex prompt should include the repo path, governing docs, task scope, forbidden scope, validation expectations, and required delivery format.

### 13.3 Template For GPT Web Review

The review prompt should include Codex's final delivery, the relevant diffs, the validation evidence, and a request for a structured accept / reject / partial review.

## 14. Minimum Collaboration Loop

Every collaboration round should close the loop at least this far:

1. clarify the requirement;
2. freeze the task boundary;
3. execute;
4. review and summarize the result.

Skipping the loop increases drift and false confidence.

## 15. Context-Length Handling Rules

When the active GPT web thread becomes too long or unreliable:

1. summarize the current state first;
2. capture the active boundary, key decisions, and pending risks;
3. move to a fresh window;
4. continue with the summary as the handoff context.

This is mandatory when long-context degradation starts to affect quality.

## 16. Final Discipline

The model may implement, summarize, and self-check.

It may not:

- pretend to be the final approver;
- pretend unverified work is verified;
- override project contracts silently;
- replace explicit human acceptance.

### Original Chinese Source

The original Chinese source text is kept below for human readers and traceability.

# GPT_CODEX_WORKFLOW.md

# Warden 项目中 GPT 网页端与 Codex 的使用步骤与方法

## 1. 文档目的

本文件定义在 Warden 项目中，如何严格、低歧义地使用 GPT 网页端与 Codex 协同工作。

目标不是“让模型自由发挥”，而是：

1. 让 GPT 网页端负责高层设计、审查、长上下文整理、任务单生成、二次审查
2. 让 Codex 负责执行、改代码、跑命令、做交付
3. 让项目经理（你）负责冻结边界、验收结果、合并决策

这不是可选建议，而是默认工作法。

---

## 2. 角色分工

### 2.1 GPT 网页端的默认角色

GPT 网页端默认扮演：

- 总设计师
- 规格审查员
- 长上下文整理器
- 任务单生成器
- 二次审稿人
- 交接总结整理器

GPT 网页端不默认扮演：

- 本地仓库真实执行者
- 测试已经跑过的见证人
- 终端输出的唯一事实来源
- 最终合并决策者

### 2.2 Codex 的默认角色

Codex 默认扮演：

- 执行工程师
- 仓库阅读者
- 文件修改者
- 命令运行者
- 差异交付者
- 初步自检者

Codex 不默认扮演：

- 项目总架构最终拍板者
- 标签语义修改审批者
- 冻结字段改名审批者
- 最终发布批准者

### 2.3 你的默认角色

你默认扮演：

- 项目经理
- 需求拆分者
- 边界冻结者
- 最终验收者
- 文档合并者
- 聊天窗口切换协调者

你不能把“最终判断责任”外包给模型。

---

## 3. 绝对规则

以下规则必须遵守：

1. 不允许直接把模糊需求扔给 Codex 开工
2. 不允许让 GPT 网页端假装已经跑过本地命令
3. 不允许让 Codex 自作主张重构整个模块
4. 不允许跳过 `AGENTS.md`
5. 不允许跳过任务单 `TASK_TEMPLATE.md`
6. 不允许跳过交接单 `HANDOFF_TEMPLATE.md`
7. 不允许在未明确批准时修改冻结字段、冻结文件名、冻结枚举
8. 不允许把弱标签当成人工金标
9. 不允许把“模型觉得可以”当成通过验收
10. 不允许让两个窗口同时修改同一组公共接口而不先冻结契约
11. 不允许把 GPT 网页端输出直接当作“已经验证过的工程事实”
12. 当网页端聊天上下文过长、开始卡顿或出现幻觉风险时，必须先让 GPT 网页端总结当前进度，再切换到新窗口继续
13. 当任务需要回到 GPT 网页端做需求整理、二审或长上下文切窗时，Codex 必须主动提醒你返回 GPT 网页端
14. 当任务单、handoff、规范文档等活跃工件来自仓库外路径（如 `Downloads` / `Desktop`）且后续需要继续协作时，Codex 必须先在仓库内落一份并明确返回仓库内路径，不能默认用户会接受仓库外路径

---

## 4. 标准工作流总览

标准流程固定为四段：

1. 需求整理
2. 任务生成
3. 执行与交付
4. 审查与验收

顺序不能乱。

---

## 5. 第一步：需求整理（先用 GPT 网页端，不先用 Codex）

### 5.1 何时必须先用 GPT 网页端

以下情况必须先经过 GPT 网页端：

- 需求跨多个模块
- 需求涉及 schema、label、目录结构、CLI、输出格式
- 需求上下文很长
- 需求涉及多份历史 handoff
- 需求本身有歧义
- 需求可能影响 `PROJECT.md / MODULE_*.md`
- 需求需要结合多个聊天窗口历史内容
- 需求需要先整理成低歧义工程任务

### 5.2 给 GPT 网页端的输入

必须提供：

- `AGENTS.md`
- `PROJECT.md`
- 对应模块文档
- 最近相关 `HANDOFF.md`
- 本次目标描述
- 如有必要，附上仓库目录或相关脚本内容
- 如上下文来自旧窗口，附上旧窗口总结

若缺少任何关键输入，要在提示词里明确说明“以下内容缺失”。

### 5.3 GPT 网页端的输出要求

GPT 网页端输出必须是结构化任务结论，而不是空泛建议。

推荐输出固定为：

- goal
- scope_in
- scope_out
- constraints
- files_to_touch
- acceptance
- risks
- doc_updates_needed

### 5.4 GPT 网页端阶段禁止事项

GPT 网页端阶段禁止：

- 假装已经运行代码
- 假装已经读过本地仓库全部文件
- 直接输出未经边界控制的大重构方案
- 改写冻结字段名
- 用“可以考虑”堆满整页废话
- 把未确认的仓库状态说成事实

---

## 6. 第二步：生成任务单

### 6.1 谁来生成任务单

默认由 GPT 网页端先产出结构化任务内容，
然后由你整理进 `TASK_TEMPLATE.md`。

### 6.2 任务单必须写死的内容

任务单里必须明确：

- 背景
- 目标
- 允许修改范围
- 禁止修改范围
- 输入文件
- 输出要求
- 硬约束
- 接口 / schema 约束
- 验收条件
- 最小验证要求

### 6.3 任务单禁止模糊措辞

避免以下垃圾表述：

- “适当优化”
- “必要时重构”
- “如有需要可调整结构”
- “尽量保持兼容”
- “酌情修改”

必须替换成硬表述，例如：

- “不得修改 top-level JSON key”
- “不得新增第三方依赖”
- “不得改动训练模块”
- “仅允许修改 scripts/labeling 下文件”
- “必须保持旧 CLI 命令可运行”

---

## 7. 第三步：交给 Codex 执行

### 7.1 Codex 的输入

交给 Codex 的内容最少包含：

- `AGENTS.md`
- `PROJECT.md`
- 对应模块文档
- 填好的 `TASK_TEMPLATE.md`

若任务涉及历史改动，再附：

- 最近 handoff
- 相关 diff 摘要
- 相关 bug / 报错

### 7.2 给 Codex 的固定执行指令

你给 Codex 的执行指令应固定成这种结构：

1. 先读相关文件，不要先改
2. 明确列出将修改哪些文件
3. 只在 scope_in 范围内修改
4. 禁止触碰 scope_out
5. 先做最小修改
6. 运行最小必要验证
7. 输出 handoff

### 7.3 Codex 阶段必须要求的输出

Codex 最终必须交付：

- Summary
- Files Changed
- Key Logic Changes
- Validation Performed
- Compatibility Impact
- Risks / Caveats
- Recommended Next Step

若任务非 trivial，还必须按 `HANDOFF_TEMPLATE.md` 输出交接单。

### 7.4 Codex 阶段禁止事项

Codex 阶段禁止：

- 顺手大重构
- 改名成自己喜欢的字段
- 把 scope_out 也一起修了
- 没跑验证却说“应该没问题”
- 没写兼容性影响
- 把文档更新需求藏起来不说

---

## 8. 第四步：审查与验收（再回 GPT 网页端）

### 8.1 为什么要再回 GPT 网页端

Codex 负责执行，不负责最终拍板。

GPT 网页端在这一步的职责是：

- 看交付内容是否满足任务单
- 看是否触碰了禁止范围
- 看是否破坏了接口 / schema
- 看文档债务有没有漏报
- 看下一步建议是否合理
- 看是否需要切换到新聊天窗口继续

### 8.2 交给 GPT 网页端的材料

必须提供：

- Codex 的最终输出
- 关键 diff 摘要
- 验证结果
- handoff 内容
- 若涉及文档修改，则附更新后的文档片段

### 8.3 GPT 网页端的审查输出格式

建议 GPT 网页端固定输出：

- accept: yes / no / partial
- requirement_coverage
- interface_break_risk
- missing_validation
- missing_doc_updates
- notable_risks
- recommended_next_task

### 8.4 GPT 网页端审查阶段禁止事项

禁止：

- 因为“思路看起来不错”就默认通过
- 把没运行的验证当作已通过
- 帮你替代最终审批
- 把接口破坏说成“问题不大”
- 把上下文里没确认的仓库状态写成确定事实

---

## 9. 最终验收由谁做

最终验收只能由你做。

你的验收检查顺序固定如下：

1. 目标是否完成
2. 是否越界修改
3. 是否触碰冻结字段 / 冻结输出
4. 是否真的做了验证
5. 是否写清兼容性影响
6. 是否需要同步更新文档
7. 下一步是否明确

模型不能代替你做最后批准。

---

## 10. 四类任务的推荐分工

### 10.1 架构 / 规格类任务

优先给 GPT 网页端：

- 模块边界设计
- schema 影响分析
- L0/L1/L2 责任分拆
- 接口契约审查
- 论文方法部分骨架
- 多窗口内容汇总
- 长上下文工程任务整理

Codex 只在规格明确后执行骨架代码落地。

### 10.2 数据 / 标注类任务

GPT 网页端负责：

- 字段冻结审查
- 风险标签体系一致性检查
- 品牌词典策略审查
- backfill 范围说明
- 训练集纳入标准整理
- manifest 字段方案整理

Codex 负责：

- 补标脚本修改
- 品牌匹配脚本实现
- 报告导出
- 小批量 smoke test
- consistency / manifest / split 脚本执行实现

### 10.3 训练 / 实验类任务

GPT 网页端负责：

- 实验矩阵设计
- ablation 设计
- loss 设计评审
- 指标解释
- 训练 smoke test 的任务拆解

Codex 负责：

- config 落地
- train/eval 脚本
- 日志整理
- 实验结果导出工具
- dataset reader / dataloader 实现

### 10.4 文档 / 论文类任务

GPT 网页端负责：

- 创新点归纳
- 方法表述
- related work 对照
- 图表叙事结构
- 聊天窗口总结与接力提示词

Codex 负责：

- 表格整理脚本
- 结果统计脚本
- 图表生成脚本
- 复现实验命令归档

---

## 11. 什么时候只用 GPT 网页端，不用 Codex

以下情况优先只用 GPT 网页端：

- 需求还没收敛
- 只是要做方案比较
- 只是要审文档
- 只是要看 handoff 是否合理
- 只是要生成任务单
- 只是要看接口冲突风险
- 只是要整合多个聊天窗口内容
- 只是要总结当前进度，准备换窗口

这一步别急着让 Codex 动手，不然像没图纸就开钻，机械美感很差。

---

## 12. 什么时候只用 Codex，不用 GPT 网页端

以下情况可直接用 Codex，但仍需带上任务单：

- 很小的局部 bug fix
- 明确的路径修正
- 已冻结设计下的小范围代码实现
- 文档明确、接口明确、范围明确的单点修改

前提是：任务真的小，不是假装小。

---

## 13. 推荐提示词模板

### 13.1 给 GPT 网页端的模板

用途：生成任务单 / 审规格 / 长上下文整理

```text
你现在是 Warden 项目的规格审查员。
请严格依据以下文件工作：
1. AGENTS.md
2. PROJECT.md
3. 对应模块文档
4. 最近相关 handoff
5. 如有必要，补充旧聊天窗口总结

任务目标：
[写目标]

请输出结构化结果，不要空泛建议。
输出字段固定为：
goal
scope_in
scope_out
constraints
files_to_touch
acceptance
risks
doc_updates_needed

严格要求：
- 不允许建议修改冻结字段名
- 不允许建议大范围重构，除非我明确要求
- 必须优先保持向后兼容
- 若发现信息不足，要明确指出缺失项
- 不要假装已经运行仓库代码
```

### 13.2 给 Codex 的模板

用途：执行实现

```text
你现在是 Warden 项目的执行工程师。
先阅读 AGENTS.md、PROJECT.md、模块文档与以下任务单，再执行。

执行要求：
1. 先列出你将修改的文件
2. 只能修改 scope_in
3. 不得触碰 scope_out
4. 不得修改冻结字段、冻结文件名、冻结枚举
5. 优先最小修改
6. 完成后运行最小必要验证
7. 最后按固定格式输出：
   - Summary
   - Files Changed
   - Key Logic Changes
   - Validation Performed
   - Compatibility Impact
   - Risks / Caveats
   - Recommended Next Step

若任务非 trivial，还必须补一份 HANDOFF_TEMPLATE.md 格式的交接单。
```

### 13.3 给 GPT 网页端的审查模板

用途：二审

```text
请作为 Warden 项目的二审审查员，审查以下 Codex 交付结果。
依据：
1. AGENTS.md
2. PROJECT.md
3. 对应模块文档
4. 原任务单
5. Codex 最终输出
6. handoff
7. 验证结果

请固定输出：
accept
requirement_coverage
interface_break_risk
missing_validation
missing_doc_updates
notable_risks
recommended_next_task

严格要求：
- 不要把未运行验证当成已通过
- 不要因为思路合理就默认接受
- 若发现越界修改，要直接指出
- 若当前聊天窗口上下文过长，先总结当前进度，再建议切换窗口
```

---

## 14. 每轮协作的最小闭环

每一轮都应满足这个闭环：

1. GPT 网页端整理任务
2. 你冻结任务单
3. Codex 执行
4. Codex 提交 handoff
5. GPT 网页端二审
6. 你最终验收

少一步都可能埋坑。

---

## 15. 上下文过长时的处理规则

当 GPT 网页端聊天窗口出现以下任一情况时，必须考虑切换新窗口：

- 上下文过长
- 上下文估计已接近 90%
- 响应明显变慢
- 重复内容增多
- 事实错误变多
- 开始混淆旧任务和新任务

处理顺序固定如下：

1. 先让 GPT 网页端总结当前 Warden 进度
2. 总结内容必须包含：
   - 当前任务状态
   - 项目定位
   - 已完成内容
   - 当前进行到的位置
   - 下一步最合理任务
   - 当前冻结约束
   - 需要转接到新窗口的文件清单
3. 生成可直接复制到新聊天窗口的交接文本
4. 提醒用户切换到新窗口继续

禁止在高风险长上下文状态下继续硬撑。

---

## 16. 最终纪律

在 Warden 项目里：

- GPT 网页端负责想清楚、整理清楚、审查清楚
- Codex 负责做出来、跑出来、交付清楚
- 你负责拍板

不要混岗。
一混岗，文档、代码、责任边界就会一起煮成一锅浑汤。

