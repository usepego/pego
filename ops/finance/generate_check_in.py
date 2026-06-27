#!/usr/bin/env python3
"""Generate a targeted PEGO finance check-in from private scenario assumptions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import private_root as private_root_config  # noqa: E402
REQUIRED_SCENARIOS = {"conservative", "base", "upside", "stress", "lifestyle_upgrade"}


@dataclass(frozen=True)
class Question:
    question: str
    signal: str
    decision_use: str
    required: bool = True


def privacy_rule() -> str:
    return (
        "Ask for private financial values only inside the protected private instance, "
        "and only when the answer changes a directive, scenario, governance gate, or strategy review."
    )


def scenario_names(config: dict) -> set[str]:
    return {str(scenario.get("name", "")) for scenario in config.get("scenarios", [])}


def has_value(values: dict, key: str) -> bool:
    value = values.get(key)
    return value not in ("", None, [], {})


def build_questions(config: dict) -> list[Question]:
    current_position = config.get("current_position", {})
    global_assumptions = config.get("global_assumptions", {})
    names = scenario_names(config)
    missing = sorted(REQUIRED_SCENARIOS - names)

    questions = [
        Question(
            "Has income, recurring burn, savings rate, or any large expected expense changed since the last finance scenario input?",
            "assumption",
            "Determines whether PEGO must update scenarios before finance, career, venture, or spending directives.",
        ),
        Question(
            "Is there any upcoming spending, renovation, travel, tax, insurance, debt, or account decision that needs lead-time review?",
            "decision",
            "Creates a finance/admin directive or escalation packet before the decision becomes urgent.",
        ),
        Question(
            "Are the private account and balance inputs current enough for runway decisions, or should PEGO request an account-data refresh?",
            "account_data",
            "Determines whether low-risk planning can proceed or whether scenario outputs are stale.",
        ),
    ]

    if missing:
        questions.append(
            Question(
                "Can PEGO add or update the missing required scenarios: " + ", ".join(missing) + "?",
                "assumption",
                "Restores scenario coverage before finance directives rely on the model.",
            )
        )

    if has_value(current_position, "liquid_savings"):
        questions.append(
            Question(
                "Has liquid runway materially changed, or is the emergency-runway target still appropriate?",
                "runway",
                "Determines whether PEGO should prioritize runway protection over discretionary or venture directives.",
                required=False,
            )
        )
    else:
        questions.append(
            Question(
                "Is liquid runway known in the protected private model, or should PEGO avoid runway-dependent directives?",
                "runway",
                "Prevents PEGO from making finance recommendations without liquidity context.",
            )
        )

    if has_value(global_assumptions, "target_date"):
        questions.append(
            Question(
                "Has the target date, longevity assumption, inflation assumption, or return assumption changed materially?",
                "assumption",
                "Determines whether the financial freedom model needs to be rerun before strategy decisions.",
                required=False,
            )
        )

    if has_value(global_assumptions, "social_security_monthly_estimate"):
        questions.append(
            Question(
                "Should scenarios that depend on Social Security or pension offsets remain allowed, or should PEGO treat them as upside only?",
                "risk",
                "Controls governance flags for assumptions that may overstate safety.",
                required=False,
            )
        )

    return questions


def build_artifact(config: dict, output_date: str) -> dict[str, object]:
    return {
        "artifact_type": "finance_check_in",
        "schema_version": 1,
        "date": output_date,
        "purpose": "Collect only the finance state needed to update scenarios, classify risk, or choose safe finance-related directives.",
        "privacy_rule": privacy_rule(),
        "questions": [
            {
                "question": question.question,
                "signal": question.signal,
                "decision_use": question.decision_use,
                "required": question.required,
            }
            for question in build_questions(config)
        ],
        "privacy_status": "protected_private_instance",
        "next_step": "Record answers under protected private finance state or the current session log, then rerun scenario generation or scenario review if assumptions changed.",
    }


def build_markdown(config: dict, output_date: str) -> str:
    artifact = build_artifact(config, output_date)
    rows = [
        f"| {question['question']} | {question['signal']} | {question['decision_use']} | {'Yes' if question['required'] else 'No'} |"
        for question in artifact["questions"]
    ]
    return "\n".join(
        [
            f"# Finance Check-In: {output_date}",
            "",
            "## Date",
            "",
            str(artifact["date"]),
            "",
            "## Purpose",
            "",
            str(artifact["purpose"]),
            "",
            "## Privacy Rule",
            "",
            str(artifact["privacy_rule"]),
            "",
            "## Questions",
            "",
            "| Question | Signal | Decision Use | Required |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
            "## Do Not Ask",
            "",
            "- Broad money reflection.",
            "- Account balances or holdings unless the protected private destination is clear.",
            "- Trade, transfer, or allocation instructions without governance review.",
            "- Public or third-party disclosure of private financial facts.",
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
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
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
    private = private_root_config.resolve_private_root(args.private_root)
    args.input = args.input or private / "finance" / "scenarios.json"
    args.output = args.output or private / "finance" / "check-ins" / "finance-check-in.md"
    if not args.input.is_file():
        raise SystemExit(f"missing finance scenario input: {args.input}")
    config = json.loads(args.input.read_text())
    write_output(args.output, build_markdown(config, args.date), args.force)
    print(f"wrote: {args.output}")
    if args.json_output:
        artifact = build_artifact(config, args.date)
        write_output(
            args.json_output,
            json.dumps(artifact, indent=2, sort_keys=True) + "\n",
            args.force,
        )
        print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
