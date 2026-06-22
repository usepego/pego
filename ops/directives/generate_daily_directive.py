#!/usr/bin/env python3
"""Generate a protected PEGO daily directive packet.

The output is written into the private instance under private/directives/daily/.
This runner intentionally uses generic conservative defaults and does not expose
private instance content in framework files.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"


def read_if_exists(path: Path) -> str | None:
    if path.exists():
        text = path.read_text().strip()
        return text or None
    return None


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def build_directive(target_date: str) -> str:
    protected_time = read_if_exists(PRIVATE / "time" / "protected-time.md")
    health_directives = read_if_exists(PRIVATE / "health" / "directives.md")
    finance_review = read_if_exists(PRIVATE / "finance" / "finance-agent-initial-review.md")
    career_review = read_if_exists(PRIVATE / "career" / "career-agent-initial-review.md")

    protected_summary = (
        "Preserve protected time from the private time rules. If no private rule is available, "
        "do not let PEGO work expand into spouse/partner, sleep, recovery, or existing commitments."
    )
    if protected_time:
        protected_summary = (
            "Follow the local protected-time file. Do not override it without governance review."
        )

    health_summary = "Use the lowest-friction approved health action available locally."
    if health_directives:
        health_summary = (
            "Follow the local health directive file, keeping actions low-risk and reversible."
        )

    finance_summary = "No trading, major spending, or financial execution without formal review."
    if finance_review:
        finance_summary = (
            "Follow the local Finance Agent review. Do not execute trades, job-risk decisions, "
            "or major spending without formal governance review."
        )

    career_summary = "No major career move without a career decision packet and governance review."
    if career_review:
        career_summary = (
            "Follow the local Career Agent review. Treat career work as Level 1 unless explicitly escalated."
        )

    parts = [
        f"# Daily Directive: {target_date}\n",
        section("Status", "Draft local directive. Authority level: Level 1, Recommend."),
        section(
            "Operating Thesis",
            "Advance PEGO and the active life strategy without disrupting protected time, privacy, or household stability.",
        ),
        section(
            "Governance Status",
            "Light review required before treating this as an active directive. No Level 2 authority is implied.",
        ),
        section("Protected Time", protected_summary),
        section(
            "Must Do",
            "- Preserve privacy and do not move private instance data into Git.\n"
            "- Keep the daily plan small enough to execute.\n"
            "- Complete one concrete PEGO-building or life-maintenance action.",
        ),
        section(
            "Should Do",
            f"- Health: {health_summary}\n"
            f"- Finance: {finance_summary}\n"
            f"- Career: {career_summary}",
        ),
        section(
            "Optional",
            "- Add missing local context if it is easy and private.\n"
            "- Review yesterday's directive outcome if one exists.",
        ),
        section(
            "Stop Conditions",
            "- The directive conflicts with protected time.\n"
            "- The directive requires financial, medical, legal, career, relationship, or privacy-impacting execution.\n"
            "- The directive depends on weak assumptions but presents itself as certain.",
        ),
        section(
            "End-of-Day Review",
            "- What happened?\n"
            "- What failed?\n"
            "- What created energy or clarity?\n"
            "- What should PEGO change tomorrow?",
        ),
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    target = PRIVATE / "directives" / "daily" / f"{args.date}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {target}")

    target.write_text(build_directive(args.date))
    print(f"wrote: {target}")


if __name__ == "__main__":
    main()
