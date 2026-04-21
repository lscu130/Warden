# Handoff Metadata

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

- Handoff ID: 2026-04-08-channel-url-keep-oldest-dedup
- Related Task ID: TASK-2026-04-08-CHANNEL-URL-KEEP-OLDEST-DEDUP
- Task Title: 为 channel 目录新增按 URL 去重并保留最老样本的低内存维护脚本
- Module: data / maintenance / dataset hygiene
- Author: Codex
- Date: 2026-04-08
- Status: DONE

---

## 1. Executive Summary

本次交付新增了一个 `channel/` 目录维护脚本：按样本目录名中的 URL 键分组，只保留最老时间戳对应的目录。  
脚本默认 dry-run，仅输出保留/删除清单；显式传 `--delete` 时才会删除较新的重复目录。  
实现采用两遍扫描，只在内存中保留每个 URL 的当前最老候选，避免把所有样本元数据整批载入内存。

---

## 2. What Changed

### Code Changes

- 新增 `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- 该脚本：
  - 扫描 `channel` 根目录下一层子目录
  - 解析 `<url_key>_<YYYYMMDDTHHMMSSZ>` 目录名
  - 按 `url_key` 分组，只保留最老时间戳目录
  - 输出 `keep_manifest.jsonl`、`delete_manifest.jsonl`、`summary.json`
  - 默认 dry-run，显式 `--delete` 才执行删除
  - 删除前校验目标目录仍位于输入根目录下

### Doc Changes

- 新增任务单：`docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- 更新 `docs/modules/MODULE_DATA.md`，明确该工具属于 opt-in maintenance utility，而不是默认 manifest intake 入口
- 新增本 handoff 文档

### Output / Artifact Changes

- dry-run 验证输出：
  - `E:\Warden\tmp\channel_url_dedup_real_check\keep_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_real_check\delete_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_real_check\summary.json`
- 删除模式 smoke 输出：
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\keep_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\delete_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\summary.json`

---

## 3. Files Touched

- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `docs/modules/MODULE_DATA.md`
- `docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- `docs/handoff/2026-04-08_channel_url_keep_oldest_dedup.md`

Optional notes per file:

- 新脚本没有修改任何现有 manifest / consistency 正式入口
- `MODULE_DATA.md` 只补了 maintenance 边界说明，没有改动冻结样本契约

---

## 4. Behavior Impact

### Expected New Behavior

- 运行新脚本时，会按目录名中的 `url_key` 对 `channel` 子目录分组
- 每个 `url_key` 只保留最老时间戳目录，较新的重复目录进入删除清单
- 默认模式下不会删除目录，只输出可审计的 keep/delete 清单
- 显式传 `--delete` 时，脚本才会递归删除较新的重复目录

### Preserved Behavior

- 现有 `build_manifest.py` 行为不变
- 现有 `check_dataset_consistency.py` 行为不变
- 冻结样本文件名、样本目录内部结构、manifest 字段和 schema 均未改变
- 新脚本不读取目录内 JSON 文件作为默认分组路径，因此不会放大 I/O 成本

### User-facing / CLI Impact

- 新增 CLI：
  - `python scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- 主要参数：
  - `--input-root`
  - `--output-dir`
  - `--delete`
  - `--skip-nonmatching`

### Output Format Impact

- 新增该脚本专用输出：
  - `keep_manifest.jsonl`
  - `delete_manifest.jsonl`
  - `summary.json`
- 现有任何脚本输出格式未被修改

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- new maintenance CLI at `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `docs/modules/MODULE_DATA.md` maintenance-utility documentation boundary

Compatibility notes:

本次没有改动冻结样本 schema、字段名、文件名、manifest 核心字段或已有 CLI。  
唯一新增的是一个独立维护脚本及其输出工件，因此兼容性风险局限在新工具本身。  
真实删除仍需操作者显式传 `--delete`，默认行为是只读 dry-run。

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --help
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root E:\Warden\channel --output-dir E:\Warden\tmp\channel_url_dedup_real_check
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root E:\Warden\tmp\channel_url_dedup_smoke --output-dir E:\Warden\tmp\channel_url_dedup_smoke_out --delete
```

### Result

- `py_compile` 通过
- `--help` 正常输出
- 对真实 `E:\Warden\channel` 的 dry-run 结果：
  - 扫描 2 个目录
  - 识别 1 个 URL key
  - 保留 `1-easybank-landing-page-master.vercel.app_20251230T075649Z`
  - 标记 `1-easybank-landing-page-master.vercel.app_20260306T075237Z` 为 `would_delete`
- 对临时 smoke 数据的删除模式结果：
  - 扫描 4 个子目录，其中 3 个匹配目录名模式、1 个非匹配目录 `notes`
  - `alpha.example_20250101T000000Z` 被保留
  - `alpha.example_20260101T000000Z` 被实际删除并记录为 `action=deleted`
  - `beta.example_20251231T235959Z` 保持不变

### Not Run

- 针对更大规模 `channel` 数据集的性能基准
- 递归目录场景验证
- 目录名不符合 `<url_key>_<YYYYMMDDTHHMMSSZ>` 但仍需去重的兼容路径

Reason:

本次目标是最小可用维护脚本与真实样本点验，不是全量性能基准或多种命名兼容策略扩展。  
当前实现按用户给出的 `channel` 目录模式和已观测样本目录名工作。

---

## 7. Risks / Caveats

- 当前分组依据是目录名中的 `url_key`，不是目录内 `url.json`；如果未来存在目录名与真实 URL 不一致的样本，本脚本会按目录名处理
- 当前扫描只看输入根目录下一层子目录，不做递归
- 若操作者把 `output-dir` 放到 `input-root` 之下，输出目录会被视为非匹配目录并计入 skipped 统计

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/MODULE_DATA.md`
- `docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- `docs/handoff/2026-04-08_channel_url_keep_oldest_dedup.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- 如果后续 `channel/` 目录规模明显增大，补一次针对真实大目录的耗时统计
- 如果后续发现目录名和 `url.json` 可能不一致，再单独立任务决定是否增加可选 `url.json` 校验模式
- 二审时重点确认：按目录名去重是否就是你要的业务口径

## English Version

# Handoff Metadata

- Handoff ID: 2026-04-08-channel-url-keep-oldest-dedup
- Related Task ID: TASK-2026-04-08-CHANNEL-URL-KEEP-OLDEST-DEDUP
- Task Title: Add a low-memory maintenance script that deduplicates channel directories by URL and keeps the oldest sample
- Module: data / maintenance / dataset hygiene
- Author: Codex
- Date: 2026-04-08
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

This delivery adds a `channel/` maintenance script that groups sample directories by the URL key encoded in the directory name and keeps only the oldest timestamped directory for each URL key.  
The script defaults to dry-run and emits keep/delete manifests; it deletes newer duplicate directories only when `--delete` is explicitly passed.  
The implementation uses two passes and keeps only the current oldest candidate per URL key in memory, rather than loading all sample metadata at once.

---

## 2. What Changed

### Code Changes

- Added `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- The script:
  - scans one directory level under a channel root
  - parses directory names of the form `<url_key>_<YYYYMMDDTHHMMSSZ>`
  - groups by `url_key` and keeps only the oldest timestamped directory
  - writes `keep_manifest.jsonl`, `delete_manifest.jsonl`, and `summary.json`
  - defaults to dry-run and only deletes on explicit `--delete`
  - verifies delete targets remain inside the requested input root before recursive removal

### Doc Changes

- Added task doc: `docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- Updated `docs/modules/MODULE_DATA.md` to state that this utility is an opt-in maintenance path rather than a default manifest-intake entrypoint
- Added this handoff doc

### Output / Artifact Changes

- Dry-run validation artifacts:
  - `E:\Warden\tmp\channel_url_dedup_real_check\keep_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_real_check\delete_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_real_check\summary.json`
- Delete-mode smoke artifacts:
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\keep_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\delete_manifest.jsonl`
  - `E:\Warden\tmp\channel_url_dedup_smoke_out\summary.json`

---

## 3. Files Touched

- `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `docs/modules/MODULE_DATA.md`
- `docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- `docs/handoff/2026-04-08_channel_url_keep_oldest_dedup.md`

Optional notes per file:

- The new script does not modify any existing manifest or consistency entrypoint.
- `MODULE_DATA.md` only received a maintenance-boundary clarification; no frozen sample contract was changed.

---

## 4. Behavior Impact

### Expected New Behavior

- Running the new script groups `channel` child directories by the `url_key` encoded in their directory names.
- For each `url_key`, only the oldest timestamped directory is kept; newer duplicate directories enter the delete manifest.
- In default mode, no directory is deleted and only auditable keep/delete artifacts are written.
- When `--delete` is explicitly passed, the script recursively deletes newer duplicate directories.

### Preserved Behavior

- `build_manifest.py` behavior is unchanged.
- `check_dataset_consistency.py` behavior is unchanged.
- Frozen sample filenames, sample-directory internal structure, manifest fields, and schema are unchanged.
- The new script does not read per-directory JSON files in its default grouping path, so it avoids unnecessary extra I/O.

### User-facing / CLI Impact

- Added new CLI:
  - `python scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- Main flags:
  - `--input-root`
  - `--output-dir`
  - `--delete`
  - `--skip-nonmatching`

### Output Format Impact

- Added script-specific outputs:
  - `keep_manifest.jsonl`
  - `delete_manifest.jsonl`
  - `summary.json`
- No output format of any existing script was changed.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: YES
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- new maintenance CLI at `scripts/data/maintenance/dedup_channel_by_url_keep_oldest.py`
- `docs/modules/MODULE_DATA.md` maintenance-utility boundary text

Compatibility notes:

No frozen sample schema, field name, file name, manifest core field, or existing CLI was changed.  
The only new interface is an independent maintenance script and its output artifacts, so compatibility risk is isolated to the new tool itself.  
Real deletion still requires the operator to pass `--delete`; the default behavior remains a read-only dry-run.

---

## 6. Validation Performed

### Commands Run

```bash
python -m py_compile E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --help
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root E:\Warden\channel --output-dir E:\Warden\tmp\channel_url_dedup_real_check
python E:\Warden\scripts\data\maintenance\dedup_channel_by_url_keep_oldest.py --input-root E:\Warden\tmp\channel_url_dedup_smoke --output-dir E:\Warden\tmp\channel_url_dedup_smoke_out --delete
```

### Result

- `py_compile` passed.
- `--help` rendered correctly.
- Real dry-run over `E:\Warden\channel`:
  - scanned 2 directories,
  - identified 1 URL key,
  - kept `1-easybank-landing-page-master.vercel.app_20251230T075649Z`,
  - marked `1-easybank-landing-page-master.vercel.app_20260306T075237Z` as `would_delete`.
- Delete-mode smoke run over controlled temp data:
  - scanned 4 child directories, with 3 matching the naming pattern and 1 non-matching `notes` directory,
  - kept `alpha.example_20250101T000000Z`,
  - actually deleted `alpha.example_20260101T000000Z` and recorded `action=deleted`,
  - left `beta.example_20251231T235959Z` unchanged.

### Not Run

- performance benchmarking over a larger real `channel` dataset
- recursive-directory validation
- a compatibility path for directories whose names do not follow `<url_key>_<YYYYMMDDTHHMMSSZ>` but still need deduplication

Reason:

The target here was a minimum viable maintenance script plus a real observed-sample check, not a full performance benchmark or expanded naming-compatibility strategy.  
The current implementation intentionally follows the user's observed `channel` naming pattern and current sample names.

---

## 7. Risks / Caveats

- Grouping is currently based on the directory-name `url_key`, not `url.json`; if future samples contain directory names that diverge from the real URL, this script will still deduplicate by directory name.
- The current scan is non-recursive and only inspects direct child directories under the input root.
- If an operator places `output-dir` inside `input-root`, that output directory will be treated as a non-matching child directory and counted under skipped entries.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `docs/modules/MODULE_DATA.md`
- `docs/tasks/2026-04-08_channel_url_keep_oldest_dedup_task.md`
- `docs/handoff/2026-04-08_channel_url_keep_oldest_dedup.md`

Doc debt still remaining:

- none

---

## 9. Recommended Next Step

- If `channel/` grows significantly, add one real larger-directory timing check.
- If directory names and `url.json` may diverge later, open a separate task to decide whether to add an optional `url.json` verification mode.
- In review, confirm that deduplicating by directory-name URL key is the intended business rule.
