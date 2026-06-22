#!/usr/bin/env python3
"""Smoke tests for PEGO weekly cycle runner."""

from __future__ import annotations

import tempfile
from pathlib import Path

import weekly_cycle


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which event needs prep? | Lead time | Weekly | Add candidate |
| Which home area is most annoying? | Environment | Weekly | Add candidate |
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        weekly_cycle.PRIVATE = private
        register = private / "operator" / "operating-register.md"
        output = private / "directives" / "weekly" / "test.md"
        register.parent.mkdir(parents=True)
        register.write_text(REGISTER)

        weekly_cycle.main_with_args(
            [
                "--week",
                "2026-W26",
                "--register",
                str(register),
                "--output",
                str(output),
            ]
        )
        text = output.read_text()
        if "Which event needs prep?" not in text:
            raise AssertionError(text)
        if "Authority level: Level 1, Recommend" not in text:
            raise AssertionError(text)

    print("weekly cycle smoke tests passed.")


if __name__ == "__main__":
    main()
