#!/usr/bin/env python3
"""Smoke tests for PEGO session closeout."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import close_session


SESSION = {
    "artifact_type": "intra_day_session_log",
    "schema_version": 1,
    "date": "2026-06-23",
    "active_queue": "queue.md",
    "operating_frame": "USER mode",
    "events": [
        {"time": "09:00", "human_input": "Done.", "state_update": {}},
        {"time": "10:00", "human_input": "Blocked.", "state_update": {}},
    ],
    "completed_directives": [
        {
            "time": "09:00",
            "directive": "Breakfast Anchor",
            "evidence": "reported by human",
            "notes": "completed",
        }
    ],
    "blocked_or_partial_directives": [
        {
            "time": "10:00",
            "directive": "Venture Problem Map",
            "status": "blocked",
            "reason": "missing input",
            "next_handling": "ask targeted question",
        }
    ],
    "queue_adjustments": [],
    "deferrals": [],
    "governance_notes": [],
    "end_of_day_transfer": [],
}


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        session = root / "session.json"
        output = root / "review.md"
        json_output = root / "review.json"
        session.write_text(json.dumps(SESSION))

        result = close_session.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--session-json",
                str(session),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        if result["learning_decision"] != "resynthesize_with_blockers":
            raise AssertionError(result)
        data = json.loads(json_output.read_text())
        if data["artifact_type"] != "session_review":
            raise AssertionError(data)
        if data["completed_count"] != 1 or data["blocked_or_partial_count"] != 1:
            raise AssertionError(data)
        if not data["context_update_candidates"]:
            raise AssertionError(data)
        if "missing input" not in output.read_text():
            raise AssertionError(output.read_text())

    print("session closeout smoke tests passed.")


if __name__ == "__main__":
    main()
