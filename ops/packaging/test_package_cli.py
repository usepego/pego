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
    if "daily" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "weekly" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "monthly" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "intake" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "daily-directive" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "finance-run" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "finance-review" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "health-candidates" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "meal" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "home-candidates" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "anticipate" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "attention" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "compliance-review" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "public-writing" not in completed.stdout:
        raise AssertionError(completed.stdout)
    if "--private-root" not in completed.stdout:
        raise AssertionError(completed.stdout)

    print("package CLI smoke tests passed.")


if __name__ == "__main__":
    main()
