#!/usr/bin/env python3
"""Resolve PEGO protected private instance roots."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIVATE_ROOT = ROOT / "private"
ENV_PRIVATE_ROOT = "PEGO_PRIVATE_ROOT"


def resolve_private_root(value: str | Path | None = None) -> Path:
    """Return the configured private root without creating it."""
    if value:
        return Path(value).expanduser()
    configured = os.environ.get(ENV_PRIVATE_ROOT)
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_PRIVATE_ROOT


def display_private_root(path: Path, reveal_path: bool = False) -> str:
    resolved = path.expanduser().resolve()
    if reveal_path:
        return str(resolved)
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return "external_private_root"
    return "private/"


def framework_relative_private_path(private_root: Path, relative: str) -> str:
    """Return a non-sensitive display path for a private-root relative file."""
    prefix = display_private_root(private_root, reveal_path=False).rstrip("/")
    return f"{prefix}/{relative}".replace("//", "/")
