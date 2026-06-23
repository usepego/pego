#!/usr/bin/env python3
"""Smoke tests for the root PEGO command wrapper."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PEGOCTL = ROOT / "pegoctl"


QUEUE = """# Directive Queue: test

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


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PEGOCTL), *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> None:
    help_result = run(["--help"])
    if "check-in" not in help_result.stdout:
        raise AssertionError(help_result.stdout)

    doctor = run(["doctor"])
    if "PEGO doctor passed" not in doctor.stdout:
        raise AssertionError(doctor.stdout)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        private_root = root / "private"
        readiness = root / "readiness.json"
        queue = root / "queue.md"
        register = root / "register.md"
        session = root / "session.md"
        session_json = root / "session.json"
        brief = root / "brief.md"
        brief_json = root / "brief.json"
        session_review = root / "session-review.md"
        session_review_json = root / "session-review.json"
        promotion_summary = root / "promotion-summary.json"
        context_updates = root / "context-updates"
        response = root / "response.md"
        response_json = root / "response.json"
        preflight = root / "preflight.json"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        run(
            [
                "readiness",
                "--private-root",
                str(private_root),
                "--output",
                str(readiness),
            ]
        )
        readiness_data = json.loads(readiness.read_text())
        if readiness_data["artifact_type"] != "private_instance_readiness":
            raise AssertionError(readiness_data)

        run(
            [
                "check-in",
                "Breakfast is done. What is next?",
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--done",
                "Breakfast Anchor",
                "--available",
                "45",
                "--energy",
                "medium",
                "--location",
                "computer",
                "--session-output",
                str(session),
                "--session-json-output",
                str(session_json),
                "--response-output",
                str(response),
                "--response-json-output",
                str(response_json),
                "--preflight-output",
                str(preflight),
                "--force",
            ]
        )
        session_data = json.loads(session_json.read_text())
        if session_data["artifact_type"] != "intra_day_session_log":
            raise AssertionError(session_data)
        if len(session_data["events"]) != 1:
            raise AssertionError(session_data)

        run(
            [
                "brief",
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--session-json",
                str(session_json),
                "--output",
                str(brief),
                "--json-output",
                str(brief_json),
                "--force",
            ]
        )
        brief_data = json.loads(brief_json.read_text())
        if brief_data["artifact_type"] != "operating_brief":
            raise AssertionError(brief_data)
        if not brief.exists():
            raise AssertionError("expected markdown brief output")

        run(
            [
                "close-session",
                "--date",
                "2026-06-23",
                "--session-json",
                str(session_json),
                "--output",
                str(session_review),
                "--json-output",
                str(session_review_json),
                "--force",
            ]
        )
        review_data = json.loads(session_review_json.read_text())
        if review_data["artifact_type"] != "session_review":
            raise AssertionError(review_data)
        if not session_review.exists():
            raise AssertionError("expected markdown session review output")

        run(
            [
                "promote-context",
                "--date",
                "2026-06-23",
                "--review",
                str(session_review_json),
                "--output-dir",
                str(context_updates),
                "--summary-output",
                str(promotion_summary),
                "--force",
            ]
        )
        promotion_data = json.loads(promotion_summary.read_text())
        if promotion_data["artifact_type"] != "session_context_promotion":
            raise AssertionError(promotion_data)

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        (private_root / "directives" / "queues").mkdir(parents=True)
        (private_root / "operator").mkdir(parents=True)
        (private_root / "directives" / "queues" / "2026-06-23-queue.md").write_text(QUEUE)
        (private_root / "operator" / "operating-register.md").write_text(REGISTER)
        run(
            [
                "--private-root",
                str(private_root),
                "check-in",
                "Breakfast is done. What is next?",
                "--date",
                "2026-06-23",
                "--time",
                "09:00",
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
        if not (private_root / "operator" / "sessions" / "2026-06-23-user-mode.json").exists():
            raise AssertionError("expected pegoctl check-in session under configured private root")
        if not (private_root / "directives" / "command-responses" / "2026-06-23-next.json").exists():
            raise AssertionError("expected pegoctl command response under configured private root")

    with tempfile.TemporaryDirectory() as directory:
        private_root = Path(directory) / "pego-private"
        (private_root / "health").mkdir(parents=True)
        (private_root / "finance").mkdir(parents=True)
        (private_root / "operator").mkdir(parents=True)
        (private_root / "directives" / "candidates").mkdir(parents=True)
        (private_root / "health" / "baseline.json").write_text(
            json.dumps(
                {
                    "artifact_type": "health_baseline",
                    "schema_version": 1,
                    "evidence_policy": {"tracking_level": "minimal"},
                    "goal": {},
                    "constraints": {},
                    "preferences": {},
                    "current_routine": {},
                    "availability": {},
                    "metrics": {},
                }
            )
        )
        (private_root / "operator" / "operating-register.md").write_text(REGISTER)
        run(
            [
                "--private-root",
                str(private_root),
                "daily",
                "health-check-in",
                "--date",
                "2026-06-23",
                "--force",
            ]
        )
        if not (private_root / "health" / "check-ins" / "health-check-in.md").exists():
            raise AssertionError("expected pegoctl daily output under configured private root")

        run(
            [
                "--private-root",
                str(private_root),
                "weekly",
                "--week",
                "2026-W26",
                "--force",
            ]
        )
        if not (private_root / "directives" / "weekly" / "2026-W26.md").exists():
            raise AssertionError("expected pegoctl weekly output under configured private root")

        run(
            [
                "--private-root",
                str(private_root),
                "monthly",
                "--month",
                "2026-06",
                "--force",
            ]
        )
        if not (private_root / "directives" / "monthly" / "2026-06-strategy-review.json").exists():
            raise AssertionError("expected pegoctl monthly output under configured private root")

    print("pegoctl smoke tests passed.")


if __name__ == "__main__":
    main()
