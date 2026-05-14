"""Feature-flagged L1 draft bridge for runtime debug sidecars."""

from __future__ import annotations

import os
import inspect
import time
from pathlib import Path
from typing import Any, Callable, Dict, Mapping

from warden.l1 import run_l1_baseline_for_sample

from .core import SampleContext

L1_DRAFT_ENV_VAR = "WARDEN_ENABLE_L1_DRAFT"
_TRUE_VALUES = {"1", "true", "yes", "on"}


def l1_draft_enabled(env: Mapping[str, str] | None = None) -> bool:
    """Return whether the runtime should attach an L1 draft sidecar."""

    source = os.environ if env is None else env
    return str(source.get(L1_DRAFT_ENV_VAR, "")).strip().lower() in _TRUE_VALUES


def make_l1_draft_skipped_trace() -> Dict[str, Any]:
    return {
        "stage": "l1_draft",
        "enabled": False,
        "draft": True,
        "not_final_schema": True,
        "status": "skipped",
        "result": {},
        "error": None,
        "duration_ms": 0.0,
    }


def run_l1_draft_bridge(
    context: SampleContext,
    *,
    runner: Callable[..., Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    """Run L1 draft on a sample path and convert failures into trace data.

    The bridge passes only the sample directory to the L1 runner. Runtime labels,
    split metadata, and folder-derived triage hints are not injected into the
    evidence input.
    """

    started = time.perf_counter()
    trace: Dict[str, Any] = {
        "stage": "l1_draft",
        "enabled": True,
        "draft": True,
        "not_final_schema": True,
        "status": "ok",
        "result": {},
        "error": None,
        "duration_ms": 0.0,
    }
    try:
        active_runner = run_l1_baseline_for_sample if runner is None else runner
        cheap_snapshot = context.cheap_snapshot.to_dict() if context.cheap_snapshot is not None else None
        signature = inspect.signature(active_runner)
        accepts_snapshot = "cheap_snapshot" in signature.parameters or any(
            parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in signature.parameters.values()
        )
        if accepts_snapshot:
            trace["result"] = active_runner(context.artifacts.sample_dir, cheap_snapshot=cheap_snapshot)
        else:
            trace["result"] = active_runner(context.artifacts.sample_dir)
    except Exception as exc:  # pragma: no cover - exception type is intentionally broad for runtime safety.
        trace["status"] = "error"
        trace["result"] = {}
        trace["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
    finally:
        trace["duration_ms"] = round((time.perf_counter() - started) * 1000.0, 3)
    return trace


def maybe_attach_l1_draft_trace(context: SampleContext) -> Dict[str, Any] | None:
    if not l1_draft_enabled():
        return None
    trace = run_l1_draft_bridge(context)
    context.terminal_outputs["l1_draft"] = trace
    return trace
