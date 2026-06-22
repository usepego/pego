#!/usr/bin/env python3
"""Smoke tests for PEGO directive queue synthesis."""

from __future__ import annotations

import tempfile
from pathlib import Path

import synthesize_queue


CANDIDATES = """# Candidates

| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Venture Problem Map | Venture | 60 min | Medium | Computer | Today | Level 1 | Draft | Strategic progress | Delays business clarity | None |
| Garden Weed Block | Home and Environment | 20 min | Medium | Outside | Before evening | Level 1 | Draft | Preserves home serenity | Visible friction increases | Low |
| Quit Job Decision | Career | 30 min | High | Computer | This week | Level 4 | Escalated | Income strategy | Opportunity cost | High |
| Breakfast Anchor | Health | 10 min | Low | Home | Morning | Level 1 | Draft | Stabilizes diet | Hunger and snacking | None |
"""


ANTICIPATION_SCAN = """# Anticipation Scan

## Domain

Event

## Candidate Directive

Decide outfit for dinner

## Lead Time

3 days

## Governance Status

Level 1 recommendation unless spending is material.
"""


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        candidate_file = root / "candidates.md"
        scan_file = root / "scan.md"
        output = root / "queue.md"
        candidate_file.write_text(CANDIDATES)
        scan_file.write_text(ANTICIPATION_SCAN)

        synthesize_queue.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--candidate",
                str(candidate_file),
                "--candidate",
                str(scan_file),
                "--available",
                "30",
                "--output",
                str(output),
                "--force",
            ]
        )

        text = output.read_text()
        assert_contains(text, "Breakfast Anchor")
        assert_contains(text, "Garden Weed Block")
        assert_contains(text, "Decide outfit for dinner")
        assert_contains(text, "Venture Problem Map | Does not fit available window")
        assert_contains(text, "Quit Job Decision | Needs governance review")

    print("directive synthesis smoke tests passed.")


if __name__ == "__main__":
    main()
