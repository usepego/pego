#!/usr/bin/env python3
"""Contract tests for PEGO governance-loop runner outputs."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import schema_validation


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "pego" / "schemas"


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load module: {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


record_state_signal = load_module("contract_record_state_signal", "ops/state/record_state_signal.py")
update_goal_progress = load_module("contract_update_goal_progress", "ops/goals/update_goal_progress.py")
reconcile_goals = load_module("contract_reconcile_goals", "ops/goals/reconcile_goals.py")
synthesize_decision = load_module("contract_synthesize_decision", "ops/council/synthesize_decision.py")
synthesize_queue = load_module("contract_synthesize_queue", "ops/synthesis/synthesize_queue.py")
review_outcome = load_module("contract_review_outcome", "ops/review/review_outcome.py")
detect_behavior_loops = load_module("contract_detect_behavior_loops", "ops/loops/detect_behavior_loops.py")
run_scenario_benchmarks = load_module("contract_run_scenario_benchmarks", "ops/evaluation/run_scenario_benchmarks.py")
monthly_cycle = load_module("contract_monthly_cycle", "ops/cycles/monthly_cycle.py")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def validate_artifact(data: dict[str, Any], schema_name: str) -> None:
    schema_validation.validate(data, schema_validation.load_json(SCHEMAS / schema_name))


def validate_file(path: Path, schema_name: str) -> dict[str, Any]:
    data = read_json(path)
    validate_artifact(data, schema_name)
    return data


def recommendation(agent: str, directive: str, benefit: str) -> dict[str, Any]:
    return {
        "artifact_type": "agent_recommendation",
        "schema_version": 1,
        "agent": agent,
        "recommendation_type": "recommend",
        "proposed_directive": directive,
        "authority_level": "level_1_recommend",
        "relevant_facts": ["Synthetic contract fact."],
        "assumptions": [{"statement": "Synthetic context is stable.", "certainty": "medium"}],
        "evidence_quality": ["human_report"],
        "expected_benefit": benefit,
        "costs_and_tradeoffs": ["Uses a small amount of attention."],
        "risks": ["time"],
        "reversibility": "easy_to_reverse",
        "privacy_impact": "private_only",
        "required_handoffs": [],
        "dissent": "",
        "stop_conditions": ["Stop if the context changes materially."],
        "review": {"review_date_or_success_criteria": "Review after synthetic outcome."},
    }


def calibration(agent: str, score_delta: int, action: str) -> dict[str, Any]:
    return {
        "artifact_type": "agent_calibration_record",
        "schema_version": 1,
        "date": "2026-07-04",
        "agent": agent,
        "source_reviews": ["synthetic-contract-review"],
        "recommendation_usefulness": "adequate",
        "score_delta": score_delta,
        "calibration_action": action,
        "friction_prediction": "adequate",
        "evidence_quality": "adequate",
        "stress_impact": "preserved",
        "missed_risks": [],
        "cautions": ["Synthetic contract caution."],
        "council_summary": "Synthetic calibration context.",
        "future_weighting_note": "Use this synthetic calibration only for contract testing.",
        "next_review": "Next synthetic review.",
    }


def directive_outcome(source_directive: str) -> dict[str, Any]:
    return {
        "artifact_type": "directive_outcome",
        "schema_version": 1,
        "date": "2026-07-04",
        "source_directive": source_directive,
        "directive_summary": "Take a 20 minute recovery walk",
        "completion": "completed",
        "what_happened": "The synthetic walk was completed.",
        "evidence": ["human_report"],
        "friction": [],
        "benefit": "Energy was preserved.",
        "outcome_progress": "Recovery behavior became easier.",
        "contentment_signal": "More contentment",
        "cost": "None recorded.",
        "protected_time_impact": "none",
        "stakeholder_impact": "None recorded.",
        "environment_impact": "Outside route was usable.",
        "follow_up_directive_candidates": [],
        "agent_updates": [],
        "governance_notes": "None recorded.",
        "next_review": "Next weekly review.",
    }


def directive_candidate() -> dict[str, Any]:
    return {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": "Recovery Walk",
        "domain": "health",
        "altitude": "directive",
        "proposed_action": "Take a 20 minute recovery walk",
        "duration": "20 min",
        "timing": "Before evening",
        "energy_required": "low",
        "location_required": "outside",
        "dependencies": [],
        "expected_benefit": "Reduces stress and protects energy.",
        "consequence_of_deferral": "Energy ambiguity and future scrambling continue.",
        "target_behavior": "Shift into a low-friction recovery default.",
        "environment_design": "Use the outside route before the next work block.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "draft",
        "conflicts": [],
        "stop_condition": "Stop if pain appears.",
    }


def test_governance_loop_contracts() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private = root / "private"
        private.mkdir()

        signal_json = private / "telemetry" / "signals" / "home-signal.json"
        record_state_signal.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--observed-at",
                "2026-07-04T09:00:00",
                "--source-type",
                "manual_text",
                "--domain",
                "home",
                "--signal-type",
                "environment",
                "--summary",
                "Visible maintenance friction is increasing.",
                "--measurement",
                "visible_friction=medium,,today,lower_is_better",
                "--affected-goal",
                "Preserve home serenity.",
                "--output",
                str(signal_json),
                "--force",
            ]
        )
        state_signal = validate_file(signal_json, "state-signal.schema.json")
        if state_signal["domain"] != "home_environment":
            raise AssertionError("expected canonical home_environment domain")

        update_goal_progress.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--signal",
                str(signal_json),
                "--lagging-indicator",
                "name=visible_friction;value=medium;confidence=medium",
                "--force",
            ]
        )
        goal_progress_path = private / "goals" / "progress" / "home_environment.json"
        validate_file(goal_progress_path, "goal-progress.schema.json")

        reconcile_goals.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--force",
            ]
        )
        reconciliation = validate_file(private / "goals" / "goal-reconciliation.json", "goal-reconciliation.schema.json")
        if "home_environment" not in {item["domain"] for item in reconciliation["active_goals"]}:
            raise AssertionError("expected home_environment in goal reconciliation")

        operations_rec = private / "recommendations" / "operations.json"
        health_rec = private / "recommendations" / "health.json"
        operations_calibration = private / "agents" / "calibration" / "operations.json"
        health_calibration = private / "agents" / "calibration" / "health.json"
        write_json(operations_rec, recommendation("Operations Agent", "Run a 30 minute work map", "Clarifies work next step."))
        write_json(health_rec, recommendation("Health Agent", "Take a 20 minute recovery walk", "Protects energy."))
        write_json(operations_calibration, calibration("Operations Agent", -2, "decrease_weight"))
        write_json(health_calibration, calibration("Health Agent", 2, "increase_weight"))
        validate_file(operations_rec, "agent-recommendation.schema.json")
        validate_file(health_rec, "agent-recommendation.schema.json")
        validate_file(operations_calibration, "agent-calibration-record.schema.json")
        validate_file(health_calibration, "agent-calibration-record.schema.json")

        council_json = private / "council" / "decisions" / "council-decision.json"
        synthesize_decision.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--frame",
                "Choose the next synthetic directive.",
                "--recommendation",
                str(operations_rec),
                "--recommendation",
                str(health_rec),
                "--agent-calibration",
                str(operations_calibration),
                "--agent-calibration",
                str(health_calibration),
                "--priority-assumption",
                "Use low-risk reversible synthetic work.",
                "--json-output",
                str(council_json),
                "--force",
            ]
        )
        council = validate_file(council_json, "council-decision.schema.json")
        if council["proposed_directive"] != "Take a 20 minute recovery walk":
            raise AssertionError("expected calibrated council selection")

        candidate_json = private / "directives" / "candidates" / "candidate.json"
        queue_json = private / "directives" / "queues" / "queue.json"
        write_json(candidate_json, directive_candidate())
        validate_file(candidate_json, "directive-candidate.schema.json")
        synthesize_queue.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--candidate",
                str(candidate_json),
                "--json-output",
                str(queue_json),
                "--force",
            ]
        )
        queue = validate_file(queue_json, "directive-queue.schema.json")
        if "anxiety_reduction" not in {
            item["dimension"] for item in queue["active_candidates"][0]["scorecard"]["score_dimensions"]
        }:
            raise AssertionError("expected anxiety_reduction score dimension")

        outcome_json = private / "outcomes" / "directives" / "outcome.json"
        review_json = private / "reviews" / "outcomes" / "review.json"
        write_json(outcome_json, directive_outcome(str(queue_json)))
        validate_file(outcome_json, "directive-outcome.schema.json")
        review_outcome.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--outcome",
                str(outcome_json),
                "--council-decision",
                str(council_json),
                "--recommendation",
                str(health_rec),
                "--json-output",
                str(review_json),
                "--write-calibration",
                "--force",
            ]
        )
        outcome_review = validate_file(review_json, "outcome-review.schema.json")
        for record in outcome_review["agent_calibration_records"]:
            validate_artifact(record, "agent-calibration-record.schema.json")

        detect_behavior_loops.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-07-04",
                "--outcome-review",
                str(review_json),
                "--outcome-review",
                str(review_json),
                "--force",
            ]
        )
        loop_paths = [
            path
            for path in sorted((private / "behavior-loops").glob("*.json"))
            if path.name != "detection-summary.json"
        ]
        if not loop_paths:
            raise AssertionError("expected behavior loop artifact")
        validate_file(loop_paths[0], "behavior-loop.schema.json")
        loop_candidates = sorted((private / "directives" / "candidates").glob("behavior-loop-*.json"))
        if not loop_candidates:
            raise AssertionError("expected behavior-loop directive candidate")
        validate_file(loop_candidates[0], "directive-candidate.schema.json")

        benchmark_json = private / "evaluations" / "benchmarks" / "scenario-benchmark.json"
        run_scenario_benchmarks.main_with_args(
            [
                "--date",
                "2026-07-04",
                "--output",
                str(private / "evaluations" / "benchmarks" / "scenario-benchmark.md"),
                "--json-output",
                str(benchmark_json),
                "--force",
            ]
        )
        benchmark = validate_file(benchmark_json, "scenario-benchmark.schema.json")
        if benchmark["summary"]["ties"] < 1:
            raise AssertionError("expected benchmark suite to preserve a tie")

        monthly_json = private / "directives" / "monthly" / "2026-07-strategy-review.json"
        monthly_cycle.main_with_args(
            [
                "--private-root",
                str(private),
                "--month",
                "2026-07",
                "--json-output",
                str(monthly_json),
                "--force",
            ]
        )
        monthly = validate_file(monthly_json, "monthly-strategy-review.schema.json")
        for agent in ["venture", "home_environment", "communications"]:
            if agent not in monthly["agent_assessments"]:
                raise AssertionError(f"expected monthly assessment for {agent}")


def main() -> None:
    test_governance_loop_contracts()
    print("schema contract smoke tests passed.")


if __name__ == "__main__":
    main()
