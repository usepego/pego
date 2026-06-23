#!/usr/bin/env python3
"""Select a PEGO attention directive from protected attention options."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_OUTPUT = Path("private/attention/decisions/attention-decision.md")
DEFAULT_CANDIDATE_OUTPUT = Path("private/directives/candidates/attention-candidate.md")

LEVEL_SCORE = {"high": 0, "medium": 1, "unknown": 2, "low": 3}
RECOMMENDATION_DIRECTIVE = {
    "watch_live": "Watch live with full attention.",
    "multitask_live": "Watch live while doing only low-cognitive work.",
    "highlights_later": "Skip live viewing and watch highlights later.",
    "score_only": "Check the score or outcome only.",
    "defer": "Defer to a scheduled leisure block.",
    "skip": "Skip this event.",
    "escalate": "Escalate before deciding.",
}


@dataclass(frozen=True)
class AttentionOption:
    event: str
    recommendation: str
    live_value: str
    personal_importance: str
    recovery_value: str
    social_or_cultural_value: str
    multitask_compatibility: str
    opportunity_cost: str
    best_alternative: str
    risk: list[str]
    stop_condition: str


def normalize_level(value: object) -> str:
    raw = str(value or "unknown").lower().strip()
    return raw if raw in LEVEL_SCORE else "unknown"


def read_options(paths: list[Path]) -> list[AttentionOption]:
    options: list[AttentionOption] = []
    for path in paths:
        data = json.loads(path.read_text())
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict) or item.get("artifact_type") != "attention_option":
                continue
            options.append(
                AttentionOption(
                    event=str(item.get("event", "")),
                    recommendation=str(item.get("recommendation", "skip")),
                    live_value=normalize_level(item.get("live_value")),
                    personal_importance=normalize_level(item.get("personal_importance")),
                    recovery_value=normalize_level(item.get("recovery_value")),
                    social_or_cultural_value=normalize_level(item.get("social_or_cultural_value")),
                    multitask_compatibility=str(item.get("multitask_compatibility", "unknown")),
                    opportunity_cost=str(item.get("opportunity_cost", "")),
                    best_alternative=str(item.get("best_alternative", "")),
                    risk=[str(value) for value in item.get("risk", []) if str(value).strip()],
                    stop_condition=str(item.get("stop_condition", "")),
                )
            )
    return options


def option_score(option: AttentionOption) -> tuple[int, int, int, int]:
    if option.recommendation == "escalate":
        return (-1, 0, 0, 0)
    if option.recommendation == "skip":
        recommendation_penalty = 5
    elif option.recommendation == "score_only":
        recommendation_penalty = 4
    elif option.recommendation == "highlights_later":
        recommendation_penalty = 3
    elif option.recommendation == "multitask_live":
        recommendation_penalty = 1
    else:
        recommendation_penalty = 0
    return (
        recommendation_penalty,
        LEVEL_SCORE[option.live_value] + LEVEL_SCORE[option.personal_importance],
        LEVEL_SCORE[option.recovery_value],
        LEVEL_SCORE[option.social_or_cultural_value],
    )


def choose_option(options: list[AttentionOption]) -> AttentionOption:
    if not options:
        raise SystemExit("at least one --option attention option file is required")
    return sorted(options, key=option_score)[0]


def build_decision(option: AttentionOption, options: list[AttentionOption], args: argparse.Namespace) -> dict[str, object]:
    directive = RECOMMENDATION_DIRECTIVE.get(option.recommendation, "Skip this event.")
    if option.recommendation in {"watch_live", "multitask_live"}:
        directive = f"{directive} Event: {option.event}."
    return {
        "artifact_type": "attention_decision",
        "schema_version": 1,
        "date": args.date,
        "context": args.context,
        "event": option.event,
        "options_considered": [f"{item.event}: {item.recommendation}" for item in options],
        "selected_directive": directive,
        "rationale": "Selected by comparing live value, personal importance, recovery value, social/cultural value, and opportunity cost.",
        "tradeoffs": [
            f"Opportunity cost: {option.opportunity_cost or 'Unknown'}",
            f"Best alternative: {option.best_alternative or 'None recorded'}",
            f"Risks: {'; '.join(option.risk) if option.risk else 'None recorded'}",
        ],
        "follow_up": args.follow_up,
        "governance_status": "Level 1 attention recommendation unless protected time, obligations, safety, or compulsive pattern risk appears.",
        "review_question": args.review_question,
    }


def build_markdown(decision: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Attention Decision: {decision['date']}",
            "",
            "## Context",
            "",
            str(decision["context"]),
            "",
            "## Event",
            "",
            str(decision["event"]),
            "",
            "## Options Considered",
            "",
            *[f"- {item}" for item in decision["options_considered"]],
            "",
            "## Selected Directive",
            "",
            str(decision["selected_directive"]),
            "",
            "## Rationale",
            "",
            str(decision["rationale"]),
            "",
            "## Tradeoffs",
            "",
            *[f"- {item}" for item in decision["tradeoffs"]],
            "",
            "## Follow-Up",
            "",
            str(decision["follow_up"]),
            "",
            "## Governance Status",
            "",
            str(decision["governance_status"]),
            "",
            "## Review Question",
            "",
            str(decision["review_question"]),
            "",
        ]
    )


def build_candidate(decision: dict[str, object]) -> dict[str, object]:
    return {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": f"Attention: {decision['event']}",
        "domain": "happiness",
        "altitude": "directive",
        "proposed_action": str(decision["selected_directive"]),
        "target_behavior": "Turn live attention into an intentional allocation instead of passive drift.",
        "environment_design": "Pre-classify the event and viewing mode before the attention window is consumed by default.",
        "duration": "30 min",
        "timing": "Current attention window",
        "energy_required": "low",
        "location_required": "home",
        "dependencies": ["Event remains available."],
        "expected_benefit": str(decision["rationale"]),
        "consequence_of_deferral": "Attention may drift reactively instead of being governed deliberately.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "reviewed",
        "conflicts": [],
        "stop_condition": "Stop if protected time, sleep, work obligations, or compulsive viewing risk appears.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--option", type=Path, action="append", default=[])
    parser.add_argument("--context", default="Current attention window.")
    parser.add_argument("--follow-up", default="Record whether this restored energy, created drift, or should be pre-classified next time.")
    parser.add_argument("--review-question", default="Was this worth live attention, or would highlights have been enough?")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--candidate-output", type=Path, default=DEFAULT_CANDIDATE_OUTPUT)
    parser.add_argument("--candidate-json-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)
    print(f"wrote: {path}")


def main_with_args(argv: list[str] | None = None) -> dict[str, object]:
    parser = build_parser()
    args = parser.parse_args(argv)
    options = read_options(args.option)
    selected = choose_option(options)
    decision = build_decision(selected, options, args)
    candidate = build_candidate(decision)
    write_output(args.output, build_markdown(decision), args.force)
    if args.json_output:
        write_output(args.json_output, json.dumps(decision, indent=2, sort_keys=True) + "\n", args.force)
    write_output(args.candidate_output, build_markdown_candidate(candidate), args.force)
    if args.candidate_json_output:
        write_output(args.candidate_json_output, json.dumps(candidate, indent=2, sort_keys=True) + "\n", args.force)
    return decision


def build_markdown_candidate(candidate: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Directive Candidate: {candidate['candidate']}",
            "",
            "## Candidate",
            "",
            str(candidate["candidate"]),
            "",
            "## Domain",
            "",
            "Happiness",
            "",
            "## Altitude",
            "",
            "Directive",
            "",
            "## Proposed Action",
            "",
            str(candidate["proposed_action"]),
            "",
            "## Target Behavior",
            "",
            str(candidate["target_behavior"]),
            "",
            "## Environment Design",
            "",
            str(candidate["environment_design"]),
            "",
            "## Duration",
            "",
            str(candidate["duration"]),
            "",
            "## Timing",
            "",
            str(candidate["timing"]),
            "",
            "## Energy Required",
            "",
            "Low",
            "",
            "## Location Required",
            "",
            "Home",
            "",
            "## Dependencies",
            "",
            "- Event remains available.",
            "",
            "## Expected Benefit",
            "",
            str(candidate["expected_benefit"]),
            "",
            "## Consequence of Deferral",
            "",
            str(candidate["consequence_of_deferral"]),
            "",
            "## Protected-Time Impact",
            "",
            "None",
            "",
            "## Authority Level",
            "",
            "Level 1",
            "",
            "## Governance Status",
            "",
            "Reviewed",
            "",
            "## Conflicts",
            "",
            "- None.",
            "",
            "## Stop Condition",
            "",
            str(candidate["stop_condition"]),
            "",
        ]
    )


if __name__ == "__main__":
    main_with_args()
