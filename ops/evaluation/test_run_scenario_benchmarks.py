#!/usr/bin/env python3
"""Smoke tests for public-safe PEGO scenario benchmarks."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import run_scenario_benchmarks


def run_benchmark(root: Path) -> dict[str, object]:
    output = root / "benchmark.md"
    json_output = root / "benchmark.json"
    run_scenario_benchmarks.main_with_args(
        [
            "--date",
            "2026-07-04",
            "--output",
            str(output),
            "--json-output",
            str(json_output),
            "--force",
        ]
    )
    if "Failure modes preserved" not in output.read_text():
        raise AssertionError("markdown should preserve failure modes")
    return json.loads(json_output.read_text())


def test_synthetic_fixture_guard() -> None:
    with tempfile.TemporaryDirectory() as directory:
        private = Path(directory) / "private" / "speckit"
        private.mkdir(parents=True)
        try:
            run_scenario_benchmarks.main_with_args(["--fixture-dir", str(private)])
        except SystemExit as exc:
            if "private" not in str(exc).lower():
                raise AssertionError(exc)
        else:
            raise AssertionError("expected private fixture path rejection")


def test_baseline_comparison_and_public_export() -> None:
    with tempfile.TemporaryDirectory() as directory:
        data = run_benchmark(Path(directory))
        if data["artifact_type"] != "scenario_benchmark":
            raise AssertionError(data)
        if not data["public_safe"]:
            raise AssertionError(data["public_export_review"])
        if data["summary"]["scenario_count"] < 3:
            raise AssertionError(data["summary"])
        if data["summary"]["baseline_wins"] + data["summary"]["ties"] < 1:
            raise AssertionError("expected at least one preserved tie or baseline win")
        first = data["scenarios"][0]
        if not first["baseline_outputs"]:
            raise AssertionError("expected baseline outputs")
        if not first["scoring_criteria"]:
            raise AssertionError("expected scoring criteria")
        if first["result"]["pego_score_total"] <= first["result"]["best_baseline_score_total"]:
            raise AssertionError(first["result"])


def test_failure_modes_are_preserved() -> None:
    with tempfile.TemporaryDirectory() as directory:
        data = run_benchmark(Path(directory))
        failures = data["failure_modes"]
        if not failures:
            raise AssertionError("expected benchmark failure modes")
        if not all(item["preserved"] for item in failures):
            raise AssertionError(failures)
        systems = {item["system"] for item in failures}
        if "pego" not in systems:
            raise AssertionError("expected PEGO failure mode preservation")


def test_export_review_blocks_speckit_marker() -> None:
    scenario = run_scenario_benchmarks.built_in_scenarios()[0]
    polluted = run_scenario_benchmarks.Scenario(
        scenario_id=scenario.scenario_id,
        title="Synthetic case with Speckit leak",
        decision_frame=scenario.decision_frame,
        synthetic_context="This synthetic text mentions private/speckit and should fail.",
        priority_assumption=scenario.priority_assumption,
        recommendations=scenario.recommendations,
        baselines=scenario.baselines,
        scoring_criteria=scenario.scoring_criteria,
        expected_council_outcome=scenario.expected_council_outcome,
        known_pego_failure_modes=scenario.known_pego_failure_modes,
    )
    try:
        run_scenario_benchmarks.build_artifact([polluted], "2026-07-04", "synthetic")
    except SystemExit:
        pass
    else:
        raise AssertionError("expected public export guard to reject Speckit marker")


def main() -> None:
    test_synthetic_fixture_guard()
    test_baseline_comparison_and_public_export()
    test_failure_modes_are_preserved()
    test_export_review_blocks_speckit_marker()
    print("scenario benchmark smoke tests passed.")


if __name__ == "__main__":
    main()
