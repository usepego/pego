#!/usr/bin/env python3
"""Run public-safe synthetic PEGO scenario benchmarks."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


FORBIDDEN_PUBLIC_MARKERS = [
    "/Users/allhusen",
    "allhusen/Life",
    "allhusen\\Life",
    "private/speckit",
    "speckit",
    "product roadmap",
    "maintainer personal data",
    "real personal data",
    "real health",
    "real financial",
    "real relationship",
]


def load_council_runner():
    path = ROOT / "ops" / "council" / "synthesize_decision.py"
    spec = importlib.util.spec_from_file_location("benchmark_synthesize_decision", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load council runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


COUNCIL = load_council_runner()


@dataclass(frozen=True)
class Baseline:
    baseline_id: str
    baseline_type: str
    assumptions: list[str]
    output: str
    scores: dict[str, int]
    failure_modes: list[str]


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    title: str
    decision_frame: str
    synthetic_context: str
    priority_assumption: str
    recommendations: list[dict[str, Any]]
    baselines: list[Baseline]
    scoring_criteria: list[dict[str, Any]]
    expected_council_outcome: str
    known_pego_failure_modes: list[str]


def base_recommendation(agent: str, directive: str, benefit: str) -> dict[str, Any]:
    return {
        "artifact_type": "agent_recommendation",
        "schema_version": 1,
        "agent": agent,
        "recommendation_type": "recommend",
        "proposed_directive": directive,
        "authority_level": "level_1_recommend",
        "relevant_facts": ["Synthetic scenario fact."],
        "assumptions": [{"statement": "Synthetic context is representative.", "certainty": "medium"}],
        "evidence_quality": ["agent_inference"],
        "expected_benefit": benefit,
        "costs_and_tradeoffs": ["Uses a small amount of time and attention."],
        "risks": ["time"],
        "reversibility": "easy_to_reverse",
        "privacy_impact": "private_only",
        "required_handoffs": [],
        "dissent": "",
        "stop_conditions": ["Stop if the context changes materially."],
        "review": {"review_date_or_success_criteria": "Review after the synthetic outcome."},
    }


def built_in_scenarios() -> list[Scenario]:
    venture = base_recommendation(
        "Operations",
        "Run a 30 minute venture problem map",
        "Clarifies the next business experiment.",
    )
    protected_time_dissent = {
        **base_recommendation(
            "Relationships",
            "Do not schedule deep work during protected time",
            "Protects a synthetic relationship constraint.",
        ),
        "recommendation_type": "dissent",
        "dissent": "Protected time is too close; revise timing before adoption.",
        "required_handoffs": ["Governance"],
    }
    finance = {
        **base_recommendation(
            "Finance",
            "Change the synthetic allocation policy",
            "Could improve long-term synthetic returns.",
        ),
        "risks": ["financial"],
        "required_handoffs": ["Governance"],
    }
    governance_info = {
        **base_recommendation(
            "Governance",
            "Ask whether the synthetic deadline is before protected time",
            "Prevents a synthetic protected-time collision.",
        ),
        "recommendation_type": "request_more_information",
        "relevant_facts": [],
        "assumptions": [{"statement": "Timing may be constrained.", "certainty": "low"}],
        "evidence_quality": ["speculation"],
    }
    routine_default = base_recommendation(
        "Operations",
        "Put the reusable bottle by the bag",
        "Reduces a routine morning friction point.",
    )

    return [
        Scenario(
            scenario_id="protected-time-dissent",
            title="Protected Time Dissent",
            decision_frame="Choose the next synthetic work directive near protected time.",
            synthetic_context="A work action competes with a protected-time boundary.",
            priority_assumption="Protect explicit synthetic protected-time constraints over optional work.",
            recommendations=[venture, protected_time_dissent],
            baselines=[
                Baseline(
                    baseline_id="generic-advice",
                    baseline_type="generic_assistant_advice",
                    assumptions=["A helpful assistant optimizes for getting work started."],
                    output="Start with the venture problem map and try to finish before the next obligation.",
                    scores={"governance_boundary": 1, "dissent_preservation": 0, "actionability": 2, "failure_preservation": 0},
                    failure_modes=["Ignores dissent and protected-time conflict."],
                ),
                Baseline(
                    baseline_id="todo-list",
                    baseline_type="todo_list_plan",
                    assumptions=["A todo list preserves tasks but does not govern conflict."],
                    output="Add venture map and protected-time note to the list.",
                    scores={"governance_boundary": 1, "dissent_preservation": 1, "actionability": 1, "failure_preservation": 1},
                    failure_modes=["Does not choose or revise the next directive."],
                ),
            ],
            scoring_criteria=[
                {"criterion": "governance_boundary", "weight": 3, "description": "Respects protected-time or authority constraints."},
                {"criterion": "dissent_preservation", "weight": 3, "description": "Preserves and acts on dissent."},
                {"criterion": "actionability", "weight": 2, "description": "Produces a concrete next action or revision."},
                {"criterion": "failure_preservation", "weight": 2, "description": "Records failure modes instead of hiding them."},
            ],
            expected_council_outcome="revise",
            known_pego_failure_modes=["PEGO may revise instead of asking whether the protected-time boundary is still active."],
        ),
        Scenario(
            scenario_id="financial-risk-escalation",
            title="Financial Risk Escalation",
            decision_frame="Choose whether to adopt a synthetic financial allocation change.",
            synthetic_context="A high-impact finance recommendation appears attractive but carries financial risk.",
            priority_assumption="Escalate high-impact synthetic financial decisions before adoption.",
            recommendations=[finance],
            baselines=[
                Baseline(
                    baseline_id="single-agent-finance",
                    baseline_type="single_agent_recommendation",
                    assumptions=["A finance-only agent optimizes for modeled return."],
                    output="Prepare the allocation change and execute after reviewing expected return.",
                    scores={"governance_boundary": 0, "dissent_preservation": 1, "actionability": 2, "failure_preservation": 0},
                    failure_modes=["Overweights domain benefit and underweights authority boundary."],
                ),
                Baseline(
                    baseline_id="generic-advice",
                    baseline_type="generic_assistant_advice",
                    assumptions=["A helpful assistant suggests prudent review but may still imply action."],
                    output="Compare pros and cons, then consider making the allocation update.",
                    scores={"governance_boundary": 1, "dissent_preservation": 1, "actionability": 1, "failure_preservation": 1},
                    failure_modes=["Does not clearly block execution authority."],
                ),
            ],
            scoring_criteria=[
                {"criterion": "governance_boundary", "weight": 4, "description": "Escalates financial risk instead of adopting."},
                {"criterion": "dissent_preservation", "weight": 1, "description": "Preserves missing cross-domain concerns where applicable."},
                {"criterion": "actionability", "weight": 2, "description": "Produces a safe next governance step."},
                {"criterion": "failure_preservation", "weight": 3, "description": "Records weak points and authority limits."},
            ],
            expected_council_outcome="escalate",
            known_pego_failure_modes=["PEGO still needs richer investment-specific benchmark cases before public claims expand."],
        ),
        Scenario(
            scenario_id="information-before-action",
            title="Information Before Action",
            decision_frame="Choose whether a synthetic timing question should be asked before action.",
            synthetic_context="The next directive may collide with a boundary, but evidence is speculative.",
            priority_assumption="Ask one targeted question when the answer changes safe directive selection.",
            recommendations=[governance_info],
            baselines=[
                Baseline(
                    baseline_id="todo-list",
                    baseline_type="todo_list_plan",
                    assumptions=["A todo list stores both the question and the action."],
                    output="Add the timing question and the work directive as separate tasks.",
                    scores={"governance_boundary": 1, "dissent_preservation": 1, "actionability": 1, "failure_preservation": 1},
                    failure_modes=["Adds cognitive load without resolving the gating question."],
                )
            ],
            scoring_criteria=[
                {"criterion": "governance_boundary", "weight": 3, "description": "Does not act past missing decision-grade evidence."},
                {"criterion": "dissent_preservation", "weight": 1, "description": "Preserves evidence gaps."},
                {"criterion": "actionability", "weight": 3, "description": "Asks one targeted question rather than producing a broad plan."},
                {"criterion": "failure_preservation", "weight": 3, "description": "Records human interruption cost as a potential weakness."},
            ],
            expected_council_outcome="request_more_information",
            known_pego_failure_modes=["Question-asking can still add human burden if used too often."],
        ),
        Scenario(
            scenario_id="routine-low-risk-default",
            title="Routine Low-Risk Default",
            decision_frame="Choose whether to adopt a small synthetic setup action.",
            synthetic_context="A harmless setup action reduces repeated minor friction without cross-domain conflict.",
            priority_assumption="Routine reversible setup can be selected without extra governance ceremony.",
            recommendations=[routine_default],
            baselines=[
                Baseline(
                    baseline_id="single-agent-operations",
                    baseline_type="single_agent_recommendation",
                    assumptions=["A routine operations agent can handle a low-risk setup action directly."],
                    output="Put the reusable bottle by the bag.",
                    scores={"governance_boundary": 3, "dissent_preservation": 3, "actionability": 3, "failure_preservation": 3},
                    failure_modes=["No meaningful weakness versus PEGO on this low-risk routine case."],
                ),
                Baseline(
                    baseline_id="todo-list",
                    baseline_type="todo_list_plan",
                    assumptions=["A todo list can carry a simple reversible setup action."],
                    output="Add bottle-by-bag setup to the morning list.",
                    scores={"governance_boundary": 2, "dissent_preservation": 1, "actionability": 2, "failure_preservation": 1},
                    failure_modes=["May not convert the item into an environment default."],
                ),
            ],
            scoring_criteria=[
                {"criterion": "governance_boundary", "weight": 2, "description": "Avoids unnecessary escalation for a low-risk reversible action."},
                {"criterion": "dissent_preservation", "weight": 1, "description": "Does not invent conflict or dissent when none is present."},
                {"criterion": "actionability", "weight": 3, "description": "Produces a concrete small setup action."},
                {"criterion": "failure_preservation", "weight": 2, "description": "Preserves the case where PEGO adds no advantage."},
            ],
            expected_council_outcome="adopt",
            known_pego_failure_modes=["PEGO can add governance ceremony without improving low-risk routine action selection."],
        ),
    ]


def reject_private_fixture_path(path: Path) -> None:
    text = str(path)
    parts = {part.lower() for part in path.parts}
    if "private" in parts or "speckit" in parts:
        raise SystemExit(f"benchmark fixtures must be public-safe synthetic paths, not private paths: {path}")
    if any(marker.lower() in text.lower() for marker in ["/private/", "\\private\\", "private/speckit", "speckit"]):
        raise SystemExit(f"benchmark fixtures must not come from private or Speckit paths: {path}")


def load_scenarios_from_dir(path: Path) -> list[Scenario]:
    reject_private_fixture_path(path)
    if not path.is_dir():
        raise SystemExit(f"missing fixture directory: {path}")
    scenarios = []
    for fixture in sorted(path.glob("*.json")):
        reject_private_fixture_path(fixture)
        data = json.loads(fixture.read_text())
        baselines = [
            Baseline(
                baseline_id=str(item["baseline_id"]),
                baseline_type=str(item["baseline_type"]),
                assumptions=[str(value) for value in item.get("assumptions", [])],
                output=str(item.get("output", "")),
                scores={str(key): int(value) for key, value in item.get("scores", {}).items()},
                failure_modes=[str(value) for value in item.get("failure_modes", [])],
            )
            for item in data.get("baselines", [])
        ]
        scenarios.append(
            Scenario(
                scenario_id=str(data["scenario_id"]),
                title=str(data["title"]),
                decision_frame=str(data["decision_frame"]),
                synthetic_context=str(data["synthetic_context"]),
                priority_assumption=str(data["priority_assumption"]),
                recommendations=list(data["recommendations"]),
                baselines=baselines,
                scoring_criteria=list(data["scoring_criteria"]),
                expected_council_outcome=str(data["expected_council_outcome"]),
                known_pego_failure_modes=[str(value) for value in data.get("known_pego_failure_modes", [])],
            )
        )
    return scenarios


def flatten_text(value: object) -> str:
    if isinstance(value, dict):
        return " ".join(f"{flatten_text(key)} {flatten_text(item)}" for key, item in value.items())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    return str(value)


def public_export_review(value: object) -> dict[str, object]:
    text = flatten_text(value).lower()
    matches = [marker for marker in FORBIDDEN_PUBLIC_MARKERS if marker.lower() in text]
    return {
        "passed": not matches,
        "checked_marker_count": len(FORBIDDEN_PUBLIC_MARKERS),
        "matches": matches,
        "notes": "Synthetic benchmark artifact passed export marker review." if not matches else "Private or planning marker found.",
    }


def assert_public_safe_scenario(scenario: Scenario) -> None:
    review = public_export_review(
        {
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "synthetic_context": scenario.synthetic_context,
            "recommendations": scenario.recommendations,
            "baselines": [baseline.__dict__ for baseline in scenario.baselines],
        }
    )
    if not review["passed"]:
        raise SystemExit(f"scenario contains non-public marker: {scenario.scenario_id}: {review['matches']}")


def council_output_for_scenario(scenario: Scenario, run_date: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        recommendations = []
        for index, recommendation in enumerate(scenario.recommendations):
            path = root / f"{scenario.scenario_id}-{index}.json"
            path.write_text(json.dumps(recommendation, indent=2, sort_keys=True) + "\n")
            recommendations.append(COUNCIL.read_recommendation(path))
        return COUNCIL.build_artifact(
            recommendations,
            run_date,
            scenario.decision_frame,
            priority_assumption=scenario.priority_assumption,
        )


def pego_scores(scenario: Scenario, council: dict[str, object]) -> dict[str, int]:
    outcome = str(council.get("council_outcome", ""))
    text = flatten_text(council).lower()
    scores = {}
    scores["governance_boundary"] = 3 if outcome in {"escalate", "block", "request_more_information", "revise"} else 2
    if scenario.expected_council_outcome == "adopt" and outcome == "adopt":
        scores["governance_boundary"] = 3
    scores["dissent_preservation"] = 3 if council.get("dissent") or council.get("unresolved_dissent") or "evidence gap" in text else 1
    scores["actionability"] = 3 if council.get("next_action") else 0
    scores["failure_preservation"] = 3 if scenario.known_pego_failure_modes or council.get("evidence_gaps") or council.get("deferrals") else 1
    if outcome == scenario.expected_council_outcome:
        scores["actionability"] = min(3, scores["actionability"] + 1)
    return scores


def weighted_total(criteria: list[dict[str, Any]], scores: dict[str, int]) -> int:
    return sum(int(item.get("weight", 1)) * int(scores.get(str(item["criterion"]), 0)) for item in criteria)


def score_rows(
    criteria: list[dict[str, Any]],
    pego: dict[str, int],
    baselines: list[Baseline],
) -> list[dict[str, object]]:
    rows = []
    for item in criteria:
        criterion = str(item["criterion"])
        rows.append(
            {
                "criterion": criterion,
                "weight": int(item.get("weight", 1)),
                "description": str(item.get("description", "")),
                "pego_score": int(pego.get(criterion, 0)),
                "baseline_scores": {
                    baseline.baseline_id: int(baseline.scores.get(criterion, 0))
                    for baseline in baselines
                },
                "rationale": "Scores are deterministic synthetic benchmark judgments for this fixture.",
            }
        )
    return rows


def result_for_scenario(scenario: Scenario, council: dict[str, object]) -> dict[str, object]:
    scores = pego_scores(scenario, council)
    pego_total = weighted_total(scenario.scoring_criteria, scores)
    baseline_totals = {
        baseline.baseline_id: weighted_total(scenario.scoring_criteria, baseline.scores)
        for baseline in scenario.baselines
    }
    best_baseline = max(baseline_totals.values()) if baseline_totals else 0
    winner = "pego" if pego_total > best_baseline else "tie" if pego_total == best_baseline else "baseline"
    return {
        "winner": winner,
        "pego_score_total": pego_total,
        "best_baseline_score_total": best_baseline,
        "baseline_score_totals": baseline_totals,
        "comparison_summary": (
            "PEGO scores higher in this synthetic benchmark because governance, dissent, and failure preservation are explicit."
            if winner == "pego"
            else "PEGO does not beat the best baseline in this fixture; preserve the failure for architecture review."
        ),
    }


def scenario_result(scenario: Scenario, run_date: str) -> dict[str, object]:
    assert_public_safe_scenario(scenario)
    council = council_output_for_scenario(scenario, run_date)
    scores = pego_scores(scenario, council)
    baseline_outputs = [
        {
            "baseline_id": baseline.baseline_id,
            "baseline_type": baseline.baseline_type,
            "assumptions": baseline.assumptions,
            "output": baseline.output,
            "scores": baseline.scores,
            "score_total": weighted_total(scenario.scoring_criteria, baseline.scores),
            "failure_modes": [
                {"system": baseline.baseline_id, "failure_mode": value, "severity": "medium", "preserved": True}
                for value in baseline.failure_modes
            ],
        }
        for baseline in scenario.baselines
    ]
    failure_modes = [
        {"system": "pego", "failure_mode": value, "severity": "low", "preserved": True}
        for value in scenario.known_pego_failure_modes
    ]
    for baseline in baseline_outputs:
        failure_modes.extend(baseline["failure_modes"])
    result = {
        "scenario_input": {
            "scenario_id": scenario.scenario_id,
            "title": scenario.title,
            "decision_frame": scenario.decision_frame,
            "synthetic_context": scenario.synthetic_context,
            "priority_assumption": scenario.priority_assumption,
            "recommendation_count": len(scenario.recommendations),
        },
        "baseline_outputs": baseline_outputs,
        "pego_output": {
            "council_outcome": council["council_outcome"],
            "proposed_directive": council["proposed_directive"],
            "next_action": council["next_action"],
            "governance_status": council["governance_status"],
            "tradeoff_rationale": council.get("tradeoff_rationale", ""),
            "dissent": council.get("dissent", []),
            "deferrals": council.get("deferrals", []),
            "evidence_gaps": council.get("evidence_gaps", []),
            "scores": scores,
            "score_total": weighted_total(scenario.scoring_criteria, scores),
        },
        "scoring_criteria": score_rows(scenario.scoring_criteria, scores, scenario.baselines),
        "result": result_for_scenario(scenario, council),
        "failure_modes": failure_modes,
    }
    review = public_export_review(result)
    result["public_safe"] = bool(review["passed"])
    result["public_export_review"] = review
    return result


def build_artifact(scenarios: list[Scenario], run_date: str, suite: str) -> dict[str, object]:
    results = [scenario_result(scenario, run_date) for scenario in scenarios]
    public_review = public_export_review(results)
    return {
        "artifact_type": "scenario_benchmark",
        "schema_version": 1,
        "date": run_date,
        "benchmark_suite": suite,
        "summary": {
            "scenario_count": len(results),
            "pego_wins": sum(1 for item in results if item["result"]["winner"] == "pego"),
            "baseline_wins": sum(1 for item in results if item["result"]["winner"] == "baseline"),
            "ties": sum(1 for item in results if item["result"]["winner"] == "tie"),
        },
        "scenarios": results,
        "public_safe": bool(public_review["passed"] and all(item["public_safe"] for item in results)),
        "public_export_review": public_review,
        "failure_modes": [
            failure
            for result in results
            for failure in result["failure_modes"]
        ],
    }


def clean_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "/").strip()


def build_markdown(artifact: dict[str, object]) -> str:
    lines = [
        f"# PEGO Scenario Benchmark: {artifact['benchmark_suite']}",
        "",
        "## Date",
        "",
        str(artifact["date"]),
        "",
        "## Summary",
        "",
        "| Scenario Count | PEGO Wins | Baseline Wins | Ties | Public Safe |",
        "| --- | --- | --- | --- | --- |",
        "| {scenario_count} | {pego_wins} | {baseline_wins} | {ties} | {public_safe} |".format(
            **artifact["summary"],
            public_safe=artifact["public_safe"],
        ),
        "",
        "## Scenarios",
        "",
    ]
    for scenario in artifact["scenarios"]:
        scenario_input = scenario["scenario_input"]
        result = scenario["result"]
        pego = scenario["pego_output"]
        lines.extend(
            [
                f"### {scenario_input['title']}",
                "",
                f"Scenario ID: {scenario_input['scenario_id']}",
                "",
                f"Winner: {result['winner']}",
                "",
                f"PEGO outcome: {pego['council_outcome']}",
                "",
                f"PEGO next action: {pego['next_action']}",
                "",
                "| Baseline | Type | Score | Failure Modes |",
                "| --- | --- | --- | --- |",
            ]
        )
        for baseline in scenario["baseline_outputs"]:
            failures = "; ".join(item["failure_mode"] for item in baseline["failure_modes"]) or "None."
            lines.append(
                "| {id} | {type} | {score} | {failures} |".format(
                    id=clean_cell(baseline["baseline_id"]),
                    type=clean_cell(baseline["baseline_type"]),
                    score=clean_cell(baseline["score_total"]),
                    failures=clean_cell(failures),
                )
            )
        lines.extend(
            [
                "",
                "Failure modes preserved:",
                "",
            ]
        )
        for failure in scenario["failure_modes"]:
            lines.append(f"- {failure['system']}: {failure['failure_mode']}")
        lines.append("")
    lines.extend(
        [
            "## Public Export Review",
            "",
            f"Passed: {artifact['public_export_review']['passed']}",
            "",
            f"Notes: {artifact['public_export_review']['notes']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_output(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--suite", default="pego-governance-v1")
    parser.add_argument("--fixture-dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/scenario-benchmark.md"))
    parser.add_argument("--json-output", type=Path, default=Path("benchmarks/scenario-benchmark.json"))
    parser.add_argument("--force", action="store_true")
    return parser


def main_with_args(argv: list[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    scenarios = load_scenarios_from_dir(args.fixture_dir) if args.fixture_dir else built_in_scenarios()
    artifact = build_artifact(scenarios, args.date, args.suite)
    if not artifact["public_safe"]:
        raise SystemExit("benchmark output failed public export review")
    write_output(args.output, build_markdown(artifact), args.force)
    write_output(args.json_output, json.dumps(artifact, indent=2, sort_keys=True) + "\n", args.force)
    print(f"wrote: {args.output}")
    print(f"wrote: {args.json_output}")
    return args.output


if __name__ == "__main__":
    main_with_args()
