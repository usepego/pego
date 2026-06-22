#!/usr/bin/env python3
"""Select a PEGO meal directive from protected food options."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_OUTPUT = Path("private/health/meal-decisions/meal-decision.md")
DEFAULT_CANDIDATE_OUTPUT = Path("private/directives/candidates/meal-candidate.md")

FIT_SCORE = {
    "strong": 0,
    "acceptable": 1,
    "unknown": 2,
    "weak": 3,
    "poor": 4,
}


@dataclass(frozen=True)
class FoodOption:
    source: str
    provider: str
    item: str
    calories: float | None
    protein_g: float | None
    fiber_g: float | None
    sugar_g: float | None
    sodium_mg: float | None
    minutes: int | None
    cost: float | None
    goal_fit: str
    enjoyment_fit: str
    satiety_estimate: str
    tradeoffs: list[str]
    stop_condition: str
    raw: dict[str, object]


def normalize_fit(value: object) -> str:
    normalized = str(value or "unknown").strip().lower()
    return normalized if normalized in FIT_SCORE else "unknown"


def number_or_none(value: object) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def read_options(paths: list[Path]) -> list[FoodOption]:
    options: list[FoodOption] = []
    for path in paths:
        data = json.loads(path.read_text())
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict) or item.get("artifact_type") != "food_option":
                continue
            nutrition = item.get("nutrition_estimate", {})
            friction = item.get("time_and_friction", {})
            cost = item.get("cost_estimate", {})
            options.append(
                FoodOption(
                    source=str(path),
                    provider=str(item.get("provider", "")),
                    item=str(item.get("item", "")),
                    calories=number_or_none(nutrition.get("calories")) if isinstance(nutrition, dict) else None,
                    protein_g=number_or_none(nutrition.get("protein_g")) if isinstance(nutrition, dict) else None,
                    fiber_g=number_or_none(nutrition.get("fiber_g")) if isinstance(nutrition, dict) else None,
                    sugar_g=number_or_none(nutrition.get("sugar_g")) if isinstance(nutrition, dict) else None,
                    sodium_mg=number_or_none(nutrition.get("sodium_mg")) if isinstance(nutrition, dict) else None,
                    minutes=int(friction["minutes"]) if isinstance(friction, dict) and isinstance(friction.get("minutes"), int) else None,
                    cost=number_or_none(cost.get("amount")) if isinstance(cost, dict) else None,
                    goal_fit=normalize_fit(item.get("goal_fit")),
                    enjoyment_fit=normalize_fit(item.get("enjoyment_fit")),
                    satiety_estimate=normalize_fit(item.get("satiety_estimate")),
                    tradeoffs=[str(value) for value in item.get("tradeoffs", []) if str(value).strip()],
                    stop_condition=str(item.get("stop_condition", "")),
                    raw=item,
                )
            )
    return options


def calorie_component(option: FoodOption, strategy: str) -> float:
    calories = option.calories if option.calories is not None else 700
    if strategy in {"weight_gain", "muscle_gain", "appetite_recovery"}:
        return -calories
    if strategy in {"performance"}:
        return abs(calories - 750)
    if strategy in {"maintenance", "balanced"}:
        return abs(calories - 600)
    return calories


def macro_component(option: FoodOption, strategy: str) -> float:
    protein_bonus = -(option.protein_g or 0)
    fiber_bonus = -(option.fiber_g or 0)
    if strategy in {"weight_gain", "muscle_gain", "performance", "appetite_recovery"}:
        return protein_bonus
    if strategy in {"metabolic_stability", "weight_loss", "balanced", "maintenance"}:
        return protein_bonus + fiber_bonus
    return protein_bonus + fiber_bonus


def score(option: FoodOption, strategy: str) -> tuple[int, float, float, int, float]:
    time_penalty = option.minutes if option.minutes is not None else 30
    return (
        FIT_SCORE[option.goal_fit] + FIT_SCORE[option.satiety_estimate],
        calorie_component(option, strategy),
        macro_component(option, strategy),
        time_penalty,
        option.cost if option.cost is not None else 20,
    )


def choose_option(options: list[FoodOption], strategy: str) -> FoodOption:
    if not options:
        raise SystemExit("at least one food option is required")
    return sorted(options, key=lambda option: score(option, strategy))[0]


def option_label(option: FoodOption) -> str:
    provider = f"{option.provider}: " if option.provider else ""
    return f"{provider}{option.item}"


def split_recent_food(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def build_decision(options: list[FoodOption], selected: FoodOption, args: argparse.Namespace) -> dict[str, object]:
    rejected = [
        f"{option_label(option)}: lower fit for current goal, satiety, time, or calorie tradeoff."
        for option in options
        if option is not selected
    ]
    return {
        "artifact_type": "meal_decision",
        "schema_version": 1,
        "date": args.date,
        "meal_window": args.meal,
        "current_context": {
            "hunger": args.hunger,
            "energy": args.energy,
            "location": args.location,
            "schedule": args.schedule,
            "recent_food": split_recent_food(args.recent_food),
            "constraints": split_recent_food(args.constraints),
        },
        "goal_context": args.goal_context,
        "nutrition_strategy": args.strategy,
        "available_options": [option_label(option) for option in options],
        "selected_directive": f"Eat {option_label(selected)}.",
        "rationale": f"Best current balance of goal fit, satiety, time friction, and estimated nutrition among available options.",
        "tradeoffs": selected.tradeoffs,
        "rejected_options": rejected,
        "follow_up": args.follow_up,
        "governance_status": "Level 1 food recommendation using imperfect nutrition estimates.",
        "stop_condition": selected.stop_condition or "Stop if this conflicts with medical advice, protected time, or significant aversion.",
        "review_question": "After eating, was hunger controlled and did this create later cravings or friction?",
    }


def build_markdown(decision: dict[str, object]) -> str:
    current = decision["current_context"]
    assert isinstance(current, dict)
    return "\n".join(
        [
            f"# Meal Decision: {decision['date']} {decision['meal_window']}",
            "",
            "## Date",
            "",
            str(decision["date"]),
            "",
            "## Current Context",
            "",
            f"- Hunger: {current['hunger']}",
            f"- Energy: {current['energy']}",
            f"- Location: {current['location']}",
            f"- Schedule: {current['schedule']}",
            f"- Recent food: {'; '.join(current['recent_food']) if current['recent_food'] else 'Unknown'}",
            f"- Constraints: {'; '.join(current['constraints']) if current['constraints'] else 'None recorded'}",
            "",
            "## Goal Context",
            "",
            str(decision["goal_context"]),
            "",
            "## Nutrition Strategy",
            "",
            str(decision["nutrition_strategy"]),
            "",
            "## Available Options",
            "",
            *[f"- {item}" for item in decision["available_options"]],
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
            *([f"- {item}" for item in decision["tradeoffs"]] or ["- None recorded."]),
            "",
            "## Rejected Options",
            "",
            *([f"- {item}" for item in decision["rejected_options"]] or ["- None."]),
            "",
            "## Follow-Up",
            "",
            str(decision["follow_up"]),
            "",
            "## Governance Status",
            "",
            str(decision["governance_status"]),
            "",
            "## Stop Condition",
            "",
            str(decision["stop_condition"]),
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
        "candidate": f"Meal: {decision['meal_window']}",
        "domain": "health",
        "altitude": "directive",
        "proposed_action": str(decision["selected_directive"]),
        "duration": "20 min",
        "timing": str(decision["meal_window"]),
        "energy_required": "low",
        "location_required": "home",
        "dependencies": ["Food option remains available."],
        "expected_benefit": str(decision["rationale"]),
        "consequence_of_deferral": "Reactive food choice may become more likely.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "reviewed",
        "conflicts": [],
        "stop_condition": str(decision["stop_condition"]),
    }


def candidate_markdown(candidate: dict[str, object]) -> str:
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
            "Health",
            "",
            "## Altitude",
            "",
            "Directive",
            "",
            "## Proposed Action",
            "",
            str(candidate["proposed_action"]),
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
            "- Food option remains available.",
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--meal", default="Next meal")
    parser.add_argument("--option", type=Path, action="append", default=[])
    parser.add_argument("--hunger", default="Unknown")
    parser.add_argument("--energy", choices=["low", "medium", "high", "unknown"], default="unknown")
    parser.add_argument("--location", default="Unknown")
    parser.add_argument("--schedule", default="Unknown")
    parser.add_argument("--recent-food", default="")
    parser.add_argument("--constraints", default="")
    parser.add_argument(
        "--strategy",
        choices=[
            "weight_loss",
            "weight_gain",
            "maintenance",
            "muscle_gain",
            "performance",
            "metabolic_stability",
            "appetite_recovery",
            "balanced",
        ],
        default="balanced",
    )
    parser.add_argument("--goal-context", default="Support the current nutrition strategy with a satisfying, lower-friction meal.")
    parser.add_argument("--follow-up", default="Record whether hunger, satisfaction, energy, or cravings changed.")
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
    if not args.option:
        raise SystemExit("at least one --option food option file is required")
    options = read_options(args.option)
    selected = choose_option(options, args.strategy)
    decision = build_decision(options, selected, args)
    candidate = build_candidate(decision)
    write_output(args.output, build_markdown(decision), args.force)
    if args.json_output:
        write_output(args.json_output, json.dumps(decision, indent=2, sort_keys=True) + "\n", args.force)
    write_output(args.candidate_output, candidate_markdown(candidate), args.force)
    if args.candidate_json_output:
        write_output(args.candidate_json_output, json.dumps(candidate, indent=2, sort_keys=True) + "\n", args.force)
    return decision


if __name__ == "__main__":
    main_with_args()
