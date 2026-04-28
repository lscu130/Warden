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
- Claude Code：负责低风险、低难度但消耗执行额度的具体操作；也可在任务单明确时执行中等难度局部任务。
- Codex：负责高难度或高风险执行；对 Claude Code 完成的低难度任务做审查，对中等难度任务做强制审查并在必要时接管。
- 人类负责人：负责冻结边界、做最终接受和跨窗口延续。
- 若交付的是 Markdown 文档，默认按“中文摘要在前、英文全文在后、英文权威”执行。

## 3. 阅读重点

优先看英文版的：

- `Absolute Rules`
- `Standard Workflow Overview`
- `Step Two: Generate The Task Document`
- `Step Three: Classify The Task And Route Execution`
- `Task Difficulty Classification And Routing`
- `When To Use GPT Web, Claude Code, And Codex By Difficulty`

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat the English section below as the authoritative version. The Chinese section is for human readers, collaboration, and quick orientation.

# GPT_CODEX_WORKFLOW.md

This workflow document defines the collaboration contract between GPT web chat, Codex, and the human project owner inside Warden.

The goal is not to let models improvise freely. The goal is:

1. GPT web handles higher-level design, long-context synthesis, task drafting, and secondary review.
2. Claude Code handles low-risk, low-difficulty, execution-heavy tasks that would otherwise consume unnecessary Codex quota, and may implement medium-difficulty local tasks when the task document is explicit.
3. Codex handles high-difficulty or high-risk repository execution, reviews low-difficulty Claude Code outputs, and performs mandatory review for medium-difficulty Claude Code outputs before acceptance.
4. The human owner freezes boundaries, decides acceptance, and makes merge or release decisions.

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

### 2.2 Claude Code Default Role

Claude Code is the default executor for low-risk, low-difficulty, execution-heavy work when the task boundary is already explicit. Claude Code may also execute medium-difficulty local tasks only when the task document freezes scope, constraints, compatibility requirements, and validation commands.

Claude Code is the default for:

- repository search and document lookup;
- focused Markdown or documentation edits inside frozen boundaries;
- mechanical formatting, heading, table-of-contents, path, link, and typo cleanup;
- simple local code edits with obvious intent and low interface risk;
- adding or updating comments, docstrings, small examples, or help text;
- read-only inventory work such as locating files, listing references, or collecting candidate paths;
- simple validation commands that have been explicitly requested in the task;
- medium-difficulty local implementation tasks when the task document is explicit and Codex review is mandatory.

Claude Code is not the default for:

- architecture or specification decisions;
- schema, label, taxonomy, threat-definition, or frozen-enumeration changes;
- high-risk training, inference, capture, security, or dataset-admission logic;
- broad refactors;
- dependency changes;
- debugging failures with unclear root cause;
- final acceptance.

### 2.3 Codex Default Role

Codex is the default executor for high-difficulty or high-risk repository work.

Codex is the default for:

- complex implementation;
- cross-module code changes;
- interface-sensitive edits;
- validation design for non-trivial changes;
- debugging unclear failures;
- integration-sensitive repository work;
- reviewing Claude Code outputs for low-difficulty high-quota tasks;
- mandatory review of medium-difficulty Claude Code outputs;
- taking over medium-difficulty tasks when Claude Code output is incomplete, unsafe, incompatible, or out of scope.

For low-difficulty high-quota tasks, Codex should act as a reviewer by default. For medium-difficulty tasks implemented by Claude Code, Codex review is mandatory. Codex should inspect the task boundary, Claude Code's diff, validation evidence, compatibility impact, and handoff. Codex should not redo the concrete operation unless the review finds a real defect, the validation fails, Claude Code is blocked, the task expands beyond the frozen boundary, or the human owner explicitly escalates the task.

Codex is not the default:

- final architecture approver;
- semantic approver for label redesign;
- approver for frozen-field renaming;
- final release authority;
- executor for low-risk mechanical work that Claude Code can perform under a fixed task.

### 2.4 Human Default Role

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
17. Low-difficulty high-quota tasks must be routed to Claude Code first, with Codex used as reviewer rather than executor.
18. Codex must not redo Claude Code's low-risk mechanical work unless there is a concrete defect, a validation failure, a boundary violation, a blocked execution state, or explicit escalation by the human owner.
19. Medium-difficulty tasks may be implemented by Claude Code only when the task document explicitly defines `scope_in`, `scope_out`, frozen constraints, compatibility requirements, minimum validation, and expected outputs.
20. Medium-difficulty Claude Code output must receive Codex review before GPT web secondary review or human acceptance.
21. If a task touches threat-definition semantics, labels, frozen enums, schema, manifest conventions, dataset admission, training, inference, capture, evaluation correctness, dependencies, or cross-module interfaces, route it as high-difficulty by default.

## 4. Standard Workflow Overview

The standard sequence is fixed:

1. Requirement clarification.
2. Task generation.
3. Execution routing, execution, and delivery.
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

## 7. Step Three: Classify The Task And Route Execution

After the task boundary is frozen, classify the task before any repository edit happens. The routing decision is part of the task contract.

### 7.1 Task Difficulty Classification And Routing

Use four routing classes:

| Class | Definition | Primary Executor | Required Reviewer | GPT Web First? |
|---|---|---|---|---|
| Low-difficulty high-quota | Mechanical, local, low-risk work that mainly consumes execution quota | Claude Code | Codex optional or lightweight review unless the task asks for formal review | Usually no |
| Medium-difficulty | Local and clearly scoped, but incorrect changes may affect compatibility, validation behavior, data conventions, or downstream workflow | Claude Code | Codex mandatory review | Usually yes when task boundaries or constraints need freezing |
| High-difficulty / high-risk | Architecture-sensitive, semantic, schema-sensitive, training-sensitive, security-sensitive, cross-module, or hard-to-debug work | Codex | GPT web secondary review + human final acceptance | Yes |
| Exploratory / undefined | The goal, scope, design, or acceptance conditions are not settled | GPT web | Human owner | Yes; no repository execution yet |

When uncertain, route upward to the safer class. Do not downgrade a task merely because the code diff may be small.

### 7.2 Low-Difficulty High-Quota Tasks

A task is low-difficulty high-quota when all of the following are true:

- the goal is explicit;
- the allowed files or directories are explicit;
- the forbidden scope is explicit;
- the operation is mostly mechanical;
- validation is simple or read-only;
- the expected diff shape is obvious;
- no architecture, schema, label, taxonomy, training behavior, inference behavior, capture behavior, evaluation behavior, or public output contract is being redesigned.

Typical examples:

- modifying Markdown documents under a fixed scope;
- locating documents, paths, references, TODOs, headings, examples, or stale links;
- normalizing headings, tables of contents, links, repository paths, filenames in text, bilingual structure, or formatting;
- fixing typos, wording consistency, comment wording, docstrings, small examples, or CLI help text;
- making mechanical code edits such as a known import path, string literal, comment block, or narrow config reference update;
- running read-only checks such as `rg`, file inventory, path existence checks, or simple document consistency checks;
- applying a clearly specified small patch where the expected diff shape is obvious.

Routing rule: Claude Code executes first. Codex reviews only when formal review is requested, when the task is part of a larger workflow, or when the output will be used as a base for later engineering work.

### 7.3 Medium-Difficulty Tasks

A task is medium-difficulty when it has clear local scope and limited architectural impact, but an incorrect change may still break compatibility, validation behavior, data conventions, reports, CLI behavior, or downstream workflow.

A task may be classified as medium-difficulty only when all of the following are true:

- `scope_in` and `scope_out` are explicit;
- frozen fields, filenames, labels, enums, and schemas are not being changed;
- the task does not redesign threat semantics, taxonomy, dataset admission, training, inference, capture, or evaluation logic;
- the implementation is local enough for Claude Code to edit safely;
- the minimum validation command or read-only check is known;
- the expected compatibility impact can be stated before execution.

Typical examples:

- adding a warning-only check to an existing consistency checker without changing error semantics;
- adding a small optional CLI flag while preserving old CLI behavior;
- adding dry-run output to an existing script without changing default behavior;
- appending fields to a report while preserving existing top-level keys and old columns;
- fixing Windows / WSL path handling inside a narrow utility;
- adding small unit tests or fixtures for already-defined behavior;
- synchronizing several documents to an already-frozen definition without redesigning that definition.

Routing rule: Claude Code may implement the patch, but Codex review is mandatory before GPT web secondary review or human acceptance.

Codex review for medium-difficulty work must check:

- whether the task remained inside `scope_in`;
- whether `scope_out` was untouched;
- whether frozen fields, filenames, enums, labels, schemas, and output contracts were preserved;
- whether the diff is minimal;
- whether validation evidence is real and sufficient;
- whether old CLI behavior, old report consumers, and downstream workflows remain compatible;
- whether the task should be escalated to Codex execution or GPT web requirement review.

Codex should take over execution only if Claude Code's result is incomplete, unsafe, incompatible, out of scope, blocked, or failed validation.

### 7.4 High-Difficulty Or High-Risk Tasks

Route the task directly to Codex when any of the following is true:

- the task changes threat-definition semantics, label taxonomy, or frozen enums;
- the task changes schema, manifest conventions, dataset split rules, or training-set admission rules;
- the task affects model training, inference, fusion, scoring, metrics, or evaluation correctness;
- the task affects capture, browser automation, network evidence, HTML parsing, or security-sensitive parsing;
- the task changes public CLI behavior, output schema, downstream compatibility, or cross-module interfaces;
- the task requires dependency changes, broad refactors, migration logic, or repository-wide cleanup;
- the task requires debugging a failing command with unclear root cause;
- the implementation spans multiple modules or shared interfaces;
- a wrong patch could silently corrupt data, labels, metrics, or experiment results.

Routing rule: GPT web should clarify and freeze the task first when the scope or semantics are not already settled. Codex executes after the task document is explicit. GPT web then performs secondary review, and the human owner performs final acceptance.

### 7.5 Exploratory Or Undefined Tasks

Use GPT web only when the task is still exploratory, for example:

- the user is comparing design options;
- the acceptance criteria are not known;
- the scope boundary is not frozen;
- the work depends on long prior context;
- semantic definitions or architecture need to be decided;
- the task may affect multiple modules, but the target change is not yet specified.

Routing rule: do not execute repository changes yet. GPT web should produce a structured task conclusion first.

### 7.6 Claude Code Inputs

Claude Code should receive at least:

- `AGENTS.md`;
- `PROJECT.md`;
- relevant module docs;
- a completed task document based on `TASK_TEMPLATE.md`;
- explicit `scope_in` and `scope_out`;
- explicit frozen constraints and compatibility constraints;
- the minimum validation command or read-only check expected.

When the task depends on prior history, also provide:

- the latest handoff;
- relevant file paths or search terms;
- bugs or error reports if applicable.

### 7.7 Fixed Execution Instructions For Claude Code

The execution instruction given to Claude Code should follow this shape:

1. Read relevant files before editing.
2. State which files will be changed.
3. Edit only inside `scope_in`.
4. Do not touch `scope_out`.
5. Prefer the smallest valid patch.
6. Do not redesign architecture, schemas, labels, taxonomy, threat definitions, or frozen enums.
7. Preserve old CLI behavior, public outputs, and downstream compatibility unless the task explicitly says otherwise.
8. Run the explicitly requested minimum validation.
9. Produce a concise handoff.
10. If the deliverable is Markdown, write it as bilingual Chinese-summary-first / full-English-second, with English authoritative.

### 7.8 Codex Direct Execution Rule

Codex should execute directly only when at least one high-difficulty condition applies, or when the human owner explicitly asks Codex to execute.

For medium-difficulty tasks, Codex should not execute first by default. It should review Claude Code's implementation unless the task has already escalated.

### 7.9 Codex Review Mode For Claude Code Work

When Claude Code performs low- or medium-difficulty work, Codex review should check:

- whether Claude Code stayed inside `scope_in`;
- whether `scope_out` was untouched;
- whether frozen fields, filenames, enumerations, labels, schemas, and public outputs were preserved;
- whether the change is minimal;
- whether validation evidence matches the task;
- whether compatibility impact is stated;
- whether the handoff is complete enough for GPT web secondary review;
- whether the task should be escalated.

Codex may ask Claude Code for a targeted fix. Codex should take over execution only when review finds a real defect, validation fails, Claude Code is blocked, the task expanded beyond its class, or the human owner explicitly escalates.

### 7.10 What Codex Must Not Do

Codex must not:

- perform opportunistic large refactors;
- rename fields to match personal preference;
- silently fix extra items outside scope;
- claim "should be fine" without validation;
- omit compatibility impact;
- hide documentation-update requirements;
- consume execution quota on low-risk mechanical work that Claude Code can perform under a fixed task;
- redo Claude Code work merely because it can.

## 8. Step Four: Review And Acceptance

After Claude Code or Codex finishes execution, the result should return to GPT web for secondary review and then to the human owner for final acceptance.

### 8.1 Why GPT Web Is Used Again

Claude Code or Codex may execute the work, but neither makes the final approval decision.

GPT web is useful here for:

- checking whether the task requirements were met;
- checking whether forbidden scope was touched;
- checking interface or schema risk;
- checking whether documentation debt was missed;
- checking whether the proposed next step is coherent;
- deciding whether the work should continue in a fresh chat window.

### 8.2 Materials To Provide For Review

The review step should receive:

- Claude Code's or Codex's final output;
- Codex review notes when Claude Code executed the work;
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

After the spec is clear, Claude Code may perform low-risk skeleton or documentation edits. Codex should execute only higher-risk implementation and should review Claude Code outputs when Claude Code was used.

### 10.2 Data / Labeling Tasks

GPT web should handle:

- frozen-field review;
- label-consistency review;
- brand-lexicon strategy review;
- backfill-scope definition;
- training-set admission design;
- manifest-field design.

Claude Code may handle low-risk mechanical data-task support such as locating files, updating documentation, formatting reports, or running explicitly requested read-only checks.

Codex should handle or review:

- backfill-script changes;
- brand-matching implementation;
- report export;
- small-batch smoke tests;
- consistency / manifest / split script execution and delivery.

For low-difficulty high-quota parts of these tasks, Claude Code executes first and Codex reviews.

### 10.3 Training / Experiment Tasks

GPT web should handle:

- experiment-matrix design;
- ablation design;
- loss-design review;
- metric interpretation;
- training smoke-test decomposition.

Claude Code may handle mechanical experiment-support tasks such as locating configs, formatting logs, updating docs, or adding comments under a fixed scope.

Codex should handle or review:

- config implementation;
- train and eval scripts;
- log organization;
- experiment-export tooling;
- dataset-reader or dataloader implementation.

Codex executes directly when the change affects training behavior or evaluation correctness.

### 10.4 Documentation / Paper Tasks

GPT web should handle:

- novelty framing;
- method wording;
- related-work comparison;
- figure and table narrative structure;
- cross-window summary and relay prompts.

Claude Code should handle low-risk documentation execution such as formatting fixes, document-structure normalization, heading cleanup, bilingual skeleton updates, repository path checks, and simple referenceable artifacts.

Codex should review those outputs. Codex should execute directly only for table-generation scripts, result-statistics scripts, figure-generation scripts, or documentation tasks that depend on non-trivial repository logic.

## 11. When To Use Only GPT Web

Use only GPT web when the task is still purely about:

- requirement clarification;
- architectural comparison;
- high-level specification drafting;
- paper positioning;
- long-context synthesis;
- risk analysis without local execution.

If repository execution is not needed yet, Codex does not need to be involved.

## 12. When To Use GPT Web, Claude Code, And Codex By Difficulty

This section is the compact routing reference. Section 7 is the authoritative operational rule.

### 12.1 Use Only GPT Web

Use only GPT web when the task is still exploratory or specification-level:

- requirement clarification;
- architectural comparison;
- high-level specification drafting;
- paper positioning;
- long-context synthesis;
- risk analysis without local execution;
- task decomposition before repository work.

Output should be a structured task conclusion, not repository edits.

### 12.2 Use Claude Code First, Codex Optional Or Lightweight Review

Use Claude Code first for low-difficulty high-quota work:

- fixed-scope Markdown edits;
- document lookup and repository search;
- heading, link, path, formatting, bilingual-structure, or typo cleanup;
- simple comments, docstrings, examples, or CLI help text;
- read-only checks such as `rg`, file inventory, or path existence checks;
- mechanical code edits with obvious expected diff shape.

Codex should not spend execution quota on these unless formal review is requested or defects appear.

### 12.3 Use Claude Code First, Codex Mandatory Review

Use this route for medium-difficulty tasks:

- local script enhancements with known validation;
- warning-only checker additions;
- optional CLI flags that preserve old behavior;
- report additions that preserve old keys and columns;
- small compatibility fixes such as Windows / WSL path handling;
- tests or fixtures for already-defined behavior;
- document synchronization to an already-frozen definition.

Requirements for this route:

1. The task document must define `scope_in`, `scope_out`, frozen constraints, compatibility constraints, minimum validation, and expected outputs.
2. Claude Code may implement.
3. Codex must review the final diff, validation evidence, and compatibility impact.
4. Codex does not reimplement unless there is a defect, failed validation, boundary violation, incompatibility, blocked execution, or explicit escalation.

### 12.4 Use Codex Directly

Use Codex directly for high-difficulty or high-risk work:

- threat-definition semantics;
- label taxonomy or frozen enum changes;
- schema, manifest, dataset split, or training-set admission changes;
- training, inference, fusion, scoring, metrics, or evaluation logic;
- capture, browser automation, network evidence, or security-sensitive parsing;
- public CLI behavior, output schema, or downstream compatibility changes;
- dependency changes, broad refactors, migration logic, or repository-wide cleanup;
- unclear failing tests or unclear runtime failures;
- cross-module interfaces;
- changes that may silently corrupt data, labels, metrics, or experiment results.

GPT web should first freeze the requirement when semantics, architecture, or cross-module contracts are involved.

### 12.5 Escalation Rule

A task must be escalated upward when it exceeds its original class:

- Low to medium: the task stops being mechanical and starts changing local behavior.
- Medium to high: the task touches frozen fields, schemas, labels, threat semantics, training, inference, capture, evaluation correctness, dependencies, or cross-module interfaces.
- Any class to GPT web: the requirement becomes ambiguous or acceptance criteria are no longer clear.

The executor should stop, report the reason, and wait for a new frozen task boundary.

## 13. Recommended Prompt Templates

### 13.1 Template For GPT Web

The GPT web prompt should include the active contracts, the relevant context, the explicit goal, the boundaries, the requested task class if known, and the required structured task output.

### 13.2 Template For Claude Code

The Claude Code prompt should include the repo path, governing docs, task class, task scope, forbidden scope, frozen constraints, compatibility expectations, validation expectations, and required delivery format. It should explicitly state whether the task is low-difficulty or medium-difficulty. For medium-difficulty tasks, it must state that Codex review is mandatory.

### 13.3 Template For Codex

The Codex prompt should state whether Codex is executing directly or reviewing Claude Code output. In review-only mode, the prompt should include Claude Code's final delivery, key diffs, validation evidence, compatibility notes, and the original task boundary. For medium-difficulty tasks, Codex must explicitly decide whether the result is acceptable, needs targeted Claude Code repair, or requires Codex takeover.

### 13.4 Template For GPT Web Review

The review prompt should include Claude Code's or Codex's final delivery, Codex's review notes if applicable, the relevant diffs, the validation evidence, the task class, and a request for a structured accept / reject / partial review.

## 14. Minimum Collaboration Loop

Every collaboration round should close the loop at least this far:

1. clarify the requirement;
2. freeze the task boundary;
3. classify the task as exploratory, low, medium, or high difficulty;
4. route execution to GPT web, Claude Code, or Codex;
5. execute only after the boundary is frozen;
6. have Codex review Claude Code output when required, always for medium-difficulty work;
7. review and summarize the result.

Skipping the loop increases drift and false confidence.

## 15. Context-Length Handling Rules

When the active GPT web thread becomes too long or unreliable:

1. summarize the current state first;
2. capture the active boundary, key decisions, and pending risks;
3. move to a fresh window;
4. continue with the summary as the handoff context.

This is mandatory when long-context degradation starts to affect quality.

## 16. Final Discipline

Claude Code may perform low-risk execution and medium-difficulty local execution under mandatory Codex review. Codex may execute high-risk work, review Claude Code output, summarize, and self-check.

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
2. 让 Claude Code 负责低风险、低难度但消耗执行额度的具体操作；在任务单明确时，也可执行中等难度局部任务
3. 让 Codex 负责高难度或高风险执行；对 Claude Code 完成的低难度任务做审查，对中等难度任务做强制审查并在必要时接管
4. 让项目经理（你）负责冻结边界、验收结果、合并决策

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

### 2.2 Claude Code 的默认角色

Claude Code 默认负责低风险、低难度、但会消耗执行额度的具体操作。任务单明确时，也可执行中等难度局部任务，但必须接受 Codex 审查。

Claude Code 默认适合：

- 仓库内查找文档、路径、引用、TODO、标题
- 在冻结边界内修改 Markdown 或说明文档
- 格式、标题、目录、路径、链接、错别字和表述一致性清理
- 明确指定的小型机械性代码改动
- 增补注释、docstring、简单示例、CLI help 文案
- 运行明确要求的只读检查或最小验证命令
- 在任务单明确、Codex 必审的前提下，执行中等难度局部任务

Claude Code 不默认负责：

- 架构或规格决策
- schema、label、taxonomy、威胁定义、冻结枚举修改
- 训练、推理、采集、安全敏感解析、数据集准入等高风险逻辑
- 大范围重构
- 依赖变更
- 原因不清的失败调试
- 最终验收

### 2.3 Codex 的默认角色

Codex 默认负责高难度或高风险仓库工作。

Codex 默认适合：

- 复杂实现
- 跨模块代码修改
- 接口敏感修改
- 非平凡变更的验证设计
- 原因不清的失败调试
- 集成敏感的仓库工作
- 审查 Claude Code 对低难度高额度任务的交付结果
- 强制审查 Claude Code 对中等难度任务的交付结果
- 当中等难度任务出现不完整、不安全、不兼容或越界时接管执行

对于低难度高额度任务，Codex 默认只做审查。对于 Claude Code 执行的中等难度任务，Codex 必须审查。它应检查任务边界、Claude Code diff、验证证据、兼容性影响和 handoff。只有当发现明确缺陷、验证失败、Claude Code 被阻塞、任务超出冻结边界，或项目负责人明确升级任务时，Codex 才接手执行。

Codex 不默认扮演：

- 项目总架构最终拍板者
- 标签语义修改审批者
- 冻结字段改名审批者
- 最终发布批准者
- 可由 Claude Code 在固定任务内完成的低风险机械劳动执行者

### 2.4 你的默认角色

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
15. 低难度高额度任务必须优先交给 Claude Code 执行，Codex 默认只做审查
16. Codex 不得仅因为自己能做，就重做 Claude Code 已完成的低风险机械任务；除非有明确缺陷、验证失败、越界修改、Claude Code 被阻塞，或项目负责人明确升级任务
17. 中等难度任务只有在任务单明确写清 `scope_in`、`scope_out`、冻结约束、兼容性要求、最小验证和预期输出时，才允许 Claude Code 执行
18. Claude Code 执行的中等难度任务，必须经过 Codex 审查后，才能进入 GPT 网页端二审或项目负责人验收
19. 只要任务触碰威胁定义语义、标签、冻结枚举、schema、manifest 约定、数据集准入、训练、推理、采集、评估正确性、依赖或跨模块接口，默认按高难度处理

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

## 7. 第三步：任务分级并选择执行者

任务边界冻结后，先分级，再决定由谁执行。执行者选择本身就是任务契约的一部分。

### 7.1 任务难度分级与路由规则

统一分成四类：

| 类型 | 定义 | 默认执行者 | 必要审查者 | 是否必须先用 GPT 网页端 |
|---|---|---|---|---|
| 低难度高额度 | 机械、本地、低风险，主要消耗执行额度 | Claude Code | Codex 可轻审；正式任务可审查 | 通常不用 |
| 中等难度 | 范围局部清楚，但改错可能影响兼容性、验证行为、数据规范或下游流程 | Claude Code | Codex 必审 | 边界或约束需要冻结时建议先用 |
| 高难度 / 高风险 | 涉及架构、语义、schema、训练、安全、跨模块、难调试或公共接口 | Codex | GPT 网页端二审 + 你最终验收 | 必须 |
| 探索型 / 未定型 | 目标、范围、设计或验收条件还没确定 | GPT 网页端 | 你判断 | 必须；先不改仓库 |

拿不准时，向上升级。不要因为 diff 看起来小，就把任务降级。

### 7.2 低难度高额度任务

同时满足以下条件，才算低难度高额度任务：

- 目标明确
- 允许修改的文件或目录明确
- 禁止范围明确
- 操作以机械执行为主
- 验证简单或只读
- 预期 diff 形状很清楚
- 不重新设计架构、schema、label、taxonomy、训练行为、推理行为、采集行为、评估行为或公开输出契约

典型例子：

- 在固定范围内修改 Markdown 文档
- 查找文档、路径、引用、TODO、标题、示例、过期链接
- 规范标题、目录、链接、仓库路径、正文文件名、双语结构或格式
- 修正错别字、表述一致性、注释、docstring、简单示例、CLI help 文案
- 做机械性代码改动，例如已知 import 路径、字符串字面量、注释块、窄范围 config 引用更新
- 运行 `rg`、文件清单、路径存在性检查、简单文档一致性检查等只读检查
- 应用明确指定的小补丁，且预期 diff 形状很清楚

路由规则：Claude Code 先执行。只有正式任务要求审查、该结果会作为后续工程基础、或发现缺陷时，Codex 再审查。

### 7.3 中等难度任务

中等难度任务是指：范围局部、目标明确、架构影响有限，但改错后可能影响兼容性、验证行为、数据规范、报告、CLI 行为或下游流程的任务。

只有同时满足以下条件，才允许归为中等难度：

- `scope_in` 和 `scope_out` 明确
- 不修改冻结字段、冻结文件名、标签、枚举和 schema
- 不重新设计威胁语义、taxonomy、数据集准入、训练、推理、采集或评估逻辑
- 实现范围足够局部，Claude Code 可以安全编辑
- 最小验证命令或只读检查已知
- 执行前能说明预期兼容性影响

典型例子：

- 给已有 consistency checker 增加 warning-only 检查，不改变 error 语义
- 增加一个小的可选 CLI 参数，并保持旧命令行为不变
- 给已有脚本增加 dry-run 输出，但不改变默认行为
- 给 report 追加字段，同时保留旧 top-level key 和旧列
- 在窄范围 utility 中修复 Windows / WSL 路径兼容
- 给已定义行为补小型单元测试或 fixture
- 按已经冻结的定义同步多份文档，不重新设计定义本身

路由规则：Claude Code 可以实现，但 Codex 必须审查后，才能进入 GPT 网页端二审或项目负责人验收。

Codex 对中等难度任务必须检查：

- 是否仍在 `scope_in` 内
- 是否没有触碰 `scope_out`
- 是否保留冻结字段、文件名、枚举、标签、schema 和输出契约
- diff 是否足够小
- 验证证据是否真实且足够
- 旧 CLI 行为、旧报告消费者、下游流程是否仍兼容
- 是否需要升级为 Codex 执行或回 GPT 网页端重整需求

只有当 Claude Code 结果不完整、不安全、不兼容、越界、被阻塞或验证失败时，Codex 才接管执行。

### 7.4 高难度或高风险任务

以下情况直接交给 Codex：

- 修改威胁定义语义、标签 taxonomy 或冻结枚举
- 修改 schema、manifest 约定、数据集切分规则或训练集准入规则
- 影响模型训练、推理、融合、打分、指标或评估正确性
- 影响采集、浏览器自动化、网络证据、HTML 解析或安全敏感解析
- 修改公开 CLI 行为、输出 schema、下游兼容性或跨模块接口
- 依赖变更、大范围重构、迁移逻辑或仓库级清理
- 调试原因不清的失败命令
- 实现横跨多个模块或共享接口
- 错误补丁可能悄悄污染数据、标签、指标或实验结果

路由规则：如果范围或语义还没明确，先回 GPT 网页端冻结任务；任务单明确后由 Codex 执行；之后 GPT 网页端二审，你最终验收。

### 7.5 探索型或未定型任务

以下情况只用 GPT 网页端：

- 正在比较设计方案
- 验收标准未知
- 范围边界没有冻结
- 依赖很长的历史上下文
- 需要先决定语义定义或架构
- 可能影响多个模块，但具体改什么还没确定

路由规则：此时不改仓库。GPT 网页端先输出结构化任务结论。

### 7.6 给 Claude Code 的输入

交给 Claude Code 的内容最少包含：

- `AGENTS.md`
- `PROJECT.md`
- 对应模块文档
- 填好的 `TASK_TEMPLATE.md`
- 明确的 `scope_in` 和 `scope_out`
- 明确的冻结约束和兼容性约束
- 明确要求的最小验证命令或只读检查

若任务涉及历史改动，再附：

- 最近 handoff
- 相关文件路径或搜索关键词
- 相关 bug / 报错

### 7.7 给 Claude Code 的固定执行指令

你给 Claude Code 的执行指令应固定成这种结构：

1. 先读相关文件，不要先改
2. 明确列出将修改哪些文件
3. 只在 scope_in 范围内修改
4. 禁止触碰 scope_out
5. 优先最小修改
6. 不得重设架构、schema、label、taxonomy、威胁定义或冻结枚举
7. 除非任务明确要求，否则必须保留旧 CLI 行为、公开输出和下游兼容性
8. 运行明确要求的最小验证
9. 输出简洁 handoff
10. 如果交付物是 Markdown，必须按中文摘要在前、英文全文在后、英文权威执行

### 7.8 Codex 直接执行规则

只有满足高难度条件，或项目负责人明确要求 Codex 执行时，Codex 才直接执行。

中等难度任务默认不由 Codex 先执行。Codex 默认审查 Claude Code 的实现，除非任务已经升级。

### 7.9 Claude Code 执行后的 Codex 审查模式

Claude Code 完成低难度或中等难度任务后，Codex 审查应检查：

- 是否严格在 `scope_in` 内修改
- 是否没有触碰 `scope_out`
- 是否保留冻结字段、文件名、枚举、标签、schema 和公开输出
- diff 是否足够小
- 验证证据是否符合任务要求
- 是否说明兼容性影响
- handoff 是否足以交给 GPT 网页端二审
- 是否需要升级任务

Codex 可以要求 Claude Code 做定向修复。只有当发现明确缺陷、验证失败、Claude Code 被阻塞、任务超出原等级，或项目负责人明确升级任务时，Codex 才接手执行。

### 7.10 Codex 阶段禁止事项

Codex 禁止：

- 顺手大重构
- 改名成自己喜欢的字段
- 把 scope_out 也一起修了
- 没跑验证却说“应该没问题”
- 没写兼容性影响
- 把文档更新需求藏起来不说
- 在 Claude Code 可完成的低风险机械任务上消耗执行额度
- 仅因为自己能做就重做 Claude Code 的工作

## 8. 第四步：审查与验收（再回 GPT 网页端）

### 8.1 为什么要再回 GPT 网页端

Claude Code 或 Codex 可以负责执行，但都不负责最终拍板。

GPT 网页端在这一步的职责是：

- 看交付内容是否满足任务单
- 看是否触碰了禁止范围
- 看是否破坏了接口 / schema
- 看文档债务有没有漏报
- 看下一步建议是否合理
- 看是否需要切换到新聊天窗口继续

### 8.2 交给 GPT 网页端的材料

必须提供：

- Claude Code 或 Codex 的最终输出
- 如果由 Claude Code 执行，还要附 Codex 审查意见
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

规格明确后，Claude Code 可执行低风险文档或骨架整理；Codex 只执行高风险实现，并审查 Claude Code 的低难度交付。

### 10.2 数据 / 标注类任务

GPT 网页端负责：

- 字段冻结审查
- 风险标签体系一致性检查
- 品牌词典策略审查
- backfill 范围说明
- 训练集纳入标准整理
- manifest 字段方案整理

Claude Code 可负责低风险机械辅助工作，例如查找文件、更新文档、整理报告格式、运行明确指定的只读检查。

Codex 负责或审查：

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

Claude Code 可负责机械性实验辅助任务，例如查找配置、整理日志格式、更新文档或在固定范围内补注释。

Codex 负责或审查：

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

Claude Code 优先负责低风险文档执行，例如格式修复、文档结构规范化、标题清理、双语骨架更新、仓库路径检查和简单可引用工件整理。

Codex 审查这些结果。只有表格生成脚本、结果统计脚本、图表生成脚本，或依赖非平凡仓库逻辑的文档任务，才由 Codex 直接执行。

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

## 12. 按难度使用 GPT 网页端、Claude Code 与 Codex

本节是简明路由参考。第 7 节是正式操作规则。

### 12.1 只用 GPT 网页端

以下情况只用 GPT 网页端：

- 需求澄清
- 架构比较
- 高层规格草拟
- 论文定位
- 长上下文整合
- 不需要本地执行的风险分析
- 仓库执行前的任务拆分

输出应该是结构化任务结论，不是仓库修改。

### 12.2 Claude Code 先执行，Codex 可选轻审

低难度高额度任务优先交给 Claude Code：

- 固定范围 Markdown 修改
- 文档查找和仓库搜索
- 标题、链接、路径、格式、双语结构、错别字清理
- 简单注释、docstring、示例、CLI help 文案
- `rg`、文件清单、路径存在性检查等只读检查
- 预期 diff 形状明显的机械性代码改动

Codex 不应在这些任务上消耗执行额度，除非任务要求正式审查或发现缺陷。

### 12.3 Claude Code 先执行，Codex 强制审查

中等难度任务走这条路线：

- 有明确验证方式的局部脚本增强
- warning-only checker 增补
- 保留旧行为的可选 CLI 参数
- 保留旧 key 和旧列的 report 增补
- Windows / WSL 路径兼容等小型兼容修复
- 对已定义行为补测试或 fixture
- 按已冻结定义同步文档

这条路线的要求：

1. 任务单必须写清 `scope_in`、`scope_out`、冻结约束、兼容性约束、最小验证和预期输出。
2. Claude Code 可以实现。
3. Codex 必须审查最终 diff、验证证据和兼容性影响。
4. 除非出现缺陷、验证失败、越界、不兼容、执行阻塞或明确升级，Codex 不重新实现。

### 12.4 Codex 直接执行

高难度或高风险任务直接给 Codex：

- 威胁定义语义
- 标签 taxonomy 或冻结枚举修改
- schema、manifest、数据集切分、训练集准入修改
- 训练、推理、融合、打分、指标或评估逻辑
- 采集、浏览器自动化、网络证据、安全敏感解析
- 公开 CLI 行为、输出 schema 或下游兼容性变更
- 依赖变更、大范围重构、迁移逻辑或仓库级清理
- 原因不清的测试失败或运行失败
- 跨模块接口
- 可能悄悄污染数据、标签、指标或实验结果的变更

涉及语义、架构或跨模块契约时，必须先由 GPT 网页端冻结需求。

### 12.5 升级规则

任务超过原等级时，必须向上升级：

- 低难度升中等难度：任务不再是机械修改，开始改变局部行为。
- 中等难度升高难度：任务触碰冻结字段、schema、标签、威胁语义、训练、推理、采集、评估正确性、依赖或跨模块接口。
- 任意等级回 GPT 网页端：需求开始变模糊，或验收标准不再清楚。

执行者应停止、说明升级原因，并等待新的冻结任务边界。

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

请先判断任务等级：探索型 / 低难度 / 中等难度 / 高难度。
然后输出结构化结果，不要空泛建议。
输出字段固定为：
goal
scope_in
scope_out
constraints
files_to_touch
acceptance
risks
doc_updates_needed
recommended_executor
required_reviewer

严格要求：
- 不允许建议修改冻结字段名
- 不允许建议大范围重构，除非我明确要求
- 必须优先保持向后兼容
- 若发现信息不足，要明确指出缺失项
- 不要假装已经运行仓库代码
```

### 13.2 给 Claude Code 的模板

用途：低难度高额度任务 / 中等难度局部任务执行

```text
你现在是 Warden 项目的执行助手。
本任务等级为：[低难度 / 中等难度]。
如果是低难度任务，由你先执行，Codex 可审查或轻审。
如果是中等难度任务，由你先执行，但 Codex 必须审查后才能验收。
先阅读 AGENTS.md、PROJECT.md、模块文档与以下任务单，再执行。

执行要求：
1. 先列出你将修改的文件
2. 只能修改 scope_in
3. 不得触碰 scope_out
4. 不得修改冻结字段、冻结文件名、冻结枚举
5. 不得重设架构、schema、label、taxonomy、威胁定义或训练/推理/采集/评估逻辑
6. 保持旧 CLI 行为、公开输出和下游兼容性，除非任务单明确要求改变
7. 优先最小修改
8. 完成后运行明确要求的最小验证或只读检查
9. 最后按固定格式输出：
   - Summary
   - Files Changed
   - Key Logic Changes
   - Validation Performed
   - Compatibility Impact
   - Risks / Caveats
   - Recommended Next Step

若任务非 trivial，还必须补一份 HANDOFF_TEMPLATE.md 格式的交接单。
```

### 13.3 给 Codex 的模板

用途：高风险执行 / 审查 Claude Code 结果

```text
你现在是 Warden 项目的执行工程师或审查员。
请先确认本任务模式：
1. Codex 直接执行高难度任务；或
2. Codex 审查 Claude Code 的低难度 / 中等难度任务结果。

如果本任务由 Claude Code 先执行，你默认只审查，不重做；中等难度任务必须强制审查。
只有发现明确缺陷、验证失败、越界修改、不兼容、Claude Code 被阻塞，或项目负责人明确升级任务时，才接手执行。
先阅读 AGENTS.md、PROJECT.md、模块文档、原任务单、Claude Code 输出与相关 diff，再审查或执行。

审查要求：
1. 检查是否符合 scope_in
2. 检查是否触碰 scope_out
3. 检查是否修改冻结字段、冻结文件名、冻结枚举、schema、label 或公开输出
4. 检查 diff 是否最小
5. 检查验证证据是否真实且足够
6. 检查兼容性影响是否说清楚
7. 明确结论：accept / needs targeted Claude Code fix / Codex takeover required

如需接手执行：
1. 先列出你将修改的文件
2. 只能修改 scope_in
3. 不得触碰 scope_out
4. 优先最小修改
5. 完成后运行最小必要验证
6. 最后按固定格式输出：
   - Summary
   - Files Changed
   - Key Logic Changes
   - Validation Performed
   - Compatibility Impact
   - Risks / Caveats
   - Recommended Next Step

若任务非 trivial，还必须补一份 HANDOFF_TEMPLATE.md 格式的交接单。
```

### 13.4 给 GPT 网页端的审查模板

用途：二审

```text
请作为 Warden 项目的二审审查员，审查以下 Claude Code 或 Codex 交付结果。
依据：
1. AGENTS.md
2. PROJECT.md
3. 对应模块文档
4. 原任务单
5. 任务等级：探索型 / 低难度 / 中等难度 / 高难度
6. Claude Code 或 Codex 最终输出
7. 如由 Claude Code 执行，附 Codex 审查意见
8. handoff
9. 验证结果

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
- 若中等难度任务缺少 Codex 审查，不能建议验收
- 若当前聊天窗口上下文过长，先总结当前进度，再建议切换窗口
```

## 14. 每轮协作的最小闭环

每一轮都应满足这个闭环：

1. GPT 网页端整理任务
2. 你冻结任务单
3. 先判断任务等级：探索型 / 低难度 / 中等难度 / 高难度
4. 按等级路由给 GPT 网页端、Claude Code 或 Codex
5. 边界冻结后再执行
6. 如果由 Claude Code 执行，按规则让 Codex 审查；中等难度必须审查
7. GPT 网页端二审
8. 你最终验收

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
- Claude Code 负责低风险机械任务做出来、跑出来、交付清楚；也可在 Codex 必审前提下执行中等难度局部任务
- Codex 负责高风险执行，审查 Claude Code 的低难度任务，并强制审查 Claude Code 的中等难度任务
- 你负责拍板

不要混岗。
一混岗，文档、代码、责任边界就会一起煮成一锅浑汤。

