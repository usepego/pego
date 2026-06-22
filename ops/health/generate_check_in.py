#!/usr/bin/env python3
"""Generate a targeted PEGO health check-in from a private baseline."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_INPUT = Path("private/health/baseline.json")
DEFAULT_OUTPUT = Path("private/health/check-ins/health-check-in.md")


@dataclass(frozen=True)
class Question:
    question: str
    signal: str
    decision_use: str
    required: bool = True


def minutes(value: object) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def has_values(values: object) -> bool:
    if not isinstance(values, dict):
        return False
    return any(value not in ("", None, [], {}) for value in values.values())


def measurement_rule(baseline: dict) -> str:
    policy = baseline.get("evidence_policy", {})
    rule = policy.get("measurement_rule")
    if isinstance(rule, str) and rule.strip():
        return rule.strip()
    return "Ask for new metrics only when they change a directive, risk classification, escalation, or strategy review."


def tracking_level(baseline: dict) -> str:
    level = baseline.get("evidence_policy", {}).get("tracking_level", "minimal")
    return str(level)


def build_questions(baseline: dict) -> list[Question]:
    routine = baseline.get("current_routine", {})
    preferences = baseline.get("preferences", {})
    availability = baseline.get("availability", {})
    constraints = baseline.get("constraints", {})
    metrics = baseline.get("metrics", {})

    questions = [
        Question(
            "How did you sleep last night: duration, quality, and anything that materially changed recovery?",
            "sleep",
            "Sets movement intensity, food conservatism, and whether recovery should outrank optional tasks.",
        ),
        Question(
            "What is the next realistic meal window, and is an approved food default available?",
            "food",
            "Chooses the next food directive and prevents reactive snacking.",
        ),
        Question(
            "Are hunger, cravings, or sweet triggers active right now?",
            "hunger",
            "Determines whether PEGO should issue a food-default, environment, or delay directive.",
        ),
        Question(
            "Did the last movement directive happen, and is there any pain, injury, illness, or unsafe condition today?",
            "movement",
            "Decides whether to repeat, reduce, defer, or escalate movement.",
        ),
    ]

    if not routine.get("breakfast"):
        questions.append(
            Question(
                "What did you actually eat or drink first today?",
                "food",
                "Updates the baseline before changing breakfast directives.",
                required=False,
            )
        )

    if preferences.get("sweet_triggers"):
        questions.append(
            Question(
                "Which known sweet trigger is most likely in the next six hours?",
                "environment",
                "Lets PEGO remove or route around the highest-friction cue.",
                required=False,
            )
        )

    available_minutes = (
        minutes(availability.get("morning_minutes"))
        + minutes(availability.get("midday_minutes"))
        + minutes(availability.get("evening_minutes"))
    )
    if available_minutes <= 10:
        questions.append(
            Question(
                "What is the smallest movement window available today, even if it is only five minutes?",
                "movement",
                "Prevents PEGO from issuing a directive that does not fit the day.",
                required=False,
            )
        )

    if constraints.get("medical_constraints") or constraints.get("injuries"):
        questions.append(
            Question(
                "Has any medical constraint, symptom, injury, medication, or clinician instruction changed since the last check-in?",
                "constraint",
                "Determines whether health directives must remain conservative or escalate.",
            )
        )

    glucose = metrics.get("glucose", {})
    if has_values(glucose):
        questions.append(
            Question(
                "Is there any already-available glucose or A1C context that should change today's food or movement conservatism?",
                "metric",
                "Uses existing glucose evidence as context without requiring new tracking.",
                required=False,
            )
        )
    elif tracking_level(baseline) != "minimal":
        questions.append(
            Question(
                "Is blood sugar or A1C already known and relevant, or should PEGO ignore glucose for now?",
                "metric",
                "Determines whether glucose belongs in the current health model without creating a daily tracking burden.",
                required=False,
            )
        )

    return questions


def build_artifact(baseline: dict, output_date: str) -> dict[str, object]:
    return {
        "artifact_type": "health_check_in",
        "schema_version": 1,
        "date": output_date,
        "purpose": "Collect only the health state needed to choose safe near-term food, movement, sleep, and recovery directives.",
        "measurement_rule": measurement_rule(baseline),
        "questions": [
            {
                "question": question.question,
                "signal": question.signal,
                "decision_use": question.decision_use,
                "required": question.required,
            }
            for question in build_questions(baseline)
        ],
        "privacy_status": "protected_private_instance",
        "next_step": "Record answers under protected private health state or the current session log, then regenerate health candidates if directive selection changes.",
    }


def build_markdown(baseline: dict, output_date: str) -> str:
    artifact = build_artifact(baseline, output_date)
    rows = [
        f"| {question['question']} | {question['signal']} | {question['decision_use']} | {'Yes' if question['required'] else 'No'} |"
        for question in artifact["questions"]
    ]
    return "\n".join(
        [
            f"# Health Check-In: {output_date}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Purpose",
            "",
            str(artifact["purpose"]),
            "",
            "## Measurement Rule",
            "",
            str(artifact["measurement_rule"]),
            "",
            "## Questions",
            "",
            "| Question | Signal | Decision Use | Required |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
            "## Do Not Ask",
            "",
            "- Broad self-help reflection.",
            "- New biomarker tracking without a decision reason.",
            "- Medical interpretation that requires clinician review.",
            "",
            "## Privacy Status",
            "",
            "Protected private instance.",
            "",
            "## Next Step",
            "",
            str(artifact["next_step"]),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.input.is_file():
        raise SystemExit(f"missing health baseline: {args.input}")
    baseline = json.loads(args.input.read_text())
    write_output(args.output, build_markdown(baseline, args.date), args.force)
    print(f"wrote: {args.output}")
    if args.json_output:
        artifact = build_artifact(baseline, args.date)
        write_output(
            args.json_output,
            json.dumps(artifact, indent=2, sort_keys=True) + "\n",
            args.force,
        )
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
