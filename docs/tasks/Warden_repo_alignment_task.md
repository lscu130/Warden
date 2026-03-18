# Warden repo alignment task

## goal
将仓库代码与文档重新对齐到当前 TRAINSET_V1 数据结构；清理仍在“活跃代码/文档/默认路径”中的 EVT 残留；重新补回 `scripts/data/build_manifest.py` 与 `scripts/data/check_dataset_consistency.py`。

## scope_in
- `docs/data/TRAINSET_V1.md`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/data/build_manifest.py`（新增）
- `scripts/data/check_dataset_consistency.py`（新增）

## scope_out
- 不批量改写 `data/raw/**` 现有样本内容
- 不重命名冻结样本文件名
- 不改训练模块
- 不改推理模块
- 不新增第三方依赖
- 不把弱标签改写成金标语义

## constraints
1. 保持当前样本目录冻结结构：
   - required: `meta.json`, `url.json`, `env.json`, `redirect_chain.json`, `screenshot_viewport.png`, `net_summary.json`, `auto_labels.json`
   - recommended: `visible_text.txt`, `forms.json`, `html_rendered.html`
   - optional: `html_raw.html`, `screenshot_full.png`, `rule_labels.json`, `manual_labels.json`
2. `build_manifest.py` 输出主文件为 `manifest.jsonl`
3. `check_dataset_consistency.py` 读取 `manifest.jsonl`
4. 目录层 `phish/benign` 不能被当作绝对真值；弱标签优先来自 `auto_labels.json`
5. `Warden_auto_label_utils_brandlex.py` 允许保留 EVT 旧品牌词典文件名作为兼容 fallback，但默认活跃命名应切到 Warden
6. 不修改现有 top-level JSON key 语义

## files_to_touch
- `docs/data/TRAINSET_V1.md`
- `scripts/labeling/Warden_dataset_backfill_labels_brandlex.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`

## required_fixes
1. 文档中的脚本链路改为 Warden 命名，不再写 `evt_dataset_backfill_labels_brandlex.py` / `evt_auto_label_utils_brandlex.py`
2. `Warden_dataset_backfill_labels_brandlex.py` 的 usage / import 全部改为 Warden 命名
3. `Warden_auto_label_utils_brandlex.py` 的默认品牌词典发现逻辑：
   - 先找 `WARDEN_BRAND_LEXICON`
   - 再找 Warden 风格文件名
   - 最后兼容回退 EVT 风格文件名
4. 新增 `scripts/data/build_manifest.py`
5. 新增 `scripts/data/check_dataset_consistency.py`

## acceptance
- 仓库中 `scripts/` 下重新出现 `data/` 目录与两份脚本
- `TRAINSET_V1.md` 中不再把活跃脚本链路写成 EVT 名称
- `Warden_dataset_backfill_labels_brandlex.py` 能正确 import `Warden_auto_label_utils_brandlex`
- `Warden_auto_label_utils_brandlex.py` 的默认路径/环境变量不再以 EVT 为主
- `build_manifest.py` 可根据当前冻结结构导出 `manifest.jsonl`
- `check_dataset_consistency.py` 可对 `manifest.jsonl` 生成 JSON/Markdown 报告
- 保持无新增第三方依赖
