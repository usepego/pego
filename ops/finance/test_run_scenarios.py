#!/usr/bin/env python3
"""Smoke tests for the PEGO finance scenario runner using synthetic data."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import run_scenarios


CONFIG = {
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


def main() -> None:
    output = run_scenarios.run(CONFIG)
    if output["validation"]["status"] != "missing_required_scenarios":
        raise AssertionError(output["validation"])
    if output["summary"]["scenario_count"] != 2:
        raise AssertionError(output["summary"])
    if not output["summary"]["flagged_scenarios"]:
        raise AssertionError("expected at least one flagged scenario")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        input_path = root / "input.json"
        output_path = root / "output.json"
        summary_path = root / "summary.md"
        input_path.write_text(json.dumps(CONFIG))
        run_scenarios.main_with_args(
            [
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--summary-output",
                str(summary_path),
                "--write-summary",
            ]
        )
        if not output_path.exists() or not summary_path.exists():
            raise AssertionError("expected output and summary files")

    print("finance scenario smoke tests passed.")


if __name__ == "__main__":
    main()
