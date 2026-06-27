#!/usr/bin/env python3
"""Smoke tests for PEGO monthly strategy review runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import monthly_cycle


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which strategic assumption is weakest? | Prevents drift | Monthly | Add review |
"""


SCHEMA_KEYS = {
    "artifact_type",
    "schema_version",
    "month",
    "strategic_thesis",
    "outcome_summary",
    "goal_progress",
    "agent_assessments",
    "assumptions_revisited",
    "strategy_changes",
    "decision_packets_needed",
    "constitution_concerns",
    "next_month_priorities",
    "stop_conditions",
}


def seed_private_root(private: Path) -> None:
    (private / "operator").mkdir(parents=True)
    (private / "outcomes" / "directives").mkdir(parents=True)
    (private / "reviews" / "outcomes").mkdir(parents=True)
    (private / "reviews" / "sessions").mkdir(parents=True)
    (private / "context" / "updates").mkdir(parents=True)
    (private / "governance" / "preflight").mkdir(parents=True)
    (private / "directives" / "queues").mkdir(parents=True)
    (private / "directives" / "weekly").mkdir(parents=True)
    (private / "operator" / "operating-register.md").write_text(REGISTER)
    (private / "outcomes" / "directives" / "2026-06-01-test.md").write_text("# Outcome\n")
    (private / "reviews" / "outcomes" / "2026-06-01-test.md").write_text("# Review\n")
    (private / "context" / "updates" / "2026-06-01-test.md").write_text("# Context\n")
    (private / "governance" / "preflight" / "2026-06-01-test.json").write_text("{}\n")
    (private / "directives" / "queues" / "2026-06-01-queue.md").write_text("# Queue\n")
    (private / "directives" / "weekly" / "2026-W23.md").write_text("# Weekly\n")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        seed_private_root(private)

        review = monthly_cycle.main_with_args(
            [
                "--private-root",
                str(private),
                "--month",
                "2026-06",
                "--force",
            ]
        )
        if set(review) != SCHEMA_KEYS:
            raise AssertionError(sorted(set(review) - SCHEMA_KEYS))
        if review["artifact_type"] != "monthly_strategy_review":
            raise AssertionError(review)
        if review["agent_assessments"]["operations"]["what_learned"].find("1 outcomes") == -1:
            raise AssertionError(review["agent_assessments"]["operations"])
        if review["assumptions_revisited"][0]["status"] != "supported":
            raise AssertionError(review["assumptions_revisited"])

        markdown = private / "directives" / "monthly" / "2026-06-strategy-review.md"
        structured = private / "directives" / "monthly" / "2026-06-strategy-review.json"
        if "Which strategic assumption is weakest?" not in markdown.read_text():
            raise AssertionError(markdown.read_text())
        data = json.loads(structured.read_text())
        if set(data) != SCHEMA_KEYS:
            raise AssertionError(data)

    print("monthly strategy review smoke tests passed.")


if __name__ == "__main__":
    main()
