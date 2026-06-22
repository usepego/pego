#!/usr/bin/env python3
"""Smoke tests for PEGO finance scenario review runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import review_scenarios


OUTPUT = {
    "version": 1,
    "as_of": "2026-01-01",
    "validation": {
        "required_scenarios": ["base", "conservative", "lifestyle_upgrade", "stress", "upside"],
        "present_scenarios": ["base", "stress"],
        "missing_required_scenarios": ["conservative", "lifestyle_upgrade", "upside"],
        "status": "missing_required_scenarios",
    },
    "summary": {
        "scenario_count": 2,
        "flagged_scenarios": [
            {
                "name": "stress",
                "risk_flags": ["target_after_target_date", "negative_gap_at_target_date"],
            }
        ],
    },
    "results": [
        {"name": "base", "months_to_target": 180},
        {"name": "stress", "months_to_target": None},
    ],
}


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        input_path = root / "scenario-output.json"
        output_path = root / "review.md"
        input_path.write_text(json.dumps(OUTPUT))
        review_scenarios.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--force",
            ]
        )
        text = output_path.read_text()
        assert_contains(text, "Risk Posture")
        assert_contains(text, "Blocked")
        assert_contains(text, "Missing required scenarios")
        assert_contains(text, "No trade, transfer, account change")

    print("finance scenario review smoke tests passed.")


if __name__ == "__main__":
    main()
