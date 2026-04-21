# 中文摘要

- Task ID: TASK-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Task Title: Restore corrupted Chinese lexicon entries in `Warden_auto_label_utils_brandlex.py`
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: labeling
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; user-provided baseline file `C:\Users\20516\Desktop\Warden_auto_label_utils_brandlex.py`
- Created At: 2026-04-14
- Requested By: user

## 1. Background

当前仓库文件 `scripts/labeling/Warden_auto_label_utils_brandlex.py` 出现编码污染，多个中文词表被替换为 `??` 占位串，且部分位置此前混入了隐藏乱码字符。该问题会削弱规则召回，并曾导致导入路径不稳定。用户已提供桌面旧版本文件作为恢复参考。

## 2. Goal

恢复当前工作树中被污染的中文词表内容，优先按用户提供的旧版本逐段还原；旧版本中不存在但当前逻辑新增的词表，仅做与现有语义一致的最小补齐。要求保持当前脚本结构、接口、字段、函数和规则流程不变。

## 3. Scope In

允许修改：

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

允许变更：

- 修复被污染的中文关键词字面量
- 清除剩余的 `??` 占位词表项
- 记录恢复来源与推定补齐范围

## 4. Scope Out

- 不重构标注逻辑
- 不修改 schema、函数签名、CLI、输出文件结构
- 不新增依赖
- 不处理与本次词表恢复无关的脚本问题

## 5. Inputs

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs/workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs/templates\TASK_TEMPLATE.md`
- `E:\Warden\docs/templates\HANDOFF_TEMPLATE.md`

### Code / Scripts

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `C:\Users\20516\Desktop\Warden_auto_label_utils_brandlex.py`

### Prior Handoff

- none

### Missing Inputs

- 当前新增词表的单独设计文档缺失

## 6. Required Outputs

- 恢复后的 `Warden_auto_label_utils_brandlex.py`
- 对应 repo task 文档
- 对应 repo handoff 文档
- 最小验证结果

## 7. Hard Constraints

- 保持向后兼容
- 不重命名冻结字段
- 不静默修改输出格式
- 不新增第三方依赖
- 优先最小补丁
- 仅恢复损坏词表，不扩大到规则重写
- 对旧文件不存在的新增词表，补齐必须与当前列表用途一致

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels`
- `derive_rule_labels`
- 现有 `auto_labels` / `rule_labels` 输出结构

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
  - `python -c "import Warden_auto_label_utils_brandlex"`
  - existing labeling imports from capture scripts

Downstream consumers to watch:

- capture import path
- labeling rule recall for Chinese pages

## 9. Suggested Execution Plan

1. Read the current file and the user-provided baseline file.
2. Identify placeholder-corrupted lexicon entries.
3. Restore entries from baseline where available.
4. Fill remaining placeholder entries in newer lists with minimal semantically aligned Chinese keywords.
5. Run import and placeholder scans.
6. Produce handoff.

Task-specific execution notes:

- Prefer exact baseline restoration over inference.
- Mark inferred restorations clearly in handoff.
- Do not touch unrelated local edits in the same file.

## 10. Acceptance Criteria

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes
- [ ] No `??` placeholder lexicon entries remain in `Warden_auto_label_utils_brandlex.py`
- [ ] The labeling module imports successfully
- [ ] The source of each restored block is documented

## 11. Validation Checklist

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -c "import pathlib; import sys; sys.path.insert(0, r'E:\Warden\scripts\labeling'); import Warden_auto_label_utils_brandlex; print('import_ok')"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print('??' in text)"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print(any(0xE000 <= ord(ch) <= 0xF8FF or ord(ch)==0xFEFF for ch in text))"
```

Expected evidence to capture:

- import succeeds
- placeholder and hidden-codepoint scans return clean

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- exact restored lexicon areas
- distinction between baseline-restored and inferred entries
- validation performed
- residual recall risks

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

## 13. Open Questions / Blocking Issues

- none

---

# English Version

# Task Metadata

- Task ID: TASK-2026-04-14-RESTORE-CORRUPTED-LABEL-LEXICONS
- Task Title: Restore corrupted Chinese lexicon entries in `Warden_auto_label_utils_brandlex.py`
- Owner Role: Codex
- Priority: High
- Status: DONE
- Related Module: labeling
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; user-provided baseline file `C:\Users\20516\Desktop\Warden_auto_label_utils_brandlex.py`
- Created At: 2026-04-14
- Requested By: user

Use this task doc for the current non-trivial labeling repair.

## 1. Background

The current repo copy of `scripts/labeling/Warden_auto_label_utils_brandlex.py` has encoding corruption. Multiple Chinese lexicon entries were replaced by `??` placeholders, and some locations previously contained hidden corrupted codepoints. This weakens rule recall and previously made import stability unreliable. The user has provided an older desktop copy as a recovery baseline.

## 2. Goal

Restore the corrupted Chinese lexicon content in the current working tree. Use the user-provided older file as the primary recovery source wherever possible. For newer lexicon lists that do not exist in the older file, apply only the smallest semantically aligned fill needed to remove the damaged placeholders. Keep the current script structure, interfaces, fields, and rule flow unchanged.

## 3. Scope In

This task is allowed to touch:

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`
- `E:\Warden\docs\tasks\2026-04-14_restore_corrupted_label_lexicons.md`
- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

This task is allowed to change:

- corrupted Chinese keyword literals
- remaining `??` placeholder lexicon entries
- documentation of recovery source and inferred fill areas

## 4. Scope Out

This task must NOT do the following:

- redesign labeling logic
- modify schema, function signatures, CLI, or output file structure
- add dependencies
- fix unrelated script issues outside this lexicon restoration

## 5. Inputs

### Docs

- `E:\Warden\AGENTS.md`
- `E:\Warden\docs/workflow\GPT_CODEX_WORKFLOW.md`
- `E:\Warden\docs/templates\TASK_TEMPLATE.md`
- `E:\Warden\docs/templates\HANDOFF_TEMPLATE.md`

### Code / Scripts

- `E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- `C:\Users\20516\Desktop\Warden_auto_label_utils_brandlex.py`

### Prior Handoff

- none

### Missing Inputs

- no separate design doc exists for the newer lexicon additions

## 6. Required Outputs

This task should produce:

- restored `Warden_auto_label_utils_brandlex.py`
- repo task document
- repo handoff document
- minimal validation results

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies.
- Prefer a minimal patch.
- Restore damaged lexicons only; do not broaden into rule redesign.
- For newer lists absent from the baseline file, any fill must remain aligned with the current list purpose.

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- `derive_auto_labels`
- `derive_rule_labels`
- the current `auto_labels` / `rule_labels` output structure

Schema / field constraints:

- Schema changed allowed: no
- If yes, required compatibility plan: not applicable
- Frozen field names involved: none

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python E:\Warden\scripts\capture\capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
  - `python -c "import Warden_auto_label_utils_brandlex"`
  - existing labeling imports from capture scripts

Downstream consumers to watch:

- capture import path
- labeling rule recall for Chinese pages

## 9. Suggested Execution Plan

1. Read the current file and the user-provided baseline file.
2. Identify placeholder-corrupted lexicon entries.
3. Restore entries from the baseline where available.
4. Fill remaining placeholder entries in newer lists with minimal semantically aligned Chinese keywords.
5. Run import and placeholder scans.
6. Prepare handoff.

Task-specific execution notes:

- Prefer exact baseline restoration over inference.
- Mark inferred restorations clearly in the handoff.
- Do not overwrite unrelated local edits in the same file.

## 10. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] Goal is met
- [ ] Scope-out items were not touched
- [ ] Relevant files were updated correctly
- [ ] No silent schema / interface break was introduced
- [ ] Validation was run, or inability to run was explicitly stated
- [ ] Risks are documented
- [ ] Required docs were updated or doc debt was explicitly listed
- [ ] Final response follows required engineering format
- [ ] Handoff is provided for non-trivial changes
- [ ] No `??` placeholder lexicon entries remain in `Warden_auto_label_utils_brandlex.py`
- [ ] The labeling module imports successfully
- [ ] The source of each restored block is documented

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -c "import pathlib; import sys; sys.path.insert(0, r'E:\Warden\scripts\labeling'); import Warden_auto_label_utils_brandlex; print('import_ok')"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print('??' in text)"
python -c "from pathlib import Path; text=Path(r'E:\Warden\scripts\labeling\Warden_auto_label_utils_brandlex.py').read_text(encoding='utf-8'); print(any(0xE000 <= ord(ch) <= 0xF8FF or ord(ch)==0xFEFF for ch in text))"
```

Expected evidence to capture:

- import succeeds
- placeholder and hidden-codepoint scans are clean

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- exact restored lexicon areas
- distinction between baseline-restored and inferred entries
- validation performed
- residual recall risks

Repo handoff path if one should be created:

- `E:\Warden\docs\handoff\2026-04-14_restore_corrupted_label_lexicons.md`

## 13. Open Questions / Blocking Issues

- none
