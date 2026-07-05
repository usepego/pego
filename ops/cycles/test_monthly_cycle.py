#!/usr/bin/env python3
"""Smoke tests for PEGO monthly strategy review runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import monthly_cycle


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which strategic assumption is weakest? | Prevents drift | Monthly | Add review |
"""


SCHEMA_KEYS = {
    "artifact_type",
    "schema_version",
    "month",
    "strategic_thesis",
    "outcome_summary",
    "decision_quality_summary",
    "agent_calibration_summary",
    "goal_progress_summary",
    "behavior_loop_summary",
    "scenario_benchmark_summary",
    "governance_review_items",
    "evidence_gathering_directives",
    "council_strategy_summary",
    "goal_progress",
    "agent_assessments",
    "assumptions_revisited",
    "strategy_changes",
    "decision_packets_needed",
    "constitution_concerns",
    "next_month_priorities",
    "stop_conditions",
}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def seed_private_root(private: Path) -> None:
    (private / "operator").mkdir(parents=True)
    (private / "outcomes" / "directives").mkdir(parents=True)
    (private / "reviews" / "outcomes").mkdir(parents=True)
    (private / "reviews" / "sessions").mkdir(parents=True)
    (private / "context" / "updates").mkdir(parents=True)
    (private / "governance" / "preflight").mkdir(parents=True)
    (private / "directives" / "queues").mkdir(parents=True)
    (private / "directives" / "weekly").mkdir(parents=True)
    (private / "agents" / "calibration").mkdir(parents=True)
    (private / "goals" / "progress").mkdir(parents=True)
    (private / "behavior-loops").mkdir(parents=True)
    (private / "evaluations" / "scenario-benchmarks").mkdir(parents=True)
    (private / "operator" / "operating-register.md").write_text(REGISTER)
    (private / "outcomes" / "directives" / "2026-06-01-test.md").write_text("# Outcome\n")
    (private / "reviews" / "outcomes" / "2026-06-01-test.md").write_text("# Review\n")
    (private / "context" / "updates" / "2026-06-01-test.md").write_text("# Context\n")
    (private / "governance" / "preflight" / "2026-06-01-test.json").write_text("{}\n")
    (private / "directives" / "queues" / "2026-06-01-queue.md").write_text("# Queue\n")
    (private / "directives" / "weekly" / "2026-W23.md").write_text("# Weekly\n")
    calibration = {
        "artifact_type": "agent_calibration_record",
        "schema_version": 1,
        "date": "2026-06-04",
        "agent": "Health Agent",
        "source_reviews": ["synthetic-review"],
        "recommendation_usefulness": "adequate",
        "score_delta": -1,
        "calibration_action": "decrease_weight",
        "friction_prediction": "weak",
        "evidence_quality": "adequate",
        "stress_impact": "unknown",
        "missed_risks": ["friction"],
        "cautions": ["Missed execution friction; require explicit friction prediction."],
        "council_summary": "Health Agent: outcome downgrade; friction=weak.",
        "future_weighting_note": "Lower confidence until friction is predicted explicitly.",
        "next_review": "Next weekly review.",
    }
    write_json(private / "agents" / "calibration" / "2026-06-health.json", calibration)
    write_json(
        private / "reviews" / "outcomes" / "2026-06-01-test.json",
        {
            "artifact_type": "outcome_review",
            "schema_version": 1,
            "date": "2026-06-01",
            "source_outcome": "synthetic-outcome",
            "directive": "Synthetic health directive",
            "completion_class": "Completed",
            "evidence_summary": "Synthetic evidence was captured.",
            "friction_summary": "",
            "benefit_summary": "Visible progress.",
            "outcome_progress": "Goal moved.",
            "contentment_signal": "More contentment",
            "cost_summary": "",
            "learning_decision": "Repeat",
            "queue_implication": "Add follow-up candidate if recurrence is useful.",
            "context_update_recommendation": "Record provisional pattern if repeated once more.",
            "agent_routing": "Health Agent, Operations",
            "governance_status": "Level 1 learning review; no authority increase approved.",
            "decision_quality_review": {
                "artifact_type": "decision_quality_review",
                "overall_assessment": "improved_decision_quality",
                "dimensions": {},
                "next_architecture_adjustment": "Keep decision pattern available.",
            },
            "council_synthesis_review": {
                "artifact_type": "council_synthesis_review",
                "review_outcome": "improve",
                "governance_fit": {
                    "rating": "strong",
                    "notes": "Level 1 fit.",
                },
            },
            "agent_calibration_records": [calibration],
            "next_review": "Next weekly review.",
        },
    )
    write_json(
        private / "goals" / "progress" / "health.json",
        {
            "artifact_type": "goal_progress",
            "schema_version": 1,
            "date": "2026-06-08",
            "domain": "health",
            "owning_agent": "Health Agent",
            "goal": "Synthetic health progress",
            "goal_id": "synthetic-health-progress",
            "source_signals": ["synthetic-signal"],
            "current_state_summary": "Synthetic health signal showed partial progress.",
            "leading_indicators": [
                {
                    "name": "walks",
                    "value": "2",
                    "unit": "count",
                    "indicator_type": "leading",
                    "source_signal": "synthetic-signal",
                    "confidence": "medium",
                    "updated_at": "2026-06-08",
                }
            ],
            "lagging_indicators": [],
            "trajectory": "stable",
            "confidence": "low",
            "progress_status": "unknown",
            "directive_attribution": ["synthetic-directive"],
            "next_measurement_need": "Add a lagging outcome indicator for health.",
            "governance_notes": ["Sensitive health signal; keep raw telemetry in protected private storage."],
            "review_after": "2026-06-15",
        },
    )
    write_json(
        private / "behavior-loops" / "2026-06-energy-loop.json",
        {
            "artifact_type": "behavior_loop",
            "schema_version": 1,
            "date": "2026-06-10",
            "loop": "Low-energy state appears before the directive",
            "domain": "health",
            "status": "active",
            "confidence": "supported",
            "occurrence_count": 2,
            "source_events": ["synthetic-review-1", "synthetic-review-2"],
            "trigger": "Low-energy state appears before the directive",
            "routine": "Planned directive loses momentum.",
            "reward_or_relief": "Avoids immediate friction and preserves effort.",
            "strategic_effect": "mixed",
            "evidence": "repeated_outcome",
            "replacement_frame": "Switch to the low-energy version before the directive is abandoned.",
            "disruption_directive_candidate": "When low energy appears, use the low-energy version.",
            "guardrails": ["Keep the first disruption small and reversible."],
            "authority_level": "level_1_recommend",
            "review_rule": "Review after the next trigger exposure.",
        },
    )
    write_json(
        private / "evaluations" / "scenario-benchmarks" / "2026-06-benchmark.json",
        {
            "artifact_type": "scenario_benchmark",
            "schema_version": 1,
            "date": "2026-06-20",
            "benchmark_suite": "synthetic-suite",
            "summary": {
                "scenario_count": 3,
                "pego_wins": 2,
                "baseline_wins": 1,
                "ties": 0,
            },
            "scenarios": [],
            "public_safe": True,
            "public_export_review": {"passed": True, "notes": "Synthetic fixture."},
            "failure_modes": [
                {
                    "system": "pego",
                    "failure_mode": "Synthetic architecture gap.",
                    "severity": "low",
                    "preserved": True,
                }
            ],
        },
    )


def seed_thin_private_root(private: Path) -> None:
    (private / "operator").mkdir(parents=True)
    (private / "operator" / "operating-register.md").write_text(REGISTER)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        seed_private_root(private)

        review = monthly_cycle.main_with_args(
            [
                "--private-root",
                str(private),
                "--month",
                "2026-06",
                "--force",
            ]
        )
        if set(review) != SCHEMA_KEYS:
            raise AssertionError(sorted(set(review) - SCHEMA_KEYS))
        if review["artifact_type"] != "monthly_strategy_review":
            raise AssertionError(review)
        if review["agent_assessments"]["operations"]["what_learned"].find("1 outcomes") == -1:
            raise AssertionError(review["agent_assessments"]["operations"])
        if review["assumptions_revisited"][0]["status"] != "supported":
            raise AssertionError(review["assumptions_revisited"])
        if review["decision_quality_summary"]["review_count"] != 1:
            raise AssertionError(review["decision_quality_summary"])
        if review["agent_calibration_summary"]["record_count"] < 1:
            raise AssertionError(review["agent_calibration_summary"])
        if review["goal_progress_summary"]["record_count"] != 1:
            raise AssertionError(review["goal_progress_summary"])
        if review["behavior_loop_summary"]["active_loop_count"] != 1:
            raise AssertionError(review["behavior_loop_summary"])
        if review["scenario_benchmark_summary"]["scenario_count"] != 3:
            raise AssertionError(review["scenario_benchmark_summary"])
        if not review["governance_review_items"]:
            raise AssertionError("expected governance review items")
        if not any(
            "lagging outcome indicator" in item["directive"]
            for item in review["evidence_gathering_directives"]
        ):
            raise AssertionError(review["evidence_gathering_directives"])
        if review["council_strategy_summary"]["strategy_posture"] != "hold_strategy_and_gather_evidence":
            raise AssertionError(review["council_strategy_summary"])

        markdown = private / "directives" / "monthly" / "2026-06-strategy-review.md"
        structured = private / "directives" / "monthly" / "2026-06-strategy-review.json"
        if "Which strategic assumption is weakest?" not in markdown.read_text():
            raise AssertionError(markdown.read_text())
        if "Decision Quality Summary" not in markdown.read_text():
            raise AssertionError(markdown.read_text())
        data = json.loads(structured.read_text())
        if set(data) != SCHEMA_KEYS:
            raise AssertionError(data)

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "thin-private"
        seed_thin_private_root(private)
        review = monthly_cycle.main_with_args(
            [
                "--private-root",
                str(private),
                "--month",
                "2026-06",
                "--force",
            ]
        )
        sources = {item["source"] for item in review["evidence_gathering_directives"]}
        expected_sources = {
            "outcome_reviews",
            "agent_calibration_records",
            "goal_progress",
            "behavior_loops",
            "scenario_benchmark_summary",
        }
        if not expected_sources.issubset(sources):
            raise AssertionError(review["evidence_gathering_directives"])

    print("monthly strategy review smoke tests passed.")


if __name__ == "__main__":
    main()
