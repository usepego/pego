#!/usr/bin/env python3
"""Smoke tests for session-review context promotion."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import promote_session_review


REVIEW = {
    "artifact_type": "session_review",
    "schema_version": 1,
    "date": "2026-06-23",
    "source_session": "session.json",
    "event_count": 2,
    "completed_count": 1,
    "blocked_or_partial_count": 1,
    "completed_directives": [],
    "blockers": [],
    "governance_notes": [],
    "learning_decision": "resynthesize_with_blockers",
    "context_update_candidates": [
        {
            "source": "Outcome",
            "update_class": "Pattern",
            "evidence_strength": "Directive outcome",
            "stability": "Provisional",
            "proposed_update": "Directive blocker observed: missing input.",
            "affected_agents": "Operations",
            "action": "Record only",
        }
    ],
    "next_day_inputs": ["Move blocked directives to blocked/deferred."],
    "next_review": "Next daily planning cycle.",
}


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        review = root / "session-review.json"
        output_dir = root / "updates"
        summary = root / "summary.json"
        review.write_text(json.dumps(REVIEW))

        result = promote_session_review.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--review",
                str(review),
                "--output-dir",
                str(output_dir),
                "--summary-output",
                str(summary),
                "--force",
            ]
        )

        if result["promoted_count"] != 1:
            raise AssertionError(result)
        data = json.loads(summary.read_text())
        if data["artifact_type"] != "session_context_promotion":
            raise AssertionError(data)
        outputs = list(output_dir.glob("*.md"))
        if len(outputs) != 1:
            raise AssertionError(outputs)
        text = outputs[0].read_text()
        if "Directive blocker observed" not in text:
            raise AssertionError(text)

    print("session-review context promotion smoke tests passed.")


if __name__ == "__main__":
    main()
