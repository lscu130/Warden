# Handoff Metadata

- Handoff ID: 2026-03-20-agents-workflow-contract-strengthening
- Related Task ID: ad-hoc-user-request
- Task Title: Strengthen AGENTS to enforce workflow, task, and handoff contracts
- Module: project-governance
- Author: Codex
- Date: 2026-03-20
- Status: DONE

---

## 1. Executive Summary

Updated the root `AGENTS.md` to make `AGENTS.md`, `docs/workflow/GPT_CODEX_WORKFLOW.md`, `docs/templates/TASK_TEMPLATE.md`, and `docs/templates/HANDOFF_TEMPLATE.md` mandatory governing files instead of soft references.
This change was made so future threads in `E:\Warden` are forced to respect workflow order, task-boundary discipline, and handoff requirements.
Current completion state: done.

---

## 2. What Changed

### Code Changes
- none

### Doc Changes
- Rewrote `AGENTS.md` into a stronger process contract with explicit mandatory-file rules.
- Added hard rules for when task docs are required, when handoffs are required, and when execution must stop for clarification.
- Added cross-thread continuity rules so new threads do not silently ignore workflow artifacts or repository-external active documents.

### Output / Artifact Changes
- Added this handoff document under `docs/handoff/`.
- No runtime artifact or data output format changed.

---

## 3. Files Touched

- `AGENTS.md`
- `docs/handoff/2026-03-20_agents_workflow_contract_strengthening.md`

Optional notes per file:

- `AGENTS.md`: strengthened process and delivery rules without changing product logic.
- `docs/handoff/2026-03-20_agents_workflow_contract_strengthening.md`: records rationale, impact, and validation for this governance change.

---

## 4. Behavior Impact

### Expected New Behavior
- Future threads must treat workflow, task, and handoff templates as mandatory project contracts.
- Non-trivial work is now explicitly expected to have an active task definition and template-aligned handoff coverage.

### Preserved Behavior
- Existing Warden engineering constraints on schema, labels, stage boundaries, and module ownership remain in force.
- Backward-compatibility-first execution remains the default expectation.

### User-facing / CLI Impact
- none

### Output Format Impact
- No runtime output format changed.
- Project-process expectations for future engineering responses are stricter.

---

## 5. Schema / Interface Impact

- Schema changed: NO
- Backward compatible: YES
- Public interface changed: NO
- Existing CLI still valid: YES

Affected schema fields / interfaces:

- `AGENTS.md` process contract
- engineering-task delivery expectations

Compatibility notes:

This change affects project workflow expectations, not runtime schemas or public APIs.
Downstream risk is procedural: future threads that ignore task or handoff requirements will now be non-compliant with the root project rules.

---

## 6. Validation Performed

List what was actually checked.

### Commands Run

```bash
Get-Content -Path 'E:\Warden\AGENTS.md' -TotalCount 320
Get-Content -Path 'E:\Warden\AGENTS.md' | Select-Object -Skip 320 -First 220
```

Additional checks performed:

- Verified that `AGENTS.md` now explicitly references `GPT_CODEX_WORKFLOW.md`, `TASK_TEMPLATE.md`, and `HANDOFF_TEMPLATE.md`.
- Verified that the updated `AGENTS.md` includes source-of-truth priority, non-trivial-task gating, mandatory task rules, mandatory handoff rules, and cross-thread continuity rules.

---

## 7. Risks / Caveats

- The stronger `AGENTS.md` raises process strictness; future ad-hoc threads may need explicit task framing more often.
- `HANDOFF_TEMPLATE.md` in the repo appears truncated, so future refinement of the template itself may still be needed.

---

## 8. Recommended Next Step

Normalize the repository templates next:

- expand `docs/templates/HANDOFF_TEMPLATE.md` into a complete template file if the current version is incomplete
- add one canonical example task doc under `docs/tasks/`
- add one canonical example handoff under `docs/handoff/`
