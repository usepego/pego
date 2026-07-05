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


ALTERNATIVE = {
    **RECOMMEND,
    "agent": "Health",
    "proposed_directive": "Take a 20 minute recovery walk",
    "expected_benefit": "Protects energy before the next work block.",
    "costs_and_tradeoffs": ["Defers desk work briefly."],
    "risks": ["time"],
    "required_handoffs": ["Health"],
    "review": {"review_date_or_success_criteria": "Review after energy check."},
}


INFO_REQUEST = {
    **RECOMMEND,
    "agent": "Governance",
    "recommendation_type": "request_more_information",
    "proposed_directive": "Ask whether protected time starts within the next hour",
    "relevant_facts": [],
    "assumptions": [{"statement": "Timing may be constrained", "certainty": "low"}],
    "evidence_quality": ["speculation"],
    "expected_benefit": "Prevents a protected-time collision.",
    "costs_and_tradeoffs": ["Adds one targeted question before action."],
    "risks": ["time"],
    "required_handoffs": ["Governance"],
}


HIGH_RISK = {
    **RECOMMEND,
    "agent": "Finance",
    "proposed_directive": "Change the synthetic allocation policy",
    "expected_benefit": "Could improve long-term synthetic returns.",
    "risks": ["financial"],
    "required_handoffs": ["Governance"],
}


VETO = {
    **RECOMMEND,
    "agent": "Governance",
    "proposed_directive": "Share a synthetic private summary externally",
    "expected_benefit": "Could speed up an external review.",
    "privacy_impact": "blocked",
    "vetoes": ["Synthetic veto: disclosure approval is missing."],
    "required_handoffs": ["Governance"],
}


def calibration_record(agent: str, score_delta: int, action: str, note: str) -> dict[str, object]:
    return {
        "artifact_type": "agent_calibration_record",
        "schema_version": 1,
        "date": "2026-06-23",
        "agent": agent,
        "source_reviews": ["synthetic-outcome-review"],
        "recommendation_usefulness": "adequate",
        "score_delta": score_delta,
        "calibration_action": action,
        "friction_prediction": "adequate",
        "evidence_quality": "adequate",
        "stress_impact": "preserved",
        "missed_risks": [],
        "cautions": ["Synthetic calibration caution."],
        "council_summary": "Synthetic calibration record for council weighting.",
        "future_weighting_note": note,
        "next_review": "Next synthetic review.",
    }


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in output:\n{text}")


def run_decision(
    root: Path,
    recommendations: list[dict[str, object]],
    name: str,
    calibrations: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    inputs = []
    for index, recommendation in enumerate(recommendations):
        path = root / f"{name}-{index}.json"
        path.write_text(json.dumps(recommendation))
        inputs.extend(["--recommendation", str(path)])
    for index, calibration in enumerate(calibrations or []):
        path = root / f"{name}-calibration-{index}.json"
        path.write_text(json.dumps(calibration))
        inputs.extend(["--agent-calibration", str(path)])

    output = root / f"{name}.md"
    json_output = root / f"{name}.json"
    synthesize_decision.main_with_args(
        [
            "--date",
            "2026-06-23",
            "--frame",
            "Choose next synthetic directive.",
            *inputs,
            "--priority-assumption",
            "Use only low-risk reversible synthetic work unless governance blocks adoption.",
            "--output",
            str(output),
            "--json-output",
            str(json_output),
            "--force",
        ]
    )
    return json.loads(json_output.read_text())


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
                "--priority-assumption",
                "Protect relationship constraints over optional venture work during protected time.",
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
        assert_contains(text, "Deliberation Summary")
        assert_contains(text, "Tradeoff Rationale")
        assert_contains(text, "Tradeoff Scorecard")
        assert_contains(text, "Deferrals")

        structured = json.loads(json_output.read_text())
        if structured["artifact_type"] != "council_decision":
            raise AssertionError("expected council_decision artifact")
        if structured["schema_version"] != 2:
            raise AssertionError("expected v2 council decision artifact")
        if structured["council_outcome"] != "revise":
            raise AssertionError("expected dissent to force revision")
        if "time" not in structured["key_risks"]:
            raise AssertionError("expected risk preservation")
        if structured["goal_reconciliation_status"] != "temporary_priority_assumption":
            raise AssertionError("expected explicit priority assumption")
        if "relationship constraints" not in structured["priority_assumption"]:
            raise AssertionError("expected priority assumption preservation")
        summary = structured["deliberation_summary"]
        for key in ["claims", "objections", "concessions", "evidence_gaps", "vetoes", "unresolved_dissent"]:
            if key not in summary:
                raise AssertionError(f"expected deliberation summary field: {key}")
        if not summary["claims"]:
            raise AssertionError("expected claims in deliberation summary")
        if "Protected time is too close" not in " ".join(summary["unresolved_dissent"]):
            raise AssertionError("expected unresolved dissent preservation")
        if structured["unresolved_dissent"] != summary["unresolved_dissent"]:
            raise AssertionError("expected top-level unresolved dissent mirror")
        if not structured["tradeoff_scorecard"]:
            raise AssertionError("expected tradeoff scorecard rows")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = run_decision(root, [RECOMMEND, ALTERNATIVE], "adopt-with-deferral-a")
        second = run_decision(root, [RECOMMEND, ALTERNATIVE], "adopt-with-deferral-b")

        if first["council_outcome"] != "adopt":
            raise AssertionError("expected low-risk recommendations to adopt")
        if "Health: deferred Take a 20 minute recovery walk" not in " ".join(first["deferrals"]):
            raise AssertionError("expected non-selected recommendation deferral")
        statuses = [row["selection_status"] for row in first["tradeoff_scorecard"]]
        if statuses != ["selected", "deferred"]:
            raise AssertionError(f"unexpected scorecard statuses: {statuses}")
        for field in ["deliberation_summary", "tradeoff_rationale", "tradeoff_scorecard", "deferrals"]:
            if first[field] != second[field]:
                raise AssertionError(f"expected deterministic {field}")

        calibrated = run_decision(
            root,
            [RECOMMEND, ALTERNATIVE],
            "adopt-with-calibration",
            calibrations=[
                calibration_record("Operations Agent", -2, "decrease_weight", "Reduce weight after friction."),
                calibration_record("Health Agent", 2, "increase_weight", "Increase weight after useful recovery prediction."),
            ],
        )
        if calibrated["proposed_directive"] != "Take a 20 minute recovery walk":
            raise AssertionError("expected calibration to select health recommendation")
        if not calibrated["agent_calibration_context"]:
            raise AssertionError("expected agent calibration context")
        health_row = next(row for row in calibrated["tradeoff_scorecard"] if row["agent"] == "Health")
        if health_row["selection_status"] != "selected":
            raise AssertionError("expected calibrated health row to be selected")
        if health_row["calibration_adjustment"] <= 0:
            raise AssertionError("expected positive health calibration adjustment")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        high_risk = run_decision(root, [HIGH_RISK], "high-risk")
        if high_risk["council_outcome"] != "escalate":
            raise AssertionError("expected high-risk recommendation to escalate")
        if high_risk["tradeoff_scorecard"][0]["selection_status"] != "escalated":
            raise AssertionError("expected high-risk scorecard status")

        information = run_decision(root, [INFO_REQUEST], "information")
        if information["council_outcome"] != "request_more_information":
            raise AssertionError("expected information request outcome")
        if "requested information before adoption" not in " ".join(information["evidence_gaps"]):
            raise AssertionError("expected information request evidence gap")

        veto = run_decision(root, [VETO], "veto")
        if veto["council_outcome"] != "block":
            raise AssertionError("expected veto to block adoption")
        if "disclosure approval is missing" not in " ".join(veto["vetoes"]):
            raise AssertionError("expected veto preservation")

    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "pego-private"
        private.mkdir()
        recommendation = private / "recommend.json"
        json_output = private / "council" / "decisions" / "council-decision.json"
        recommendation.write_text(json.dumps(RECOMMEND))

        synthesize_decision.main_with_args(
            [
                "--private-root",
                str(private),
                "--date",
                "2026-06-25",
                "--frame",
                "Choose next directive with private goal reconciliation.",
                "--recommendation",
                str(recommendation),
                "--json-output",
                str(json_output),
            ]
        )

        if not (private / "goals" / "goal-reconciliation.json").exists():
            raise AssertionError("expected council to build goal reconciliation")
        structured = json.loads(json_output.read_text())
        if structured["goal_reconciliation_status"] != "current_goal_reconciliation_supplied":
            raise AssertionError("expected council to use generated goal reconciliation")

    print("council decision smoke tests passed.")


if __name__ == "__main__":
    main()
