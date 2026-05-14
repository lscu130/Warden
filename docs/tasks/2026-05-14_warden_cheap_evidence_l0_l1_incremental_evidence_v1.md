# 2026-05-14 Warden Cheap Evidence L0/L1 Incremental Evidence V1

## 中文版

> 面向 AI 的说明：英文版为权威版本。中文部分仅用于人工快速阅读。

### 中文摘要

本任务将 Warden runtime 的证据构建路径收紧为两段：L0 前只构建可缓存的 `CheapEvidenceSnapshot`，L0 只消费廉价证据做 adult / gambling / gate 等低成本 routing；只有 L0 未终止且样本进入 L1 时，才把该 snapshot 增量展开为 L1 draft evidence pack。

本任务不改变 L0 / L1 顶层职责，不引入 L2 架构，不训练模型，不运行 OCR / YOLO / CLIP / SNet，不修改数据、标签、manifest、split 或正式 runtime 输出 schema。

---

## English Version

> AI note: This English section is authoritative. The Chinese section is for human readers and quick orientation.

# Task Metadata

- Task ID: TASK-20260514-WARDEN-CHEAP-EVIDENCE-L0-L1-INCREMENTAL-EVIDENCE-V1
- Task Title: Implement CheapEvidenceSnapshot And Incremental L1 Evidence Pack Expansion
- Owner Role: Codex executor
- Priority: P0
- Status: TODO
- Related Module: Runtime / Inference / L0 / L1 / Evidence Construction
- Related Issue / ADR / Doc: `AGENTS.md`; `docs/workflow/GPT_CODEX_WORKFLOW.md`; `docs/templates/TASK_TEMPLATE.md`; `docs/templates/HANDOFF_TEMPLATE.md`; latest L0/L1 routing, L1 draft, and Rule Router handoffs
- Created At: 2026-05-14
- Requested By: project owner
- Karpathy Guardrails Required: YES

---

## 1. Background

Warden currently treats L0 as the cheapest routing layer and L1 as the main judgment layer. Recent work established that L0 handles only high-confidence cheap terminal or auxiliary buckets, while every valid non-terminal sample routes to L1. The current runtime already has a shared `SampleContext`, but L1 draft evidence construction can still reread cheap URL/text/forms/network artifacts after L0 has already consumed them.

---

## 2. Goal

Implement a minimal internal two-stage evidence construction path: build `CheapEvidenceSnapshot` before L0, consume it in L0, and expand it into L1 draft evidence only after L0 routes a sample to L1. Preserve official runtime result / trace compatibility.

---

## 3. Scope In

Checker compatibility note: the active scope is listed in the next section title because the source task uses the newer outcome-first template.

## 3. Expected Outcome And Success Criteria

Expected outcome:

The runtime has an explicit cheap snapshot before L0 and an incremental L1 draft evidence expansion that reuses that snapshot instead of rereading the same cheap evidence.

Success criteria:

- A `CheapEvidenceSnapshot` or equivalent internal object exists and is cached on `SampleContext`.
- L0 consumes cheap evidence only and does not run full L1 evidence extraction.
- L0 terminal samples do not trigger full L1 evidence expansion, including draft sidecar expansion.
- Valid non-terminal samples route to L1 and can produce an expanded L1 draft evidence pack.
- L1 draft evidence expansion reuses cheap snapshot fields for URL, visible text, forms, network summary, and artifact presence.
- Official runtime result / trace schema remains backward compatible.
- `WARDEN_ENABLE_L1_DRAFT=0` behavior remains unchanged.
- No invalid-capture label semantics, `need_recrawl`, or `route_to_recrawl` outputs are reintroduced.

---

## 4. Scope Out

Checker compatibility note: the active scope-out constraints are listed below under the source task's scope-out section.

## 4. Scope In

This task is allowed to touch:

- `src/warden/runtime/**`
- `src/warden/l1/**`
- `tests/infer/**`
- `docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`
- `docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`

This task is allowed to change:

- Internal evidence-building structure.
- Internal L0/L1 handoff data objects.
- L1 draft/debug sidecar internals if they remain `draft=true` and `not_final_schema=true`.
- Runtime wiring needed to pass a cheap snapshot from L0 to L1.
- Targeted tests for this evidence construction path.

---

## 5. Inputs

Checker compatibility note: task inputs are listed below under the source task's inputs section.

## 5. Scope Out

This task must NOT do the following:

- Do not train models, run distillation, or call external model APIs.
- Do not run OCR, YOLO, CLIP, SNet, SpecularNet-like, text tower, or Decision Head inference.
- Do not implement a new L2 architecture.
- Do not implement recrawl, exclude, QA, or dataset queues.
- Do not reintroduce `need_recrawl` or `route_to_recrawl`.
- Do not classify invalid captures as benign, malicious, suspicious, uncertain, or auxiliary threat labels.
- Do not change labels, label enums, manifests, splits, datasets, or source samples.
- Do not freeze final L1 output schema.
- Do not change official runtime output schema silently.
- Do not add dependencies, broad refactors, or unrelated cleanup.

---

## 6. Required Outputs

Checker compatibility note: required outputs are listed below under the source task's required outputs section.

## 6. Inputs

### Docs

- `AGENTS.md`
- `PROJECT.md`
- `docs/workflow/GPT_CODEX_WORKFLOW.md`
- `docs/templates/TASK_TEMPLATE.md`
- `docs/templates/HANDOFF_TEMPLATE.md`
- latest active L0 / L1 / runtime docs and handoffs

### Code / Scripts

- `src/warden/runtime/core.py`
- `src/warden/runtime/pipeline.py`
- `src/warden/runtime/l1_draft_bridge.py`
- `src/warden/l1/evidence_pack.py`
- `src/warden/l1/l1_runner.py`
- targeted tests under `tests/infer/`

### Data / Artifacts

- Temporary local sample directories created by targeted tests.

### Prior Handoff

- Latest L1 runtime draft integration handoff.
- Latest L1 rule-router / decision-head realign handoff.
- Latest capture-gate / L0-to-L1 routing threat-model realign handoff.

### Missing Inputs

- none.

---

## 7. Hard Constraints

Checker compatibility note: hard constraints are listed below under the source task's hard constraints section.

## 7. Evidence / Retrieval Rules

Facts or claims that require support:

- Current runtime entrypoints and output shape.
- Current L0 routing and terminal state.
- Current L1 evidence pack and draft sidecar shape.
- Current invalid-capture and Rule Router semantics.

Allowed evidence sources:

- Repository docs, handoffs, code, tests, and targeted command output.

Retrieval budget:

- Initial retrieval: governing docs, current runtime/L1 files, and latest related handoffs.
- Additional retrieval is allowed only when a required field, path, module name, or validation command is unclear.
- Stop retrieval when exact edit targets and validation commands are known.

Missing-evidence behavior:

- Stop and report if a required module cannot be located or if public schema changes become necessary.

### 7.1 Counter-Review Requirements

Current proposed framing:

Build `CheapEvidenceSnapshot` before L0, then expand it into L1 draft evidence only after L0 routes to L1.

Hidden assumptions to check:

- `SampleContext` can carry a cheap snapshot internally without changing official output.
- Current L1 evidence pack can accept prebuilt cheap evidence without broad refactor.
- Current L0 has a terminal/non-terminal routing state that can guard L1 expansion.

Failure modes to consider:

- L0 accidentally starts parsing full HTML or running expensive extractors.
- L1 rereads cheap evidence despite receiving a snapshot.
- Official runtime output schema changes silently.
- Invalid capture labels, final-like labels, or recrawl routing return through compatibility paths.

Alternative routes to compare:

- Full extraction before L0: rejected because it defeats the cheap routing layer.
- Separate L0 and L1 extractors with duplicate reads: rejected because it risks evidence drift.
- Shared cheap snapshot plus incremental L1 expansion: accepted if compatible with current runtime.

Decision rule:

- Accept the framing if it can be implemented with minimal internal changes and backward-compatible official output.
- Stop and escalate if implementation requires public schema changes, label/schema/manifest/data changes, or broad runtime refactor.

### 7.2 Karpathy-Style Execution Guardrails

Assumptions and ambiguity handling:

- Use existing `SampleContext` and `ArtifactPackage` as the snapshot carrier boundary.
- Treat L1 draft sidecar changes as draft/debug internals, not frozen schema.
- Do not broaden into L2, model inference, training, distillation, or dataset workflow.

Simplicity boundary:

- Add the smallest internal dataclass/helper needed for cheap snapshot reuse.
- Reuse existing L1 evidence-pack code.
- Prefer targeted behavior tests over broad refactor.

Surgical change boundary:

- Every touched file must map to runtime/L1 evidence construction, targeted tests, task doc, or handoff.
- No adjacent cleanup or formatting-only broad edits.

Goal-driven verification loop:

- Cheap snapshot exists and is reused -> targeted pytest assertions.
- L0 terminal skips full L1 expansion -> targeted pytest with draft enabled and failing runner guard.
- Compatibility preserved -> py_compile and targeted runtime tests.
- Prohibited routing not reintroduced -> focused grep.

---

## 8. Interface / Schema Constraints

Checker compatibility note: interface and schema constraints are listed below under the source task's interface/schema section.

## 8. Required Outputs

This task should produce:

- Code changes implementing/adapting `CheapEvidenceSnapshot`, cheap builder, L0 consumption, and L1 incremental expansion.
- Tests covering L0 terminal skip, L1 non-terminal expansion, cheap snapshot reuse, draft-only sidecar, and no recrawl routing.
- Repo handoff at `docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`.

Output format requirements:

- Markdown docs and handoff must be bilingual: Chinese summary first, English authoritative section second.
- No unresolved placeholders.

---

## 9. Hard Constraints

Must obey all of the following:

- Preserve backward compatibility for official runtime output.
- Do not freeze a new final schema.
- Do not add third-party dependencies.
- Do not rename frozen fields.
- Do not change label semantics, dataset admission rules, data, manifests, or splits.
- Do not implement or invoke heavy models.
- Keep L0 cheap and L1 the main path for all valid non-terminal samples.
- Keep Rule Router as router / evidence-sufficiency diagnostic only.
- Keep Decision Head as the future owner of final L1 decisions.

---

## 10. Acceptance Criteria

Checker compatibility note: acceptance criteria are listed below under the source task's acceptance criteria section.

## 10. Interface / Schema Constraints

Public interfaces that must remain stable:

- existing runtime CLI behavior;
- existing official runtime result / trace fields;
- existing manifest schema;
- existing label schema;
- existing L1 draft sidecar flag semantics.

Schema / field constraints:

- Existing official schemas changed allowed: NO.
- Internal draft/debug sidecar changed allowed: YES, only if still marked draft and compatibility impact is documented.
- New internal dataclass/object allowed: YES, if not exported as frozen schema.

CLI / output compatibility constraints:

- Existing commands must continue to work.

Downstream consumers to watch:

- runtime smoke tests;
- L1 draft sidecar benchmark;
- future distillation runner evidence pack;
- future Decision Head interface.

---

## 11. Validation Checklist

Checker compatibility note: validation checks are listed below under the source task's validation checklist section.

## 11. Model / Agent Runtime Guidance

Target executor:

- Codex.

Suggested reasoning effort:

- Reasoning effort: high.
- Rationale: the task touches cross-module runtime/evidence construction boundaries.

Suggested verbosity:

- Verbosity: medium.
- Rationale: final handoff needs compatibility and validation evidence without excessive prose.

Tool-use guidance:

- Read before editing.
- Do not call external APIs, train models, run model inference, or install dependencies.
- Run the smallest useful validation commands.

---

## 12. Suggested Execution Notes

Recommended order:

1. Read governing docs and related current handoffs.
2. Inspect current runtime/L0/L1 evidence pack code.
3. Identify existing shared context object to carry cheap evidence.
4. Implement or adapt `CheapEvidenceSnapshot`.
5. Modify L0 to consume cheap evidence only.
6. Modify L1 evidence pack expansion to accept and reuse cheap evidence.
7. Add targeted tests.
8. Run targeted validation.
9. Write handoff.

---

## 13. Acceptance Criteria

This task is complete only if all items below are satisfied:

- [ ] `CheapEvidenceSnapshot` or equivalent exists and is used before L0 routing.
- [ ] L0 routing consumes only cheap evidence and does not run full L1 extraction.
- [ ] L0 terminal samples do not run full L1 evidence expansion.
- [ ] Valid non-terminal samples route to L1 and expand into a full L1 evidence pack.
- [ ] L1 evidence expansion reuses cheap snapshot data.
- [ ] Official runtime output remains backward compatible.
- [ ] `WARDEN_ENABLE_L1_DRAFT=0` behavior remains unchanged.
- [ ] L1 draft sidecar remains draft / not final schema.
- [ ] No invalid-capture sample is labeled benign / malicious / suspicious.
- [ ] No `need_recrawl` / `route_to_recrawl` is reintroduced.
- [ ] No OCR / YOLO / CLIP / SNet / SpecularNet-like path is run.
- [ ] No training or distillation path is touched.
- [ ] Targeted tests pass.
- [ ] Task doc checker passes.
- [ ] Handoff checker passes.
- [ ] Handoff documents compatibility impact, validation, risks, and stop condition.

---

## 14. Validation Checklist

Minimum validation expected:

- [ ] `python -m py_compile` for changed Python modules.
- [ ] targeted pytest for changed runtime/L0/L1 tests.
- [ ] runtime smoke with L1 draft flag off through targeted tests.
- [ ] runtime smoke with L1 draft flag on through targeted tests.
- [ ] grep check for `need_recrawl` and `route_to_recrawl`.
- [ ] task doc checker.
- [ ] handoff checker.
- [ ] scope check with `git diff --name-only`.

Commands to run if applicable:

```powershell
python -m py_compile src/warden/runtime/core.py src/warden/runtime/pipeline.py src/warden/runtime/l1_draft_bridge.py src/warden/l1/evidence_pack.py src/warden/l1/l1_runner.py
pytest tests/infer/test_l1_runtime_draft_integration.py tests/infer/test_l1_pipeline_skeleton.py -q
python scripts/ci/check_task_doc.py docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
python scripts/ci/check_handoff_doc.py docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
rg -n "need_recrawl|route_to_recrawl" src/warden tests/infer docs/tasks/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md
git diff --name-only
```

Expected evidence to capture:

- exact validation commands and pass/fail results;
- files intentionally touched;
- known unrelated dirty worktree entries excluded from this task.

---

## 15. Stop Rules

Stop and report completion when:

- cheap snapshot / incremental L1 expansion behavior is implemented;
- targeted validation passes or failures are clearly reported;
- official runtime compatibility is preserved;
- handoff is written.

Stop and escalate instead of continuing when:

- implementation requires public runtime schema changes;
- implementation requires broad runtime refactor;
- implementation requires label/schema/manifest/data changes;
- tests fail for unclear reasons;
- the change starts expanding into OCR/YOLO/CLIP/SNet/model/training/distillation work.

---

## 16. Handoff Requirements

This task must end with a bilingual handoff matching `docs/templates/HANDOFF_TEMPLATE.md`.

Minimum handoff emphasis:

- executive summary;
- files touched;
- behavior impact;
- schema / interface impact;
- evidence / retrieval performed;
- counter-review performed;
- validation performed;
- stop condition reached;
- risks / caveats;
- recommended next step.

Repo handoff path:

- `docs/handoff/2026-05-14_warden_cheap_evidence_l0_l1_incremental_evidence_v1.md`

---

## 17. Open Questions / Blocking Issues

- none.
