#!/usr/bin/env python3
"""Smoke tests for the installable PEGO CLI package surface."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env["PEGO_FRAMEWORK_ROOT"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "usepego.cli", "--help"],
        cwd=ROOT,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if "pegoctl" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "apply-context" not in completed.stdout:
        raise AssertionError(completed.stdout)

    print("package CLI smoke tests passed.")


if __name__ == "__main__":
    main()
