#!/usr/bin/env python3
"""Smoke tests for PEGO home/environment candidate generation."""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_candidates


REGISTER = """# Operating Register

## Recurring Annoyances

| Annoyance | Domain | Trigger | Smallest Preventive Action | Review Cadence | Status |
| --- | --- | --- | --- | --- | --- |
| Mudroom clutter | Home | Shoes pile up | Reset mudroom shelf | Weekly | Open |

## Supply Gaps

| Supply | Domain | Needed For | Consequence if Missing | Next Action | Status |
| --- | --- | --- | --- | --- | --- |
| Yard waste bags | Home | Garden cleanup | Cleanup stalls | Add to store list | Needed |
| Protein yogurt | Health | Breakfast | Poor food default | Add to grocery list | Needed |

## Home and Environment Watchlist

| Area | Condition | Smallest Useful Action | Weather / Tool Dependency | Next Review |
| --- | --- | --- | --- | --- |
| Front garden | Weeds visible | Weed 20 minutes | Dry weather | This week |
| Exterior trim | Paint peeling | Get repair quote | Contractor availability | This month |
"""


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        register = root / "register.md"
        output = root / "home-candidates.md"
        register.write_text(REGISTER)
        generate_candidates.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--register",
                str(register),
                "--output",
                str(output),
                "--force",
            ]
        )
        text = output.read_text()
        assert_contains(text, "Front garden: Weed 20 minutes")
        assert_contains(text, "Mudroom clutter: Reset mudroom shelf")
        assert_contains(text, "Yard waste bags: Add to store list")
        assert_contains(text, "spending or contractor commitment requires governance review")
        if "Protein yogurt" in text:
            raise AssertionError(text)

    print("home candidate smoke tests passed.")


if __name__ == "__main__":
    main()
