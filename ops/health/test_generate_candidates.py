#!/usr/bin/env python3
"""Smoke tests for PEGO health directive candidate generator."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_candidates


BASELINE = {
    "version": 1,
    "as_of": "2026-06-23",
    "goal": {
        "current_weight_kg": 88,
        "target_weight_kg": 80,
        "priority": "weight_loss",
    },
    "constraints": {
        "medical_constraints": [],
        "injuries": [],
        "forbidden_directives": [],
        "protected_time": "Evening relationship time",
    },
    "preferences": {
        "food_defaults": ["eggs and fruit", "greek yogurt"],
        "food_aversions": [],
        "sweet_triggers": ["cookies after dinner"],
        "movement_preferences": [],
        "movement_aversions": ["gym"],
        "available_equipment": [],
    },
    "current_routine": {
        "breakfast": "",
        "lunch": "",
        "dinner": "",
        "snacks": "",
        "movement": "",
        "sleep": "",
    },
    "availability": {
        "morning_minutes": 10,
        "midday_minutes": 20,
        "evening_minutes": 5,
        "outside_ok": True,
    },
}


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        input_path = root / "baseline.json"
        output_path = root / "health-candidates.md"
        input_path.write_text(json.dumps(BASELINE))
        generate_candidates.main_with_args(
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
        assert_contains(text, "Breakfast Anchor")
        assert_contains(text, "Walk Outside")
        assert_contains(text, "Sweet Trigger Control")
        assert_contains(text, "Level 1")
        assert_contains(text, "Do not treat candidates as medical advice")

    print("health candidate smoke tests passed.")


if __name__ == "__main__":
    main()
