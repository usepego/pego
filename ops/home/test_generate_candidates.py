#!/usr/bin/env python3
"""Smoke tests for PEGO home/environment candidate generation."""

from __future__ import annotations

import json
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
        json_output = root / "home-candidates.json"
        register.write_text(REGISTER)
        generate_candidates.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--register",
                str(register),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
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

        structured = json.loads(json_output.read_text())
        if structured[0]["artifact_type"] != "directive_candidate":
            raise AssertionError("expected directive candidate artifact")
        if structured[0]["domain"] != "home_environment":
            raise AssertionError("expected home_environment domain")
        if not any(candidate["candidate"] == "Front garden: Weed 20 minutes" for candidate in structured):
            raise AssertionError("expected front garden structured candidate")
        quote = next(candidate for candidate in structured if candidate["candidate"] == "Exterior trim: Get repair quote")
        if quote["governance_status"] != "reviewed":
            raise AssertionError("expected repair quote to require review")

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        register = private / "operator" / "operating-register.md"
        register.parent.mkdir(parents=True)
        register.write_text(REGISTER)
        generate_candidates.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-23",
                "--json-output",
                str(private / "directives" / "candidates" / "home-candidates.json"),
                "--force",
            ]
        )
        if not (private / "directives" / "candidates" / "home-candidates.md").exists():
            raise AssertionError("expected home candidates under configured private root")

    print("home candidate smoke tests passed.")


if __name__ == "__main__":
    main()
