#!/usr/bin/env python3
"""Smoke tests for context commands against an external private root."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import apply_context_updates
import promote_session_review


def write_session_review(private_root: Path) -> Path:
    review = {
        "artifact_type": "session_review",
        "schema_version": 1,
        "date": "2026-06-23",
        "source_session": "2026-06-23-user-mode",
        "context_update_candidates": [
            {
                "title": "Lunch preference",
                "source": "Direct statement",
                "update_class": "Preference",
                "evidence_strength": "Direct statement",
                "stability": "Stable",
                "proposed_update": "The human prefers low-friction lunches during work blocks.",
                "affected_agents": "Health, Operations",
                "action": "Update destination",
            }
        ],
    }
    path = private_root / "reviews" / "sessions" / "2026-06-23-session-review.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(review, indent=2) + "\n")
    return path


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        write_session_review(private_root)

        summary = promote_session_review.main_with_args(
            [
                "--private-root",
                str(private_root),
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if summary["promoted_count"] != 1:
            raise AssertionError(summary)
        update_paths = sorted((private_root / "context" / "updates").glob("*.md"))
        if len(update_paths) != 1:
            raise AssertionError(update_paths)

        review = apply_context_updates.main_with_args(
            [
                "--private-root",
                str(private_root),
                "--date",
                "2026-06-23",
                "--default-destinations",
                "--apply",
                "--force",
            ]
        )
        if review["applied_count"] != 1:
            raise AssertionError(review)
        destination = private_root / "person" / "preferences.md"
        if "low-friction lunches" not in destination.read_text():
            raise AssertionError(destination)
        if not (
            private_root / "context" / "application-reviews" / "2026-06-23-memory-application.json"
        ).exists():
            raise AssertionError("expected memory application review under external private root")

    print("external private-root context smoke tests passed.")


if __name__ == "__main__":
    main()
