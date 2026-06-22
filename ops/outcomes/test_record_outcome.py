#!/usr/bin/env python3
"""Smoke tests for the PEGO outcome recorder."""

from __future__ import annotations

import tempfile
from pathlib import Path

import record_outcome


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        output = root / "outcome.md"
        session = root / "session.md"
        record_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
                "--directive",
                "Breakfast Anchor",
                "--completion",
                "completed",
                "--what-happened",
                "Synthetic outcome.",
                "--evidence",
                "Synthetic report.",
                "--output",
                str(output),
                "--append-session",
                "--session-log",
                str(session),
            ]
        )
        text = output.read_text()
        if "Breakfast Anchor" not in text or "Completed" not in text:
            raise AssertionError(text)
        session_text = session.read_text()
        if "Outcome recorded" not in session_text:
            raise AssertionError(session_text)

    print("outcome recorder smoke tests passed.")


if __name__ == "__main__":
    main()
