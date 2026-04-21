# 2026-04-10_capture_html_json_storage

## 中文版

> 面向 AI 的说明：GPT、Gemini、Codex、Grok、Claude 仅将下方英文版视为权威版本。中文仅供人类阅读、协作与快速导览。

### 使用说明

- 本任务用于把抓取产物里的 HTML 从裸 `.html` 文件改为 JSON 封装，降低 Windows 安全中心隔离风险。
- 这次改动会触碰当前冻结输出文档中的 HTML 文件名约定，所以必须同步更新受影响脚本和文档，不能只改抓取入口。
- 若涉及精确文件名、兼容性、CLI 或验证结果，以英文版为准。

## English Version

# Task Metadata

- Task ID: WARDEN-CAPTURE-HTML-JSON-STORAGE-V1
- Task Title: Store captured HTML payloads as JSON wrappers, keep downstream readers migration-compatible, and add a legacy HTML-to-JSON conversion utility
- Owner Role: Codex execution engineer
- Priority: High
- Status: DONE
- Related Module: Data module / capture operations / labeling compatibility
- Related Issue / ADR / Doc: `AGENTS.md`; `PROJECT.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; `docs/modules/MODULE_DATA.md`; `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`; `docs/frozen/SCHEMA_REGISTRY.md`; `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- Created At: 2026-04-10
- Requested By: user

---

## 1. Background

The current capture pipeline writes raw HTML artifacts directly as `.html` files such as `html_raw.html`, `html_rendered.html`, variant `html_rendered.html`, and `after_action/step1_html_rendered.html`.
The user explicitly requested changing captured HTML storage to JSON because Windows security tooling may quarantine raw HTML files.
This request conflicts with the current frozen output docs that still describe `.html` files, so the change must be handled as an explicit contract update with synchronized downstream-reader compatibility and documentation updates.

---

## 2. Goal

Update the capture pipeline so newly captured HTML payloads are stored as JSON files instead of raw `.html` files, add a repo utility that converts legacy sample directories from old HTML files to the new JSON form, and preserve downstream usability by making current readers support both the new JSON storage and legacy `.html` fallback during migration.

---

## 3. Scope In

This task is allowed to touch:

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/common/`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/common/fingerprint_utils.py`
- `scripts/data/benign/recover_benign_batch.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`
- `scripts/data/maintenance/`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`
- `docs/tasks/`
- `docs/handoff/`

This task is allowed to change:

- capture-time HTML artifact filenames and file format for newly written HTML payloads
- downstream file-presence and file-read logic for HTML payloads
- maintenance tooling for legacy sample conversion
- docs that describe the frozen sample-output contract and operational usage

If a file or directory is not listed here, assume it is out of scope unless explicitly approved later.

---

## 4. Scope Out

This task must NOT do the following:

- do not redesign the whole capture pipeline or sample directory layout
- do not rename non-HTML sample artifacts such as `meta.json`, `url.json`, `visible_text.txt`, `forms.json`, `net_summary.json`, or screenshots
- do not change weak-label schema, manifest core field names, or training/inference logic
- do not add new third-party dependencies
- do not silently broaden this patch into unrelated cleanup across other modules

---

## 5. Inputs

Relevant inputs for this task:

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- `docs/modules/MODULE_DATA.md`
- `docs/modules/Warden_DATA_INGEST_RUNBOOK_V1.md`
- `docs/frozen/SCHEMA_REGISTRY.md`
- `docs/frozen/Warden_Dataset_Output_Frozen_Spec_v1.1.md`

### Code / Scripts

- `scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/common/fingerprint_utils.py`
- `scripts/data/benign/recover_benign_batch.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

### Data / Artifacts

- legacy sample directories that still contain `*.html` artifacts

### Prior Handoff

- none

### Missing Inputs

- none

---

## 6. Required Outputs

This task should produce:

- updated capture logic that writes HTML payloads as JSON files for new captures
- downstream reader compatibility for both new HTML JSON files and legacy `.html` files
- a new maintenance script that converts legacy HTML files to JSON wrappers
- updated frozen-output and runbook docs that describe the new contract
- a formal repo handoff document

Be concrete.

---

## 7. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility unless explicitly waived.
- Do not rename frozen schema fields.
- Do not silently change output format.
- Do not add third-party dependencies without approval.
- Prefer minimal patch over broad refactor.
- Update relevant docs if behavior changes.
- Follow `AGENTS.md`.
- Follow `docs/workflow/GPT_CODEX_WORKFLOW.md`.
- Produce handoff content for non-trivial changes.
- If this task outputs Markdown documents, those documents must be bilingual by default: Chinese summary first, full English version second, with English authoritative.

Task-specific constraints:

- The explicit user request allows changing current HTML artifact file names from `.html` to `.json`, but only for HTML payload artifacts.
- New downstream read paths must accept both new JSON HTML wrappers and legacy raw `.html` files during migration.
- The JSON wrapper must preserve the HTML text payload in UTF-8 and remain easy to audit.
- Newly captured sample directories should stop writing raw `.html` files for the HTML payloads covered by this task.

---

## 8. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing `run_benign_capture.py` commands
- existing `run_malicious_capture.py` commands
- existing `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py` commands unrelated to HTML storage naming

Schema / field constraints:

- Schema changed allowed: YES
- If yes, required compatibility plan: change only HTML artifact filenames and storage format, keep current semantic meanings, preserve legacy-read fallback, and update affected docs in the same patch
- Frozen field names involved: `has_html_rendered`, `has_html_raw`, `html_raw.html`, `html_rendered.html`, `step1_html_rendered.html`

CLI / output compatibility constraints:

- Existing commands that must keep working:
  - `python scripts/data/benign/run_benign_capture.py --input_path ...`
  - `python scripts/data/malicious/run_malicious_capture.py --input_path ... --source ...`
  - `python scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py --input_path ... --label ...`

Downstream consumers to watch:

- `scripts/data/build_manifest.py`
- `scripts/data/check_dataset_consistency.py`
- `scripts/data/common/fingerprint_utils.py`
- `scripts/data/benign/recover_benign_batch.py`
- `scripts/labeling/Warden_auto_label_utils_brandlex.py`

---

## 9. Suggested Execution Plan

Recommended order:

1. Read the current capture write paths and downstream HTML read paths.
2. Add a small shared helper for HTML JSON write/read and legacy fallback.
3. Update the capture script to write HTML JSON payloads for main sample output, `after_action`, and variant output.
4. Update downstream readers and presence checks to treat new JSON HTML files as the active format while keeping legacy `.html` fallback.
5. Add a maintenance conversion CLI for legacy sample directories.
6. Update output-contract and operator docs.
7. Run the smallest meaningful validation.
8. Prepare handoff.

Task-specific execution notes:

- Keep manifest booleans such as `has_html_rendered` and `has_html_raw` unchanged in meaning.
- Prefer a single helper implementation over scattered ad hoc parsing.
- If destructive legacy cleanup is supported by the conversion tool, make it explicit and auditable rather than implicit.

---

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

Task-specific acceptance checks:

- [ ] new captures write HTML payloads as JSON files instead of raw `.html` files
- [ ] downstream readers can still read legacy sample directories that only contain raw `.html` files
- [ ] a legacy conversion script exists and can convert at least one old sample directory layout
- [ ] docs now describe the new HTML JSON storage contract and migration compatibility

---

## 11. Validation Checklist

Minimum validation expected:

- [ ] syntax / import sanity
- [ ] targeted smoke test
- [ ] backward compatibility spot-check
- [ ] output artifact spot-check

Commands to run if applicable:

```bash
python -m py_compile scripts/capture/capture_url_v6_optimized_v6_2_plus_labels_brandlex.py scripts/data/build_manifest.py scripts/data/check_dataset_consistency.py scripts/data/common/fingerprint_utils.py scripts/data/benign/recover_benign_batch.py scripts/labeling/Warden_auto_label_utils_brandlex.py scripts/data/maintenance/convert_legacy_html_to_json.py
python scripts/data/maintenance/convert_legacy_html_to_json.py --help
python scripts/data/maintenance/convert_legacy_html_to_json.py --input_roots <temp_root> --dry_run
```

Expected evidence to capture:

- successful syntax compilation of touched Python files
- conversion-script help and smoke output showing legacy HTML detection / conversion counts

---

## 12. Handoff Requirements

This task must end with handoff coverage matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis for this task:

- executive summary
- files touched
- behavior impact
- schema / interface impact
- validation performed
- risks / caveats
- recommended next step

Repo handoff path if one should be created:

- `docs/handoff/2026-04-10_capture_html_json_storage.md`

---

## 13. Open Questions / Blocking Issues

- none
