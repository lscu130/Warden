"""Warden L1 pipeline skeleton and conservative rule baseline.

This package implements a model-independent L1 draft path. Action surfaces
such as login, payment, wallet, download, support, and redirect are evidence
signals. They may become threat actions only when combined with deceptive
identity, manipulative narrative, suspicious target, abnormal submission, or
business-context conflict.

CLIP / MobileCLIP and SNet / SpecularNet-like routes are kept for offline
experiments or future optional switches. They are not implemented in this
default online L1 skeleton.
"""

from .l1_runner import run_l1_baseline_for_manifest_row, run_l1_baseline_for_sample

__all__ = ["run_l1_baseline_for_manifest_row", "run_l1_baseline_for_sample"]
