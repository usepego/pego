#!/usr/bin/env python3
"""Smoke tests for PEGO anticipation scan generator."""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_scan


REGISTER = """# Operating Register

## Upcoming Events

| Event | Date or Window | Prep Needed | Lead Time | Owner Agent | Status |
| --- | --- | --- | --- | --- | --- |
| Dinner event | Friday | Decide outfit | 3 days | Relationships | Open |

## Home and Environment Watchlist

| Area | Condition | Smallest Useful Action | Weather / Tool Dependency | Next Review |
| --- | --- | --- | --- | --- |
| Front garden | Weeds visible | Weed 20 minutes | Dry weather | This week |

## Strategic Dependencies

| Goal or Program | Dependency | Blocking Risk | Next Evidence Action | Review Date |
| --- | --- | --- | --- | --- |
| Venture income | Customer problem map | No business thesis | Draft 10 problem hypotheses | Friday |
"""


def run_scan(*args: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        register = root / "register.md"
        output = root / "scan.md"
        register.write_text(REGISTER)

        generate_scan.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--horizon",
                "14 days",
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
    event_scan = run_scan("--domain", "Event")
    assert_contains(event_scan, "Dinner event")
    assert_contains(event_scan, "Decide outfit")

    environment_scan = run_scan("--domain", "Environment")
    assert_contains(environment_scan, "Front garden")
    assert_contains(environment_scan, "Weed 20 minutes")

    strategy_scan = run_scan("--domain", "Strategy")
    assert_contains(strategy_scan, "Customer problem map")
    assert_contains(strategy_scan, "Draft 10 problem hypotheses")

    print("anticipation scan smoke tests passed.")


if __name__ == "__main__":
    main()
