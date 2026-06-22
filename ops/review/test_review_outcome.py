#!/usr/bin/env python3
"""Smoke tests for PEGO outcome review runner."""

from __future__ import annotations

import tempfile
from pathlib import Path

import review_outcome


COMPLETED = """# Directive Outcome: test

## Directive Summary

Breakfast Anchor

## Completion

Completed

## What Happened

Ate protein breakfast.

## Evidence

Human report.

## Friction

None recorded.

## Benefit

Reduced snacking.

## Cost

None recorded.

## Protected-Time Impact

None
"""


BLOCKED = """# Directive Outcome: test

## Directive Summary

Garden Weed Block

## Completion

Blocked

## What Happened

Could not start.

## Evidence

Human report.

## Friction

Rain and no dry window.

## Benefit

None recorded.

## Cost

None recorded.

## Protected-Time Impact

None
"""


ESCALATE = """# Directive Outcome: test

## Directive Summary

Career Exit Work

## Completion

Completed

## What Happened

Drafted exit plan.

## Evidence

Artifact.

## Friction

None recorded.

## Benefit

Strategic clarity.

## Cost

Stress.

## Protected-Time Impact

High
"""


def run_review(text: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.md"
        output = root / "review.md"
        outcome.write_text(text)
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--output",
                str(output),
                "--force",
            ]
        )
        return output.read_text()


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    completed = run_review(COMPLETED)
    assert_contains(completed, "Repeat")
    assert_contains(completed, "Health")

    blocked = run_review(BLOCKED)
    assert_contains(blocked, "Block pending dependency")
    assert_contains(blocked, "Home and Environment")

    escalated = run_review(ESCALATE)
    assert_contains(escalated, "Escalate")
    assert_contains(escalated, "Needs governance review")

    print("outcome review smoke tests passed.")


if __name__ == "__main__":
    main()
