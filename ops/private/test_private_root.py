#!/usr/bin/env python3
"""Smoke tests for PEGO private-root resolution."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import private_root


def main() -> None:
    original = os.environ.get(private_root.ENV_PRIVATE_ROOT)
    try:
        os.environ.pop(private_root.ENV_PRIVATE_ROOT, None)
        if private_root.resolve_private_root() != private_root.DEFAULT_PRIVATE_ROOT:
            raise AssertionError("expected default repo private root")

        with tempfile.TemporaryDirectory() as directory:
            external = Path(directory) / "pego-private"
            os.environ[private_root.ENV_PRIVATE_ROOT] = str(external)
            if private_root.resolve_private_root() != external:
                raise AssertionError("expected env-configured private root")
            if private_root.display_private_root(external) != "external_private_root":
                raise AssertionError("expected redacted external private root")
            if not private_root.framework_relative_private_path(external, "README.md").startswith(
                "external_private_root/"
            ):
                raise AssertionError("expected redacted private path")

        explicit = Path("~/pego-test")
        if private_root.resolve_private_root(explicit) != explicit.expanduser():
            raise AssertionError("expected explicit path to override env")
    finally:
        if original is None:
            os.environ.pop(private_root.ENV_PRIVATE_ROOT, None)
        else:
            os.environ[private_root.ENV_PRIVATE_ROOT] = original

    print("private-root smoke tests passed.")


if __name__ == "__main__":
    main()
