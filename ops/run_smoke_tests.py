#!/usr/bin/env python3
"""Discover and run PEGO smoke tests.

CI should not need a manually maintained list every time a new reference runner
or contract test is added.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops"


def discover_tests() -> list[Path]:
    return sorted(OPS.rglob("test_*.py"))


def main() -> int:
    tests = discover_tests()
    if not tests:
        print("No smoke tests discovered under ops/", file=sys.stderr)
        return 1

    for test in tests:
        rel = test.relative_to(ROOT)
        print(f"==> {rel}", flush=True)
        result = subprocess.run([sys.executable, str(test)], cwd=ROOT)
        if result.returncode != 0:
            print(f"FAILED: {rel}", file=sys.stderr)
            return result.returncode

    print(f"Ran {len(tests)} smoke test files.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
