#!/usr/bin/env python3
"""Smoke tests for PEGO attention decision runner."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import decide_attention


def option(event: str, recommendation: str, live_value: str, personal: str, recovery: str) -> dict[str, object]:
    return {
        "artifact_type": "attention_option",
        "schema_version": 1,
        "date": "2026-06-23",
        "event": event,
        "source": "manual_report",
        "event_type": "sports",
        "live_value": live_value,
        "personal_importance": personal,
        "recovery_value": recovery,
        "social_or_cultural_value": "medium",
        "opportunity_cost": "Could use the same window for focused work.",
        "multitask_compatibility": "low_cognitive_work",
        "time_window": "Now",
        "best_alternative": "Highlights later.",
        "risk": ["Time drift"],
        "recommendation": recommendation,
        "stop_condition": "Stop if this displaces a higher-priority directive.",
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        options = root / "options.json"
        decision = root / "decision.md"
        decision_json = root / "decision.json"
        candidate = root / "candidate.md"
        candidate_json = root / "candidate.json"
        options.write_text(
            json.dumps(
                [
                    option("World tournament group match", "multitask_live", "medium", "low", "medium"),
                    option("World tournament group match highlights", "highlights_later", "low", "low", "low"),
                ]
            )
        )

        result = decide_attention.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--option",
                str(options),
                "--context",
                "Low personal stake but enjoyable live sports window.",
                "--output",
                str(decision),
                "--json-output",
                str(decision_json),
                "--candidate-output",
                str(candidate),
                "--candidate-json-output",
                str(candidate_json),
                "--force",
            ]
        )

        if "low-cognitive" not in result["selected_directive"]:
            raise AssertionError(result)
        if "Attention Decision" not in decision.read_text():
            raise AssertionError(decision.read_text())
        structured = json.loads(decision_json.read_text())
        if structured["artifact_type"] != "attention_decision":
            raise AssertionError(structured)
        candidate_data = json.loads(candidate_json.read_text())
        if candidate_data["artifact_type"] != "directive_candidate":
            raise AssertionError(candidate_data)
        if candidate_data["domain"] != "happiness":
            raise AssertionError(candidate_data)

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        options = private / "attention" / "options" / "options.json"
        options.parent.mkdir(parents=True)
        options.write_text(
            json.dumps(
                [
                    option("Synthetic live event", "multitask_live", "medium", "low", "medium"),
                    option("Synthetic live event highlights", "highlights_later", "low", "low", "low"),
                ]
            )
        )
        decide_attention.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-23",
                "--option",
                str(options),
                "--candidate-json-output",
                str(private / "directives" / "candidates" / "attention-candidate.json"),
                "--force",
            ]
        )
        if not (private / "attention" / "decisions" / "attention-decision.md").exists():
            raise AssertionError("expected attention decision under configured private root")
        if not (private / "directives" / "candidates" / "attention-candidate.md").exists():
            raise AssertionError("expected attention candidate under configured private root")

    print("attention decision smoke tests passed.")


if __name__ == "__main__":
    main()
