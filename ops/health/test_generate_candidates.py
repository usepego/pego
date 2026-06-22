#!/usr/bin/env python3
"""Smoke tests for PEGO health directive candidate generator."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_candidates


BASELINE = {
    "artifact_type": "health_baseline",
    "schema_version": 1,
    "as_of": "2026-06-23",
    "evidence_policy": {
        "tracking_level": "periodic_metrics",
        "burden_limit": "Use periodic metrics without daily tracking burden.",
        "medical_interpretation": "agent_may_use_as_context_only",
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
        "morning_minutes": 10,
        "midday_minutes": 20,
        "evening_minutes": 5,
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
        output_path = root / "health-candidates.md"
        json_output = root / "health-candidates.json"
        input_path.write_text(json.dumps(BASELINE))
        generate_candidates.main_with_args(
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
        assert_contains(text, "Breakfast Anchor")
        assert_contains(text, "Walk Outside")
        assert_contains(text, "Sweet Trigger Control")
        assert_contains(text, "Optional health metrics available: glucose")
        assert_contains(text, "use as context only")
        assert_contains(text, "Level 1")
        assert_contains(text, "Do not treat candidates as medical advice")

        structured = json.loads(json_output.read_text())
        if structured[0]["artifact_type"] != "directive_candidate":
            raise AssertionError("expected directive candidate artifact")
        if structured[0]["candidate"] != "Breakfast Anchor":
            raise AssertionError("expected Breakfast Anchor as first structured candidate")
        if structured[0]["domain"] != "health":
            raise AssertionError("expected health domain")
        if structured[0]["authority_level"] != "level_1_recommend":
            raise AssertionError("expected Level 1 authority")
        if not any(candidate["candidate"] == "Walk Outside" for candidate in structured):
            raise AssertionError("expected Walk Outside structured candidate")

    print("health candidate smoke tests passed.")


if __name__ == "__main__":
    main()
