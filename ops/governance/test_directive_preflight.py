#!/usr/bin/env python3
"""Smoke tests for PEGO directive governance preflight."""

from __future__ import annotations

import directive_preflight


def assert_outcome(text: str, expected: str) -> None:
    result = directive_preflight.preflight(text)
    if result.outcome != expected:
        raise AssertionError(f"expected {expected}, got {result.outcome}: {result}")


def main() -> None:
    assert_outcome("Eat a protein breakfast. Authority level: Level 1.", "pass")
    assert_outcome("Stop if this conflicts with protected time. Level 1.", "pass")
    assert_outcome("Use protected time for a work block. Level 1.", "needs_review")
    assert_outcome("Schedule a weekly recurring workout block. Level 2.", "needs_review")
    assert_outcome("Quit job and make a major investment change. Level 4.", "escalate")
    assert_outcome("Publish account data to a third party integration.", "escalate")
    print("directive preflight smoke tests passed.")


if __name__ == "__main__":
    main()
