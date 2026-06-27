#!/usr/bin/env python3
"""Smoke tests for PEGO first-run intake generator."""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_intake


def run_intake(phase: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "intake.md"
        generate_intake.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--phase",
                phase,
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
    aim = run_intake("aim")
    assert_contains(aim, "What future state would make life clearly better?")
    assert_contains(aim, "Ask the user to choose a 1-year or 10-year timeline.")

    environment = run_intake("environment")
    assert_contains(environment, "Which visible part of the home or yard is most annoying right now?")
    assert_contains(environment, "private/operator/operating-register.md")

    health = run_intake("health")
    assert_contains(health, "blood pressure, blood sugar/A1C, lipids")
    assert_contains(health, "without requiring new tracking")
    assert_contains(health, "Ask the user to start measuring biomarkers")

    finance = run_intake("finance-baseline")
    assert_contains(finance, "rough monthly take-home pay")
    assert_contains(finance, "rough monthly burn")
    assert_contains(finance, "Require a spreadsheet before creating a useful baseline.")

    career = run_intake("career-baseline")
    assert_contains(career, "current role, compensation dependency")
    assert_contains(career, "Ask the user to decide whether to quit.")

    happiness = run_intake("happiness-baseline")
    assert_contains(happiness, "Which impressive goals could become traps")
    assert_contains(happiness, "Treat happiness as a mood score.")

    reconciliation = run_intake("goal-reconciliation")
    assert_contains(reconciliation, "Which goals must PEGO protect")
    assert_contains(reconciliation, "When finance, health, work, home, relationships")
    assert_contains(reconciliation, "Ask the user to rank every life goal.")

    authority = run_intake("authority")
    assert_contains(authority, "Which low-risk daily choices may PEGO direct by default?")
    assert_contains(authority, "Treat silence as authority.")

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        generate_intake.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-23",
                "--phase",
                "boundary",
                "--force",
            ]
        )
        output = private / "onboarding" / "intake" / "2026-06-23-boundary.md"
        assert_contains(output.read_text(), "Which PEGO mode are we in right now")

    print("first-run intake smoke tests passed.")


if __name__ == "__main__":
    main()
