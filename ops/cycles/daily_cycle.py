#!/usr/bin/env python3
"""Run PEGO daily-cycle operations through one entry point.

Subcommands:

- next: select one next directive and run governance preflight.
- outcome: record execution outcome evidence.
- review: convert an outcome into a learning decision.
- synthesize: convert directive candidates into an active queue.
- council: synthesize agent recommendations into a council decision.
- council-candidate: convert a council decision into a directive candidate.
- learn: record a context update from an outcome, conversation, or observation.
- finance-check-in: generate targeted finance questions for directive selection.
- health-check-in: generate targeted health questions for directive selection.
- writing-brief: generate a public-writing brief and communications candidate.

The runner delegates to local tools that write protected private artifacts and
print only safe status/paths.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops" / "operator"))
sys.path.insert(0, str(ROOT / "ops" / "outcomes"))
sys.path.insert(0, str(ROOT / "ops" / "review"))
sys.path.insert(0, str(ROOT / "ops" / "context"))
sys.path.insert(0, str(ROOT / "ops" / "synthesis"))
sys.path.insert(0, str(ROOT / "ops" / "health"))

import generate_check_in  # noqa: E402
import next_step  # noqa: E402
import record_context_update  # noqa: E402
import record_outcome  # noqa: E402
import review_outcome  # noqa: E402
import synthesize_queue  # noqa: E402


def load_finance_check_in():
    path = ROOT / "ops" / "finance" / "generate_check_in.py"
    spec = importlib.util.spec_from_file_location("finance_generate_check_in", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load finance check-in runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_council_decision():
    path = ROOT / "ops" / "council" / "synthesize_decision.py"
    spec = importlib.util.spec_from_file_location("council_synthesize_decision", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load council decision runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_council_candidate():
    path = ROOT / "ops" / "council" / "decision_to_candidate.py"
    spec = importlib.util.spec_from_file_location("council_decision_to_candidate", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load council candidate runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_writing_brief():
    path = ROOT / "ops" / "communications" / "generate_public_writing_brief.py"
    spec = importlib.util.spec_from_file_location("communications_generate_public_writing_brief", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load writing brief runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


finance_generate_check_in = load_finance_check_in()
council_synthesize_decision = load_council_decision()
council_decision_to_candidate = load_council_candidate()
communications_generate_public_writing_brief = load_writing_brief()


def add_shared_date(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--date", default=date.today().isoformat())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-root", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    next_parser = subparsers.add_parser("next")
    add_shared_date(next_parser)
    next_parser.add_argument("--queue", type=Path)
    next_parser.add_argument("--register", type=Path)
    next_parser.add_argument("--done", action="append", default=[])
    next_parser.add_argument("--blocked", default="")
    next_parser.add_argument("--available", type=int)
    next_parser.add_argument("--energy", choices=["low", "medium", "high"])
    next_parser.add_argument("--location")
    next_parser.add_argument("--response-output", type=Path)
    next_parser.add_argument("--preflight-output", type=Path)
    next_parser.add_argument("--force", action="store_true")

    synthesize_parser = subparsers.add_parser("synthesize")
    add_shared_date(synthesize_parser)
    synthesize_parser.add_argument("--candidate", type=Path, action="append", default=[])
    synthesize_parser.add_argument("--available", type=int)
    synthesize_parser.add_argument("--time")
    synthesize_parser.add_argument("--location")
    synthesize_parser.add_argument("--energy")
    synthesize_parser.add_argument("--environment")
    synthesize_parser.add_argument("--obligations")
    synthesize_parser.add_argument("--constraints")
    synthesize_parser.add_argument("--protected-time", default="")
    synthesize_parser.add_argument("--frame", default="Synthesize current candidate directives into one active queue.")
    synthesize_parser.add_argument("--output", type=Path)
    synthesize_parser.add_argument("--force", action="store_true")

    outcome_parser = subparsers.add_parser("outcome")
    add_shared_date(outcome_parser)
    outcome_parser.add_argument("--time")
    outcome_parser.add_argument("--directive", required=True)
    outcome_parser.add_argument(
        "--completion",
        choices=sorted(record_outcome.VALID_COMPLETIONS),
        required=True,
    )
    outcome_parser.add_argument("--source")
    outcome_parser.add_argument("--what-happened", default="")
    outcome_parser.add_argument("--evidence", default="")
    outcome_parser.add_argument("--friction", default="")
    outcome_parser.add_argument("--benefit", default="")
    outcome_parser.add_argument("--outcome-progress", default="")
    outcome_parser.add_argument(
        "--contentment-signal",
        default="Unknown",
        choices=["More contentment", "Less contentment", "No material change", "Unknown"],
    )
    outcome_parser.add_argument("--cost", default="")
    outcome_parser.add_argument(
        "--protected-time-impact",
        default="None",
        choices=["None", "Low", "Medium", "High"],
    )
    outcome_parser.add_argument("--stakeholder-impact", default="")
    outcome_parser.add_argument("--environment-impact", default="")
    outcome_parser.add_argument("--follow-up", default="")
    outcome_parser.add_argument("--agent-updates", default="")
    outcome_parser.add_argument("--governance-notes", default="")
    outcome_parser.add_argument("--next-review", default="")
    outcome_parser.add_argument("--output", type=Path)
    outcome_parser.add_argument("--append-session", action="store_true")
    outcome_parser.add_argument("--session-log", type=Path)
    outcome_parser.add_argument("--force", action="store_true")

    review_parser = subparsers.add_parser("review")
    add_shared_date(review_parser)
    review_parser.add_argument("--outcome", type=Path, required=True)
    review_parser.add_argument("--output", type=Path)
    review_parser.add_argument("--force", action="store_true")

    learn_parser = subparsers.add_parser("learn")
    add_shared_date(learn_parser)
    learn_parser.add_argument("--title", default="")
    learn_parser.add_argument("--source", choices=sorted(record_context_update.SOURCES), required=True)
    learn_parser.add_argument("--raw-observation", required=True)
    learn_parser.add_argument(
        "--update-class",
        choices=sorted(record_context_update.UPDATE_CLASSES),
        required=True,
    )
    learn_parser.add_argument(
        "--evidence-strength",
        choices=sorted(record_context_update.EVIDENCE_STRENGTHS),
        required=True,
    )
    learn_parser.add_argument(
        "--stability",
        choices=sorted(record_context_update.STABILITY),
        required=True,
    )
    learn_parser.add_argument("--destination-file", type=Path)
    learn_parser.add_argument("--proposed-update", required=True)
    learn_parser.add_argument("--affected-agents", default="")
    learn_parser.add_argument("--governance-impact", default="")
    learn_parser.add_argument("--action", choices=sorted(record_context_update.ACTIONS), default="Record only")
    learn_parser.add_argument("--review-date", default="")
    learn_parser.add_argument("--output", type=Path)
    learn_parser.add_argument("--apply", action="store_true")
    learn_parser.add_argument("--force", action="store_true")

    health_parser = subparsers.add_parser("health-check-in")
    add_shared_date(health_parser)
    health_parser.add_argument("--input", type=Path)
    health_parser.add_argument("--output", type=Path)
    health_parser.add_argument("--json-output", type=Path)
    health_parser.add_argument("--force", action="store_true")

    finance_parser = subparsers.add_parser("finance-check-in")
    add_shared_date(finance_parser)
    finance_parser.add_argument("--input", type=Path)
    finance_parser.add_argument("--output", type=Path)
    finance_parser.add_argument("--json-output", type=Path)
    finance_parser.add_argument("--force", action="store_true")

    council_parser = subparsers.add_parser("council")
    add_shared_date(council_parser)
    council_parser.add_argument("--frame", default="Council synthesis of current agent recommendations.")
    council_parser.add_argument("--recommendation", type=Path, action="append", default=[])
    council_parser.add_argument("--goal-reconciliation", type=Path, action="append", default=[])
    council_parser.add_argument("--priority-assumption", default="")
    council_parser.add_argument("--output", type=Path)
    council_parser.add_argument("--json-output", type=Path)
    council_parser.add_argument("--force", action="store_true")

    council_candidate_parser = subparsers.add_parser("council-candidate")
    council_candidate_parser.add_argument("--decision", type=Path, required=True)
    council_candidate_parser.add_argument("--output", type=Path)
    council_candidate_parser.add_argument("--json-output", type=Path)
    council_candidate_parser.add_argument("--force", action="store_true")

    writing_parser = subparsers.add_parser("writing-brief")
    add_shared_date(writing_parser)
    writing_parser.add_argument("--artifact", default="PEGO introduction essay")
    writing_parser.add_argument("--public-purpose")
    writing_parser.add_argument("--opportunity-thesis")
    writing_parser.add_argument("--audience")
    writing_parser.add_argument("--reader-reaction")
    writing_parser.add_argument("--core-claim")
    writing_parser.add_argument("--supporting-claims")
    writing_parser.add_argument("--private-source-material")
    writing_parser.add_argument("--public-safe-material")
    writing_parser.add_argument("--structure")
    writing_parser.add_argument("--dissent")
    writing_parser.add_argument("--next-action")
    writing_parser.add_argument("--review-rule")
    writing_parser.add_argument("--duration")
    writing_parser.add_argument("--timing")
    writing_parser.add_argument("--energy", choices=["low", "medium", "high"])
    writing_parser.add_argument("--voice-model", type=Path)
    writing_parser.add_argument("--brief-output", type=Path)
    writing_parser.add_argument("--candidate-output", type=Path)
    writing_parser.add_argument("--json-output", type=Path)
    writing_parser.add_argument("--force", action="store_true")

    return parser


def main_with_args(argv: list[str] | None = None) -> object:
    parser = build_parser()
    args = parser.parse_args(argv)
    values = vars(args)
    command = values.pop("command")

    delegated_args: list[str] = []
    for key, value in values.items():
        if value in (None, "", False):
            continue
        option = "--" + key.replace("_", "-")
        if value is True:
            delegated_args.append(option)
        elif isinstance(value, list):
            for item in value:
                delegated_args.extend([option, str(item)])
        else:
            delegated_args.extend([option, str(value)])

    if command == "next":
        return next_step.main_with_args(delegated_args)
    if command == "synthesize":
        return synthesize_queue.main_with_args(delegated_args)
    if command == "outcome":
        return record_outcome.main_with_args(delegated_args)
    if command == "review":
        return review_outcome.main_with_args(delegated_args)
    if command == "learn":
        return record_context_update.main_with_args(delegated_args)
    if command == "health-check-in":
        return generate_check_in.main_with_args(delegated_args)
    if command == "finance-check-in":
        return finance_generate_check_in.main_with_args(delegated_args)
    if command == "council":
        return council_synthesize_decision.main_with_args(delegated_args)
    if command == "council-candidate":
        return council_decision_to_candidate.main_with_args(delegated_args)
    if command == "writing-brief":
        return communications_generate_public_writing_brief.main_with_args(delegated_args)
    raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    main_with_args()
