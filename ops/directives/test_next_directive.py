#!/usr/bin/env python3
"""Smoke tests for the local PEGO next-directive selector."""

from __future__ import annotations

import tempfile
from pathlib import Path

import next_directive


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 60 min | Medium | Computer | Workday | Level 1 | Ready |
| 3 | Garden Weed Block | Home | 25 min | Medium-low | Outside | Before evening | Level 1 | Conditional |
| 4 | Store List | Health/Ops | 10 min | Low | Phone/computer | Before grocery trip | Level 1 | Optional |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which visible part of the home or yard is most annoying right now? | Selects action | Weekly | Add candidate |
"""


def run_selector(*args: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        output = root / "response.md"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        next_directive.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--output",
                str(output),
                "--force",
                *args,
            ]
        )
        return output.read_text()


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    breakfast = run_selector("--available", "15", "--energy", "low", "--location", "home")
    assert_contains(breakfast, "Breakfast Anchor")

    venture = run_selector(
        "--done",
        "Breakfast Anchor",
        "--available",
        "45",
        "--energy",
        "medium",
        "--location",
        "computer",
    )
    assert_contains(venture, "Reduced Venture Problem Map")

    question = run_selector(
        "--done",
        "Breakfast Anchor",
        "--done",
        "Venture Problem Map",
        "--done",
        "Garden Weed Block",
        "--done",
        "Store List",
        "--available",
        "5",
    )
    assert_contains(question, "Which visible part of the home or yard is most annoying right now?")

    print("next directive smoke tests passed.")


if __name__ == "__main__":
    main()
