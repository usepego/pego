#!/usr/bin/env python3
"""Run one PEGO operator step.

This composes directive selection with governance preflight:

1. Select one next directive from private queue/register state.
2. Write the command response to ignored private output.
3. Run governance preflight on the response.
4. Write a derived preflight JSON record to ignored private output.

The runner does not print private directive content.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
sys.path.insert(0, str(ROOT / "ops" / "directives"))
sys.path.insert(0, str(ROOT / "ops" / "governance"))

import directive_preflight  # noqa: E402
import next_directive  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--register", type=Path)
    parser.add_argument("--done", action="append", default=[])
    parser.add_argument("--blocked", default="")
    parser.add_argument("--available", type=int)
    parser.add_argument("--energy", choices=["low", "medium", "high"])
    parser.add_argument("--location")
    parser.add_argument("--response-output", type=Path)
    parser.add_argument("--preflight-output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> dict:
    parser = build_parser()
    args = parser.parse_args(argv)

    response_output = args.response_output or (
        PRIVATE / "directives" / "command-responses" / f"{args.date}-next.md"
    )
    preflight_output = args.preflight_output or (
        PRIVATE / "governance" / "preflight" / f"{args.date}-next.json"
    )

    directive_args = [
        "--date",
        args.date,
        "--output",
        str(response_output),
    ]
    if args.queue:
        directive_args.extend(["--queue", str(args.queue)])
    if args.register:
        directive_args.extend(["--register", str(args.register)])
    for done in args.done:
        directive_args.extend(["--done", done])
    if args.blocked:
        directive_args.extend(["--blocked", args.blocked])
    if args.available is not None:
        directive_args.extend(["--available", str(args.available)])
    if args.energy:
        directive_args.extend(["--energy", args.energy])
    if args.location:
        directive_args.extend(["--location", args.location])
    if args.force:
        directive_args.append("--force")

    next_directive.main_with_args(directive_args)
    response_text = response_output.read_text()
    preflight = directive_preflight.preflight(response_text)

    preflight_output.parent.mkdir(parents=True, exist_ok=True)
    if preflight_output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {preflight_output}")
    preflight_output.write_text(json.dumps(preflight.to_dict(), indent=2) + "\n")

    summary = {
        "response_output": str(response_output),
        "preflight_output": str(preflight_output),
        "preflight_outcome": preflight.outcome,
        "review_level": preflight.review_level,
        "required_next_step": preflight.required_next_step,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main_with_args()
