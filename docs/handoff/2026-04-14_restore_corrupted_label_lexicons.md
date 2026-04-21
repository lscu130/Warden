# 中文摘要

- Handoff ID: HANDOFF-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Related Task ID: TASK-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Task Title: Restore corrupted Chinese lexicon entries in `Warden_auto_label_utils_brandlex.py`
- Module: labeling
- Author: Codex
- Date: 2026-04-14
- Status: DONE

## 1. Executive Summary

已修复 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 中剩余的中文词表污染问题。优先使用用户提供的桌面旧版本文件恢复历史存在的中文词条；对旧版本中不存在但当前工作树新增的少量列表，按现有列表职责做了最小中文补齐。当前文件可正常导入，`??` 占位词已清除，隐藏乱码字符也已清除。

## 2. What Changed

### Code Changes

- 恢复了 `WEB3_WALLET_KEYWORDS` 的中文词条，来源为用户提供的旧文件。
- 恢复了 `GAMBLING_KEYWORDS`、`GAMBLING_BONUS_KEYWORDS` 的中文词条，来源为用户提供的旧文件。
- 恢复了 `ADULT_KEYWORDS`、`ADULT_HIGH_CONFIDENCE_KEYWORDS`、`ADULT_AGE_GATE_KEYWORDS` 的中文词条，来源为用户提供的旧文件。
- 恢复了 `GATE_SURFACE_KEYWORDS`、`GATE_STRONG_KEYWORDS` 的中文词条，来源为用户提供的旧文件，并补了一个与当前列表语义一致的 `点击继续`。
- 为当前工作树新增但旧文件未包含的列表做了最小补齐：`GAMBLING_STRONG_TEXT_KEYWORDS`、`GAMBLING_ACTION_KEYWORDS`、`GAMBLING_STRONG_BONUS_KEYWORDS`、`GATE_SHORT_FLOW_KEYWORDS`。

### Doc Changes

- 新增 task 文档。
- 新增 handoff 文档。

### Output / Artifact Changes

- none

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` 仅做词表修复和占位词清理，未改接口或判定流程。
- task 文档记录本次恢复边界。
- handoff 文档记录恢复来源和残余风险。

## 4. Behavior Impact

### Expected New Behavior

- 中文赌博、成人、门控、人机验证和 web3 钱包相关规则词条重新可用。
- 规则召回不再因为 `??` 占位词而丢失这部分中文信号。
- 标注工具导入稳定，不再受这批已确认乱码字符影响。

### Preserved Behavior

- `derive_auto_labels` / `derive_rule_labels` 接口未变。
- schema、CLI、输出结构未变。
- 当前工作树已有的规则流程和加权逻辑未改。

### User-facing / CLI Impact

- 无新增 CLI。
- 现有抓取脚本对该模块的导入路径保持不变。

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

本次只恢复词表字面量，不改函数签名、不改输出 key、不改调用方式。下游脚本无需改动。

## 6. Validation Performed

### Commands Run

```bash
Select-String -Path 'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py' -Pattern '"\?\?|"\\?\\?\\?|"\?\?\?\?|"\?\?\?\?\?' -Encoding UTF8
python -c "import sys; sys.path.insert(0, r'E:\Warden\scripts\labeling'); import Warden_auto_label_utils_brandlex as m; print('import_ok'); print('彩金' in m.GAMBLING_KEYWORDS, '约炮' in m.ADULT_KEYWORDS, '人机验证' in m.GATE_SURFACE_KEYWORDS)"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print(any(0xE000 <= ord(ch) <= 0xF8FF or ord(ch) == 0xFEFF for ch in text))"
```

### Result

- `Select-String` 未返回剩余 `??` 词表占位项。
- 模块导入成功，代表性恢复词条命中结果为 `True True True`。
- 隐藏私有区字符和 BOM 扫描结果为 `False`。

### Not Run

- 完整抓取流程实跑
- 标注规则回归集评估
- 全量数据集召回对比

Reason:

本次任务目标是词表恢复和导入稳定性修复，未扩展到全量抓取或规则评估。

## 7. Risks / Caveats

- `GAMBLING_STRONG_TEXT_KEYWORDS`、`GAMBLING_ACTION_KEYWORDS`、`GAMBLING_STRONG_BONUS_KEYWORDS`、`GATE_SHORT_FLOW_KEYWORDS` 中的中文补齐有一部分来自当前逻辑语义推定，不是从旧文件逐字恢复。
- 即便 `??` 已清除，词表召回质量仍应通过小批量中文样本做一次回归验证。
- 当前工作树本身还有其他与本任务无关的本地改动；本次未处理它们。

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

Doc debt still remaining:

- none

## 9. Recommended Next Step

- 用 10 到 20 个中文赌博 / 成人 / gate 页面样本跑一次 `derive_auto_labels` 小批量 smoke，确认恢复后的中文词条实际参与命中。
- 如果你手上还有更早的完整版本，可以再对 `GAMBLING_ACTION_KEYWORDS` 和 `GATE_SHORT_FLOW_KEYWORDS` 做一次逐字核对。

---

# English Version

# Handoff Metadata

- Handoff ID: HANDOFF-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Related Task ID: TASK-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Task Title: Restore corrupted Chinese lexicon entries in `Warden_auto_label_utils_brandlex.py`
- Module: labeling
- Author: Codex
- Date: 2026-04-14
- Status: DONE

## 1. Executive Summary

The remaining corrupted Chinese lexicon entries in `scripts/labeling/Warden_auto_label_utils_brandlex.py` were repaired. Historical Chinese entries were restored primarily from the user-provided desktop baseline file. A small number of newer lists that do not exist in the older file were filled with the smallest semantically aligned Chinese entries consistent with their current purpose. The file now imports cleanly, no `??` placeholder entries remain, and hidden corrupted codepoints are gone.

## 2. What Changed

### Code Changes

- Restored `WEB3_WALLET_KEYWORDS` Chinese entries from the user-provided baseline file.
- Restored `GAMBLING_KEYWORDS` and `GAMBLING_BONUS_KEYWORDS` Chinese entries from the user-provided baseline file.
- Restored `ADULT_KEYWORDS`, `ADULT_HIGH_CONFIDENCE_KEYWORDS`, and `ADULT_AGE_GATE_KEYWORDS` Chinese entries from the user-provided baseline file.
- Restored `GATE_SURFACE_KEYWORDS` and `GATE_STRONG_KEYWORDS` Chinese entries from the user-provided baseline file and added one semantically aligned `点击继续` entry for the larger current list.
- Applied minimal semantic fills for current working-tree lists that do not exist in the older file: `GAMBLING_STRONG_TEXT_KEYWORDS`, `GAMBLING_ACTION_KEYWORDS`, `GAMBLING_STRONG_BONUS_KEYWORDS`, and `GATE_SHORT_FLOW_KEYWORDS`.

### Doc Changes

- Added the task document.
- Added the handoff document.

### Output / Artifact Changes

- none

## 3. Files Touched

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

Optional notes per file:

- `Warden_auto_label_utils_brandlex.py` was changed only for lexicon restoration and placeholder cleanup; interfaces and rule flow were preserved.
- The task doc records the execution boundary.
- The handoff doc records recovery sources and residual risk.

## 4. Behavior Impact

### Expected New Behavior

- Chinese gambling, adult, gate / human-verification, and web3 wallet rule keywords are usable again.
- Rule recall no longer drops these Chinese signals because of `??` placeholder entries.
- Labeling-module import stability is no longer affected by this confirmed set of corrupted lexicon content.

### Preserved Behavior

- `derive_auto_labels` / `derive_rule_labels` interfaces are unchanged.
- Schema, CLI, and output structure are unchanged.
- The current rule flow and weighting logic in the working tree were not modified.

### User-facing / CLI Impact

- No new CLI was added.
- Existing capture-script imports of this module remain unchanged.

### Output Format Impact

- none

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- none

Compatibility notes:

This change only restores lexicon literals. It does not modify function signatures, output keys, or call patterns. Downstream scripts do not need changes.

## 6. Validation Performed

### Commands Run

```bash
Select-String -Path 'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py' -Pattern '"\?\?|"\\?\\?\\?|"\?\?\?\?|"\?\?\?\?\?' -Encoding UTF8
python -c "import sys; sys.path.insert(0, r'E:\Warden\scripts\labeling'); import Warden_auto_label_utils_brandlex as m; print('import_ok'); print('彩金' in m.GAMBLING_KEYWORDS, '约炮' in m.ADULT_KEYWORDS, '人机验证' in m.GATE_SURFACE_KEYWORDS)"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print(any(0xE000 <= ord(ch) <= 0xF8FF or ord(ch) == 0xFEFF for ch in text))"
```

### Result

- `Select-String` returned no remaining `??` placeholder lexicon entries.
- Module import succeeded, and representative restored keywords returned `True True True`.
- Hidden private-use and BOM scan returned `False`.

### Not Run

- full capture-flow execution
- labeling regression-set evaluation
- full-dataset recall comparison

Reason:

The scope of this task was lexicon restoration and import stability. It did not extend into full capture execution or broad rule evaluation.

## 7. Risks / Caveats

- Some Chinese fills in `GAMBLING_STRONG_TEXT_KEYWORDS`, `GAMBLING_ACTION_KEYWORDS`, `GAMBLING_STRONG_BONUS_KEYWORDS`, and `GATE_SHORT_FLOW_KEYWORDS` were inferred from the current list semantics rather than copied verbatim from the older file.
- Even though `??` placeholders are gone, recall quality should still be verified on a small Chinese sample set.
- The working tree contains other unrelated local changes; this task did not touch them.

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

Doc debt still remaining:

- none

## 9. Recommended Next Step

- Run a small 10 to 20 sample Chinese gambling / adult / gate smoke set through `derive_auto_labels` to confirm the restored keywords actually participate in matches.
- If an even older complete version exists, use it to do a literal cross-check on `GAMBLING_ACTION_KEYWORDS` and `GATE_SHORT_FLOW_KEYWORDS`.
