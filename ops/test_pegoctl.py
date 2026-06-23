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

    print("pegoctl smoke tests passed.")


if __name__ == "__main__":
    main()
