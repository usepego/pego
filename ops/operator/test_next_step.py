#!/usr/bin/env python3
"""Smoke tests for the PEGO operator next-step runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import next_step


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
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        summary = next_step.main_with_args(
            [
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

        if not response.exists() or not preflight.exists():
            raise AssertionError("expected response and preflight files")
        if summary["preflight_outcome"] != "pass":
            raise AssertionError(summary)
        data = json.loads(preflight.read_text())
        if data["outcome"] != "pass":
            raise AssertionError(data)

    print("operator next-step smoke tests passed.")


if __name__ == "__main__":
    main()
