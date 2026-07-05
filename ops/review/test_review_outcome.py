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


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def synthetic_recommendation(agent: str = "Health Agent") -> dict[str, object]:
    return {
        "artifact_type": "agent_recommendation",
        "schema_version": 1,
        "agent": agent,
        "recommendation_type": "recommend",
        "proposed_directive": "Breakfast Anchor",
        "authority_level": "level_1_recommend",
        "relevant_facts": ["Synthetic morning food friction is low."],
        "assumptions": [{"statement": "The morning window is available.", "certainty": "medium"}],
        "evidence_quality": ["human_report"],
        "expected_benefit": "Reduced snacking.",
        "costs_and_tradeoffs": [],
        "risks": ["energy"],
        "reversibility": "easy_to_reverse",
        "privacy_impact": "private_only",
        "required_handoffs": [],
        "dissent": "",
        "stop_conditions": ["Stop if it creates protected-time conflict."],
        "review": {"review_date_or_success_criteria": "After next breakfast outcome."},
    }


def synthetic_council_decision(recommendation_path: Path) -> dict[str, object]:
    return {
        "artifact_type": "council_decision",
        "schema_version": 2,
        "date": "2026-06-23",
        "decision_frame": "Select a low-friction morning health directive.",
        "goal_reconciliation_status": "temporary_priority_assumption",
        "goal_reconciliation_sources": [],
        "priority_assumption": "Synthetic conservative priority assumption.",
        "source_recommendations": [str(recommendation_path)],
        "proposed_directive": "Breakfast Anchor",
        "council_outcome": "adopt",
        "rationale": "Synthetic council selected the lowest-friction action.",
        "expected_benefit": "Reduced snacking.",
        "key_risks": ["energy"],
        "dissent": [],
        "evidence_gaps": [],
        "vetoes": [],
        "unresolved_dissent": [],
        "tradeoff_rationale": "Synthetic tradeoff rationale.",
        "tradeoff_scorecard": [],
        "deferrals": ["Operations Agent: defer longer planning until breakfast is stable."],
        "required_handoffs": [],
        "governance_status": "Level 1 council synthesis; no authority increase approved.",
        "stop_conditions": ["Stop if protected time is affected."],
        "next_action": "Breakfast Anchor",
        "review": "After next outcome.",
    }


def run_attributed_review() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        outcome = root / "outcome.md"
        recommendation = root / "recommendation.json"
        council = root / "council.json"
        output = root / "review.md"
        json_output = root / "review.json"
        calibration_dir = private / "agents" / "calibration"
        outcome.write_text(COMPLETED)
        write_json(recommendation, synthetic_recommendation())
        write_json(council, synthetic_council_decision(recommendation))
        review_outcome.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--council-decision",
                str(council),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--write-calibration",
                "--calibration-dir",
                str(calibration_dir),
                "--force",
            ]
        )
        data = json.loads(json_output.read_text())
        calibration_files = sorted(calibration_dir.glob("*.json"))
        if not calibration_files:
            raise AssertionError("expected calibration record output")
        data["written_calibration"] = json.loads(calibration_files[0].read_text())
        data["markdown"] = output.read_text()
        return data


def run_missed_friction_review() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.md"
        output = root / "review.md"
        recommendation = root / "recommendation.json"
        json_output = root / "review.json"
        outcome.write_text(BLOCKED)
        write_json(recommendation, synthetic_recommendation("Home and Environment Agent"))
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--recommendation",
                str(recommendation),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )
        return json.loads(json_output.read_text())


def run_missing_source_review() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        outcome = root / "outcome.md"
        output = root / "review.md"
        json_output = root / "review.json"
        outcome.write_text(COMPLETED)
        review_outcome.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--recommendation",
                str(root / "missing-recommendation.json"),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )
        return json.loads(json_output.read_text())


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

    attributed = run_attributed_review()
    if attributed["council_synthesis_review"]["artifact_type"] != "council_synthesis_review":
        raise AssertionError("expected nested council synthesis review")
    if attributed["council_synthesis_review"]["selection_quality"]["rating"] != "strong":
        raise AssertionError(attributed["council_synthesis_review"])
    if not attributed["agent_recommendation_reviews"]:
        raise AssertionError("expected nested agent recommendation review")
    agent_review = attributed["agent_recommendation_reviews"][0]
    if agent_review["reviewed_agent"] != "Health Agent":
        raise AssertionError(agent_review)
    if agent_review["review_outcome"] != "improve":
        raise AssertionError(agent_review)
    calibration = attributed["agent_calibration_records"][0]
    if calibration["artifact_type"] != "agent_calibration_record":
        raise AssertionError(calibration)
    if calibration["calibration_action"] != "increase_weight":
        raise AssertionError(calibration)
    if attributed["written_calibration"]["agent"] != "Health Agent":
        raise AssertionError("written calibration should match nested record")
    assert_contains(attributed["markdown"], "Council Synthesis Review")
    assert_contains(attributed["markdown"], "Agent Calibration Records")

    missed = run_missed_friction_review()
    caution = " ".join(missed["agent_calibration_records"][0]["cautions"])
    if "Missed execution friction" not in caution:
        raise AssertionError(missed["agent_calibration_records"][0])
    if missed["agent_calibration_records"][0]["calibration_action"] != "decrease_weight":
        raise AssertionError(missed["agent_calibration_records"][0])

    missing = run_missing_source_review()
    missing_review = missing["agent_recommendation_reviews"][0]
    if missing_review["review_outcome"] != "quarantine":
        raise AssertionError(missing_review)
    if missing_review["fit_assessment"]["rating"] != "missing":
        raise AssertionError(missing_review)

    escalated = run_review(ESCALATE)
    assert_contains(escalated, "Escalate")
    assert_contains(escalated, "Needs governance review")
    assert_contains(escalated, "Risk Control")

    print("outcome review smoke tests passed.")


if __name__ == "__main__":
    main()
