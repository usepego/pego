#!/usr/bin/env python3
"""Smoke tests for PEGO daily cycle runner."""

from __future__ import annotations

import tempfile
from pathlib import Path

import daily_cycle


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 60 min | Medium | Computer | Workday | Level 1 | Ready |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which missing supply would block tomorrow? | Prevents scramble | Daily | Add candidate |
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        response = root / "response.md"
        preflight = root / "preflight.json"
        outcome = root / "outcome.md"
        context = root / "context.md"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        daily_cycle.main_with_args(
            [
                "next",
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--response-output",
                str(response),
                "--preflight-output",
                str(preflight),
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "outcome",
                "--date",
                "2026-06-23",
                "--directive",
                "Reduced Venture Problem Map",
                "--completion",
                "completed",
                "--what-happened",
                "Synthetic outcome.",
                "--output",
                str(outcome),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "learn",
                "--date",
                "2026-06-23",
                "--source",
                "Outcome",
                "--raw-observation",
                "Synthetic learning.",
                "--update-class",
                "Pattern",
                "--evidence-strength",
                "Directive outcome",
                "--stability",
                "Current but changeable",
                "--proposed-update",
                "Synthetic update.",
                "--output",
                str(context),
                "--force",
            ]
        )

        for path in (response, preflight, outcome, context):
            if not path.exists():
                raise AssertionError(f"missing expected file: {path}")

    print("daily cycle smoke tests passed.")


if __name__ == "__main__":
    main()
