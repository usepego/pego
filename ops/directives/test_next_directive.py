#!/usr/bin/env python3
"""Smoke tests for the local PEGO next-directive selector."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import next_directive


QUEUE = """# Directive Queue: test

## Active Candidates

| Rank | Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Breakfast Anchor | Health | 10-15 min | Low | Home | Morning | Level 1 | Ready |
| 2 | Venture Problem Map | Venture | 60 min | Medium | Computer | Workday | Level 1 | Ready |
| 3 | Garden Weed Block | Home | 25 min | Medium-low | Outside | Before evening | Level 1 | Conditional |
| 4 | Store List | Health/Ops | 10 min | Low | Phone/computer | Before grocery trip | Level 1 | Optional |

## Behavioral Strategy

| Rank | Candidate | Target Behavior | Environment Design |
| --- | --- | --- | --- |
| 1 | Breakfast Anchor | Make the first food decision stable instead of reactive. | Use home default food before hunger creates convenience-seeking. |
| 2 | Venture Problem Map | Create one strategic work artifact. | Put the human at the computer with a bounded research block. |
| 3 | Garden Weed Block | Reduce visual home-environment irritation before it becomes background stress. | Put the human outside at the garden bed with a short timer. |
| 4 | Store List | Change future food defaults before the next grocery trip. | Move food choices into a list context before shopping. |
"""


REGISTER = """# Register

## Questions to Ask

| Question | Why It Matters | Ask By | Follow-Up Action |
| --- | --- | --- | --- |
| Which visible part of the home or yard is most annoying right now? | Selects action | Weekly | Add candidate |
"""


def run_selector(*args: str) -> str:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        output = root / "response.md"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        next_directive.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--output",
                str(output),
                "--force",
                *args,
            ]
        )
        return output.read_text()


def run_selector_json(*args: str) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        queue = root / "queue.md"
        register = root / "register.md"
        output = root / "response.md"
        json_output = root / "response.json"
        queue.write_text(QUEUE)
        register.write_text(REGISTER)

        next_directive.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--queue",
                str(queue),
                "--register",
                str(register),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
                *args,
            ]
        )
        return json.loads(json_output.read_text())


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    breakfast = run_selector("--available", "15", "--energy", "low", "--location", "home")
    assert_contains(breakfast, "Breakfast Anchor")
    assert_contains(breakfast, "Make the first food decision stable instead of reactive.")
    assert_contains(breakfast, "Use home default food before hunger creates convenience-seeking.")

    structured_breakfast = run_selector_json("--available", "15", "--energy", "low", "--location", "home")
    if structured_breakfast["artifact_type"] != "command_response":
        raise AssertionError("expected command_response JSON artifact")
    if structured_breakfast["next_directive"]["directive"] != "Breakfast Anchor":
        raise AssertionError("expected Breakfast Anchor structured directive")
    if structured_breakfast["next_directive"]["authority_level"] != "level_1_recommend":
        raise AssertionError("expected normalized authority level")
    if structured_breakfast["next_directive"]["target_behavior"] != "Make the first food decision stable instead of reactive.":
        raise AssertionError("expected structured target behavior")
    if structured_breakfast["next_directive"]["environment_design"] != "Use home default food before hunger creates convenience-seeking.":
        raise AssertionError("expected structured environment design")

    venture = run_selector(
        "--done",
        "Breakfast Anchor",
        "--available",
        "45",
        "--energy",
        "medium",
        "--location",
        "computer",
    )
    assert_contains(venture, "Reduced Venture Problem Map")

    question = run_selector(
        "--done",
        "Breakfast Anchor",
        "--done",
        "Venture Problem Map",
        "--done",
        "Garden Weed Block",
        "--done",
        "Store List",
        "--available",
        "5",
    )
    assert_contains(question, "Which visible part of the home or yard is most annoying right now?")

    structured_question = run_selector_json(
        "--done",
        "Breakfast Anchor",
        "--done",
        "Venture Problem Map",
        "--done",
        "Garden Weed Block",
        "--done",
        "Store List",
        "--available",
        "5",
    )
    if structured_question["next_directive"]["candidate_rank"] is not None:
        raise AssertionError("expected no candidate rank for targeted question")
    if "targeted_question" not in structured_question:
        raise AssertionError("expected targeted question in structured response")

    print("next directive smoke tests passed.")


if __name__ == "__main__":
    main()
