#!/usr/bin/env python3
"""Record a protected PEGO directive outcome.

The runner writes protected private outcome records. It prints only the output
path by default because outcome content may contain private facts.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
VALID_COMPLETIONS = {"completed", "partial", "not_completed", "blocked", "canceled"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "directive"


def completion_label(value: str) -> str:
    return {
        "completed": "Completed",
        "partial": "Partially completed",
        "not_completed": "Not completed",
        "blocked": "Blocked",
        "canceled": "Canceled",
    }[value]


def build_outcome(args: argparse.Namespace) -> str:
    return "\n".join(
        [
            f"# Directive Outcome: {args.date} - {args.directive}",
            "",
            "## Date",
            "",
            args.date,
            "",
            "## Source Directive",
            "",
            args.source or "Not supplied.",
            "",
            "## Directive Summary",
            "",
            args.directive,
            "",
            "## Completion",
            "",
            completion_label(args.completion),
            "",
            "## What Happened",
            "",
            args.what_happened or "Not supplied.",
            "",
            "## Evidence",
            "",
            args.evidence or "Human report.",
            "",
            "## Friction",
            "",
            args.friction or "None recorded.",
            "",
            "## Benefit",
            "",
            args.benefit or "None recorded.",
            "",
            "## Cost",
            "",
            args.cost or "None recorded.",
            "",
            "## Protected-Time Impact",
            "",
            args.protected_time_impact,
            "",
            "## Stakeholder Impact",
            "",
            args.stakeholder_impact or "None recorded.",
            "",
            "## Environment Impact",
            "",
            args.environment_impact or "None recorded.",
            "",
            "## Follow-Up Directive Candidates",
            "",
            args.follow_up or "None recorded.",
            "",
            "## Agent Updates",
            "",
            args.agent_updates or "Operations Agent should ingest this outcome.",
            "",
            "## Governance Notes",
            "",
            args.governance_notes or "No governance issue recorded.",
            "",
            "## Next Review",
            "",
            args.next_review or "Next daily or weekly review.",
            "",
        ]
    )


def append_session_event(args: argparse.Namespace, outcome_path: Path) -> Path:
    session_path = args.session_log or (
        PRIVATE / "directives" / "sessions" / f"{args.date}-session-log.md"
    )
    session_path.parent.mkdir(parents=True, exist_ok=True)
    if not session_path.exists():
        session_path.write_text(
            "\n".join(
                [
                    f"# Intra-Day Session Log: {args.date}",
                    "",
                    "## Session Events",
                    "",
                    "| Time | Human Input | State Change | PEGO Response | Outcome |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
            + "\n"
        )
    timestamp = args.time or datetime.now().strftime("%H:%M")
    row = (
        f"| {timestamp} | Outcome recorded | {args.directive}: "
        f"{completion_label(args.completion)} | Outcome recorder | {outcome_path} |\n"
    )
    with session_path.open("a") as handle:
        handle.write(row)
    return session_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--time")
    parser.add_argument("--directive", required=True)
    parser.add_argument("--completion", choices=sorted(VALID_COMPLETIONS), required=True)
    parser.add_argument("--source")
    parser.add_argument("--what-happened", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--friction", default="")
    parser.add_argument("--benefit", default="")
    parser.add_argument("--cost", default="")
    parser.add_argument(
        "--protected-time-impact",
        default="None",
        choices=["None", "Low", "Medium", "High"],
    )
    parser.add_argument("--stakeholder-impact", default="")
    parser.add_argument("--environment-impact", default="")
    parser.add_argument("--follow-up", default="")
    parser.add_argument("--agent-updates", default="")
    parser.add_argument("--governance-notes", default="")
    parser.add_argument("--next-review", default="")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--append-session", action="store_true")
    parser.add_argument("--session-log", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = args.output or (
        PRIVATE
        / "outcomes"
        / "directives"
        / f"{args.date}-{slugify(args.directive)}.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_outcome(args))

    print(f"wrote: {output}")
    if args.append_session:
        session_path = append_session_event(args, output)
        print(f"updated: {session_path}")
    return output


if __name__ == "__main__":
    main_with_args()
