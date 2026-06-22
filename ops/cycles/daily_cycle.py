#!/usr/bin/env python3
"""Run PEGO daily-cycle operations through one entry point.

Subcommands:

- next: select one next directive and run governance preflight.
- outcome: record execution outcome evidence.
- learn: record a context update from an outcome, conversation, or observation.

The runner delegates to local tools that write ignored private artifacts and
print only safe status/paths.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops" / "operator"))
sys.path.insert(0, str(ROOT / "ops" / "outcomes"))
sys.path.insert(0, str(ROOT / "ops" / "context"))

import next_step  # noqa: E402
import record_context_update  # noqa: E402
import record_outcome  # noqa: E402


def add_shared_date(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--date", default=date.today().isoformat())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
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
    if command == "outcome":
        return record_outcome.main_with_args(delegated_args)
    if command == "learn":
        return record_context_update.main_with_args(delegated_args)
    raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    main_with_args()
