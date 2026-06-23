#!/usr/bin/env python3
"""Smoke tests for PEGO operating brief generation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_brief


QUEUE = """# Directive Queue: test

## Protected Time

Evening block is protected.

## Current State

- Time: morning
- Location: home
- Energy: medium

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 45 min | Medium | Computer | Workday | Level 1 | Ready |
"""


SESSION = {
    "artifact_type": "intra_day_session_log",
    "schema_version": 1,
    "date": "2026-06-23",
    "active_queue": "queue.md",
    "operating_frame": "USER mode",
    "events": [{"time": "09:00"}],
    "completed_directives": [],
    "blocked_or_partial_directives": [],
    "queue_adjustments": [],
    "deferrals": [],
    "governance_notes": [],
    "end_of_day_transfer": [],
}


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        session = root / "session.json"
        output = root / "brief.md"
        json_output = root / "brief.json"
        queue.write_text(QUEUE)
        session.write_text(json.dumps(SESSION))

        result = generate_brief.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--session-json",
                str(session),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        if result["active_candidates"] != 2:
            raise AssertionError(result)
        if not result["has_first_directive"]:
            raise AssertionError(result)
        data = json.loads(json_output.read_text())
        if data["artifact_type"] != "operating_brief":
            raise AssertionError(data)
        if data["first_directive"]["candidate"] != "Breakfast Anchor":
            raise AssertionError(data)
        if data["session_events"] != 1:
            raise AssertionError(data)
        if "Evening block" not in output.read_text():
            raise AssertionError(output.read_text())

    print("operating brief smoke tests passed.")


if __name__ == "__main__":
    main()
