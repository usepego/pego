#!/usr/bin/env python3
"""Smoke tests for the PEGO outcome recorder."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import record_outcome


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        output = root / "outcome.md"
        json_output = root / "outcome.json"
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
                "--outcome-progress",
                "Breakfast default became easier tomorrow.",
                "--contentment-signal",
                "More contentment",
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--append-session",
                "--session-log",
                str(session),
            ]
        )
        text = output.read_text()
        if "Breakfast Anchor" not in text or "Completed" not in text:
            raise AssertionError(text)
        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "directive_outcome":
            raise AssertionError("expected directive_outcome artifact")
        if structured["completion"] != "completed":
            raise AssertionError("expected normalized completion")
        if structured["evidence"] != ["human_report"]:
            raise AssertionError("expected human_report evidence")
        if structured["outcome_progress"] != "Breakfast default became easier tomorrow.":
            raise AssertionError("expected outcome progress evidence")
        if structured["contentment_signal"] != "More contentment":
            raise AssertionError("expected contentment signal")
        session_text = session.read_text()
        if "Outcome recorded" not in session_text:
            raise AssertionError(session_text)

    print("outcome recorder smoke tests passed.")


if __name__ == "__main__":
    main()
