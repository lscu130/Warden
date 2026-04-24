# Warden Window Handoff Summary For GPT Web

## 中文摘要

> 用途：这份文档给新的 GPT 网页端窗口继续使用。它只总结当前仓库已经对齐过的 L0 定义、边界和下一步延续点。  
> 权威说明：若本文件与 repo 内 `AGENTS.md`、`PROJECT.md`、`docs/modules/MODULE_INFER.md`、`docs/modules/L0_DESIGN_V1.md` 或 active task/handoff 冲突，以 repo 内更高优先级文档为准。

### 1. 当前 L0 正式口径

- Warden 的官方顶层阶段仍然是 `L0 / L1 / L2`。
- 当前 L0 是低成本、快速、可解释的 screening / routing 层。
- 当前 L0 的专注范围已经收紧为：`gambling / adult / gate`。
- 其他非特化样本默认继续进入 L1。

### 2. 当前 L0 默认输入

L0 默认热路径只使用低成本输入：

- URL 及其轻量结构信号
- visible text / title
- form summary
- network summary
- raw visible-text observability
- 已存在的 compact diff / evasion hints

### 3. 当前 L0 默认禁止事项

L0 默认不做以下内容：

- 不默认吃完整 HTML
- 不默认做 brand extraction
- 不默认吃 screenshot / OCR
- 不走 heavy model inference
- 不做 click-through / interaction recovery
- 不做 gate solving

`html_features` 和 `brand_signals` 仍可作为兼容字段或外部已提供 side inputs 被保留，但它们不代表 L0 默认热路径要主动计算这些重输入。

### 4. 已经失效或不应继续沿用的旧口径

- 不要再把 `fake verification` 当成当前 L0 的独立 active specialized family。
- 不要把 `L0-fast / L1-text / L1-mm` 当成当前对外的官方顶层 stage 命名。
- 不要默认认为 L0 已冻结成“广义可直接完成最终 resolution 的层”。
- 不要默认把 full HTML、brand、screenshot/OCR、heavy recovery 重新塞回 L0。

### 5. 当前实现状态

- 当前 active L0 实现在 `src/warden/module/l0.py`。
- 旧脚本兼容入口仍保留在 `scripts/labeling/Warden_auto_label_utils_brandlex.py`。
- `specialized_fast_resolution_candidate` 目前仍属于弱信号 / routing 信号语义。
- 如果未来要把某些 obvious specialized family 真正冻结成 L0 直接完成的 resolution contract，需要单独开 task 和文档更新，不能默认为当前已经生效。

### 6. 给下个 GPT 网页端窗口的延续边界

如果下个窗口继续讨论 L0，请默认以下边界已经冻结：

- L0 继续只做 `gambling / adult / gate` 的低成本特化判断与路由
- 非特化样本继续上推 L1
- L0 不重新打开 full HTML / default brand extraction / screenshot-OCR / heavy interaction 路径
- 后续 L0 工作优先是样本驱动的小范围 tuning，而不是职责改写

## English Version

> AI note: The English section is authoritative for exact contract wording and continuation boundaries.

# Warden Window Handoff Summary For GPT Web

## 1. Purpose

This document is for continuing Warden work in a fresh GPT web window.

It only summarizes the current repo-aligned L0 contract, its boundaries, and the safest continuation assumptions. If this handoff conflicts with `AGENTS.md`, `PROJECT.md`, `docs/modules/MODULE_INFER.md`, `docs/modules/L0_DESIGN_V1.md`, or an active task/handoff, the repo-local higher-priority docs win.

## 2. Current Official L0 State

- Warden's official top-level stages remain `L0 / L1 / L2`.
- The current L0 is a fast, low-cost, explainable screening and routing layer.
- The current L0 specialization scope has been narrowed to `gambling / adult / gate`.
- Non-specialized samples should normally continue to L1.

## 3. Current Default L0 Inputs

The default L0 hot path is intentionally narrow and low-cost. It uses:

- URL and cheap URL-structure signals
- visible text and title
- form summary
- network summary
- raw visible-text observability
- already available compact diff / evasion hints

## 4. Current Default L0 Prohibitions

The current default L0 path must not assume:

- full HTML scanning by default
- default brand extraction
- screenshot or OCR evidence
- heavy model inference
- click-through or interaction recovery
- gate solving

`html_features` and `brand_signals` may still exist as compatibility fields or externally provided side inputs. Their presence does not mean the default L0 hot path actively computes full HTML features or default brand extraction.

## 5. Older Assumptions That Should Not Be Carried Forward

Do not carry forward the following older assumptions:

- `fake verification` as a standalone active L0 specialized family
- `L0-fast / L1-text / L1-mm` as the official public top-level stage contract
- broad direct L0 resolution as an already frozen default contract
- full HTML, default brand extraction, screenshot/OCR, or heavy recovery logic as part of the normal L0 hot path

## 6. Current Implementation Status

- The active L0 implementation path is `src/warden/module/l0.py`.
- The legacy compatibility entrypoint remains in `scripts/labeling/Warden_auto_label_utils_brandlex.py`.
- `specialized_fast_resolution_candidate` currently remains a weak-signal and routing-oriented concept.
- If future work wants to freeze certain obvious specialized families into true direct L0 resolution, that requires a separate explicit task and doc update. That contract is not assumed to be active now.

## 7. Safe Continuation Boundary For The Next GPT Web Window

If the next window continues L0 work, keep these assumptions frozen:

- L0 continues to handle only low-cost specialized screening and routing for `gambling / adult / gate`
- non-specialized samples continue to L1
- L0 does not reopen the full HTML, default brand extraction, screenshot/OCR, or heavy interaction path
- future L0 work should stay in narrow sample-driven tuning unless a new explicit task changes the contract

## 8. One-Paragraph Continuation Summary

Warden's current repo-aligned L0 is a narrowed, low-cost, explainable screening and routing layer focused on `gambling / adult / gate`, using cheap URL/text/form/network evidence plus existing compact observability hints. It does not currently treat `fake verification` as a separate active family, does not expose `L0-fast / L1-text / L1-mm` as the official top-level contract, and does not reopen full HTML, default brand extraction, screenshot/OCR, heavy model inference, or interaction recovery in the default L0 hot path.
