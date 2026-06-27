#!/usr/bin/env python3
"""Smoke tests for governed context update application."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import apply_context_updates


def context_update(destination: Path) -> str:
    return "\n".join(
        [
            "# Context Update: Synthetic Preference",
            "",
            "## Date",
            "",
            "2026-06-23",
            "",
            "## Source",
            "",
            "Conversation",
            "",
            "## Raw Observation",
            "",
            "Synthetic preference stated directly.",
            "",
            "## Update Class",
            "",
            "Preference",
            "",
            "## Evidence Strength",
            "",
            "Direct statement",
            "",
            "## Stability",
            "",
            "Stable",
            "",
            "## Destination File",
            "",
            str(destination),
            "",
            "## Proposed Update",
            "",
            "Synthetic preference should be remembered.",
            "",
            "## Affected Agents",
            "",
            "Operations",
            "",
            "## Governance Impact",
            "",
            "None recorded.",
            "",
            "## Action",
            "",
            "Update destination",
            "",
            "## Review Date",
            "",
            "Next weekly review.",
            "",
        ]
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private_root = root / "private"
        update = root / "update.md"
        destination = private_root / "person" / "preferences.md"
        output = root / "review.md"
        json_output = root / "review.json"
        update.write_text(context_update(destination))

        review_only = apply_context_updates.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--private-root",
                str(private_root),
                "--update",
                str(update),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )
        if review_only["eligible_count"] != 1 or review_only["applied_count"] != 0:
            raise AssertionError(review_only)
        if destination.exists():
            raise AssertionError("review-only mode must not write destination")

        applied = apply_context_updates.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--private-root",
                str(private_root),
                "--update",
                str(update),
                "--output",
                str(root / "review-apply.md"),
                "--json-output",
                str(root / "review-apply.json"),
                "--apply",
                "--force",
            ]
        )
        if applied["applied_count"] != 1:
            raise AssertionError(applied)
        if "Synthetic preference should be remembered" not in destination.read_text():
            raise AssertionError(destination.read_text())
        data = json.loads((root / "review-apply.json").read_text())
        if data["artifact_type"] != "memory_application_review":
            raise AssertionError(data)

    print("context application review smoke tests passed.")


if __name__ == "__main__":
    main()
