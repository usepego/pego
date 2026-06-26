#!/usr/bin/env python3
"""Smoke tests for PEGO outcome review runner."""

from __future__ import annotations

import tempfile
import json
from pathlib import Path

import review_outcome


COMPLETED = """# Directive Outcome: test

## Directive Summary

Breakfast Anchor

## Completion

Completed

## What Happened

Ate protein breakfast.

## Evidence

Human report.

## Friction

None recorded.

## Benefit

Reduced snacking.

## Outcome Progress

Breakfast default became easier tomorrow.

## Contentment Signal

More contentment

## Cost

None recorded.

## Protected-Time Impact

None
"""


BLOCKED = """# Directive Outcome: test

## Directive Summary

Garden Weed Block

## Completion

Blocked

## What Happened

Could not start.

## Evidence

Human report.

## Friction

Rain and no dry window.

## Benefit

None recorded.

## Cost

None recorded.

## Protected-Time Impact

None
"""


ESCALATE = """# Directive Outcome: test

## Directive Summary

Career Exit Work

## Completion

Completed

## What Happened

Drafted exit plan.

## Evidence

Artifact.

## Friction

None recorded.

## Benefit

Strategic clarity.

## Cost

Stress.

## Protected-Time Impact

High
"""


def run_review(text: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.md"
        output = root / "review.md"
        outcome.write_text(text)
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--output",
                str(output),
                "--force",
            ]
        )
        return output.read_text()


def run_json_review(text: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.md"
        output = root / "review.md"
        json_output = root / "review.json"
        outcome.write_text(text)
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )
        return json.loads(json_output.read_text())


def run_review_from_json_outcome() -> tuple[str, dict[str, object]]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.json"
        output = root / "review.md"
        json_output = root / "review.json"
        outcome.write_text(
            json.dumps(
                {
                    "artifact_type": "directive_outcome",
                    "schema_version": 1,
                    "date": "2026-06-23",
                    "source_directive": "private/directives/queues/day.json",
                    "directive_summary": "Garden weed pass",
                    "completion": "blocked",
                    "what_happened": "Rain prevented outdoor work.",
                    "evidence": ["human_report"],
                    "friction": ["weather"],
                    "benefit": "None recorded.",
                    "outcome_progress": "None recorded.",
                    "contentment_signal": "Unknown",
                    "cost": "None recorded.",
                    "protected_time_impact": "none",
                    "stakeholder_impact": "None recorded.",
                    "environment_impact": "Weeds remain visible.",
                    "follow_up_directive_candidates": [],
                    "agent_updates": [],
                    "governance_notes": "None recorded.",
                    "next_review": "Next weekly review.",
                }
            )
        )
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )
        return output.read_text(), json.loads(json_output.read_text())


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    completed = run_review(COMPLETED)
    assert_contains(completed, "Repeat")
    assert_contains(completed, "Health")
    assert_contains(completed, "Decision Quality Review")
    assert_contains(completed, "Outcome Progress")
    assert_contains(completed, "Human Burden")
    assert_contains(completed, "improved_decision_quality")

    completed_json = run_json_review(COMPLETED)
    if completed_json["artifact_type"] != "outcome_review":
        raise AssertionError("json review must declare outcome_review artifact_type")
    if completed_json["learning_decision"] != "Repeat":
        raise AssertionError("completed low-friction outcome should repeat")
    if completed_json["outcome_progress"] != "Breakfast default became easier tomorrow.":
        raise AssertionError("review should preserve outcome progress")
    if completed_json["contentment_signal"] != "More contentment":
        raise AssertionError("review should preserve contentment signal")
    quality = completed_json["decision_quality_review"]
    if quality["artifact_type"] != "decision_quality_review":
        raise AssertionError("expected nested decision quality review")
    if quality["dimensions"]["actionability"]["rating"] != "strong":
        raise AssertionError("completed directive should be strongly actionable")
    if quality["overall_assessment"] != "improved_decision_quality":
        raise AssertionError("completed low-friction benefit should improve decision quality")

    blocked = run_review(BLOCKED)
    assert_contains(blocked, "Block pending dependency")
    assert_contains(blocked, "Home and Environment")

    blocked_markdown, blocked_json = run_review_from_json_outcome()
    assert_contains(blocked_markdown, "Block pending dependency")
    if blocked_json["directive"] != "Garden weed pass":
        raise AssertionError("json outcome directive was not reviewed")
    if blocked_json["learning_decision"] != "Block pending dependency":
        raise AssertionError("blocked json outcome should become a blocker")

    escalated = run_review(ESCALATE)
    assert_contains(escalated, "Escalate")
    assert_contains(escalated, "Needs governance review")
    assert_contains(escalated, "Risk Control")

    print("outcome review smoke tests passed.")


if __name__ == "__main__":
    main()
