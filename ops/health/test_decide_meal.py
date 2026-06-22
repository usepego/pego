#!/usr/bin/env python3
"""Smoke tests for PEGO meal decision runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import decide_meal


def food_option(
    item: str,
    calories: int,
    protein: int,
    fiber: int,
    goal_fit: str,
    satiety: str,
    minutes: int,
) -> dict[str, object]:
    return {
        "artifact_type": "food_option",
        "schema_version": 1,
        "date": "2026-06-23",
        "source": "agent_estimate",
        "source_confidence": "low",
        "location_type": "home",
        "provider": "Synthetic provider",
        "item": item,
        "components": ["Synthetic component"],
        "availability": "Now",
        "cost_estimate": {"amount": 10, "currency": "USD", "confidence": "low"},
        "time_and_friction": {"minutes": minutes, "friction_notes": ["Synthetic friction"]},
        "nutrition_estimate": {
            "calories": calories,
            "protein_g": protein,
            "fiber_g": fiber,
            "sugar_g": 5,
            "sodium_mg": 500,
            "confidence": "low",
        },
        "goal_fit": goal_fit,
        "enjoyment_fit": "acceptable",
        "satiety_estimate": satiety,
        "tradeoffs": ["Synthetic tradeoff"],
        "stop_condition": "Synthetic stop condition.",
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        options = root / "options.json"
        decision = root / "decision.md"
        decision_json = root / "decision.json"
        candidate = root / "candidate.md"
        candidate_json = root / "candidate.json"
        options.write_text(
            json.dumps(
                [
                    food_option("Large restaurant sandwich", 1200, 45, 3, "weak", "strong", 20),
                    food_option("Egg bowl with fruit", 450, 32, 8, "strong", "strong", 10),
                ]
            )
        )

        result = decide_meal.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--meal",
                "Lunch",
                "--option",
                str(options),
                "--recent-food",
                "one egg; espresso",
                "--strategy",
                "weight_loss",
                "--output",
                str(decision),
                "--json-output",
                str(decision_json),
                "--candidate-output",
                str(candidate),
                "--candidate-json-output",
                str(candidate_json),
                "--force",
            ]
        )

        if "Egg bowl with fruit" not in result["selected_directive"]:
            raise AssertionError(result)
        if "Meal Decision" not in decision.read_text():
            raise AssertionError(decision.read_text())
        structured = json.loads(decision_json.read_text())
        if structured["artifact_type"] != "meal_decision":
            raise AssertionError(structured)
        candidate_data = json.loads(candidate_json.read_text())
        if candidate_data["artifact_type"] != "directive_candidate":
            raise AssertionError(candidate_data)
        if candidate_data["domain"] != "health":
            raise AssertionError(candidate_data)

    print("meal decision smoke tests passed.")


if __name__ == "__main__":
    main()
