#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
from pathlib import Path


def get_data_root() -> Path:
    """Return the active Warden runtime data root.

    The default local contract is `E:\\WardenData`, while `WARDEN_DATA_ROOT`
    remains available as an explicit override for operators who need a
    different local root.
    """

    return Path(os.environ.get("WARDEN_DATA_ROOT", r"E:\WardenData"))


def data_path(*parts: str) -> Path:
    return get_data_root().joinpath(*parts)
