#!/usr/bin/env python3
"""Smoke tests for PEGO USER-mode check-in runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import user_check_in


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 45 min | Medium | Computer | Workday | Level 1 | Ready |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which appointment requires preparation? | Prevents scrambling | Daily | Add candidate |
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        session = root / "session.md"
        session_json = root / "session.json"
        response = root / "response.md"
        response_json = root / "response.json"
        preflight = root / "preflight.json"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        first = user_check_in.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
                "--input",
                "Breakfast is done. What is next?",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--session-output",
                str(session),
                "--session-json-output",
                str(session_json),
                "--response-output",
                str(response),
                "--response-json-output",
                str(response_json),
                "--preflight-output",
                str(preflight),
                "--force",
            ]
        )

        if first["preflight_outcome"] != "pass":
            raise AssertionError(first)
        if not session.exists() or not session_json.exists():
            raise AssertionError("expected session outputs")
        if not response_json.exists():
            raise AssertionError("expected structured command response")

        data = json.loads(session_json.read_text())
        if data["artifact_type"] != "intra_day_session_log":
            raise AssertionError(data)
        if len(data["events"]) != 1:
            raise AssertionError(data)
        if data["completed_directives"][0]["directive"] != "Breakfast Anchor":
            raise AssertionError(data)

        second = user_check_in.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--time",
                "09:45",
                "--input",
                "The venture block is blocked by missing input.",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--blocked",
                "missing input",
                "--available",
                "15",
                "--energy",
                "low",
                "--location",
                "home",
                "--session-output",
                str(session),
                "--session-json-output",
                str(session_json),
                "--response-output",
                str(root / "response-2.md"),
                "--response-json-output",
                str(root / "response-2.json"),
                "--preflight-output",
                str(root / "preflight-2.json"),
                "--force",
            ]
        )

        if second["events"] != 2:
            raise AssertionError(second)
        data = json.loads(session_json.read_text())
        if len(data["blocked_or_partial_directives"]) != 1:
            raise AssertionError(data)

    print("operator user check-in smoke tests passed.")


if __name__ == "__main__":
    main()
