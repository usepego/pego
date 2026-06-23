#!/usr/bin/env python3
"""Smoke tests for bootstrapping an explicit protected private root."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PEGOCTL = ROOT / "pegoctl"


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        completed = subprocess.run(
            [
                sys.executable,
                str(PEGOCTL),
                "bootstrap",
                "--private-root",
                str(private_root),
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "external_private_root/active-operating-brief.md" not in completed.stdout:
            raise AssertionError(completed.stdout)
        for relative in [
            "active-operating-brief.md",
            "constitution/constitution.md",
            "operator/operating-register.md",
            "_local/finance",
        ]:
            if not (private_root / relative).exists():
                raise AssertionError(f"missing bootstrapped path: {relative}")

    print("private bootstrap smoke tests passed.")


if __name__ == "__main__":
    main()
