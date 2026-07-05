#!/usr/bin/env python3
"""Smoke tests for PEGO directive queue synthesis."""

from __future__ import annotations

import tempfile
import json
from pathlib import Path

import synthesize_queue


CANDIDATES = """# Candidates

| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Venture Problem Map | Venture | 60 min | Medium | Computer | Today | Level 1 | Draft | Strategic progress | Delays business clarity | None |
| Garden Weed Block | Home and Environment | 20 min | Medium | Outside | Before evening | Level 1 | Draft | Preserves home serenity | Visible friction increases | Low |
| Quit Job Decision | Career | 30 min | High | Computer | This week | Level 4 | Escalated | Income strategy | Opportunity cost | High |
| Breakfast Anchor | Health | 10 min | Low | Home | Morning | Level 1 | Draft | Stabilizes diet | Hunger and snacking | None |
"""


TIE_CANDIDATES = """# Tied Candidates

| Candidate | Domain | Duration | Energy | Location | Deadline | Authority | Governance Status | Expected Benefit | Consequence of Deferral | Protected-Time Impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Large Ambiguous Task | Operations | 25 min | Low | Home | Today | Level 1 | Draft |  |  | None |
| Small Ambiguous Task | Operations | 5 min | Low | Home | Today | Level 1 | Draft |  |  | None |
"""


ANTICIPATION_SCAN = """# Anticipation Scan

## Domain

Event

## Candidate Directive

Decide outfit for dinner

## Lead Time

3 days

## Governance Status

Level 1 recommendation unless spending is material.
"""


JSON_CANDIDATES = [
    {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": "Structured Health Walk",
        "domain": "health",
        "altitude": "directive",
        "proposed_action": "Structured Health Walk",
        "duration": "15 min",
        "timing": "Before lunch",
        "energy_required": "low",
        "location_required": "outside",
        "dependencies": ["Safe walking conditions"],
        "expected_benefit": "Preserves health capacity.",
        "consequence_of_deferral": "Movement remains at zero baseline.",
        "target_behavior": "Create a movement action before sedentary inertia wins.",
        "environment_design": "Put the human outside before lunch.",
        "protected_time_impact": "none",
        "authority_level": "level_1_recommend",
        "governance_status": "draft",
        "conflicts": [],
        "stop_condition": "Stop if pain appears.",
    },
    {
        "artifact_type": "directive_candidate",
        "schema_version": 1,
        "candidate": "Structured Contractor Quote",
        "domain": "home_environment",
        "altitude": "directive",
        "proposed_action": "Get contractor quote",
        "duration": "15 min",
        "timing": "This month",
        "energy_required": "medium",
        "location_required": "phone",
        "dependencies": ["Repair scope"],
        "expected_benefit": "Clarifies repair cost.",
        "consequence_of_deferral": "Repair remains ambiguous.",
        "target_behavior": "Convert vague home concern into a scoped repair decision.",
        "environment_design": "Move the issue into a phone call context before the next review.",
        "protected_time_impact": "low",
        "authority_level": "level_1_recommend",
        "governance_status": "reviewed",
        "conflicts": [],
        "stop_condition": "Stop before commitment or spending.",
    },
]


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        candidate_file = root / "candidates.md"
        scan_file = root / "scan.md"
        structured_file = root / "structured-candidates.json"
        tie_file = root / "tie-candidates.md"
        output = root / "queue.md"
        json_output = root / "queue.json"
        tie_output = root / "tie-queue.md"
        tie_json_output = root / "tie-queue.json"
        candidate_file.write_text(CANDIDATES)
        scan_file.write_text(ANTICIPATION_SCAN)
        structured_file.write_text(json.dumps(JSON_CANDIDATES))
        tie_file.write_text(TIE_CANDIDATES)

        synthesize_queue.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--candidate",
                str(candidate_file),
                "--candidate",
                str(scan_file),
                "--candidate",
                str(structured_file),
                "--available",
                "30",
                "--output",
                str(output),
                "--json-output",
                str(json_output),
                "--force",
            ]
        )

        text = output.read_text()
        assert_contains(text, "Breakfast Anchor")
        assert_contains(text, "Garden Weed Block")
        assert_contains(text, "## Scoring Model")
        assert_contains(text, "## Scorecards")
        assert_contains(text, "Safe tie-break order")
        assert_contains(text, "Decide outfit for dinner")
        assert_contains(text, "Structured Health Walk")
        assert_contains(text, "Create a movement action before sedentary inertia wins.")
        assert_contains(text, "Structured Contractor Quote")
        assert_contains(text, "Venture Problem Map | Does not fit available window")
        assert_contains(text, "Quit Job Decision | Needs governance review")

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "directive_queue":
            raise AssertionError("expected directive_queue JSON artifact")
        if structured["scoring_model"]["model"] != "directive-scoring-v1":
            raise AssertionError("expected directive-scoring-v1 model metadata")
        if not any(item["dimension"] == "urgency" for item in structured["scoring_model"]["dimensions"]):
            raise AssertionError("expected scoring dimensions in structured queue")
        if not any(item["dimension"] == "anxiety_reduction" for item in structured["scoring_model"]["dimensions"]):
            raise AssertionError("expected anxiety reduction scoring dimension")
        if structured["active_candidates"][0]["candidate"] != "Structured Health Walk":
            raise AssertionError("expected Structured Health Walk as first active candidate")
        if "scorecard" not in structured["active_candidates"][0]:
            raise AssertionError("expected active candidate scorecard")
        if structured["active_candidates"][0]["score_total"] <= 0:
            raise AssertionError("expected positive active candidate score")
        if not structured["active_candidates"][0]["scorecard"]["score_dimensions"]:
            raise AssertionError("expected score dimensions on active scorecard")
        if not any(
            item["dimension"] == "anxiety_reduction"
            for item in structured["active_candidates"][0]["scorecard"]["score_dimensions"]
        ):
            raise AssertionError("expected anxiety reduction on active candidate scorecard")
        if structured["next_directive"]["directive"] != "Structured Health Walk":
            raise AssertionError("expected structured next directive")
        if "scorecard" not in structured["next_directive"]:
            raise AssertionError("expected scorecard on next directive")
        if "target_behavior" not in structured["next_directive"]:
            raise AssertionError("expected target behavior in structured next directive")
        if not any(item["candidate"] == "Breakfast Anchor" for item in structured["active_candidates"]):
            raise AssertionError("expected Breakfast Anchor in active candidates")
        if not any(
            item["candidate"] == "Structured Health Walk"
            and item["target_behavior"] == "Create a movement action before sedentary inertia wins."
            for item in structured["active_candidates"]
        ):
            raise AssertionError("expected structured health candidate in active candidates")
        if not any(
            item["candidate"] == "Quit Job Decision"
            and item["reason_deferred"].startswith("Needs governance review")
            for item in structured["deferred"]
        ):
            raise AssertionError("expected Level 4 candidate deferred for governance")
        quit_job = next(item for item in structured["deferred"] if item["candidate"] == "Quit Job Decision")
        if quit_job["governance_status"] != "needs_formal_review":
            raise AssertionError("expected escalated governance status on deferred candidate")
        if "scorecard" not in quit_job or quit_job["score_total"] <= 0:
            raise AssertionError("expected scored governance-deferred candidate")

        synthesize_queue.main_with_args(
            [
                "--date",
                "2026-06-23",
                "--candidate",
                str(tie_file),
                "--available",
                "30",
                "--output",
                str(tie_output),
                "--json-output",
                str(tie_json_output),
                "--force",
            ]
        )
        tie_structured = json.loads(tie_json_output.read_text())
        first_tie = tie_structured["active_candidates"][0]
        second_tie = tie_structured["active_candidates"][1]
        if first_tie["candidate"] != "Small Ambiguous Task":
            raise AssertionError("expected smaller weak-evidence candidate to win tie-break")
        if first_tie["score_total"] != second_tie["score_total"]:
            raise AssertionError("expected tie fixture to have equal score totals")
        if "Evidence is weak" not in first_tie["selection_rationale"]:
            raise AssertionError("expected weak-evidence rationale on tied candidate")
        if tie_structured["next_directive"]["directive"] != "Small Ambiguous Task":
            raise AssertionError("expected tie-break winner as next directive")

    print("directive synthesis smoke tests passed.")


if __name__ == "__main__":
    main()
