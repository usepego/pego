#!/usr/bin/env python3
"""Smoke tests for PEGO council decision synthesis."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import synthesize_decision


RECOMMEND = {
    "artifact_type": "agent_recommendation",
    "schema_version": 1,
    "agent": "Operations",
    "recommendation_type": "recommend",
    "proposed_directive": "Run a 30 minute venture problem map",
    "authority_level": "level_1_recommend",
    "relevant_facts": ["Synthetic test fact"],
    "assumptions": [{"statement": "Synthetic assumption", "certainty": "medium"}],
    "evidence_quality": ["agent_inference"],
    "expected_benefit": "Clarifies the next business experiment.",
    "costs_and_tradeoffs": ["Uses focused work time."],
    "risks": ["time", "energy"],
    "reversibility": "easy_to_reverse",
    "privacy_impact": "private_only",
    "required_handoffs": ["Venture"],
    "dissent": "",
    "stop_conditions": ["Stop if protected time begins."],
    "review": {"review_date_or_success_criteria": "Review after artifact exists."},
}


DISSENT = {
    **RECOMMEND,
    "agent": "Relationships",
    "recommendation_type": "dissent",
    "proposed_directive": "Do not schedule during protected time",
    "expected_benefit": "Protects relationship constraints.",
    "required_handoffs": ["Governance"],
    "dissent": "Protected time is too close; revise the timing.",
}


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        recommend = root / "recommend.json"
        dissent = root / "dissent.json"
        output = root / "decision.md"
        json_output = root / "decision.json"
        recommend.write_text(json.dumps(RECOMMEND))
        dissent.write_text(json.dumps(DISSENT))

        synthesize_decision.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--frame",
                "Choose next work directive.",
                "--recommendation",
                str(recommend),
                "--recommendation",
                str(dissent),
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        text = output.read_text()
        assert_contains(text, "Council Outcome")
        assert_contains(text, "revise")
        assert_contains(text, "Protected time is too close")
        assert_contains(text, "Governance")

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "council_decision":
            raise AssertionError("expected council_decision artifact")
        if structured["council_outcome"] != "revise":
            raise AssertionError("expected dissent to force revision")
        if "time" not in structured["key_risks"]:
            raise AssertionError("expected risk preservation")

    print("council decision smoke tests passed.")


if __name__ == "__main__":
    main()
