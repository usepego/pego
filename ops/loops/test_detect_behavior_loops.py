#!/usr/bin/env python3
"""Smoke tests for PEGO behavior loop detection."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import detect_behavior_loops


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def outcome_review(path: Path, directive: str, friction: str) -> None:
    write_json(
        path,
        {
            "artifact_type": "outcome_review",
            "schema_version": 1,
            "date": "2026-07-04",
            "source_outcome": "synthetic-outcome.json",
            "directive": directive,
            "completion_class": "Blocked",
            "evidence_summary": "Synthetic outcome evidence.",
            "friction_summary": friction,
            "benefit_summary": "None recorded.",
            "outcome_progress": "None recorded.",
            "contentment_signal": "Unknown",
            "cost_summary": "None recorded.",
            "learning_decision": "Block pending dependency",
            "queue_implication": "Move candidate to blocked until dependency changes.",
            "context_update_recommendation": "Update operating register with blocker.",
            "agent_routing": "Home and Environment, Operations",
            "governance_status": "Level 1 learning review; no authority increase approved.",
            "decision_quality_review": {
                "artifact_type": "decision_quality_review",
                "overall_assessment": "mixed",
                "dimensions": {},
                "next_architecture_adjustment": "Alter conditions before repeating.",
            },
            "next_review": "Next weekly review.",
        },
    )


def read_first_loop(private: Path) -> dict[str, object]:
    loops = sorted((private / "behavior-loops").glob("*.json"))
    loops = [path for path in loops if path.name != "detection-summary.json"]
    if not loops:
        raise AssertionError("expected behavior loop output")
    return json.loads(loops[0].read_text())


def test_repeated_outcomes_create_active_loop_and_candidate() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        review_a = root / "review-a.json"
        review_b = root / "review-b.json"
        outcome_review(review_a, "Garden Weed Block", "Rain and no dry outdoor window.")
        outcome_review(review_b, "Garden Weed Block", "Rain prevented outdoor work again.")

        detect_behavior_loops.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--outcome-review",
                str(review_a),
                "--outcome-review",
                str(review_b),
                "--force",
            ]
        )

        loop = read_first_loop(private)
        if loop["status"] != "active" or loop["confidence"] != "supported":
            raise AssertionError(loop)
        if loop["occurrence_count"] != 2:
            raise AssertionError(loop)
        candidates = sorted((private / "directives" / "candidates").glob("behavior-loop-*.json"))
        if not candidates:
            raise AssertionError("expected disruption directive candidate")
        candidate = json.loads(candidates[0].read_text())
        if candidate["artifact_type"] != "directive_candidate":
            raise AssertionError(candidate)
        if "operating default" not in candidate["proposed_action"]:
            raise AssertionError(candidate)
        wording = " ".join(
            [
                candidate["proposed_action"],
                candidate["target_behavior"],
                candidate["environment_design"],
                candidate["stop_condition"],
            ]
        ).lower()
        for blocked_word in ["lazy", "bad", "weakness", "self-control failure"]:
            if blocked_word in wording:
                raise AssertionError(f"blame wording found: {blocked_word}")


def test_single_outcome_stays_provisional_without_candidate() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        review = root / "review.json"
        outcome_review(review, "Garden Weed Block", "Rain prevented outdoor work.")

        detect_behavior_loops.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--outcome-review",
                str(review),
                "--force",
            ]
        )

        loop = read_first_loop(private)
        if loop["status"] != "proposed" or loop["confidence"] != "provisional":
            raise AssertionError(loop)
        candidates = sorted((private / "directives" / "candidates").glob("behavior-loop-*.json"))
        if candidates:
            raise AssertionError("single provisional loop should not emit candidate by default")


def test_state_signal_can_seed_provisional_loop() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        signal = root / "signal.json"
        write_json(
            signal,
            {
                "artifact_type": "state_signal",
                "schema_version": 1,
                "date": "2026-07-04",
                "observed_at": "2026-07-04T14:00:00",
                "source_type": "manual_text",
                "ingestion_mode": "manual",
                "domain": "health",
                "owning_agent": "Health Agent",
                "signal_type": "behavior_observed",
                "summary": "Evening snack environment repeatedly changes the food default.",
                "measurements": [],
                "affected_goals": ["Synthetic nutrition consistency"],
                "evidence_strength": "human_report",
                "confidence": "medium",
                "privacy_class": "protected_private",
                "raw_source_reference": "",
                "raw_data_retention": "not_stored",
                "governance_notes": [],
                "review_after": "2026-07-11",
                "expires_after": "2026-07-18",
            },
        )

        detect_behavior_loops.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--state-signal",
                str(signal),
                "--force",
            ]
        )

        loop = read_first_loop(private)
        if loop["domain"] != "health":
            raise AssertionError(loop)
        if loop["confidence"] != "provisional":
            raise AssertionError(loop)


def main() -> None:
    test_repeated_outcomes_create_active_loop_and_candidate()
    test_single_outcome_stays_provisional_without_candidate()
    test_state_signal_can_seed_provisional_loop()
    print("behavior loop detector smoke tests passed.")


if __name__ == "__main__":
    main()
