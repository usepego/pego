#!/usr/bin/env python3
"""Record a protected PEGO context update.

The runner writes protected private context-update records. It can optionally
append the proposed update to a private destination file when explicitly asked.
It prints only paths by default because updates may contain private facts.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"

SOURCES = {
    "Conversation",
    "Outcome",
    "Telemetry",
    "Document",
    "Agent observation",
    "External input",
    "Other",
}
UPDATE_CLASSES = {
    "Fact",
    "Preference",
    "Constraint",
    "Goal",
    "Strategy",
    "Pattern",
    "Tone rule",
    "Governance rule",
}
EVIDENCE_STRENGTHS = {
    "Direct statement",
    "Repeated statement",
    "Observed behavior",
    "Directive outcome",
    "Telemetry",
    "Model output",
    "Professional input",
    "Agent inference",
    "Speculation",
}
STABILITY = {"Stable", "Current but changeable", "Provisional", "Needs confirmation"}
ACTIONS = {"Record only", "Update destination", "Request confirmation", "Escalate", "Reject"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "context-update"


def validate_private_destination(path: Path) -> None:
    try:
        resolved = path.resolve()
    except FileNotFoundError:
        resolved = path.parent.resolve() / path.name
    private_root = PRIVATE.resolve()
    if private_root not in resolved.parents and resolved != private_root:
        raise SystemExit(f"destination must be under private/: {path}")


def build_update(args: argparse.Namespace) -> str:
    return "\n".join(
        [
            f"# Context Update: {args.title}",
            "",
            "## Date",
            "",
            args.date,
            "",
            "## Source",
            "",
            args.source,
            "",
            "## Raw Observation",
            "",
            args.raw_observation,
            "",
            "## Update Class",
            "",
            args.update_class,
            "",
            "## Evidence Strength",
            "",
            args.evidence_strength,
            "",
            "## Stability",
            "",
            args.stability,
            "",
            "## Destination File",
            "",
            str(args.destination_file) if args.destination_file else "None.",
            "",
            "## Proposed Update",
            "",
            args.proposed_update,
            "",
            "## Affected Agents",
            "",
            args.affected_agents or "Operations.",
            "",
            "## Governance Impact",
            "",
            args.governance_impact or "None recorded.",
            "",
            "## Action",
            "",
            args.action,
            "",
            "## Review Date",
            "",
            args.review_date or "Next weekly review.",
            "",
        ]
    )


def apply_update(args: argparse.Namespace, update_path: Path) -> Path:
    if args.action != "Update destination":
        raise SystemExit("--apply requires --action 'Update destination'")
    if not args.destination_file:
        raise SystemExit("--apply requires --destination-file")
    validate_private_destination(args.destination_file)
    args.destination_file.parent.mkdir(parents=True, exist_ok=True)
    with args.destination_file.open("a") as handle:
        handle.write(
            "\n".join(
                [
                    "",
                    f"## Context Update: {args.date} - {args.title}",
                    "",
                    args.proposed_update,
                    "",
                    f"Source: `{update_path}`",
                    "",
                ]
            )
        )
    return args.destination_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--title", default="")
    parser.add_argument("--source", choices=sorted(SOURCES), required=True)
    parser.add_argument("--raw-observation", required=True)
    parser.add_argument("--update-class", choices=sorted(UPDATE_CLASSES), required=True)
    parser.add_argument("--evidence-strength", choices=sorted(EVIDENCE_STRENGTHS), required=True)
    parser.add_argument("--stability", choices=sorted(STABILITY), required=True)
    parser.add_argument("--destination-file", type=Path)
    parser.add_argument("--proposed-update", required=True)
    parser.add_argument("--affected-agents", default="")
    parser.add_argument("--governance-impact", default="")
    parser.add_argument("--action", choices=sorted(ACTIONS), default="Record only")
    parser.add_argument("--review-date", default="")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.title:
        args.title = slugify(args.raw_observation)[:80]
    if args.destination_file:
        validate_private_destination(args.destination_file)

    output = args.output or (
        PRIVATE
        / "context"
        / "updates"
        / f"{args.date}-{slugify(args.title)}.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    output.write_text(build_update(args))

    print(f"wrote: {output}")
    if args.apply:
        destination = apply_update(args, output)
        print(f"updated: {destination}")
    return output


if __name__ == "__main__":
    main_with_args()
