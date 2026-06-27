#!/usr/bin/env python3
"""Smoke tests for protected goal reconciliation generation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import reconcile_goals


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        (private / "constitution").mkdir(parents=True)
        (private / "finance").mkdir(parents=True)
        (private / "health").mkdir(parents=True)
        (private / "happiness").mkdir(parents=True)
        (private / "time").mkdir(parents=True)
        (private / "constitution" / "constitution.md").write_text("Synthetic privacy and authority boundary.")
        (private / "finance" / "financial-position.md").write_text("Synthetic income and burn baseline.")
        (private / "health" / "baseline.json").write_text(json.dumps({"goal": {"priority": "synthetic health"}}))
        (private / "happiness" / "model.md").write_text("Synthetic lived-fit model.")
        (private / "time" / "protected-time.md").write_text("Synthetic protected time.")

        output = private / "goals" / "goal-reconciliation.md"
        json_output = private / "goals" / "goal-reconciliation.json"
        reconcile_goals.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-25",
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        text = output.read_text()
        if "Current Priority Thesis" not in text:
            raise AssertionError(text)
        if "Protect financial downside" not in text:
            raise AssertionError(text)
        if "Targeted Questions" not in text:
            raise AssertionError(text)

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "goal_reconciliation":
            raise AssertionError("expected goal_reconciliation artifact")
        finance = next(goal for goal in structured["active_goals"] if goal["domain"] == "finance")
        if finance["status"] != "active":
            raise AssertionError(finance)
        career = next(goal for goal in structured["active_goals"] if goal["domain"] == "career")
        if career["status"] != "needs_baseline":
            raise AssertionError(career)
        if not structured["targeted_questions"]:
            raise AssertionError("expected targeted question")

    print("goal reconciliation smoke tests passed.")


if __name__ == "__main__":
    main()
