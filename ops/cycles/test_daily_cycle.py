#!/usr/bin/env python3
"""Smoke tests for PEGO daily cycle runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import daily_cycle


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 60 min | Medium | Computer | Workday | Level 1 | Ready |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which missing supply would block tomorrow? | Prevents scramble | Daily | Add candidate |
"""


CANDIDATES = """# Candidates

| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Breakfast Anchor | Health | 10 min | Low | Home | Morning | Level 1 | Draft | Stabilizes diet | Hunger and snacking | None |
| Venture Problem Map | Venture | 60 min | Medium | Computer | Workday | Level 1 | Draft | Strategic progress | Delays clarity | None |
"""


HEALTH_BASELINE = """{
  "artifact_type": "health_baseline",
  "schema_version": 1,
  "as_of": "2026-06-23",
  "evidence_policy": {
    "tracking_level": "minimal",
    "burden_limit": "Use the least tracking that produces better directives.",
    "medical_interpretation": "agent_may_use_as_context_only",
    "measurement_rule": "Ask only when the metric changes a concrete decision."
  },
  "goal": {
    "current_weight_kg": null,
    "target_weight_kg": null,
    "priority": "weight_loss"
  },
  "constraints": {
    "medical_constraints": [],
    "injuries": [],
    "forbidden_directives": [],
    "protected_time": ""
  },
  "preferences": {
    "food_defaults": ["eggs"],
    "food_aversions": [],
    "sweet_triggers": [],
    "movement_preferences": [],
    "movement_aversions": [],
    "available_equipment": []
  },
  "current_routine": {
    "breakfast": "",
    "lunch": "",
    "dinner": "",
    "snacks": "",
    "movement": "",
    "sleep": ""
  },
  "availability": {
    "morning_minutes": 10,
    "midday_minutes": 10,
    "evening_minutes": 10,
    "outside_ok": true
  },
  "metrics": {
    "body": {},
    "vitals": {},
    "glucose": {},
    "lipids_metabolic": {},
    "fitness": {},
    "sleep_recovery": {},
    "clinical_context": {}
  }
}
"""


FINANCE_SCENARIOS = """{
  "artifact_type": "finance_scenario_input",
  "schema_version": 1,
  "version": 1,
  "as_of": "2026-01-01",
  "currency": "USD",
  "current_position": {
    "liquid_savings": 120000,
    "total_model_savings": 500000
  },
  "global_assumptions": {
    "current_age": 40,
    "retirement_start_age": 60,
    "age_to_live": 95,
    "target_date": "2040-01-01",
    "social_security_monthly_estimate": 2000,
    "emergency_runway_months": 12
  },
  "scenarios": [
    {
      "name": "base",
      "monthly_burn": 7000,
      "nominal_return": 0.07,
      "inflation": 0.03,
      "monthly_savings": 4000,
      "include_social_security": false
    },
    {
      "name": "stress",
      "monthly_burn": 9000,
      "nominal_return": 0.03,
      "inflation": 0.05,
      "monthly_savings": 1000,
      "include_social_security": false
    }
  ]
}
"""


AGENT_RECOMMENDATION = {
    "artifact_type": "agent_recommendation",
    "schema_version": 1,
    "agent": "Operations",
    "recommendation_type": "recommend",
    "proposed_directive": "Run a 30 minute venture problem map",
    "authority_level": "level_1_recommend",
    "relevant_facts": ["Synthetic test fact"],
    "assumptions": [{"statement": "Synthetic assumption", "certainty": "medium"}],
    "evidence_quality": ["agent_inference"],
    "expected_benefit": "Clarifies the next business experiment.",
    "costs_and_tradeoffs": ["Uses focused work time."],
    "risks": ["time", "energy"],
    "reversibility": "easy_to_reverse",
    "privacy_impact": "private_only",
    "required_handoffs": ["Venture"],
    "dissent": "",
    "stop_conditions": ["Stop if protected time begins."],
    "review": {"review_date_or_success_criteria": "Review after artifact exists."},
}


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        response = root / "response.md"
        preflight = root / "preflight.json"
        outcome = root / "outcome.md"
        review = root / "review.md"
        context = root / "context.md"
        candidates = root / "candidates.md"
        health_baseline = root / "health-baseline.json"
        health_check_in = root / "health-check-in.md"
        health_check_in_json = root / "health-check-in.json"
        finance_scenarios = root / "finance-scenarios.json"
        finance_check_in = root / "finance-check-in.md"
        finance_check_in_json = root / "finance-check-in.json"
        recommendation = root / "recommendation.json"
        council_decision = root / "council-decision.md"
        council_decision_json = root / "council-decision.json"
        council_candidate = root / "council-candidate.md"
        council_candidate_json = root / "council-candidate.json"
        writing_brief = root / "writing-brief.md"
        writing_candidate = root / "writing-candidate.md"
        writing_candidate_json = root / "writing-candidate.json"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)
        candidates.write_text(CANDIDATES)
        health_baseline.write_text(HEALTH_BASELINE)
        finance_scenarios.write_text(FINANCE_SCENARIOS)
        recommendation.write_text(json.dumps(AGENT_RECOMMENDATION))

        daily_cycle.main_with_args(
            [
                "health-check-in",
                "--date",
                "2026-06-23",
                "--input",
                str(health_baseline),
                "--output",
                str(health_check_in),
                "--json-output",
                str(health_check_in_json),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "finance-check-in",
                "--date",
                "2026-06-23",
                "--input",
                str(finance_scenarios),
                "--output",
                str(finance_check_in),
                "--json-output",
                str(finance_check_in_json),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "council",
                "--date",
                "2026-06-23",
                "--frame",
                "Choose next work directive.",
                "--recommendation",
                str(recommendation),
                "--priority-assumption",
                "Synthetic test assumption: preserve low-risk reversible work only.",
                "--output",
                str(council_decision),
                "--json-output",
                str(council_decision_json),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "council-candidate",
                "--decision",
                str(council_decision_json),
                "--output",
                str(council_candidate),
                "--json-output",
                str(council_candidate_json),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "writing-brief",
                "--date",
                "2026-06-23",
                "--artifact",
                "PEGO introduction essay",
                "--voice-model",
                str(root / "missing-voice-model.md"),
                "--brief-output",
                str(writing_brief),
                "--candidate-output",
                str(writing_candidate),
                "--json-output",
                str(writing_candidate_json),
                "--force",
            ]
        )

        daily_cycle.main_with_args(
            [
                "synthesize",
                "--date",
                "2026-06-23",
                "--candidate",
                str(candidates),
                "--candidate",
                str(council_candidate_json),
                "--candidate",
                str(writing_candidate_json),
                "--available",
                "30",
                "--output",
                str(queue),
                "--force",
            ]
        )

        daily_cycle.main_with_args(
            [
                "next",
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--response-output",
                str(response),
                "--preflight-output",
                str(preflight),
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "outcome",
                "--date",
                "2026-06-23",
                "--directive",
                "Reduced Venture Problem Map",
                "--completion",
                "completed",
                "--what-happened",
                "Synthetic outcome.",
                "--output",
                str(outcome),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "review",
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome),
                "--output",
                str(review),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                "learn",
                "--date",
                "2026-06-23",
                "--source",
                "Outcome",
                "--raw-observation",
                "Synthetic learning.",
                "--update-class",
                "Pattern",
                "--evidence-strength",
                "Directive outcome",
                "--stability",
                "Current but changeable",
                "--proposed-update",
                "Synthetic update.",
                "--output",
                str(context),
                "--force",
            ]
        )

        for path in (
            queue,
            response,
            preflight,
            outcome,
            review,
            context,
            health_check_in,
            health_check_in_json,
            finance_check_in,
            finance_check_in_json,
            council_decision,
            council_decision_json,
            council_candidate,
            council_candidate_json,
            writing_brief,
            writing_candidate,
            writing_candidate_json,
        ):
            if not path.exists():
                raise AssertionError(f"missing expected file: {path}")
        if "Learning Decision" not in review.read_text():
            raise AssertionError(review.read_text())
        if "How did you sleep last night" not in health_check_in.read_text():
            raise AssertionError(health_check_in.read_text())
        if "Has income, recurring burn, savings rate" not in finance_check_in.read_text():
            raise AssertionError(finance_check_in.read_text())
        if "Council Outcome" not in council_decision.read_text():
            raise AssertionError(council_decision.read_text())
        if "directive_candidate" not in council_candidate_json.read_text():
            raise AssertionError(council_candidate_json.read_text())
        if "communications" not in writing_candidate_json.read_text():
            raise AssertionError(writing_candidate_json.read_text())

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        (private / "health").mkdir(parents=True)
        (private / "finance").mkdir(parents=True)
        (private / "operator").mkdir(parents=True)
        (private / "directives" / "candidates").mkdir(parents=True)
        (private / "person").mkdir(parents=True)
        (private / "health" / "baseline.json").write_text(HEALTH_BASELINE)
        (private / "finance" / "scenarios.json").write_text(FINANCE_SCENARIOS)
        (private / "operator" / "operating-register.md").write_text(REGISTER)
        recommendation = private / "recommendation.json"
        seed_candidate = private / "directives" / "candidates" / "seed-candidates.md"
        recommendation.write_text(json.dumps(AGENT_RECOMMENDATION))
        seed_candidate.write_text(CANDIDATES)

        root_args = ["--private-root", str(private)]
        daily_cycle.main_with_args([*root_args, "health-check-in", "--date", "2026-06-23", "--force"])
        daily_cycle.main_with_args([*root_args, "finance-check-in", "--date", "2026-06-23", "--force"])
        daily_cycle.main_with_args(
            [
                *root_args,
                "council",
                "--date",
                "2026-06-23",
                "--recommendation",
                str(recommendation),
                "--force",
            ]
        )
        if not (private / "goals" / "goal-reconciliation.json").exists():
            raise AssertionError("expected daily council to build goal reconciliation")
        daily_cycle.main_with_args(
            [
                *root_args,
                "council-candidate",
                "--decision",
                str(private / "council" / "decisions" / "council-decision.md"),
                "--force",
            ]
        )
        daily_cycle.main_with_args([*root_args, "writing-brief", "--date", "2026-06-23", "--force"])
        daily_cycle.main_with_args(
            [
                *root_args,
                "synthesize",
                "--date",
                "2026-06-23",
                "--candidate",
                str(seed_candidate),
                "--candidate",
                str(private / "directives" / "candidates" / "council-candidate.md"),
                "--candidate",
                str(private / "directives" / "candidates" / "communications-candidates.md"),
                "--available",
                "45",
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                *root_args,
                "next",
                "--date",
                "2026-06-23",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                *root_args,
                "outcome",
                "--date",
                "2026-06-23",
                "--directive",
                "Venture Problem Map",
                "--completion",
                "completed",
                "--what-happened",
                "Synthetic daily-cycle outcome.",
                "--force",
            ]
        )
        outcome_path = private / "outcomes" / "directives" / "2026-06-23-venture-problem-map.md"
        daily_cycle.main_with_args(
            [
                *root_args,
                "review",
                "--date",
                "2026-06-23",
                "--outcome",
                str(outcome_path),
                "--force",
            ]
        )
        daily_cycle.main_with_args(
            [
                *root_args,
                "learn",
                "--date",
                "2026-06-23",
                "--source",
                "Outcome",
                "--raw-observation",
                "Synthetic daily-cycle learning.",
                "--update-class",
                "Pattern",
                "--evidence-strength",
                "Directive outcome",
                "--stability",
                "Current but changeable",
                "--proposed-update",
                "Synthetic daily-cycle update.",
                "--force",
            ]
        )

        expected_private_outputs = [
            private / "health" / "check-ins" / "health-check-in.md",
            private / "finance" / "check-ins" / "finance-check-in.md",
            private / "council" / "decisions" / "council-decision.md",
            private / "directives" / "candidates" / "council-candidate.md",
            private / "directives" / "candidates" / "communications-candidates.md",
            private / "directives" / "queues" / "2026-06-23-queue.md",
            private / "directives" / "command-responses" / "2026-06-23-next.md",
            private / "governance" / "preflight" / "2026-06-23-next.json",
            outcome_path,
            private / "reviews" / "outcomes" / "2026-06-23-2026-06-23-venture-problem-map.md",
        ]
        for path in expected_private_outputs:
            if not path.exists():
                raise AssertionError(f"missing private-root output: {path}")
        if not list((private / "writing" / "briefs").glob("*.md")):
            raise AssertionError("expected writing brief under external private root")
        if not list((private / "context" / "updates").glob("*.md")):
            raise AssertionError("expected context update under external private root")

    print("daily cycle smoke tests passed.")


if __name__ == "__main__":
    main()
