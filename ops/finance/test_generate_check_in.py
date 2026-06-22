#!/usr/bin/env python3
"""Smoke tests for PEGO finance check-in generator."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_check_in


CONFIG = {
    "artifact_type": "finance_scenario_input",
    "schema_version": 1,
    "version": 1,
    "as_of": "2026-01-01",
    "currency": "USD",
    "current_position": {
        "liquid_savings": 120000,
        "total_model_savings": 500000,
    },
    "global_assumptions": {
        "current_age": 40,
        "retirement_start_age": 60,
        "age_to_live": 95,
        "target_date": "2040-01-01",
        "social_security_monthly_estimate": 2000,
        "emergency_runway_months": 12,
    },
    "scenarios": [
        {
            "name": "base",
            "monthly_burn": 7000,
            "nominal_return": 0.07,
            "inflation": 0.03,
            "monthly_savings": 4000,
            "include_social_security": False,
        },
        {
            "name": "stress",
            "monthly_burn": 9000,
            "nominal_return": 0.03,
            "inflation": 0.05,
            "monthly_savings": 1000,
            "include_social_security": False,
        },
    ],
}


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        input_path = root / "scenarios.json"
        output_path = root / "finance-check-in.md"
        json_output = root / "finance-check-in.json"
        input_path.write_text(json.dumps(CONFIG))
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
        assert_contains(text, "Has income, recurring burn, savings rate")
        assert_contains(text, "missing required scenarios")
        assert_contains(text, "liquid runway")
        assert_contains(text, "Broad money reflection")
        assert_contains(text, "Public or third-party disclosure")

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "finance_check_in":
            raise AssertionError("expected finance_check_in artifact")
        if structured["privacy_status"] != "protected_private_instance":
            raise AssertionError("expected protected private privacy status")
        if not any(question["signal"] == "runway" for question in structured["questions"]):
            raise AssertionError("expected runway question")

    print("finance check-in smoke tests passed.")


if __name__ == "__main__":
    main()
