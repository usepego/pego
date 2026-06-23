#!/usr/bin/env python3
"""Smoke tests for PEGO daily directive generation."""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_daily_directive


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        (private / "time").mkdir(parents=True)
        (private / "health").mkdir(parents=True)
        (private / "time" / "protected-time.md").write_text("Synthetic protected evening block.")
        (private / "health" / "directives.md").write_text("Synthetic low-friction health directive.")

        result = generate_daily_directive.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-23",
                "--force",
            ]
        )

        expected = private / "directives" / "daily" / "2026-06-23.md"
        if result != expected:
            raise AssertionError(f"expected {expected}, got {result}")
        text = expected.read_text()
        if "Daily Directive: 2026-06-23" not in text:
            raise AssertionError(text)
        if "Follow the local protected-time file" not in text:
            raise AssertionError(text)
        if "Follow the local health directive file" not in text:
            raise AssertionError(text)
        if "Authority level: Level 1" not in text:
            raise AssertionError(text)

    print("daily directive smoke tests passed.")


if __name__ == "__main__":
    main()
