# Handoff Metadata

- Handoff ID: HANDOFF-2026-03-20-DATASET-REVIEWER-UNDO-PATH-FIX
- Related Task ID: TASK-2026-03-20-DATASET-REVIEWER-UNDO-PATH-FIX
- Task Title: Fix undo path nesting in dataset reviewer external script
- Module: external dataset review utility
- Author: Codex
- Date: 2026-03-20
- Status: DONE

Use this template for any non-trivial engineering delivery in Warden.

Rules:

- Write what actually happened, not what was planned.
- If something was not run, say so explicitly.
- If no change happened in a category, write `none`.
- Keep claims auditable against diffs, commands, and current files.

---

## 1. Executive Summary

Updated the repo-tracked copy of `dataset_reviewed_switchable_targets.py` to make undo restore removed samples back to the canonical dataset-relative path derived from `sample.key`, instead of trusting only the transient recorded source path. Also pruned empty parent directories left inside the target tree after undo. This addresses the reported `phish/removed` and lingering `removed/phish` nesting pattern.

---

## 2. What Changed

### Code Changes

- Added a non-persisted `target_root` field to `ActionRecord` so undo can clean up empty parent directories inside the original remove target tree.
- Added helpers to derive a stable sample-relative path and canonical restore path from `sample.key`.
- Changed undo for `remove` actions to restore to the canonical dataset-relative path and prune empty target-side parent directories after the move back.

### Doc Changes

- Added a repo task document for this repair.
- Added this repo handoff document.
- none

### Output / Artifact Changes

- Added a targeted validation script under `E:\Warden\tmp\dataset_reviewer_undo_validation.py`.
- none
- none

If nothing changed in one category, say `none`.

---

## 3. Files Touched

List only files actually touched.

- `E:\Warden\temp\dataset_reviewed_switchable_targets.py`
- `E:\Warden\docs\tasks\2026-03-20_dataset_reviewer_undo_path_fix.md`
- `E:\Warden\docs\handoff\2026-03-20_dataset_reviewer_undo_path_fix.md`
- `E:\Warden\tmp\dataset_reviewer_undo_validation.py`

Optional notes per file:

- Script copy updated with the minimal path-handling fix.
- Task doc created because this is a non-trivial behavior change under repo workflow.
- Validation helper created for a synthetic `phish -> removed -> undo` scenario.

---

## 4. Behavior Impact

Describe what behavior is now different.

### Expected New Behavior

- Undo after a remove restores the sample directory to `dataset_root / sample.key`.
- Undo no longer depends solely on the previously recorded `src` path when deciding where the sample goes back.
- Empty parent directories such as `removed/phish` created only to hold a removed sample are pruned after a successful undo.

### Preserved Behavior

- Remove still moves the sample into the currently selected target root while preserving the sample-relative layout.
- Keep, conflict skip, auto skip, UI controls, state file names, and target history file names are unchanged.
- No persisted schema or public CLI entrypoint was renamed.

### User-facing / CLI Impact

- `python E:\Warden\temp\dataset_reviewed_switchable_targets.py` remains valid.

### Output Format Impact

- No output file format changes.

Do not hand-wave here.
If behavior did not change, say so explicitly.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `ActionRecord` runtime history object in memory only
- `sample.key` as the canonical dataset-relative restore basis
- Tkinter remove / undo behavior

Compatibility notes:

No persisted JSON schema, log file name, target history format, or CLI entrypoint changed. The new `target_root` field exists only in runtime history records and is not written to disk. Downstream scripts reading `.review_state.json` or `.review_targets.json` are unaffected.

If there is any downstream risk, spell it out clearly.

---

## 6. Validation Performed

List what was actually checked.

### Commands Run

```bash
python -m py_compile E:\Warden\temp\dataset_reviewed_switchable_targets.py
python E:\Warden\tmp\dataset_reviewer_undo_validation.py
```

### Result

- Syntax compilation passed.
- Synthetic path validation passed for `phish/case1 -> removed/phish/case1 -> undo`.
- Validation confirmed the canonical restore path exists after undo and that no nested `phish\removed` or empty `removed\phish` directory remains.

### Not Run

- Full interactive Tkinter UI manual test
- Validation against the user's real dataset tree
- Regression test for all alternate target-root selections outside the default `removed`

Reason:

Only a minimal local smoke validation was run in the workspace sandbox. No real user dataset or interactive desktop session was exercised in this turn.

---

## 7. Risks / Caveats

- The repo-tracked fix still needs to be copied back to `C:\Users\20516\Downloads\dataset_reviewed_switchable_targets.py` to affect the user’s original file.
- The targeted validation covered the reported default `phish` / `removed` pattern, not every possible custom target-root topology.
- Existing misnested directories already created in the user dataset are not automatically repaired by this patch.

If there are no meaningful risks, say `none`.

---

## 8. Docs Impact

- Docs updated: YES

Docs touched:

- `E:\Warden\docs\tasks\2026-03-20_dataset_reviewer_undo_path_fix.md`
- `E:\Warden\docs\handoff\2026-03-20_dataset_reviewer_undo_path_fix.md`

Doc debt still remaining:

- none
- none

If none, say `none`.

---

## 9. Recommended Next Step

- Copy `E:\Warden\temp\dataset_reviewed_switchable_targets.py` back to `C:\Users\20516\Downloads\dataset_reviewed_switchable_targets.py`.
- Run one manual remove/undo cycle against the real dataset tree that previously produced `phish/removed` and `removed/phish`.
- If old nested directories already exist, clean them manually or with a separate repair script after confirming which samples they belong to.
