#!/usr/bin/env python3
"""Smoke tests for the root PEGO command wrapper."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PEGOCTL = ROOT / "pegoctl"


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 45 min | Medium | Computer | Workday | Level 1 | Ready |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which dependency could block the next work block? | Prevents delay | Daily | Add candidate |
"""


FINANCE_SCENARIOS = {
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


HEALTH_BASELINE = {
    "artifact_type": "health_baseline",
    "schema_version": 1,
    "evidence_policy": {"tracking_level": "minimal"},
    "goal": {"priority": "weight_loss"},
    "constraints": {},
    "preferences": {
        "food_defaults": ["synthetic eggs and fruit"],
        "sweet_triggers": ["synthetic evening snack"],
    },
    "current_routine": {},
    "availability": {"morning_minutes": 10, "midday_minutes": 15, "outside_ok": True},
    "metrics": {},
}


FOOD_OPTIONS = [
    {
        "artifact_type": "food_option",
        "schema_version": 1,
        "date": "2026-06-23",
        "source": "synthetic_estimate",
        "source_confidence": "low",
        "location_type": "home",
        "provider": "Synthetic provider",
        "item": "Protein bowl",
        "components": ["Synthetic protein", "Synthetic vegetables"],
        "availability": "Now",
        "cost_estimate": {"amount": 10, "currency": "USD", "confidence": "low"},
        "time_and_friction": {"minutes": 12, "friction_notes": ["Synthetic friction"]},
        "nutrition_estimate": {
            "calories": 520,
            "protein_g": 40,
            "fiber_g": 8,
            "sugar_g": 5,
            "sodium_mg": 500,
            "confidence": "low",
        },
        "goal_fit": "strong",
        "enjoyment_fit": "acceptable",
        "satiety_estimate": "strong",
        "tradeoffs": ["Synthetic tradeoff"],
        "stop_condition": "Synthetic stop condition.",
    }
]


HOME_REGISTER = """# Operating Register

## Supply Gaps

| Supply | Domain | Needed For | Consequence if Missing | Next Action | Status |
| --- | --- | --- | --- | --- | --- |
| Synthetic yard bags | Home | Synthetic cleanup | Cleanup stalls | Add to store list | Needed |

## Home and Environment Watchlist

| Area | Condition | Smallest Useful Action | Weather / Tool Dependency | Next Review |
| --- | --- | --- | --- | --- |
| Synthetic garden | Weeds visible | Weed 20 minutes | Dry weather | This week |
"""


ATTENTION_OPTIONS = [
    {
        "artifact_type": "attention_option",
        "schema_version": 1,
        "date": "2026-06-23",
        "event": "Synthetic live event",
        "source": "synthetic_estimate",
        "event_type": "sports",
        "live_value": "medium",
        "personal_importance": "low",
        "recovery_value": "medium",
        "social_or_cultural_value": "medium",
        "opportunity_cost": "Could use the same window for focused work.",
        "multitask_compatibility": "low_cognitive_work",
        "time_window": "Now",
        "best_alternative": "Highlights later.",
        "risk": ["Time drift"],
        "recommendation": "multitask_live",
        "stop_condition": "Synthetic stop condition.",
    }
]


COMPLIANCE_DIRECTIVE = """# Synthetic Directive

Authority level: Level 2

Synthetic action requiring review.
"""


VOICE_MODEL = """# Voice And Taste Model

## Writing Voice

Clear synthetic voice.

## Humor

Understated.

## Intellectual Posture

Practical builder.

## Vocabulary

Avoid: generic self-help.
"""


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PEGOCTL), *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> None:
    help_result = run(["--help"])
    if "check-in" not in help_result.stdout:
        raise AssertionError(help_result.stdout)
    if "guide" not in help_result.stdout:
        raise AssertionError(help_result.stdout)
    if "reconcile-goals" not in help_result.stdout:
        raise AssertionError(help_result.stdout)
    if "review-outcome" not in help_result.stdout:
        raise AssertionError(help_result.stdout)
    if "behavior-loops" not in help_result.stdout:
        raise AssertionError(help_result.stdout)
    if "scenario-benchmarks" not in help_result.stdout:
        raise AssertionError(help_result.stdout)

    doctor = run(["doctor"])
    if "PEGO doctor passed" not in doctor.stdout:
        raise AssertionError(doctor.stdout)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private_root = root / "private"
        readiness = root / "readiness.json"
        queue = root / "queue.md"
        register = root / "register.md"
        session = root / "session.md"
        session_json = root / "session.json"
        brief = root / "brief.md"
        brief_json = root / "brief.json"
        session_review = root / "session-review.md"
        session_review_json = root / "session-review.json"
        promotion_summary = root / "promotion-summary.json"
        context_updates = root / "context-updates"
        response = root / "response.md"
        response_json = root / "response.json"
        preflight = root / "preflight.json"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        run(
            [
                "readiness",
                "--private-root",
                str(private_root),
                "--output",
                str(readiness),
            ]
        )
        readiness_data = json.loads(readiness.read_text())
        if readiness_data["artifact_type"] != "private_instance_readiness":
            raise AssertionError(readiness_data)

        guide = run(
            [
                "guide",
                "--private-root",
                str(private_root),
            ]
        )
        if "PEGO operating guide" not in guide.stdout:
            raise AssertionError(guide.stdout)
        if str(private_root) in guide.stdout:
            raise AssertionError(guide.stdout)

        run(
            [
                "check-in",
                "Breakfast is done. What is next?",
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--session-output",
                str(session),
                "--session-json-output",
                str(session_json),
                "--response-output",
                str(response),
                "--response-json-output",
                str(response_json),
                "--preflight-output",
                str(preflight),
                "--force",
            ]
        )
        session_data = json.loads(session_json.read_text())
        if session_data["artifact_type"] != "intra_day_session_log":
            raise AssertionError(session_data)
        if len(session_data["events"]) != 1:
            raise AssertionError(session_data)

        run(
            [
                "brief",
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--session-json",
                str(session_json),
                "--output",
                str(brief),
                "--json-output",
                str(brief_json),
                "--force",
            ]
        )
        brief_data = json.loads(brief_json.read_text())
        if brief_data["artifact_type"] != "operating_brief":
            raise AssertionError(brief_data)
        if not brief.exists():
            raise AssertionError("expected markdown brief output")

        run(
            [
                "close-session",
                "--date",
                "2026-06-23",
                "--session-json",
                str(session_json),
                "--output",
                str(session_review),
                "--json-output",
                str(session_review_json),
                "--force",
            ]
        )
        review_data = json.loads(session_review_json.read_text())
        if review_data["artifact_type"] != "session_review":
            raise AssertionError(review_data)
        if not session_review.exists():
            raise AssertionError("expected markdown session review output")

        run(
            [
                "promote-context",
                "--date",
                "2026-06-23",
                "--review",
                str(session_review_json),
                "--output-dir",
                str(context_updates),
                "--summary-output",
                str(promotion_summary),
                "--force",
            ]
        )
        promotion_data = json.loads(promotion_summary.read_text())
        if promotion_data["artifact_type"] != "session_context_promotion":
            raise AssertionError(promotion_data)

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        (private_root / "directives" / "queues").mkdir(parents=True)
        (private_root / "operator").mkdir(parents=True)
        (private_root / "directives" / "queues" / "2026-06-23-queue.md").write_text(QUEUE)
        (private_root / "operator" / "operating-register.md").write_text(REGISTER)
        run(
            [
                "--private-root",
                str(private_root),
                "check-in",
                "Breakfast is done. What is next?",
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
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
        if not (private_root / "operator" / "sessions" / "2026-06-23-user-mode.json").exists():
            raise AssertionError("expected pegoctl check-in session under configured private root")
        if not (private_root / "directives" / "command-responses" / "2026-06-23-next.json").exists():
            raise AssertionError("expected pegoctl command response under configured private root")

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        (private_root / "health").mkdir(parents=True)
        (private_root / "finance").mkdir(parents=True)
        (private_root / "operator").mkdir(parents=True)
        (private_root / "directives" / "candidates").mkdir(parents=True)
        (private_root / "health" / "baseline.json").write_text(
            json.dumps(
                {
                    "artifact_type": "health_baseline",
                    "schema_version": 1,
                    "evidence_policy": {"tracking_level": "minimal"},
                    "goal": {},
                    "constraints": {},
                    "preferences": {},
                    "current_routine": {},
                    "availability": {},
                    "metrics": {},
                }
            )
        )
        (private_root / "operator" / "operating-register.md").write_text(REGISTER)
        run(
            [
                "--private-root",
                str(private_root),
                "daily",
                "health-check-in",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if not (private_root / "health" / "check-ins" / "health-check-in.md").exists():
            raise AssertionError("expected pegoctl daily output under configured private root")

        run(
            [
                "--private-root",
                str(private_root),
                "weekly",
                "--week",
                "2026-W26",
                "--force",
            ]
        )
        if not (private_root / "directives" / "weekly" / "2026-W26.md").exists():
            raise AssertionError("expected pegoctl weekly output under configured private root")

        run(
            [
                "--private-root",
                str(private_root),
                "monthly",
                "--month",
                "2026-06",
                "--force",
            ]
        )
        if not (private_root / "directives" / "monthly" / "2026-06-strategy-review.json").exists():
            raise AssertionError("expected pegoctl monthly output under configured private root")

        run(
            [
                "--private-root",
                str(private_root),
                "reconcile-goals",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if not (private_root / "goals" / "goal-reconciliation.json").exists():
            raise AssertionError("expected pegoctl goal reconciliation under configured private root")

        state_signal = private_root / "telemetry" / "signals" / "synthetic-health.json"
        run(
            [
                "--private-root",
                str(private_root),
                "state-signal",
                "--date",
                "2026-06-23",
                "--observed-at",
                "2026-06-23T09:15:00",
                "--source-type",
                "wearable_activity",
                "--ingestion-mode",
                "import",
                "--domain",
                "health",
                "--signal-type",
                "activity",
                "--summary",
                "Synthetic activity summary for CLI routing.",
                "--measurement",
                "active_minutes=20,minutes,today,higher_is_better",
                "--affected-goal",
                "Synthetic health consistency",
                "--output",
                str(state_signal),
                "--force",
            ]
        )
        if not state_signal.exists():
            raise AssertionError("expected pegoctl state-signal output under configured private root")
        state_signal_data = json.loads(state_signal.read_text())
        if state_signal_data["privacy_class"] != "sensitive_health":
            raise AssertionError(state_signal_data)

        run(
            [
                "--private-root",
                str(private_root),
                "goal-progress",
                "--date",
                "2026-06-23",
                "--signal",
                str(state_signal),
                "--force",
            ]
        )
        goal_progress = private_root / "goals" / "progress" / "health.json"
        if not goal_progress.exists():
            raise AssertionError("expected pegoctl goal-progress output under configured private root")
        goal_progress_data = json.loads(goal_progress.read_text())
        if goal_progress_data["artifact_type"] != "goal_progress":
            raise AssertionError(goal_progress_data)

        run(
            [
                "--private-root",
                str(private_root),
                "behavior-loops",
                "--date",
                "2026-06-23",
                "--state-signal",
                str(state_signal),
                "--force",
            ]
        )
        behavior_summary = private_root / "behavior-loops" / "detection-summary.json"
        if not behavior_summary.exists():
            raise AssertionError("expected pegoctl behavior-loop detection summary")
        behavior_data = json.loads(behavior_summary.read_text())
        if behavior_data["artifact_type"] != "behavior_loop_detection_summary":
            raise AssertionError(behavior_data)

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        finance_input = private_root / "finance" / "scenarios.json"
        finance_input.parent.mkdir(parents=True)
        finance_input.write_text(json.dumps(FINANCE_SCENARIOS))
        run(
            [
                "--private-root",
                str(private_root),
                "finance-run",
                "--write-summary",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "finance-review",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if not (private_root / "_local" / "finance" / "scenario-output.json").exists():
            raise AssertionError("expected pegoctl finance-run output under configured private root")
        if not (private_root / "finance" / "reviews" / "scenario-review.md").exists():
            raise AssertionError("expected pegoctl finance-review output under configured private root")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        benchmark_md = root / "scenario-benchmark.md"
        benchmark_json = root / "scenario-benchmark.json"
        run(
            [
                "scenario-benchmarks",
                "--date",
                "2026-06-23",
                "--output",
                str(benchmark_md),
                "--json-output",
                str(benchmark_json),
                "--force",
            ]
        )
        if not benchmark_json.exists():
            raise AssertionError("expected pegoctl scenario benchmark output")
        benchmark_data = json.loads(benchmark_json.read_text())
        if benchmark_data["artifact_type"] != "scenario_benchmark":
            raise AssertionError(benchmark_data)

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        baseline = private_root / "health" / "baseline.json"
        food_options = private_root / "health" / "food-options" / "options.json"
        register = private_root / "operator" / "operating-register.md"
        baseline.parent.mkdir(parents=True)
        food_options.parent.mkdir(parents=True)
        register.parent.mkdir(parents=True)
        baseline.write_text(json.dumps(HEALTH_BASELINE))
        food_options.write_text(json.dumps(FOOD_OPTIONS))
        register.write_text(HOME_REGISTER)
        run(
            [
                "--private-root",
                str(private_root),
                "health-candidates",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "meal",
                "--date",
                "2026-06-23",
                "--meal",
                "Lunch",
                "--option",
                str(food_options),
                "--strategy",
                "weight_loss",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "home-candidates",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if not (private_root / "directives" / "candidates" / "health-candidates.md").exists():
            raise AssertionError("expected pegoctl health candidates under configured private root")
        if not (private_root / "health" / "meal-decisions" / "meal-decision.md").exists():
            raise AssertionError("expected pegoctl meal decision under configured private root")
        if not (private_root / "directives" / "candidates" / "meal-candidate.md").exists():
            raise AssertionError("expected pegoctl meal candidate under configured private root")
        if not (private_root / "directives" / "candidates" / "home-candidates.md").exists():
            raise AssertionError("expected pegoctl home candidates under configured private root")

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        register = private_root / "operator" / "operating-register.md"
        attention_options = private_root / "attention" / "options" / "options.json"
        register.parent.mkdir(parents=True)
        attention_options.parent.mkdir(parents=True)
        register.write_text(HOME_REGISTER)
        attention_options.write_text(json.dumps(ATTENTION_OPTIONS))
        run(
            [
                "--private-root",
                str(private_root),
                "anticipate",
                "--date",
                "2026-06-23",
                "--domain",
                "Environment",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "attention",
                "--date",
                "2026-06-23",
                "--option",
                str(attention_options),
                "--force",
            ]
        )
        if not (private_root / "anticipation" / "scans" / "2026-06-23-synthetic-garden.md").exists():
            raise AssertionError("expected pegoctl anticipation scan under configured private root")
        if not (private_root / "attention" / "decisions" / "attention-decision.md").exists():
            raise AssertionError("expected pegoctl attention decision under configured private root")
        if not (private_root / "directives" / "candidates" / "attention-candidate.md").exists():
            raise AssertionError("expected pegoctl attention candidate under configured private root")

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        directive = Path(directory) / "directive.md"
        (private_root / "time").mkdir(parents=True)
        (private_root / "person").mkdir(parents=True)
        (private_root / "time" / "protected-time.md").write_text("Synthetic protected time.")
        (private_root / "person" / "voice-and-taste.md").write_text(VOICE_MODEL)
        directive.write_text(COMPLIANCE_DIRECTIVE)
        run(
            [
                "--private-root",
                str(private_root),
                "intake",
                "--date",
                "2026-06-23",
                "--phase",
                "boundary",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "public-writing",
                "--date",
                "2026-06-23",
                "--artifact",
                "Synthetic public essay",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "daily-directive",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        run(
            [
                "--private-root",
                str(private_root),
                "compliance-review",
                "--directive",
                str(directive),
                "--date",
                "2026-06-23",
                "--slug",
                "synthetic-directive",
                "--force",
            ]
        )
        if not (private_root / "onboarding" / "intake" / "2026-06-23-boundary.md").exists():
            raise AssertionError("expected pegoctl intake under configured private root")
        if not (private_root / "directives" / "daily" / "2026-06-23.md").exists():
            raise AssertionError("expected pegoctl daily directive under configured private root")
        if not (private_root / "governance" / "reviews" / "2026-06-23-synthetic-directive.md").exists():
            raise AssertionError("expected pegoctl compliance review under configured private root")
        if not (private_root / "writing" / "briefs" / "2026-06-23-synthetic-public-essay.md").exists():
            raise AssertionError("expected pegoctl public-writing brief under configured private root")
        if not (private_root / "directives" / "candidates" / "communications-candidates.md").exists():
            raise AssertionError("expected pegoctl communications candidate under configured private root")

    print("pegoctl smoke tests passed.")


if __name__ == "__main__":
    main()
