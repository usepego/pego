#!/usr/bin/env python3
"""Smoke tests for USER-mode operators against an external private root."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import close_session
import generate_brief
import user_check_in


QUEUE = """# Directive Queue: test

## Protected Time

Evening block is protected.

## Current State

- Time: morning
- Location: home
- Energy: medium

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 45 min | Medium | Computer | Workday | Level 1 | Ready |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which dependency could block the next work block? | Prevents delay | Daily | Add candidate |
"""


def seed_private_root(private_root: Path) -> None:
    (private_root / "directives" / "queues").mkdir(parents=True)
    (private_root / "operator").mkdir(parents=True)
    (private_root / "active-operating-brief.md").write_text(
        "# Active Operating Brief\n\n## Active Objective\n\nOperate from external private root.\n"
    )
    (private_root / "directives" / "queues" / "2026-06-23-queue.md").write_text(QUEUE)
    (private_root / "operator" / "operating-register.md").write_text(REGISTER)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        seed_private_root(private_root)

        check_in = user_check_in.main_with_args(
            [
                "--private-root",
                str(private_root),
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
                "--input",
                "Breakfast is done. What is next?",
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--force",
            ]
        )
        if check_in["events"] != 1:
            raise AssertionError(check_in)
        if not (private_root / "operator" / "sessions" / "2026-06-23-user-mode.json").exists():
            raise AssertionError("expected session JSON under external private root")
        if not (private_root / "directives" / "command-responses" / "2026-06-23-next.json").exists():
            raise AssertionError("expected command response under external private root")
        if not (private_root / "governance" / "preflight" / "2026-06-23-next.json").exists():
            raise AssertionError("expected preflight under external private root")

        brief = generate_brief.main_with_args(
            [
                "--private-root",
                str(private_root),
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if brief["active_candidates"] != 2:
            raise AssertionError(brief)
        brief_data = json.loads(
            (private_root / "operator" / "briefs" / "2026-06-23-brief.json").read_text()
        )
        if brief_data["active_objective"] != "Operate from external private root.":
            raise AssertionError(brief_data)

        review = close_session.main_with_args(
            [
                "--private-root",
                str(private_root),
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if review["event_count"] != 1:
            raise AssertionError(review)
        if not (private_root / "reviews" / "sessions" / "2026-06-23-session-review.json").exists():
            raise AssertionError("expected session review under external private root")

    print("external private-root operator smoke tests passed.")


if __name__ == "__main__":
    main()
