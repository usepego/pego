#!/usr/bin/env python3
"""Smoke tests for PEGO health check-in generator."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_check_in


BASELINE = {
    "artifact_type": "health_baseline",
    "schema_version": 1,
    "as_of": "2026-06-23",
    "evidence_policy": {
        "tracking_level": "periodic_metrics",
        "burden_limit": "Use periodic metrics without daily tracking burden.",
        "medical_interpretation": "agent_may_use_as_context_only",
        "measurement_rule": "Ask only when the metric changes a concrete decision.",
    },
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
        "morning_minutes": 5,
        "midday_minutes": 0,
        "evening_minutes": 0,
        "outside_ok": True,
    },
    "metrics": {
        "body": {},
        "vitals": {},
        "glucose": {"a1c_percent": "provided privately"},
        "lipids_metabolic": {},
        "fitness": {},
        "sleep_recovery": {},
        "clinical_context": {},
    },
}


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        input_path = root / "baseline.json"
        output_path = root / "health-check-in.md"
        json_output = root / "health-check-in.json"
        input_path.write_text(json.dumps(BASELINE))
        generate_check_in.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        text = output_path.read_text()
        assert_contains(text, "How did you sleep last night")
        assert_contains(text, "What is the next realistic meal window")
        assert_contains(text, "Which known sweet trigger")
        assert_contains(text, "already-available glucose or A1C")
        assert_contains(text, "Ask only when the metric changes a concrete decision.")
        assert_contains(text, "Broad self-help reflection")

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "health_check_in":
            raise AssertionError("expected health_check_in artifact")
        if structured["privacy_status"] != "protected_private_instance":
            raise AssertionError("expected protected private privacy status")
        if not any(question["signal"] == "metric" for question in structured["questions"]):
            raise AssertionError("expected metric question when glucose context exists")

    print("health check-in smoke tests passed.")


if __name__ == "__main__":
    main()
