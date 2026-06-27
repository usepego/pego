#!/usr/bin/env python3
"""Smoke tests for converting council decisions to directive candidates."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import decision_to_candidate


BASE_DECISION = {
    "artifact_type": "council_decision",
    "schema_version": 1,
    "date": "2026-06-23",
    "decision_frame": "Choose next work directive.",
    "source_recommendations": ["recommendation.json"],
    "proposed_directive": "Run a 30 minute venture problem map",
    "council_outcome": "adopt",
    "rationale": "Best current use of focused work time.",
    "expected_benefit": "Clarifies the next business experiment.",
    "key_risks": ["time", "energy"],
    "dissent": [],
    "required_handoffs": ["Venture"],
    "governance_status": "Level 1 council synthesis.",
    "stop_conditions": ["Stop if protected time begins."],
    "next_action": "Run a 30 minute venture problem map",
    "review": "Review after artifact exists.",
}


DIRECTIVE_CANDIDATE_FIELDS = {
    "artifact_type",
    "schema_version",
    "candidate",
    "domain",
    "altitude",
    "proposed_action",
    "duration",
    "timing",
    "energy_required",
    "location_required",
    "dependencies",
    "expected_benefit",
    "consequence_of_deferral",
    "protected_time_impact",
    "authority_level",
    "governance_status",
    "conflicts",
    "stop_condition",
}


def convert(root: Path, decision: dict[str, object]) -> dict[str, object]:
    input_path = root / "decision.json"
    markdown_output = root / "candidate.md"
    json_output = root / "candidate.json"
    input_path.write_text(json.dumps(decision))
    decision_to_candidate.main_with_args(
        [
            "--decision",
            str(input_path),
            "--output",
            str(markdown_output),
            "--json-output",
            str(json_output),
            "--force",
        ]
    )
    if "Directive Candidate" not in markdown_output.read_text():
        raise AssertionError("expected markdown directive candidate")
    candidate = json.loads(json_output.read_text())
    extra_fields = sorted(set(candidate) - DIRECTIVE_CANDIDATE_FIELDS)
    if extra_fields:
        raise AssertionError(f"unexpected directive-candidate fields: {extra_fields}")
    return candidate


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        adopted = convert(root, BASE_DECISION)
        if adopted["artifact_type"] != "directive_candidate":
            raise AssertionError("expected directive_candidate artifact")
        if adopted["candidate"] != "Run a 30 minute venture problem map":
            raise AssertionError(adopted)
        if adopted["governance_status"] != "reviewed":
            raise AssertionError("adopted decision should be queue-ready")

        revise = convert(root, {**BASE_DECISION, "council_outcome": "revise", "next_action": "Revise the directive and rerun council synthesis."})
        if revise["candidate"] != "Revise council directive":
            raise AssertionError(revise)
        if revise["domain"] != "governance":
            raise AssertionError("revise follow-up should be governance domain")

        escalate = convert(root, {**BASE_DECISION, "council_outcome": "escalate", "next_action": "Create or update a decision packet before adoption."})
        if escalate["authority_level"] != "level_4_escalate":
            raise AssertionError("escalation must not become a normal executable directive")
        if escalate["governance_status"] != "escalated":
            raise AssertionError("escalation must stay escalated")

    print("council decision-to-candidate smoke tests passed.")


if __name__ == "__main__":
    main()
