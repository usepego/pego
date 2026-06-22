#!/usr/bin/env python3
"""Run PEGO financial freedom scenarios from private JSON assumptions."""

from __future__ import annotations

import argparse
import json
import math
from datetime import date, timedelta
from pathlib import Path


DEFAULT_INPUT = Path("private/finance/scenarios.json")
DEFAULT_OUTPUT = Path("private/_local/finance/scenario-output.json")
DEFAULT_SUMMARY_OUTPUT = Path("private/finance/scenario-results.md")
REQUIRED_SCENARIOS = {"conservative", "base", "upside", "stress", "lifestyle_upgrade"}


def target_multiple(nominal_return: float, inflation: float, years: int) -> float:
    """Present-value multiple for one unit of annual spend over a finite horizon."""
    real_rate = nominal_return - inflation
    if abs(real_rate) < 1e-9:
        return float(years)
    return (1 - (1 + real_rate) ** (-years)) / real_rate


def future_value(
    principal: float,
    monthly_contribution: float,
    annual_return: float,
    months: int,
) -> float:
    monthly_return = annual_return / 12
    if months <= 0:
        return principal
    if abs(monthly_return) < 1e-12:
        return principal + monthly_contribution * months
    return (
        principal * (1 + monthly_return) ** months
        + monthly_contribution * (((1 + monthly_return) ** months - 1) / monthly_return)
    )


def months_to_target(
    principal: float,
    monthly_contribution: float,
    annual_return: float,
    target: float,
    max_months: int = 1200,
) -> int | None:
    if principal >= target:
        return 0
    for month in range(1, max_months + 1):
        if future_value(principal, monthly_contribution, annual_return, month) >= target:
            return month
    return None


def add_months_approx(start: date, months: int) -> date:
    return start + timedelta(days=round(months * 365.2425 / 12))


def run(config: dict) -> dict:
    as_of = date.fromisoformat(config["as_of"])
    position = config["current_position"]
    globals_ = config["global_assumptions"]
    current_age = int(globals_["current_age"])
    retirement_start_age = int(globals_.get("retirement_start_age", current_age))
    age_to_live = int(globals_["age_to_live"])
    years_to_fund = max(1, age_to_live - retirement_start_age)
    target_date = date.fromisoformat(globals_["target_date"])
    social_security_monthly = float(globals_.get("social_security_monthly_estimate", 0))

    liquid = float(position["liquid_savings"])
    total_savings = float(position["total_model_savings"])

    results = []
    for scenario in config["scenarios"]:
        monthly_burn = float(scenario["monthly_burn"])
        annual_extra_burn = float(scenario.get("annual_extra_burn", 0))
        annual_burn = monthly_burn * 12 + annual_extra_burn
        nominal_return = float(scenario["nominal_return"])
        inflation = float(scenario["inflation"])
        monthly_savings = float(scenario["monthly_savings"])
        include_ss = bool(scenario.get("include_social_security", False))

        multiple = target_multiple(nominal_return, inflation, years_to_fund)
        annual_ss_offset = social_security_monthly * 12 if include_ss else 0
        target = max(0, (annual_burn - annual_ss_offset) * multiple)
        target_without_ss = annual_burn * multiple
        liquid_runway_months = liquid / monthly_burn if monthly_burn else math.inf
        total_runway_months = total_savings / monthly_burn if monthly_burn else math.inf
        months = months_to_target(total_savings, monthly_savings, nominal_return, target)
        achieved_date = add_months_approx(as_of, months).isoformat() if months is not None else None

        target_date_months = max(0, round((target_date - as_of).days / (365.2425 / 12)))
        projected_at_target_date = future_value(
            total_savings, monthly_savings, nominal_return, target_date_months
        )

        result = (
            {
                "name": scenario["name"],
                "description": scenario.get("description", ""),
                "monthly_burn": round(monthly_burn, 2),
                "annual_burn": round(annual_burn, 2),
                "nominal_return": nominal_return,
                "inflation": inflation,
                "target_multiple": round(multiple, 2),
                "current_age": current_age,
                "retirement_start_age": retirement_start_age,
                "years_to_fund": years_to_fund,
                "target_number": round(target, 2),
                "target_number_without_social_security": round(target_without_ss, 2),
                "liquid_runway_months": round(liquid_runway_months, 1),
                "total_runway_months": round(total_runway_months, 1),
                "monthly_savings": round(monthly_savings, 2),
                "months_to_target": months,
                "target_achieved_date": achieved_date,
                "target_date": target_date.isoformat(),
                "projected_savings_at_target_date": round(projected_at_target_date, 2),
                "surplus_or_gap_at_target_date": round(projected_at_target_date - target, 2),
                "include_social_security": include_ss,
            }
        )
        result["risk_flags"] = risk_flags(
            result=result,
            target_date_months=target_date_months,
            emergency_months=float(globals_.get("emergency_runway_months", 12)),
        )
        results.append(result)

    return {
        "version": config["version"],
        "as_of": config["as_of"],
        "currency": config.get("currency", "USD"),
        "validation": validate_config(config),
        "summary": summarize_results(results),
        "results": results,
    }


def risk_flags(result: dict, target_date_months: int, emergency_months: float) -> list[str]:
    flags = []
    if result["months_to_target"] is None:
        flags.append("target_not_reached_within_model_window")
    elif result["months_to_target"] > target_date_months:
        flags.append("target_after_target_date")
    if result["surplus_or_gap_at_target_date"] < 0:
        flags.append("negative_gap_at_target_date")
    if result["liquid_runway_months"] < emergency_months:
        flags.append("liquid_runway_below_emergency_target")
    if result["include_social_security"]:
        flags.append("depends_on_social_security_offset")
    return flags


def validate_config(config: dict) -> dict:
    names = {scenario["name"] for scenario in config.get("scenarios", [])}
    missing = sorted(REQUIRED_SCENARIOS - names)
    present = sorted(names)
    return {
        "required_scenarios": sorted(REQUIRED_SCENARIOS),
        "present_scenarios": present,
        "missing_required_scenarios": missing,
        "status": "ok" if not missing else "missing_required_scenarios",
    }


def summarize_results(results: list[dict]) -> dict:
    if not results:
        return {
            "scenario_count": 0,
            "earliest_target_scenario": None,
            "latest_target_scenario": None,
            "highest_target_number_scenario": None,
            "negative_gap_scenarios": [],
            "flagged_scenarios": [],
        }

    reached = [result for result in results if result["months_to_target"] is not None]
    earliest = min(reached, key=lambda result: result["months_to_target"]) if reached else None
    latest = max(reached, key=lambda result: result["months_to_target"]) if reached else None
    highest = max(results, key=lambda result: result["target_number"])
    return {
        "scenario_count": len(results),
        "earliest_target_scenario": earliest["name"] if earliest else None,
        "latest_target_scenario": latest["name"] if latest else None,
        "highest_target_number_scenario": highest["name"],
        "negative_gap_scenarios": [
            result["name"] for result in results if result["surplus_or_gap_at_target_date"] < 0
        ],
        "flagged_scenarios": [
            {"name": result["name"], "risk_flags": result["risk_flags"]}
            for result in results
            if result["risk_flags"]
        ],
    }


def format_markdown_summary(output: dict) -> str:
    lines = [
        f"# Finance Scenario Results: {output['as_of']}",
        "",
        "Status: Local private output",
        "",
        "## Validation",
        "",
        f"- Status: {output['validation']['status']}",
        f"- Missing required scenarios: {', '.join(output['validation']['missing_required_scenarios']) or 'none'}",
        "",
        "## Summary",
        "",
        f"- Scenario count: {output['summary']['scenario_count']}",
        f"- Earliest target scenario: {output['summary']['earliest_target_scenario'] or 'none'}",
        f"- Latest target scenario: {output['summary']['latest_target_scenario'] or 'none'}",
        f"- Highest target number scenario: {output['summary']['highest_target_number_scenario'] or 'none'}",
        f"- Negative gap scenarios: {', '.join(output['summary']['negative_gap_scenarios']) or 'none'}",
        "",
        "## Scenario Risk Flags",
        "",
    ]
    for result in output["results"]:
        flags = ", ".join(result["risk_flags"]) or "none"
        lines.append(f"- {result['name']}: {flags}")
    lines.extend(
        [
            "",
            "## Privacy Note",
            "",
            "This file is protected private operating state and may contain private financial model outputs if expanded.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument("--print", action="store_true", help="print private scenario output to stdout")
    return parser


def main_with_args(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = json.loads(args.input.read_text())
    output = run(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    if args.write_summary:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        args.summary_output.write_text(format_markdown_summary(output))
    if args.print:
        print(json.dumps(output, indent=2))
    else:
        print(f"wrote: {args.output}")
        if args.write_summary:
            print(f"wrote: {args.summary_output}")


if __name__ == "__main__":
    main_with_args()
